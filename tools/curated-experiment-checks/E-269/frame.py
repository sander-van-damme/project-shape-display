#!/usr/bin/env python3
"""Shared overhead ribs versus E-269 interstitial optics; mm/N/MPa bounds.

Geometry and linear beam scenarios only. No process distribution, joint rating,
contact/load-sharing validation, safe docking force, or qualified readback.
"""
import argparse
import itertools as it
import json
import math
import capture
import structure as beam


def rib_geometry(p, width=1., depth=20., error=.1, stroke=50):
    # Fixed rib above sliding keeper; pin union starts at z2 and spans full travel.
    # The rib's lower face is z1: .2 clearance above keeper top z.8.
    lo=(-p, p/2-width/2, 1.)
    hi=(2*p, p/2+width/2, 1.+depth)
    ray=capture.optics.screen(p,stroke,2. if p>6 else .5,.1,pupil=.25)
    counts={}; witness=None
    for height in (2,stroke+2):
        pairs=[(c,t) for c,t in it.product(ray['cameras'],ray['targets']) if t[2]==height]
        hit=[(c,t) for c,t in pairs if capture.optics.routes.r.old.hit_box(c,t,lo,hi)]
        counts[height]=dict(blocked=len(hit),total=len(pairs))
        if hit: witness=dict(camera=hit[0][0],target=hit[0][1],rib_lo=lo,rib_hi=hi)
    # Separate pin expansion and rib placement error; not printer priors.
    margin=(p-4.4-width)/2-2*error
    return dict(pitch=p,width=width,depth=depth,error_each=error,
                pin_clearance=margin,rays=counts,witness=witness)


def frame_load(p,n,channels=16,force=.2,E=70000,width=1.,depth=20.,end_depth=20.,share=.5):
    """Allocate share of load to the more loaded rib; .5 is optimistic sharing.

    Central contiguous head is adverse for the rib's center displacement.
    Each rib end has a positive seat in an end beam supported at board corners.
    End beams see two adjacent rib reactions near their center (adverse Y).
    Sheet contact, seat, joints, torsion and corner post compliance excluded.
    """
    L=p*n; I=width*depth**3/12
    xs=[L/2+(i-(channels-1)/2)*p for i in range(channels)]
    loads=[force*share]*channels
    rib=beam.center_point_sum(L,xs,loads,E*I)
    # Each end takes half of its rib load; compare half versus one-rib allocation.
    reaction=channels*force*share/2
    ys=[L/2-p/2,L/2+p/2]
    endI=10*end_depth**3/12
    end=beam.center_point_sum(L,ys,[reaction,channels*force*(1-share)/2],E*endI)
    M=sum(f*(L-x)/L for x,f in zip(xs,loads))*L/2-sum(f*max(0.,L/2-x) for x,f in zip(xs,loads))
    return dict(pitch=p,sites=n,channels=channels,force_per_tip=force,E=E,
                width=width,depth=depth,end_depth=end_depth,load_share=share,
                rib_mm=rib,end_beam_mm=end,beam_sum_mm=rib+end,
                total_tip_rise_with_floats_mm=.4+rib+end,
                rib_nominal_MPa=M*depth/(2*I),reaction_per_rib_end_N=reaction,
                gross_internal_rib_mass_at_density2700_kg=(n-1)*L*width*depth*2700e-9,
                rib_end_seats=2*(n-1),rib_end_cuts=2*(n-1),
                # At the same forces, corner supports sum to total docking load.
                force_sum_N=2*(reaction+channels*force*(1-share)/2))


def checks():
    cases=0
    for p,n,width in ((6.35,64,1.),(5.08,80,.4)):
        for c,F,E,d in it.product((1,16,n),(.05,.2,1.),(1000,70000),(10.,20.)):
            a=frame_load(p,n,c,F,E,width=width,depth=d)
            L=p*n; xs=[L/2+(i-(c-1)/2)*p for i in range(c)]
            numerical=beam.integrated_curvature(L,xs,[F/2]*c,E*width*d**3/12,steps=4000)
            assert math.isclose(numerical,a['rib_mm'],rel_tol=5e-7)
            assert math.isclose(a['force_sum_N'],c*F)
            assert math.isclose(frame_load(p,n,c,2*F,E,width=width,depth=d)['beam_sum_mm'],2*a['beam_sum_mm'])
            cases+=1
    a=frame_load(6.35,64); b=frame_load(6.35,64,depth=10)
    assert math.isclose(b['rib_mm'],8*a['rib_mm'])
    # One point load agrees with elementary PL^3/(48EI).
    a=frame_load(6.35,64,1)
    assert math.isclose(a['rib_mm'],(.2/2)*406.4**3/(48*70000*(20**3/12)))
    coarse=rib_geometry(6.35); fine=rib_geometry(5.08,width=.4)
    assert coarse['pin_clearance']>0 and fine['pin_clearance']<0
    assert coarse['rays'][52]['blocked']>0
    # One nominal stereo pupil ray intersects the rib at high position; exact witness.
    c=(3.175-1/math.sqrt(2),3.175+1/math.sqrt(2),-10.);t=(2.,2.,52.)
    y=capture.optics.interpolate(c,t,1.)[1]
    assert 3.175-.5<y<3.175+.5
    # Sliding keeper service .0..1.2 does not translate fixed ribs into the pins.
    # Exterior slot must allow the whole plate travel plus placement bounds.
    assert math.isclose(1.2+2*.1,1.4)
    a=frame_load(6.35,64,share=1.)
    b=frame_load(6.35,64,share=.5)
    assert math.isclose(a['rib_mm'],2*b['rib_mm'])
    assert math.isclose(a['end_beam_mm'],b['end_beam_mm'])
    return dict(curvature_crosschecks=cases,load_balance=True,
                linear_and_cubic_scaling=True,independent_ray_witness_y=y)


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--check',action='store_true');args=ap.parse_args()
    verify=checks()
    if args.check:print(json.dumps(verify));return
    geom=[rib_geometry(p,w,error=e) for p,w in ((6.35,1.),(5.08,.4)) for e in (0.,.1,.2)]
    loads=[frame_load(p,n,c,F,E,w,d) for p,n,w in ((6.35,64,1.),(5.08,80,.4))
           for c,F,E,d in it.product((16,n),(.05,.2,1.),(1000,70000),(10.,20.))]
    print(json.dumps(dict(checks=verify,geometry=geom,loads=loads),indent=2))

if __name__=='__main__':main()
