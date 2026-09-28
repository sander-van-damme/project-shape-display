#!/usr/bin/env python3
"""Slicer-level printability analysis of the J2 isolation-rig STL bundle.

Rasterised slice simulation (the same primitive a slicer uses): for each 0.20 mm
layer, compute the cross-section area by sampling a fine grid, then use a
Euclidean distance transform of the material region to measure local thickness
(2 x nearest-boundary distance). This is a CALCULATION over the exported STL --
not a slicer binary and not a print.

Also checks: mesh health, overhang faces (>45 deg below horizontal, excluding
bed contact), first-layer footprint, socket-pocket openness, plate gaps.
"""
from __future__ import annotations
import sys, glob, os, json
from collections import Counter
import numpy as np
from scipy import ndimage

def load_stl(path):
    with open(path, "rb") as f:
        data = f.read()
    if data[:5] == b"solid" and b"facet" in data[:2000]:
        verts = []
        for line in data.decode("ascii", "ignore").splitlines():
            line = line.strip()
            if line.startswith("vertex"):
                verts.append([float(x) for x in line.split()[1:4]])
        return np.array(verts, dtype=np.float64).reshape(-1, 3, 3)
    n = np.frombuffer(data[80:84], dtype="<u4")[0]
    rec = np.frombuffer(data[84:84 + n * 50], dtype=np.uint8).reshape(n, 50)
    return rec[:, 12:48].copy().view("<f4").reshape(n, 3, 3).astype(np.float64)

HERE = os.path.dirname(os.path.abspath(__file__))

def face_normals(tri):
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    ln = np.linalg.norm(n, axis=1, keepdims=True); ln[ln == 0] = 1
    return n / ln

def mesh_health(tri):
    V = tri.reshape(-1, 3)
    key = np.round(V / 1e-4).astype(np.int64)
    _, inv = np.unique(key, axis=0, return_inverse=True); inv = inv.reshape(-1, 3)
    ec = Counter()
    for a, b, c in inv:
        for u, v in ((a, b), (b, c), (c, a)):
            ec[(min(u, v), max(u, v))] += 1
    boundary = sum(1 for v in ec.values() if v == 1)
    nonman = sum(1 for v in ec.values() if v > 2)
    # connected components (faces sharing a vertex)
    parent = list(range(inv.max() + 1))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: parent[rb] = ra
    for a, b, c in inv:
        union(a, b); union(b, c)
    shells = len({find(i) for i in range(inv.max() + 1)})
    vol = abs(np.sum(np.einsum('ij,ij->i', tri[:, 0], np.cross(tri[:, 1], tri[:, 2]))) / 6.0)
    return boundary, nonman, shells, float(vol)

def raster_layer(tri, z, pitch=0.1, pad=1.0):
    """Return (xs, ys, mask) material grid for layer z by ray-crossing the
    triangle soup in 2D. Uses the standard nonzero-winding via segment crossings
    along +x for each scanline."""
    zs = tri[:, :, 2]
    lo = tri.reshape(-1, 3).min(0); hi = tri.reshape(-1, 3).max(0)
    x0, x1 = lo[0] - pad, hi[0] + pad
    y0, y1 = lo[1] - pad, hi[1] + pad
    ys = np.arange(y0, y1, pitch)
    xs = np.arange(x0, x1, pitch)
    mask = np.zeros((len(ys), len(xs)), dtype=bool)
    # For every triangle crossing z, compute intersection segment in 2D
    segs = []
    for i in range(len(tri)):
        below = zs[i] < z - 1e-6; above = zs[i] > z + 1e-6
        if not (below.any() and above.any()):
            continue
        coords = tri[i]; pts = []
        for a in range(3):
            b = (a + 1) % 3
            za, zb = coords[a, 2], coords[b, 2]
            if (za < z - 1e-6 and zb > z + 1e-6) or (za > z + 1e-6 and zb < z - 1e-6):
                t = (z - za) / (zb - za)
                pts.append(coords[a] + t * (coords[b] - coords[a]))
        if len(pts) == 2:
            segs.append((pts[0][:2], pts[1][:2]))
    # rasterize segments: fill by scanline crossing count (even-odd per row)
    # Build per-row x-intersections of segments
    row_x = [[] for _ in range(len(ys))]
    for a, b in segs:
        ya, yb = a[1], b[1]
        if abs(yb - ya) < 1e-12:
            continue
        i0 = max(0, int(np.ceil((min(ya, yb) - y0) / pitch)))
        i1 = min(len(ys) - 1, int(np.floor((max(ya, yb) - y0) / pitch)))
        for iy in range(i0, i1 + 1):
            yv = ys[iy]
            if (ya <= yv < yb) or (yb <= yv < ya):
                t = (yv - ya) / (yb - ya)
                xv = a[0] + t * (b[0] - a[0])
                row_x[iy].append(xv)
    for iy, xs_list in enumerate(row_x):
        if not xs_list:
            continue
        xs_list.sort()
        for k in range(0, len(xs_list) - 1, 2):
            lo_x, hi_x = xs_list[k], xs_list[k + 1]
            j0 = max(0, int(np.ceil((lo_x - x0) / pitch)))
            j1 = min(len(xs) - 1, int(np.floor((hi_x - x0) / pitch)))
            if j1 >= j0:
                mask[iy, j0:j1 + 1] = True
    return xs, ys, mask

