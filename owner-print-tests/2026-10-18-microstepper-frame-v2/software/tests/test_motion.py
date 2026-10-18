"""Exercise the firmware planner itself; no physical movement is claimed."""
import importlib.util
import math
from pathlib import Path
import unittest


FIRMWARE = Path(__file__).resolve().parents[1] / "main.py"
spec = importlib.util.spec_from_file_location("motion_firmware", FIRMWARE)
fw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fw)


class PlannerTest(unittest.TestCase):
    def setUp(self):
        self.config = dict(fw.DEFAULT_MOTOR_CONFIG)
        self.planner = fw.MotionPlanner(self.config)
        self.now = 0.0

    def tick(self, dt=0.02, write_latency=0.0):
        self.now += dt
        desired = self.planner.update(self.now)
        value = fw.rpm_to_vactual(desired, self.config)
        actual = fw.vactual_to_rpm(value, self.config)
        self.now += write_latency
        self.planner.applied(actual, self.now)
        return actual

    def finish(self, limit=20000):
        samples = []
        for unused in range(limit):
            samples.append(self.tick())
            if not self.planner.active:
                return samples
        self.fail("planner did not finish")

    def test_integrates_written_sample_hold_not_requested_ramp(self):
        p = self.planner
        p.start("continuous", 100, 100, 100)
        p.applied(12, 0.1)
        # Desired updates are not evidence a UART write took place.
        p.update(0.2)
        p.update(0.4)
        p.applied(30, 0.5)
        s = p.status(1.0)
        self.assertAlmostEqual(s["position_rev_calculated"], 12 * .4 / 60 + 30 * .5 / 60)
        self.assertAlmostEqual(s["distance_rev_calculated"], s["position_rev_calculated"])
        self.assertEqual(s["rpm_calculated"], 30)

    def test_uart_latency_is_integrated_at_old_velocity(self):
        p = self.planner
        p.start("continuous", 120, 1000, 1000)
        p.applied(60, .1)
        proposed = p.update(.2)
        p.applied(proposed, .205)
        self.assertAlmostEqual(p.position_rev_calculated, .105)

    def test_trapezoid_acceleration_cruise_and_deceleration(self):
        p = self.planner
        p.start("revolutions", 120, 120, 240, revolutions=10)
        speeds = self.finish()
        quantum = p.quantum_rpm
        self.assertGreater(sum(abs(s - 120) < quantum for s in speeds), 40)
        for old, new in zip([0] + speeds, speeds):
            self.assertLessEqual(new - old, 120 * .02 + quantum + 1e-9)
            self.assertLessEqual(old - new, 240 * .02 + quantum + 1e-9)
        self.assertTrue(p.completed)
        self.assertLessEqual(abs(p.status(self.now)["residual_rev"]), p.endpoint_resolution_rev())

    def test_short_move_triangle_never_reaches_cruise(self):
        p = self.planner
        p.start("revolutions", 1000, 100, 100, revolutions=.01)
        speeds = self.finish()
        self.assertLess(max(speeds), math.sqrt(120 * 100 * .01))
        self.assertGreater(max(speeds), 0)
        self.assertLessEqual(abs(p.position_rev_calculated - .01), p.endpoint_resolution_rev())

    def test_low_acceleration_accumulates_below_velocity_quantum(self):
        p = self.planner
        p.start("revolutions", 2 * p.quantum_rpm, .01, .01, revolutions=.001)
        speeds = self.finish()
        self.assertGreater(sum(v != 0 for v in speeds), 0)
        self.assertLessEqual(abs(p.position_rev_calculated - .001), p.endpoint_resolution_rev())

    def test_tiny_distance_reports_resolution_and_residual(self):
        p = self.planner
        distance = p.endpoint_resolution_rev() / 10
        p.start("revolutions", 100, 100, 100, revolutions=distance)
        self.finish()
        self.assertTrue(p.completed)
        self.assertEqual(p.position_rev_calculated, 0)
        self.assertEqual(p.status(self.now)["residual_rev"], distance)

    def test_continuous_reversal_crosses_written_zero(self):
        p = self.planner
        p.start("continuous", 100, 100, 80)
        for unused in range(100):
            self.tick()
        p.set_speed(-160, accel=200, decel=80, now=self.now)
        speeds = [p.rpm_calculated]
        for unused in range(200):
            speeds.append(self.tick())
        first_negative = next(i for i, s in enumerate(speeds) if s < 0)
        self.assertEqual(speeds[first_negative - 1], 0)
        self.assertAlmostEqual(speeds[-1], -160, delta=p.quantum_rpm)
        self.assertTrue(p.active)
        self.assertGreater(p.distance_rev_calculated, abs(p.position_rev_calculated))

    def test_normal_stop_decelerates_and_waits_for_zero_write(self):
        p = self.planner
        p.start("continuous", 100, 1000, 50)
        for unused in range(20):
            self.tick()
        before = self.now
        p.stop(now=self.now)
        speeds = self.finish()
        self.assertGreater(self.now - before, 1.9)
        self.assertFalse(p.completed)
        self.assertEqual(p.completion_reason, "stopped")
        self.assertEqual(speeds[-1], 0)

    def test_no_false_completion_until_zero_is_applied(self):
        p = self.planner
        p.start("continuous", 10, 100, 100)
        p.applied(10, .1)
        p.stop(.2)
        self.assertEqual(p.update(.5), 0)
        self.assertTrue(p.active)
        self.assertEqual(p.update(.6), 0)
        self.assertTrue(p.active)
        p.applied(0, .61)
        p.update(.62)
        self.assertFalse(p.active)

    def test_duration_includes_acceleration_and_deceleration(self):
        p = self.planner
        p.start("duration", 120, 120, 120, duration_s=3)
        speeds = self.finish()
        self.assertLessEqual(self.now, 3.06)
        self.assertGreater(self.now, 2.98)
        self.assertGreater(max(speeds), 119)
        self.assertAlmostEqual(p.distance_rev_calculated, 4.0, delta=.09)

    def test_short_duration_triangular(self):
        p = self.planner
        p.start("duration", 120, 120, 120, duration_s=.4)
        speeds = self.finish()
        self.assertLess(max(speeds), 24.1)
        self.assertGreater(max(speeds), 0)
        self.assertLessEqual(self.now, .46)

    def test_cycles_return_to_absolute_origin_with_dwell(self):
        p = self.planner
        p.position_rev_calculated = 2.5
        p.start("cycles", -100, 200, 200, revolutions=.1, cycles=12, dwell_s=.04)
        self.finish()
        self.assertEqual(p.cycle, 12)
        self.assertTrue(p.completed)
        self.assertLessEqual(abs(p.position_rev_calculated - 2.5), p.endpoint_resolution_rev())
        self.assertAlmostEqual(p.distance_rev_calculated, 2.4, delta=.005)

    def test_stop_during_dwell_does_not_resume(self):
        p = self.planner
        p.start("cycles", 100, 200, 200, revolutions=.01, cycles=3, dwell_s=5)
        for unused in range(200):
            self.tick()
            if p.status(self.now)["phase"] == "dwell":
                break
        else:
            self.fail("no dwell observed")
        position = p.position_rev_calculated
        p.stop(self.now)
        self.finish()
        self.assertEqual(p.position_rev_calculated, position)
        self.assertFalse(p.completed)

    def test_emergency_stop_integrates_to_actual_disable_time(self):
        p = self.planner
        p.start("continuous", 60, 100, 100)
        p.applied(60, .1)
        p.emergency_stop(.6)
        self.assertAlmostEqual(p.position_rev_calculated, .5)
        self.assertEqual(p.rpm_calculated, 0)
        self.assertFalse(p.active)
        self.assertEqual(p.status(1)["elapsed_s"], .6)

    def test_invalid_command_preserves_active_run(self):
        p = self.planner
        p.start("continuous", 60, 100, 100)
        self.tick()
        previous = p.status(self.now)
        for bad in (float("inf"), float("nan"), "12", True):
            with self.assertRaises(ValueError):
                p.set_speed(bad, now=self.now)
        with self.assertRaises(ValueError):
            p.set_speed(90, accel=0, now=self.now)
        with self.assertRaises(ValueError):
            p.start("duration", 1, 2, 3, duration_s=1, now=self.now)
        self.assertEqual(previous, p.status(self.now))

    def test_start_validation_and_unbounded_useful_values(self):
        p = self.planner
        for kwargs in ({"rpm": 0}, {"accel": 0}, {"decel": -1}, {"dwell_s": -1}):
            values = dict(mode="continuous", rpm=1000, accel=100, decel=100)
            values.update(kwargs)
            with self.assertRaises(ValueError):
                p.start(**values)
            self.assertFalse(p.active)
        p.start("cycles", 10000, 1000, 1000, revolutions=1000000, cycles=10**12)
        self.assertEqual(p._cycles, 10**12)
        p.emergency_stop(0)
        p.start("duration", 10000, 1000, 1000, duration_s=10**12)
        self.assertTrue(p.active)

    def test_minimum_and_maximum_vactual_are_accepted(self):
        for value in (1, -1, (1 << 23) - 1, -(1 << 23)):
            p = fw.MotionPlanner(self.config)
            rpm = fw.vactual_to_rpm(value, self.config)
            p.start("continuous", rpm, 1e12, 1e12)
            self.assertEqual(p.rpm_requested, rpm)
        with self.assertRaises(ValueError):
            fw.MotionPlanner(self.config).start("continuous", self.planner.quantum_rpm / 10, 100, 100)

    def test_calibration_affects_integration_consistently(self):
        self.config["calibration_factor"] = 1.2
        self.planner = fw.MotionPlanner(self.config)
        self.planner.start("revolutions", 300, 1000, 1000, revolutions=.2)
        self.finish()
        self.assertLessEqual(abs(self.planner.position_rev_calculated - .2), self.planner.endpoint_resolution_rev())

    def test_timing_overrun_is_reported_not_hidden(self):
        p = self.planner
        p.start("continuous", 100, 100, 100)
        self.tick(.2)
        s = p.status(self.now)
        self.assertEqual(s["late_updates"], 1)
        self.assertEqual(s["max_update_gap_s"], .2)
        with self.assertRaises(ValueError):
            p.update(.1)

    def test_stopping_reserve_includes_sampling_and_quantization(self):
        p = self.planner
        p.start("continuous", 120, 1000, 240)
        p.applied(120, .1)
        self.assertGreater(p.stopping_distance_rev(), 120**2 / (120 * 240))
        self.assertGreater(p.stopping_distance_rev(reaction_s=.1), p.stopping_distance_rev())

    def test_pin_bound_clamps_large_acceleration_before_first_write(self):
        p = self.planner
        p.start("continuous", 100000, 1e9, 1000)
        bounds = (-.01, .01)
        for unused in range(1000):
            self.now += .02
            desired = p.update(self.now, bounds=bounds)
            actual = fw.vactual_to_rpm(fw.rpm_to_vactual(desired, self.config), self.config)
            p.applied(actual, self.now)
            self.assertGreaterEqual(p.position_rev_calculated, bounds[0])
            self.assertLessEqual(p.position_rev_calculated, bounds[1])
            if not p.active:
                break
        self.assertFalse(p.active)
        self.assertEqual(p.completion_reason, "boundary")
        self.assertFalse(p.completed)

    def test_repeated_stop_requests_do_not_prevent_deceleration(self):
        p = self.planner
        p.start("continuous", 60, 1000, 100)
        for unused in range(10):
            self.tick()
        for unused in range(100):
            p.stop(self.now)
            self.tick()
            if not p.active:
                break
        self.assertFalse(p.active)


if __name__ == "__main__":
    unittest.main()
