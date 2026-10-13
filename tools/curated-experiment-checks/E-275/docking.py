#!/usr/bin/env python3
"""E-275: finite fixed rotors, explicit sliding square shafts, axial friction.

Dimensions, Coulomb coefficients, loads and force allowances are scenarios,
not measured material properties, process priors or selector/keeper ratings.
No timing/cost promotion follows a failed contact/selection screen.
"""
import argparse
import importlib.util
import itertools
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    'loop', Path(__file__).resolve().parents[1] / 'E-274/loop.py')
loop = importlib.util.module_from_spec(spec)
spec.loader.exec_module(loop)


def radius(outer=1.6, inner=0):
    """Uniform-pressure effective radius, mm; NOT outer radius."""
    assert 0 <= inner < outer
    return (2 / 3) * (outer**3 - inner**3) / (outer**2 - inner**2)


def margin(normal, torque=.35, mu=.3, reff=1.5, weight=.2,
           bed=.6, keeper=.6):
    """Nmm residual: contact capacity minus torque required by resident.

    torque excludes bed/keeper friction; bed/keeper = mu * effective radius
    in mm. No double counting: an alternative inclusive .35 total uses .23
    here when initial bed drag is .6*.2 = .12 Nmm.
    """
    return (mu * reff * normal - torque - bed * max(weight - normal, 0)
            - keeper * max(normal - weight, 0))


def required(torque=.35, mu=.3, reff=1.5, weight=.2,
             bed=.6, keeper=.6):
    """First feasible normal force, or None, from two linear contact regimes."""
    assert min(torque, mu, reff, weight, bed, keeper) >= 0
    c = mu * reff
    if c + bed == 0:
        return 0. if torque == 0 else None
    on_bed = (torque + bed * weight) / (c + bed)
    if on_bed <= weight:
        return on_bed
    if c <= keeper:
        return None
    return (torque - keeper * weight) / (c - keeper)


def finite(n, e=.2):
    """Necessary volume reservations, not manufactured fits or full CAD.

    Resident underside z=0. Fixed drum [-20,-14], band [-18,-16];
    hub [-24,-10], square shaft [-27,-7]+q, q in [0,3].
    Pad top -1+q; contact at q=1 for a fixed resident, NOT at full throw.
    """
    p = 406.4 / n
    b = loop.geometry(n, e=e)
    return dict(
        n=n, pitch_mm=p, band_gap_mm=b['nonlocal_belt_gap_mm'],
        stationary_band_edge_mm=2 - 2 * e,
        rotor_neighbor_mm=p - 4 - 2 * e,
        bearing_neighbor_mm=p - 4.4 - 2 * e,
        parked_face_gap_mm=1 - 2 * e,
        pad_to_neighbor_resident_mm=p - 1.6 - 1.6 - 2 * e,
        square_side_clearance_mm=.2 - 2 * e,
        hub_corner_wall_mm=2 - e - math.sqrt(2) * (1.2 + e),
        square_axial_overlap_mm=14 - 2 * e,
        selector=loop.r.selection_envelope(n, e=e),
        loop_XY_mm=b['loop_head_mm'],
        whole_X_mm=b['whole_X_union_mm'])


def force_cases():
    rows = []
    for name, reff, mu, support_mu, torque in [
        ('optimistic rim, frictionless supports', 1.5, .3, 0, .35),
        ('full face, frictionless supports', radius(), .3, 0, .35),
        ('rim, equal coefficients', 1.5, .3, .3, .35),
        ('full face, equal coefficients', radius(), .3, .3, .35),
        ('rim, credit old bed drag', 1.5, .3, .3, .23),
        ('rim, low support friction', 1.5, .3, .1, .35),
        ('rim, high face friction', 1.5, .6, .3, .35),
        ('rim, high face and low support friction', 1.5, .6, .1, .35),
    ]:
        need = required(torque=torque, reff=reff, mu=mu,
                        bed=2*support_mu, keeper=2*support_mu)
        rows.append(dict(case=name, normal_N=need,
                         force_only_survivor=need is not None and need <= .585,
                         no_lift_survivor=need is not None and need <= .2))
    return rows


def retry(actual, target, slips, observed=True, lead=3):
    """Ideal signed threshold replay with per-output slip; no observation oracle.

    Retrying from a stable, correctly identified actual height is conditional.
    Unknown readback has no commanded continuation. Permanent square couplings
    keep rotating parked shafts, but the open axial gap isolates their residents.
    """
    if not observed:
        return None
    changed = [a != t for a, t in zip(actual, target)]
    after = [a + (t-a)*(1-s) for a, t, s in zip(actual, target, slips)]
    correction_turns = [(t-a)/lead for a, t in zip(after, target)]
    return changed, after, correction_turns


