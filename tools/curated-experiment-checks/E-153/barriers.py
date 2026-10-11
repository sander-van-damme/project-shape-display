#!/usr/bin/env python3
"""E-153 necessary-condition screens; stdlib, deterministic, JSON to stdout.
Cam: favorable holonomic height path, NOT constructed roller/contact geometry.
Capillary: generous pressure bound + separate fully wetted flow relaxation.
All unspecified numerical inputs are bounded scenarios, not process priors.
"""
import itertools
import json
import math

TAU = 2 * math.pi


def cam(lead=4., amplitude=.3, waves=4):
    k = lead / TAU
    def h(q):
        return k*q + amplitude*math.sin(waves*q)
    def dh(q):
        return k + waves*amplitude*math.cos(waves*q)
    def ddh(q):
        return -waves**2*amplitude*math.sin(waves*q)
    if amplitude*waves <= k:
        return h, dh, ddh, None
    peak = math.acos(-k/(amplitude*waves))/waves
    valley = (TAU-math.acos(-k/(amplitude*waves)))/waves
    period = TAU/waves
    barrier = h(peak)-h(valley)
    assert abs(dh(peak)) < 1e-12 and abs(dh(valley)) < 1e-12
    assert ddh(peak) < 0 < ddh(valley)
    assert barrier > 0
    return h, dh, ddh, dict(peak_rad=peak, valley_rad=valley,
                           period_rad=period, step_mm=lead/waves,
                           downhill_barrier_mm=barrier,
                           uphill_barrier_mm=barrier+lead/waves)


def free_cut(lead, amplitude, load, spin=-1., inertia=1e-5, mass_kg=.02):
    # N, mm, seconds: J is N mm s²; translational mass is kg/1000.
    h, dh, _, wells = cam(lead, amplitude)
    assert wells is not None
    peak = wells['peak_rad'] + 39*wells['period_rad']
    q0 = peak-.01  # down-going side of a high barrier, above 39 lower ones
    jeff = inertia + mass_kg/1000*dh(q0)**2
    energy = load*h(q0) + .5*jeff*spin**2
    # Downhill maxima strictly decrease. Positive margin at the first means
    # no turning point anywhere in subsequent ideal periods: all are traversable.
    margins = [energy-load*h(peak-j*wells['period_rad']) for j in range(1,40)]
    assert all(x > 0 for x in margins)
    assert all(b >= a-1e-12 for a,b in zip(margins,margins[1:]))
    return dict(first_lower_peak_energy_margin_Nmm=margins[0],
                last_peak_energy_margin_Nmm=margins[-1],
                traversable_lower_peaks=len(margins),
                initial_height_mm=h(q0), kinetic_Nmm=.5*jeff*spin**2)


def cam_screen():
    h, dh, ddh, wells = cam()
    p, v, period = wells['peak_rad'], wells['valley_rad'], wells['period_rad']
    levels = [h(v+i*period)-h(v) for i in range(41)]
    assert all(abs(z-i) < 1e-12 for i,z in enumerate(levels))
    # Exact periodic identity and signed work, checked across both directions.
    convergence=[]
    for n in (64,256,1024):
        q=[v+i*40*period/n for i in range(n+1)]
        for a in q:
            assert abs((h(a+period)-h(a))-1) < 1e-12
        dq=40*period/n
        work=dq*(sum(dh(x) for x in q)-.5*(dh(q[0])+dh(q[-1])))
        reverse=list(reversed(q))
        reverse_work=sum(.5*(dh(a)+dh(b))*(b-a)
                         for a,b in zip(reverse,reverse[1:]))
        assert abs(work-40) < 1e-10
        assert abs(reverse_work+40) < 1e-10
        step=1/n
        err=max(abs((h(x+step)-h(x-step))/(2*step)-dh(x)) for x in q)
        convergence.append(dict(intervals=n,derivative_error_mm_per_rad=err,
                                signed_work_error_Nmm_at_1N=abs(work-40)))
    # Non-integer interval avoids relying only on periodic quadrature cancellation.
    a,b=.123,3.456
    quad=[]
    for n in (64,256,1024):
        step=(b-a)/n
        vals=[dh(a+i*step) for i in range(n+1)]
        integral=step*(sum(vals)-.5*(vals[0]+vals[-1]))
        quad.append(abs(integral-(h(b)-h(a))))
    assert quad[2] < quad[1] < quad[0]
    corners=[]
    for lead,amp,load in itertools.product((3.9,4.1),(.25,.35),(.02,1.,10.)):
        _,_,_,w=cam(lead,amp)
        cut=free_cut(lead,amp,load)
        corners.append(dict(lead_mm=lead,amplitude_mm=amp,load_N=load,
                            barrier_Nmm=load*w['downhill_barrier_mm'],
                            travel_40_steps_mm=40*w['step_mm'], **cut))
    # Zero load has no potential wells despite a corrugated geometric path.
    zero=free_cut(4.,.3,0.)
    _,_,_,monotone=cam(amplitude=.1)
    assert monotone is None
    cut_at_rest=free_cut(4.,.3,10.,spin=0.)
    return dict(nominal=wells, retained_levels_mm=levels,
                peak_torque_Nmm_at_10N=10*(4/TAU+4*.3),
                nominal_barrier_Nmm={str(f): f*wells['downhill_barrier_mm']
                                     for f in (0.,.02,1.,10.)},
                cuts={str(f):free_cut(4.,.3,f) for f in (0.,.02,1.,10.)},
                zero_load=zero, released_at_rest_on_downhill=cut_at_rest,
                corners=corners, derivative_checks=convergence,
                nonperiodic_work_errors_Nmm_at_1N=quad,
                minimum_work_removal_per_down_step_Nmm_at_10N=10.,
                minimum_mean_dissipative_torque_Nmm_at_10N=10*4/TAU,
                low_friction_screw_turns_40mm=40/(math.pi*3*.05),
                cam_turns_40mm=10.)


