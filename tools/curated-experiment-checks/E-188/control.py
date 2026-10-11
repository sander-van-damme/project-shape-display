#!/usr/bin/env python3
"""Signed band bounds, imposed coil opening, and shared-cam energy accounting.

Standard library, SI units. All numerical inputs are bounded scenarios, not
measured PLA/wire properties, release-force predictions, or reliability priors.
"""
import importlib.util
import itertools
import json
import math
import pathlib
import sys


def band(torque, radius, mu, turns, segments=0):
    """Incipient sliding of a flexible tensile band; NOT a wire release law."""
    theta = 2*math.pi*turns
    gain = math.exp(mu*theta)
    slack = abs(torque)/(radius*math.expm1(mu*theta))
    tight = gain*slack
    # Euler integrate dT/dtheta=mu*T as a separate discretized holdout.
    numerical = slack*(1+mu*theta/segments)**segments if segments else tight
    assert math.isclose(radius*(tight-slack), abs(torque), abs_tol=1e-12)
    return dict(gain=gain, slack_N=slack, tight_N=tight,
                fixed_end_reverse_ratio=gain, numerical_tight_N=numerical)


def opening(turns=3, wire=.0003, modulus=200e9, error=.0001, robust=False):
    """Inextensible planar curved-rod trial shape, constant curvature.

    Tang angle opens natural coil radius Rf to Rf*theta/(theta-alpha).
    Circumferential stiffness EI/(Rf*theta); ignores helix/tang/contact effects.
    Error is a radius bound on EACH of hub and natural coil; no probability.
    """
    hub, interference, gap, seat = .003, .00005, .00005, .0035
    if robust:
        interference = max(interference,2*error+.000025)
    theta = 2*math.pi*turns
    rf = hub+wire/2-interference
    # Exact worst corner: small natural coil, large hub.
    required = hub+error+wire/2+gap
    alpha = theta*(1-(rf-error)/required)
    assert 0 < alpha < theta
    rows = []
    for eh, ef in itertools.product([-error, error], repeat=2):
        actual_rf = rf+ef
        rc = hub+eh+wire/2
        ro = actual_rf*theta/(theta-alpha)
        # A loose coil stays at its natural radius, not artificially compressed
        # inward onto a smaller hub. Such a corner has no earned engagement.
        ac = max(0.,theta*(1-actual_rf/rc))
        stiffness = modulus*math.pi*wire**4/64/(actual_rf*theta)
        u = .5*stiffness*(alpha**2-ac**2)
        # Trial-shape stress magnitude at endpoint, not an allowable.
        stress = modulus*wire/2*abs(1/ro-1/actual_rf)
        rows.append(dict(gap_m=ro-wire/2-(hub+eh), natural_interference_m=rc-actual_rf,
                         opening_work_J=u, unloaded_tang_force_N=stiffness*alpha/seat,
                         trial_stress_Pa=stress))
        assert rows[-1]['gap_m'] >= gap-1e-14
        # Independent energy quadrature over imposed angle, with SI work units.
        count = 1000
        da = (alpha-ac)/count
        work = sum(stiffness*(ac+(i+.5)*da)*da for i in range(count))
        assert math.isclose(work, u, abs_tol=1e-12)
    return dict(turns=turns, wire_m=wire, modulus_Pa=modulus, each_radius_bound_m=error,
                robust_interference=robust, nominal_interference_m=interference,
                angle_rad=alpha, one_end_arc_m=seat*alpha,
                min_gap_m=min(x['gap_m'] for x in rows),
                min_natural_interference_m=min(x['natural_interference_m'] for x in rows),
                max_work_J=max(x['opening_work_J'] for x in rows),
                max_unloaded_force_N=max(x['unloaded_tang_force_N'] for x in rows),
                max_trial_stress_Pa=max(x['trial_stress_Pa'] for x in rows))


