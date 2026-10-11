#!/usr/bin/env python3
"""Deterministic transport bounds; units mm, s. No hardware/process priors."""
import itertools
import json
import math

PITCH = 5.08
TRAVEL = 40.0


def move(d, v=300.0, a=5000.0):
    d = abs(d)
    return 2 * math.sqrt(d / a) if d <= v*v/a else d/v + v/a


def empty(d, scale=1.0):
    return move(d, 600*scale, 5000*scale)


def loaded(d, scale=1.0):
    return move(d, 300*scale, 5000*scale)


def direct(old, new, slot=.05, home=-4.0, scale=1.0):
    if old == new:
        return 0.0
    return empty(old-home, scale)+loaded(new-old, scale)+empty(new-home, scale)+2*slot


def continuous_worst(slot=.05, scale=1.0):
    """Analytical maxima for the stated scales; checked against finite search.

    Rest-to-rest t(d) is concave, with derivative 1/sqrt(a*d) until speed
    saturation, then 1/v. For direct, one endpoint is 40; optimize the other.
    For pair with one job in each half-cycle, empty flanks have equal length x.
    Both jobs in one half have at most five legs plus a 40-mm empty half.
    Jensen with all five legs charged as loaded gives an independent upper bound.
    """
    a, v = 5000*scale, 300*scale
    x = min(TRAVEL/3, v*v/a)
    paired = 2*(2*empty(x,scale)+loaded(TRAVEL-2*x,scale))+4*slot
    same_phase_upper = 5*loaded(TRAVEL/5,scale)+empty(TRAVEL,scale)+4*slot
    assert same_phase_upper <= paired+1e-12
    witness = ((TRAVEL-x,x),(TRAVEL-x,x))
    assert abs(pair(witness,slot,scale)[0]-paired) < 1e-10
    y = min(44/2, v*v/a)
    direct_max = empty(44,scale)+empty(y,scale)+loaded(44-y,scale)+2*slot
    assert abs(direct(40,y-4,slot,scale=scale)-direct_max) < 1e-10
    return {'direct_s':direct_max,'direct_witness':(40,y-4),
            'pair_s':paired,'pair_witness':witness,
            'same_phase_upper_s':same_phase_upper}


def pair(jobs, slot=.05, scale=1.0):
    """Two opposite carriages zA=q, zB=40-q; full q cycle 0->40->0.

    Each changed job selects its appropriate half-cycle. Stop at each actual
    acquire/release event; a disconnected carriage continues empty. Same-phase
    coincident events share a stop/slot but require independent local gates.
    Reversal boundary events are deliberately charged on BOTH adjacent phases;
    there is no unearned parallelization of support proof and next acquisition.
    """
    events = [{}, {}]
    heights = [j[0] for j in jobs]
    supported = [True, True]
    active = set()
    for i, (old, new) in enumerate(jobs):
        if old == new:
            continue
        phase = 0 if (new > old) == (i == 0) else 1
        for h, action in ((old, 'acquire'), (new, 'release')):
            q = h if i == 0 else TRAVEL-h
            events[phase].setdefault(q, []).append((i, action))
    if not any(events):
        return 0.0, 0, 0
    duration = 0.0
    stops = 0
    legs = 0
    for phase in (0, 1):
        ordered = sorted(set(events[phase]) | {0.0, TRAVEL}, reverse=bool(phase))
        prev = ordered[0]
        for q in ordered:
            distance = abs(q-prev)
            if distance:
                duration += loaded(distance, scale) if active else empty(distance, scale)
                legs += 1
                for i in active:
                    heights[i] = q if i == 0 else TRAVEL-q
            if q in events[phase]:
                duration += slot
                stops += 1
                for i, action in events[phase][q]:
                    if action == 'acquire':
                        assert supported[i] and i not in active
                        assert abs(heights[i]-(q if i == 0 else TRAVEL-q)) < 1e-9
                        # Grant verified capture before withdrawing ground support.
                        active.add(i)
                        supported[i] = False
                    else:
                        assert i in active and abs(heights[i]-jobs[i][1]) < 1e-9
                        # Grant proved ground seating BEFORE disconnecting carriage.
                        supported[i] = True
                        active.remove(i)
            assert all(supported[i] or i in active for i in (0, 1))
            prev = q
        assert not active
    assert all(abs(h-j[1]) < 1e-10 for h,j in zip(heights,jobs)) and all(supported)
    return duration, stops, legs


