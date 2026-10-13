#!/usr/bin/env python3
"""Conditional bank schedules with at most K energized outputs per head.

All motors/feedback/docks remain installed. Nonpreemptive longest-first admission
is a feasible electrical-slot schedule, not a fabricated or qualified drive.
Reuse E-258 geometry and E-255 motion/overhead. JSON stdout is disposable.
"""
import argparse
import heapq
import itertools
import json
import math
from functools import lru_cache
from pathlib import Path
import importlib.util

spec = importlib.util.spec_from_file_location('channels', Path(__file__).with_name('channel_screen.py'))
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
r = c.r


def slots(jobs, k):
    """Return LPT witness (cell,start,end,slot), plus rigorous row lower bound.

    Jobs run on their own physical motors. A slot is an admission token, not a
    motor multiplexor. Completion releases the token after the modelled stop.
    """
    if k < 1 or int(k) != k:
        raise ValueError('positive integer concurrency required')
    jobs = sorted(jobs, key=lambda item: (-item[1], item[0]))
    if not jobs:
        return [], 0.0
    if any(t <= 0 or not math.isfinite(t) for _, t in jobs):
        raise ValueError('finite positive durations required')
    free = [(0.0, i) for i in range(k)]
    witness = []
    for cell, duration in jobs:
        start, lane = heapq.heappop(free)
        end = start + duration
        witness.append((cell, start, end, lane))
        heapq.heappush(free, (end, lane))
    # Any j jobs at least duration t need a lane containing ceil(j/k) of them.
    lower = max(sum(t for _, t in jobs)/k,
                max(math.ceil(j/k)*t for j, (_, t) in enumerate(jobs, 1)))
    return witness, lower


@lru_cache(maxsize=None)
def row_bounds(row, k, rpm, accel, proof, release, lead=3):
    jobs = [(x, r.spin(abs(d)/lead, rpm, accel)+release)
            for x, d in enumerate(row) if d]
    if not jobs:
        return 0.0, 0.0
    witness, lower = slots(jobs, k)
    return .08+proof+lower, .08+proof+max(job[2] for job in witness)


def schedule(delta, k, rpm=2000, accel=1000, proof=.02, release=0, lead=3, banks=2):
    """Fixed row banks; preserved seek, return, full-row retry and 4 s.

    Lower/upper bracket the inherited additive accounting (4 + slowest bank
    + globally longest row retry), with fixed local quotas. This conservative
    retry charge is not the tight adversarial wall-clock optimum. Global token
    lending, preemption or changed routes are not bounded.
    release is an assumed per-output stop/current-settle token occupancy.
    """
    n = len(delta)
    assert all(len(row) == n for row in delta)
    assert 1 <= k <= n and rpm > 0 and accel > 0 and proof >= 0 and release >= 0
    assert lead > 0 and math.isfinite(lead) and 1 <= banks <= n and int(banks) == banks
    width = math.ceil(n/banks)
    bank_times = []; retry = [0.0, 0.0]; stations = 0
    for base in range(0, n, width):
        last = 0; times = [0.0, 0.0]; active = False
        for y in range(base, min(n, base+width)):
            if not any(delta[y]):
                continue
            # Identical independent outputs: service depends on absolute move
            # multiset, not cell order/sign. Preserve geometry for seeks only.
            key = tuple(sorted(abs(d) for d in delta[y] if d))
            dwell = row_bounds(key, k, rpm, accel, proof, release, lead)
            seek = max(.05, r.move(abs(y-base-last)*c.v.s.WIDTH/n))
            for i in (0, 1):
                times[i] += seek+dwell[i]
                retry[i] = max(retry[i], dwell[i])
            last = y-base; active = True; stations += 1
        if active:
            times = [t+r.move(last*c.v.s.WIDTH/n) for t in times]
        bank_times.append(times)
    result = [4+max(b[i] for b in bank_times)+retry[i] for i in (0, 1)] if stations else [0., 0.]
    assert result[0] <= result[1]+1e-9
    return dict(lower_s=result[0], feasible_s=result[1], stations=stations)


@lru_cache(maxsize=None)
def workloads(n):
    states = {}
    for mode, depth in (('shallow', 20), ('deep', 30)):
        targets, start = c.terrain(n, 30, depth)
        states.update({mode+':'+name: targets[name] for name in c.v.s.SUITES['relief']})
    cases = {'ground>'+name: r.delta(start, h) for name, h in states.items()}
    cases.update({a+'>'+b: r.delta(states[a], states[b]) for a, b in itertools.permutations(states, 2)})
    return cases


