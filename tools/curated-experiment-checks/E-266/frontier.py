#!/usr/bin/env python3
"""Bounded axial bank/concurrency comparison. Scenarios, not safe speeds or BOM.

Reuse E-259's physical scenes, electrical-slot scheduler and E-255 overhead.
No new maps, rotor or selector detail. JSON stdout is reproducible/disposable.
"""
import argparse
import importlib.util
import itertools
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location('lead', Path(__file__).resolve().parents[1]
                                             / 'E-259/lead_sensitivity.py')
l = importlib.util.module_from_spec(spec)
spec.loader.exec_module(l)
a = l.a


def bulk(needed, tiers):
    return min(((max(needed, q), p) for q, p in tiers), key=lambda v: v[0]*v[1])


def cost(n, banks):
    outputs = n*banks
    mq, mp = bulk(outputs, ((1, 1.95), (10, 1.76), (100, 1.56)))
    dq, dp = bulk(outputs//2, ((1, 5.95), (10, 5.36), (100, 4.76)))
    reserve = a.r.costs(banks, n=n)['reserve']
    total = reserve+mq*mp+dq*dp
    return dict(outputs=outputs, motor_quantity=mq, driver_boards=dq,
                spare_motors=mq-outputs, spare_boards=dq-outputs//2,
                reserve_USD=reserve, subset_plus_reserve_USD=total,
                remaining_per_output_USD={b: (b-total)/outputs for b in (500, 1000, 1500)},
                installed_motor_kg=.0175*outputs,
                illustrative_one_minute_per_channel_h=outputs/60)


def case(n, banks, k, lead, rpm, stroke, accel=1000, release=0):
    neutral = stroke-20
    deltas = {name: d for name, d in a.workloads(n).items()
              if stroke == 50 or 'deep:' not in name}
    kw = dict(banks=banks, lead=lead, rpm=rpm, accel=accel, release=release)
    schedules = {name: a.schedule(d, k, **kw) for name, d in deltas.items()}
    worst = max(schedules, key=lambda name: schedules[name]['feasible_s'])
    prep = a.schedule(a.c.v.s.flat(n, neutral), k, **kw)['feasible_s']
    dense = a.schedule(a.c.v.s.flat(n, stroke), k, **kw)['feasible_s']
    initial = max(v['feasible_s'] for name, v in schedules.items() if name.startswith('ground>'))
    # Illustrative sequence, not observed play frequency. Returns to flat neutral
    # are not inserted between maps. Every command pays its own retry allowance.
    sequence = ['ground>shallow:road', 'shallow:road>shallow:ruins',
                'shallow:ruins>shallow:ravine']
    if stroke == 50:
        sequence += ['shallow:ravine>deep:ravine']
    return dict(n=n, banks=banks, k=k, lead_mm=lead, rpm=rpm, stroke_mm=stroke,
                neutral_mm=neutral, accel_rev_s2=accel, release_s=release,
                commands=len(deltas), worst=worst,
                scene_s=schedules[worst]['feasible_s'],
                scene_lower_s=max(v['lower_s'] for v in schedules.values()),
                prep_s=prep, dense_s=dense, cold_first_s=prep+initial,
                sequence=sequence, sequence_wait_s=sum(schedules[name]['feasible_s'] for name in sequence),
                powered_outputs=banks*k, rated_load_motor_A=.25*banks*k,
                stall_motor_A=.5*banks*k, **cost(n, banks))


def quotas(n, banks):
    # Include nearly equal <=64-token allocations; 3 banks leave one token idle.
    return sorted({16, 24, 32, n, min(n, 64//banks)})


def dominates(x, y):
    keys = ('subset_plus_reserve_USD', 'outputs', 'powered_outputs',
            'scene_s', 'prep_s', 'dense_s')
    return all(x[k] <= y[k]+1e-9 for k in keys) and any(x[k] < y[k]-1e-9 for k in keys)


def sweep():
    rows = []
    for n, lead, rpm, stroke in itertools.product((64, 80), (2, 3), (400, 600, 850), (40, 50)):
        group = [case(n, b, k, lead, rpm, stroke) for b in (1, 2, 3, 4) for k in quotas(n, b)]
        # Do not let unqualified faster RPM, a different physical depth or pitch
        # dominate another scenario. Neither is a free interchangeable resource.
        for row in group:
            row['pareto'] = not any(dominates(other, row) for other in group)
        rows += group
    return rows


def checks():
    anchors = dense_checks = 0
    for n, banks, lead, rpm in itertools.product((64, 80), (1, 2, 3, 4), (2, 3), (400, 600, 850)):
        for delta in a.workloads(n).values():
            scaled = [[d*3/lead for d in row] for row in delta]
            ref = a.r.schedule(scaled, banks, pitch=a.c.v.s.WIDTH/n, rpm=rpm)['seconds']
            got = a.schedule(delta, n, rpm, lead=lead, banks=banks)
            assert math.isclose(ref, got['feasible_s'], abs_tol=1e-9)
            assert math.isclose(ref, got['lower_s'], abs_tol=1e-9)
            anchors += 1
        for k, stroke in itertools.product(quotas(n, banks), (40, 50)):
            width = math.ceil(n/banks)
            dwell = .1+math.ceil(n/k)*a.r.spin(stroke/lead, rpm)
            seek = .05+(width-1)*max(.05, a.r.move(a.c.v.s.WIDTH/n))
            exact = 4+seek+a.r.move((width-1)*a.c.v.s.WIDTH/n)+(width+1)*dwell
            got = a.schedule(a.c.v.s.flat(n, stroke), k, rpm, lead=lead, banks=banks)
            assert math.isclose(got['feasible_s'], exact, abs_tol=1e-9)
            assert math.isclose(got['lower_s'], exact, abs_tol=1e-9)
            dense_checks += 1
    for n, banks in itertools.product((64, 80), (1, 2, 3, 4)):
        c = cost(n, banks)
        if banks >= 2:
            assert c['subset_plus_reserve_USD'] == l.subset_cost(n, banks)['allocated_plus_quoted_USD']
        # Brute-force supplier orders independently validate tier choices,
        # including one-bank prices and the 192-output driver surplus.
        motors = min(q*(1.56 if q >= 100 else 1.76 if q >= 10 else 1.95)
                     for q in range(c['outputs'], max(100,c['outputs'])+1))
        drivers = min(q*(4.76 if q >= 100 else 5.36 if q >= 10 else 5.95)
                      for q in range(c['outputs']//2, max(100,c['outputs']//2)+1))
        assert math.isclose(c['subset_plus_reserve_USD'], c['reserve_USD']+motors+drivers)
        assert banks*min(n,64//banks) <= 64
        for budget, residual in c['remaining_per_output_USD'].items():
            assert math.isclose(c['subset_plus_reserve_USD']+c['outputs']*residual,budget)
    assert cost(64,1)['motor_quantity'] == 64
    assert cost(64,3)['spare_boards'] == 4
    assert abs(case(64,2,32,3,850,40)['scene_s']-35.54) < .01
    assert abs(case(64,2,32,3,850,50)['scene_s']-43.29) < .01
    for n in (64,80):
        # Shallow deltas really apply to N20/S40; no free moving-neutral premise.
        targets, start = a.c.terrain(n,20,20)
        old = a.workloads(n)
        for name in a.c.v.s.SUITES['relief']:
            assert a.r.delta(start,targets[name]) == old['ground>shallow:'+name]
        assert all(0 <= h <= 40 for name in a.c.v.s.SUITES['relief'] for row in targets[name] for h in row)
        targets,_ = a.c.terrain(n,30,30)
        assert all(0 <= h <= 50 for name in a.c.v.s.SUITES['relief'] for row in targets[name] for h in row)
    toy = dict(subset_plus_reserve_USD=1,outputs=1,powered_outputs=1,scene_s=1,prep_s=1,dense_s=1)
    assert not dominates(toy,toy)
    assert dominates(toy,dict(toy,scene_s=2))
    assert not dominates(dict(toy,powered_outputs=2),dict(toy,scene_s=2))
    return f'{anchors} full-slot inherited anchors; {dense_checks} exact dense waves; E-262 anchors, supplier enumeration, quotas, budgets, reach/deltas and Pareto controls'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--local-reveals', action='store_true',
                        help='run the reusable XY-head extension preserved in E-267')
    args = parser.parse_args()
    if args.local_reveals:
        spec = importlib.util.spec_from_file_location('short_head',
                    Path(__file__).resolve().parents[1] / 'E-267/screen.py')
        short = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(short)
        verified = short.checks()
        print(verified if args.check else json.dumps(short.report(verified), indent=2))
        return
    verified = checks()
    if args.check:
        print(verified)
        return
    rows = sweep()
    sensitivity = [case(n,b,k,lead,850,stroke,accel=200,release=.005)
                   for n,lead,stroke,b,k in itertools.product((64,80),(2,3),(40,50),(2,3),(32,))]
    print(json.dumps(dict(evidence='Conditional schedules and dated price subset, not ratings/BOM',
        verification=verified, rows=rows, slower_ramp_and_stop_sensitivity=sensitivity), indent=2))


if __name__ == '__main__':
    main()
