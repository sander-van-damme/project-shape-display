#!/usr/bin/env python3
"""Independent B-workstream screening calculations, not physical qualification.

Dimensions are mm, forces N, Young's modulus N/mm². Timing is a lower-bound
screen for the specified complete row transaction. No measured actuator speed
or polymer properties are asserted.
"""
import json
import math
from pathlib import Path


def trap(distance, speed, acceleration):
    distance = abs(distance)
    critical = speed * speed / acceleration
    if distance <= critical:
        return 2 * math.sqrt(distance / acceleration)
    return distance / speed + speed / acceleration


def screen():
    E, width, thick, length, release = 2000., 3.8, .6, 20., .8
    inertia = width * thick**3 / 12
    mechanical = {
        'assumed_E_MPa': E,
        'leaf_dimensions_mm': [width, thick, length],
        'transverse_release_mm': release,
        'leaf_force_N': 3*E*inertia*release/length**3,
        'leaf_outer_fiber_stress_MPa': 1.5*E*thick*release/length**2,
        'unsupported_vertical_cantilever_euler_N': math.pi**2*E*inertia/(4*length**2),
        'tooth_load_N': .5,
        'tooth_bearing_MPa_3p8_by_0p6': .5/(3.8*.6),
        'tooth_root_stress_MPa_1mm_thick_0p6_projection': 6*.5*.6/(3.8*1.**2),
        'row_lift_load_N_at_64_times_0p5': 64*.5,
        'row_motor_torque_Nm_at_8mm_radius_80pct_efficiency': 64*.5*.008/.8,
        'common_rack_tooth_span_mm_for_40mm_terrain_and_40mm_shuttle': 40+40+6,
    }
    timing=[]
    for banks in [1, 2, 4, 8]:
        for speed in [40, 80, 120]:
            # Full up sweep and full down sweep; ends where it starts. Both
            # signed cohorts engage at the two sweep endpoints. Each lane has
            # an independent finite-speed release, a qualification assumption.
            row = 2*trap(40, speed, 1000) + 2*.12 + trap(6.35, 100, 1000) + .05
            timing.append({'banks':banks, 'selectors':64*banks,
                           'speed_mm_s':speed, 'row_seconds':row,
                           'full_64_row_seconds':math.ceil(64/banks)*row,
                           'one_mm_latch_window_ms':1000/speed,
                           '0p8_mm_compliance_ms':800/speed})
    return {'classification':'computational screen with unqualified assumptions',
            'mechanics':mechanical, 'continuous_release_two_sweep_timing':timing}


if __name__ == '__main__':
    result=screen()
    out=Path(__file__).with_suffix('.json')
    out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
