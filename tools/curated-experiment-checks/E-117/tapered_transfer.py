#!/usr/bin/env python3
"""E-117 deterministic finite tapered-pin transfer. Units mm, N, MPa.
All error/friction/strength values are explicit bounds, not measured priors.
No random population or full selector acceptance. Standard library only.
"""
from dataclasses import dataclass
from itertools import product
import json

EPS = 1e-9

@dataclass(frozen=True)
class Pin:
    width: float = 1.4
    tip: float = .2
    taper: float = 1.5
    length: float = 14.2

    def half(self, z):
        assert -EPS <= z <= self.length+EPS
        return self.tip/2 + (self.width-self.tip)/2 * min(1., max(0.,z)/self.taper, max(0.,self.length-z)/self.taper)

@dataclass(frozen=True)
class Slot:
    bottom: float
    top: float
    center: float
    half_width: float
    slope: float
    y: float = 0.

    def interval(self, pin, q):
        lo=max(0.,self.bottom-q); hi=min(pin.length,self.top-q)
        if lo > hi+EPS: return None
        zs=[lo,hi]+[v for v in (pin.taper,pin.length-pin.taper) if lo<=v<=hi]
        radius=max(pin.half(z) for z in zs)
        clearance=self.half_width-(1+self.slope)*radius
        center=self.center-self.slope*self.y
        return (center-clearance,center+clearance)


def intersection(intervals):
    valid=[v for v in intervals if v is not None]
    if not valid: return None
    return max(v[0] for v in valid),min(v[1] for v in valid)


def knots(pin, slots, ends):
    """All axial contact/topology changes; slot interval endpoints affine between."""
    a,b=sorted(ends)
    return sorted({a,b}|{face-z for s in slots for face in (s.bottom,s.top)
                        for z in (0.,pin.taper,pin.length-pin.taper,pin.length)
                        if a<face-z<b})


def boundary_interval(pin, slots, q, direction):
    # One-sided limit excludes a plate being exited. The finite tip causes a
    # genuine entry constraint; it must contain all possible prior positions.
    active=[]
    for s in slots:
        if q+pin.length<s.bottom-EPS or q>s.top+EPS: continue
        if direction>0 and abs(q-s.top)<EPS: continue
        if direction<0 and abs(q+pin.length-s.bottom)<EPS: continue
        active.append(s.interval(pin,q))
    return intersection(active)


def path(pin, slots, ends):
    """Set-valued contact path; check ALL source slack at each new entry.
    Within each segment constraints are affine. Nonempty endpoint intersections
    imply nonempty convex feasible (q,x) strip throughout. Projection moves the
    output only when a taper wall contacts it; no commanded centering is assumed.
    """
    direction=1 if ends[1]>ends[0] else -1
    nodes=knots(pin,slots,ends)
    if direction<0: nodes.reverse()
    initial=boundary_interval(pin,slots,nodes[0],direction)
    if initial is None or initial[0]>initial[1]: return {'ok':False,'reason':'initial'}
    worst_entry=1e9; min_width=1e9; max_motion=0.; traces=[]
    for start in initial:
        x=start; trace=[(nodes[0],x)]
        for a,b in zip(nodes,nodes[1:]):
            # Include both one-sided sets at an event. Immediately before entry
            # any point in the old interval is a permissible stationary state.
            old=boundary_interval(pin,slots,a,-direction)
            new=boundary_interval(pin,slots,a,direction)
            if old is not None and new is not None:
                entering=any(abs(a+pin.length-s.bottom)<EPS if direction>0 else abs(a-s.top)<EPS for s in slots)
                if entering:
                    entrants=[s.interval(pin,a) for s in slots if (abs(a+pin.length-s.bottom)<EPS if direction>0 else abs(a-s.top)<EPS)]
                    receiving=intersection(entrants)
                    margin=min(old[0]-receiving[0],receiving[1]-old[1])
                    worst_entry=min(worst_entry,margin)
                    if margin < -EPS: return {'ok':False,'reason':'tip_entry','margin':margin}
            end=boundary_interval(pin,slots,b,-direction)
            if new is None or end is None: return {'ok':False,'reason':'ungrounded'}
            min_width=min(min_width,new[1]-new[0],end[1]-end[0])
            if min_width < -EPS: return {'ok':False,'reason':'opposed_walls','margin':min_width}
            # Projection onto moving convex interval; each endpoint is piecewise
            # affine, and clamp is exact for monotone ramps in this segment.
            x=max(end[0],min(end[1],x));trace.append((b,x));max_motion=max(max_motion,abs(x-start))
        traces.append(trace)
    return dict(ok=True,entry_margin=worst_entry,min_interval_width=min_width,max_recenter=max_motion,traces=traces)


