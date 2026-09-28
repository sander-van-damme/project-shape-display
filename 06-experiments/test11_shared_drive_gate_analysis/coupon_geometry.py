#!/usr/bin/env python3
"""Geometry self-consistency check for selector_fanout_coupon.scad.

OpenSCAD is not available in every run environment, so this script reads the
SAME parametric values and asserts the fit arithmetic that the coupon is meant
to test. It is a *CALCULATED* geometry screen, not a rendered or printed result.

If OpenSCAD is present, render the coupon as well:
    openscad -o selector_fanout_coupon.stl selector_fanout_coupon.scad

Run: python coupon_geometry.py
"""

from __future__ import annotations

from math import asin, degrees

PITCH = 5.08
ROWS_PER_STATION = 4
BAND = PITCH / ROWS_PER_STATION          # 1.27 mm cam land per row

FINGER_T = 0.80
FINGER_H = 3.20
FINGER_L = 4.40
PIVOT_D = 0.80
NOTCH_D = 0.55

# Per-row finger envelope must fit inside the band shared by 4 rows.
finger_fit_mm = BAND - FINGER_T          # slack between neighbouring fingers
finger_web_mm = BAND - FINGER_T          # printed gap left in the band

# Rocker angular throw that a 0.9 mm cam land can produce at FINGER_H/2:
LAND_H = 0.90
throw_deg = degrees(asin(min(1.0, LAND_H / FINGER_H)))

# Cross-cell: two columns share the 406 mm width at 5.08 pitch; the finger must
# not cross into the neighbour. FINGER_L is along travel, FINGER_T across the row
# axis, so the lateral envelope is finger thickness only.
lat_margin = PITCH - FINGER_T - PIVOT_D  # pivot band vs neighbour column

def main() -> None:
    rows = [
        ("finger fits one 1.27 mm row band", FINGER_T < BAND, f"{FINGER_T:.2f} < {BAND:.2f} mm"),
        ("positive web between adjacent fingers", finger_web_mm >= 0.20, f"web {finger_web_mm:.2f} mm"),
        ("bank throw from 0.9 mm land", 5.0 <= throw_deg <= 40.0, f"{throw_deg:.1f} deg"),
        ("notch is a printable feature on 0.2 mm nozzle", NOTCH_D >= 0.20, f"d={NOTCH_D:.2f} mm"),
        ("lateral clearance to neighbour column", lat_margin > 0, f"{lat_margin:.2f} mm"),
        ("0.4 mm nozzle can print the 0.55 mm notch", NOTCH_D >= 0.4, f"d={NOTCH_D:.2f} mm"),
    ]
    ok = True
    for name, cond, detail in rows:
        print(f"[{'PASS' if cond else 'FAIL'}] {name}: {detail}")
        ok &= cond
    print()
    print("COUPON GEOMETRY CONSISTENT (not rendered, not printed)" if ok else "GEOMETRY INVALID")
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
