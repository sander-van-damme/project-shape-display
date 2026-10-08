"""Optimistic rest-to-rest pawl stroke bound; mm, s; bounded scenarios only."""
import json
from math import sqrt, isclose
from elevator_bound import move, solve, PAIRS, validate
from asymmetric_motion import phases, replay


def main():
    stroke = 1.22  # E-052 middle-bound witness, not universal architecture minimum
    rows = []
    for margin in (None, .5):
        vertical = 20000 if margin is None else 2 / (1/20000 + 1/4905)
        index = max(.025, move(10.16, 400, 20000))
        zero = solve(PAIRS, 400, vertical, 0)
        baseline = 2 + 40*(zero['seconds'] + index)
        allowance = (30-baseline)/360
        for acceleration in (5000, 20000, 50000, 100000):
            dwell = move(stroke, 400, acceleration)
            # Independent integration and speed-unlimited triangular lower bound.
            x, v = replay(phases(stroke, 400, acceleration, acceleration, 1))
            assert isclose(x, stroke, abs_tol=1e-12) and abs(v)<1e-9
            assert dwell >= 2*sqrt(stroke/acceleration)-1e-12
            result = solve(PAIRS, 400, vertical, dwell)
            validate(result['path_mm'], PAIRS)
            assert result['path_mm'] == [0,10,20,30,40,30,20,10,0]
            total = 2+40*(result['seconds']+index)
            assert isclose(total, baseline+360*dwell, abs_tol=1e-9)
            rows.append(dict(margin=margin, lateral_accel_mm_s2=acceleration,
                stroke_ms=1000*dwell, map_s=total, survives=total<30))
        print(json.dumps(dict(margin=margin, baseline_s=baseline,
            dwell_ceiling_ms=1000*allowance,
            necessary_lateral_accel_mm_s2=4*stroke/allowance**2,
            max_stroke_at_20000_mm=20000*(allowance/2)**2)))
    assert all(r['map_s']>=30 for r in rows if r['margin']==.5 and r['lateral_accel_mm_s2']<=50000)
    print(json.dumps(rows, indent=2))


def serial_paths():
    """Two explicit rest-to-rest paths, plus an optimistic branch relaxation.

    Seat cycle: arrive at z; grip outgoing; lift h; insert incoming pawls and
    withdraw outgoing pawls concurrently; lower h; release incoming grippers.
    Clearance cycle: arrive at z+h; insert incoming; lower h; release/grip;
    lift h; withdraw outgoing; depart. Initial/final stops have one branch.
    Neither path overlaps microtravel with the 10-mm inter-level moves.
    """
    from capture_load import PATH, PAIRS as HEIGHT_PAIRS, intervals
    h, stroke = .47, 1.22
    choices = [intervals(*pair)[-1] for pair in HEIGHT_PAIRS]
    captures = [any(i == k for i, j in choices) for k in range(9)]
    deposits = [any(j == k for i, j in choices) for k in range(9)]
    assert captures == [True]*8 + [False]
    assert deposits == [False] + [True]*8
    records = []
    for down in (20000, 4905):
        effective = 2/(1/20000 + 1/down)
        u = move(h, 400, effective)
        for direction in (-1, 1):
            p = phases(h, 400, 20000, down, direction)
            x, velocity = replay(p)
            assert isclose(x, direction*h, abs_tol=1e-12)
            assert abs(velocity) < 1e-9
            assert isclose(sum(t for t, a in p), u, abs_tol=1e-12)
        base = 2 + 40*(8*move(10, 400, effective) + max(.025, move(10.16, 400, 20000)))
        allowance = (30-base)/360
        # Even infinitely fast lateral travel cannot rescue this relaxation
        # when one additional vertical branch already exceeds the allowance.
        residual = allowance-u
        required = 4*stroke/residual**2 if residual > 0 else None
        print(json.dumps(dict(serial_down_mm_s2=down, vertical_leg_ms=u*1000,
            branch_lateral_accel_floor_mm_s2=required,
            infinite_lateral_branch_map_s=base+360*u,
            max_extra_vertical_leg_mm=effective*(allowance/2)**2)))
        for a in (5000, 20000, 50000, 100000):
            lateral = move(stroke, 400, a)
            # Independent event-list replay checks vertical displacement,
            # inter-level distance, endpoint closure, and operation counts.
            for name in ('seat_cycle', 'clearance_cycle'):
                height = 0.
                vertical_distance = lateral_count = duration = 0.
                for k, z in enumerate(PATH):
                    arrival = z if name == 'seat_cycle' or k == 0 else z+h
                    d = abs(arrival-height)
                    if k:
                        assert isclose(d, 10., abs_tol=1e-12)
                    duration += move(d, 400, effective)
                    if name == 'seat_cycle':
                        legs, strokes, height = 2, 1, z
                    else:
                        legs = strokes = int(captures[k])+int(deposits[k])
                        height = z+h if captures[k] else z
                    vertical_distance += legs*h
                    lateral_count += strokes
                    duration += legs*u + strokes*lateral
                assert height == 0
                count = 9 if name == 'seat_cycle' else 16
                legs = 18 if name == 'seat_cycle' else 16
                assert lateral_count == count
                assert isclose(vertical_distance, legs*h, abs_tol=1e-12)
                total = 2+40*(duration+max(.025, move(10.16, 400, 20000)))
                assert isclose(total, base+40*(legs*u+count*lateral), abs_tol=1e-10)
                lateral_budget = ((30-base)/40-legs*u)/count
                records.append(dict(down_mm_s2=down, lateral_mm_s2=a, path=name,
                    map_s=total, survives=total<30,
                    remaining_ms_per_stop=(30-total)/360*1000,
                    lateral_accel_floor_mm_s2=(4*stroke/lateral_budget**2
                        if lateral_budget > 0 else None)))
            relaxed = base+360*(u+lateral)
            assert relaxed <= min(r['map_s'] for r in records[-2:])
            records.append(dict(down_mm_s2=down, lateral_mm_s2=a,
                path='one_branch_relaxation', map_s=relaxed, survives=relaxed<30))
    assert all(not r['survives'] for r in records if r['down_mm_s2']==4905)
    print(json.dumps(records, indent=2))


if __name__ == '__main__':
    main()
    serial_paths()
