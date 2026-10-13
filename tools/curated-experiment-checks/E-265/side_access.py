#!/usr/bin/env python3
"""Finite cylinder sweeps and bounded force/schedule screen, not mating CAD."""
import argparse
import importlib.util
import itertools
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location('access', Path(__file__).parents[1]/'E-264/access.py')
e = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e)


def segment_distance(a, b, c):
    v = [b[i]-a[i] for i in range(2)]
    vv = sum(x*x for x in v)
    t = max(0., min(1., sum((c[i]-a[i])*v[i] for i in range(2))/vv)) if vv else 0.
    return math.hypot(*(a[i]+t*v[i]-c[i] for i in range(2)))


def sweep(a, b, radius, zlo, zhi, obstacles, skip=()):
    """Exact XY capsule vs vertical cylinders, for constant tool Z interval."""
    values = []
    for name, xy, r, lo, hi in obstacles:
        if name in skip or min(zhi,hi) <= max(zlo,lo):
            continue
        values.append((segment_distance(a,b,xy)-radius-r,name))
    return min(values, default=(math.inf,'none'))


def route(p, stroke, contact):
    """Transit, rise at interstice, engage/release all four neighboring cells.

    The head rises 3 mm; shafts run down to a below-tail bridge. The bridge
    stays below longest tails. Target tooth overlap / roller compression granted.
    All other cells are unchanged and retain their full tail union at every Z.
    """
    assert contact in ('positive','friction')
    d = 2.6 if contact == 'positive' else 2.95
    obs=[]
    for i,j in itertools.product(range(-2,4),repeat=2):
        xy=(i*p,j*p); key=f'{i},{j}'
        obs.extend([(f'tail:{key}',xy,1.6,-stroke-2,12),
                    (f'rim:{key}',xy,2.2,-3.5,-2.5),
                    (f'neck:{key}',xy,1.75,-2.5,0),
                    (f'bed:{key}',xy,2.4,-.5,0)])
    cavity=(p/2,p/2)
    stages={}
    stages['tail_transit']=sweep((p/2,-p/2),(p/2,1.5*p),.8,-7,-5,obs)
    # Vertical movement swept union [-7,-2], exact because XY stays constant.
    stages['lift']=sweep(cavity,cavity,.8,-7,-2,obs)
    for i,j in itertools.product((0,1),repeat=2):
        target=(i*p,j*p)
        q=tuple(target[k]+(1 if target[k]==0 else -1)*d/math.sqrt(2) for k in range(2))
        key=f'{i},{j}'
        stages['wheel_'+key]=sweep(cavity,q,.8,-4,-2,obs,skip=(f'rim:{key}',))
        stages['shaft_'+key]=sweep(cavity,q,.5,-stroke-5,-4,obs)
        # Release reverses exactly the same capsule, including neighbor rows.
        assert stages['wheel_'+key] == sweep(q,cavity,.8,-4,-2,obs,skip=(f'rim:{key}',))
    # Rotor/bed axial clearances, housing not present in this first embodiment.
    stages['bed_axial']=(1.5,'bed underside')
    stages['rim_transit_axial']=(1.5,'rim underside')
    minimum=min(v[0] for v in stages.values())
    return dict(min_gap_mm=minimum, stages=stages,
                coherent_gap_bounds={str(b):minimum-b for b in (0,.15,.3,.6)},
                service_center_mm=d, approach_mm=p/math.sqrt(2)-d,
                access_s=2*(e.move(3)+e.move(p/math.sqrt(2)-d)))


def forces(torque=.35, mu=.3, stroke=50, diameter=1., E=200000.):
    """N mm, mm, N/mm2. E is a favorable metal-shaft scenario, not a quote."""
    I=math.pi*diameter**4/64
    L=stroke+2 # service center -3; bridge bearing no higher than -(S+5)
    ft=torque/2
    gear=ft/math.cos(math.radians(20))
    fn=torque/(mu*2.2)
    roller=math.hypot(fn,torque/2.2)
    return dict(torque_Nmm=torque,mu=mu,span_mm=L,
        gear_tangential_N=ft,gear_radial_N=ft*math.tan(math.radians(20)),
        gear_resultant_N=gear,roller_normal_N=fn,roller_resultant_N=roller,
        gear_deflection_mm=gear*L**3/(3*E*I),
        roller_deflection_mm=roller*L**3/(3*E*I),
        gear_max_span_at_point2mm=(.2*3*E*I/gear)**(1/3),
        roller_max_span_at_point2mm=(.2*3*E*I/roller)**(1/3),
        gear_max_torque_at_point2mm=.2*3*E*I/L**3*2*math.cos(math.radians(20)),
        roller_max_torque_at_point2mm=.2*3*E*I/L**3/math.hypot(1/(mu*2.2),1/2.2))


def coupled_shaft(p, stroke, torque=.35, mu=.3, gap_error=.3):
    # Largest bare shaft allowed by both transit and target-tail separation.
    # No bearing housing is included; equality has zero residual radial gap.
    dmax=2*(min(p/2-1.6,2.95-1.6)-gap_error)
    f=forces(torque,mu,stroke,dmax)
    radial=f['roller_normal_N']*(stroke+2)**3/(3*200000*math.pi*dmax**4/64)
    return dict(max_bare_diameter_mm=dmax,radial_deflection_mm=radial,
                torque_ceiling_for_005mm_fixed_squeeze_Nmm=torque*.05/radial)


