"""Finite corner-followed trip ramp and passive detent completion, mm/N.
Epistemic boxes, deterministic synthesis; no measured priors or 3D qualification.
"""
from itertools import product
from math import isclose
import json

PITCH = 5.08


def section(d, w, e, r, land=.1, guide=.4, stop_error=0.):
    # A flat pin top touches the lowest underside point: its RIGHT corner.
    # z = z0 + m*q - m*x. Release occurs when the wing's LEFT edge
    # passes that corner. Other ramp points are then entirely right of the pin.
    left = -r+w/2
    right = w/2+3.5*e+land
    releases, initial, gaps = [], [], []
    for dp, db, dw, dl, dr in product((-e, e), repeat=5):
        pin = (dp-(w+dw)/2, dp+(w+dw)/2)
        wing = (db+left+dl, db+right+dr)
        releases.append(pin[1]-wing[0])
        initial.extend((pin[0]-wing[0], wing[1]-pin[1]))
    for q0, q1, b0, b1, r0, l1 in product((0., d+stop_error), (0., d+stop_error), *[(-e, e)]*4):
        gaps.append(PITCH+q1+b1+left+l1-(q0+b0+right+r0)-2*guide)
    assert isclose(min(releases), r-3.5*e, abs_tol=1e-12)
    assert isclose(max(releases), r+3.5*e, abs_tol=1e-12)
    assert isclose(min(gaps), PITCH-d-stop_error-r-7.5*e-land-2*guide, abs_tol=1e-12)
    # Crest position is independently bounded by +/-e.
    margins = dict(initial_land=min(initial), neighbor_gap=min(gaps),
                   past_crest=min(releases)-(d/2+e),
                   before_stop=d-stop_error-max(releases))
    return dict(release_min=min(releases), release_max=max(releases),
                wing_length=right-left, **margins,
                fits=min(margins.values())>1e-10)


def coast(d, crest, height, k, c, mu, drag, release):
    """Exact work from zero-speed release down a triangular spring detent.
    Fnet = k*(c+t*(d-q))*(t-mu)-drag; slope t=height/(d-crest).
    No post-release pin work. A positive net work with negative end force
    permits inertial arrival only; positive end force permits slow seating.
    """
    assert crest < release < d and height > 0
    t = height/(d-crest)
    L = d-release
    endpoint_force = k*c*(t-mu)-drag
    work = endpoint_force*L + .5*k*t*(t-mu)*L*L
    start_force = endpoint_force+k*t*(t-mu)*L
    return dict(work=work, start_force=start_force, end_force=endpoint_force,
                passes=start_force>0 and work>0, slow_seating=endpoint_force>0)


def robust_coast(d, e, a, k, c, mu, r, stop_error=0.):
    # k,c,mu are competing coherent scenarios, NOT distributions.
    # Include BOTH actual end positions; work need not have one worst corner.
    if a<=e:
        return dict(passes=False, slow_seating=False, reason='nonpositive_ridge')
    out=[]
    for h, xc, rel, end in product((a-e,a+e), (d/2-e,d/2+e),
                                   (r-3.5*e,r+3.5*e),
                                   (d-stop_error,d+stop_error)):
        out.append(coast(end,xc,h,k,c,mu,.01,rel))
    # Continuous-box slow-seating bound: shallowest descending slope.
    t=(a-e)/(d+stop_error-(d/2-e))
    end_force=k*c*(t-mu)-.01
    slow=end_force>0
    assert slow == all(o['slow_seating'] for o in out)
    passed=all(o['passes'] for o in out)
    return dict(passes=passed, slow_seating=slow,
                reason='slow_seating' if slow else 'inertial_only' if passed else 'passive_stall',
                minimum_corner_work=min(o['work'] for o in out), end_force=end_force)


