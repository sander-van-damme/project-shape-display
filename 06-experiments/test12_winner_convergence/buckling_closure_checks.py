"""Regression + honesty gates for the DND-44 K1 buckling closure.

Run: python buckling_closure_checks.py
Requires numpy (same dependency as the repo's test08 cam_strength.py).
"""
from __future__ import annotations

import unittest

import buckling_closure as bk


class BucklingClosureChecks(unittest.TestCase):
    def test_repo_core_1p0_anchor_is_reproduced(self):
        table = {r["core_radius_mm"]: r for r in bk.core_reference()}
        self.assertAlmostEqual(table[1.0]["critical_load_n"], bk.CRITICAL_CORE_1P0_N, places=2)

    def test_critical_load_rises_with_core_radius(self):
        loads = [r["critical_load_n"] for r in bk.core_reference()]
        self.assertEqual(loads, sorted(loads))
        self.assertGreater(loads[-1], loads[0])

    def test_service_load_closes_with_wide_margin(self):
        b = bk.service_load_bound()
        # Even a 1 kg miniature on the smallest standard base is well under the
        # 4.96 N core, so the distributed service load is not a K1 driver.
        self.assertLess(b["worst_per_column_load_n"], 0.5)
        self.assertGreater(b["service_margin_vs_core"], 10.0)
        # The 1 N working assumption was conservative, not optimistic.
        self.assertTrue(b["assumption_was_conservative"])

    def test_base_distribution_is_the_governing_argument(self):
        # A base must spread over >1 column at this pitch, else the argument
        # collapses to a point load and we must fall back to the abuse case.
        for base, dia in bk.BASE_DIAMETER_MM.items():
            n = bk.columns_under_base(dia)
            self.assertGreater(n, 1, base)

    def test_core_1p0_does_not_clear_the_abuse_screen(self):
        # Honesty: the ORIGINAL core does not meet the 5 N screen; do not claim
        # the service bound silences the localized abuse case.
        table = {r["core_radius_mm"]: r for r in bk.core_reference()}
        self.assertFalse(table[1.0]["clears_5n_abuse"])

    def test_core_1p1_clears_the_abuse_screen(self):
        table = {r["core_radius_mm"]: r for r in bk.core_reference()}
        self.assertTrue(table[1.1]["clears_5n_abuse"])


if __name__ == "__main__":
    unittest.main()
