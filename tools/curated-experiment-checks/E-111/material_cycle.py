#!/usr/bin/env python3
"""Closed-cycle inventory/flow screen; mm, N, MPa unless units named.

Deterministic scenarios, NOT material data or finite membrane/contact analysis.
No output files. --all prints the enumerated short-stroke population.
"""
import argparse
import json
from itertools import product
from math import ceil, isclose, pi, radians, sqrt, tan, tanh


def overlap(a, b, c, d):
    return max(0., min(b, d)-max(a, c))


def keyed_length(length, phase, width=.4, period=1.):
    return sum(overlap(0, length, i*period+phase, i*period+phase+width)
               for i in range(-2, ceil(length/period)+2))


def bath(stroke=40., collar=5.2, radius=1.5, gap=.1, depth=.2,
         end_margin=.2, phase=0.):
    # Moving keyed interval: [margin+q, margin+q+collar+stroke].
    # q spans [0,stroke]; fixed smooth-land seals at 0 and chamber_length.
    track = collar+stroke
    length = collar+2*stroke+2*end_margin
    annulus = pi*((radius+gap)**2-radius**2)*length
    tail = pi*(radius**2-(radius-depth)**2)*keyed_length(track, phase)
    cup = pi*((radius+gap+depth)**2-(radius+gap)**2)*keyed_length(collar, 0)
    return dict(chamber_length_mm=length, keyed_track_mm=track,
                minimum_smooth_land_each_mm=stroke+end_margin,
                liquid_mm3=annulus+tail+cup,
                board_W_30s_at_0_5_J_mm3=6400*(annulus+tail+cup)*.5/30)


def bath_quadrature(q, phase, n):
    """Independent spatial integration including finite translated track."""
    b = bath(phase=phase)
    length, track = b['chamber_length_mm'], b['keyed_track_mm']
    total = 0.
    for i in range(n):
        z = (i+.5)*length/n
        u = z-(.2+q)
        inner = 1.5-(.2 if 0 <= u <= track and (u-phase) % 1 < .4 else 0)
        # Cup's local fixed 5.2-mm keyed section; central placement.
        v = z-40.2
        outer = 1.6+(.2 if 0 <= v <= 5.2 and v % 1 < .4 else 0)
        total += pi*(outer**2-inner**2)*length/n
    return total


def slit_pressure(mu_Pa_s, flow_mm3_s, h_mm, w_mm=.8, length_mm=2.):
    """Rectangular duct Stokes solution, 100 positive odd modes.

    Infinite parallel-plate conductance is an independent lower pressure bound.
    Developing flow, bends, wetting and non-Newtonian effects are excluded.
    """
    if h_mm <= 0:
        return None
    h, w, length = h_mm/1000, w_mm/1000, length_mm/1000
    assert w >= h
    series = sum(tanh(n*pi*w/(2*h))/n**5 for n in range(1, 200, 2))
    factor = 1-192*h/(pi**5*w)*series
    infinite = 12*mu_Pa_s*length*(flow_mm3_s*1e-9)/(w*h**3)
    return dict(pressure_Pa=infinite/factor, slit_lower_Pa=infinite,
                sidewall_factor=factor)


def strut(angle, stress, error, dead_fraction, duct_height=.2):
    # Frictionless ramp: lateral structural load = vertical load*tan(angle).
    # error coherently reduces cap radius, increases withdrawal, closes duct.
    force = 10*tan(radians(angle))
    nominal_r = sqrt(force/(pi*stress)) if force else 0.
    radius = nominal_r+error  # resize cap to preserve assumed stress cut
    area = pi*radius**2
    stroke, end_gap = .3+.15+error, .2
    duct = .8*duct_height*2
    volume = (area*(stroke+2*end_gap)+duct)*(1+dead_fraction)
    # Two opposed variable-length chambers; at x their core lengths are
    # end_gap+stroke-x and end_gap+x. Closed material stays inside capsule.
    flow = area*stroke/.5  # assumed 0.5-s liquid transfer, not update schedule
    failures = []
    diameter = 2*radius+.6  # only outer radial allocation, not a packed machine
    if diameter > 5.08: failures.append('radial_allocation_exceeds_pitch')
    effective_h = duct_height-error
    if effective_h <= 0: failures.append('duct_closed_by_coherent_error')
    return dict(angle_deg=angle, stress_MPa=stress, error_mm=error,
                dead_fraction=dead_fraction, lateral_load_N=force,
                cap_radius_mm=radius, radial_allocation_mm=diameter,
                stroke_mm=stroke, liquid_mm3=volume,
                transferred_mm3=area*stroke, flow_mm3_s=flow,
                board_W_30s_at_0_5_J_mm3=6400*volume*.5/30,
                flow_force_N_at_mu_0_002_0_02_1=[
                    None if effective_h <= 0 else
                    slit_pressure(mu, flow, effective_h)['pressure_Pa']*area*1e-6
                    for mu in (.002, .02, 1.)], failures=failures)


