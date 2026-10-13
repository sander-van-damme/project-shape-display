#!/usr/bin/env python3
"""Pixel-level conditional stereo discriminator, not a camera or PLA qualification.

Uniform caps versus an ideal view-consistent texture control. No commanded
height or supplied correspondence enters the decoder. numpy only; --check
runs fault/limiting-case checks; default adds the bounded scenario tables.
"""
import argparse
from functools import lru_cache
import importlib.util
import itertools
import json
from pathlib import Path
import numpy as np

spec = importlib.util.spec_from_file_location('shared_field', Path(__file__).with_name('shared_field.py'))
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)


def texture(x, y):
    # Analytic aperiodic-in-this-field texture, NOT qualified printable/projected detail.
    return .55 + sum(.055*np.sin(kx*x+ky*y+phase) for kx,ky,phase in
                     ((12,7,.1),(21,-11,1.7),(7,19,2.8),(17,23,.7)))


@lru_cache(maxsize=20)
def raster(pitch, heights, baseline, textured, aa=2):
    """Rectified 1920x24 images of opaque 4.4-square prisms from z=-10 to top.

    Pinhole visibility includes sides/occlusion, 2x2 pixel integration followed
    by an assigned Gaussian PSF. PSF is not a fitted lens/diffraction model.
    """
    D=1000.;f=s.optics(pitch,50,16,D,baseline)['focal_px']
    nrow,ncol=24,1920
    u=(np.arange(ncol*aa)+.5)/aa-ncol/2
    w=(np.arange(nrow*aa)+.5)/aa-nrow/2
    dx,dy=np.meshgrid(u/f,w/f)
    out=[]
    for cx in (-baseline/2,baseline/2):
        best=np.full(dx.shape,np.inf); img=np.full(dx.shape,.1)
        for i,z in enumerate(heights):
            x=(i-7.5)*pitch
            # Intersect full closed prism slabs, with ray (cx,0,D)+t*(dx,dy,-1).
            with np.errstate(divide='ignore',invalid='ignore'):
                a=(x-2.2-cx)/dx;b=(x+2.2-cx)/dx
                c=-2.2/dy;d=2.2/dy
                near=np.maximum.reduce([np.minimum(a,b),np.minimum(c,d),np.full(dx.shape,D-z)])
                far=np.minimum.reduce([np.maximum(a,b),np.maximum(c,d),np.full(dx.shape,D+10)])
            hit=(near<=far)&(near<best)&(near>0)
            top=abs(near-(D-z))<1e-8
            radiance=texture(cx+near*dx,near*dy) if textured else np.full(dx.shape,.65)
            img=np.where(hit,np.where(top,radiance,.35),img);best=np.where(hit,near,best)
        img=img.reshape(nrow,aa,ncol,aa).mean(axis=(1,3))
        out.append(img)
    return out,f


def render(pitch, heights, baseline, textured, blur=1., noise=0., seed=0, aa=2):
    raw,f=raster(pitch,tuple(heights),baseline,textured,aa)
    rng=np.random.default_rng(seed);out=[]
    for raw_image in raw:
        img=raw_image.copy()
        if blur:
            radius=int(np.ceil(4*blur)); q=np.arange(-radius,radius+1)
            kernel=np.exp(-q*q/(2*blur*blur));kernel/=kernel.sum()
            for axis in (0,1):
                img=np.apply_along_axis(lambda a: np.convolve(np.pad(a,radius,mode='edge'),kernel,mode='valid'),axis,img)
        img+=rng.uniform(-noise,noise,img.shape)
        out.append(img)
    return out,f


def bilinear(image,u,v):
    # Image centers are (index+.5)-size/2, unlike corner coordinates.
    x=u+image.shape[1]/2-.5;y=v+image.shape[0]/2-.5
    ix=np.floor(x).astype(int);iy=np.floor(y).astype(int)
    if np.any(ix<0) or np.any(ix>=image.shape[1]-1) or np.any(iy<0) or np.any(iy>=image.shape[0]-1):
        raise ValueError('sample outside frame')
    a=x-ix;b=y-iy
    return ((1-a)*(1-b)*image[iy,ix]+a*(1-b)*image[iy,ix+1]
            +(1-a)*b*image[iy+1,ix]+a*b*image[iy+1,ix+1])


