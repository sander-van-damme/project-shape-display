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

if __name__ == '__main__':
    main()
