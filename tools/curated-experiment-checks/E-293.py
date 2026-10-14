#!/usr/bin/env python3
"""Finite opaque pit versus triangulation baseline; bounds, not measured optics."""
import importlib.util
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location("optics", Path(__file__).with_name("E-292.py"))
optics = importlib.util.module_from_spec(spec)
spec.loader.exec_module(optics)
D, DQ, APERTURE = 300., .0005, 1.927
GRIDS = [(5.08, 4.4, 6400), (6.35, 4.4, 4096), (12.7, 10.3, 1024)]


def height_bin(b, z=0):
    return (D-z)**2*DQ/(b+(D-z)*DQ)


def footprint(p, w, h, b, angle, z=0, inward=0, registration=0, offset=(0.,0.)):
    # Both pupils must see the same cap patch. Circular pupils share an assumed
    # diameter; checking extreme x/y support exactly bounds their square-well rays.
    t = (h-z)/(D-z)
    a = p-w/2-inward
    widths=[]
    for f,c in zip((math.cos(angle), math.sin(angle)),offset):
        half=(a-t*(abs(b*f)/2+APERTURE/2))/(1-t)-registration
        center=t*c/(1-t)
        widths.append(max(0., min(w/2,center+half)-max(-w/2,center-half)))
    return dict(widths_mm=widths, fraction=math.prod(widths)/w**2)



def ray_hits_box(start, end, low, high):
    # Independent slab intersection; cap endpoints are excluded.
    near, far = 1e-9, 1-1e-9
    for s,e,lo,hi in zip(start,end,low,high):
        d=e-s
        if abs(d)<1e-14:
            if not lo<=s<=hi: return False
        else:
            aa,bb=sorted(((lo-s)/d,(hi-s)/d))
            near,far=max(near,aa),min(far,bb)
            if near>far: return False
    return True


def check_geometry():
    checked=0
    gap_escapes=0
    for p,w,_ in GRIDS:
        for h in (40.,50.):
            boxes=[((i*p-w/2,j*p-w/2,-1),(i*p+w/2,j*p+w/2,h))
                   for i in (-1,0,1) for j in (-1,0,1) if i or j]
            for b in (8.,45.,90.):
                for angle in (0.,math.pi/4):
                    u=(math.cos(angle),math.sin(angle))
                    # The inscribed square opening is sufficient, not necessary:
                    # actual column gaps can admit additional off-center rays.
                    # Validate clear rectangles and central blocking separately.
                    for ix in range(-4,5):
                        for iy in range(-4,5):
                            x,y=ix*w/10,iy*w/10
                            t=h/D; a=p-w/2
                            analytic=all((1-t)*abs(v)+t*(abs(b*f)/2+APERTURE/2)<a
                                         for v,f in zip((x,y),u))
                            blocked=False
                            for sign in (-1,1):
                                for dx,dy in ((APERTURE/2,0),(-APERTURE/2,0),(0,APERTURE/2),(0,-APERTURE/2)):
                                    end=(sign*b*u[0]/2+dx,sign*b*u[1]/2+dy,D)
                                    blocked |= any(ray_hits_box((x,y,0),end,lo,hi) for lo,hi in boxes)
                            assert not analytic or not blocked, (p,h,b,angle,x,y)
                            gap_escapes += (not analytic and not blocked)
                            if ix==iy==0:
                                assert analytic == (not blocked)
                            checked+=1
    # Flat terrain has no neighbor occlusion; zero baseline gives no height info.
    assert footprint(5.08,4.4,0,90,0)['fraction']==1
    assert abs(height_bin(0)-D)<1e-12
    return checked,gap_escapes


def main():
    checked,gap_escapes=check_geometry()
    rows=[]
    for p,w,n in GRIDS:
        for h in (40.,50.):
            for b in (8.,45.,90.):
                for degrees in (0,45):
                    r=dict(pitch=p,width=w,cells=n,stroke=h,baseline=b,angle_deg=degrees,
                           bottom_bin_mm=height_bin(b))
                    r.update(footprint(p,w,h,b,math.radians(degrees)))
                    r['four_cap_grid_row_worst_fraction']=min(footprint(p,w,h,b,math.radians(degrees),offset=(0.,j*p))['fraction'] for j in (-1.5,-.5,.5,1.5))
                    r['bounded_fraction']=footprint(p,w,h,b,math.radians(degrees),inward=.2,registration=.2)['fraction']
                    rows.append(r)
    for b in (8.,45.,90.):
        # Invert the bin endpoints independently rather than derivative approximation.
        q=b/D
        assert abs(height_bin(b)-(D-b/(q+DQ)))<1e-10
    delta=(1/250-1/300)/2
    transfer=min(optics.otf(APERTURE,1/(4*DQ),delta*i/40,1024) for i in range(41))
    print(json.dumps(dict(assumptions='D300, dq .0005, two 1.927mm circular pupils, '
        'opaque square columns, eight H-high neighbors around z0 cap; no props; '
        'wall inward .2mm plus common target registration .2mm are sensitivity bounds',
        segment_box_checks=checked, outside_rectangle_clear_samples=gap_escapes, inherited_S50_min_fundamental_transfer=transfer,
        baseline_for_1mm_bin=D*DQ*(D-1), baseline_for_half_mm_bin=D*DQ*(D-.5)/.5,
        rows=rows),indent=2))

if __name__=='__main__': main()
