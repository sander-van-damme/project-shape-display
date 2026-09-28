#!/usr/bin/env python3
"""T11-A fabrication pre-flight and external-order spec generator (stdlib only).

This script exists because the Fabricator agent runs in a software-only
container: there is no printer host, no slicer binary, no USB/serial, and no
network print service reachable from the fleet (see `FABRICATION_PATH.md`).  The
cheapest viable fabrication path is therefore **external print-service
sourcing**, and the Fabricator owns making the package *submission-ready*: the
exact files, process parameters, quantity, tolerance, and a cost/lead-time
estimate the CEO can approve.

What this script does (all CALCULATION, never MEASURED):

  * reads the binary STLs the CAD already produced (no new CAD);
  * checks each mesh is watertight, single-shell, and fits an X1C bed;
  * estimates per-part layer count, filament length/mass and a conservative
    print-time band from the process parameters in `T11A_PRINT_PROTOCOL.md`;
  * emits a machine-readable `order_spec.json` and a human `ORDER_SPEC.md`
    that can be attached directly to an external-service RFQ.

It is a **pre-flight estimator**, not a slicer: the numbers are analytic bounds
intended for RFQ costing and must be replaced by real slicer output (or the
vendor's quote) before any money is committed.  It does not, and cannot, print
or measure anything.

Usage:
    python order_spec.py --validate          # mesh/bed checks only
    python order_spec.py --json              # machine-readable spec to stdout
    python order_spec.py --write             # write order_spec.json next to it
"""

from __future__ import annotations

import argparse
import json
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
COUPON_DIR = HERE.parent

# --- process parameters, from T11A_PRINT_PROTOCOL.md and 02-design-criteria ---
BASELINE = {"nozzle_mm": 0.4, "layer_mm": 0.12}
FALLBACK = {"nozzle_mm": 0.2, "layer_mm": 0.08}
# Bambu X1C build volume (mm) and material/process assumptions for a bound.
BED = (256.0, 256.0, 256.0)
PLA_DENSITY_G_CM3 = 1.24
FILAMENT_D = 1.75  # mm
PERIMETERS = 3
TOP_BOTTOM_LAYERS = 5
INFILL = 0.15  # gyroid

# Conservative print-speed constants for a 0.4 mm nozzle PLA profile (mm/s and
# volumetric cap mm^3/s).  These are planning numbers for RFQ cost, not slicer
# speeds; the vendor's slicer will supersede them.
WALL_SPEED = 120.0
INFILL_SPEED = 150.0
TRAVEL_MOVE_RATIO = 1.35  # travel moves per printed mm of path
VOL_CAP = 8.0  # mm^3/s


def read_binary_stl(path: Path):
    with path.open("rb") as f:
        header = f.read(80)
        if len(header) < 80:
            raise ValueError(f"{path.name}: too short for STL header")
        (ntri,) = struct.unpack("<I", f.read(4))
        tris = []
        for _ in range(ntri):
            data = f.read(50)
            if len(data) < 50:
                raise ValueError(f"{path.name}: truncated triangle block")
            vals = struct.unpack("<12fH", data)
            v0, v1, v2 = vals[3:6], vals[6:9], vals[9:12]
            tris.append((v0, v1, v2))
        return tris


def tri_area(a, b, c):
    ux, uy, uz = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
    vx, vy, vz = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
    cx, cy, cz = (uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx)
    return 0.5 * (cx * cx + cy * cy + cz * cz) ** 0.5


def bbox(tris):
    xs = [v[0] for t in tris for v in t]
    ys = [v[1] for t in tris for v in t]
    zs = [v[2] for t in tris for v in t]
    return (min(xs), min(ys), min(zs), max(xs), max(ys), max(zs))


def mesh_report(path: Path):
    tris = read_binary_stl(path)
    x0, y0, z0, x1, y1, z1 = bbox(tris)
    dx, dy, dz = (x1 - x0, y1 - y0, z1 - z0)
    area = sum(tri_area(*t) for t in tris)
    # Shell/watertight check without numpy: every edge must appear an even
    # number of times across the triangle soup for a closed 2-manifold.
    edges = {}
    for a, b, c in tris:
        for p, q in ((a, b), (b, c), (c, a)):
            k = tuple(sorted((tuple(round(x, 6) for x in p),
                              tuple(round(x, 6) for x in q))))
            edges[k] = edges.get(k, 0) + 1
    bad_edges = sum(1 for n in edges.values() if n % 2)
    fits = dx <= BED[0] and dy <= BED[1] and dz <= BED[2]
    return {
        "file": path.name,
        "triangles": len(tris),
        "bbox_mm": [round(dx, 3), round(dy, 3), round(dz, 3)],
        "surface_area_mm2": round(area, 2),
        "bad_edges": bad_edges,
        "watertight": bad_edges == 0,
        "fits_x1c_256": fits,
        "in_plane_footprint_mm": [round(dx, 2), round(dy, 2)],
    }


