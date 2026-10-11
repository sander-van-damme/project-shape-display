#!/usr/bin/env python3
"""Finite bayonet bearing / reciprocal cap screen. Units mm, N, MPa.

Deterministic bounds, not PLA/X1C priors. Equal normal stiffness is a
competing contact law, not a calibrated prediction. JSON is disposable.
"""
import importlib.util
import itertools
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    'guidance', Path(__file__).resolve().parents[1] / 'E-168/guidance.py')
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
b = g.b


def geometry(L, W, r, e=.05, d=4.6, c=.025):
    """Lug half-length/width, circular stem radius, square cap edge.

    Slot/pocket halfwidth W+.2; central half-aperture r+.2. Restrict W<=r,
    so two simple bearing rectangles remain at centered adverse size corner.
    Rotation cap/lug z-overlap is real: active lug [42.3,43.5], neighbor cap
    [42,44]. Finite polygon tests below independently reconstruct that case.
    """
    a = r+.2
    # Manufactured lug grows on both axes; cap half-edge and registration
    # each grow by e. Active writer centering is ideal beyond this e.
    cap_drift = c*(1+2*44/25)
    reciprocal = b.P-d/2-2*e-cap_drift-math.hypot(L+e, W+e)
    # Extend E-168's midheight necessary witness to the full rotating-cap
    # interval that can overlap a stationary stem (upper endpoint z=36.3).
    slope = 2*c/25
    cap_stem = (b.P-math.sqrt(2)*(d/2+e)-e
                -(r+e)*math.sqrt(1+slope*slope)-c*(1+2*36.3/25))
    # An aligned lug passes a stationary cap during long axial moves.
    axial_cap = b.P-d/2-L-3*e-cap_drift
    same_level = b.P-2*L-4*e-2*c*(1+2*41.2/25)
    # All lug rotations clear unchanged stems, including conservative drift
    # at the highest raised lug upper face (z=43.5).
    stem_lug = (b.P-math.hypot(L+e,W+e)-(r+e)*math.sqrt(1+slope*slope)-e
                -c*(1+2*43.5/25))
    active_diagonal = math.sqrt(2)*b.P-2*math.hypot(L+e,W+e)-2*e
    # Actual centered smaller lug, larger aperture/slot corner.
    land = L-e-(a+e)
    area = 4*max(0,W-e)*max(0,land)
    minimum_land = land-e
    return dict(L=L,W=W,r=r,d=d,e=e,area=area,
                mean_pressure=10/area if area else None,
                reciprocal_cap_margin=reciprocal,cap_stem_margin=cap_stem,
                axial_cap_margin=axial_cap,same_level_lug_margin=same_level,
                stem_lug_margin=stem_lug,active_diagonal_margin=active_diagonal,
                slot_margin=.2-3*e,minimum_land=minimum_land,
                admissible=(W<=r and area>0 and min(reciprocal,cap_stem,
                    axial_cap,same_level,stem_lug,active_diagonal,.2-3*e,
                    minimum_land)>0))


def search(step, d=4.6, r=1.48, e=.05):
    # Only one topology: not a count of independent mechanisms.
    candidates = survivors = 0
    best = None
    for i in range(math.ceil(1.8/step), math.floor(2.5/step)+1):
        for j in range(math.ceil(.45/step), math.floor(r/step)+1):
            row = geometry(i*step,j*step,r,e,d)
            candidates += 1
            if row['admissible']:
                survivors += 1
                if best is None or row['area'] > best['area']:
                    best = row
    return dict(step=step,candidates=candidates,survivors=survivors,best=best)


def relaxed_area_supremum(d=4.6,r=1.48,e=.05,c=.025):
    # Independent continuous optimization on the active reciprocal envelope.
    # Other gates are omitted: this bounds this rectangular W<=r encoding.
    # Strict positive clearance means the boundary maximum is a supremum.
    R = b.P-d/2-2*e-c*(1+2*44/25)
    B = r+.2+3*e
    lo,hi = .45+e,min(r+e,R)
    for _ in range(80):
        y = (lo+hi)/2
        x = math.sqrt(R*R-y*y)
        derivative = x-B-(y-2*e)*y/x
        if derivative>0:
            lo=y
        else:
            hi=y
    y=(lo+hi)/2
    x=math.sqrt(R*R-y*y)
    return dict(L=x-e,W=y-e,area_supremum=4*(y-2*e)*(x-B))


def extra_lug_volume(L,W,r):
    # L>r, W<r here; exact circular strip intersection avoids counting stem
    # material twice. Return added volume per 1.2-mm-thick lug, mm^3.
    assert L>r>W
    intersection=2*(W*math.sqrt(r*r-W*W)+r*r*math.asin(W/r))
    return 1.2*(4*L*W-intersection)


