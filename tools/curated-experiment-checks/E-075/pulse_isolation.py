#!/usr/bin/env python3
"""Bounded dimensionless dynamics, no manufactured damping or field priors.
q=x/s, tau=t*sqrt(k/m), V=q^2(1-q)^2/2. No random sampling.
"""
import json
import math
from itertools import product
from functools import lru_cache

BETA=math.pi/3  # assumed 60-degree total angular stroke


def potential(q):
    return q*q*(1-q)**2/2


def restoring(q):
    return q*(1-q)*(1-2*q)


def maximum(f, lo, hi):
    # Independent dense bound adequate for choosing well-separated pulse amplitudes.
    return max(f(lo+(hi-lo)*i/10000) for i in range(10001))


@lru_cache(None)
def energy_threshold(g):
    if g == "torque":
        return maximum(lambda q: potential(q)/((math.sin(BETA*(q-.5))+math.sin(BETA/2))/BETA), 1e-8, 1)
    if g is None:
        return 2/27
    return maximum(lambda q: g*q*(1-q)**2*(g-q)/2, 0, 1)


def step(q,v,h,z,a,g,on):
    def acc(x,y):
        drive = (a*math.cos(BETA*(x-.5)) if g == "torque" else
                 a if g is None else a/(g-x)**2)
        return on*drive-restoring(x)-2*z*y
    k1=(v,acc(q,v))
    k2=(v+h*k1[1]/2,acc(q+h*k1[0]/2,v+h*k1[1]/2))
    k3=(v+h*k2[1]/2,acc(q+h*k2[0]/2,v+h*k2[1]/2))
    k4=(v+h*k3[1],acc(q+h*k3[0],v+h*k3[1]))
    return (q+h*(k1[0]+2*k2[0]+2*k3[0]+k4[0])/6,
            v+h*(k1[1]+2*k2[1]+2*k3[1]+k4[1])/6)


def run(g,z,fraction,restitution,h=.01,horizon=150,mode='pump',schedule=None):
    a=fraction*energy_threshold(g)
    q=v=0.; low=high=0.; edges=[]; prior=False; crossed=None
    for i in range(round(horizon/h)):
        t=i*h
        if schedule is not None:
            # Replay fixed open-loop edge schedule, independent of current state.
            while len(edges)<len(schedule) and t+1e-9>=schedule[len(edges)]:
                edges.append(schedule[len(edges)])
            on=bool(len(edges)%2)
        else:
            on=(mode=='constant' or v>=0)
            if on != prior:
                edges.append(t)
            prior=on
        q,v=step(q,v,h,z,a,g,on)
        if restitution is not None and q<0:
            q=0.;v=-restitution*v if v<0 else v
        low=min(low,q);high=max(high,q)
        if q>=1:
            crossed=(i+1)*h
            break
    return dict(gap_over_stroke=g,damping_ratio=z,amplitude_fraction_single_step=fraction,
                stop_restitution=restitution,mode=mode,step=h,horizon=horizon,
                cross_time=crossed,min_q=low,max_q=high,pulse_edges=edges)


def checks():
    # Unforced energy conservation and mirrored signed reset symmetry.
    for h in (.02,.01):
        q,v=.1,0.; e=potential(q)
        for _ in range(round(30/h)):
            q,v=step(q,v,h,0,0,None,False)
        assert abs(potential(q)+v*v/2-e)<1e-8
    q,v=.2,.03
    for g in (None, 'torque'):
        l=step(q,v,.01,.1,.05,g,True)
        r=step(1-q,-v,.01,.1,-.05,g,True)
        assert abs(l[0]+r[0]-1)<1e-12 and abs(l[1]+r[1])<1e-12
    assert math.isclose(energy_threshold(None),2/27)
    # Single sustained steps below the analytical threshold cannot cross losslessly.
    for g in (None,"torque",1.5,2.5,5.):
        assert run(g,0,.95,None,mode='constant')['cross_time'] is None


def main():
    checks()
    rows=[run(g,z,f,r) for g,z,f,r in product((None,"torque",1.5,2.5,5.),(0.,.02,.1),(.8,.95),(None,0.,.5,1.))]
    refined=[run(r['gap_over_stroke'],r['damping_ratio'],r['amplitude_fraction_single_step'],
                 r['stop_restitution'],h=.005) for r in rows]
    assert all((a['cross_time'] is None)==(b['cross_time'] is None) for a,b in zip(rows,refined))
    # Replay adversarial witnesses as fixed-time schedules at refined time steps.
    # A replay is a physically possible pulse sequence, not a proposed controller.
    witnesses=[]
    for g in (None,"torque",1.5,2.5,5.):
        base=run(g,0,.8,None)
        assert base['cross_time'] is not None
        trials=[run(g,0,.8,None,h=h,schedule=base['pulse_edges']) for h in (.005,.0025)]
        assert all(t['cross_time'] is not None for t in trials)
        assert abs(trials[0]['cross_time']-trials[1]['cross_time'])<.02
        witnesses.append(dict(base=base,replay=trials))
    print(json.dumps(dict(evidence='bounded ODE scenarios; no yield or hardware qualification',
        refinement_classification_agreement=len(rows),cases=len(rows),crossings=sum(r['cross_time'] is not None for r in rows),
        cases_all=rows,witnesses=witnesses),indent=2))

if __name__=='__main__':
    main()
