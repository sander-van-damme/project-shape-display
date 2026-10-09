"""Full-travel sliding-ramp geometry and Coulomb force bounds; mm, N.
Deterministic epistemic boxes; no process distribution or hardware acceptance.
"""
from itertools import product
from math import isclose, sqrt
import json

PITCH = 5.08


def ramp_geometry(d, w, e, land=.1, guide=.4):
    # Pin and ramp body centers each +/-e; pin width +/-e.
    # Each ramp edge additionally +/-e; preserve full pin-footprint coverage.
    left = -d-w/2-3.5*e-land
    right = w/2+3.5*e+land
    cover = []
    # Finite translating polygon x projection at both stroke endpoints.
    for q, db, dp, dw, dl, dr in product((0., d), *[(-e, e)]*5):
        pin = (dp-(w+dw)/2, dp+(w+dw)/2)
        ramp = (q+db+left+dl, q+db+right+dr)
        cover.extend((pin[0]-ramp[0], ramp[1]-pin[1]))
    # Neighbor at off while this dog is on is the closest arbitrary-mask pair.
    gaps = []
    for q0, q1, b0, b1, r0, l1 in product((0., d), (0., d), *[(-e, e)]*4):
        gaps.append(PITCH+q1+b1+left+l1-(q0+b0+right+r0)-2*guide)
    exact_gap = PITCH-2*d-w-11*e-2*land-2*guide
    assert isclose(min(cover), land, abs_tol=1e-12)
    assert isclose(min(gaps), exact_gap, abs_tol=1e-12)
    return dict(stroke=d, pin_width=w, error=e, ramp_length=right-left,
                footprint_edge_margin=min(cover), neighbor_gap=exact_gap,
                survives=exact_gap>1e-12)


def force_ratio(m, mu, guide_mu):
    # Ramp underside z=z0+m*q-m*x. Relative sliding tangent (-1,m).
    # On dog: N*(m,1)/sqrt(1+m*m) + mu*N*(-1,m)/sqrt(1+m*m).
    # Vertical reaction P also loads dog guide; guide friction opposes x.
    gain = (m-mu)/(1+mu*m)-guide_mu
    return None if gain <= 0 else 1/gain


def writer(d, m, mu, guide_mu, detent=.04, drag=.01,
           preload=.01, spring_k=.10, n=80):
    # Assumed triangular detent ridge, apex at d/2. detent is the maximum
    # horizontal elastic resistance just before the apex. It assists afterward.
    ratio = force_ratio(m, mu, guide_mu)
    if ratio is None:
        return dict(slope=m, mu=mu, guide_mu=guide_mu, transferable=False)
    # Separate guide shoes conservatively carry ramp and plunger reactions;
    # no cancellation of opposing vertical loads is credited.
    detent_slope = .4/d
    plunger_peak = detent/detent_slope
    plunger_end = plunger_peak/3
    peak = (detent+drag+guide_mu*plunger_peak)*ratio
    end = max(0., drag+(guide_mu-detent_slope)*plunger_end)*ratio
    # Driver peak position: reach end, overcome pre-apex or residual end drag.
    # Positive preload means selected force cannot be less than preload.
    h = m*d
    driver = max(h, h/2+max(0., peak-preload)/spring_k,
                 h+max(0., end-preload)/spring_k)
    return dict(slope=m, mu=mu, guide_mu=guide_mu, transferable=True,
                peak_pin_force=peak, end_pin_force=end, ramp_rise=h, driver_stroke_lower=driver,
                all_blocked_row_force=n*(preload+spring_k*driver),
                pin_to_dog_force_ratio=ratio)


def verify():
    # Independent vector force reconstruction, including guide friction.
    for m, mu, mg in product((.5, 1., 1.5), (.1, .3, .5), (.1, .3)):
        ratio = force_ratio(m, mu, mg)
        if ratio is None:
            continue
        P = .05*ratio
        N = P*sqrt(1+m*m)/(1+mu*m)
        H = N*(m-mu)/sqrt(1+m*m)-mg*P
        assert isclose(H, .05, abs_tol=1e-12)
    assert isclose(force_ratio(2., 0., 0.), .5)  # ideal work P dz = H dx
    assert force_ratio(.5, .5, 0.) is None
    assert force_ratio(.5, .3, .3) is None
    # Sample an explicit triangular ridge with linear spring pressure. The
    # peak is approached from below; refinement must approach driver formula.
    d, m, k, p0, a, c0, kd, drag = 1.2, 1., .3, .01, .2, .1, .4, .01
    detent = kd*(c0+a)*(2*a/d)  # .04 N at apex, no detent friction credited
    out = writer(d,m,.3,.1,detent=detent,spring_k=k)
    errors=[]
    for n in (100, 200, 400):
        ratio=force_ratio(m,.3,.1)
        required=[m*d]
        for i in range(n):
            q=d*.5*i/n
            H=kd*(c0+2*a*q/d)*(2*a/d+.1)+drag
            required.append(m*q+max(0.,H*ratio-p0)/k)
        errors.append(out['driver_stroke_lower']-max(required))
    # Here end stroke dominates, so also exercise a force-dominated spring.
    assert all(abs(x)<1e-12 for x in errors)
    errors=[]
    for n in (100,200,400):
        k=.02
        exact=writer(d,m,.3,.1,detent=detent,spring_k=k)['driver_stroke_lower']
        sampled=max(m*d,max(m*(d*.5*i/n)+max(0.,
                    (kd*(c0+2*a*(d*.5*i/n)/d)*(2*a/d+.1)+drag)*
                    force_ratio(m,.3,.1)-p0)/k for i in range(n)))
        errors.append(exact-sampled)
    assert all(isclose(errors[i]/errors[i+1],2,rel_tol=1e-9) for i in (0,1))
    for mu_g in (.1,.3):
        exact = writer(d,m,.3,mu_g,detent=detent)['driver_stroke_lower']
        gain_inv = force_ratio(m,.3,mu_g)
        sampled = m*d
        for i in range(1001):
            q=d*i/1000
            height=2*a*min(q,d-q)/d
            slope=2*a/d if q<=d/2 else -2*a/d
            H=max(0.,kd*(c0+height)*(slope+mu_g)+drag)
            sampled=max(sampled,m*q+max(0.,H*gain_inv-p0)/.1)
        assert isclose(sampled,exact,abs_tol=1e-12)
    return errors


def main():
    errors=verify()
    geometry=[ramp_geometry(d,w,e) for e,d,w in
              product((.05,.1,.2),(1.2,1.5,1.8),(.6,.8,1.))]
    cases=[writer(1.2,m,mu,mg) for m,mu,mg in
           product((.5,1.,1.5),(.1,.3,.5),(.1,.3))]
    print(json.dumps(dict(geometry=geometry,force_cases=cases,
        counts={str(e):sum(r['survives'] for r in geometry if r['error']==e)
                for e in (.05,.1,.2)},
        driver_grid_errors=errors,
        spring_sensitivity=[dict(spring_k=k,**writer(1.2,1.,.3,.1,spring_k=k))
                            for k in (.02,.05,.1)],
        frictional_failures=sum(not r['transferable'] for r in cases)),indent=2))

if __name__ == '__main__':
    main()
