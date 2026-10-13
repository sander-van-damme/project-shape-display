#!/usr/bin/env python3
"""E-262 section alternatives: conditional stiffness escapes, no rotor rating.

SI section reconstruction maps EI/mass into the existing beam implementation.
Metal transfer=0/1 are competing credit scenarios, not a calibrated bond model.
"""
import argparse
import importlib.util
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location('stability', Path(__file__).with_name('stability.py'))
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)


def section(root=1.4, outer=3.2, bore=0., core=0., transfer=1., E=1000., rho=1400.):
    """Polymer root annulus; OD cylinder mass less bore plus metal core.

    200 GPa/7900 kg/m3: Outokumpu austenitic sheet EPD, p7. Application
    to straight wire is an explicit material analogy, not a supplier rating.
    Adhesive in radial gap is unmodelled; this is NOT a bonded-joint design.
    """
    assert 0 <= core <= bore < root <= outer and 0 <= transfer <= 1
    area = lambda d: math.pi*(d/1000)**2/4
    inertia = lambda d: math.pi*(d/1000)**4/64
    EI = E*1e6*(inertia(root)-inertia(bore)) + transfer*200e9*inertia(core)
    mu = rho*(area(outer)-area(bore)) + 7900*area(core)
    # Reference root/OD retained only as a numerical encoding of EI and mu.
    equivalent = dict(root=1.4, mass_d=3.2,
                      E=EI/inertia(1.4)/1e6, rho=mu/area(3.2))
    return dict(EI_Nm2=EI, mass_kg_m=mu, equivalent=equivalent,
                root_ligament_mm=(root-bore)/2)


def variants():
    return {'historical': section(),
            'wide_polymer': section(root=2.6, outer=4.4),
            'core_full_credit': section(bore=1.2, core=1.),
            'core_no_credit': section(bore=1.2, core=1., transfer=0.)}


def rigid_bound(sec, stroke=50, kn=.1, ktheta=10., nut_mass=.02, P=.2):
    """Rigid-tilt Rayleigh trial: upper bound on lowest mode, not safe RPM.

    Admissible for a translation-fixed, rotational-spring base and finite nut
    spring. w(z)=z*theta gives Ktheta=kbase+kn*x^2-P*x.
    """
    L=(stroke+14)/1000
    rows=[]
    for u in range(stroke+1):
        x=(7+u)/1000
        K=ktheta/1000+kn*1000*x*x-P*x
        J=sec['mass_kg_m']*L**3/3+nut_mass*x*x
        rpm=.8*60/(2*math.pi)*math.sqrt(max(0,K/J))
        rows.append((rpm,u))
    rpm,u=min(rows)
    return dict(screen_rpm_upper_bound=rpm, at_u_mm=u)


def scans():
    support = {'ideal_nut': dict(base='pinned', kn=math.inf),
               'soft_nut_mass': dict(base='spring', ktheta=10, kn=.1, nut_mass=.02),
               'stiffer_nut_mass': dict(base='spring', ktheta=10, kn=1, nut_mass=.02)}
    return [dict(variant=name, S=stroke, support=label,
                 **s.scan(S=stroke, step=1, P=.2, **v['equivalent'], **kw))
            for name,v in variants().items() for stroke in (40,50)
            for label,kw in support.items()]


def ledger(n, stroke=50):
    count = n*n
    length = (stroke+14)/1000
    base, wide, core = (variants()[k] for k in ('historical','wide_polymer','core_full_credit'))
    # Unchanged .44-mm tube wall; excludes cap, nut and seats.
    tube_area = lambda w: w*w-(w-.88)**2
    pin_length = stroke+46
    return dict(n=n, sites=count, installed_outputs=2*n,
                core_stock_m=count*length,
                core_stock_kg=count*length*7900*math.pi*.001**2/4,
                added_screw_mass_kg={k:count*length*(v['mass_kg_m']-base['mass_kg_m'])
                                     for k,v in [('wide',wide),('core',core)]},
                wider_pin_extra_tube_l=count*pin_length*(tube_area(5.6)-tube_area(4.4))/1e6,
                extra_10s_operation_hours=count*10/3600,
                extra_30s_operation_hours=count*30/3600,
                extra_005_dollar_site=count*.05,
                # Inherited $4.24/output plus $360 reserve, excluding resident allowance.
                residual_per_site={budget:(budget-4.24*2*n-360)/count for budget in (500,1000,1500)})


