#!/usr/bin/env python3
"""Finite complementary pad sections and bounded command transfer; SI units.

All numeric inputs are scenarios, not measured process/part capabilities.
Run with Python 3; stdout JSON is disposable. No external dependencies.
"""
import itertools
import json
import math
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Pads:
    stroke: float = .0014
    aw: float = .0011
    ad: float = .0003
    kw: float = 20000.
    kd: float = 20000.
    mu: float = .1
    radius: float = .003
    return_force: float = 40.
    return_k: float = 2000.
    guide_drag: float = 1.
    mass: float = .01

    def normals(self, q):
        return self.kw * max(self.aw-q, 0), self.kd * max(q-self.ad, 0)

    def torques(self, q):
        return tuple(self.mu*self.radius*n for n in self.normals(q))

    def potential(self, q):
        return (self.return_force*q + .5*self.return_k*q*q + .5*self.kw*max(self.aw-q, 0)**2
                + .5*self.kd*max(q-self.ad, 0)**2)

    def command_work(self):
        return self.potential(self.stroke)-self.potential(0)+self.guide_drag*self.stroke

    def metrics(self):
        # Exact minimum: capacity is continuous piecewise affine in q.
        knots = sorted({0., self.stroke, min(self.stroke, max(0., self.aw)),
                        min(self.stroke, max(0., self.ad))})
        nw0, nd0 = self.normals(0)
        nws, nds = self.normals(self.stroke)
        return dict(min_capacity=min(sum(self.torques(q)) for q in knots),
                    park_capacity=self.torques(0)[0], drive_capacity=self.torques(self.stroke)[1],
                    park_clearance=self.ad, drive_clearance=self.stroke-self.aw,
                    return_margin=self.return_force-nw0+nd0-self.guide_drag,
                    peak_command=self.return_force+self.return_k*self.stroke+nds-nws+self.guide_drag,
                    command_work=self.command_work())


def section_check(p):
    """Check both 1D finite pad/rotor intervals, including spring overtravel.

    Separate axial stations: work rotor [-1,0] mm, idle rotor [0,1] mm.
    Work follower is to its right; idle follower to its left. Each follower
    has 1-mm thickness. Contact pins its face, compressing a separate spring;
    compression is NOT interpenetration of solids. Radial housing not modeled.
    """
    max_compression = 0.
    overlap = lambda a, b: max(0., min(a[1], b[1])-max(a[0], b[0]))
    work_rotor, idle_rotor = (-.001, 0.), (0., .001)
    assert math.isclose(overlap(work_rotor, (-.00005, .00095)), .00005)
    for i in range(1001):
        q = p.stroke*i/1000
        wface = max(0., q-p.aw)
        dface = min(0., q-p.ad)
        work_pad, idle_pad = (wface, wface+.001), (dface-.001, dface)
        assert overlap(work_rotor, work_pad) == 0
        assert overlap(idle_rotor, idle_pad) == 0
        assert wface >= 0 and dface <= 0
        cw, cd = max(p.aw-q, 0), max(q-p.ad, 0)
        nw, nd = p.normals(q)
        assert abs(nw*wface) < 1e-14 and abs(nd*dface) < 1e-14
        assert math.isclose(nw, p.kw*cw) and math.isclose(nd, p.kd*cd)
        max_compression = max(max_compression, cw, cd)
    return max_compression


def corners(p, e):
    # Threshold errors include coherent and opposing registration/warp biases.
    # Independent stiffness endpoints include shared lot shifts and mismatch.
    for dw, dd, sw, sd, mu, rad, ret in itertools.product(
            [-e, e], [-e, e], [.8, 1.2], [.8, 1.2], [.1, .3], [.9, 1.1], [.8, 1.2]):
        yield replace(p, aw=p.aw+dw, ad=p.ad+dd, kw=p.kw*sw, kd=p.kd*sd,
                      mu=mu, radius=p.radius*rad, return_force=p.return_force*ret,
                      return_k=p.return_k*ret)


def box(p, e, load=1., r=.002):
    stats = [c.metrics() for c in corners(p, e)]
    good = lambda m: (m['min_capacity'] > load*r and m['return_margin'] > 0
                      and min(m['park_clearance'], m['drive_clearance']) > 0)
    return dict(corners=len(stats), passing=sum(map(good, stats)),
                min_capacity=min(m['min_capacity'] for m in stats),
                min_return=min(m['return_margin'] for m in stats),
                peak_command=max(m['peak_command'] for m in stats),
                max_work=max(m['command_work'] for m in stats))


