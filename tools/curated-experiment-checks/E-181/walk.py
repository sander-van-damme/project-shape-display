#!/usr/bin/env python3
"""E-181: prescribed walking-clamp sections; deterministic bounds, not dynamics.
mm, N, s throughout except explicit energy conversion. JSON is disposable.
"""
import itertools
import json
import math


def move(d, v=200., a=5000.):
    return 2*math.sqrt(d/a) if d < v*v/a else d/v+v/a


def schedule(stroke=1., ramp=.003, dwell=.002, guard=.001, feed=.04):
    # Cyclic state: A closed, B open, B carrier at -stroke/2.
    knots = [(0., 0., .7, -stroke/2)]
    for duration, a, b, x in [
        (ramp,0,0,-stroke/2), (dwell,0,0,-stroke/2),
        (ramp,.7,0,-stroke/2), (guard,.7,0,-stroke/2),
        (feed,.7,0,stroke/2), (guard,.7,0,stroke/2),
        (ramp,0,0,stroke/2), (dwell,0,0,stroke/2),
        (ramp,0,.7,stroke/2), (guard,0,.7,stroke/2),
        (feed,0,.7,-stroke/2), (guard,0,.7,-stroke/2)]:
        if duration:
            knots.append((knots[-1][0]+duration,a,b,x))
    return knots


def value(knots, t, col):
    t %= knots[-1][0]
    for left,right in zip(knots,knots[1:]):
        if t <= right[0]:
            q=(t-left[0])/(right[0]-left[0])
            return left[col]+q*(right[col]-left[col])
    raise AssertionError(t)


def inspect(knots, mu, bias, errors, shifts, load=1.):
    # Aggregate normal force of opposed pads per clamp. Free compression .4 mm;
    # k=40 N/mm at 1-N load scenario. No material or dimensional prior asserted.
    k=40*load
    compression=[.4*bias+e for e in errors]
    period=knots[-1][0]
    events={0.,period}
    for col,shift in [(1,shifts[0]),(2,shifts[1]),(3,0.)]:
        for row in knots:
            events.add((row[0]+shift)%period)
        if col<3:
            threshold=compression[col-1]
            for a,b in zip(knots,knots[1:]):
                if min(a[col],b[col])<threshold<max(a[col],b[col]):
                    t=a[0]+(b[0]-a[0])*(threshold-a[col])/(b[col]-a[col])
                    events.add((t+shift)%period)
    events=sorted(events)
    def capacities(t):
        return [mu*k*max(0.,compression[j]-value(knots,t-shifts[j],j+1))
                for j in range(2)]
    minimum=min(sum(capacities(t)) for t in events)
    wrong_distance=0.
    for a,b in zip(events,events[1:]):
        mid=(a+b)/2
        dx=value(knots,b,3)-value(knots,a,3)
        ca,cb=capacities(mid)
        if (dx>1e-12 and ca>1e-12) or (dx< -1e-12 and cb>1e-12):
            wrong_distance+=abs(dx)
    return minimum,wrong_distance


def min_heads(service):
    return next((h for h in range(1,6401) if 6+math.ceil(6400/h)*service<30-1e-10),None)


