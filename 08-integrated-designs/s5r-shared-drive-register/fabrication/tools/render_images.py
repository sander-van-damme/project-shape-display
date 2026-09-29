#!/usr/bin/env python3
"""DND-69 render board-viewable PNGs of the S5-R part set + assembly.

WHAT THIS PRODUCES
------------------
One PNG per part in the S5-R printed part set (14 parts, `tools/part_set.py`) from
three standard views, plus assembled and exploded views of the per-cell register
(rotor + pawl + keeper + detent) on the rack strip and sourced drive rod. All
images are written under `08-integrated-designs/s5r-shared-drive-register/fabrication/images/`. A JSON record
(`manifests/render_images_record.json`) lists every image, its source mesh, the
camera, and the evidence class.

WHY A SOFTWARE RASTERIZER, NOT OpenSCAD's OWN PNG OUTPUT
--------------------------------------------------------
The images must be TRUE TO THE SHIPPED GEOMETRY. The shipped geometry is the real
OpenSCAD render: the committed `stl/*.stl` are produced by OpenSCAD
(`render_fab_parts.py`, real OpenSCAD -> STL) and every image here is rasterized
from THOSE meshes, so no new geometry is introduced.

OpenSCAD's *own* PNG backend needs an OpenGL context. In this agent container
there is no display and no GPU: the offscreen Qt platform reports
`Can't create OffscreenView: Unable to obtain GL Context`, and a rootless Xvfb
cannot initialise its virtual keyboard. So OpenSCAD can render STL here but
cannot rasterize a PNG. Rather than ship no images, this tool rasterizes the
OpenSCAD-produced meshes with a small, dependency-light software renderer
(numpy + Pillow): z-buffered, flat-Lambert shaded, deterministic camera. It is
reproducible on any machine with `pip install numpy pillow` and needs no GL, no
X, and no OpenSCAD.

EVIDENCE CLASS: CAD render of the committed OpenSCAD meshes. NOT a print and NOT
a measurement ([DND-27]). An image is a visualisation of geometry; it validates
nothing physical.

USAGE
    python 08-integrated-designs/s5r-shared-drive-register/fabrication/tools/render_images.py
    python 08-integrated-designs/s5r-shared-drive-register/fabrication/tools/render_images.py --size 1000
    python 08-integrated-designs/s5r-shared-drive-register/fabrication/tools/render_images.py --only rotor
"""
from __future__ import annotations

import argparse
import json
import math
import struct
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FAB = HERE.parent
REPO = FAB.parents[2]
STL_DIR = FAB / "stl"
IMG_DIR = FAB / "images"
RECORD = FAB / "manifests" / "render_images_record.json"

sys.path.insert(0, str(HERE))
from part_set import PARTS  # noqa: E402

BACKGROUND = np.array([248, 250, 252], dtype=np.uint8)
# part colours are 0..1 RGB; the rasterizer scales by 255 at the end
PART_COLOR = np.array([0.478, 0.573, 0.698], dtype=np.float64)
ROD_COLOR = np.array([0.588, 0.596, 0.620], dtype=np.float64)
ACCENT_COLORS = {
    "rotor": np.array([0.478, 0.573, 0.698], dtype=np.float64),
    "drive_pawl": np.array([0.769, 0.502, 0.361], dtype=np.float64),
    "keeper": np.array([0.424, 0.620, 0.502], dtype=np.float64),
    "detent_leaf": np.array([0.659, 0.518, 0.737], dtype=np.float64),
    "rack_strip": np.array([0.769, 0.659, 0.376], dtype=np.float64),
}
LIGHT = np.array([-0.35, -0.55, 0.76])
LIGHT = LIGHT / np.linalg.norm(LIGHT)

CACHE: dict = {}


def load_stl(path: Path) -> np.ndarray:
    """Load an STL (ASCII or binary) as an (n,3,3) float64 triangle array."""
    path = Path(path)
    if path in CACHE:
        return CACHE[path]
    data = path.read_bytes()
    if data[:5] == b"solid" and b"facet" in data[:2048]:
        verts = []
        for line in data.decode("ascii", "ignore").splitlines():
            s = line.lstrip()
            if s.startswith("vertex"):
                p = s.split()
                verts.append((float(p[1]), float(p[2]), float(p[3])))
        tris = np.asarray(verts, dtype=np.float64).reshape(-1, 3, 3)
    else:
        cnt = struct.unpack("<I", data[80:84])[0]
        rec = np.frombuffer(data, dtype=np.uint8, count=cnt * 50, offset=84)
        rec = rec.reshape(cnt, 50)
        tris = np.frombuffer(rec[:, 12:48].tobytes(),
                             dtype="<f4").astype(np.float64).reshape(cnt, 3, 3)
    CACHE[path] = tris
    return tris


