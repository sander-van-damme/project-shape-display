"""Regression + honesty gates for the DND-44 K6 timing closure.

Run: python timing_closure_checks.py
Standard library only.
"""
from __future__ import annotations

import math
import unittest

import timing_closure as tc


class TimingClosureChecks(unittest.TestCase):
    def test_closed_form_matches_the_repo_schedule(self):
        cc = tc.cross_check()
        self.assertLess(cc["abs_error_s"], 1e-9, cc)

    def test_design_point_is_the_documented_baseline(self):
        self.assertAlmostEqual(tc.full_map_s(400), 26.251292522118074, places=6)

    def test_rate_independent_floor_is_real_and_binds(self):
        # The floor cannot be beaten by any step rate: at 1e9 pps the time
        # must still exceed it, and adding rate can only reduce it.
        floor = tc.rate_independent_floor_s()
        self.assertGreater(floor, 18.0)
        self.assertGreaterEqual(tc.full_map_s(1e9), floor - 1e-6)
        self.assertLess(tc.full_map_s(1e9), floor + 1e-3)

    def test_required_rate_is_below_the_design_rate(self):
        # If the required rate were at/above 400 pps the design point would be
        # fragile; the closure shows it is not (268 pps << 400 pps).
        req = tc.required_rate_pps(30.0)
        self.assertLess(req, tc.TIMING["rate_hz"])
        self.assertAlmostEqual(tc.full_map_s(req), 30.0, places=2)

    def test_worst_corner_is_not_rate_recoverable(self):
        # The 45 s worst corner has a rate-independent floor above 30 s, so no
        # motor upgrade fixes it. This is the honesty gate: do not claim the
        # sweep failure is a step-rate problem.
        worst = tc.scenario_timing(0.050, 0.040, 1000)
        floor = tc.rate_independent_floor_s(worst)
        self.assertGreater(floor, 30.0)
        self.assertTrue(math.isinf(tc.required_rate_pps(30.0, worst, 3.0)))

    def test_engagement_dwell_is_the_governing_lever(self):
        # Improving the engage/settle dwells must move the required rate more
        # than any plausible step-rate choice alone.
        central = tc.required_rate_pps(30.0)
        pessimistic = tc.required_rate_pps(30.0, tc.scenario_timing(0.050, 0.040, 4000))
        self.assertGreater(pessimistic, 2 * central)


if __name__ == "__main__":
    unittest.main()
