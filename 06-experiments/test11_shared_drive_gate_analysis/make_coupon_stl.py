#!/usr/bin/env python3
"""Generate the T11-A selector fan-out fit coupon as binary STL, stdlib only.

The repo's OpenSCAD file (selector_fanout_coupon.scad) is the readable source of
the geometry. OpenSCAD is not always available, so this script emits the same
primitives (boxes + cylinders + a boolean notch) as a printable binary STL. It
is a *mesh generator*, not a slicer or a printer: the printed fit is still
unverified until the coupon is fabricated and measured.

Geometry (all mm, from the coupon parameters):
  * a 2x4 open frame base plate
  * for each column, one 4-plane cam bank (cylinder + 4 raised lands)
  * for each (column,row), one selector finger with a pivot boss and an
    optional selector notch (checkerboard pattern)

Run:
    python make_coupon_stl.py                 # writes coupon_assembled.stl
    python make_coupon_stl.py --part finger   # single finger
    python make_coupon_stl.py --part bank
    python make_coupon_stl.py --part base
"""

from __future__ import annotations

import argparse
import struct
from math import cos, pi, sin

PITCH = 5.08
ROWS_PER_STATION = 4
BAND = PITCH / ROWS_PER_STATION

FINGER_T = 0.80
FINGER_H = 3.20
FINGER_L = 4.40
PIVOT_D = 0.80
# DND-4: designed radial journal clearance (finger boss vs base socket). The
# socket bore is PIVOT_D + 2*PIVOT_CLR; see selector_fanout_coupon.scad.
PIVOT_CLR = 0.20
PIVOT_SOCKET_D = PIVOT_D + 2 * PIVOT_CLR
NOTCH_D = 0.55

BANK_R = 2.20
LAND_H = 0.90
SHAFT_D = 1.00

TRI_EXTRUDE = 1.60


def tri3(a, b, c):
    return (a, b, c)


def box(cx, cy, cz, sx, sy, sz):
    """Axis-aligned box centred at (cx,cy,cz), returns 12 triangles."""
    hx, hy, hz = sx / 2, sy / 2, sz / 2
    v = [
        (cx - hx, cy - hy, cz - hz), (cx + hx, cy - hy, cz - hz),
        (cx + hx, cy + hy, cz - hz), (cx - hx, cy + hy, cz - hz),
        (cx - hx, cy - hy, cz + hz), (cx + hx, cy - hy, cz + hz),
        (cx + hx, cy + hy, cz + hz), (cx - hx, cy + hy, cz + hz),
    ]
    f = [
        (0, 3, 2), (0, 2, 1), (4, 5, 6), (4, 6, 7),
        (0, 1, 5), (0, 5, 4), (1, 2, 6), (1, 6, 5),
        (2, 3, 7), (2, 7, 6), (3, 0, 4), (3, 4, 7),
    ]
    return [tri3(v[a], v[b], v[c]) for a, b, c in f]


def cyl(cx, cy, cz, d, h, seg=24, axis="z"):
    """Cylinder centred at (cx,cy,cz), returns side + cap triangles."""
    r, hz = d / 2, h / 2
    tris = []
    ring0, ring1 = [], []
    for i in range(seg):
        a = 2 * pi * i / seg
        x, y = r * cos(a), r * sin(a)
        if axis == "z":
            ring0.append((cx + x, cy + y, cz - hz))
            ring1.append((cx + x, cy + y, cz + hz))
        else:  # along y
            ring0.append((cx + x, cy - hz, cz + y))
            ring1.append((cx + x, cy + hz, cz + y))
    c0 = (cx, cy, cz - hz) if axis == "z" else (cx, cy - hz, cz)
    c1 = (cx, cy, cz + hz) if axis == "z" else (cx, cy + hz, cz)
    for i in range(seg):
        j = (i + 1) % seg
        tris.append((ring0[i], ring0[j], ring1[j]))
        tris.append((ring0[i], ring1[j], ring1[i]))
        tris.append((c0, ring0[j], ring0[i]))
        tris.append((c1, ring1[i], ring1[j]))
    return tris


