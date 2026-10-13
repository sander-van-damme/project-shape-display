#!/usr/bin/env python3
"""Propagate 2/3-mm lead scenarios; no measured lead bounds or motor qualification.

E-256 owner estimate does not identify a thread. Keep geometry, friction, torque
and acceleration assumptions explicit. JSON stdout is disposable.
"""
import argparse
import importlib.util
import itertools
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location('admission', Path(__file__).with_name('concurrency.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
e = a.c.e


def subset_cost(n, banks):
    """Dated Adafruit 711/3297 tiers plus inherited unquoted reserve, NOT BOM.

    Compare buying only needed boards with a surplus order to reach next tier.
    Source URLs/2026-10-13 check in canonical E-259. No extra tax/freight quote.
    """
    outputs = n*banks
    assert outputs >= 100 and outputs % 2 == 0
    needed = outputs//2
    quantity, unit = min(((max(needed, q), price) for q, price in
                         ((1, 5.95), (10, 5.36), (100, 4.76))),
                        key=lambda qp: qp[0]*qp[1])
    reserve = a.r.costs(banks, n=n)['reserve']
    total = reserve+outputs*1.56+quantity*unit
    return dict(installed_outputs=outputs, driver_boards_needed=needed,
                driver_boards_bought=quantity, spare_boards=quantity-needed,
                allocated_plus_quoted_USD=total,
                remaining_per_output_USD={b: (b-total)/outputs for b in (500,1000,1500)},
                motor_kg=outputs*.0175)


def rpm_boundary(n, k, lead, accel, banks=2, field='feasible_s'):
    """30-second boundary for this schedule, not physical maximum speed."""
    # Largest move is <=50 mm; all durations triangular above this speed.
    low, high = 1., 60*math.sqrt(50/lead*accel)
    def worst(rpm):
        return a.suite(n,k,rpm,accel,lead=lead,banks=banks)[field]
    ceiling = worst(high)
    if ceiling >= 30:
        return dict(rpm=None, triangular_limit_s=ceiling)
    for _ in range(35):
        middle = (low+high)/2
        if worst(middle) >= 30:
            low = middle
        else:
            high = middle
    return dict(rpm=high, triangular_limit_s=ceiling)


def drive(lead, ratio, motor_accel=1500):
    """Transform ONE rated-point hypothesis; not a speed-torque curve.

    Motor 3000 rpm is the lower listed loaded endpoint. Common assumed motor
    acceleration propagates through ratio. Efficiency .7 is an assumption for
    both routes; the 1:1 comparator still owes shaft routing/docking. J includes
    motor-reflected and output hardware inertia; its bound is not measured.
    """
    rpm = 3000/ratio
    accel = motor_accel/ratio
    available = .980665*ratio*.7
    required = e.torque(20,.3,.05,accel,0,lead=lead)
    jmax = (available-required)/(1000*2*math.pi*accel)
    return dict(lead_mm=lead, ratio=ratio, assumed_motor_accel_rev_s2=motor_accel,
                output_rpm=rpm, output_accel_rev_s2=accel,
                axial_speed_mm_s=lead*rpm/60, axial_accel_mm_s2=lead*accel,
                available_Nmm=available, required_excluding_rotating_J_Nmm=required,
                effective_output_J_ceiling_kgm2=jmax,
                motor_J_ceiling_with_zero_output_inertia_kgm2=jmax/ratio**2,
                all_presets_64_K32_s=a.suite(64,32,rpm,accel,lead=lead)['feasible_s'])


def checks():
    anchors = 0
    for n, banks, lead in itertools.product((64,80),(2,3),(2,3)):
        for delta in a.workloads(n).values():
            # Independent existing scheduler uses 3-mm lead; scaling only the
            # mathematical delta gives identical turns. Never reinterpret maps.
            scaled = [[d*3/lead for d in row] for row in delta]
            ref = a.r.schedule(scaled,banks,pitch=a.c.v.s.WIDTH/n,rpm=2000)['seconds']
            actual = a.schedule(delta,n,lead=lead,banks=banks)
            assert math.isclose(ref,actual['feasible_s'],abs_tol=1e-9)
            assert math.isclose(ref,actual['lower_s'],abs_tol=1e-9)
            anchors += 1
        for k in (16,n):
            assert a.schedule([[0]*n for _ in range(n)],k,lead=lead,banks=banks)['feasible_s'] == 0
            positive = [[50]*n for _ in range(n)]
            assert a.schedule(positive,k,lead=lead,banks=banks) == a.schedule(
                [[-50]*n for _ in range(n)],k,lead=lead,banks=banks)
            # Exact dense wave count and largest bank independently reconstructed.
            width = math.ceil(n/banks)
            dwell = .1+math.ceil(n/k)*a.r.spin(50/lead,2000)
            travel = .05+(width-1)*max(.05,a.r.move(a.c.v.s.WIDTH/n))+a.r.move((width-1)*a.c.v.s.WIDTH/n)
            assert math.isclose(a.schedule(positive,k,lead=lead,banks=banks)['feasible_s'],
                                4+travel+(width+1)*dwell,abs_tol=1e-9)
    # Exact trajectory equivalence requires scaling BOTH speed and acceleration.
    for turns in (.1,1,10,25):
        assert math.isclose(a.r.spin(turns,2000,1000),
                            a.r.spin(1.5*turns,3000,1500))
    for lead in (2,3):
        up, down = e.coefficients(0,lead=lead)
        assert math.isclose(up,lead/(2*math.pi)) and down == -up
        mu = lead/(math.pi*2.3)*math.cos(math.radians(15))
        assert abs(e.coefficients(mu,lead=lead)[1]) < 1e-15
        added = e.torque(20,0,0,1000,lead=lead)-e.torque(20,0,0,lead=lead)
        j = .02*(lead/1000/(2*math.pi))**2
        assert math.isclose(added,j*2*math.pi*1000*1000)
    # Cache must distinguish lead and bank settings, irrespective of call order.
    delta = next(iter(a.workloads(64).values()))
    before = a.schedule(delta,32,lead=3)
    a.schedule(delta,32,lead=2,banks=3)
    assert before == a.schedule(delta,32,lead=3)
    assert subset_cost(64,2)['allocated_plus_quoted_USD'] == a.c.cost(64)['allocated_plus_quoted']
    c3 = subset_cost(64,3)
    assert c3['driver_boards_bought'] == 100 and c3['spare_boards'] == 4
    assert 100*4.76 < 96*5.36
    for n, banks in itertools.product((64,80),(2,3)):
        c = subset_cost(n,banks)
        for budget,remain in c['remaining_per_output_USD'].items():
            assert math.isclose(c['allocated_plus_quoted_USD']+n*banks*remain,budget)
    return f'{anchors} inherited full-slot anchors; exact dense-wave, signed/no-op, cache, work/inertia, motion-scaling and quantity-tier controls'


def main():
    rows = []
    for n, lead, banks, k, rpm, accel in itertools.product((64,80),(2,3),(2,3),(32,64),(2000,3000),(200,1000)):
        # k=64 is full only for64; include80 separately below.
        result = a.suite(n,k,rpm,accel,lead=lead,banks=banks)
        rows.append(dict(n=n,lead_mm=lead,banks=banks,k=k,rpm=rpm,accel=accel,**result))
    full = [dict(n=n,lead_mm=lead,banks=2,k=n,
                 **a.suite(n,n,2000,1000,lead=lead)) for n,lead in itertools.product((64,80),(2,3))]
    setup_stress = [dict(n=n,lead_mm=lead,k=k,
        prep30_s=a.schedule(a.c.v.s.flat(n,30),k,lead=lead)['feasible_s'],
        dense50_s=a.schedule(a.c.v.s.flat(n,50),k,lead=lead)['feasible_s'])
        for n,lead,k in itertools.product((64,80),(2,3),(32,64))]
    boundaries = [dict(n=n,k=k,lead_mm=2,accel=accel,
                  **rpm_boundary(n,k,2,accel)) for n in (64,80) for k in (32,n) for accel in (200,1000)]
    print(json.dumps(dict(evidence='Conditional calculations; rough 2-mm estimate is not a measured CAD lead',
        verification=checks(),schedules=rows,full_concurrency=full,setup_stress=setup_stress,
        boundaries=boundaries,drive=[drive(lead,ratio) for lead,ratio in ((3,1.5),(2,1.5),(2,1))],
        costs=[dict(n=n,banks=b,**subset_cost(n,b)) for n,b in itertools.product((64,80),(2,3))]),indent=2))


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    if parser.parse_args().check:
        print(checks())
    else:
        main()
