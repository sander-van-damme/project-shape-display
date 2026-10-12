#!/usr/bin/env python3
"""Bounded rotary architecture screen. All rates/costs are assumptions, not passes.
Reuses retained E-254 arrays; no network, CAD, random priors or generated files.
"""
import itertools
import json
import math
from pathlib import Path

N, PITCH, LEAD = 80, 5.08, 3.0


def move(d):
    return 2*math.sqrt(d/5000) if d <= 8 else d/200+.04


def spin(turns, rpm=3000, accel=1000):
    v, a = rpm/60, accel
    return 2*math.sqrt(turns/a) if turns <= v*v/a else turns/v+v/a


def program(row):
    """Stopped signed threshold groups: ascending magnitudes, retire finished tips."""
    groups = []
    for sign in (1, -1):
        last = 0
        for endpoint in sorted({sign*x for x in row if sign*x > 0}):
            mask = [sign*x >= endpoint for x in row]
            groups.append((sign*(endpoint-last), mask))
            last = endpoint
    return groups


def dwell(row, shared=False, write=.01, proof=.02, rpm=3000, accel=1000):
    if not any(row):
        return 0
    if not shared:
        return .08+proof+spin(max(map(abs, row))/LEAD, rpm, accel)
    # Write all mask positions at rest, prove command and engage dog in .02 s.
    # Clear the mask after the last group, with another write/engagement allowance.
    groups = program(row)
    return .08+proof+sum(write+.02+spin(abs(d)/LEAD, rpm, accel) for d, _ in groups)+write+.02


def schedule(delta, b=2, shared=False, pre=False, **kw):
    banks, starts, maxrow, writes, stations = [], [], 0, 0, 0
    width = math.ceil(N/b)
    for base in range(0, N, width):
        last, total, first = 0, 0, None
        for y in range(base, min(N, base+width)):
            row = delta[y]
            if not any(row):
                continue
            seek = max(.05, move(abs(y-base-last)*PITCH))
            if first is None:
                first = seek
            service = dwell(row, shared, **kw)
            total += seek+service
            maxrow = max(maxrow, service)
            stations += 1
            writes += N*(len(program(row))+1) if shared else 0
            last = y-base
        if first is not None:
            total += move(last*PITCH)
        banks.append(total-(first or 0) if pre else total)
        starts.append(first or 0)
    if not stations:
        return dict(seconds=0, stations=0, mask_decisions=0, maxrow=0)
    # One immediate full station retry, final return and four-second common budget.
    return dict(seconds=4+max(banks)+maxrow, stations=stations,
                mask_decisions=writes, maxrow=maxrow, first_seek=max(starts))


def quarters(delta):
    """Four disjoint 40x40 regions, one 16-tip head each, three strips/row.
    Last strip uses eight tips. XY simultaneous rest-to-rest motion and return.
    """
    banks, worst, stations = [], 0, 0
    for y0, x0 in itertools.product((0, 40), repeat=2):
        pos, total = (0, 0), 0
        for y in range(40):
            for x in ((0, 16, 32) if y % 2 == 0 else (32, 16, 0)):
                row = delta[y0+y][x0+x:x0+min(40, x+16)]
                if not any(row):
                    continue
                total += max(.05, move(abs(x-pos[0])*PITCH), move(abs(y-pos[1])*PITCH))
                service = dwell(row)
                total += service
                worst = max(worst, service)
                pos = x, y
                stations += 1
        total += max(move(pos[0]*PITCH), move(pos[1]*PITCH))
        banks.append(total)
    return 4+max(banks)+worst if stations else 0


def delta(a, b):
    return [[y-x for x, y in zip(r, s)] for r, s in zip(a, b)]


def cases():
    raw = json.loads((Path(__file__).resolve().parent.parent/'E-254/heightmaps.json').read_text())
    maps = {k: [[int(c)*10 for c in row] for row in rows] for k, rows in raw.items()}
    flat = [[0]*N for _ in range(N)]
    out = {'initial_'+k: delta(flat, m) for k, m in maps.items()}
    for a, b in itertools.permutations(('ruins', 'road', 'ravine'), 2):
        out[a+'_to_'+b] = delta(maps[a], maps[b])
    for k in ('ruins', 'road', 'ravine'):
        m = maps[k]
        for name, visible in [('east', lambda x, y: x < 40),
                              ('local', lambda x, y: not (40 <= x < 60 and 20 <= y < 40))]:
            old = [[h if visible(x, y) else 0 for x, h in enumerate(row)] for y, row in enumerate(m)]
            out[name+'_'+k] = delta(old, m)
    out['dense_stress'] = [[40]*N for _ in range(N)]
    out['mixed_dense_stress'] = [[40 if (x+y) % 2 else -40 for x in range(N)] for y in range(N)]
    return out


