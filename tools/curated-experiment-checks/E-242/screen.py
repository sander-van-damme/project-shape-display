"""E-242: reused traveling command writers, not a qualified magnetic machine.

Stdlib; stdout only. Timing/cost screen deliberately precedes field refinement.
All motion, geometric and allocation scenarios are bounds, not measurements.
"""
import importlib.util
import itertools as it
import json
import math
from functools import lru_cache
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    'e241', Path(__file__).resolve().parents[1]/'E-241'/'screen.py')
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
drive = prior.prior
GROUPS = (1, 2, 4, 5, 8, 10, 16, 20, 40)
SPEEDS = ((.2, 8.), (.5, 20.), (1., 40.), (2., 80.))


def writer(mode, q, pitch, pulse, width, speed, acceleration):
    """q parallel tracks, 80/q flags/track; alternating scan, no empty return.

    Flying current+extinction fit inside the granted spatial field window.
    Endpoint acceleration gives MORE dwell; no instantaneous speed change.
    A final 1 ms extinction and 3 ms physical proof are charged conservatively.
    Field width is a grant, not an electromagnetic result.
    """
    n = 80//q
    assert 80 % q == 0
    if mode == 'stopped':
        return n*(pulse+.001)+(n-1)*drive.move(pitch, v=speed, a=acceleration)+.003
    assert mode == 'flying'
    v = min(speed, width/1000/(pulse+.001))
    return drive.move((n-1)*pitch+width, v=v, a=acceleration)+.004


@lru_cache(None)
def cost(banks, q, turns):
    flags = 80*banks
    writers = q*banks
    bridges = min(max(150,5*math.ceil(writers/5))*.1684,
                  max(500,5*math.ceil(writers/5))*.1428)
    magnets = min(math.ceil(flags/10)*1.32, max(50,math.ceil(flags/10))*1.20)
    shifts = max(50,math.ceil(2*writers/8))*.0906
    wire = prior.e240.wire_buy(writers*turns*.030*1.15)[0]
    sourced = dict(bridges=bridges, magnets=magnets, shifts=shifts, wire=wire)
    # Retain the existing $20 common writer drive; synchronized slides only.
    # Added bank guide/mount allowance explicitly pays some new scan machinery.
    extras = dict(pcbs=25, pulse_power=20, targets_pivots=.05*flags,
                  harness=10, passives=5, winding_fixture=5, scan_mounts=5*banks)
    reserve = sum(drive.reserve(banks).values())
    return dict(reserve=reserve, sourced=sourced, extras_assumed=extras,
                total=reserve+sum(sourced.values())+sum(extras.values()))


def scan_bits(old, target, q, reverse):
    """Ideal spatial addressing and passive retention only; no field immunity."""
    n = len(old)//q
    bits = list(old)
    order = list(range(n))
    if reverse:
        order.reverse()
    written = set()
    observations = 0
    for position in order:
        for track in range(q):
            index = track*n+position
            bits[index] = target[index]
            written.add(index)
        for index in range(len(bits)):
            assert bits[index] == (target[index] if index in written else old[index])
            observations += 1
    return tuple(bits), observations


def expanded_schedule(banks, write, rows=None):
    # Independently expand actual rows and the causal complete-row retry.
    elapsed = 2.
    for _ in range((math.ceil(80/banks) if rows is None else rows)+1):
        for stroke in drive.SEQ:
            elapsed += write
            for _ in range(2):
                elapsed += drive.move(2)+.003
            elapsed += drive.move(stroke)
            for _ in range(2):
                elapsed += drive.move(2)+.003
        elapsed += drive.move(5.08)
    return elapsed+drive.move(30)+.010


def checks():
    overwrites = observations = 0
    for old, target in it.product(it.product((0,1), repeat=4), repeat=2):
        for q, reverse in it.product((1,2,4),(False,True)):
            result, count = scan_bits(old,target,q,reverse)
            assert result == target
            observations += count
            overwrites += 1
    schedules = 0
    for b, mode, q in it.product((4,5,8,20),('stopped','flying'),(1,20,40)):
        w = writer(mode,q,20.32,.02,4,.2,8)
        assert abs(expanded_schedule(b,w)-drive.schedule(b,writer=w)) < 1e-9
        schedules += 1
    # One site is a direct dwell in the stopped limit. No hidden return stroke.
    assert abs(writer('stopped',80,20,.02,4,.2,8)-.024) < 1e-12
    # A cruise window receives at least pulse plus extinction at capped speed.
    for pulse, width, (v,a) in it.product((.005,.01,.02,.04),(2,4,8),SPEEDS):
        speed = min(v,width/1000/(pulse+.001))
        assert width/1000/speed+1e-12 >= pulse+.001
    # Reuse does not create free double buffers or permit writing loaded outputs.
    permitted = 0
    for resident, pickup, rewriting in it.product((False,True), repeat=3):
        ok = (resident or pickup) and (not rewriting or (resident and not pickup))
        if ok:
            assert not (pickup and rewriting)
            permitted += 1
    return dict(overwrites=overwrites,bit_observations=observations,
                schedule_expansions=schedules,allowed_support_states=permitted)


