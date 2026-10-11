"""E-156: signed square-thread/belt bounds. SI, explicit scenarios, no process priors.
Python standard library only. Prints disposable JSON. No actual CAD or hardware pass.
"""
import itertools
import json
import math


def constants(r, lead, mu, direction):
    k = lead/(2*math.pi)
    s = k/r
    c = r*(mu+direction*s)/(1-direction*mu*s)
    return k, c


def rotor(r, lead, rho=1250):
    # Rotating nut plus drive collar; translating screw avoids long spinning core.
    # Nut material occupies an annulus outside thread major radius, plus a
    # conservative solid annulus for the whole thread-root region (overcounts voids).
    ri, ro, length = r-lead/4, r+.0007, .004
    R, collar_length = ro+.0003, .001
    annulus = lambda a,b,h: rho*math.pi*h*(b**4-a**4)/2
    j = annulus(ri,ro,length)+annulus(ri,R,collar_length)
    mass = rho*math.pi*((ro*ro-ri*ri)*length+(R*R-ri*ri)*collar_length)
    return j, R, mass


def state(r, lead, mu, W, m, J, direction, torque):
    """Signed torque/angle: positive raises. Single loaded flank, checked explicitly."""
    k,c = constants(r,lead,mu,direction)
    A = J+direction*m*k*c
    if A <= 0:
        return None
    alpha = (torque-direction*W*c)/A
    F = W+m*k*alpha
    # F=0 is only allowed for the zero-bias/free diagnostic, never loaded support.
    if F < -1e-12:
        return None
    drag = F*(c-direction*k)
    assert drag >= -1e-12
    # Per rad/s, input - potential - heat equals kinetic power.
    assert abs((torque-W*k-direction*drag)-(J+m*k*k)*alpha) < 1e-10
    return alpha,F,drag


def coast(r,lead,mu,W,m,J,direction,v,torque=0):
    out = state(r,lead,mu,W,m,J,direction,torque)
    if out is None:
        return {'state':'flank_or_inertance_limit'}
    a,F,drag = out
    k=lead/(2*math.pi)
    if direction*a >= -1e-14:
        return {'state':'no_arrest','acceleration_m_s2':k*a}
    t = -direction*v/(k*a)
    q = direction*v/k*t+.5*a*t*t
    heat = drag*abs(q)
    initial = .5*(J+m*k*k)*(v/k)**2
    # The applied torque may exchange energy with a source/belt.
    assert abs(initial+torque*q-W*k*q-heat) < 1e-8
    return {'state':'first_stop','distance_mm':abs(k*q)*1000,'time_s':t,
            'heat_J':heat,'axial_N':F,'source_work_J':torque*q}


def retained(r,lead,mu,W,m,J,R,direction,v,Mbelt,H,capacity):
    """Exact symmetric sticking mode after motor torque cut; H identical cells.
    All contact forces stay constant to first stop. No passive source brake.
    """
    k,c=constants(r,lead,mu,direction)
    extra=Mbelt*R*R/H
    out=coast(r,lead,mu,W,m,J+extra,direction,v)
    A=J+direction*m*k*c
    alpha=-direction*W*c/(A+extra)
    f=-Mbelt*R*alpha/H
    assert abs(R*f-direction*W*c-A*alpha)<1e-12
    assert abs(-H*f-Mbelt*R*alpha)<1e-12
    assert abs(f)<=capacity, 'stick assumption exceeds friction cone'
    out.update(contact_force_N=f,added_inertia_kg_m2=extra,belt_slip_heat_J=0)
    return out


