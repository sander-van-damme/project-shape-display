"""SHA-19 divergent screen — F2 buckling-sheet snap array gate.

Cheapest analytic test for the single advanced mechanism of SHA-19: an
in-plane edge-compressed stack of bistable dome sheets snapping 80x80
columns through printed shutter selection.

Evidence class: CALCULATION over design-criteria geometry (02) + SHA-7
assumption-class snap forces + textbook dome-rise ratios. No print, no
purchase, no measurement (DND-27).

Binding insight asserted and checked below: a snap dome on a <= 4.6 mm
footprint rises only a fraction of its diameter (~1.4-2.3 mm), so one
sheet cannot deliver 40 mm (>= 18 sheets needed); and every dome
snapping on a stroke loads the shared edge actuator simultaneously
(6400 x F_snap >= 11.5 kN even at the -40% corner), so banking to
affordable force multiplies strokes past the 30 s budget at every
corner — the D1 force/stroke triangle in the buckling domain.

Kill criteria (up front, binding):
  KC4 geometry .. single-sheet stroke must reach 40 mm; KILL if the
                  optimistic dome rise is an order below travel.
  KC4 stack ..... sheet count for 40 mm must be buildable (<= ~6);
                  KILL if >= 18 sheets with 18 mask layers.
  KC1 cost ...... single-pass edge force must fit an affordable stage;
                  KILL if the optimistic corner already needs
                  industrial hydraulics (floor ~$300 >> A1 $181).
  KC2 timing .... banked strokes to affordable force must fit < 30 s;
                  KILL if the optimistic corner alone exceeds 30 s.
  (KC3 silent shutter-miss recorded in the verdict note; the stroke +
  force triangle kills first and needs no measurement.)

Run:  python 06-experiments/test21_divergent_screen4/buckling_gate.py
Gate: python 06-experiments/test21_divergent_screen4/buckling_gate.py --gate
"""

from __future__ import annotations

import argparse
import math

# ---- Board geometry (design criteria 02) ----
N_COLS = 6400            # 80x80
TRAVEL_MM = 40.0         # minimum usable vertical travel
TIME_BUDGET_S = 30.0     # full-map change strictly < 30 s

# ---- Dome-rise geometry (textbook snap-dome class, generous) ----
# Stable dome rise is a fraction of footprint diameter. Cell pitch
# 5.08 mm with printed walls leaves <= ~4.6 mm dome diameter.
DOME_DIA_MM = 4.6
# Rise ratio (rise/diameter): optimistic 0.5 (deep draw, generous),
# nominal 0.3 (shallow printable cap). Confidence: medium (textbook
# bistability class, not a coupon measurement).
RISE = {"optimistic": 0.5 * DOME_DIA_MM, "nominal": 0.3 * DOME_DIA_MM}
# Buildable stack ceiling: generously 6 sheets (6 mask layers,
# registration, edge-drive compliance). Anything double-digit is
# an unbuildable laminate.
STACK_CEILING = 6

# ---- Snap forces (SHA-7 assumption class, +/-40% spread) ----
F_SNAP = {"optimistic": 1.8, "nominal": 3.0, "worst": 4.2}  # N/dome

# ---- Sourced-class edge actuator (same class as the D1 platen gate) ----
# Generous hobby/industrial boundary: 1 kN force, 20 mm/s under load.
# In-plane compression stroke per pass ~10 mm + shutter/switch/settle.
FORCE_LIMIT_N = 1000.0
T_STROKE_S = 1.0         # per banked stroke incl. overhead, optimistic
# Big-actuator sourced-class floor before plumbing/frame.
BIG_ACTUATOR_FLOOR_USD = 300.0
A1_PARTS = 181.0         # SHA-7 sourced-class BOM (medium)
LEVELS = 4               # height increments per map (5 states)

CHECKS: list[tuple[str, str]] = [
    ("single_dome_stroke_kills",
     "optimistic dome rise an order below 40 mm travel"),
    ("stack_sheets_kills",
     "sheets needed for 40 mm exceed any buildable stack"),
    ("single_pass_force_kills",
     "optimistic single-pass edge force needs hydraulics"),
    ("banked_timing_kills",
     "banked strokes to affordable force exceed 30 s"),
    ("actuator_cost_kills",
     "big-actuator floor alone exceeds A1 $181"),
]