def suite(n, k, rpm=2000, accel=1000, release=0, lead=3, banks=2):
    cases = workloads(n)
    rows = {name: schedule(d, k, rpm, accel, release=release, lead=lead, banks=banks)
            for name, d in cases.items()}
    maximum = max(rows, key=lambda name: rows[name]['feasible_s'])
    lower = max(v['lower_s'] for v in rows.values())
    return dict(lower_s=lower, feasible_s=rows[maximum]['feasible_s'], worst=maximum,
        shallow_max_s=max(v['feasible_s'] for name, v in rows.items() if 'deep:' not in name),
        deep_max_s=max(v['feasible_s'] for name, v in rows.items() if 'shallow:' not in name),
        switch_s=rows['shallow:ravine>deep:ravine']['feasible_s'])


def exact_small(durations, k):
    """Independent exhaustive partition oracle for small validation inputs."""
    best = sum(durations)
    for assignment in itertools.product(range(k), repeat=len(durations)):
        loads = [0.]*k
        for lane, duration in zip(assignment, durations):
            loads[lane] += duration
        best = min(best, max(loads))
    return best


def checks():
    # Reconstruct witness: every cell once, finite duration, no same-slot overlap.
    checked = 0
    for durations in itertools.product((1., 2., 3.), repeat=5):
        for k in (1, 2, 3):
            witness, lower = slots(list(enumerate(durations)), k)
            assert sorted(w[0] for w in witness) == list(range(5))
            for cell, start, end, lane in witness:
                assert math.isclose(end-start, durations[cell]) and start >= 0
            for lane in range(k):
                intervals = sorted((s, e) for _, s, e, l in witness if l == lane)
                assert all(a[1] <= b[0]+1e-12 for a, b in zip(intervals, intervals[1:]))
            exact = exact_small(durations, k)
            assert lower <= exact+1e-10 <= max(w[2] for w in witness)+1e-10
            checked += 1
    # LPT is not asserted optimal: classic counterexample 3,3,2,2,2 on two slots.
    w, lower = slots(list(enumerate((3, 3, 2, 2, 2))), 2)
    assert lower == 6 and max(j[2] for j in w) == 7 and exact_small((3,3,2,2,2),2) == 6
    for n in (64, 80):
        for name, delta in workloads(n).items():
            reference = r.schedule(delta, 2, pitch=c.v.s.WIDTH/n, rpm=2000)['seconds']
            full = schedule(delta, n)
            assert math.isclose(full['lower_s'], reference, abs_tol=1e-9)
            assert math.isclose(full['feasible_s'], reference, abs_tol=1e-9)
            assert schedule([[-d for d in row] for row in delta], 16) == schedule(delta, 16)
        assert schedule([[0]*n for _ in range(n)], 1)['feasible_s'] == 0
        # Dense equal-duration case has exactly ceil(n/k) waves at each station.
        for k in (8, 16, 24, n):
            dense = [[40]*n for _ in range(n)]
            result = schedule(dense, k)
            dwell = .1+math.ceil(n/k)*r.spin(40/3, 2000)
            travel = .05+(n//2-1)*max(.05, r.move(c.v.s.WIDTH/n))+r.move((n//2-1)*c.v.s.WIDTH/n)
            exact = 4+travel+(n//2+1)*dwell
            assert math.isclose(result['lower_s'], exact, abs_tol=1e-9)
            assert math.isclose(result['feasible_s'], exact, abs_tol=1e-9)
    return f'{checked} exhaustive small row comparisons; LPT nonoptimal witness; all full-concurrency map anchors; signed/no-op/dense controls'


def main():
    result = dict(verification=checks(), scenarios=[])
    for n, rpm, accel in itertools.product((64, 80), (2000, 1500), (1000, 200)):
        scan = {k: suite(n, k, rpm, accel) for k in range(1, n+1)}
        sufficient = next((k for k, v in scan.items() if v['feasible_s'] <= 30), None)
        possible = next((k for k, v in scan.items() if v['lower_s'] <= 30), None)
        sample = sorted({8, 16, 24, 32, 48, n} | ({sufficient} if sufficient else set()))
        rows = []
        for k in sample:
            rows.append(dict(k_per_head=k, **scan[k],
                rated_load_motor_A=2*k*.25, stall_motor_A=2*k*.5,
                prep30_s=schedule(c.v.s.flat(n, 30), k, rpm, accel)['feasible_s'],
                dense50_s=schedule(c.v.s.flat(n, 50), k, rpm, accel)['feasible_s'],
                release5ms_s=suite(n, k, rpm, accel, .005)['feasible_s']))
        result['scenarios'].append(dict(n=n, rpm=rpm, accel_rev_s2=accel,
            smallest_not_excluded_k=possible, smallest_LPT_sufficient_k=sufficient, rows=rows))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='only run verification controls')
    if parser.parse_args().check:
        print(checks())
    else:
        main()