def friction_step(u, load_torque, bw, bd, omega, inertia, dt):
    """Backward Euler, exact prox of bw*|u|+bd*|u-omega|; includes static hold."""
    z = u-load_torque*dt/inertia
    a, b = bw*dt/inertia, bd*dt/inertia
    if z < -a-b:
        return z+a+b
    if z <= a-b:
        return 0.
    if z < omega+a-b:
        return z-a+b
    if z <= omega+a+b:
        return omega
    return z-a-b


def transition(p, family, sign, mode, dt, load=1., speed=.1, jd=1e-8):
    r = .002
    jw = max(.002, load/9.81)*r*r+1e-8
    inertia = jw+(jd if family == 'differential' else 0)
    omega = speed/r
    q, qv, u = (0., 0., 0.) if mode == 'start' else (p.stroke, 0., omega)
    x = heat = 0.
    q_stop = shaft_stop = None
    min_u = u
    max_q_energy_error = 0.
    q_energy0 = p.potential(q)
    guide_work = 0.
    command_peak = 0.
    for i in range(round(.15/dt)):
        t = (i+1)*dt
        qold = q
        if mode == 'start':
            # Prescribed smooth 5-ms command, finite endpoint speed/acceleration.
            z = min(t/.005, 1.)
            q = p.stroke*(3*z*z-2*z*z*z)
            qacc = p.stroke*(6-12*z)/.005**2 if t < .005 else 0.
            nw, nd = p.normals(q)
            cmd = p.mass*qacc+p.return_force+p.return_k*q+nd-nw+p.guide_drag
            command_peak = max(command_peak, cmd)
        elif q > 0:
            nw, nd = p.normals(q)
            force = nw-nd-p.return_force-p.return_k*q+p.guide_drag  # returning qv<0
            assert force < 0, 'return no longer monotone'
            qv += dt*force/p.mass
            q += dt*qv
            if q <= 0:
                q = 0.
                qv = 0.  # ideal dissipative endpoint; impact is not qualified
                q_stop = t
            else:
                guide_work += p.guide_drag*(qold-q)
                error = .5*p.mass*qv*qv+p.potential(q)+guide_work-q_energy0
                max_q_energy_error = max(max_q_energy_error, abs(error))
        bw, bd = p.torques(q)
        unew = friction_step(u, sign*load*r, bw, bd, omega, inertia, dt)
        x += r*unew*dt
        heat += dt*(bw*abs(unew)+bd*abs(omega-unew))
        min_u = min(min_u, unew)
        u = unew
        if mode == 'stop' and u == 0 and shaft_stop is None:
            shaft_stop = t
        if mode == 'stop' and q == 0 and u == 0:
            break
        if mode == 'start' and q == p.stroke and u == omega:
            break
    return dict(time=t, distance=x, heat=heat, q_stop=q_stop, shaft_stop=shaft_stop,
                min_speed=min_u*r, final_speed=u*r, max_q_energy_error=max_q_energy_error,
                command_peak=command_peak)


def checks():
    p = Pads()
    assert math.isclose(section_check(p), .0011)
    # Section closes by follower displacement, not a rigid overlapping shuttle.
    assert min(p.metrics()['park_clearance'], p.metrics()['drive_clearance']) > 0
    # Independent analytic V-min for unequal slopes: minimum at a contact edge.
    for c in corners(p, .0001):
        analytical = c.mu*c.radius*min(c.kw, c.kd)*(c.aw-c.ad)
        assert math.isclose(c.metrics()['min_capacity'], analytical, rel_tol=1e-12)
    # Midpoint work quadrature independently checks potential differences.
    n = 10000
    work = 0.
    for i in range(n):
        nw, nd = p.normals(p.stroke*(i+.5)/n)
        q = p.stroke*(i+.5)/n
        work += (p.return_force+p.return_k*q+nd-nw+p.guide_drag)*p.stroke/n
    assert abs(work-p.command_work()) < 1e-10
    # Exact free and middle-slip torque limits; both signed loads.
    for load in [-.002, .002]:
        assert math.isclose(friction_step(20, load, 0, 0, 50, 1e-6, 1e-5), 20-load*10)
        assert math.isclose(friction_step(20, load, .003, .004, 50, 1e-6, 1e-5),
                            20+(.004-.003-load)*10)
    assert friction_step(0, .002, .003, 0, 50, 1e-6, 1e-5) == 0
    assert friction_step(50, -.002, 0, .003, 50, 1e-6, 1e-5) == 50
    assert friction_step(0, .002, 0, 0, 50, 1e-6, 1e-5) < 0
    # Jidle -> 0 gives same reduced tangential transfer as friction clutch.
    a = transition(p, 'differential', 1, 'start', 1e-5, jd=0)
    b = transition(p, 'clutch', 1, 'start', 1e-5)
    assert a == b