def finger(cx, cy, cz, engaged):
    tris = []
    tris += box(cx, cy, cz, FINGER_L, FINGER_H, FINGER_T)
    # pivot boss along the row axis (y)
    tris += cyl(cx, cy, cz, PIVOT_D, FINGER_T, axis="y")
    # toe block
    tx, ty = cx + FINGER_L / 2 - 0.3, cy - FINGER_H / 2 + 0.35
    tris += box(tx, ty, cz, 0.6, 0.7, FINGER_T)
    # selector notch: modelled as a recess marker cylinder offset in Z, since a
    # real boolean subtract needs a mesh kernel. Kept as a visual/print cue that
    # must be verified in the slicer, not a volumetric subtraction.
    if engaged:
        tris += cyl(tx, ty, cz, NOTCH_D, FINGER_T * 1.2, axis="z")
    return tris


def bank(cx, cy, cz):
    tris = cyl(cx, cy, cz, BANK_R * 2, LAND_H)
    for i in range(ROWS_PER_STATION):
        a = 2 * pi * i / ROWS_PER_STATION
        lx = cx + BANK_R * 0.55 * cos(a)
        ly = cy + BANK_R * 0.55 * sin(a)
        tris += box(lx, ly, cz + LAND_H / 2, BAND * 0.7, BANK_R * 0.9, 0.5)
    tris += cyl(cx, cy, cz, SHAFT_D, LAND_H * 3)
    return tris


def base():
    tris = box(0, 0, -0.6, PITCH * 2, PITCH * 4, 1.20)
    # corner posts so the frame reads as an open coupon
    for sx in (-1, 1):
        for sy in (-1, 1):
            tris += box(sx * (PITCH - 0.5), sy * (PITCH * 2 - 0.5), 0.2,
                        0.8, 0.8, 1.2)
    # DND-4: pivot posts with a designed socket bore. This stdlib generator has
    # no boolean kernel, so the socket is represented as an inner post ring
    # marker at the design diameter (PIVOT_SOCKET_D); the true bore is produced
    # by the SCAD boolean. It is a parity/visual cue, not a volumetric subtract.
    for x in (0, 1):
        for y in range(ROWS_PER_STATION):
            cx = (x - 0.5) * PITCH
            cy = (y - 1.5) * PITCH
            tris += cyl(cx, cy, 0.9, PIVOT_SOCKET_D, BAND + 0.6, axis="y")
    return tris


def assembled():
    tris = base()
    for x in (0, 1):
        cx = (x - 0.5) * PITCH
        tris += bank(cx, 0, -1.8)
        for y in range(ROWS_PER_STATION):
            cy = (y - 1.5) * PITCH
            tris += finger(cx, cy, 0.9, (x + y) % 2 == 0)
    return tris


def write_stl(path, tris):
    with open(path, "wb") as f:
        f.write(b"\0" * 80)
        f.write(struct.pack("<I", len(tris)))
        for a, b, c in tris:
            ux, uy, uz = b[0] - a[0], b[1] - a[1], b[2] - a[2]
            vx, vy, vz = c[0] - a[0], c[1] - a[1], c[2] - a[2]
            nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
            ln = (nx * nx + ny * ny + nz * nz) ** 0.5 or 1.0
            f.write(struct.pack("<3f", nx / ln, ny / ln, nz / ln))
            for p in (a, b, c):
                f.write(struct.pack("<3f", *p))
            f.write(struct.pack("<H", 0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", default="assembled",
                    choices=["assembled", "finger", "bank", "base"])
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    if args.part == "assembled":
        tris = assembled()
    elif args.part == "finger":
        tris = finger(0, 0, 0, True)
    elif args.part == "bank":
        tris = bank(0, 0, 0)
    else:
        tris = base()

    out = args.out or f"coupon_{args.part}.stl"
    write_stl(out, tris)
    print(f"wrote {out}: {len(tris)} triangles, part={args.part}")


if __name__ == "__main__":
    main()