def mismatch(radius=1., stroke=.5, bias=0., differential=.05):
    # Shared bias affects both chambers, differential mismatch opposes them.
    a = pi*(radius+bias+differential)**2
    b = pi*(radius+bias-differential)**2
    return (a-b)*stroke


def verify():
    # Exact translated finite groove inventory; no motion-induced liquid loss.
    exact = bath(phase=.173)['liquid_mm3']
    holdouts = ((7.317, .129), (17.319, .173), (39.923, .381))
    errors = [max(abs(bath_quadrature(q, p, n)-bath(phase=p)['liquid_mm3'])
                  for q, p in holdouts) for n in (10000, 100000, 1000000)]
    assert errors[-1] < .003 and errors[-1] < errors[0]
    for q in (0, 7.31, 40):
        assert abs(bath_quadrature(q, .173, 100000)-exact) < .03
        # Keyed section never intersects the fixed seal planes.
        assert .2+q > 0 and .2+q+45.2 < bath()['chamber_length_mm']
    r, s, h = 1.3, .5, .2
    a = pi*r*r
    for i in range(101):
        x = i*s/100
        v1, v2 = a*(h+s-x), a*(h+x)
        assert isclose(v1+v2, a*(2*h+s))
        # If reservoir cannot move, incompressible liquid prohibits any stroke.
        displaced = a*x
        assert isclose(displaced, v2-a*h, abs_tol=1e-14)
    assert mismatch(differential=0) == 0
    assert isclose(mismatch(), 4*pi*1*.05*.5)
    assert isclose(mismatch(bias=.1), 4*pi*1.1*.05*.5)
    p = slit_pressure(.02, 2, .1)
    assert p['pressure_Pa'] > p['slit_lower_Pa']
    assert isclose(slit_pressure(.04, 2, .1)['pressure_Pa'], 2*p['pressure_Pa'])
    assert isclose(slit_pressure(.02, 4, .1)['pressure_Pa'], 2*p['pressure_Pa'])
    assert slit_pressure(.02, 2, 0) is None
    assert strut(0, 1, 0, 0)['lateral_load_N'] == 0  # command-latch limit
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', action='store_true')
    args = parser.parse_args()
    errors = verify()
    rows = [strut(*p) for p in product((15, 30, 45), (.25, 1, 5),
                                     (0, .05, .15), (0, .5, 1))]
    example = strut(30, 1, .05, .5)
    mismatch_volume = mismatch(example['cap_radius_mm'], example['stroke_mm'])
    expansion = .05*example['liquid_mm3']  # explicit +/-5% volume scenario
    extra_travel = (mismatch_volume+expansion)/(pi*(example['cap_radius_mm']-.05)**2)
    examples = [strut(30, sigma, e, .5) for sigma, e in
                product((.25, 1, 5), (0, .05, .15))]
    print(json.dumps(dict(
        evidence='bounded inventory/kinematic/laminar-flow calculation; no hardware pass',
        cases=len(rows), rejected_radial=sum('radial_allocation_exceeds_pitch' in r['failures'] for r in rows),
        bath=bath(), bath_integration_errors_mm3=errors,
        mismatch_example_mm3=mismatch(),
        middle_case_extra_reservoir_travel_mm_at_5pct=extra_travel,
        examples=examples, rows=rows if args.all else None), indent=2))


if __name__ == '__main__':
    main()
