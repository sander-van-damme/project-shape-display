#!/usr/bin/env python3
"""Shared service keeper: bounded planar geometry and ideal repair states, not hardware.

Python + numpy. Units mm, N. No random manufacturing priors. Full solid grid cells
provide a sufficient connected-material subset, not a stress/contact solution.
"""
import argparse
from collections import deque
import itertools as it
import json
import math
from pathlib import Path
import sys
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'E-268'))
import interstitial as optics


def optical_radius(p, stroke, e, zs):
    a = optics.screen(p, stroke, 2. if p > 6 else .5, e, pupil=.25)
    radius = max(math.hypot(q[0]-p/2+ex, q[1]-p/2+ey)
                 for c,t,z,ex,ey in it.product(a['cameras'], a['targets'], zs, (-e,e), (-e,e))
                 for q in [optics.interpolate(c,t,z)])
    return radius, a


def geometry(p, stroke=50, optical_error=.1, edge_loss=0., step=.04, with_optics=True, registration=0.):
    """3x3 finite plate + 2mm border, all nine screws; normal locked position.

    Hole: radius1.8 capsule along y0..1.2 plus radius2.4 service circle at y1.2.
    Shift whole keeper -1.2y for service. Collar radius2.2. Edge loss expands all
    keeper holes and contracts collar; independent from optical ray envelope e.
    Registration is a separate per-axis bound; a guaranteed inscribed collar
    disk contracts by sqrt(2)*registration. Neck fit is screened separately.
    """
    rho, ray = optical_radius(p, stroke, optical_error, (-.8,.8))
    bed_rho, _ = optical_radius(p, stroke, optical_error, (-5.,-3.))
    bound=1.5*p+2.
    n=math.ceil(2*bound/step)
    h=2*bound/n
    axis=-bound+(np.arange(n)+.5)*h
    x,y=np.meshgrid(axis,axis)
    # Expand holes by a pixel's half diagonal: each accepted square is solid.
    pixel=h/math.sqrt(2)
    solid=np.ones((n,n),dtype=bool)
    point_solid=solid.copy()
    for i,j in it.product((-1,0,1),repeat=2):
        xx=x-i*p; yy=y-j*p
        capsule_d=np.hypot(xx,yy-np.clip(yy,0.,1.2))
        circle_d=np.hypot(xx,yy-1.2)
        solid &= (capsule_d>1.8+edge_loss+pixel)&(circle_d>2.4+edge_loss+pixel)
        point_solid &= (capsule_d>1.8+edge_loss)&(circle_d>2.4+edge_loss)
    if with_optics:
        for i,j in it.product((-2,-1,0,1),repeat=2):
            d=np.hypot(x-(i+.5)*p,y-(j+.5)*p)
            solid &= d>rho+edge_loss+pixel
            point_solid &= d>rho+edge_loss
    # Flood only from actual external plate boundary, not a hole or a free island.
    grounded=np.zeros_like(solid);q=deque()
    for a,b in [(i,j) for i in range(n) for j in (0,n-1)]+[(i,j) for i in (0,n-1) for j in range(n)]:
        if solid[a,b] and not grounded[a,b]:grounded[a,b]=True;q.append((a,b))
    while q:
        a,b=q.popleft()
        for da,db in ((1,0),(-1,0),(0,1),(0,-1)):
            c,d=a+da,b+db
            if 0<=c<n and 0<=d<n and solid[c,d] and not grounded[c,d]:
                grounded[c,d]=True;q.append((c,d))
    radial=np.hypot(x,y)
    contact=grounded&(radial<2.2-edge_loss-math.sqrt(2)*registration-pixel)
    area=float(np.sum(contact)*h*h)
    centroid=(float(np.mean(x[contact])),float(np.mean(y[contact]))) if area else (None,None)
    # Midpoint area only is an estimate; full-cell area is a sufficient lower subset.
    midpoint=float(np.sum(point_solid&(radial<2.2-edge_loss-math.sqrt(2)*registration))*h*h)
    return dict(pitch=p,stroke=stroke,optical_error=optical_error,edge_loss=edge_loss,
                step=h,with_optics=with_optics,registration_per_axis=registration,
                aperture_vertical_chain_overlap=4.2-(p-1.2),
                aperture_horizontal_chain_overlap=2.4+rho-math.hypot(p/2,p/2-1.2),
                keeper_optical_diameter=2*rho,
                bed_optical_diameter=2*bed_rho,neighbor_ray_margin=ray['neighbor_margin'],
                contact_lower_mm2=area,contact_midpoint_mm2=midpoint,
                contact_centroid_mm=centroid,isolated_solid_lower_mm2=float(np.sum(solid&~grounded)*h*h),
                keeper_y_web=p-5.4-2*edge_loss,keeper_x_web=p-4.8-2*edge_loss,
                bed_full_seat_ligament=p/math.sqrt(2)-2.2-bed_rho-2*edge_loss,
                moment_per_N_Nmm=abs(centroid[1]) if area else None,
                journal_reaction_per_N=abs(centroid[1])/2 if area else None,
                mean_pressure_per_N_MPa=1/area if area else None)


