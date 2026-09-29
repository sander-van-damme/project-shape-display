"""SHA-16 divergent screen — D1 global-platen force/timing gate.

Cheapest analytic test for the single advanced mechanism of SHA-16: the
compliant staged-snap column (4 stacked bistable frustums, 10 mm each)
driven by one rigid platen over the full 400x400 board, with a printed
shutter mask selecting which columns snap per stroke.

Evidence class: CALCULATION over SHA-7 assumption-class snap forces plus
sourced-class actuator limits. No print, no purchase, no measurement
(DND-27).

Binding insight asserted and checked below: platen force and stroke count
form a closed triangle. Single-pass (4 strokes/map) puts all 6400
snap-through forces on the platen at once (>= 11.5 kN even at the
optimistic corner — industrial hydraulics, cost kill). Banking the mask
(1/P of the board per pass) divides force by P but multiplies strokes to
4 x P (>= 48 strokes even at the optimistic corner with a generous
actuator — timing kill). Softening the frustums to cut F_snap surrenders
the ~5 N abuse-hold the D1 seed itself demands (same-order bistable
physics: holding force and snap-through force scale together), so the
floor and the ceiling are the same quantity.

Kill criteria (up front, binding):
  KC2 timing .. sustained full-map platen cycle must fit < 30 s incl.
                shutter-switch/settle; KILL if banked strokes at the
                optimistic corner already exceed 30 s.
  KC1 cost .... single-pass actuator class (>= 12 kN) must beat A1 ($181);
                KILL if its sourced-class floor exceeds A1, let alone the
                $500 absolute ceiling with plumbing.
  (KC3 silent-shutter / KC4 PLA-creep recorded in the verdict note; the
  triangle kills first and needs no measurement.)

Run:  python 06-experiments/test19_divergent_screen2/platen_gate.py
Gate: python 06-experiments/test19_divergent_screen2/platen_gate.py --gate
"""

from __future__ import annotations

import argparse
import math

# ---- Board geometry (design criteria 02) ----
N_COLS = 6400            # 80x80
LEVELS = 4               # 4 x 10 mm snaps = 40 mm
STROKE_MM = 10.0         # platen travel per level-stroke

# ---- Snap-through force per frustum (SHA-7 W4, assumption-class) ----
# Nominal 3.0 N, worst 4.2 N (+/-40% spread), coupon kill line 7.14 N.
# Low corner 1.8 N (-40%) is the optimistic bound used for kill checks:
# if the triangle fails there, no measurement can rescue it.
F_SNAP = {"low": 1.8, "nominal": 3.0, "high": 4.2}   # N
# Abuse-hold floor from the D1 seed note: columns must hold ~5 N handling
# load without snap-back; bistable holding and snap-through forces scale
# together, so designable F_snap cannot sit far below this floor.
F_ABUSE_FLOOR = 5.0      # N (assumption-class, seed demand)

# ---- Sourced-class platen actuators (2026-09 web sweep, ranges) ----
# Affordable class: 12 V linear actuator 600-1000 N @ ~8 mm/s, $30-60
# retail; NEMA17 + T8 lead screw ~500 N usable. Generous corner for the
# kill checks: 1000 N force, 20 mm/s ball-screw speed (faster than the
# affordable class actually delivers under kN load).
F_AFFORD_N = {"low": 500.0, "nominal": 750.0, "high": 1000.0}
V_NOMINAL_MM_S = 8.0     # affordable-class speed under load
V_GENEROUS_MM_S = 20.0   # ball-screw corner, generous to the mechanism
OVERHEAD_S = 0.5         # shutter-switch + settle per stroke (generous low)
# Single-pass class: >= 12 kN electric cylinder or hydraulic power pack +
# cylinder + plumbing. Sourced-class floor ~$300 (low confidence, wide
# range $300-800); margin over A1 $181 is so large the spread is moot.
BIG_ACTUATOR_FLOOR_USD = 300.0
A1_PARTS = 181.0         # SHA-7 sourced-class BOM (medium)

SINGLE_PASS_KN_LINE = 10.0   # no sub-$500 COTS stage holds this over 400 mm


def full_board_force_n(f_snap: float) -> float:
    """All 6400 frustums snapping on one stroke (worst-case map)."""
    return N_COLS * f_snap


def passes_per_level(f_snap: float, f_act: float) -> int:
    """Mask passes needed so one pass fits the actuator force."""
    return math.ceil(N_COLS * f_snap / f_act)


def stroke_time_s(speed_mm_s: float) -> float:
    return STROKE_MM / speed_mm_s + OVERHEAD_S


