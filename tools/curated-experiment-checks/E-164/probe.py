#!/usr/bin/env python3
"""E-164: rigid finite extrusions, captured frictionless pivot; mm and N.

Bounds are declared scenarios, not manufacturing distributions. No elastic,
dynamic, return-spring, writer or hardware validation is claimed.
"""
import json
import math

PITCH = 5.08


def rotate(x, z, b, q):
    return (b + (x-b)*math.cos(q)-z*math.sin(q),
            (x-b)*math.sin(q)+z*math.cos(q))


def seat(r, a, t, b, e=0):
    """First left-slot corner reaches fixed tail left face e-r."""
    d = b-e+r
    radius = math.hypot(b+a, t/2)
    q = math.acos(d/radius)-math.atan2(t/2, b+a)
    z = math.sqrt(radius*radius-d*d)
    return q, z, z/d


def required_b(r, a, t, mu, e=0):
    # z² = 2 D delta + delta² + h² and z/D <= mu.
    delta = a-r+e
    d = (delta+math.sqrt(delta*delta+mu*mu*(delta*delta+(t/2)**2)))/(mu*mu)
    return d+e-r


def rectangle(lo, hi, t):
    return [(lo,-t/2),(hi,-t/2),(hi,t/2),(lo,t/2)]


def extrema(A, B, lo, hi):
    # Exact extrema of A*cos(q)+B*sin(q) over a closed interval.
    qs = [lo,hi]
    phase = math.atan2(B,A)
    for k in range(-3,4):
        q = phase+k*math.pi
        if lo <= q <= hi:
            qs.append(q)
    vals = [A*math.cos(q)+B*math.sin(q) for q in qs]
    return min(vals),max(vals)


def envelope(poly, b, q):
    xs = [extrema(x-b,-z,0,q) for x,z in poly]
    zs = [extrema(z,x-b,0,q) for x,z in poly]
    return [b+min(v[0] for v in xs),b+max(v[1] for v in xs),
            min(v[0] for v in zs),max(v[1] for v in zs)]


def solids(a, t, b, bypass):
    outer = a+.4
    # Solid x-z sections extruded across the stated y intervals.
    parts = [(rectangle(-outer,-a,t),(-1.8,1.8)),
             (rectangle(a,outer,t),(-1.8,1.8))]
    if bypass:
        parts += [(rectangle(-outer,b+.8,t),(-1.8,-1.2)),
                  (rectangle(-outer,b+.8,t),(1.2,1.8)),
                  # Conservative solid envelope of an annular boss. Its exact
                  # circular bore and axle are checked separately below; do not
                  # treat this bounding rectangle as filled manufactured solid.
                  (rectangle(b-.8,b+.8,1.6),(-1.8,1.8))]
    else:
        parts += [(rectangle(a,b+.8,t),(-1.8,1.8)),
                  (rectangle(-outer,outer,t),(-1.8,-1.2)),
                  (rectangle(-outer,outer,t),(1.2,1.8))]
    return parts


