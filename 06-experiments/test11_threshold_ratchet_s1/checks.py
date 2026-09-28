#!/usr/bin/env python3
"""Regression checks for the S1/S2 rejection arithmetic and timing models.

These lock the *reasoning*, not a physical claim. If a future change alters a
verdict without changing the stated threshold, this fails loudly.
"""

import unittest

import geometry
import rejection
import timing


class GeometryTest(unittest.TestCase):
    def test_pitch_partition(self) -> None:
        b = geometry.pitch_breakdown()
        self.assertAlmostEqual(b["pitch_mm"], 5.08)
        self.assertAlmostEqual(b["total_top_gap_mm"], 0.36, places=6)

    def test_gate_clearance(self) -> None:
        fits, spare = geometry.gate_clearance_ok()
        self.assertTrue(fits)
        self.assertGreater(spare, 1.0)

    def test_mask_decisions(self) -> None:
        self.assertEqual(geometry.mask_budget().moving_holes_per_plane, 3200)
        self.assertEqual(geometry.CELLS * (geometry.LEVELS - 1), 25_600)


class TimingTest(unittest.TestCase):
    def test_s1_full_map_passes_assumed_budget(self) -> None:
        r = timing.S1Timing().full_map()
        self.assertTrue(r["pass"])
        self.assertLess(r["total_s"], 30.0)
        self.assertAlmostEqual(r["total_s"], 5.30, places=2)

    def test_s2_full_map_is_short(self) -> None:
        r = timing.S2Timing().full_map()
        self.assertTrue(r["pass"])
        self.assertLess(r["total_s"], 3.0)

    def test_information_lower_bound(self) -> None:
        self.assertAlmostEqual(timing.full_map_bits(), 14860.34, places=1)


class RejectionTest(unittest.TestCase):
    def test_gate_density_fair_sub_surface(self) -> None:
        v = rejection.test_gate_density()
        self.assertEqual(v.verdict, rejection.PASS)

    def test_aggregate_force_marginal(self) -> None:
        v = rejection.test_aggregate_stroke_force()
        self.assertEqual(v.verdict, rejection.PASS)

    def test_all_armed_fails(self) -> None:
        v = rejection.test_worst_case_simultaneous()
        self.assertEqual(v.verdict, rejection.FAIL)

    def test_mask_visible_fails(self) -> None:
        v = rejection.test_mask_write_throughput()
        self.assertEqual(v.verdict, rejection.FAIL)

    def test_offline_writer_passes_at_interval(self) -> None:
        v = rejection.test_media_hidden_pipeline()
        self.assertEqual(v.verdict, rejection.PASS)

    def test_variation_break_even(self) -> None:
        be = rejection_print_break_even()
        self.assertGreater(be, 0.05)
        self.assertLess(be, 0.15)


def rejection_print_break_even() -> float:
    import sensitivity
    return sensitivity.variation_break_even()


if __name__ == "__main__":
    unittest.main()