def scenario(e, signs, gap=.65, taper=1.5):
    # Common XY bias translates both slots and pin, hence cancels exactly.
    # Remaining independent +/-e relative errors may be coherent across a bank.
    dp,dt,dl,ck,cc,dy,wk,wc,zk,zc= [v*e for v in signs]
    pin=Pin(width=1.4+dp,tip=.2+dp,taper=taper+dt,length=14.2+dl)
    slots=[Slot(-1.2+zk,zk,ck,.7+gap+wk,0),
           Slot(10+zc,11.2+zc,cc,1.05+gap+wc,.5,dy)]
    return pin,slots


def finite_holdout(pin,slots,ends,n=256):
    # Independent plane/vertex clipping: sample the actual 3D square-pin profile
    # at all plate faces and pin breaks. Find feasible x by half-plane extrema.
    xlo=1e9;xhi=-1e9;minimum=1e9
    for i in range(n+1):
        q=ends[0]+(ends[1]-ends[0])*i/n
        left=[];right=[]
        for s in slots:
            zs=[z for z in (q,q+pin.taper,q+pin.length-pin.taper,q+pin.length,s.bottom,s.top)
                if q-EPS<=z<=q+pin.length+EPS and s.bottom-EPS<=z<=s.top+EPS]
            if not zs: continue
            for z in zs:
                r=pin.half(z-q)
                for ux,uy in product((-r,r),repeat=2):
                    left.append(s.center-s.half_width-ux-s.slope*(s.y+uy))
                    right.append(s.center+s.half_width-ux-s.slope*(s.y+uy))
        assert left
        lo,hi=max(left),min(right)
        assert hi-lo>=-EPS
        expected=intersection([s.interval(pin,q) for s in slots])
        assert abs(lo-expected[0])<EPS and abs(hi-expected[1])<EPS
        xlo=min(xlo,lo);xhi=max(xhi,hi);minimum=min(minimum,hi-lo)
    return dict(x_bounds=[xlo,xhi],min_width=minimum)


def force(tangent,mu):
    # Equivalent 2D Coulomb contact ONLY. The oblique square-cam edge has
    # a 3D normal cone: this projected model is NOT a certified force bound.
    # Wall tangent for insertion: v=(-a,1). Reaction N*(-1,-a),
    # friction -mu*N*v. Horizontal recenter F=N*(1-mu*a).
    # Thus axial push/F=(a+mu)/(1-mu*a).
    # On extraction with outward load F: axial resistance/F=(mu-a)/(1+mu*a).
    return dict(push_gain=(tangent+mu)/(1-mu*tangent),
                pull_gain=max(0.,(mu-tangent)/(1+mu*tangent)),
                self_eject_gain=max(0.,(tangent-mu)/(1+mu*tangent)))