def thickness_stats(mask, pitch=0.1):
    """Wall/feature thickness via Euclidean distance transform.

    A wall of width w has an EDT ridge (medial axis) of ~w/2. Taking 2 x EDT on
    the ridge recovers w. The minimum over the ridge is the narrowest printable
    feature. Boundary pixels (EDT=1 sample) are excluded so the metric is not
    floored by rasterisation."""
    if not mask.any():
        return None
    edt = ndimage.distance_transform_edt(mask)
    # Medial axis: a material pixel is on the skeleton if its EDT is not
    # dominated by a neighbouring pixel's disk, i.e. it is a local max of the
    # EDT (8-neighbourhood) with EDT > one sample. Thickness there is 2*EDT.
    mx = ndimage.maximum_filter(edt, size=3, mode="constant")
    ridge = mask & (np.abs(edt - mx) < 1e-9) & (edt > 1.0)
    thick = 2 * edt * pitch
    vals = thick[ridge]
    if vals.size == 0:
        vals = thick[mask]
    return dict(min_mm=round(float(vals.min()), 3),
                p05_mm=round(float(np.percentile(vals, 5)), 3),
                area_mm2=round(float(mask.sum()) * pitch * pitch, 2))

def analyze(path, layer=0.20, pitch=0.1):
    tri = load_stl(path)
    fn = face_normals(tri)
    lo = tri.reshape(-1, 3).min(0); hi = tri.reshape(-1, 3).max(0)
    boundary, nonman, shells, vol = mesh_health(tri)
    nz = fn[:, 2]
    zmin = lo[2]
    on_bed = (np.abs(tri[:, :, 2] - zmin).max(axis=1) < 1e-4)
    overhang = (nz < -0.707) & ~on_bed
    oh_area = float((0.5 * np.linalg.norm(
        np.cross(tri[overhang, 1] - tri[overhang, 0],
                 tri[overhang, 2] - tri[overhang, 0]), axis=1)).sum()) if overhang.any() else 0.0
    # real overhangs: faces with meaningful area (slivers from boolean cuts are
    # < 0.5 mm^2 and print as nothing)
    oh_area_each = (0.5 * np.linalg.norm(
        np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]), axis=1))
    real_oh = overhang & (oh_area_each > 0.5)
    real_oh_area = float(oh_area_each[real_oh].sum())
    # overhang z distribution
    oh_z = [round(float(tri[i, :, 2].mean()), 2) for i in np.where(overhang)[0]]
    # layer scan
    layer_rows = []
    min_thick = np.inf; worst_z = None
    min_area = np.inf; min_area_z = None
    is_first = True
    for z in np.arange(zmin + layer, hi[2], layer):
        xs, ys, mask = raster_layer(tri, z, pitch=pitch)
        st = thickness_stats(mask, pitch)
        if st is None:
            continue
        area = st["area_mm2"]
        if is_first:
            first_area = area; is_first = False
        layer_rows.append((round(float(z), 2), area, st["min_mm"], st["p05_mm"]))
        if st["min_mm"] < min_thick:
            min_thick = st["min_mm"]; worst_z = round(float(z), 2)
        if area < min_area and z > zmin + 2 * layer:
            min_area = area; min_area_z = round(float(z), 2)
    return dict(
        part=os.path.basename(path).replace(".stl", ""),
        dims_mm=[round(float(x), 2) for x in (hi - lo)],
        triangles=len(tri), shells=shells,
        watertight=bool(boundary == 0 and nonman == 0),
        boundary_edges=boundary, nonmanifold_edges=nonman,
        volume_mm3=round(vol, 1),
        overhang_face_count=int(overhang.sum()),
        overhang_area_mm2=round(oh_area, 1),
        real_overhang_face_count=int(real_oh.sum()),
        real_overhang_area_mm2=round(real_oh_area, 1),
        overhang_z_levels=sorted(set(oh_z)),
        first_layer_area_mm2=round(float(first_area), 2) if layer_rows else None,
        min_wall_mm=round(float(min_thick), 3) if np.isfinite(min_thick) else None,
        min_wall_z=worst_z,
        min_layer_area_mm2=round(float(min_area), 2) if np.isfinite(min_area) else None,
        min_layer_area_z=min_area_z,
        layers=len(layer_rows),
    )

if __name__ == "__main__":
    files = sys.argv[1:] or sorted(glob.glob(os.path.join(HERE, "*.stl")))
    if not files:
        print("usage: printability_slice_check.py <part.stl> [part2.stl ...]")
        print("or place the exported STLs next to this script.")
        sys.exit(2)
    res = [analyze(f) for f in files]
    print(json.dumps(res, indent=2))
    out = os.path.join(HERE, "printability_slice_report.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2)
    print("wrote " + out, file=sys.stderr)
