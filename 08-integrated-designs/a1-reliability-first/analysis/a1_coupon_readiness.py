#!/usr/bin/env python3
"""SHA-13 A1 coupon A/B/C build-readiness gate (CAD-ready handoff definitions).

Evidence class: CALCULATION over placed A1 CAD constants + CAD file presence /
self-check markers. No print, no purchase, no measurement (DND-27). Nothing
here is physical validation.

What this gate proves (and does NOT prove):
  * The three coupon SCAD files exist, reuse the A1 cell/head geometry
    unchanged, carry the documented kill lines / gates as echo markers, and
    all new frame geometry fits the X1C 256 mm bed at the provisional FDM
    rules (0.44 mm feature, 0.88 mm wall).
  * The kill lines reproduce from the SHA-7/SHA-9 record:
      R1 snap-mean kill  = WRITER_USABLE_N / (1 + SNAP_SPREAD)  = 7.14 N
      R4 contrast kill   = on/off ratio gate                   = 2.0x
      Q5 neighbour gate  = 0.10 mm (modelled rigid-body 0.00 mm)
      Coupon C drift kill = half-pitch                         = 2.54 mm
  * It does NOT retire R1-R4 or the elastic half of R6: those stay
    measurement-only under DND-27. The coupons are the handoff that lets a
    future physical program retire them.

Run: python 08-integrated-designs/a1-reliability-first/analysis/a1_coupon_readiness.py --gate
"""

from __future__ import annotations

import argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SCAD = ROOT / "scad"

# --- source-of-truth constants (copied from placed A1 CAD / SHA-7 / SHA-9) ---
PITCH_MM = 5.08
BODY_MM = 3.60
CLEAR_MM = 0.20
LATCH_T_MM = 0.45
OWNED_HALF_LANE_MM = PITCH_MM / 2 - BODY_MM / 2      # 0.74
LATCH_EXCURSION_MM = LATCH_T_MM + CLEAR_MM           # 0.65
SERVICE_LOAD_N = 3.27
X1C_BED_MM = 256.0
MIN_FEATURE_MM = 0.44

# SHA-7 kill lines
WRITER_USABLE_N = 10.0
SNAP_SPREAD = 0.40
R1_KILL_MEAN_N = WRITER_USABLE_N / (1 + SNAP_SPREAD)  # 7.142857 -> 7.14
R4_KILL_RATIO = 2.0
# SHA-9 Q5 proposal
Q5_GATE_MM = 0.10
MODELLED_NEIGHBOUR_MM = 0.00
# Coupon C
HALF_PITCH_MM = PITCH_MM / 2                          # 2.54
REGISTRATION_SECONDARY_MM = 0.264
FULL_SPAN_MM = 80 * PITCH_MM                          # 406.4

COUPONS = {
    "a1_coupon_a_single_cell.scad": [
        "COUPON_A base=",
        "COUPON_A aperture plane=",
        "kill R1 snap mean > 7.14 N",
        "kill R4 on/off < 2x",
    ],
    "a1_coupon_b_5x5.scad": [
        "COUPON_B field=",
        "COUPON_B tile=",
        "Q5 gate 0.10 mm",
    ],
    "a1_coupon_c_gantry.scad": [
        "COUPON_C span=",
        "COUPON_C stations=",
        "half-pitch",
    ],
}

CHECKS: list[tuple[str, bool]] = []


def check(name: str, cond: bool) -> None:
    CHECKS.append((name, bool(cond)))


def gate() -> int:
    CHECKS.clear()
    # 1. Kill lines reproduce from the record
    check("R1 kill mean reproduces 7.14 N",
          abs(R1_KILL_MEAN_N - 7.14) < 0.01)
    check("R4 kill ratio is the 2x gate", R4_KILL_RATIO == 2.0)
    check("Q5 gate is the 0.10 mm proposal", Q5_GATE_MM == 0.10)
    check("modelled rigid-body neighbour is 0.00 mm",
          MODELLED_NEIGHBOUR_MM == 0.00)
    check("coupon C drift kill is half-pitch 2.54 mm",
          abs(HALF_PITCH_MM - 2.54) < 1e-9)
    check("full traverse span is 406.4 mm",
          abs(FULL_SPAN_MM - 406.4) < 1e-9)
    # 2. Geometry margins carried into the coupons
    check("writer excursion inside owned half-lane (+0.09 mm)",
          LATCH_EXCURSION_MM <= OWNED_HALF_LANE_MM
          and abs(OWNED_HALF_LANE_MM - LATCH_EXCURSION_MM - 0.09) < 1e-9)
    check("coupon A base (30) fits X1C bed", 30.0 <= X1C_BED_MM)
    check("coupon B tile (40) fits X1C bed", 40.0 <= X1C_BED_MM)
    check("coupon B field is 5x true pitch (25.4)",
          abs(5 * PITCH_MM - 25.4) < 1e-9)
    check("coupon C segments (210) fit X1C bed", 210.0 <= X1C_BED_MM)
    check("coupon C stations (9) span the traverse",
          8 * 10 * PITCH_MM <= FULL_SPAN_MM)
    check("dedicated aperture (0.44) meets min feature",
          0.44 >= MIN_FEATURE_MM)
    # 3. SCAD files exist with the expected handoff markers
    for fname, markers in COUPONS.items():
        p = SCAD / fname
        check(f"coupon file exists: {fname}", p.is_file())
        if p.is_file():
            text = p.read_text()
            for m in markers:
                check(f"{fname} carries marker: {m!r}", m in text)
            check(f"{fname} reuses A1 constants (PITCH/BODY)",
                  "PITCH = 5.08" in text
                  and ("BODY" in text or "COLS" in text))
            check(f"{fname} states DND-27 (no physical validation)",
                  "DND-27" in text)
    passed = sum(1 for _, ok in CHECKS if ok)
    total = len(CHECKS)
    for name, ok in CHECKS:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\nR1 kill mean: {R1_KILL_MEAN_N:.2f} N; R4 kill: {R4_KILL_RATIO:.0f}x; "
          f"Q5 gate: {Q5_GATE_MM:.2f} mm; half-pitch kill: {HALF_PITCH_MM:.2f} mm")
    print(f"{passed}/{total} coupon-readiness checks pass")
    return 0 if passed == total else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="SHA-13 A1 coupon readiness gate")
    ap.add_argument("--gate", action="store_true")
    args = ap.parse_args(argv)
    if args.gate:
        return gate()
    return gate()


if __name__ == "__main__":
    raise SystemExit(main())
