#!/usr/bin/env python3
"""E-250: rigid axial turn, fixed finite rail, unchanged square caps.
mm/seconds/degrees; labelled scenarios, no process priors or hardware claims.
"""
import importlib.util
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location('e167', Path(__file__).resolve().parents[1]/'E-167/probe.py')
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
P, D = 5.08, 4.8


def rect(x0,x1,y0,y1):
    return [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]


def rotate(poly,theta):
    c,s=math.cos(theta),math.sin(theta)
    return [(x*c-y*s,x*s+y*c) for x,y in poly]


def cap_limit(E=0,d=D):
    # E: total adverse horizontal gap loss. Here realized as relative pitch loss.
    k=(2*(P-E)/d-1)/math.sqrt(2)
    if P-E<=d: return 0.
    if k>=1: return math.pi/4
    return math.pi/4-math.acos(k)


def support_release(E=0):
    # Lug [.6,2] x [-.4,.4]; finite rail [1.2,2.54] x [-1,-.1].
    # E grows rail top in +y, reducing release gap. Last contact is rail's
    # upper-left corner with lug's rotated lower edge; valid in tested range.
    c=.1-E
    return math.asin(.4/math.hypot(1.2,c))-math.atan2(c,1.2)


def t(d,v=200,a=8000):
    return 2*math.sqrt(d/a) if d<=v*v/a else d/v+v/a


def service(angle,lift,colors):
    # Same linear motion, empty parking and retry accounting as E-249.
    # Two color phases needed for adjacent integral caps turning through 45deg.
    angular=2*t(angle,720,7200)
    active=2*t(lift)+t(40)+angular+.1
    empty=2*t(40+lift)
    slot=empty+colors*active+t(P)
    for banks in range(1,81):
        total=2+(math.ceil(80/banks)+1)*slot
        if total<30:
            return dict(banks=banks,channels=80*banks,colors=colors,
                        active_s=active,empty_s=empty,slot_s=slot,map_s=total,
                        dollars_per_pair=(500-295)/(80*banks))


def main():
    lug=rect(.6,2,-.4,.4)
    rail=rect(1.2,2.54,-1,-.1)
    theta=cap_limit()
    release=support_release()
    # Independent finite SAT threshold checks, on both sides of analytic roots.
    for E in (0,.05,.1,.2):
        a=cap_limit(E)
        neighbor=g.rectangle(D/2,D/2,dx=P-E)
        assert not g.intersect(g.rectangle(D/2,D/2,a-1e-6),neighbor)
        assert g.intersect(g.rectangle(D/2,D/2,a+1e-6),neighbor)
        r=support_release(E)
        obstacle=rect(1.2,2.54,-1,-.1+E)
        assert g.intersect(rotate(lug,r-1e-6),obstacle)
        assert not g.intersect(rotate(lug,r+1e-6),obstacle)
    # An interior material point proves overlap throughout [-theta,+theta]:
    # x and y are monotone over this interval; both endpoint ranges are in rail.
    endpoints=[rotate([(1.6,-.35)],a)[0] for a in (-theta,theta)]
    assert all(1.2<x<2.54 and -1<y<-.1 for x,y in endpoints)
    # x'= -1.6sin(a)+.35cos(a)>0, y'=1.6cos(a)+.35sin(a)>0.
    assert .35*math.cos(theta)-1.6*math.sin(theta)>0
    assert 1.6*math.cos(theta)-.35*math.sin(theta)>0
    samples=[]
    for n in (16,64,256):
        angles=[-theta+2*theta*i/n for i in range(n+1)]
        count=sum(g.intersect(rotate(lug,a),rail) for a in angles)
        assert count==n+1
        samples.append(dict(intervals=n,blocked=count))
    # Lift is not an escape for small-angle held transit: cap crosses old-height U.
    # At lug bottom z=-.6, lug top=.6 intersects rail [-1.2,0].
    # Cap top=44-.6, bottom=42-.6 intersects unchanged [42,44].
    crossing=-.6
    support_hit=g.intersect(rotate(lug,theta),rail)
    cap_hit=g.intersect(g.rectangle(2.4,2.4,release+1e-5),
                        g.rectangle(2.4,2.4,dx=P))
    assert support_hit and cap_hit
    assert min(crossing+1.2,0)>max(crossing,-1.2)
    assert min(44+crossing,44)>max(42+crossing,42)
    # 90 degrees is an escape in XY, but continuous turn must cross forbidden angles.
    assert not g.intersect(rotate(lug,math.pi/2),rail)
    assert not g.intersect(g.rectangle(2.4,2.4,math.pi/2),g.rectangle(2.4,2.4,dx=P))
    assert g.intersect(g.rectangle(2.4,2.4,math.pi/4),g.rectangle(2.4,2.4,dx=P))
    # Critical cap width for this particular release angle; no surface acceptance implied.
    critical=2*P/(1+math.cos(release)+math.sin(release))
    sensitivities=[]
    for E in (0,.05,.1,.2,.28):
        a=cap_limit(E)
        # Corner travel is exact; chord is general point-displacement upper bound.
        sensitivities.append(dict(total_cap_gap_loss=E,cap_limit_deg=math.degrees(a),
            chord_at_R2_mm=4*math.sin(a/2),
            inward_rail_gap_loss=E,release_deg=math.degrees(support_release(E))))
    # Explicit union inventory: 72-mm r=.8 cylinder; 2mm cap; 5 integral lugs.
    # Lug/cylinder overlap integral through |y|<=.4, x>=.6.
    primitive=lambda y: .5*(y*math.sqrt(.8**2-y*y)+.8**2*math.asin(y/.8))
    overlap=2*(primitive(.4)-.6*.4)
    volume=(math.pi*.8**2*72 + D*D*2 + 5*1.2*(1.4*.8-overlap))*6400/1e6
    print(json.dumps(dict(cap_limit_deg=math.degrees(theta),release_deg=math.degrees(release),
        fixed_material_point_endpoints=endpoints,angular_samples=samples,
        crossing_z=crossing,cap_intrusion_at_release=2.4*(math.cos(release)+math.sin(release))+2.4-P,
        cap_width_at_release_touch=critical,coverage_at_touch=(critical/P)**2,
        sensitivity=sensitivities,
        service_oracles=dict(no_yaw=service(0,.6,1),failed_microturn=service(math.degrees(release),.6,1),
                             quarter_turn_one_color=service(90,2.3,1),quarter_turn_two_colors=service(90,2.3,2)),
        solid_liters=volume,extrusion_hours=[volume*1e6/(rate*3600) for rate in (15,5)]),indent=2))

if __name__=='__main__': main()
