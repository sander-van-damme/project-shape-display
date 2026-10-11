#!/usr/bin/env python3
"""E-155. mm geometry; SI dynamics. Deterministic bounds, not process priors.
Finite contact sections + physical bus constraints + arbitrary-map schedules.
Run with Python 3 and numpy. Output is reproducible and not an artifact to retain.
"""
import itertools
import json
import math
import numpy as np

TAU = 2 * math.pi
P = TAU / 4
K = 4 / TAU
A = .3
PEAK = math.acos(-K / (4*A)) / 4
VALLEY = P-PEAK


def law(q, lead=4., amp=.3):
    q = np.asarray(q)
    return lead/TAU*q+amp*np.sin(4*q), lead/TAU+4*amp*np.cos(4*q), -16*amp*np.sin(4*q)


def flat_shoe(q, radius, width):
    """Exact max of rail h over finite horizontal shoe, with x=radius*q.
    Straight strip section, not a wrapped barrel CAD claim.
    """
    lo, hi = q-width/(2*radius), q+width/(2*radius)
    values = [float(law(lo)[0]), float(law(hi)[0])]
    for n in range(math.floor((lo-PEAK)/P)-1, math.ceil((hi-PEAK)/P)+2):
        t = PEAK+n*P
        if lo <= t <= hi:
            values.append(float(law(t)[0]))
    return max(values)


def flat_checks():
    rows = []
    for radius,width in itertools.product((1.5,3.,6.),(1.,2.,3.,4.)):
        q = np.linspace(0,2*P,4097)
        h = np.array([flat_shoe(x,radius,width) for x in q])
        # Maximum cumulative downhill fall: zero means no restoring minimum
        # on this continuous max-envelope; sampled barrier heights are estimates.
        falls = np.maximum.accumulate(h)-h
        barrier = float(falls.max())
        rows.append(dict(radius_mm=radius,shoe_width_mm=width,
                         downhill_well_mm=barrier,
                         downhill_barrier_exists=barrier>1e-6))
    # Any window >= one complete period has a monotonic maximum envelope:
    # dropped left segment is dominated by the same point one period to right.
    for radius in (1.5,3.,6.):
        q = np.linspace(0,2*P,2049)
        h = np.array([flat_shoe(x,radius,radius*P) for x in q])
        assert np.min(np.diff(h)) >= -1e-12
    lo,hi=VALLEY-PEAK, P
    for _ in range(80):
        mid=(lo+hi)/2
        if law(PEAK+mid)[0] < law(PEAK)[0]: lo=mid
        else: hi=mid
    assert abs(float(law(PEAK+hi)[0]-law(PEAK)[0]))<1e-12
    # Flat maximum cannot fall once its trailing maximum is replaced by an
    # at-least-as-high leading point. This is an exact threshold for this law.
    return dict(cases=rows,critical_angular_width_rad=hi,
                critical_width_at_R1_5_mm=1.5*hi)


def loaded_law(q, radius=6., gap=.1, lead=4., amp=.3):
    """Analytic lower-contact offset, before polyline approximation.
    Roller center = pitch - gap*normal; invert its x to the imposed x=R*q.
    """
    t=np.array(q,dtype=float,copy=True)
    for _ in range(10):
        h,hp,hpp=law(t,lead,amp)
        slope=hp/radius
        dx=radius+gap*hpp/radius/(1+slope*slope)**1.5
        t-=(radius*t+gap*slope/np.sqrt(1+slope*slope)-radius*q)/dx
    h,hp,hpp=law(t,lead,amp)
    slope=hp/radius
    z=h-gap/np.sqrt(1+slope*slope)
    return z,hp,hpp/(1+gap*hpp/radius**2/(1+slope*slope)**1.5)


def disk_above(poly,x,r):
    """Exact support against each finite line segment and vertex (mm)."""
    dx=poly[:,0]-x
    valid=np.abs(dx)<r
    values=list(poly[valid,1]+np.sqrt(r*r-dx[valid]**2))
    a,b=poly[:-1],poly[1:]
    slopes=(b[:,1]-a[:,1])/(b[:,0]-a[:,0])
    tx=x+r*slopes/np.sqrt(1+slopes*slopes)
    active=(tx>=a[:,0]) & (tx<=b[:,0])
    values.extend(a[active,1]+slopes[active]*(x-a[active,0])+r*np.sqrt(1+slopes[active]**2))
    return max(values)


