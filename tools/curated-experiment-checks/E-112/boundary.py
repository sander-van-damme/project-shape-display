#!/usr/bin/env python3
"""Prescribed finite thermal-strut boundaries; mm, N, MPa. No material pass.

Deterministic generator, no random seed. Liquid-facing circular-U meridian;
finite wall extends toward the dry side. This is kinematics, not equilibrium.
"""
import argparse
from collections import Counter
from itertools import product
import json
from math import cos, sin, pi, sqrt, tan, radians, isclose

PITCH = 5.08


def shape(a, rho, stroke, q, n=256, margin=.1):
    """Fluid-facing meridian, inner to outer attachment, including legs."""
    b = a+2*rho
    straight = stroke/2+2*margin
    zc = (q-straight)/2
    return [(a, q), (a, zc)] + [
        (a+rho-rho*cos(pi*i/n), zc-rho*sin(pi*i/n))
        for i in range(1, n+1)] + [(b, 0.)]


def wall(a, rho, stroke, q, thickness, n=256):
    """Dry face of same wall; rho>thickness required (no offset cusp)."""
    straight = stroke/2+.2
    zc = (q-straight)/2
    return [(a+thickness, q), (a+thickness, zc)] + [
        (a+rho-(rho-thickness)*cos(pi*i/n),
         zc-(rho-thickness)*sin(pi*i/n)) for i in range(1, n+1)
    ] + [(a+2*rho-thickness, 0.)]


def area(a, rho):
    b = a+2*rho
    return pi*(a*a+b*b)/2


def volume(a, rho, stroke, q=0., clearance=.1):
    """Exact liquid volume below the U and cap, above a fixed base."""
    b = a+2*rho
    straight = stroke/2+.2
    base_depth = stroke/2+.1+rho+clearance
    zc = (q-straight)/2
    return (pi*b*b*base_depth+pi*a*a*q+pi*(b*b-a*a)*zc
            -pi*pi*(a+rho)*rho*rho)


def mesh_volume(a, rho, stroke, q, n):
    # Independent signed-frustum boundary integral: V=-integral pi*r^2 dz.
    B = stroke/2+.1+rho+.1
    curve = [(0., q)] + shape(a, rho, stroke, q, n) + [
        (a+2*rho, -B), (0., -B), (0., q)]
    return -sum(pi*(r*r+r*R+R*R)*(Z-z)/3
                for (r,z),(R,Z) in zip(curve, curve[1:]))


def material_radius(u, a, rho, stroke, q):
    inner_length = (q+stroke/2+.2)/2
    if u <= inner_length:
        return a
    if u >= inner_length+pi*rho:
        return a+2*rho
    return a+rho-rho*cos((u-inner_length)/rho)


def hoop_excursion(a, rho, stroke, n=4000):
    """Max circumference ratio at a material coordinate across full stroke.

    Meridian length conserved; this prescribed surface still changes hoop
    length. No reference prestrain, constitutive law or wrinkle suppression.
    """
    L = stroke/2+.2+pi*rho
    return max(material_radius(L*i/n,a,rho,stroke,-stroke/2) /
               material_radius(L*i/n,a,rho,stroke,stroke/2)-1
               for i in range(n+1))


def paired(a, rho, stroke, error, excursion=.05):
    """Adverse opposite-radius corner, free reservoir; no rigid equal-stroke link.

    Main a+error; reservoir a-error. Reservoir has both signs of +/-excursion
    liquid-volume allowance at every main-cap state. Volume feeds back into
    required travel; fixed point converges for excursion<1.
    """
    am, ar = a+error, a-error
    Am, Ar = area(am,rho), area(ar,rho)
    sr = stroke
    for _ in range(100):
        V = volume(am,rho,stroke,clearance=.1+error)+volume(ar,rho,sr,clearance=.1+error)+.32
        new = Am/Ar*stroke+2*excursion*V/Ar
        if abs(new-sr) < 1e-12:
            break
        sr = new
    else:
        raise AssertionError("reservoir iteration did not converge")
    return sr, V, Am, Ar


def candidate(stress, error, rho, thickness, rack, excursion):
    H = 10*tan(radians(30))
    a = sqrt(H/(pi*stress))+error
    s = .45+error
    sr,V,Am,Ar = paired(a,rho,s,error,excursion)
    # Capsules at separate vertical levels; no credit for sharing pitch.
    # Radial maximum corner + wall/flange (.3), not cap diameter alone.
    outer_radius = a+error+2*rho+.3
    width = 2*outer_radius
    # Rack centered at x=0. Capsule front starts at rack edge + .15.
    # Jaw withdrawal is cap stroke; .2 cap and .3 base wall included.
    # x-axis capsule extent B + q_max + cap + base = S+.1+rho+c+.5.
    span = max(s,sr)+.1+rho+(.1+error)+.5
    x_max = rack/2+.15+span
    failures=[]
    if rho <= thickness: failures.append('wall_offset_cusp')
    if 2*rho-2*thickness-2*error <= 1e-12: failures.append('fold_gap_closed')
    if width > PITCH: failures.append('transverse_pitch')
    if x_max > PITCH/2: failures.append('radial_side_bay')
    # Unconditional kinematic demand, not a pass against invented allowables.
    hoop = hoop_excursion(a-error,rho,sr,1000)
    return dict(stress_MPa=stress,error_mm=error,fold_radius_mm=rho,
                film_mm=thickness,rack_mm=rack,volume_excursion=excursion,
                core_radius_mm=a,main_stroke_mm=s,reservoir_stroke_mm=sr,
                liquid_mm3=V,transverse_width_mm=width,
                side_bay_overrun_mm=x_max-PITCH/2,
                max_hoop_excursion=hoop,
                flat_annulus_min_strain=sqrt(1+(sr/(4*rho))**2)-1,
                area_discrepancy_vs_midradius=Ar/(pi*(a-error+rho)**2)-1,
                bend_strain_scale=thickness/(2*rho),
                board_W_30s_at_half_J_mm3=V*6400*.5/30,
                effective_area_correction_vs_cap=Am/(pi*(a+error)**2)-1,
                failures=failures)


