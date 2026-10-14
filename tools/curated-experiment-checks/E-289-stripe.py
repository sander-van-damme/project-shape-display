#!/usr/bin/env python3
"""Finite stripe -> sampled pixels -> blind centroid/shape decoder.

Scenario radiometry, not measured PLA, a full image renderer or qualified optics.
Run with Python + numpy. No random distributions or stored generated outputs.
"""
import importlib.util
import json
from pathlib import Path
import numpy as np

spec = importlib.util.spec_from_file_location('plane', Path(__file__).with_name('E-289.py'))
plane = importlib.util.module_from_spec(spec)
spec.loader.exec_module(plane)
D, B = 300., 8.


def render(z, b, f, gradient=0., sigma=.05, sheet=0., peak=1200.,
           gain=1., offset=0., sub=32, quantize=True, visible=True):
    """1D central cap strip. All dimensions mm except pixel coordinates.

    Inverse-map sensor samples onto a planar cap. A finite Gaussian sheet is
    multiplied by exp(gradient*y), bounded to [0,1] via a .1 albedo at y=0.
    Gaussian optical PSF sigma .65 pixels precedes unit-pixel integration.
    Ambient is a constant 100 DN + dark 20 DN in each exposure. Directional
    laser reflectance may differ from ambient response. 12-bit quantization.
    No oracle height, centroid or target window reaches decode_profile.
    """
    vs = [f*(y-b)/(D-h)+offset for y in (-.5,.5) for h in (0.,50.)]
    start, stop = int(np.floor(min(vs)))-8, int(np.ceil(max(vs)))+9
    centers = np.arange(start, stop, dtype=float)
    coords = (centers[:,None] + (np.arange(sub)+.5)/sub-.5).ravel()
    y = (coords-offset)*(D-z)/f+b
    albedo = np.clip(.1*np.exp(np.clip(gradient*y,-100,100)),0,1)
    light = np.exp(-.5*((y-sheet)/sigma)**2)
    signal = peak*gain*light*albedo/.1 if visible else np.zeros_like(y)
    radius=int(np.ceil(5*.65*sub))
    kernel=np.exp(-.5*(np.arange(-radius,radius+1)/(.65*sub))**2)
    kernel/=kernel.sum()
    signal=np.convolve(signal,kernel,mode='same').reshape(-1,sub).mean(axis=1)
    off=np.full_like(signal,120.)
    on=np.clip(off+signal,0,4095)
    if quantize:
        off,on=np.rint(off),np.rint(on)
    return centers,on,off


def decode_profile(data):
    """Threshold, component segmentation, centroid and symmetry diagnostic.

    Single exposed cap identity is granted. No commanded height used. Reject
    no-return, saturation, multiple components or large standardized skew.
    A Gaussian-looking biased line can still pass, which is the question tested.
    """
    x,on,off=data
    if np.max(on)>=4095:
        return None
    signal=np.maximum(on-off,0)
    if signal.max()<20:
        return None
    mask=signal>max(2.,signal.max()*.01)
    edges=np.diff(np.r_[False,mask,False].astype(int))
    if np.sum(edges==1)!=1:
        return None
    weight=np.where(mask,signal,0)
    center=float(np.sum(x*weight)/weight.sum())
    var=float(np.sum((x-center)**2*weight)/weight.sum())
    skew=float(np.sum((x-center)**3*weight)/weight.sum()/var**1.5)
    if abs(skew)>.1:
        return None
    return center, var**.5, skew


def height(v,b,f):
    return D+f*b/v


def stereo(vplus,vminus,f):
    # Same emitting y coordinate is the conditional stereo correspondence.
    return D-2*f*B/(vminus-vplus)


