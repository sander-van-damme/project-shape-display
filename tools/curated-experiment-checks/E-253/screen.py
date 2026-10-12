#!/usr/bin/env python3
"""E-253: offset-radius shared crank, stdlib and labelled scenario bounds.
No physical validation. stdout only; no guessed manufacturing probabilities.
"""
import importlib.util
import itertools as it
import json
import math
from pathlib import Path

spec=importlib.util.spec_from_file_location('e251',Path(__file__).resolve().parents[1]/'E-251/screen.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
move=p.move
Q=(1,2,4,5,8,10,16,20,40,80)
LEVELS=(0,10,20,30,40)


def geometry(degrees, gap=8., frame=4.):
    a=math.radians(degrees)
    rmin=gap/math.cos(a)
    span=80/math.sin(a)
    rmid=rmin+span/2
    rmax=rmin+span
    return dict(angle_deg=degrees,angle_rad=a,rmin=rmin,rmid=rmid,rmax=rmax,
                span=span,pitch=span/8,width=rmax+frame,
                compensation=rmid*math.sin(a),bank_cap=math.floor(406.4/(rmax+frame)))


def rotation(g):
    # Limit outer-point tangential v to 200mm/s. Conservative sum of tangential
    # and centripetal accelerations <=8000mm/s², including acceleration ramps.
    radius=g['rmax']; v=200.
    acc=8000-v*v/radius
    return move(radius*g['angle_rad'],acc,v)


def writer(g,q,kind='stopped'):
    n=80//q; d=g['span']; j=move(2)+.003
    group=8*move(d/8)+10*j+move(d)
    if kind=='absolute_oracle': group=2*move(d)+.010
    if kind=='free': return 0.
    # Same explicit reset/unlock/sweep/select/return/clamp/read boundary as E-247.
    return 2*move(d)+2*j+.010+n*group+(n-1)*move(5.08)+move((n-1)*5.08)


def row(g,q,kind='stopped',colors='serial'):
    # Serial: one 80-channel shaft; only changed outputs of one color capture.
    # Parallel relaxation: two arbitrarily packable color decks, all extras free.
    lift=3.2 if colors=='serial' else 6.4
    ends=3*(move(2)+.003)+2*(move(lift)+.003)+2*(p.angular()+.003)
    factor=2 if colors=='serial' else 1
    return writer(g,q,kind)+factor*(ends+2*rotation(g))+move(5.08)


def timing(g,b,q,kind='stopped',colors='serial',visits=None):
    n=math.ceil(80/b) if visits is None else visits
    return 2.010+(n+1)*row(g,q,kind,colors)


def cost(b,q):
    # Favorable inherited ALLOCATIONS, not priced hardware. Extra shaft carriage,
    # cams, yokes, radial locks and second color deck get zero incremental dollars.
    return 195+20*b+.5*b*q+.02*80*b


def replay(old,target,fault=None):
    g=geometry(60); a=g['angle_rad']; obs=0
    h=list(old); ground=[True]*3; capture=[False]*3
    locked=True; arrested=True
    radius=[g['rmid']+(b-v)/math.sin(a) for v,b in zip(old,target)]
    for color in (0,1):
        active=[i%2==color and v!=b for i,(v,b) in enumerate(zip(old,target))]
        capture=[on and fault!='capture' for on in active]
        for i,on in enumerate(active):
            if on: ground[i]=False
        for k in range(17):
            th=a*k/16
            if fault=='radius_unlock': locked=False
            if fault=='arrest': arrested=False
            for i,on in enumerate(active):
                if on: h[i]=old[i]+(radius[i]-g['rmid'])*math.sin(th)
                assert ground[i] or (capture[i] and locked and arrested)
                assert min(old[i],target[i])-1e-9<=h[i]<=max(old[i],target[i])+1e-9
                if old[i]==target[i]: assert ground[i] and not capture[i] and h[i]==old[i]
                obs+=1
        for i,on in enumerate(active):
            if on: ground[i]=fault!='reseat'
        capture=[False]*3
        assert all(ground)
        # All outputs reset empty on inverse shaft motion; resident U untouched.
        assert all(abs(v-b)<1e-9 for i,(v,b) in enumerate(zip(h,target)) if i%2==color)
    assert all(abs(v-b)<1e-9 for v,b in zip(h,target))
    return obs


def main():
    maps=observations=0
    for old,target in it.product(it.product(LEVELS,repeat=3),repeat=2):
        observations+=replay(old,target);maps+=1
    caught=0
    for f in ('capture','radius_unlock','arrest','reseat'):
        try:replay((0,40,20),(40,0,20),f)
        except AssertionError:caught+=1
        else:raise AssertionError(f)
    # On-grid wrong endpoints only; one entire extra row service charged above.
    retries=0
    for old,actual,target in it.product(LEVELS,repeat=3):
        replay((old,20,20),(actual,20,20));replay((actual,20,20),(target,20,20));retries+=1
    # Independent continuous proof: lambda=sin(theta)/sin(alpha) increases 0..1.
    # Actual crank coordinates, including pivot compensation, match interpolation.
    g=geometry(60);coordinate_checks=0
    for old,target,k in it.product(LEVELS,LEVELS,range(101)):
        th=g['angle_rad']*k/100
        r=g['rmid']+(target-old)/math.sin(g['angle_rad'])
        z=-g['rmid']*math.sin(th)+r*math.sin(th)
        assert abs(z-(target-old)*math.sin(th)/math.sin(g['angle_rad']))<1e-12
        assert r*math.cos(th)>=8-1e-12
        coordinate_checks+=1
    # Single-plane symmetric signed-radius yoke crosses a continuous shaft at
    # neutral: its connected slot [-R,R] includes the shaft center (0,0).
    assert -40<0<40
    optimum=math.degrees(math.atan((80/8)**(1/3)))
    analytical_width=(80**(2/3)+8**(2/3))**1.5+4
    assert abs(geometry(optimum)['width']-analytical_width)<1e-10
    angles=tuple(range(20,81))+ (optimum,)
    results=[]
    for kind,colors,planar in it.product(('stopped','absolute_oracle','free'),('serial','parallel_oracle'),(False,True)):
        cases=[]
        for angle in angles:
            gg=geometry(angle)
            for b,q in it.product(range(1,(gg['bank_cap'] if planar else 80)+1),Q):
                t=timing(gg,b,q,kind,colors)
                if t<30:cases.append(dict(angle=angle,b=b,q=q,channels=b*q,outputs=80*b,seconds=t,cost=cost(b,q),width=gg['width']))
        best=min(cases,key=lambda x:(x['cost'],x['seconds'])) if cases else None
        results.append(dict(writer=kind,colors=colors,planar=planar,best=best))
    # Expanded causal schedule; first write, full reset, retry included.
    for b,q in ((3,80),(10,40),(16,80)):
        steps=[2.,.010]
        for _ in range(math.ceil(80/b)+1):
            steps.append(writer(g,q))
            for _ in (0,1):
                steps += [3*(move(2)+.003),2*(move(3.2)+.003),2*(p.angular()+.003),rotation(g),rotation(g)]
            steps.append(move(5.08))
        assert abs(sum(steps)-timing(g,b,q))<1e-10
    planar_free=min((timing(geometry(a),geometry(a)['bank_cap'],80,'free','parallel_oracle'),a) for a in angles)
    gap_oracles=[]
    for gap in (0,4,8,12):
        candidates=[geometry(a,gap=gap) for a in range(20,90)]
        best=min((timing(x,x['bank_cap'],80,'free','parallel_oracle'),x['angle_deg'])
                 for x in candidates if x['bank_cap']>0)
        gap_oracles.append(dict(exclusion_mm=gap,seconds=best[0],angle=best[1]))
    errors=[]
    for er,ez,da in it.product((.15,.35,.7),(.15,.35,.7),(0,.5,1.)):
        worst=max(abs((d/math.sin(g['angle_rad'])+sr*er)*math.sin(g['angle_rad']+sa*math.radians(da))+sz*ez-d)
            for d,sr,sa,sz in it.product(range(-40,41,10),(-1,1),(-1,1),(-1,1)))
        errors.append(dict(radius_error=er,carrier_error=ez,angle_error_deg=da,worst_height_error=worst))
    # Coupled path torque (shaft branch), not merely net useful work.
    torque=[]
    for f in (.1,1,10):
        torque.append(dict(per_output_N=f,forty_output_start_Nm=40*f*g['rmax']/1000,
                           radial_lock_N=f*math.sin(g['angle_rad']),carrier_reaction_N=40*f))
    print(json.dumps(dict(replay=dict(maps=maps,observations=observations,faults=caught,stable_wrong_retries=retries),
        coordinate_checks=coordinate_checks,inherited_cap_checks=p.geometry(16),base_geometry=g,
        minimum_width=dict(angle=optimum,width=analytical_width,banks=math.floor(406.4/analytical_width)),
        cases=results,base_times=dict(writer=writer(g,80),rotation=rotation(g),serial_row=row(g,80),
            b3_serial=timing(g,3,80),b3_parallel=timing(g,3,80,colors='parallel_oracle'),
            b3_free_parallel=timing(g,3,80,'free','parallel_oracle')),
        fastest_planar_free_parallel=dict(seconds=planar_free[0],angle=planar_free[1]),
        exclusion_sensitivity_free_parallel=gap_oracles,errors=errors,torque=torque),indent=2))

if __name__=='__main__':main()
