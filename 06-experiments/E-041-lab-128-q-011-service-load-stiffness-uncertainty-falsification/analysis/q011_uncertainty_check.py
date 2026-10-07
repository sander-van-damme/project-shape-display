#!/usr/bin/env python3
"""Sensitivity check for the inherited Q-011 beam/shaft screening model."""
from math import pi

L = 406.4
E_AL = 69_000.0
G_STEEL = 79_000.0
GATE = 0.10
LEVER = 10.0


def beam_mm(load_n: float, side_mm: float) -> float:
    inertia = side_mm * side_mm**3 / 12.0
    return load_n * L**3 / (48.0 * E_AL * inertia)


def torsion_mm(torque_per_rotor_nmm: float, count: int, diameter_mm: float) -> float:
    total_torque = torque_per_rotor_nmm * count
    polar = pi * diameter_mm**4 / 32.0
    return total_torque * L / (polar * G_STEEL) * LEVER


def main() -> None:
    print("Q-011 uncertainty screen (calculation only)")
    print("rail: load_N side_mm deflection_mm pass")
    for load in (100.0, 150.0, 200.0):
        for side in (20.0, 25.0):
            value = beam_mm(load, side)
            print(f"rail: {load:.0f} {side:.0f} {value:.6f} {value < GATE}")
    print("shaft: torque_per_rotor_Nmm diameter_mm motion_mm pass")
    for torque in (4.0, 8.0):
        for diameter in (6.0, 8.0):
            value = torsion_mm(torque, 80, diameter)
            print(f"shaft: {torque:.1f} {diameter:.1f} {value:.6f} {value < GATE}")
    assert beam_mm(100.0, 25.0) < GATE
    assert beam_mm(150.0, 25.0) < GATE
    assert beam_mm(200.0, 25.0) > GATE
    assert beam_mm(100.0, 20.0) > GATE
    assert torsion_mm(4.0, 80, 8.0) < GATE
    assert torsion_mm(8.0, 80, 8.0) < GATE
    assert torsion_mm(4.0, 80, 6.0) > GATE
    assert torsion_mm(8.0, 80, 6.0) > GATE


if __name__ == "__main__":
    main()
