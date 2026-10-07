#!/usr/bin/env python3
"""Reproduce the DES-005/A-011 Q-011 analytical screening gate."""
from math import pi

L = 406.4
E = 69_000.0
G = 79_000.0
RAIL = 25.0
SHAFT = 8.0
LEVER = 10.0
GATE = 0.10


def rail_mm(load_n, span=L):
    inertia = RAIL**4 / 12.0
    return load_n * span**3 / (48.0 * E * inertia)


def shaft_mm(torque_per_rotor_nmm, count=80):
    polar = pi * SHAFT**4 / 32.0
    return torque_per_rotor_nmm * count * L / (polar * G) * LEVER


def local_radial_mm(load_n=3.27, span=50.8):
    inertia = pi * SHAFT**4 / 64.0
    return load_n * span**3 / (48.0 * E * inertia)


def main():
    service_torque = 3.27 * 2.0
    print("DES-005/A-011 Q-011 frozen load-path screen (calculation only)")
    print(f"rail_3.27N_mm={rail_mm(3.27):.5f}")
    print(f"rail_100N_mm={rail_mm(100.0):.5f}")
    print(f"shaft_80x6.54Nmm_mm={shaft_mm(service_torque):.5f}")
    print(f"local_radial_3.27N_mm={local_radial_mm():.5f}")
    bounded_stack = 0.09
    combined = rail_mm(100.0) + shaft_mm(service_torque) + bounded_stack
    declared_stack = 0.60
    print(f"bounded_stack_mm={bounded_stack:.5f}")
    print(f"combined_100N_mm={combined:.5f} pass={combined < GATE}")
    print(f"declared_tolerance_stack_mm={declared_stack:.2f}")
    assert rail_mm(3.27) < GATE
    assert rail_mm(100.0) < GATE
    assert shaft_mm(service_torque) < GATE
    assert local_radial_mm() < GATE
    assert combined > GATE  # integration disposition remains HOLD


if __name__ == "__main__":
    main()
