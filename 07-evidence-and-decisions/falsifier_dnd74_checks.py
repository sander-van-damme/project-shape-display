#!/usr/bin/env python3
"""DND-74 falsifier findings — RESOLUTION gate (DND-93).

Run from anywhere:  python 07-evidence-and-decisions/falsifier_dnd74_checks.py

The original DND-74 gate asserted the S6-LC *break* (G3 lift gate computed on
1/8 the load; circular ceiling; cost-headroom collapse; mask-write load-bearing;
reliability roll). DND-93 repairs it. This gate locks the RESOLVED state for the
DND-74-specific findings so they cannot drift back. Companion to
`falsifier_dnd91_checks.py` (the A1/A2/A3/A6 resolution gate).

Evidence class: CALCULATION over the repo's own S6-LC model. No print, purchase
or measurement (DND-27). See 07-evidence-and-decisions/dnd93-s6lc-repair.md.
"""
from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
S6LC_PY = REPO / "09-low-cost-variant" / "s6lc" / "analysis" / "s6lc.py"

FAILURES: list[str] = []
CHECKS = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global CHECKS
    CHECKS += 1
    print(("  PASS  " if cond else "  FAIL  ") + name + (f"  {detail}" if detail else ""))
    if not cond:
        FAILURES.append(name)


def _torque(force_n: float, lead_mm: float, eff: float = 0.5) -> float:
    return force_n * (lead_mm / 1000.0) / (2 * math.pi * eff)


def main() -> int:
    spec = importlib.util.spec_from_file_location("s6lc_dnd74", S6LC_PY)
    s6 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(s6)

    print("DND-74 falsifier findings - RESOLUTION gate (DND-93)")
    print("=" * 52)
    lift = s6.lift_axis()
    rel = s6.release_force()
    tm = s6.timing()
    b = s6.bom()
    dec = s6.decide()

    # --- G3 lift-axis: RESOLVED ------------------------------------------
    print("[A2] Lift-axis sizing -- RESOLVED (whole board, honest load)")
    check("lift_axis now lifts the WHOLE board (6400 cells)",
          lift["cells_lifted"] == s6.CELLS,
          f"cells_lifted={lift['cells_lifted']}")
    check("per-column load is the honest stack-up, not 0.4 N",
          lift["per_column_load_n"] < 0.4,
          f"{lift['per_column_load_n']} N/col")
    check("lift torque passes on the 0.30 Nm NEMA17",
          lift["passes"], f"{lift['torque_needed_nm']} vs {lift['motor_torque_nm']} Nm")
    check("lift torque margin >= 1.3x", lift["margin"] >= 1.3, f"{lift['margin']}x")
    # historical: the 2,560 N audit bound at 0.4 N/col exceeded the motor
    check("historical: 6400 x 0.4 N = 2560 N needs 1.63 Nm (audit bound)",
          abs(_torque(s6.CELLS * 0.4, s6.LEAD_MM) - 1.63) < 0.01,
          f"{_torque(s6.CELLS * 0.4, s6.LEAD_MM):.2f} Nm")
    check("model no longer codes lift on one bank (800 cells)",
          lift["cells_lifted"] != s6.CELLS_PER_BANK == 800)

    # --- Release ceiling: RESOLVED ---------------------------------------
    print("[A5] Release-force ceiling -- RESOLVED (computed, not circular)")
    check("ceiling is NOT the borrowed 296.0",
          rel["banked_ceiling_n"] != 296.0, f"{rel['banked_ceiling_n']}")
    check("ceiling is min(tooth*teeth, reset-motor force)",
          abs(rel["banked_ceiling_n"] -
              min(rel["comb_tooth_limit_n"] * rel["teeth_in_bank_comb"],
                  rel["reset_motor_force_n"])) < 0.15)
    check("ceiling is labelled assumption-class",
          "assumption" in rel["banked_ceiling_class"])
    check("banked release is within the computed ceiling", rel["banked_ok"])

    # --- Cost headroom: RESOLVED (repriced + capabilities listed) ---------
    print("[A1] Cost ladder honesty -- RESOLVED")
    check("base no longer quotes the soft $139.77 parts",
          b["purchased_parts_usd"] != 139.77, f"${b['purchased_parts_usd']}")
    check("purchased parts still < $250 (mission gate)", b["clears_parts"],
          f"${b['purchased_parts_usd']}")
    check("the six unlisted capabilities are now BOM lines",
          all(any(k in r["item"] for r in b["lines"]) for k in
              ("Mask media", "puncher", "linkage", "traverse rails",
               "splice", "home sensors")))
    check("delivered is reported (not hidden) even when over $250",
          dec["g6_delivered_usd"] == b["delivered_usd"])

    # --- Mask write / regional: product statement retained ---------------
    print("[A3] Mask write / regional -- product statement retained")
    ops = 3200 * (s6.LEVELS - 1)
    check("serial punch is still hopeless (>>30 s)", ops * 0.20 > 300.0,
          f"{ops * 0.20:.0f} s")
    check("mask prep is still stated off the visible budget",
          any("off" in r.lower() and "mask" in r.lower()
              or "mask" in r.lower() and "budget" in r.lower()
              for r in dec["residual_uncertainty"]))

    # --- Reliability: ADDRESSED via G7 -----------------------------------
    print("[A4] Per-cell reliability -- ADDRESSED (G7)")
    p_all = (1 - 1e-4) ** s6.CELLS
    check("at 0.01% per-cell error P(all 6400) ~= 52.7%",
          abs(p_all - 0.527) < 0.01, f"{p_all:.4f}")
    check("a G7 reliability field exists and is UNRESOLVED",
          "g7_reliability_pass" in dec and dec["g7_reliability_pass"] is False)

    # --- Timing: RESOLVED (mask/carriage priced) -------------------------
    print("[A6] Timing completeness -- RESOLVED")
    check("mask-index time is priced", hasattr(s6, "MASK_INDEX_S"))
    check("carriage-traverse time is priced", hasattr(s6, "CARRIAGE_TRAVERSE_S"))
    check("full map still < 30 s", tm["clears_30s"], f"{tm['full_map_s']} s")

    # --- Pawl load holding: RESOLVED (hold gate) -------------------------
    print("[A7] Pawl load holding -- RESOLVED")
    check("a hold gate exists", "holds" in s6.pawl_spring())
    check("the pawl holds via the P1 hard-stop latch", s6.pawl_spring()["holds"])

    print("=" * 52)
    print(f"{CHECKS - len(FAILURES)}/{CHECKS} resolution checks passed")
    if FAILURES:
        print("FAILED: " + ", ".join(FAILURES))
        return 1
    print("All DND-74 findings are RESOLVED and locked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
