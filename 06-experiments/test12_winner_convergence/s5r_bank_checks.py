"""Regression + honesty gates for the DND-55 S5-R R=4 bank assembly model.

Run: python s5r_bank_checks.py
Standard library only (imports s5r_bank / s5r_register).

These fail if (a) a torsion/clearance figure is mis-computed, (b) the model
drifts from the SCAD source of truth, (c) the assembly verdict is silently
softened (the bar-torsion gate is EXPECTED to fail for the DND-54 placeholder
section and for a printed 3x12 at the worst-case eccentricity -- a later edit
that flips that without new evidence must break CI), or (d) the evidence class
is mislabelled as anything but CAD + CALCULATION.

The CAD (OpenSCAD) render + interference queries are exercised separately by
`python s5r_bank.py --cad` and by the winner-cad-render / geometry-validation
CI jobs; these checks are the stdlib-only arithmetic/honesty layer.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

import s5r_bank as b
import s5r_register as reg

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
SCAD = HERE / "s5r_bank.scad"
ADR = REPO / "07-evidence-and-decisions" / "dnd55-s5r-bank-assembly.md"


def _scad_const(name: str) -> float:
    text = SCAD.read_text()
    m = re.search(r"^%s\s*=\s*([0-9.]+)\s*;" % name, text, re.M)
    assert m, f"{name} missing from s5r_bank.scad"
    return float(m.group(1))


class BankChecks(unittest.TestCase):
    def test_scad_and_model_constants_agree(self):
        pairs = {
            "PITCH": b.PITCH_MM, "ROW_PITCH": b.ROW_PITCH_MM,
            "BANK_ROWS": b.BANK_ROWS, "BAR_W": b.BAR_W_MM, "BAR_H": b.BAR_H_MM,
            "RACK_TOOTH_PITCH": b.RACK_TOOTH_PITCH_MM,
            "RACK_TOOTH_HEIGHT": b.RACK_TOOTH_HEIGHT_MM,
            "CELL_H": b.CELL_H_MM, "COMBER_TINE_T": b.COMBER_TINE_T_MM,
            "CARRIAGE_WALL": b.CARRIAGE_WALL_MM,
            "CARRIAGE_X": b.CARRIAGE_X_MM, "CARRIAGE_Y": b.CARRIAGE_Y_MM,
            "CARRIAGE_Z": b.CARRIAGE_Z_MM, "CARRIAGE_CLEAR": b.CARRIAGE_CLEAR_MM,
        }
        for name, model in pairs.items():
            self.assertAlmostEqual(_scad_const(name), float(model), places=6,
                                   msg=f"{name} drifted between SCAD and model")

    def test_per_pawl_force_is_inherited_from_dnd54(self):
        import s5r_register as reg
        self.assertAlmostEqual(b.PER_PAWL_N,
                               reg.pawl_spring()["force_n"] + reg.WRITE_LOAD_N,
                               places=9)

    def test_torsion_constants_are_textbook(self):
        # solid rectangle J (Timoshenko) and solid round J = pi d^4/32
        import math
        self.assertAlmostEqual(b.torsion_constant_round(6.0),
                               math.pi * 6.0 ** 4 / 32.0, places=6)
        j = b.torsion_constant_rect(3.0, 2.0)
        self.assertAlmostEqual(j, (2.0 ** 3 * 3.0 / 3.0) * (1 - 0.630 * 2 / 3),
                               places=6)

    def test_placeholder_bar_fails_the_gate_by_a_lot(self):
        # This is the DECISION-CHANGING number: DND-54's 3x2 placeholder bar is
        # ~20x over the gate. A change that "fixes" this without a new section
        # must break CI.
        r = b.bar_torsion(j_mm4=b.torsion_constant_rect(3, 2))
        self.assertFalse(r["passes"])
        self.assertGreater(r["peak_tip_skew_mm"], 4.0)

    def test_printed_3x12_is_marginal_at_worst_case_eccentricity(self):
        r = b.bar_torsion(j_mm4=b.torsion_constant_rect(3, 12),
                          eccentricity_mm=1.5)
        self.assertFalse(r["passes"], "3x12 must not silently 'pass' at e=W/2")

    def test_sourced_steel_rod_passes_robustly(self):
        g = b.shear_modulus_mpa(b.STEEL_E_MPA, b.STEEL_POISSON)
        r = b.bar_torsion(j_mm4=b.torsion_constant_round(6.0), g_mpa=g,
                          eccentricity_mm=3.0)
        self.assertTrue(r["passes"])
        self.assertLess(r["peak_tip_skew_mm"], b.KEEPER_GATE_STEP_MM / 20.0)

    def test_bar_motor_margin_reproduces_dnd54(self):
        # The bank drive force must match the DND-54 register figure (2.15x).
        r = b.bar_torsion()
        self.assertAlmostEqual(r["motor_margin"], 2.145, places=2)
        self.assertAlmostEqual(r["total_rack_force_n"], 27.968, places=3)

    def test_sensitivity_breaks_even_eccentricity(self):
        s = b.torsion_sensitivity()
        self.assertLess(s["placeholder_eccentricity_break_even_mm"], 0.1)
        self.assertGreater(s["chosen_eccentricity_break_even_mm"], 0.9)
        self.assertLess(s["chosen_eccentricity_break_even_mm"], 1.2)

    def test_carriage_clears_columns_worst_case(self):
        c = b.clearance_stack_up()
        self.assertTrue(c["carriage_clears_columns_worst_case"])
        self.assertGreaterEqual(c["carriage_z_clearance_worst_case_mm"], 0.2)

    def test_comber_rides_between_columns(self):
        c = b.clearance_stack_up()
        self.assertTrue(c["comber_tines_ride_between_columns"])
        self.assertGreater(c["comber_tine_x_gap_mm"], 3.0)
        self.assertTrue(c["comber_body_clear_of_columns"])

    def test_R4_adds_no_pitch_penalty(self):
        p = b.pitch_penalty_check()
        self.assertTrue(p["no_pitch_penalty"])
        self.assertEqual(p["pitch_penalty_mm"], 0.0)

    def test_assembly_verdict_is_honest(self):
        # B1 (bar skew) is EXPECTED to be the only failing assembly gate, and
        # that must be surfaced, not hidden.
        d = b.decide()
        self.assertFalse(d["all_assembly_gates_pass"])
        self.assertFalse(d["gates"]["B1_bar_skew_inside_gate_half"])
        for k in ("B2_carriage_clears_columns_worst_case",
                  "B3_comber_rides_between_columns",
                  "B4_carriage_y_clears_R4_bank", "B5_no_pitch_penalty_at_R4"):
            self.assertTrue(d["gates"][k], k)

    def test_evidence_class_is_cad_plus_calculation_only(self):
        d = b.decide()
        self.assertIn("CAD", d["evidence_class"])
        self.assertIn("CALCULATION", d["evidence_class"])
        self.assertIn("DND-27", d["evidence_class"])
        self.assertIn("DND-27", b.screen()["evidence_class"])

    def test_rack_tooth_gap_is_printable(self):
        # DND-55 correction: the rack gap must clear the one-line floor.
        gap = b.RACK_TOOTH_PITCH_MM - b.RACK_TOOTH_HEIGHT_MM
        self.assertGreaterEqual(gap, 0.44)
        self.assertGreaterEqual(b.RACK_TOOTH_HEIGHT_MM, 0.44)

    def test_scad_has_corrected_rack_and_no_legacy_constants(self):
        text = SCAD.read_text()
        self.assertIn("RACK_TOOTH_PITCH = 1.00", text)
        self.assertIn("RACK_TOOTH_HEIGHT = 0.50", text)
        self.assertNotIn("RACK_TOOTH_PITCH = 0.60", text)

    def test_dnd59_keeper_is_two_lines_and_in_y(self):
        # DND-59: the keeper is re-profiled to 2 lines and moved to +Y; the bank
        # SCAD must carry KEEPER_T = 0.90 and the comber must be clear of it.
        self.assertAlmostEqual(_scad_const("KEEPER_T"), 0.90, places=6)
        self.assertGreaterEqual(reg.KEEPER_LEAF_T_MM, reg.MIN_WALL_MM - 1e-9)
        c = b.clearance_stack_up()
        self.assertTrue(c["comber_clears_keeper_in_y"])
        self.assertGreater(c["comber_clears_keeper_y_mm"], 0.0)
        # the keeper no longer consumes the X-band, so the tine gap grows
        self.assertAlmostEqual(c["comber_tine_x_gap_mm"],
                               b.PITCH_MM - reg.PAWL_T_MM, places=3)

    def test_adr_document_carries_the_decisive_numbers(self):
        self.assertTrue(ADR.exists(), f"missing ADR {ADR}")
        text = ADR.read_text()
        for token in ("R = 4", "0.35", "steel", "DND-55", "NOT a print",
                      "eccentricity"):
            self.assertIn(token, text, f"{token!r} missing from the ADR")


if __name__ == "__main__":
    unittest.main(verbosity=2)