def main():
    scenarios = []
    screened = 0
    for mode, q, pitch, pulse, width, (v,a) in it.product(
            ('stopped','flying'),GROUPS,(10.16,20.32,40.64),
            (.005,.01,.02,.04),(2,4,8),SPEEDS):
        if mode == 'stopped' and width != 2:
            continue  # spatial-window width has no effect on a stopped writer
        screened += 1
        w = writer(mode,q,pitch,pulse,width,v,a)
        # Charge all 160B signed command bits at an assumed 1-Mbit/s bus,
        # even though streaming could overlap travel. No free data fanout.
        b = next((b for b in range(4,81)
                  if drive.schedule(b,writer=w+160*b/1e6)<30),None)
        if b is None:
            continue
        w += 160*b/1e6
        for turns in (100,200,400):
            scenarios.append(dict(mode=mode,banks=b,q=q,flags=80*b,writers=q*b,
                pitch_mm=pitch,pulse_ms=1000*pulse,width_mm=width,v=v,a=a,
                turns=turns,write_s=w,seconds=drive.schedule(b,writer=w),
                cost=cost(b,q,turns)['total']))
    # Select by price then time, without misreporting tested counts as designs.
    key = lambda c:(c['cost'],c['seconds'])
    best = []
    for mode,(v,a) in it.product(('stopped','flying'),SPEEDS):
        xs = [c for c in scenarios if c['mode']==mode and c['v']==v]
        c = min(xs,key=key)
        best.append(dict(**c,ledger=cost(c['banks'],c['q'],c['turns'])))
    cheapest = min(scenarios,key=key)
    # Before constructing fringe fields: grant E-241's stronger bore field.
    # This is a deliberately favorable COMPARATOR, not a bound on every magnet.
    # Reusing a coil does not itself change that coil/flag motion certificate.
    motion = []
    for turns,current,pulse in it.product((100,200,400),(.2,.4,.8,1.2),(.005,.01,.02,.04)):
        power = prior.power(1,turns,current,pulse,1)
        window = prior.barrier_window(turns,current,pulse)
        if power['coil_voltage']+power['bridge_voltage_typ'] >= 5:
            continue
        low = window['barrier_low_uJ']
        kinetic = window['midpoint_kinetic_uJ']
        friction = 6e-6*prior.A*1e6
        # A nominal barrier large enough to retain its -30% specimen must
        # also switch its +30% specimen; the reader is retracted during write.
        demand = 1.3*low+kinetic+friction
        motion.append(dict(turns=turns,current=current,pulse_ms=pulse*1000,
            **window,midpoint_demand_uJ=demand,
            midpoint_ok=window['midpoint_input_uJ']>=demand))
    print(json.dumps(dict(checks=checks(),timing_cases=screened,
        timed_winding_cases=len(scenarios),best_by_speed=best,
        under_500=[c for c in scenarios if c['cost']<500],
        cheapest=cheapest,
        allocation_sensitivity=[dict(reserve_reduction=cut,
            best_cost=cheapest['cost']-cut,
            timed_cases_under_500=sum(c['cost']-cut<500 for c in scenarios))
            for cut in (0,25,50,100)],
        optimistic_bore_motion=motion,
        motion_certificates=sum(c['feasible'] for c in motion),
        midpoint_survivors=sum(c['midpoint_ok'] for c in motion),
        reader_sensitivity=[dict(reader_N=f,field_factor=k,
            **prior.barrier_window(200,.8,.02,reader=f,k=k))
            for f,k in it.product((0,.005,.01),(.25,.5,1))],
        direct_comparator=dict(seconds=drive.schedule(4,writer=prior.write_time(4,.005,80)),
                               cost=prior.costs(4,100)['total']),
        regional_example_s=drive.schedule(cheapest['banks'],writer=cheapest['write_s'],rows=5),
        cheapest_pulse_power=prior.power(cheapest['banks'],100,1.2,.005,cheapest['q']),
        nonlocal_field_bounds=[prior.parasitic_bound(p,c,r) for p,c,r in
                               ((.01016,40,2),(.02032,20,4),(.04064,10,8))]),indent=2))


if __name__ == '__main__':
    main()
