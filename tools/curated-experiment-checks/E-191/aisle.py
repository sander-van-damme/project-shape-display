#!/usr/bin/env python3
"""Finite necessary-condition screen, mm/N/s. No qualified material priors.
Rigid rectangular C hook on a round shaft; rotate 90 degrees OR slide into
one straight x aisle. Exact arc extrema enclose all intermediate material.
"""
import importlib.util
import itertools
import json
import math
from pathlib import Path

P = 5.08
S = 1.2

def rect(x0, x1, y0, y1):
    return [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]

def arc_bounds(vertices, pivot, angle=math.pi/2):
    """Exact coordinate extrema of every vertex through [0,angle]."""
    points=[]
    for x,y in vertices:
        x-=pivot
        angles=[0,angle]
        phi=math.atan2(y,x)
        for k in range(-4,5):
            for a in (k*math.pi-phi, math.pi/2+k*math.pi-phi):
                if 0<a<angle: angles.append(a)
        points += [(pivot+x*math.cos(a)-y*math.sin(a),x*math.sin(a)+y*math.cos(a)) for a in angles]
    return (min(x for x,y in points),max(x for x,y in points),min(y for x,y in points),max(y for x,y in points))

def gap(a,b):
    """Best coordinate separation, negative when all projections overlap."""
    return max(b[0]-a[1],a[0]-b[1],b[2]-a[3],a[2]-b[3],b[4]-a[5],a[4]-b[5])

def section(f,b,d,tip,delta,kind):
    pivot=P/2; w=.6
    lip=rect(tip,pivot+w/2,-b/2,b/2)
    web=rect(pivot-w/2,pivot+w/2,-b/2,b/2)
    if kind=='rotate':
        lp=arc_bounds(lip,pivot); wb=arc_bounds(web,pivot)
        final=(pivot-b/2,pivot+b/2,tip-pivot,w/2)
        stroke=math.pi/2
    else:
        stroke=f/2+delta+.025-tip
        lp=(tip,pivot+w/2+stroke,-b/2,b/2)
        wb=(pivot-w/2,pivot+w/2+stroke,-b/2,b/2)
        final=(tip+stroke,pivot+w/2+stroke,-b/2,b/2)
    solids=[(*lp,-1.,-.5),(*lp,1.7,2.2),(*wb,-.5,1.7),
            (pivot-d/2,pivot+d/2,-d/2,d/2,-91.,-1.)]
    # Own foot/stem at h=0. Every OTHER foot and stem spans all relative heights.
    obstacles=[(-f/2,f/2,-1.4,1.4,0.,1.2),(-S/2,S/2,-S/2,S/2,1.2,121.2)]
    for i,j in itertools.product(range(-1,2),repeat=2):
        if i==j==0: continue
        obstacles += [(i*P-f/2,i*P+f/2,j*P-1.4,j*P+1.4,-40.,41.2),
                      (i*P-S/2,i*P+S/2,j*P-S/2,j*P+S/2,-38.8,121.2)]
    path_margin=min(gap(a,o) for a in solids for o in obstacles)-delta
    # On the withdrawn y route any neighbor height and row offset is legal.
    # Straight aisle must contain hook AND its shaft; no x crossover is needed.
    xmin=min(final[0],pivot-d/2); xmax=max(final[1],pivot+d/2)
    transport_margin=min(xmin-f/2,P-f/2-xmax)-delta
    overlap=f/2-tip-delta
    head_margin=P-(max(a[1] for a in solids)-min(a[0] for a in solids))-delta
    margin=min(path_margin,transport_margin,overlap,head_margin)
    return dict(kind=kind,foot=f,lip_width=b,shaft_d=d,tip=tip,
                margin=margin,path_margin=path_margin,transport_margin=transport_margin,
                overlap_margin=overlap,head_margin=head_margin,stroke=stroke)

def mechanics(c,E,F=.13405,h=40.5):
    # Shaft lower guides at -10,-40; upper hook load at h, an eccentric END
    # MOMENT bound. Contact coupled to the column is deliberately NOT solved.
    I=math.pi*c['shaft_d']**4/64
    L=h+10; span=30
    contact=(c['tip']+c['foot']/2)/2
    eccentric=P/2-contact
    M=F*eccentric
    u=M*(L*L/2+span*L/3)/(E*I)
    stress=F/(math.pi*c['shaft_d']**2/4)+M*c['shaft_d']/2/I
    pcr=math.pi**2*E*I/(4*L*L) # optimistic clamped-overhang comparator
    return dict(E=E,force=F,free_tip_mm=u,elastic_stress_MPa=stress,
                clamped_euler_N=pcr,shaft_I=I,eccentric=eccentric)


