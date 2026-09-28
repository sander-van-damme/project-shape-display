#!/usr/bin/env python3
"""Validate the generated coupon STLs: header, triangle count and bounds.

Checks that the binary STLs are well-formed, that every vertex is finite, and
that each part fits the X1C 256x256x256 mm envelope. This is a MESH check, not a
slicer or print check.

Run: python verify_coupon_stl.py
"""

from __future__ import annotations

import struct
import sys
from pathlib import Path

BUILD_MM = 256.0


def read_stl(path: Path):
    data = path.read_bytes()
    if len(data) < 84:
        raise ValueError(f"{path}: too short")
    n = struct.unpack("<I", data[80:84])[0]
    expected = 84 + n * 50
    if len(data) != expected:
        raise ValueError(f"{path}: size {len(data)} != {expected} for {n} triangles")
    lo = [1e9] * 3
    hi = [-1e9] * 3
    for i in range(n):
        off = 84 + i * 50 + 12
        for v in range(3):
            x, y, z = struct.unpack("<3f", data[off + v * 12: off + v * 12 + 12])
            for k, c in enumerate((x, y, z)):
                if c != c or abs(c) > 1e6:
                    raise ValueError(f"{path}: non-finite vertex {c}")
                lo[k] = min(lo[k], c)
                hi[k] = max(hi[k], c)
    return n, lo, hi


def main() -> int:
    here = Path(__file__).parent
    parts = ["assembled", "finger", "bank", "base"]
    ok = True
    for p in parts:
        f = here / f"coupon_{p}.stl"
        if not f.exists():
            print(f"[SKIP] {f.name} not generated")
            continue
        n, lo, hi = read_stl(f)
        size = [hi[k] - lo[k] for k in range(3)]
        fits = all(s <= BUILD_MM for s in size)
        wellformed = n > 0 and all(hi[k] > lo[k] for k in range(3))
        verdict = "PASS" if (fits and wellformed) else "FAIL"
        print(f"[{verdict}] {f.name}: {n} tris, bbox "
              f"x={size[0]:.2f} y={size[1]:.2f} z={size[2]:.2f} mm, fits256={fits}")
        ok &= fits and wellformed
    print()
    print("ALL STL CHECKS PASS" if ok else "STL CHECK FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
