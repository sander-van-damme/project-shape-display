"""E-216: deterministic architecture bounds, NOT calibrated hardware predictions.
Run with Python standard library. All dimensional/force/rate inputs are scenarios.
"""
from functools import lru_cache
import itertools
import json
import math

N, ROWS, COLS = 6400, 80, 80


def move(d, a, v=200):
    """Rest-to-rest trapezoid, mm, mm/s², mm/s."""
    d = abs(d)
    return 2*math.sqrt(d/a) if d <= v*v/a else d/v + v/a


def replay(old, target, fail=None):
    """One row: common resident comb, independent temporary hold/travel grips.
    Six-state old mask includes BYPASS; target has five states. Ideal sensing.
    No geometry, frictional support qualification, unload motion or power-loss proof.
    """
    h = list(old)
    hold, grip = set(), {}
    changed = {i for i in range(len(h)) if old[i] != target[i]}
    comb, e, path, transfers = True, 0, [0], 0
    def check():
        assert all(comb or i in hold or i in grip for i in range(len(h))), 'unsupported'
        assert all(h[i] == old[i] for i in range(len(h)) if i not in changed), 'neighbor moved'
        assert all(h[i] >= 0 for i in range(len(h)))
        assert all(h[i] == e+d for i,d in grip.items())
    if not changed:
        return dict(path=path, transfers=0)
    hold.update(range(len(h)))  # observe each actual clamp, not just common actuator
    if fail == 'takeover': hold.remove(0)
    comb = False
    check()
    transfers += len(h)
    def acquire(sites):
        nonlocal transfers
        for i in sites:
            assert i in hold
            grip[i] = h[i]-e
        check()
        hold.difference_update(sites)
        transfers += len(sites)
        check()
    def deposit(sites):
        nonlocal transfers
        if fail != 'deposit': hold.update(sites)
        check()
        for i in sites: del grip[i]
        transfers += len(sites)
        check()
    def travel(z):
        nonlocal e
        if z == e: return
        assert not (hold & grip.keys())
        e = z
        path.append(z)
        for i,d in grip.items(): h[i] = e+d
        check()
    down = {i for i in changed if old[i] > 0}
    acquire(down)
    for level in sorted({old[i] for i in down}):
        travel(-level)
        deposit({i for i in down if old[i] == level})
    assert all(h[i] == 0 for i in changed)
    bottom = e
    up = {i for i in changed if target[i] > 0}
    acquire(up)
    for level in sorted({target[i] for i in up}):
        travel(bottom+level)
        deposit({i for i in up if target[i] == level})
    travel(0)  # empty carriage return remains charged
    assert h == list(target) and not grip
    if fail != 'comb': comb = True
    hold.clear()
    transfers += len(h)
    check()
    return dict(path=path, transfers=transfers)


@lru_cache(maxsize=None)
def row_time(old, target, q, a, dwell=.020, row_aux=.5):
    """q serial setting lanes/head. Values are physically overwritten on every
    visited row, including BYPASS entries; each value has 15-mm worst travel.
    row_aux covers dock, comb out/in, registration, grip proof and final readback.
    dwell covers each elevator stop. These unresolved allowances are explicit.
    """
    r = replay(old, target)
    if old == target: return 0.
    groups = math.ceil(COLS/q)
    setter = move(15,a)+2*move(2,a)+.005  # change state, engage/retract, read
    writing = 2*groups*setter + (groups-1)*move(5.08,a)
    motion = sum(move(y-x,a) for x,y in zip(r['path'],r['path'][1:]))
    return writing+motion+(len(r['path'])-1)*dwell+row_aux+move(5.08,a)


def schedule(old, target, banks, q, a, row_aux=.5):
    """Contiguous equal banks, no balancing across physical bank boundaries.
    No overlapping writing with loaded motion. One complete failed-row retry
    charged at critical-path worst row; covers detected retry, not arbitrary faults.
    """
    times=[row_time(tuple(x),tuple(y),q,a,row_aux=row_aux) for x,y in zip(old,target)]
    width=ROWS//banks
    loads=[sum(times[k:k+width]) for k in range(0,ROWS,width)]
    return 2.+max(loads)+max(times)  # map processing/home/settle allowance + retry