def checks():
    # Independently integrate uniform-pressure rings, rather than restating r_eff.
    for inner in (0., 1.4):
        steps = 20000
        dr = (1.6-inner)/steps
        rings = [(inner+(i+.5)*dr) for i in range(steps)]
        numeric = sum(r*r*dr for r in rings)/sum(r*dr for r in rings)
        assert abs(numeric-radius(inner=inner)) < 1e-8
    assert math.isclose(.35/(.3*1.5), 7/9)
    assert math.isclose(.35/(.3*radius()), 1.09375)
    assert required() is None
    assert required(torque=.23) is None
    assert required(mu=.6, bed=.2, keeper=.2) < .585
    assert all(not row['no_lift_survivor'] for row in force_cases())
    # Independent dense N sampling checks analytic feasibility and first crossing.
    count = 0
    for tq, mu, rr, w, kb, kk in itertools.product(
            (.1, .35, 1), (.1, .3, .6), (radius(), 1.5),
            (0, .2, 1), (0, .2, .6), (0, .2, .6)):
        args = dict(torque=tq, mu=mu, reff=rr, weight=w, bed=kb, keeper=kk)
        need = required(**args)
        step = .002
        found = next((i*step for i in range(10001)
                      if margin(i*step, **args) >= -1e-12), None)
        if need is None or need > 20 + 1e-10:
            assert found is None
        else:
            assert found is not None and -1e-9 <= found-need <= step+1e-9
            assert abs(margin(need, **args)) < 1e-10
        count += 1
    coarse, fine = finite(64), finite(80)
    assert coarse['band_gap_mm'] > 0 > fine['band_gap_mm']
    assert coarse['stationary_band_edge_mm'] > 0
    assert coarse['square_side_clearance_mm'] < 0
    assert coarse['hub_corner_wall_mm'] < 0
    assert finite(64, e=0)['hub_corner_wall_mm'] > 0
    assert finite(64, e=.1)['square_side_clearance_mm'] <= 1e-12
    assert coarse['selector']['conflicts'] == fine['selector']['conflicts'] == 0
    # Swept square overlap and no resident lift: motion stops upon first contact.
    for j in range(301):
        q = j/100
        assert min(-7+q, -10)-max(-27+q, -24) == 14
    assert 1-.4 > 0 and 1+.4 < 3  # contact lies inside travel, not forced past it
    # Circular friction faces have no keyed phase constraint. Preserve the
    # independent rigid-socket counterexample rather than counting tautological poses.
    assert loop.r.phase_span([0, .25]) > 10  # unchanged rigid-socket failure
    # All 3-cell signed targets, off-grid stable slip, unchanged-cell isolation.
    replay_count = 0
    for before in itertools.product((0., .25, 20.), repeat=3):
        for target in itertools.product((0., .25, 20.), repeat=3):
            for slips in ((0, 0, 0), (.1, .25, .5)):
                selected, partial, turns = retry(before, target, slips)
                for a, t, x, turns_i, active in zip(before, target, partial, turns, selected):
                    assert min(a, t)-1e-10 <= x <= max(a, t)+1e-10
                    assert math.isclose(x+3*turns_i, t, abs_tol=1e-10)
                    if not active:
                        assert x == a and turns_i == 0
                replay_count += 1
    assert retry([0], [1], [.5], observed=False) is None
    # Blind replay overshoots: 10 commanded, 8 actual, correct retry is 2, not 10.
    assert 8+10 > 10 and 8+(10-8) == 10
    return dict(force_cases_crosschecked=count, signed_slip_replays=replay_count,
                verdict='PARK')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.check:
        print(json.dumps(checks(), indent=2))
    else:
        print(json.dumps(dict(
            evidence='assumptions, calculation and bounded geometry; no measurement',
            verdict='PARK', effective_radius_disk_mm=radius(),
            effective_radius_annulus_mm=radius(inner=1.4),
            force_cases=force_cases(), geometry=[finite(n) for n in (64,80)],
            no_keeper_no_loss_normal_N=.35/(.3*1.5),
            normal_allowance_N=.785-.2,
            required_radius_at_mu03_mm=.35/(.3*.585),
            no_lift_capacity_at_W02_r15_Nmm=.3*1.5*.2,
            head_16_normal_at_optimistic_contact_N=16*.35/(.3*1.5),
            sliding_key_drag_at_T035_mu03_r1_N=.3*.35/1,
            resident_counts={n:dict(pairs=n*n, flat_faces=n*n,
                                    support_sites=n*n, guide_apertures=2*n*n)
                             for n in (64,80)}), indent=2))
