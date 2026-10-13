#!/usr/bin/env python3
"""One reusable XY rotary line: conditional schedules, not a routed machine.

Reuse physical terrain and E-266 costs; compare fewer installed channels rather
than merely limiting electrical slots. Each selected tip has an independent
reversible drive. Unselected overlapping tips must stay isolated (unqualified).
"""
import argparse
import importlib.util
import itertools
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location('frontier', Path(__file__).resolve().parents[1] / 'E-266/frontier.py')
f = importlib.util.module_from_spec(spec)
spec.loader.exec_module(f)
a = f.a


def stations(delta, width):
    """Greedy interval cover per row; alternating row directions, no overhang.

    Select only still-unwritten changed cells within each width-long footprint.
    This minimizes station count per row, not weighted dwell or XY route time.
    """
    n = len(delta)
    assert 1 <= width <= n and all(len(row) == n for row in delta)
    out = []; previous_x = 0
    for y, row in enumerate(delta):
        remaining = {x for x, d in enumerate(row) if d}
        while remaining:
            if y % 2:
                x0 = max(0, max(remaining)-width+1)
            else:
                x0 = min(min(remaining), n-width)
            selected = sorted(x for x in remaining if x0 <= x < x0+width)
            # Slide the same selected group within the footprint toward the last
            # X position. Do not zigzag a wide head across a narrow reveal merely
            # because successive rows choose opposite greedy cover directions.
            lo = max(0, max(selected)-width+1)
            hi = min(min(selected), n-width)
            x0 = max(lo, min(hi, previous_x))
            previous_x = x0
            out.append((x0, y, tuple((x, row[x]) for x in selected)))
            remaining.difference_update(selected)
    return out


def schedule(delta, width, rpm=850, lead=3, accel=1000, extra_dock=0):
    n = len(delta); pitch = a.c.v.s.WIDTH/n
    path = stations(delta, width)
    if not path:
        return dict(seconds=0., stations=0, first_seek_s=0., travel_s=0.,
                    seek_s=0., return_s=0., dock_proof_s=0., common_s=0.,
                    spin_s=0., retry_s=0., lower_s=0., changed_cells=0,
                    raised_cells=0, lowered_cells=0, unchanged_cells=n*n,
                    visited_rows=0, seeks=0, dock_cycles=0, retry_cycles=0)
    # Compare row order with a column-major serpentine through the same jobs.
    # This removes the gratuitous full-width sweep after each dense row without
    # pretending to solve a continuous routing or weighted-cover optimum.
    xs = {x:i for i,x in enumerate(sorted({x for x,_,_ in path}))}
    alternate = sorted(path,key=lambda st:(st[0],st[1] if xs[st[0]]%2==0 else -st[1]))
    def journey(route):
        last=(0,0); total=first=0.
        for x,y,_ in route:
            seek=max(.05,a.r.move(abs(x-last[0])*pitch),a.r.move(abs(y-last[1])*pitch))
            if not first: first=seek
            total+=seek; last=x,y
        return total+max(a.r.move(last[0]*pitch),a.r.move(last[1]*pitch)),first
    path = min((path,alternate),key=lambda route:journey(route)[0])
    pos = (0,0); travel = spin = retry = first = 0.
    for x,y,selected in path:
        seek = max(.05, a.r.move(abs(x-pos[0])*pitch), a.r.move(abs(y-pos[1])*pitch))
        if not first:
            first = seek
        rotation = a.r.spin(max(abs(d) for _,d in selected)/lead,rpm,accel)
        dwell = .1+extra_dock+rotation
        travel += seek; spin += rotation; retry = max(retry,dwell)
        pos = x,y
    seek = travel
    return_time = max(a.r.move(pos[0]*pitch),a.r.move(pos[1]*pitch))
    travel += return_time
    dock = len(path)*(.1+extra_dock)
    total = 4+travel+dock+spin+retry
    # Relaxation: ignore travel/overhead/retry and allow free concurrent routing.
    work = sum(a.r.spin(abs(d)/lead,rpm,accel) for row in delta for d in row if d)
    lower = work/width
    assert total+1e-8 >= lower
    return dict(seconds=total,stations=len(path),first_seek_s=first,
                travel_s=travel,seek_s=seek,return_s=return_time,
                dock_proof_s=dock,common_s=4.,spin_s=spin,retry_s=retry,lower_s=lower,
                changed_cells=sum(d!=0 for row in delta for d in row),
                raised_cells=sum(d>0 for row in delta for d in row),
                lowered_cells=sum(d<0 for row in delta for d in row),
                unchanged_cells=sum(d==0 for row in delta for d in row),
                visited_rows=len({y for _,y,_ in path}),seeks=len(path),
                dock_cycles=len(path),retry_cycles=1)


