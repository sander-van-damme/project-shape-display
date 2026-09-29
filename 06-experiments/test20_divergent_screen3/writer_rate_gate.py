"""SHA-17 divergent screen — E3 external-robot writer rate gate.

Cheapest analytic test for the single advanced mechanism of SHA-17: the
off-board robot writer (commodity desktop arm / XY plotter + Z press)
setting passive printed ratchet columns one touch at a time.

Evidence class: CALCULATION over sourced-class robot cycle rates plus
board geometry (02). No print, no purchase, no measurement (DND-27).

Binding insight asserted and checked below: a serial off-board touch
process must sustain >= 213 cells/s for a full-map < 30 s change, but a
hobby pick-press cycle is class ~1-2.5 cells/s — shortfall ~85-200x at
the optimistic corner. Parallelising into 64+ fingers rebuilds the
gantry it was meant to delete, at a cost floor above A1 $181. Hobby-arm
repeatability (+/-0.2-0.5 mm) against 5.08 mm pitch adds a silent
mis-press mode with no on-board readback.

Kill criteria (up front, binding):
  KC2 timing .. serial full-map press cycle must fit < 30 s incl.
                travel/press/settle; KILL if the optimistic corner alone
                already exceeds 30 s.
  KC1 cost .... parallel fingers needed to close the rate gap must beat
                A1 ($181); KILL if fingers x $/finger floor exceeds A1.
  (KC3 pitch-vs-repeatability recorded in the verdict note; the rate gap
  kills first and needs no measurement.)

Run:  python 06-experiments/test20_divergent_screen3/writer_rate_gate.py
Gate: python 06-experiments/test20_divergent_screen3/writer_rate_gate.py --gate
"""

from __future__ import annotations

import argparse
import math

# ---- Board geometry (design criteria 02) ----
N_COLS = 6400            # 80x80
TIME_BUDGET_S = 30.0     # full-map change strictly < 30 s

# ---- Sourced-class serial press cycle (2026-09 class sweep, ranges) ----
# Hobby pick-press cycle (move + press + retract): optimistic 0.4 s/cell
# (fast desktop SCARA class, short travel), nominal 1.0 s, slow 1.5 s.
# Confidence: medium (catalog cycle class, not a quotation).
T_CELL = {"optimistic": 0.4, "nominal": 1.0, "slow": 1.5}  # s/cell
# Demonstrated sustained serial rate of the optimistic corner.
DEMO_RATE_S = 1.0 / T_CELL["optimistic"]  # ~2.5 cells/s
# Required sustained rate for a full-map change inside the budget.
REQUIRED_RATE_S = N_COLS / TIME_BUDGET_S  # ~213.3 cells/s

# ---- Sourced-class parallel-finger costing ----
# One press finger channel (solenoid/mini-actuator + driver share):
# floor ~$8/channel before frame/wiring (low-medium confidence, wide).
FINGER_FLOOR_USD = 8.0
A1_PARTS = 181.0         # SHA-7 sourced-class BOM (medium)

# ---- Sourced-class repeatability vs pitch (KC3 corroboration) ----
PITCH_MM = 5.08
REPEAT_MM = {"optimistic": 0.2, "nominal": 0.5}  # hobby-arm class

CHECKS: list[tuple[str, str]] = [
    ("serial_time_kills",
     "optimistic serial full-map time >> 30 s"),
    ("rate_shortfall_kills",
     "required rate exceeds demonstrated serial rate by >= 50x"),
    ("parallel_heads_cost_kills",
     "fingers to close the gap cost past A1 $181"),
    ("nominal_serial_kills",
     "nominal serial time >> 30 s (corroboration)"),
    ("pitch_repeatability_kills",
     "nominal repeatability eats the pitch margin (silent mis-press)"),
]


def serial_time_s(t_cell: float) -> float:
    """Full-map serial press time, zero overhead credited."""
    return N_COLS * t_cell


def fingers_needed(t_cell: float) -> int:
    """Parallel fingers so N cells finish inside the budget."""
    return math.ceil(serial_time_s(t_cell) / TIME_BUDGET_S)


def run_gate() -> tuple[int, int, list[str]]:
    lines: list[str] = []
    passed = 0

    t_opt = serial_time_s(T_CELL["optimistic"])
    ok = t_opt >= TIME_BUDGET_S
    lines.append(f"[{'PASS' if ok else 'FAIL'} ] serial_time_kills: "
                 f"{t_opt:.0f} s optimistic serial >= {TIME_BUDGET_S:.0f} s budget")
    passed += ok

    gap = REQUIRED_RATE_S / DEMO_RATE_S
    ok = gap >= 50.0
    lines.append(f"[{'PASS' if ok else 'FAIL'} ] rate_shortfall_kills: "
                 f"{REQUIRED_RATE_S:.0f} cells/s required vs "
                 f"{DEMO_RATE_S:.1f} demonstrated = {gap:.0f}x gap >= 50x")
    passed += ok

    n = fingers_needed(T_CELL["optimistic"])
    cost = n * FINGER_FLOOR_USD
    ok = cost >= A1_PARTS
    lines.append(f"[{'PASS' if ok else 'FAIL'} ] parallel_heads_cost_kills: "
                 f"{n} fingers x ${FINGER_FLOOR_USD:.0f} = ${cost:.0f} "
                 f">= A1 ${A1_PARTS:.0f}")
    passed += ok

    t_nom = serial_time_s(T_CELL["nominal"])
    ok = t_nom >= TIME_BUDGET_S
    lines.append(f"[{'PASS' if ok else 'FAIL'} ] nominal_serial_kills: "
                 f"{t_nom:.0f} s nominal serial >= {TIME_BUDGET_S:.0f} s budget")
    passed += ok

    # Generous reading: mis-press when 3-sigma repeatability exceeds
    # half the pitch-to-feature margin (~1 mm usable at 5.08 mm pitch
    # with 0.4 mm features and print variation).
    margin = 1.0  # mm, generous
    ok = 3 * REPEAT_MM["nominal"] >= margin
    lines.append(f"[{'PASS' if ok else 'FAIL'} ] pitch_repeatability_kills: "
                 f"3-sigma {3 * REPEAT_MM['nominal']:.1f} mm >= "
                 f"{margin:.1f} mm margin (silent wrong-tooth press)")
    passed += ok

    print(f"E3 writer gate: {passed}/{len(CHECKS)} kill-confirming checks hold")
    for line in lines:
        print(" ", line)
    return passed, len(CHECKS), lines


def main() -> None:
    parser = argparse.ArgumentParser(description="E3 external-robot writer gate")
    parser.add_argument("--gate", action="store_true",
                        help="run kill-confirming gate checks")
    parser.add_argument("--json", action="store_true", help="emit JSON summary")
    args = parser.parse_args()

    if args.json:
        import json as _json
        print(_json.dumps({
            "required_rate_cells_s": REQUIRED_RATE_S,
            "demo_rate_cells_s": DEMO_RATE_S,
            "gap_factor": REQUIRED_RATE_S / DEMO_RATE_S,
            "serial_time_s": {k: serial_time_s(v) for k, v in T_CELL.items()},
            "fingers_needed_optimistic": fingers_needed(T_CELL["optimistic"]),
            "fingers_cost_floor_usd":
                fingers_needed(T_CELL["optimistic"]) * FINGER_FLOOR_USD,
        }, indent=1))
        return

    passed, total, _ = run_gate()
    if args.gate and passed != total:
        raise SystemExit(f"GATE INCOMPLETE: {passed}/{total} (E3 not killed)")


if __name__ == "__main__":
    main()
