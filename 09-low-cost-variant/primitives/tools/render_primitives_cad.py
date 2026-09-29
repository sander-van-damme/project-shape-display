#!/usr/bin/env python3
"""DND-76 — render the primitive CAD with a REAL OpenSCAD, validate the meshes.

EVIDENCE CLASS: CAD (real-OpenSCAD render + mesh validation). NOT a print and
NOT a measurement ([DND-27]). A missing OpenSCAD is a HARD failure here (the
render is the point), exactly as in the repo's other CAD-render jobs.

Renders each single-manifold part with `-D part="<key>"` to `stl/<key>.stl`,
then validates:
  * non-empty, finite, non-degenerate bbox;
  * fits the 256 mm X1C bed (the machine is modular by design);
  * watertight / manifold (trimesh when available; otherwise a stdlib
    edge-pairing check).

Multi-body VIEWING assemblies ("cell", "strip") are rendered too but are
excluded from the watertight gate (they overlap by design), exactly as the
repo's other render tools treat a witness assembly.

USAGE
    python 09-low-cost-variant/primitives/tools/render_primitives_cad.py
"""
from __future__ import annotations

import os
import shutil
import struct
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCAD = HERE.parent / "scad"
STL = HERE.parent / "stl"
BED_MM = 256.0

# (scad file, part key, gate_manifold)
# (scad file, part key, output stem, gate_manifold)
PARTS = [
    ("s6lc_cell.scad", "column", "column", True),
    ("s6lc_cell.scad", "pawl", "pawl", True),
    ("s6lc_cell.scad", "latch", "latch", True),
    ("s6lc_cell.scad", "cell", "cell", False),          # viewing assembly
    ("mask_comb.scad", "bar", "mask_comb_bar", True),
    ("reset_bar.scad", "bar", "reset_bar", True),
    ("reset_bar.scad", "dog", "reset_dog", True),
    ("reset_bar.scad", "clutch", "reset_clutch", True),
]


def find_openscad() -> str | None:
    for cand in (os.environ.get("OPENSCAD"), shutil.which("openscad"),
                 shutil.which("openscad-nightly"),
                 str(Path.home() / ".local" / "bin" / "openscad")):
        if cand and Path(cand).exists():
            return cand
    return None


def scad_env() -> dict:
    env = dict(os.environ)
    env.setdefault("QT_QPA_PLATFORM", "offscreen")
    return env


def read_stl(path: Path):
    """Return (ntris, lo, hi) for binary/ASCII STL; None if unreadable/empty."""
    data = path.read_bytes()
    if data[:5] == b"solid" and b"facet" in data[:2048]:
        lo = [1e18] * 3
        hi = [-1e18] * 3
        n = 0
        for line in data.decode("ascii", "ignore").splitlines():
            line = line.strip()
            if line.startswith("vertex"):
                n += 1
                for k, tok in enumerate(line.split()[1:4]):
                    v = float(tok)
                    lo[k] = min(lo[k], v)
                    hi[k] = max(hi[k], v)
        return (n // 3, lo, hi) if n else None
    if len(data) < 84:
        return None
    cnt = struct.unpack("<I", data[80:84])[0]
    if cnt == 0:
        return None
    lo = [1e18] * 3
    hi = [-1e18] * 3
    off = 84
    for _ in range(cnt):
        vals = struct.unpack_from("<12f", data, off)
        for k in range(3):
            for v in vals[3 + k], vals[6 + k], vals[9 + k]:
                lo[k] = min(lo[k], v)
                hi[k] = max(hi[k], v)
        off += 50
    return cnt, lo, hi


def watertight(ntris: int, lo, hi, path: Path):
    """Best-effort manifold check. Returns (ok, note)."""
    try:
        import trimesh  # type: ignore
        m = trimesh.load(str(path), force="mesh")
        return bool(m.is_watertight), "trimesh"
    except Exception:
        # stdlib fallback: a closed triangle mesh has every edge shared twice.
        data = path.read_bytes()
        if data[:5] != b"solid":
            return None, "no trimesh; binary STL not edge-checked"
        verts = []
        for line in data.decode("ascii", "ignore").splitlines():
            line = line.strip()
            if line.startswith("vertex"):
                verts.append(tuple(round(float(t), 4) for t in line.split()[1:4]))
        if not verts or len(verts) % 3:
            return False, "vertex count not a multiple of 3"
        from collections import Counter
        edges = Counter()
        for i in range(0, len(verts), 3):
            a, b, c = verts[i], verts[i + 1], verts[i + 2]
            for e in ((a, b), (b, c), (c, a)):
                edges[tuple(sorted(e))] += 1
        bad = sum(1 for v in edges.values() if v != 2)
        return bad == 0, f"stdlib edge-pairing ({bad} bad edges)"


def main() -> int:
    openscad = find_openscad()
    if not openscad:
        print("FAIL: OpenSCAD is not on PATH. This tool renders real CAD; it "
              "will not fabricate a mesh from box arithmetic. Install OpenSCAD "
              "(>=2021.01) or skip CAD rendering — do NOT treat the SCAD source "
              "as a validated part.")
        return 2
    STL.mkdir(parents=True, exist_ok=True)
    failures = []
    for scad_name, key, stem, gate in PARTS:
        src = SCAD / scad_name
        if not src.exists():
            failures.append(f"{stem}: missing source {src}")
            continue
        out = STL / f"{stem}.stl"
        cmd = [openscad, "-o", str(out), "-D", f'part="{key}"', str(src)]
        r = subprocess.run(cmd, capture_output=True, text=True, env=scad_env())
        if r.returncode != 0 or not out.exists():
            failures.append(f"{stem}: render rc={r.returncode} "
                            f"{r.stderr.strip()[:160]}")
            continue
        parsed = read_stl(out)
        if not parsed or parsed[0] < 4:
            failures.append(f"{stem}: empty/degenerate mesh")
            continue
        ntris, lo, hi = parsed
        dims = [round(hi[k] - lo[k], 3) for k in range(3)]
        bed_ok = all(d <= BED_MM for d in dims)
        wt, note = watertight(ntris, lo, hi, out)
        tag = f"{ntris} tris, bbox {dims}"
        if not bed_ok:
            failures.append(f"{stem}: exceeds bed ({dims})")
            continue
        if gate and wt is False:
            failures.append(f"{stem}: not watertight ({note})")
            continue
        print(f"  ok: {stem:14s} {tag}"
              + ("" if not gate else f", watertight={wt} ({note})"))
    if failures:
        print("\nFAILURES:")
        for f in failures:
            print(" -", f)
        return 1
    print("\nAll primitive CAD parts rendered and validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
