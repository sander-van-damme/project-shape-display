#!/usr/bin/env python3
"""E-172: finite crossbolt/ladder section, bounded transfer and schedule.
Units mm, N, s. Standard library. No process distribution or hardware claims.
"""
import itertools as it
import json
import math

PITCH = 5.08
STEP = 10.1
HALF_KEY = 1.7
SHIFT = .7
INNER = 1.4
OUTER = 2.3
KEY_T = .8
FLOOR_T = 1.
BREADTH = 1.6
EPS = 1e-9


def overlap(a, b):
    return max(0., min(a[1], b[1]) - max(a[0], b[0]))


def volume(a, b):
    return math.prod(overlap(x, y) for x, y in zip(a, b))


def key(q, z):
    return ((q-HALF_KEY, q+HALF_KEY), (-.8, .8), (z, z+KEY_T))


def floors(g, c, d):
    # Prisms are actual isolated shelf solids, NOT complete connected racks.
    return [((x0, x1), (-.8, .8), (j*STEP+e+dz-FLOOR_T, j*STEP+e+dz))
            for x0, x1, errors, dz in ((-OUTER, -INNER, g, 0),
                                       (INNER, OUTER, c, d))
            for j, e in enumerate(errors)]


def check_pose(q, z, d, g, c):
    body = key(q, z)
    supports = []
    for floor in floors(g, c, d):
        assert volume(body, floor) < EPS, (q, z, d, body, floor)
        if abs(z-floor[2][1]) < EPS:
            area = overlap(body[0], floor[0])*overlap(body[1], floor[1])
            if area > EPS:
                supports.append(area)
    assert supports, (q, z, d)
    # Any positive downward load has nonnegative vertical support reactions.
    # Grounded prismatic guides must supply moments; they are NOT built here.
    for force in (.1, 1., 10.):
        reactions = [force*a/sum(supports) for a in supports]
        assert min(reactions) > 0 and abs(sum(reactions)-force) < EPS
    return min(supports)


def route(old, new, g, c, e, subdivisions=1):
    a = 2*e+.1
    delta = (new-old)*STEP
    go, gn, co = old*STEP+g[old], new*STEP+g[new], old*STEP+c[old]
    # Each tuple: q endpoints, deck endpoints, exact unilateral support law.
    legs = [(-SHIFT, 0, -a, -a, lambda d: go),
            (0, 0, -a, a, lambda d: max(go, co+d)),
            (0, SHIFT, a, a, lambda d: co+d),
            (SHIFT, SHIFT, a, delta+a, lambda d: co+d),
            (SHIFT, 0, delta+a, delta+a, lambda d: co+d),
            (0, 0, delta+a, delta-a, lambda d: max(gn, co+d)),
            (0, -SHIFT, delta-a, delta-a, lambda d: gn),
            (-SHIFT, -SHIFT, delta-a, -a, lambda d: gn)]
    count, minimum = 0, float('inf')
    for q0, q1, d0, d1, height in legs:
        ts = {i/subdivisions for i in range(subdivisions+1)}
        # Every possible overlap/support/vertical intersection event is included.
        if q0 != q1:
            for edge in (-OUTER, -INNER, INNER, OUTER):
                for s in (-HALF_KEY, HALF_KEY):
                    t = (edge-s-q0)/(q1-q0)
                    if 0 < t < 1:
                        ts.add(t)
        if d0 != d1:
            for ground in (go, gn):
                t = (ground-co-d0)/(d1-d0)
                if 0 < t < 1:
                    ts.add(t)
        # Midpoints discriminate contact intervals, not just endpoint touching.
        ordered = sorted(ts)
        ts.update((x+y)/2 for x, y in zip(ordered, ordered[1:]))
        for t in sorted(ts):
            q, d = q0+(q1-q0)*t, d0+(d1-d0)*t
            minimum = min(minimum, check_pose(q, height(d), d, g, c))
            count += 1
    assert abs(gn-go - ((new-old)*STEP+g[new]-g[old])) < EPS
    return count, minimum


