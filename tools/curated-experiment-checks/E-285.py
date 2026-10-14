#!/usr/bin/env python3
"""Necessary deposition/support screen of unchanged E-277/E-280 paired solids.

Standard library only. Analytical envelopes, NOT a slice or physical print.
Angle is screw axis from bed normal; tilt toward the retained +X channel wall.
"""
import json
import math


def minima(theta, h=2.0):
    c, s = math.cos(theta), math.sin(theta)
    # Exact extrema of body box (retained +X lower corner) and circular collar
    # rim. Socket removes the centre, not the extremal outer rim. For 0..90deg
    # collar remains below both journal and threaded-envelope extrema.
    body = h*c - 5.15*s
    screw = -10*c - 2.2*s
    return body, screw


def gap(theta):
    b, s = minima(theta)
    bed = min(b, s)
    return dict(body_above_bed_mm=b-bed, screw_above_bed_mm=s-bed)


def main():
    theta = math.atan2(12, 2.95)
    # Independent bisection verifies closed-form simultaneous bed contact.
    lo, hi = 0., math.pi/2
    for _ in range(80):
        mid = (lo+hi)/2
        b, s = minima(mid)
        if b > s: lo = mid
        else: hi = mid
    assert abs(theta-(lo+hi)/2)<1e-12
    assert gap(0)['body_above_bed_mm']==12
    assert abs(gap(math.pi/2)['screw_above_bed_mm']-2.95)<1e-12
    assert max(gap(theta).values())<1e-12
    for deg in range(91):
        a=math.radians(deg); c,s=math.cos(a),math.sin(a)
        collar=minima(a)[1]
        assert collar <= -4*c-1.4*s+1e-12
        assert collar <= -1.6*s+1e-12
    # Translation of a shallow longitudinal outer boundary per layer.
    # > extrusion width means no overlap of equal-width successive boundary
    # tracks. Interior infill/bridging may help: not a universal print theorem.
    shifts={str(layer):layer*math.tan(theta) for layer in (.1,.2)}
    result=dict(axis_tilt_degrees=math.degrees(theta),
        upright=gap(0),horizontal=gap(math.pi/2),tilted=gap(theta),
        outer_boundary_shift_per_layer_mm=shifts,
        comparison_extrusion_width_mm=.45,
        max_layer_for_any_boundary_track_overlap_mm=.45/math.tan(theta),
        body_projected_bed_length_mm=136*math.sin(theta)+10.3*math.cos(theta),
        extra_support_contacts='Unknown; cannot be inferred from envelopes',
        assumed_saved_threading_seconds_per_pair=[5,15,30],
        saved_hours={str(n):[n*t/3600 for t in (5,15,30)] for n in (1024,4096,6400)})
    # Separate-body control is bed supported with no 12-mm pedestal. It retains
    # threading; code does not subtract it from an earlier ledger automatically.
    assert shifts['0.2']>.45 and shifts['0.1']<.45
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
