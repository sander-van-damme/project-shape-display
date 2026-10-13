#!/usr/bin/env python3
"""Intact-guide readback route bounds. No camera, bore or hardware qualification."""
import argparse
import importlib.util
import itertools
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location('readback', Path(__file__).with_name('readback.py'))
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
head = r.head


def end_clearance(pitch, cells, error, camera_offset=20., width=4.4):
    """Last target recessed e, preceding pin protrudes e; same-height side view.

    Camera (-offset,p/2); target ((cells-1)*p,w/2-e). At the preceding
    pin's far edge, positive clearance is necessary for this ray to pass.
    Common rigid translation cancels; alternating deviations need not.
    """
    x = (cells-1)*pitch
    edge = x-pitch+width/2
    target_y = width/2-error
    y = target_y+(pitch/2-target_y)*(x-edge)/(x+camera_offset)
    return y-(width/2+error)


def end_limit(pitch, cells):
    # Closed form of clearance=0 with only face-normal errors; no X error.
    d = pitch-2.2
    D = (cells-1)*pitch+20.
    return ((pitch-4.4)/2)*d/(2*D-d)


def end_rows():
    out=[]
    for pitch,n in ((6.35,64),(5.08,80)):
        for cells in (n, n//2, 16):
            D=(cells-1)*pitch+20.
            g=(pitch-4.4)/2
            # Angular width of a .16mm mark, normal-to-row camera near grazing.
            angular=math.atan2(g,D-.08)-math.atan2(g,D+.08)
            out.append(dict(pitch=pitch,cells=cells,error_limit_mm=end_limit(pitch,cells),
                            clearance_at_005_mm=end_clearance(pitch,cells,.05),
                            mark_radians=angular,pixels_at_f1200=angular*1200,
                            focal_pixels_for_2px=2/angular))
    return out


def axial(stroke,bore=.8,root=1.4,radial_error=.1,pupil_radius=.1,target_radius=.2):
    """Straight bore z0..S+14, camera z-10, cap underside z=S+46+u.

    Independent disk envelopes for pupil/target; line radius is bounded by
    their convex interpolation. radial_error is a combined bore/ray-axis bound
    (including straightness), not a printer distribution or a measured margin.
    """
    assert 0 < bore < root and 0 <= radial_error < bore/2
    L=stroke+14
    rows=[]
    for u in (0,stroke/2,stroke):
        Z=stroke+46+u
        D=Z+10
        radii=[pupil_radius+(target_radius-pupil_radius)*(z+10)/D for z in (0,L)]
        clearance=bore/2-radial_error-max(radii)
        # A centered point camera cone that passes the distant end of the bore.
        cone=2*math.atan2(max(0,bore/2-radial_error),L+10)
        # Optimistic stereo baseline bound at the entrance; centered cap target.
        baseline=2*max(0,bore/2-radial_error)*D/Z
        # Disparity=f*b/D; local propagated depth uncertainty D²*sigma/(f*b).
        depth_error=D*D*.1/(1200*baseline)
        focal_for_half=D*D*.1/(.5*baseline)
        rows.append(dict(u=u,cap_z_mm=Z,range_mm=D,ray_margin_mm=clearance,
                         point_camera_cone_deg=math.degrees(cone),
                         optimistic_stereo_baseline_mm=baseline,
                         depth_error_at_f1200_sigma01_mm=depth_error,
                         focal_pixels_for_half_mm=focal_for_half))
    return dict(stroke=stroke,bore=bore,root=root,root_wall_mm=(root-bore)/2,
                retained_root_I=1-(bore/root)**4,
                ideal_Euler_E1000_K1_N=math.pi**2*1000*math.pi*(root**4-bore**4)/64/(stroke+7)**2,
                bore_aspect_ratio=L/bore,rows=rows)


def axial_schedule(delta,q,read=.1,transfer=.1,index=.05,lead=3):
    """Replace E-267 proof with q parallel coaxial channels, after undocking.

    Grant routing, free selective interrogation within a field, and static hold.
    transfer includes required writer/reader exchange; index is a scenario.
    One failed station retry is recomputed using the same full station dwell.
    No global second pass or free actual-pin sensing is assumed.
    """
    base=head.schedule(delta,16,lead=lead)
    if not base['stations']:
        return dict(seconds=0.,added_s=0.,stations=0,groups=0)
    extras=[]; old_dwells=[]; new_dwells=[]; groups=0
    for _,_,selected in head.stations(delta,16):
        count=math.ceil(len(selected)/q); groups+=count
        extra=transfer+count*read+(count-1)*index-.02
        spin=head.a.r.spin(max(abs(d) for _,d in selected)/lead,850,1000)
        extras.append(extra);old_dwells.append(.1+spin);new_dwells.append(.1+spin+extra)
    added=sum(extras)+max(new_dwells)-max(old_dwells)
    return dict(seconds=base['seconds']+added,added_s=added,
                stations=base['stations'],groups=groups)


def timing():
    out=[]
    for n,S in itertools.product((64,80),(40,50)):
        local={k:d for k,d in head.local_cases(n,S).items() if any(map(any,d))}
        scenes={k:d for k,d in head.a.workloads(n).items() if S==50 or 'deep:' not in k}
        for q,transfer,index in ((16,0,0),(16,.1,.05),(4,.1,.05),(1,.1,.05)):
            def calc(d):return axial_schedule(d,q,transfer=transfer,index=index)
            times={k:calc(d) for k,d in local.items()}; worst=max(times,key=lambda k:times[k]['seconds'])
            out.append(dict(n=n,stroke=S,channels=q,read_s=.1,transfer_s=transfer,index_s=index,
                local_max_s=times[worst]['seconds'],worst=worst,worst_ledger=times[worst],
                within30=sum(v['seconds']<=30 for v in times.values()),
                scene_max_s=max(calc(d)['seconds'] for d in scenes.values()),
                cold_neutral_s=calc(head.a.c.v.s.flat(n,S-20))['seconds'],
                dense_s=calc(head.a.c.v.s.flat(n,S))['seconds']))
    return out


def checks():
    # Independent slab witness: actual straight segment through previous pin.
    for p,n in ((6.35,64),(5.08,80)):
        for count in (n,n//2,16):
            e=end_limit(p,count)
            assert abs(end_clearance(p,count,e))<1e-12
            x=(count-1)*p
            for error in (0,e*.9,e*1.1,.05):
                cam=(-20,p/2,0);target=(x,2.2-error,0)
                lo=(x-p-2.2,-2.2,-1);hi=(x-p+2.2,2.2+error,1)
                hit=r.old.hit_box(cam,target,lo,hi)
                assert hit==(end_clearance(p,count,error)<0)
    # Finite-bore continuous envelope: affine ray/axis -> convex norm; endpoints suffice.
    checked=0
    for S,b in itertools.product((40,50),(.8,1.,1.2)):
        a=axial(S,bore=b)
        for row in a['rows']:
            D=row['range_mm'];L=S+14
            # Independent central-difference disparity derivative, fixed baseline.
            B=row['optimistic_stereo_baseline_mm'];h=.001
            derivative=(1200*B/(D-h)-1200*B/(D+h))/(2*h)
            assert math.isclose(.1/derivative,row['depth_error_at_f1200_sigma01_mm'],rel_tol=1e-8)
            for theta,phi in itertools.product(range(0,360,30),repeat=2):
                c=(.1*math.cos(math.radians(theta)),.1*math.sin(math.radians(theta)))
                t=(.2*math.cos(math.radians(phi)),.2*math.sin(math.radians(phi)))
                for z in (0,L/4,L/2,3*L/4,L):
                    s=(z+10)/D
                    rad=math.hypot(*(c[i]+s*(t[i]-c[i]) for i in range(2)))
                    assert rad+.1<=b/2-row['ray_margin_mm']+1e-12
                    checked+=1
        # Direct numerical polar area integral independently checks root inertia.
        R=1.4/2;ri=b/2;N=10000;dr=(R-ri)/N
        integrated=sum(math.pi*(ri+(i+.5)*dr)**3*dr for i in range(N))
        assert math.isclose(integrated,math.pi*(1.4**4-b**4)/64,rel_tol=1e-8)
    # Distance target changes while a blocked bore must remain unknown.
    assert axial(50)['rows'][0]['cap_z_mm']!=axial(50)['rows'][-1]['cap_z_mm']
    # Dense and mixed station accounting against independent constant-slot scheduler.
    cases=[[[30 if x==y else 0 for x in range(16)] for y in range(16)],[[30]*16 for _ in range(16)]]
    for d in cases:
        assert math.isclose(axial_schedule(d,16,read=.02,transfer=0,index=0)['seconds'],head.schedule(d,16)['seconds'])
        assert math.isclose(axial_schedule(d,16)['seconds'],head.schedule(d,16,extra_dock=.18)['seconds'])
    d=[[30]*16 for _ in range(16)]
    # q1:16 reads +15 indexes +transfer instead of .02, paid at16 stations+retry.
    extra=.1+16*.1+15*.05-.02
    assert math.isclose(axial_schedule(d,1)['added_s'],17*extra)
    assert axial_schedule([[0]*16 for _ in range(16)],1)['seconds']==0
    return dict(finite_ray_samples=checked,checks='independent slab witness, exact face-error root, circular-section integration, continuous bore envelope, proof replacement and serial dense retry')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');args=p.parse_args()
    v=checks()
    if args.check: print(json.dumps(v));return
    print(json.dumps(dict(verification=v,end_view=end_rows(),axial=[axial(S,bore=b) for S,b in itertools.product((40,50),(.8,1.,1.2))],timing=timing()),indent=2))

if __name__=='__main__':main()
