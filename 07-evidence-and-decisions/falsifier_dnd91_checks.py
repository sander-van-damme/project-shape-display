#!/usr/bin/env python3
"""DND-91 Falsifier checks: adversarial audit of S6-LC — NOW A RESOLUTION GATE.

Run from anywhere:  python 07-evidence-and-decisions/falsifier_dnd91_checks.py

The original DND-91 gate asserted that S6-LC's headline was *broken* (A1..A8). That
audit drove [DND-93](/DND/issues/DND-93). This gate is updated to lock the
*RESOLVED* state so the fixes cannot drift back. Each attack is retained as a
historical counter-number and paired with a resolution assertion:

  A1 cell-fit lane gate          -> fixed: owned half-lane gate + outboard root
  A2 pawl spring (8x) + no hold  -> fixed: leaf section used + P1 latch hold gate
  A3 circular 296 N ceiling      -> fixed: computed comb-tooth + motor-stall limit
  A4 timing unpriced terms       -> fixed: mask-index + carriage-traverse priced
  A5 BOM soft lines / unlisted   -> fixed: soft lines repriced + 6 capability lines
  A6 no per-cell reliability gate-> fixed: G7 added, explicitly UNRESOLVED
  A7 unloaded-write assumption   -> fixed: G3 load re-derived for the whole board
  A8 regional/jam asserted       -> fixed: G8 reset-carriage torque gate added

Evidence class: CALCULATION over the repo's own S6-LC model. No print, no
purchase, no measurement (DND-27).
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
S6LC_ANALYSIS = REPO / "09-low-cost-variant" / "s6lc" / "analysis"
SCAD = REPO / "09-low-cost-variant" / "s6lc" / "scad" / "s6lc_machine.scad"

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
    print("DND-91 falsifier findings - RESOLUTION gate (DND-93)")
    print("=" * 56)

    fit = s6lc.column_fit()
    pawl = s6lc.pawl_spring()
    rel = s6lc.release_force()
    tm = s6lc.timing()
    lift = s6lc.lift_axis()
    rc = s6lc.reset_carriage()
    b = s6lc.bom()
    dec = s6lc.decide()
    scad = SCAD.read_text()

    # ---- A1: cell fit now gates the OWNED half-lane ---------------------
    print("[A1] Cell fit / lane budget -- RESOLVED")
    owned_lane = s6lc.PITCH_MM / 2 - s6lc.COLUMN_BODY_MM / 2
    check("owned lane to half-pitch is 0.74 mm", abs(owned_lane - 0.74) < 1e-9,
          f"{owned_lane:.3f}")
    check("model now exposes the OWNED lane (not the whole gap)",
          "owned_lane_mm" in fit and abs(fit["owned_lane_mm"] - 0.74) < 1e-9)
    check("pawl LEAF (0.45) + clearance fits the owned lane",
          pawl["leaf_t_mm"] + s6lc.LANE_BLEED_MM <= owned_lane,
          f"{pawl['leaf_t_mm']} + {s6lc.LANE_BLEED_MM}")
    check("root block declared outboard of the pitch band", fit["root_outboard"])
    check("SCAD no longer places the pawl at BODY/2 + 0.10",
          "BODY/2 + 0.10" not in scad, "placement corrected")
    check("cell fits overall", fit["fits"])
    # historical counter-number retained
    check("historical: the OLD 0.90 pawl overflowed by 0.260 mm",
          abs(((s6lc.COLUMN_BODY_MM / 2 + 0.10 + 0.90) - s6lc.PITCH_MM / 2) - 0.26) < 1e-9)

    # ---- A2: spring uses the leaf + a hold gate -------------------------
    print("[A2] Pawl spring section + hold -- RESOLVED")
    k_leaf = s6lc._cantilever_rate_n_per_mm(pawl["leaf_t_mm"], s6lc.PAWL_W_MM, s6lc.PAWL_L_MM)
    check("model k uses the 0.45 mm leaf (~0.0801 N/mm)",
          abs(k_leaf - 0.0801) < 1e-3, f"{k_leaf:.4f}")
    check("model no longer uses the 0.90 root section for k",
          abs(pawl["rate_n_per_mm"] - 0.0801) < 1e-3)
    check("true release ~= 0.020 N", abs(pawl["release_force_n"] - 0.02) < 1e-3,
          f"{pawl['release_force_n']}")
    check("a HOLD gate now exists", "holds" in pawl and "hold_required_n" in pawl)
    check("hold is by the P1 hard-stop latch (compression, not friction)",
          "P1" in pawl["hold_mechanism"] and pawl["holds"])

    # ---- A3: ceiling is now computed ------------------------------------
    print("[A3] Release ceiling -- RESOLVED (no longer circular)")
    check("model ceiling is NOT the borrowed 296.0",
          rel["banked_ceiling_n"] != 296.0, f"{rel['banked_ceiling_n']}")
    check("ceiling is min(per-tooth*teeth, reset-motor force)",
          abs(rel["banked_ceiling_n"] -
              min(rel["comb_tooth_limit_n"] * rel["teeth_in_bank_comb"],
                  rel["reset_motor_force_n"])) < 0.15)
    check("ceiling is labelled assumption-class (not sourced)",
          "assumption" in rel["banked_ceiling_class"])
    check("banked release within the computed ceiling", rel["banked_ok"],
          f"{rel['banked_all_armed_n']} <= {rel['banked_ceiling_n']}")

    # ---- A4: timing now prices mask + carriage --------------------------
    print("[A4] Timing terms -- RESOLVED")
    check("mask-index time is now priced", hasattr(s6lc, "MASK_INDEX_S")
          and s6lc.MASK_INDEX_S > 0)
    check("carriage-traverse time is now priced",
          hasattr(s6lc, "CARRIAGE_TRAVERSE_S") and s6lc.CARRIAGE_TRAVERSE_S > 0)
    check("full map still < 30 s with the added terms", tm["clears_30s"],
          f"{tm['full_map_s']} s")
    check("full map is no longer the bare 7.4 s", tm["full_map_s"] != 7.4,
          f"{tm['full_map_s']} s")

    # ---- A5: BOM repriced + capabilities listed -------------------------
    print("[A5] Cost ladder honesty -- RESOLVED")
    check("purchased parts < $250 (mission gate)", b["clears_parts"],
          f"${b['purchased_parts_usd']}")
    check("soft lines repriced above the old $139.77 base",
          b["purchased_parts_usd"] > 139.77, f"${b['purchased_parts_usd']}")
    check("the six missing capabilities are now listed",
          all(any(key in r["item"] for r in b["lines"]) for key in
              ("Mask media", "puncher", "linkage", "traverse rails",
               "splice", "home sensors")))
    check("more than one 'assumption' line is admitted",
          sum(1 for r in b["lines"] if r["evidence"] == "assumption") > 1,
          f"{sum(1 for r in b['lines'] if r['evidence'] == 'assumption')} lines")
    check("delivered overrun is reported (not hidden)",
          dec["g6_delivered_under_250"] in (True, False)
          and dec["g6_delivered_usd"] == b["delivered_usd"])

    # ---- A6: reliability gate G7 ----------------------------------------
    print("[A6] Per-cell reliability -- ADDRESSED (G7 unresolved)")
    rg = s6lc.reliability()
    check("per-cell break-even for a 99% map is ~1.57e-6",
          abs(rg["per_cell_error_break_even"] - 1.570e-6) < 1e-9,
          f"{rg['per_cell_error_break_even']}")
    check("a G7 reliability field exists in decide()",
          "g7_reliability_pass" in dec and "g7_reliability_status" in dec)
    check("G7 is explicitly NOT satisfied analytically (honest)",
          dec["g7_reliability_pass"] is False)
    check("G7 names the coupon-C1 measurement path",
          "C1" in rg["evidence_path"])
    check("S6-LC still admits no per-cell feedback",
          any("no per-cell feedback" in r.lower()
              for r in dec["residual_uncertainty"]))

    # ---- A7: lift load re-derived ---------------------------------------
    print("[A7] Lift load -- RESOLVED (whole board, honest stack-up)")
    check("lift axis lifts the WHOLE board (6400 cells)",
          lift["cells_lifted"] == s6lc.CELLS)
    check("per-column lift load is the honest stack-up (~0.05 N)",
          abs(lift["per_column_load_n"] - 0.0498) < 5e-3,
          f"{lift['per_column_load_n']} N")
    check("lift torque passes with the 0.30 Nm NEMA17", lift["passes"],
          f"{lift['torque_needed_nm']} vs {lift['motor_torque_nm']} Nm")
    check("lift torque margin >= 1.3x", lift["margin"] >= 1.3, f"{lift['margin']}x")
    check("model no longer claims a 1.47x margin on 800 cells",
          lift["cells_lifted"] != s6lc.CELLS_PER_BANK)

    # ---- A8: reset-carriage torque gate ---------------------------------
    print("[A8] Reset carriage -- GATE ADDED")
    check("G8 reset-carriage torque gate exists",
          "G8_reset_carriage_torque" in dec["gates"])
    check("reset-carriage torque passes its motor", rc["passes"],
          f"{rc['torque_needed_nm']} vs {rc['motor_rated_nm']} Nm")

    # ---- resolution integrity -------------------------------------------
    print("[G0] Resolution integrity")
    check("all analytic gates pass", dec["all_gates_pass"], str(dec["gates"]))
    check("verdict reflects the measurement gate",
          dec["verdict"] == "PROMOTE_TO_09_WITH_MEASUREMENT_GATE",
          dec["verdict"])

    print("=" * 56)
    print(f"{CHECKS - len(FAILURES)}/{CHECKS} resolution checks passed")
    if FAILURES:
        print("FAILED: " + ", ".join(FAILURES))
        return 1
    print("All DND-91 findings are RESOLVED and locked: no regression to the "
          "broken headline.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