def slip_interval(r,lead,mu,W,m,J,R,direction,v,belt_v,Mbelt,H,capacity):
    """Exact first sliding interval: both belt directions, motor already cut.
    End at first zero rotor speed or zero slip; not continued across topology change.
    """
    k=lead/(2*math.pi)
    omega=direction*v/k
    slip=belt_v-R*omega
    assert abs(slip)>1e-8
    f=math.copysign(capacity,slip)
    out=state(r,lead,mu,W,m,J,direction,R*f)
    if out is None:
        return {'state':'flank_or_inertance_limit'}
    alpha,F,drag=out
    bacc=-H*f/Mbelt
    slipacc=bacc-R*alpha
    ts=-slip/slipacc if slip*slipacc<0 else math.inf
    tr=-omega/alpha if omega*alpha<0 else math.inf
    t=min(ts,tr,.1)
    q=omega*t+.5*alpha*t*t
    b=belt_v*t+.5*bacc*t*t
    qbelt=H*f*(b-R*q)
    qthread=H*drag*abs(q)
    e0=H*.5*(J+m*k*k)*omega*omega+.5*Mbelt*belt_v*belt_v
    e1=H*(.5*(J+m*k*k)*(omega+alpha*t)**2+W*k*q)+.5*Mbelt*(belt_v+bacc*t)**2
    residual=e1+qbelt+qthread-e0
    assert qbelt>=-1e-12 and abs(residual)<1e-8
    return {'state': 'slip_zero' if ts==t else 'rotor_zero' if tr==t else 'horizon',
            'time_s':t,'travel_mm':k*q*1000,'belt_heat_J':qbelt,
            'thread_heat_J':qthread,'energy_residual_J':residual,'axial_N':F}


def elastic(r,lead,mu,W,m,J,direction,v,stiffness,n):
    """Exact two-rotor solution after belt separation, valid until first stop/flank loss.
    Split J equally between rim and nut, spring initially carries steady load torque.
    Analytic extrema bracket first zero; n bisections refine it. No damping grant.
    Infinite-thread diagnostic; finite overlap must be checked separately.
    """
    k,c=constants(r,lead,mu,direction)
    Jn,Jd=J/2,J/2
    A=Jn+direction*m*k*c
    if A<=0:
        return {'state':'inertance_limit'}
    tau=direction*W*c
    delta0=tau/stiffness
    deq=tau*Jd/(stiffness*(A+Jd))
    amp=delta0-deq
    om=math.sqrt(stiffness*(1/A+1/Jd))
    a0=-tau/(A+Jd)
    ac=stiffness*amp/A
    rigid_t=v/k/abs(a0)
    horizon=2*rigid_t
    e0=.5*(J+m*k*k)*(v/k)**2+.5*stiffness*delta0**2
    def values(t):
        delta=deq+amp*math.cos(om*t)
        deltad=-amp*om*math.sin(om*t)
        theta=direction*v/k*t+.5*a0*t*t+ac/om**2*(1-math.cos(om*t))
        omega=direction*v/k+a0*t+ac/om*math.sin(om*t)
        alpha=a0+ac*math.cos(om*t)
        F=W+m*k*alpha
        heat=(direction*c-k)*(W*theta+.5*m*k*(omega*omega-(v/k)**2))
        E=.5*(Jn+m*k*k)*omega**2+.5*Jd*(omega+deltad)**2+.5*stiffness*delta**2+W*k*theta
        # Independent rotor equations and total signed energy.
        assert abs(A*alpha-(stiffness*delta-tau))<1e-10
        assert abs(Jd*(alpha-amp*om*om*math.cos(om*t))+stiffness*delta)<1e-10
        assert abs(E+heat-e0)<1e-9
        return theta,omega,alpha,F,delta,deltad,E+heat-e0
    # All velocity extrema partition the exact solution into monotonic intervals.
    # Unlike a time grid this cannot skip a short velocity reversal.
    points=[0.,horizon]
    ratio=-a0/ac
    if abs(ratio)<=1:
        phase=math.acos(ratio)
        for cycle in range(math.ceil(horizon*om/(2*math.pi))+1):
            points.extend(t for t in ((2*math.pi*cycle+phase)/om,
                                      (2*math.pi*(cycle+1)-phase)/om) if 0<t<horizon)
    points=sorted(set(points))
    stop=None
    for left,right in zip(points,points[1:]):
        if direction*values(right)[1]<=0:
            for _ in range(n):
                mid=(left+right)/2
                if direction*values(mid)[1]>0: left=mid
                else: right=mid
            stop=(left,right)
            break
    assert stop is not None
    # Earliest normal-reaction zero, if present, is in the first oscillation.
    if m>0 and abs(ac)>0:
        normal_ratio=(-W/(m*k)-a0)/ac
        if abs(normal_ratio)<=1:
            tf=math.acos(normal_ratio)/om
            if tf<stop[1]:
                return {'state':'flank_loss','time_s':tf}
    t=stop[1]
    theta,omega,alpha,F,delta,deltad,residual=values(t)
    return {'state':'first_zero_not_settled','event_bracket_s':stop,
            'travel_mm':theta*k*1000,'spring_energy_at_cut_J':.5*stiffness*delta0**2,
            'initial_twist_rad':delta0,'remaining_rim_speed_rad_s':omega+deltad,
            'spring_torque_at_event_Nm':stiffness*delta,
            'energy_residual_J':residual}


