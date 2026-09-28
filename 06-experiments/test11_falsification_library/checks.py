#!/usr/bin/env python3
"""Regression checks for the Test11 falsification arithmetic.

Standard library only. These tests pin the *project's own headline numbers*
(e.g. 52.7% at q=0.01%) so that any edit to reliability.py that changes the
adversarial story fails CI rather than silently rewriting project risk.
"""

import unittest

import reliability as r


class PerfectMapTest(unittest.TestCase):
    def test_headline_0001(self) -> None:
        # The project's stated 0.01% per-cell error case.
        self.assertAlmostEqual(r.perfect_map_probability(1e-4), 0.52729, places=4)

    def test_headline_000001(self) -> None:
        self.assertAlmostEqual(r.perfect_map_probability(1e-5), 0.93800, places=4)

    def test_monotone(self) -> None:
        self.assertLess(
            r.perfect_map_probability(1e-4),
            r.perfect_map_probability(1e-5),
        )

    def test_cell_error_budget_for_99pct(self) -> None:
        # Test09 states q <= 1.570e-6 for a 99% perfect-map goal.
        q = r.cell_error_budget(0.99)
        self.assertAlmostEqual(q, 1.570e-6, places=9)

    def test_zero_failure_trials_formula(self) -> None:
        # Direct formula check: n >= ln(conf)/ln(1-q).
        n = r.zero_failure_trials(1e-4, confidence=0.95)
        self.assertEqual(n, 513)
        # Test09's ~1.91 million figure corresponds to q ~= 2.69e-8, i.e. the
        # per-cell-update rate needed for a 99% perfect map *before correlated
        # faults*; it is NOT the same q as the 1.57e-6 budget above.
        self.assertIn(r.zero_failure_trials(2.6887970294708907e-08, confidence=0.95),
                      (1_907_667, 1_907_668))

    def test_expected_failures(self) -> None:
        self.assertAlmostEqual(r.assumed_failures_per_map(1e-4), 0.64, places=6)


class RegionalTest(unittest.TestCase):
    def test_10x10_tile_fraction(self) -> None:
        # 8x8 = 64 tiles of 10x10 cells.
        self.assertAlmostEqual(r.regional_fraction(8, 1), 1.0 / 64.0, places=9)

    def test_20x20_tile_fraction(self) -> None:
        self.assertAlmostEqual(r.regional_fraction(4, 1), 1.0 / 16.0, places=9)

    def test_regional_scales_below_full(self) -> None:
        t = r.regional_update_seconds(26.251, 4.0, r.regional_fraction(8, 4))
        self.assertLess(t, 26.251)
        self.assertAlmostEqual(t, 4.0 + 22.251 * (4.0 / 64.0), places=4)

    def test_regional_never_negative(self) -> None:
        self.assertEqual(r.regional_update_seconds(26.251, 100.0, 0.0), 100.0)

    def test_jam_classification(self) -> None:
        self.assertEqual(r.jam_containment(100, 0, False), "CONTAINED")
        self.assertEqual(r.jam_containment(100, 10, False), "BOUNDED_BUT_EXPOSED")
        self.assertEqual(r.jam_containment(100, 10, True), "CORRELATED_FAIL")


class ReturnTest(unittest.TestCase):
    def test_solid_column_header(self) -> None:
        # Test08: solid 2.069 g, 5 mN modelled drag.
        m = r.return_margin(2.069, 5.0)
        self.assertAlmostEqual(m.gravity_mn, 20.29, places=1)
        self.assertAlmostEqual(m.ratio, 4.058, places=2)
        self.assertTrue(m.passes(2.0))

    def test_hollow_column_header(self) -> None:
        # Test08: hollow 0.997 g, 5 mN -> 4.78 mN net, ratio below 2x.
        m = r.return_margin(0.997, 5.0)
        self.assertAlmostEqual(m.gravity_mn, 9.78, places=1)
        self.assertFalse(m.passes(2.0))

    def test_extra_drag_to_fail(self) -> None:
        m = r.return_margin(2.069, 5.0)
        self.assertAlmostEqual(m.extra_drag_to_fail(), 15.29, places=1)

    def test_ratio_one_is_exactly_no_return(self) -> None:
        m = r.return_margin(1.0, r.gravity_mn(1.0))
        self.assertAlmostEqual(m.net_mn, 0.0, places=9)
        self.assertFalse(m.passes(1.0))


class ToleranceTest(unittest.TestCase):
    def test_zero_sigma_is_certain(self) -> None:
        self.assertAlmostEqual(r.tolerance_yield(0.10, 1e-9, 0.05), 1.0, places=6)

    def test_crossing_point_is_half(self) -> None:
        self.assertAlmostEqual(r.tolerance_yield(0.05, 0.02, 0.05), 0.5, places=9)

    def test_board_yield_compounds(self) -> None:
        # A 99.99% per-cell pass still loses ~47% of boards at 6400 cells.
        self.assertAlmostEqual(r.board_yield(0.9999), 0.5273, places=3)

    def test_yield_needed_for_99pct_board(self) -> None:
        per_cell = 0.99 ** (1.0 / r.CELLS_FULL)
        self.assertAlmostEqual(r.board_yield(per_cell), 0.99, places=6)


if __name__ == "__main__":
    unittest.main()