def checks():
    count = 0
    for old in itertools.product(range(0, 41, 10), repeat=3):
        for new in itertools.product(range(0, 41, 10), repeat=3):
            row = [b-a for a, b in zip(old, new)]
            actual = list(old)
            for step, mask in program(row):
                actual = [h+step if bit else h for h, bit in zip(actual, mask)]
                assert all(min(a, b) <= h <= max(a, b) for a, b, h in zip(old, new, actual))
                assert all(h == a for a, b, h in zip(old, new, actual) if a == b)
            assert actual == list(new)
            # A stopped partial first move must regenerate its remaining delta.
            groups = program(row)
            if groups:
                step, mask = groups[0]
                partial = [h+step/2 if bit else h for h, bit in zip(old, mask)]
                for remaining, active in program([b-a for a, b in zip(partial, new)]):
                    partial = [h+remaining if bit else h for h, bit in zip(partial, active)]
                assert partial == list(new)
            count += 1
    assert abs(spin(100)-2.05) < 1e-12
    assert schedule([[0]*N for _ in range(N)])['seconds'] == 0
    assert abs(3.4/2+2*.65-1.35-3.2/2-.05) < 1e-12
    assert schedule([[40]*N for _ in range(N)], shared=True)['seconds'] > schedule([[40]*N for _ in range(N)])['seconds']
    # Cartesian-product half-selection witness, independent of torque mechanism.
    wanted = {(0, 0), (1, 1)}
    activated = set(itertools.product({p[0] for p in wanted}, {p[1] for p in wanted}))
    assert activated-wanted == {(0, 1), (1, 0)}
    return count


def costs(b, shared=False, channel=4):
    # Explicit favorable complete allocation; no quotes or force-qualified hardware.
    # Common electronics20, PSU/protection40, frame60, sensing50, harness20,
    # fasteners20, freight/spares40. Resident stock .02/site.
    reserve = 250+6400*.02+b*(55+(35 if shared else 0))
    return dict(reserve=reserve, channels=80*b, assumed_total=reserve+80*b*channel,
                caps={c: (c-reserve)/(80*b) for c in (500, 1000, 1500)})


def main():
    replay = checks()
    data = cases()
    benchmark = [d for k, d in data.items() if '_to_' in k or k in ('initial_ruins', 'initial_road', 'initial_ravine')]
    minima = {}
    for shared in (False, True):
        for write, proof, rpm in ((.01, .02, 3000), (.05, .02, 3000), (.01, .10, 3000), (.01, .02, 1500)):
            for b in range(1, 17):
                t = max(schedule(d, b, shared, write=write, proof=proof, rpm=rpm)['seconds'] for d in benchmark)
                if t < 30:
                    minima[f'{shared=},{write=},{proof=},{rpm=}'] = dict(b=b, seconds=t, cost=costs(b, shared))
                    break
    results = {}
    for name, d in data.items():
        transposed = list(map(list, zip(*d)))
        horizontal = schedule(d, 1)['seconds']
        vertical = schedule(transposed, 1)['seconds']
        # Outbound and return yaw total .5 s, plus two full origin exchange legs.
        # This is a declared geometric/rate oracle, not a collision-cleared head.
        results[name] = dict(changed=sum(x != 0 for row in d for x in row),
            total_turns=sum(abs(x) for row in d for x in row)/LEAD,
            independent_b2=schedule(d), shared_b2=schedule(d, shared=True),
            shared_b3=schedule(d, 3, True), quarters_4x16=quarters(d),
            rotating_1x80=min(horizontal, vertical+.5+2*move(79*PITCH)),
            orthogonal_2x80_serial=min(horizontal, vertical),
            local_known_preposition=schedule(d, pre=True)['seconds'],
            # Unknown reveal after a wrong pre-position can require full bank traversal.
            unknown_preposition_upper=schedule(d)['seconds']+move(39*PITCH))
    static = []
    for dm, mu in itertools.product((2.3, 3.0), (.1, .3, .5)):
        r, effective = dm/2, mu/math.cos(math.radians(15))
        slope = LEAD/(math.pi*dm)
        # Torque per axial newton, N mm/N; collar term independent.
        lower = r*(effective-slope)/(1+effective*slope)
        static.append(dict(mean_diameter=dm, mu=mu, lowering_Nmm_per_N=lower,
                           collar_mu01_r2_net=lower+.1*2,
                           mu_threshold=slope*math.cos(math.radians(15))))
    print(json.dumps(dict(evidence='Conditional schedules and bounds; no hardware qualification',
        replay_cases=replay, minima=minima, cases=results, hold=static,
        power_loss_delay_mm={str(ms): LEAD*50*ms/1000 for ms in (1, 5, 20)},
        assembly_hours={str(seconds): 6400*seconds/3600 for seconds in (5, 10, 20)}), indent=2))


if __name__ == '__main__':
    main()
