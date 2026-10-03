#!/usr/bin/env python3
"""E-009 analytical bound for untouched-neighbour motion.

This is a falsification screen, not FEA or physical validation.  It uses the
E-009 load-transfer model to calculate the stiffness required by the 0.10 mm
gate and the maximum admissible per-boundary-cell coupling at supplied
stiffness values.  Since DES-003 currently supplies neither measured stiffness
nor a bounded coupling/support/trajectory model, the disposition is explicitly
UNRESOLVED for every region.
"""

from __future__ import annotations

SERVICE_LOAD_N = 3.27
MOTION_GATE_MM = 0.10
REGIONS = (5, 10, 20)
COUPLING_SENSITIVITIES = (0.01, 0.05, 0.10)
STIFFNESS_SENSITIVITIES = (10.0, 32.7, 50.0)


def boundary_cells(side: int) -> int:
    if side < 1:
        raise ValueError("side must be positive")
    return 1 if side == 1 else 4 * (side - 1)


def equivalent_force(side: int, coupling: float) -> float:
    return SERVICE_LOAD_N * boundary_cells(side) * coupling


def predicted_motion(side: int, coupling: float, stiffness: float) -> float:
    if stiffness <= 0:
        raise ValueError("stiffness must be positive")
    return equivalent_force(side, coupling) / stiffness


def required_stiffness(side: int, coupling: float) -> float:
    return equivalent_force(side, coupling) / MOTION_GATE_MM


def maximum_coupling(side: int, stiffness: float) -> float:
    return stiffness * MOTION_GATE_MM / (SERVICE_LOAD_N * boundary_cells(side))


def main() -> int:
    print("E-009 DES-003 analytical regional-coupling bound")
    print("calculated inputs: service load=%.2f N; proposed motion gate=%.2f mm" %
          (SERVICE_LOAD_N, MOTION_GATE_MM))
    print("evidence limits: no measured/FEA stiffness, coupling, support, or trajectory")
    print("\nRequired support stiffness for each assumed coupling fraction")
    print("region | boundary cells | " + " | ".join("alpha=%g" % a for a in COUPLING_SENSITIVITIES))
    for side in REGIONS:
        values = " | ".join("%7.2f N/mm" % required_stiffness(side, a)
                             for a in COUPLING_SENSITIVITIES)
        print("%2dx%-2d   | %14d | %s" % (side, side, boundary_cells(side), values))

    print("\nMaximum coupling fraction that would meet the gate")
    print("region | " + " | ".join("k=%g N/mm" % k for k in STIFFNESS_SENSITIVITIES))
    for side in REGIONS:
        values = " | ".join("%8.3f%%" % (100 * maximum_coupling(side, k))
                             for k in STIFFNESS_SENSITIVITIES)
        print("%2dx%-2d   | %s" % (side, side, values))

    print("\nDisposition")
    for side in REGIONS:
        print("%2dx%-2d: UNRESOLVED (analytical sensitivity only; no defensible bound)" %
              (side, side))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