def roller_section(radius=6., roller=1.5, gap=.1, n=256, error=0.):
    # Lower/upper normal offsets. Extruding this section across a 3.2-mm
    # supported axle span gives a finite planar rail, not a helical surface.
    q=np.linspace(-2*P,3*P,5*n+1)
    h,hp,hpp=law(q)
    slope=hp/radius
    curve=np.stack((radius*q,h),axis=1)
    normal=np.stack((-slope,np.ones_like(slope)),axis=1)/np.sqrt(1+slope*slope)[:,None]
    lo=curve-(roller+gap)*normal
    hi=curve+(roller+gap)*normal
    # Adverse common offset closure and oversized roller.
    lo[:,1]+=error
    hi[:,1]-=error
    r_actual=roller+error
    if min(np.diff(lo[:,0]).min(),np.diff(hi[:,0]).min())<=0:
        return dict(radius_mm=radius,folded_offset=True)
    phases=np.linspace(0,P,n+1)
    lower=np.array([disk_above(lo,radius*x,r_actual) for x in phases])
    upper=np.array([-disk_above(hi*np.array([1,-1]),radius*x,r_actual) for x in phases])
    rho=(1+slope*slope)**1.5/np.maximum(abs(hpp/radius**2),1e-20)
    return dict(radius_mm=radius,folded_offset=False,n=n,error_mm=error,
                min_curvature_radius_mm=float(rho.min()),
                min_center_clearance_mm=float((upper-lower).min()),
                nominal_path_error_mm=float(np.max(abs(lower-law(phases)[0]))),
                analytic_offset_error_mm=float(np.max(abs(lower-loaded_law(phases,radius,gap)[0]))) if error==0 else None,
                end_rise_mm=float(lower[-1]-lower[0]))


def supported_axle():
    # Simply supported round axle, center point load; no fictitious double-shear
    # exemption from bending. 3.2-mm span, 2-mm diameter, 1-mm cheek thickness.
    rows=[]
    for load,diameter in itertools.product((10.,20.,320.),(1.8,2.,2.2)):
        rows.append(dict(load_N=load,diameter_mm=diameter,
            bending_MPa=8*load*3.2/(math.pi*diameter**3),
            double_shear_MPa=2*load/(math.pi*diameter**2),
            cheek_bearing_MPa=load/(2*diameter*1.)))
    return rows


def motion_grid(n):
    # Quintic rest-to-rest bus increment between adjacent wells; every output
    # uses h(q), so output acceleration includes BOTH terms of chain rule.
    s=np.linspace(0,1,n+1)
    S=10*s**3-15*s**4+6*s**5
    Sp=30*s**2-60*s**3+30*s**4
    Spp=60*s-180*s**2+120*s**3
    results=[]
    for direction,lead,amp in itertools.product((-1,1),(3.9,4.,4.1),(.25,.3,.35)):
        peak=math.acos(-(lead/TAU)/(4*amp))/4
        valley=P-peak
        q=valley+direction*P*S
        _,hp,hpp=loaded_law(q,lead=lead,amp=amp)
        acc=(hpp*(P*Sp)**2+hp*direction*P*Spp)*.001 # m per normalized t^2
        # N=F+M*a >= .5F for gravitational M=F/g, explicit margin scenario.
        tmin=math.sqrt(max(0.,-float(acc.min()))/(.5*9.81))
        results.append(dict(direction=direction,lead_mm=lead,amp_mm=amp,
            step_s=tmin,max_accel_at_step_m_s2=float(acc.max())/tmin**2,
            max_normal_N_at_10N=float(np.max((10+10/9.81*acc/tmin**2)*np.sqrt(1+(hp/6.)**2))),
            peak_rpm=float((P*Sp).max())/tmin*60/TAU))
    return results


def required_heads(site_time):
    return next((h for h in range(1,6401) if 6+math.ceil(6400/h)*site_time<30),None)


def schedules(step):
    # Workload contains changes +1..+44 and -1..-44 in every full group.
    # Direct zero-speed dog selection permits an ascending and descending pass.
    # A 44-step bound covers 40 mm at min common lead; targets need calibration.
    rows=[]
    for select in (0.,.002,.01,.02):
        cycle=88*(step+select)+.10
        heads=required_heads(cycle)
        rows.append(dict(protocol='rigid two-direction selected bank',
            selection_s_per_step=select,group_s=cycle,heads=heads,
            time_s=6+math.ceil(6400/heads)*cycle if heads else None,
            remaining_per_head_dollars=250/heads if heads else None))
    cycle=88*(step/math.sqrt(2))+.1
    rows.append(dict(protocol='rigid zero contact margin sensitivity',group_s=cycle,
                     heads=required_heads(cycle)))
    # Best one-direction workload; a bound, not arbitrary-map guarantee.
    cycle=44*step+.1
    rows.append(dict(protocol='rigid one-direction favorable',group_s=cycle,
                     heads=required_heads(cycle)))
    for rpm in (300.,400.):
        cycle=11*60/rpm+.1
        h=required_heads(cycle)
        rows.append(dict(protocol='independent constant-speed ideal cam',rpm=rpm,
             group_s=cycle,heads=h,motor_relay_only_dollars=h*(2.30+2.80390)))
    return rows


