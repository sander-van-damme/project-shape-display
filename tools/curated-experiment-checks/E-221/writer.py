"""E-221 necessary conditions; explicit scenario bounds, no hardware validation.
stdlib; deterministic support replay and schedule enumeration; stdout only.
"""
import itertools as it
import json
import math

LEVELS = (0, 10, 20, 30, 40)


def move(d, a, v=200):
    d = abs(d)
    return 2*math.sqrt(d/a) if d <= v*v/a else d/v+v/a


def row_visit(old, target, fault=None):
    """Independent shoes acquire bottom feet with resident row keeper seated.
    Each shoe has its OWN grounded arrest. Geometry/sensing are obligations.
    """
    n = len(old)
    shoe = [-5.] * n
    keeper = True
    arrested = [True] * n
    for u in (0, .5, 1):
        shoe = [-5+(h+5)*u for h in old]
        assert all(s <= h for s, h in zip(shoe, old))
        assert keeper
    if fault == 'acquisition':
        shoe[0] -= 1
    if fault == 'arrest':
        arrested[0] = False
    if shoe != list(old) or not all(arrested):
        assert keeper
        return False
    keeper = False
    for u in (0, .25, .5, .75, 1):
        shoe = [o+(t-o)*u for o, t in zip(old, target)]
        # Continuous affine support path; source loss idealized as zero-motion
        # arrested axis here. Indexed catch descent is bounded separately.
        assert all(arrested)
        for o, t, s in zip(old, target, shoe):
            assert min(o,t) <= s <= max(o,t)
            if o == t:
                assert s == o
    if fault == 'deposit':
        assert not keeper and all(arrested)
        return False
    keeper = True
    assert shoe == list(target) and all(h in LEVELS for h in shoe)
    for u in (0, .5, 1):
        shoe = [h-(h+5)*u for h in target]
        assert keeper and all(s <= h for s,h in zip(shoe,target))
    return True


def caught_sweep(old, target):
    """Common lift plus individual resident catches; ideal point engagements.
    Changed columns are picked up when lift reaches old height; deposited at
    target on descent. Unchanged catches never open. This charges real catches.
    """
    selected = [o != t for o,t in zip(old,target)]
    for upward in (True,False):
        for q in (range(-5,41) if upward else range(40,-6,-1)):
            for o,t,change in zip(old,target,selected):
                caught = not change or (q < o if upward else q <= t)
                h = o if not change else (max(o,q) if upward else max(t,q))
                if not caught:
                    assert h == q  # grounded arrested common lift
                else:
                    assert h == (o if upward or not change else t)
                if not change:
                    assert h == o
    return True


def sweep_counterexample():
    old, target = (0, 40, 20), (40, 0, 20)
    # Removing individually selected catches from that construction and
    # acquiring the whole row with a common backing resets unchanged cells.
    h = list(old)
    for q in range(41):
        h = [max(o,q) for o in old]
    assert h[2] != old[2]
    # No resident state: after a finite travelling backing leaves, gravity
    # returns every ideal frictionless column to its common bottom stop.
    return dict(old=old, target=target, after_common_acquisition=h,
                unchanged_displacement_mm=h[2]-old[2])


def service(a, aux, indexed=False):
    # Worst-useful row includes both 0->40 and 40->0; independent maxima of
    # acquisition, rewrite, clearance are attained simultaneously in that row.
    loaded = 40*(move(1,a)+.001) if indexed else move(40,a)
    return 2*move(45,a)+loaded+aux


def stopped(b, a, aux, indexed=False, changed_rows=80):
    # One serial critical bank; worst regional distribution also matters.
    cycle = service(a,aux,indexed)+move(5.08,a)
    return 2+(math.ceil(changed_rows/b)+1)*cycle


def continuous(b, a, aux, width=2., indexed=False):
    # Finite total contact window; acquisition+rewrite+clearance all inside.
    # Row-boundary keeper must stay seated until acquisition and re-seat before
    # departure. Wider windows would need multi-row interaction geometry.
    tau = service(a,aux,indexed)*5.08/width
    speed = 5.08/tau
    # Charge an extra pitch for entry/exit, one retried row interval, and
    # start/stop ramps. Grant retry without reversal: optimistic lower screen.
    total = 2+(math.ceil(80/b)+2)*tau+speed/a
    return total


def main():
    count=0
    for old,target in it.product(it.product(LEVELS,repeat=3),repeat=2):
        assert row_visit(old,target)
        assert caught_sweep(old,target)
        count+=1
    for fault in ('acquisition','arrest','deposit'):
        assert not row_visit((0,40,20),(40,0,20),fault)
    # Independent limiting cases and exact workload attaining schedule maxima.
    assert move(0,8000)==0 and math.isclose(move(5,8000),.05)
    old,target=(0,40),(40,0)
    assert max(h+5 for h in old)==45
    assert max(abs(t-o) for o,t in zip(old,target))==40
    assert max(h+5 for h in target)==45
    assert math.isclose(service(8000,.1),.825)
    scenarios=[]
    for indexed,a,aux in it.product((False,True),(2000,8000),(.1,.25,.5)):
        for mode,fn in (('stopped',stopped),('continuous_2mm',continuous)):
            b=next((b for b in range(1,81) if fn(b,a,aux,indexed=indexed)<30),None)
            scenarios.append(dict(mode=mode,indexed=indexed,a=a,aux=aux,banks=b,
                                  axes=80*b if b else None,
                                  seconds=fn(b,a,aux,indexed=indexed) if b else None))
    # All physical command words originate after receipt; buffers don't change
    # sustainable production. Independent 80-axis rows need two setpoints/cell.
    assert 2*6400/30 > 426
    print(json.dumps(dict(ideal_three_cell_visits=count,
        sweep_failure=sweep_counterexample(),scenarios=scenarios,
        fast_stopped_3bank_aux={str(x):stopped(3,8000,x) for x in (.1,.25,.5)},
        continuous_width_sensitivity={str(w):next(b for b in range(1,81)
            if continuous(b,8000,.1,width=w)<30) for w in (1.,2.,4.)},
        coherent_error_bounds=[dict(e=e,vertical_takeover=2*e,
            groove_margin=1-e,shoe_lateral_margin=.7-e) for e in (.15,.35,.70)],
        cost_ceiling_250_reserve={str(c):250/c for c in (240,320,480,640)},
        per_axis_force_scenarios=[dict(F=F,bank_load=80*F,
            bank_work_J=80*F*.04,axis_ideal_torque_Nm=F*.01)
            for F in (1,3.27,10)]),indent=2))


if __name__=='__main__':
    main()
