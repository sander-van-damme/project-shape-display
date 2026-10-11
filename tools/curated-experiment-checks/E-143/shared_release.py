#!/usr/bin/env python3
"""E-143 deterministic necessary-condition screen; SI throughout, no fitted priors.
Run directly; JSON is disposable. Not a contact simulation or hardware qualification.
"""
import json
import math


def deflection(x, a, length, force, ei):
    """Simply supported Euler-Bernoulli beam, positive point-load deflection."""
    if x > a:
        return deflection(length-x, length-a, length, force, ei)
    b = length-a
    return force*b*x*(length*length-b*b-x*x)/(6*length*ei)


def beam(n, depth, young, steps=1024):
    # Internal head pitch, NOT 5.08-mm output pitch. Both beam ends are driven.
    length, width = n*.04, .01
    force = 960/20  # coherent +20% normal-spring bias, ideal lossless lever
    sites = [(i+.5)*.04 for i in range(n)]
    ei = young*width*depth**3/12
    values = [sum(deflection(length*j/steps, a, length, force, ei)
                  for a in sites) for j in range(steps+1)]
    return max(values)


def beam_integral(n, depth, young, steps):
    # Independent integration of curvature, then enforce y(L)=0.
    length = n*.04
    dx = length/steps
    sites = [(i+.5)*.04 for i in range(n)]
    force = 48
    reaction = n*force/2
    ei = young*.01*depth**3/12
    curvatures = [(reaction*x-sum(force*max(x-a, 0) for a in sites))/ei
                  for x in (j*dx for j in range(steps+1))]
    slopes, positions = [0.], [0.]
    for k in range(steps):
        slopes.append(slopes[-1]+dx*(curvatures[k]+curvatures[k+1])/2)
        positions.append(positions[-1]+dx*(slopes[k]+slopes[k+1])/2)
    end = positions[-1]
    return max(end*k/steps-p for k, p in enumerate(positions))


def min_heads(cycle):
    return next(h for h in range(1, 6401) if 6+math.ceil(6400/h)*cycle < 30)


def jam_closures(n, coupling, stuck_member=None, common_stuck=False):
    """Exact kinematic constraint screen, not finite geometry/dynamics.
    q=0 means locally returned; q=1 means still open. In unilateral model
    q_i>=u and local spring minimizes q_i. In tied model q_i=u.
    Common return is GRANTED here to isolate member versus common jam.
    """
    u = int(common_stuck or (coupling == 'tied' and stuck_member is not None))
    return [not (u or i == stuck_member) for i in range(n)]


def main():
    report = {}
    assert min_heads(.45) == 121 and min_heads(.85) == 229
    report['joint_cost'] = []
    for h in (121, 229):
        for motor in (1.56, 3.96):
            report['joint_cost'].append(dict(heads=h, motor_each=motor,
                motor_total=h*motor, remaining_after_250_reserve=250-h*motor,
                remaining_per_head=(250-h*motor)/h,
                remaining_per_cell=(250-h*motor)/6400))
    report['opening'] = []
    # Re-size to same 12.8-N minimum static friction capacity at each mu floor.
    for mu in (.02, .1, .3):
        normal = 12.8/(.8*mu)
        for n in (1, 4, 8, 16):
            low_work, high_work = .8*normal*.0002*n, 1.2*normal*.0004*n
            report['opening'].append(dict(mu_floor=mu, bank=n,
                normal_nominal_N=normal, peak_lever_input_N=1.2*normal*n/20,
                work_J=[low_work, high_work], peak_input_travel_mm=8,
                ideal_412_units_at_5N_constant=math.ceil(high_work/.0275)))
            assert math.isclose((normal*n/20)*(.0004*20), normal*n*.0004)
    report['beam'] = []
    for n in (2, 4, 8):
        for depth in (.01, .02, .04):
            d = beam(n, depth, 1e9)
            report['beam'].append(dict(heads=n, span_mm=n*40, depth_mm=depth*1000,
                worst_deflection_mm=d*1000, pad_gap_loss_mm=d/20*1000,
                small_deflection_valid=d < n*.04/20,
                pad_margin_mm=(.0004-.0001-.0002-d/20)*1000))
    report['beam_checks'] = []
    for steps in (256, 512, 1024):
        exact = beam(4, .02, 2e9, steps)
        numeric = beam_integral(4, .02, 2e9, steps)
        report['beam_checks'].append(dict(steps=steps, exact_mm=exact*1000,
                                       error_mm=abs(exact-numeric)*1000))
    assert abs(beam(4,.02,2e9)-beam_integral(4,.02,2e9,1024)) < 1e-8
    assert math.isclose(beam(4,.02,1e9), 3*beam(4,.02,3e9))
    assert math.isclose(deflection(.5,.5,1,1,1), 1/48)
    assert deflection(0,.5,1,1,1) == deflection(1,.5,1,1,1) == 0
    report['jam'] = {}
    for coupling in ('tied','unilateral'):
        report['jam'][coupling] = {
            'normal_closed': sum(jam_closures(8,coupling)),
            'one_member_jammed_closed_count': sum(jam_closures(8,coupling,3)),
            'common_jammed_closed_count': sum(jam_closures(8,coupling,common_stuck=True))}
    assert report['jam']['tied']['one_member_jammed_closed_count'] == 0
    assert report['jam']['unilateral']['one_member_jammed_closed_count'] == 7
    assert report['jam']['unilateral']['common_jammed_closed_count'] == 0
    report['closure_and_stop_optimism'] = []
    # Instant full normal, no drive energy: independent best-case bound, no transient claim.
    for mass in (.05, 1.1):
        for delay in (0,.002,.01):
            f, drag, speed = 10.,12.8,.1
            v = speed+f/mass*delay
            distance = speed*delay+f*delay**2/(2*mass)+mass*v*v/(2*(drag-f))
            report['closure_and_stop_optimism'].append(dict(mass_kg=mass,
                delay_ms=1000*delay, distance_mm=distance*1000))
    report['downstream'] = []
    for stiffness in (100,1000,10000):
        # Equilibrium extension cancels for zero incremental force; speed is relative.
        amp = .1*math.sqrt(1.1/stiffness)
        report['downstream'].append(dict(K_N_per_m=stiffness,
                                        residual_amplitude_mm=amp*1000))
    report['guide_load_sensitivity'] = [dict(guide_N=g, guaranteed_pad_normal_N=640-g,
        minimum_drag_N=.02*(640-g)) for g in (0,40,80,160)]
    report['common_return_sensitivity'] = [dict(heads=n, guide_and_drive_resistance_N=g,
        net_return_N=n*640/20+8-g) for n in (1,8) for g in (0,50,300)]
    report['pressure_release'] = dict(pressure_Pa=500000,
        summed_piston_area_mm2=960/500000*1e6,
        equivalent_diameter_mm=math.sqrt(4*(960/500000)/math.pi)*1000,
        bank8_displaced_volume_ml=8*960/500000*.0004*1e6)
    report['motor_711'] = dict(rated_torque_Nm=10*9.80665e-5,
        rated_power_at_3000_4500_6000_rpm_W=[10*9.80665e-5*r*2*math.pi/60
                                         for r in (3000,4500,6000)],
        required_output_W=10*.1)
    report['schedule'] = [dict(cycle_s=t,heads=min_heads(t),
                               time_s=6+math.ceil(6400/min_heads(t))*t)
                          for t in (.45,.50,.85,.90)]
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
