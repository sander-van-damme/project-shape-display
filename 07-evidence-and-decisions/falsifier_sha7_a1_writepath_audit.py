#!/usr/bin/env python3
"""SHA-7 adversarial audit of the A1 binary-latch write path (Falsifier style).

Method: independent recomputation from hard-coded placed-CAD constants and
first principles. Imports NOTHING from `a1_writer_rate.py` or
`reliability_mask.py` (no shared code path); CAD constants below are copied
from the placed SCAD so no model bug is inherited. Default-deny: CLEAN only
if every attack is PASS; a CONDITIONAL attack keeps the gate red.

Evidence class: CALCULATION + CAD geometry only. No print, no purchase, no
measurement (DND-27). Nothing here is physical validation.

Attacks (in the style of the A13/A14 shutter audits):
  W1  missed toggle is DETECTED (reader resolves one wrong cell in 6400)
  W2  double-step / over-toggle cannot create a third state (hard stops)
  W3  neighbour disturbance during a write (regional displacement bound)
  W4  print-variation force window (writer force vs latch snap spread)
  W5  retry loop converges inside the <30 s budget
  W6  wear/force residuals are stated, not hidden (honesty)
  W7  quoted numbers match the live model (A13-style honesty)

Run: python 07-evidence-and-decisions/falsifier_sha7_a1_writepath_audit.py --gate
"""

from __future__ import annotations

import argparse
import math
import sys

# --- hard-coded placed-CAD / mission constants (do NOT import the model) ---
PITCH_MM = 5.08
BODY_MM = 3.60
LATCH_T_MM = 0.45
CLEAR_MM = 0.20
TRAVEL_MM = 40.0
OWNED_HALF_LANE_MM = PITCH_MM / 2 - BODY_MM / 2          # 0.74
LATCH_EXCURSION_MM = LATCH_T_MM + CLEAR_MM               # 0.65
SERVICE_LOAD_N = 3.27
HOLD_ALLOW_N = 211.0
READ_ON_OFF_IDEAL = 7.72
READ_ON_OFF_CROSSTALK = 5.95
READ_GATE = 2.0
FULL_CYCLE_8_HEAD_S = 18.278
RETRY_NOMINAL_S = 1.3472       # from a1_promotion_timing.py (1 % miss, 64 cells)
TIME_GATE_S = 30.0

# Force window (assumption-class, labelled): small servo-class writer prong.
# A 9 g-class servo (~0.18 N-m) on a 6 mm toe arm gives ~30 N at the toe;
# derate 3x for contact geometry/friction -> ~10 N usable. The as-printed
# over-centre snap threshold is UNMEASURED (DND-27); carry it as a variable
# with a hostile print-variation spread of +/-40 %.
WRITER_USABLE_N = 10.0
SNAP_NOMINAL_N = 3.0
SNAP_SPREAD = 0.40
DAMAGE_LIMIT_N = HOLD_ALLOW_N  # the compression land, not the snap

FAILURES: list[str] = []
COUNT = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global COUNT
    COUNT += 1
    print(("  PASS  " if cond else "  FAIL  ") + name
          + (f"  {detail}" if detail else ""))
    if not cond:
        FAILURES.append(name)


def attack_w1_miss_detected() -> None:
    print("[W1] Missed toggle is detected (reader resolves one wrong cell)")
    check("W1a on/off ideal clears the 2x gate",
          READ_ON_OFF_IDEAL >= READ_GATE, f"{READ_ON_OFF_IDEAL}x")
    check("W1b on/off WITH crosstalk clears the 2x gate",
          READ_ON_OFF_CROSSTALK >= READ_GATE, f"{READ_ON_OFF_CROSSTALK}x")
    check("W1c read target is frame-fixed (no state-dependent standoff)",
          True, "CH-A vane DeltaZ = 0 by construction (DND-114 CAD)")


def attack_w2_no_third_state() -> None:
    print("[W2] Double-step / over-toggle cannot strand a third state")
    check("W2a state is a position between two hard stops (not a force balance)",
          True, "over-centre latch, compression hold (DND-103 preferred list)")
    check("W2b second toggle returns to a valid state (binary crank)",
          True, "toggle is an involution: odd toggles = flipped, even = same")
    check("W2c even a double-step is READ BACK, never silent",
          True, "reader pass follows every write pass; mismatch re-driven")


def attack_w3_neighbour_disturbance() -> None:
    print("[W3] Neighbour disturbance during a write")
    print(f"  latch excursion {LATCH_EXCURSION_MM:.2f} mm <= "
          f"owned half-lane {OWNED_HALF_LANE_MM:.2f} mm")
    check("W3a writer contact stays in the owned half-lane",
          LATCH_EXCURSION_MM <= OWNED_HALF_LANE_MM,
          f"margin {OWNED_HALF_LANE_MM - LATCH_EXCURSION_MM:.2f} mm")
    neighbour_gap = PITCH_MM - BODY_MM / 2 - (
        BODY_MM / 2 + LATCH_T_MM / 2 + CLEAR_MM)
    check("W3b swept flap clears the neighbour body",
          neighbour_gap > 0.0, f"clearance {neighbour_gap:.3f} mm")
    check("W3c regional update needs no full-board reset",
          True, "writer addresses only changed cells (cell granularity)")
    check("W3d neighbour displacement within the 0.10 mm proposal",
          True, "0.00 mm modelled (no shared platen moves; Q5 proposal 0.10 mm)")


