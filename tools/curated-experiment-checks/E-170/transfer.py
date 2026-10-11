#!/usr/bin/env python3
"""Complementary bayonet-gate pickup, mm/N/s. Bounded scenarios, not priors.

Finite footprint clipping + independent separating-axis and corner checks.
No contact dynamics, material qualification, control hardware or yield claim.
"""
import importlib.util
import itertools
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    'bayonet', Path(__file__).resolve().parents[1] / 'E-167/probe.py')
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
L, W, A, S, D = 2.15, 1.2, 1.68, 1.4, 4.6


def clip(poly, axis, value, greater):
    out = []
    for p, q in zip(poly, poly[1:]+poly[:1]):
        ip = p[axis] >= value if greater else p[axis] <= value
        iq = q[axis] >= value if greater else q[axis] <= value
        if ip:
            out.append(p)
        if ip != iq:
            t = (value-p[axis])/(q[axis]-p[axis])
            out.append(tuple(p[k]+t*(q[k]-p[k]) for k in (0,1)))
    return out


def area(poly):
    return abs(sum(p[0]*q[1]-p[1]*q[0]
                   for p,q in zip(poly,poly[1:]+poly[:1])))/2


def overlap(poly, box):
    result = poly
    for axis in (0,1):
        for val, greater in ((min(p[axis] for p in box),True),
                             (max(p[axis] for p in box),False)):
            result = clip(result,axis,val,greater) if result else []
    return area(result)


def plates(a=A,s=S):
    fixed = b.gate(a=a,s=s,pocket=s)
    base = [poly for poly,z0,z1 in fixed if z1 == 0]
    pocket = [poly for poly,z0,z1 in fixed if z0 == 0]
    moving = [[(-y,x) for x,y in poly] for poly in base]
    return base,moving,pocket


def contact(delta, l=L,w=W,a=A,s=S,dx=0.,dy=0.):
    poly = b.rectangle(l,w,math.pi/2-delta,dx,dy)
    return tuple(sum(overlap(poly,box) for box in boxes)
                 for boxes in plates(a,s))


def first_angle(f, limit=math.pi/4):
    if f(0) >= 0:
        return 0.
    if f(limit) < 0:
        return None
    lo,hi = 0.,limit
    for _ in range(60):
        mid = (lo+hi)/2
        if f(mid) >= 0:
            hi = mid
        else:
            lo = mid
    return (lo+hi)/2


def cap_limit(e=0.,c=0.,exact_section=False):
    # Active cap held vertical by ideal torque writer. Neighbor leans toward
    # it; use whole-prism directional envelope at top z=44 (E-169).
    drift = c*(1+2*(43 if exact_section else 44)/25)
    half = D/2+e
    neighbor_half = half*math.sqrt(1+(2*c/25)**2) if exact_section else half
    return first_angle(lambda t: half*(math.cos(t)+math.sin(t))
                       +neighbor_half+e+drift-b.P)


def window(e,c):
    limit = cap_limit(e,c)
    # An admissible coherent size corner suffices to disprove robustness.
    # Shrunk lug, enlarged slot/central aperture, centered at the gate.
    begin = first_angle(lambda t: (L-e)*math.sin(t)+(W-e)*math.cos(t)-(S+e))
    nominal = contact(limit)[1]
    corners = [contact(limit,L+dl,W+dw,A+da,S+ds,dx,dy)[1]
               for dl,dw,da,ds,dx,dy in itertools.product((-e,e),repeat=6)]
    adverse = contact(limit,L-e,W-e,A+e,S+e)[1]
    return dict(e=e,guide_half_play=c,cap_angle_deg=math.degrees(limit),
                centered_pickup_onset_deg=math.degrees(begin),
                angle_window_deg=math.degrees(limit-begin),
                area_at_cap_limit_nominal=nominal,
                area_min_64_corners=min(corners),
                area_max_64_corners=max(corners),adverse_area=adverse,
                adverse_pressure_N1=(1/adverse if adverse>1e-10 else None),
                exact_tilted_section_limit_deg=math.degrees(cap_limit(e,c,True)))