def decode(images,f,pitch,baseline,cell,step=.1,residual=.01,texture_floor=.02,right_shift=0.):
    """Search ALL physical heights; low texture/nonunique/inconsistent -> unknown.

    25 samples in .4-mm-square patch. Independent board registration granted.
    A set of sampled photometrically compatible heights is a discriminator,
    NOT a rigorous continuous/noise/model-error confidence interval.
    """
    heights=np.linspace(0,50,round(50/step)+1)
    ox,oy=np.meshgrid(np.linspace(-.2,.2,5),np.linspace(-.2,.2,5))
    x=(cell-7.5)*pitch+ox.ravel()[None,:];y=oy.ravel()[None,:]
    depth=1000-heights[:,None]; patches=[]
    for img,cx,shift in zip(images,(-baseline/2,baseline/2),(0,right_shift)):
        patches.append(bilinear(img,f*(x-cx)/depth+shift,f*y/depth))
    left,right=patches
    cost=np.sqrt(np.mean((left-right)**2,axis=1))
    contrast=np.minimum(np.std(left,axis=1),np.std(right,axis=1))
    valid=(cost<=residual)&(contrast>=texture_floor)
    possible=heights[valid]
    if not len(possible): return dict(state='unknown',reason='no textured compatible height')
    span=float(possible[-1]-possible[0])
    if span>.5+1e-9: return dict(state='unknown',reason='ambiguous',span_mm=span)
    best=np.flatnonzero(valid)[np.argmin(cost[valid])]
    return dict(state='candidate',height_mm=float(heights[best]),span_mm=span,
                rms=float(cost[best]),contrast=float(contrast[best]))


def evaluate(pitch,baseline,heights,textured,blur=1.,noise=0.,seed=0,step=.1,right_shift=0.,aa=2):
    images,f=render(pitch,heights,baseline,textured,blur,noise,seed,aa)
    results=[decode(images,f,pitch,baseline,i,step=step,right_shift=right_shift) for i in range(16)]
    errors=[abs(r['height_mm']-z) for r,z in zip(results,heights) if r['state']=='candidate']
    return dict(candidates=len(errors),unknown=16-len(errors),
                max_error_mm=max(errors,default=None),
                wrong_candidates_over_p25mm=sum(e>.25+1e-9 for e in errors)),results


def calibration(error=.1):
    """Independent shared depth references correct a changed rectified d=A/Z+q.

    No image detection is claimed for references. Fresh known depth + absolute
    fiducial identity must come from a separately grounded frame, not commands.
    """
    out=[]
    for pitch,b in ((6.35,40.),(5.08,12.)):
        D=1000.;A=s.optics(pitch,50,16,D,b)['focal_px']*b
        worst=dict(raw=0.,one_ref=0.,two_refs=0.)
        exact=0.
        for scale,q,e0,e1,et in itertools.product((.999,1.001),(-.2,.2),(-error,error),(-error,error),(-error,error)):
            actual=A*scale
            d0=actual/D+q+e0;d1=actual/(D-50)+q+e1
            fitted=(d1-d0)/(1/(D-50)-1/D);offset=d0-fitted/D
            # Independent analytic fit, not a numerical optimizer.
            for z in (0.,12.5,25.,37.5,50.):
                d=actual/(D-z)+q+et
                raw=D-A/d
                # One reference cancels a common disparity offset, nominal scale remains.
                one=D-A/(d-d0+A/D)
                two=D-fitted/(d-offset)
                for key,estimate in [('raw',raw),('one_ref',one),('two_refs',two)]:
                    worst[key]=max(worst[key],abs(estimate-z))
            clean0=actual/D+q;clean1=actual/(D-50)+q
            a=(clean1-clean0)/(1/(D-50)-1/D);o=clean0-a/D
            exact=max(exact,abs(D-a/(actual/(D-23.7)+q-o)-23.7))
        assert exact<1e-8
        out.append(dict(pitch=pitch,baseline=b,disparity_error_bound_px=error,
                        bounded_error_mm=worst,exact_two_ref_error_mm=exact))
    return out


