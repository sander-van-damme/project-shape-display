#!/usr/bin/env python3
"""Finite support routes and unilateral top-guide beam model, mm/N/MPa.

Deterministic engineering scenarios; no process distributions or hardware pass.
Python standard library. Prior geometry is imported, not silently redesigned.
"""
import importlib.util
import itertools
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    'grounded', Path(__file__).parents[1]/'E-192/grounded.py')
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
P, X = prior.P, prior.X
L = 66.0  # bottom clamp z=-10; equivalent lateral guide contact z=56


def shift(b, x=0., y=0., z=0.):
    return tuple(v+q for v, q in zip(b, (x,x,y,y,z,z)))


def sections():
    out = []
    for f,d,g,w,tip in itertools.product(
            (2.6,2.8,3.,3.2,3.4), tuple(.4+.1*k for k in range(10)),
            (.05,.1,.15,.25), (.2,.4,.8), tuple(.8+.01*k for k in range(56))):
        if g <= .125:
            continue
        if min((P-f)/2-(d/2+g+w)-.375,
               f/2-tip-.375,tip-.6-.375) <= 1e-10:
            continue
        c = prior.package(f,d,g,w,tip,.375)
        if c['margin'] > 1e-10:
            out.append(c)
    assert len(out) == 18
    return out


def geometry(c):
    """Continuous swept boxes, exact quarter-turn extrema, finite frame material.

    A post through the aisle is the control collision. Offset posts use row gaps;
    bridges above the translating head connect two longitudinal guide cheeks.
    Intentionally omit drive/reader/lock inventions and any joint-strength claim.
    """
    d, f = c['rail_d'], c['foot']
    r, guide_gap, wall = d/2, .15, .4
    local = {
        'post': (-1.2,1.2,P/2-.5,P/2+.5,-14.,58.),
        'bridge': (-1.2,X+r+guide_gap+wall,P/2-.5,P/2+.5,58.,60.),
        'left_cheek': (X-r-guide_gap-wall,X-r-guide_gap,-P,3*P,54.,58.),
        'right_cheek': (X+r+guide_gap,X+r+guide_gap+wall,-P,3*P,54.,58.),
    }
    frame = []
    for i in range(-1,2):
        frame += [shift(local[k], x=i*P) for k in ('left_cheek','right_cheek')]
        frame += [shift(local[k], x=i*P,y=j*P)
                  for j in range(-1,3) for k in ('post','bridge')]
    columns = []
    for i,j in itertools.product(range(-2,3), range(-2,5)):
        # Union of all foot, stem and cap positions for h in [0,40].
        columns += [shift(b,i*P,j*P) for b in (
            (-f/2,f/2,-1.4,1.4,0.,41.2),
            (-.6,.6,-.6,.6,1.2,121.2),
            (-2.5,2.5,-2.5,2.5,81.2,123.2))]
    frame_column_gap = min(prior.arc.gap(a,b) for a in frame for b in columns)
    routes = prior.finite_routes()['boxes']
    old_block = routes['ground_block']
    # The inherited 3-mm-wide moving clamp hits the offset posts. Retain this
    # collision and test a changed 1.6-mm clamp; fixity remains an assumption.
    routes['ground_block'] = (X-.8,X+.8,-1.5,1.5,-14.,-10.)
    # Extend the old moving rail into the new fixed guide. Compare it separately
    # to its intentional bearing cheeks; its running gap is NOT external reserve.
    routes['rail'] = (X-r,X+r,-r,r,-12.,57.)
    moving = [b for k,b in routes.items() if k != 'rail']
    moving += [(X-c['outer_r'],X+c['outer_r'],-c['outer_r'],c['outer_r'],-4.5,42.7),
               (X-.3,X+.3,c['tip']-X,0.,-1.5,42.7)]
    # Withdrew before y transport. These boxes cover every intermediate y and h.
    swept = [(a,b,y0,y1+2*P,z0,z1) for a,b,y0,y1,z0,z1 in moving]
    transport_gap = min(prior.arc.gap(a,b) for a in frame for b in swept)
    # Active swing at each serviced row, throughout the vertical stroke.
    end = X-(d/2+c['gap'])/math.cos(math.pi/64)
    lip = prior.arc.arc_bounds(prior.arc.rect(c['tip'],end,-.3,.3), X)
    swing = [shift((*lip,-1.5,42.7),y=j*P) for j in range(3)]
    swing_gap = min(prior.arc.gap(a,b) for a in frame for b in swing)
    rail_sweep = (X-r,X+r,-r,2*P+r,-12.,57.)
    nonbearing = [shift(local[k],x=i*P,y=j*P)
                  for i,j in itertools.product(range(-1,2),range(-1,3))
                  for k in ('post','bridge')]
    assert min(prior.arc.gap(rail_sweep,b) for b in nonbearing) > .375
    # Real material collision when a support post instead lies on the travel lane.
    aisle_post = ((X-.2,P-.2,-10.),(X+.2,P+.2,54.))
    shell = prior.ring(c['outer_r'],d/2+c['gap'])
    # Post offset .5 in x penetrates annular material, not merely its empty bore.
    obstacle = (X+.3,X+.7,-.2,.2)
    shell_volume = sum(prior.overlap(poly,obstacle) for poly in shell)*6.2
    rail_volume = prior.time.box_overlap(aisle_post,
        ((X-r,P-r,-12.),(X+r,P+r,57.)))
    assert rail_volume > 0 and shell_volume > 0
    b=shift(old_block,y=P/2)
    p=local['post']
    old_block_volume=prior.time.box_overlap(
        ((b[0],b[2],b[4]),(b[1],b[3],b[5])),
        ((p[0],p[2],p[4]),(p[1],p[3],p[5])))
    assert abs(old_block_volume-.64) < 1e-12
    assert min(frame_column_gap,transport_gap,swing_gap) > .375
    # Positive-area intended joins at z=58: post -> bridge -> guide cheeks.
    assert local['post'][5] == local['bridge'][4] == local['left_cheek'][5]
    return dict(new_frame=local,frame_column_margin=frame_column_gap-.375,
                withdrawn_transport_margin=transport_gap-.375,
                active_swing_margin=swing_gap-.375,
                top_nominal_radial_gap=guide_gap,
                inherited_block_post_collision_mm3=old_block_volume,
                changed_clamp=routes['ground_block'],
                centre_post_rail_collision_mm3=rail_volume,
                offset_post_shell_collision_mm3=shell_volume)


