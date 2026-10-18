"""Behavioural tests of the real controller with simulated TMC2208 channels.

These tests establish software behavior only: there is no motor feedback and
no Pico, USB CDC, UART wire, or physical driver in this test process.
"""
import importlib.util
import json
from pathlib import Path
import unittest


SPEC = importlib.util.spec_from_file_location(
    "e302_integration_firmware", Path(__file__).resolve().parents[1] / "main.py"
)
fw = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fw)


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


class ControllerIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
        self.firmware = fw.make_simulated_firmware(clock=self.clock, motor_count=2)
        self.sequence = 0
        # Long driver configuration is performed before simultaneous movement;
        # subsequent starts use the bounded preflight/health path.
        self.okay("configure", motor="m1", config={})
        self.okay("configure", motor="m2", config={})

    def command(self, cmd, **fields):
        self.sequence += 1
        request = dict(fields, cmd=cmd, id=self.sequence)
        # Exercise JSON's data types and require serializable replies.
        result = self.firmware.handle(json.loads(json.dumps(request)))
        json.dumps(result, allow_nan=False)
        self.assertEqual(result["id"], self.sequence)
        return result

    def okay(self, cmd, **fields):
        response = self.command(cmd, **fields)
        self.assertTrue(response["ok"], response)
        return response["result"]

    def rejected(self, cmd, **fields):
        response = self.command(cmd, **fields)
        self.assertFalse(response["ok"], response)
        self.assertTrue(response["error"])
        return response

    def status(self, motor="m1"):
        result = self.okay("status", motor=motor)
        self.assertEqual(len(result["motors"]), 1)
        return result["motors"][0]

    def advance(self, seconds, heartbeat=True, step=0.01):
        until = self.clock.now + seconds
        next_heartbeat = self.clock.now
        while self.clock.now < until - 1e-10:
            self.clock.now = min(until, self.clock.now + step)
            if heartbeat and self.clock.now >= next_heartbeat:
                self.okay("heartbeat")
                next_heartbeat = self.clock.now + 0.4
            self.firmware.tick(self.clock.now)

    def start(self, motor="m1", **changes):
        fields = dict(motor=motor, mode="continuous", rpm=60,
                      accel=120, decel=120)
        fields.update(changes)
        return self.okay("move", **fields)

    def pin(self, motor="m1", **changes):
        settings = dict(mode="pin", min_mm=0, max_mm=12,
                        lead_mm_per_rev=3, position_mm=6)
        settings.update(changes)
        return self.okay("mechanics", motor=motor, settings=settings)

    def test_simulator_debug_history_is_bounded_without_losing_write_counts(self):
        motor = self.firmware.motors["m1"]
        motor.driver.configure()
        before = motor.driver.stats["writes"]
        for velocity in range(1, 1025):
            motor.driver.set_velocity(velocity)
        self.assertEqual(motor.driver.stats["writes"] - before, 1024)
        self.assertEqual(len(motor.driver.transport.writes), 128)
        self.assertEqual(motor.driver.transport.writes[-1], (0x22, 1024))
        motor.driver.check_health()

    def test_hello_exposes_schema_profiles_and_motor_selection(self):
        hello = self.okay("hello")
        self.assertEqual(hello["protocol"], 1)
        self.assertEqual(hello["motors"], ["m1", "m2"])
        self.assertTrue(hello["profiles"])
        self.assertTrue(hello["config_schema"])

    def test_configuration_validation_is_transactional(self):
        self.okay("configure", motor="m1", config={"irun": 7})
        original = self.status()["config"]
        for invalid in ({"irun": 32}, {"ihold": -1}, {"microsteps": 3},
                        {"full_steps_per_rev": 0}, {"not_a_setting": 1},
                        {"irun": 8, "microsteps": 3}):
            with self.subTest(invalid=invalid):
                self.rejected("configure", motor="m1", config=invalid)
                self.assertEqual(self.status()["config"], original)

    def test_bad_commands_during_motion_preserve_motion_and_configuration(self):
        self.start()
        self.advance(0.3)
        original = self.status()["config"]
        for command, fields in (
                ("unknown", {}), ("configure", {"config": {"irun": 8}}),
                ("speed", {"rpm": "fast"}),
                ("move", {"mode": "impossible", "rpm": 100}),
                ("reference", {"position_mm": 1})):
            with self.subTest(command=command):
                self.rejected(command, motor="m1", **fields)
                current = self.status()
                self.assertEqual(current["state"], "running")
                self.assertIsNone(current["fault"])
                self.assertEqual(current["config"], original)

    def test_unknown_motor_never_routes_to_another_controller(self):
        self.rejected("move", motor="missing", mode="continuous", rpm=60,
                      accel=120, decel=120)
        self.assertEqual(self.status("m1")["state"], "idle")
        self.assertEqual(self.status("m2")["state"], "idle")

    def test_nonfinite_motion_inputs_are_rejected_without_mutation(self):
        for key, value in (("rpm", float("nan")), ("rpm", float("inf")),
                           ("accel", 0), ("decel", -1)):
            fields = dict(motor="m1", mode="continuous", rpm=60,
                          accel=120, decel=120)
            fields[key] = value
            self.rejected("move", **fields)
            self.assertEqual(self.status()["state"], "idle")

    def test_speeds_above_old_120_rpm_limit_and_negative_direction(self):
        self.start(rpm=600, accel=3000, decel=3000)
        self.advance(0.4)
        self.assertGreater(self.status()["motion"]["rpm_calculated"], 590)
        self.okay("speed", motor="m1", rpm=-600)
        samples = []
        for _ in range(60):
            self.advance(0.01)
            samples.append(self.status()["motion"]["rpm_calculated"])
        self.assertLess(samples[-1], -590)
        # Firmware writes at 20 ms, so adjacent 10 ms observations can differ
        # by up to 60 RPM at 3000 RPM/s, plus register quantization.
        self.assertLess(max(abs(b - a) for a, b in zip(samples, samples[1:])), 65)

    def test_normal_stop_decelerates_to_idle(self):
        self.start()
        self.advance(0.6)
        self.okay("stop", motor="m1")
        self.advance(0.1)
        midway = self.status()
        self.assertGreater(midway["motion"]["rpm_calculated"], 0)
        self.assertLess(midway["motion"]["rpm_calculated"], 60)
        self.advance(0.6)
        stopped = self.status()
        self.assertEqual(stopped["state"], "idle")
        self.assertEqual(stopped["motion"]["rpm_calculated"], 0)

    def test_heartbeat_loss_stops_latches_and_does_not_resume(self):
        self.start()
        self.advance(0.4)
        self.advance(2.1, heartbeat=False)
        stopped = self.status()
        self.assertEqual(stopped["state"], "fault")
        self.assertIn("heartbeat", stopped["fault"].lower())
        self.assertEqual(stopped["motion"]["rpm_calculated"], 0)
        self.okay("heartbeat")
        self.advance(1)
        self.assertEqual(self.status()["state"], "fault")
        self.rejected("move", motor="m1", mode="continuous", rpm=60,
                      accel=120, decel=120)
        self.okay("clear_fault", motor="m1")
        self.assertEqual(self.status()["state"], "idle")
        self.advance(1)
        self.assertEqual(self.status()["motion"]["rpm_calculated"], 0)

    def test_pin_requires_explicit_mechanics_and_reference(self):
        for settings in ({"mode": "pin"},
                         {"mode": "pin", "min_mm": 0, "max_mm": 50},
                         {"mode": "pin", "min_mm": 5, "max_mm": 5,
                          "lead_mm_per_rev": 3, "position_mm": 5}):
            self.rejected("mechanics", motor="m1", settings=settings)
        self.pin()
        self.rejected("reference", motor="m1", position_mm=13)
        self.okay("reference", motor="m1", position_mm=6)
        self.start(mode="revolutions", revolutions=0.5, rpm=30)
        self.advance(3)
        self.assertEqual(self.status()["state"], "idle")

    def test_pin_rejects_move_beyond_explicit_stroke(self):
        self.pin()
        self.rejected("move", motor="m1", mode="revolutions", rpm=60,
                      accel=120, decel=120, revolutions=3)
        self.assertEqual(self.status()["state"], "idle")

    def test_nonkinematic_configuration_preserves_calculated_pin_reference(self):
        self.pin()
        self.start(mode="revolutions", revolutions=0.5, rpm=30)
        self.advance(3)
        before = self.status()["mechanics"]["position_mm_calculated"]
        self.assertGreater(before, 7)
        self.okay("configure", motor="m1", config={"irun": 6})
        after = self.status()["mechanics"]["position_mm_calculated"]
        self.assertAlmostEqual(after, before, places=6)

    def test_kinematic_configuration_invalidates_pin_reference(self):
        self.pin()
        self.okay("configure", motor="m1", config={"full_steps_per_rev": 40})
        self.assertIsNone(self.status()["mechanics"]["position_mm_calculated"])
        self.rejected("move", motor="m1", mode="revolutions", rpm=30,
                      accel=120, decel=120, revolutions=0.5)

    def test_pin_continuous_motion_stops_before_bound(self):
        self.pin(position_mm=6)
        self.start(rpm=60)
        self.advance(8)
        status = self.status()
        self.assertNotEqual(status["state"], "running")
        distance = status["motion"]["position_rev_calculated"] * 3
        self.assertLessEqual(distance, 6 + 0.001)

    def test_pin_rejects_realtime_deceleration_that_cannot_fit_remaining_stroke(self):
        self.pin()
        self.start(rpm=60)
        self.advance(0.6)
        self.rejected("speed", motor="m1", rpm=60, decel=0.01)
        status = self.status()
        self.assertEqual(status["state"], "running")
        self.assertEqual(status["motion"]["decel_rpm_s"], 120)
        self.advance(8)
        status = self.status()
        self.assertEqual(status["state"], "idle")
        self.assertLessEqual(status["mechanics"]["position_mm_calculated"], 12)

    def test_pin_reference_invalidated_on_emergency_stop(self):
        self.pin()
        self.start(mode="revolutions", revolutions=0.5, rpm=30)
        self.advance(0.1)
        self.okay("stop", motor="m1", emergency=True)
        self.rejected("move", motor="m1", mode="revolutions", rpm=30,
                      accel=120, decel=120, revolutions=0.5)

    def test_driver_communication_failure_stops_and_latches(self):
        self.start()
        self.advance(0.2)
        transport = self.firmware.motors["m1"].driver.transport
        transport.fail = True
        self.advance(1.1)
        stopped = self.status()
        self.assertEqual(stopped["state"], "fault")
        self.assertEqual(stopped["motion"]["rpm_calculated"], 0)
        self.rejected("clear_fault", motor="m1")
        transport.fail = False
        self.advance(0.2)
        self.assertEqual(self.status()["state"], "fault")
        self.okay("clear_fault", motor="m1")
        self.assertEqual(self.status()["state"], "idle")

    def test_driver_fault_bits_fail_stop(self):
        self.start()
        self.advance(0.2)
        # DRV_STATUS.ot, TMC2208 data sheet 0x6F bit 1.
        self.firmware.motors["m1"].driver.transport.registers[0x6F] |= 1 << 1
        self.advance(1.1)
        self.assertEqual(self.status()["state"], "fault")

    def test_automatic_driver_check_before_move(self):
        self.firmware.motors["m1"].driver.transport.fail = True
        self.rejected("move", motor="m1", mode="continuous", rpm=60,
                      accel=120, decel=120)
        self.assertNotEqual(self.status()["state"], "running")

    def test_separate_channels_and_independent_motor_stop(self):
        first = self.firmware.motors["m1"].driver.transport
        second = self.firmware.motors["m2"].driver.transport
        self.assertIsNot(first, second)
        self.assertIsNot(first.registers, second.registers)
        self.start("m1", rpm=60)
        self.start("m2", rpm=-30)
        self.advance(0.6)
        self.assertGreater(self.status("m1")["motion"]["rpm_calculated"], 0)
        self.assertLess(self.status("m2")["motion"]["rpm_calculated"], 0)
        self.okay("stop", motor="m1")
        self.advance(0.6)
        self.assertEqual(self.status("m1")["state"], "idle")
        self.assertEqual(self.status("m2")["state"], "running")

    def test_emergency_stop_reaches_all_motors(self):
        self.start("m1")
        self.start("m2", rpm=-30)
        self.advance(0.2)
        self.firmware.emergency_stop()
        for motor in ("m1", "m2"):
            status = self.status(motor)
            self.assertNotEqual(status["state"], "running")
            self.assertEqual(status["motion"]["rpm_calculated"], 0)

    def test_cycles_finish_without_accumulating_requested_displacement(self):
        self.start(mode="cycles", rpm=60, revolutions=0.5,
                   cycles=3, dwell_s=0.02)
        self.advance(15)
        status = self.status()
        self.assertEqual(status["state"], "idle")
        self.assertTrue(status["motion"]["completed"])
        self.assertLess(abs(status["motion"]["position_rev_calculated"]), 0.03)
        self.assertAlmostEqual(status["motion"]["distance_rev_calculated"], 3,
                               delta=0.1)

    def test_large_valid_duration_and_cycle_count_have_no_artificial_caps(self):
        for fields in ({"mode": "duration", "duration_s": 1000000},
                       {"mode": "cycles", "cycles": 1000000,
                        "revolutions": 1000000}):
            self.start(**fields)
            self.firmware.emergency_stop()
            # STOP may latch a fault, but never schedules automatic restart.
            status = self.status()
            if status["fault"]:
                self.okay("clear_fault", motor="m1")

    def test_fragmented_json_multiple_messages_and_correlated_replies(self):
        self.assertEqual(self.firmware.feed(b'{"id":31,"cmd":"hel'), [])
        replies = self.firmware.feed(b'lo"}\n{"id":32,"cmd":"heartbeat"}\r\n')
        self.assertEqual([r["id"] for r in replies], [31, 32])
        self.assertTrue(all(r["ok"] for r in replies))

    def test_supplied_invalid_request_ids_never_execute(self):
        for invalid_id in (True, "1", [], {}, 1.5):
            result = self.firmware.handle({"id": invalid_id, "cmd": "move",
                "motor": "m1", "mode": "continuous", "rpm": 60,
                "accel": 120, "decel": 120})
            self.assertFalse(result["ok"])
            self.assertEqual(self.status()["state"], "idle")

    def test_holding_motor_is_disabled_on_heartbeat_loss(self):
        self.okay("configure", motor="m1", config={"hold_on_stop": True})
        self.start(mode="duration", duration_s=0.5)
        self.advance(1)
        self.assertEqual(self.status()["state"], "holding")
        self.advance(2.2, heartbeat=False)
        self.assertEqual(self.status()["state"], "fault")
        self.assertFalse(self.firmware.motors["m1"].driver.enabled)

    def test_stealthchop_warmup_can_be_stopped_without_later_restart(self):
        self.okay("configure", motor="m1",
                  config={"chopper": "stealthchop", "tpowerdown": 20})
        self.start()
        self.assertEqual(self.status()["state"], "warming")
        self.okay("stop", motor="m1")
        self.advance(0.5)
        self.assertEqual(self.status()["state"], "idle")
        self.assertFalse(self.firmware.motors["m1"].driver.enabled)

    def test_stealthchop_warmup_enters_motion_and_completes(self):
        self.okay("configure", motor="m1",
                  config={"chopper": "stealthchop", "tpowerdown": 20})
        self.start(mode="duration", duration_s=0.8)
        self.assertEqual(self.status()["state"], "warming")
        self.advance(0.4)
        self.assertEqual(self.status()["state"], "running")
        self.assertGreater(self.status()["motion"]["rpm_calculated"], 0)
        self.advance(1)
        self.assertEqual(self.status()["state"], "idle")
        self.assertTrue(self.status()["motion"]["completed"])

    def test_multiple_channels_reject_shared_wire_and_state_machine(self):
        first = {"id": "m1", "transport": "pio", "pin": 4,
                 "sm_id": 0, "enable_pin": 6}
        second = {"id": "m2", "transport": "pio", "pin": 8,
                  "sm_id": 2, "enable_pin": 9}
        fw.validate_channels([first, second])
        for changed in ({"pin": 4}, {"sm_id": 0}, {"enable_pin": 4},
                        {"id": "m1"}, {"pin": 23}):
            invalid = dict(second, **changed)
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                fw.validate_channels([first, invalid])

    def test_slow_other_motor_operations_rejected_without_disturbing_motion(self):
        self.start()
        self.advance(0.3)
        for command, fields in (("configure", {"config": {"irun": 6}}),
                                ("diagnose", {}), ("clear_fault", {})):
            with self.subTest(command=command):
                self.rejected(command, motor="m2", **fields)
                self.assertEqual(self.status("m1")["state"], "running")
                self.assertIsNone(self.status("m1")["fault"])

    def test_unconfigured_second_motor_start_requires_idle_configuration(self):
        self.firmware = fw.make_simulated_firmware(clock=self.clock, motor_count=2)
        self.start("m1")
        self.advance(0.3)
        self.rejected("move", motor="m2", mode="continuous", rpm=30,
                      accel=120, decel=120)
        self.assertEqual(self.status("m1")["state"], "running")
        self.assertEqual(self.status("m2")["state"], "idle")

    def test_uart_latency_uses_fresh_motor_times_and_one_health_check_per_pass(self):
        self.pin()
        for motor in self.firmware.motors.values():
            original = motor.driver.transport.exchange

            def delayed_exchange(packet, reply_length=0, original=original):
                self.clock.now += 0.0015 if reply_length else 0.0008
                return original(packet, reply_length)

            motor.driver.transport.exchange = delayed_exchange
        self.start("m1", rpm=120, accel=240, decel=240)
        self.start("m2", rpm=-240, accel=480, decel=480)
        endpoint = self.clock.now + 5
        heartbeat_at = self.clock.now
        health_passes = 0
        while self.clock.now < endpoint:
            self.clock.now += 0.005
            if self.clock.now >= heartbeat_at:
                self.okay("heartbeat")
                heartbeat_at = self.clock.now + 0.4
            before = [m.last_health for m in self.firmware.motors.values()]
            # Exercise actual run() behavior: no injected fixed tick timestamp.
            self.firmware.tick()
            after = [m.last_health for m in self.firmware.motors.values()]
            changed = sum(a != b for a, b in zip(before, after))
            self.assertLessEqual(changed, 1)
            health_passes += changed
            for motor in ("m1", "m2"):
                self.assertIsNone(self.status(motor)["fault"])
        self.assertGreater(health_passes, 5)
        self.assertEqual(self.status("m1")["state"], "idle")
        self.assertLessEqual(self.status("m1")["mechanics"]["position_mm_calculated"], 12)
        self.assertEqual(self.status("m2")["state"], "running")

    def test_malformed_protocol_input_preserves_active_motion(self):
        self.start()
        self.advance(0.3)
        for malformed in (b'not-json\n', b'[]\n', b'null\n', b'\xff\n'):
            replies = self.firmware.feed(malformed)
            self.assertEqual(len(replies), 1)
            self.assertFalse(replies[0]["ok"])
            self.assertEqual(self.status()["state"], "running")

    def test_oversized_protocol_line_recovers_at_next_newline(self):
        replies = self.firmware.feed(b'x' * (fw.MAX_LINE_BYTES + 100) + b'\n')
        self.assertEqual(len(replies), 1)
        self.assertFalse(replies[0]["ok"])
        replies = self.firmware.feed(b'{"id":33,"cmd":"hello"}\n')
        self.assertEqual(replies[0]["id"], 33)
        self.assertTrue(replies[0]["ok"])

    def test_emergency_byte_bypasses_partial_or_oversized_lines(self):
        for partial in (b'{"id":34,"cmd":"', b'x' * (fw.MAX_LINE_BYTES + 1)):
            self.start("m1")
            self.start("m2")
            self.advance(0.3)
            self.assertEqual(self.firmware.feed(partial), [])
            self.firmware.feed(b'!')
            for motor in ("m1", "m2"):
                self.assertNotEqual(self.status(motor)["state"], "running")
                self.assertEqual(self.status(motor)["motion"]["rpm_calculated"], 0)
            recovered = self.firmware.feed(b'{"id":35,"cmd":"hello"}\n')
            self.assertTrue(recovered[0]["ok"])


if __name__ == "__main__":
    unittest.main()
