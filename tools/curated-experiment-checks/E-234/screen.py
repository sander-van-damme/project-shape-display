"""E-234: paired captive supports, unloaded vertical shared-stroke writing.
Stdlib, stdout only. Assumed motion/friction/allocation bounds, ideal replay.
No process priors, CAD, prices, sensing, dynamic contact or physical validation.
"""
from itertools import product
import json
import math

LEVELS = (0, 10, 20, 30, 40)
Q = (1, 2, 4, 5, 8, 10, 16, 20, 40, 80)
D = 45


def move(d, v=200., a=8000.):
    assert d >= 0 and v > 0 and a > 0
    return 2 * math.sqrt(d / a) if d <= v*v/a else d/v + v/a


def write(prior, target, retention=True):
    """Terrain is on other dock throughout. Working values are 1 mm above
    final seated datum. Common platen resets; friction holds parked outputs.
    Common row comb then captures; pad releases; gravity seating is GRANTED.
    """
    raw = [0] * len(prior)  # reset whole inactive row; prior can be arbitrary
    active = [t > 0 for t in target]
    for z in LEVELS[1:]:
        for i in range(len(raw)):
            if active[i]:
                raw[i] = z
            elif not retention:
                raw[i] = 0
        active = [a and t > z for a, t in zip(active, target)]
    if not retention:
        raw = [0] * len(raw)  # all fingers must leave before head departure
    assert tuple(raw) == target, 'unloaded bars still require temporary retention'
    return tuple(raw)


def handoff(old, target, samples=1):
    """Disjoint fixed bearing lanes; new rise then old descent. Both keepers
    seated and shared elevators arrested are prerequisites, not implemented.
    Contacts at exact switches plus interval midpoints; sampled holdout optional.
    """
    state_count = 0
    last = list(old)
    for stage in ('new_up', 'old_down'):
        breaks = {0., float(D)}
        if stage == 'new_up':
            breaks.update(float(o-t+D) for o,t in zip(old,target) if 0 <= o-t+D <= D)
        else:
            breaks.update(float(o-t) for o,t in zip(old,target) if 0 <= o-t <= D)
        ordered = sorted(breaks)
        points = set(ordered)
        points.update((x+y)/2 for x,y in zip(ordered, ordered[1:]))
        if samples > 1:
            points.update(k*D/samples for k in range(samples+1))
        for x in sorted(points):
            a,b = (0., x-D) if stage == 'new_up' else (-x, 0.)
            h = [max(o+a,t+b) for o,t in zip(old,target)]
            for i,(o,t,y) in enumerate(zip(old,target,h)):
                assert min(o,t) <= y <= max(o,t)
                assert y in (o+a,t+b), 'no positive bearing path'
                assert o != t or y == o
                assert (y-last[i])*(t-o) >= -1e-9, 'nonmonotone change'
            last = h
            state_count += 1
    assert tuple(last) == target
    return state_count


def schedule(b,q,aux=.25,acc=8000.,indexed=False):
    """q evenly spaced outputs; 80/q adjacent phases. Whole-row reset before
    phases; head x return and empty lifts charged each service. One full retry.
    Two shared loaded lifts use 45 mm; empty resets also 45 mm. No overlap.
    """
    m = lambda d: move(d, a=acc)
    g = 80//q
    # Preset + five releases, each 3-mm travel and 3-ms proof allocation.
    group = 4*m(10) + m(40) + 6*(m(3)+.003)
    reset = 2*m(40) + 2*m(3)
    xscan = (g-1)*m(5.08) + m((g-1)*5.08)
    loaded = 45*(m(1)+.001) if indexed else m(45)
    exchange = 2*loaded + 2*m(45) + 2*m(3)
    row = reset + g*group + xscan + exchange + aux + m(5.08)
    seconds = 2 + (math.ceil(80/b)+1)*row
    # Scenarios only, not quotes. Resident paid hardware allowance 160*$0.20.
    cost = 130 + 160*.20 + 65*b + .35*b*q
    return {'banks':b,'q':q,'channels':b*q,'groups':g,'row_s':row,
            'seconds':seconds,'assumed_cost':cost}


