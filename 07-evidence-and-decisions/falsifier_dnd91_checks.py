#!/usr/bin/env python3
"""DND-91 Falsifier checks: adversarially audit the SELECTED ultra-low-cost machine S6-LC.

Run from anywhere:  python 07-evidence-and-decisions/falsifier_dnd91_checks.py

Evidence class: CALCULATION / adversarial re-derivation over the repo's own S6-LC
model, CAD source and BOM, plus sourced-fact readings of the repo's own documents.
No print, no purchase, no measurement (DND-27). Like falsifier_s5_review_checks.py
and the DND-46 gate, these checks assert the *counter-numbers* the audit reports,
so the prose cannot drift from the arithmetic.

RE-BASELINED after DND-93 (the G3 fix). The original gate asserted the pre-fix
broken state; DND-93 corrected the model (lift_axis sized on the whole 6,400-cell
board, a real structural release limit replacing the circular 296 N, a reset-
carriage torque gate, priced mask-index + carriage-traverse timing terms, and the
six honest BOM allowances). This gate now asserts the CORRECTED state and keeps
the still-open attacks (A1 cell-fit overflow, A2 pawl-spring section, A6 absent
reliability gate, A7 unloaded-write assumption) locked as open defects.

Attacks encoded (see dnd91-s6lc-falsification.md and dnd93-s6lc-g3-fix.md):
  A1 cell-fit lane gate ignores placement; CAD pawl overflows the pitch band  [OPEN]
  A2 pawl spring uses the root block section, not the 0.45 mm leaf (factor 8) [OPEN]
  A3 the "296 N ceiling" is 0.37 N/cell x 800 (borrowed, not sourced)        [FIXED-DND-93]
  A4 timing prices 4 strokes + dwells only; traverse/mask index unpriced      [FIXED-DND-93]
  A5 BOM soft lines repriced to plausible retail; unlisted capabilities       [FIXED-DND-93]
  A6 per-cell reliability: q=1e-4 -> P(all 6400) = 52.7 %; no G7 gate          [OPEN]
  A7 platen-unloaded assumption contradicts the tabletop-in-play product      [OPEN]
  A8 regional/jam behaviour asserted, not modelled                            [OPEN]
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
    print("DND-91 Falsifier - adversarial audit of S6-LC (re-baselined by DND-93)")
    print("=" * 60)

    # ---- A1: cell fit ignores placement (STILL OPEN) ---------------------
    print("[A1] Cell fit / lane budget (OPEN - not fixed by DND-93)")
    half_pitch = s6lc.PITCH_MM / 2
    offset = s6lc.COLUMN_BODY_MM / 2 + 0.10          # scad: BODY/2 + 0.10
    pawl_reach = offset + s6lc.PAWL_T_MM
    owned_lane = s6lc.PITCH_MM / 2 - s6lc.COLUMN_BODY_MM / 2
    check("model claims lane_free == 1.48", abs((s6lc.PITCH_MM - s6lc.COLUMN_BODY_MM) - 1.48) < 1e-9)
    check("owned lane to half-pitch is only 0.74 mm", abs(owned_lane - 0.74) < 1e-9,
          f"{owned_lane:.3f}")
    check("pawl thickness (0.90) exceeds the owned lane",
          s6lc.PAWL_T_MM > owned_lane, f"{s6lc.PAWL_T_MM} > {owned_lane:.2f}")
    check("CAD pawl still overflows the pitch band (reach > half-pitch)",
          pawl_reach > half_pitch, f"reach {pawl_reach:.2f} > half_pitch {half_pitch:.2f}")
    check("overflow is 0.260 mm", abs((pawl_reach - half_pitch) - 0.26) < 1e-9,
          f"{pawl_reach - half_pitch:.3f}")
    check("SCAD places the pawl at BODY/2 + 0.10",
          "BODY/2 + 0.10" in SCAD.read_text())

    # ---- A2: spring uses the wrong section (STILL OPEN) ------------------
    print("[A2] Pawl spring section (OPEN - not fixed by DND-93)")
    k_model = s6lc._cantilever_rate_n_per_mm(s6lc.PAWL_T_MM, s6lc.PAWL_W_MM, s6lc.PAWL_L_MM)
    k_leaf = s6lc._cantilever_rate_n_per_mm(s6lc.PAWL_T_MM / 2, s6lc.PAWL_W_MM, s6lc.PAWL_L_MM)
    check("model k ~= 0.6407 N/mm", abs(k_model - 0.6407) < 1e-3, f"{k_model:.4f}")
    check("CAD leaf k ~= 0.0801 N/mm", abs(k_leaf - 0.0801) < 1e-3, f"{k_leaf:.4f}")
    check("model overstates k by 8x", abs(k_model / k_leaf - 8.0) < 1e-6, f"{k_model / k_leaf:.3f}")
    check("true release ~= 0.020 N", abs(k_leaf * s6lc.PAWL_DEFLECTION_MM - 0.02) < 1e-3,
          f"{k_leaf * s6lc.PAWL_DEFLECTION_MM:.4f}")
    check("SCAD leaf is PAWL_T/2 (0.45) in the bending axis",
          "PAWL_T/2" in SCAD.read_text())
    _src = (S6LC_ANALYSIS / "s6lc.py").read_text().lower()
    check("no hold-force gate exists in the model (still open)",
          "hold_force" not in _src and "hold_force_n" not in _src and "slip" not in _src)

    # ---- A3: circular ceiling (FIXED by DND-93) --------------------------
    print("[A3] Release-force ceiling provenance (FIXED by DND-93)")
    rel = s6lc.release_force()
    check("model no longer hard-codes 296.0",
          rel["banked_ceiling_n"] != 296.0, f"{rel['banked_ceiling_n']} N")
    check("ceiling is comb-tooth bending (independent structural limit)",
          "CALCULATION" in rel["banked_ceiling_evidence"])
    check("comb-tooth limit ~= 413 N", abs(rel["banked_ceiling_n"] - 413.0) < 1.0,
          f"{rel['banked_ceiling_n']}")
    check("banked force (128.2 N) < comb limit -> banked_ok",
          rel["banked_ok"], f"{rel['banked_all_armed_n']} N")
    check("0.37 * 800 == the old 296 N number for the record",
          abs(0.37 * 800 - 296.0) < 1e-9)

    # ---- A4/A6: timing terms (FIXED by DND-93) ---------------------------
    print("[A4] Timing terms (FIXED by DND-93)")
    tm = s6lc.timing()
    check("mask-index term is now present", hasattr(s6lc, "MASK_INDEX_S")
          and tm["mask_index_s"] > 0.0, f"{tm['mask_index_s']} s")
    check("carriage-traverse term is now present", hasattr(s6lc, "CARRIAGE_TRAVERSE_S")
          and tm["carriage_traverse_s"] > 0.0, f"{tm['carriage_traverse_s']} s")
    check("full map now 11.956 s (not the old 7.4 s)", abs(tm["full_map_s"] - 11.956) < 1e-3,
          f"{tm['full_map_s']}")
    check("full map still < 30 s", tm["clears_30s"])

    # ---- A5: BOM honesty (FIXED by DND-93) -------------------------------
    print("[A5] Cost ladder honesty (FIXED by DND-93)")
    b = s6lc.bom()
    check("six allowance lines added",
          sum(1 for r in b["lines"] if r["evidence"] == "allowance") == 6)
    check("parts == $226.77 (was $139.77)",
          abs(b["purchased_parts_usd"] - 226.77) < 1e-9, f"${b['purchased_parts_usd']}")
    check("delivered == $263.05 (was $162.13)",
          abs(b["delivered_usd"] - 263.05) < 1e-9, f"${b['delivered_usd']}")
    check("G6 delivered cost now FAILS honestly (over by $13.05)",
          not b["clears_delivered"], f"${b['delivered_usd']} vs $250")
    check("lift motor re-priced to the NEMA23-class ($30)",
          any("NEMA23" in r["item"] and abs(r["ext"] - 30.0) < 1e-9 for r in b["lines"]))

    # ---- A6: reliability inversion (STILL OPEN) --------------------------
    print("[A6] Per-cell reliability (OPEN - not fixed by DND-93)")
    import reliability  # noqa: E402
    q1 = 1e-4
    p_all = reliability.perfect_map_probability(q1, cells=6400)
    check("P(all 6400 correct | q=1e-4) == 52.7 %", abs(p_all - 0.52729) < 1e-4,
          f"{p_all*100:.2f}%")
    check("program's 99 %-map budget is q <= 1.57e-6",
          abs(reliability.cell_error_budget(0.99) - 1.570e-6) < 1e-9)
    check("no reliability gate in decide() (G7 is now reset-carriage, not reliability)",
          "G7" in "".join(s6lc.decide()["gates"])
          and "reliab" not in "".join(s6lc.decide()["gates"]).lower())
    check("S6-LC admits no per-cell feedback",
          any("no per-cell feedback" in r.lower()
              for r in s6lc.decide()["residual_uncertainty"]))

    # ---- A7: unloaded-write assumption vs product (STILL OPEN) -----------
    print("[A7] Load vs write (OPEN - not fixed by DND-93)")
    lift = s6lc.lift_axis()
    check("lift_axis is now sized on the whole board (6400 cells, was 800)",
          lift["cells_lifted"] == s6lc.CELLS, f"{lift['cells_lifted']}")
    check("global load == 2560 N, torque == 1.6297 Nm",
          abs(lift["load_n"] - 2560.0) < 1e-6 and abs(lift["torque_needed_nm"] - 1.6297) < 1e-3,
          f"{lift['load_n']} N -> {lift['torque_needed_nm']} Nm")
    check("G3 passes with a NEMA23-class motor at 1.35x margin",
          lift["passes"] and abs(lift["margin"] - 1.35) < 0.01, f"{lift['margin']}x")
    check("model still assumes an UNLOADED write (open product contradiction)",
          any("assumed unloaded" in r for r in s6lc.decide()["residual_uncertainty"]))

    # ---- A8: regional/jam asserted (STILL OPEN) --------------------------
    print("[A8] Regional / jam (OPEN - bounded)")
    check("three actuators for eight bank gates + eight combs",
          b["bought_actuators"] == 3)
    check("model states all-armed requires banking (jam class)",
          rel["unbanked_all_armed_n"] > rel["banked_ceiling_n"])

    # ---- reset-carriage gate (NEW from DND-93) ---------------------------
    print("[G7] Reset-carriage torque gate (NEW from DND-93)")
    reset = s6lc.reset_carriage_axis()
    check("reset carriage load is one bank (128.2 N)",
          abs(reset["load_n"] - 128.2) < 0.05, f"{reset['load_n']} N")
    check("reset torque == 0.0816 Nm < 0.16 Nm small stepper",
          abs(reset["torque_needed_nm"] - 0.0816) < 1e-3 and reset["passes"],
          f"{reset['torque_needed_nm']} Nm, margin {reset['margin']}x")

    # ---- audit-gate integrity -------------------------------------------
    print("[G0] The audit's own claims hold")
    check("A1/A2 counter-numbers are self-consistent",
          abs(pawl_reach - half_pitch - 0.26) < 1e-9 and abs(k_model / k_leaf - 8.0) < 1e-6)
    check("corrected verdict is REJECT (G6 over)",
          s6lc.decide()["verdict"] == "REJECT")

    print("=" * 60)
    print(f"{CHECKS - len(FAILURES)}/{CHECKS} audit checks passed")
    if FAILURES:
        print("FAILED: " + ", ".join(FAILURES))
        return 1
    print("Audit assertions hold: fixed items are corrected, open attacks remain open.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
