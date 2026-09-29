"""Regression + honesty gates for the DND-54 S5-R register model.

Run: python s5r_register_checks.py
Standard library only (imports the s5r_register module).

These checks fail if (a) a gate figure is mis-computed, (b) the S5-R verdict
silently regresses to "promotable" on a broken assumption, or (c) the evidence
class is mislabelled as anything but CAD + CALCULATION. They also assert the ADR
document carries the decisive numbers, so a later edit that quietly changes the
verdict without updating the record breaks CI.
"""
from __future__ import annotations

import unittest
from pathlib import Path

import s5r_register as s

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
ADR = REPO / "07-evidence-and-decisions" / "dnd54-s5r-register-latch.md"


class RegisterChecks(unittest.TestCase):
    def test_constants_match_the_cad_source_of_truth(self):
        # The SCAD file is the CAD source of truth for the printability gate;
        # the model must not drift from it.
        scad = (HERE / "s5r_register.scad").read_text()
        for token in ("PAWL_T = 0.90", "PAWL_LEN = 8.00", "KEEPER_T = 0.45",
                      "KEEPER_OVER_CENTRE = 0.06", "WALL = 0.90",
                      "ROTOR_BORE_CLEAR = 0.40", "RACK_TOOTH_PITCH = 1.00",
                      "RACK_TOOTH_HEIGHT = 0.50", "BAR_D = 6.0"):
            self.assertIn(token, scad, f"{token} missing from s5r_register.scad")

    def test_dnd58_rack_reconciles_to_corrected_pitch(self):
        # DND-58: the DND-55 bank close-out re-dimensioned the rack to
        # pitch 1.00 / tooth 0.50 (0.15 mm gap fuses at a 0.4 mm nozzle); the
        # register's per-stroke advance must follow the PITCH (1.00 mm), not the
        # old tooth height (0.45 mm).
        self.assertEqual(s.RACK_TOOTH_PITCH_MM, 1.00)
        self.assertEqual(s.RACK_TOOTH_HEIGHT_MM, 0.50)
        self.assertEqual(s.RACK_STROKE_MM, 1.00)
        # gap clears one extrusion line
        self.assertGreaterEqual(s.RACK_TOOTH_PITCH_MM - s.RACK_TOOTH_HEIGHT_MM,
                                s.MIN_FEATURE_MM)
        # the timing pass is angular, so the pitch change does not move it
        t = s.timing(s.ROWS_IN_BANK)
        self.assertEqual(t["rack_stroke_mm"], 1.00)
        self.assertAlmostEqual(t["full_map_s5r_s"], 24.615, places=3)

    def test_dnd58_drive_bar_is_sourced_steel(self):
        # The printed 3x2 placeholder is refuted (DND-55); the bar is a sourced
        # steel rod d=6. The model must declare that section, not a printed one.
        self.assertEqual(s.BAR_D_MM, 6.0)
        self.assertIn("steel", s.BAR_MATERIAL)
        b = s.bom(s.ROWS_IN_BANK)
        self.assertEqual(b["steel_rod_count"], 1)
        self.assertGreater(b["rod_parts_usd"], 0.0)

    def test_pawl_is_low_force_and_printable_two_lines(self):
        p = s.pawl_spring()
        self.assertLess(p["force_n"], 0.10, "pawl force must stay small")
        self.assertGreaterEqual(s.PAWL_T_MM, s.MIN_WALL_MM - 1e-9,
                                "load-bearing pawl must be >= 2 extrusion lines")

    def test_cell_fit_passes_with_print_margin(self):
        f = s.cell_fit()
        self.assertTrue(f["fits_worst_case"])
        self.assertGreaterEqual(f["tip_gap_worst_mm"], 0.20)

    def test_no_neighbour_crosstalk_is_a_gap_not_a_force(self):
        x = s.neighbour_crosstalk()
        self.assertTrue(x["no_contact"])
        self.assertEqual(x["dropped_pawl_rack_force_n"], 0.0)
        self.assertGreater(x["gap_after_lash_mm"], 0.0)

    def test_writer_solenoid_has_margin(self):
        w = s.writer_budget()
        self.assertTrue(w["pass_gate"])
        self.assertGreater(w["margin"], 5.0)

    def test_bank_drive_passes_with_two_motors_and_fails_with_one(self):
        b = s.bank_drive_load(s.ROWS_IN_BANK)
        self.assertTrue(b["pass_gate"])
        self.assertGreater(b["margin"], 1.5)
        # The sensitivity number: one motor alone would be marginal (<1.1x).
        sens = s.sensitivity(s.ROWS_IN_BANK)
        self.assertLess(sens["bank_torque_margin_at_chosen"], 1.2)

    def test_latch_inherits_the_k1_bound_unchanged(self):
        lat = s.latch_holding_vs_service()
        self.assertTrue(lat["inherits_k1_bound"])
        self.assertEqual(lat["latch_load_in_service_n"], 0.0)
        self.assertAlmostEqual(lat["k1_service_bounding_n"], 3.27, places=2)

    def test_full_map_under_30s_with_margin(self):
        t = s.timing(s.ROWS_IN_BANK)
        self.assertTrue(t["clears_30s"])
        self.assertLess(t["full_map_s5r_s"], 30.0)
        self.assertGreater(t["margin_to_30s_s"], 3.0)

    def test_s5_reference_is_reproduced(self):
        t = s.timing(s.ROWS_IN_BANK)
        self.assertAlmostEqual(t["full_map_s5_reference_s"], 26.251, places=3)

    def test_cost_clears_with_large_margin(self):
        b = s.bom(s.ROWS_IN_BANK)
        self.assertTrue(b["clears"])
        self.assertLess(b["delivered_usd"], 450.0)
        self.assertLess(b["actuator_count"], 80)

    def test_block_channels_priced_once_and_claim_reproduces(self):
        # DND-56: the fixed no-channel base has the 80-motor line AND the
        # 80-channel TB6612 block removed, so the S5-R block must price its OWN
        # channels exactly once (no double-count). The $397.53 DND-54 claim must
        # still reproduce as the channels-unpriced sub-field.
        b = s.bom(s.ROWS_IN_BANK)
        self.assertEqual(b["delivered_claim_usd"], 397.53)
        self.assertEqual(b["parts_claim_usd"], 342.70)
        self.assertAlmostEqual(b["channel_parts_usd"], 3.09, places=2)
        # 2 bank H-bridge ICs + 5 darlington writer chips.
        self.assertEqual(b["bank_ic_count"], 2)
        self.assertEqual(b["writer_chip_count"], 5)
        # The DND-56 ratification total (channels priced, rod unpriced) is kept
        # as `delivered_no_rod_usd` so that figure still reproduces.
        self.assertAlmostEqual(b["delivered_no_rod_usd"],
                               b["delivered_claim_usd"] + 3.09 * s.cc.UPLIFT,
                               places=1)
        self.assertEqual(b["delivered_no_rod_usd"], 401.12)
        # DND-58 honest working total adds the 1 sourced steel drive rod.
        self.assertEqual(b["steel_rod_count"], 1)
        self.assertAlmostEqual(b["delivered_usd"],
                               b["delivered_no_rod_usd"] + 3.00 * s.cc.UPLIFT,
                               places=1)
        self.assertEqual(b["delivered_usd"], 404.60)
        self.assertEqual(b["margin_usd"], 95.40)
        self.assertTrue(b["clears"])

    def test_endurance_is_reported_with_order_unknown_label(self):
        e = s.endurance(s.ROWS_IN_BANK)
        self.assertEqual(e["label"], ">=1e6, order unknown")
        self.assertLess(e["cycles_span"][0], 4.0e6 * 1.05)
        self.assertGreater(e["cycles_span"][1], 9.0e7)

    def test_verdict_is_all_gates_and_is_promotable(self):
        d = s.decide()
        self.assertTrue(all(d["gates"].values()), d["gates"])
        self.assertTrue(d["promotable"])
        self.assertEqual(d["verdict"], "PROMOTE_TO_08")

    def test_evidence_class_is_cad_plus_calculation_only(self):
        d = s.decide()
        self.assertIn("CAD", d["evidence_class"])
        self.assertIn("CALCULATION", d["evidence_class"])
        self.assertIn("DND-27", d["evidence_class"])
        screen = s.screen()
        self.assertIn("DND-27", screen["evidence_class"])

    def test_sensitivity_reports_the_discriminating_numbers(self):
        sens = s.sensitivity(s.ROWS_IN_BANK)
        # Timing flips below ~468 deg/s crank at the chosen settle.
        self.assertGreater(sens["timing_min_crank_deg_s_for_30s"], 400.0)
        self.assertLess(sens["timing_min_crank_deg_s_for_30s"], 900.0)
        # Fit tolerates far more than the +/-0.1 mm assumed print error.
        self.assertGreater(sens["max_dim_accuracy_for_fit_mm"],
                           2.0 * s.DIM_ACCURACY_MM)

    def test_adr_document_carries_the_decisive_numbers(self):
        self.assertTrue(ADR.exists(), f"missing ADR {ADR}")
        text = ADR.read_text()
        for token in ("S5-R", "R = 4", "24.6", "397.53",
                      "DND-54", "NOT a print", "PROMOTE",
                      "404.60", "pitch 1.00", "steel rod", "DND-58"):
            self.assertIn(token, text, f"{token!r} missing from the ADR")

    def test_dnd58_adr_exists_and_carries_the_reconciliation(self):
        adr = REPO / "07-evidence-and-decisions" / "dnd58-s5r-register-reconcile.md"
        self.assertTrue(adr.exists(), f"missing ADR {adr}")
        text = adr.read_text()
        for token in ("pitch 1.00", "0.50", "RACK_STROKE_MM", "steel rod",
                      "404.60", "R-DND55-4", "closed", "NOT a print",
                      "24.62"):
            self.assertIn(token, text, f"{token!r} missing from the DND-58 ADR")


if __name__ == "__main__":
    unittest.main(verbosity=2)
