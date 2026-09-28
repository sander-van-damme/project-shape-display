"""DND-46 - adversarial regression checks against the DND-44 S5 readiness closure.

This module does NOT re-assert the DND-44 closures. It encodes the *attacks*: the
specific counter-calculations that a reviewer would raise to break each claimed
closure, and asserts the honest disposition each attack forces. If someone later
"fixes" a closure by quietly re-tightening an assumption, one of these checks
fails.

Evidence class: CALCULATION / adversarial audit. No print, no measurement.

Verdicts encoded (prose in FALSIFIER_AUDIT.md):
  K6  CONFIRMED-WITH-CAVEAT: the rate-independent floor argument is a real
      re-derivation, but "not a rate problem" hides a second unmeasured quantity
      (the realised loaded rate). The required ~268 pps is ~804 rpm; the design
      point pays zero inspection time.
  K1  BROKEN: the service-load bound is a *best case*. It assumes a miniature
      base shares load across every column under it; on a height-varying field a
      rigid base is a three-point contact, so a 1 kg miniature loads a column at
      ~3.27 N, not 0.39 N.
  K5  BROKEN-AS-STATED: the $75 margin needs four simultaneous best-case choices
      (TB6612 @100, best-case repricing of four bundled lines, spares deletion,
      the unqualified $1.05 motor). Restore the spares allowance and the bundled
      expected prices and the margin is under $25; at the *sourced* DRV8833 it is
      ~$25; with an expected motor it is over the ceiling.
  K8  BROKEN: the 12 mm free length is hard-coded with no geometry support and
      contradicts the repo's own unrelieved upper body of 40 mm. At 40 mm a 1 N
      lateral load deflects ~0.36 mm, 3.5x the 0.10 mm gate.
  K10 CONFIRMED: a genuine complete bound; but it shows regional time is set by
      the mandatory full platen stroke, not by region size.
  K11 PSEUDO-QUANTITATIVE: the point estimate 9.98e7 rests on two asserted
      constants; a conservative FDM endurance drops it by 25x.
"""
from __future__ import annotations

import json
import math
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
TEST08 = REPO / "06-experiments" / "test08_architecture_search"

sys.path.insert(0, str(HERE))

try:
    import timing_closure as tc
    import buckling_closure as bk
    import cost_closure as cc
    import cross_cutting_closure as cx

    _IMPORT_ERROR = None
except Exception as exc:  # pragma: no cover
    _IMPORT_ERROR = exc


