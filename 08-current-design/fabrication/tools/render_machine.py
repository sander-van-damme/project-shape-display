#!/usr/bin/env python3
"""DND-88 board-viewable renders of the WHOLE S5-R machine assembled.

WHAT THIS ADDS
--------------
DND-69 (`render_images.py`) renders every part plus a 3x3 per-cell register
cluster. It does **not** show the whole machine assembled. The board asked for
"images of everything assembled" (DND-88, child of DND-68). This tool composes
the FULL S5-R machine from the committed part STLs at their real assembly
positions and rasterizes it:

  * the 3x3 cartridge field (411.48 x 411.48 mm, the real field envelope:
    3 x 27 = 81 cell columns across, 80 used);
  * the 3x3 platen-module lift deck under it;
  * the perimeter lift-frame rails and corner guide brackets;
  * one rack strip + sourced steel rod per driven row (witness rows);
  * the bank drive housing at the -X edge and the writer carriage at the +X edge;
  * a documented representative 9x9-cell sub-block (81 of the 6,400 cells) with
    every rotor / pawl / keeper / detent installed, so the register reads at a
    legible scale. The full 6,400 installed cells are NOT individually modelled --
    that is stated on every such image.

It also renders an **exploded view of the complete assembly** (DND-68 board ask
`3075ea65`): the same committed solids displaced along +Z by a documented
explosion ladder (`EXPLODE_DZ`), top-to-bottom drive / register / cartridge field
/ witness rack+rod / platen deck / frame rails / guide brackets. Only rigid
translations of the same committed STLs -- no new geometry, no design change.

EVIDENCE CLASS: CAD render of the committed OpenSCAD meshes. NOT a print and NOT
a measurement ([DND-27]). An image is a visualisation of geometry; it validates
nothing physical. No part has been printed and none will be.

WHY A SOFTWARE RASTERIZER
-------------------------
Identical to `render_images.py`: OpenSCAD's own PNG backend needs a GL context
that this container does not have. Every mesh here is a committed OpenSCAD STL,
rasterized by the shared software renderer imported from `render_images.py`
(numpy+Pillow; z-buffered, flat-Lambert). No new geometry is introduced; the
sourced steel rod is a bare cylinder (not printed).

USAGE
    python 08-current-design/fabrication/tools/render_machine.py
    python 08-current-design/fabrication/tools/render_machine.py --size 800
    python 08-current-design/fabrication/tools/render_machine.py --check
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
sys.path.insert(0, str(HERE))

# Reuse the DND-69 rasterizer/loader -- same renderer, no fork.
from render_images import (  # noqa: E402
    ACCENT_COLORS, ROD_COLOR, annotate, bbox_size, load_stl, rasterize,
    translate,
)

FAB = HERE.parent
REPO = FAB.parents[1]
STL_DIR = FAB / "stl"
IMG_DIR = FAB / "images"
RECORD = FAB / "manifests" / "render_machine_record.json"

# --- real S5-R geometry (mirror of scad/s5r_parts_common.scad) --------------
PITCH = 5.08
WALL = 0.90
PAWL_T = 0.90
KEEPER_T = 0.90
BAR_D = 6.0
RACK_STRIP_W = 3.0
CARTRIDGE_W = 137.16          # 27 * PITCH
FIELD_CARTS = 3               # 3 x 3 cartridges = 81 x 81 cells (80 used)
FRAME_RAIL = 8.0
PLATEN_T = 7.0                # platen_module bbox z-extent
RAIL_LEN = 145.16

# palette (0..1 RGB)
CART_COLOR = np.array([0.60, 0.66, 0.72], dtype=np.float64)
PLATEN_COLOR = np.array([0.72, 0.74, 0.78], dtype=np.float64)
RAIL_COLOR = np.array([0.55, 0.60, 0.66], dtype=np.float64)
HOUSING_COLOR = np.array([0.42, 0.46, 0.52], dtype=np.float64)
CARRIAGE_COLOR = np.array([0.78, 0.55, 0.35], dtype=np.float64)
BRACKET_COLOR = np.array([0.50, 0.58, 0.66], dtype=np.float64)

# the representative installed register sub-block (documented on every image)
SUB_CELLS = 9                 # 9 x 9 = 81 cells of the 6,400 modelled installed


def _field_centers(n=FIELD_CARTS):
    """Return the (x, y) centre of each cartridge tile in an n x n field."""
    span = n * CARTRIDGE_W
    return [((cx + 0.5) * CARTRIDGE_W - span / 2,
             (cy + 0.5) * CARTRIDGE_W - span / 2)
            for cx in range(n) for cy in range(n)]


def _rotz(tris, deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    r = np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])
    return tris @ r.T


def _cylinder(radius, length, axis="z", segs=40):
    ang = np.linspace(0, 2 * math.pi, segs, endpoint=False)
    ring = np.stack([np.cos(ang) * radius, np.sin(ang) * radius], axis=1)
    if axis == "z":
        a = np.concatenate([ring, np.zeros((segs, 1))], axis=1)
        b = np.concatenate([ring, np.full((segs, 1), length)], axis=1)
    elif axis == "x":
        a = np.concatenate([np.zeros((segs, 1)), ring], axis=1)
        b = np.concatenate([np.full((segs, 1), length), ring], axis=1)
    tris = []
    for i in range(segs):
        j = (i + 1) % segs
        tris += [[a[i], a[j], b[j]], [a[i], b[j], b[i]]]
    return np.asarray(tris, dtype=np.float64)


def _register_cell(rotor, pawl, keeper, detent, ox, oy):
    """One populated cell's moving parts at their real relative offsets."""
    return ([translate(rotor, (ox, oy, 0.0)),
             translate(pawl, (ox + PAWL_T / 2, oy, 0.0)),
             translate(keeper, (ox, oy + KEEPER_T / 2, 0.0)),
             translate(detent, (ox - WALL, oy, 0.0))],
            [ACCENT_COLORS["rotor"], ACCENT_COLORS["drive_pawl"],
             ACCENT_COLORS["keeper"], ACCENT_COLORS["detent_leaf"]])


