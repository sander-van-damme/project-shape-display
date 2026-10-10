#!/usr/bin/env python3
"""Finite capillary-accumulator bridge. mm, N, Pa unless specified.
Deterministic bounds, no probability/yield inference or hardware validation.
"""
from math import pi, cos, radians, tan, isclose
import json

H = 10*tan(radians(30))
GAMMA = .417  # N/m; clean Field's metal, NOT oxide constitutive law


def intersect(a, b):
    return max(0., min(a[1], b[1])-max(a[0], b[0]))


def box_intersection(a, b):
    v = 1.
    for x, y in zip(a, b):
        v *= intersect(x, y)
    return v


def pore_pressure(r, theta, gamma=GAMMA):
    # Liquid pressure above gas in a nonwetting circular tube.
    return -2*gamma*cos(radians(theta))/(r*1e-3)


def slit_entry(c, theta, gamma=GAMMA):
    # Parallel nonwetting walls: curvature across width neglected.
    return -2*gamma*cos(radians(theta))/(c*1e-3)


def geometry(e=0.):
    # q increases outwards, withdrawing dry jaw .5. Face remains wet.
    # Fixed cup x=-.65.. .9; solid wall .6.. .9; four bores extend to x=3.4.
    # Cup inside y,z +/-1.15; piston y,z +/-1; stem length 1.3; rear always crosses the lip at -.65.
    # Bores have radius .4, centers +/- .55. Exterior fixed envelope:
    # x[-.95,3.7], y,z[-1.45,1.45], in a layer below the rack.
    r=.4-e; side=2-2*e; A=side*side
    assert r>0 and side>0
    centers=[(y,z) for y in (-.55,.55) for z in (-.55,.55)]
    for y,z in centers:
        assert abs(y)+r<=side/2+1e-12 and abs(z)+r<=side/2+1e-12
    for i,(y,z) in enumerate(centers):
        for yy,zz in centers[i+1:]:
            assert (y-yy)**2+(z-zz)**2 >= (2*r)**2
    bore_area=len(centers)*pi*r*r
    # Fixed .3 perforated load wall plus 2.5-mm active meniscus stroke.
    return dict(A=A, bore_area=bore_area, bearing=A-bore_area,
                capacity=bore_area*2.5, centers=centers)


def case(e=.05, angles=(130.,145.), oxide=0., accel=10., mu=.02):
    cmin=.15-e; cmax=.15+e; rmin=.4-e; rmax=.4+e
    g=geometry(e)
    # Bounded volume allocation: nominal charge includes .5-mm bore penetration,
    # .3 fixed-wall bores, and all peripheral slots within hot sleeve.
    Amax=(2+2*e)**2
    slot=((2.3+2*e)**2-(2+2*e)**2)*1.25
    # Fixed nominal charge across the batch; this corner grows the piston/cup
    # together and shrinks pores. Slot-filled bound does not claim free-surface shape.
    charge=4*.6+4*pi*.4**2*(.3+.5)+(2.3**2-4)*1.25
    # +/-5% volume change and coherent maximum-area travel .5.
    needed=Amax*.5+2*.05*charge
    # rho bound and conservative effective acceleration across 4-mm hot pocket.
    disturbance=9000*(9.81+accel)*.004 + .5*9000*.01**2
    # Four fully molten tubes; maximum wetted length2.8; flow over .5s.
    Q=Amax*.5/.5*1e-9; r=rmin*1e-3; L=.0028
    viscous=8*mu*L*Q/(4*pi*r**4)
    pmin=pore_pressure(rmax,angles[0]); pmax=pore_pressure(rmin,angles[1])
    entry=slit_entry(cmax,angles[0])
    # Stronger than merely retaining liquid: positive return drive AND no spill.
    margin=min(pmin-disturbance-viscous,entry-pmax-disturbance-viscous)-oxide
    # Separate load-contact corner: pore growth/body shrinkage. Negative edge
    # land means full-hole subtraction is conservative, not a leakage proof.
    bearing=(2-2*e)**2-4*pi*rmax*rmax
    edge_land=(2-2*e)/2-(.55+rmax)
    initial_pores=charge-Amax*.6-slot-g['bore_area']*.3
    inventory_ok=(initial_pores-.05*charge>0 and
                  initial_pores+Amax*.5+.05*charge<g['capacity'])
    return dict(e=e,angles=angles,oxide_Pa=oxide,clearance=cmin,
                charge_mm3=charge,capacity_mm3=g['capacity'],needed_mm3=needed,
                bearing_mm2=bearing,stress_MPa=H/bearing if bearing>0 else None,
                edge_land_mm=edge_land,initial_pores_mm3=initial_pores,
                pore_min_Pa=pmin,pore_max_Pa=pmax,entry_Pa=entry,
                disturbance_Pa=disturbance,viscous_Pa=viscous,margin_Pa=margin,
                pass_necessary=cmin>0 and .1-e>0 and inventory_ok and margin>0)


