#!/usr/bin/env python3
"""Ideal finite direct images and interval calibration; no earned optics/noise.

Numpy raster, exact pinhole intersections and square-pixel integration. The
visibility mask is an oracle from E-293 geometry, NOT recovered segmentation.
"""
import json
import math
import numpy as np

D, B, P, W, DQ, Q0, BITS = 300., 90., 12.7, 10.3, .0005, .07, 11
U = math.sqrt(.5)


def gray(q):
    n=np.floor((q-Q0)/DQ).astype(int)
    assert np.all((n>=0)&(n<2**BITS))
    return n^(n>>1)


def bounds(address, ray, dr, angular=0., baseline=0., height=0.):
    qlo=Q0+address*DQ
    # Common systematic calibration bounds, not independent noise to average.
    lo=D-height-(B+baseline)/(qlo-(ray+dr/2+angular))
    hi=D+height-(B-baseline)/(qlo+DQ-(ray-dr/2-angular))
    return lo,hi


def image(n, z, ray_bias=0.):
    dr=.2/n
    r,s=np.meshgrid(-.27+(np.arange(n)+.5)*dr,
                    -.1+(np.arange(n)+.5)*dr)
    # Camera C=(B/2)*u. v=(-u_y,u_x). Parallel image plane at D.
    x=B/2*U+(D-z)*U*(r-s)
    y=B/2*U+(D-z)*U*(r+s)
    t=(50-z)/(D-z)
    a=P-W/2
    half=(a-t*(B*U/2+1.927/2))/(1-t)
    # Entire finite pixel must remain within one sufficient clear rectangle.
    margin=(D-z)*U*dr
    masks=[]
    for j in (-1.5,-.5,.5,1.5):
        cx,cy=0.,j*P
        hx0=max(-W/2,-half);hx1=min(W/2,half)
        hy0=max(-W/2,t*cy/(1-t)-half)
        hy1=min(W/2,t*cy/(1-t)+half)
        masks.append((x-cx>hx0+margin)&(x-cx<hx1-margin)&
                     (y-cy>hy0+margin)&(y-cy<hy1-margin))
    valid=np.logical_or.reduce(masks)
    rays=r[valid]
    # Direct illumination only. Pixel mean over uniform horizontal flat cap;
    # s cancels in rectified q. All vertical subpixel samples are identical.
    qleft=rays-dr/2+B/(D-z)
    qright=qleft+dr
    first=np.floor((qleft-Q0)/DQ).astype(int)
    intensities=np.zeros((BITS,len(rays)))
    total_weight=np.zeros(len(rays))
    # Exact piecewise integration, including all crossed address boundaries.
    for offset in range(math.ceil(dr/DQ)+1):
        address=first+offset
        left=Q0+address*DQ
        weight=np.maximum(0.,np.minimum(qright,left+DQ)-np.maximum(qleft,left))/dr
        total_weight+=weight
        code=address^(address>>1)
        intensities+=((code[None,:]>>np.arange(BITS)[:,None])&1)*weight[None,:]
    assert np.max(abs(total_weight-1))<1e-9
    # Independent dense quadrature on a bounded subset of pixels.
    check=rays[:17,None]+dr*((np.arange(8192)+.5)/8192-.5)+B/(D-z)
    codes=gray(check)
    sampled=np.array([np.mean((codes>>k)&1,axis=1) for k in range(BITS)])
    assert np.max(abs(sampled-intensities[:,:17]))<.001
    # Equivalent to black0, white1 and complementary Gray pairs (24 frames).
    keep=np.min(abs(2*intensities-1),axis=0)>=.5
    decoded=np.sum((intensities>.5).astype(int)*(1<<np.arange(BITS))[:,None],axis=0)
    addr=decoded.copy()
    shift=decoded>>1
    while np.any(shift):
        addr^=shift;shift>>=1
    ray=rays+ray_bias
    lo,hi=bounds(addr,ray,dr)
    blo,bhi=bounds(addr,ray,dr,.0002,.1,.2)
    assert np.all((blo[keep]<=z+1e-9)&(bhi[keep]>=z-1e-9))
    if not ray_bias:
        assert np.all((lo[keep]<=z+1e-9)&(hi[keep]>=z-1e-9))
    counts=[int(np.count_nonzero(m)) for m in masks]
    aggregates=[]
    for mask in masks:
        selected=mask[valid]&keep
        assert np.any(selected)
        il,ih=float(max(lo[selected])),float(min(hi[selected]))
        bl,bh=float(max(blo[selected])),float(min(bhi[selected]))
        assert bl<=z+1e-9 and bh>=z-1e-9
        if not ray_bias: assert il<=z+1e-9 and ih>=z-1e-9
        else: assert not il<=z<=ih
        aggregates.append(dict(ideal=[il,ih],bounded=[bl,bh]))
    rejected=int(np.count_nonzero(~keep))
    return dict(n=n,z=z,oracle_pixels_per_cap=counts,
                accepted=int(sum(keep)),rejected=rejected,
                max_ideal_interval_mm=float(np.max((hi-lo)[keep])),
                max_bounded_interval_mm=float(np.max((bhi-blo)[keep])),
                naive_false_intervals=int(np.sum(keep&((lo>z+1e-9)|(hi<z-1e-9)))),
                max_midpoint_error_mm=float(np.max(abs(((lo+hi)/2-z)[keep]))),
                flat_cap_intersections=aggregates)


def main():
    rows=[image(n,z) for n in (256,1024) for z in (0.,25.,30.,50.)]
    bias=[image(1024,z,.0002) for z in (0.,25.,30.,50.)]
    # Independent exact corner envelope vs all 16 parameter corners.
    q=.32;r=.02;dr=.2/1024
    addr=round((q-Q0)/DQ)
    lo,hi=bounds(addr,r,dr,.0002,.1,.2)
    corners=[dd-bb/(qq-rr) for dd in (299.8,300.2) for bb in (89.9,90.1)
             for qq in (q,q+DQ) for rr in (r-dr/2-.0002,r+dr/2+.0002)]
    assert abs(lo-min(corners))<1e-10 and abs(hi-max(corners))<1e-10
    print(json.dumps(dict(assumptions='ideal sharp direct-only projection/camera; '
         'finite square pixels, flat caps, oracle visibility mask; angular .0002, '
         'baseline .1mm and origin .2mm are bounds not measured calibration',
         rows=rows,common_ray_bias=bias),indent=2))

if __name__=='__main__':main()
