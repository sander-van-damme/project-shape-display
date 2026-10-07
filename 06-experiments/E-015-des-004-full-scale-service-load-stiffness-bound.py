#!/usr/bin/env python3
"""Q-011 DES-004 frame/shaft bound; calculation only, no physical validation."""
from math import pi

L = 406.4
P = 100.0
B = H = 25.0
E = 69_000.0
G = 79_000.0
N = 80
F_T = 2.0
R = 2.0
LEVER = 10.0
GATE = 0.10


def frame_deflection() -> float:
    inertia = B * H**3 / 12.0
    return P * L**3 / (48.0 * E * inertia)


def shaft_motion(diameter: float) -> float:
    torque = N * F_T * R
    polar = pi * diameter**4 / 32.0
    return torque * L / (polar * G) * LEVER


def main() -> None:
    frame = frame_deflection()
    print("Q-011 DES-004 full-scale bound (calculation only)")
    print(f"frame deflection: {frame:.6f} mm; margin: {GATE - frame:.6f} mm")
    for diameter in (1.0, 4.0, 6.0, 8.0):
        print(f"shaft d={diameter:.1f} mm: end motion={shaft_motion(diameter):.6f} mm")
    assert abs(frame - 0.06225754355385507) < 1e-12
    assert abs(shaft_motion(1.0) - 167.678233938) < 1e-6
    assert shaft_motion(8.0) < GATE
    assert frame < GATE


if __name__ == "__main__":
    main()