def banked_cycle_s(f_snap: float, f_act: float, speed_mm_s: float) -> float:
    return LEVELS * passes_per_level(f_snap, f_act) * stroke_time_s(speed_mm_s)


CHECKS: list[tuple[str, str]] = [
    ("single_pass_force_kills",
     "full-board force at the OPTIMISTIC corner >= 10 kN (no affordable stage)"),
    ("banked_timing_kills",
     "banked cycle at optimistic corner + generous actuator >= 30 s"),
    ("nominal_banked_kills",
     "banked cycle at nominal corner >> 30 s (corroboration)"),
    ("abuse_floor_closes",
     "5 N abuse-hold floor implies >= 32 kN single-pass (softening is no exit)"),
    ("big_actuator_cost_kills",
     "single-pass actuator floor ($300) >= A1 $181 with no path to beat it"),
]


def run_gate() -> tuple[int, int, list[str]]:
    lines: list[str] = []
    passed = 0

    f_low = full_board_force_n(F_SNAP["low"])
    ok = f_low >= SINGLE_PASS_KN_LINE * 1000.0
    lines.append(f"[{'PASS' if ok else 'FAIL'} ] single_pass_force_kills: "
                 f"{f_low / 1000:.1f} kN at 1.8 N corner >= 10 kN line")
    passed += ok

    p = passes_per_level(F_SNAP["low"], F_AFFORD_N["high"])
    tc = banked_cycle_s(F_SNAP["low"], F_AFFORD_N["high"], V_GENEROUS_MM_S)
    ok = tc >= 30.0
    lines.append(f"[{'PASS' if ok else 'FAIL'} ] banked_timing_kills: "
                 f"{LEVELS * p} strokes ({p}/level) x "
                 f"{stroke_time_s(V_GENEROUS_MM_S):.2f} s = {tc:.1f} s >= 30 s")
    passed += ok

    pn = passes_per_level(F_SNAP["nominal"], F_AFFORD_N["nominal"])
    tn = banked_cycle_s(F_SNAP["nominal"], F_AFFORD_N["nominal"], V_NOMINAL_MM_S)
    ok = tn >= 30.0
    lines.append(f"[{'PASS' if ok else 'FAIL'} ] nominal_banked_kills: "
                 f"{LEVELS * pn} strokes x "
                 f"{stroke_time_s(V_NOMINAL_MM_S):.2f} s = {tn:.1f} s >= 30 s")
    passed += ok

    f_abuse = full_board_force_n(F_ABUSE_FLOOR)
    ok = f_abuse >= 32_000.0
    lines.append(f"[{'PASS' if ok else 'FAIL'} ] abuse_floor_closes: "
                 f"{f_abuse / 1000:.0f} kN at 5 N hold-floor; "
                 f"banked to 1 kN needs "
                 f"{LEVELS * passes_per_level(F_ABUSE_FLOOR, 1000.0)} strokes")
    passed += ok

    ok = BIG_ACTUATOR_FLOOR_USD >= A1_PARTS
    lines.append(f"[{'PASS' if ok else 'FAIL'} ] big_actuator_cost_kills: "
                 f"floor ${BIG_ACTUATOR_FLOOR_USD:.0f} >= A1 ${A1_PARTS:.0f} "
                 f"(before plumbing/manifold)")
    passed += ok

    print(f"D1 platen gate: {passed}/{len(CHECKS)} kill-confirming checks hold")
    for line in lines:
        print(" ", line)
    return passed, len(CHECKS), lines


def main() -> None:
    parser = argparse.ArgumentParser(description="D1 global-platen gate")
    parser.add_argument("--gate", action="store_true",
                        help="run kill-confirming gate checks")
    parser.add_argument("--json", action="store_true", help="emit JSON summary")
    args = parser.parse_args()

    if args.json:
        import json as _json
        print(_json.dumps({
            "full_board_force_kN": {
                k: full_board_force_n(v) / 1000.0 for k, v in F_SNAP.items()},
            "abuse_floor_force_kN": full_board_force_n(F_ABUSE_FLOOR) / 1000.0,
            "banked_cycle_s": {
                "optimistic_generous": banked_cycle_s(
                    F_SNAP["low"], F_AFFORD_N["high"], V_GENEROUS_MM_S),
                "nominal": banked_cycle_s(
                    F_SNAP["nominal"], F_AFFORD_N["nominal"], V_NOMINAL_MM_S),
            },
            "big_actuator_floor_usd": BIG_ACTUATOR_FLOOR_USD,
        }, indent=1))
        return

    passed, total, _ = run_gate()
    if args.gate and passed != total:
        raise SystemExit(f"GATE INCOMPLETE: {passed}/{total} (D1 not killed)")


if __name__ == "__main__":
    main()
