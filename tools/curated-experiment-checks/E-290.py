#!/usr/bin/env python3
"""Temporal projector-phase discriminator; synthetic radiometry, not hardware data.

No random priors. Static gain/offset cancellation and exact mixed-return witnesses.
Run with Python standard library. Geometry is a single calibrated camera ray.
"""
import itertools
import json
import math

D, B, PERIOD, ORIGIN = 300., 8., .02, -.01
RAY = -B / 275.


def phase(z, ray=RAY):
    q = ray + B / (D-z)
    return 2*math.pi*(q-ORIGIN)/PERIOD


def frames(z, gain=1., ambient=120., count=4, ray=RAY):
    return [ambient+gain*(1000+500*math.cos(phase(z, ray)+2*math.pi*j/count))
            for j in range(count)]


def decode(samples, ray=RAY, stroke=50):
    """Only samples, calibrated ray and allowed travel; no target-height input."""
    n=len(samples)
    if max(samples)>=4095 or min(samples)<0:
        return None
    mean=sum(samples)/n
    c=2/n*sum(v*math.cos(2*math.pi*j/n) for j,v in enumerate(samples))
    s=-2/n*sum(v*math.sin(2*math.pi*j/n) for j,v in enumerate(samples))
    amp=math.hypot(c,s)
    if amp<10:
        return None
    angle=math.atan2(s,c) % (2*math.pi)
    residual=max(abs(v-(mean+c*math.cos(2*math.pi*j/n)-s*math.sin(2*math.pi*j/n)))
                 for j,v in enumerate(samples))
    if residual>1:
        return None
    candidates=[]
    for branch in range(-3,4):
        q=ORIGIN+PERIOD*(angle/(2*math.pi)+branch)
        if q>ray:
            z=D-B/(q-ray)
            if -0.1<=z<=stroke+0.1:  # finite quantization reserve, not mechanical extra travel
                candidates.append(z)
    if len(candidates)!=1:
        return None
    return dict(z=candidates[0], amplitude=amp, residual=residual, mean=mean)


def main():
    errors=[]
    unknown=0
    by_gain={g:[] for g in (.05,.2,1)}
    for z,g,a,n,r in itertools.product((0,10,25,40,50),(.05,.2,1), (120,300), (4,8), (RAY-.003,RAY,RAY+.003)):
        raw=frames(z,g,a,n,r)
        exact=decode(raw,r)
        assert exact and abs(exact['z']-z)<1e-9
        got=decode([round(v) for v in raw],r)
        if got is None:
            assert z in (0,50)
            unknown+=1
        else:
            errors.append(abs(got['z']-z))
            by_gain[g].append(abs(got['z']-z))
    assert decode([120]*4) is None
    assert decode([4095]*4) is None
    # Four-step identity independently checks Fourier sign convention.
    raw=frames(25)
    four=math.atan2(raw[3]-raw[1],raw[0]-raw[2]) % (2*math.pi)
    assert abs(four-phase(25) % (2*math.pi))<1e-12
    # A second transport path carries another projector phase onto this pixel.
    # Both paths sum into a perfect single sinusoid at ANY number of phase steps.
    mixed=[]
    for n in (4,8,16):
        direct=frames(25,ambient=0,count=n)
        indirect=frames(45,gain=.2,ambient=0,count=n)
        data=[120+x+y for x,y in zip(direct,indirect)]
        got=decode(data)
        assert got and got['residual']<1e-9
        # Construct a direct-only sinusoid with exactly these same measurements.
        # DC and contrast are independent nuisance terms for a real optical system.
        witness=[got['mean']+got['amplitude']*math.cos(phase(got['z'])+2*math.pi*j/n) for j in range(n)]
        assert max(abs(x-y) for x,y in zip(data,witness))<1e-9
        quant=decode([round(x) for x in data])
        assert quant
        mixed.append(dict(frames=n,decoded_mm=got['z'],quantized_mm=quant['z'],residual_DN=got['residual']))
    # Cap-specific frame gain drift can exactly counterfeit a 1mm height change.
    base=frames(25,ambient=0)
    target=frames(26,ambient=0)
    gains=[b/a for a,b in zip(base,target)]
    forged=[120+a*g for a,g in zip(base,gains)]
    assert abs(decode(forged)['z']-26)<1e-9
    # Geometry check: points along the fixed ray remain inside even a 4.4mm cap.
    assert max(abs(B+r*(D-z)) for z,r in itertools.product((0,50),(RAY-.003,RAY,RAY+.003)))<2.2
    # Coarse unambiguous phase period exceeds the ray's whole-travel q interval.
    assert B/(D-50)-B/D < PERIOD
    print(json.dumps(dict(controls=len(errors)+unknown,accepted_quantized=len(errors),boundary_unknown=unknown,max_quantized_error_mm=max(errors),
        max_quantized_error_by_gain={str(g):max(v) for g,v in by_gain.items()},
        mixed_returns=mixed,one_mm_alias_frame_gain_range=[min(gains),max(gains)],
        acquisition_seconds={str(n):{str(N):N/4*n*.1 for N in (1024,4096,6400)} for n in (4,8)},
        local_four_frame_seconds={str(groups):groups*4*.1 for groups in (1,4,8)}),indent=2))


if __name__=='__main__':
    main()
