"""DND-45 K9 checks. Run from anywhere: python k9_checks.py.

Regression + honesty gates for the K9 Monte-Carlo angular-margin stack-up. These
pin the nominal geometry, assert the tolerance actually changes the answer, and
assert the model does NOT overclaim (5 levels is only conditionally safe).
"""
from __future__ import annotations

import math
import unittest

import k9_angular_margin as k9


class K9AngularMarginChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Fewer draws than production so CI stays fast; the ordering claims are
        # deterministic at this draw count with the fixed seed.
        cls.res = k9.run(draws=40_000, seed=k9.DEFAULT_SEED)

    def _row(self, levels, distribution, seating_random):
        return next(r for r in self.res["results"]
                    if r["levels"] == levels
                    and r["distribution"] == distribution
                    and r["seating_is_random"] == seating_random)

    # --- geometry reproduction ----------------------------------------------
    def test_toe_angle_reproduces_test09_envelope(self):
        # atan2(0.50, 1.15) = 23.4986 deg; Test09 README quotes 23.50 deg.
        self.assertAlmostEqual(k9.toe_angle_deg(k9.TOE_X_MM, k9.CENTER_X_MM,
                                                k9.TOE_WIDTH_MM), 23.4986, places=3)

    def test_nominal_margins_match_levels_csv(self):
        # Test09 README: 4 levels 21.50, 5 levels 12.50, 6 levels 6.50 deg.
        self.assertAlmostEqual(k9.nominal_margin_deg(4), 21.5014, places=3)
        self.assertAlmostEqual(k9.nominal_margin_deg(5), 12.5014, places=3)
        self.assertAlmostEqual(k9.nominal_margin_deg(6), 6.5014, places=3)

    # --- the tolerance actually bites ----------------------------------------
    def test_tolerance_reduces_the_5_level_margin(self):
        # A +/-0.05 mm tolerance must visibly reduce 5-level margin below the
        # 6.50 deg nominal-after-seating figure, or the MC is not propagating.
        r = self._row(5, "uniform", False)
        self.assertLess(r["mean_deg"], 6.50)
        # The worst-case seat model centre sits near 6.50 - E[tolerance penalty].
        self.assertGreater(r["std_deg"], 0.5)

    def test_six_levels_fails_nominally_after_seating(self):
        # 6 levels leave only 0.50 deg nominal after the 6 deg seat; tolerance
        # makes it clearly negative.
        r = self._row(6, "uniform", False)
        self.assertLess(r["mean_deg"], 0.0)
        self.assertGreater(r["p_negative"], 0.5)

    # --- the honest K9 verdict ----------------------------------------------
    def test_five_levels_is_gate_positive_under_bounded_tolerance(self):
        # Primary reading: +/-0.05 mm is a bounded capability limit. Then 5
        # levels keeps margin positive in every draw, but only just.
        r = self._row(5, "uniform", False)
        self.assertEqual(r["p_negative"], 0.0)
        self.assertLess(r["min_deg"], 3.0)        # thin guaranteed margin
        self.assertGreater(r["min_deg"], 0.0)
        self.assertEqual(self.res["max_safe_levels_primary"], 5)

    def test_five_levels_is_not_unconditionally_safe(self):
        # Honesty gate: under a Gaussian tail (0.05 as 1 sigma) 5 levels has a
        # nonzero failure probability. We must NOT claim 5 levels is robust.
        r = self._row(5, "gaussian", False)
        self.assertGreater(r["p_negative"], 0.0)
        self.assertEqual(self.res["max_safe_levels_gaussian_conservative"], 4)

    def test_four_levels_is_safe_everywhere(self):
        for dist in ("uniform", "gaussian"):
            for random_seat in (False, True):
                r = self._row(4, dist, random_seat)
                self.assertEqual(r["p_negative"], 0.0, msg=f"{dist}/{random_seat}")

    def test_margin_is_monotone_decreasing_in_level_count(self):
        rows = [self._row(L, "uniform", False) for L in k9.LEVEL_COUNTS]
        means = [r["mean_deg"] for r in rows]
        for a, b in zip(means, means[1:]):
            self.assertGreater(a, b)

    def test_random_seating_is_less_pessimistic_than_worst_case(self):
        for L in (5, 6):
            wc = self._row(L, "uniform", False)
            rnd = self._row(L, "uniform", True)
            self.assertGreater(rnd["mean_deg"], wc["mean_deg"])

    def test_evidence_class_states_no_measurement(self):
        self.assertIn("no measurement", self.res["evidence_class"])
        self.assertIn("DND-27", self.res["evidence_class"])


if __name__ == "__main__":
    unittest.main()
