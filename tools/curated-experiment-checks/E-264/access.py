#!/usr/bin/env python3
"""Rotating-nut closed-socket access screen; assumptions, not hardware ratings.

Uses existing physical river/ravine scenes. Sequential Z/Y access, fixed row
banks, conditional independent rotary channels. No generated files are needed.
"""
import argparse
import importlib.util
import itertools
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location('admission', Path(__file__).parents[1]/'E-259/concurrency.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


def move(distance, speed=200, accel=5000):
    assert distance >= 0 and speed > 0 and accel > 0
    return (2*math.sqrt(distance/accel) if distance <= speed*speed/accel
            else distance/speed+speed/accel)


def geometry(stroke, u, span=40):
    # Fixed nut [0,10]; threaded tail has 2-mm end margins at both extremes.
    assert 0 <= u <= stroke
    return dict(thread=(u-stroke-2, u+12), nut=(0,10),
                stem=(u+12, u+stroke+span+16),
                guides=((stroke+14,stroke+16), (stroke+span+14,stroke+span+16)),
                tail_below_nut=stroke+2-u, cap=u+stroke+span+16)


def pairs(n, stroke):
    neutral = stroke-20
    states = {}
    for label, depth in ((('shallow',20),) if stroke == 40 else (('shallow',20),('deep',30))):
        maps, start = a.c.terrain(n, neutral, depth)
        states.update({label+':'+k:maps[k] for k in a.c.v.s.SUITES['relief']})
    result = {'ground>'+k:(start,v) for k,v in states.items()}
    result.update({x+'>'+y:(states[x],states[y]) for x,y in itertools.permutations(states,2)})
    return result


def schedule(before, after, stroke, policy='full', rpm=2000, lead=3,
             speed=200, accel=5000, banks=2, k=32):
    """Sufficient envelope route, not full mechanism or globally optimal schedule.

    Start/end below the longest possible tail. At each row stop rotary motion,
    prove, descend, seek, ascend. Adaptive transit accounts for ALL tails in
    crossed rows, not merely changed outputs. No overlapping Z/Y motion.
    Retry conservatively repeats one row and full-depth exit/re-entry.
    Existing .08 docking/selection + .02 proof allowance stays, unreduced.
    """
    n = len(before)
    assert len(after) == n and all(len(row) == n for row in before+after)
    assert policy in ('full','adaptive','free')
    assert all(0 <= h <= stroke for row in before+after for h in row)
    delta = a.r.delta(before,after)
    width = math.ceil(n/banks)
    times=[]; retry=0.; stations=0; depths=[]
    full = stroke+3  # tail at -(S+2), plus 1-mm axial clearance
    ztime = lambda d: 0. if policy == 'free' else move(d,speed,accel)
    for base in range(0,n,width):
        rows = [y for y in range(base,min(n,base+width)) if any(delta[y])]
        if not rows:
            times.append(0.); continue
        total = ztime(full)*2  # first ascent and last descent, real home state
        last = base
        for index,y in enumerate(rows):
            total += max(.05,a.r.move(abs(y-last)*a.c.v.s.WIDTH/n))
            key=tuple(sorted(abs(d) for d in delta[y] if d))
            dwell=a.row_bounds(key,k,rpm,1000,.02,0,lead)[1]
            total += dwell
            retry=max(retry,dwell+2*ztime(full))
            stations+=1
            if index:
                previous=rows[index-1]
                # Previous row has been written; all following crossed rows
                # still have their original heights at this forward visit.
                lowest=min(min(after[previous]),
                           min(min(before[j]) for j in range(previous+1,y+1)))
                d=full if policy == 'full' else full-lowest
                depths.append(d)
                total += 2*ztime(d)
            last=y
        total += a.r.move((last-base)*a.c.v.s.WIDTH/n)
        times.append(total)
    return dict(seconds=4+max(times)+retry if stations else 0., stations=stations,
                min_transit_mm=min(depths,default=0),max_transit_mm=max(depths,default=0))


def suite(n, stroke, **kw):
    values={key:schedule(x,y,stroke,**kw)['seconds'] for key,(x,y) in pairs(n,stroke).items()}
    worst=max(values,key=values.get)
    flat=a.c.v.s.flat
    return dict(max_s=values[worst],worst=worst,
        prep_s=schedule(flat(n,0),flat(n,stroke-20),stroke,**kw)['seconds'],
        dense_s=schedule(flat(n,0),flat(n,stroke),stroke,**kw)['seconds'])


def section(stroke, E=1000, root=1.4):
    I=math.pi*root**4/64
    length=stroke+4 # nut upper edge to lower guide lower edge
    pinned=math.pi**2*E*I/length**2
    return dict(root_only_pinned_Euler_N=pinned,cantilever_control_N=pinned/4,
                root_EI_Nmm2=E*I,compressed_span_mm=length,
                thread_length_mm=stroke+14,stem_length_mm=stroke+44,
                stock_mm=2*stroke+58,lowest_cap_mm=stroke+56,
                below_low_cap_mm=2*stroke+58)


def checks():
    count=0
    for s in (40,50):
        for u in (i/4 for i in range(4*s+1)):
            g=geometry(s,u); lo,hi=g['thread']
            assert lo<=-2+1e-12 and hi>=12-1e-12
            assert math.isclose(hi-lo,s+14)
            assert all(g['stem'][0]<=l and h<=g['stem'][1] for l,h in g['guides'])
            assert -(s+3)<lo # full-clear plane is below every tail
            count+=1
        # Explicit failed shallow extraction: low tail still crosses socket.
        assert geometry(s,0)['thread'][0] < -2 < 0
        assert math.isclose(section(s,E=2000)['root_only_pinned_Euler_N'],
                            2*section(s)['root_only_pinned_Euler_N'])
        for n in (64,80):
            for x,y in pairs(n,s).values():
                reference=a.schedule(a.r.delta(x,y),32)['feasible_s']
                free=schedule(x,y,s,policy='free')['seconds']
                adaptive=schedule(x,y,s,policy='adaptive')['seconds']
                full=schedule(x,y,s)['seconds']
                assert math.isclose(reference,free,abs_tol=1e-9)
                assert free<=adaptive+1e-9<=full+1e-9
            flat=a.c.v.s.flat
            assert schedule(flat(n,20),flat(n,20),s)['seconds']==0
            # Dense equal jobs/row makes the fixed-access addition exact.
            d=schedule(flat(n,0),flat(n,s),s)['seconds']
            baseline=a.schedule(flat(n,s),32)['feasible_s']
            assert math.isclose(d-baseline,(n//2+1)*2*move(s+3),abs_tol=1e-9)
    # A low unchanged intermediate row forces full clearance on the path.
    x=[[40.]*4 for _ in range(4)]; y=[row[:] for row in x]
    x[1][2]=y[1][2]=0; y[0][0]=y[2][0]=30
    v=schedule(x,y,40,policy='adaptive',banks=1)
    assert v['max_transit_mm']==43
    for d in (0,1,8,9,43,53): assert math.isclose(move(d),a.r.move(d))
    # Annular nominal spacing is a head-only envelope, not mating CAD.
    assert 5.08-5.9<0<6.35-5.9
    return f'{count} axial/guide poses; all inherited scene anchors; no-op/dense/access-order controls; crossed unchanged-tail witness'


def main():
    out=dict(verification=checks(),sections={s:section(s) for s in (40,50)},scenarios=[])
    for n,s in itertools.product((64,80),(40,50)):
        rows={p:suite(n,s,policy=p) for p in ('free','adaptive','full')}
        rows['adaptive_fast_z']=suite(n,s,policy='adaptive',speed=400,accel=8000)
        rows['slow_rotating_screw_850']=dict(max_s=max(a.schedule(a.r.delta(x,y),32,rpm=850)['feasible_s'] for x,y in pairs(n,s).values()))
        rows['lead2_adaptive']=suite(n,s,policy='adaptive',lead=2)
        out['scenarios'].append(dict(n=n,stroke=s,**rows))
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true')
    if p.parse_args().check: print(checks())
    else: main()
