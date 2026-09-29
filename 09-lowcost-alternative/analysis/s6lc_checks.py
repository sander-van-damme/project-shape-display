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

    print("[2] Cell fit / printability")
    check("column body is a robust wall", fit["column_wall_ok"])
    check("pawl + bleed fits the lane", fit["pawl_plus_bleed_mm"] <= fit["lane_free_mm"])
    check("gate + bleed fits the lane", fit["gate_plus_bleed_mm"] <= fit["lane_free_mm"])
    check("inter-column gap is >= 1 line", fit["x_gap_mm"] >= 0.44)
    check("cell fits overall", fit["fits"])

    print("[3] Pawl release force (S1-B banked)")
    check("per-pawl force <= S1 design ceiling",
          rel["under_design_ceiling"], f"{rel['per_cell_n']} N")
    check("banked all-armed force <= 296 N",
          rel["banked_ok"], f"{rel['banked_all_armed_n']} N")
    check("banking is required (unbanked exceeds ceiling)",
          rel["unbanked_all_armed_n"] > 296.0)

    print("[4] Lift axis")
    check("lead <= 2 mm (DND-43)", lift["lead_mm"] <= 2.0)
    check("lift torque under motor rating", lift["passes"],
          f"{lift['torque_needed_nm']} Nm vs {lift['motor_torque_nm']}")
    check("lift torque margin >= 1.3x", lift["margin"] >= 1.3)

    print("[5] Full-map timing")
    check("full map < 30 s", tm["clears_30s"], f"{tm['full_map_s']} s")
    check("timing margin >= 10 s", tm["margin_s"] >= 10.0, f"{tm['margin_s']} s")
    check("timing uses 4 global strokes", tm["strokes"] == 4)

    print("[6] Cost (purchased parts, excl. printed)")
    check("purchased parts < $250", b["clears_parts"], f"${b['purchased_parts_usd']}")
    check("delivered < $250", b["clears_delivered"], f"${b['delivered_usd']}")
    check("delivered margin >= $50", b["margin_delivered_usd"] >= 50.0,
          f"${b['margin_delivered_usd']}")
    check("no per-cell bought actuator",
          not any(r["qty"] > 10 for r in b["lines"]))
    check("bought actuator count <= 3", b["bought_actuators"] <= 3)
    check("BOM has no line above $30 (no cost cliff)",
          all(r["ext"] <= 30.0 for r in b["lines"]))

    print("[7] Adversarial headroom")
    check("cost headroom >= $60 delivered",
          sens["cost_headroom_delivered_usd"] >= 60.0)
    check("release-force headroom >= 100 N", sens["release_force_headroom_n"] >= 100.0)
    check("min platen speed for 30 s is low (robust)",
          sens["min_platen_speed_mm_s_for_30s"] < 5.0)

    print("[8] Decision")
    check("all six gates pass", dec["all_gates_pass"])
    check("verdict is PROMOTE_TO_09", dec["verdict"] == "PROMOTE_TO_09")

    print("=" * 30)
    print(f"{CHECKS - len(FAILURES)}/{CHECKS} checks passed")
    if FAILURES:
        print("FAILED: " + ", ".join(FAILURES))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
