#!/usr/bin/env python3
"""E-130: finite counterexamples, not a complete pocket assembly. Units mm,N,rad.

Trace rigid sphere/pin geometry in both directions; stop hardware admission at
an input-loss witness. Force cones are deliberately relaxed (ignore sphere spin
and grant captive pocket reactions); infeasibility survives those concessions.
"""
import itertools
import json
import math

D = 4.0
R = 4.0
PITCH = 5.08
PIN_R = .25
PIN_Y = 1.30
PIN_Z = -math.sqrt((D/2+PIN_R)**2-PIN_Y**2)


def distance(a, b):
    return math.sqrt(sum((x-y)**2 for x, y in zip(a, b)))


def state(kind, theta, n, d=D, radius=R):
    """Incoming sphere, old stack, grounded seat pins; actual center coordinates."""
    if kind == 'linear':
        lower = (-d*math.cos(theta), 0., 0.)
    else:
        lower = (-radius*math.cos(theta), 0.,
                 radius*math.sin(theta)-radius)
    # Exact old/new sphere contact; unlike a flags-only support model.
    dz = math.sqrt(d*d-lower[0]*lower[0])
    upper_z = lower[2]+dz
    stack = [(0., 0., upper_z+i*d) for i in range(n)]
    return lower, stack


def trace(kind, n, steps):
    start = 0. if kind == 'linear' else math.pi/6
    pins = [(0., s*PIN_Y, PIN_Z) for s in (-1, 1)]
    neighbor = [(0., PITCH, i*D) for i in range(8)]
    gap = math.inf
    neighbor_gap = math.inf
    contact_error = 0.
    heights = []
    for direction in (1, -1):
        indices = range(steps+1) if direction == 1 else range(steps, -1, -1)
        values = []
        for i in indices:
            angle = start+(math.pi/2-start)*i/steps
            lower, stack = state(kind, angle, n)
            contact_error = max(contact_error, abs(distance(lower, stack[0])-D))
            balls = [lower]+stack
            # Pins represent hemispherical tips on outboard rods. Distance to
            # each outboard rod is minimized at its listed inner endpoint.
            gap = min(gap, *(distance(b,p)-D/2-PIN_R for b in balls for p in pins))
            neighbor_gap = min(neighbor_gap,
                               *(distance(b,c)-D for b in balls for c in neighbor))
            for a, b in zip(stack, stack[1:]):
                assert abs(distance(a,b)-D) < 1e-10
            # Contact support of original bottom is lost immediately after start;
            # incoming sphere reaches the grounded seat only at the final pose.
            old_seat_gap = min(distance(stack[0],p)-D/2-PIN_R for p in pins)
            new_seat_gap = min(distance(lower,p)-D/2-PIN_R for p in pins)
            if i == 0:
                assert abs(old_seat_gap) < 1e-9
            elif i == steps:
                assert abs(new_seat_gap) < 1e-9
            else:
                assert old_seat_gap > 0 and new_seat_gap > 0
            values.append(stack[-1][2]+D)  # height above initial bottom tangent
        heights.append(values)
    assert heights[0] == list(reversed(heights[1]))
    assert abs(heights[0][0]-n*D) < 1e-9
    assert abs(heights[0][-1]-(n+1)*D) < 1e-9
    assert gap >= -1e-9 and neighbor_gap > 0 and contact_error < 1e-9
    return dict(topology=kind, n=n, steps=steps,
                height_endpoints=[heights[0][0],heights[0][-1]],
                pin_min_clearance=gap, neighbor_min_clearance=neighbor_gap,
                sphere_contact_residual=contact_error)


