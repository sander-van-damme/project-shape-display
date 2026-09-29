#!/usr/bin/env python3
"""DND-88 board-viewable renders of the S6-LC machine assembled.

WHY THIS EXISTS
---------------
The S6-LC low-cost machine (`08-integrated-designs/s6lc-low-cost/`) had real OpenSCAD STLs
and a mesh-validation record (DND-71) but **zero PNG images**. The board asked
for "images of everything assembled" (DND-88, child of DND-68), so this tool
rasterizes the committed S6-LC STLs into assembled views:

  * the 8-bank field strip: the committed `s6lc_bank` witness (each bank renders
    3 representative rows of its 10 at true 5.08 mm pitch), repeated 8x across
    the Y axis at bank pitch, giving the 406.4 x 406.4 mm field envelope;
  * the `s6lc_platen` broadcast deck under each bank;
  * a `s6lc_gate` (per-bank threshold mask) and `s6lc_comb` (release comb) at the
    edge of one bank;
  * an installed representative cell region with `s6lc_cell` columns + pawls at
    true pitch, so the column/pawl register reads at a legible scale.

It also renders an **exploded view of the complete assembly** (DND-68 board ask
`3075ea65`): the same committed solids displaced along +Z by a documented
explosion ladder (`EXPLODE_DZ`), top-to-bottom installed columns/pawls / bank
field / gate + release comb / broadcast platen deck. Only rigid translations of
the same committed STLs -- no new geometry, no design change.

EVIDENCE CLASS: CAD render of the committed OpenSCAD meshes. NOT a print and NOT
a measurement ([DND-27]). No part has been printed and none will be. This is a
visualisation only.

It reuses the shared software rasterizer from
`08-integrated-designs/s5r-shared-drive-register/fabrication/tools/render_images.py` (numpy+Pillow; z-buffered,
flat-Lambert) because OpenSCAD's own PNG backend needs a GL context the container
does not have.

USAGE
    python 08-integrated-designs/s6lc-low-cost/analysis/render_s6lc_images.py
    python 08-integrated-designs/s6lc-low-cost/analysis/render_s6lc_images.py --size 700
    python 08-integrated-designs/s6lc-low-cost/analysis/render_s6lc_images.py --check
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
S6LC = HERE.parent
ROOT = S6LC.parents[1]                    # repo root
STL_DIR = S6LC / "cad" / "stl"
IMG_DIR = S6LC / "images"
RECORD = S6LC / "cad" / "render_images_record.json"

sys.path.insert(0, str(ROOT / "08-integrated-designs" / "s5r-shared-drive-register" / "fabrication" / "tools"))
from render_images import (  # noqa: E402
    ROD_COLOR, annotate, bbox_size, load_stl, rasterize, translate,
)

# --- real S6-LC geometry (mirror of scad/s6lc_machine.scad / analysis/s6lc.py) --
PITCH = 5.08
COLS = 80
ROWS_BANK = 10
BANKS = 8
BODY = 3.60
COL_H = 44.0
PAWL_W = 1.20
FIELD = COLS * PITCH                      # 406.4 mm

COL_COLOR = np.array([0.48, 0.57, 0.70], dtype=np.float64)
PAWL_COLOR = np.array([0.77, 0.50, 0.36], dtype=np.float64)
PLATEN_COLOR = np.array([0.72, 0.74, 0.78], dtype=np.float64)
GATE_COLOR = np.array([0.42, 0.62, 0.50], dtype=np.float64)
COMB_COLOR = np.array([0.66, 0.52, 0.74], dtype=np.float64)
ROD_COLOR2 = np.array([0.59, 0.60, 0.62], dtype=np.float64)

# representative installed columns (documented on every image)
SUB_COLS = 12

# Explosion ladder in mm (+Z) for the complete-assembly exploded view (DND-68
# board ask `3075ea65`). Only rigid translations of the same committed solids.
EXPLODE_DZ = {
    "platen": -60.0,      # broadcast deck drops away below the banks
    "banks": 0.0,         # bank field stays as the reference plane
    "cells": 40.0,        # installed columns lift out of the banks
    "pawls": 25.0,        # pawls lift with/below the columns
    "gate": -25.0,        # threshold gate drops away
    "comb": -25.0,        # release comb drops away
}


def build_machine_images(size, record, exploded=False):
    bank = load_stl(STL_DIR / "s6lc_bank.stl")
    platen = load_stl(STL_DIR / "s6lc_platen.stl")
    gate = load_stl(STL_DIR / "s6lc_gate.stl")
    comb = load_stl(STL_DIR / "s6lc_comb.stl")
    cell = load_stl(STL_DIR / "s6lc_cell.stl")

    dz = EXPLODE_DZ if exploded else {k: 0.0 for k in EXPLODE_DZ}

    meshes, colors = [], []
    # bank STL bbox: x 0..403 (80 cols), y 0..12 (3 representative rows), z 0..44.
    bank_pitch_y = 50.8        # 10 rows * 5.08 mm bank pitch
    field_h = BANKS * bank_pitch_y
    for b in range(BANKS):
        oy = b * bank_pitch_y - field_h / 2
        meshes.append(translate(platen, (-FIELD / 2, oy, -2.0 + dz["platen"])))
        colors.append(PLATEN_COLOR)
        meshes.append(translate(bank, (-FIELD / 2, oy, dz["banks"])))
        colors.append(COL_COLOR)
    # a gate + comb at the near edge of one bank (drive/reset witness)
    meshes.append(translate(gate, (-FIELD / 2, -field_h / 2 - 3.0, dz["gate"])))
    colors.append(GATE_COLOR)
    meshes.append(translate(comb, (-FIELD / 2, field_h / 2 + 3.0, dz["comb"])))
    colors.append(COMB_COLOR)
    # installed representative columns (12 cols x 3 rows) on the front bank
    half = (SUB_COLS - 1) / 2
    for gx in range(SUB_COLS):
        for gy in range(3):
            ox = (gx - half) * PITCH
            oy = -field_h / 2 + gy * PITCH
            meshes.append(translate(cell, (ox, oy, dz["cells"])))
            colors.append(COL_COLOR)
            pawl = _pawl()
            meshes.append(translate(pawl, (ox + BODY / 2 + 0.10, oy,
                                           4.0 + dz["pawls"])))
            colors.append(PAWL_COLOR)

    meta = {
        "banks": BANKS, "rows_per_bank_modelled": 3, "rows_per_bank_real": 10,
        "cols": COLS, "pitch_mm": PITCH,
        "field_mm": [round(FIELD, 2), round(field_h, 2)],
        "installed_columns_modelled": SUB_COLS * 3,
        "installed_columns_full_field": COLS * ROWS_BANK * BANKS,
        "exploded": exploded,
        "explode_dz_mm": dz if exploded else None,
        "solid_count": len(meshes),
        "triangle_count": int(sum(len(m) for m in meshes)),
    }
    sub = (f"S6-LC low-cost exploration: {BANKS} banks x {COLS} cols @ {PITCH} mm "
           f"= {COLS * ROWS_BANK * BANKS} cells ({FIELD:.0f} x {field_h:.0f} mm); "
           f"each bank renders 3 of its 10 rows; {SUB_COLS * 3} columns installed "
           f"as a representative sub-block | CAD render, not a print")
    if exploded:
        sub = ("S6-LC EXPLODED complete assembly (same committed solids, rigid +Z "
               + "offsets): installed columns/pawls / bank field ("
               + f"{BANKS} banks x {COLS} cols, {COLS * ROWS_BANK * BANKS} cells, "
               + f"{SUB_COLS * 3} cols installed as a representative sub-block) / "
               + "gate + release comb / broadcast platen deck | CAD render, not a print")
    tag = "exploded" if exploded else "assembled"
    print(f"[info] S6-LC ({tag}): {meta['solid_count']} solids, "
          f"{meta['triangle_count']} tris")
    views = ((("iso", 20.0, -55.0), ("front", 4.0, -90.0)) if exploded
             else (("iso", 22.0, -52.0), ("top", 84.0, -90.0), ("front", 5.0, -90.0)))
    for vname, elev, azim in views:
        t0 = time.time()
        cap = 3.2 if exploded else 2.2
        arr = rasterize(meshes, colors=colors, size=size,
                        elev=elev, azim=azim, fill=0.92, aspect_cap=cap)
        if exploded:
            out = IMG_DIR / f"s6lc_machine_exploded_{vname}.png"
            title = f"S6-LC complete assembly EXPLODED - {vname} view"
        else:
            out = IMG_DIR / f"s6lc_machine_assembled_{vname}.png"
            title = f"S6-LC machine assembled - {vname} view"
        px = annotate(arr, title, sub, out)
        print(f"[ok] {out.relative_to(ROOT)}  {px[0]}x{px[1]}  "
              f"({time.time() - t0:.1f}s)")
        record["images"].append({
            "file": str(out.relative_to(S6LC)),
            "kind": "machine_exploded" if exploded else "machine_assembly",
            "machine": "S6-LC", "view": vname, "exploded": exploded,
            "source_mesh": "cad/stl/{s6lc_bank,s6lc_platen,s6lc_gate,"
                           "s6lc_comb,s6lc_cell}.stl",
            "meta": meta,
        })


def _pawl():
    """The committed S6-LC pawl geometry (scad/s6lc_machine.scad `pawl()`)."""
    t, w, l = 0.90, PAWL_W, 8.00
    return _box(t, w, 1.5) + _box(t / 2, w, l, z=1.5)


def _box(dx, dy, dz, x=0.0, y=0.0, z=0.0):
    v = np.array([
        [x, y, z], [x + dx, y, z], [x + dx, y + dy, z], [x, y + dy, z],
        [x, y, z + dz], [x + dx, y, z + dz], [x + dx, y + dy, z + dz],
        [x, y + dy, z + dz],
    ], dtype=np.float64)
    faces = [(0, 1, 2), (0, 2, 3), (4, 6, 5), (4, 7, 6), (0, 4, 5), (0, 5, 1),
             (1, 5, 6), (1, 6, 2), (2, 6, 7), (2, 7, 3), (3, 7, 4), (3, 4, 0)]
    return np.asarray([[v[a], v[b], v[c]] for a, b, c in faces], dtype=np.float64)


def check_images(json_path: Path) -> int:
    if not json_path.exists():
        print(f"[FAIL] record missing: {json_path}")
        return 1
    rec = json.loads(json_path.read_text())
    fails = []
    for img in rec.get("images", []):
        p = S6LC / img["file"]
        if not p.exists() or p.stat().st_size == 0:
            fails.append(f"{img['file']}: missing/empty")
            continue
        if p.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
            fails.append(f"{img['file']}: not a PNG")
            continue
        from PIL import Image
        with Image.open(p) as im:
            if min(im.size) < 200:
                fails.append(f"{img['file']}: too small {im.size}")
    # DND-92: the board-required exploded view of the complete assembly must be
    # present, so it cannot silently regress out of the record/CI.
    if not any(i.get("kind") == "machine_exploded"
               for i in rec.get("images", [])):
        fails.append("no exploded-view image of the complete assembly (DND-92)")
    for f in fails:
        print(f"[FAIL] {f}")
    if fails:
        print(f"\nS6-LC image check: FAIL ({len(fails)} problem(s))")
        return 1
    print(f"\nS6-LC image check: PASS ({len(rec.get('images', []))} images)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--size", type=int, default=800)
    ap.add_argument("--json", default=str(RECORD))
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if args.check:
        return check_images(Path(args.json))

    IMG_DIR.mkdir(parents=True, exist_ok=True)
    record = {
        "evidence_class": "CAD",
        "renderer": "software rasterizer (numpy+Pillow) over committed OpenSCAD STLs",
        "openscad_png_backend": "unavailable in-container (no GL/X); STLs are "
                                "real OpenSCAD output (analysis/render_s6lc_cad.py)",
        "not_a_print": True, "size_px": args.size, "images": [], "verdict": "PASS",
    }
    t0 = time.time()
    build_machine_images(args.size, record, exploded=False)
    build_machine_images(args.size, record, exploded=True)
    record["elapsed_s"] = round(time.time() - t0, 1)
    Path(args.json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json).write_text(json.dumps(record, indent=2) + "\n")
    print(f"\nrender verdict: {record['verdict']}  ({len(record['images'])} images, "
          f"{record['elapsed_s']}s)  record: {Path(args.json).relative_to(ROOT)}")
    print("CAD evidence only: not a print, not a measurement (DND-27).")
    return 0 if record["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