def bypass_worst(n, levels, slot=.05, home=-4.0, scale=1.0):
    """Exact worst closed itinerary over n changed sites in fixed row order.

    Grants an unbuilt height-preserving corridor, with all local gates within
    the same slot as direct. Max-plus DP; state is last target height.
    """
    states = {home: 0.0}
    for _ in range(n):
        states = {new: max(cost+empty(old-prev, scale)+loaded(new-old, scale)+2*slot
                           for prev, cost in states.items() for old in levels if old != new)
                  for new in levels}
    return max(cost+empty(new-home, scale) for new, cost in states.items())


def sequence_time(jobs, slot=.05, home=-4.0, scale=1.0):
    prev, t = home, 0.0
    for old, new in jobs:
        if old != new:
            t += empty(old-prev, scale)+loaded(new-old, scale)+2*slot
            prev = new
    return t+empty(prev-home, scale)


def bypass_bank(n, slot=.05, scale=1.0):
    # Shared row barriers can have DIFFERENT critical columns. First acquisition
    # <=44, later acquisitions <=40, loaded strokes <=40, final return <=44.
    # Two columns attain all bounds: repeat 40->0 on one, 0->40 on the other.
    return (2*empty(44,scale)+(n-1)*empty(40,scale)
            +n*(loaded(40,scale)+2*slot))


def parallel_sequence(lanes, slot=.05):
    prev = [-4.]*len(lanes)
    t = 0.
    for row in zip(*lanes):
        t += max(empty(old-p)+loaded(new-old)+2*slot
                 for p,(old,new) in zip(prev,row))
        prev = [new for old,new in row]
    return t+max(empty(p+4) for p in prev)


def banks(service, capacity, slot_overhead=6.0, scale=1.0, clearance_drop=0.0):
    # 80 simultaneous x columns; capacity=1 or 2 neighboring y rows/transaction.
    # One common y carriage per bank. Return-to-start included for sustained maps.
    for b in range(1, 81):
        nrows = math.ceil(80/b)
        visits = math.ceil(nrows/capacity)
        distance = capacity*PITCH
        scan = (visits-1)*empty(distance, scale)+empty((visits-1)*distance, scale)
        # Both carriages must clear every foot before indexing. A shared bank
        # z axis lowers after withdrawal, then restores after addressing. Its
        # assumed motion uses loaded limits although carried bank inertia and
        # stiffness are UNQUALIFIED. Final return-to-start pays the same route.
        if visits > 1:
            scan += visits*2*loaded(clearance_drop, scale)
        t = slot_overhead+visits*service+scan
        if t < 30:
            return {'banks': b, 'motors': 80*b, 'carriages': capacity*80*b,
                    'seconds': t, 'complete_motor_branch_allowance': 250/(80*b)}
    raise AssertionError('No schedule')


def box_overlap(a, b):
    return math.prod(max(0.0, min(a[1][k], b[1][k])-max(a[0][k], b[0][k])) for k in range(3))


def geometry():
    # Generated solid foot and a moving solid compact shoe spine. Independent
    # height pairs can place them at equal z, so a planar obstruction is real.
    foot = ((-1., -PITCH-1.4, 0.), (1., -PITCH+1.4, 1.2))
    shoe = ((-2., -2.25, 0.), (2., -1.65, 1.2))
    # E-123's .965-mm y withdrawal followed by -one-pitch row translation.
    # Its continuous [-.965,-6.045] sweep contains y offset -3.08 mm.
    moved = tuple(tuple(p[k]+(-3.08 if k == 1 else 0.) for k in range(3)) for p in shoe)
    witness = box_overlap(foot, moved)
    assert abs(witness-1.44) < 1e-12
    # To follow the declared Manhattan half-pitch corridor around rectangular
    # feet, an axis-aligned solid retracted package must fit BOTH gaps.
    # e comprises independent center +/-e and face +/-e, relative closure 4e.
    out = []
    for e, pose in itertools.product((0., .025, .05, .1, .2), (0., .05, .15)):
        out.append({'e_mm': e, 'additional_relative_pose_mm': pose,
                    'max_retracted_width_x_mm': PITCH-2.-4*e-pose-.025,
                    'max_retracted_depth_y_mm': PITCH-2.8-4*e-pose-.025})
    return {'shoe_spine_crossing_mm3': witness, 'corridor_limits': out}