def support_compliance(kind, Eframe=2000., ends='pinned'):
    """One loaded cheek, not an imaginary composite wide box section.

    Favorable perfect bridge joints; fixed post roots; no joint/contact losses.
    Midspan point load; 2 equal posts. Eframe also applies to cheek and bridge.
    """
    if kind == 'ideal':
        return 0.
    span = P if kind == 'distributed' else 81*P
    Icheek = 4*.4**3/12
    Ipost = 1*2.4**3/12
    divisor = 48 if ends == 'pinned' else 192
    beam = span**3/(divisor*Eframe*Icheek)
    posts = .5*68**3/(3*Eframe*Ipost)
    bridge = .5*3.5/(Eframe*1*2)  # favorable axial contribution only
    return beam+posts+bridge


def response(c, a, Ecore, gap, compliance, force=.13405):
    """Clamp + eccentric couple + unilateral lateral guide with slack.

    Complementarity solved analytically. No column contact, axial preload,
    bearing friction or geometric stiffness. h=a-10, loaded sleeve half-length3.1.
    """
    EI = Ecore*math.pi*c['rail_d']**4/64
    M = force*(X-(c['tip']+c['foot']/2)/2)
    free_top = M*a*(2*L-a)/(2*EI)
    R = -max(0.,free_top-gap)/(L**3/(3*EI)+compliance)
    u = M*a*a/(2*EI)+R*a*a*(3*L-a)/(6*EI)
    theta = M*a/EI+R*a*(2*L-a)/(2*EI)
    utop = free_top+R*L**3/(3*EI)
    relative = utop+R*compliance
    assert R <= 1e-12 and relative <= gap+1e-9
    assert abs(R*(relative-gap)) < 1e-8
    return dict(envelope=abs(u)+3.1*abs(theta),u=u,theta=theta,R=R,
                top=utop,relative_top=relative)


