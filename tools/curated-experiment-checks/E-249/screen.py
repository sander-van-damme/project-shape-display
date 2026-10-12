#!/usr/bin/env python3
"""Rigid-column shunting screen. mm; deterministic bounds, no process priors.
Nominal 2D polygons are extruded through a common y interval. No force model.
"""
import importlib.util
import itertools
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location('bayonet', Path(__file__).resolve().parents[1] / 'E-167/probe.py')
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
P = 5.08


def rect(x0, x1, z0, z1):
    return [(x0,z0),(x1,z0),(x1,z1),(x0,z1)]


def shapes(H0, h, theta, s=2., g=.5, w=.7, d=4.8):
    """Cap underside pivot H0+h; five integral teeth, no swivel or hinge."""
    b = s/2 + g + w
    local = [('stem',rect(-s/2,s/2,-H0-42,0)),
             ('cap',rect(-d/2,d/2,0,2))]
    local += [(f'tooth{j}',rect(0,b,-H0-10*j,-H0-10*j+2)) for j in range(5)]
    c, sn = math.cos(theta), math.sin(theta)
    return [(name,[(c*x+sn*z,H0+h-sn*x+c*z) for x,z in poly]) for name,poly in local]


def margins(H0, theta, s=2., g=.5, w=.7, E=.3):
    """Sufficient envelopes; E is total adverse gap error, NOT per-part sigma.
    All local sides plus relative registration/warp must fit this bound.
    Rotation model grants perfect commanded angle; extra angle error unpaid.
    """
    b, a = s/2+g+w, s/2+g
    c, sn = math.cos(theta), math.sin(theta)
    return dict(body_rail=g-E, bearing=w-E,
                bypass=a-(b*c-(H0-2)*sn)-E,
                neighbor=P-b-s/2*c-(H0+42)*sn-E)


def optimum(H0, s=2., g=.5, w=.7, E=.3):
    # Bypass improves and left-neighbor envelope worsens in this interval.
    lo, hi = 0., math.radians(5)
    for _ in range(60):
        mid = (lo+hi)/2
        m = margins(H0,mid,s,g,w,E)
        if m['bypass'] < m['neighbor']:
            lo = mid
        else:
            hi = mid
    theta = (lo+hi)/2
    m = margins(H0,theta,s,g,w,E)
    return dict(H0=H0,s=s,g=g,w=w,E=E,angle_deg=math.degrees(theta),
                minimum_margin=min(m.values()),**m)


def path(H0, start, target, theta, n):
    lift = 2.
    for phase in range(5):
        for i in range(n+1):
            q = i/n
            h, a = [(start+lift*q,0), (start+lift,theta*q),
                    (start+lift+(target-start)*q,theta),
                    (target+lift,theta*(1-q)), (target+lift*(1-q),0)][phase]
            yield phase,h,a


def replay(H0, theta, n):
    # A rail per cell, not an infinite half-plane; all tooth/stem polygons count.
    rails = [rect(k*P+1.5,k*P+P/2,-2,0) for k in (-1,0,1)]
    neighbors = {h: [(name,[(x+k*P,z) for x,z in p])
                    for k in (-1,1) for name,p in shapes(H0,h,0)] for h in range(0,41,10)}
    def bounds(poly):
        return (min(x for x,z in poly),max(x for x,z in poly),
                min(z for x,z in poly),max(z for x,z in poly))
    obstacles=[('rail',q) for q in rails]
    obstacles += [(f'neighbor_{nh}_{nm}',q) for nh,qs in neighbors.items() for nm,q in qs]
    obstacles=[(name,q,bounds(q)) for name,q in obstacles]
    count = hits = 0
    first = None
    for start,target in itertools.permutations(range(0,41,10),2):
        for phase,h,angle in path(H0,start,target,theta,n):
            active=shapes(H0,h,angle)
            count += 1
            for name,p in active:
                p0,p1,p2,p3=bounds(p)
                for nm,q,(q0,q1,q2,q3) in obstacles:
                    # Cheap interval broad phase before exact convex SAT.
                    if p1<=q0 or q1<=p0:
                        continue
                    if p3<=q2 or q3<=p2:
                        continue
                    if old.intersect(p,q):
                        hits += 1
                        if first is None:
                            first=dict(start=start,target=target,phase=phase,h=h,angle_deg=math.degrees(angle),moving=name,obstacle=nm)
    return dict(poses=count,intersections=hits,first=first)