def reciprocal_witness(L,W,d=4.6,e=0,c=0,n=256):
    # Selected top=44, j=4 lug raised to [42.3,43.5].
    # Highest unchanged cap occupies nominal [42,44]. At z=42.9, its
    # exact horizontal section includes the entire in-plane square width,
    # even with slope -2c/25: vertical cap bounds are checked below.
    z,slope = 42.9,2*c/25
    angle = -math.atan(slope)
    for u in (-(d/2+e),d/2+e):
        local_z = (z-43+u*math.sin(angle))/math.cos(angle)
        assert abs(local_z)<1
    drift = c*(1+2*z/25)
    hx = (d/2+e)*math.sqrt(1+slope*slope)
    other = b.rectangle(hx,d/2+e,dx=b.P-e-drift)
    hits = sum(b.intersect(b.rectangle(L+e,W+e,math.pi*i/(2*n)),other)
               for i in range(n+1))
    angle = math.atan2(W+e,L+e)  # exact maximum x projection
    at_peak = b.intersect(b.rectangle(L+e,W+e,angle),other)
    margin = b.P-e-drift-hx-math.hypot(L+e,W+e)
    assert at_peak == (margin < -1e-9)
    return dict(samples=n+1,hits=hits,peak_collision=at_peak,margin=margin)


def paths(L,W,r,n):
    # Finite own ground and lower guide, reconstructed with widened slot.
    solids = b.gate(a=r+.2,s=W+.2,pocket=W+.2)
    solids += g.guide(-25,a=r+.2,slot=W+.2)
    checks = hits = 0
    for angle,shift in g.poses(n):
        for j in range(5):
            checks += 1
            hits += b.collisions(angle,shift+10*j,solids,L,W)
    assert hits == 0
    # Coherent in-plane manufacturing corners, both engaged and transit poses.
    corner_hits = 0
    for dx,dy,dL,dW,da,ds in itertools.product((-.05,.05),repeat=6):
        gate = b.gate(a=r+.2+da,s=W+.2+ds,pocket=W+.2+ds)
        corner_hits += bool(b.collisions(0,-.6,gate,L+dL,W+dW,dx,dy))
        corner_hits += bool(b.collisions(math.pi/2,.1,gate,L+dL,W+dW,dx,dy))
    assert corner_hits == 0
    return dict(lug_poses=checks,hits=hits,manufacturing_pose_cases=128,
                manufacturing_hits=corner_hits)


def bearing_patches(L,W,a,s,dx=0.,dy=0.):
    """Clip the seated lug footprint against actual generated base boxes."""
    lug = b.rectangle(L,W,math.pi/2,dx,dy)
    lx0,lx1 = min(x for x,y in lug),max(x for x,y in lug)
    ly0,ly1 = min(y for x,y in lug),max(y for x,y in lug)
    patches = []
    for poly,z0,z1 in b.gate(a=a,s=s,pocket=s):
        if z1 != 0:
            continue
        x0 = max(lx0,min(x for x,y in poly))
        x1 = min(lx1,max(x for x,y in poly))
        y0 = max(ly0,min(y for x,y in poly))
        y1 = min(ly1,max(y for x,y in poly))
        if x1>x0 and y1>y0:
            patches.append((x0,x1,y0,y1))
    return patches


def bearing_corners():
    areas = []
    for dx,dy,dL,dW,da,ds in itertools.product((-.05,.05),repeat=6):
        patches = bearing_patches(2.15+dL,1.2+dW,1.68+da,1.4+ds,dx,dy)
        area = sum((x1-x0)*(y1-y0) for x0,x1,y0,y1 in patches)
        areas.append(area)
        assert len(patches)==2 and area>0
    adverse = bearing_patches(2.1,1.15,1.73,1.45)
    area = sum((x1-x0)*(y1-y0) for x0,x1,y0,y1 in adverse)
    inertia = sum((x1**3-x0**3)/3*(y1-y0) for x0,x1,y0,y1 in adverse)
    assert abs(area-1.702)<1e-12
    assert abs(inertia-area*1.15**2/3)<1e-12
    assert abs(min(areas)-area)<1e-12
    return dict(corners=len(areas),area_min=min(areas),area_max=max(areas),
                adverse_patches=adverse,adverse_second_area_moment=inertia)


