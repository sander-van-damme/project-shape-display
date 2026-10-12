#!/usr/bin/env python3
"""Finite interlevel-turn spacing screen. mm; error budgets are scenarios.

Extends E-167, not a new gate design. Uses original convex SAT independently
of the axial interval calculation. No probability or manufactured-fit claim.
"""
import json
import math
from probe import P, rectangle, intersect, gate


def window(step, cap=2.0, cap_error=0.0, gate_error=0.0,
           lug=1.2, base=1.2, pocket=.4):
    lo = max(cap + cap_error, pocket + gate_error)
    hi = step - max(cap + cap_error, lug + base + gate_error)
    return lo, hi, hi - lo


def overlap(a, b):
    return min(a[1], b[1]) - max(a[0], b[0]) > 1e-10


def finite_hits(step, lift, angle, error=0.0):
    """One coherent adverse realization of the two gap budgets.

Active cap bottom is lift. Lower neighbor top is 2+error; upper neighbor
bottom is step-error. Fixed base is thickened downward by error. These
independent dimensions can share batch bias; no IID interpretation is used.
Gate/lug XY is exactly the original E-167 geometry (itself unqualified).
"""
    cap = rectangle(2.4, 2.4, angle)
    neighbors = [(rectangle(2.4, 2.4, dx=P), (0., 2.+error)),
                 (rectangle(2.4, 2.4, dx=-P), (step-error, step+2.))]
    cap_hits = sum(intersect(cap, p) and overlap((lift, lift+2), z)
                   for p, z in neighbors)
    solids = [(p, z0-error if z0 < 0 else z0, z1)
              for p, z0, z1 in gate()]
    lug = rectangle(2., .45, angle)
    # Selected lug and the station immediately below it, at an interior height.
    gate_hits = sum(intersect(lug, p) and overlap((z, z+1.2), (z0, z1))
                    for z in (lift, lift-step) for p, z0, z1 in solids)
    return cap_hits, gate_hits


def travel(distance, speed, acceleration):
    return (2*math.sqrt(distance/acceleration) if distance <= speed**2/acceleration
            else distance/speed + speed/acceleration)


def service_bound(lift):
    # Same optimistic allowances as E-167; omits transport/conflict routing.
    service = travel(40, 300, 3000) + 2*travel(lift, 300, 3000)
    service += 2*travel(90, 720, 7200) + .05
    heads = next(h for h in range(1, 6401) if 6+math.ceil(6400/h)*service < 30)
    return dict(service_s=service, independent_output_pairs=heads,
                optimistic_map_s=6+math.ceil(6400/heads)*service,
                dollars_per_pair_after_295_reserve=205/heads)


def main():
    # Analytical projection and exact SAT agree that 45-degree caps overlap
    # both unchanged lateral neighbors. Smaller caps are an explicit escape.
    for d in (4.0, 4.8):
        actual = intersect(rectangle(d/2, d/2, math.pi/4),
                           rectangle(d/2, d/2, dx=P))
        assert actual == (d/math.sqrt(2) + d/2 > P)
    table = []
    for step in (10., 5., 2.5):
        for error in (0., .15, .35, .70):
            lo, hi, width = window(step, cap_error=error, gate_error=error)
            table.append(dict(step=step, levels=round(40/step)+1,
                              gap_error=error, lower=lo, upper=hi, width=width,
                              board_lug_stations=6400*(round(40/step)+1)))
            # The interval is exact for the stated axial separating bounds.
            for n in (16, 64, 256):
                for k in range(n+1):
                    lift = step*k/n
                    cap_clear = lift > 2+error and lift < step-2-error
                    gate_clear = lift > .4+error and lift < step-2.4-error
                    assert (lo < lift < hi) == (cap_clear and gate_clear)
            if width > 0:
                # Reduced cap + own-gate solids are clear through whole turn.
                # Does not include remote lugs, guides, active neighbors or head.
                lift = (lo+hi)/2
                for n in (16, 64, 256):
                    assert all(finite_hits(step, lift, math.pi/2*k/n, error)==(0, 0)
                               for k in range(n+1))
    # Independent finite witness: 9 levels at 5 mm, .35-mm gap bounds.
    # At L=2.3, both lower neighbor cap and next-lower lug penetrate by .05 mm.
    assert finite_hits(5, 2.3, math.pi/4, .35)[0] > 0
    assert finite_hits(5, 2.3, math.pi/4, .35)[1] > 0
    assert all(sum(finite_hits(5, 5*k/2000, math.pi/4, .35)) > 0
               for k in range(2001))
    # Holdouts: gate separation starts failing at 2.25; cap clears only at 2.35.
    assert finite_hits(5, 2.25-1e-6, math.pi/4, .35)[1] == 0
    assert finite_hits(5, 2.25+1e-6, math.pi/4, .35)[1] > 0
    assert finite_hits(5, 2.35-1e-6, math.pi/4, .35)[0] > 0
    assert finite_hits(5, 2.35+1e-6, math.pi/4, .35)[0] == 0
    # Nominal 5-mm case exists; zero nominal collisions is not robust evidence.
    assert finite_hits(5, 2.3, math.pi/4, 0) == (0, 0)
    print(json.dumps(dict(spacing_table=table,
        witness=dict(step=5, lift=2.3, error=.35, cap_penetration=.05,
                     lower_lug_penetration=.05, sampled_midturn_heights=2001),
        sensitivity_min_step=[dict(cap=t, gap_error=e,
                    strict_step_above=max(t+e,.4+e)+max(t+e,2.4+e))
                    for t in (1.,2.,3.) for e in (0.,.15,.35,.70)],
        direct_head_oracle=service_bound(2.3)), indent=2))


if __name__ == '__main__':
    main()