def geometry():
    result=[]
    for outer,width,pitch in ((3.2,4.4,5.08),(4.4,5.6,6.35)):
        root=outer-1.8
        mean=outer-.9
        for stroke in (40,50):
            U=.24/2+.24*(stroke+2)/42
            result.append(dict(outer_mm=outer, root_mm=root, pin_mm=width,pitch_mm=pitch,S=stroke,
                               cutter_wall_mm=(width-(outer+.3))/2,
                               guide_only_neighbor_gap_mm=pitch-width-2*U,
                               thread_only_mu_threshold=3/(math.pi*mean)*math.cos(math.radians(15))))
    return result


def schedules():
    spec=importlib.util.spec_from_file_location('admission',Path(__file__).parents[1]/'E-259/concurrency.py')
    a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
    rows=[]
    for n in (64,80):
        for rpm in (850,1200,2000):
            for lead in (2,3):
                v=a.suite(n,32,rpm,1000,lead=lead)
                rows.append(dict(n=n,rpm=rpm,lead=lead,shallow_s=v['shallow_max_s'],deep_s=v['feasible_s'],
                    prep30_s=a.schedule(a.c.v.s.flat(n,30),32,rpm,lead=lead)['feasible_s'],
                    dense50_s=a.schedule(a.c.v.s.flat(n,50),32,rpm,lead=lead)['feasible_s']))
    return rows


def checks():
    v=variants()
    # Pure polymer and ideal metal cylinder recover direct section identities.
    base=v['historical']
    assert math.isclose(base['equivalent']['E'],1000)
    assert math.isclose(base['equivalent']['rho'],1400)
    assert math.isclose(v['wide_polymer']['EI_Nm2']/base['EI_Nm2'],(2.6/1.4)**4)
    assert math.isclose(v['wide_polymer']['mass_kg_m']/base['mass_kg_m'],(4.4/3.2)**2)
    same=section(bore=0,core=0,transfer=0)
    assert same==base
    for x in (7,32,57):
        original=s.mode(x=x,base='pinned',kn=math.inf,P=.2)['rpm']
        mapped=s.mode(x=x,base='pinned',kn=math.inf,P=.2,**base['equivalent'])['rpm']
        assert math.isclose(original,mapped,rel_tol=1e-10)
    for name,sec in v.items():
        # Independent uniform cantilever formula uses the actual composite EI/mu.
        ref=60/(2*math.pi)*1.875104068712**2/.064**2*math.sqrt(sec['EI_Nm2']/sec['mass_kg_m'])
        actual=s.mode(L=64,x=32,**sec['equivalent'])['rpm']
        assert math.isclose(ref,actual,rel_tol=2e-5),(name,ref,actual)
    assert v['core_no_credit']['EI_Nm2'] < base['EI_Nm2'] < v['core_full_credit']['EI_Nm2']
    assert math.isclose(v['core_full_credit']['root_ligament_mm'],.1)
    # Independent rigid-tilt Rayleigh bound exposes support-limited stiffness gains.
    for sec in v.values():
        got=s.scan(step=1,P=.2,base='spring',ktheta=10,kn=.1,nut_mass=.02,**sec['equivalent'])
        assert got['min_screen_rpm'] <= rigid_bound(sec)['screen_rpm_upper_bound']*(1+1e-6)
    # Composite mesh convergence, separate from contact uncertainty.
    errors=[]
    for name in ('wide_polymer','core_full_credit'):
        for x in (7,32,57):
            kw=dict(x=x,base='spring',ktheta=10,kn=.1,nut_mass=.02,P=.2,**v[name]['equivalent'])
            coarse=s.mode(elements=40,**kw)['rpm'];fine=s.mode(elements=80,**kw)['rpm']
            errors.append(abs(coarse-fine)/max(1,fine))
            assert errors[-1]<.0002
    for n in (64,80):
        assert ledger(n)['sites']==n*n
        assert math.isclose(ledger(n)['extra_30s_operation_hours'],n*n/120)
    assert math.isclose(geometry()[-1]['guide_only_neighbor_gap_mm'],-.0842857142857,abs_tol=1e-9)
    assert math.isclose(schedules()[5]['deep_s'],25.38,abs_tol=.01)
    return dict(controls='section identities, baseline mapping, independent composite cantilever, bond-credit limits, mesh and ledgers',
                largest_40_to_80_relative_error=max(errors))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true')
    args=p.parse_args()
    result=checks()
    if not args.check:
        result=dict(verification=result,sections=variants(),scans=scans(),geometry=geometry(),
                    rigid_bounds={name:rigid_bound(sec) for name,sec in variants().items()},
                    ledger=[ledger(n) for n in (64,80)],schedules=schedules())
    print(json.dumps(result,indent=2))