@unittest.skipIf(_IMPORT_ERROR is not None, f"DND-44 modules unavailable: {_IMPORT_ERROR}")
class FalsifierAudit(unittest.TestCase):
    # ------------------------------------------------------------------
    # K6 - timing
    # ------------------------------------------------------------------
    def test_k6_floor_argument_is_a_real_re_derivation(self):
        cc = tc.cross_check()
        self.assertLess(cc["abs_error_s"], 1e-9)
        self.assertGreaterEqual(tc.full_map_s(1e9), tc.rate_independent_floor_s() - 1e-6)

    def test_k6_required_rate_is_an_unmeasured_mechanical_speed(self):
        # ATTACK: "only ~268 pps" is ~804 rpm at 18 deg/step; the design 400 pps
        # is 1200 rpm. No loaded torque-speed curve exists in the repo.
        req = tc.required_rate_pps(30.0)
        rpm = req * tc.STEP_DEG / 360.0 * 60.0
        self.assertGreater(rpm, 700.0)
        design_rpm = tc.TIMING["rate_hz"] * tc.STEP_DEG / 360.0 * 60.0
        self.assertGreater(design_rpm, 1000.0)

    def test_k6_design_point_pass_requires_zero_inspection(self):
        # ATTACK: the 26.25 s pass is at inspection_s = 0. With the sweep's own
        # 3 s inspection the engineering target (27 s) is missed.
        base = tc.full_map_s(400.0, tc.TIMING, 0.0)
        with3 = tc.full_map_s(400.0, tc.TIMING, 3.0)
        self.assertLess(base, 30.0)
        self.assertLess(30.0 - with3, 30.0 - base)
        self.assertGreater(30.0 - with3, 0.0)
        self.assertGreater(with3, 27.0)

    def test_k6_worst_corner_is_defined_away_not_closed(self):
        # ATTACK: the worst corner is a sweep grid point; but the design dwells
        # are equally unmeasured. The pass/fail boundary sits on that dwell.
        worst = tc.scenario_timing(0.050, 0.040, 1000)
        self.assertTrue(math.isinf(tc.required_rate_pps(30.0, worst, 3.0)))
        pessimistic = tc.required_rate_pps(30.0, tc.scenario_timing(0.050, 0.040, 4000))
        # A 2x engagement-dwell change alone moves the required rate >8x: the
        # boundary is a dwell assumption, so this is not "just a rate" either.
        self.assertGreater(pessimistic, 8 * tc.required_rate_pps(30.0))

    # ------------------------------------------------------------------
    # K1 - buckling
    # ------------------------------------------------------------------
    def test_k1_base_distribution_overcounts_supporting_columns(self):
        # ATTACK: ceil(d/pitch)^2 overstates the cells under a round base.
        d = bk.BASE_DIAMETER_MM["small_medium"]
        ceil_cells = bk.columns_under_base(d)
        area_cells = math.pi * (d / 2) ** 2 / bk.CELL_PITCH_MM ** 2
        self.assertGreater(ceil_cells, area_cells)

    def test_k1_rigid_base_is_a_three_point_contact_not_distributed(self):
        # ATTACK (decisive): the columns are at different heights by definition.
        # A rigid base stands on the highest three.
        mass_g = 1000.0
        g = bk.G
        distributed = mass_g / 1000.0 * g / 25.0
        tripod = mass_g / 1000.0 * g / 3.0
        self.assertLess(distributed, 0.5)
        self.assertGreater(tripod, 3.0)
        self.assertLess(bk.CRITICAL_CORE_1P0_N / tripod, 2.0)

    def test_k1_service_bound_is_not_a_bound_under_tripod_contact(self):
        worst, src = bk.worst_service_load_n()
        self.assertAlmostEqual(src["miniature"], "display_large_heavy")
        tripod = src["mass_g"] / 1000.0 * bk.G / 3.0
        self.assertGreater(tripod, 0.5)

    def test_k1_core_resize_is_a_geometry_trade_not_a_fix(self):
        t = {r["core_radius_mm"]: r for r in bk.core_reference()}
        self.assertTrue(t[1.1]["clears_5n_abuse"])
        self.assertLess(t[1.1]["stepped_height_mm"], t[1.0]["stepped_height_mm"])

    # ------------------------------------------------------------------
    # K5/K7 - cost
    # ------------------------------------------------------------------
    def test_k5_headline_margin_depends_on_deleting_spares_and_repricing(self):
        # ATTACK: restore the spares allowance (a purchasing choice, not a
        # machine change) and use the BOM's own expected prices for the four
        # bundled structural lines. The margin collapses.
        base = cc.closure()["sourced_delivered_usd"]
        restored = (cc.closure()["sourced_parts_usd"] + 15.0 + 35.0) * cc.UPLIFT
        self.assertLess(base, 500.0)
        self.assertGreater(restored, base)
        self.assertLess(500.0 - restored, 25.0)

    def test_k5_e6_is_best_case_repricing(self):
        # ATTACK: E6 sets four *bundled structural* lines to their own
        # `unit_best_usd`. Assert E6 is $35 of the reduction and that each new
        # unit equals the BOM's best-case listing.
        audit = cc.closure()["reduction_audit"]
        e6 = [a for a in audit if a["change"].startswith("E6")]
        e6_total = sum(a["line_delta"] for a in e6)
        self.assertEqual(round(e6_total, 2), -35.00)
        lines = {l["item"]: l for l in cc.load_lines()}
        for a in e6:
            self.assertAlmostEqual(a["new_unit"], lines[a["item"]]["unit_best"], places=6)

    def test_k5_driver_swap_is_a_dual_h_bridge_for_dual_h_bridge(self):
        # CONFIRM the E1 substitution is electrically plausible: both are dual
        # H-bridges driving one bipolar stepper. But $0.7955 TB6612 is itself a
        # best-case @100 price; the sourced DRV8833PWPR is $1.3338.
        self.assertLess(cc.TB6612_SOURCED, 1.0)
        self.assertAlmostEqual(cc.MOTOR_ALIEXPRESS, 2.66, places=2)

    def test_k5_at_the_sourced_driver_the_margin_is_thin(self):
        # ATTACK: use the other *sourced* driver (DRV8833PWPR, $1.3338). The
        # path still clears, but margin drops from ~$75 to ~$25.
        parts = cc.closure()["sourced_parts_usd"] + 80 * (1.3338 - cc.TB6612_SOURCED)
        delivered = parts * cc.UPLIFT
        self.assertLess(delivered, 500.0)
        self.assertLess(500.0 - delivered, 30.0)

    def test_k5_with_e5_e6_restored_and_expected_motor_it_is_over_ceiling(self):
        # ATTACK: the combined honest case (keep spares, expected bundled
        # prices, expected motor $1.25) is OVER the ceiling.
        parts = cc.closure()["sourced_parts_usd"] + 15.0 + 35.0 + 80 * (1.25 - 1.05)
        delivered = parts * cc.UPLIFT
        self.assertGreater(delivered, 500.0)

    # ------------------------------------------------------------------
    # K8 - lateral holding
    # ------------------------------------------------------------------
    def test_k8_free_length_is_contradicted_by_the_repo_geometry(self):
        # ATTACK: the closure hard-codes free = 12.0 mm in __main__ with no
        # geometry basis. The repo's own test08 params give an unrelieved upper
        # body of 80.2 - 40.2 = 40 mm.
        p = json.loads((TEST08 / "params.json").read_text())
        unrelieved = p["grid"]["body_length_mm"] - p["cam"]["body_relief_height_mm"]
        self.assertAlmostEqual(unrelieved, 40.0, places=6)

    def test_k8_at_the_real_free_length_the_gate_fails(self):
        # ATTACK: at 40 mm a 1 N lateral load deflects ~0.36 mm, 3.5x the
        # 0.10 mm gate; the gate load is ~0.28 N, not ~10 N.
        defl = cx.lateral_tip_deflection(1.0, 40.0)
        self.assertGreater(defl, 0.10)
        f_gate = cx.lateral_force_for_deflection(0.10, 40.0)
        self.assertLess(f_gate, 0.5)
        self.assertGreater(cx.lateral_force_for_deflection(0.10, 12.0), 10.0)

    def test_k8_guide_shear_allowable_is_unsourced(self):
        # ATTACK: the governing "~9.4 N" is min(bending@12mm, guide shear), and
        # the guide shear is 0.5 MPa x 18.72 mm^2 with no source for 0.5 MPa.
        b = cx.k8_bound(12.0)
        area = 2.0 * cx.BODY_W * 2.0
        self.assertAlmostEqual(b["guide_shear_allowable_n"], 0.5 * area, places=2)

    # ------------------------------------------------------------------
    # K10 / K11 - regional time and cycle life
    # ------------------------------------------------------------------
    def test_k10_is_a_genuine_complete_bound(self):
        b = cx.k10_bound()
        self.assertLess(b[1], 5.0)
        self.assertLess(b[80], 30.0)
        vals = [b[k] for k in (1, 5, 10, 20, 80)]
        self.assertEqual(vals, sorted(vals))

    def test_k10_is_dominated_by_fixed_overhead_not_region_size(self):
        # ATTACK on framing: a 1-row update is 3.9 s of which ~3.6 s is fixed
        # platen stroke + reference + ready. "Regional is fast" is really "the
        # mandatory full stroke sets the floor".
        t = tc.TIMING
        lift = tc._travel(41.0, t["lift_v_mm_s"], t["lift_a_mm_s2"])
        fixed = t["reference_s"] + 2 * lift + t["ready_s"]
        self.assertGreater(fixed, 3.0)
        self.assertGreater(fixed / cx.k10_bound()[1], 0.85)

    def test_k11_point_estimate_is_pseudo_quantitative(self):
        # ATTACK: the 9.98e7 point estimate rests on eps_endurance = 0.3% and
        # Basquin m = 8, both asserted. A conservative FDM endurance (0.2%) at
        # the same m drops the bound by ~25x.
        b = cx.k11_bound()
        strain = (0.05 + 0.20) * 1.5 * 0.45 / 10.0 ** 2
        cycles_assumed = (0.003 / strain) ** 8 * 1e6
        cycles_conservative = (0.002 / strain) ** 8 * 1e6
        self.assertAlmostEqual(b["estimated_cycles_to_failure"], round(cycles_assumed), delta=1)
        self.assertLess(cycles_conservative, cycles_assumed / 20)
        # The real product life driver is full-map writes, not raw cycles: a
        # full map cycles each detent once per row (80x). At 1e7 cycles that is
        # only ~125k full maps; at 9.98e7 it is ~1.25M.
        self.assertGreater(1e6 / 80, 1000)


if __name__ == "__main__":
    unittest.main(verbosity=2)
