#!/usr/bin/env python3
"""E-283 stock mass consequence using E-262's conditional linear beam.

No calibrated stiffness, friction, load population or lateral participation.
JSON stdout is reproducible output, not a physical measurement.
"""
import importlib.util
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    'stability', Path(__file__).resolve().parents[1]/'E-262/stability.py')
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)
G = 9.81


def bodies():
    # E-283 nominal tube plus explicit 2-g cap/nut/join allowance.
    # E-277 open-channel geometry + SOLID nut envelope (bore not deducted).
    # Density assumptions, not measured parts; screw mass stays in beam model.
    return {'printed_channel': (124*23.44+2*10.3**2+10*10.3**2)*1.24/1e6,
            'aluminium_stock': 124*(10**2-8**2)*2.7/1e6+.002}


def torque(force, mu, angle):
    mean, lead = 2.3, 3.
    lam = math.atan(lead/(math.pi*mean))
    wedge = math.sqrt(1+(math.cos(lam)*math.tan(math.radians(angle/2)))**2)
    eff = mu*wedge
    return dict(raise_Nmm=force*mean/2*(math.tan(lam)+eff)/(1-eff*math.tan(lam)),
                lower_Nmm=force*mean/2*(eff-math.tan(lam))/(1+eff*math.tan(lam)),
                hold_mu_threshold=math.tan(lam)/wedge)


def rows():
    result=[]
    for body,mass in bodies().items():
        for payload in (0., .2):
            total_mass=mass+payload/G
            for support,kw in {
                'fixed_no_nut':dict(base='fixed',kn=0.),
                'ideal_point_nut':dict(base='pinned',kn=math.inf),
                'soft_nut':dict(base='spring',ktheta=10.,kn=.1),
                'stiffer_nut':dict(base='spring',ktheta=10.,kn=1.)}.items():
                # Zero/full translational lump are allocation scenarios, not
                # bounds on a long column's rotational inertia/contact modes.
                for fraction in (0.,1.) if support in ('soft_nut','stiffer_nut') else (0.,):
                    result.append(dict(body=body,payload_N=payload,P_N=total_mass*G,
                        support=support,lump_fraction=fraction,
                        **s.scan(S=50,step=1,P=total_mass*G,nut_mass=fraction*total_mass,**kw)))
    return result


def checks():
    mass=bodies()['aluminium_stock']
    assert math.isclose((mass-.002)*1024,12.3420672)
    assert bodies()['printed_channel'] < mass
    # Recover E-277 torque anchor and force-triangle formula independently.
    assert math.isclose(torque(.2,.3,90)['raise_Nmm'],.228,abs_tol=.0005)
    for angle in (30,90):
        for mu in (.1,.3,.5):
            a=torque(.2,mu,angle); b=torque(.4,mu,angle)
            assert math.isclose(b['raise_Nmm'],2*a['raise_Nmm'])
            assert (a['lower_Nmm']>=0)==(mu>=a['hold_mu_threshold'])
            lam=math.atan(3/(math.pi*2.3))
            wedge=math.sqrt(1+(math.cos(lam)*math.tan(math.radians(angle/2)))**2)
            assert math.isclose(a['raise_Nmm'],.2*1.15*math.tan(lam+math.atan(mu*wedge)))
        assert abs(torque(.2,torque(.2,.3,angle)['hold_mu_threshold'],angle)['lower_Nmm'])<1e-15
    # A physically unchanged beam with heavier payload must not gain frequency.
    errors=[]
    for x in (7,32,57):
        kw=dict(x=x,base='spring',ktheta=10.,kn=.1)
        light=s.mode(P=.2,nut_mass=.02,**kw)['rpm']
        heavy=s.mode(P=mass*G+.2,nut_mass=mass+.2/G,**kw)['rpm']
        assert heavy<light
        fine=s.mode(P=mass*G+.2,nut_mass=mass+.2/G,elements=80,**kw)['rpm']
        errors.append(abs(heavy-fine)/max(1,fine))
        assert errors[-1]<.0002
    # Simple pinned compressed segment SI and N-mm Euler calculations agree.
    pc=math.pi**2*1e9*(math.pi*.0014**4/64)/.057**2
    assert math.isclose(pc,math.pi**2*1000*(math.pi*1.4**4/64)/57**2)
    return dict(max_40_to_80_relative_error=max(errors),pinned57mm_Pcr_N=pc)


if __name__=='__main__':
    out=dict(verification=checks(),moving_body_kg=bodies(),scans=rows(),
        torque=[dict(body=b,payload_N=p,extra_upward_drag_N=d,mu=mu,angle=angle,
                     **torque(m*G+p+d,mu,angle))
                for b,m in bodies().items() for p in (0.,.2) for d in (0.,.1)
                for mu in (.1,.3,.5) for angle in (30,90)])
    print(json.dumps(out,indent=2))