def horizontal(e):
    # Independent key translation, key edge error, rail inner-edge error.
    # Exhaustive corners; overlap/off-clearance are piecewise affine here.
    bridge, off = [], []
    for x, size, edge in it.product((-e, e), repeat=3):
        bridge.append(overlap((-HALF_KEY+x-size, HALF_KEY+x+size),
                              (INNER+edge, OUTER)))
        off.append((INNER+edge)-(-SHIFT+HALF_KEY+x+size))
    return dict(e=e, min_bridge_mm=min(bridge), min_off_mm=min(off),
                adjacent_key_gap_mm=PITCH-2*(HALF_KEY+SHIFT)-4*e,
                adjacent_floor_gap_mm=PITCH-2*OUTER-4*e,
                min_endpoint_span_mm=4*STEP-2*e)


def move(d, v=200., acc=5000.):
    d = abs(d)
    return 2*math.sqrt(d/acc) if d <= v*v/acc else d/v+v/acc


def schedule(banks, slot=.1, v=200., acc=5000., overhead=2., e=.05):
    """Constructive independent signed-displacement groups, not optimum."""
    n = 80//banks
    a = 2*e+.1
    # Eight groups; four full serpentine scans each. Even scans finish at home.
    # slot includes approach/set/retention/readback/withdrawal of 80 channels.
    scans = 32
    write = scans*n*slot
    index = scans*(n-1)*move(PITCH, v, acc)
    lift = sum(2*move(2*a, v, acc)+2*move(k*STEP, v, acc)
               for k in range(1, 5) for sign in (-1, 1))
    proof = 16*.1
    # One failed slot repeat + supported .4-mm reseat in each parallel bank.
    retry = slot+2*move(2*a, v, acc)+.1
    return dict(banks=banks, seconds=overhead+write+index+lift+proof+retry,
                slots=scans*n, lift_s=lift, channels=82*banks,
                ceiling_free_sites=(500-250)/(82*banks),
                ceiling_2cent_sites=(500-250-6400*.02)/(82*banks))


def reachability():
    # Any map is the union of these disjoint difference groups. Verify all
    # two-cell old/new assignments, including identity and opposite signs.
    maps = 0
    for old in it.product(range(5), repeat=2):
        for targets in it.product(range(5), repeat=2):
            current = list(old)
            for delta in (-4, -3, -2, -1, 1, 2, 3, 4):
                for i in range(2):
                    if targets[i]-old[i] == delta:
                        current[i] += delta
            assert tuple(current) == targets
            maps += 1
    return maps