def best(aux=.25,acc=8000.,indexed=False):
    rows = [schedule(b,q,aux,acc,indexed) for b in range(1,81) for q in Q]
    feasible = [r for r in rows if r['seconds'] < 30]
    return {'least_cost':min(feasible,key=lambda r:r['assumed_cost']),
            'least_channels':min(feasible,key=lambda r:(r['channels'],r['assumed_cost'],r['seconds']))}


def friction(mass=.0004352, disturbance=.01, n=.3, spread=.5):
    # mu=.1.. .4 and ±spread common/local pressure variation are assumed bounds.
    lower = .1*n*(1-spread) - mass*9.81 - disturbance
    upper = .4*n*(1+spread) + mass*(9.81+8)
    return {'hold_margin_N':lower,'push_N_per_bar':upper,
            'push_N_80':80*upper}


def main():
    # Motion limiting cases and independent trapezoid calculation.
    assert move(0) == 0
    assert math.isclose(move(5),.05)
    assert math.isclose(move(45), .05 + (45-5)/200)
    assert move(45,a=2000) > move(45)
    assert schedule(8,80,aux=.5)['seconds'] > schedule(8,80)['seconds']
    pairs = states = 0
    for old in product(LEVELS,repeat=3):
        for target in product(LEVELS,repeat=3):
            assert write(old,target) == target
            states += handoff(old,target)
            pairs += 1
    for o,t in product(LEVELS,repeat=2):
        handoff((o,),(t,),samples=997)
    try:
        write((40,),(20,),retention=False)
    except AssertionError:
        pass
    else:
        raise AssertionError('missing pad control must fail')
    # Wrong media code before transfer is safely rewritten under old dock.
    # Wrong but stable code after transfer: read actual, rewrite OTHER lane;
    # never reset currently loaded media. Original unchanged-invariance claim
    # does not cover reader false acceptance or a bad physical target.
    retries = wrong_codes = 0
    for old in product(LEVELS,repeat=2):
        for target in product(LEVELS,repeat=2):
            for i in range(2):
                for wrong in LEVELS:
                    actual=list(target); actual[i]=wrong; actual=tuple(actual)
                    handoff(old,actual)
                    handoff(actual,write(old,target))
                    retries += 1
                    wrong_codes += wrong != target[i]
    # Counterexample to rewriting active bars: reset drops 40-mm terrain to 0.
    assert max(0,40-D) != 40
    # Bounded error examples: relative old/new seat errors, row/batch correlated.
    margins=[]
    for e in (.15,.35,.70):
        margins.append({'e_mm':e,'keeper_margin_mm':1-2*e,
                        'lane_gap_mm':.8-2*e,'unchanged_shift_mm':2*e,
                        'reset_insertion_margin_mm':D-41-2-2*e})
    # Source loss without arrest during new rise: target 40 at b=-20 falls
    # back to old zero if its elevator is free. A powered motor is no proof.
    assert max(0, 40-20) > max(0, 40-D)
    # Media stock: 64 x 3.4 x 1.6 mm per bar, two per cell.
    volume_l = 12800*64*3.4*1.6/1e6
    out={'maps':pairs,'contact_states':states,'retry_and_control_cases':retries,'actual_wrong_codes':wrong_codes,
         'nominal':best(),
         'bank_cost_sensitivity':{str(c):min((dict(r, cost=162+c*r['banks']+.35*r['channels']) for b in range(1,81) for q in Q if (r:=schedule(b,q))['seconds'] < 30),key=lambda r:r['cost']) for c in (0,20,65)},'aux_050':best(aux=.5),'aux_100':best(aux=1),
         'slower':best(acc=2000),'indexed':best(indexed=True),
         'friction':{str(d):friction(disturbance=d) for d in (.005,.01,.05)},
         'geometry':margins,'bar_stock_l':volume_l,
         'bar_print_h_at_5_15_with_10pct_scrap':[volume_l*1e6/r/3600/.9 for r in (5,15)],
         'bar_assembly_h_at_10_30s':[12800*s/3600 for s in (10,30)]}
    print(json.dumps(out,indent=2))


if __name__ == '__main__':
    main()