def schedule(before, after, stroke, contact='friction', rpm=2000, lead=3, extra=None):
    """Per-channel engagement is granted; no unchanged nut is touched.

    Banks each have n shafts, only changed shafts execute the radial stroke.
    All shafts transit low. Each visited row pays out/back radial stroke and
    lift/lower; inherited .08 selection plus .02 proof is NOT removed.
    Two synchronized banks; no XY/Z overlap; return and one row retry included.
    """
    n=len(before); delta=e.a.r.delta(before,after); p=406.4/n
    access=route(p,stroke,contact)['access_s'] if extra is None else extra
    totals=[]; retry=0.; stations=0
    for base in range(0,n,n//2):
        total=0.; last=base
        for y in range(base,base+n//2):
            if not any(delta[y]): continue
            dwell=e.a.row_bounds(tuple(sorted(abs(d) for d in delta[y] if d)),32,rpm,1000,.02,0,lead)[1]
            total+=max(.05,e.move((y-last)*p))+dwell+access
            retry=max(retry,dwell+access); last=y; stations+=1
        total+=e.move((last-base)*p); totals.append(total)
    return 4+max(totals)+retry if stations else 0.


def suite(n,stroke,contact,**kw):
    values={k:schedule(x,y,stroke,contact,**kw) for k,(x,y) in e.pairs(n,stroke).items()}
    flat=e.a.c.v.s.flat
    return dict(max_s=max(values.values()),worst=max(values,key=values.get),
                prep_s=schedule(flat(n,0),flat(n,stroke-20),stroke,contact,**kw),
                dense_s=schedule(flat(n,0),flat(n,stroke),stroke,contact,**kw))


def checks():
    # Independent limits and interior-segment witness (endpoint-only fails).
    assert segment_distance((-1,1),(1,1),(0,0))==1
    assert segment_distance((1,0),(2,0),(0,0))==1
    assert segment_distance((1,1),(1,1),(0,0))==math.sqrt(2)
    for p,s,c in itertools.product((6.35,5.08),(40,50),('positive','friction')):
        g=route(p,s,c)
        assert math.isclose(g['stages']['tail_transit'][0],p/2-2.4,abs_tol=1e-12)
        assert g['min_gap_mm']>0
        # Adjacent row-head outputs use the same approach quadrant. Independent
        # radial phases reduce their X separation by at most one X throw.
        assert p-(p/2-g['service_center_mm']/math.sqrt(2)) > 1.6
        if c == 'positive': assert math.isclose(g['min_gap_mm'],.05,abs_tol=1e-12)
        # Mirror symmetry tests all four targets, including both adjacent rows.
        vals=[g['stages']['wheel_'+f'{i},{j}'][0] for i,j in itertools.product((0,1),repeat=2)]
        assert max(vals)-min(vals)<1e-12
        for i,j in itertools.product((0,1),repeat=2):
            assert g['stages']['shaft_'+f'{i},{j}'][0]>.49
    assert route(6.35,50,'friction')['coherent_gap_bounds']['0.3']>0
    assert route(5.08,50,'friction')['coherent_gap_bounds']['0.15']<0
    assert route(6.35,50,'positive')['coherent_gap_bounds']['0.3']<0
    # Attempting a straight radial approach to a row, fine pitch, hits neighbor.
    assert 5.08-2.6-2.2-.8<0
    # Two independent force identities, scaling, and schedule anchors.
    f=forces(); f2=forces(torque=.7)
    assert math.isclose(f2['roller_deflection_mm'],2*f['roller_deflection_mm'])
    assert math.isclose(forces(diameter=2)['roller_deflection_mm'],f['roller_deflection_mm']/16)
    assert math.isclose(f['roller_normal_N']*.3*2.2,.35)
    assert math.isclose(coupled_shaft(6.35,50)['max_bare_diameter_mm'],2.1)
    assert coupled_shaft(6.35,50)['radial_deflection_mm']>.05
    for n,s in itertools.product((64,80),(40,50)):
        for x,y in e.pairs(n,s).values():
            assert math.isclose(schedule(x,y,s,extra=0),e.schedule(x,y,s,policy='free')['seconds'],abs_tol=1e-9)
        flat=e.a.c.v.s.flat
        assert schedule(flat(n,20),flat(n,20),s)==0
        added=schedule(flat(n,0),flat(n,s),s)-schedule(flat(n,0),flat(n,s),s,extra=0)
        assert math.isclose(added,(n//2+1)*route(406.4/n,s,'friction')['access_s'],abs_tol=1e-9)
    return 'Exact swept capsules; four target/reverse symmetry; interior collision witness; coherent bounds; force identities; all inherited zero-access schedules; dense/no-op anchors'


def main():
    p=argparse.ArgumentParser(); p.add_argument('--check',action='store_true'); args=p.parse_args()
    check=checks()
    if args.check: print(check); return
    print(json.dumps(dict(checks=check,
      routes={str(p):{c:route(p,50,c) for c in ('positive','friction')} for p in (6.35,5.08)},
      coupled_shafts=[dict(p=p,stroke=s,**coupled_shaft(p,s)) for p,s in itertools.product((6.35,5.08),(40,50))],
      forces=[forces(t,mu,s) for t,mu,s in itertools.product((.05,.35,1.),(.15,.3,.6),(40,50))],
      schedules=[dict(n=n,stroke=s,**{c:suite(n,s,c) for c in ('positive','friction')},
                      friction_lead2=suite(n,s,'friction',lead=2)) for n,s in itertools.product((64,80),(40,50))]),indent=2))

if __name__=='__main__': main()
