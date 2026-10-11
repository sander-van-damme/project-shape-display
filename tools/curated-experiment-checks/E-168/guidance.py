#!/usr/bin/env python3
"""E-168: finite slotted guides and optimistic bayonet load envelope; mm,N,MPa.

Deterministic uncertainty bounds, not measured PLA/X1C distributions.
Retains E-167 polygon primitives; no third-party dependencies.
"""
import importlib.util
import itertools
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "bayonet", Path(__file__).resolve().parents[1] / "E-167/probe.py")
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)


def guide(z, a=1.6, slot=.65):
    """Six finite blocks: central square plus full-width horizontal slot."""
    return [(p, lo+z+.6, hi+z+.6)
            for p, lo, hi in b.gate(a=a, s=slot) if hi <= 0]


def poses(n):
    for old, new in itertools.permutations(range(5), 2):
        for i in range(n+1):
            t = i/n
            yield math.pi/2, -10*old+2.3*t
            yield math.pi/2*(1-t), -10*old+2.3
            yield 0, -10*(old+(new-old)*t)+2.3
            yield math.pi/2*t, -10*new+2.3
            yield math.pi/2, -10*new+2.3*(1-t)


def finite_guides(n):
    # Modified r=1.4 stem, enlarged a=1.6 gate, one lower slotted guide.
    solids = b.gate(a=1.6) + guide(-25)
    checks = hits = 0
    for angle, shift in poses(n):
        # Circle lies in central square at all angles; finite axial overlap.
        assert 1.4 < 1.6
        assert -30+shift < -25.6 and 42+shift > 0
        cap = b.rectangle(2.4, 2.4, angle)
        for poly, lo, hi in solids:
            if min(44+shift, hi) > max(42+shift, lo)+1e-9:
                hits += b.intersect(cap, poly)
        for j in range(5):
            hits += b.collisions(angle, shift+10*j, solids)
            checks += 1
    assert hits == 0
    # Phase-blind guide at -20 clips a 90-degree lug during initial lift.
    bad = b.collisions(math.pi/2, -20, guide(-20))
    assert bad > 0
    # A stem-fitting upper guide at z=12 meets the cap at the low-to-high move.
    cap = b.rectangle(2.4, 2.4)
    cap_hits = sum(b.intersect(cap, poly) for poly, lo, hi in guide(12)
                   if min(13, hi) > max(11, lo))
    assert cap_hits > 0
    return dict(lug_poses=checks, collisions=hits,
                wrong_phase_guide_hits=bad, upper_guide_cap_hits=cap_hits)


def segments(rigid_lugs=True):
    # Extremely favorable clamp at z=2, load at cap underside z=42.
    # Actual ground support at z=0 and cap top at z=44 can only worsen this
    # bound within this no-upper-brace linear elastic model.
    if not rigid_lugs:
        return [(2., 42., False)]
    result = []
    z = 2.
    for lo in (10., 20., 30., 40.):
        result += [(z, lo, False), (lo, lo+1.2, True)]
        z = lo+1.2
    result.append((z, 42., False))
    return result


def rayleigh(n=None, rigid_lugs=True):
    """Pcr <= EI*quotient using theta=sin(pi*s/(2*Lf)).

    s measures cumulative flexible length; theta is constant through lugs.
    Thus lug bending energy is zero even if lugs are infinitely stiff.
    Integral theta'^2 / integral theta^2 is a Rayleigh upper bound, not a
    critical-load prediction. Exact piecewise integrals or midpoint holdout.
    """
    seg = segments(rigid_lugs)
    flex = sum(hi-lo for lo, hi, rigid in seg if not rigid)
    s = numerator = denominator = 0.
    for lo, hi, rigid in seg:
        length = hi-lo
        if n is None:
            if rigid:
                denominator += length*math.sin(math.pi*s/(2*flex))**2
            else:
                wave = flex/(2*math.pi)*(math.sin(math.pi*(s+length)/flex)
                                           - math.sin(math.pi*s/flex))
                denominator += length/2-wave
                numerator += (math.pi/(2*flex))**2*(length/2+wave)
        else:
            for j in range(n):
                x = s if rigid else s+length*(j+.5)/n
                denominator += math.sin(math.pi*x/(2*flex))**2*length/n
                if not rigid:
                    numerator += (math.pi/(2*flex)*math.cos(
                        math.pi*x/(2*flex)))**2*length/n
        if not rigid:
            s += length
    return numerator/denominator