def sheets_needed(rise_mm: float) -> int:
    """Sheets so stacked dome rises cover 40 mm."""
    return math.ceil(TRAVEL_MM / rise_mm)


def single_pass_force_n(f_snap: float) -> float:
    """Edge force if all 6400 domes snap on one stroke."""
    return N_COLS * f_snap


def banked_strokes(f_snap: float) -> int:
    """Passes: P banks per level so per-stroke force <= 1 kN."""
    per_stroke = single_pass_force_n(f_snap)
    banks = math.ceil(per_stroke / FORCE_LIMIT_N)
    return LEVELS * banks


def run_gate() -> tuple[int, int, list[str]]:
    lines: list[str] = []
    passed = 0

    rise_opt = RISE["optimistic"]
    ok = rise_opt <= TRAVEL_MM / 10.0  # order below travel
    lines.append(f"[{'PASS' if ok else 'FAIL'} ] single_dome_stroke_kills: "
                 f"{rise_opt:.1f} mm optimistic dome rise "
                 f"<= {TRAVEL_MM / 10.0:.1f} mm (tenth of travel)")
    passed += ok

    n_opt = sheets_needed(rise_opt)
    ok = n_opt > STACK_CEILING * 2  # double-digit laminate
    lines.append(f"[{'PASS' if ok else 'FAIL'} ] stack_sheets_kills: "
                 f"{n_opt} sheets needed optimistic "
                 f">> {STACK_CEILING}-sheet ceiling")
    passed += ok

    f_opt = single_pass_force_n(F_SNAP["optimistic"])
    ok = f_opt >= 10 * FORCE_LIMIT_N  # order above affordable stage
    lines.append(f"[{'PASS' if ok else 'FAIL'} ] single_pass_force_kills: "
                 f"{f_opt / 1000:.1f} kN optimistic single-pass "
                 f">> {FORCE_LIMIT_N / 1000:.0f} kN affordable stage")
    passed += ok

    # Generous fiction: grant 4 deep-drawn sheets (unphysical per
    # check 1) and count only D1-analogous 4xP strokes — still kills.
    s_fiction = banked_strokes(F_SNAP["optimistic"])
    t_fiction = s_fiction * T_STROKE_S
    ok = t_fiction >= TIME_BUDGET_S
    lines.append(f"[{'PASS' if ok else 'FAIL'} ] banked_timing_kills: "
                 f"{s_fiction} strokes x {T_STROKE_S:.2f} s = "
                 f"{t_fiction:.0f} s optimistic (4-sheet fiction) "
                 f">= {TIME_BUDGET_S:.0f} s budget")
    passed += ok

    ok = BIG_ACTUATOR_FLOOR_USD >= A1_PARTS
    lines.append(f"[{'PASS' if ok else 'FAIL'} ] actuator_cost_kills: "
                 f"${BIG_ACTUATOR_FLOOR_USD:.0f} actuator floor "
                 f">= A1 ${A1_PARTS:.0f} (before sheets/masks/frame)")
    passed += ok

    print(f"F2 buckling gate: {passed}/{len(CHECKS)} kill-confirming checks hold")
    for line in lines:
        print(" ", line)
    return passed, len(CHECKS), lines


def main() -> None:
    parser = argparse.ArgumentParser(description="F2 buckling-sheet gate")
    parser.add_argument("--gate", action="store_true",
                        help="run kill-confirming gate checks")
    parser.add_argument("--json", action="store_true", help="emit JSON summary")
    args = parser.parse_args()

    if args.json:
        import json as _json
        print(_json.dumps({
            "rise_mm": RISE,
            "sheets_needed": {k: sheets_needed(v) for k, v in RISE.items()},
            "single_pass_force_N": {k: single_pass_force_n(v)
                                    for k, v in F_SNAP.items()},
            "banked_strokes_4sheet_fiction": {k: banked_strokes(v)
                                              for k, v in F_SNAP.items()},
        }, indent=1))
        return

    passed, total, _ = run_gate()
    if args.gate and passed != total:
        raise SystemExit(f"GATE INCOMPLETE: {passed}/{total} (F2 not killed)")


if __name__ == "__main__":
    main()
