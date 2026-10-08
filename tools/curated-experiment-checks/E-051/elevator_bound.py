"""Exact abstract event scheduling; mm/s. No geometry or hardware qualification.
Run from any directory with Python 3. No stochastic assumptions or seed.
"""
import heapq
import itertools
import json
from math import sqrt

LEVELS = (0, 10, 20, 30, 40)
PAIRS = tuple(itertools.permutations(range(5), 2))
SCENARIOS = {'fast': (400, 20000, .025, 2),
             'central': (200, 5000, .05, 4),
             'slow': (80, 1000, .10, 8)}


def move(d, v, a):
    return 2 * sqrt(d / a) if d <= v * v / a else d / v + v / a


def solve(pairs, v, a, event):
    """Acquire at first old-height visit; release at first subsequent target.
    State: elevator level, ever visited levels, completed ordered transitions.
    Zero-offset rigid grippers follow elevator while attached. All same-height
    operations run in parallel. event is total serial dwell per visited stop,
    including acquisition/unload/unlock or relatch/proof/release. Count home
    initially and finally; permit cost-free terminal home dwell as a relaxation.
    """
    goal = (1 << len(pairs)) - 1
    start = (0, 1, 0)
    costs = {start: event}
    queue = [(event, start, (0,))]
    settled = 0
    while queue:
        cost, state, path = heapq.heappop(queue)
        if cost != costs[state]:
            continue
        settled += 1
        pos, seen, done = state
        if pos == 0 and done == goal:
            return dict(seconds=cost, path_mm=[LEVELS[x] for x in path],
                        settled_states=settled)
        for dest in range(5):
            if dest == pos:
                continue
            completed = done
            for bit, (old, new) in enumerate(pairs):
                if new == dest and seen & (1 << old):
                    completed |= 1 << bit
            next_state = (dest, seen | (1 << dest), completed)
            # A return with all work already done needs no event dwell.
            dwell = 0 if dest == 0 and done == goal else event
            trial = cost + move(abs(LEVELS[dest] - LEVELS[pos]), v, a) + dwell
            if trial < costs.get(next_state, float('inf')):
                costs[next_state] = trial
                heapq.heappush(queue, (trial, next_state, path + (dest,)))
    raise AssertionError('unreachable')


def validate(path, pairs):
    # Independently replay individual cells, not search bitmasks.
    for old, new in pairs:
        status = 'latched'
        for height in path:
            if status == 'latched' and height == LEVELS[old]:
                status = 'held'
            elif status == 'held' and height == LEVELS[new]:
                status = 'done'
        assert status == 'done'


def main():
    assert move(0, 400, 20000) == 0
    assert abs(move(40, 400, 20000) - .12) < 1e-12
    # Independent limiting case: just one 0->40 cell, home round trip.
    one = solve(((0, 4),), 400, 20000, 0)
    assert abs(one['seconds'] - .24) < 1e-12
    records = []
    for scenario, (v, a, index_min, overhead) in SCENARIOS.items():
        for event in (0, .01, .02, .04, .08):
            result = solve(PAIRS, v, a, event)
            validate(result['path_mm'], PAIRS)
            for heads in (80, 160):
                rows = heads // 80
                index = max(index_min, move(5.08 * rows, v, a))
                seconds = overhead + (80 // rows) * (result['seconds'] + index)
                records.append(dict(scenario=scenario, heads=heads,
                                    event_dwell_s=event, full_map_s=seconds,
                                    passes=seconds < 30, **result))
    # Compare the optimum to a separately computed feasible eight-edge sweep.
    # This hand trajectory is not an independent proof of global optimality.
    fast = solve(PAIRS, 400, 20000, 0)
    assert abs(fast['seconds'] - 8 * move(10, 400, 20000)) < 1e-12
    assert len(fast['path_mm']) == 9
    print(json.dumps({'transitions': len(PAIRS), 'records': records}, indent=2))

if __name__ == '__main__':
    main()
