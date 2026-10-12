#!/usr/bin/env python3
"""E-256: deterministic friction/drive bounds, not a PLA process model.

Torque is N mm, length mm unless explicitly SI. No generated files or priors.
Fit-induced drag is an independent measured-equivalent parameter: this code
does not map CAD clearance to friction, nor predict a moving-loss trajectory.
"""
import itertools
import json
import math

import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "screw_screen", Path(__file__).resolve().parent.parent / "E-255/screen.py")
screen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(screen)

G = 9.80665
LEAD = 3.0


def coefficients(mu, diameter=2.3, collar=0):
    """Quasistatic raise/lower torque per axial N. Collar is mu_c*r_c (mm)."""
    radius = diameter / 2
    slope = LEAD / (math.pi * diameter)
    effective = mu / math.cos(math.radians(15))
    assert effective * slope < 1
    return (radius * (slope + effective) / (1 - slope * effective) + collar,
            radius * (effective - slope) / (1 + slope * effective) + collar)


def torque(mass_g, mu, drag, accel=0, inertia=0, guide_force=0, collar=0):
    """Raising torque with constant upward acceleration and rotor inertia.

    accel: rev/s^2. inertia: all rotating inertia reflected to screw, kg m^2.
    Axial thread force includes translating inertia; do not count it twice.
    guide_force: an assumed resisting axial N, NOT a measured guide load.
    """
    mass = mass_g / 1000
    axial_force = mass * (G + LEAD / 1000 * accel) + guide_force
    up, _ = coefficients(mu, collar=collar)
    return axial_force * up + drag + inertia * (2 * math.pi * accel) * 1000


def thresholds(mass_g, mu_static, mu_running, ratio, collar=0):
    """Required static drag D, with running drag ratio*D.

    First bound holds at rest; second gives positive quasistatic lowering
    resistance. Equality is neutral; neither bound certifies dynamic arrest.
    """
    weight = mass_g / 1000 * G
    static = max(0, -weight * coefficients(mu_static, collar=collar)[1])
    running = max(0, -weight * coefficients(mu_running, collar=collar)[1] / ratio)
    return static, running


def rpm_boundary(benchmark, banks, accel=1000, proof=.02):
    """Bisection of sample max =30 s; strictly faster is required, no margin."""
    def worst(rpm):
        return max(screen.schedule(d, banks, rpm=rpm, accel=accel,
                                   proof=proof)['seconds'] for d in benchmark)
    max_turns = max(abs(x) / LEAD for d in benchmark for row in d for x in row)
    # At this speed ceiling every move is triangular; higher RPM cannot help.
    low, high = 1., 60 * math.sqrt(max_turns * accel)
    if worst(high) >= 30:
        return None
    for _ in range(42):
        middle = (low + high) / 2
        if worst(middle) >= 30:
            low = middle
        else:
            high = middle
    assert worst(low) >= 30 and worst(high) < 30
    return high


def checks():
    # Zero friction conserves screw work and permits backdrive.
    up, down = coefficients(0)
    assert math.isclose(up, LEAD / (2 * math.pi))
    assert math.isclose(down, -up)
    critical_mu = LEAD / (math.pi * 2.3) * math.cos(math.radians(15))
    assert abs(coefficients(critical_mu)[1]) < 1e-15
    # At zero load only imposed drag and rotating inertia remain.
    assert torque(0, .3, .05) == .05
    assert math.isclose(torque(0, .3, .05, 1000, 1e-8), .05 + .02 * math.pi)
    # Frictionless acceleration agrees with reflected translational inertia.
    added = torque(20, 0, 0, 1000) - torque(20, 0, 0)
    reflected = .02 * (.003 / (2 * math.pi))**2
    assert math.isclose(added, reflected * (2 * math.pi * 1000) * 1000)
    # Static hold is not the moving-resistance test, even at the same load.
    static, running = thresholds(20, .3, .1, .5)
    assert static < .05 < running
    assert thresholds(20, .3, .1, .5, collar=.2)[0] == 0
    assert thresholds(100, .3, .1, .5)[0] > static
    # Independent triangular/trapezoidal motion checks.
    assert math.isclose(screen.spin(1, 3000, 200), 2 * math.sqrt(1/200))
    assert math.isclose(screen.spin(40/3, 2000, 1000), .4 + 1/30)
    return 'frictionless work, self-lock boundary, inertia, load and hold witnesses'


def main():
    verified = checks()
    data = screen.cases()
    benchmark = [d for k, d in data.items() if '_to_' in k or k.startswith('initial_')]
    boundaries = {f'B{b}_a{a}_proof{p}': rpm_boundary(benchmark, b, a, p)
                  for b, a, p in ((2, 1000, .02), (2, 500, .02),
                                  (2, 200, .02), (2, 1000, .1), (3, 1000, .02))}
    matrix = []
    for mass, mu, drag in itertools.product((5, 20, 100), (.1, .3, .5), (0, .05, .2)):
        steady = torque(mass, mu, drag)
        peak = torque(mass, mu, drag, 1000, 1e-8)
        matrix.append(dict(total_moving_mass_g=mass, mu=mu, running_drag_Nmm=drag,
                           steady_Nmm=steady, accelerating_Nmm=peak,
                           steady_output_W_160=160 * steady / 1000 * 100 * math.pi))
    # Necessary average net braking torque to dissipate initial kinetic energy
    # in selected travel distances. Net excludes gravity; actual resisting torque
    # must additionally cover W*lead/(2*pi). Not a predicted stopping distance.
    braking = []
    for inertia, distance in itertools.product((1e-9, 1e-8, 1e-7), (.1, 1)):
        reflected = .02 * (.003 / (2 * math.pi))**2
        energy = .5 * (inertia + reflected) * (100 * math.pi)**2
        angle = distance / LEAD * 2 * math.pi
        braking.append(dict(rotating_inertia_kgm2=inertia, allowed_distance_mm=distance,
                            initial_energy_J=energy, average_net_braking_Nmm=energy/angle*1000))
    print(json.dumps(dict(evidence='Labelled scenarios; no process or motor qualification',
        checks=verified, rpm_at_30_seconds=boundaries, coefficients={str(mu): coefficients(mu)
        for mu in (.1, .3, .5)}, drag_static_and_running_thresholds_Nmm={
            str(m): thresholds(m, .3, .1, .5) for m in (5, 20, 100)},
        same_with_collar_02=thresholds(20, .3, .1, .5, collar=.2),
        torque_cases=matrix, braking_energy_requirements=braking,
        drag_005_dense_40mm_J=6400 * .05 / 1000 * 40/LEAD * 2*math.pi,
        rotor_acceleration_Nmm={str(j): j*2*math.pi*1000*1000 for j in (1e-9, 1e-8, 1e-7)}),
        indent=2))


if __name__ == '__main__':
    main()
