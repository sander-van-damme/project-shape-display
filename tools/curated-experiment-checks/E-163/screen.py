#!/usr/bin/env python3
"""E-163: deterministic necessary-condition screens; mm, N, N mm.
Finite aperture section, ideal frictionless toe reaction, NOT a complete lock.
All manufacturing/friction ranges are explicit scenarios, not probability laws.
"""
import itertools
import json
import math


def section(r, a, t):
    """Centered vertical rod, rotated rectangular through-slot of halfwidth a."""
    assert a >= r > 0 and t > 0
    h = t / 2
    angle = math.acos(r / math.hypot(a, h)) - math.atan2(h, a)
    z = math.sqrt(a*a + h*h - r*r)
    return angle, z


def corners(a, t, outer, angle):
    c, s = math.cos(angle), math.sin(angle)
    def rotate(u, v):
        return (u*c-v*s, u*s+v*c)
    return [[rotate(u,v) for u,v in [(lo,-t/2),(hi,-t/2),(hi,t/2),(lo,t/2)]]
            for lo,hi in [(-outer,-a),(a,outer)]]


def metrics(r, clearance, t, b, mu, load=10):
    angle,z=section(r,r+clearance,t)
    # Balanced lateral normals, vertical toe only; symmetric tangential solution.
    return dict(angle_deg=math.degrees(angle), contact_halfspan_mm=z,
                mu_min=z/b, normal_sum_N=b*load/z,
                extra_return_moment_Nmm=max(0,load*(z/mu-b)))


def run():
    # Independent polygon extrema/rotation checks at multiple sweep resolutions.
    errors=[]
    for n in (16,64,256):
        err=0.0
        for r,c,t in itertools.product((.75,1,1.5),(.025,.1,.35),(.4,.8,1.2)):
            a=r+c; angle,z=section(r,a,t)
            for i in range(n+1):
                q=angle*i/n
                left,right=corners(a,t,2.4,q)
                gap=min(x for x,y in right)-r
                assert gap >= -1e-12
                assert max(x for x,y in left) <= -r+1e-12
                err=max(err,abs(gap-(a*math.cos(q)-t/2*math.sin(q)-r)))
            left,right=corners(a,t,2.4,angle)
            witness=min(right,key=lambda p:p[0])
            err=max(err,abs(witness[0]-r),abs(witness[1]-z))
            # Beyond seating, finite polygons enter the rod; geometry detects it.
            assert min(x for x,y in corners(a,t,2.4,angle+.001)[1]) < r
        errors.append([n,err])

    # Independent traction-allocation minimization: d=(TL-TR)/F in [-1,1].
    # Equal N each follows from absence of lateral toe reaction. b>r.
    cone_error=0
    for r,c,t,b in itertools.product((.75,1,1.5),(.025,.1,.35),(.4,.8,1.2),(2.4,4,8)):
        _,z=section(r,r+c,t)
        grid=min(z*(1+abs(d))/(b+r*d) for d in (i/1000 for i in range(-1000,1001)))
        cone_error=max(cone_error,abs(grid-z/b))
    assert cone_error < 1e-12

    # Manufacturing uncertainty box: two competing coherent batches. Release
    # worst case: slot halfwidth -.1, tail halfwidth +.1, eccentricity .1.
    # Hold worst case: slot halfwidth +.1, tail halfwidth -.1, thickness +.1.
    # Hold calculation grants recentering and ideal toe, favorable assumptions.
    results=[]
    for b in (2.4,4,8):
        for mu in (.1,.2,.4,.6):
            valid=[]; total=0; release=0; lateral_relaxed=0
            for r,c,t in itertools.product((.75,1,1.5),(.025,.05,.1,.2,.3,.35,.4),(.4,.8,1.2)):
                total+=1
                # At least .4 mm nominal outer ligament within local halfwidth b.
                if r+c+.4 > b: continue
                free=c-.1-.1-.1
                if free < .05-1e-12: continue
                release+=1
                _,z=section(r-.1,r+c+.1,t+.1)
                if mu*(b+r-.1) >= z:
                    lateral_relaxed+=1
                if mu*b >= z:
                    valid.append(dict(r=r,c=c,t=t,b=b,mu_min=z/b))
            results.append(dict(b_mm=b,mu=mu,total=total,release_cases=release,
                                necessary_condition_survivors=len(valid),lateral_relaxed_survivors=lateral_relaxed,best=min(valid,key=lambda x:x['mu_min']) if valid else None))

    nominal=[dict(r=r,clearance=c,t=t,b=b,mu=mu,**metrics(r,c,t,b,mu))
             for r,c,t,b,mu in [(1.5,.025,.4,2.4,.2),(1.5,.1,.8,2.4,.2),
                               (1.5,.35,.8,2.4,.2),(.75,.35,.4,2.4,.2)]]
    required_levers=[]
    for r in (.75,1,1.5):
        for t in (.4,.8):
            _,z=section(r-.1,r+.35+.1,t+.1)
            required_levers.append(dict(r=r,t=t,b_required_at_mu_point2=z/.2))

    capstan=[]
    for mu,turns in itertools.product((.1,.2,.4),(1,2,3)):
        ratio=math.exp(mu*2*math.pi*turns)
        capstan.append(dict(mu=mu,turns=turns,ratio=ratio,
                           hold_tail_at_10N=10/ratio,raise_tail_at_10N=10*ratio,
                           board_raise_J_at_1N=6400*.04*ratio))
    # Independent midpoint integration of dT/dtheta=mu*T; convergence check.
    cap_errors=[]
    for n in (32,128,512):
        h=4*math.pi/n; T=1.0
        for _ in range(n): T*=1+.2*h+(.2*h)**2/2
        cap_errors.append([n,abs(T-math.exp(.2*4*math.pi))])
    assert cap_errors[-1][1] < cap_errors[0][1]/100
    assert math.exp(0)==1
    # No-tail and reversed-load limits (zero spring torque): no support available.
    # For upward F, symmetric normal sum is negative; a unilateral contact opens.
    assert 2.4*(-1)/section(1.5,1.6,.8)[1] < 0
    assert 0*math.exp(.4*6*math.pi)==0

    schedule=[]
    for cell_time in (.1,.25,.45,.8):
        H=next(H for H in range(1,6401) if 6+math.ceil(6400/H)*cell_time<30)
        schedule.append(dict(cell_time_s=cell_time,heads=H,
                             full_time_s=6+math.ceil(6400/H)*cell_time,
                             head_ceiling_if_free_cells_and_250_shared=250/H))
    return dict(evidence='analytical and deterministic finite-section screen, not hardware',
                polygon_checks=errors,force_cone_error=cone_error,nominal=nominal,
                bounded_grid=results,required_levers=required_levers,
                capstan=capstan,capstan_integration_errors=cap_errors,schedule=schedule,
                bought_allowance_per_plate_at_500_with_250_shared=250/12800)


if __name__=='__main__':
    print(json.dumps(run(),indent=2))
