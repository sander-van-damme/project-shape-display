"""Direction-dependent acceleration screen, mm/s; no calibrated drive model.
Common profile is enforced on empty and loaded moves. Analytic, deterministic.
"""
import json
from math import sqrt, isclose
from elevator_bound import move, solve, validate, PAIRS


def phases(distance, speed, positive, negative, direction):
    """Positive/negative are magnitudes of upward/downward acceleration."""
    assert distance >= 0 and min(speed, positive, negative) > 0
    assert direction in (-1, 1)
    accel, brake = (positive, negative) if direction == 1 else (negative, positive)
    peak = min(speed, sqrt(2 * distance / (1 / accel + 1 / brake)))
    cruise_distance = max(0, distance - peak**2 / (2 * accel) - peak**2 / (2 * brake))
    return ((peak / accel, direction * accel),
            (cruise_distance / peak if peak else 0, 0),
            (peak / brake, -direction * brake))


def replay(parts):
    """Integrate piecewise constant acceleration independently of distance formula."""
    x = v = 0
    for t, a in parts:
        x += v * t + .5 * a * t * t
        v += a * t
    return x, v


def main():
    # Zero, triangular, transition and long trapezoidal cases in both directions.
    for up, down in ((20000, 9810), (20000, 4905), (5000, 5000)):
        effective = 2 / (1 / up + 1 / down)
        crossover = 400**2 / effective
        for d in (0, .001, 10, 40, crossover, 1000):
            for sign in (-1, 1):
                p = phases(d, 400, up, down, sign)
                x, v = replay(p)
                assert isclose(x, sign * d, abs_tol=1e-9)
                assert abs(v) < 1e-9
                assert isclose(sum(t for t, _ in p), move(d, 400, effective), abs_tol=1e-12)
                assert all(-down <= a <= up for _, a in p)
    records = []
    for margin in (0, .25, .5, .75):
        up, down = 20000, 9810 * (1 - margin)
        effective = 2 / (1 / up + 1 / down)
        for pairs, workload in ((PAIRS, 'all_pairs'), (((0, 4),), 'uniform_up'), (((4, 0),), 'uniform_down')):
            for dwell in (0, .01, .02, .04):
                result = solve(pairs, 400, effective, dwell)
                validate(result['path_mm'], pairs)
                path = result['path_mm']
                duration = 0
                for a, b in zip(path, path[1:]):
                    p = phases(abs(b-a), 400, up, down, 1 if b>a else -1)
                    duration += sum(t for t, _ in p)
                    # Normal force per unit miniature weight, N/(mg).
                    assert min(1 + az/9810 for t, az in p if t) >= margin - 1e-12
                if dwell == 0:
                    assert isclose(duration, result['seconds'], abs_tol=1e-12)
                if workload == 'all_pairs':
                    assert path == [0,10,20,30,40,30,20,10,0]
                for heads in (80,160):
                    stations = 6400 // heads
                    index = max(.025, move(5.08 * heads / 80, 400, 20000))
                    seconds = 2 + stations * (result['seconds'] + index)
                    records.append(dict(normal_force_margin=margin, workload=workload,
                        heads=heads, dwell_ms=dwell*1000, full_map_s=seconds,
                        survives=seconds<30, path_mm=path))
    # The half-weight profile strictly rescues the former zero-dwell rejection.
    r = next(r for r in records if r['normal_force_margin']==.5 and
             r['workload']=='all_pairs' and r['heads']==160 and r['dwell_ms']==0)
    assert r['full_map_s'] < 30
    print(json.dumps({'records':records},indent=2))

if __name__ == '__main__':
    main()
