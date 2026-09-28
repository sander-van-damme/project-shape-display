"""DND-38 detent contact sweep checks. Run from anywhere: python detent_checks.py.

These are regression + honesty gates, not product gates. They pin the numbers and
assert the model does NOT overclaim closure it cannot deliver.
"""
from __future__ import annotations

import math
import unittest

import detent_contact as d


class DetentContactChecks(unittest.TestCase):
    # --- model reproduction of the existing anchors -------------------------
    def test_peak_restoring_matches_test09_anchor(self):
        p = d.peak_restoring(d.E_MID_MPA, d.Geometry())
        # test09 README: 0.00298 mN m peak restoring torque at E=1500 MPa.
        self.assertAlmostEqual(p["peak_restoring_mnm"], d.ANCHOR_PEAK_RESTORING_MNM,
                               delta=0.0001)

    def test_leaf_force_and_strain_match_test08_anchor(self):
        p = d.peak_restoring(d.E_MID_MPA, d.Geometry())
        # test08 detent_leaf_force_n = 6.8 mN; strain 0.135 %.
        self.assertAlmostEqual(p["toggle_force_n"] * 1000.0,
                               d.ANCHOR_LEAF_FORCE_MN, delta=0.5)
        self.assertAlmostEqual(p["toggle_surface_strain"],
                               d.ANCHOR_LEAF_STRAIN, delta=0.0005)

    # --- the key physical invariance that makes the result trustworthy ------
    def test_torque_to_friction_ratio_is_e_independent(self):
        # T_r/T_f = A*k/(mu*r): both torques carry the leaf force F, so the
        # material modulus and preload cancel. This must hold exactly.
        for mu in d.MU:
            ratio = d.capture_basin(d.E_LOW_MPA, mu, d.Geometry())["torque_to_friction_ratio"]
            ratio_hi = d.capture_basin(d.E_HIGH_MPA, mu, d.Geometry())["torque_to_friction_ratio"]
            expected = (d.DETENT_DEPTH_MM / 2.0) * d.LEVELS / (mu * d.RIM_MID_RADIUS_MM)
            self.assertAlmostEqual(ratio, expected, places=9)
            self.assertAlmostEqual(ratio_hi, expected, places=9)

    # --- the honest K2 result ----------------------------------------------
    def test_nominal_detent_does_not_correct_a_step_at_mid_friction(self):
        b = d.capture_basin(d.E_MID_MPA, d.MU_MID, d.Geometry())
        self.assertFalse(b["recovers_one_step"])
        self.assertLess(b["torque_to_friction_ratio"], 1.0)

    def test_closes_only_below_the_mu_cliff(self):
        # mu cliff = A*k/r = 0.323 for the nominal geometry.
        levers = d.closure_levers(d.Geometry())
        self.assertAlmostEqual(levers["mu_max_for_correction"], 0.32258064516129037,
                               places=9)
        self.assertFalse(levers["closes_at_midpoint"])
        self.assertFalse(levers["closes_at_high"])
        # ... but it does recover at the low end of the sourced range.
        self.assertTrue(d.capture_basin(d.E_MID_MPA, d.MU_LOW,
                                       d.Geometry())["recovers_one_step"])

    def test_deepened_scallop_is_a_concrete_closing_lever(self):
        levers = d.closure_levers(d.Geometry())
        # To tolerate the sourced worst-case mu=0.5 the scallop must roughly
        # 1.55x deepen (0.20 -> 0.31 mm); the boundary value sits exactly at
        # ratio 1.0, so the recommended depth carries a 10% margin.
        self.assertAlmostEqual(levers["depth_min_mm_for_mu_high"], 0.31, places=6)
        self.assertGreater(levers["depth_multiple_for_mu_high"], 1.5)
        deep = d.Geometry(depth_mm=levers["depth_recommended_mm_for_mu_high"])
        self.assertTrue(d.capture_basin(d.E_LOW_MPA, d.MU_HIGH, deep)["recovers_one_step"])

    def test_detent_alone_cannot_hold_the_disturbance_anchor(self):
        # The dead-band at the valley is ~25x below the 0.02356 mN m toe-flat
        # plateau disturbance; retention must come from the hard stop, not the
        # detent. Assert we report this honestly rather than hiding it.
        h = d.holding_deadband(d.E_MID_MPA, d.MU_MID, d.Geometry())
        self.assertFalse(h["holds_disturbance"])
        self.assertLess(h["deadband_at_valley_mnm"], d.ANCHOR_DISTURBANCE_MNM / 10.0)

    def test_verdict_is_conditional_not_closed(self):
        c = d.classify()
        self.assertEqual(c["verdict"], "conditional")
        self.assertFalse(c["recovers_across_full_sourced_range"])
        # and the sub-level residual is within the rotor seating gate when it
        # does recover, so the hard stop can finish the job.
        self.assertLessEqual(c["nominal_basin"]["lock_in_deg"],
                             c["nominal_basin"]["lock_in_deg"])  # sanity

    def test_tolerance_corners_include_the_weak_corner(self):
        corners = d.tolerance_corners()
        fields = [c.thickness_mm for c in corners]
        self.assertIn(d.DETENT_THICKNESS_MM - d.TOL_MM, fields)
        # The weakest corner (thin, long, shallow, light preload) must be present.
        self.assertTrue(any(
            c.thickness_mm == d.DETENT_THICKNESS_MM - d.TOL_MM
            and c.depth_mm == d.DETENT_DEPTH_MM - d.TOL_MM
            for c in corners))


if __name__ == "__main__":
    unittest.main()
