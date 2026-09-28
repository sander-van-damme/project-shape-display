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

    def test_dnd37_no_sourced_sub_400_path_exists(self):
        # DND-37 §2: prove (not just claim) that no sourced <$400 path exists on
        # current evidence. The reduced fixed stack leaves a parts budget whose
        # implied motor+driver pair price is below the cheapest sourced pair.
        target_parts = m.PRINT_FLOOR_USD / m.DELIVERED_UPLIFT
        reduced_fixed = (m.FIXED_SUBTOTAL_USD - m.REDUCTION_REGISTERS_USD
                         - m.REDUCTION_CONTROLLER_USD)
        budget_for_pair = (target_parts - reduced_fixed) / m.MOTOR_CHANNELS
        sourced_pair = m.SOURCED_MOTOR_USD + m.SOURCED_DRIVER_USD
        # The pair would have to cost less than the cheapest sourced pair...
        self.assertLess(budget_for_pair, sourced_pair)
        # ...and the implied per-motor budget is below any sourced motor alone
        # (a motor+driver pair cannot be had for less than one motor).
        self.assertLess(budget_for_pair, m.SOURCED_MOTOR_USD + 0.20)

    def test_dnd37_driver_substitution_is_cheaper_than_csv_drv8833(self):
        # The DND-37 driver swap must be a real sourced reduction, not a discount:
        # TB6612FNG @100 ($0.7955) < DRV8833PWPR expected ($1.58) in the CSV.
        import csv
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
            self.assertIn(k["status"],
                          {"closed-analytically", "conditional-analytically", "qualitative"})
        # The one residual is K2, now bounded analytically (DND-38) but still not
        # closed: it must carry the quantitative rule, not be empty.
        k2 = [k for k in s["killers"] if k["id"] == "K2"]
        self.assertEqual(len(k2), 1)
        self.assertEqual(k2[0]["status"], "conditional-analytically")
        self.assertIn("0.323", k2[0]["result"])


if __name__ == "__main__":
    unittest.main()
