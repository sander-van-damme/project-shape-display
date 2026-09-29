#!/usr/bin/env python3
"""DND-91 Falsifier checks: adversarially audit the SELECTED ultra-low-cost machine S6-LC.

Run from anywhere:  python 07-evidence-and-decisions/falsifier_dnd91_checks.py

Evidence class: CALCULATION / adversarial re-derivation over the repo's own S6-LC
model, CAD source and BOM, plus sourced-fact readings of the repo's own documents.
No print, no purchase, no measurement (DND-27). Like falsifier_s5_review_checks.py
and the DND-46 gate, these checks assert the *counter-numbers* the audit reports,
so the prose cannot drift from the arithmetic.

Attacks encoded (see dnd91-s6lc-falsification.md):
  A1 cell-fit lane gate ignores placement; CAD pawl overflows the pitch band
  A2 pawl spring uses the root block section, not the 0.45 mm leaf (factor 8)
  A3 the "296 N ceiling" is 0.37 N/cell x 800 (borrowed, not sourced)
  A4 timing prices 4 strokes + dwells only; traverse/mask index unpriced
  A5 BOM soft lines repriced to plausible retail; unlisted capabilities
  A6 per-cell reliability: q=1e-4 -> P(all 6400) = 52.7 %; no G7 gate
  A7 platen-unloaded assumption contradicts the tabletop-in-play product
  A8 regional/jam behaviour asserted, not modelled
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
    print("DND-91 Falsifier - adversarial audit of S6-LC")
    print("=" * 52)

    # ---- A1: cell fit ignores placement --------------------------------
    print("[A1] Cell fit / lane budget (BROKEN)")
    half_pitch = s6lc.PITCH_MM / 2
    offset = s6lc.COLUMN_BODY_MM / 2 + 0.10          # scad: BODY/2 + 0.10
    pawl_reach = offset + s6lc.PAWL_T_MM
    owned_lane = s6lc.PITCH_MM / 2 - s6lc.COLUMN_BODY_MM / 2
    check("model claims lane_free == 1.48", abs((s6lc.PITCH_MM - s6lc.COLUMN_BODY_MM) - 1.48) < 1e-9)
    check("owned lane to half-pitch is only 0.74 mm", abs(owned_lane - 0.74) < 1e-9,
          f"{owned_lane:.3f}")
    check("pawl thickness (0.90) exceeds the owned lane",
          s6lc.PAWL_T_MM > owned_lane, f"{s6lc.PAWL_T_MM} > {owned_lane:.2f}")
    check("CAD pawl overflows the pitch band (reach > half-pitch)",
          pawl_reach > half_pitch, f"reach {pawl_reach:.2f} > half_pitch {half_pitch:.2f}")
    check("overflow is 0.260 mm", abs((pawl_reach - half_pitch) - 0.26) < 1e-9,
          f"{pawl_reach - half_pitch:.3f}")
    check("SCAD places the pawl at BODY/2 + 0.10",
          "BODY/2 + 0.10" in SCAD.read_text())

    # ---- A2: spring uses the wrong section ------------------------------
    print("[A2] Pawl spring section (BROKEN, 8x)")
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
    check("no hold-force gate exists in the model",
          "hold_force" not in _src and "hold_force_n" not in _src and "slip" not in _src)

    # ---- A3: circular ceiling -------------------------------------------
    print("[A3] 296 N ceiling is borrowed (BROKEN, circular)")
    rel = s6lc.release_force()
    check("ceiling == 0.37 * 800 (old S1 per-cell)", abs(0.37 * 800 - 296.0) < 1e-9)
    check("model ceiling_n is hard-coded 296.0", rel["banked_ceiling_n"] == 296.0)
    check("per-cell release != 0.37 (it is the S6-LC pawl)", rel["per_cell_n"] != 0.37,
          f"{rel['per_cell_n']}")

    # ---- A4: timing prices strokes + dwells only ------------------------
    print("[A4] Timing unpriced terms (BOUNDED)")
    tm = s6lc.timing()
    check("full map is 7.4 s", abs(tm["full_map_s"] - 7.4) < 1e-9, f"{tm['full_map_s']}")
    check("model has no mask-index-time term",
          not hasattr(s6lc, "MASK_INDEX_S"))
    check("model has no carriage-traverse-time term",
          not hasattr(s6lc, "CARRIAGE_TRAVERSE_S"))
    check("sensitivity tolerates 53 banks (margins are assumed)",
          s6lc.sensitivity()["max_banks_for_30s_at_reset_s"] >= 50,
          f"{s6lc.sensitivity()['max_banks_for_30s_at_reset_s']}")

    # ---- A5: BOM soft lines / unlisted capabilities ---------------------
    print("[A5] Cost ladder honesty (BOUNDED-NEEDS-SOURCING)")
    b = s6lc.bom()
    check("base parts == $139.77", abs(b["purchased_parts_usd"] - 139.77) < 1e-9)
    check("delivered == $162.13", abs(b["delivered_usd"] - 162.13) < 1e-9)
    soft = {"4x T8 lead screw + anti-backlash nut": 40.0,
            "Guide rods + bushings (platen)": 22.0,
            "Timing belt + 2 pulleys (4-screw sync)": 14.0,
            "Lift motor (NEMA17-class stepper)": 14.0,
            "Motor couplers + thrust washers": 8.0}
    revised = sum(soft.get(r["item"], r["ext"]) for r in b["lines"])
    check("repriced parts == $169.77", abs(revised - 169.77) < 1e-9, f"{revised:.2f}")
    check("repriced delivered == $196.93 (still < $250)",
          abs(revised * s6lc.UPLIFT - 196.93) < 0.01, f"{revised * s6lc.UPLIFT:.2f}")
    check("repriced margin == $53.07", abs(250 - revised * s6lc.UPLIFT - 53.07) < 0.01,
          f"{250 - revised * s6lc.UPLIFT:.2f}")
    check("only one 'assumption' line (spares $8) is admitted",
          sum(1 for r in b["lines"] if r["evidence"] == "assumption") == 1)
    check("softest lines are 'sourced-class', not sourced-listing",
          sum(1 for r in b["lines"] if r["evidence"] == "sourced-class") >= 8,
          f"{sum(1 for r in b['lines'] if r['evidence'] == 'sourced-class')} lines")

    # ---- A6: reliability inversion --------------------------------------
    print("[A6] Per-cell reliability (BROKEN AS STATED)")
    import reliability  # noqa: E402
    q1 = 1e-4
    p_all = reliability.perfect_map_probability(q1, cells=6400)
    check("P(all 6400 correct | q=1e-4) == 52.7 %", abs(p_all - 0.52729) < 1e-4,
          f"{p_all*100:.2f}%")
    check("program's 99 %-map budget is q <= 1.57e-6",
          abs(reliability.cell_error_budget(0.99) - 1.570e-6) < 1e-9)
    check("S6-LC decide() has fewer gates than the program's requirement set",
          len(s6lc.decide()["gates"]) == 6 and "G7" not in "".join(s6lc.decide()["gates"]),
          "no reliability gate")
    check("S6-LC admits no per-cell feedback",
          any("no per-cell feedback" in r.lower()
              for r in s6lc.decide()["residual_uncertainty"]))

    # ---- A7: unloaded-write assumption vs product -----------------------
    print("[A7] Load vs write (BROKEN vs requirement)")
    lift = s6lc.lift_axis()
    check("lift margin is only 1.47x", abs(lift["margin"] - 1.47) < 0.01, f"{lift['margin']}")
    check("model explicitly assumes an UNLOADED write",
          any("assumed unloaded" in r for r in s6lc.decide()["residual_uncertainty"]))

    # ---- A8: regional/jam asserted --------------------------------------
    print("[A8] Regional / jam (BOUNDED-NEEDS-MEASUREMENT)")
    check("three actuators for eight bank gates + eight combs",
          b["bought_actuators"] == 3)
    check("model states all-armed requires banking (jam class)",
          rel["unbanked_all_armed_n"] > 296.0)

    # ---- audit-gate integrity -------------------------------------------
    print("[G0] The audit's own claims hold")
    check("A1/A2 counter-numbers are self-consistent",
          abs(pawl_reach - half_pitch - 0.26) < 1e-9 and abs(k_model / k_leaf - 8.0) < 1e-6)

    print("=" * 52)
    print(f"{CHECKS - len(FAILURES)}/{CHECKS} audit checks passed")
    if FAILURES:
        print("FAILED: " + ", ".join(FAILURES))
        return 1
    print("All DND-91 falsification assertions hold: the attacks are reproduced.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
