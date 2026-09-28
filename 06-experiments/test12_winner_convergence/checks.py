"""DND-35 convergence checks. Run from anywhere: python checks.py."""
from __future__ import annotations

import csv
import unittest
from pathlib import Path

import model as m

S5_BOM = (m.REPO / "06-experiments" / "test11_cost_printability_reliability"
          / "delivered_3scenario" / "bom_S5_delivered.csv")


class WinnerConvergenceChecks(unittest.TestCase):
    def test_fixed_subtotal_is_reproduced_from_the_sourced_bom(self):
        rows = list(csv.DictReader(S5_BOM.open(newline="")))
        fixed = sum(
            int(r["quantity"]) * float(r["unit_expected_usd"])
            for r in rows
            if not r["item"].startswith(("PM motor", "Dual H-bridge"))
        )
        self.assertAlmostEqual(fixed, m.FIXED_SUBTOTAL_USD, places=2)

    def test_exactly_one_winner(self):
        wins = [k for k, (d, _) in m.DISPOSITIONS.items() if d == "win"]
        self.assertEqual(wins, [m.WINNER])

    def test_every_loser_has_killing_evidence(self):
        for cand, (disp, why) in m.DISPOSITIONS.items():
            self.assertIn(disp, {"kill", "park", "win"})
            self.assertTrue(why and len(why) > 20, f"{cand} lacks evidence")

    def test_two_bet_framing_and_no_fallback_cost_kill(self):
        # Falsifier DND-36: S1-S4 are Bet A; S5 is Bet B. Cost must not be cited
        # as the binding evidence for S1/S2/S4 (their BOMs are fallback-inflated).
        for cand in ("S1", "S2", "S4"):
            self.assertEqual(m.DISPOSITIONS[cand][0], "kill" if cand == "S1" else "park")
            self.assertIn("Bet A", m.DISPOSITIONS[cand][1])
        self.assertIn("Bet B", m.DISPOSITIONS["S5"][1])
        self.assertIn("sourced selectors", m.DISPOSITIONS["S3"][1])

    def test_full_map_time_under_deadline(self):
        self.assertLess(m.FULL_MAP_TIME_S, m.DEADLINE_S)
        # and the margin must be a real, positive number of seconds
        self.assertGreater(m.DEADLINE_S - m.FULL_MAP_TIME_S, 3.0)

    def test_sourced_cost_hugs_ceiling_and_reduction_clears_it(self):
        pair = m.winner_delivered_usd()
        # The sourced motor+driver pair lands essentially ON the ceiling (the
        # repo's own DND-11 check asserts within $5). Assert that honestly.
        self.assertLess(abs(pair - m.CEILING_USD), 5.0)
        reduced = m.winner_reduced_delivered_usd()
        self.assertLess(reduced, m.CEILING_USD)
        # Must clear the ceiling by a real, non-trivial margin, not by cents.
        self.assertLess(reduced, m.CEILING_USD - 10.0)
        # Reaching the <$400 ideal band is NOT yet demonstrated; assert only
        # that we do not falsely claim it.
        self.assertGreater(reduced, m.PRINT_FLOOR_USD)

    def test_reliability_model_is_honest(self):
        q99 = m.required_q_for(0.99)
        # At the assumed q the whole-map probability must be reported as low,
        # not hidden. This asserts we did not pick a flattering number.
        self.assertLess(m.p_perfect_map(0.0001), 0.60)
        self.assertGreater(m.p_perfect_map(q99), 0.98)

    def test_isolation_and_travel_gates(self):
        s = m.stackup()
        self.assertTrue(s["isolation"]["pass"])
        self.assertTrue(s["travel"]["pass"])
        self.assertGreaterEqual(s["travel"]["increment_mm"], 9.9)

    def test_abuse_screen_is_not_a_design_gate(self):
        # The 5 N is a handling screen; the 1 N service load must pass with margin.
        self.assertGreater(m.CAM_CRITICAL_BUCKLING_N, m.SERVICE_LOAD_N * 4.0)
        self.assertGreater(m.ABUSE_SCREEN_N, m.SERVICE_LOAD_N)
        self.assertLess(m.CAM_CRITICAL_BUCKLING_N, m.ABUSE_SCREEN_N)

    def test_killer_list_closes_the_numeric_ones(self):
        s = m.stackup()
        self.assertTrue(s["time"]["pass"])
        self.assertTrue(s["cost"]["pass"])
        for k in s["killers"]:
            self.assertIn(k["status"], {"closed-analytically", "qualitative"})
        qual = [k for k in s["killers"] if k["status"] == "qualitative"]
        # the residual qualitative risk must be named, not empty
        self.assertTrue(qual)


if __name__ == "__main__":
    unittest.main()