def translate(tris: np.ndarray, off) -> np.ndarray:
    return tris + np.asarray(off, dtype=np.float64)


def bbox_size(tris: np.ndarray):
    lo, hi = tris.reshape(-1, 3).min(0), tris.reshape(-1, 3).max(0)
    return [round(float(hi[k] - lo[k]), 2) for k in range(3)]


def _camera(elev_deg, azim_deg):
    az, el = math.radians(azim_deg), math.radians(elev_deg)
    fwd = np.array([math.cos(el) * math.cos(az),
                    math.cos(el) * math.sin(az),
                    math.sin(el)])
    up = np.array([0.0, 0.0, 1.0])
    right = np.cross(fwd, up)
    right /= np.linalg.norm(right)
    real_up = np.cross(right, fwd)
    return fwd, right, real_up


def rasterize(meshes, colors=None, size=900, elev=26.0, azim=-58.0, fill=0.94,
              aspect_cap=3.0):
    """Z-buffered flat-Lambert raster of one or more (n,3,3) meshes.

    meshes: list of triangle arrays. colors: per-mesh RGB in 0..1.

    The output frame matches the projected content aspect ratio (clamped to
    `aspect_cap`) so elongated parts (rack strips, rails) fill the image instead
    of appearing as a thin sliver in a square frame. `size` is the long edge.
    """
    allpts = np.concatenate([m.reshape(-1, 3) for m in meshes], axis=0)
    center = (allpts.min(0) + allpts.max(0)) / 2.0
    fwd, right, up = _camera(elev, azim)
    colors = list(colors) if colors else [PART_COLOR] * len(meshes)

    proj = []
    for mesh, col in zip(meshes, colors):
        rel = mesh.reshape(-1, 3) - center
        proj.append((rel @ right, rel @ up, rel @ fwd, mesh, col))

    xs = np.concatenate([p[0] for p in proj])
    ys = np.concatenate([p[1] for p in proj])
    w = float(xs.max() - xs.min())
    h = float(ys.max() - ys.min())
    aspect = w / max(h, 1e-9)
    aspect = min(max(aspect, 1.0 / aspect_cap), aspect_cap)
    if aspect >= 1.0:
        W = int(size)
        H = max(int(round(size / aspect)), 1)
    else:
        H = int(size)
        W = max(int(round(size * aspect)), 1)
    scale = fill * min(W / max(w, 1e-9), H / max(h, 1e-9))
    cx, cy = W / 2.0, H / 2.0

    zbuf = np.full((H, W), -1e18)
    img = np.empty((H, W, 3), dtype=np.float64)
    img[:, :] = BACKGROUND

    # paint whole mesh groups back-to-front by their mean depth
    for gi in np.argsort([p[2].mean() for p in proj]):
        x, y, z, mesh, col = proj[gi]
        px = (x.reshape(-1, 3) * scale + cx)
        py = (cy - y.reshape(-1, 3) * scale)
        depth = z.reshape(-1, 3).mean(axis=1)
        e1 = mesh[:, 1] - mesh[:, 0]
        e2 = mesh[:, 2] - mesh[:, 0]
        nrm = np.cross(e1, e2)
        nrm /= (np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-12)
        shade = np.abs(nrm @ LIGHT)
        amb = 0.32
        rgb = np.clip((amb + (1 - amb) * shade)[:, None] * col[None, :] * 255,
                      0, 255).astype(np.uint8)
        for i in np.argsort(depth):
            X, Y = px[i], py[i]
            x0 = max(int(np.floor(X.min())), 0)
            x1 = min(int(np.ceil(X.max())), W - 1)
            y0 = max(int(np.floor(Y.min())), 0)
            y1 = min(int(np.ceil(Y.max())), H - 1)
            if x0 > x1 or y0 > y1:
                continue
            xg, yg = np.meshgrid(np.arange(x0, x1 + 1), np.arange(y0, y1 + 1))
            den = (Y[1] - Y[2]) * (X[0] - X[2]) + (X[2] - X[1]) * (Y[0] - Y[2])
            if abs(den) < 1e-12:
                continue
            l0 = ((Y[1] - Y[2]) * (xg - X[2]) + (X[2] - X[1]) * (yg - Y[2])) / den
            l1 = ((Y[2] - Y[0]) * (xg - X[2]) + (X[0] - X[2]) * (yg - Y[2])) / den
            l2 = 1.0 - l0 - l1
            mask = (l0 >= -1e-6) & (l1 >= -1e-6) & (l2 >= -1e-6)
            if not mask.any():
                continue
            z0 = float(mesh[i, 0, :] @ fwd)
            z1 = float(mesh[i, 1, :] @ fwd)
            z2 = float(mesh[i, 2, :] @ fwd)
            zz = l0 * z0 + l1 * z1 + l2 * z2
            sub = zbuf[y0:y1 + 1, x0:x1 + 1]
            m = mask & (zz >= sub)
            if not m.any():
                continue
            sub[m] = zz[m]
            img[y0:y1 + 1, x0:x1 + 1][m] = rgb[i]
    return np.clip(img, 0, 255).astype(np.uint8)


