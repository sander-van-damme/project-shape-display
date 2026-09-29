"""Regression + honesty gates for the DND-59 S5-R residual retirement.

Run: python s5r_residuals_checks.py
Standard library only (imports s5r_residuals / s5r_register).

These fail if (a) any retired residual gate is mis-computed, (b) the keeper
re-profile silently regresses to 1 line or to a tolerance-fragile bending hold,
or (c) the evidence class is mislabelled as anything but CAD + CALCULATION +
sourced. They also assert the DND-59 ADR carries the decisive numbers.
"""
from __future__ import annotations

import unittest
from pathlib import Path

import s5r_register as reg
import s5r_residuals as r

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
ADR = REPO / "07-evidence-and-decisions" / "dnd59-s5r-residual-retirement.md"


class ResidualChecks(unittest.TestCase):
    def test_keeper_is_two_lines_not_one(self):
        k = r.keeper_reprofile()
        self.assertGreaterEqual(r.KEEPER_T_MM, r.MIN_WALL_MM - 1e-9)
        self.assertEqual(k["printability_verdict"], "PASS")
        self.assertIn("2 extrusion lines", k["new_leaf"]["verdict"])
        # the superseded DND-54 keeper is recorded as 1 line / RISK
        self.assertAlmostEqual(k["old_leaf"]["t_mm"], 0.45, places=6)

    def test_keeper_hold_is_a_compression_shoulder(self):
        k = r.keeper_reprofile()
        hm = k["hold_mechanism"]
        self.assertIn("compression", hm["kind"])
        # the shoulder carries the pawl push-out with a large margin
        self.assertGreater(hm["margin_lo"], 3.0)
        self.assertGreater(hm["capacity_lo_n"], hm["shoulder_load_n"])

    def test_keeper_hold_does_not_depend_on_offset(self):
        # The whole point: the bending-only hold is tolerance-fragile, the
        # hard-shoulder hold is not. Assert the MC shows the difference.
        mc = r.keeper_tolerance_mc(n=50000, seed=11)
        self.assertLess(mc["p_hold_bending_only"], 0.95)
        self.assertEqual(mc["p_hold_hard_shoulder"], 1.0)

    def test_keeper_reprofile_still_fits_the_cell(self):
        fit = reg.cell_fit()
        self.assertTrue(fit["fits_worst_case"])
        self.assertGreaterEqual(fit["tip_gap_worst_mm"], 0.20)

    def test_writer_force_bottom_up_passes(self):
        w = r.writer_force_bottom_up()
        self.assertTrue(w["pass_gate"])
        self.assertGreater(w["margin"], 2.0)
        # bottom-up force is required, not asserted
        self.assertGreater(w["required_solenoid_n"], 0.0)
        # the gate travel must NOT be multiplied through the leaf rate
        self.assertLess(w["required_solenoid_n"], 1.0)

    def test_reliability_requirement_and_levers(self):
        rel = r.reliability()
        # 99 percent of 6400 cells => q of order 1.6e-6
        self.assertAlmostEqual(rel["bare_q_required"], 1.57e-6, places=9)
        archs = rel["architectures"]
        # verify+retry relaxes the requirement (q_vs_bare > 1)
        self.assertGreater(archs["per_group_verify_retry_c90"]["q_vs_bare"], 5.0)
        self.assertGreater(archs["writer_redundancy_2x"]["q_vs_bare"], 100.0)

    def test_crank_speed_margin(self):
        c = r.crank_speed()
        self.assertTrue(c["speed_inside_sourced_class"])
        self.assertGreater(c["crank_margin"], 1.0)
        self.assertGreater(c["settle_margin"], 1.0)
        self.assertGreater(c["torque_margin"], 1.5)
        # break-even matches the DND-54 figure (~468 deg/s)
        self.assertAlmostEqual(c["min_crank_deg_s_for_30s"], 468.0, delta=1.0)

    def test_bar_eccentricity_closed_for_steel_rod(self):
        e = r.bar_eccentricity()
        self.assertTrue(e["closed"])
        self.assertEqual(e["chosen_bar_d_mm"], 6.0)
        self.assertGreater(e["margin_at_extreme_e"], 10.0)
        # break-even e is far beyond any physical tooth-contact offset
        self.assertGreater(e["break_even_eccentricity_mm"], 50.0)

    def test_all_retirable_gates_pass(self):
        d = r.decide()
        self.assertTrue(all(d["gates"].values()), d["gates"])
        self.assertTrue(d["all_retirable_gates_pass"])

    def test_measurement_only_residue_is_named(self):
        d = r.decide()
        residue = " ".join(d["measurement_only_residue"])
        for token in ("friction", "creep", "reliability", "speed/torque"):
            self.assertIn(token, residue)

    def test_evidence_class_is_cad_calc_sourced_only(self):
        d = r.decide()
        self.assertIn("CAD", d["evidence_class"])
        self.assertIn("CALCULATION", d["evidence_class"])
        self.assertIn("sourced", d["evidence_class"])
        self.assertIn("DND-27", d["evidence_class"])

    def test_adr_carries_the_decisive_numbers(self):
        self.assertTrue(ADR.exists(), f"missing ADR {ADR}")
        text = ADR.read_text()
        for token in ("R-DND54-KEEPER", "R-DND54-6", "R-DND54-5", "R-DND54-3",
                      "R-DND55-1", "2 lines", "compression", "0.90",
                      "0.1794", "1.57e-6", "468", "DND-59", "NOT a print"):
            self.assertIn(token, text, f"{token!r} missing from the DND-59 ADR")


if __name__ == "__main__":
    unittest.main(verbosity=2)