def capillary_screen():
    # Sum of two menisci, each at maximum |curvature sum|=2/r.
    # Favorable |cos(theta)|=1; no oxide skin or frozen solid included.
    area=16e-6  # m²; piston 4x4 mm, packaging not qualified
    rows=[]
    for tension,radius in itertools.product((.03,.075,.5),(50e-6,100e-6,150e-6)):
        pressure=4*tension/radius
        # Independent circumference/area balance at each meniscus.
        one=2*math.pi*radius*tension/(math.pi*radius**2)
        assert abs(pressure-2*one) < 1e-9
        rows.append(dict(tension_N_per_m=tension,pore_radius_um=radius*1e6,
                         max_pressure_Pa=pressure,max_force_N=pressure*area))
    small=[]
    for force in (1.,10.):
        r=4*.075*area/force
        for length in (1e-5,1e-4):
            # Optimistic straight, fully liquid pores; viscous pressure is
            # EXTRA to burst/load pressure. This does not retain menisci.
            phi=.5; mu=.001; dp=100000.
            count=phi*area/(math.pi*r*r)
            single=math.pi*r**4*dp/(8*mu*length)
            flow=phi*area*r*r*dp/(8*mu*length)
            assert math.isclose(flow,count*single,rel_tol=1e-12)
            volume=area*.04
            small.append(dict(force_N=force,max_radius_um=r*1e6,
                pore_length_um=length*1e6,ideal_pores_per_site=count,
                flow_mm3_per_s=flow*1e9,transfer_40mm_s=volume/flow,
                aspect_ratio=length/(2*r),
                long_pore_approximation_eligible=length/(2*r)>=10))
    # Coherent worst holding corner: larger pore, lower tension, smaller piston.
    corners=[]
    for side,r,gamma in itertools.product((3.8,4.2),(50.,150.),(.03,.075)):
        corners.append(4*gamma/(r*1e-6)*(side*1e-3)**2)
    return dict(pressure_rows=rows,microinsert_relaxation=small,
                coherent_force_bounds_N=[min(corners),max(corners)],
                one_cell_40mm_volume_mm3=640.,board_volume_litres=4.096,
                single_100um_pore_required_1N_piston_area_mm2=1/(4*.075/100e-6)*1e6)


def min_heads(service):
    return next(h for h in range(1,6401) if 6+math.ceil(6400/h)*service < 30)


def board_screen():
    rows=[]
    for rpm in (600,1200,2400):
        service=10/(rpm/60)+.1
        heads=min_heads(service)
        rows.append(dict(rpm=rpm,service_s=service,heads=heads,
                    time_s=6+math.ceil(6400/heads)*service,
                    head_allowance_USD=250/heads))
    assert min_heads(.6)==165  # strict boundary: 40*.6+6 =30, disallowed
    return dict(cam=rows,site_allowance_USD=250/6400,
                handling_hours={str(t):6400*t/3600 for t in (10,30)},
                load_work_J={str(f):6400*f*.04 for f in (1,10)},
                frame_force_N={str(f):6400*f for f in (1,10)})


if __name__ == '__main__':
    print(json.dumps(dict(cam=cam_screen(),capillary=capillary_screen(),
                         board=board_screen()),indent=2))
