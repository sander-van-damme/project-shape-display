#!/usr/bin/env python3
"""E-148: deterministic force/state/energy screens; SI, no empirical priors.

No contact CAD or motor design is represented. Print disposable JSON to stdout.
The signed output model grants a constant grounded Coulomb brake after a delay;
its purpose is to separate excitation, closure, and actual downstream arrest.
"""
import itertools
import json
import math

MU0 = 4 * math.pi * 1e-7


def box(mu, preload=1., gap=0.):
    # E-145 force boxes, summed pad-normal/opening coordinate (not per pad).
    scale = .1 / mu
    spring = 160 * scale * preload
    slope = 40000 * scale
    guide = 8 * scale
    stroke = .0004 + gap
    return_min = .8 * spring - guide
    peak = 1.2 * spring + slope * stroke + guide
    work = (1.2 * spring + guide) * stroke + .5 * slope * stroke**2
    return dict(mu=mu, spring=spring, slope=slope, guide=guide, stroke=stroke,
                return_min=return_min, peak=peak, work=work,
                capacity=mu * max(return_min, 0))


def magnetic_force(B, area):
    return B * B * area / (2 * MU0)


def field_return(b, area, B0, residual, tau, mass=.02, opening_speed=0., desired_capacity=11.):
    """Conservative return delay under an imposed field envelope.

    q stays at/below the opening stop until field falls to chosen threshold;
    thereafter force toward closure >= desired_capacity / mu. Assumes
    no rebound reopens pads, no regeneration, no remanence exceeding residual,
    and continued field envelope during motion. Not an electromagnetic solution.
    """
    remaining = b['return_min'] - magnetic_force(residual, area)
    capacity = b['mu'] * max(remaining, 0)
    target_normal = desired_capacity / b['mu']
    if remaining <= target_normal:
        return dict(delay=None, asymptotic_capacity=capacity, capacity=0.)
    threshold = math.sqrt(2 * MU0 * (b['return_min'] - target_normal) / area)
    wait = max(0., tau * math.log((B0-residual)/(threshold-residual)))
    accel = target_normal / mass
    mechanical = (opening_speed + math.sqrt(opening_speed**2 +
                  2*accel*b['stroke'])) / accel
    return dict(delay=wait + mechanical, field_wait=wait,
                mechanical=mechanical, capacity=desired_capacity, asymptotic_capacity=capacity)


def arrest(force, mass, velocity, delay, capacity, extra_energy=0.):
    """Down positive. Free motion, then ideal constant Coulomb reaction.

    Extra accessible energy is inserted in the velocity direction
    at closure. For zero velocity the force direction (or down) is used. No
    elasticity/impact/settling performance is silently inferred from this model.
    """
    x = velocity*delay + .5*force/mass*delay**2
    v = velocity + force/mass*delay
    extrema = [0., x]
    if force and 0 < -velocity*mass/force < delay:
        turn = -velocity*mass/force
        extrema.append(velocity*turn + .5*force/mass*turn**2)
    sign = 1 if v > 0 else -1 if v < 0 else 1 if force >= 0 else -1
    v = sign * math.sqrt(v*v + 2*extra_energy/mass)
    if capacity <= abs(force):
        return dict(holds=False, x_at_closure=x, v_at_closure=v)
    denom = capacity - sign*force
    slide = .5*mass*v*v / denom
    end = x + sign*slide
    extrema.append(end)
    # Explicit signed work and heat balance, including the admitted extra energy.
    heat = capacity*slide
    residual = .5*mass*velocity**2 + force*end + extra_energy - heat
    assert abs(residual) < 1e-10
    return dict(holds=True, minimum=min(extrema), maximum=max(extrema),
                final=end, stop_time=delay+mass*abs(v)/denom,
                heat=heat, energy_residual=residual)


def ground_path(where, closed, transmission=True, capture=True, jaw=True):
    # Graph is connectivity only: a positive answer is NOT rigidity or strength.
    edges = [('motor','shaft')] if transmission else []
    if capture:
        edges += [('shaft','column')]
    if closed:
        edges += [(where,'ground')] if where == 'motor' or jaw else []
    seen = {'column'}
    while True:
        nxt = seen | {b for a,b in edges if a in seen} | {a for a,b in edges if b in seen}
        if nxt == seen:
            return 'ground' in seen
        seen = nxt


def minimum_heads(extra, empty_return=0.):
    return next(h for h in range(1,6401)
                if 6 + math.ceil(6400/h)*(.45+extra+empty_return) < 30)