def workloads(levels=5):
    heights=[40*i/(levels-1) for i in range(levels)]
    # Contains all 25 old/new pairs; full rows include unchanged and changed cells.
    pairs=list(itertools.product(heights,repeat=2))
    old=[[pairs[c%len(pairs)][0] for c in range(COLS)] for _ in range(ROWS)]
    target=[[pairs[c%len(pairs)][1] for c in range(COLS)] for _ in range(ROWS)]
    return old,target


def checks():
    for pair in itertools.product(range(5),repeat=4):
        replay([10*x for x in pair[:2]],[10*x for x in pair[2:]])
    for fault in ('takeover','deposit','comb'):
        try: replay([10,40],[40,0],fault)
        except AssertionError: pass
        else: raise AssertionError('fault escaped: '+fault)
    assert move(0,2000)==0 and math.isclose(move(20,2000),.2)
    assert math.isclose(move(40,2000),.3)
    assert math.isclose(move(5,2000),.1)
    # Independent row motion witness: 4 down and 4 up stops each 10 mm.
    old,target=workloads()
    r=replay(old[0],target[0]); assert r['path']==[0,-10,-20,-30,-40,-30,-20,-10,0]
    assert sum(abs(y-x) for x,y in zip(r['path'],r['path'][1:]))==80
    assert math.isclose(sum(move(y-x,2000) for x,y in zip(r['path'],r['path'][1:])),8*2*math.sqrt(10/2000))
    # Unknown independent failures cannot be turned into qualified iid yield.
    assert math.isclose((1-.001)**6400, math.exp(6400*math.log1p(-.001)))


def main():
    checks()
    old,target=workloads()
    rows=[]
    for b,a in itertools.product((1,2,4,8,16),(500,2000,8000)):
        passing=[q for q in (1,2,4,8,16,40,80) if schedule(old,target,b,q,a)<30]
        if passing:
            q=min(passing)
            rows.append(dict(banks=b,acceleration=a,lanes_per_head=q,
                setter_lanes=b*q,time_s=round(schedule(old,target,b,q,a),3),
                head_grips=160*b,mask_sliders=160*b,
                remaining_per_lane_usd=round(250/(b*q),3)))
    flat=[[0]*COLS for _ in range(ROWS)]
    patch=[r[:] for r in flat]
    for r in range(5):
        for c in range(5): patch[r][c]=10*(1+c%4)
    print(json.dumps(dict(
        evidence='calculation and logical replay; all rates/costs/tolerances assumed bounds',
        checks='625 two-cell maps, 3 injected missing supports, analytical motion limits',
        rows=rows,
        reference_times={str((b,q,a)):round(schedule(old,target,b,q,a),3)
                         for b,q,a in [(8,1,2000),(8,8,2000),(8,16,8000),(8,40,2000),(16,8,2000)]},
        selected_sensitivity={str(aux):round(schedule(old,target,8,40,8000,row_aux=aux),3) for aux in (.25,.5,1,2)},
        regional_5x5_s=round(schedule(flat,patch,8,40,8000),3),
        full_support_observations=sum(replay(x,y)['transfers'] for x,y in zip(old,target)),
        layered_mask_write_s={str(lanes):round(25600/(lanes*71),3) for lanes in (1,8,16,32)},
        shutter_support_normal_load_N={str(f):6400*f for f in (1,3.27,10)},
        head_clamp_total_normal_N={str((f,mu)):round(80*f/mu,2) for f,mu in itertools.product((1,3.27,10),(.1,.2,.4))},
        comb_phase_error_mm={str((bias,local,skew)):bias+local+skew for bias,local,skew in ((.05,.05,.05),(.15,.1,.1),(.3,.2,.2))},
        independent_all_good={str(n):(1-.001)**n for n in (6400,12800,25600)},
        batch_fault_affected={'one_comb':80,'one_head_8_banks':800,'one_shared_reader':6400},
        labor_hours={str(seconds):round(6400*seconds/3600,3) for seconds in (5,10,30)},
        column_stock_cm3=6400*3*3*80/1000,
        shutter_stock_cm3=4*406.4**2*2/1000,
    ),indent=2))

if __name__=='__main__': main()
