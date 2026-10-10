#!/usr/bin/env python3
"""E-126 necessary conditions only. mm, N, s, USD; no process distributions."""
import itertools
import json
import math

PITCH = 5.08
CELLS = 6400


def height(n, d, clearance):
    """Rigid equal spheres in a straight bore; alternating wall-contact minimum."""
    if n == 0:
        return 0.0
    return d + (n - 1) * math.sqrt(d*d - clearance*clearance)


def required_count(d, clearance):
    n = 0
    while height(n, d, clearance) < 40:
        n += 1
    return n


def distance_rectangle(x, z, box):
    xmin, xmax, zmin, zmax = box
    return math.hypot(max(xmin-x, 0, x-xmax), max(zmin-z, 0, z-zmax))


def fork_clearance(d, bore, a, width, thickness, error):
    """Finite x-z blades swept through all y. Exact sphere/swept-box distance.

    Lower sphere centre z=0 is a local fixture assumption. Test common bead
    diameter extremes, bore extremes, all opposing/same-side centre offsets,
    and blade growth. Does not supply a full transfer or qualify guides.
    """
    worst = math.inf
    for dd, bb in itertools.product((d-error, d+error),
                                    (bore-2*error, bore+2*error)):
        play = bb-dd
        if play < 0:
            return -math.inf
        for sign0, sign1 in itertools.product((-1, 1), repeat=2):
            x0, x1 = sign0*play/2, sign1*play/2
            dz = math.sqrt(dd*dd-(x1-x0)**2)
            for side in (-1, 1):
                xlo, xhi = sorted((side*a, side*(a+width)))
                box = (xlo-error, xhi+error,
                       d/2-thickness/2-error, d/2+thickness/2+error)
                for x, z in ((x0, 0), (x1, dz)):
                    worst = min(worst, distance_rectangle(x, z, box)-dd/2)
    return worst


def stroke_time(distance, vmax, accel):
    """Rest-to-rest symmetric acceleration; no jerk or load derating."""
    if distance <= vmax*vmax/accel:
        return 2*math.sqrt(distance/accel)
    return distance/vmax + vmax/accel


def cycles(deltas, heads, shared_direction):
    total = 0
    for start in range(0, len(deltas), heads):
        batch = deltas[start:start+heads]
        if shared_direction:
            total += max([0]+batch) + max([0]+[-d for d in batch])
        else:
            total += max(abs(d) for d in batch)
    return total


def checks():
    assert height(10, 4, 0) == 40
    assert height(0, 4, .2) == 0
    # Independently reconstruct a finite alternating stack, checking contacts.
    for n, d, c in itertools.product((1, 2, 11), (2, 4), (0, .2, .4)):
        points = [(0.0, d/2)]
        for i in range(1, n):
            x = c if i % 2 else 0.0
            oldx, oldz = points[-1]
            z = oldz + math.sqrt(d*d-(x-oldx)**2)
            assert abs(math.hypot(x-oldx, z-oldz)-d) < 1e-12
            points.append((x, z))
        assert abs(points[-1][1]+d/2-height(n, d, c)) < 1e-10
    assert cycles([3, -3], 2, True) == 6
    assert cycles([3, -3], 2, False) == 3
    assert cycles([0, 0], 2, True) == 0
    assert cycles([1], 80, True) == 1
    # Reconstruct optimal abstract unit-step schedules for every two-site map.
    for delta in itertools.product(range(-4, 5), repeat=2):
        state = [0, 0]
        count = 0
        for sign in (1, -1):
            while any(sign*(target-current)>0 for target,current in zip(delta,state)):
                state = [v+sign if sign*(t-v)>0 else v for t,v in zip(delta,state)]
                count += 1
        assert tuple(state) == delta and count == cycles(list(delta), 2, True)
    assert distance_rectangle(0, 0, (1, 2, 1, 2)) == math.sqrt(2)
    assert distance_rectangle(1.5, 1.5, (1, 2, 1, 2)) == 0
    # Time formula continuous at triangular/trapezoidal boundary.
    assert abs(stroke_time(10, 100, 1000)-.2) < 1e-12


def main():
    checks()
    sections = []
    # Explicit bounds, not X1C priors. Cell envelope excludes supply magazine.
    for d, c, wall, e in itertools.product((2, 3, 4), (.1, .2, .4),
                                           (.3, .4), (.025, .05, .1)):
        if c-3*e <= 0 or d+c+2*wall+2*e > PITCH:
            continue
        candidates = []
        for k in range(8, 45):
            a = k*.05
            if a+.4+wall+e > PITCH/2:
                continue
            gap = fork_clearance(d, d+c, a, .4, .4, e)
            if gap >= 0:
                candidates.append((a, gap))
        if candidates:
            sections.append({'d': d, 'clearance': c, 'wall': wall, 'e': e,
                             'smallest_a': candidates[0][0],
                             'sweep_clearance': candidates[0][1]})
    # Common lower-diameter/bore-upper corner: no iid averaging allowed.
    stacks = []
    for d, c, e in itertools.product((2, 3, 4), (.2, .4), (.025, .05, .1)):
        lowd, highc = d-e, c+3*e
        n = required_count(lowd, highc)
        stacks.append({'d': d, 'clearance': c, 'e': e, 'count': n,
                       'nominal_height': n*d, 'minimum_height': height(n, lowd, highc),
                       'aligned_high_height': n*(d+e),
                       'inventory': CELLS*n, 'bead_price_ceiling': 250/(CELLS*n)})
    timing = []
    n = required_count(3.95, .35)
    for heads, vmax, accel in itertools.product((80,160,320), (100,300), (1000,10000)):
        # Hypothetical reversible shuttle: four serial 4-mm rest-to-rest strokes.
        # Optimistic: no fork transfer, selector, sensing or feed dwell per particle.
        tau = 4*stroke_time(4, vmax, accel)
        mixed = [n if i%2 else -n for i in range(CELLS)]
        ncycles = cycles(mixed, heads, True)
        timing.append({'heads': heads, 'vmax': vmax, 'accel': accel,
                       'particle_cycle_s': tau, 'mixed_cycles': ncycles,
                       'mixed_map_s': 6+ncycles*tau,
                       'independent_direction_s': 6+cycles(mixed,heads,False)*tau,
                       'max_cycle_s_shared': 24/ncycles})
    continuous = []
    for heads in (80, 160, 320):
        batches = math.ceil(CELLS/heads)
        move = stroke_time(40, 300, 10000)
        continuous.append({'heads': heads, 'stroke_s': move,
                           'shared_direction_map_s': 6+2*batches*move,
                           'independent_direction_map_s': 6+batches*move,
                           'channel_price_ceiling': 250/heads})
    print(json.dumps({'checks': 'passed', 'fork_sections': sections,
                      'stacks': stacks, 'timing': timing, 'continuous': continuous}, indent=2))


if __name__ == '__main__':
    main()