def checks():
    # Independent integral of virtual work for both signs of stator rotation.
    b = box(.1)
    errors = []
    for sign, n in itertools.product([-1,1],[16,64,256]):
        work = 0.
        phi_max = sign*.2
        dq_dphi = sign*b['stroke']/.2
        for j in range(n):
            phi = (j+.5)*phi_max/n
            force = 1.2*b['spring'] + b['slope']*dq_dphi*phi + b['guide']
            work += force*dq_dphi*phi_max/n
        errors.append(abs(work-b['work']))
    assert max(errors) < 1e-14  # Linear force: midpoint rule exact.
    assert math.isclose(box(.1)['work'], .0832)
    assert math.isclose(box(.1)['capacity'], 12.)
    # Signed work at normal steady speed: motor torque +Fr for either velocity.
    for F,v in itertools.product([0.,.02,1.,10.],[-.1,.1]):
        r=.002
        torque=F*r
        omega=-v/r  # down-positive v; up-positive rotor angle
        assert math.isclose(torque*omega, -F*v, abs_tol=1e-12)
    # Exact frictionless/unloaded delay and kinetic braking limits.
    a=arrest(0.,1.,.1,0.,2.)
    assert math.isclose(a['final'], .0025)
    a=arrest(0.,1.,-.1,.02,2.)
    assert math.isclose(a['final'], -.0045)
    assert ground_path('motor',True)
    assert not ground_path('motor',True,capture=False)
    assert ground_path('column',True,transmission=False,capture=False)
    assert not ground_path('column',True,capture=False,jaw=False)
    return dict(work_integral_errors=errors, signed_limits='pass')


def run():
    force_boxes = []
    for mu in [.02,.1,.3]:
        b=box(mu)
        force_boxes.append(dict(**b,
            direct_pole_area_at_1T_mm2=2*MU0*b['peak']*1e6,
            reaction_peak_Nm=b['peak']*b['stroke']/.2,
            reaction_work_rotation_at_10N=b['work']/.02))
    # Bounded shared errors; all heads in each box suffer the SAME shift.
    corners=[]
    for mu,preload,gap,field_factor in itertools.product(
            [.02,.1,.3],[.8,1.2],[-.0001,.00015],[.7,1.2]):
        b=box(mu,preload,gap)
        corners.append(dict(mu=mu,preload=preload,gap=gap,field_factor=field_factor,
            opening_margin=magnetic_force(field_factor,.0006)-b['peak'],
            hold_capacity=b['capacity'],work=b['work'],
            reaction_peak=b['peak']*b['stroke']/.2))
    returns=[]
    for tau,rem in itertools.product([.001,.01,.1],[0.,.1,.3,.6]):
        d=field_return(box(.1),.0006,1.,rem,tau)
        returns.append(dict(tau=tau,residual=rem,**d,
             output=arrest(10.,1.1,.1,d['delay'],d['capacity'])
             if d['delay'] is not None else None))
    signed=[]
    for F,v,E in itertools.product([0.,.02,1.,10.],[-.1,0.,.1],[0.,.005,.05]):
        signed.append(dict(force=F,velocity=v,extra_energy=E,
                           result=arrest(F,1.1,v,.01,12.,E)))
    graph=[]
    for where,trans,cap,jaw in itertools.product(['motor','column'],[False,True],
                                                [False,True],[False,True]):
        graph.append(dict(where=where,transmission=trans,capture=cap,jaw=jaw,
                          connected=ground_path(where,True,trans,cap,jaw)))
    # Observable state witnesses, not authenticated truth predicates.
    states=[]
    for name,B,torque,command in [
        ('powered_raise',1.,.02,True),('powered_lower',1.,.02,True),
        ('energized_stall',1.,.5,True),('wrong_sustained',1.,.02,True),
        ('isolated_field_decayed',0.,0.,False),
        ('free_inertia_open_circuit',0.,0.,False),
        ('regenerative_excitation_witness',1.,.5,False),
        ('zero_load_powered_motion',1.,0.,True)]:
        states.append(dict(name=name,field_open=magnetic_force(B,.0006)>=box(.1)['peak'],
            reaction_open=abs(torque)>=box(.1)['peak']*box(.1)['stroke']/.2,
            separate_open=command))
    return dict(checks=checks(),force_boxes=force_boxes,coherent_corners=corners,
        field_returns=returns,signed_arrest=signed,ground_graph=graph,states=states,
        schedules=[dict(extra=t,heads=minimum_heads(t),
                    head_ceiling=250/minimum_heads(t),
                    heads_with_empty_return=minimum_heads(t,.4))
                   for t in [0.,.01,.05,.1]],
        limits='Scenarios, not yield; graph connectivity is not force capacity.')

if __name__ == '__main__':
    print(json.dumps(run(),indent=2))