def optimum_section(e, stop_error, land=.1, guide=.4):
    # Maximize the minimum of crest, before-stop and neighbor margins in
    # continuous (d,r). Their positive weighted sum eliminates d and r:
    # Weights crest=4, stop=3, neighbor=1 (sum=8).
    # d: -2+3-1=0; r: 4-3-1=0. Bound C/8-4.5e-.5s.
    C=PITCH-land-2*guide
    d=C/2-2*e
    r=.75*d+.5*e-.5*stop_error
    margin=C/8-4.5*e-.5*stop_error
    return dict(d=d,r=r,margin=margin)


def driven_force(d,e,a,k,c,mu,m=1.,ramp_mu=.3,spring_k=.1,preload=.01,r=None):
    # Separate guide shoes as E-078. Largest rising slope at latest crest? No:
    # H=k(c+a)*(a/crest+mu)+drag, so EARLIEST crest is the force worst corner.
    gain=(m-ramp_mu)/(1+ramp_mu*m)-mu
    if gain<=0:
        return None
    h=a+e
    P=(k*(c+h)*(h/(d/2-e)+mu)+.01)/gain
    # Conservative sufficient driver position for bounded crest location:
    # combine largest peak force and latest crest, even though not coincident.
    # Covers approach to crest and rise through latest release. Free approach
    # through shutters excluded; this is not a complete actuator stroke.
    D=max(m*(r+3.5*e),m*(d/2+e)+max(0.,P-preload)/spring_k)
    return dict(peak_force_upper=P, driver_travel_bound=D,
                all_blocked_force_at_bound=80*(preload+spring_k*D))


def verify():
    # Independent midpoint integration of affine post-crest force is exact.
    for d,crest,a,k,c,mu,rel in ((1.2,.6,.2,.4,.1,.1,.65),
                                 (1.2,.6,.2,.4,.1,.3,.65),
                                 (1.8,.8,.3,.8,.15,.1,1.79)):
        exact=coast(d,crest,a,k,c,mu,.01,rel)
        for n in (20,40,80):
            dx=(d-rel)/n
            total=0
            for i in range(n):
                q=rel+(i+.5)*dx
                z=a*(d-q)/(d-crest)
                # Elastic work - guide Coulomb work - constant drag.
                total+=(k*(c+z)*a/(d-crest)-mu*k*(c+z)-.01)*dx
            assert isclose(total,exact['work'],abs_tol=1e-12)
    # Frictionless work equals independent spring-potential difference.
    x=coast(1.2,.6,.2,.4,.1,0.,0.,.65)
    z=.2*(1.2-.65)/.6
    assert isclose(x['work'],.5*.4*((.1+z)**2-.1**2),abs_tol=1e-12)
    assert not coast(1.2,.6,.2,.4,.1,.3,.01,.65)['passes']
    # Necessary release-window inequality: d > 16e; strict boundaries fail.
    for d,e in product((1.2,1.5,1.8),(.05,.1,.2)):
        lo=d/2+4.5*e
        hi=d-3.5*e
        assert (hi-lo>1e-10)==(d>16*e+1e-10)
    # Independent continuous-domain upper certificate plus off-optimum holdouts.
    for e, stop_error in product((.05,.1,.2), (0.,.05,.1,.2)):
        opt=optimum_section(e,stop_error)
        d,r=opt['d'],opt['r']
        for dd,rr in product(range(-20,21),repeat=2):
            trial_d=d+dd*.01
            trial_r=r+rr*.01
            margins=(trial_r-trial_d/2-4.5*e,
                     trial_d-stop_error-trial_r-3.5*e,
                     5.08-trial_d-stop_error-trial_r-7.5*e-.1-.8)
            assert isclose((4*margins[0]+3*margins[1]+margins[2])/8,
                           opt['margin'],abs_tol=1e-12)
            assert min(margins)<=opt['margin']+1e-12
        sec=section(d,.8,e,r,stop_error=stop_error)
        for key in ('past_crest','before_stop','neighbor_gap'):
            assert isclose(sec[key],opt['margin'],abs_tol=1e-12)
    assert section(1.8,.8,.1,1.44)['fits']
    assert not section(1.8,.8,.1,1.44,stop_error=.1)['fits']
    assert optimum_section(.1,.1)['margin'] < .05
    assert isclose(optimum_section(.1045,.1045)['margin'],0.,abs_tol=1e-12)
    # Separate inertia-only arrival from positive force all the way to the stop.
    inertia=coast(1.2,.6,.2,.4,.1,.1,.012,.65)
    assert inertia['passes'] and not inertia['slow_seating']
    # Slow seating is robust over interior points too, not only chosen corners.
    for a,k,c,mu in product((.2,.3,.4),(.2,.4,.8),(.05,.1,.15),(.1,.3)):
        opt=optimum_section(.1,.1)
        bound=robust_coast(opt['d'],.1,a,k,c,mu,opt['r'],stop_error=.1)
        for h,xc,end in product((a-.1,a,a+.1),
                                (opt['d']/2-.1,opt['d']/2,opt['d']/2+.1),
                                (opt['d']-.1,opt['d'],opt['d']+.1)):
            out=coast(end,xc,h,k,c,mu,.01,opt['r'])
            assert out['end_force']>=bound['end_force']-1e-12

    return 'corner, work, limiting-case and release-window checks pass'


