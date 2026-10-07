#!/usr/bin/env python3
"""Q-011 analytical frame/shaft bound; no FEA or physical validation."""

from math import pi

L = 406.4
FRAME_LOAD = 100.0
FRAME_B = FRAME_H = 25.0
E_AL = 69_000.0
SHAFT_G = 79_000.0
ROTORS = 80
TANGENTIAL_FORCE = 2.0
ROTOR_RADIUS = 2.0
LEVER = 10.0
MOTION_GATE = 0.10


def frame_deflection(load: float, length: float, b: float, h: float, modulus: float) -> float:
    inertia = b * h**3 / 12.0
    return load * length**3 / (48.0 * modulus * inertia)


def shaft_tip_motion(diameter: float) -> float:
    torque = ROTORS * TANGENTIAL_FORCE * ROTOR_RADIUS
    polar = pi * diameter**4 / 32.0
    twist = torque * L / (polar * SHAFT_G)
    return twist * LEVER


def main() -> None:
    frame = frame_deflection(FRAME_LOAD, L, FRAME_B, FRAME_H, E_AL)
    print("Q-011 DES-004 full-scale bound (calculation only)")
    print(f"frame: L={L:.1f} mm, P={FRAME_LOAD:.1f} N, 25x25 mm, E={E_AL:.0f} N/mm^2")
    print(f"  midspan deflection={frame:.6f} mm; margin={MOTION_GATE-frame:.6f} mm")
    print("shaft: 80 rotors x 2.0 N x 2.0 mm, steel G=79000 N/mm^2")
    for d in (1.0, 4.0, 6.0, 8.0):
        motion = shaft_tip_motion(d)
        print(f"  d={d:.1f} mm: end motion at 10 mm lever={motion:.6f} mm")
    assert abs(frame - 0.06225754355385507) < 1e-12
    assert abs(shaft_tip_motion(1.0) - 167.678233938) < 1e-6
    assert shaft_tip_motion(8.0) < MOTION_GATE
    assert frame < MOTION_GATE


if __name__ == "__main__":
    main()