def checks():
    assert move(0) == 0 and abs(move(18)-.12) < 1e-12
    assert abs(move(72)-.30) < 1e-12
    # Independent trapezoid integration and both limiting regimes.
    for d in (1., 18., 40., 72.):
        t = move(d)
        vp = min(300., math.sqrt(d*5000.))
        assert abs(vp*(t-vp/5000.)-d) < 1e-10
    small = (0., 20., 40.)
    jobs = [(a,b) for a in small for b in small if a != b]
    for n in (1,2,3):
        brute = max(sequence_time(s) for s in itertools.product(jobs, repeat=n))
        assert abs(brute-bypass_worst(n,small)) < 1e-10
    # All 9^4 states include unchanged cells, opposite signs and equal events.
    count = 0
    for h in itertools.product(range(0,41,5), repeat=4):
        pair((h[:2],h[2:]))
        count += 1
    # Coincident endpoints: four independently verified transfer slots, not two.
    t, stops, _ = pair(((0,40),(0,40)))
    assert stops == 4 and abs(t-(2*loaded(40)+.2)) < 1e-12
    assert pair(((20,20),(0,0)))[0] == 0
    for n in (1,2,3,80):
        witness = parallel_sequence([[(40,0)]*n,[(0,40)]*n])
        assert abs(witness-bypass_bank(n)) < 1e-10
    geometry()
    return {'pair_state_cases': count, 'dp_bruteforce_lengths': [1,2,3]}


def run():
    levels = list(range(0,41,5))
    jobs = [(a,b) for a in levels for b in levels if a != b]
    results = []
    for scale, slot in itertools.product((.5,1.,2.), (.02,.05,.1)):
        wd = max((direct(a,b,slot,scale=scale),(a,b)) for a,b in jobs)
        wp = max((pair((a,b),slot,scale)[0],(a,b)) for a,b in itertools.product(jobs,repeat=2))
        analytical = continuous_worst(slot,scale)
        assert wd[0] <= analytical['direct_s']+1e-10
        assert wp[0] <= analytical['pair_s']+1e-10
        bd = banks(analytical['direct_s'],1,scale=scale)
        bp = banks(analytical['pair_s'],2,scale=scale)
        bp_clear = banks(analytical['pair_s'],2,scale=scale,clearance_drop=44.)
        bb = None
        for b in range(1,81):
            n = math.ceil(80/b)
            t = 6+bypass_bank(n,slot,scale=scale)+(n-1)*empty(PITCH,scale)+empty((n-1)*PITCH,scale)
            if t < 30:
                bb = {'banks':b,'motors':80*b,'seconds':t}
                break
        results.append({'scale':scale,'transfer_slot_s':slot,'direct_worst':wd,
                        'pair_worst':wp,'continuous_maxima':analytical,
                        'direct':bd,'pair_free_corridor':bp,
                        'pair_shared_clearance_axis':bp_clear,'ideal_bypass':bb})
    # Workload transparency: a full 80-row lane, serial acquisition/release slots.
    workloads = {'all_up':[(0,40)]*80, 'all_down':[(40,0)]*80,
                 'alternating':[(0,40),(40,0)]*40,
                 'small_raise':[(20,25)]*80}
    wt = {}
    for name, js in workloads.items():
        wt[name] = {'home_vertical_s':sum(direct(*j) for j in js),
                    'bypass_vertical_s':sequence_time(js),
                    'pair_vertical_s':sum(pair(js[k:k+2])[0] for k in range(0,80,2))}
    # Head geometry/retraction still must be built: this is refinement of scalar
    # event-grid search, not convergence of a contact or dynamic solver.
    fine = {}
    for step in (10,5,2,1):
        js = [(a,b) for a in range(0,41,step) for b in range(0,41,step) if a!=b]
        if step >= 2:
            worst = max((pair((a,b))[0],(a,b)) for a,b in itertools.product(js,repeat=2))
            fine[step] = worst
        else:
            # Holdout around the prior maximizer plus every boundary combination.
            center = fine[2][1]
            vals = [sorted(set([0,40]+[v for v in range(max(0,h-2),min(40,h+2)+1)]))
                    for j in center for h in j]
            fine[step] = max((pair((h[:2],h[2:]))[0],(h[:2],h[2:]))
                             for h in itertools.product(*vals) if h[0]!=h[1] and h[2]!=h[3])
    return {'checks':checks(),'geometry':geometry(),'scenarios':results,
            'workload_vertical_only':wt,'pair_event_grid_refinement':fine,
            'bypass_worst_vertical_80_s':bypass_worst(80,levels),
            'bypass_bank_worst_vertical_80_s':bypass_bank(80),
            'local_5_rows_pair_jobs_s':sum(pair(j)[0] for j in
                 [((20,25),(20,25)),((20,25),(20,25)),((20,25),(20,20))])}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
