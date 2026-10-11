"""Reproduce E-189. --full adds mesh, friction and manufactured-radius scenarios.

Python 3, numpy 1.26.4, scipy 1.14.1 were used. JSON is disposable.
Solver failures are indeterminate, never mechanism failures or passing cases.
"""
import argparse
import json
import math
import numpy as np
from rod import Coil, clean, sweep


def arrest_bound(torque_Nmm):
    """Imposed constant post-engagement capacity, grounded rotor, zero delay."""
    load,pinion,speed,inertia=1.,.002,.3,1e-8
    mass=load/9.81+inertia/pinion**2
    brake=torque_Nmm*.001/pinion
    if brake<=load:return dict(finite_stop=False)
    distance=.5*mass*speed**2/(brake-load)
    heat=brake*distance
    assert abs(heat-(.5*mass*speed**2+load*distance))<1e-12
    return dict(finite_stop=True,distance_mm=1000*distance,heat_mJ=1000*heat)


def mechanics_checks():
    c=Coil(n=8)
    rng=np.random.default_rng(189)
    x=rng.normal(0,.01,27)
    u,g,_=c.energy_gradient(x)
    numeric=np.array([np.imag(c.energy_gradient(x.astype(complex)+1e-25j*e)[0])/1e-25
                      for e in np.eye(len(x))])
    gradient_error=float(max(abs(g-numeric)))
    assert gradient_error<1e-8
    rotated=x+np.tile([0,.73*c.r,0],c.n+1)
    assert abs(c.energy_gradient(rotated)[0]-u)<1e-9
    # Cartesian translation must preserve strain energy, including finite rotation.
    theta=np.linspace(0,6*math.pi,c.n+1)
    w,a,b=x.reshape(-1,3).T
    phi=theta+a/c.r
    px=(c.r+w)*np.cos(phi)+.21
    py=(c.r+w)*np.sin(phi)-.17
    moved_phi=np.unwrap(np.arctan2(py,px))
    moved=np.stack([np.hypot(px,py)-c.r,c.r*(moved_phi-theta),
                    c.r*(phi+b/c.r-moved_phi)],axis=1).ravel()
    assert abs(c.energy_gradient(moved)[0]-u)<1e-9
    # Independent exact uniformly opened circular rod: inextensible pure bending.
    ro=c.r+.12
    circle=np.zeros((c.n+1,3))
    circle[:,0]=ro-c.r
    circle[:,1]=c.r*theta*(c.r/ro-1)
    eu,_,fields=c.energy_gradient(circle.ravel())
    expected=c.ei*(6*math.pi*c.r)/2*(1/ro-1/c.r)**2
    assert abs(eu-expected)<1e-10 and max(abs(fields['strain']))<1e-12
    assert max(abs(fields['shear']))<1e-12
    assert c.geometry(circle.ravel())['min_arc_gap_mm']>.06
    # Straight-element sinc limit with the rod's intrinsic curvature retained.
    ss=np.linspace(0,c.h*c.n,c.n+1)
    ph=np.arctan2(ss,3.)
    straight=np.stack([np.hypot(ss,3.)-c.r,c.r*(ph-theta),-c.r*ph],axis=1)
    su,_,sf=c.energy_gradient(straight.ravel())
    assert abs(su-c.ei*(c.h*c.n)/(2*c.r*c.r))<1e-9
    assert max(abs(sf['strain']))<1e-12 and max(abs(sf['shear']))<1e-12
    zero=Coil(n=60,mu=0).solve()
    assert zero['torque_Nmm']==0
    assert not arrest_bound(2.)['finite_stop']
    assert arrest_bound(6.)['finite_stop']
    return dict(gradient_error=gradient_error,pure_bending_energy_mJ=float(eu),
                rigid_motion=True,zero_friction=True)


def signed_check(n):
    forward=sweep(n=n,openings=[0,.1,.6])
    reverse=sweep(n=n,slip=-1,anchor='end',openings=[0,.1,.6])
    for a,b in zip(forward['states'],reverse['states']):
        assert abs(a['torque_Nmm']+b['torque_Nmm'])<2e-5
        assert abs(a['tang_force_N']-b['tang_force_N'])<2e-5
    return dict(mesh=n,forward=forward,reverse=reverse)


def emit(name,fn):
    try:
        result=fn()
    except RuntimeError as exc:
        print(json.dumps(dict(case=name,status='indeterminate_solver',error=str(exc))),flush=True)
        return None
    print(json.dumps(dict(case=name,status='solved',result=result)),flush=True)
    return result


def friction_continuation():
    c=Coil(n=120)
    states=[dict(mu=.05,**clean(Coil(n=120,mu=.05).solve()))]
    for mu in [.1,.125,.15,.175,.2]:
        c.mu=mu
        s=c.solve()
        states.append(dict(mu=mu,**clean(s)))
    start=float(c.last[0][3*c.command+1])
    release=[]
    previous=0.
    for q in [0,.1,.3,.6,1.,2.5]:
        for intermediate in np.linspace(previous,q,max(1,math.ceil(abs(q-previous)/.1))+1)[1:]:
            r=c.solve(start-intermediate)
        previous=q
        release.append(dict(q_mm=q,force_N=float(-r['reaction'][3*c.command+1]),**clean(r)))
    return dict(initial=states,high_mu_release=release,
                imposed_arrest=[dict(mu=s['mu'],**arrest_bound(s['torque_Nmm'])) for s in states])


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--full',action='store_true')
    args=parser.parse_args()
    print(json.dumps(dict(checks=mechanics_checks())),flush=True)
    # Numerical checks are hard failures; unresolved scenario roots are labelled.
    print(json.dumps(dict(signed=signed_check(60))),flush=True)
    if args.full:
        for n in [60,120,240]:
            emit(f'mesh_{n}',lambda n=n:sweep(n=n,openings=[0,.1,.3,.6,1.,2.5]))
        emit('friction_continuation',friction_continuation)
        cases=[dict(mu=.05),dict(slip=-1),dict(clamped=False),
               dict(hub=2.9,interference=.05),dict(hub=2.9,interference=-.15),
               dict(hub=3.1,interference=.25),dict(hub=3.1,interference=.05)]
        for case in cases:
            emit(str(case),lambda case=case:sweep(n=120,**case,openings=[0,.1,.6,2.5]))
