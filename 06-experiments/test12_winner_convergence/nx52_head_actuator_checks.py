"""Regression + honesty gates for the DND-52 head-actuator / drive-topology screen.

Run: python nx52_head_actuator_checks.py
Standard library only.
"""
from __future__ import annotations

import unittest

import nx52_head_actuator as nx


class HeadActuatorChecks(unittest.TestCase):
    def test_s5_break_even_matches_dnd49(self):
        # The whole pivot is measured against the same $1.86 bar DND-49 used.
        self.assertAlmostEqual(nx.S5_MOTOR_BREAK_EVEN, 1.8587, places=3)

    def test_s5_reference_reproduces_the_refuted_cost(self):
        ref = nx.s5_reference()
        self.assertAlmostEqual(ref["matched_delivered_usd"], 1366.87, places=2)
        self.assertGreater(ref["matched_delivered_usd"], nx.CEILING)
        self.assertLess(ref["untraced_multipack_delivered_usd"], nx.CEILING)

    def test_no_double_counted_driver_in_the_channel_base(self):
        # The fixed base carries the 80-channel driver block; options that
        # replace the channel must start from the no-channel base.
        self.assertAlmostEqual(
            nx.FIXED_PARTS_NO_CHANNEL + nx.S5_DRIVER_PARTS, nx.FIXED_PARTS, places=2)
        self.assertAlmostEqual(nx.S5_DRIVER_PARTS, 63.64, places=2)

    def test_shared_register_clears_cost_and_time(self):
        o = nx.shared_register_option()
        self.assertTrue(o["clears_cost"], "register must clear the ceiling")
        self.assertTrue(o["clears_time"], "register must clear 30 s")
        self.assertLess(o["delivered_usd"], 400.0)  # reaches the ideal band
        self.assertLess(o["actuator_count"], 80)

    def test_wider_head_fails_cost_at_the_real_order_tier(self):
        o = nx.wider_head_option(4)
        self.assertFalse(o["clears_cost"],
                         "R=4 must not clear at the 100-qty matched tier")
        self.assertTrue(o["clears_time"])
        self.assertLess(o["est_full_map_s"], 30.0)

    def test_wider_head_boundary_is_between_the_two_real_tiers(self):
        b = nx.wider_head_cost_boundary(4)
        self.assertFalse(b["clears_at_100qty"])
        self.assertTrue(b["clears_at_3001qty"])
        self.assertGreater(b["max_station_motor_usd"], 8.20)
        self.assertLess(b["max_station_motor_usd"], 11.20)

    def test_servo_class_is_rejected_on_pitch_not_cost(self):
        o = nx.servo_option()
        self.assertIn("PITCH", o["verdict"])
        self.assertIn("5.08", o["pitch_feasibility"])

    def test_printed_pancake_clears_cost_but_is_torque_unproven(self):
        o = nx.printed_pancake_option()
        self.assertTrue(o["clears_cost"])
        self.assertIn("UNPROVEN", o["verdict"])

    def test_global_memory_is_over_the_time_budget(self):
        o = nx.global_memory_option()
        self.assertFalse(o["clears_time"])
        self.assertGreater(o["est_full_map_s"], 30.0)

    def test_every_option_reports_the_four_required_quantities(self):
        for o in nx.options():
            for key in ("actuator_count", "actuator_cost_parts_usd",
                        "est_full_map_s", "deciding_quantity", "pitch_feasibility"):
                self.assertIn(key, o, f"{o['id']} missing {key}")
            self.assertTrue(o["deciding_quantity"])

    def test_mission_target_is_not_a_success_and_not_a_failure(self):
        s = nx.screen()
        self.assertIn("NOT DEMONSTRATED", s["mission_target_reachable"])
        # Survivors exist, so this is not a proven dead end either.
        self.assertTrue(s["cost_time_survivors"])

    def test_evidence_class_is_calculation_only(self):
        s = nx.screen()
        self.assertIn("CALCULATION", s["evidence_class"])
        self.assertIn("DND-27", s["evidence_class"])


if __name__ == "__main__":
    unittest.main()
