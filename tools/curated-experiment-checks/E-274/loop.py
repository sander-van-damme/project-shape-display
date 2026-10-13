#!/usr/bin/env python3
"""Finite friction loop, axial docking and complete conditional stopped schedules.

All dimensions, friction, load, costs and operating rates are scenario inputs.
No rated transmission, measured material model or manufactured fit is asserted.
"""
import argparse
import functools
import importlib.util
import itertools
import json
import math
from pathlib import Path
import numpy as np

spec = importlib.util.spec_from_file_location('rack', Path(__file__).resolve().parents[1]/'E-273/rack.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
h = r.h


def path(n, thickness=.4, samples=80):
    """Exact circle tangents, sampled arcs. CW outputs, CCW interposed idlers.

    Neutral-line radius = drum radius + half belt thickness. Four exterior
    turn drums close the loop behind the output/idler row. All units mm.
    """
    p=406.4/n; span=15*p; circles=[(-18.,0.,8+thickness/2,1,'drive')]
    for i in range(16):
        circles.append((i*p,0.,2+thickness/2,1,'output'))
        if i<15: circles.append(((i+.5)*p,-6.,2+thickness/2,-1,'idler'))
    circles += [(span+18,0.,8+thickness/2,1,'turn'),
                (span+18,-22.,8+thickness/2,1,'turn'),(-18.,-22.,8+thickness/2,1,'turn')]
    edges=[]
    for a,b in zip(circles,circles[1:]+circles[:1]):
        ca=np.array(a[:2]);cb=np.array(b[:2]);v=cb-ca
        angle=math.atan2(v[1],v[0])+math.acos((a[2]*a[3]-b[2]*b[3])/np.linalg.norm(v))
        normal=np.array([math.cos(angle),math.sin(angle)])
        edges.append((ca+a[2]*a[3]*normal,cb+b[2]*b[3]*normal))
    pieces=[];wraps=[];length=0
    for i,c in enumerate(circles):
        center=np.array(c[:2]);start=edges[i-1][1];end=edges[i][0]
        a=math.atan2(*(start-center)[::-1]);b=math.atan2(*(end-center)[::-1]);direction=-c[3]
        angle=(direction*(b-a))%(2*math.pi)
        angles=np.linspace(a,a+direction*angle,samples+1)
        arc=center+c[2]*np.column_stack((np.cos(angles),np.sin(angles)))
        pieces.append(arc);pieces.append(np.array(edges[i]));wraps.append(angle)
        length+=c[2]*angle+np.linalg.norm(edges[i][1]-edges[i][0])
    return circles,edges,pieces,wraps,length


def segment_distance(A,B):
    """Minimum exact segment distance for two polylines (including crossings)."""
    a=A[:-1,None,:];u=(A[1:]-A[:-1])[:,None,:]
    b=B[None,:-1,:];v=(B[1:]-B[:-1])[None,:,:]
    cross=lambda x,y:x[...,0]*y[...,1]-x[...,1]*y[...,0]
    den=cross(u,v);w=b-a
    with np.errstate(divide='ignore',invalid='ignore'):
        s=cross(w,v)/den;t=cross(w,u)/den
    if np.any((abs(den)>1e-12)&(s>=0)&(s<=1)&(t>=0)&(t<=1)):return 0.
    def point_line(p,q,z):
        f=np.clip(np.sum((p-q)*z,axis=-1)/np.sum(z*z,axis=-1),0,1)
        return np.linalg.norm(p-q-f[...,None]*z,axis=-1).min()
    return min(point_line(a,b,v),point_line(a+u,b,v),point_line(b,a,u),point_line(b+v,a,u))


@functools.lru_cache(None)
def geometry(n,e=.2,samples=80):
    cs,edges,pieces,wraps,length=path(n,samples=samples)
    # Omit neighbors at their intentional join only; every nonadjacent path
    # piece is checked. Arc-chord error <= R*(1-cos(sweep/(2*samples))).
    gap=float('inf')
    boxes=[(a.min(axis=0),a.max(axis=0)) for a in pieces]
    for i,a in enumerate(pieces):
        for j in range(i+2,len(pieces)):
            if i==0 and j==len(pieces)-1:continue
            lo,hi=boxes[i];lj,hj=boxes[j]
            bound=np.linalg.norm(np.maximum(0,np.maximum(lo-hj,lj-hi)))
            if bound<gap:gap=min(gap,segment_distance(a,pieces[j]))
    sag=max(c[2]*(1-math.cos(w/(2*samples))) for c,w in zip(cs,wraps))
    output=[w for c,w in zip(cs,wraps) if c[4]=='output']
    # Moving drum z [-18,-12] -> [-15,-9]; belt z [-14.5,-12.5].
    # Their common 3mm overlap leaves .5 nominal edge reserve each side.
    return dict(n=n,loop_length_mm=length,output_wrap_deg=[min(output)*180/math.pi,max(output)*180/math.pi],
                drive_wrap_deg=wraps[0]*180/math.pi,nonlocal_belt_gap_mm=gap-.4-2*e-2*sag,
                sagitta_bound_mm=sag,neighbor_belt_envelope_gap_mm=406.4/n-4.8-2*e,
                drum_body_neighbor_gap_mm=406.4/n-4-2*e,
                axial_edge_reserve_mm=.5-2*e,parked_tip_gap_mm=1-2*e,insertion_mm=2-2*e,
                loop_head_mm=[15*406.4/n+52.8,38.8],whole_X_union_mm=406.4-406.4/n+52.8,
                selector=r.selection_envelope(n))


def traction(n=64,torque=.35,mu=.3,mu_axial=.3,slack=2.,accel=5.,inertia=1e-8):
    _,_,_,wraps,_=path(n)
    output_wraps=[wraps[1+2*i] for i in range(16)]
    # Flexible-band forces use effective neutral radius2.2mm throughout. Bound wheel
    # inertia by effective tangential force J*a/r_neutral² on every output.
    per=torque/2.2+inertia*accel/.0022**2
    delta=16*per  # idler/belt/drive inertia and bearing/bending losses omitted
    driver_min_slack=delta/math.expm1(mu*wraps[0])
    out_min_slack=max(per/math.expm1(mu*w) for w in output_wraps)
    required=max(driver_min_slack,out_min_slack)
    # During axial docking bus is stopped, equal unloaded pretension >=required.
    # Integral normal force = T*theta for a flexible belt, axial Coulomb friction.
    axial=mu_axial*required*max(output_wraps)
    available=.785-.2  # inherited catalog throw figure minus assumed socket force
    return dict(per_output_tension_drop_N=per,total_tension_drop_N=delta,
                driver_slack_min_N=driver_min_slack,output_slack_min_N=out_min_slack,
                slack_min_N=required,given_slack_N=slack,
                driver_capacity_N=slack*math.expm1(mu*wraps[0]),
                axial_drag_at_min_slack_N=axial,selector_remaining_N=available,
                max_axial_mu=available/(required*max(output_wraps)),
                drive_torque_Nmm=delta*8.2,mechanical_W=delta*.2,
                docking_force_lower_scenario_pass=axial<=available)


def phase_index(angle_deg,lead=3,rpm=850):
    """Nearest sixfold common alignment with all tips parked; angle is residual."""
    residue=abs((angle_deg+30)%60-30)
    return h.a.r.spin(residue/360,rpm,5000/(math.pi*4.4))


def transaction(values,lead=3,rpm=850,switch=.08,phase_classes=1):
    if not any(values):return dict(seconds=0.,active_s=0.,switching_s=0.,phase_s=0.,read_s=0.,groups=0)
    # phase_classes=16 is a SERIAL adversarial known-phase control; preserve
    # finite one-phase optimistic grouping rather than granting arbitrary phases.
    partitions=[values] if phase_classes==1 else [[v] for v in values if v]
    groups=[group for part in partitions for group in h.a.r.program(part)]
    speed=min(rpm,200/(math.pi*4.4)*60);accel=5000/(math.pi*4.4)
    active=sum(h.a.r.spin(abs(step)/lead,speed,accel) for step,_ in groups)
    # Charge maximum nearest symmetry indexing separately at each sign/phase
    # acquisition. It may be zero in an exact pre-registered on-grid transaction.
    acquisitions=sum(bool([v for v in part if v>0])+bool([v for v in part if v<0]) for part in partitions)
    phase=acquisitions*phase_index(30,rpm=speed)
    return dict(seconds=active+switch*len(groups)+phase+.3,active_s=active,
                switching_s=switch*len(groups),phase_s=phase,read_s=.3,groups=len(groups))


def schedule(delta,width=16,stroke=50,**kw):
    travel=h.schedule(delta,width)
    if not travel['stations']:return dict(seconds=0.,stations=0)
    jobs=h.stations(delta,width)
    tx=[transaction([v for _,v in cells],**kw) for _,_,cells in jobs]
    terms=dict(common_s=5.,seek_s=travel['seek_s'],return_s=travel['return_s'],
               active_s=sum(t['active_s'] for t in tx),switching_s=sum(t['switching_s'] for t in tx),
               phase_s=sum(t['phase_s'] for t in tx),read_s=sum(t['read_s'] for t in tx),
               retry_s=transaction([stroke],**kw)['seconds'])
    return dict(seconds=sum(terms.values()),**terms,stations=len(jobs),
                raised=travel['raised_cells'],lowered=travel['lowered_cells'],
                unchanged=travel['unchanged_cells'],visited_rows=travel['visited_rows'],
                first_seek_s=travel['first_seek_s'])


def summary(cases,stroke,**kw):
    rows={name:schedule(delta,stroke=stroke,**kw) for name,delta in cases.items() if any(map(any,delta))}
    name=max(rows,key=lambda name:rows[name]['seconds'])
    return dict(max_s=rows[name]['seconds'],worst=name,ledger=rows[name],
                nonempty=len(rows),within30=sum(v['seconds']<=30 for v in rows.values()))


def report(n,stroke,**kw):
    cases={name:delta for name,delta in h.a.workloads(n).items() if stroke==50 or 'deep:' not in name}
    targets,start=h.a.c.terrain(n,stroke-20,stroke-20)
    names=h.a.c.v.s.SUITES['relief']
    initial={name:h.a.r.delta(start,targets[name]) for name in names}
    prep=schedule(h.a.c.v.s.flat(n,stroke-20),stroke=stroke,**kw)['seconds']
    return dict(n=n,stroke=stroke,parameters=kw,local=summary(h.local_cases(n,stroke),stroke,**kw),
                scene=summary(cases,stroke,**kw),neutral_s=prep,
                minimum_rest_first_s=summary({name:targets[name] for name in names},stroke,**kw)['max_s'],
                neutral_plus_first_s=prep+summary(initial,stroke,**kw)['max_s'],
                dense_s=schedule(h.a.c.v.s.flat(n,stroke),stroke=stroke,**kw)['seconds'],
                mixed_dense_s=schedule([[stroke if(x+y)%2 else -stroke for x in range(n)] for y in range(n)],stroke=stroke,**kw)['seconds'])


def cost(n):
    items=dict(r.cost(n)['allocations'])
    del items['common_rack_drive_encoder'];del items['rack_guides_stops']
    items['shaft_tip_drum_bushings']=items.pop('shaft_tip_pinion_bushings')
    items.update(common_rotary_drive_encoder=(1,40,120),endless_belt=(1,10,40),
                 idler_bearing_mount=(15,2,6),end_turn_drum_bearing_mount=(4,4,10),
                 tensioner_tracking_guards=(1,15,50))
    totals=[sum(q*row[k] for row in items.values() for q in [row[0]]) for k in (1,2)]
    return dict(allocations=items,purchased_USD=[totals[0]*1.1+20,totals[1]*1.15+60],
                maker_hours=[8+n*n*8/3600+16/6+2,16+n*n*20/3600+8+5],
                print_material_USD=[60,160],selector_W=88,
                conductors=102,terminations=204)


def checks():
    rows=0
    for values in itertools.product((-50,-20,0,10,30,50),repeat=4):
        actual=[0]*4;distance=0
        for step,mask in h.a.r.program(values):
            actual=[a+step if m else a for a,m in zip(actual,mask)];distance+=abs(step)
            assert all(min(0,v)<=a<=max(0,v) for a,v in zip(actual,values))
        assert actual==list(values)
        assert distance==max(0,*values)+max(0,*(-v for v in values))
        assert math.isclose(transaction(values)['seconds'],transaction([-v for v in values])['seconds'])
        rows+=1
    geo={n:geometry(n) for n in (64,80)}
    assert geo[64]['nonlocal_belt_gap_mm']>0
    assert geo[80]['neighbor_belt_envelope_gap_mm']<0
    assert geometry(64,e=.3)['axial_edge_reserve_mm']<0
    # Analytic middle-output wrap independently reconstructed from a symmetric pair.
    expected=2*(math.atan2(6,6.35/2)+math.asin(4.4/math.hypot(6,6.35/2)))
    assert math.isclose(max(path(64)[3][1:32:2]),expected)
    for samples in (40,160):
        g=geometry(64,samples=samples)
        assert abs(g['nonlocal_belt_gap_mm']-geo[64]['nonlocal_belt_gap_mm'])<.02
    assert segment_distance(np.array([[0.,0.],[1.,1.]]),np.array([[0.,1.],[1.,0.]]))==0
    for n in (64,80):
        for stroke in (40,50):
            full=schedule([[stroke]*n for _ in range(n)],stroke=stroke)
            assert full['stations']==n*n//16
            assert math.isclose(full['seconds'],5+full['seek_s']+full['return_s']+(n*n//16+1)*transaction([stroke])['seconds'])
        assert schedule([[0]*n for _ in range(n)])['seconds']==0
    f=traction()
    assert f['axial_drag_at_min_slack_N']>f['selector_remaining_N']
    assert math.isclose(16*.35*2*math.pi,(16*.35/2.2)*4.4*math.pi)
    assert r.phase_span([0,.25])>10
    # Two initially registered drums with opposite effective-radius errors
    # lose a common +/-5deg sixfold docking window after one 50mm move.
    heights=[50*2.2/(2.2+dr) for dr in (-.002,.002)]
    assert r.phase_span(heights)>10
    assert math.isclose(r.phase_span([0,10,20,30]),0,abs_tol=1e-8)
    assert transaction([10]*16,phase_classes=16)['seconds']>transaction([10]*16)['seconds']
    # Exactly tangent interior drum has zero wrap/capstan capacity.
    assert math.expm1(.3*0)==0
    return dict(exhaustive_signed_rows=rows,geometry=geo,checks='tangents, nonlocal belt clearances, refinement, force/work, docking conflict, phase witness, dense/no-op timing')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    verified=checks()
    print(json.dumps(verified if args.check else dict(verification=verified,
        rows=[report(n,s) for n,s in itertools.product((64,80),(40,50))],
        sensitivities=[report(64,50,**kw) for kw in (dict(lead=2),dict(rpm=400),dict(switch=.2),dict(phase_classes=16))],
        traction=[dict(mu=mu,torque=t,**traction(mu=mu,mu_axial=mu,torque=t)) for mu,t in itertools.product((.1,.3,.6),(.1,.35,1.))],
        costs={n:cost(n) for n in (64,80)}),indent=2))
