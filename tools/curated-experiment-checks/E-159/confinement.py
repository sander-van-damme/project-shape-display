#!/usr/bin/env python3
"""E-159 deterministic necessary conditions, SI units; no material/yield priors."""
import itertools
import json
import math
import sys


def braid(mu, angle, length, radius, preload, gap):
    t2 = math.tan(math.radians(angle)) ** 2
    exponent = mu * length * t2 / radius
    radicand = 1 - t2 * ((1 + gap / radius) ** 2 - 1)
    stroke = length * (1 - math.sqrt(radicand)) if radicand >= 0 else None
    return dict(K=exponent, down_N=preload * math.expm1(exponent),
                up_N=preload * -math.expm1(-exponent), stroke_m=stroke)


def grain(mu_i, mu_o, K, length, ri, ro, spring_force):
    """Limiting annular stress field for a descending stalk, compression positive.
    Stalk drags grains down, outer wall reacts upward, bottom seat takes S(L).
    K and simultaneous friction mobilization are assumptions, not a packing law.
    """
    area = math.pi * (ro * ro - ri * ri)
    inner, outer = mu_i * 2 * math.pi * ri, mu_o * 2 * math.pi * ro
    rate = K * (inner - outer) / area
    integral = length if abs(rate) < 1e-10 else math.expm1(rate*length)/rate
    return spring_force * inner * K / area * integral


def cut(capacity, up_capacity, closure, mass, force, velocity):
    """Piecewise free gap then instant full Coulomb brake; favorable witness.
    force downward, v positive downward. No elastic inventory/dynamic braid."""
    x = velocity * closure + force / mass * closure ** 2 / 2
    v = velocity + force / mass * closure
    if v >= 0:
        if capacity <= force:
            return dict(gap_m=x, stop_m=None, reason='no downward arrest')
        coast = mass * v * v / (2 * (capacity - force))
    else:
        coast = -mass * v * v / (2 * (up_capacity + force))
    return dict(gap_m=x, stop_m=x + coast, reason='conditional first stop')


def schedule(heads, speed, overhead=.10):
    # Shared signed strokes, one extra empty return, completion reserve.
    return 6 + math.ceil(6400 / heads) * (3 * .04 / speed + overhead)


def state_witness():
    # Quasistatic scalar force witnesses, NOT contact geometry or sensor proof.
    closed = braid(.2,45,.02,.0015,.1,0)['down_N']
    load, writer_capacity = 1.0, 10.0
    phases = [('park',1,False), ('capture',1,True), ('release',0,True),
              ('move',0,True), ('return',1,True), ('proof',1,True),
              ('withdraw',1,False)]
    cuts, count = [], 0
    for old, new in itertools.product([0, .01, .04], repeat=2):
        position, neighbor = old, .025
        for name, contact, capture in phases:
            if name == 'move': position = new
            ground = closed * contact
            support = ground + writer_capacity * capture
            assert support >= load
            assert closed >= load and neighbor == .025
            if ground < load: cuts.append([old,new,name])
            count += 1
        assert position == new
    # Explicit faults: global open, weak contact, and a lying proof reader.
    half = .1*math.expm1(braid(.2,45,.02,.0015,.1,0)['K']*.5)
    faults = dict(global_open_neighbor_margin_N=-load,
                  half_contact_after_withdraw_margin_N=half-load,
                  false_accept_open_withdraw_margin_N=-load)
    assert all(value < 0 for value in faults.values())
    return dict(guard_cases=count, unsupported_drive_cuts=len(cuts),
                cut_states=cuts, faults=faults,
                meaning='ideal capacity guards; cut motion evaluated separately')


def checks():
    b = braid(0, 45, .02, .0015, .1, 0)
    assert b['down_N'] == b['up_N'] == b['stroke_m'] == 0
    assert braid(.2, 45, .02, .0015, 0, 0)['down_N'] == 0
    # Independent segment equilibrium approximation, converges to exponential.
    K, P = 2.666666666666666, .1
    exact = P * math.exp(K)
    errs = []
    for n in [100, 200, 400, 800]:
        value = P
        for _ in range(n):
            value += value * K / n
        errs.append(abs(value - exact))
    assert all(b < a for a, b in zip(errs, errs[1:]))
    # Virtual-work helix derivative dL/dr=-L*tan(theta)^2/r.
    r, L, angle = .0015, .02, 45
    dg = 1e-9
    derivative = braid(.2, angle, L, r, .1, dg)['stroke_m'] / dg
    assert math.isclose(derivative, L / r, rel_tol=1e-5)
    # Exact strand length conservation in finite release.
    nturn = L * math.tan(math.radians(angle)) / (2 * math.pi * r)
    stroke = braid(.2, angle, L, r, .1, .00015)['stroke_m']
    assert math.isclose(L**2 + (2*math.pi*nturn*r)**2,
                        (L-stroke)**2 + (2*math.pi*nturn*(r+.00015))**2)
    # Annular axial equilibrium, plus zero length/friction limits.
    assert grain(0, .2, .5, .02, .0015, .0022, 1) == 0
    assert grain(.2, .2, .5, 0, .0015, .0022, 1) == 0
    ri, ro, K, L, S = .0015, .0022, .5, .01, 1
    fi = grain(.2,.2,K,L,ri,ro,S)
    fo = fi * ro/ri
    rate = K*(.2*2*math.pi*ri-.2*2*math.pi*ro)/(math.pi*(ro*ro-ri*ri))
    assert math.isclose(S*math.exp(rate*L)-S, fi-fo)
    # Matched wall line friction is the finite zero-rate limit.
    assert math.isclose(grain(.22,.15,K,L,ri,ro,S),
                        S*.22*2*math.pi*ri*K*L/(math.pi*(ro*ro-ri*ri)))
    # Brake work equals initial KE + gravitational work, zero gap limit.
    d = cut(2, .1, 0, .02, 1, .1)['stop_m']
    assert math.isclose(2*d, .5*.02*.1**2 + d)
    return dict(segment_force_errors_N=errs, finite_helix_work_check=True)