def jaw_gap(rack, engagement, withdrawal, lift, x):
    # Rack underside and jaw top have equal +30-degree slope in support.
    # The cap moves the jaw outward; lift is the collet's upward unloading.
    start = rack/2-engagement
    rack_z = tan(radians(30))*(x-start)+lift
    jaw_z = tan(radians(30))*(x-start-withdrawal)
    return rack_z-jaw_z


def verify():
    # Explicit dry-rack/jaw section states, including continuous withdrawal.
    # At q=0 surfaces share a finite .3-mm contact. Collet raises .1 mm;
    # throughout withdrawal the gap grows. Only then allow arbitrary z travel.
    for rack in (1., 1.5, 2.):
        for k in range(101):
            dx = .5*k/100
            left, right = rack/2-.3+dx, rack/2
            if left < right:
                for x in (left, (left+right)/2, right):
                    assert jaw_gap(rack,.3,dx,.1,x) >= .1-1e-12
            if k == 100:
                assert left >= rack/2+.15
        assert isclose(jaw_gap(rack,.3,0,0,rack/2-.15),0.)
    errors=[]
    for n in (32,128,512):
        errors.append(max(abs(mesh_volume(a,r,s,q,n)-volume(a,r,s,q))
                          for a,r,s,q in [(1.371,.17,.673,-.219),(.63,.29,.91,.413)]))
    assert errors[2]<errors[1]<errors[0] and errors[2]<2e-5
    for a,r,s in [(1.37,.2,.5),(.65,.15,.8)]:
        for i in range(101):
            q=-s/2+s*i/100
            points=shape(a,r,s,q)
            assert min(z for _,z in points)>=-(s/2+.1+r)-1e-12
            assert isclose(volume(a,r,s,q)-volume(a,r,s,0),area(a,r)*q,abs_tol=1e-12)
            assert isclose(volume(a,r,s,q)+volume(a,r,s,-q),2*volume(a,r,s),abs_tol=1e-12)
            straight=s/2+.2
            li=(q+straight)/2;lo=(straight-q)/2
            assert min(li,lo)>=.1-1e-12
            assert isclose(li+lo+pi*r,straight+pi*r)
            wf=wall(a,r,s,q,.025)
            assert all(a<=R<=a+2*r for R,_ in wf)
        sr,V,Am,Ar=paired(a,r,s,.05)
        constant = volume(a+.05,r,s,clearance=.15)+volume(a-.05,r,0,clearance=.15)+.32
        closed_form = (Am/Ar*s+.1*constant/Ar)/.95
        assert isclose(sr,closed_form,abs_tol=1e-10)
        for q in (-s/2,0,s/2):
            for dv in (-.05*V,.05*V):
                qr=(-Am*q+dv)/Ar
                assert abs(qr)<=sr/2+1e-10
        assert isclose(area(a,r)-pi*(a+r)**2,pi*r*r,abs_tol=1e-12)
    convergence=[hoop_excursion(.65,.15,.813,n) for n in (500,2000,8000)]
    assert max(convergence)-min(convergence)<1e-5
    # Equal chambers and zero excursion reduce exactly to opposed equal stroke.
    assert isclose(paired(1,.2,.5,0,0)[0],.5)
    assert hoop_excursion(1,.2,0)==0
    # Explicit fault corners: high error blocks the dry gap; thick film cusps.
    assert 'fold_gap_closed' in candidate(5,.15,.1,.05,1,.05)['failures']
    assert 'wall_offset_cusp' in candidate(5,0,.1,.15,1,.05)['failures']
    return dict(volume_errors_mm3=errors,hoop_refinement=convergence)


def main():
    p=argparse.ArgumentParser();p.add_argument('--all',action='store_true');args=p.parse_args()
    checks=verify()
    rows=[candidate(*x) for x in product((1,5),(0,.05,.15),(.1,.2,.3),
           (.025,.05,.1),(1,1.5,2),(0,.05,.1))]
    examples=[candidate(5,e,.2,.05,w,.05) for e,w in product((0,.05,.15),(1,2))]
    survivors=[r for r in rows if not r['failures']]
    print(json.dumps(dict(evidence='prescribed geometry and bounded scenarios only',
        checks=checks,cases=len(rows),not_rejected=len(survivors),
        rejection_counts=Counter(f for r in rows for f in r['failures']),
        not_rejected_by_error=Counter(r['error_mm'] for r in survivors),
        examples=examples,
        least_inventory=min(survivors,key=lambda r:r['liquid_mm3']) if survivors else None,
        rows=rows if args.all else None),indent=2))

if __name__=='__main__': main()