def check():
    # Pressure independent force balance and SI work/volume equality.
    r=.0004; theta=140; p=pore_pressure(r*1000,theta)
    assert isclose(p*pi*r*r,-2*pi*r*GAMMA*cos(radians(theta)))
    A=4.; dq=.1
    assert isclose(p*A*1e-6*dq*1e-3,p*A*dq*1e-9)
    assert pore_pressure(.4,60)<0  # a wetting wick sucks rather than returns
    assert isclose(pore_pressure(.8,140),p/2)
    assert isclose(slit_entry(.15,90),0.,abs_tol=1e-10)
    # Explicit swept piston vs fixed wall, frozen core, and rear hot-lip coverage.
    frozen=((0.,.6),(-1.,1.),(-1.,1.))
    wall=((.6,.9),(-1.15,1.15),(-1.15,1.15))
    worst=0.
    for i in range(501):
        q=.5*i/500
        piston=((q-1.3,q),(-1.,1.),(-1.,1.))
        assert box_intersection(piston,wall)==0
        assert isclose(box_intersection(piston,frozen),4*q,abs_tol=1e-12)
        # Positive overlap at rear capillary lip throughout; no open rear bypass.
        assert q-1.3<-.65 and q<=.6
        worst=max(worst,box_intersection(piston,frozen))
        # Independent cavity-minus-solid integration matches front+slot formula.
        cavity=((- .65,.6),(-1.15,1.15),(-1.15,1.15))
        direct=1.25*2.3**2-box_intersection(piston,cavity)
        assert isclose(direct,4*(.6-q)+(2.3**2-4)*1.25)
    assert isclose(worst,2.)
    # Pore volume checked by independent midpoint integration of circular slices.
    errors=[]
    for n in (100,1000,10000):
        dr=.8/n
        area=sum(2*max(0,.4**2-(-.4+(i+.5)*dr)**2)**.5*dr for i in range(n))
        errors.append(abs(4*area*2.5-4*pi*.4**2*2.5))
    assert errors[2]<errors[1]<errors[0] and errors[2]<1e-5
    # Film transported from fixed lip(-.65) on .5 return reaches -1.15,
    # intersecting cold guide[-1.25,-.85]; return does not recover it while hot.
    assert intersect((-1.15,-.65),(-1.25,-.85))>.29
    # P*stroke*t thin-film bound, not Landau-Levich or a measured loss rate.
    carryout={str(t):8*.5*t for t in (0.,.01,.05,.15)}
    # Frozen film on stem and prior guide residue can close .1 minimum gap.
    blocked={str(t):2*t >= .15-.05 for t in (0.,.01,.05,.15)}
    assert blocked['0.05'] and not blocked['0.01']
    # Wetting wick competes with broad bridge suction; same wettable walls.
    wick=2*GAMMA*cos(radians(30))/(.1e-3)
    bridge=2*GAMMA*cos(radians(30))/(.6e-3)
    assert wick>bridge
    # Simple crossbolt: 1-mm jaw thickness, depth withdrawal1.15 leaves .15 gap.
    jaw_released=((.5,1.5),(0.,1.),(0.,1.))
    bolt_engaged=((1.,2.),(0.,1.),(0.,1.))
    bolt_withdrawn=((1.,2.),(0.,1.),(1.15,2.15))
    assert box_intersection(jaw_released,bolt_engaged)==.5
    assert box_intersection(jaw_released,bolt_withdrawn)==0
    return dict(volume_quadrature_errors_mm3=errors,frozen_sweep_mm3=worst,
                transported_film_mm3=carryout,frozen_slit_blocked=blocked,
                wick_suction_Pa=wick,bridge_suction_Pa=bridge)


if __name__=='__main__':
    rows=[case(e,a,ox) for e in (0.,.05,.15)
          for a in ((130.,145.),(110.,150.)) for ox in (0.,200.,1000.)]
    print(json.dumps({'checks':check(),'cases':rows,
        'budget_per_site_USD':{str(b):(500-b)/6400 for b in (150,250,350)},
        'handling_hours':{str(t):6400*t/3600 for t in (5,15,30)},
        'slow_motion_sensitivity':case(.05,(130.,145.),200.,accel=0.),
        'mechanical_nominal_stress_MPa':H},indent=2))