def main():
    out = {'checks': checks(), 'state': state_witness()}
    out['braid_nominal'] = {str(a): braid(.2,a,.02,.0015,.1,.00015)
                            for a in [30,45,55]}
    # Whole-bank material/friction bias, geometry bias and spring relaxation.
    # Corners are epistemic bounds, not samples or probabilities.
    cases = []
    for mu, angle, L, r, P, gap in itertools.product(
            [.1,.2,.3], [40,45,50], [.019,.021], [.0014,.0016],
            [.05,.15], [.00005,.00015,.00030]):
        b = braid(mu,angle,L,r,P,gap)
        cases.append(dict(mu=mu, angle=angle, L=L, r=r, P=P, gap=gap, **b))
    out['braid_grid'] = dict(cases=len(cases), down_range_N=[min(c['down_N'] for c in cases),max(c['down_N'] for c in cases)],
        up_range_N=[min(c['up_N'] for c in cases),max(c['up_N'] for c in cases)],
        positive_helix_radicand=sum(c['stroke_m'] is not None for c in cases),
        hold_release_counts={str(F):sum(c['down_N']>=F and c['stroke_m'] is not None for c in cases) for F in [1,10]})
    out['coherent_braid'] = {name:braid(*args) for name,args in {
        'weak':(.1,40,.019,.0016,.05,.00030),
        'nominal':(.2,45,.02,.0015,.1,.00015),
        'strong':(.3,50,.021,.0014,.15,.00005)}.items()}
    b=out['braid_nominal']['45']
    stroke=b['stroke_m']
    # Return spring stores energy; guide+bend resistance competes with it.
    out['return'] = {str(drag): dict(net_N=.1-drag,
        closure_s=math.sqrt(2*stroke*.001/(.1-drag)) if drag<.1 else None)
        for drag in [0,.05,.12]}
    out['opening_work_J'] = .1*stroke
    out['cuts'] = {str((F,delay,v)):cut(b['down_N'],b['up_N'],delay,.02,F,v)
        for F,delay,v in itertools.product([0,1,10],[.002,.010,.030],[-.1,.1])}
    out['upward_unloaded_coast_m'] = cut(b['down_N'],b['up_N'],.01,.02,0,-.1)
    out['partial_release'] = {str(c): .1*math.expm1(b['K']*c) for c in [1,.5,.25,0]}
    granular=[]
    for mu_i,mu_o,K,S,L,ri,ro in itertools.product([.1,.3],[.1,.3],[.2,.8],[.5,2,10],[.009,.011],[.0014,.0016],[.0021,.0023]):
        granular.append(grain(mu_i,mu_o,K,L,ri,ro,S))
    out['granular'] = dict(cases=len(granular),range_N=[min(granular),max(granular)],
        nominal_per_N=grain(.2,.2,.5,.01,.0015,.0022,1),
        pressure_required_Pa={str(F):F/(.2*2*math.pi*.0015*.01) for F in [1,10]},
        lost_set_cases={str(c):10000*max(.0002-c,0) for c in [0,.0001,.0002,.0003]})
    out['granular']['high_gain_example_N_per_N']=grain(.3,.1,.8,.011,.0016,.0021,1)
    out['bulk'] = dict(height_span_for_40mm_bed_m=.04*(.64/.55-1),
                       min_bed_for_40mm_span_m=.04/(.64/.55-1))
    out['laminate_interfaces']={str((F,p,mu)):math.ceil(F/(p*40e-6*mu))
        for F,p,mu in itertools.product([1,10],[50000,500000],[.1,.2,.3])}
    out['schedule_s'] = {str((H,v)):schedule(H,v) for H,v in itertools.product([80,160,320],[.1,.3])}
    out['min_heads'] = {str(v):next(H for H in range(1,6401) if schedule(H,v)<30) for v in [.1,.3]}
    out['joint_budget_head_dollars'] = {str((H,cell)):(250-6400*cell)/H for H,cell in itertools.product([160,320],[0,.01,.03])}
    out['braid_inventory'] = dict(sleeve_m=6400*.02,
        yarn_m_16_strands=6400*16*.02/math.cos(math.pi/4),
        annulus_grain_litres=6400*math.pi*(.0022**2-.0015**2)*.01*1000)
    if '--all' in sys.argv:out['all_braid_cases']=cases
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