def cost(n,width,xy_extra=35):
    # Same dated tier inputs. Extra XY axis is a labelled allocation, not quote.
    mq,mp = f.bulk(width,((1,1.95),(10,1.76),(100,1.56)))
    dq,dp = f.bulk(math.ceil(width/2),((1,5.95),(10,5.36),(100,4.76)))
    reserve = a.r.costs(1,n=n)['reserve']+(xy_extra if width<n else 0)
    total = reserve+mq*mp+dq*dp
    return dict(outputs=width,subset_plus_reserve_USD=total,
                motor_quantity=mq,driver_boards=dq,xy_extra_USD=xy_extra if width<n else 0,
                residual_per_output_USD={b:(b-total)/width for b in (500,1000,1500)},
                motor_kg=.0175*width,rated_load_motor_A=.25*width,stall_motor_A=.5*width)


def local_cases(n,stroke):
    # 406.4-mm board =16 D&D squares; 4-square windows at 2-square offsets.
    # 7x7 overlapping windows/map. This is spatial coverage, not a play sample.
    targets,start = a.c.terrain(n,stroke-20,stroke-20)
    w = n//4; step = n//8
    out = {}
    for name in a.c.v.s.SUITES['relief']:
        d = a.r.delta(start,targets[name])
        for y0,x0 in itertools.product(range(0,n-w+1,step),repeat=2):
            out[f'{name}:{x0},{y0}'] = [[v if x0<=x<x0+w and y0<=y<y0+w else 0
                                        for x,v in enumerate(row)] for y,row in enumerate(d)]
    return out


def summarize(cases,width,**kw):
    rows = {name:schedule(d,width,**kw) for name,d in cases.items()}
    active = {k:v for k,v in rows.items() if v['stations']}
    worst = max(active,key=lambda k:active[k]['seconds'])
    return dict(max_s=active[worst]['seconds'],worst=worst,
                worst_ledger=active[worst],
                min_nonempty_s=min(v['seconds'] for v in active.values()),
                nonempty=len(active),within30=sum(v['seconds']<=30 for v in active.values()),
                max_stations=max(v['stations'] for v in active.values()),
                max_work_lower_s=max(v['lower_s'] for v in active.values()),
                max_known_preposition_s=max(v['seconds']-v['first_seek_s'] for v in active.values()))


def full_row_local(n,stroke,banks,k=32):
    """Same reveal windows and rate, E-266 bank scheduler (not a new workload)."""
    rows={name:a.schedule(d,k,850,lead=3,banks=banks)['feasible_s']
          for name,d in local_cases(n,stroke).items() if any(map(any,d))}
    worst=max(rows,key=rows.get)
    return dict(n=n,stroke=stroke,banks=banks,k=k,outputs=n*banks,
                max_s=rows[worst],worst=worst,nonempty=len(rows),
                within30=sum(t<=30 for t in rows.values()))


def case(n,width,stroke,rpm=850,lead=3,accel=1000,extra_dock=0):
    kw=dict(rpm=rpm,lead=lead,accel=accel,extra_dock=extra_dock)
    scenes = {k:d for k,d in a.workloads(n).items() if stroke==50 or 'deep:' not in k}
    local = local_cases(n,stroke)
    prep = schedule(a.c.v.s.flat(n,stroke-20),width,**kw)['seconds']
    initial = max(schedule(d,width,**kw)['seconds'] for k,d in scenes.items() if k.startswith('ground>'))
    return dict(n=n,width=width,stroke=stroke,rpm=rpm,lead=lead,
                scene=summarize(scenes,width,**kw),local=summarize(local,width,**kw),
                cold_neutral_s=prep,cold_first_s=prep+initial,
                dense_s=schedule(a.c.v.s.flat(n,stroke),width,**kw)['seconds'],**cost(n,width))


