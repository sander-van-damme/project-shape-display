"""Bounded analytical check for loaded-neighbour disturbance.

This is a sensitivity model, not a structural simulation. It separates the
known service load from the unknown fraction of regional actuation load that
could couple into one untouched neighbour. No material stiffness or coupling
coefficient is asserted as measured evidence.
"""

from __future__ import annotations

SERVICE_LOAD_N = 3.27  # design-calculated loaded-neighbour service load
Q5_GATE_MM = 0.10      # proposed coupon gate, not an established product limit


def boundary_cells(side: int) -> int:
    """Number of cells on the perimeter of a square region."""
    if side < 1:
        raise ValueError("side must be positive")
    return 1 if side == 1 else 4 * (side - 1)


def displacement(force_n: float, stiffness_n_per_mm: float) -> float:
    """Return linear spring displacement in millimetres."""
    if force_n < 0 or stiffness_n_per_mm <= 0:
        raise ValueError("force must be non-negative and stiffness positive")
    return force_n / stiffness_n_per_mm


def required_stiffness(force_n: float) -> float:
    """Stiffness required to meet the proposed displacement gate."""
    return force_n / Q5_GATE_MM


def sweep(sides=(5, 10, 20), coupling=(0.01, 0.05, 0.10)) -> list[dict]:
    """Evaluate explicit per-boundary-cell load-transfer sensitivities."""
    rows = []
    for side in sides:
        perimeter = boundary_cells(side)
        for fraction in coupling:
            force = SERVICE_LOAD_N * perimeter * fraction
            rows.append({
                "region": f"{side}x{side}",
                "boundary_cells": perimeter,
                "coupling_fraction": fraction,
                "effective_force_n": force,
                "required_stiffness_n_per_mm": required_stiffness(force),
            })
    return rows


def critical_coupling(side: int, stiffness_n_per_mm: float) -> float:
    """Maximum per-boundary-cell coupling fraction at a given stiffness."""
    return (stiffness_n_per_mm * Q5_GATE_MM /
            (SERVICE_LOAD_N * boundary_cells(side)))


def main() -> int:
    print("E-006 bounded elastic-disturbance sensitivity")
    print("Inputs: service load %.2f N; proposed gate %.2f mm" %
          (SERVICE_LOAD_N, Q5_GATE_MM))
    print("\nPer-boundary-cell coupling sensitivity")
    print("region | boundary | coupling | force (N) | k required (N/mm)")
    for row in sweep():
        print("{region:>6} | {boundary_cells:>8} | {coupling_fraction:>8.2%} | "
              "{effective_force_n:>9.3f} | {required_stiffness_n_per_mm:>16.2f}"
              .format(**row))
    print("\nCritical coupling fraction for candidate stiffness sensitivities")
    print("region | k=10 N/mm | k=32.7 N/mm | k=50 N/mm")
    for side in (5, 10, 20):
        print("%6dx%-5d | %10.2f%% | %12.2f%% | %10.2f%%" %
              (side, side, critical_coupling(side, 10.0) * 100,
               critical_coupling(side, 32.7) * 100,
               critical_coupling(side, 50.0) * 100))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