def checks():
    # Independent renderer/projection anchor: central cap ray must return top radiance.
    im,f=render(6.35,[25.]*16,40,False,blur=0,aa=2)
    u=f*((7-7.5)*6.35+20)/(1000-25)
    assert abs(float(bilinear(im[0],np.array(u),np.array(0)))-.65)<1e-10
    blank,r=evaluate(6.35,40,[25.]*16,False)
    assert blank['candidates']==0,blank
    # Geometry-correct projection alone cannot give a texture-free patch information.
    ideal,r=evaluate(6.35,40,[25.]*16,True,blur=.4,noise=0)
    assert ideal['candidates']>0 and ideal['wrong_candidates_over_p25mm']==0,ideal
    # This deliberately simple candidate gate is NOT safe confidence logic:
    # blur makes two wrong narrow candidate sets on a flat noiseless surface.
    rejected_decoder,_=evaluate(6.35,40,[25.]*16,True,blur=1.)
    assert rejected_decoder['wrong_candidates_over_p25mm']>0,rejected_decoder
    # A full-pitch registration shift selects a different valid neighboring cell.
    # Checkerboard heights expose the identity error even with unique pixel matching.
    heights=[0.,50.]*8;images,f=render(6.35,heights,40,True,blur=.4)
    alias=decode(images,f,6.35,40,8)
    assert alias['state']=='candidate' and abs(alias['height_mm']-heights[7])>49
    # Independent absolute labeled fiducial would have a pitch-size residual, not zero.
    fiducial_residuals=[]
    for p,b in ((6.35,40.),(5.08,12.)):
        focal=s.optics(p,50,16,1000,b)['focal_px']
        # A physically labeled, independent frame fiducial, x=0/z=10.
        measured=[s.project(0,10,cx,1000,focal) for cx in (-b/2,b/2)]
        rx,rz=s.reconstruct(*measured,1000,b,focal)
        assert abs(rx)<1e-9 and abs(rz-10)<1e-9
        wrong_frame_x=rx+p
        assert abs(wrong_frame_x)>.2  # assigned frame gate, not measured accuracy
        fiducial_residuals.append(dict(pitch=p,wrong_frame_residual_mm=wrong_frame_x))
    # Sampling and pixel integration sensitivity on a successful control.
    refined,_=evaluate(6.35,40,[25.]*16,True,blur=.4,step=.05,aa=4)
    assert refined['wrong_candidates_over_p25mm']==0
    finer,_=evaluate(6.35,40,[25.]*16,True,blur=.4,step=.025,aa=8)
    assert finer['wrong_candidates_over_p25mm']==0
    return dict(blank=blank,textured_control=ideal,rejected_decoder=rejected_decoder,refined_control=refined,
                finer_control=finer,independent_fiducial_residuals=fiducial_residuals,
                pitch_alias_decoded_height_mm=alias['height_mm'],
                calibration=[row for error in (0,.025,.05,.1) for row in calibration(error)])


def scenarios():
    out=[]
    fields=((6.35,40.),(5.08,12.))
    scenes={'flat25':[25.]*16,'alternating':[0.,50.]*8,'ramp':np.linspace(0,50,16).tolist()}
    for (pitch,b),(name,z),textured,blur,noise in itertools.product(fields,scenes.items(),(False,True),(.4,1.,2.),(0.,2/255)):
        row,_=evaluate(pitch,b,z,textured,blur,noise,seed=73)
        out.append(dict(pitch=pitch,baseline=b,scene=name,textured=textured,blur_px=blur,noise_bound=noise,**row))
    faults=[]
    for pitch,b in fields:
        for shift in (.1,.2,.5):
            row,_=evaluate(pitch,b,[25.]*16,True,blur=.4,right_shift=shift)
            faults.append(dict(pitch=pitch,right_image_shift_px=shift,**row))
    thresholds=[]
    images,f=render(6.35,[25.]*16,40,True,blur=1.,noise=2/255,seed=73)
    for residual,floor in itertools.product((.005,.01,.02),(.01,.02,.04)):
        rr=[decode(images,f,6.35,40,i,residual=residual,texture_floor=floor) for i in range(16)]
        errors=[abs(r['height_mm']-25) for r in rr if r['state']=='candidate']
        thresholds.append(dict(residual=residual,contrast_floor=floor,candidates=len(errors),
                               max_error_mm=max(errors,default=None)))
    return dict(scenarios=out,uncorrected_calibration_faults=faults,threshold_sensitivity=thresholds)


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--check',action='store_true');args=ap.parse_args()
    result=checks()
    if not args.check: result.update(scenarios())
    print(json.dumps(result,indent=2))
