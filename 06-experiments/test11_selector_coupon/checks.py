#!/usr/bin/env python3
"""Test11 acceptance checks.  Pure stdlib; each check is falsifiable.

Exit code 0 = all analytical checks pass; 1 = at least one fails.  A failed
check is a *design* result, not a bug: it is how the coupon-boundary is found
before CAD/BOM.  No check substitutes for the printed coupon.
"""
from __future__ import annotations

import sys

import coupon_geometry as g


def check_min_printable_wall() -> tuple[bool, str]:
    band = g.PITCH - g.BODY - 2 * g.CLEAR
    need = 2 * g.A_PRINT_WALL_MIN
    return (band < need,
            "cell lattice wall band %.3f mm is thinner than two printed walls "
            "%.2f mm => gate slot + load-bearing wall cannot share the band"
            % (band, need))


def check_linear_gate() -> tuple[bool, str]:
    d = g.gate_stroke_band()
    return (not d["blocked"],
            d["verdict"] + " => a linear gate needs pitch >= %.2f mm or a "
            "narrower body" % (g.BODY + 2 * g.A_PRINT_WALL_MIN + d["printable_slot_plus_walls_mm"]))


def check_rotary_blade_fits() -> tuple[bool, str]:
    d = g.radial_budget()
    fits = d["clearance_to_neighbour_mm"] >= 0.10
    return (fits,
            "rotary blade must stay out of the neighbour: clearance %.2f mm "
            "(needs >= 0.10 mm) => %.2f mm blade crosses an occupied cell"
            % (d["clearance_to_neighbour_mm"], d["gate_blade_length_mm"] - 0.10))


def check_shared_stroke() -> tuple[bool, str]:
    d = g.shared_stroke_partition()
    return (d["fraction_of_40mm"] < 1.0,
            "shared stroke is %.0f%% of 40 mm; %d strokes reach the top, "
            "independent of column count"
            % (100 * d["fraction_of_40mm"], d["strokes_needed_to_reach_top"]))


def check_tooth_overlap() -> tuple[bool, str]:
    d = g.tooth_overlap()
    return (d["actual_blade_overlap_mm"] >= 0.25,
            "actual engaged overlap is %.2f mm, not the intended %.2f mm; "
            "the %.2f mm tip recess consumes %.0f%% of it"
            % (d["actual_blade_overlap_mm"], d["intended_overlap_mm"],
               g.A_RECESS, 100 * (d["overlap_shortfall_vs_intent_mm"] / d["intended_overlap_mm"])))


def check_retaining_face_abuse() -> tuple[bool, str]:
    d = g.retaining_face_abuse()
    # A printed coupon must measure this; the calculation only flags the region.
    return (d["avg_shear_stress_mpa"] < 20.0,
            "one latch tooth sees %.1f MPa average shear at the 5 N abuse gate "
            "(PLA shear yield ~30-40 MPa ideal); edge stress concentration is "
            "unmodelled" % d["avg_shear_stress_mpa"])


def check_gate_bus() -> tuple[bool, str]:
    d = g.gate_bus()
    return (d["fits_dwell"],
            "addressing 80 columns on one 2-wire gate bus takes %.3f s > the "
            "0.60 s dwell; %d gates draw %.1f A if energised together"
            % (d["worst_total_s"], d["columns"], d["simultaneous_current_a"]))


CHECKS = [
    ("MIN_PRINTABLE_WALL", check_min_printable_wall),
    ("LINEAR_GATE", check_linear_gate),
    ("ROTARY_BLADE_FITS", check_rotary_blade_fits),
    ("SHARED_STROKE", check_shared_stroke),
    ("TOOTH_OVERLAP", check_tooth_overlap),
    ("RETAINING_FACE_ABUSE", check_retaining_face_abuse),
    ("GATE_BUS", check_gate_bus),
]


def main() -> int:
    failures = 0
    print("Test11 selector-fanout coupon checks (calculated, not measured)\n")
    for name, fn in CHECKS:
        try:
            ok, msg = fn()
        except Exception as exc:  # pragma: no cover - defensive
            ok, msg = False, "raised %r" % (exc,)
        status = "PASS" if ok else "FAIL"
        if not ok:
            failures += 1
        print("[%s] %-24s %s" % (status, name, msg))
    print("\n%d check(s) failed" % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
