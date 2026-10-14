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
    print(json.dumps(spatial_separation(), indent=2))


def spatial_separation():
    """Finite 1D binary carrier times temporal sinusoid; ideal linear transport.

    Four carrier shifts per phase, then max-minus-min isolates the direct
    waveform ONLY when global return is invariant to those carrier shifts.
    The period below deliberately constructs a localized-path alias, not a
    measured projector resolution or an optimized carrier specification.
    """
    q0 = RAY+B/(D-25)
    q1 = RAY+B/(D-45)
    period = (q1-q0)/6

    def mask(q, shift):
        return float(((q-q0)/period+.13+shift/4) % 1 < .5)

    def illumination(q, j):
        return 1000+500*math.cos(2*math.pi*(q-ORIGIN)/PERIOD+2*math.pi*j/4)

    def capture(paths, smooth=False):
        # paths are (projector ray, nonnegative transport weight).
        rows=[]
        for j in range(4):
            rows.append([120+sum(w*illumination(q,j)*mask(q,s) for q,w in paths)
                         + (.1*illumination(q1,j) if smooth else 0)
                         for s in range(4)])
        return rows

    def separate(rows):
        return [max(row)-min(row) for row in rows]

    # Independent limiting cases: zero indirect and exactly shift-invariant
    # global (which may still vary across temporal phases) recover direct.
    controls=0
    for z,g in itertools.product((0,10,25,40,50),(.05,.2,1)):
        q=RAY+B/(D-z)
        for smooth in (False,True):
            got=decode(separate(capture([(q,g)],smooth)))
            assert got and abs(got['z']-z)<1e-9
            controls+=1

    # Broad spatial transport: explicit nonnegative, normalized Gaussian lobe.
    # Doubling quadrature is a numerical check, not a process/noise prior.
    broad=[]
    for count in (2048,4096):
        rays=[q1-.003+.006*(i+.5)/count for i in range(count)]
        weights=[math.exp(-.5*((q-q1)/.0008)**2) for q in rays]
        total=sum(weights)
        paths=[(q0,1)]+[(q,.2*w/total) for q,w in zip(rays,weights)]
        got=decode(separate(capture(paths)))
        assert got
        broad.append(got['z'])
    assert abs(broad[1]-broad[0])<.01

    # Localized reflected path at q1 shares all four masks with q0. Its
    # modulation survives max-min exactly, including the 20% phase witness.
    assert all(mask(q0,s)==mask(q1,s) for s in range(4))
    data=capture([(q0,1),(q1,.2)])
    separated=separate(data)
    expected=[illumination(q0,j)+.2*illumination(q1,j) for j in range(4)]
    assert max(abs(a-b) for a,b in zip(separated,expected))<1e-9
    got=decode(separated)
    rounded=decode(separate([[round(x) for x in row] for row in data]))
    assert got and rounded and abs(got['z']-28.3788)<.0001
    # Retaining the binary mask identity does not reject this witness either:
    # the inferred false ray falls in the same four-mask address class.
    false_q=RAY+B/(D-got['z'])
    assert all(mask(false_q,s)==mask(q0,s) for s in range(4))
    # Therefore a direct-only scene with the decoded height and inferred
    # mean/contrast duplicates ALL 16 raw samples, not only their extrema.
    alternative=[[120+mask(false_q,s)*(got['mean']+got['amplitude']*
                  math.cos(phase(got['z'])+2*math.pi*j/4))
                  for s in range(4)] for j in range(4)]
    raw_alias=max(abs(a-b) for row,other in zip(data,alternative)
                  for a,b in zip(row,other))
    assert raw_alias<1e-9
    return dict(spatial_separation_controls=controls,carrier_ray_period=period,
                carrier_mm_at_z25=period*275,
                broad_transport_decoded_mm=broad,
                localized_path_decoded_mm=got['z'],
                localized_path_quantized_mm=rounded['z'],
                localized_path_residual_DN=got['residual'],
                full_16_frame_alias_max_DN=raw_alias,
                acquisition_16_frames_s={str(N):N/4*16*.1 for N in (1024,4096,6400)},
                local_16_frames_s={str(g):g*16*.1 for g in (1,4,8)})


if __name__=='__main__':
    main()