def schedule(v, overhead=.10, mixed=True):
    service=(2 if mixed else 1)*.04/v+overhead
    H=next((h for h in range(1,6401) if 6+math.ceil(6400/h)*service<30),None)
    return {'channels':H,'service_s':service,
            'map_s':None if H is None else 6+math.ceil(6400/H)*service,
            'channel_ceiling_free_sites_USD':None if H is None else 250/H,
            'motor_selector_comparator_USD':None if H is None else 250+2.30*max(H,100)}


def main():
    r,lead=.0015,.00015
    J,R,rmass=rotor(r,lead)
    k=lead/(2*math.pi)
    separated={}
    for W,m in ((.02,.002),(1,.05),(10,1.)):
        for mu,d in itertools.product((.01,.02,.05,.3),(-1,1)):
            separated[f'W{W}_mu{mu}_d{d}']=coast(r,lead,mu,W,m,J,d,.1)
    # Zero generalized bias isn't zero payload: diagnostic with no translated mass.
    assert coast(r,lead,.05,0,0,J,-1,.1)['state']=='no_arrest'
    retained_cases={}
    for M,H,d in itertools.product((.02,.2,2.),(1,80,320),(-1,1)):
        retained_cases[f'M{M}_H{H}_d{d}']=retained(r,lead,.02,.02,.002,J,R,d,.1,M,H,2)
    slip={}
    for d,belt_sign in itertools.product((-1,1),(-1,1)):
        slip[f'd{d}_belt{belt_sign}']=slip_interval(r,lead,.02,1,.05,J,R,d,.02,
                                                   belt_sign*R*.04/k,.02,1,.1)
    elastic_cases={}
    for stiff,d in itertools.product((1e-5,1e-4,1e-3),(-1,1)):
        elastic_cases[f'K{stiff}_d{d}']=[elastic(r,lead,.02,.02,.002,J,d,.02,stiff,n)
                                      for n in (16,32,48)]
    # Bounded coherent print/lot corners, not independent-cell random samples.
    uncertainty=[]
    for rr,ll,rho,extra,mu in itertools.product((.00145,.0015,.00155),
            (.0001,.00015,.0002),(1000,1300),(0,1),(.01,.02,.05,.3)):
        jj,_,_=rotor(rr,ll,rho)
        uncertainty.append(coast(rr,ll,mu,.02,.002,jj*(1+extra),-1,.1))
    uncertainty_summary={label:sum(row['state']==label for row in uncertainty)
                         for label in ('first_stop','no_arrest','flank_or_inertance_limit')}
    stops=[row['distance_mm'] for row in uncertainty if row['state']=='first_stop']
    uncertainty_summary.update(cases=len(uncertainty),coast_range_mm=[min(stops),max(stops)],
                               above_40mm=sum(s>40 for s in stops))
    # Minimum coast-contained travel time with unbounded powered acceleration.
    lower_a=.1/separated['W0.02_mu0.02_d-1']['time_s']
    raise_a=.1/separated['W0.02_mu0.02_d1']['time_s']
    lower_t=math.sqrt(2*.04/lower_a)
    raise_t=math.sqrt(2*.04/raise_a)
    service=lower_t+raise_t+.1
    safe_H=next(h for h in range(1,6401) if 6+math.ceil(6400/h)*service<30)
    contained=dict(lower_time_s=lower_t,raise_time_s=raise_t,mixed_service_s=service,
                   channels=safe_H,channel_ceiling_USD=250/safe_H,
                   full_stroke_speed_limit_mm_s=1000*math.sqrt(2*lower_a*.04))
    # All geometries are envelopes; teeth, bearings, guides and lever CAD are unbuilt.
    geometry=[]
    for r0,l0 in ((.0015,.00015),(.003,.0003),(.006,.0005),(.0015,.0005)):
        jj,rr,mm=rotor(r0,l0)
        slope=l0/(2*math.pi*r0)
        upc=constants(r0,l0,.3,1)[1]
        geometry.append(dict(mean_diameter_mm=2*r0*1000,lead_mm=l0*1000,rotor_diameter_mm=2*rr*1000,
            J_kg_m2=jj,rotor_mass_g=1000*mm,lead_slope=slope,tooth_width_mm=l0*500,
            turns_per_40mm=.04/l0,rpm_at_100mm_s=60*.1/l0,
            belt_speed_at_100mm_s=rr*.1/(l0/(2*math.pi)),
            down_coast_mm=coast(r0,l0,.02,.02,.002,jj,-1,.1),
            normal_for_10N_mu03_belt_mu015_N=10*upc/(.15*rr),
            raise_thread_heat_6400_J=(10*upc/(l0/(2*math.pi))-10)*.04*6400))
    # Idler translates y; belt support half-span a, tension T. Explicit return spring.
    selector=[]
    for gap,stroke in itertools.product((.0001,.00025,.0004),(.0004,.0005,.0006)):
        N=40000*max(0,stroke-gap)
        ret=5000*stroke
        belt_restore=4*stroke/math.sqrt(.00508**2+stroke**2)
        selector.append(dict(gap_mm=gap*1000,stroke_mm=stroke*1000,N=N,
                             command_force_N=N+ret+belt_restore))
    # Ideal spring-only first contact opening from .5 to .25 mm, released at rest.
    # Actual contact/belt forces assist return; motor drag, damping and delay unknown.
    return_time=math.acos(.00025/.0005)*math.sqrt(.001/5000)
    thermal=[]
    for W,mu in itertools.product((.02,1,10),(.02,.05,.3)):
        _,c=constants(r,lead,mu,1)
        torque=W*c
        mechanical=torque/k*.04
        heat=(torque/k-W)*.04
        thermal.append(dict(W=W,mu=mu,thread_heat_per_map_J=6400*heat,
                            extra_belt_heat_10percent_slip_J=6400*mechanical*.1/.9,
                            raising_power_320_at_v01_W=320*torque*.1/k))
    # Exhaust all old/new 2-cell maps: individual timed contact in each signed pass.
    count=0
    for old0,old1,new0,new1 in itertools.product(range(5),repeat=4):
        out=[old0,old1]
        for d in (-1,1):
            for i,target in enumerate((new0,new1)):
                if (target-out[i])*d>0:
                    out[i]=target  # ideal measured stop; physics is tested separately
        assert out==[new0,new1]
        count+=1
    # Sign, frictionless and threshold checks, independent of the previous source.
    for d in (-1,1):
        a,_,_=state(r,lead,0,1,.05,J,d,0)
        assert abs(a*k+1/(.05+J/k**2))<1e-12
    assert abs(constants(r,lead,k/r,-1)[1])<1e-18
    # Finite engagement: translating screw [h-50,h+4] mm, fixed nut [-5,-1].
    assert all(h-50<=-5 and h+4>=-1 for h in (0,40))
    # Near-zero load coast threshold, and source delivery during delayed release.
    release=[]
    for delay in (.001,.003,.010):
        c0=coast(r,lead,.02,.02,.002,J,-1,.1)
        release.append(dict(delay_s=delay,constant_speed_plus_coast_mm=1000*.1*delay+c0['distance_mm']))
    print(json.dumps(dict(rotor=dict(J=J,R=R,mass_g=rmass*1000),geometry=geometry,
        separated=separated,retained=retained_cases,slip_intervals=slip,elastic=elastic_cases,
        selector=selector,ideal_return_time_s=return_time,
        unselected_clearance_mm={str(e):.25-3*e for e in (.025,.05,.1)},thermal=thermal,
        schedules={str(v):schedule(v) for v in (.025,.05,.1,.2,.3)},release_delays=release,
        uncertainty=uncertainty_summary,contained_schedule=contained,
        zero_bias='No contact, no bias, no bearing drag: finite J coasts indefinitely.',
        maps_replayed=count),indent=2))

if __name__=='__main__':
    main()