def bus_modes():
    # Open differential: common generator sees mean speed. Outputs have
    # an undamped antisymmetric mode, even with an infinitely locked carrier.
    B=np.array([[.5,.5]])
    v=np.array([-1.,1.])
    assert np.linalg.norm(B@v)==0
    q=np.linspace(0,2*P,10001)
    hp=law(q)[1]*.001
    i=int(np.argmax(hp))
    grav_power=-float(np.array([10*hp[i],.02*hp[i]])@v)
    # At q=0, the heavy output initially accelerates downhill from rest
    # in the exact carrier-locked differential coordinate.
    assert grav_power>0
    # Smooth output handoff: ground lock qi=0 plus drive qi-qbus=0
    # forces qbus=0; disengage first instead leaves qi unconstrained.
    both=np.array([[1.,-1.],[1.,0.]])
    assert np.linalg.matrix_rank(both)==2
    assert np.linalg.norm(both@np.array([0.,1.]))>0
    # All old/new pair states 0..4: two signed passes reach targets and
    # unselected outputs never move. Each connected phase stops at every step.
    count=0
    for old0,old1,new0,new1 in itertools.product(range(5),repeat=4):
        state=[old0,old1]; target=[new0,new1]
        for sign in (1,-1):
            for _ in range(4):
                for j in range(2):
                    if sign*(target[j]-state[j])>0:
                        state[j]+=sign
        assert state==target
        count+=1
    # Relative registration error destroys strict common seating: both
    # quadratics minimized at q=-weighted mean(delta), not each local minimum.
    phase_error=.02
    # Equal loads and opposite phase bias: solve aggregate equilibrium, then
    # expose each nonzero torque that was balanced THROUGH the shared bus.
    lo,hi=VALLEY-.05,VALLEY+.05
    for _ in range(80):
        qmid=(lo+hi)/2
        torque=10*(law(qmid-phase_error)[1]+law(qmid+phase_error)[1])
        if torque<0: lo=qmid
        else: hi=qmid
    residual=abs(10*float(law((lo+hi)/2+phase_error)[1]))
    return dict(differential_undamped_dimension=1,
        generator_speed_rad_s=float((B@v)[0]),
        downhill_power_W=grav_power,ground_drive_constraint_rank=2,
        exhaustive_two_cell_maps=count,phase_error_rad=phase_error,
        opposing_local_torque_at_stationary_bus_Nmm=residual)


def cost_and_energy():
    rows=[]
    for h,head,cell,shared in itertools.product((800,1600,2134,3200,6400),(.05,.1,.25), (0.,.02), (150.,250.)):
        rows.append((h,head,cell,shared,h*head+6400*cell+shared))
    # Coherent all-loaded banks; generator drag is load independent at speed.
    omega=2*math.pi*300/60
    heat=[]
    for n in (1,80,800,1600,3200):
        c=n*.001 # E-154 strong-capture scenario, not a sized generator
        heat.append(dict(engaged=n,c_Nms=c,heat_W_at_300rpm=c*omega**2,
            static_peak_torque_Nm=n*10*(K+4*A)*.001))
    return dict(hypothetical_joint_costs=[dict(heads=h,per_head=a,per_cell=b,shared=c,total=t)
        for h,a,b,c,t in rows if h in (1600,3200) and a in (.1,.25)],
        shared_sink_scaling=heat,
        payload_work_J={str(f):6400*f*.04 for f in (.02,1.,10.)},
        square_interleave_tier_counts=[dict(diameter_mm=d,square_grid_tiers=math.ceil(d/5.08)**2)
                                   for d in (8.,14.,18.)])


def main():
    motion=[motion_grid(n) for n in (512,2048,8192)]
    maxima=[max(r['step_s'] for r in group) for group in motion]
    assert abs(maxima[-1]-maxima[-2])<1e-6
    sections=[roller_section(n=n) for n in (64,256,1024)]
    assert abs(sections[-1]['end_rise_mm']-1)<1e-10
    assert sections[-1]['min_center_clearance_mm']>0
    assert roller_section(radius=1.5)['folded_offset']
    assert roller_section(error=.1)['min_center_clearance_mm']<0
    # Independent periodic identity & exact conservative work.
    q=np.linspace(-2,2,333)
    assert np.max(abs(law(q+P)[0]-law(q)[0]-1))<1e-12
    eps=1e-5
    zz,zp,zpp=loaded_law(q)
    assert np.max(abs((loaded_law(q+eps)[0]-loaded_law(q-eps)[0])/(2*eps)-zp))<1e-8
    assert np.max(abs((loaded_law(q+eps)[1]-loaded_law(q-eps)[1])/(2*eps)-zpp))<1e-7
    assert sections[-1]['analytic_offset_error_mm'] < sections[0]['analytic_offset_error_mm']/100
    print(json.dumps(dict(flat_shoes=flat_checks(),roller_convergence=sections,
        roller_error_bounds=[roller_section(error=e) for e in (0.,.025,.05,.1)],
        narrow_roller=roller_section(radius=1.5),axle=supported_axle(),
        motion_step_convergence_s=maxima,motion=motion[-1],
        schedules=schedules(maxima[-1]),bus=bus_modes(),
        accounting=cost_and_energy()),indent=2))


if __name__=='__main__':
    main()