def worst(c, Ecore, gap, compliance, n=1024, force=.13405):
    samples = [dict(a=9.5+41*k/n, **response(c,9.5+41*k/n,Ecore,gap,compliance,force))
               for k in range(n+1)]
    return max(samples, key=lambda s:s['envelope'])


def sweep(cases):
    rows=[]
    for Ecore, Eframe, gap, kind in itertools.product(
            (2000.,100000.,200000.),(2000.,100000.),(0.,.05,.15,.3),
            ('ideal','edge','distributed')):
        C=support_compliance(kind,Eframe)
        results=[(worst(c,Ecore,gap,C,n=1024),c) for c in cases]
        best,c=min(results,key=lambda pair:pair[0]['envelope']/pair[1]['route_margin'])
        passing=[c for s,c in results if s['envelope']<c['route_margin']]
        rows.append(dict(Ecore=Ecore,Eframe=Eframe,gap=gap,kind=kind,
                         compliance=C,sections_below_route_margin=len(passing),
                         thicker_sections_below_margin=sum(c['wall']>=.4 for c in passing),
                         best_ratio=best['envelope']/c['route_margin'],
                         best_section=c,best_response=best))
    return rows


def checks(c):
    # Independent curvature integration, point-couple discontinuity handled
    # explicitly. Simpson quadrature is exact here (piecewise quadratic).
    def simpson(f,left,right):
        return (right-left)*(f(left)+4*f((left+right)/2)+f(right))/6
    E, a, gap = 100000.,37.125,.15
    C=support_compliance('distributed')
    s=response(c,a,E,gap,C)
    EI=E*math.pi*c['rail_d']**4/64
    M=.13405*(X-(c['tip']+c['foot']/2)/2)
    lower=lambda x: (M+s['R']*(L-x))/EI
    upper=lambda x: s['R']*(L-x)/EI
    theta=simpson(lower,0,a)
    u=simpson(lambda x:(a-x)*lower(x),0,a)
    tip=simpson(lambda x:(L-x)*lower(x),0,a)+simpson(lambda x:(L-x)*upper(x),a,L)
    assert max(abs(theta-s['theta']),abs(u-s['u']),abs(tip-s['top'])) < 1e-11
    assert worst(c,E,0,0,force=0)['envelope'] == 0
    # Slack support recovers original cantilever response at the load.
    free=response(c,50.5,E,1e6,0)
    assert abs(free['u']-prior.free_response(c,E)) < 1e-12
    assert abs(response(c,a,E*2,0,0)['u']*2-response(c,a,E,0,0)['u']) < 1e-12
    # Use an interior maximum, not a trivially sampled stroke endpoint.
    interior=dict(c,rail_d=.4)
    vals=[worst(interior,E,.15,C,n=n)['envelope'] for n in (64,256,1024,4096)]
    assert abs(vals[-1]-vals[-2]) < 1e-6
    # Beam flexibility independently follows unit-load virtual work.
    span=P; EIcheek=2000*4*.4**3/12
    virtual=2*simpson(lambda x:(x/2)**2/EIcheek,0,span/2)
    assert abs(virtual-span**3/(48*EIcheek)) < 1e-12
    return dict(curvature_residual_mm=abs(tip-s['top']),refinement=vals)


if __name__ == '__main__':
    cases=sections()
    thin=min(cases,key=lambda c:prior.free_response(c)/c['route_margin'])
    thick=min((c for c in cases if c['wall']>=.4),key=lambda c:prior.free_response(c))
    print(json.dumps(dict(sections=len(cases),geometry=geometry(thin),
        thick_geometry=geometry(thick),sweep=sweep(cases),checks=checks(thin),
        thick_ideal_zero_gap=worst(thick,100000,0,0,n=4096),
        edge_clamped_compliance=support_compliance('edge',2000,'clamped'),
        force_sensitivity=[dict(force=f,**worst(thin,100000,.15,
                           support_compliance('distributed'),force=f))
                           for f in (0.,.13405,1.)],
        inventory=dict(distributed_posts=80*81,longitudinal_cheeks=160,
                       guide_length_mm=160*81*P,
                       post_volume_litre=80*81*2.4*1*72/1e6,
                       ten_second_post_assembly_hours=80*81*10/3600)),indent=2))