def envelope(E, e, c, d=4.8, force=10.):
    # Perfectly centered rotating cap at midpoint z=35.3 (selected level 1).
    # Unchanged neighbor at highest level: stem runs through this height.
    # Effective residual center play +/-c at gate z=0 and guide z=-25.
    # Adverse opposite contacts give straight-axis displacement D at z=35.3.
    drift = c*(1+2*35.3/25)
    # Cap half-edge +e; shaft radius +e; relative center registration +e.
    r_max = b.P-math.sqrt(2)*(d/2+e)-2*e-drift
    # A different allowed manufacturing corner has radius r_nominal-e.
    # Robust population requirement must satisfy both, not conflate them.
    r_small = max(0, r_max-e)
    q = rayleigh()
    upper = E*math.pi*r_small**4/4*q
    r_need = (force/(E*math.pi/4*q))**.25+e
    d_max = 2*((b.P-2*e-drift-r_need)/math.sqrt(2)-e)
    land = 2-(r_need+.2)-3*e  # minimum individual wing, includes offset
    # Separate centered corner: both lug ends shrink and both aperture edges
    # grow. Translation cannot shorten both wings at once. Actual area here
    # yields a pressure floor for r>=r_need, not a conservative-area fiction.
    centered_land = 2-(r_need+.2)-2*e
    area = 4*max(0, .45-e)*max(0, centered_land)
    return dict(E_MPa=E, edge_bound=e, residual_play=c,
                neighbor_axis_drift=drift, nominal_radius_max=r_max,
                buckling_upper_N=upper, necessary_radius_for_10N=r_need,
                cap_width_max_for_10N=d_max,
                minimum_single_wing_land_at_needed_radius=land,
                centered_adverse_wing_land=centered_land,
                bearing_stress_floor_MPa=(force/area if area else None))


def tilted_witness(n):
    """Actual rigid tilted cylinder vs 45-degree square prism at z=35.3.

    c=.025 after form/sleeve-length allowances; e=.05 opposite manufacturing
    edges. Sample an exact horizontal ellipse section of tilted cylinder.
    Inscribed polygon intersection gives a positive-volume collision witness.
    """
    e, c, radius, z = .05, .025, 1.4, 35.3
    slope = -2*c/25
    center = b.P-c+slope*z-e
    # Cylinder radius is measured normal to its axis.
    rx, ry = (radius+e)*math.sqrt(1+slope*slope), radius+e
    cylinder = [(center+rx*math.cos(2*math.pi*j/n),
                 ry*math.sin(2*math.pi*j/n)) for j in range(n)]
    cap = b.rectangle(2.4+e, 2.4+e, math.pi/4)
    overlap = b.intersect(cylinder, cap)
    # This r=1.4 case is near-clear; r=1.45 supplies a failing holdout.
    fail_radius = 1.45+e
    failed = [(center+fail_radius*math.sqrt(1+slope*slope)*math.cos(2*math.pi*j/n),
               fail_radius*math.sin(2*math.pi*j/n)) for j in range(n)]
    assert not overlap and b.intersect(failed, cap)
    return dict(vertices=n, r14_collision=overlap, r145_collision=True,
                r145_axis_penetration=(2.45*math.sqrt(2)
                       -(center-fail_radius*math.sqrt(1+slope*slope))))


def main():
    q = rayleigh()
    assert abs(rayleigh(rigid_lugs=False)-math.pi**2/(4*40**2)) < 1e-16
    convergence = [dict(steps_per_segment=n, quotient=rayleigh(n))
                   for n in (16, 64, 256)]
    assert abs(convergence[-1]['quotient']/q-1) < 1e-6
    # Scaling and robustness controls: halved E halves bound; radius^4.
    assert abs(envelope(1000,.05,.025)['buckling_upper_N']*2
               -envelope(2000,.05,.025)['buckling_upper_N']) < 1e-12
    rows = [envelope(E,e,c) for E,e,c in itertools.product(
        (1000,2000,3000),(0,.025,.05,.1),(0,.025,.05))]
    target = envelope(2000,.05,.025)
    assert target['buckling_upper_N'] < 10
    assert envelope(2000,.05,0)['buckling_upper_N'] > 10
    print(json.dumps(dict(
        finite_guides={str(n):finite_guides(n) for n in (16,64,256)},
        tilted_sections=[tilted_witness(n) for n in (32,128,512)],
        rayleigh_quotient=q,
        rigid_lug_factor=q/(math.pi**2/(4*40**2)),
        integration_holdouts=convergence,
        bounded_scenarios=rows,
        narrowed_cap=envelope(2000,.05,.025,d=4.6),
        target=target,
        inventory=dict(columns=6400,lugs=32000,ground_gates=6400,
                       lower_guide_sites=6400,minimum_stem_length_mm=72,
                       foot_top_range_mm=[-70,-27.7])), indent=2))


if __name__ == '__main__':
    main()