def checks():
    replay = 0
    # Independent exact interval set-cover oracle checks all small binary rows.
    for n in range(1,8):
        for width in range(1,n+1):
            for bits in itertools.product((0,1),repeat=n):
                d=[list(bits)]+[[0]*n for _ in range(n-1)]
                got=stations(d,width)
                wanted={i for i,b in enumerate(bits) if b}
                covers=[set(range(x,x+width)) for x in range(n-width+1)]
                best=0 if not wanted else next(k for k in range(1,n+1)
                     if any(wanted<=set().union(*c) for c in itertools.combinations(covers,k)))
                assert len(got)==best
                replay+=1
    anchors = 0
    for n in (64,80):
        for d in a.workloads(n).values():
            for width in (8,16,32,n):
                path=stations(d,width);seen={}
                for x0,y,items in path:
                    assert 0<=x0<=n-width
                    for x,v in items:
                        assert x0<=x<x0+width and (x,y) not in seen
                        seen[x,y]=v
                assert seen=={(x,y):v for y,row in enumerate(d) for x,v in enumerate(row) if v}
                got=schedule(d,width)
                reverse=schedule([[-v for v in row] for row in d],width)
                assert got['seconds']==reverse['seconds']
                assert got['raised_cells']==reverse['lowered_cells']
                assert got['lowered_cells']==reverse['raised_cells']
                assert got['changed_cells']+got['unchanged_cells']==n*n
                assert math.isclose(got['seconds'],sum(got[key] for key in
                    ('seek_s','return_s','dock_proof_s','spin_s','retry_s','common_s')))
                assert got['seeks']==got['dock_cycles']==got['stations']
            for lead in (2,3):
                ref=a.schedule(d,n,850,lead=lead,banks=1)['feasible_s']
                assert math.isclose(schedule(d,n,lead=lead)['seconds'],ref,abs_tol=1e-9)
                anchors+=1
        assert math.isclose(cost(n,n)['subset_plus_reserve_USD'],f.cost(n,1)['subset_plus_reserve_USD'])
        for stroke in (40,50):
            for width in (8,16,32,n):
                # Exact dense number and independent spin total, including n80/w32.
                got=schedule(a.c.v.s.flat(n,stroke),width)
                count=n*math.ceil(n/width)
                assert got['stations']==count
                assert math.isclose(got['spin_s'],count*a.r.spin(stroke/3,850),abs_tol=1e-8)
                assert schedule(a.c.v.s.flat(n,0),width)['seconds']==0
                assert math.isclose(cost(n,width)['subset_plus_reserve_USD']+
                     width*cost(n,width)['residual_per_output_USD'][500],500)
    # A solid local window fitting the head must not create lateral zigzags.
    for width in (16,32,64):
        d=[[30 if 32<=x<48 and 32<=y<48 else 0 for x in range(64)] for y in range(64)]
        path=stations(d,width)
        assert len(path)==16 and len({x for x,_,_ in path})==1
    # Far-corner singleton: explicitly pay outward/return motion and one retry.
    d=[[0]*64 for _ in range(64)];d[-1][-1]=-30
    got=schedule(d,16); move=a.r.move(63*6.35); spin=a.r.spin(10,850)
    assert math.isclose(got['seconds'],4+2*move+2*(.1+spin))
    assert got['dock_cycles']==got['retry_cycles']==got['lowered_cells']==1
    assert schedule([[0]*64 for _ in range(64)],16)['retry_cycles']==0
    return f'{replay} exhaustive interval covers; {anchors} full-row anchors; signed/cell replay, dense/no-op/cost identities'


def report(verified):
    rows=[case(n,w,s) for n,s in itertools.product((64,80),(40,50)) for w in (8,16,32,n)]
    sensitivity=[case(64,16,50,**kw) for kw in (dict(lead=2),dict(rpm=400),dict(rpm=600),
        dict(accel=200,extra_dock=.1))]
    full_rows=[full_row_local(n,s,b) for n,s,b in itertools.product((64,80),(40,50),(1,2))]
    return dict(verification=verified,rows=rows,sensitivity=sensitivity,
                full_row_local_controls=full_rows)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args(); verified=checks()
    print(verified if args.check else json.dumps(report(verified),indent=2))


if __name__=='__main__':
    main()
