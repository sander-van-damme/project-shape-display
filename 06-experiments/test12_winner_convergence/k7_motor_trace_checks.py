"""Regression + honesty gates for the DND-49 K7 motor trace.

Run: python k7_motor_trace_checks.py
Standard library only.
"""
from __future__ import annotations

import unittest

import k7_motor_trace as k


class K7MotorTraceChecks(unittest.TestCase):
    def test_break_even_motor_is_1_86_delivered(self):
        # The DND-44/47 path clears only for a motor <= $1.86 delivered-inclusive.
        self.assertAlmostEqual(k.verdict()["break_even_motor_usd"], 1.8587, places=3)

    def test_no_matched_traced_part_at_or_below_ceiling(self):
        # K7 is REFUTED: every matched live candidate exceeds the break-even.
        be = k.verdict()["break_even_motor_usd"]
        matched = k.matched_candidates()
        self.assertTrue(matched, "must have at least one matched candidate")
        for c in matched:
            self.assertGreater(c["unit_usd"], be,
                               f"{c['id']} undercuts the {be} break-even")

    def test_cheapest_matched_is_ccht(self):
        v = k.verdict()
        self.assertEqual(v["cheapest_matched_id"], "CCHT-07-005-032")
        self.assertAlmostEqual(v["cheapest_matched_unit_usd"], 8.20, places=2)
        # Real 80+spares order tier is 100 pieces at $11.20, not the 3,001+ tier.
        self.assertAlmostEqual(v["cheapest_matched_at_100qty_usd"], 11.20, places=2)

    def test_cheapest_matched_delivered_is_over_the_ceiling(self):
        v = k.verdict()
        self.assertGreater(v["cheapest_matched_delivered_usd"], k.CEILING)
        self.assertGreater(v["moons_delivered_usd"], k.CEILING)

    def test_untraced_multipack_is_the_only_sub_ceiling_basis(self):
        # The $1.05 line clears, and it is explicitly unverified.
        v = k.verdict()
        self.assertLess(v["untraced_multipack_delivered_usd"], k.CEILING)
        row = next(r for r in v["rows"] if r["id"] == "Amazon-Abovehill")
        self.assertFalse(row["matched"])
        self.assertIn("UNVERIFIED", row["evidence"])

    def test_marketplace_rows_are_not_matched(self):
        for c in k.CANDIDATES:
            if c["evidence"].startswith("UNVERIFIED"):
                self.assertFalse(c["matched"], f"{c['id']} must not be matched")

    def test_reduced_head_lever_fails_the_time_budget(self):
        # The only machine-level lever (fewer motors) breaks the 30 s budget.
        lev = k.design_lever()
        by_width = {r["width"]: r for r in lev["rows"]}
        self.assertTrue(by_width[80]["under_30s"])
        self.assertFalse(by_width[40]["under_30s"])
        self.assertGreater(by_width[40]["est_full_map_s"], 30.0)

    def test_verdict_says_refuted(self):
        self.assertIn("REFUTED", k.verdict()["verdict"])

    def test_mainstream_sources_recorded_as_not_stocked(self):
        joined = " ".join(k.MAINSTREAM_NOT_STOCKED).lower()
        for src in ("lcsc", "digikey", "mouser", "octopart"):
            self.assertIn(src, joined)


if __name__ == "__main__":
    unittest.main()
