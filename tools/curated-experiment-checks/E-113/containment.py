#!/usr/bin/env python3
"""LAB-210 bounded containment closure; mm, N, MPa, seconds.
No random sampling, constitutive fit, hardware qualification or generated output.
Two topologies only: backed rolling diaphragm and O-ring piston.
"""
from math import pi, sqrt, tan, radians, cos, sin, isclose
import json
import importlib.util
from pathlib import Path
spec = importlib.util.spec_from_file_location('e112', Path(__file__).parents[1]/'E-112/boundary.py')
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
H = 10*tan(radians(30))


def roll_volume(a, rho, stroke, q=0, h=.2):
    # Liquid ABOVE the U, roof T; piston and bore back the dry underside.
    b = a+2*rho
    T = stroke/2+h
    zc = (q-stroke/2-.2)/2
    return pi*b*b*T-pi*a*a*q-pi*(b*b-a*a)*zc+pi*pi*(a+rho)*rho*rho


def integrated_volume(a, rho, stroke, q, n):
    # Independent radial quadrature: roof minus liquid-facing floor.
    T=stroke/2+.2;zc=(q-stroke/2-.2)/2
    dr=2*rho/n
    return pi*a*a*(T-q)+sum(2*pi*r*(T-zc+sqrt(max(0,rho*rho-(r-a-rho)**2)))*dr
        for r in (a+(i+.5)*dr for i in range(n)))


def spring(stroke, preload=.03):
    # Explicit candidate, not a material specification: steel coil, 8 active,
    # 2 inactive turns, wire .08, mean diameter .8, G=70000 MPa.
    d,D,n,G=.08,.8,8,70000
    k=G*d**4/(8*D**3*n)
    solid=(n+2)*d
    # .1 residual gap at max compression; preload compression included.
    installed_min=solid+.1
    installed_max=installed_min+stroke
    free=installed_max+preload/k
    C=D/d;W=(4*C-1)/(4*C-4)+.615/C
    force_max=preload+k*stroke
    stress=W*8*force_max*D/(pi*d**3)
    return dict(k=k,preload=preload,force_max=force_max,installed_min=installed_min,
                installed_max=installed_max,free=free,outer_diameter=D+d,
                max_shear_MPa=stress)


def flow_dp(mu,Q,w=.8,h=.15,L=5.):
    # Q mm3/s, geometry mm -> SI then Pa -> MPa. Fully molten Newtonian only.
    if h<=0:return float('inf')
    w,h,L=w*1e-3,h*1e-3,L*1e-3
    correction=1-192*h/(pi**5*w)*sum(tan_h(n*pi*w/(2*h))/n**5 for n in range(1,100,2))
    return 12*mu*L*(Q*1e-9)/(w*h**3*correction)/1e6


def tan_h(x):
    from math import tanh
    return tanh(x)


