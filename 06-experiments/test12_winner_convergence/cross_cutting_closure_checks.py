"""Regression + honesty gates for the DND-44 K8/K10/K11 cross-cutting closure.

Run: python cross_cutting_closure_checks.py
Standard library only.
"""
from __future__ import annotations

import unittest

import cross_cutting_closure as cx


class CrossCuttingChecks(unittest.TestCase):
    def test_k8_lateral_limit_clears_the_protocol_load(self):
        b = cx.k8_bound(12.0)
        # A 1 N protocol lateral load must deflect less than the 0.10 mm gate.
        self.assertLess(b["tip_deflection_at_1n_mm"], 0.10)
        self.assertGreater(b["governing_lateral_limit_n"], 1.0)
        # Honesty: the detent alone cannot hold a 1 N lateral load; that must be
        # stated, not hidden, so the record cannot imply the detent does it.
        self.assertFalse(b["detent_holds_against_1n"])

    def test_k10_regional_is_bounded_and_under_full_map_time(self):
        b = cx.k10_bound()
        self.assertLess(b[1], 5.0)      # a one-row regional rewrite is quick
        self.assertLess(b[10], 10.0)    # a 10-row region is well inside budget
        self.assertLess(b[80], 30.0)    # a full rewrite is the full-map case
        for k in (1, 5, 10, 20, 80):
            self.assertLess(b[k], cx.tc.full_map_s(400) + 1.0)

    def test_k10_regional_is_monotonic(self):
        b = cx.k10_bound()
        vals = [b[k] for k in (1, 5, 10, 20, 80)]
        self.assertEqual(vals, sorted(vals))

    def test_k11_cycle_bound_is_order_of_magnitude_only(self):
        b = cx.k11_bound()
        # A bound must be finite and clearly labelled as an estimate, not a
        # qualification.
        self.assertGreater(b["estimated_cycles_to_failure"], 1e6)
        self.assertIn("order-of-magnitude", b["note"])
        self.assertIn("not measured", b["note"])

    def test_k11_strain_is_plausible_for_a_printed_leaf(self):
        b = cx.k11_bound()
        # Surface strain below the 0.3% endurance assumption (else the leaf is
        # already at/over the fatigue limit and the bound would flip).
        self.assertLess(b["detent_surface_strain_percent"], b["assumed_endurance_strain_percent"])


if __name__ == "__main__":
    unittest.main()
