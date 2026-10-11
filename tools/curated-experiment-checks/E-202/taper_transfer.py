#!/usr/bin/env python3
"""E-202. Finite square double-frustum pin between extruded keeper/cam slots.
Units mm, N. Explicit bounded scenarios, no process probabilities or dynamics.
Only x and z translate; y datum is fixed. External bilateral z drive is assumed.
"""
from dataclasses import dataclass
from itertools import product
import json
from math import sqrt

TOL = 1e-9
E = .05
M = .3
G = 4.
PLATE = 1.2
DRIFT = .30

@dataclass(frozen=True)
class Pin:
    b: float
    tip: float
    length: float
    taper: float

    def width(self, z):
        return self.tip + (self.b-self.tip)*min(1., max(0., min(z, self.length-z)/self.taper))

@dataclass(frozen=True)
class Slot:
    lo: float
    hi: float
    center: float
    half: float
    slope: float
    ymin: float
    ymax: float


def stations(pin, q, slot):
    lo, hi = max(0., slot.lo-q), min(pin.length, slot.hi-q)
    if lo > hi+TOL:
        return []
    return sorted(set([lo, hi]+[z for z in (pin.taper,pin.length-pin.taper) if lo < z < hi]))


def interval(pin, q, slot, y):
    zs = stations(pin, q, slot)
    if not zs:
        return None
    b = max(pin.width(z) for z in zs)
    if y-b/2 < slot.ymin-TOL or y+b/2 > slot.ymax+TOL:
        raise AssertionError('finite y end collision')
    half = slot.half-b*(1+slot.slope)/2
    c = slot.center-slot.slope*y
    return (c-half,c+half)


def bounds(pin,q,slots,y):
    active=[v for s in slots if (v:=interval(pin,q,s,y)) is not None]
    assert active, 'no lateral capture'
    return max(v[0] for v in active), min(v[1] for v in active)


def knots(pin, slots, q0, q1):
    # All changes in the clipped frustum/plate topology, plus support crossover.
    k=sorted(set([q0,q1]+[face-z for s in slots for face in (s.lo,s.hi)
        for z in (0.,pin.taper,pin.length-pin.taper,pin.length)
        if q0 < face-z < q1]))
    # Extremum of max(keeper shank overlap, cam shank overlap) can be between knots.
    out=list(k)
    for a,b in zip(k,k[1:]):
        da=shank(pin,a,slots[0])-shank(pin,a,slots[1])
        db=shank(pin,b,slots[0])-shank(pin,b,slots[1])
        if da*db<0:
            out.append(a+(b-a)*da/(da-db))
    return sorted(out)


def shank(pin,q,s):
    return max(0.,min(q+pin.length-pin.taper,s.hi)-max(q+pin.taper,s.lo))


def vertices_clear(pin,q,x,y,slots):
    # Independent explicit clipped-frustum vertices against all finite slot faces.
    worst=1e9
    for s in slots:
        for z in stations(pin,q,s):
            w=pin.width(z)
            for dx,dy in product((-w/2,w/2),repeat=2):
                X,Y=x+dx,y+dy
                worst=min(worst,s.half-abs(X+s.slope*Y-s.center),Y-s.ymin,s.ymax-Y)
    return worst


def trace(pin,slots,y,q0,q1,n=0):
    ks=knots(pin,slots,q0,q1)
    if n:
        ks=sorted(set(ks+[q0+(q1-q0)*i/n for i in range(n+1)]))
    # All limiting entrance intervals must already contain the incoming path.
    # Active plate switches otherwise create an unphysical instantaneous recenter.
    margin=min(bounds(pin,q,slots,y)[1]-bounds(pin,q,slots,y)[0] for q in ks)
    cover=min(max(shank(pin,q,s) for s in slots) for q in ks)
    if margin < -TOL:
        return {'failure':'pinch','margin':margin,'shank_cover':cover}
    max_jump=0.; max_shift=0.; min_face=1e9; max_entry_penetration=0.
    for grid in (ks,list(reversed(ks))):
        lo,hi=bounds(pin,grid[0],slots,y)
        for initial in (lo,hi):
            x=initial
            for prev,q in zip(grid,grid[1:]):
                # Just before a new plate is touched, retain the limiting x.
                before=q+(prev-q)*1e-8
                l,h=bounds(pin,before,slots,y)
                old=min(h,max(l,x))
                l,h=bounds(pin,q,slots,y)
                new=min(h,max(l,old))
                max_entry_penetration=max(max_entry_penetration,-vertices_clear(pin,q,old,y,slots))
                max_jump=max(max_jump,abs(new-old))
                x=new
                max_shift=max(max_shift,abs(x-initial))
                min_face=min(min_face,vertices_clear(pin,q,x,y,slots))
    return dict(failure='entrance' if max_jump>1e-6 else None,
                margin=margin,shank_cover=cover,jump=max_jump,
                lateral_shift=max_shift,min_face=min_face,entry_penetration=max_entry_penetration)


