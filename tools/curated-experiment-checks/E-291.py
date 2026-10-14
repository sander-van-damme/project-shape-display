#!/usr/bin/env python3
"""Complementary absolute Gray addresses: bounded synthetic transport, not images.

No random distributions or hardware priors. The decoder sees only captured
intensities, calibration and stroke. Finite footprint is uniform ray integration,
not a calibrated projector PSF or a complete reflected scene.
"""
import itertools
import json
import math

D, B, RAY = 300., 8., -8/275
LO, WIDTH, BITS = -.025, .05, 11
CELLS = 1 << BITS
DQ = WIDTH/CELLS


def q_at(z, ray=RAY):
    return ray+B/(D-z)


def address(q):
    assert LO <= q < LO+WIDTH
    return math.floor((q-LO)/DQ)


def bit(q, j):
    n=address(q)
    return ((n ^ (n >> 1)) >> j) & 1


def capture(paths, ambient=120., gain=1., footprint=0., samples=1):
    # paths: (source ray, nonnegative transport weight), no direct/indirect label.
    # All-white / all-black references precede the bit/complement sequence.
    assert all(w >= 0 for q,w in paths)
    out=[ambient+gain*1000*sum(w for q,w in paths),ambient]
    for j in range(BITS):
        signal=sum(w*sum(bit(q+footprint*((k+.5)/samples-.5),j)
                        for k in range(samples))/samples for q,w in paths)
        out.extend((ambient+gain*1000*signal,
                    ambient+gain*1000*(sum(w for q,w in paths)-signal)))
    return out


def decode(data, ray=RAY, stroke=50.):
    if len(data)!=2+2*BITS or min(data)<0 or max(data)>=4095:
        return None
    white,black=data[:2]
    contrast=white-black
    if contrast<10:
        return None
    gray=0
    margins=[]
    for j in range(BITS):
        a,b=data[2+2*j:4+2*j]
        if abs(a+b-white-black)>2.:  # quantization reserve, not earned noise bound
            return None
        margins.append(abs(a-b)/contrast)
        if margins[-1]<.5:
            return None
        gray |= (a>b) << j
    n=gray
    shift=gray >> 1
    while shift:
        n ^= shift
        shift >>= 1
    qlo=LO+n*DQ
    qhi=qlo+DQ
    if qlo<=ray:
        return None
    zlo,zhi=D-B/(qlo-ray),D-B/(qhi-ray)
    # Intersect quantized interval with allowed travel, never desired height.
    zlo,zhi=max(0.,zlo),min(stroke,zhi)
    if zlo>zhi:
        return None
    return dict(address=n,interval_mm=[zlo,zhi],height_mm=(zlo+zhi)/2,
                min_normalized_contrast=min(margins))


def geometry_screen():
    """Opaque, flat caps; central point; point source; no material inference.

    Ray coordinates are in the coding plane: projector (0,D), camera (B,D).
    Check the 2D segment inside the terrain slab by its linear endpoints.
    Any extra *single* surface interaction would have to be the first hit.
    Multiple interreflections and subsurface transport are explicitly excluded.
    """
    stroke = 50.
    maximum = 0.
    camera_max = 0.
    cases = 0
    for h, claimed in itertools.product(range(51), repeat=2):
        ray = -B/(D-h)  # actual cap center is x=0, forward geometry only
        q = q_at(claimed, ray)
        endpoints = [q*(D-z) for z in (h, stroke)]
        camera_endpoints = [B+ray*(D-z) for z in (h, stroke)]
        maximum = max(maximum, *map(abs, endpoints))
        camera_max = max(camera_max, *map(abs, camera_endpoints))
        # Direct ray's endpoint on the true plane is independently projected.
        assert abs(endpoints[0] - B*(claimed-h)/(D-claimed)) < 1e-12
        assert max(map(abs, endpoints+camera_endpoints)) < 2.2
        cases += 1
    analytic = B*stroke/(D-stroke)
    assert abs(maximum-analytic) < 1e-12
    # Exact old witness: wrong source ray hits a different point on the SAME
    # flat cap. It cannot then travel through free space to its coplanar center.
    landing = q_at(45)*(D-25)
    assert abs(landing-0.6274509803921569) < 1e-12
    def unit(v):
        length = math.sqrt(sum(x*x for x in v))
        return tuple(x/length for x in v)
    # A stripe address is a PLANE of source rays, not one 2D ray.
    # Adjacent taller column's near vertical wall can reflect downward to cap.
    def first_hit(a, b, lower, upper):
        lo, hi = 0., 1.
        for x, y, mn, mx in zip(a, b, lower, upper):
            delta = y-x
            if abs(delta) < 1e-14:
                if not mn <= x <= mx:
                    return None
                continue
            t0, t1 = sorted(((mn-x)/delta, (mx-x)/delta))
            lo, hi = max(lo, t0), min(hi, t1)
            if lo > hi+1e-12:
                return None
        return lo
    wall_controls = []
    for pitch, width in ((5.08,4.4),(6.35,4.4),(12.7,10.3)):
        src = (0.,0.,D)
        cap = (0.,0.,25.)
        point = (q_at(45)*(D-45),pitch-width/2,45.)
        target_box = ((-width/2,-width/2,-100.),(width/2,width/2,25.))
        wall_box = ((-width/2,pitch-width/2,-100.),
                    (width/2,pitch+width/2,50.))
        assert first_hit(src,point,*target_box) is None
        assert abs(first_hit(src,point,*wall_box)-1) < 1e-12
        assert abs(first_hit(point,cap,*target_box)-1) < 1e-12
        # Open outgoing segment lies strictly outside wall (decreasing y).
        assert point[1] > cap[1]
        toward_source = unit(tuple(a-b for a,b in zip(src,point)))
        toward_target = unit(tuple(a-b for a,b in zip(cap,point)))
        incidence, emergence = -toward_source[1], -toward_target[1]
        assert incidence > 0 and emergence > 0
        assert first_hit(src,cap,*wall_box) is None
        assert first_hit((B,0.,D),cap,*wall_box) is None
        wall_controls.append(dict(pitch_mm=pitch,bounce_mm=point,
                                  incident_normal_cosine=incidence,
                                  outgoing_normal_cosine=emergence))
    return dict(three_dimensional_wall_paths=wall_controls,
                sampled_height_pairs=cases,
                continuous_projector_envelope_mm=analytic,
                sampled_camera_envelope_mm=camera_max,
                remaining_half_width_mm={str(w):w/2-analytic for w in (4.4,10.3)},
                old_witness_first_hit_x_mm=landing)