def linear_margin(load, mu_contact, mu_guide, mu_pallet, mass_load, theta=math.pi/4):
    """Necessary input-free force balance, relaxed sphere moments.

    Old/new force ratio Fx/Fz >= cot(theta+atan(mu_contact)) = rho.
    For actual ratio r >= rho, upper guide gives Fz >= W/(1+mu_guide*r).
    Pallet grounded guide
    can resist at most mu_pallet*(Fz+mass_load). Positive result is a
    lower bound on missing horizontal restraint, for rho>mu_pallet.
    Increasing rho increases this bound; choose its most favorable endpoint.
    """
    rho = 1/math.tan(theta+math.atan(mu_contact))
    return (rho-mu_pallet)*load/(1+mu_guide*rho)-mu_pallet*mass_load


def rotary_bound(load, mu, journal_mu, journal_radius, carrier_weight):
    """At theta=45 deg with radius=D: all contact force ratios positive.

    T=((R-r)*Fz+(R+r)*Fx)/sqrt(2), including tangential force moment
    at the actual sphere contact point; journal friction <= mu_b*r_b*|bearing load|.
    Triangle inequality |bearing load| <= Fx+Fz+C. Load at pivot is a
    favorable assumption for carrier weight C. Ball weight is omitted.
    """
    rho = 1/math.tan(math.pi/4+math.atan(mu))
    fz = load/(1+mu*rho)
    # Minimize the COMBINED torque deficit over r >= rho. Its derivative
    # has sign (b-j)-mu*(a-j)>0 throughout these parameter bounds.
    sum_min = (1+rho)*fz
    torque_min = ((R-D/2)+(R+D/2)*rho)*fz/math.sqrt(2)
    return torque_min-journal_mu*journal_radius*(sum_min+carrier_weight)


def finite_witness(kind):
    lower, stack = state(kind, math.pi/4, 3)
    # Finite rear and bottom pocket pad tips, both compressive supporting faces.
    # Other walls/captive lips are granted, not claimed constructed. No old-ball
    # collision at this witness; no claim of complete rotating-pocket sweeps.
    pads = [(lower[0]-D/2-PIN_R,0.,lower[2]),
            (lower[0],0.,lower[2]-D/2-PIN_R)]
    assert all(abs(distance(lower,p)-D/2-PIN_R)<1e-10 for p in pads)
    gap = min(distance(b,p)-D/2-PIN_R for b in stack for p in pads)
    pins = [(0.,s*PIN_Y,PIN_Z) for s in (-1,1)]
    return dict(topology=kind, lower=lower, upper=stack[0], pad_old_gap=gap,
                old_seat_gap=min(distance(stack[0],p)-D/2-PIN_R for p in pins),
                new_seat_gap=min(distance(lower,p)-D/2-PIN_R for p in pins),
                height_above_old_seat=stack[0][2])


def checks():
    # Independent virtual work derivative vs contact-force reaction for frictionless
    # linear and rotary witnesses; centered derivative convergence is explicit.
    derivative = []
    for kind in ('linear','rotary'):
        expected = 1. if kind == 'linear' else (R+D)/math.sqrt(2)
        errors = []
        for eps in (1e-3, 1e-4, 1e-5):
            lo, sl = state(kind,math.pi/4-eps,3)
            hi, sh = state(kind,math.pi/4+eps,3)
            denom = hi[0]-lo[0] if kind == 'linear' else 2*eps
            estimate = (sh[0][2]-sl[0][2])/denom
            errors.append(abs(estimate-expected))
        assert errors[-1] < 1e-8
        derivative.append(dict(topology=kind,errors=errors))
    # Reconstruct torque about rotary pivot at the actual upper/lower contact.
    lower, stack = state('rotary', math.pi/4, 3)
    contact = tuple((a+b)/2 for a,b in zip(lower,stack[0]))
    for rho in (.53846153846,1.,1.857142857):
        rx, rz = contact[0], contact[2]+R
        cross = rx*(-1)-rz*(-rho)
        closed = ((R-D/2)+(R+D/2)*rho)/math.sqrt(2)
        assert abs(cross-closed) < 1e-10
    # Limit: zero friction linear restraint equals W*cot(theta).
    assert abs(linear_margin(1,0,0,0,0)-1) < 1e-12
    # Infinite friction is not inferred: mark exact wedge threshold independently.
    threshold_mu = math.sqrt(2)-1
    assert abs(linear_margin(1,threshold_mu,0,threshold_mu,0)) < 1e-12
    # This obstruction disappears above threshold; not a full equilibrium proof.
    assert linear_margin(1,.5,.5,.5,0) < 0
    return derivative


