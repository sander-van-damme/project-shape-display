#!/usr/bin/env python3
"""Bounded underside-corner optical access; no manufactured/sensor qualification.

Units mm. Solid screws radius1.6, square pins4.4, nut bottom z2+u,
intact lower guide bottom S+4. Entrance pupils at z-10, thrust plate -2..0.
All e terms are independently adverse axis-wise bounds, NOT process priors.
"""
import argparse
import itertools as it
import json
import math
import intact_routes as routes


def interpolate(c,t,z):
    a=(z-c[2])/(t[2]-c[2])
    return tuple(c[i]+a*(t[i]-c[i]) for i in range(2))


def axis_distance(c,t,x,y):
    """Exact closest XY distance along a segment to a vertical axis."""
    vx,vy=t[0]-c[0],t[1]-c[1]
    den=vx*vx+vy*vy
    k=0. if den==0 else max(0.,min(1.,((x-c[0])*vx+(y-c[1])*vy)/den))
    return math.hypot(c[0]+k*vx-x,c[1]+k*vy-y)


def screen(p,S,b,e,depth=10.,pupil=.05,target=2.,patch=.1):
    """Two entrance pupils tangent to the diagonal; rectangular outer envelope.

    Envelope corners enclose both pupils including independent lateral error.
    Target is an integral underside patch, not a glued flag. Target lateral
    error and plate/neighbor error can be coherent or opposing. Aperture radius
    is rounded up separately by the caller if an embodiment is later chosen.
    """
    d=b/(2*math.sqrt(2)); m=p/2
    cameras=[(m+s*d+dx,m-s*d+dy,-depth)
             for s in (-1,1) for dx,dy in it.product((-pupil-e,pupil+e),repeat=2)]
    targets=[(target+dx,target+dy,2+u) for u in (0,S)
             for dx,dy in it.product((-patch-e,patch+e),repeat=2)]
    # Norm of affine rays on plate slab is convex: endpoints suffice. The norm
    # is also convex over each input rectangle; all endpoint corners suffice.
    aperture=max(math.hypot(q[0]-m+ex,q[1]-m+ey)
                 for c,t,z,ex,ey in it.product(cameras,targets,(-2,0),(-e,e),(-e,e))
                 for q in [interpolate(c,t,z)])
    # For all possible neighbor heights, their union starts at z2. Segment above
    # z2 stays within a rectangle. Keep it below neighboring near faces on both
    # axes, sufficient even for an arbitrary neighbor-height pattern.
    max_xy=max(max(*interpolate(c,t,2),t[0],t[1]) for c,t in it.product(cameras,targets))
    neighbor=p-2.2-e-max_xy
    # Both coordinates positive and >= min endpoint throughout screw region;
    # this deliberately overbounds the screw with an infinite cylinder.
    min_xy=min(min(c[0],c[1],t[0],t[1]) for c,t in it.product(cameras,targets))
    screw=math.sqrt(2)*min_xy-(1.6+e)
    # Seat/hole edges can each move adversely e. Optical aperture above already
    # includes an independent e displacement, not a manufactured radius guarantee.
    seat=p/math.sqrt(2)-(2.2+e)-(aperture+e)
    journal=p/math.sqrt(2)-(1.8+e)-(aperture+e)
    shoulder=min(axis_distance(c,t,ix*p,iy*p)-(2.2+e)
                 for c,t,ix,iy in it.product(cameras,targets,(-1,0,1),(-1,0,1)))
    D=S+2+depth
    # Ideal active triangulation/stereo sensitivity; two rays must identify the
    # same projected spot. f and pixel error are explicit assumptions.
    uncertainty=D*D*.1/(1200*b)
    return dict(pitch=p,stroke=S,baseline=b,error=e,
                required_aperture_diameter=2*aperture,neighbor_margin=neighbor,
                pupil_diameter=2*pupil,airy_radius_550nm=1.22*.00055*D/(2*pupil),
                screw_margin=screw,shoulder_cylinder_margin=shoulder,full_seat_ligament=seat,journal_ligament=journal,
                guide_clearance_z=(S+4)-(S+2),
                depth_error_f1200_sigma01=uncertainty,
                guide_web=p-4.64,ray_count=len(cameras)*len(targets),
                cameras=cameras,targets=targets)


def checks():
    count=0
    for p,S,b,e,pupil in it.product((6.35,5.08),(40,50),(.5,1.,2.),(0,.1,.2),(.05,.25)):
        a=screen(p,S,b,e,pupil=pupil)
        # Sampled independent exact slab intersections against eight neighbors,
        # every combination of low/high poses is covered by their full envelope.
        for c,t in it.product(a['cameras'],a['targets']):
            for ix,iy in it.product((-1,0,1),repeat=2):
                if ix==iy==0:continue
                lo=(ix*p-2.2-e,iy*p-2.2-e,2)
                hi=(ix*p+2.2+e,iy*p+2.2+e,2*S+48)
                if a['neighbor_margin']>0:
                    assert not routes.r.old.hit_box(c,t,lo,hi)
                count+=1
            # Independent interior ray sampling cannot exceed plate-end envelope.
            for z in (-2,-1.5,-1,-.5,0):
                x,y=interpolate(c,t,z)
                for ex,ey in it.product((-e,e),repeat=2):
                    assert math.hypot(x-p/2+ex,y-p/2+ey)<=a['required_aperture_diameter']/2+1e-12
        D=S+12;eps=.001
        derivative=(1200*b/(D-eps)-1200*b/(D+eps))/(2*eps)
        assert math.isclose(.1/derivative,a['depth_error_f1200_sigma01'],rel_tol=1e-8)
    # Positive coarse access; fine margin lost before adding mounting/optic body.
    assert screen(6.35,50,2.,.1)['neighbor_margin']>0
    assert screen(5.08,50,.5,.1)['neighbor_margin']>0
    assert screen(5.08,50,.5,.2)['neighbor_margin']<0
    assert screen(6.35,50,2.,.1,pupil=.25)['full_seat_ligament']>0
    assert screen(6.35,50,2.,.1,pupil=.25)['shoulder_cylinder_margin']>0
    assert math.isclose(axis_distance((0,0,0),(2,0,3),1,1),1.)
    assert screen(6.35,50,2.,.2,pupil=.25)['full_seat_ligament']<0
    assert screen(5.08,50,.5,.1,pupil=.25)['neighbor_margin']<0
    assert math.isclose(screen(6.35,50,2.,.1,pupil=.25)['airy_radius_550nm'],.083204)
    # Concrete high-target/low-neighbor collision, beyond conservative rejection.
    a=screen(5.08,50,2.,.1)
    assert any(routes.r.old.hit_box(c,t,(5.08-2.3,-2.3,2),(5.08+2.3,2.3,98))
               for c,t in it.product(a['cameras'],a['targets']) if t[2]==52)
    # A lifted blind target can alias a separated cap; actual nut position is
    # adequate only while the integral pin is intact. No read proves retention.
    return dict(neighbor_slab_checks=count,convex_plate_bound=True,
                disparity_derivative=True,explicit_neighbor_collision=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true');args=parser.parse_args()
    verification=checks()
    if args.check: print(json.dumps(verification));return
    rows=[]
    for p,S,b,e,pupil in it.product((6.35,5.08),(40,50),(.5,1.,2.),(0,.1,.2),(.05,.25)):
        a=screen(p,S,b,e,pupil=pupil);a.pop('cameras');a.pop('targets');rows.append(a)
    print(json.dumps(dict(verification=verification,rows=rows),indent=2))

if __name__=='__main__':main()