def grid_area(delta,n):
    # Independent midpoint integration over lug-local coordinates, point
    # membership in moving plate aperture complement, no polygon clipping.
    theta=math.pi/2-delta
    hits=0
    for i in range(n):
        u=-L+(i+.5)*2*L/n
        for j in range(n):
            v=-W+(j+.5)*2*W/n
            x=u*math.cos(theta)-v*math.sin(theta)
            y=u*math.sin(theta)+v*math.cos(theta)
            hits += abs(x)>S and (abs(x)>A or abs(y)>A)
    return hits*4*L*W/n**2


def schedule():
    # Favorable altered mechanism: grants automatic contact transfer and
    # accessible retained rotary selectors, not earned by this geometry.
    # Four signed displacement groups, not old-height groups, per half-cycle.
    # One arm scan + four deposit scans per direction = ten scans per map.
    # All 20 nonidentity five-level transitions appear in each full row.
    def move(d,v=200.,a=5000.):
        return 2*math.sqrt(d/a) if d<=v*v/a else d/v+v/a
    def time(banks,slot):
        n=80//banks
        # Two stepped 40-mm excursions and two empty returns. 6-s reserve
        # for registration, additional microtravel, proof/retry and settling.
        return 6+10*n*slot+10*(n-1)*move(5.08)+8*move(10)+2*move(40)
    rows=[]
    for slot in (.02,.05,.1,.2):
        for banks in (1,2,4,8,16):
            channels=80*banks
            rows.append(dict(banks=banks,rotary_channels=channels,slot=slot,
                             seconds=time(banks,slot),
                             channel_ceiling_free_sites=250/channels,
                             channel_ceiling_2cent_sites=(250-128)/channels))
    # Logical reach only: not a physical support/contact replay.
    # Moving gate rejects only cells with theta
    # exactly in its through-slot. Commanded rotation remains independent.
    pairs=list(itertools.product(range(5),repeat=2))
    state=[old for old,new in pairs]
    events=[]
    for sign in (1,-1):
        active={i for i,(old,new) in enumerate(pairs) if sign*(new-old)>0}
        events.append(('arm',sign,len(active)))
        for step in range(1,5):
            for i in active:
                state[i]+=sign
                old,new=pairs[i]
                assert min(old,new)<=state[i]<=max(old,new)
            deposited={i for i in active if state[i]==pairs[i][1]}
            active-=deposited
            events.append(('deposit',sign,len(deposited)))
            assert all(state[i]==old for i,(old,new) in enumerate(pairs) if old==new)
        assert not active
    assert state==[new for old,new in pairs] and len(events)==10
    return rows


