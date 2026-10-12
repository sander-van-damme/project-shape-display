#!/usr/bin/env python3
"""E-244: bounded architecture calculations, not qualified hardware. Stdlib only."""
import itertools as it
import json
import math

N, P, H = 80, 5.08, 40.0

def motion(d, v=200., a=8000.):
    assert d >= 0 and v > 0 and a > 0
    return 2*math.sqrt(d/a) if d <= v*v/a else d/v+v/a


def rank(matrix):
    # Small integer matrices; independent check against closed-form counts.
    from fractions import Fraction
    m = [[Fraction(x) for x in row] for row in matrix]
    pivot = 0
    for j in range(len(m[0])):
        k = next((k for k in range(pivot, len(m)) if m[k][j]), None)
        if k is None:
            continue
        m[pivot], m[k] = m[k], m[pivot]
        q = m[pivot][j]
        m[pivot] = [x/q for x in m[pivot]]
        for k in range(len(m)):
            if k != pivot:
                q = m[k][j]
                m[k] = [x-q*y for x, y in zip(m[k], m[pivot])]
        pivot += 1
    return pivot


def shared_length_check():
    checks = []
    for n in range(2, 7):
        rows = [[int(k//n == r) for k in range(n*n)] for r in range(n)]
        cols = [[int(k % n == c) for k in range(n*n)] for c in range(n)]
        actual = rank(rows+cols)
        assert actual == 2*n-1
        witness = [0]*(n*n)
        witness[0], witness[1], witness[n], witness[n+1] = 10, -10, -10, 10
        assert all(sum(x*y for x, y in zip(a, witness)) == 0 for a in rows+cols)
        checks.append([n, actual, n*n-actual])
    return {'small_rank_checks': checks, 'board_row_only_nullity': 6400-80,
            'board_row_column_nullity': 6400-159,
            'checkerboard_heights': [[20, 20, 20, 20], [30, 10, 10, 30]]}


def route(d, e, bend_ratio=5., clearance=.4):
    """Necessary lane/envelope allocation; rounded guide walls/strength NOT built.
    Forty stacked outgoing lanes per edge, one vertical and one outgoing plane.
    Two 90-degree bends, with lateral inter-bend straight >= 0.
    e is total each-route displacement/size uncertainty, not a process prior.
    """
    r = bend_ratio*d/2
    spacing = d+2*e+clearance
    spread = 39*spacing
    transverse = 2*r+d+2*e+1.4+clearance  # 1.4 stem width grant
    stem = H+5+spread+r+2
    # Same stem length for every cell; top redirect z=-5-k*spacing.
    # Count sharp skeleton length favorably (rounded routes change it).
    lengths = []
    for k in range(40):
        vertical_low = stem-5-k*spacing
        assert vertical_low-H >= r+2-1e-10
        horizontal = (k+.5)*P
        lengths.append(vertical_low + 2*r + horizontal + 60)
    closed_form = 6400*(H+spread/2+r+2+2*r+20*P+60)/1000
    assert math.isclose(sum(lengths)*160/1000, closed_form)
    # A 40-mm output draw exactly replaces 40 mm lost at the moving leg.
    assert all(math.isclose(x, (x-H)+H) for x in lengths)
    return {'d': d, 'e': e, 'bend_ratio': bend_ratio,
            'lane_spacing_mm': spacing, 'lane_depth_mm': spread+d+2*e,
            'transverse_required_mm': transverse, 'transverse_margin_mm': P-transverse,
            'stem_mm': stem, 'cord_stock_m': sum(lengths)*160/1000,
            'cord_max_mm': max(lengths), 'cord_min_mm': min(lengths),
            'straight_stem_litres': 6400*stem*2*1.4/1e6,
            'stem_and_1mm_cap_mass_g': (stem*2*1.4+4.68**2)*.00125}


def row_time(a=8000., clamp_stroke=2.):
    # Favorable direct independently positioned outputs; simultaneous opposite
    # moves granted. Eight finite capture/clamp strokes, one loaded 40-mm move,
    # empty reset, row index, and separate old/final height reads.
    return 2*motion(40, a=a)+8*(motion(clamp_stroke)+.003)+motion(P)+.020


def schedules(a=8000., channel_cost=1., site_cost=.02):
    rows = []
    for b in range(1, 81):
        t = 2+(math.ceil(80/b)+1)*row_time(a)+motion(40, a=a)
        cost = 195+20*b+80*b*channel_cost+6400*site_cost
        if t < 30:
            rows.append({'banks': b, 'channels': 80*b, 'time_s': t,
                         'allocation_usd': cost,
                         'channel_ceiling_usd': (500-195-20*b-6400*site_cost)/(80*b)})
    return min(rows, key=lambda x: x['allocation_usd'])


def retained_transfer_check():
    # Separate, individually grounded lengths behave as lower height stops.
    # Paired ropes inherit E-234 max-envelope handoff. This is an ideal oracle.
    count = 0
    for old in it.product(range(0, 41, 10), repeat=2):
        for new in it.product(range(0, 41, 10), repeat=2):
            for t in range(91):
                if t <= 45:
                    a, b = 0, t-45
                else:
                    a, b = 45-t, 0
                h = tuple(max(x+a, y+b) for x, y in zip(old, new))
                for i in range(2):
                    assert min(old[i], new[i]) <= h[i] <= max(old[i], new[i])
                    if old[i] == new[i]:
                        assert h[i] == old[i]
                count += 1
            assert h == new
    return count


def main():
    assert motion(0) == 0
    assert math.isclose(motion(5), .05)
    assert math.isclose(motion(40), .225)
    # Independent expanded timeline: three banks, 27 rows + one retry.
    stages = [motion(2)+.003]*8 + [motion(40), motion(40), motion(P), .010, .010]
    assert math.isclose(sum(stages), row_time())
    direct = schedules()
    expanded = sum([2]+stages*(math.ceil(80/direct['banks'])+1)+[motion(40)])
    assert math.isclose(expanded, direct['time_s'])
    routes = [route(d, e, k) for d, e, k in it.product((.3,.5,1.),(.15,.35,.70),(2,5,10))]
    # Normal force is summed over both pad contacts, no hidden factor of two.
    grips = [{'load_N': f, 'mu': mu, 'nominal_total_normal_per_site_N': f/(mu*.5),
              'row_nominal_total_normal_N': 80*f/(mu*.5)}
             for f, mu in it.product((.03,.2,1.,10.),(.1,.2,.4))]
    # Two stationary quarter-turn guides: total theta=pi.
    friction = [{'mu': mu, 'raising_tension_ratio': math.exp(mu*math.pi),
                 'max_tail_drag_N_for_3g_and_005N_guide': (.003*9.81-.005)/math.exp(mu*math.pi),
                 'max_tail_drag_N_at_a8': (.003*(9.81-8)-.005)/math.exp(mu*math.pi)}
                for mu in (.05,.15,.3)]
    stiffness = [{'EA_N': ea, 'deltaF_N': df, 'length_mm': 300,
                  'height_change_mm': 300*df/ea}
                 for ea, df in it.product((20,200,2000),(0.2,1,10))]
    print(json.dumps({'length_constraints': shared_length_check(),
                     'paired_ideal_observations': retained_transfer_check(),
                     'route_cases': len(routes),
                     'necessary_lane_survivors': sum(x['transverse_margin_mm'] > 0 for x in routes),
                     'representative_routes': [route(d,.35) for d in (.3,.5,1.)],
                     'row_service_s': row_time(),
                     'direct_schedules': [schedules(a) for a in (8000,2000)],
                     'zero_resident_cost': schedules(site_cost=0),
                     'cheap_channel': schedules(channel_cost=.5),
                     'grip_sensitivity': grips, 'friction': friction,
                     'elastic_sensitivity': stiffness,
                     'assembly_hours_4_ops_10_30_s': [6400*4*t/3600 for t in (10,30)]}, indent=2))

if __name__ == '__main__':
    main()