def horizontal(p=.6,e=E):
    for dp,ck,cc,dy,wk,wc in product((-e,e),repeat=6):
        yield p+dp,ck,cc,dy,p/2+.2+wk,p*(1+M)/2+.2+wc


def make_slots(h,dlo=0.,dup=0.,nominal=.6):
    b,ck,cc,dy,hk,hc=h
    Y=nominal/2+.2
    return (Slot(-PLATE+dlo,dlo,ck,hk,0.,-Y+E,Y-E),
            Slot(G+dup,G+PLATE+dup,cc,hc,M,-3-Y+E,Y-E))


def contact_gain(r,m,mu):
    # Square-frustum corner at straight oblique mouth lip. Horizontal normal
    # ratio (1,m) follows lip tangent (-m,1,0); frustum gives axial slope a.
    # Bilateral y guide is frictionless. Coulomb sliding vector is (a,0,1).
    a=(1+m)*r
    norm=sqrt(1+m*m+a*a)
    speed=sqrt(1+a*a)
    x_per_N=1/norm-mu*a/speed
    if x_per_N<=1e-12:
        return None
    N=1/x_per_N  # unit transverse resistance
    F=N*(a/norm+mu/speed)
    assert abs(N/norm-mu*N*a/speed-1)<TOL
    assert abs(F-N*a/norm-mu*N/speed)<TOL
    reaction_y=-N*m/norm
    assert abs(N*m/norm+reaction_y)<TOL
    assert abs(sum(n*v for n,v in zip((1.,m,-a),(a,0.,1.))))<TOL
    return F


def aperture(nominal,tipmax):
    blunt=[]; mouth=[]; overlap=[]
    for h in horizontal(nominal):
        b,ck,cc,dy,hk,hc=h
        K=(ck-hk+b/2,ck+hk-b/2)
        C=(cc-M*dy-hc+b*(1+M)/2,cc-M*dy+hc-b*(1+M)/2)
        blunt.append(max(C[0]-K[0],K[1]-C[1],K[0]-C[0],C[1]-K[1]))
        Ktip=(ck-hk+tipmax/2,ck+hk-tipmax/2)
        Ctip=(cc-M*dy-hc+tipmax*(1+M)/2,cc-M*dy+hc-tipmax*(1+M)/2)
        mouth.append(min(K[0]-Ctip[0],Ctip[1]-K[1],C[0]-Ktip[0],Ktip[1]-C[1]))
        overlap.append(min(K[1],C[1])-max(K[0],C[0]))
    return dict(blunt_max_mismatch=max(blunt),tip_capture_reserve=min(mouth),
                full_shank_interval_width=min(overlap))