def pad_model():
    path = pathlib.Path(__file__).resolve().parents[1]/'E-187'/'transfer.py'
    spec = importlib.util.spec_from_file_location('e187', path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.Pads()


def cam(qphase, p):
    # One opening and closing per revolution; zero endpoint velocities.
    q = .5*p.stroke*(1-math.cos(qphase))
    derivative = .5*p.stroke*math.sin(qphase)
    nw, nd = p.normals(q)
    potential_derivative = p.return_force+p.return_k*q+nd-nw
    torque = potential_derivative*derivative+p.guide_drag*abs(derivative)
    return torque


def recovery(steps):
    p = pad_model()
    dphi = 2*math.pi/steps
    torques = [cam((i+.5)*dphi,p) for i in range(steps)]
    positive = sum(max(t,0)*dphi for t in torques)
    returned = -sum(min(t,0)*dphi for t in torques)
    du = p.potential(p.stroke)-p.potential(0)
    assert abs(positive-(du+p.guide_drag*p.stroke)) < 1e-7
    assert abs(returned-(du-p.guide_drag*p.stroke)) < 1e-7
    residual = positive-returned-2*p.guide_drag*p.stroke
    assert abs(residual) < 2e-9
    # Shared phase necessarily gives equal commands for identical rigid followers.
    # Best possible common q approximating requested endpoints (0,S) still misses S/2.
    mismatch = min(max(abs(p.stroke*i/1000), abs(p.stroke*i/1000-p.stroke))
                   for i in range(1001))
    assert math.isclose(mismatch,p.stroke/2)
    # Both followers opening at once: there is no balancing return partner.
    return dict(steps=steps, input_J=positive, returned_J=returned,
                net_J=positive-returned, energy_residual_J=residual, peak_torque_Nm=max(torques),
                two_head_min_endpoint_error_m=mismatch,
                bank_183_peak_torque_Nm=183*max(torques),
                bank_183_stored_delta_J=183*du,
                board_command_J_by_recovery={str(eta):4*6400*(positive-eta*returned)
                                            for eta in (0,.5,.8,1)})


def heads(service):
    for h in range(1,6401):
        total = 6+math.ceil(6400/h)*service
        if total < 30:
            return dict(heads=h, seconds=total, allowance_USD=(500-250)/h)
    raise ValueError('no admissible head count')


def loss_delay(delay, force=1., speed=.3, brake_torque=.006, radius=.002):
    """Favorable constant brake after a stipulated delay; not wrap contact dynamics."""
    mass = max(.002,force/9.81)+1e-8/radius**2
    acceleration = force/mass
    travel_before = speed*delay+.5*acceleration*delay**2
    v = speed+acceleration*delay
    if brake_torque/radius <= force:
        return dict(delay_s=delay, finite_stop=False)
    stop = .5*mass*v*v/(brake_torque/radius-force)
    heat = brake_torque/radius*stop
    assert math.isclose(heat,.5*mass*speed**2+force*(travel_before+stop),abs_tol=1e-12)
    return dict(delay_s=delay, finite_stop=True, travel_m=travel_before+stop, brake_heat_J=heat)


def main():
    # Direction swap exchanges ends, not torque capacity; fixed-end control pays gain.
    bands = []
    for mu, turns in itertools.product((.05,.1,.2), (1,3,5)):
        a = band(.002,.003,mu,turns)
        assert a == band(-.002,.003,mu,turns)
        bands.append(dict(mu=mu, turns=turns, **a))
    # mu -> 0 eliminates self-energizing advantage, requiring divergent band preload.
    low = band(.002,.003,1e-7,3)
    assert math.isclose(low['slack_N']*.003*(1e-7*6*math.pi), .002, rel_tol=1e-5)
    capstan_holdout = []
    exact = band(.002,.003,.1,3)['tight_N']
    for n in (100,1000,10000):
        capstan_holdout.append(dict(segments=n, relative_error=
            abs(band(.002,.003,.1,3,n)['numerical_tight_N']/exact-1)))
    assert all(a['relative_error']>b['relative_error'] for a,b in zip(capstan_holdout,capstan_holdout[1:]))
    openings = [opening(wire=d,modulus=e,error=b,robust=r) for d,e,b,r in
                itertools.product((.0003,.0006),(3e9,200e9),(0,.000025,.0001,.0002),(False,True))]
    # Turns multiply angle/work but not strain or tang force in this restricted trial family.
    a,b=opening(turns=1),opening(turns=5)
    assert math.isclose(b['max_work_J'],5*a['max_work_J'])
    assert math.isclose(b['max_unloaded_force_N'],a['max_unloaded_force_N'])
    assert math.isclose(b['max_trial_stress_Pa'],a['max_trial_stress_Pa'])
    recovery_rows = [recovery(n) for n in (2000,8000,32000)]
    schedules = {str(ms):heads(4*(.04/.3+ms/1000)+.1) for ms in (0,5,10,20)}
    print(json.dumps(dict(bands=bands,capstan_holdout=capstan_holdout,openings=openings,
                          recovery=recovery_rows,schedules=schedules,
                          loss_delay=[loss_delay(t) for t in (0,.005,.02)]),indent=2))


if __name__ == '__main__':
    main()
