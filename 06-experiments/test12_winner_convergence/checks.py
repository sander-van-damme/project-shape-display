"""DND-35 convergence checks. Run from anywhere: python checks.py."""
from __future__ import annotations

import csv
import unittest
from pathlib import Path

import model as m
import ratify_bom as rb

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

    def test_ratify_bom_agrees_with_model_on_the_headline_costs(self):
        # Root-cause guard [DND-41]: ratify_bom.py and model.py must never drift.
        # Before this gate main carried two contradictory cost models (491/501 vs
        # 493/503) on different uplift bases. Both must now use the additive
        # x1.16 basis and the net-consolidation method.
        self.assertAlmostEqual(rb.UPLIFT, m.DELIVERED_UPLIFT, places=6)
        rows = rb.load_rows()
        fixed = rb.fixed_expected(rows)
        reg_expected = sum(
            int(r["quantity"]) * float(r["unit_expected_usd"])
            for r in rows if rb.is_register(r["item"])
        )
        ctrl_expected = sum(
            int(r["quantity"]) * float(r["unit_expected_usd"])
            for r in rows if rb.is_controller(r["item"])
        )
        sourced = rb.delivered(fixed + 80 * rb.MOTOR_SOURCED + 80 * rb.DRIVER_TB6612_SOURCED)
        honest_fixed = (
            fixed
            - (reg_expected - 40 * rb.REGISTER_SOURCED)
            - (ctrl_expected - rb.CONTROLLER_SOURCED)
        )
        reduced = rb.delivered(
            honest_fixed + 80 * rb.MOTOR_SOURCED + 80 * rb.DRIVER_TB6612_SOURCED
        )
        self.assertAlmostEqual(sourced, m.winner_delivered_usd(), places=2)
        self.assertAlmostEqual(reduced, m.winner_reduced_delivered_usd(), places=2)

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

    # --- DND-37 regression gates (ported from superseded PR #32) ---
    # These three guards fence the *cost claims a future edit may make*. They are
    # independent of the DND-41 basis correction above: (1) they stop a quiet
    # sub-$400 claim, (2) they prove the model is a genuine function of the
    # sourced prices rather than a hard-coded constant, and (3) they keep the
    # matched-motor fallback recorded as dead.

    def test_no_sourced_path_claims_the_400_ideal_band(self):
        # The <$400 ideal band is NOT demonstrated at any sourced motor/driver
        # price in the traceable range. Guard against an edit that quietly
        # asserts a sub-$400 winner.
        self.assertGreater(m.winner_delivered_usd(), m.PRINT_FLOOR_USD)
        self.assertGreater(m.winner_reduced_delivered_usd(), m.PRINT_FLOOR_USD)

    def test_cost_model_is_a_real_function_of_sourced_prices(self):
        # Swapping in the traceable DRV8833 driver ($1.3338, LCSC C50506) must
        # move the headline by exactly the sourced delta x the additive uplift;
        # a hard-coded total would fail this. The matched motor may only push
        # cost up, never down.
        base = m.winner_delivered_usd()
        drv = m.winner_delivered_usd(driver_usd=1.3338)
        expected_delta = round(
            m.DRIVER_CHANNELS * (1.3338 - m.SOURCED_DRIVER_USD) * m.DELIVERED_UPLIFT, 2
        )
        self.assertAlmostEqual(round(drv - base, 2), expected_delta, places=2)
        self.assertGreater(m.winner_delivered_usd(motor_usd=5.00), base)

    def test_matched_motor_fallback_is_dead(self):
        # The only traceable matched part (MOONS 8PM020S1, ~$40/ea) puts the
        # winner far over the ceiling: 80 x $40 = $3,200 alone. No sub-$1.05
        # *matched* motor exists; the sourced unit is an untraced multipack (K7).
        # Guard that no one re-brands the matched part as a winner path.
        self.assertGreater(m.winner_delivered_usd(motor_usd=40.0), 2.0 * m.CEILING_USD)


if __name__ == "__main__":
    unittest.main()