def main():
    counts={}
    population=[]
    for e in (.05,.1,.2):
        geometries=0
        passed=0
        by_mu={str(mu):0 for mu in (.1,.3)}
        for d,w,f in product((1.2,1.5,1.8),(.6,.8),(.55,.6,.65,.7,.75,.8,.85)):
            r=d*f
            geo=section(d,w,e,r)
            if not geo['fits']:
                population.append(dict(e=e,d=d,w=w,release_fraction=f,reason='geometry',**geo))
                continue
            geometries+=1
            for a,k,c,mu in product((.2,.3,.4),(.2,.4,.8),(.05,.1,.15),(.1,.3)):
                result=robust_coast(d,e,a,k,c,mu,r)
                passed+=result['passes']
                by_mu[str(mu)]+=result['passes']
                population.append(dict(e=e,d=d,w=w,release_fraction=f,a=a,k=k,c=c,mu=mu,
                                       **geo,**result))
        counts[str(e)]=dict(geometries=geometries,geometry_population=42,
                           force_cases=geometries*54,passive_survivors=passed,by_mu=by_mu)
    witness=dict(d=1.8,w=.8,e=.1,r=1.44)
    geo=section(**witness)
    sensitivity=[]
    for a,k,c,mu in product((.2,.3,.4),(.2,.4,.8),(.05,.1,.15),(.1,.3)):
        result=robust_coast(1.8,.1,a,k,c,mu,1.44)
        sensitivity.append(dict(a=a,k=k,c=c,mu=mu,**result,
            drive=driven_force(1.8,.1,a,k,c,mu,r=1.44)))
    extended=[]
    for e in (.05,.1,.2):
        opt=optimum_section(e,e)
        sec=section(opt['d'],.8,e,opt['r'],stop_error=e)
        cases=[]
        if sec['fits']:
            for a,k,c,mu in product((.2,.3,.4),(.2,.4,.8),(.05,.1,.15),(.1,.3)):
                result=robust_coast(opt['d'],e,a,k,c,mu,opt['r'],stop_error=e)
                cases.append(dict(a=a,k=k,c=c,mu=mu,**result,
                    drive=driven_force(opt['d'],e,a,k,c,mu,r=opt['r'])))
        extended.append(dict(e=e,optimum=opt,geometry=sec,cases=cases,
            slow_survivors=sum(x['slow_seating'] for x in cases)))
    print(json.dumps(dict(checks=verify(),counts=counts,witness=dict(**witness,**geo),
                         sensitivity=sensitivity,stop_aware=extended,
                         population=population),indent=2))

if __name__=='__main__':
    main()
