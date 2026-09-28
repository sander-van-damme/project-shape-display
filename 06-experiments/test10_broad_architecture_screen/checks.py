#!/usr/bin/env python3
"""Regression checks for the Test10 scale arithmetic."""

import unittest

import model


class ScaleBoundsTest(unittest.TestCase):
    def test_reference_scale(self) -> None:
        r = model.results()
        self.assertEqual(r["cells"], 6400)
        self.assertAlmostEqual(r["active_width_mm"], 406.4)
        self.assertEqual(r["tile_count_10x10"], 64)
        self.assertEqual(r["unary_threshold_decisions"], 25_600)

    def test_serial_rate_and_parallel_stations(self) -> None:
        r = model.results()
        self.assertAlmostEqual(r["minimum_cell_transactions_per_s"], 213.333333, places=5)
        self.assertAlmostEqual(model.station_time(1, 0.4), 32.0)
        self.assertAlmostEqual(model.station_time(4, 0.4), 8.0)


if __name__ == "__main__":
    unittest.main()
