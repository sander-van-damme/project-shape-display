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

    def test_full_map_time_is_conditional_best_corner(self):
        # 26.251 s is the best corner. The design is conditional on a measured
        # >=400 pps loaded rate; the prior "3.749 s margin" is withdrawn (DND-41).
        s = m.stackup()
        self.assertLess(m.FULL_MAP_TIME_S, m.DEADLINE_S)
        self.assertTrue(s["time"]["conditional"])
        self.assertLess(m.TIMING_PASS_400, m.TIMING_CASES_PER_RATE / 4)
        self.assertGreater(m.TIMING_WORST_400_S, m.DEADLINE_S)

    def test_sourced_cost_is_over_ceiling_and_reduction_barely_clears(self):
        # DND-41: on the repo's additive basis (x1.16) the sourced pair is OVER
        # the ceiling; only the reduced path clears it, by a small margin.
        pair = m.winner_delivered_usd()
        self.assertGreater(pair, m.CEILING_USD)          # over the ceiling
        self.assertLess(pair, m.CEILING_USD + 5.0)       # but only just
        reduced = m.winner_reduced_delivered_usd()
        self.assertLess(reduced, m.CEILING_USD)
        # small margin, and NOT yet in the <$400 ideal band
        self.assertGreater(reduced, m.CEILING_USD - 25.0)
        self.assertGreater(reduced, m.PRINT_FLOOR_USD)

    def test_cost_basis_is_additive_and_register_saving_is_net(self):
        # DND-41 cost-basis reconciliation: the delivered uplift must be the
        # repo's additive x1.16 (NOT the multiplicative 1.10*1.06), and the
        # register consolidation saving must be the NET $10.30 (remove the whole
        # $14 allowance, add the sourced $3.70 chips) — not the $14 gross, and
        # not the $3.70-only credit that earlier mis-stated the reduced total as
        # $493.57. Guard so $493.57 cannot return.
        self.assertAlmostEqual(m.DELIVERED_UPLIFT, 1.16, places=6)
        self.assertNotAlmostEqual(m.DELIVERED_UPLIFT, 1.10 * 1.06, places=3)
        self.assertAlmostEqual(m.REDUCTION_REGISTERS_USD, 10.30, places=2)
        self.assertEqual(m.winner_delivered_usd(), 501.12)
        self.assertEqual(m.winner_reduced_delivered_usd(), 483.37)

    def test_reliability_model_is_honest(self):
        q99 = m.required_q_for(0.99)
        # At the assumed q the whole-map probability must be reported as low,
        # not hidden. This asserts we did not pick a flattering number.
        self.assertLess(m.p_perfect_map(0.0001), 0.60)
        self.assertGreater(m.p_perfect_map(q99), 0.98)

    def test_isolation_and_travel_gates(self):
        s = m.stackup()
        # Isolation is only a structural sub-bound; J2 engine returns INCONCLUSIVE.
        self.assertTrue(s["isolation"]["pass"])
        self.assertTrue(s["isolation"]["conditional"])
        self.assertTrue(s["travel"]["pass"])
        self.assertGreaterEqual(s["travel"]["increment_mm"], 9.9)

    def test_K1_abuse_screen_is_an_open_blocker(self):
        # DND-41: 4.96 N < 5 N Test08 measurement-protocol screen; the 1 N service
        # load is unsourced, so K1 is OPEN, not closed.
        self.assertLess(m.CAM_CRITICAL_BUCKLING_N, m.ABUSE_SCREEN_N)
        k1 = [k for k in m.stackup()["killers"] if k["id"] == "K1"]
        self.assertEqual(len(k1), 1)
        self.assertEqual(k1[0]["status"], "open")

    def test_killer_list_is_honestly_labelled(self):
        s = m.stackup()
        statuses = {k["id"]: k["status"] for k in s["killers"]}
        # DND-41 relabels and the six added killers.
        self.assertEqual(statuses["K1"], "open")
        self.assertEqual(statuses["K4"], "partially-closed")
        self.assertEqual(statuses["K6"], "conditional")
        for kid in ("K7", "K8", "K9", "K10", "K11", "K12"):
            self.assertEqual(statuses[kid], "open")
        # K2 remains bounded-but-not-closed by DND-38.
        self.assertEqual(statuses["K2"], "conditional-analytically")
        self.assertIn("0.323", [k["result"] for k in s["killers"] if k["id"] == "K2"][0])


if __name__ == "__main__":
    unittest.main()
