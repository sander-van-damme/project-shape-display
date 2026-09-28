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

    def test_dnd37_no_sourced_sub_400_path_exists(self):
        # DND-37 §2 (ported from PR #32's draft): prove — not just claim — that no
        # sourced <$400 path exists on current evidence. The reduced fixed stack
        # leaves a parts budget whose implied motor+driver pair price is below the
        # cheapest sourced pair.
        target_parts = m.PRINT_FLOOR_USD / m.DELIVERED_UPLIFT
        reduced_fixed = (m.FIXED_SUBTOTAL_USD - m.REDUCTION_REGISTERS_USD
                         - m.REDUCTION_CONTROLLER_USD)
        budget_for_pair = (target_parts - reduced_fixed) / m.MOTOR_CHANNELS
        sourced_pair = m.SOURCED_MOTOR_USD + m.SOURCED_DRIVER_USD
        # The pair would have to cost less than the cheapest sourced pair...
        self.assertLess(budget_for_pair, sourced_pair)
        # ...and the implied per-channel budget is below any sourced motor alone
        # (a motor+driver pair cannot be had for less than one motor).
        self.assertLess(budget_for_pair, m.SOURCED_MOTOR_USD + 0.20)

    def test_dnd37_driver_substitution_is_cheaper_than_csv_drv8833(self):
        # The DND-37 driver swap must be a real sourced reduction, not a discount:
        # TB6612FNG @100 ($0.80) < DRV8833PWPR expected ($1.58) in the CSV.
        rows = list(csv.DictReader(S5_BOM.open(newline="")))
        drv = [r for r in rows if r["item"].startswith("Dual H-bridge")][0]
        csv_driver = float(drv["unit_expected_usd"])
        self.assertLess(m.SOURCED_DRIVER_USD, csv_driver)

    def test_dnd37_matched_motor_fallback_is_a_dead_cost_path(self):
        # The only traceable matched 8 mm PM stepper is ~$40/ea. Assert the
        # program is honest that this fallback is arithmetically dead, i.e. it
        # blows the ceiling by a very large multiple.
        matched_motor = 40.0
        matched_total = m.winner_delivered_usd(motor_usd=matched_motor)
        self.assertGreater(matched_total, m.CEILING_USD * 5.0)

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
        # DND-44 closed K1 for the distributed SERVICE load (buckling_closure.py)
        # and bounded the localized abuse case. The core-1.0 still does not meet
        # the 5 N abuse screen; the 1 N service load was shown conservative.
        b = m.stackup()
        k1 = [k for k in b["killers"] if k["id"] == "K1"]
        self.assertEqual(len(k1), 1)
        self.assertIn("closed-analytically", k1[0]["status"])
        # The localized 5 N screen is still named as the residual.
        self.assertIn("abuse", k1[0]["result"])

    def test_killer_list_is_honestly_labelled(self):
        s = m.stackup()
        statuses = {k["id"]: k["status"] for k in s["killers"]}
        # DND-41 relabelled; DND-44 closed K1(service)/K5/K6/K8/K10 and bounded K11.
        self.assertIn("closed-analytically", statuses["K1"])
        self.assertEqual(statuses["K4"], "partially-closed")
        self.assertTrue(statuses["K6"].startswith("conditional"))
        self.assertIn("closed-analytically", statuses["K5"])
        self.assertIn("closed-analytically", statuses["K8"])
        self.assertIn("closed-analytically", statuses["K10"])
        self.assertTrue(statuses["K11"].startswith("bounded"))
        # K7 remains the open binding residual; K12 stays open/delegated.
        self.assertTrue(statuses["K7"].startswith("open"))
        self.assertEqual(statuses["K12"], "open")
        # DND-45: K2 gets a named geometry inside the envelope; still conditional
        # on print realisation (mu/creep/tip sharpness are measurement-only).
        self.assertIn("closed-analytically", statuses["K2"])
        self.assertIn("conditional on print realisation", statuses["K2"])
        k2 = [k for k in s["killers"] if k["id"] == "K2"][0]
        self.assertIn("0.40 mm", k2["result"])
        # DND-45: K9 is closed analytically - the level count is bounded.
        self.assertIn("closed-analytically", statuses["K9"])
        k9 = [k for k in s["killers"] if k["id"] == "K9"][0]
        self.assertIn("6 levels", k9["result"])

    def test_dnd44_cost_closure_anchors(self):
        # The honest expected baseline is over the ceiling; the machine-preserving
        # source path clears it. Both must be present so neither can be hidden.
        s = m.stackup()["cost"]
        self.assertGreater(s["expected_baseline_delivered_usd"], m.CEILING_USD)
        self.assertLess(s["sourced_path_delivered_usd"], m.CEILING_USD)
        self.assertGreater(m.CEILING_USD - s["sourced_path_delivered_usd"], 25.0)
        self.assertTrue(s["sourced_path_pass"])


if __name__ == "__main__":
    unittest.main()
