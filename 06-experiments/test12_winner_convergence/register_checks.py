"""DND-48 - regression checks for the robust S5 readiness register.

The DND-46 adversarial audit (`FALSIFIER_AUDIT.md`) broke three of the six DND-44
closure headlines. DND-48 folds the robust figures back into
`08-current-design/README.md` and the company `plan` document.

These checks fail if either (a) a robust figure is mis-computed, or (b) the
register silently regresses to a DND-44 headline. They assert the register
documents (not just the closure modules) carry the corrected numbers, so a later
edit that reinstates "$424.95 / $75 margin", "<=0.39 N", "1 N -> 0.01 mm" or
"~1e8 cycles" as a *closure* breaks CI.

Evidence class: CALCULATION over the repo's own closure modules. No print.

Run: `python register_checks.py`
"""
from __future__ import annotations

import json
import math
import re
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
REGISTER = (REPO / "08-integrated-designs" / "s5r-shared-drive-register"
            / "README.md")
READINESS = HERE / "DND44_READINESS.md"

sys.path.insert(0, str(HERE))

try:
    import cost_closure as cc
    import buckling_closure as bk
    import cross_cutting_closure as cx
    import timing_closure as tc

    _IMPORT_ERROR = None
except Exception as exc:  # pragma: no cover
    _IMPORT_ERROR = exc


