#!/usr/bin/env python3
"""E-251: shared staggered carriers; bounded geometry/schedule, not hardware.
All rates, errors, force and dollar allocations are assumptions. Stdlib only.
"""
import importlib.util
import itertools as it
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load(name, file):
    s = importlib.util.spec_from_file_location(name, ROOT / file)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m
c = load('e236', 'E-236/screen.py')
g = load('e167', 'E-167/probe.py')
move = c.move
P, CAP, LUG, BASE, D = 5.08, 2., 1.2, 1.2, 10.
PHASES = (3.2, 6.4)

def angular(d=90, v=720, a=7200):
    return 2*math.sqrt(d/a) if d <= v*v/a else d/v+v/a

def phase_margin(s1, s2, error=0, spacing=D):
    # U/active cap gaps, opposite-color cap gap and next-lug/rail gap.
    return min(s1-CAP, s2-s1-CAP, spacing-s2-LUG-BASE)-error

def phase_optimum(spacing, error):
    # Maximize common slack over three disjoint intervals; sum gives upper bound.
    margin=(spacing-2*CAP-LUG-BASE)/3-error
    s1=CAP+error+margin; s2=2*s1
    return dict(spacing_mm=spacing,error_mm=error,phases_mm=[s1,s2],margin_mm=margin)

def z_overlap(a,b):
    return min(a+CAP,b+CAP) > max(a,b)+1e-9

def geometry(n):
    # Enumerate rotations, all old heights, active/unchanged, adjacent and diagonal.
    # At turns all active banks share stroke phase and integer heights.
    checks=0
    for dx,dy in ((1,0),(0,1),(1,1),(2,0)):
        for h0,h1,on0,on1 in it.product(range(5),range(5),(0,1),(0,1)):
            color1=(dx+dy)%2
            z0=10*h0+PHASES[0]*on0
            z1=10*h1+PHASES[color1]*on1
            for k in range(n+1):
                a=math.pi*k/(2*n)
                pa=g.rectangle(2.4,2.4,a*on0)
                pb=g.rectangle(2.4,2.4,a*on1,dx*P,dy*P)
                assert not (z_overlap(z0,z1) and g.intersect(pa,pb))
                checks+=1
    # Same-phase adjacent selected caps DO intersect at the midturn.
    assert g.intersect(g.rectangle(2.4,2.4,math.pi/4),
                       g.rectangle(2.4,2.4,math.pi/4,P,0))
    # Off-grid neighbor during independent bank motion defeats phase proof.
    assert z_overlap(3.2,3.2) and g.intersect(
        g.rectangle(2.4,2.4,math.pi/4),g.rectangle(2.4,2.4,math.pi/2,P,0))
    # Same-color diagonal clearance has an angle-independent circumcircle bound.
    assert math.sqrt(2)*P > 4.8*math.sqrt(2)
    # Aligned caps during lift/lower/translation have XY clearance, any heights.
    assert not g.intersect(g.rectangle(2.4,2.4),g.rectangle(2.4,2.4,dx=P))
    # At rotation, next lower lug must be below base; current lug is above it.
    for s in PHASES:
        assert s > CAP and s-D+LUG < -BASE
    return checks

def overhead(mode='staggered', proof=.003, throw=2, yaw_factor=1):
    # Sequential: write, capture, lift, turn, move, return turn, seat, detach.
    # The move duration is counted separately; all eight stages owe proof.
    lift = PHASES[1] if mode=='staggered' else PHASES[0]
    return 3*move(throw)+2*move(lift)+2*angular()/yaw_factor+8*proof

def row_time(seq, mode='staggered', **kw):
    pulse=sum(move(10*abs(d)) for d in seq)+len(seq)*overhead(mode,**kw)
    return pulse*(2 if mode=='serial' else 1)+move(P)

def schedule(seq,banks,mode='staggered',rows=None,**kw):
    # One stable-state retry; reset empty pickup after partial completed pulses.
    q=list(it.accumulate(seq,initial=0))
    recovery=move(10*max(abs(x) for x in q))+.010
    visits=math.ceil(80/banks) if rows is None else rows
    return 2+recovery+(visits+1)*row_time(seq,mode,**kw)

def first(seq,mode,**kw):
    for b in range(1,81):
        t=schedule(seq,b,mode,**kw)
        if t<30:
            # Favorable reuse of E-236 shared allocation, adding NO extra cost
            # for second carrier or yaw. Explicit relaxed comparator only.
            cost=195+20*b+.52*80*b
            return dict(banks=b,channels=80*b,map_s=t,row_s=row_time(seq,mode,**kw),
                        relaxed_dollars=cost,remaining_per_channel=(500-195-20*b)/(80*b))
    return None

def synthesize():
    counts=[]; candidates=[]
    for n in range(2,6):
        tested=reachable=retained=0
        for middle in it.product(range(-4,1),repeat=n-1):
            q=(0,)+middle+(0,)
            seq=tuple(b-a for a,b in zip(q,q[1:]))
            if 0 in seq: continue
            tested+=1
            if not all(len(c.reachable(seq,h))==5 for h in range(5)): continue
            reachable+=1
            table=c.codes(seq,6)
            if table is None: continue
            retained+=1
            candidates.append((row_time(seq),max(abs(x) for x in q),seq))
        counts.append(dict(pulses=n,tested=tested,reachable=reachable,seven_lugs=retained))
    winner=min(candidates)[2]
    # For any n>=6 at least 80mm total motion and n acceleration penalties;
    # same per-pulse transaction assumed. This is grammar-local optimality.
    assert .4+6*.025+6*overhead()+move(P) > row_time(winner)
    return counts,winner

