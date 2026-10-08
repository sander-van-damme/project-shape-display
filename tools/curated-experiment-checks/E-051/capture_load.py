"""Exact capture-choice enumeration on E-051's fixed sweep; SI force units.
Uncalibrated mass bounds; no contact, drive sizing, or hardware validation.
"""
import itertools
import json

from elevator_bound import move, solve, PAIRS as INDEX_PAIRS

PATH = (0, 10, 20, 30, 40, 30, 20, 10, 0)  # mm
PAIRS = tuple(itertools.permutations((0, 10, 20, 30, 40), 2))


def intervals(old, new):
    # Releasing later than the first target visit only adds attached segments.
    return tuple((i, next(j for j in range(i + 1, len(PATH)) if PATH[j] == new))
                 for i, z in enumerate(PATH)
                 if z == old and new in PATH[i + 1:])


def profile(choices):
    return tuple(sum(i <= k < j for i, j in choices) for k in range(len(PATH) - 1))


def travel(choices):
    return sum(abs(PATH[k + 1] - PATH[k]) for i, j in choices for k in range(i, j))


def main():
    options = [intervals(*p) for p in PAIRS]
    choices = list(itertools.product(*options))
    early = tuple(o[0] for o in options)
    delayed = tuple(o[-1] for o in options)
    low = profile(delayed)
    # Exhaustive componentwise dominance, stronger than minimum scalar load.
    assert all(all(a <= b for a, b in zip(low, profile(c))) for c in choices)
    direct = sum(abs(new - old) for old, new in PAIRS)
    assert travel(delayed) == direct
    for c in choices:
        signed = sum(PATH[j] - PATH[i] for i, j in c)
        assert signed == sum(new - old for old, new in PAIRS) == 0
        for (old, new), (i, j) in zip(PAIRS, c):
            assert PATH[i] == old and PATH[j] == new and i < j
    # Independent cut count: upward pairs crossing each of four level gaps.
    assert low[:4] == tuple((k + 1) * (4 - k) for k in range(4))
    assert low[4:] == low[:4][::-1]
    scenarios = []
    for n in (80, 160):
        for mass_g in (5, 20, 50):
            for name, c in [('early', early), ('delayed', delayed)]:
                peak = max(profile(c)) * (n // 20)
                mass = peak * mass_g / 1000
                scenarios.append(dict(heads=n, policy=name, mass_per_column_g=mass_g,
                    peak_attached=peak, peak_column_mass_kg=mass,
                    column_force_envelope_N=mass * (9.81 + 20),
                    absolute_column_travel_m=travel(c) * (n // 20) / 1000))
    # Uniform full-height change attaches every head, unlike all-pairs maps.
    assert max(profile([intervals(0, 40)[0]] * 160)) == 160
    timing = []
    for a in (20000, 9810, 4905):  # mm/s^2; g is a zero-normal-force limit
        optimum = solve(INDEX_PAIRS, 400, a, 0)
        assert abs(optimum["seconds"] - 8 * move(10, 400, a)) < 1e-12
        base = 2 + 40 * (optimum["seconds"] + max(.025, move(10.16, 400, 20000)))
        timing.append(dict(acceleration_mm_s2=a, zero_dwell_160_s=base,
                           event_dwell_ceiling_ms=(30 - base) / 360 * 1000))
    print(json.dumps(dict(timing=timing, capture_assignments=len(choices),
        early_per_20=profile(early), delayed_per_20=low,
        early_travel_mm_per_20=travel(early), delayed_travel_mm_per_20=direct,
        scenarios=scenarios), indent=2))


if __name__ == '__main__':
    main()