@unittest.skipIf(_IMPORT_ERROR is not None, f"closure modules unavailable: {_IMPORT_ERROR}")
class RegisterFigures(unittest.TestCase):
    """The robust numbers, recomputed from the modules and asserted in the docs."""

    # ------------------------------------------------------------------
    # K5 - cost basis
    # ------------------------------------------------------------------
    def test_k5_robust_planning_basis_is_482_95(self):
        # E5 (spares +15) and E6 (four bundled lines +35) restored from the
        # published $424.95 headline -> the defensible planning number.
        parts = cc.closure()["sourced_parts_usd"] + 15.0 + 35.0
        delivered = parts * cc.UPLIFT
        self.assertAlmostEqual(round(delivered, 2), 482.95, places=2)
        self.assertAlmostEqual(round(500.0 - delivered, 2), 17.05, places=2)

    def test_k5_sourced_driver_variant_is_474_91(self):
        parts = cc.closure()["sourced_parts_usd"] + 80 * (1.3338 - cc.TB6612_SOURCED)
        self.assertAlmostEqual(round(parts * cc.UPLIFT, 2), 474.91, places=2)

    def test_k5_expected_motor_case_is_over_ceiling(self):
        parts = cc.closure()["sourced_parts_usd"] + 15.0 + 35.0 + 80 * (1.25 - 1.05)
        self.assertAlmostEqual(round(parts * cc.UPLIFT, 2), 501.51, places=2)
        self.assertGreater(parts * cc.UPLIFT, 500.0)

    def test_k5_register_carries_robust_basis_not_headline(self):
        text = REGISTER.read_text()
        self.assertIn("$482.95", text)
        self.assertIn("E5 spares + E6 bundled lines restored", text)
        # The DND-44 headline must no longer be presented as the clearing verdict.
        self.assertNotIn("clears, $75.05 margin**", text.replace("— **not defensible as stated**", ""))

    # ------------------------------------------------------------------
    # K1 - buckling service load
    # ------------------------------------------------------------------
    def test_k1_service_load_spans_0p39_to_3p27(self):
        g = bk.G
        mass = 1.0  # kg
        distributed = mass * g / 25.0
        tripod = mass * g / 3.0
        self.assertAlmostEqual(round(distributed, 2), 0.39, places=2)
        self.assertAlmostEqual(round(tripod, 2), 3.27, places=2)
        # The tripod case leaves only ~1.5x margin vs the 4.96 N core.
        self.assertLess(bk.CRITICAL_CORE_1P0_N / tripod, 2.0)

    def test_k1_register_states_the_span_and_tripod_bounding(self):
        text = REGISTER.read_text()
        self.assertIn("0.39–3.27 N/column", text)
        self.assertIn("three-point contact", text)
        self.assertIn("~3.3 N", text)
        self.assertNotIn("distributed tabletop service load ≤ 0.39 N/column (12.7× margin)", text)

    # ------------------------------------------------------------------
    # K8 - lateral free length
    # ------------------------------------------------------------------
    def test_k8_at_40mm_the_gate_load_is_0p28n(self):
        self.assertAlmostEqual(round(cx.lateral_force_for_deflection(0.10, 40.0), 2), 0.28, places=2)
        self.assertAlmostEqual(round(cx.lateral_tip_deflection(1.0, 40.0), 3), 0.356, places=3)

    def test_k8_register_states_the_free_length_reality(self):
        text = REGISTER.read_text()
        self.assertIn("0.356 mm", text)
        self.assertIn("0.28 N", text)
        self.assertIn("40 mm", text)
        self.assertNotIn("1 N → **0.01 mm**", text)

    # ------------------------------------------------------------------
    # K6 - timing conditional
    # ------------------------------------------------------------------
    def test_k6_conditional_on_dwell_and_rate(self):
        req = tc.required_rate_pps(30.0)
        self.assertAlmostEqual(round(req, 1), 267.9, places=1)
        rpm = req * tc.STEP_DEG / 360.0 * 60.0
        self.assertGreater(rpm, 800.0)
        # Design-point pass assumes zero inspection time.
        self.assertLess(30.0 - tc.full_map_s(400.0, tc.TIMING, 3.0), 1.0)

    def test_k6_register_flags_inspection_assumption(self):
        text = REGISTER.read_text()
        self.assertIn(">=268 pps" if ">=268 pps" in text else "≥268 pps", text)
        self.assertIn("inspection_s = 0", text)
        self.assertIn("804 rpm", text)

    # ------------------------------------------------------------------
    # K11 - cycle life span
    # ------------------------------------------------------------------
    def test_k11_defensible_constants_span_4e5_to_1e9(self):
        seen = []
        for eps, m in ((0.003, 8), (0.002, 8), (0.0015, 8), (0.003, 12)):
            strain = (0.05 + 0.20) * 1.5 * 0.45 / 10.0 ** 2
            seen.append((eps / strain) ** m * 1e6)
        self.assertLess(min(seen), 4.0e5 * 1.1)
        self.assertGreater(max(seen), 9.0e8)

    def test_k11_register_states_order_unknown(self):
        text = REGISTER.read_text()
        self.assertIn(">=1e6, order unknown", text)
        self.assertIn("4e5–1e9", text)
        self.assertNotIn("detent leaf ~10⁸ cycles", text)

    # ------------------------------------------------------------------
    # Residual list matches FALSIFIER_AUDIT.md section 8
    # ------------------------------------------------------------------
    def test_residual_ids_match_falsifier_audit_section_8(self):
        audit = (HERE / "FALSIFIER_AUDIT.md").read_text()
        # The §8 table row ids are the contract for the register's residual list.
        for rid in ("K1-service", "K1-abuse", "K5-basis", "K7", "K6-rate",
                    "K6-dwell", "K8-free", "K8-shear", "K9", "K11-span", "R1", "R2"):
            self.assertIn(rid, audit, f"{rid} missing from FALSIFIER_AUDIT.md")
        register = REGISTER.read_text()
        for rid in ("K1-service", "K1-abuse", "K5-basis", "K7", "K6-rate",
                    "K6-dwell", "K8-free", "K8-shear", "K9", "K11-span", "R1", "R2"):
            self.assertIn(rid, register, f"{rid} missing from the register")

    def test_readiness_doc_banner_flags_supersession(self):
        text = READINESS.read_text()
        self.assertIn("DND-48", text)
        self.assertIn("Superseded in part", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