# Explosion ladder in mm. Each functional group is displaced along +Z from its
# real assembly height so the stack reads top-to-bottom. `exploded=False` gives
# every group its true assembly offset (the assembled views).
EXPLODE_DZ = {
    "platen": -70.0,      # lift deck drops away from the cartridge field
    "cartridge": 0.0,     # cartridge field stays as the reference plane
    "register": 55.0,     # rotor/pawl/keeper/detent lift out of the cartridges
    "rack_rod": -35.0,    # witness rack strip + sourced rod drop below the field
    "rails": -120.0,      # perimeter lift-frame rails drop away
    "drive": 15.0,        # bank housing + writer carriage lift slightly
    "bracket": -95.0,     # corner guide brackets drop away
}


def _machine_meshes(sub_block=True, rods=True, drives=True, exploded=False):
    """Compose the whole S5-R machine from committed part STLs.

    Every solid is a committed STL placed at its real assembly offset; the only
    generated primitive is the sourced steel rod (a bare cylinder, not printed).
    With ``exploded=True`` each functional group is additionally displaced along
    +Z by ``EXPLODE_DZ`` (the stack order: drive / register / cartridge field /
    rack+rod / platen / rails / brackets) so the assembly order is visible. No
    geometry changes -- only rigid translation of the same committed solids.
    Returns (meshes, colors, meta).
    """
    cart = load_stl(STL_DIR / "cell_cartridge.stl")
    platen = load_stl(STL_DIR / "platen_module.stl")
    rail = load_stl(STL_DIR / "lift_frame_rail.stl")
    rack = load_stl(STL_DIR / "rack_strip.stl")

    dz = EXPLODE_DZ if exploded else {k: 0.0 for k in EXPLODE_DZ}

    meshes, colors = [], []
    centers = _field_centers()
    span = FIELD_CARTS * CARTRIDGE_W

    # --- platen lift deck (3x3 tiles) at the bottom of the stack -------------
    for (ox, oy) in centers:
        meshes.append(translate(platen, (ox, oy,
                                         -(BAR_D + 1.0) - PLATEN_T + dz["platen"])))
        colors.append(PLATEN_COLOR)

    # --- cartridge field (3x3 true 137.16 mm tiles) --------------------------
    for (ox, oy) in centers:
        meshes.append(translate(cart, (ox, oy, dz["cartridge"])))
        colors.append(CART_COLOR)

    # --- perimeter lift-frame rails (16): 2 per side, lap at cartridges ------
    rail_x = _rotz(rail, 90.0)
    for s in (-1, 1):
        for t in (-1, 1):
            meshes.append(translate(rail, (s * (span / 2) - RAIL_LEN / 2,
                                           t * (span / 2) - FRAME_RAIL / 2,
                                           dz["rails"])))
            colors.append(RAIL_COLOR)
            meshes.append(translate(rail_x, (t * (span / 2) - FRAME_RAIL / 2,
                                             -s * (span / 2) - RAIL_LEN / 2,
                                             dz["rails"])))
            colors.append(RAIL_COLOR)

    # --- representative installed register sub-block (81 of 6,400 cells) -----
    if sub_block:
        rotor = load_stl(STL_DIR / "rotor.stl")
        pawl = load_stl(STL_DIR / "drive_pawl.stl")
        keeper = load_stl(STL_DIR / "keeper.stl")
        detent = load_stl(STL_DIR / "detent_leaf.stl")
        cx0, cy0 = centers[len(centers) // 2]        # centre cartridge
        for gx in range(SUB_CELLS):
            for gy in range(SUB_CELLS):
                ox = cx0 + (gx - (SUB_CELLS - 1) / 2) * PITCH
                oy = cy0 + (gy - (SUB_CELLS - 1) / 2) * PITCH
                m, c = _register_cell(rotor, pawl, keeper, detent, ox, oy)
                m = [translate(t, (0.0, 0.0, dz["register"])) for t in m]
                meshes += m
                colors += c

    # --- one rack strip + sourced rod per driven row (witness rows) ----------
    if rods:
        n_witness = 3
        for r in range(n_witness):
            ry = (r - (n_witness - 1) / 2) * (span / (n_witness + 1))
            meshes.append(translate(rack, (-span / 2, ry - RACK_STRIP_W / 2,
                                           -(BAR_D + 1.0) + dz["rack_rod"])))
            colors.append(ACCENT_COLORS["rack_strip"])
            rod = _cylinder(BAR_D / 2, span + 40.0, axis="x")
            meshes.append(translate(rod, (-(span + 40.0) / 2, ry + 3.0,
                                          -(BAR_D + 1.0) - BAR_D / 2
                                          + dz["rack_rod"])))
            colors.append(ROD_COLOR)

    # --- purchased drive assemblies at the field edges ----------------------
    if drives:
        housing = load_stl(STL_DIR / "bank_drive_housing.stl")
        carriage = load_stl(STL_DIR / "writer_carriage.stl")
        bracket = load_stl(STL_DIR / "guide_bracket.stl")
        meshes.append(translate(housing, (-span / 2 - 60.0, -20.0,
                                          -(BAR_D + 1.0) + dz["drive"])))
        colors.append(HOUSING_COLOR)
        meshes.append(translate(carriage, (span / 2 + 22.0, 0.0, dz["drive"])))
        colors.append(CARRIAGE_COLOR)
        for sx in (-1, 1):
            for sy in (-1, 1):
                meshes.append(translate(bracket,
                                        (sx * (span / 2 - 20.0) - 8.0,
                                         sy * (span / 2) - 1.5,
                                         -10.0 + dz["bracket"])))
                colors.append(BRACKET_COLOR)

    meta = {
        "field_cartridges": FIELD_CARTS ** 2,
        "field_cell_columns": FIELD_CARTS * 27,
        "field_mm": [round(span, 2), round(span, 2)],
        "installed_cells_modelled": SUB_CELLS ** 2 if sub_block else 0,
        "installed_cells_full_field": 6400,
        "exploded": exploded,
        "explode_dz_mm": dz if exploded else None,
        "solid_count": len(meshes),
        "triangle_count": int(sum(len(m) for m in meshes)),
    }
    return meshes, colors, meta


MACHINE_VIEWS = [
    ("iso", 24.0, -52.0),
    ("top", 82.0, -90.0),
    ("front", 6.0, -90.0),
]

# the exploded whole-machine is shown iso + front (top adds little to a stack)
MACHINE_EXPLODED_VIEWS = [
    ("iso", 22.0, -55.0),
    ("front", 4.0, -90.0),
]

SUBTITLE = (
    "3x3 cartridge field = {cols}x{cols} cell envelope ({w:.0f} x {w:.0f} mm); "
    "register installed in {sub} of {full} cells (representative 9x9 sub-block), "
    "shown on the platen + frame | CAD render, not a print"
)

EXPLODE_SUBTITLE = (
    "EXPLODED whole-machine stack (same committed solids, rigid +Z offsets): "
    "drive / installed 9x9 register ({sub} of {full} cells, representative) / "
    "cartridge field {cols}x{cols} ({w:.0f} x {w:.0f} mm) / witness rack+rod / "
    "platen lift deck / lift-frame rails / guide brackets | CAD render, not a print"
)


def build_machine_images(size, record, exploded=False):
    meshes, colors, meta = _machine_meshes(sub_block=True, exploded=exploded)
    dims = bbox_size(np.concatenate(meshes, axis=0))
    tag = "exploded" if exploded else "assembled"
    print(f"[info] machine ({tag}): {meta['solid_count']} solids, "
          f"{meta['triangle_count']} tris, bbox "
          f"{dims[0]:.1f} x {dims[1]:.1f} x {dims[2]:.1f} mm")
    template = EXPLODE_SUBTITLE if exploded else SUBTITLE
    sub = template.format(cols=meta["field_cell_columns"],
                          w=meta["field_mm"][0],
                          sub=meta["installed_cells_modelled"],
                          full=meta["installed_cells_full_field"])
    views = MACHINE_EXPLODED_VIEWS if exploded else MACHINE_VIEWS
    for vname, elev, azim in views:
        t0 = time.time()
        # a wide exploded stack needs a looser aspect cap so it is not cropped
        cap = 3.1 if exploded else 2.4
        arr = rasterize(meshes, colors=colors, size=size,
                        elev=elev, azim=azim, fill=0.90, aspect_cap=cap)
        # assembled views keep the DND-88 filenames already on the branch;
        # exploded views get an explicit `_exploded_` infix.
        if exploded:
            out = IMG_DIR / f"assembly_full_machine_exploded_{vname}.png"
            title = f"S5-R full machine EXPLODED - {vname} view"
        else:
            out = IMG_DIR / f"assembly_full_machine_{vname}.png"
            title = f"S5-R full machine assembled - {vname} view"
        px = annotate(arr, title, sub, out)
        print(f"[ok] {out.relative_to(REPO)}  {px[0]}x{px[1]}  "
              f"({time.time() - t0:.1f}s)")
        record["images"].append({
            "file": str(out.relative_to(FAB)),
            "kind": "machine_exploded" if exploded else "machine_assembly",
            "machine": "S5-R", "view": vname, "exploded": exploded,
            "source_mesh": "stl/{cell_cartridge,platen_module,lift_frame_rail,"
                           "guide_bracket,rack_strip,bank_drive_housing,"
                           "writer_carriage,rotor,drive_pawl,keeper,"
                           "detent_leaf}.stl",
            "meta": meta,
        })


def build_subblock_images(size, record):
    """A zoomed 9x9 populated register sub-block (register parts + rack + rod)."""
    rotor = load_stl(STL_DIR / "rotor.stl")
    pawl = load_stl(STL_DIR / "drive_pawl.stl")
    keeper = load_stl(STL_DIR / "keeper.stl")
    detent = load_stl(STL_DIR / "detent_leaf.stl")
    rack = load_stl(STL_DIR / "rack_strip.stl")
    meshes, colors = [], []
    half = (SUB_CELLS - 1) / 2
    for gx in range(SUB_CELLS):
        for gy in range(SUB_CELLS):
            m, c = _register_cell(rotor, pawl, keeper, detent,
                                  (gx - half) * PITCH, (gy - half) * PITCH)
            meshes += m
            colors += c
    blk = SUB_CELLS * PITCH
    meshes.append(translate(rack, (-blk / 2, -RACK_STRIP_W / 2, -(BAR_D + 1.0))))
    colors.append(ACCENT_COLORS["rack_strip"])
    rod = _cylinder(BAR_D / 2, blk + 12.0, axis="x")
    meshes.append(translate(rod, (-(blk + 12.0) / 2, 3.0,
                                  -(BAR_D + 1.0) - BAR_D / 2)))
    colors.append(ROD_COLOR)
    sub = (f"{SUB_CELLS}x{SUB_CELLS} = {SUB_CELLS ** 2} installed cells at "
           f"{PITCH} mm pitch ({blk:.1f} x {blk:.1f} mm) -- {SUB_CELLS ** 2} of "
           f"6,400 | rotor (blue) + pawl (orange) + keeper (green) + detent "
           f"(violet) on rack strip (gold) + sourced rod | CAD render, not a print")
    for vname, elev, azim in (("iso", 26.0, -58.0), ("top", 80.0, -90.0),
                              ("front", 5.0, -90.0)):
        arr = rasterize(meshes, colors=colors, size=size,
                        elev=elev, azim=azim, fill=0.92, aspect_cap=2.2)
        out = IMG_DIR / f"assembly_register_9x9_{vname}.png"
        px = annotate(arr, f"S5-R installed register sub-block (9x9) - "
                           f"{vname} view", sub, out)
        print(f"[ok] {out.relative_to(REPO)}  {px[0]}x{px[1]}")
        record["images"].append({
            "file": str(out.relative_to(FAB)), "kind": "register_subblock",
            "machine": "S5-R", "view": vname,
            "cells_shown": SUB_CELLS ** 2, "cells_full_field": 6400,
            "source_mesh": "stl/{rotor,drive_pawl,keeper,detent_leaf,"
                           "rack_strip}.stl"})


def check_images(json_path: Path) -> int:
    """Verify every recorded image exists, is a valid PNG, and is non-blank."""
    if not json_path.exists():
        print(f"[FAIL] record missing: {json_path}")
        return 1
    rec = json.loads(json_path.read_text())
    fails = []
    for img in rec.get("images", []):
        p = FAB / img["file"]
        if not p.exists() or p.stat().st_size == 0:
            fails.append(f"{img['file']}: missing/empty")
            continue
        if p.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
            fails.append(f"{img['file']}: not a PNG")
            continue
        from PIL import Image
        with Image.open(p) as im:
            w, h = im.size
            if w < 200 or h < 200:
                fails.append(f"{img['file']}: too small {w}x{h}")
    # DND-92: the board-required exploded view of the complete assembly must be
    # present, so it cannot silently regress out of the record/CI.
    if not any(i.get("kind") == "machine_exploded"
               for i in rec.get("images", [])):
        fails.append("no exploded-view image of the complete assembly (DND-92)")
    for f in fails:
        print(f"[FAIL] {f}")
    total = len(rec.get("images", []))
    if fails:
        print(f"\nmachine-image check: FAIL ({len(fails)} problem(s))")
        return 1
    print(f"\nmachine-image check: PASS ({total} images, all present/valid)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--size", type=int, default=800, help="image edge in px")
    ap.add_argument("--json", default=str(RECORD))
    ap.add_argument("--check", action="store_true",
                    help="verify the committed machine images (no render)")
    args = ap.parse_args()

    if args.check:
        return check_images(Path(args.json))

    IMG_DIR.mkdir(parents=True, exist_ok=True)
    record = {
        "evidence_class": "CAD",
        "renderer": "software rasterizer (numpy+Pillow) over committed OpenSCAD STLs",
        "openscad_png_backend": "unavailable in-container (no GL/X); STLs are "
                                "real OpenSCAD output (render_fab_parts.py)",
        "not_a_print": True, "size_px": args.size, "images": [], "verdict": "PASS",
    }
    t0 = time.time()
    build_machine_images(args.size, record, exploded=False)
    build_machine_images(args.size, record, exploded=True)
    build_subblock_images(args.size, record)
    record["elapsed_s"] = round(time.time() - t0, 1)
    Path(args.json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json).write_text(json.dumps(record, indent=2) + "\n")
    n = len(record["images"])
    print(f"\nrender verdict: {record['verdict']}  ({n} images, "
          f"{record['elapsed_s']}s)  record: {Path(args.json).relative_to(REPO)}")
    print("CAD evidence only: not a print, not a measurement (DND-27).")
    return 0 if record["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