def main():
    # Exact event intersections bound continuous piecewise-linear contact capacity.
    rows=[]
    for e,eps,guard,mu in [(0,0,0,.1),(.05,.001,0,.1),(.05,.001,.001,.1),
                           (.10,.001,.001,.1),(.05,.001,.001,.02)]:
        knots=schedule(dwell=2*eps,guard=guard)
        cases=[]
        for bias,ea,eb,sa,sb in itertools.product((.8,1.2),(-e,e),(-e,e),(-eps,eps),(-eps,eps)):
            cases.append(inspect(knots,mu,bias,(ea,eb),(sa,sb)))
        rows.append(dict(edge_mm=e,phase_s=eps,guard_s=guard,mu=mu,cases=len(cases),
                         min_capacity_N=min(x[0] for x in cases),
                         max_wrong_grip_motion_mm=max(x[1] for x in cases)))
    # Explicit no-guard counterexample uses faster ramp; not an interpolated conclusion.
    bad=schedule(ramp=.001,dwell=.002,guard=0)
    bad_case=inspect(bad,.1,1.2,(.05,.05),(.001,-.001))
    # Independent regular sampling holdout against exact-event minima.
    knots=schedule()
    exact=inspect(knots,.1,.8,(-.05,-.05),(.001,-.001))[0]
    sampled=[]
    for n in (1000,4000,16000):
        ans=min(sum(.1*40*max(0.,.27-value(knots,i*knots[-1][0]/n-shift,j+1))
                    for j,shift in enumerate((.001,-.001))) for i in range(n+1))
        sampled.append(ans)
        assert abs(ans-exact)<1e-10
    assert abs(exact-1.08)<1e-10
    assert rows[2]['max_wrong_grip_motion_mm']<1e-9
    assert rows[3]['min_capacity_N']<1
    assert rows[4]['min_capacity_N']<1
    assert bad_case[1]>0
    # Logical signed steps; no perfect sensing or physical reach asserted here.
    for old,new,stroke in itertools.product(range(0,41,10),range(0,41,10),(.5,1,2,4,8)):
        pos=float(old)
        for _ in range(math.ceil(abs(new-old)/stroke)):
            pos+=math.copysign(min(stroke,abs(new-pos)),new-pos)
        assert abs(pos-new)<1e-12
    # Local phase is explicitly distinct from correlated shift of both jaw commands.
    coherent=[]
    for delay in (-.001,0,.001):
        coherent.append(inspect(knots,.1,.8,(-.05,-.05),(delay,delay)))
    timing=[]
    for s in (.1,.25,.5,1,2,4,8):
        tstep=4*.003+8*.001+2*move(s)
        n=math.ceil(40/s)
        service=.1+n*tstep
        h=min_heads(service)
        timing.append(dict(stroke_mm=s,cycles=n,cycle_s=tstep,service_s=service,
                           full_s_H160=6+40*service,min_H=h,
                           dollars_per_head_free_cells=250/h if h else None,
                           handovers_per_board=2*n*6400))
    # Quasistatic grip ratio bounds upward acceleration (and downward braking).
    # Scenario output mass W/g; guide drag and compliance omitted favorably.
    a_grip=(1.08-1)*9.81*1000
    grip_timing=[]
    for s in (.5,1,2,4,8):
        service=.1+math.ceil(40/s)*(.020+move(s,a=a_grip)+move(s))
        grip_timing.append(dict(stroke_mm=s,accel_mm_s2=a_grip,service_s=service,
                                min_H=min_heads(service),T_H160_s=6+40*service))
    sensitivity=[]
    for tc,eps,v in itertools.product((.001,.003,.010),(0,.001,.003),(100,200,500)):
        service=.1+20*(4*tc+8*eps+move(2,v=v,a=a_grip)+move(2,v=v))
        sensitivity.append(min_heads(service))
    # Finite jaw prisms: x radial, z vertical; y=[-.6,.6]. Rod x/y=+/-.75,
    # z=[h-50,h+3], h in [0,40]. A centered z=0, B z=-5+xstage.
    # The prescribed compliant spring takes indentation, not the rigid pad body.
    geometry=[]
    for stroke in (1,2,4,8):
        knots=schedule(stroke=stroke)
        collision=0.; neighbor_gap=math.inf; tail_margin=math.inf
        for i in range(1201):
            t=i*knots[-1][0]/1200
            qa,qb,x=(value(knots,t,c) for c in (1,2,3))
            ga,gb=(max(0,q-.27) for q in (qa,qb))
            # Positive-side pads [r+gap,r+gap+1] by [center-.6,center+.6].
            radial=max(0,min(1.75+ga,1.75+gb)-max(.75+ga,.75+gb))
            axial=max(0,min(.6,-5+x+.6)-max(-.6,-5+x-.6))
            collision=max(collision,radial*axial*1.2)
            neighbor_gap=min(neighbor_gap,5.08-2*(1.75+max(ga,gb)))
            tail_margin=min(tail_margin,(-5+x-.6)-(-10),3-.6)
        # Independent continuous envelope separation (sufficient, exact axial gap).
        axial_gap=5-stroke/2-1.2
        assert neighbor_gap>=.72-1e-10
        if axial_gap>=0: assert collision==0
        geometry.append(dict(stroke_mm=stroke,axial_envelope_gap_mm=axial_gap,
                             sampled_collision_mm3=collision,neighbor_gap_mm=neighbor_gap,
                             rod_end_margin_mm=tail_margin))
    assert geometry[-1]['sampled_collision_mm3']>0
    # Exact single-fault witness: A stays open, B on frictionless unpowered slider.
    # Both masses fall at g until B hits a perfectly inelastic lower end stop.
    # Column retains its velocity; finite B friction then permits further sliding.
    s=1.; W=1.; m=W/9.81; v0=.05; C=1.08
    vimpact=math.sqrt(v0*v0+2*9.81*s/2000)
    impact_time=(vimpact-v0)/9.81
    slip=m*vimpact*vimpact/(2*(C-W))*1000
    assert abs(.5*m*vimpact*vimpact-(C-W)*slip/1000)<1e-15
    cut_witness=dict(stroke_mm=s,cut_to_stop_mm=s/2,impact_s=impact_time,
                     impact_speed_m_s=vimpact,post_stop_column_slip_mm=slip)
    # Kinematic outage bound only: B remains gripped to carrier in [-s/2,+s/2].
    # A unpowered-close transient can reduce excursion, but is NOT assumed here.
    cuts=[]
    for s in (.5,1,2,8):
        for load in (.02,1,10):
            mass=load/9.81+.001 # gravity-matched output + 1-g carrier assumption
            for speed in (0,50,200):
                for kstage in (0,1,10): # N/mm, spring anchored at x=0
                    kinetic=.5*mass*(speed/1000)**2
                    spring=.5*kstage*(s/2)**2/1000
                    # Upper bound on available energy before either stop; not impact prediction.
                    energy=kinetic+(load+.001*9.81)*s/1000+spring
                    cuts.append(dict(stroke_mm=s,W_N=load,v_mm_s=speed,k_N_mm=kstage,
                                     max_geometric_excursion_mm=s,energy_upper_J=energy))
    # Stalled shared stage with both grips: equal tangential stiffness Kt,
    # extra opposing force Kt*delta/2, independent of normal capacity model.
    mismatch=[dict(delta_mm=d,internal_force_N=10*d/2) for d in (.01,.05,.1,.5)]
    # Affine contact model limiting checks and strict timing boundary.
    for load in (.02,1,10):
        cap,_=inspect(knots,.1,.8,(-.05,-.05),(.001,-.001),load)
        assert abs(cap-1.08*load)<1e-9
    assert inspect(knots,0,1,(0,0),(0,0))[0]==0
    assert move(0)==0
    for t in timing:
        if t['min_H']:
            h=t['min_H']; service=t['service_s']
            assert 6+math.ceil(6400/h)*service<30-1e-10
            if h>1: assert 6+math.ceil(6400/(h-1))*service>=30-1e-10
    print(json.dumps(dict(contact=rows,fast_ramp_counterexample=bad_case,
                         sample_holdout=sampled,correlated_jaw_shift=coherent,
                         timing=timing,grip_timing=grip_timing,
                         sensitivity_H_range=[min(sensitivity),max(sensitivity)],
                         direct_control_service_s=.1+2*move(40),
                         direct_control_H=min_heads(.1+2*move(40)),
                         mismatch=mismatch,geometry=geometry,cut_witness=cut_witness,outage=cuts),indent=2))


if __name__=='__main__':
    main()