def check():
    rows=[]
    for p,w in ((5.08,4.4),(6.35,4.4),(12.7,10.3)):
        f=plane.scenario(p,w,4,D,B,50)['f']
        uniform=[]
        for z in (0.,10.,25.,40.,50.):
            d=decode_profile(render(z,B,f))
            assert d is not None
            uniform.append(abs(height(d[0],B,f)-z))
        assert max(uniform)<.08
        z=25.
        a=8. # .1 -> .495 over y=0..+.2mm, not a measured material property
        shift=a*.05**2
        plus=decode_profile(render(z,B,f,gradient=a))
        minus=decode_profile(render(z,-B,f,gradient=a))
        opposite=decode_profile(render(z,-B,f,gradient=-a))
        assert all(d is not None for d in (plus,minus,opposite))
        analytic=height(f*(shift-B)/(D-z),B,f)
        single=height(plus[0],B,f)
        common=stereo(plus[0],minus[0],f)
        differential=stereo(plus[0],opposite[0],f)
        assert abs(single-analytic)<.08
        assert abs(common-z)<.08
        assert abs(single-z)>.5 and abs(differential-z)>.5
        assert decode_profile(render(z,B,f,visible=False)) is None
        assert decode_profile(render(z,B,f,peak=10000)) is None
        # Shared affine image bias corrected by two exposed known-height refs.
        refs=(0.,50.)
        ref_v=[decode_profile(render(h,B,f,offset=.7))[0] for h in refs]
        ideal_v=[f*(-B)/(D-h) for h in refs]
        scale=(ideal_v[1]-ideal_v[0])/(ref_v[1]-ref_v[0])
        bias=ideal_v[0]-scale*ref_v[0]
        measured=decode_profile(render(z,B,f,gradient=a,offset=.7))[0]
        corrected=height(scale*measured+bias,B,f)
        assert abs(corrected-z)>.5
        # Convergence without quantization isolates integration discretization.
        c=[decode_profile(render(z,B,f,gradient=a,sub=s,quantize=False))[0]
           for s in (16,32,64)]
        convergence=max(abs(height(v,B,f)-height(c[-1],B,f)) for v in c)
        assert convergence<.01
        rows.append(dict(pitch=p,uniform_max_error=max(uniform),
                         single_height=single,reference_corrected=corrected,
                         stereo_common=common,stereo_differential=differential,
                         accepted_skew=plus[2],convergence_mm=convergence))
    # Smooth reflectance generates an exact continuous shifted Gaussian:
    # exp(-y²/2s²)*exp(a*y)=exp(a²s²/2)*exp(-(y-a*s²)²/2s²).
    y=np.linspace(-.2,.2,1001);s=.05;a=8.
    left=np.exp(-y*y/(2*s*s))*np.exp(a*y)
    right=np.exp(a*a*s*s/2)*np.exp(-(y-a*s*s)**2/(2*s*s))
    assert np.max(np.abs(left-right))<1e-14
    # Full one-dimensional pixel profiles: different true heights and a smooth
    # bounded reflectance law can produce a sub-DN profile match with fixed sheet sigma.
    # Construct the necessary albedo analytically, not by editing pixels.
    f=plane.scenario(6.35,4.4,4,D,B,50)['f']; z0=25.; z1=26.
    x,on0,off=render(z0,B,f,quantize=False)
    # Separate general renderer below preserves identical PSF/pixel chain.
    x1,on1,off1=render_alias(z0,z1,f)
    assert np.array_equal(x,x1)
    difference=float(np.max(np.abs(on0-on1)))
    assert difference<.1
    assert abs(height(decode_profile((x,on1,off1))[0],B,f)-z0)<.08
    return rows,dict(profile_alias_DN=difference,actual_heights=[z0,z1],
                     albedo_range_core=alias_bounds(z0,z1))


def alias_albedo(y,z0,z1):
    # y0 is the point at z0 seen at the SAME sensor coordinate as y at z1.
    y0=(y-B)*(D-z0)/(D-z1)+B
    return np.clip(.1*np.exp(np.clip((y*y-y0*y0)/(2*.05**2),-100,100)),0,1)


def alias_bounds(z0,z1):
    ys=np.linspace(-.15,.15,1001)
    r=alias_albedo(ys,z0,z1)
    return [float(r.min()),float(r.max())]


def render_alias(z0,z1,f):
    # Fixed same world sheet, exposure, blur and pixel integration as render.
    x,_,off=render(z0,B,f,quantize=False)
    sub=32
    v=(x[:,None]+(np.arange(sub)+.5)/sub-.5).ravel()
    y=(v)*(D-z1)/f+B
    signal=1200*np.exp(-.5*(y/.05)**2)*alias_albedo(y,z0,z1)/.1
    radius=int(np.ceil(5*.65*sub))
    kernel=np.exp(-.5*(np.arange(-radius,radius+1)/(.65*sub))**2);kernel/=kernel.sum()
    signal=np.convolve(signal,kernel,mode='same').reshape(-1,sub).mean(axis=1)
    return x,off+signal,off


if __name__=='__main__':
    rows,alias=check()
    print(json.dumps({'profile_cases':rows,'alias_witness':alias},indent=2))