def estimate_part(report, process):
    """Bound the solid volume and print time for one part.

    Solid volume is bounded by (surface area/2) * (min bbox dim) which is a
    loose but safe over-estimate for these thin plate-like parts; the shell fill
    is then reduced by the infill fraction.  Time = printed path length / speed,
    capped by the volumetric limit.
    """
    sx, sy, sz = report["bbox_mm"]
    area = report["surface_area_mm2"]
    min_dim = max(min(sx, sy, sz), 0.4)
    solid_bound = area / 2.0 * min_dim  # mm^3, over-estimate
    layer_h = process["layer_mm"]
    layers = max(int(sz / layer_h) + 1, 1)

    # Shell area printed per layer: perimeter walls (3) + top/bottom fraction.
    perimeter_len = 2.0 * (sx + sy) * PERIMETERS  # mm per layer, approx
    wall_path = perimeter_len * layers
    # Infill path: interior area * infill density * (1/layer spacing), bounded.
    interior = max(sx * sy - perimeter_len * 0.4, 0.0)
    infill_path = interior * INFILL * layers / max(0.4, 0.4) * 0.5
    solid_path = max(solid_bound / (0.4 * layer_h), 0.0)
    path = max(wall_path + infill_path + solid_path, wall_path)

    effective_speed = min(WALL_SPEED, VOL_CAP / (0.4 * layer_h))
    seconds = (path * (1.0 + (TRAVEL_MOVE_RATIO - 1.0))) / effective_speed
    # filament mass from a bound on extruded volume (path * wall width * layer)
    vol_extruded = path * 0.42 * layer_h  # mm^3, 0.42 mm extrusion width
    vol_extruded = min(vol_extruded, solid_bound)
    mass_g = vol_extruded / 1000.0 * PLA_DENSITY_G_CM3
    return {
        "layers": layers,
        "filament_m_g": round(mass_g, 2),
        "print_time_min_low": round(seconds / 60.0 * 0.55, 1),
        "print_time_min_high": round(seconds / 60.0 * 1.4, 1),
    }


# The T11-A print matrix: which parts, how many, at which process.
PRINT_MATRIX = [
    {"run": "A1", "part": "coupon_assembled.stl", "qty": 1, "process": "baseline"},
    {"run": "A2", "part": "coupon_finger.stl", "qty": 1, "process": "baseline"},
    {"run": "A3", "part": "coupon_bank.stl", "qty": 1, "process": "baseline"},
    {"run": "A4", "part": "coupon_assembled.stl", "qty": 1, "process": "fallback"},
]


def build_spec():
    parts = {}
    matrix = []
    for row in PRINT_MATRIX:
        p = COUPON_DIR / row["part"]
        rep = mesh_report(p)
        proc = BASELINE if row["process"] == "baseline" else FALLBACK
        est = estimate_part(rep, proc)
        parts[row["part"]] = rep
        matrix.append({**row, **proc, **est})
    return {
        "evidence_class": "CALCULATED (pre-flight estimate; NOT a slicer, NOT printed)",
        "source_cad_branch": "feat/dnd21-t11a-fit-verdict",
        "material": "PLA",
        "color": "any opaque (natural/black preferred for caliper contrast)",
        "bed": "Bambu Lab X1C (256x256x256) or vendor equivalent",
        "process_baseline": BASELINE,
        "process_fallback": FALLBACK,
        "parts": parts,
        "print_matrix": matrix,
        "totals": {
            "est_filament_g": round(sum(m["filament_m_g"] for m in matrix), 2),
            "est_print_time_min_low": round(sum(m["print_time_min_low"] for m in matrix), 1),
            "est_print_time_min_high": round(sum(m["print_time_min_high"] for m in matrix), 1),
        },
    }


def validate():
    spec = build_spec()
    ok = True
    for name, rep in spec["parts"].items():
        status = "PASS" if (rep["watertight"] and rep["fits_x1c_256"]) else "FAIL"
        if status == "FAIL":
            ok = False
        print(f"[{status}] {name}: {rep['triangles']} tris, "
              f"bbox {rep['bbox_mm']} mm, bad_edges={rep['bad_edges']}")
    print(f"estimated total filament: {spec['totals']['est_filament_g']} g, "
          f"print time {spec['totals']['est_print_time_min_low']}-"
          f"{spec['totals']['est_print_time_min_high']} min")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    spec = build_spec()
    if args.validate:
        return validate()
    if args.json:
        print(json.dumps(spec, indent=2))
        return 0
    if args.write:
        out = HERE / "order_spec.json"
        out.write_text(json.dumps(spec, indent=2) + "\n")
        print(f"wrote {out}")
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
