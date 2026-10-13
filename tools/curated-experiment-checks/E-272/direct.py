#!/usr/bin/env python3
"""Spaced direct drives: finite envelopes and conditional workload replay.

No rated RPM, calibrated process distribution, optical decoder or hardware pass.
All geometry except catalog motor envelope and all non-catalog costs are bounds.
"""
import argparse
import functools
import importlib.util
import itertools
import json
import math
from pathlib import Path


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).resolve().parents[1]/relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h = load('short_head', 'E-267/screen.py')
r = load('routing', 'E-271/routing.py')
# Rasterization is invariant across head comparisons; cached arrays are read-only.
h.a.c.terrain = functools.lru_cache(None)(h.a.c.terrain)
h.local_cases = functools.lru_cache(None)(h.local_cases)
h.a.workloads = functools.lru_cache(None)(h.a.workloads)
SHAPES = {1: (1, 1), 2: (2, 1), 4: (2, 2), 8: (4, 2)}


def layout(n, k, mode='compact'):
    nx, ny = SHAPES[k]
    sx, sy = (n//16, n//16) if mode == 'compact' else (n//nx, n//ny)
    return nx, ny, sx, sy


def stations(delta, k, mode='compact'):
    """Greedy rectangle cover in each residue class; each change written once.

    Direct tips at (i*sx,j*sy). Group identical residues then greedily cover
    their coarse lattice. Rectangles may overlap but already-written cells
    are never selected again. This is constructive, not an optimum.
    Unchanged members stay parked. All tips remain inside the board.
    """
    n = len(delta)
    nx, ny, sx, sy = layout(n, k, mode)
    residues = {}
    for y, row in enumerate(delta):
        for x, d in enumerate(row):
            if d:
                px, py = x % sx, y % sy
                residues.setdefault((px,py), {})[(x//sx,y//sy)] = (x,y,d)
    out = []
    for (px,py),remaining in residues.items():
        for u,v in sorted(remaining,key=lambda p:(p[1],p[0])):
            if (u,v) not in remaining:
                continue
            ax,ay = min(u,n//sx-nx),min(v,n//sy-ny)
            chosen = [(x,y) for y,x in itertools.product(range(ay,ay+ny),range(ax,ax+nx))
                      if (x,y) in remaining]
            out.append((ax*sx+px,ay*sy+py,tuple(remaining.pop(p) for p in chosen)))
    return out


def schedule(delta, k, stroke, mode='compact', rpm=850, lead=3, overhead=.38):
    n = len(delta)
    pitch = 406.4/n
    jobs = stations(delta, k, mode)
    changed = [(x,y,d) for y,row in enumerate(delta) for x,d in enumerate(row) if d]
    if not jobs:
        return dict(seconds=0., stations=0, changed=0, raised=0, lowered=0,
                    unchanged=n*n, work_lower_s=0., transaction_lower_s=0., first_seek_s=0.)
    xs = {x:i for i,x in enumerate(sorted({j[0] for j in jobs}))}
    ys = {y:i for i,y in enumerate(sorted({j[1] for j in jobs}))}
    paths = [sorted(jobs, key=lambda j:(j[1], j[0] if ys[j[1]]%2==0 else -j[0])),
             sorted(jobs, key=lambda j:(j[0], j[1] if xs[j[0]]%2==0 else -j[1]))]

    def journey(path):
        pos = (0,0)
        total = first = 0.
        for index,(x,y,_) in enumerate(path):
            seek = max(.05, h.a.r.move(abs(x-pos[0])*pitch), h.a.r.move(abs(y-pos[1])*pitch))
            if index == 0:
                first = seek
            total += seek
            pos = x,y
        ret = max(h.a.r.move(pos[0]*pitch), h.a.r.move(pos[1]*pitch))
        return total, ret, first

    path = min(paths, key=lambda p:sum(journey(p)[:2]))
    seek, ret, first = journey(path)
    spin = sum(h.a.r.spin(max(abs(d) for _,_,d in cells)/lead, rpm) for _,_,cells in path)
    # Immediate retry after fresh stable actual height; no replay of stale delta.
    # Unknown/covered/broken cases are outside this successful single-retry bound.
    retry = overhead+h.a.r.spin(stroke/lead, rpm)
    common = 5.  # inherited4 + 1 shared top-reader deployment/parking
    dock_read = len(path)*overhead
    work = sum(h.a.r.spin(abs(d)/lead, rpm) for _,_,d in changed)
    return dict(seconds=common+seek+ret+spin+dock_read+retry, stations=len(path),
                changed=len(changed), raised=sum(d>0 for _,_,d in changed),
                lowered=sum(d<0 for _,_,d in changed), unchanged=n*n-len(changed),
                resident_rows=len({y for _,y,_ in changed}), seek_s=seek, return_s=ret,
                first_seek_s=first, spin_s=spin, dock_read_s=dock_read,
                retry_s=retry, common_s=common, work_lower_s=work/k,
                transaction_lower_s=common+retry+work/k+(overhead+.05)*math.ceil(len(changed)/k),
                utilization=len(changed)/(k*len(path)))


def envelope(n, k, mode='compact', e=.2, spacing_override=None):
    nx, ny, sx, sy = layout(n,k,mode)
    px, py = sx*406.4/n, sy*406.4/n
    if spacing_override is not None:
        px = py = spacing_override
    parts = []
    for j,i in itertools.product(range(ny), range(nx)):
        c = j*nx+i
        x,y = i*px,j*py
        # Swept entire motor/guide/selector carrier, not its internal assembly.
        parts += [r.box(c,'carrier_harness',x-11,x+11,y-12,y+12,-96,-7),
                  r.box(c,'direct_shaft_tip',x-1.5,x+1.5,y-1.5,y+1.5,-10,2)]
    return dict(conflicts=len(r.conflicts(parts,e)),
                neighbor_margin_mm=min((r.gap(a,b)-2*e for a,b in itertools.combinations(parts,2)
                                        if a['channel']!=b['channel']), default=None),
                head_mm=[(nx-1)*px+34,(ny-1)*py+34,116],
                # Side electronics tray/harness adds60mm on Y; limits/enclosure additional.
                motion_union_mm=[406.4-406.4/n+34,406.4-406.4/n+94,116],
                parked_gap_mm=1-2*e, effective_insertion_mm=2-2*e,
                neighbor_socket_gap_mm=406.4/n-1.5-2.2-2*e)


def cost(n,k):
    # 2026-10-13 catalog price tiers; allocations are not quotes or price floors.
    catalog = dict(motors=k*(29.85 if k>=5 else 32.45),
                   encoder_cables=k*(2.76 if k>=5 else 3.), dual_bridges=math.ceil(k/2)*5.95,
                   docking_solenoids=k*4.95)
    allocations = dict(
        short_coupler_tip_two_bushings=(k,2.5,7),
        carrier_guides_stops_return_mount=(k,3,8),
        selector_MOSFET_flyback=(k,1,2),
        harness_connectors_strain_relief=(k,1.5,4),
        two_docking_state_switches=(k,2,4),
        precision_plate_jig=(1,30+5*(k-1),80+12*(k-1)),
        head_distribution_capture=(1,15+2*(k-1),40+5*(k-1)),
        XY_guides_drives_limits=(1,120,240), chassis_service=(1,35,75),
        power_protection_cooling=(1,30+4*(k-1),60+8*(k-1)), controller=(1,35,70),
        resident_support=(n*n,.02,.08), actual_cap_reader=(1,80,250),
        reader_mount_carrier=(1,80,180),
        extra_simultaneous_reader_paths=(k-1,5,20))
    pre = [sum(catalog.values())+sum(q*v[j] for q,*v in allocations.values()) for j in (0,1)]
    bought = [1.10*pre[0]+20,1.15*pre[1]+60]
    hours = [8+n*n*8/3600+k/6,16+n*n*20/3600+k/2]
    return dict(catalog_USD=catalog,allocations_q_low_high=allocations,
                bought_USD=bought,residuals={b:[b-c for c in bought] for b in (500,1000,1500)},
                maker_hours=hours,printing_material_USD=[60,160],
                all_in_at_20_USD_hour=[bought[j]+[60,160][j]+20*hours[j] for j in (0,1)],
                selector_W=5.5*k, motor_stall_A=1.5*k, max_channel_conductors=12*k)


def summary(cases,k,stroke,**kw):
    rows = {name:schedule(d,k,stroke,**kw) for name,d in cases.items() if any(map(any,d))}
    worst = max(rows,key=lambda key:rows[key]['seconds'])
    return dict(worst=worst,max_s=rows[worst]['seconds'],worst_ledger=rows[worst],
                nonempty=len(rows),within30=sum(v['seconds']<=30 for v in rows.values()),
                max_work_lower_s=max(v['work_lower_s'] for v in rows.values()),
                max_transaction_lower_s=max(v['transaction_lower_s'] for v in rows.values()),
                known_preposition_max_s=max(v['seconds']-v['first_seek_s'] for v in rows.values()))


def small_cases(n):
    # Synthetic tasks, not claimed observed player practice; near/far and tile edges.
    s = n//16
    out = {}
    for count in (1,s,2*s):
        for vertical in (False,True):
            for start in (0,s-1,n-2*s):
                d = [[0]*n for _ in range(n)]
                for t in range(count):
                    x,y = (start,start+t) if vertical else (start+t,start)
                    d[y][x] = -20 if count==2*s else 20
                out[f'{count}-cells:{vertical}:{start}'] = d
    return out


def report_case(n,k,stroke,mode='compact',rpm=850,lead=3):
    kw=dict(mode=mode,rpm=rpm,lead=lead)
    scenes={name:d for name,d in h.a.workloads(n).items() if stroke==50 or 'deep:' not in name}
    local=summary(h.local_cases(n,stroke),k,stroke,**kw)
    # Initial minimum-rest control: same relative shape as raised-neutral final map.
    targets,_=h.a.c.terrain(n,stroke-20,stroke-20)
    ground=h.a.c.v.s.flat(n,stroke-20)
    initial={name:h.a.r.delta(ground,targets[name]) for name in h.a.c.v.s.SUITES['relief']}
    direct={name:targets[name] for name in h.a.c.v.s.SUITES['relief']}
    prep=schedule(ground,k,stroke,**kw)['seconds']
    small=small_cases(n)
    return dict(n=n,k=k,stroke=stroke,mode=mode,rpm=rpm,lead=lead,local=local,
                scenes=summary(scenes,k,stroke,**kw),cold_neutral_s=prep,
                cold_first_s=prep+summary(initial,k,stroke,**kw)['max_s'],
                minimum_rest_first_s=summary(direct,k,stroke,**kw)['max_s'],
                dense_s=schedule(h.a.c.v.s.flat(n,stroke),k,stroke,**kw)['seconds'],
                small={count:summary({name:d for name,d in small.items() if name.startswith(str(count)+'-')},
                                    k,stroke,**kw)['max_s'] for count in (1,n//16,n//8)})


def checks():
    replays = 0
    # Independent cell-level replay includes signs and arbitrary masks.
    for n,k,mode in itertools.product((16,32,64,80),SHAPES,('compact','spread')):
        nx,ny,sx,sy=layout(n,k,mode)
        for d in ([[(-1)**(x+y)*(1+(x+3*y)%7) if (x+2*y)%3 else 0 for x in range(n)] for y in range(n)],
                  [[50]*n for _ in range(n)]):
            seen={}
            for ax,ay,items in stations(d,k,mode):
                assert 0<=ax<=n-1-(nx-1)*sx and 0<=ay<=n-1-(ny-1)*sy
                for x,y,value in items:
                    assert x-ax in range(0,nx*sx,sx) and y-ay in range(0,ny*sy,sy)
                    assert (x,y) not in seen
                    seen[x,y]=value
            assert seen=={(x,y):v for y,row in enumerate(d) for x,v in enumerate(row) if v}
            got=schedule(d,k,50,mode)
            assert got['seconds']>=got['work_lower_s']
            assert got['seconds']+1e-8>=got['transaction_lower_s']
            assert math.isclose(got['seconds'],sum(got[key] for key in
                                ('seek_s','return_s','spin_s','dock_read_s','retry_s','common_s')))
            assert got['changed']+got['unchanged']==n*n
            assert math.isclose(got['seconds'],schedule([[-v for v in row] for row in d],k,50,mode)['seconds'])
            replays+=1
        dense=schedule([[50]*n for _ in range(n)],k,50,mode)
        assert dense['stations']==n*n//k
        assert math.isclose(dense['spin_s'],n*n/k*h.a.r.spin(50/3,850),rel_tol=1e-10)
        assert schedule([[0]*n for _ in range(n)],k,50,mode)['seconds']==0
    for n,k in itertools.product((64,80),SHAPES):
        for mode in ('compact','spread'):
            assert envelope(n,k,mode,e=.4)['conflicts']==0
        if k>1:
            assert envelope(n,k,spacing_override=406.4/n)['conflicts']>0
        assert envelope(n,k,e=.6)['parked_gap_mm']<0
        for b,values in cost(n,k)['residuals'].items():
            assert all(math.isclose(v+c,b) for v,c in zip(values,cost(n,k)['bought_USD']))
    # Serial schedule anchors against prior independently constructed station path.
    d=[[0]*64 for _ in range(64)];d[-1][-1]=-20
    got=schedule(d,1,50)
    expected=5+2*h.a.r.move(63*6.35)+.38+h.a.r.spin(20/3,850)+.38+h.a.r.spin(50/3,850)
    assert math.isclose(got['seconds'],expected)
    # Private-quadrant drives cannot speed a local window lying entirely in one quadrant.
    # This is a work lower bound even granting free collision-free travel and readback.
    q=[[30 if 8<=x<24 and 8<=y<24 else 0 for x in range(64)] for y in range(64)]
    quadrant_work=sum(h.a.r.spin(v/3,850) for row in q for v in row if v)
    assert quadrant_work>180
    return dict(replays=replays,checks='cell reach/isolation, dense closed form, signed/no-op, finite collisions, budget and serial anchor')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    verified=checks()
    if args.check:
        print(json.dumps(verified))
    else:
        print(json.dumps(dict(verification=verified,
            rows=[report_case(n,k,stroke,mode) for n,stroke,k,mode in
                  itertools.product((64,80),(40,50),SHAPES,('compact','spread'))],
            sensitivity=[report_case(64,k,50,rpm=rpm,lead=lead) for k,rpm,lead in
                         itertools.product((1,4,8),(400,850),(2,3))],
            geometry=[dict(n=n,k=k,mode=mode,**envelope(n,k,mode)) for n,k,mode in
                      itertools.product((64,80),SHAPES,('compact','spread'))],
            costs=[dict(n=n,k=k,**cost(n,k)) for n,k in itertools.product((64,80),SHAPES)]),indent=2))