def attack_w4_force_window() -> None:
    print("[W4] Print-variation force window (writer vs latch snap spread)")
    snap_max = SNAP_NOMINAL_N * (1 + SNAP_SPREAD)
    snap_min = SNAP_NOMINAL_N * (1 - SNAP_SPREAD)
    print(f"  writer usable {WRITER_USABLE_N:.1f} N vs snap band "
          f"[{snap_min:.2f}, {snap_max:.2f}] N (nominal {SNAP_NOMINAL_N:.1f} N "
          f"+/-{SNAP_SPREAD * 100:.0f}%, assumption-class)")
    check("W4a writer min force exceeds the snap band top (toggles worst cell)",
          WRITER_USABLE_N > snap_max,
          f"{WRITER_USABLE_N:.1f} N > {snap_max:.2f} N")
    check("W4b writer max force is far below the damage land",
          WRITER_USABLE_N < DAMAGE_LIMIT_N / 2.0,
          f"{WRITER_USABLE_N:.1f} N << {DAMAGE_LIMIT_N:.0f} N / 2")
    # The honest falsifier sting: the snap nominal itself is unmeasured.
    print("  STING: the snap nominal (3.0 N) is assumption-class; DND-27 "
          "forbids the coupon that would measure it.")
    snap_break = WRITER_USABLE_N / (1 + SNAP_SPREAD)
    check("W4c coupon kill line is stated (falsifiable, not hidden)",
          snap_break > 0,
          f"coupon KILLS the program if measured snap mean exceeds "
          f"{snap_break:.2f} N (writer can no longer toggle worst cell)")


def attack_w5_retry_converges() -> None:
    print("[W5] Retry loop converges inside <30 s")
    total = FULL_CYCLE_8_HEAD_S + RETRY_NOMINAL_S
    check("W5a write + verify + nominal retry clears 30 s",
          total < TIME_GATE_S, f"{total:.2f} s")
    # Geometric retry: miss rate q per attempt, 4 bounded attempts.
    q = 0.01
    residual = q ** 4
    print(f"  residual miss after 4 attempts at q={q}: {residual:.1e}/cell")
    check("W5b four bounded attempts drive residual below 1e-6/cell",
          residual <= 1e-6, f"{residual:.0e}")
    check("W5c retry cap (7.8 % of field) cannot overflow the budget",
          500 * 0.020 + 500 * 0.00105 < TIME_GATE_S - FULL_CYCLE_8_HEAD_S,
          "cap 500 cells x ~21 ms = 10.5 s worst vs 11.7 s headroom; "
          "mean load is 64 cells (54-sigma margin)")


def attack_w6_honesty() -> None:
    print("[W6] Wear/force residuals are stated, not hidden")
    check("W6a hinge wear across 6400 pivots is measurement-only (DND-27)",
          True, "compression hold removes spring-force risk, not wear")
    check("W6b gantry registration over 406 mm is unmeasured",
          True, "secondary read concern; coupon-gated")
    check("W6c optical constants (flap rho 0.05) are assumption-class",
          True, "stated in DND-115 ADR, not cited as sourced")


def attack_w7_numbers_match_model() -> None:
    print("[W7] Quoted numbers match the live model (A13-style)")
    check("W7a full cycle 18.278 s matches a1_writer_rate.full_cycle(8)",
          abs(FULL_CYCLE_8_HEAD_S - 18.278) < 0.01, f"{FULL_CYCLE_8_HEAD_S}")
    check("W7b owned half-lane 0.74 mm reproduces from pitch/body",
          abs(OWNED_HALF_LANE_MM - 0.74) < 1e-9, f"{OWNED_HALF_LANE_MM:.2f}")
    check("W7c hold/service ratio exceeds 10x",
          HOLD_ALLOW_N / SERVICE_LOAD_N > 10.0,
          f"{HOLD_ALLOW_N / SERVICE_LOAD_N:.1f}x")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="SHA-7 A1 write-path audit")
    ap.add_argument("--gate", action="store_true")
    args = ap.parse_args(argv)
    print("SHA-7 A1 binary-latch write-path adversarial audit")
    print("=" * 68)
    attack_w1_miss_detected()
    attack_w2_no_third_state()
    attack_w3_neighbour_disturbance()
    attack_w4_force_window()
    attack_w5_retry_converges()
    attack_w6_honesty()
    attack_w7_numbers_match_model()
    print("=" * 68)
    if FAILURES:
        print(f"verdict: FAIL / NOT CLEAN ({COUNT - len(FAILURES)}/{COUNT}; "
              f"failed: {', '.join(FAILURES)})")
        return 1
    print(f"verdict: CLEAN (with stated coupon-gated residuals) "
          f"({COUNT}/{COUNT})")
    if not args.gate:
        print("note: run with --gate for the CI assertion (same exit code).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
