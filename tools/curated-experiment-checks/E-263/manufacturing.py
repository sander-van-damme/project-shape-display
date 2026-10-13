#!/usr/bin/env python3
"""E-263 print-orientation discriminator, not a slicer or process qualification.

Reads the exact retired binary STL from Git; no generated payload is retained.
Geometry refers to that revision. Labor imports E-260's labelled scenarios.
Run from any directory: python3 tools/curated-experiment-checks/E-263/manufacturing.py
"""
import importlib.util
import json
import math
from pathlib import Path
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[3]
ARCHIVE = 'd0e2470:owner-print-tests/supported-s40/s40-calibration.stl'


def triangles():
    data = subprocess.check_output(['git', 'show', ARCHIVE], cwd=ROOT)
    count, = struct.unpack_from('<I', data, 80)
    assert len(data) == 84 + 50 * count, 'Expected archived binary STL'
    faces = []
    for offset in range(84, len(data), 50):
        record = struct.unpack_from('<12fH', data, offset)
        faces.append(tuple(tuple(record[i:i+3]) for i in (3, 6, 9)))
    return faces


def x_intersections(faces, y, z):
    """Intersect an x-directed line with triangles using yz barycentrics.

    Coplanar triangles are excluded; checks use interior, non-edge sections.
    This supplies collision witnesses, not a watertightness/deposition check.
    """
    hits = []
    for a, b, c in faces:
        by, bz = b[1]-a[1], b[2]-a[2]
        cy, cz = c[1]-a[1], c[2]-a[2]
        det = by*cz-bz*cy
        if abs(det) < 1e-12:
            continue
        u = ((y-a[1])*cz-(z-a[2])*cy)/det
        v = (by*(z-a[2])-bz*(y-a[1]))/det
        if u >= -1e-9 and v >= -1e-9 and u+v <= 1+1e-9:
            hits.append(a[0]+u*(b[0]-a[0])+v*(c[0]-a[0]))
    return sorted(set(round(x, 7) for x in hits))


def support_access(faces):
    # Recover pin-local coordinates from the archived inverted print pose.
    pin = [tuple((x-215, 20-y, 86-z) for x,y,z in face)
           for face in faces if all(201-1e-4 <= x <= 229+1e-4
                                    and 6-1e-4 <= y <= 34+1e-4
                                    for x,y,z in face)]
    # Independent slab control for the line/triangle intersection method.
    slab = [((2,-1,0),(2,1,0),(2,1,2)),
            ((2,-1,0),(2,1,2),(2,-1,2))]
    assert x_intersections(slab, .13, .71) == [2]
    assert x_intersections(slab, 2, .71) == []
    cavity = x_intersections(pin, 0, 20.137)
    assert all(any(abs(x-v)<2e-4 for x in cavity) for v in (-2.2,-1.76,1.76,2.2))
    # A centered 3.30-mm square rigid prism fits the 3.52-mm cavity, but axial
    # withdrawal through the nut necessarily crosses each of these sections.
    # One collision suffices; do not interpret sampling as clearance proof.
    trials = []
    for steps in (120,240):
        sections = []
        for i in range(steps+1):
            z = 2.137+3*i/steps
            hits = x_intersections(pin, 0, z)
            positive = [x for x in hits if x>0]
            assert len(positive)>=2, (z,hits)
            assert abs(max(positive)-2.2)<2e-4, (z,hits)
            sections.append((min(positive),z))
        radius,z = min(sections)
        assert abs(radius-.85)<2e-4, (radius,z)
        assert 1.65-radius > .79  # finite witness, far from mesh-rounding error
        trials.append(dict(sections=steps+1, witness_z_mm=z,
                           bore_x_mm=radius, support_overlap_mm=1.65-radius))
    # Changed geometry control: remove the cap at z84 and extract toward it,
    # staying inside the straight square cavity, never crossing the nut.
    # This is an ideal aperture, NOT a designed joint or proof of release force.
    aperture_cases = [dict(total_width_loss_mm=e,
                           clearance_mm=3.52-e-3.30) for e in (0,.1,.3)]
    assert aperture_cases[0]['clearance_mm']>0
    assert aperture_cases[-1]['clearance_mm']<0
    return dict(rigid_support_width_mm=3.30, straight_nut_exit=trials,
                hypothetical_open_cap_exit=aperture_cases)


def batch_cleanup(n, batch_size, batch_seconds, per_part_seconds):
    """Labelled removal-time allocations; final partial batch also costs time."""
    assert n>0 and batch_size>0 and batch_seconds>=0 and per_part_seconds>=0
    return math.ceil(n/batch_size)*batch_seconds + 2*n*per_part_seconds


