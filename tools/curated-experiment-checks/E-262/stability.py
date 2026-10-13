#!/usr/bin/env python3
"""E-262: bounded Euler-Bernoulli lateral modes, not rotor/contact qualification.
Requires numpy. SI internally. JSON stdout is disposable. No fitted priors.
"""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import numpy as np


def analytic(length_mm, root_mm=1.4, mass_d_mm=3.2, E_MPa=1000,
             rho=1400, beta=1.875104068712):
    L, d, dm = length_mm/1000, root_mm/1000, mass_d_mm/1000
    return 60/(2*math.pi)*beta**2/L**2*math.sqrt(
        E_MPa*1e6*(math.pi*d**4/64)/(rho*math.pi*dm**2/4))


def matrices(L_mm, x_mm, root=1.4, mass_d=3.2, E=1000, rho=1400,
             P=0., elements=40, nut_mass=0.):
    """Consistent mass; conservative dead compression only below nut station.

    Cubic Hermite w/theta beam elements, positive geometric stiffness subtracted
    for compression. Extra node at nut makes load/support split exact. Nut mass
    is a lateral lump, separate from axial P. No gyro, rotary inertia or damping.
    """
    L, x = L_mm/1000, x_mm/1000
    grid = np.linspace(0,L,elements+1)
    nodes = np.sort(np.r_[grid[abs(grid-x)>1e-10], x])
    assert np.min(np.diff(nodes)) > 1e-10
    j = int(np.argmin(abs(nodes-x)))
    nd = 2*len(nodes)
    K, M = np.zeros((nd,nd)), np.zeros((nd,nd))
    EI = E*1e6*math.pi*(root/1000)**4/64
    mu = rho*math.pi*(mass_d/1000)**2/4
    for i, h in enumerate(np.diff(nodes)):
        ke = EI/h**3*np.array([[12,6*h,-12,6*h],[6*h,4*h*h,-6*h,2*h*h],
                               [-12,-6*h,12,-6*h],[6*h,2*h*h,-6*h,4*h*h]])
        me = mu*h/420*np.array([[156,22*h,54,-13*h],[22*h,4*h*h,13*h,-3*h*h],
                                [54,13*h,156,-22*h],[-13*h,-3*h*h,-22*h,4*h*h]])
        if nodes[i+1] <= x+1e-12:
            ke -= P/(30*h)*np.array([[36,3*h,-36,3*h],[3*h,4*h*h,-3*h,-h*h],
                                     [-36,-3*h,36,-3*h],[3*h,-h*h,-3*h,4*h*h]])
        ix = np.arange(2*i,2*i+4)
        K[np.ix_(ix,ix)] += ke
        M[np.ix_(ix,ix)] += me
    M[2*j,2*j] += nut_mass
    return K,M,j


def mode(L=64, x=7, base='fixed', kn=0., ktheta=0., nut_fixed=False,
         tip=False, **kw):
    """Base transverse translation fixed; base slope fixed/pinned/spring.

    kn: bilateral nut-to-ground tangent stiffness N/mm (inf = ideal guide).
    ktheta: base slope spring N mm/rad. nut_fixed additionally fixes nut slope.
    A real clearance/contact nut may have ZERO tangent stiffness until contact.
    """
    K,M,j = matrices(L,x,**kw)
    remove = {0}
    if base == 'fixed': remove.add(1)
    elif base == 'spring': K[1,1] += ktheta/1000
    elif base != 'pinned': raise ValueError(base)
    if math.isinf(kn): remove.add(2*j)
    else: K[2*j,2*j] += kn*1000
    if nut_fixed: remove.add(2*j+1)
    if tip: remove.add(len(K)-2)
    keep = sorted(set(range(len(K)))-remove)
    K,M = K[np.ix_(keep,keep)],M[np.ix_(keep,keep)]
    # Whiten generalized symmetric eigenproblem without scipy.
    C = np.linalg.cholesky(M)
    B = np.linalg.solve(C,K)
    B = np.linalg.solve(C,B.T).T
    lam = float(np.linalg.eigvalsh((B+B.T)/2)[0])
    rpm = 60/(2*math.pi)*math.sqrt(max(0,lam))
    return dict(rpm=rpm, screen_rpm=.8*rpm, stable=lam>1e-4)


def scan(S=50, step=2, station=7, **kw):
    values = [(float(u), mode(L=S+14,x=station+u,**kw)) for u in np.arange(0,S+.01,step)]
    u,v = min(values,key=lambda p:p[1]['rpm'])
    return dict(min_screen_rpm=v['screen_rpm'], at_u_mm=u,
                all_stable=all(v['stable'] for _,v in values),
                retracted_screen_rpm=values[0][1]['screen_rpm'],
                extended_screen_rpm=values[-1][1]['screen_rpm'])