def case(route='rolling',e=.05,eta=.05,stress=5.,seal_cs=.7,drag=0.):
    s=.45+e;core=sqrt(H/(pi*stress));rho=.2;t=.05
    # Main and reservoir on two levels, identical roof coordinate, center
    # separation chosen from outer radius. Roof ports enter at r=0; a straight
    # vertical duct in the fixed roof connects them, never crossed by pistons.
    if route=='rolling':
        am=core+t+2*e;ar=core+t
        Am,Ar=old.area(am,rho),old.area(ar,rho)
        vm=lambda S,q=0:roll_volume(am,rho,S,q)
        vr=lambda S,q=0:roll_volume(ar,rho,S,q)
        outer=max(am,ar)+2*rho+t+.3
        # Piston skirt reaches below fold at every state, r<=a-t.
        # Axial roof-to-deepest-fold plus .1 dry clearance; roof .3 + duct .2 + cover .3.
        envelope=lambda S:S+.2+.1+rho+t+.1+.8
        geometry='dry piston r<=a-t; bore r>=a+2rho+t'
    else:
        # .7-mm cross-section is a custom optimistic scenario, NOT catalog pass.
        # .15 land between load core and groove root; 15% radial squeeze.
        am=core+.15+.85*seal_cs+2*e;ar=core+.15+.85*seal_cs
        Am,Ar=pi*am*am,pi*ar*ar
        vm=lambda S,q=0:Am*(.2+S/2-q)
        vr=lambda S,q=0:Ar*(.2+S/2-q)
        outer=am+.3
        # groove width 1.3*d plus .2 land each side, full swept seal band.
        envelope=lambda S:S+.2+1.3*seal_cs+.4+.8
        geometry='cylindrical swept seal band; ports only through fixed roof'
    separation=2*outer+.4
    duct_area=.8*(.2-e)
    if duct_area<=0:raise ValueError('closed duct')
    path_length=separation+.6+(.2-e)
    # Exact union of a rectangular channel and two half-overlapping roof ports.
    duct_volume=duct_area*path_length
    # Roof channel occupies axial [.3,.3+h] above chamber roof; .3 cover.
    duct_path=[(0.,0.),(.3+(.2-e)/2,0.),(.3+(.2-e)/2,separation),(0.,separation)]
    assert .3+(.2-e)+.3 <= .8+1e-12
    Kr=vr(1)-vr(0)
    denominator=Ar-2*eta*Kr
    if denominator<=0:raise ValueError('accommodation feedback diverges')
    sr=(Am*s+2*eta*(vm(s)+vr(0)+duct_volume))/denominator
    V=vm(s)+vr(sr)+duct_volume
    sp=spring(sr,preload=.03+drag)
    pmin=(sp['preload']-drag)/Ar
    pmax=(sp['force_max']+drag)/Ar
    pressures=[]
    for mu in (.002,.02,1.):
        dp=flow_dp(mu,Am*s/.5,h=.2-e,L=path_length)
        pressures.append(dict(mu_Pas=mu,dp_MPa=dp,min_main_return_MPa=pmin-dp,
                              max_main_push_N=(pmax+dp)*Am+drag))
    # Non-nested package: at qmax the rod's spring seat is at the body's dry
    # edge; at qmin it extends Sr into the separate spring bay. Fixed ground
    # seat sits installed_max beyond that edge; rod/seat thickness omitted.
    # A remote spring/lever can escape, but is a changed placement/force path.
    axial=envelope(sr)+sp['installed_max']
    bay=5.08/2-1/2-.15
    return dict(route=route,error=e,volume_excursion=eta,solid_stress=stress,
                s=s,sr=sr,V=V,Am=Am,Ar=Ar,outer_diameter=2*outer,
                level_separation=separation,duct_volume=duct_volume,duct_path=duct_path,
                body_span=envelope(sr),spring=sp,total_span=axial,bay=bay,
                overrun=axial-bay,geometry=geometry,pressures=pressures,
                frozen_core_stress=H/(pi*core*core),
                liquid_load_pressure=H/Am,
                liquid_load_reservoir_displacement=max(0,(H*Ar/Am-sp['preload'])/sp['k']),
                hoop=old.hoop_excursion(ar,rho,sr) if route=='rolling' else None,
                eccentricity_ratio=e/(2*rho+2*t) if route=='rolling' else None,
                seal_squeeze_bounds=[.15-e/seal_cs,.15+e/seal_cs] if route!='rolling' else None)