def board(p, family, speed):
    passes = []
    for load, sign in [(.01962, 1), (1., 1), (1., -1), (.01962, -1)]:
        start = transition(p, family, sign, 'start', 4e-6, load, speed)
        stop = transition(p, family, sign, 'stop', 4e-6, load, speed)
        assert start['final_speed'] == speed and stop['final_speed'] == 0
        cruise_distance = .04-start['distance']-stop['distance']
        assert cruise_distance >= 0
        passes.append(start['time']+stop['time']+cruise_distance/speed)
    batch_time = .1+sum(passes)
    heads = next(h for h in range(1, 6401) if 6+math.ceil(6400/h)*batch_time < 30)
    return dict(heads=heads, time=6+math.ceil(6400/heads)*batch_time,
                channel_allowance=250/heads, site_2cent_allowance=122/heads,
                batch_time=batch_time, four_pass_command_work=4*6400*p.command_work(),
                simultaneous_open_power=heads*p.command_work()/.005)


def rebound(p, restitution):
    # Independent conservative return-energy bound, after immediate release at rest.
    impact = p.potential(p.stroke)-p.potential(0)-p.guide_drag*p.stroke
    energy = impact*restitution**2
    lo, hi = 0., p.stroke
    for _ in range(70):
        mid = (lo+hi)/2
        needed = p.potential(mid)-p.potential(0)+p.guide_drag*mid
        if needed < energy:
            lo = mid
        else:
            hi = mid
    return dict(impact_energy=impact, impact_speed=math.sqrt(2*impact/p.mass),
                rebound_q=(lo+hi)/2, work_capacity=p.torques((lo+hi)/2)[0])


def main():
    checks()
    p = Pads()
    out = {'evidence': 'deterministic scenarios, no measured priors', 'nominal':p.metrics(),
           'boxes':{str(e):box(p, e) for e in [0., .0001, .0002]},
           'load_10N':box(p, .0001, 10)}
    out['transitions'] = {f'{family}/{sign}/{mode}':transition(p, family, sign, mode, 2e-6)
                         for family in ['differential', 'clutch']
                         for sign in [-1, 1] for mode in ['start', 'stop']}
    out['refinement'] = {str(dt): transition(p, 'differential', -1, 'stop', dt)
                         for dt in [8e-6, 4e-6, 2e-6]}
    out['return_mass_bounds'] = {str(m):transition(replace(p, mass=m), 'differential', -1,
                                                'stop', 2e-6) for m in [.005, .02]}
    out['board'] = {f'{f}/{v}':board(p, f, v) for f in ['differential', 'clutch']
                     for v in [.1, .2, .3]}
    out['endpoint_rebound'] = {str(e): rebound(p, e) for e in [0., .3, .6, 1.]}
    # Neutral interval witness: old brake off, new one not yet touching.
    jw = max(.002, 1/9.81)*.002**2+1e-8
    out['neutral_drop_mm'] = {str(t):1000*.5*(1*.002/(jw+1e-8))*t*t*.002
                              for t in [.001, .005, .020]}
    candidates = []
    for stroke, k in itertools.product([.001, .0014, .002, .003, .005], [5000.,10000.,20000.,40000.]):
        aw, ad = stroke-.0003, .0003
        # Size return preload against maximum work-pad force + guide drag.
        ret = 1.1*(1.2*k*(aw+.0001)+1)/.8
        c = replace(p, stroke=stroke, aw=aw, ad=ad, kw=k, kd=k, return_force=ret)
        m = box(c, .0001)
        candidates.append(dict(stroke=stroke, k=k, return_force=ret, **m))
    out['synthesis'] = candidates
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