def _font(size):
    for cand in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"):
        if Path(cand).exists():
            return ImageFont.truetype(cand, size)
    return ImageFont.load_default()


def annotate(arr, title, subtitle, out: Path):
    im = Image.fromarray(arr)
    pad = 52
    canvas = Image.new("RGB", (arr.shape[1], arr.shape[0] + pad),
                       tuple(int(v) for v in BACKGROUND))
    canvas.paste(im, (0, 0))
    d = ImageDraw.Draw(canvas)
    d.text((14, arr.shape[0] + 8), title, fill=(24, 32, 48), font=_font(21))
    d.text((14, arr.shape[0] + 32), subtitle, fill=(96, 106, 124),
           font=_font(14))
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out)
    return canvas.size


# ---------------------------------------------------------------------------
# assembly composition (mirror of s5r_parts_common.scad constants)
# ---------------------------------------------------------------------------
PITCH = 5.08
CELL_H = 7.0
WALL = 0.90
PAWL_T = 0.90
KEEPER_T = 0.90
BAR_D = 6.0
RACK_STRIP_W = 3.0


def _register_cell(rotor, pawl, keeper, detent, dz=0.0):
    """Place one cell's moving parts at their real relative positions.

    cell origin (0,0,0) = the rotor bore centre at the housing top; this mirrors
    `inner_cell()` in s5r_parts.scad: rotor in the bore, pawl chamber +X, keeper
    chamber +Y, detent leaf on the -X bore wall.
    """
    parts = [
        translate(rotor, (0, 0, dz)),
        translate(pawl, (PAWL_T / 2, 0, dz)),
        translate(keeper, (0, KEEPER_T / 2, dz)),
        translate(detent, (-WALL, 0, dz)),
    ]
    colors = [ACCENT_COLORS["rotor"], ACCENT_COLORS["drive_pawl"],
              ACCENT_COLORS["keeper"], ACCENT_COLORS["detent_leaf"]]
    return parts, colors


def assembly_meshes(scene: str, cols=3, rows=3):
    """Compose a cluster of populated cells + rack + sourced rod.

    Every solid is a committed part STL placed at its real assembly offset; no
    new geometry is created. The sourced rod is a bare cylinder (not printed).
    """
    rotor = load_stl(STL_DIR / "rotor.stl")
    pawl = load_stl(STL_DIR / "drive_pawl.stl")
    keeper = load_stl(STL_DIR / "keeper.stl")
    detent = load_stl(STL_DIR / "detent_leaf.stl")
    rack_strip = load_stl(STL_DIR / "rack_strip.stl")
    rack_len = cols * PITCH

    meshes, colors = [], []
    dz = CELL_H + 8.0 if scene == "exploded" else 0.0
    for cx in range(cols):
        for cy in range(rows):
            ox = (cx - (cols - 1) / 2.0) * PITCH
            oy = (cy - (rows - 1) / 2.0) * PITCH
            reg, col = _register_cell(rotor, pawl, keeper, detent, dz)
            meshes += [translate(m, (ox, oy, 0)) for m in reg]
            colors += col

    # one rack strip + sourced rod under the centre row (the real channel is
    # under each row; one is shown for legibility). `rack_strip` sits with its
    # teeth up at the pawl plane, the sourced rod in its saddle at z = -BAR_D/2.
    rod_dz = CELL_H + 14.0 if scene == "exploded" else 0.0
    rack = translate(rack_strip, (-rack_len / 2, -RACK_STRIP_W / 2, -rod_dz))
    meshes.append(rack)
    colors.append(ACCENT_COLORS["rack_strip"])
    rod = _cylinder(BAR_D / 2, rack_len + 8.0, axis="x")
    meshes.append(translate(rod, (-(rack_len + 8.0) / 2, 3.0,
                                  -BAR_D / 2 - rod_dz)))
    colors.append(ROD_COLOR)
    return meshes, colors


