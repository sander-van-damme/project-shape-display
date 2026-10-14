#!/usr/bin/env python3
"""Continuous perforated sheets, ideal strip statics and replication only.
mm/N/MPa; assumed metal properties and loads, no hardware qualification.
Run with --check for quadrature, limiting-case and accounting controls.
"""
import argparse
import json
from math import isclose, pi, sin

E = 70000.
RHO = 2.7e-6  # kg/mm3, assumed aluminium-like metal
H = 176.


def midpoint(n, p, hole, t, force, axis, steps=32768):
    """Independent strips: ignore transverse plate load sharing.
    Simply supported at active-field edges; constant minimum section is also
    returned as a cross-check, not a guaranteed real-plate upper bound.
    """
    L = n*p
    points = [(i+.5)*p for i in range(n)]
    def inertia(cut):
        if axis == 'lateral':
            return t*(p**3-(hole**3 if cut else 0))/12
        return (p-(hole if cut else 0))*t**3/12
    result = 0.
    dx = L/steps
    # All same-sign equal loads: symmetric end reactions.
    for k in range(steps):
        x = (k+.5)*dx
        j = min(n-1, int(x/p))
        cut = abs(x-points[j]) < hole/2
        # Closed sum of previous cell loads, including current point if passed.
        count = min(n, max(0, int(x/p+.5)))
        M = force*n*x/2 - force*(count*x-p*count*count/2)
        result += M*min(x,L-x)/2/(E*inertia(cut))*dx
    weights = sum(min(a,L-a)*(3*L*L-4*min(a,L-a)**2) for a in points)
    lower = force*weights/(48*E*inertia(False))
    upper = force*weights/(48*E*inertia(True))
    return result, lower, upper


def solid_plate(n,p,t,force,terms=61):
    """Unperforated simply-supported square plate under uniform pressure.
    Favorable stiffness control, NOT a qualified bound on local hole motion.
    Navier expansion of D*laplacian(laplacian(w))=q.
    """
    L=n*p
    D=E*t**3/(12*(1-.33**2))
    q=n*n*force/L**2
    series=sum(sin(m*pi/2)*sin(k*pi/2)/(m*k*(m*m+k*k)**2)
               for m in range(1,terms+1,2) for k in range(1,terms+1,2))
    return 16*q*L**4/(pi**6*D)*series


def scenario(n,p,a,t):
    L=n*p
    guide=midpoint(n,p,a,t,.05,'lateral')[0]
    drag=midpoint(n,p,a,t,.02,'vertical')[0]
    # Circular journal holes are replaced by equal-width square cuts for the
    # strip stiffness screen, but exact circles used for material accounting.
    bed=midpoint(n,p,3.6,t,.338,'vertical')[0]
    G=E/(2*(1+.33))
    lateral=2*n*n*.05
    shell=lateral*H**3/(3*E*(2*.8*L**3/12))+lateral*H/(2*G*.8*L)
    guide_mass=2*(L*L-n*n*a*a)*t*RHO
    bed_mass=(L*L-n*n*pi*3.6**2/4)*t*RHO
    shell_mass=4*L*H*.8*RHO
    own_force=.06+bed_mass*9.81/(n*n)
    diagnostic_force=.338+bed_mass*9.81/(n*n)
    # Minimum continuous seams, NOT individual fasteners or achieved assembly.
    paths=3*4+4  # three sheet perimeters + four shell corner seams
    path_m=(12*L+4*H)/1000
    cut_m=(2*n*n*4*a+n*n*pi*3.6)/1000
    return dict(cells=n*n,pitch=p,guide_opening=a,thickness=t,
                lateral_guide_mm=guide,shell_mm=shell,lateral_sum_mm=guide+shell,
                full_drag_guide_mm=drag,full_diagnostic_bed_mm=bed*diagnostic_force/.338,
                own_weight_bed_strip_mm=bed*own_force/.338,
                solid_diagnostic_bed_mm=solid_plate(n,p,t,diagnostic_force),
                solid_own_weight_bed_mm=solid_plate(n,p,t,own_force),
                field_metal_kg=guide_mass+bed_mass+shell_mass,
                guide_pair_kg=guide_mass,bed_kg=bed_mass,shell_kg=shell_mass,
                perimeter_connection_paths=paths,connection_length_m=path_m,
                aperture_cut_length_m=cut_m,apertures=3*n*n,
                cleanup_hours_5_20s=[3*n*n*s/3600 for s in (5,20)])


def check():
    for n,p,a in [(32,12.7,10.8),(64,6.35,4.64),(80,5.08,4.64)]:
        for axis in ['lateral','vertical']:
            r,lo,hi=midpoint(n,p,a,3,.05,axis)
            r2=midpoint(n,p,a,3,.05,axis,65536)[0]
            assert lo<r<hi
            assert abs(r-r2)/r<.002
            assert isclose(midpoint(n,p,a,3,.1,axis)[0],2*r)
            scale=2 if axis=='lateral' else 8
            assert isclose(midpoint(n,p,a,6,.05,axis)[0],r/scale)
        assert isclose(solid_plate(n,p,3,.338),solid_plate(n,p,3,.338,121),rel_tol=1e-7)
        assert isclose(solid_plate(n,p,6,.338)*8,solid_plate(n,p,3,.338))
        # No holes: exact uniform beam, one central point load.
        r,lo,hi=midpoint(1,p,0,3,1,'vertical')
        exact=p**3/(48*E*(p*3**3/12))
        assert isclose(r,exact,rel_tol=1e-8) and isclose(lo,hi)
        s=scenario(n,p,a,3)
        assert s['apertures']==3*n*n
        assert s['field_metal_kg']>s['bed_kg']>0
        assert isclose(s['connection_length_m'],5.5808)
    print('PASS: section brackets, quadrature, force/thickness scaling, central-load identity, ledger')


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--check',action='store_true')
    args=ap.parse_args()
    if args.check:
        check()
    else:
        print(json.dumps([scenario(n,p,a,t) for n,p,a in
             [(32,12.7,10.8),(64,6.35,4.64),(80,5.08,4.64)]
             for t in [3,6]],indent=2))