def main():
    derivative = checks()
    traces = [trace(k,n,steps) for k,n,steps in itertools.product(
        ('linear','rotary'),(3,8),(64,256,1024))]
    scenarios = []
    for w,mc,mg,mp,c in itertools.product((1.,3.27,10.),(.05,.1,.3),
                                         (.05,.1,.3),(.05,.1,.3),(0.,.2)):
        m = linear_margin(w,mc,mg,mp,c)
        assert m > 0
        scenarios.append(m)
    rotary = [rotary_bound(w,mu,jm,jr,c) for w,mu,jm,jr,c in itertools.product(
        (1.,3.27,10.),(.05,.1,.3),(.05,.1,.3),(.4,.6),(0.,.2))]
    assert min(rotary)>0
    # Common process error changes all d/pin seats, not independent cell draws.
    dimensions = []
    for error in (-.05,0.,.05):
        d = D+error
        # Fixed nominal seat: solve actual sphere height from the pin coordinates.
        seated_z = PIN_Z+math.sqrt((d/2+PIN_R)**2-PIN_Y**2)
        angle = math.pi/4
        for kind in ('linear','rotary'):
            lower, stack = state(kind,angle,3,d=d)
            # Actual force angle, no nominal-angle assertion after size change.
            theta = math.atan2(stack[0][2]-lower[2],-lower[0])
            dimensions.append(dict(bias=error,topology=kind,seated_z=seated_z,
                contact_angle_deg=math.degrees(theta),
                linear_margin_at_same_angle=linear_margin(1,.3,.3,.3,.2,theta)))
    # Independent diameter/carrier biases at the same rotary phase, exact contact
    # torque including contact-point offset. Shared across a bank, not iid draws.
    rotary_dimension_margins = []
    for d, radius in itertools.product((3.95,4.,4.05),(3.95,4.,4.05)):
        lower, stack = state('rotary',math.pi/4,3,d,radius)
        theta = math.atan2(stack[0][2]-lower[2],-lower[0])
        rho = 1/math.tan(theta+math.atan(.3))
        fz = 1/(1+.3*rho)
        a = radius/math.sqrt(2)-d/2*math.cos(theta)
        b = radius/math.sqrt(2)+d/2*math.sin(theta)
        margin = (a+b*rho)*fz-.3*.6*((1+rho)*fz+.2)
        assert margin > 0
        rotary_dimension_margins.append(margin)
    # Full-grid copy collides with the unchanged upstream site's bottom sphere.
    inline = []
    for kind in ('linear','rotary'):
        start = 0 if kind=='linear' else math.pi/6
        lower,_ = state(kind,start,3)
        inline.append(dict(topology=kind,
                           upstream_sphere_gap=distance(lower,(-PITCH,0.,0.))-D))
    print(json.dumps(dict(checks='passed',evidence='rigid geometry and necessary force bounds; no hardware pass',
        traces=traces,witnesses=[finite_witness(k) for k in ('linear','rotary')],
        linear_scenarios=len(scenarios),linear_min_missing_force_N=min(scenarios),
        linear_3p27N_best_friction_missing_N=linear_margin(3.27,.3,.3,.3,.2),
        rotary_scenarios=len(rotary),rotary_min_missing_torque_Nmm=min(rotary),
        rotary_3p27N_best_friction_missing_Nmm=rotary_bound(3.27,.3,.3,.6,.2),
        dimensions=dimensions,rotary_dimension_min_missing_Nmm=min(rotary_dimension_margins),inline_replication=inline,derivative_checks=derivative),indent=2))

if __name__ == '__main__':
    main()