def guide_witness(H0, theta, half_gap=.2):
    # Fixed ordinary straight stem sleeve at H0-5, thickness 2; selected h=40.
    z=H0-5
    p=dict(shapes(H0,42,theta))['stem']
    left=rect(-2.5,-1-half_gap,z-1,z+1)
    return dict(guide_z=z,half_gap=half_gap,
                center_shift_at_guide=(47)*math.tan(theta),
                collision=old.intersect(p,left),
                needed_left_half_gap=48*math.tan(theta)+1/math.cos(theta)-1)


def translation_bound():
    # At downward crossing of old seat, cap is coplanar with same-height U.
    # A shelf of positive thickness must be shunted before its bottom crosses 0.
    return [dict(cap_width=d,nominal_surface_gap=P-d,
                 max_overlap_before_error=P-d,
                 coverage=(d/P)**2) for d in (4.8,4.6,4.2,4.)]


def service_bounds(theta):
    def t(d,v,a):
        return 2*math.sqrt(d/a) if d<=v*v/a else d/v+v/a
    # Independent bilateral Z/pitch outputs are granted, not implemented.
    angular=2*t(math.degrees(theta),30,360)
    rows=[]
    for proof in (.05,.1,.2):
        service=2*t(2,200,8000)+t(40,200,8000)+angular+proof
        # Park below all tails between rows; worst empty approach and return.
        service += 2*t(42,200,8000)
        for B in range(1,9):
            visits=math.ceil(80/B)+1  # one complete causal row retry
            total=2+visits*(service+t(5.08,200,8000))
            if total<30:
                rows.append(dict(proof_s=proof,B=B,outputs=80*B,service_s=service,
                                 map_s=total,budget_per_output=(500-295)/(80*B)))
                break
    return rows


def main():
    assert not old.intersect(rect(0,1,0,1),rect(1,2,0,1))
    assert old.intersect(rect(0,1,0,1),rect(.99,2,0,1))
    cases=[optimum(H0,E=E) for H0,E in itertools.product((30,50,75,100,150,250),(.1,.3,.7))]
    # Holdout grid cross-check of one-dimensional envelope optimum.
    for item in cases:
        theta=math.radians(item['angle_deg'])
        best=max(min(margins(item['H0'],math.radians(i/1000),E=item['E']).values()) for i in range(5001))
        assert item['minimum_margin'] >= best-1e-9
        assert item['minimum_margin']-best < .006
    witness=optimum(100,E=.3)
    theta=math.radians(witness['angle_deg'])
    paths=[replay(100,theta,n) for n in (4,16,64)]
    assert all(x['intersections']==0 for x in paths)
    blocked=replay(100,0,4)
    assert blocked['intersections']>0
    guide=guide_witness(100,theta)
    assert guide['collision']
    # Slenderness is a diagnostic, not a strength or stiffness prediction.
    # Square-XZ bending I = depth_y*s^3/12. E is an explicit assumed range.
    beam=[dict(E_MPa=E,unguided_length_mm=L,
               ideal_fixed_free_Pcr_N=math.pi**2*E*(2*2**3/12)/(4*L**2))
          for E,L in itertools.product((1000,2000,3000),(40,100,140))]
    # Sufficient geometry envelope rejects all this declared broad scenario,
    # not every tilt architecture. No guessed manufactured probability.
    grid=[optimum(H,s,g,w,.7) for H,s,g,w in itertools.product(
        (50,100,150,250), (1.,1.5,2.,2.5,3.), (.3,.5,.8,1.1),(.4,.7,1.0,1.3))
        if s/2+g+w<=P/2]
    assert all(x['minimum_margin']<=0 for x in grid)
    print(json.dumps(dict(translation=translation_bound(),tilt=cases,witness=witness,
                         replay=paths,unshunted_control=blocked,guide=guide,
                         wide_error_screen=dict(candidates=len(grid),positive_margins=0),
                         cap_gap_after_point1_error=P-2.4-(2.4*math.cos(theta)+2*math.sin(theta))-.1,
                         services=service_bounds(theta),ideal_beam=beam),indent=2))

if __name__=='__main__':
    main()
