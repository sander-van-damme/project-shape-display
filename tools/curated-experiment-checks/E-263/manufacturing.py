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


def vertices():
    data = subprocess.check_output(['git', 'show', ARCHIVE], cwd=ROOT)
    count, = struct.unpack_from('<I', data, 80)
    assert len(data) == 84 + 50 * count, 'Expected archived binary STL'
    points = set()
    for offset in range(84, len(data), 50):
        record = struct.unpack_from('<12fH', data, offset)
        points.update(tuple(record[i:i+3]) for i in (3, 6, 9))
    return points


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
    points = vertices()
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
    for n in (4096,6400):
        base = model.labor(n,8)
        spare = base['touch_ceiling_32h']-8
        labor.append(dict(cells=n, added_cleanup_s_per_pair_32h=spare,
                          per_part_if_equal_s=spare/2,
                          added_hours_10s_each_part=n*20/3600,
                          total_hours_10s_each_part=model.labor(n,28)['total_maker_h']))
    print(json.dumps(dict(evidence='CAD bounds and assumed labor; no print prediction',
        archived_mesh=ARCHIVE, horizontal_gaps=gap_rows,
        guide_swept_pin_interval_mm=swept, cavity_roof_span_mm=3.52,
        thread_entry_min_diameter_mm=1.70,
        batch_sample_three_miss_at_assumed_5pct_defects=.95**3,
        labor=labor,checks='91 rolls, independent envelopes, 4001 travel positions, shortened-stroke control passed'),indent=2))


if __name__ == '__main__':
    main()
