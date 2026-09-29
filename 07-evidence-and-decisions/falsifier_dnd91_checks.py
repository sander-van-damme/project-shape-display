#!/usr/bin/env python3
"""DND-91 falsifier findings — RESOLUTION gate (DND-93 + DND-97).

Run from anywhere:  python 07-evidence-and-decisions/falsifier_dnd91_checks.py

History. The original DND-91 gate asserted the S6-LC *break* (A1..A8). DND-93
fixed G3 and the DND-74/91 bounded findings and re-baselined this gate to keep
A1/A2/A6/A7/A8 "open". DND-97 then repaired the mechanism defects. This gate now
asserts the FULLY RESOLVED state so nothing can drift back to the broken
headline. Companion to `falsifier_dnd74_checks.py`.

  A1 cell-fit lane gate ignores placement -> FIXED: owned half-lane + outboard root
  A2 pawl spring uses the root section   -> FIXED: 0.45 leaf + P1-latch hold gate
  A3 circular 296 N ceiling              -> FIXED (DND-93): comb-tooth limit
  A4 timing unpriced terms               -> FIXED (DND-93): mask + carriage priced
  A5 BOM soft lines / unlisted           -> FIXED (DND-93): repriced + 6 allowances
  A6 no per-cell reliability gate        -> FIXED: G8 added, explicitly UNRESOLVED
  A7 unloaded-write assumption           -> FIXED: restated as an explicit limitation
  A8 regional/jam asserted               -> FIXED: restated as explicit limitations

Evidence class: CALCULATION over the repo's own S6-LC model. No print, no
purchase, no measurement (DND-27). Run from the repo root or anywhere.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
S6LC_ANALYSIS = REPO / "08-integrated-designs" / "s6lc-low-cost" / "analysis"
SCAD = (REPO / "08-integrated-designs" / "s6lc-low-cost" / "scad"
        / "s6lc_machine.scad")

sys.path.insert(0, str(S6LC_ANALYSIS))
sys.path.insert(0, str(REPO / "06-experiments" / "test11_falsification_library"))

import s6lc  # noqa: E402

FAILURES: list[str] = []
CHECKS = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global CHECKS
    CHECKS += 1
    print(("  PASS  " if cond else "  FAIL  ") + name + (f"  {detail}" if detail else ""))
    if not cond:
        FAILURES.append(name)


def main() -> int:
    print("DND-91 falsifier findings - RESOLUTION gate (DND-93 + DND-97)")
    print("=" * 60)

    fit = s6lc.column_fit()
    pawl = s6lc.pawl_spring()
    rel = s6lc.release_force()
    lift = s6lc.lift_axis()
    reset = s6lc.reset_carriage_axis()
    tm = s6lc.timing()
    b = s6lc.bom()
    scad = SCAD.read_text()
    dec = s6lc.decide()
    rg = s6lc.reliability()

    # ---- A1: cell fit now gates the OWNED half-lane ----------------------
    print("[A1] Cell fit / lane budget -- RESOLVED (DND-97)")
    owned_lane = s6lc.PITCH_MM / 2 - s6lc.COLUMN_BODY_MM / 2
    check("owned lane to half-pitch is 0.74 mm", abs(owned_lane - 0.74) < 1e-9,
          f"{owned_lane:.3f}")
    check("model exposes the OWNED lane", abs(fit["owned_lane_mm"] - 0.74) < 1e-9)
    check("pawl LEAF (0.45) + clearance fits the owned lane",
          fit["leaf_plus_clearance_mm"] <= fit["owned_lane_mm"],
          f"{fit['leaf_plus_clearance_mm']} <= {fit['owned_lane_mm']}")
    check("root block declared outboard of the pitch band", fit["root_outboard"])
    check("SCAD no longer places the pawl at BODY/2 + 0.10",
          "BODY/2 + 0.10" not in scad, "placement corrected")
    check("cell fits overall", fit["fits"])
    # historical counter-number retained
    check("historical: the OLD 0.90 pawl overflowed by 0.260 mm",
          abs(((s6lc.COLUMN_BODY_MM / 2 + 0.10 + 0.90) - s6lc.PITCH_MM / 2) - 0.26) < 1e-9)

    # ---- A2: spring uses the leaf + a hold gate --------------------------
    print("[A2] Pawl spring section + hold -- RESOLVED (DND-97)")
    k_leaf = s6lc._cantilever_rate_n_per_mm(pawl["leaf_t_mm"], s6lc.PAWL_W_MM, s6lc.PAWL_L_MM)
    check("model k uses the 0.45 mm leaf (~0.0801 N/mm)",
          abs(k_leaf - 0.0801) < 1e-3, f"{k_leaf:.4f}")
    check("release ~= 0.020 N", abs(pawl["release_force_n"] - 0.02) < 1e-3,
          f"{pawl['release_force_n']}")
    check("a HOLD gate exists and passes", pawl["holds"])
    check("hold is by the P1 hard-stop latch (compression)",
          "P1" in pawl["hold_mechanism"])

    # ---- A3: ceiling computed (DND-93) -----------------------------------
    print("[A3] Release-force ceiling -- RESOLVED (DND-93)")
    check("model no longer hard-codes 296.0",
          rel["banked_ceiling_n"] != 296.0, f"{rel['banked_ceiling_n']} N")
    check("ceiling is comb-tooth bending (independent structural limit)",
          "CALCULATION" in rel["banked_ceiling_evidence"])
    check("banked force within the structural limit", rel["banked_ok"])
    check("0.37 * 800 == the old 296 N number for the record",
          abs(0.37 * 800 - 296.0) < 1e-9)

    # ---- A4: timing terms (DND-93) ---------------------------------------
    print("[A4] Timing terms -- RESOLVED (DND-93)")
    check("mask-index term present", tm["mask_index_s"] > 0.0, f"{tm['mask_index_s']} s")
    check("carriage-traverse term present", tm["carriage_traverse_s"] > 0.0,
          f"{tm['carriage_traverse_s']} s")
    check("full map < 30 s", tm["clears_30s"], f"{tm['full_map_s']} s")

    # ---- A5: BOM honesty (DND-93) ----------------------------------------
    print("[A5] Cost ladder honesty -- RESOLVED (DND-93)")
    check("six allowance lines added",
          sum(1 for r in b["lines"] if r["evidence"] == "allowance") == 6)
    check("parts repriced above the old $139.77", b["purchased_parts_usd"] > 139.77,
          f"${b['purchased_parts_usd']}")
    check("lift motor re-priced to the NEMA23-class ($30)",
          any("NEMA23" in r["item"] and abs(r["ext"] - 30.0) < 1e-9 for r in b["lines"]))

    # ---- A6: reliability gate G8 (DND-97) --------------------------------
    print("[A6] Per-cell reliability -- ADDRESSED (DND-97, G8)")
    check("per-cell break-even for a 99% map is ~1.57e-6",
          abs(rg["per_cell_error_break_even"] - 1.570e-6) < 1e-9,
          f"{rg['per_cell_error_break_even']}")
    check("G8 reliability field exists in decide()",
          "g8_reliability_pass" in dec and "g8_reliability_status" in dec)
    check("G8 explicitly NOT satisfied analytically (honest)",
          dec["g8_reliability_pass"] is False)
    check("G8 names the coupon-C1 measurement path", "C1" in rg["evidence_path"])

    # ---- A7: lift load + unloaded-write limitation (DND-97) --------------
    print("[A7] Lift load / unloaded write -- RESOLVED (DND-97)")
    check("lift_axis sized on the WHOLE board (6400 cells)",
          lift["cells_lifted"] == s6lc.CELLS, f"{lift['cells_lifted']}")
    check("G3 passes with the NEMA23-class motor", lift["passes"],
          f"{lift['torque_needed_nm']} vs {lift['motor_torque_nm']} Nm")
    check("the unloaded-write case is stated as an explicit limitation (A7)",
          any("common plate" in r.lower() or "minis" in r.lower()
              or "unloaded" in r.lower()
              for r in dec["residual_uncertainty"]))
    check("'assumed unloaded' is no longer asserted as a bare assumption",
          not any("assumed unloaded" in r for r in dec["residual_uncertainty"]))

    # ---- A8: regional/jam limitations (DND-97) ---------------------------
    print("[A8] Regional / jam -- RESTATED (DND-97)")
    check("three actuators for eight bank gates + eight combs",
          b["bought_actuators"] == 3)
    check("regional/jam is stated as an explicit limitation needing a test (A8)",
          any("jam" in r.lower() for r in dec["residual_uncertainty"]))

    # ---- DND-93 gates retained ------------------------------------------
    print("[G7] Reset-carriage torque gate (DND-93)")
    check("reset carriage load is one bank (800 cells)",
          reset["cells_released"] == s6lc.CELLS_PER_BANK, f"{reset['cells_released']}")
    check("reset torque under the small-stepper rating", reset["passes"],
          f"{reset['torque_needed_nm']} vs {reset['motor_torque_nm']} Nm")

    # ---- mission gate vs internal delivered convention -------------------
    print("[G0] Mission gate vs internal delivered convention")
    check("G5 mission gate (purchased parts) PASSES", dec["mission_gate_pass"],
          f"${dec['parts_usd']}")
    check("G6 delivered convention honestly reported over the line",
          dec["delivered_convention_under_250"] is False, f"${dec['delivered_usd']}")
    check("all mission gates pass (G1-G5, G7)",
          dec["all_mission_gates_pass"], str(dec["mission_gates"]))
    check("verdict is PROMOTE_TO_09_WITH_MEASUREMENT_GATE",
          dec["verdict"] == "PROMOTE_TO_09_WITH_MEASUREMENT_GATE",
          dec["verdict"])

    print("=" * 60)
    print(f"{CHECKS - len(FAILURES)}/{CHECKS} resolution checks passed")
    if FAILURES:
        print("FAILED: " + ", ".join(FAILURES))
        return 1
    print("All DND-91 findings are RESOLVED and locked: no regression to the "
          "broken headline.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
