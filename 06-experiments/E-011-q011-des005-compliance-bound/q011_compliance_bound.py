#!/usr/bin/env python3
"""Bound omitted DES-005 interface compliance without inventing stiffness.

Calculation only: the four omitted terms are nonnegative series springs. The
script deliberately exposes the zero-compliance limit, which is enough to
test whether the retained 100 N rail-plus-shaft baseline can pass Q-011.
"""
from math import pi

L = 406.4
E_RAIL = 69_000.0
G_SHAFT = 79_000.0
RAIL = 25.0
SHAFT = 8.0
TORQUE_RADIUS = 2.0
OUTPUT_LEVER = 10.0
ROTOR_COUNT = 80
SERVICE_FORCE = 3.27
SERVICE_TORQUE = SERVICE_FORCE * TORQUE_RADIUS
INCIDENTAL_FORCE = 100.0
GATE = 0.10
FIXED_ALIGNMENT = 0.09


def rail_mm(force_n: float) -> float:
    inertia = RAIL**4 / 12.0
    return force_n * L**3 / (48.0 * E_RAIL * inertia)


def shaft_mm() -> float:
    polar = pi * SHAFT**4 / 32.0
    return SERVICE_TORQUE * ROTOR_COUNT * L / (polar * G_SHAFT) * OUTPUT_LEVER


def omitted_mm(force_n: float, stiffness_n_per_mm: dict[str, float]) -> float:
    if any(value <= 0.0 for value in stiffness_n_per_mm.values()):
        raise ValueError("stiffness values must be positive")
    return force_n * sum(1.0 / value for value in stiffness_n_per_mm.values())


def main() -> None:
    zero_compliance = rail_mm(INCIDENTAL_FORCE) + shaft_mm()
    allowance = GATE - zero_compliance
    service_baseline = rail_mm(SERVICE_FORCE) + shaft_mm()
    illustrative = {name: 10_000.0 for name in
                    ("seam", "support", "bearing", "rotor_stop")}

    print("E-011 DES-005/Q-011 compliance bound (calculation only)")
    print(f"rail_100N_mm={rail_mm(INCIDENTAL_FORCE):.5f}")
    print(f"shaft_service_torque_mm={shaft_mm():.5f}")
    print(f"zero_compliance_baseline_100N_mm={zero_compliance:.5f}")
    print(f"allowance_to_gate_100N_mm={allowance:.5f}")
    print(f"service_baseline_mm={service_baseline:.5f}")
    print(f"service_with_fixed_0.09_stack_mm={service_baseline + FIXED_ALIGNMENT:.5f}")
    print(f"illustrative_10k_each_omitted_mm={omitted_mm(INCIDENTAL_FORCE, illustrative):.5f}")

    assert zero_compliance > GATE
    assert allowance < 0.0
    assert service_baseline + FIXED_ALIGNMENT > GATE
    assert omitted_mm(INCIDENTAL_FORCE, illustrative) == 0.04


if __name__ == "__main__":
    main()
