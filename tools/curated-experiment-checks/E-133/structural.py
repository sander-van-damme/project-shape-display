#!/usr/bin/env python3
"""E-133: necessary structural-memory bounds. mm, N, N/mm², N mm.
No calibrated priors, random sampling, CAD qualification or hardware prediction.
"""
import itertools
import json
import math


def bisect(f, a, b):
    assert f(a) * f(b) <= 0
    for _ in range(80):
        c = (a + b) / 2
        if f(a) * f(c) <= 0:
            b = c
        else:
            a = c
    return (a + b) / 2


class Crown:
    """Six axial elastic spokes between coaxial rings; ideal free joints.
    r is radial span, h natural rise, A spoke cross-section, E axial modulus.
    This is a finite nonplanar truss comparator, NOT a shell constitutive law.
    """
    def __init__(self, r=1.4, h=.2, area=.16, modulus=2000):
        self.r, self.h = r, h
        self.l0 = math.hypot(r, h)
        self.c = 6 * modulus * area / self.l0

    def u(self, q):
        return self.c / 2 * (math.hypot(self.r, q) - self.l0) ** 2

    def du(self, q):
        l = math.hypot(self.r, q)
        return self.c * q * (1 - self.l0 / l)

    def k(self, q):
        return self.c * (1 - self.l0 * self.r ** 2 / math.hypot(self.r, q) ** 3)

    def fold(self):
        l = (self.l0 * self.r ** 2) ** (1 / 3)
        q = math.sqrt(l * l - self.r ** 2)
        return q, -self.du(q)

    def loaded(self, force):
        qf, fc = self.fold()
        if force >= fc:
            return {"retained": False, "fold_N": fc}
        g = lambda q: self.du(q) + force
        saddle = bisect(g, 0, qf)
        high = bisect(g, qf, self.h)
        low = bisect(g, -self.h - force / self.c - self.l0, -self.h)
        v = lambda q: self.u(q) + force * q
        return {"retained": True, "fold_N": fc, "barrier_Nmm": v(saddle)-v(high),
                "high_mm": high, "low_mm": low, "loaded_step_mm": high-low}


def crowns():
    out = []
    # Explicit coherent material/process scenarios, not probabilities.
    for h in (.2, .4, .8, 1.2):
        c = Crown(h=h)
        n = math.ceil(40/(2*h))
        out.append({"rise_mm": h, "stages": n, "board_spokes": 6400*6*n,
                    "flat_strain": 1-c.r/c.l0, "zero_load_barrier_Nmm": c.u(0),
                    "end_clamped_exchange_curvature_N_per_mm": c.k(0)+c.k(h)/(n-1),
                    "loads": {str(f): c.loaded(f) for f in (.05, .2, 1, 10)}})
    scenarios = []
    for E, width, rise_bias, radius_bias in itertools.product(
            (1000, 2000, 3000), (.3, .4, .5), (-.1, 0, .1), (-.1, 0, .1)):
        c = Crown(r=1.4+radius_bias, h=.2+rise_bias, area=width**2, modulus=E)
        scenarios.append({"fold": c.fold()[1], "strain": 1-c.r/c.l0,
                          "stroke_100": 200*c.h, "loaded": c.loaded(.2)})
    # Bias correlation affects range differently from cancelling alternating errors.
    return {"nominal": out, "coherent_cases": len(scenarios),
            "fold_range_N": [min(x['fold'] for x in scenarios),max(x['fold'] for x in scenarios)],
            "hold_0.2N_cases": sum(x['loaded']['retained'] for x in scenarios),
            "100_stage_free_travel_range_mm": [min(x['stroke_100'] for x in scenarios),max(x['stroke_100'] for x in scenarios)],
            "strain_range": [min(x['strain'] for x in scenarios),max(x['strain'] for x in scenarios)],
            "alternating_rise_bias_free_travel_mm": sum(2*(.2+(-1)**i*.1) for i in range(100))}


def kresling():
    # Two natural axial/diagonal lengths between hexagonal rings at fixed R.
    # Other stress-free branch follows sin(theta+alpha/2)=constant.
    cases = []
    R, alpha = 2.1, math.pi/3
    for H0, degrees in itertools.product((2, 4, 8, 12), (0, 15, 30, 45)):
        t0 = math.radians(degrees)
        t1 = math.pi-alpha-t0
        hsq = H0*H0+2*R*R*(math.cos(t1)-math.cos(t0))
        if hsq <= 0:
            continue
        H1 = math.sqrt(hsq)
        stroke = H0-H1
        def lengths(h,t):
            return [math.sqrt(h*h+2*R*R*(1-math.cos(t+a))) for a in (0,alpha)]
        assert max(abs(a-b) for a,b in zip(lengths(H0,t0),lengths(H1,t1))) < 1e-10
        cases.append({"H0_mm": H0, "theta0_deg": degrees, "stroke_mm": stroke,
                      "stages_for_40": math.ceil(40/stroke),
                      "twist_per_stage_deg": math.degrees(t1-t0)})
    return {"generated": 16, "real_second_states": len(cases), "cases": cases,
            "fixed_radius_two_length_stroke_upper_bound_mm": 2*R}