def run():
    checks=[]
    for n in (16,64,256):
        residual=0
        for r,a,t,b,e in [(.75,1.1,.4,2.4,0),(.65,1.2,.5,7.9,.1),
                           (.65,1.2,.5,32.92,.1)]:
            q,z,mu=seat(r,a,t,b,e)
            left=rectangle(-a-.4,-a,t)
            right=rectangle(a,a+.4,t)
            assert envelope(left,b,q)[1] <= e-r+1e-11
            assert envelope(right,b,q)[0] >= e+r-1e-11
            # Independent bisection on explicit rotated vertices.
            lo,hi=0,math.pi/2
            for _ in range(60):
                mid=(lo+hi)/2
                if max(rotate(x,y,b,mid)[0] for x,y in left) < e-r:
                    lo=mid
                else:
                    hi=mid
            residual=max(residual,abs((lo+hi)/2-q))
            for j in range(n+1):
                theta=q*j/n
                assert max(rotate(x,y,b,theta)[0] for x,y in left) <= e-r+1e-11
                assert min(rotate(x,y,b,theta)[0] for x,y in right) >= e+r-1e-11
            cx,cz=rotate(-a,-t/2,b,q)
            residual=max(residual,abs(cx-(e-r)),abs(cz+z))
            assert max(rotate(x,y,b,q+1e-4)[0] for x,y in left)>e-r
            # Reconstruct force equilibrium from actual contact coordinates.
            # Plate forces: (-N,-F) at contact; (+N,+F) at pivot.
            F=10; N=F/mu
            moment=(cx-b)*(-F)-cz*(-N)
            assert abs(moment)<1e-9
            assert N>0 and mu>0
            # Opposite load would require an inadmissible negative normal.
            assert (-F)/mu < 0
        checks.append({'intervals':n,'max_geometry_error':residual})

    rows=[]
    for b in (2.4,8,16,33.02):
        for label,r,a,t,actual_b,e in [
            ('nominal',.75,1.1,.4,b,0),
            ('size_only',.65,1.2,.5,b,0),
            ('coherent_weak_hold',.65,1.2,.5,b-.1,.1)]:
            q,z,mu=seat(r,a,t,actual_b,e)
            rows.append(dict(b_nominal_mm=b,case=label,angle_deg=math.degrees(q),
                             mu_min=mu,contact_drop_mm=z,normal_at_10N=10/mu))
    lever=[]
    for mu in (.1,.2,.4,.6):
        b=required_b(.65,1.2,.5,mu,.1)+.1
        assert abs(seat(.65,1.2,.5,b-.1,.1)[2]-mu)<1e-12
        lever.append(dict(mu=mu,nominal_b_required_mm=b))

    # Explicit finite y-bypass embodiment at nominal b=33.02, weak-hold batch.
    # Pivot local bias -.1, tail offset +.1. All neighbor tails use the same
    # coherent bias. They extend throughout the lock depth, a conservative grant.
    b=32.92; r=.65; e=.1; a=1.2; t=.5
    q,z,mu=seat(r,a,t,b,e)
    packing={}
    for bypass in (False,True):
        parts=solids(a,t,b,bypass)
        envs=[envelope(poly,b,q) for poly,y in parts]
        collisions=[]
        for neighbor in range(-2,10):
            if neighbor==0: continue
            rodlo=neighbor*PITCH+e-r
            rodhi=neighbor*PITCH+e+r
            for k,((poly,(ylo,yhi)),env) in enumerate(zip(parts,envs)):
                if yhi < -r or ylo > r: continue
                # Interval boxes prove separation; an overlap is only a possible
                # collision. At q=0 these rectangular prisms give exact witnesses.
                if max(x for x,z in poly)>rodlo and min(x for x,z in poly)<rodhi:
                    collisions.append([neighbor,k,'exact_open_state_intersection'])
                elif env[1]>rodlo and env[0]<rodhi:
                    collisions.append([neighbor,k,'sweep_envelope_overlap'])
        xmin=min(v[0] for v in envs); xmax=max(v[1] for v in envs)
        zmin=min(v[2] for v in envs); zmax=max(v[3] for v in envs)
        gap=.4  # Unqualified extra inter-plate spacing, NOT a process capability.
        tiers=math.ceil((xmax-xmin+gap)/PITCH)
        spacing=zmax-zmin+gap
        depth=(tiers-1)*spacing+zmax-zmin
        packing['bypass' if bypass else 'straight']=dict(collisions=collisions,
            moving_envelope_mm=[xmin,xmax,zmin,zmax],tiers=tiers,
            tier_spacing_mm=spacing,one_direction_stack_depth_mm=depth,
            two_mirrored_stacks_depth_mm=2*depth+gap)
        if bypass: assert not collisions
        else: assert collisions
        # Same-tier cells i and i+tiers are separated in x for ANY independent
        # angle. Different tiers are separated in z for ANY independent angle.
        assert tiers*PITCH > xmax-xmin
        assert spacing > zmax-zmin
    # Actual captured hinge: annulus R=.8, bore=.3, grounded axle=.3, extruded
    # in y. Ideal conformal, frictionless bearing is explicitly favorable.
    # Real bearing clearance/warp remains an unqualified change to this model.
    # Two side rails at |y|=1.9..2.4 ground the axle. Moving rails end at 1.8.
    bearing_error=0
    for j in range(257):
        theta=q*j/256
        for k in range(128):
            phi=2*math.pi*k/128
            x,zz=rotate(b+.3*math.cos(phi),.3*math.sin(phi),b,theta)
            bearing_error=max(bearing_error,abs(math.hypot(x-b,zz)-.3))
    assert bearing_error < 1e-12
    assert 1.9-1.8 > 0 and PITCH-2*2.4 > 0
    # The actual moving part is the UNION of collar, rails and boss MINUS the
    # circular bore through its full y width. The rectangles are external
    # collision envelopes. Removing the bore cannot create external interference.
    # Zero clearance/thickness limiting case gives zero holding threshold but
    # no useful release/manufacturing margin. Zero mu cannot hold any finite box.
    assert seat(.75,.75,0,2.4)[2]==0
    return dict(evidence='rigid geometry and quasistatic calculation; self-review',
                checks=checks,scenarios=rows,required_levers=lever,packing=packing,
                bearing_radius_error_mm=bearing_error,
                relaxed_centered_mu=math.sqrt(1.2**2+.25**2-.65**2)/(2.4+.65),
                nominal_open_clearance_tight_batch=.35-.1-.1-.1)


if __name__=='__main__':
    print(json.dumps(run(),indent=2))
