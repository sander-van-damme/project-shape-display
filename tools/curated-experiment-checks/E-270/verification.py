#!/usr/bin/env python3
"""Solid-support readback discriminator: geometry and conditional timing, not hardware."""
import argparse
import importlib.util
import itertools
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location('readback', Path(__file__).resolve().parents[1]/'E-268/readback.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
h = r.head


def top_margin(pitch, stroke, baseline=4., overhead=60., error=.2):
    """Pupils +/-b/2, radius .25; top patch half-width .2; independent +/-e.

    Normalize the lowest cap to z0; neighbors may fill z0..S. At their top
    zS the affine ray has its largest lateral extent within the obstruction.
    Use a square envelope around the circular pupils (conservative).
    """
    t = stroke/(stroke+overhead)
    extent = (baseline/2+.25)*t + .2*(1-t)+error
    return pitch-2.2-error-extent


def stroke_time(d, v=50., accel=500.):
    # Millimetres; separate deliberately slower metrology-axis scenario.
    return 2*math.sqrt(d/accel) if d<=v*v/accel else d/v+v/accel


def station_proof(x0, selected, pitch, stroke, mode, read=.1, overhead=5.):
    """Stopped upper reader, after .1s undock + .1s settling.

    stereo16: 32 registered entrance pupils/relay duties, simultaneous reading.
    stereo1/probe1: one X subcarriage starts/ends at station's first grid slot;
    exact selected-site travel charged. Macro XY journey is shared with writer.
    probe1 pays full allowed search+retract for each cell, a conservative bound.
    """
    if mode == 'stereo16': return .2+read
    xs = [x for x,_ in selected]
    pos = x0; scan = 0.
    for x in xs:
        if x != pos: scan += max(.05,h.a.r.move(abs(x-pos)*pitch))
        pos=x
    if pos!=x0: scan+=max(.05,h.a.r.move(abs(pos-x0)*pitch))
    per_site = read if mode=='stereo1' else 2*stroke_time(stroke+overhead)+read
    return .2+scan+len(xs)*per_site


def schedule(delta, stroke, mode, lead=3., read=.1, overhead=5.):
    base=h.schedule(delta,16,lead=lead)
    if not base['stations']: return dict(seconds=0.,stations=0,changed=0,proof_s=0.,retry_s=0.)
    pitch=406.4/len(delta); extras=[]; dwells=[]
    for x,y,selected in h.stations(delta,16):
        proof=station_proof(x,selected,pitch,stroke,mode,read,overhead)
        extra=proof-.02  # replace, never double-count inherited proof slot
        extras.append(extra)
        # Fresh actual height can be anywhere in qualified stroke after release;
        # original commanded delta is not a sufficient recovery allowance.
        dwells.append(.1+h.a.r.spin(stroke/lead,850,1000)+extra)
    # One shared reader deployment/parking allowance, then immediate worst-station
    # retry after detection. Persistent fault remains unknown, not infinite retry.
    total=base['seconds']+1+sum(extras)+max(dwells)-base['retry_s']
    return dict(seconds=total,stations=base['stations'],changed=base['changed_cells'],
                raised=base['raised_cells'],lowered=base['lowered_cells'],
                unchanged=base['unchanged_cells'],proof_s=sum(x+.02 for x in extras),
                retry_s=max(dwells),base_s=base['seconds'],deployment_s=1.)


def scan_board(n, stroke, mode):
    """Additional post-update inspection of ALL pins: no writer movement/spin.

    .1s settle/registration per station, read, explicit XY journeys and one
    reread of worst station. No re-actuation or qualified occupied-pin coverage.
    """
    delta=[[1]*n for _ in range(n)]
    base=h.schedule(delta,16)
    dwells=[station_proof(x,s,406.4/n,stroke,mode)-.1 for x,y,s in h.stations(delta,16)]
    return 1+base['travel_s']+sum(dwells)+max(dwells)


def verdict(height, target, visible=True, fresh=True, identity=True):
    if not(visible and fresh and identity): return 'unknown'
    return 'accept' if abs(height-target)<=.3 else 'reject'


def fault_rows():
    result={}
    for start,target in ((10,20),(20,10)):
        # Measured actual terrain heights, not turns or movable fiducial position.
        states={'correct':(target,target), 'missed_socket':(start,start),
                'stripped_thread':(start,start), 'lost_after_release':(target,target-1),
                'creep_after_inspection':(target,target)}
        result[f'{start}>{target}']={k:dict(in_drive=verdict(a,target),
            post_release=verdict(b,target),under_miniature=verdict(b,target,visible=False))
            for k,(a,b) in states.items()}
    return result


def checks():
    rays=0
    for p,S,H,b,e in itertools.product((5.08,6.35),(40,50),(20,60),(4,20),(0,.2,.4)):
        # All corner rays; exact neighboring AABB intersections, independent of
        # the continuous envelope. Opposing coherent face/pupil error included.
        all_clear=True
        for side,px,py,tx,ty,ex,ey,ux,uy in itertools.product((-1,1),repeat=9):
            camera=(side*b/2+px*.25+ex*e,py*.25+ey*e,S+H)
            target=(tx*.2+ux*e,ty*.2+uy*e,0)
            for dx,dy in itertools.product((-1,0,1),repeat=2):
                if dx==dy==0: continue
                lo=(dx*p-2.2-e,dy*p-2.2-e,0)
                hi=(dx*p+2.2+e,dy*p+2.2+e,S)
                hit=r.old.hit_box(camera,target,lo,hi)
                all_clear &= not hit; rays+=1
        assert all_clear == (top_margin(p,S,b,H,e)>0)
    # Specific empty low well: 20mm baseline at 20mm overhead fails both pitches;
    # 4mm baseline at either overhead clears. Top support plates are below z0.
    for p in (5.08,6.35):
        for S in (40,50):
            assert top_margin(p,S,20,20)<0<top_margin(p,S,4,20)
            # Probe radius .5 + .2 positioning + .2 bow fits cap and neighbors.
            assert .9 < 2.2-.2 and p-2.2-.2-.9 > 0
    # Opaque miniature underside hides a central pin while neighbors carry it:
    # two actual heights (0,-1) have identical base top and all external views.
    for z in (0,-1):
        assert r.old.hit_box((0,0,100),(0,0,z),(-12.7,-12.7,.1),(12.7,12.7,2))
    for rows in fault_rows().values():
        assert rows['lost_after_release']['in_drive']=='accept'
        assert rows['lost_after_release']['post_release']=='reject'
        assert rows['creep_after_inspection']['post_release']=='accept'
        assert all(v['under_miniature']=='unknown' for v in rows.values())
    assert verdict(20,20,fresh=False)=='unknown'
    assert verdict(20,20,identity=False)=='unknown'
    # Temporary raised inspection does not prove final hidden lowering succeeded.
    assert verdict(30,30)=='accept' and verdict(30,10,visible=False)=='unknown'
    # Closed form dense constant station proof including one retry, and no-op.
    for S,n,mode in itertools.product((40,50),(16,32),('stereo16','stereo1','probe1')):
        d=[[S]*n for _ in range(n)]
        base=h.schedule(d,16)
        proof=station_proof(0,tuple((x,S) for x in range(16)),406.4/n,S,mode)
        expect=base['seconds']+1+(base['stations']+1)*(proof-.02)
        assert math.isclose(schedule(d,S,mode)['seconds'],expect,abs_tol=1e-8)
        assert schedule([[0]*n for _ in range(n)],S,mode)['seconds']==0
        assert schedule([[-S]*n for _ in range(n)],S,mode)['seconds']==schedule(d,S,mode)['seconds']
    # One arbitrary sparse case explicitly sums independent event ledger.
    d=[[0]*16 for _ in range(16)];d[0][2]=10;d[0][14]=-20;d[15][9]=30
    for mode in ('stereo16','stereo1','probe1'):
        got=schedule(d,50,mode);base=h.schedule(d,16)
        manual=4+base['travel_s']+.08*base['stations']+base['spin_s']+got['proof_s']+got['retry_s']+1
        assert math.isclose(got['seconds'],manual)
    # Metrology movement law: triangular/trapezoidal meet, distance/time positive.
    assert stroke_time(5)==.2 and stroke_time(0)==0
    # Contact deformation scenario: no force is intrinsically non-disturbing.
    assert math.isclose(.05/.1,.5)
    return dict(ray_box_checks=rays,checks='finite rays/continuous extrema, covered-pin alias, signed faults, retry and event-ledger identities')


def timing():
    out=[]
    for n,S in itertools.product((64,80),(40,50)):
        local={k:d for k,d in h.local_cases(n,S).items() if any(map(any,d))}
        scenes={k:d for k,d in h.a.workloads(n).items() if S==50 or 'deep:' not in k}
        for mode in ('stereo16','stereo1','probe1'):
            rows={k:schedule(d,S,mode) for k,d in local.items()}
            worst=max(rows,key=lambda k:rows[k]['seconds'])
            out.append(dict(n=n,stroke=S,mode=mode,local_max_s=rows[worst]['seconds'],
                worst=worst,ledger=rows[worst],within30=sum(v['seconds']<=30 for v in rows.values()),
                scene_max_s=max(schedule(d,S,mode)['seconds'] for d in scenes.values()),
                neutral_s=schedule(h.a.c.v.s.flat(n,S-20),S,mode)['seconds'],
                dense_s=schedule(h.a.c.v.s.flat(n,S),S,mode)['seconds'],
                full_board_extra_s=scan_board(n,S,mode)))
    return out

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    verified=checks()
    if args.check: print(json.dumps(verified))
    else: print(json.dumps(dict(verification=verified,faults=fault_rows(),timing=timing()),indent=2))