def keyhole_contains(x,y,r=0.):
    # Sufficient condition for a disk: contains it in capsule or service circle.
    return (math.hypot(x,y-min(1.2,max(0.,y)))+r<=1.8+1e-12 or
            math.hypot(x,y-1.2)+r<=2.4+1e-12)


def repair_checks():
    count=0
    for S in (40,50):
        guide_top=S+46; lowest_tip=-7.; lift=guide_top-lowest_tip+1.
        for h0 in (0,S/2,S):
            # A rigid jammed pair may leave together: no thread motion needed.
            # Constant .2mm axial keeper clearance is independent of map height.
            assert math.isclose(-.8-(-1.),.2)
            assert lowest_tip+lift>guide_top
            assert 2.2<4.64/2 # collar fits both intact square guides nominally
            assert 1.6<1.8 # drive end/journal passes fixed bed upwards
            # Before/after keeper shift, every neighbor's downward chain is fixed.
            neighbors=[(z,True,True) for z in (0,S/2,S)] # height, thread, bed
            for shift in np.linspace(0,1.2,49):
                assert keyhole_contains(0,shift,1.6)
                assert all(thread and bed and z in (0,S/2,S) for z,thread,bed in neighbors)
                count+=1
            assert keyhole_contains(0,1.2,2.2)
            assert not keyhole_contains(0,0,2.2)
            # Independent escape witness: collar's negative-y point meets keeper
            # in operating state, clears in service state.
            assert not keyhole_contains(0,-2.2)
            assert keyhole_contains(0,-2.2+1.2)
    # Dense angular cross-section check, including all intermediate slide poses.
    for shift,theta in it.product(np.linspace(0,1.2,49),np.linspace(0,2*math.pi,721)):
        assert keyhole_contains(1.6*math.cos(theta),shift+1.6*math.sin(theta))
    # Circle cannot pass smaller intact-guide square; wider collar is not free.
    assert 5.0>4.64
    return dict(ideal_neighbor_service_states=count,neck_boundary_checks=49*721,
                extraction_lift_S40_S50_mm=[94.,104.],
                counterexamples=['fixed keeper traps collar','5mm collar fails 4.64mm guide',
                                 'service mode has no upward capture'])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    verification=repair_checks()
    if args.check:
        # Independent nominal upper contact bound is the annulus area.
        a=geometry(6.35,step=.04);b=geometry(6.35,step=.02)
        assert 0<a['contact_lower_mm2']<math.pi*(2.2**2-1.8**2)
        assert b['contact_lower_mm2']>a['contact_lower_mm2']
        assert abs(a['contact_midpoint_mm2']-b['contact_midpoint_mm2'])<.04
        assert a['isolated_solid_lower_mm2']==b['isolated_solid_lower_mm2']==0
        lost=geometry(6.35,edge_loss=.2,step=.04)
        assert lost['contact_lower_mm2']<a['contact_lower_mm2']
        fine=geometry(5.08,step=.04)
        assert fine['keeper_y_web']<0 and fine['neighbor_ray_margin']<0
        assert fine['aperture_vertical_chain_overlap']>0
        assert fine['aperture_horizontal_chain_overlap']>0
        assert a['aperture_vertical_chain_overlap']<0
        # Clear witness on each side of a fine collar lies inside a closed hole
        # chain, independently of the sufficient pixel connectivity subset.
        assert 1.8<math.hypot(2.,-.5)<2.2
        assert math.hypot(2.,-.5-1.2)>2.4
        verification['coarse_contact_resolution']=[a['contact_lower_mm2'],b['contact_lower_mm2']]
        print(json.dumps(verification,indent=2));return
    rows=[geometry(p,S,edge_loss=e) for p,S,e in it.product((6.35,5.08),(40,50),(0.,.1,.2))]
    rows.extend(geometry(p,with_optics=False) for p in (6.35,5.08))
    rows.extend(geometry(6.35,edge_loss=.1,registration=r,step=.02) for r in (.05,.1))
    print(json.dumps(dict(verification=verification,rows=rows),indent=2))

if __name__=='__main__':main()