def main():
    configurations=[dict(name='original_package',p=.6,tip=.1,extra=.8,t=.225),
                    dict(name='wider_longer_transfer',p=.8,tip=.2,extra=1.4,t=.4)]
    results=[]
    for cfg in configurations:
        ap=aperture(cfg['p'],cfg['tip']+E)
        assert abs(ap['blunt_max_mismatch']-.2225)<TOL
        search=[]
        for t in (.10,.15,.20,.225,.25,.30,.40,.60,.80):
            tlo,thi=t-E,t+E
            ratio=(cfg['p']+E-(cfg['tip']-E))/(2*tlo)
            cover=(cfg['extra']-3*E-2*thi)/2
            gains={str(mu):contact_gain(ratio,M,mu) for mu in (.1,.3,.5,.8)}
            search.append(dict(taper=t,worst_radial_slope=ratio,shank_cover_bound=cover,
                cam_insertion_gain=gains,
                passes_entrance_cover_mu05=ap['tip_capture_reserve']>=0 and cover>=.05-TOL and gains['0.5'] is not None))
        cases=0; failures={}; min_cover=1e9; min_margin=1e9; max_shift=0.; min_face=1e9
        witnesses={}; max_entry=0.
        # 64 horizontal corners x 32 axial/tip corners. A common taper length
        # error affects both ends coherently. Extremal lengths bound separate
        # taper errors for mouth, slope and shank-overlap necessary conditions.
        for h in horizontal(cfg['p']):
            for dl,dlo,dup,dt,dtip in product((-E,E),repeat=5):
                p=Pin(h[0],cfg['tip']+dtip,G+cfg['extra']+dl,cfg['t']+dt)
                slots=make_slots(h,dlo,dup,cfg['p'])
                idle_hi=-cfg['extra']-.6+DRIFT
                selected_lo=.6-DRIFT
                assert slots[1].lo-(idle_hi+p.length)>=.2-TOL
                assert selected_lo-slots[0].hi>=.25-TOL
                for q in (-cfg['extra']-.6-DRIFT,idle_hi):
                    assert shank(p,q,slots[0])>=.05-TOL
                for q in (selected_lo,.6+DRIFT):
                    assert shank(p,q,slots[1])>=.05-TOL
                r=trace(p,slots,h[3],-cfg['extra']-.6-DRIFT,.6+DRIFT)
                cases+=1
                reason=r['failure'] or ('shank' if r['shank_cover']<.05-TOL else 'pass')
                failures[reason]=failures.get(reason,0)+1
                min_cover=min(min_cover,r['shank_cover']); min_margin=min(min_margin,r['margin'])
                max_shift=max(max_shift,r.get('lateral_shift',0)); min_face=min(min_face,r.get('min_face',1e9))
                max_entry=max(max_entry,r.get('entry_penetration',0))
                if reason not in witnesses and reason!='pass':
                    witnesses[reason]=dict(horizontal=h,axial=[dl,dlo,dup,dt,dtip],result=r)
        bound=max(0.,(cfg['extra']-3*E-2*(cfg['t']+E))/2)
        assert abs(min_cover-bound)<TOL
        results.append(dict(configuration=cfg,aperture=ap,search=search,cases=cases,outcomes=failures,
            min_shank_cover=min_cover,min_interval_width=min_margin,max_lateral_shift=max_shift,
            min_face_clearance=min_face,max_entry_penetration=max_entry,witnesses=witnesses))
    assert results[0]['outcomes'].get('entrance',0)>0
    assert results[1]['outcomes']=={'pass':2048}
    # Actual vertices on the widest, shortest pin / adverse gap holdout.
    h=(.85,-.05,.05,-.05,.55,.67)
    p=Pin(.85,.25,5.35,.45); slots=make_slots(h,-.05,.05,.8)
    holdout=[trace(p,slots,h[3],-2.3,.9,n) for n in (16,64,256)]
    assert all(r['failure'] is None and r['min_face']>=-TOL for r in holdout)
    assert max(r['shank_cover'] for r in holdout)-min(r['shank_cover'] for r in holdout)<TOL
    # Original discontinuous-entry control, independently specified geometry.
    p=Pin(.65,.65,4.8,.25); h=(.65,-.05,.05,-.05,.55,.54)
    control=trace(p,make_slots(h),h[3],-1.7,.9)
    assert control['failure']=='entrance' and abs(control['entry_penetration']-.2225)<TOL
    # Frictionless virtual work, 2D wedge formula, singular boundary.
    for r in (0.,.6,1.5):
        assert abs(contact_gain(r,M,0)-(1+M)*r)<TOL
        for mu in (.1,.3,.5):
            assert abs(contact_gain(r,0,mu)-(r+mu)/(1-mu*r))<TOL
    assert contact_gain(2.,0,.5) is None
    # Same optimistic unsupported pin lever as E-116; no credit for a new bearing.
    limiter=[]
    for width in (.6,.8):
        passing=0
        for sigma,drag,mu in product((5.,10.,20.),(.005,.01,.05),(.1,.3,.5)):
            capacity=sigma*(width-E)**3/(6*2.4)
            passing+=capacity>80*drag
        limiter.append(dict(nominal_width=width,passing_scenarios=passing,total=27,
                            capacity_at_20MPa=20*(width-E)**3/(6*2.4)))
    print(json.dumps(dict(evidence='finite geometry and conditional contact bounds; no dynamics/hardware',
        results=results,holdout=holdout,blunt_control=control,shared_limiter=limiter),indent=2))

if __name__=='__main__':
    main()
