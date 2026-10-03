#!/usr/bin/env python3
"""Reproducible calculated gate for the DES-003 coupon-B protocol.

This is a sensitivity calculation, not FEA and not physical validation.
Inputs are the design-calculated service load and proposed Q-005 motion gate.
"""

from __future__ import annotations

SERVICE_LOAD_N = 3.27
MOTION_GATE_MM = 0.10
SIDES = (5, 10, 20)
COUPLING = (0.01, 0.05, 0.10)
STIFFNESS = (10.0, 32.7, 50.0)


def boundary_cells(side: int) -> int:
    if side < 1:
        raise ValueError("side must be positive")
    return 1 if side == 1 else 4 * (side - 1)


def required_stiffness(side: int, alpha: float) -> float:
    """N/mm required by the proposed gate for per-boundary-cell coupling."""
    force = SERVICE_LOAD_N * boundary_cells(side) * alpha
    return force / MOTION_GATE_MM


def maximum_coupling(side: int, stiffness_n_per_mm: float) -> float:
    """Maximum per-boundary-cell coupling fraction at a candidate stiffness."""
    return (stiffness_n_per_mm * MOTION_GATE_MM /
            (SERVICE_LOAD_N * boundary_cells(side)))


def main() -> int:
    print("Coupon-B regional coupling gate (calculated sensitivity only)")
    print(f"service load={SERVICE_LOAD_N:.2f} N; motion gate={MOTION_GATE_MM:.2f} mm")
    print("\nregion | boundary | alpha | equivalent force (N) | k required (N/mm)")
    for side in SIDES:
        for alpha in COUPLING:
            force = SERVICE_LOAD_N * boundary_cells(side) * alpha
            print(f"{side:>2}x{side:<2} | {boundary_cells(side):>8} | {alpha:>5.1%} |"
                  f" {force:>20.3f} | {required_stiffness(side, alpha):>18.2f}")
    print("\nregion | alpha max at candidate stiffness")
    print("       | " + " | ".join(f"k={k:g} N/mm" for k in STIFFNESS))
    for side in SIDES:
        values = " | ".join(f"{maximum_coupling(side, k):.2%}" for k in STIFFNESS)
        print(f"{side:>2}x{side:<2}   | {values}")
    print("\nDisposition: NOT FALSIFIED, OPEN, and not qualified.")
    print("No physical validation, FEA, or measured stiffness is represented.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