def main():
    controls=0
    max_error=0.
    for z,g,a,r in itertools.product((0,10,25,40,50),(.05,.2,1),
                                    (120,300),(RAY-.003,RAY,RAY+.003)):
        got=decode([round(x) for x in capture([(q_at(z,r),1)],a,g)],r)
        assert got and got['interval_mm'][0]-1e-9<=z<=got['interval_mm'][1]+1e-9
        max_error=max(max_error,abs(got['height_mm']-z))
        controls+=1
    assert decode([120.]*(2+2*BITS)) is None
    assert decode([4095.]*(2+2*BITS)) is None
    # Independent exhaustive binary/Gray roundtrip, without radiometry.
    for n in range(CELLS):
        g=n^(n>>1)
        v=g
        while g>>1:
            g>>=1
            v^=g
        assert v==n
    # Direct weight 1 dominates arbitrary nonnegative total indirect weight .2.
    # Every bit has signed direct >=1000 and opposing indirect <=200 DN,
    # hence normalized margin >=(1-.2)/(1+.2)=2/3, absent blur/drift/noise.
    minority=[]
    for zi in (0,10,26,40,45,50):
        data=capture([(q_at(25),1),(q_at(zi),.2)])
        got=decode([round(x) for x in data])
        assert got and got['address']==address(q_at(25))
        minority.append(got)
    # Equal separated paths are unknown; a dominant reflected path passes.
    assert decode(capture([(q_at(25),1),(q_at(45),1)])) is None
    data=capture([(q_at(25),.2),(q_at(45),1)])
    dominant=decode(data)
    assert dominant and dominant['address']==address(q_at(45))
    # Relabeling which physical surface/path is direct changes no raw datum.
    other=capture([(q_at(45),1),(q_at(25),.2)])
    alias=max(abs(a-b) for a,b in zip(data,other))
    assert alias<1e-10
    # The points at true 25 and 45 both lie inside the same granted 4.4mm cap.
    assert max(abs(B+RAY*(D-z)) for z in (25,45))<2.2
    # Finite uniform footprint controls: integer-bin centers avoid accidental
    # boundaries; boundary is known only to forward model, not decoder.
    center=LO+(address(q_at(25))+.5)*DQ
    blur=[]
    for width in (0.,DQ,2*DQ,4*DQ):
        pair=[]
        for count in (128,256):
            got=decode(capture([(center,1),(q_at(45),.2)],footprint=width,samples=count))
            pair.append(got)
        assert pair[0]==pair[1]
        blur.append(dict(footprint_bins=width/DQ,decoded=pair[1]))
    boundary=LO+address(q_at(25))*DQ
    assert decode(capture([(boundary,1)],footprint=DQ,samples=256)) is None
    # For this fixed field, a source bin no wider than DQ has worst interval
    # near minimum height, where dz/dq=(D-z)^2/B is largest.
    max_interval=D-B/(B/D+DQ)
    assert max_interval<.275
    # Coding axis y spans one row; four caps are across x, not fourfold y pixels.
    field={str(p):dict(required_x_span_at_z50_mm=3*p+w,
                       required_y_span_at_z50_mm=w,
                       available_y_span_mm=WIDTH*250)
           for p,w in ((5.08,4.4),(6.35,4.4),(12.7,10.3))}
    print(json.dumps(dict(geometry=geometry_screen(),
        controls=controls,max_control_midpoint_error_mm=max_error,
        address_roundtrips=CELLS,bits=BITS,frames=2+2*BITS,
        projector_bin_mm_at_z25=DQ*275,max_height_bin_mm=max_interval,
        minority_path_z45=minority[4],equal_paths='unknown',
        dominant_reflection=dominant,raw_relabel_alias_DN=alias,
        footprint_controls=blur,field=field,
        acquisition_s={str(N):N/4*(2+2*BITS)*.1 for N in (1024,4096,6400)},
        local_acquisition_s={str(k):k*(2+2*BITS)*.1 for k in (1,4,8)}),indent=2))


if __name__=='__main__':
    main()
