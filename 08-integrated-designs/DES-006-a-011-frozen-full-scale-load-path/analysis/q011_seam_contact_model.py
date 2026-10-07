#!/usr/bin/env python3
"""Parameterised Q-011 seam/contact compliance screen.

This is a conservative one-port model, not FEA.  Each omitted interface is
represented by an effective translational stiffness in N/mm.  The terms are
in series at the cell datum, so their displacements add under the declared
force.  This intentionally bounds *sensitivity*, not actual joint stiffness:
no preload, contact area, housing geometry, or material data for these joints
is frozen in DES-006.
"""
from math import pi

L = 406.4
E_RAIL = 69_000.0
G_SHAFT = 79_000.0
RAIL = 25.0
SHAFT = 8.0
LEVER = 10.0
SERVICE_FORCE = 3.27
INCIDENTAL_FORCE = 100.0
SERVICE_TORQUE = SERVICE_FORCE * 2.0
GATE = 0.10


def rail_mm(load_n: float) -> float:
    inertia = RAIL**4 / 12.0
    return load_n * L**3 / (48.0 * E_RAIL * inertia)


def shaft_mm(torque_per_rotor_nmm: float, count: int = 80) -> float:
    polar = pi * SHAFT**4 / 32.0
    return torque_per_rotor_nmm * count * L / (polar * G_SHAFT) * LEVER


def spring_mm(load_n: float, stiffness_n_per_mm: float) -> float:
    if stiffness_n_per_mm <= 0.0:
        raise ValueError("effective stiffness must be positive")
    return load_n / stiffness_n_per_mm


def missing_mm(load_n: float, stiffness: dict[str, float]) -> float:
    return sum(spring_mm(load_n, value) for value in stiffness.values())


def equivalent_stiffness(stiffness: dict[str, float]) -> float:
    return 1.0 / sum(1.0 / value for value in stiffness.values())


def report_case(name: str, load_n: float, stiffness: dict[str, float], fixed_stack: float) -> None:
    rail = rail_mm(load_n)
    shaft = shaft_mm(SERVICE_TORQUE)
    missing = missing_mm(load_n, stiffness)
    total = rail + shaft + fixed_stack + missing
    print(f"{name}: rail={rail:.5f} shaft={shaft:.5f} fixed={fixed_stack:.5f} "
          f"missing={missing:.5f} total={total:.5f} pass={total < GATE}")
    print(f"  equivalent_missing_stiffness_n_per_mm={equivalent_stiffness(stiffness):.3f}")


def main() -> None:
    baseline_structural = rail_mm(INCIDENTAL_FORCE) + shaft_mm(SERVICE_TORQUE)
    allowable_missing_at_100n = GATE - baseline_structural
    allowable_stiffness_at_100n = (
        INCIDENTAL_FORCE / allowable_missing_at_100n
        if allowable_missing_at_100n > 0.0 else None
    )
    service_structural = rail_mm(SERVICE_FORCE) + shaft_mm(SERVICE_TORQUE)
    allowable_service_no_stack = GATE - service_structural
    print("DES-006/A-011 Q-011 seam/contact model (calculation only)")
    print(f"baseline_100N_structural_mm={baseline_structural:.5f}")
    print(f"allowable_missing_at_100N_mm={allowable_missing_at_100n:.5f}")
    print(f"allowable_equivalent_stiffness_at_100N_n_per_mm={allowable_stiffness_at_100n}")
    print(f"service_structural_mm={service_structural:.5f}")
    print(f"allowable_service_missing_without_fixed_stack_mm={allowable_service_no_stack:.5f}")

    # Illustrative sensitivity points only.  They are not sourced joint values.
    terms = {"seam": 10_000.0, "support": 10_000.0,
             "bearing": 10_000.0, "rotor_stop": 10_000.0}
    report_case("100N_optimistic_10k_each_no_fixed_stack", INCIDENTAL_FORCE, terms, 0.0)
    report_case("100N_very_stiff_100k_each_no_fixed_stack", INCIDENTAL_FORCE,
                {key: 100_000.0 for key in terms}, 0.0)
    report_case("service_10k_each_plus_0.09_stack", SERVICE_FORCE, terms, 0.09)

    assert baseline_structural > GATE
    assert allowable_missing_at_100n < 0.0
    assert report_case is not None


if __name__ == "__main__":
    main()
