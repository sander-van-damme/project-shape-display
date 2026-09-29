"""DND-71 S6-LC regression checks -- locks the low-cost machine's reasoning.

Run: python s6lc_checks.py
Exit 0 if every check holds, 1 otherwise. Pure calculation over the model in
s6lc.py plus the sourced FDM limits; no print, no measurement (DND-27).
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "tools" / "fdm-limits"))

import s6lc  # noqa: E402

FAILURES: list[str] = []
CHECKS = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global CHECKS
    CHECKS += 1
    if cond:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name}  {detail}")
        FAILURES.append(name)


def main() -> int:
    fit = s6lc.column_fit()
    pawl = s6lc.pawl_spring()
    rel = s6lc.release_force()
    struct = s6lc.structural_release_limit_n()
    lift = s6lc.lift_axis()
    reset = s6lc.reset_carriage_axis()
    tm = s6lc.timing()
    b = s6lc.bom()
    sens = s6lc.sensitivity()
    dec = s6lc.decide()

    print("S6-LC low-cost machine checks")
    print("=" * 30)
    print("[1] Product gates")
    check("grid is 80x80 = 6400 cells",
          s6lc.ROWS == 80 and s6lc.COLS == 80 and s6lc.CELLS == 6400)
    check("pitch is 5.08 mm", s6lc.PITCH_MM == 5.08)
    check("travel >= 40 mm", s6lc.TRAVEL_MM >= 40.0)
    check("active area ~= 406.4 mm", abs(s6lc.ACTIVE_MM - 406.4) < 1e-9)

    print("[2] Cell fit / printability (DND-97/A1 owned half-lane)")
    check("column body is a robust wall", fit["column_wall_ok"])
    check("pawl LEAF + clearance fits the OWNED half-lane",
          fit["leaf_plus_clearance_mm"] <= fit["owned_lane_mm"],
          f"{fit['leaf_plus_clearance_mm']} <= {fit['owned_lane_mm']}")
    check("pawl root block declared outboard of the pitch band",
          fit["root_outboard"])
    check("inter-column gap is >= 1 line", fit["inter_body_gap_mm"] >= 0.44)
    check("cell fits overall", fit["fits"])

    print("[3] Pawl release + HOLD force (DND-97/A2)")
    check("pawl leaf section is the CAD leaf (0.45 mm)",
          pawl["leaf_t_mm"] == 0.45, f"{pawl['leaf_t_mm']}")
    check("per-pawl release <= S1 design ceiling",
          rel["under_design_ceiling"], f"{rel['per_cell_n']} N")
    check("pawl HOLDS the column via the P1 hard-stop latch",
          pawl["holds"], f"allow {pawl['latch_hold_allow_n']} vs {pawl['hold_required_n']}")
    check("banked all-armed force <= independent structural limit",
          rel["banked_ok"],
          f"{rel['banked_all_armed_n']} N vs {rel['banked_ceiling_n']} N")
    check("structural limit is comb-tooth bending (not 296 N circular)",
          abs(rel["banked_ceiling_n"] - 296.0) > 1.0
          and "CALCULATION" in rel["banked_ceiling_evidence"],
          f"{rel['banked_ceiling_n']} N")
    # DND-97/A2: with the corrected (8x softer) leaf the UNBANKED all-armed force
    # is now WITHIN the structural limit, so banking is no longer FORCE-required.
    # It is retained for reset mechanics and to bound the per-bank reset torque.
    check("unbanked all-armed is now within the structural limit (soft pawl)",
          rel["unbanked_all_armed_n"] <= rel["banked_ceiling_n"],
          f"unbanked {rel['unbanked_all_armed_n']} N <= {rel['banked_ceiling_n']} N")

    print("[4] Lift axis (DND-74 branch 1: global broadcast kept)")
    check("lift_axis is sized on the WHOLE board (6400 cells)",
          lift["cells_lifted"] == s6lc.CELLS, f"{lift['cells_lifted']}")
    check("lead <= 2 mm (DND-43)", lift["lead_mm"] <= 2.0)
    check("lift torque under motor rating", lift["passes"],
          f"{lift['torque_needed_nm']} Nm vs {lift['motor_torque_nm']}")
    check("lift torque margin >= 1.3x", lift["margin"] >= 1.3, f"{lift['margin']}x")
    check("global load is 6400 x 0.4 N = 2560 N",
          abs(lift["load_n"] - 2560.0) < 1e-6)

    print("[4b] Reset-carriage axis (previously ungated)")
    check("reset carriage load is one bank (800 cells)",
          reset["cells_released"] == s6lc.CELLS_PER_BANK)
    check("reset torque under the small-stepper rating", reset["passes"],
          f"{reset['torque_needed_nm']} Nm vs {reset['motor_torque_nm']}")
    check("reset torque margin >= 1.3x", reset["margin"] >= 1.3, f"{reset['margin']}x")

    print("[5] Full-map timing (mask index + carriage traverse priced)")
    check("mask-index term is priced", tm["mask_index_s"] > 0.0)
    check("carriage-traverse term is priced", tm["carriage_traverse_s"] > 0.0)
    check("full map < 30 s", tm["clears_30s"], f"{tm['full_map_s']} s")
    check("timing margin >= 10 s", tm["margin_s"] >= 10.0, f"{tm['margin_s']} s")
    check("timing uses 4 global strokes", tm["strokes"] == 4)

    print("[6] Cost (purchased parts, excl. printed)")
    check("six honest allowance lines present",
          sum(1 for r in b["lines"] if r["evidence"] == "allowance") == 6,
          f"{sum(1 for r in b['lines'] if r['evidence'] == 'allowance')} lines")
    check("purchased parts < $250", b["clears_parts"], f"${b['purchased_parts_usd']}")
    check("delivered cost is honestly quoted (G6 over the line)",
          not b["clears_delivered"] and b["delivered_usd"] == 263.05,
          f"${b['delivered_usd']}")
    check("no per-cell bought actuator",
          not any(r["qty"] > 10 for r in b["lines"]))
    check("bought actuator count <= 3", b["bought_actuators"] <= 3)
    check("BOM has no line above $40 (no cost cliff)",
          all(r["ext"] <= 40.0 for r in b["lines"]))

    print("[7] Adversarial headroom")
    check("release-force headroom >= 100 N", sens["release_force_headroom_n"] >= 100.0)
    check("min platen speed for 30 s is low (robust)",
          sens["min_platen_speed_mm_s_for_30s"] < 5.0)
    check("cost headroom <= $0 (G6 honestly over the line)",
          sens["cost_headroom_delivered_usd"] <= 0.0,
          f"${sens['cost_headroom_delivered_usd']}")

    print("[7b] Reliability gate G8 (DND-97/A6)")
    rg = s6lc.reliability()
    check("per-cell break-even for a 99% map is ~1.57e-6",
          abs(rg["per_cell_error_break_even"] - 1.570e-6) < 1e-9,
          f"{rg['per_cell_error_break_even']}")
    check("reliability is explicitly UNRESOLVED analytically",
          not rg["satisfied_analytically"])
    check("reliability names the coupon-C1 measurement path",
          "C1" in rg["evidence_path"])

    print("[8] Decision (mission gate vs internal delivered convention)")
    # DND-97: DND-70's mission gate is the PURCHASED figure ("under 250$ excluding
    # 3d printed parts"). The repo's delivered convention (G6) is stricter and
    # over the line; both must be reported honestly.
    check("G3 lift-axis passes on the full board", dec["gates"]["G3_lift_axis_torque"])
    check("G4 timing passes with the priced overheads", dec["gates"]["G4_full_map_under_30s"])
    check("G7 reset-carriage gate passes", dec["gates"]["G7_reset_carriage_torque"])
    check("G5 mission gate (purchased parts) PASSES", dec["mission_gate_pass"],
          f"${dec['parts_usd']}")
    check("G6 delivered convention is honestly reported as over the line",
          dec["delivered_convention_under_250"] is False,
          f"${dec['delivered_usd']}")
    check("G8 reliability is reported unresolved",
          dec["g8_reliability_pass"] is False)
    check("all mission gates pass",
          dec["all_mission_gates_pass"], str(dec["mission_gates"]))
    check("verdict is PROMOTE_TO_09_WITH_MEASUREMENT_GATE",
          dec["verdict"] == "PROMOTE_TO_09_WITH_MEASUREMENT_GATE",
          dec["verdict"])

    print("=" * 30)
    print(f"{CHECKS - len(FAILURES)}/{CHECKS} checks passed")
    if FAILURES:
        print("FAILED: " + ", ".join(FAILURES))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