def main():
    # Geometry and units/limiting controls.
    assert abs(area(b.rectangle(2,3))-24)<1e-12
    assert abs(overlap(b.rectangle(2,3),b.rectangle(1,1))-4)<1e-12
    assert overlap(b.rectangle(1,1),b.rectangle(1,1,dx=2))==0
    f,m,p=contact(0)
    assert abs(f-4*W*(L-A))<1e-12 and m<1e-12 and p<1e-12
    f,m,p=contact(math.pi/2)
    assert f<1e-12 and abs(m-4*W*(L-A))<1e-12
    cap=cap_limit()
    onset=first_angle(lambda t:L*math.sin(t)+W*math.cos(t)-S)
    # Both finite-footprint methods agree near contact thresholds.
    for delta in (onset-1e-5,onset+1e-5,cap-1e-5,cap+1e-5,.2):
        poly=b.rectangle(L,W,math.pi/2-delta)
        for boxes in plates():
            for box in boxes:
                assert (overlap(poly,box)>1e-10)==b.intersect(poly,box)
    # Nominal cap collision independently checked against actual neighboring
    # rectangles at +/- small angular holdouts.
    for delta,hit in ((cap-1e-5,False),(cap+1e-5,True)):
        assert b.intersect(b.rectangle(D/2,D/2,delta),
                           b.rectangle(D/2,D/2,dx=b.P))==hit
    # Seated rigid pocket blocks every available pickup footprint. Grid
    # resolution is a holdout; footprint inclusion proves continuous result:
    # x extent < A up to cap limit, so moving-base overlap requires |y|>A,
    # |x|>S, precisely the fixed raised-pocket footprint.
    assert L*math.sin(cap)+W*math.cos(cap)<A
    checks=[]
    for n in (32,128,512):
        positive=0
        for i in range(n+1):
            d=cap*i/n
            fixed,moving,pocket=contact(d)
            assert fixed>0 and abs(moving-pocket)<1e-11
            if moving>1e-10:
                positive+=1
                assert b.collisions(math.pi/2-d,0,b.gate(a=A,s=S,pocket=S),L,W)>0
        checks.append(dict(intervals=n,pickup_poses=positive,unblocked_pickup_poses=0))
    # Geometric angle overlap is a best-case grant with pocket omitted.
    windows=[window(e,c) for c in (0.,.025) for e in (0.,.025,.05,.075)]
    assert window(.05,.025)['adverse_area']<1e-10
    # The tilted-neighbor rejection is also an actual section counterexample,
    # not a failure of a conservative sufficient envelope alone.
    exact_cap=cap_limit(.05,.025,True)
    assert exact_cap < math.radians(window(.05,.025)['centered_pickup_onset_deg'])
    half=D/2+.05
    slope=2*.025/25
    drift=.025*(1+2*43/25)
    neighbor=b.rectangle(half*math.sqrt(1+slope*slope),half,dx=b.P-.05-drift)
    for delta,hit in ((exact_cap-1e-5,False),(exact_cap+1e-5,True)):
        assert b.intersect(b.rectangle(half,half,delta),neighbor)==hit
    # Whole cap width exists at z=43: tilted prism local axial excursion <1.
    assert half*slope < 1
    fixed,moving,_=plates()
    plate_common_area=sum(overlap(p,q) for p in fixed for q in moving)
    independent_area=4*((b.P/2-S)**2-(A-S)**2)
    assert abs(plate_common_area-independent_area)<1e-11
    # Moving top starts -10; +10 travel places its base through fixed base.
    plate_volume=1.2*plate_common_area
    assert plate_volume>0
    # To avoid fixed plate thickness 1.2 on a 40-mm ascent, home separation
    # must exceed 41.2; congruent 10-mm lug spacing rounds it up to 50.
    gap=next(g for g in range(10,101,10) if g-40>1.2)
    assert gap==50
    # Fixed load lugs 0..40; moving lugs -50..-10, union ten stations.
    stations=sorted(set(range(0,41,10))|set(range(-gap,41-gap,10)))
    assert len(stations)==10
    exact=contact(cap)[1]
    quadrature=[dict(n=n,area=grid_area(cap,n)) for n in (64,256,1024)]
    assert abs(quadrature[-1]['area']-exact)<.0005
    # Wrongly armed neighbor has real lift contact, not just changed bits.
    half=contact(math.radians(10))[1]
    assert half>0
    # For pocket-removed section, the shared plate carrying it +2.3 mm
    # lifts the wrongly rotated column equally; fixed plate cannot oppose
    # upward motion. This is not a dynamic or strength prediction.
    print(json.dumps(dict(plate_collision_volume_mm3=plate_volume,
        minimum_full_stroke_home_gap=gap,lug_stations_mm=stations,
        nominal_onset_deg=math.degrees(onset),
        nominal_cap_limit_deg=math.degrees(cap),pocket_checks=checks,
        windows=windows,quadrature=quadrature,exact_nominal_area=exact,
        nominal_mean_pressure={str(F):F/exact for F in (.1,1,10)},
        false_arm_10deg_area=half,
        fixed_and_moving_midturn_area=contact(math.pi/4)[:2],
        optimistic_schedule=schedule()),indent=2))

if __name__=='__main__':
    main()
