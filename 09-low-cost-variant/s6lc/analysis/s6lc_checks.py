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
    lift = s6lc.lift_axis()
    rc = s6lc.reset_carriage()
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

    print("[2] Cell fit / printability (DND-93/A1 owned half-lane)")
    check("column body is a robust wall", fit["column_wall_ok"])
    check("pawl LEAF + clearance fits the OWNED half-lane",
          fit["leaf_plus_clearance_mm"] <= fit["owned_lane_mm"],
          f"{fit['leaf_plus_clearance_mm']} <= {fit['owned_lane_mm']}")
    check("pawl root block is outboard of the pitch band", fit["root_outboard"])
    check("inter-column gap is >= 1 line", fit["inter_body_gap_mm"] >= 0.44)
    check("cell fits overall", fit["fits"])

    print("[3] Pawl release + HOLD force (DND-93/A2)")
    check("pawl leaf section is the CAD leaf (0.45 mm)",
          pawl["leaf_t_mm"] == 0.45, f"{pawl['leaf_t_mm']}")
    check("per-pawl release <= S1 design ceiling",
          rel["under_design_ceiling"], f"{rel['per_cell_n']} N")
    check("pawl HOLDS the column via the P1 hard-stop latch",
          pawl["holds"], f"allow {pawl['latch_hold_allow_n']} vs {pawl['hold_required_n']}")
    check("banked release within a computed structural ceiling (not circular)",
          rel["banked_ok"], f"{rel['banked_all_armed_n']} vs {rel['banked_ceiling_n']}")
    check("banked reset remains the binding force case (ceiling is per-tooth)",
          rel["per_tooth_load_n"] < rel["comb_tooth_limit_n"],
          f"tooth {rel['per_tooth_load_n']} < {rel['comb_tooth_limit_n']}")

    print("[4] Lift axis (DND-93/A7 full-board load)")
    check("lead <= 2 mm (DND-43)", lift["lead_mm"] <= 2.0)
    check("lift lifts the WHOLE board (6400 cells)",
          lift["cells_lifted"] == s6lc.CELLS, f"{lift['cells_lifted']}")
    check("lift torque under motor rating", lift["passes"],
          f"{lift['torque_needed_nm']} Nm vs {lift['motor_torque_nm']}")
    check("lift torque margin >= 1.3x", lift["margin"] >= 1.3, f"{lift['margin']}x")
    check("reset-carriage torque under its motor", rc["passes"],
          f"{rc['torque_needed_nm']} Nm vs {rc['motor_rated_nm']}")

    print("[5] Full-map timing (DND-93/A4 mask+carriage priced)")
    check("full map < 30 s", tm["clears_30s"], f"{tm['full_map_s']} s")
    check("timing margin >= 10 s", tm["margin_s"] >= 10.0, f"{tm['margin_s']} s")
    check("timing uses 4 global strokes", tm["strokes"] == 4)

    print("[6] Cost (purchased parts, excl. printed; DND-70 mission gate)")
    check("purchased parts < $250 (mission gate)", b["clears_parts"],
          f"${b['purchased_parts_usd']}")
    check("no per-cell bought actuator",
          not any(r["qty"] > 10 for r in b["lines"]))
    check("bought actuator count == 3", b["bought_actuators"] == 3)
    check("BOM has no line above $40 (no cost cliff)",
          all(r["ext"] <= 40.0 for r in b["lines"]))

    print("[7] Adversarial headroom (DND-93)")
    check("release-force headroom >= 100 N",
          sens["release_force_headroom_n"] >= 100.0,
          f"{sens['release_force_headroom_n']}")

    print("[8] Decision (DND-93 gates)")
    check("all analytic gates pass", dec["all_gates_pass"],
          str(dec["gates"]))
    check("G7 reliability is explicitly UNRESOLVED (measurement-only)",
          not dec["g7_reliability_pass"])
    check("verdict reflects the measurement gate",
          dec["verdict"] == "PROMOTE_TO_09_WITH_MEASUREMENT_GATE",
          dec["verdict"])
    check("delivered overrun is reported, not hidden",
          dec["g6_delivered_under_250"] is False,
          f"delivered ${dec['g6_delivered_usd']}")

    print("=" * 30)
    print(f"{CHECKS - len(FAILURES)}/{CHECKS} checks passed")
    if FAILURES:
        print("FAILED: " + ", ".join(FAILURES))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
