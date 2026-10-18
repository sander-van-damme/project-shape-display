import csv
import importlib.util
import json
import queue
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path

SOFTWARE = Path(__file__).resolve().parents[1]
if str(SOFTWARE) not in sys.path:
    sys.path.insert(0, str(SOFTWARE))
from desktop.model import Results, calibration_factor, comparison_steps, load_profile, rpm_values, save_profile
from desktop.transport import CommandError, SerialLink, SimulatedLink, StopRequested
from desktop.worker import SessionWorker


def firmware(motors=1):
    spec = importlib.util.spec_from_file_location("desktop_test_firmware", SOFTWARE / "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.make_simulated_firmware(motor_count=motors)


def until(predicate, timeout=4):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return
        time.sleep(0.01)
    raise AssertionError("Condition timed out")


class FakeSerial:
    def __init__(self, *args, **kwargs):
        self.written = []
        self.input = bytearray()
        self.reply = True
        self.bad = False
        self.closed = False

    def write(self, packet):
        self.written.append(packet)
        if packet == b"!" or not self.reply:
            return len(packet)
        request = json.loads(packet)
        answer = {"id": request["id"], "ok": not self.bad, "result": {"alive": True}, "error": "invalid config"}
        self.input.extend(b'boot banner\n{"id":-1,"ok":true}\n' + json.dumps(answer).encode() + b"\n")
        return len(packet)

    def read(self, count):
        # Emulate arbitrary USB packet fragmentation.
        result = self.input[:7]
        del self.input[:7]
        if not result:
            time.sleep(0.001)
        return bytes(result)

    def close(self):
        self.closed = True


class DesktopModelTests(unittest.TestCase):
    def test_sweep_cartesian_values_and_mode_timing(self):
        self.assertEqual(list(rpm_values(5, 16, 5)), [5, 10, 15])
        self.assertEqual(list(rpm_values(10, 0, -5)), [10, 5, 0])
        with self.assertRaises(ValueError):
            list(rpm_values(1, 5, -1))
        steps = list(comparison_steps({"mode": "duration", "duration_s": 9, "decel": 50},
                                     [10, 20], [50, 100], ["spreadcycle", "stealthchop"], [8, 16], [5]))
        self.assertEqual(len(steps), 16)
        self.assertEqual(steps[-1]["config"]["tpowerdown"], 20)
        self.assertEqual(steps[-1]["move"]["duration_s"], 9)

    def test_sweep_does_not_eagerly_consume_rpm_range(self):
        def endless_rpms():
            yield 10
            raise AssertionError("RPM generator consumed beyond requested step")
        steps = comparison_steps({"mode": "duration"}, endless_rpms(), [100], ["spreadcycle"], [8], [5])
        self.assertEqual(next(steps)["move"]["rpm"], 10)

    def test_calibration_composes_ratio_and_has_no_fabricated_measurement(self):
        self.assertAlmostEqual(calibration_factor(1.1, 10, measured_rev=9), 0.99)
        self.assertAlmostEqual(calibration_factor(1, 10, measured_mm=27, lead_mm_per_rev=3), 0.9)
        for kwargs in ({}, {"measured_rev": 1, "measured_mm": 3}, {"measured_rev": "nan"}):
            with self.assertRaises(ValueError):
                calibration_factor(1, 10, **kwargs)

    def test_profile_results_roundtrip_provenance_and_csv(self):
        results = Results()
        record = results.begin("m2", {"rpm": 300}, {"vref_v": 0.8}, simulated=True)
        results.sample(record, {"motion": {"rpm_calculated": 299.9}, "diagnostics": {"version": 32}, "uart": {"errors": 0}})
        self.assertEqual(record["manual_measurements"], {})
        results.measure(record, {"rpm": 280, "motor_temperature_c": ""}, "tachometer", "licht geluid", "instrument_measurement")
        self.assertEqual(record["manual_measurements"]["rpm"]["provenance"], "instrument_measurement")
        self.assertNotIn("motor_temperature_c", record["manual_measurements"])
        with self.assertRaises(ValueError):
            results.measure(record, {"vref_v": 0.8}, "")
        results.finish(record, "failed", "UART timeout")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            save_profile(root / "p.json", {"move": {"rpm": 300}})
            self.assertEqual(load_profile(root / "p.json")["move"]["rpm"], 300)
            results.export_json(root / "r.json")
            results.export_csv(root / "r.csv")
            self.assertEqual(json.loads((root / "r.json").read_text())["records"][0]["source"], "simulated")
            with (root / "r.csv").open(encoding="utf-8-sig", newline="") as stream:
                row = next(csv.DictReader(stream))
            self.assertEqual(json.loads(row["manual_measurements"])["rpm"]["value"], 280)
            self.assertEqual(row["outcome"], "failed")


class DesktopSerialTests(unittest.TestCase):
    def setUp(self):
        self.serial = FakeSerial()
        self.event = threading.Event()
        self.link = SerialLink("unused", self.event, timeout=0.04, serial_factory=lambda *a, **k: self.serial)

    def test_fragmented_json_ignores_startup_noise_and_old_id(self):
        self.assertEqual(self.link.request({"cmd": "heartbeat"}), {"alive": True})
        self.assertEqual(self.link.stats["invalid_lines"], 1)
        self.assertTrue(self.serial.written[0].endswith(b"\n"))

    def test_invalid_command_keeps_link_and_config_usable(self):
        self.serial.bad = True
        with self.assertRaisesRegex(CommandError, "invalid config"):
            self.link.request({"cmd": "configure"})
        self.serial.bad = False
        self.assertTrue(self.link.request({"cmd": "heartbeat"})["alive"])

    def test_timeout_and_priority_stop_interrupt_read(self):
        self.serial.reply = False
        with self.assertRaises(OSError):
            self.link.request({"cmd": "status"})
        self.assertEqual(self.link.stats["timeouts"], 1)
        self.event.set()
        with self.assertRaises(StopRequested):
            self.link.request({"cmd": "status"})
        self.assertEqual(self.serial.written[-1], b"!")

    def test_nonfinite_and_oversized_never_written(self):
        with self.assertRaises(ValueError):
            self.link.request({"cmd": "speed", "rpm": float("nan")})
        with self.assertRaises(CommandError):
            self.link.request({"cmd": "hello", "padding": "x" * 9000})
        self.assertEqual(self.serial.written, [])


class DesktopIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.fw = firmware(2)
        self.worker = SessionWorker(link_factory=lambda port, event: SimulatedLink(self.fw))
        self.worker.start()
        self.worker.connect("SIMULATIE", reconnect=False).result(timeout=3)

    def tearDown(self):
        self.worker.shutdown()
        self.worker.join(timeout=3)
        self.assertFalse(self.worker.is_alive())

    def move(self, motor="m1", **overrides):
        values = dict(motor=motor, mode="duration", rpm=30, accel=100, decel=100, duration_s=0.3)
        values.update(overrides)
        return self.worker.submit("move", **values).result(timeout=3)

    def test_actual_firmware_roundtrip_two_motors_and_logging(self):
        self.worker.submit("configure", motor="m1", config={}).result(timeout=3)
        self.worker.submit("configure", motor="m2", config={}).result(timeout=3)
        self.move("m1")
        self.move("m2", rpm=-30)
        until(lambda: len(self.worker.results.records) == 2 and not self.worker.records)
        records = self.worker.results.records
        self.assertEqual({r["motor"] for r in records}, {"m1", "m2"})
        self.assertTrue(all(r["outcome"] == "completed" for r in records))
        self.assertTrue(all(r["source"] == "simulated" for r in records))
        self.assertLess(records[1]["calculated"]["position_rev_calculated"], 0)
        self.assertGreater(records[0]["uart"]["transactions"], 0)

    def test_continuous_heartbeat_live_reverse_and_emergency(self):
        self.move(mode="continuous")
        time.sleep(2.15)  # Exceeds firmware heartbeat timeout; background worker keeps session alive.
        self.worker.submit("speed", motor="m1", rpm=-30).result(timeout=3)
        until(lambda: self.worker.statuses.get("m1", {}).get("motion", {}).get("rpm_calculated", 0) < 0)
        self.assertIsNone(self.worker.statuses["m1"]["fault"])
        self.worker.stop_now()
        until(lambda: not self.worker.records)
        status = self.worker.submit("status", motor="m1").result(timeout=3)["motors"][0]
        self.assertEqual(status["motion"]["rpm_calculated"], 0)
        self.assertEqual(self.worker.results.records[0]["outcome"], "stopped")

    def test_sweep_failure_stops_before_more_demanding_step(self):
        steps = [{"config": {"irun": 5}, "move": {"mode": "duration", "rpm": 20, "accel": 100, "decel": 100, "duration_s": 0.1}},
                 {"config": {"irun": 99}, "move": {"mode": "duration", "rpm": 30, "accel": 100, "decel": 100, "duration_s": 0.1}},
                 {"config": {"irun": 10}, "move": {"mode": "duration", "rpm": 40, "accel": 100, "decel": 100, "duration_s": 0.1}}]
        self.worker.submit("_automation", motor="m1", steps=steps).result(timeout=3)
        until(lambda: self.worker.automation is None)
        self.assertEqual([r["outcome"] for r in self.worker.results.records], ["completed", "failed"])
        self.assertEqual(self.fw.motors["m1"].driver.config["irun"], 5)

    def test_uart_fault_aborts_sweep_without_later_step(self):
        step = {"config": {}, "move": {"mode": "duration", "rpm": 20, "accel": 100, "decel": 100, "duration_s": 5}}
        self.worker.submit("_automation", motor="m1", steps=[step, step]).result(timeout=3)
        self.fw.motors["m1"].driver.transport.fail = True
        until(lambda: self.worker.automation is None)
        self.assertEqual(len(self.worker.results.records), 1)
        self.assertEqual(self.worker.results.records[0]["outcome"], "failed")
        self.assertIn("UART", self.worker.results.records[0].get("error", ""))

    def test_disconnect_cancels_commands_waiting_for_reconnect(self):
        spare = SessionWorker()
        future = spare.submit("move", motor="m1", mode="continuous", rpm=100)
        spare._disconnect("USB lost")
        with self.assertRaises(StopRequested):
            future.result()
        self.assertTrue(spare.commands.empty())

    def test_both_chopper_modes_sweep_succeeds(self):
        steps = comparison_steps({"mode": "duration", "duration_s": 0.1, "decel": 100},
                                 [20], [100], ["spreadcycle", "stealthchop"], [8], [5])
        self.worker.submit("_automation", motor="m1", steps=steps).result(timeout=3)
        until(lambda: self.worker.automation is None)
        self.assertEqual([r["outcome"] for r in self.worker.results.records], ["completed", "completed"])

    def test_disconnect_reconnect_does_not_resume_motion(self):
        self.move(mode="continuous")
        self.worker.submit("_disconnect").result(timeout=3)
        self.worker.connect("SIMULATIE", reconnect=False).result(timeout=3)
        status = self.worker.submit("status", motor="m1").result(timeout=3)["motors"][0]
        self.assertEqual(status["state"], "idle")
        self.assertEqual(status["motion"]["rpm_calculated"], 0)
        self.assertEqual(self.worker.results.records[0]["outcome"], "disconnected")

    def test_invalid_user_command_preserves_motor_configuration(self):
        self.worker.submit("configure", motor="m1", config={"irun": 6}).result(timeout=3)
        with self.assertRaises(CommandError):
            self.worker.submit("configure", motor="m1", config={"microsteps": 3}).result(timeout=3)
        self.assertEqual(self.fw.motors["m1"].driver.config["irun"], 6)
        self.move()
        until(lambda: not self.worker.records)
        self.assertEqual(self.worker.results.records[-1]["outcome"], "completed")

    def test_stop_cancels_queued_future_commands(self):
        # Deterministic direct cancellation uses the same queue path as the worker STOP.
        spare = SessionWorker()
        future = spare.submit("move", motor="m1", mode="continuous", rpm=999)
        spare._handle_stop()
        with self.assertRaises(StopRequested):
            future.result()
        self.assertTrue(spare.commands.empty())

    def test_boundary_incomplete_never_advances_sweep(self):
        spare = SessionWorker()
        spare.link = SimulatedLink(firmware())
        record = spare.results.begin("m1", {}, {}, True)
        spare.records["m1"] = record
        spare.automation = {"motor": "m1", "steps": iter([]), "index": 1}
        # Exercise completion gate independently of movement duration or physical bounds.
        spare._request = lambda *a, **k: {"motors": [{"motor": "m1", "state": "idle", "motion": {"completed": False, "completion_reason": "boundary"}}]}
        spare._poll()
        self.assertIsNone(spare.automation)
        self.assertEqual(record["outcome"], "incomplete")


if __name__ == "__main__":
    unittest.main()