def part_points(points, center, width):
    # Original check.py places these two separate solids away from frame/keys.
    x, y = center
    out = [(a-x, b-y, c) for a, b, c in points
           if x-width/2-1e-4 <= a <= x+width/2+1e-4
           and y-width/2-1e-4 <= b <= y+width/2+1e-4]
    assert out
    return out


def horizontal_gap(part, body, angle):
    # Long axis is horizontal; roll angle chooses the face/edge toward the bed.
    a = math.radians(angle)
    def projected(p):
        return p[0]*math.cos(a) + p[1]*math.sin(a)
    return min(map(projected, body)) - min(map(projected, part))


def merged(intervals):
    out = []
    for low, high in sorted(intervals):
        if out and low <= out[-1][1]:
            out[-1][1] = max(out[-1][1], high)
        else:
            out.append([low, high])
    return out


def main():
    faces = triangles()
    points = set(p for face in faces for p in face)
    access = support_access(faces)
    pin = part_points(points, (215, 20), 28)
    screw = part_points(points, (175, 20), 24)
    for part, expected in [(pin, (28,28,86)), (screw, (24,24,80))]:
        bounds = [max(p[i] for p in part)-min(p[i] for p in part) for i in range(3)]
        assert all(abs(a-b)<2e-4 for a,b in zip(bounds,expected)), bounds
    pin_body = [p for p in pin if 2-1e-4 <= p[2] <= 84+1e-4
                and abs(p[0])<=2.2001 and abs(p[1])<=2.2001]
    screw_body = [p for p in screw if p[2]>4.021]
    gap_rows = []
    # All rolls sampled, checking independent analytic square/circular envelopes.
    for angle in range(91):
        gap = horizontal_gap(pin, pin_body, angle)
        analytic = 11.8*(abs(math.cos(math.radians(angle)))+
                         abs(math.sin(math.radians(angle))))
        assert abs(gap-analytic)<2e-4
        screw_gap = horizontal_gap(screw, screw_body, angle)
        # Both circles are polygonized at 64 sides; bound discretization error.
        assert abs(screw_gap-10.4) < 12*(1-math.cos(math.pi/64)) + 2e-4
        if angle in (0,15,30,45,90):
            gap_rows.append(dict(roll_degrees=angle, pin_mm=gap, screw_mm=screw_gap))
    # Continuous guide sweeps: local coordinates = fixed guide z - pin travel q.
    guides = [(44,46),(84,86)]
    qmin,qmax = 2,42
    swept = merged([(a-qmax,b-qmin) for a,b in guides])
    assert swept == [[2,84]]
    # Independently sample travel at 0.01 mm and reconstruct coverage union.
    discrete = merged([(a-(2+i/100),b-(2+i/100))
                       for i in range(4001) for a,b in guides])
    assert discrete == swept
    # Counterexample: shortened stroke no longer sweeps the entire shank.
    assert merged([(a-12,b-2) for a,b in guides]) == [[32,44],[72,84]]
    spec = importlib.util.spec_from_file_location('manufacture', ROOT/'tools/curated-experiment-checks/E-260/manufacture.py')
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)
    labor = []
    assert batch_cleanup(17,16,30,0)==60
    assert batch_cleanup(16,16,0,10)==320
    for n in (4096,6400):
        base = model.labor(n,8)
        spare = base['touch_ceiling_32h']-8
        batch_cases = []
        for size in (3,16,64):
            # 30 seconds per batch of PAIRS; both supports handled together.
            # This is a favorable accounting control, not a demonstrated fixture.
            seconds = batch_cleanup(n,size,30,0)
            max_part = (n*spare-seconds)/(2*n)
            assert math.isclose(base['total_maker_h']+
                                (seconds+2*n*max_part)/3600,32)
            batch_cases.append(dict(pairs_per_batch=size, batch_seconds=30,
                added_hours=seconds/3600,
                remaining_individual_cleanup_s_per_part_32h=max_part))
        labor.append(dict(cells=n, added_cleanup_s_per_pair_32h=spare,
                          per_part_if_equal_s=spare/2,
                          added_hours_10s_each_part=n*20/3600,
                          total_hours_10s_each_part=model.labor(n,28)['total_maker_h'],
                          batch_removal=batch_cases,
                          extra_10s_split_join_hours=n*10/3600))
    print(json.dumps(dict(evidence='CAD bounds and assumed labor; no print prediction',
        archived_mesh=ARCHIVE, horizontal_gaps=gap_rows,
        guide_swept_pin_interval_mm=swept, cavity_roof_span_mm=3.52,
        thread_entry_min_diameter_mm=1.70,
        support_access=access,
        batch_sample_three_miss_at_assumed_5pct_defects=.95**3,
        labor=labor,checks='91 rolls; independent envelopes; 4001 travel positions; shortened-stroke control; mesh exit witnesses at two resolutions; open-cap and batch accounting controls passed'),indent=2))


if __name__ == '__main__':
    main()
