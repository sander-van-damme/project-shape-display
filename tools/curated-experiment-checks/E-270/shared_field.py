#!/usr/bin/env python3
"""Finite shared stereo field. Geometry/error scenarios, NOT a camera qualification."""
import argparse
import importlib.util
import itertools
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location('verification', Path(__file__).with_name('verification.py'))
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


def optics(pitch, stroke, count, distance, baseline, error=.2, pixels=1920, disparity_error=.1, pupil=.5):
    # Two parallel vertical pinhole cameras, optical centers +/-baseline/2.
    # Both must image the complete row at every height. Distance is from lowest cap.
    width = (count-1)*pitch
    t = stroke/distance
    margin = pitch-2.2-2*error-((width+baseline)/2+pupil/2)*t-.2*(1-t)
    # Nearest caps set FOV, farthest caps set disparity sensitivity. 10% pixel reserve.
    focal = .9*pixels*(distance-stroke)/(width+baseline+.4+2*error)
    disparity = focal*baseline/distance
    # Exact one-sided worst depth error, not just first-order derivative.
    dz = distance*disparity_error/(disparity-disparity_error) if disparity>disparity_error else math.inf
    return dict(margin_mm=margin, focal_px=focal, depth_error_mm=dz,
                patch_pixels=focal*.4/distance, low_disparity_px=disparity,
                overhead_mm=distance-stroke, airy_radius_mm=1.22*.00055*distance/pupil)


def project(x,z,camera_x,distance,focal):
    return focal*(x-camera_x)/(distance-z)


def reconstruct(left,right,distance,baseline,focal):
    depth = focal*baseline/(left-right)
    return ((left+right)*depth/(2*focal), distance-depth)


def envelope_checks():
    # Independent exact slab intersections for finite pupils and patch corners.
    # Endpoint cells bound horizontal off-axis distance; intermediate ones checked too.
    rays=0
    for p,S,k,D,b in itertools.product((5.08,6.35),(40,50),(4,16),(150,600,1000),(12,40)):
        all_clear=True
        for i in range(k):
            x=(i-(k-1)/2)*p
            for side,px,py,tx,ty in itertools.product((-1,1),repeat=5):
                # Choose opposing error corners in each transverse dimension.
                for ex,ey in itertools.product((-1,1),repeat=2):
                    camera=(side*b/2+px*.25+ex*.2,py*.25+ey*.2,D)
                    target=(x+tx*.2+ex*.2,ty*.2+ey*.2,0)
                    for dx,dy in itertools.product((-1,0,1),repeat=2):
                        if dx==dy==0: continue
                        lo=(x+dx*p-2.4,dy*p-2.4,0)
                        hi=(x+dx*p+2.4,dy*p+2.4,S)
                        all_clear &= not v.r.old.hit_box(camera,target,lo,hi)
                        rays+=1
        assert all_clear == (optics(p,S,k,D,b)['margin_mm']>0),(p,S,k,D,b)
    return rays


def reconstruction_checks():
    samples=0
    for p,S,k,D,b in itertools.product((5.08,6.35),(40,50),(4,8,16),(300,600,1000),(12,30,40)):
        o=optics(p,S,k,D,b);f=o['focal_px']
        for i,z in itertools.product(range(k),(0,S/3,S)):
            x=(i-(k-1)/2)*p
            left=project(x,z,-b/2,D,f);right=project(x,z,b/2,D,f)
            xx,zz=reconstruct(left,right,D,b,f)
            assert math.isclose(xx,x,abs_tol=1e-9) and math.isclose(zz,z,abs_tol=1e-9)
            assert max(abs(left),abs(right))<=1920/2
            for el,er in itertools.product((-.05,.05),repeat=2):
                _,zz=reconstruct(left+el,right+er,D,b,f)
                assert abs(zz-z)<=o['depth_error_mm']+1e-9
                samples+=1
    # Repeated cap texture: wrong right-image neighbor produces a plausible height.
    # z=0, right correspondence is one pitch to the left: disparity grows.
    p,D,b,f=6.35,300.,40.,5000.
    left=project(0,0,-b/2,D,f);right=project(-p,0,b/2,D,f)
    x,z=reconstruct(left,right,D,b,f)
    assert 0<z<50 and abs(z-D*p/(b+p))<1e-9
    # Its inferred x is off-lattice; geometry gating can reject this witness.
    # A common camera/grid translation by exactly one pitch instead preserves
    # all lattice residuals while silently assigning each reconstruction wrong.
    assert math.isclose(project(p,20,p-b/2,D,f),project(0,20,-b/2,D,f))
    # A paired geometry model alone cannot resolve a mistaken frame registration.
    return dict(samples=samples,wrong_neighbor_height_mm=z,wrong_neighbor_x_mm=x)