def geometry():
    # Actual radial spoke centerlines with .2-mm capsule radius; annular membranes
    # would fill their azimuthal gaps. All shapes inside a 2.3-mm outer radius.
    # Compare continuous spoke separation across adjacent stages analytically:
    # gap(s) = d0+qi + (qj-qi)*s, s in [0,1].
    h, d0, capsule, R = .2, 1., .2, 2.1
    # Generate each spoke at 6 azimuths, three states, 65 points along its length.
    points=[]
    for q, j, i in itertools.product((-h,0,h), range(6), range(65)):
        t=i/64
        radius=R-1.4*t
        angle=j*math.pi/3
        points.append((radius*math.cos(angle),radius*math.sin(angle),q*t))
    assert max(math.hypot(x,y)+capsule for x,y,z in points)<=R+capsule+1e-12
    # Fixed-radius circumcylinder contains every intermediate state, not just samples.
    gaps=[]
    for qi,qj in itertools.product((-h,0,h), repeat=2):
        gaps.append(min(d0+qi,d0+qj)-2*capsule)
    # State-independent circumcylinder bound for an unchanged adjacent column.
    neighbor_margin=5.08-2*(R+capsule)
    # Central reusable probe: lumen=.7-.2; shaft radius=.3, pose=.1.
    lumen=.7-capsule
    probe_margin=lumen-.3-.1
    # Through-spoke access at center is open; solid outer plates/actuator coupling
    # are not generated. This is envelope clearance, not a completed selector.
    return {"generated_spoke_points": len(points),
            "same_radius_stage_axial_projection_margin_mm": min(gaps),
            "neighbor_radial_envelope_margin_mm": neighbor_margin,
            "probe_lumen_margin_mm": probe_margin,
            "neighbor_margin_with_0.15_each_growth_and_0.2_relative_warp_mm": neighbor_margin-.3-.2,
            "lumen_margin_with_0.1_shrink_and_0.1_shaft_growth_mm": probe_margin-.2,
            "4.6mm_top_gap_mm":5.08-4.6}


def tape():
    # Homogeneous phase-front energy V(l)=(F-g)l. Zero slope is neutral, not memory.
    # Introduced pinning texture: B/2*(1-cos(2*pi*l/s)); this is a changed mechanism.
    step=5.
    return {"homogeneous_front_stiffness_N_per_mm":0,
            "pinning_barrier_required_Nmm": {str(F):F*step/math.pi for F in (.2,1,10)},
            "PLA_coil_min_radius_mm": {str(e):.4/(2*e) for e in (.005,.01,.02)}}


def control():
    # Reused positive ground-pin control, not a new latch/fit proposal.
    # States enumerate commanded support ownership only; contacts are NOT validated.
    levels=list(range(0,41,5))
    traces=0
    for old,new in itertools.product(levels,repeat=2):
        if old==new:
            trace=[(True,False)] # unchanged stays on ground stop
        else:
            trace=[(True,False),(True,True),(False,True),
                   (False,True),(True,True),(True,False)]
        assert all(ground or writer for ground,writer in trace)
        traces+=1
    # Failed proof cannot advance to release sole support.
    def transfer(acquired, seated):
        if not acquired:
            return (True,False)
        if not seated:
            return (False,True)
        return (True,False)
    assert transfer(False,False)==(True,False)
    assert transfer(True,False)==(False,True)
    # These guards require actual sensors/capture hardware to implement.
    return {"levels_mm":levels,"endpoint_pairs":traces,"support_guard_cases":2,
            "unchanged_deliberate_motion_mm":0,"geometry_status":"inherited E-132, not passed"}


def full_board():
    # Allocations, not measured/achievable rates. 6s all non-cell work incl bounded retry.
    budget=24
    return {"parallel_heads_min":{str(t):math.floor(6400*t/budget)+1 for t in (.02,.1,.5,1)},
            "80_head_cell_budget_s":budget/80,
            "80_head_stage_budget_s_for_100_stages":budget/80/100,
            "bought_per_site_at_250_reserve":{str(cap):(cap-250)/6400 for cap in (400,500)},
            "expected_false_acceptances_not_probability":{str(p):6400*p for p in (1e-3,1e-4,1e-5)},
            "assembly_hours_10_to_30_s_per_site":[6400*10/3600,6400*30/3600],
            "1N_full_field_work_J":6400*1*40/1000}


def checks():
    c=Crown()
    assert abs(c.u(c.h)) < 1e-20 and abs(c.du(c.h)) < 1e-10
    assert abs(c.k(c.fold()[0])) < 1e-10
    z=c.loaded(0)
    assert abs(z['barrier_Nmm']-c.u(0)) < 1e-10
    assert not c.loaded(c.fold()[1]*1.001)['retained']
    # Independent work integral and finite-difference force/stiffness holdouts.
    errors=[]
    for n in (100,1000,10000):
        dx=c.h/n
        integral=dx*(.5*c.du(0)+.5*c.du(c.h)+sum(c.du(i*dx) for i in range(1,n)))
        errors.append(abs(integral-(c.u(c.h)-c.u(0))))
    assert errors[2]<errors[1]<errors[0] and errors[2]<1e-8
    q=.13; eps=1e-5
    assert abs((c.u(q+eps)-c.u(q-eps))/(2*eps)-c.du(q))<1e-7
    assert abs((c.du(q+eps)-c.du(q-eps))/(2*eps)-c.k(q))<1e-6
    # Exact constant-total-height perturbation of one saddle + 99 extended stages.
    n=100
    def path(x): return c.u(x)+(n-1)*c.u(c.h-x/(n-1))
    curvature=c.k(0)+c.k(c.h)/(n-1)
    measured=(path(eps)-2*path(0)+path(-eps))/eps**2
    assert curvature<0 and abs(measured-curvature)<1e-3
    # Identical crowns have n+1 distinct sums, not 2**n distinct heights.
    levels={sum(bits) for bits in itertools.product((0,1),repeat=8)}
    assert len(levels)==9
    return {"work_integral_errors_Nmm":errors,"exchange_curvature_analytic":curvature,
            "exchange_curvature_finite_difference":measured,"checks":"passed"}


if __name__ == '__main__':
    print(json.dumps({"crowns":crowns(),"kresling":kresling(),"geometry":geometry(),
                      "tape":tape(),"control":control(),"board":full_board(),"verification":checks()},indent=2))