def checks():
    for L in (54,64):
        for beta, settings in ((1.875104068712,{}),(math.pi,dict(base='pinned',tip=True)),
                               (3.926602312048,dict(tip=True))):
            ref = analytic(L,beta=beta)
            got = mode(L=L,x=L,**settings)['rpm']
            assert math.isclose(got,ref,rel_tol=2e-5),(got,ref)
    for x in (7,27,47):
        assert math.isclose(mode(L=54,x=x)['rpm'],analytic(54),rel_tol=2e-5)
    assert mode(base='pinned')['rpm'] < .2 # rigid rotation, not cantilever
    base = mode()['rpm']
    assert math.isclose(mode(E=4000)['rpm'],2*base,rel_tol=2e-6)
    assert math.isclose(mode(rho=350)['rpm'],2*base,rel_tol=2e-6)
    assert math.isclose(mode(root=2.8)['rpm'],4*base,rel_tol=2e-6)
    assert math.isclose(mode(mass_d=1.6)['rpm'],2*base,rel_tol=2e-6)
    # Exact tip-load cantilever Euler bifurcation: Pcr=pi²EI/(4L²).
    pc = math.pi**2*(1e9*math.pi*.0014**4/64)/(4*.064**2)
    assert mode(x=64,P=.99*pc)['stable']
    assert not mode(x=64,P=1.01*pc)['stable']
    assert mode(x=57,P=.2)['rpm'] < mode(x=57)['rpm']
    assert mode(x=32,kn=.1,nut_mass=.02)['rpm'] < mode(x=32,kn=.1)['rpm']
    errors=[]
    for x in (7,27,57):
        for settings in (dict(base='pinned',kn=math.inf,P=.2),
                         dict(base='spring',ktheta=10,kn=.1,P=.2,nut_mass=.02)):
            vals=[mode(x=x,elements=n,**settings)['rpm'] for n in (20,40,80)]
            err=abs(vals[1]-vals[2])/max(1,vals[2]); errors.append(err)
            assert err < .0002,(x,settings,vals)
    coarse=scan(base='spring',ktheta=10,kn=.1,P=.2,nut_mass=.02)
    fine=scan(step=1,base='spring',ktheta=10,kn=.1,P=.2,nut_mass=.02)
    assert abs(coarse['min_screen_rpm']-fine['min_screen_rpm']) < .1
    return dict(controls='analytic end conditions, SI scaling, rigid mode, Euler bifurcation, compression, mass, mesh',
                largest_40_to_80_relative_change=max(errors))


def schedules():
    spec=importlib.util.spec_from_file_location('admission',Path(__file__).parents[1]/'E-259/concurrency.py')
    a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
    rows=[]
    for n in (64,80):
        for lead in (2,3):
            for rpm in (500,850,1200,1500,2000,3000):
                v=a.suite(n,32,rpm,1000,lead=lead)
                rows.append(dict(n=n,lead=lead,rpm=rpm,shallow_s=v['shallow_max_s'],deep_s=v['feasible_s'],
                    prep20_s=a.schedule(a.c.v.s.flat(n,20),32,rpm,lead=lead)['feasible_s'],
                    prep30_s=a.schedule(a.c.v.s.flat(n,30),32,rpm,lead=lead)['feasible_s'],
                    dense40_s=a.schedule(a.c.v.s.flat(n,40),32,rpm,lead=lead)['feasible_s'],
                    dense50_s=a.schedule(a.c.v.s.flat(n,50),32,rpm,lead=lead)['feasible_s']))
    assert math.isclose(next(v['deep_s'] for v in rows if v['n']==64 and v['lead']==3 and v['rpm']==2000),25.38,abs_tol=.01)
    return rows


def main():
    cases={
        'fixed_no_nut':dict(base='fixed',kn=0),
        'pinned_ideal_nut':dict(base='pinned',kn=math.inf),
        'fixed_ideal_nut':dict(base='fixed',kn=math.inf),
        'pinned_nut_slope_fixed':dict(base='pinned',kn=math.inf,nut_fixed=True),
        'pinned_tip_no_nut':dict(base='pinned',kn=0,tip=True),
        'spring10_nut0.1':dict(base='spring',ktheta=10,kn=.1),
        'spring10_nut0.1_mass20g':dict(base='spring',ktheta=10,kn=.1,nut_mass=.02),
        'spring10_nut1_mass20g':dict(base='spring',ktheta=10,kn=1,nut_mass=.02),
    }
    scans=[dict(S=S,case=name,P=P,**scan(S=S,P=P,**v))
           for S in (40,50) for name,v in cases.items() for P in (0,.2,.4)]
    stiffness=[dict(kn=kn,ktheta=kt,**scan(P=.2,base='spring',ktheta=kt,kn=kn,nut_mass=.02))
               for kn in (.01,.1,1) for kt in (1,10,100)]
    print(json.dumps(dict(verification=checks(),
        evidence='conditional one-plane linear modes; bounded scenarios, not material/contact priors',
        limiting=[dict(L=L,mass_d=dm,E=E,rho=rho,screen_rpm=.8*analytic(L,mass_d_mm=dm,E_MPa=E,rho=rho))
                  for L in (54,64) for dm in (1.4,3.2) for E,rho in ((1000,1400),(3000,1100))],
        scans=scans,stiffness=stiffness,
        favorable=scan(E=3000,rho=1100,mass_d=1.4,base='pinned',kn=math.inf,P=.2),
        root2=scan(root=2,base='pinned',kn=math.inf,P=.2),
        station_edges=[dict(station=st,**scan(station=st,base='pinned',kn=math.inf,P=.2)) for st in (2,7,12)],schedules=schedules()),indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true')
    if p.parse_args().check: print(json.dumps(checks()))
    else: main()