def grouped_schedule(delta,stroke,group,read=.1):
    """One camera pair visits group centers within each existing 16-output station.

    Starts at first group center, pays movement to occupied groups and return;
    .1s settle per visited group, .1s frame sequence allocation, .1s undock once.
    Base macro motion remains granted from E-270: tall-carrier acceleration unqualified.
    """
    if 16%group: raise ValueError('group must divide 16')
    base=v.h.schedule(delta,16)
    if not base['stations']: return dict(seconds=0.,proof_s=0.)
    pitch=406.4/len(delta);extras=[];retries=[];proofs=[]
    for x,y,selected in v.h.stations(delta,16):
        groups=sorted({(col-x)//group for col,_ in selected})
        pos=0;travel=0.
        for g in groups+[0]:
            if g!=pos: travel+=max(.05,v.h.a.r.move(abs(g-pos)*group*pitch))
            pos=g
        proof=.1+len(groups)*(.1+read)+travel
        extra=proof-.02
        proofs.append(proof);extras.append(extra)
        retries.append(.1+v.h.a.r.spin(stroke/3,850,1000)+extra)
    return dict(seconds=base['seconds']+1+sum(extras)+max(retries)-base['retry_s'],
                proof_s=sum(proofs))


def timing():
    out=[]
    for n,S in itertools.product((64,80),(40,50)):
        local={k:d for k,d in v.h.local_cases(n,S).items() if any(map(any,d))}
        scenes={k:d for k,d in v.h.a.workloads(n).items() if S==50 or 'deep:' not in k}
        for group in (4,8,16):
            out.append(dict(n=n,stroke=S,group=group,
                local_max_s=max(grouped_schedule(d,S,group)['seconds'] for d in local.values()),
                scene_max_s=max(grouped_schedule(d,S,group)['seconds'] for d in scenes.values()),
                neutral_s=grouped_schedule(v.h.a.c.v.s.flat(n,S-20),S,group)['seconds'],
                dense_s=grouped_schedule(v.h.a.c.v.s.flat(n,S),S,group)['seconds']))
    return out


def checks():
    rays=envelope_checks(); recon=reconstruction_checks()
    d=[[0]*64 for _ in range(64)];d[0][0]=10;d[0][15]=-20;d[10][20]=30
    for S in (40,50):
        assert math.isclose(grouped_schedule(d,S,16)['seconds'],v.schedule(d,S,'stereo16')['seconds'])
        assert grouped_schedule(d,S,4)['seconds']>grouped_schedule(d,S,8)['seconds']>grouped_schedule(d,S,16)['seconds']
    for g in (4,8,16):
        assert grouped_schedule([[0]*64 for _ in range(64)],50,g)['seconds']==0
        assert grouped_schedule(d,50,g)['seconds']==grouped_schedule([[-a for a in row] for row in d],50,g)['seconds']
    # Diffraction aperture tradeoff: increasing pupil improves ideal resolution
    # while consuming the same finite access margin. Not a centroid noise model.
    narrow=optics(6.35,50,16,1000,40)
    wide=optics(6.35,50,16,1000,40,pupil=3.4)
    assert narrow['airy_radius_mm']>1 and wide['airy_radius_mm']<.2
    assert 0<wide['margin_mm']<narrow['margin_mm']
    # Coarse extreme-field wider-pupil corner witness crosscheck.
    x=7.5*6.35
    for px,py,tx,ty in itertools.product((-1,1),repeat=4):
        camera=(-20+px*1.7-.2,py*1.7+.2,1000)
        target=(x+tx*.2-.2,ty*.2+.2,0)
        for dx,dy in itertools.product((-1,0,1),repeat=2):
            if dx==dy==0: continue
            assert not v.r.old.hit_box(camera,target,
                (x+dx*6.35-2.4,dy*6.35-2.4,0),
                (x+dx*6.35+2.4,dy*6.35+2.4,50))
    return dict(ray_box_checks=rays,reconstruction=recon,
                wider_pupil=wide, calibration_scale_0p1pct_mm=1000*.001,
                relative_yaw_10urad_mm=1000**2*1e-5/40)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    result=checks()
    if not args.check:
        result['fields']=[dict(pitch=p,stroke=S,count=k,distance=D,baseline=b,**optics(p,S,k,D,b))
            for p,S in itertools.product((6.35,5.08),(40,50))
            for k,D,b in ((4,300,16),(8,600,30),(16,600,40),(16,1000,40),(16,1000,12))]
        result['timing']=timing()
    print(json.dumps(result,indent=2))