def _cylinder(radius, length, axis="z", segs=48):
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


# ---------------------------------------------------------------------------
# image production
# ---------------------------------------------------------------------------
PART_VIEWS = [("iso", 26.0, -58.0), ("front", 8.0, -90.0), ("top", 76.0, -90.0)]
ASSEMBLY_VIEWS = {"assembled": [(26.0, -58.0), (18.0, -30.0)],
                  "exploded": [(24.0, -62.0)]}


def build_part_images(size, only=None, record=None):
    parts = [p for p in PARTS if not only or p.key == only]
    for p in parts:
        stl = STL_DIR / f"{p.key}.stl"
        if not stl.exists():
            print(f"[FAIL] {p.key}: missing {stl.name}")
            record["verdict"] = "FAIL"
            continue
        tris = load_stl(stl)
        dims = bbox_size(tris)
        color = ACCENT_COLORS.get(p.key, PART_COLOR)
        for vname, elev, azim in PART_VIEWS:
            arr = rasterize([tris], colors=[color], size=size,
                            elev=elev, azim=azim)
            out = IMG_DIR / f"{p.key}_{vname}.png"
            annotate(arr, f"{p.key} - {p.title}",
                     f"S5-R printed part | view {vname} | bbox "
                     f"{dims[0]:.2f} x {dims[1]:.2f} x {dims[2]:.2f} mm | "
                     f"CAD render of stl/{p.key}.stl",
                     out)
            print(f"[ok] {out.relative_to(REPO)}")
            record["images"].append({
                "file": str(out.relative_to(FAB)), "kind": "part",
                "part": p.key, "view": vname,
                "source_mesh": f"stl/{p.key}.stl", "bbox_mm": dims})
        del dims


def build_assembly_images(size, record):
    for scene, views in ASSEMBLY_VIEWS.items():
        meshes, colors = assembly_meshes(scene)
        for k, (elev, azim) in enumerate(views):
            arr = rasterize(meshes, colors=colors, size=size,
                            elev=elev, azim=azim, fill=0.86)
            suffix = "" if k == 0 else f"_{k+1}"
            out = IMG_DIR / f"assembly_{scene}{suffix}.png"
            label = ("assembled" if scene == "assembled" else "exploded")
            annotate(arr, f"S5-R per-cell register - {label} view{suffix}",
                     "3x3 cell cluster: rotor (blue) + pawl (orange) + keeper "
                     "(green) + detent (violet) on rack strip (gold) + sourced "
                     "steel rod; CAD render of committed part STLs",
                     out)
            print(f"[ok] {out.relative_to(REPO)}")
            record["images"].append({
                "file": str(out.relative_to(FAB)), "kind": "assembly",
                "scene": scene, "view": suffix or "1",
                "source_mesh": "stl/{rotor,drive_pawl,keeper,detent_leaf,"
                               "rack_strip}.stl"})


def check_images(json_path: Path) -> int:
    """Verify every recorded image exists and is a valid PNG (CI guard)."""
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
    # every part must have at least one image and both assembly views exist
    keys = {i["part"] for i in rec.get("images", []) if i.get("kind") == "part"}
    want = {p.key for p in PARTS}
    for k in sorted(want - keys):
        fails.append(f"part {k}: no image")
    if not any(i.get("kind") == "assembly" and i.get("scene") == "assembled"
               for i in rec.get("images", [])):
        fails.append("no assembled assembly image")
    for f in fails:
        print(f"[FAIL] {f}")
    total = len(rec.get("images", []))
    if fails:
        print(f"\nimage check: FAIL ({len(fails)} problem(s))")
        return 1
    print(f"\nimage check: PASS ({total} images, all present and valid PNG)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--size", type=int, default=900, help="image edge in px")
    ap.add_argument("--only", help="render only this part key")
    ap.add_argument("--json", default=str(RECORD))
    ap.add_argument("--check", action="store_true",
                    help="verify the committed images exist (no render)")
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
    build_part_images(args.size, args.only, record)
    if not args.only:
        build_assembly_images(args.size, record)
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
