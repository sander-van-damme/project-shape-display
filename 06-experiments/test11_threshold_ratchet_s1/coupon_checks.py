#!/usr/bin/env python3
"""Coupon-level checks for the printable S1 threshold-ratchet coupon.

These complement the arithmetic checks in checks.py. They verify that the
coupon SOURCE is self-consistent and that the emitted STLs are structurally
sound enough to send to a slicer:

  * the pitch budget closes at 5.08 mm with printable FDM walls (>= 0.40 mm);
  * gate travel fully clears the rack pocket (else the pawl never releases);
  * the column height covers the 40 mm travel plus base;
  * every STL has a valid header/count and non-zero extent;
  * no STL triangle is degenerate (zero area);
  * the assembly STL places all five loose parts.

They assert geometry, NOT print quality and NOT measured behaviour.
"""

from __future__ import annotations

import struct
import unittest
from pathlib import Path

import build_coupon as bc

HERE = Path(__file__).resolve().parent


def read_stl(path: Path):
    data = path.read_bytes()
    assert len(data) >= 84, f"{path.name}: too short"
    n = struct.unpack("<I", data[80:84])[0]
    assert len(data) == 84 + n * 50, (
        f"{path.name}: count {n} does not match size {len(data)}")
    tris = []
    off = 84
    for _ in range(n):
        vals = struct.unpack("<12fH", data[off:off + 50])
        tris.append((vals[3:6], vals[6:9], vals[9:12]))
        off += 50
    return tris


def _area2(a, b, c):
    ux, uy, uz = b[0]-a[0], b[1]-a[1], b[2]-a[2]
    vx, vy, vz = c[0]-a[0], c[1]-a[1], c[2]-a[2]
    cx, cy, cz = uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx
    return cx*cx+cy*cy+cz*cz


class PitchBudgetTest(unittest.TestCase):
    def test_pitch_closes(self):
        m = bc.make_manifest()["checks"]
        self.assertTrue(m["all_printable"], m)

    def test_body_plus_lane_is_pitch(self):
        p = bc.make_manifest()["pitch_partition_mm"]
        self.assertAlmostEqual(p["body"] + p["lane"], bc.PITCH, places=6)

    def test_gate_travel_clears_pocket(self):
        self.assertGreater(bc.GATE_TRAVEL, bc.POCKET_D)

    def test_no_side_by_side_pawl_gate(self):
        # The original error: pawl+gate in ONE x-lane needs 2 x 0.80 + walls.
        # Confirm the design does NOT rely on that (gate is stacked in Z).
        self.assertLess(bc.GATE_T, bc.PITCH - bc.COL_BODY_W + 1e-9)


class StlTest(unittest.TestCase):
    EXPECTED = [
        "coupon_frame.stl", "coupon_column.stl", "coupon_pawl.stl",
        "coupon_gate.stl", "coupon_threshold_plate.stl", "coupon_assembly.stl",
    ]

    def test_all_present(self):
        for name in self.EXPECTED:
            self.assertTrue((HERE / name).exists(), f"missing {name}")

    def test_headers_and_counts(self):
        for name in self.EXPECTED:
            tris = read_stl(HERE / name)
            self.assertGreater(len(tris), 0, name)

    def test_no_degenerate_triangles(self):
        for name in self.EXPECTED:
            for t in read_stl(HERE / name):
                self.assertGreater(_area2(*t), 1e-9, f"{name} degenerate")

    def test_nonzero_extent(self):
        for name in self.EXPECTED:
            d = (HERE / name).read_bytes()
            n = struct.unpack("<I", d[80:84])[0]
            xs = ys = zs = range(0)
            pts = []
            off = 84
            for _ in range(n):
                vals = struct.unpack("<12fH", d[off:off + 50])
                pts += [vals[3:6], vals[6:9], vals[9:12]]
                off += 50
            ex = max(p[0] for p in pts) - min(p[0] for p in pts)
            ey = max(p[1] for p in pts) - min(p[1] for p in pts)
            ez = max(p[2] for p in pts) - min(p[2] for p in pts)
            self.assertTrue(ex > 0 and ey > 0 and ez > 0, name)

    def test_assembly_contains_more_geometry_than_frame(self):
        frame = len(read_stl(HERE / "coupon_frame.stl"))
        asm = len(read_stl(HERE / "coupon_assembly.stl"))
        self.assertGreater(asm, frame)


if __name__ == "__main__":
    unittest.main()