def main():
    rows=[];witness=None
    for e in (.05,.1,.2):
        failures={};minimum=1e9;entry=1e9;recenter=0.;xbound=0.
        for signs in product((-1,1),repeat=10):
            pin,slots=scenario(e,signs)
            for ends in ((-5.2,1.),(1.,-5.2)):
                result=path(pin,slots,ends)
                if not result['ok']:
                    reason=result['reason'];failures[reason]=failures.get(reason,0)+1
                else:
                    minimum=min(minimum,result['min_interval_width']);entry=min(entry,result['entry_margin']);recenter=max(recenter,result['max_recenter'])
                    for q in knots(pin,slots,ends):
                        iv=intersection([s.interval(pin,q) for s in slots]);xbound=max(xbound,abs(iv[0]),abs(iv[1]))
                    if e==.1 and (witness is None or result['max_recenter']>witness['result']['max_recenter']):
                        witness=dict(signs=signs,result=result)
        # Analytical envelopes cover the continuous error box, unlike corner counts.
        # Full-width C/K intervals overlap; taper intervals are supersets.
        analytic=dict(forward_tip=.9-4.75*e,reverse_tip=.6-4.75*e,
                      intersection_width=1.3-5.75*e,full_waist_bridge=1.2-5*e,
                      independent_tip_reverse=.6-5.75*e)
        if not failures:
            assert abs(entry-min(analytic['forward_tip'],analytic['reverse_tip']))<EPS
            assert abs(minimum-analytic['intersection_width'])<EPS
        rows.append(dict(e=e,analytic=analytic,cases=2048,failures=failures,min_width=minimum,entry_margin=entry,max_recenter=recenter,x_bound=xbound))
    assert not rows[1]['failures']
    pin,slots=scenario(.1,witness['signs'])
    holdouts=[finite_holdout(pin,slots,(-5.2,1.),n) for n in (64,256,1024)]
    # Rigid support blade margins, including bounded backlash and nose datum.
    # Wider row cartridge is an explicit packaging change, not pitch compliance.
    e=.1;B=rows[1]['x_bound'];nose=1.2;stroke=3.;depth=2.5
    blade=stroke+2*B+2*e+.8
    support=dict(overlap=nose-B-e,withdrawal=stroke-nose-B-e,
                 back=depth-e-(nose+B+e),blade_length=blade,
                 width=depth+blade+stroke-nose+B+.8+4*e)
    assert min(support[k] for k in ('overlap','withdrawal','back'))>=.05
    # Finite rectangular blade and fixed guide at every extreme position.
    guide_right=nose-stroke-B-e
    guide=(guide_right-.8,guide_right)
    for tip in (nose-B-e,nose+B+e,nose-stroke-B-e,nose-stroke+B+e):
        polygon=[(tip-blade,-.8),(tip,-.8),(tip,0),(tip-blade,0)]
        assert polygon[0][0]<=guide[0]+EPS and polygon[1][0]>=guide[1]-EPS
        assert polygon[1][0]<=depth-e-.05
    assert guide[1]<0
    support['fixed_guide']=guide
    # Finite cam end faces: working motion s=0..6 shifts slot center -0.5s.
    # y in pin frame is s+dy, finite slot runs from -Y to 6+Y.
    # Every square corner remains inside its ends, including endpoint errors.
    Y=.7+.65
    for phase,dy,pw in product((0.,1.),(-e,e),(1.4-e,1.4+e)):
        for side in (-1,1):
            assert -Y <= 6*phase+dy+side*pw/2 <= 6+Y
    cam_vertices=[(sign*1.7-.5*y,y) for y,sign in [(-Y,-1),(-Y,1),(6+Y,1),(6+Y,-1)]]
    # Retained command slack from the E-116 gate, with changed vertical package.
    drift=5*e+.05
    endpoint=dict(low_cam_clear=1.-drift-2*e,
                  high_keeper_clear=1.-drift-e,
                  high_full_cam_above_top=(1.+14.2-1.5)-11.2-drift-3*e,
                  low_full_keeper_below_bottom=-1.2-(-5.2+1.5)-drift-2*e)
    assert min(endpoint.values())>.05
    # Full-width pin material common to EVERY selection position, with all
    # errors and retained endpoint slack. Any permanent finite output guide must
    # lie within this interval if it is to support the pin in both states.
    waist=(1.+drift+1.5+e,-5.2-drift+14.2-e-(1.5+e))
    bearing_lower=(3.3,4.1);bearing_upper=(5.7,6.5)
    assert waist[0]<=bearing_lower[0] and bearing_upper[1]<=waist[1]
    # At the upper load layer both output bearings lie below cam contact;
    # at lower keeper layer both lie above. Cannot use simply-supported bending.
    assert bearing_upper[1] < slots[1].bottom
    assert bearing_lower[0] > slots[0].top
    # Even arbitrary L cannot straddle a cam layer with a fixed closed guide:
    # in idle the entire pin ends below the cam. This also holds with zero taper.
    assert -5.2+14.2 < 10
    mu_cases=[]
    for mu in (0.,.1,.3,.5,.7):
        for t in (1.4,1.6):
            for m in (0.,.5):
                a=.6/t*(1+m);f=force(a,mu)
                assert 1-mu*a>0
                if mu==0: assert abs(f['push_gain']-a)<EPS and f['pull_gain']==0
                mu_cases.append(dict(mu=mu,taper=t,slot_slope=m,**f))
    # Mid-stroke pin remains in BOTH layers. At cam stroke, no position can
    # satisfy both full-width intervals: actual finite interference, not overload
    # inferred from an abstract command bit. Verify with manufactured vertices.
    pin,slots=scenario(.1,(1,)*10)
    q=-2.1;K=slots[0].interval(pin,q);C=slots[1].interval(pin,q)
    jam_gap=K[0]-(C[1]-stroke)
    assert jam_gap>0
    # Independent square-corner penetration at the closest admissible keeper x.
    r=pin.width/2;cam=slots[1]
    penetration=max(abs(K[0]+ux+cam.slope*(cam.y+uy)-cam.center+stroke)-cam.half_width
                    for ux,uy in product((-r,r),repeat=2))
    assert abs(penetration-jam_gap)<EPS
    # Relax shared tip/waist bias and reconstruct the adverse reverse entrance.
    varied_pin=Pin(width=1.3,tip=.3)
    varied_slots=[Slot(-1.2,0,-.1,1.25,0),Slot(10,11.2,.1,1.8,.5,-.1)]
    independent_tip=path(varied_pin,varied_slots,(1.,-5.2))
    assert independent_tip['ok'] and abs(independent_tip['entry_margin']-.025)<EPS
    nominal_pin,nominal_slots=scenario(0.,(1,)*10)
    for ends in ((-5.2,1.),(1.,-5.2)):
        nominal=path(nominal_pin,nominal_slots,ends)
        assert nominal['ok'] and nominal['max_recenter']<EPS
    # Bending upper bound favorable contact face; interval uses far face too.
    force_bounds=[]
    for sigma,drag in product((5.,10.,20.),(.005,.01,.05)):
        b=1.3;Z=b**3/6
        lever_lo=10-e-bearing_upper[1];lever_hi=11.2+e-bearing_upper[0]
        cap_lo=sigma*Z/lever_hi;cap_hi=sigma*Z/lever_lo
        force_bounds.append(dict(sigma=sigma,drag=drag,capacity=[cap_lo,cap_hi],bank_output=80*drag,
                                 common_window_conservative=cap_lo-80*drag))
    # Additional axial sliding drag from overhung guide reaction amplification.
    # Exact in the planar two-point-bearing idealization only; finite bearing
    # distributions, tilt and the oblique contact cone remain unqualified.
    bearing_centers=(3.7,6.1)
    load_z=11.3
    amplification=(2*load_z-sum(bearing_centers))/(bearing_centers[1]-bearing_centers[0])
    guide_drag_per_output=[dict(mu_b=mu,additional_axial_gain=mu*amplification) for mu in (.1,.3,.5,.7)]
    # Control: zero taper reduction degenerates into E-116 blunt transfer.
    blunt=Pin(width=1.4,tip=1.4)
    control=[path(blunt,scenario(.1,(1,-1,1,-1,1,-1,-1,1,-1,-1))[1],ends)
             for ends in ((-5.2,1.),(1.,-5.2))]
    assert any(not r['ok'] for r in control)
    print(json.dumps(dict(evidence='bounded finite sections and quasistatic forces; not machine/yield',
                         sweep=rows,witness=witness,holdouts=holdouts,support=support,
                         retained_endpoint_reserves=endpoint,permanent_full_waist=waist,
                         output_bearings=[bearing_lower,bearing_upper],finite_nominal_cam_vertices=cam_vertices,force_gains=mu_cases,
                         stuck_bridge=dict(q=q,keeper=K,cam_home=C,stroke=stroke,gap=jam_gap,vertex_penetration=penetration),
                         independent_tip_margin=independent_tip['entry_margin'],
                         bending_scenarios=force_bounds,guide_drag=guide_drag_per_output,blunt_control=control),indent=2))

if __name__=='__main__':main()