def verify():
    errors=[]
    for n in (128,512,2048):
        errors.append(max(abs(integrated_volume(a,r,S,q,n)-roll_volume(a,r,S,q))
            for a,r,S,q in [(.73,.17,.83,.21),(1.41,.23,1.2,-.49)]))
    assert errors[2]<errors[1]<errors[0] and errors[2]<1e-4
    # Generated backed meridians: finite thickness dry face has rho+t,
    # r in [a-t,b+t]. Piston and bore extend below the complete fold sweep.
    for a,r,S in [(.73,.2,.51),(.66,.2,1.1)]:
        t=.05;T=S/2+.2;b=a+2*r
        for i in range(101):
            q=-S/2+S*i/100;zc=(q-S/2-.2)/2
            dry=[(a+r-(r+t)*cos(pi*j/128),zc-(r+t)*sin(pi*j/128)) for j in range(129)]
            assert all(a-t-1e-12<=R<=b+t+1e-12 for R,z in dry)
            assert min(z for R,z in dry)>=-S/2-.1-r-t-1e-12
            assert T-q>=.2-1e-12
            assert isclose(roll_volume(a,r,S,q)-roll_volume(a,r,S),-old.area(a,r)*q,abs_tol=1e-12)
        # Wet-above plus wet-below exactly partitions fixed cylinder height.
        B=S/2+.1+r+.1
        assert isclose(roll_volume(a,r,S)+old.volume(a,r,S),pi*b*b*(T+B),abs_tol=1e-12)
    for route in ('rolling','piston'):
        c=case(route)
        for i in range(101):
            q=-c['s']/2+c['s']*i/100
            for dv in (-.05*c['V'],0,.05*c['V']):
                qr=(-c['Am']*q-dv)/c['Ar']
                assert abs(qr)<=c['sr']/2+1e-10
                assert isclose(-c['Am']*q-c['Ar']*qr,dv,abs_tol=1e-12)
        # Roof channel is wholly outside the moving wet boundary; separate levels
        # keep full cylinders apart with .4 clearance. End ports are
        # included in the volume; unmodeled bend losses can raise flow loss.
        assert c['level_separation']-c['outer_diameter'] >= .4-1e-12
        # Independent axial slabs of the channel/port rectangle union.
        hd=.2-c['error'];D=c['level_separation']
        union_volume=.8*(.3*2*hd+hd*(D+hd))
        assert isclose(union_volume,c['duct_volume'])
        # Independent work/force ratio, and stored spring energy integral.
        Am,Ar=c['Am'],c['Ar'];F=.12;dx=.001;dr=Am/Ar*dx
        assert isclose(F/Ar*Am*dx,F*dr)
        sp=c['spring'];S=c['sr'];k=sp['k'];F0=sp['preload']
        numerical=sum((F0+k*S*(i+.5)/1000)*S/1000 for i in range(1000))
        assert isclose(numerical,F0*S+k*S*S/2)
    assert isclose(case('piston',e=0,eta=0)['sr'],.45)
    assert isclose(flow_dp(.02,1),10*flow_dp(.002,1))
    # Independent parallel-plate lower bound; finite sidewalls increase loss.
    assert flow_dp(.02,1)>12*.02*.005*1e-9/(.0008*.00015**3)/1e6
    assert flow_dp(1,1,h=0)==float('inf')
    # Mechanical crossbolt: 1x1 contact section; z withdrawal 1.15 clears
    # jaw's z=[-.5,.5] by .15. Jaw moves only after complete bolt clearance.
    for i in range(101):
        bolt_bottom=-.5+1.15*i/100
        if i==100:assert bolt_bottom>=.5+.15-1e-12
    # Liquid load greatly exceeds preload; extrapolated spring equilibria
    # lie outside their strokes, so report travel-stop failure, not that motion.
    assert all(case(r)['liquid_load_reservoir_displacement']>case(r)['sr'] for r in ('rolling','piston'))
    return dict(radial_quadrature_errors_mm3=errors,states_per_boundary=101,
                checks='volume closure, support envelopes, force-work, spring energy, flow limits')


if __name__=='__main__':
    rows=[case(route,e=e) for route in ('rolling','piston') for e in (0,.05,.15)]
    print(json.dumps(dict(evidence='bounded geometry and quasistatic necessary conditions',
        checks=verify(),cases=rows,
        piston_drag_cases=[case('piston',drag=f) for f in (.03,.3)],
        rolling_volume_cases=[case(eta=v) for v in (0,.1)],
        residual_boundary_dollars={str(reserve):(500-reserve)/12800 for reserve in (150,250,350)},
        boundary_assembly_hours={str(seconds):12800*seconds/3600 for seconds in (5,15,30)}),indent=2))