def replay(seq, table):
    count=observations=0
    for old,target in it.product(it.product(range(5),repeat=3),repeat=2):
        h=list(old); q=0
        masks=[table[a,b][2] for a,b in zip(old,target)]
        for j,d in enumerate(seq):
            mask=[bits[j] for bits in masks]
            # Ideal support only. Ground stays installed; only selected columns
            # release it after bilateral capture. Loaded capture is an oracle.
            for i,on in enumerate(mask):
                if on: assert 0 <= 2+h[i]-q <= 6
            for stage in ('capture','lift','turn','travel','return_turn','seat','detach'):
                if stage=='travel': h=[v+d*on for v,on in zip(h,mask)]
                ground=[stage in ('capture','seat','detach') or not on for on in mask]
                capture=[bool(on) and stage!='detach' for on in mask]
                assert all(a or b for a,b in zip(ground,capture))
                assert all(v in range(5) for v in h) # height codes, not release lift
                assert all(a!=b or v==a for a,b,v in zip(old,target,h))
                observations+=1
            q+=d
        assert h==list(target) and q==0
        count+=1
    return dict(maps=count,support_states=observations)

def main():
    counts,seq=synthesize(); table=c.codes(seq,6)
    assert all(len(c.reachable(seq,h))==5 for h in range(5))
    # Independent interval-sum upper bound, and actual margins at optimizer.
    sensitivities=[]
    for spacing,error in it.product((5,7.5,10), (0,.35,.7,1.2)):
        opt=phase_optimum(spacing,error)
        assert abs(phase_margin(*opt['phases_mm'],error,spacing)-opt['margin_mm'])<1e-9
        sensitivities.append(opt)
    # Nominal material-volume union, NOT a strength-qualified embodiment.
    primitive=lambda y: .5*(y*math.sqrt(.8**2-y*y)+.8**2*math.asin(y/.8))
    overlap=2*(primitive(.4)-.6*.4)
    volume=(math.pi*.8**2*102+4.8**2*2+7*1.2*(1.4*.8-overlap))*6400/1e6
    cases={mode:first(seq,mode) for mode in ('staggered','serial','single_oracle')}
    # Stronger relaxed bound: all writing, capture, lift, seat, proof FREE.
    # Merely return-turning on five pulses plus required motion, feed/retry.
    free_row=sum(move(10*abs(d)) for d in seq)+10*angular()+move(P)
    recovery=move(10*max(abs(q) for q in it.accumulate(seq,initial=0)))+.010
    bfree=next(b for b in range(1,81) if 2+recovery+(math.ceil(80/b)+1)*free_row<30)
    # Sensitivity doubles angular speed AND acceleration (time factor is not 2).
    factor=angular()/angular(v=1440,a=14400)
    direct_slot=2*move(40+PHASES[1])+2*move(PHASES[1])+move(40)+2*angular()+.1+move(P)
    direct_b=next(b for b in range(1,81) if 2+(math.ceil(80/b)+1)*direct_slot<30)
    forces=[]
    b=cases['staggered']['banks']
    for load in (.1,1,10):
        # Payload load is force; column mass separately charged only for inertia.
        F=80*b*load+(80*b*.003+2*b*.25)*8+2*b*.25*9.81
        forces.append(dict(payload_N_per_cell=load,force_N=F,torque_Nm=F*.01,input_W=F*.2/.7))
    print(json.dumps(dict(search=counts,seq=seq,geometry=[dict(subdivisions=n,checks=geometry(n)) for n in (16,64)],
        phase_sensitivity=sensitivities,replay=replay(seq,table),timing=cases,
        solid_column_liters=volume,extrusion_hours=[volume*1e6/(r*3600) for r in (15,5)],
        overhead_s=overhead(),free_non_yaw_oracle=dict(banks=bfree,channels=80*bfree,
            map_s=2+recovery+(math.ceil(80/bfree)+1)*free_row,
            relaxed_dollars=195+20*bfree+.52*80*bfree),
        direct_staggered_control=dict(banks=direct_b,pairs=80*direct_b,
            map_s=2+(math.ceil(80/direct_b)+1)*direct_slot,
            allowance_per_pair=(500-295)/(80*direct_b)),
        doubled_angular_rates=first(seq,'staggered',yaw_factor=factor),
        sensitivity=[dict(proof_s=p,throw_mm=d,**first(seq,'staggered',proof=p,throw=d))
                     for p,d in it.product((0,.003,.01),(1,2,4))],
        regional_one_row_s=schedule(seq,b,rows=1),regional_five_rows_s=schedule(seq,b,rows=5),
        forces=forces,cap_transient_max_mm=40+PHASES[1],
        head_contact_top_mm=-20+PHASES[1],writes_per_map=6400*len(seq),
        ledger=dict(banks=b,carriers=2*b,captures=80*b,retained_bits=80*b,
                    fixed_lugs=7*6400,column_guides=2*6400,command_endpoints=160*b,
                    channels=80*b)),indent=2))
if __name__=='__main__': main()