def contact(w, land, F, q):
    """Two flat wing rectangles: x in [-w,w], combined y-length 2*land.

    Downward resultant at (q,0). Equal local normal stiffness, rigid lug.
    A plane p=C*max(x-t,0) gives exact unilateral foundation solution.
    Full contact p=F/A+F*q*x/I. No lateral-guide couple is supplied here.
    """
    assert w>0 and land>0 and F>0 and q>=0
    A = 4*w*land
    if q>=w:
        return dict(q=q,finite_equilibrium=False,
                    guide_force_infimum=F*max(0,q-w)/25)
    if q <= w/3:
        peak = F/A*(1+3*q/w)
        low = F/A*(1-3*q/w)
        return dict(q=q,finite_equilibrium=True,contact_fraction=1.,
                    peak_MPa=peak,minimum_MPa=low)
    # For a triangular pressure on [t,w], centroid is (t+2w)/3.
    t = 3*q-2*w
    C = F/(land*(w-t)**2)
    # Exact independent force and moment integrals using u=x-t.
    force = 2*land*C*(w-t)**2/2
    moment = 2*land*C*((w-t)**3/3+t*(w-t)**2/2)
    assert abs(force-F)<1e-10 and abs(moment-F*q)<1e-10
    return dict(q=q,finite_equilibrium=True,contact_fraction=(w-t)/(2*w),
                peak_MPa=C*(w-t),minimum_MPa=0.)


def quadrature_contact(w,land,F,q,n):
    exact = contact(w,land,F,q)
    assert exact['finite_equilibrium']
    A = 4*w*land
    force = moment = 0.
    for i in range(n):
        x = -w+(i+.5)*2*w/n
        if q<=w/3:
            p = F/A*(1+3*q*x/w**2)
        else:
            t = 3*q-2*w
            p = F/(land*(w-t)**2)*max(x-t,0)
        force += p*2*land*2*w/n
        moment += x*p*2*land*2*w/n
    return dict(n=n,force_N=force,moment_Nmm=moment)


def main():
    witness = geometry(2.15,1.20,1.48)
    assert witness['admissible']
    # The enlarged bearing looks attractive but clips the stationary cap.
    bad = geometry(2.40,1.48,1.48)
    assert not bad['admissible'] and bad['reciprocal_cap_margin']<0
    original = geometry(2,.45,1.48)
    assert original['admissible']
    assert reciprocal_witness(2.4,1.48)['peak_collision']
    assert not reciprocal_witness(2.15,1.2,e=.05,c=.025)['peak_collision']
    assert geometry(2.25,1.3,1.48,c=0)['admissible']
    assert not geometry(2.25,1.3,1.48,c=.025)['admissible']
    assert reciprocal_witness(2.25,1.3,e=.05,c=.025)['peak_collision']
    # Off-grid analytic circular-envelope threshold, both sides.
    W,e,d = 1.3,.05,4.6
    limit = math.sqrt((b.P-d/2-2*e)**2-(W+e)**2)-e
    for delta in (-.001,.001):
        assert reciprocal_witness(limit+delta,W,e=e)['peak_collision']==(delta>0)
    w,land = 1.2-.05,2.15-1.48-.2-.1
    contact_rows = [contact(w,land,10,q) for q in (0,.3,.6,1.,1.14,1.15,2.3)]
    # Pressure doubles with force and halves with bearing length.
    assert abs(contact(w,land,20,.6)['peak_MPa']
               -2*contact(w,land,10,.6)['peak_MPa'])<1e-10
    assert abs(contact(w,2*land,10,.6)['peak_MPa']*2
               -contact(w,land,10,.6)['peak_MPa'])<1e-10
    holdouts = [quadrature_contact(w,land,10,.6,n) for n in (32,128,512)]
    assert abs(holdouts[-1]['moment_Nmm']-6)<.0001
    data = dict(witness=witness,rejected_wider=bad,original=original,
        reciprocal={name:{str(n):reciprocal_witness(L,W,e=e,c=c,n=n)
                          for n in (16,64,256)}
                    for name,L,W,e,c in [('wide_nominal',2.4,1.48,0,0),
                                       ('witness_adverse',2.15,1.2,.05,.025),
                                       ('omitted_tilt_control',2.25,1.3,.05,.025)]},
        paths={str(n):paths(2.15,1.2,1.48,n) for n in (16,64)},
        bearing_geometry=bearing_corners(),
        search_convergence=[search(s) for s in (.02,.01,.005)],
        continuous_area_bound=relaxed_area_supremum(),
        scenarios=[dict(d=d,r=r,e=e,search=search(.01,d,r,e))
                   for d,r,e in itertools.product((4.4,4.6,4.8),
                                                  (1.44,1.48,1.54),(.025,.05,.075))],
        contact=contact_rows,contact_quadrature=holdouts,
        elastic_upper_N={str(E):E*math.pi*(1.48-.05)**4/4*g.rayleigh()
                         for E in (1000,2000,3000)},
        cap_area_fraction={str(d):(d/b.P)**2 for d in (4.4,4.6,4.8)},
        added_lug_material_cm3=32000/1000*(extra_lug_volume(2.15,1.2,1.48)
                                         -extra_lug_volume(2,.45,1.48)))
    for row in data['search_convergence']:
        assert row['best']['area'] <= data['continuous_area_bound']['area_supremum']
    print(json.dumps(data,indent=2))


if __name__ == '__main__':
    main()