def main():
    assert volume(((0, 1),)*3, ((1, 2),)*3) == 0
    assert abs(volume(((0, 1),)*3, ((.5, 1.5),)*3)-.125) < EPS
    pairs = [(o, n) for o in range(5) for n in range(5) if o != n]
    states, routes, bearing = 0, 0, float('inf')
    e = .05
    # All 2^10 support-height corners, including common and alternating biases.
    # Floor heights are affine; inequality margins below cover the interiors.
    for errors in it.product((-e, e), repeat=10):
        for old, new in pairs:
            count, area = route(old, new, errors[:5], errors[5:], e)
            routes += 1
            states += count
            bearing = min(bearing, area)
    holdouts = []
    for subdivisions in (4, 16, 64):
        count = 0
        for old, new in pairs:
            # Interior, nonsymmetric dimensions; not just sign-corner replay.
            g = (.01, -.023, .042, -.037, .016)
            c = (-.032, .011, -.015, .043, -.049)
            count += route(old, new, g, c, e, subdivisions)[0]
        holdouts.append(dict(subdivisions=subdivisions, states=count))
    # The zero-prelift one-shot handoff fails either sign of a height mismatch.
    floor = floors((0,)*5, (.05,)*5, 0)[5]
    penetration = volume(key(0, 0), floor)
    assert abs(penetration-.024) < EPS
    # Negative mismatch gives .05-mm loss of contact after ground disengagement.
    assert overlap(key(SHIFT, 0)[0], floors((0,)*5, (0,)*5, 0)[0][0]) == 0
    below = floors((0,)*5, (-.05,)*5, 0)[5]
    assert abs(key(SHIFT, 0)[2][0]-below[2][1]-.05) < EPS
    assert overlap(key(SHIFT, 0)[0], below[0]) > 0
    # A missed full carrier setting leaves the key at bridge; next fixed shelf
    # is a finite obstacle. No convenient state-bit assertion replaces geometry.
    jam = volume(key(0, 9.5), floors((0,)*5, (0,)*5, 9.5)[1])
    assert jam > 0
    # Wrong bridge selection lifts an unchanged column .5 mm at deck d=.5.
    check_pose(0, .5, .5, (0,)*5, (0,)*5)
    # Full return isolation: ground-selected key never reaches any carrier
    # shelf at any z; x-disjointness proves continuous sweep, even absent bays.
    assert -SHIFT+HALF_KEY < INNER
    horizontal_results = [horizontal(x) for x in (0, .025, .05, .075, .1)]
    # Attainable neighboring solids, not only a conservative envelope failure.
    err = .075
    left = ((SHIFT-HALF_KEY, SHIFT+HALF_KEY+2*err), (-.8, .8), (0, KEY_T))
    right = ((PITCH-SHIFT-HALF_KEY-2*err, PITCH-SHIFT+HALF_KEY),
             (-.8, .8), (0, KEY_T))
    neighbor_collision = volume(left, right)
    assert abs(neighbor_collision-.0256) < EPS
    for h in horizontal_results:
        assert abs(h['min_bridge_mm'] - max(0., .3-3*h['e'])) < EPS
        assert abs(h['min_off_mm'] - (.4-3*h['e'])) < EPS
    # Independent continuous vertical bounds, allowing both face growth and
    # floor height error: a chosen .1 reserve remains after worst-case datums.
    a = 2*e+.1
    assert a-2*e > 0
    upper_gap = STEP-2*e-(FLOOR_T+e)-(KEY_T+e)-(a+2*e)
    assert upper_gap > 0
    assert reachability() == 625
    times = [schedule(b) for b in (1, 2, 4, 8, 16)]
    # Motion limiting case and an independent hand sum for n=5.
    assert move(0) == 0
    assert abs(move(40.4)-(.202+.04)) < EPS
    assert abs(times[-1]['seconds']-(2+160*.1+128*move(PITCH)+
               times[-1]['lift_s']+1.6+.1+2*move(.4)+.1)) < EPS
    print(json.dumps(dict(routes=routes, checked_states=states,
        holdouts=holdouts, nominal_min_contact_area_mm2=bearing,
        horizontal_bounds=horizontal_results,
        bridge_worst_case_mean_pressure_MPa={str(f):f/(.15*(BREADTH-2*e))
                                            for f in (.1, 1, 10)},
        upper_clearance_bound_mm=upper_gap,
        direct_handoff_collision_mm3=penetration, missed_shift_jam_mm3=jam,
        adverse_neighbor_collision_mm3=neighbor_collision,
        map_reachability_cases=625, schedules=times,
        sensitivity=[dict(slot=s, first_passing_banks=next(
            (b for b in (1, 2, 4, 8, 16) if schedule(b, s, v, acc)['seconds']<30), None),
            v=v, acc=acc) for v, acc in ((80,1000), (200,5000), (400,20000))
            for s in (.02,.05,.1,.2)],
        cell_ladders=6400*2, shelf_sites=6400*2*5,
        shared_ladder_swept_height_mm=12*STEP+2*a+FLOOR_T,
        minimum_free_carrier_gravity_force_N={str(w):6400/16*w for w in (.1,1,10)},
        assumptions='Ideal grounded key/column guides and retained three-state selector; '
                    'shared carrier brake required but not implemented; quasistatic only.'), indent=2))


if __name__ == '__main__':
    main()