def guide_check(c):
    # Two connected square sleeves below feet, .8-mm walls, .05-mm nominal
    # radial clearance to a ROUND 90-mm shaft. This is nominal material only;
    # sleeve error/contact/actuator qualification is not granted.
    x=P/2; r=c['shaft_d']/2; bore=r+.05; outer=bore+.8
    walls=[]
    for z in (-10.,-40.):
        walls += [(x-outer,x-bore,-outer,outer,z-1,z+1),
                  (x+bore,x+outer,-outer,outer,z-1,z+1),
                  (x-bore,x+bore,-outer,-bore,z-1,z+1),
                  (x-bore,x+bore,bore,outer,z-1,z+1)]
    for h in (-.5,0.,20.,40.,40.5):
        shaft=(x-r,x+r,-r,r,h-91.,h-1.)
        assert all(gap(shaft,w)>=.05-1e-12 for w in walls)
        assert shaft[4]<-41 and shaft[5]>-9
    assert 2*outer<P
    # Finite shaft-to-lower-lip connection has positive nominal projected area.
    contact_width=max(0.,min(x+r,x+.3)-max(x-r,c['tip']))
    assert contact_width>0 and c['lip_width']>0
    return dict(sleeve_outer_mm=2*outer,shaft_length_mm=90.,
                shaft_bottom_at_min_mm=-91.5,nominal_guide_gap_mm=.05)

def check_arcs():
    # Independently sample transformed vertices and refine envelope approaches.
    vs=rect(1.01,2.84,-.3,.3); hull=arc_bounds(vs,2.54)
    errors=[]
    for n in (16,64,256,1024):
        pts=[(2.54+(x-2.54)*math.cos(a)-y*math.sin(a),
              (x-2.54)*math.sin(a)+y*math.cos(a))
             for k in range(n+1) for a in [k*math.pi/(2*n)] for x,y in vs]
        sampled=(min(x for x,y in pts),max(x for x,y in pts),min(y for x,y in pts),max(y for x,y in pts))
        assert all(hull[0]-1e-12<=x<=hull[1]+1e-12 and hull[2]-1e-12<=y<=hull[3]+1e-12 for x,y in pts)
        errors.append(max(abs(a-b) for a,b in zip(sampled,hull)))
    assert errors[-1]<1e-6 and errors[-1]<errors[0]
    assert arc_bounds(vs,2.54,0)==(1.01,2.84,-.3,.3)
    return errors

def curvature_check(c):
    E=2000.;I=math.pi*c['shaft_d']**4/64;L=50.;span=30.
    # Independently integrate supported-span linear M(x), choose slope for
    # zero displacement at both bearings, then integrate constant end moment.
    exact=(L*L/2+span*L/3)/(E*I)
    errors=[]
    for n in (16,64,256):
        dx=span/n; theta=0.; y=0.
        for k in range(n):
            curvature=((k+.5)*dx/span)/(E*I)
            y+=theta*dx+curvature*dx*dx/2;theta+=curvature*dx
        slope_correction=-y/span
        theta+=slope_correction
        tip=theta*L+L*L/(2*E*I)
        errors.append(abs(tip-exact))
    assert errors[-1]<errors[0]/100
    return errors

def main():
    results=[]; selected=None
    for e,dpose in ((.025,.05),(.05,.15),(.1,.15)):
        delta=4*e+dpose+.025
        for kind in ('slide','rotate'):
            candidates=[]
            for f,b,d,tip in itertools.product((2.,2.2,2.4,2.6,2.8,3.,3.2,3.4),(.6,.8,1.),(.8,1.,1.3,1.6),[.7+.025*k for k in range(45)]):
                if not S/2<tip<f/2:continue
                c=section(f,b,d,tip,delta,kind)
                if c['margin']>0:candidates.append(c)
            best=max(candidates,key=lambda c:c['margin']) if candidates else None
            thick=max(candidates,key=lambda c:(c['shaft_d'],c['margin'])) if candidates else None
            results.append(dict(e=e,pose=dpose,delta=delta,kind=kind,passing=len(candidates),best=best,thickest=thick))
            if e==.05 and kind=='rotate':selected=thick
    assert selected is not None
    spec=importlib.util.spec_from_file_location('transport',Path(__file__).parents[1]/'E-190'/'transport.py')
    t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
    timing=[]
    for rotation in (.02,.05,.1):
        # Charge two added full-bank turns per row, no overlap credited.
        for banks in range(1,81):
            n=math.ceil(80/banks)
            sec=6+t.bypass_bank(n)+(n-1)*t.empty(P)+t.empty((n-1)*P)+2*n*rotation
            if sec<30:break
        timing.append(dict(one_turn_s=rotation,banks=banks,motors=80*banks,seconds=sec))
    mech=[mechanics(selected,E) for E in (500.,2000.,100000.)]
    assert mechanics(selected,2000.,F=0)['free_tip_mm']==0
    assert abs(mech[1]['free_tip_mm']/mech[2]['free_tip_mm']-50)<1e-10
    # Shaft radius vs foot aisle for the old 2-mm-foot hook: explicit regression.
    assert section(2.,1.,1.3,.8,.375,'rotate')['margin']<0
    print(json.dumps(dict(scenarios=results,central_selected=selected,mechanics=mech,guides=guide_check(selected),
                         timing=timing,transfer_budget_two_banks_s=.05+(30-(6+t.bypass_bank(40)+39*t.empty(P)+t.empty(39*P)))/80,
                         takeup_half_mm_s=t.loaded(.5),arc_error_mm=check_arcs(),
                         curvature_error_mm=curvature_check(selected)),indent=2))

if __name__=='__main__':main()
