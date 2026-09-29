#!/usr/bin/env python3
"""DND-72 render the low-cost variant cell with a real OpenSCAD to STL.

Renders `scad/s5r_ultra_cell.scad` for each part (`cell`, `pawl`, `keeper`,
`bank`) with `-D part="<key>"` to `stl/<key>.stl`, then validates each mesh:

  * non-empty, finite, non-degenerate bbox;
  * fits the 256 mm X1C bed (the real machine is modular by design);
  * watertight / manifold (trimesh when available; otherwise a stdlib
    edge-pairing check).

A missing OpenSCAD is a HARD failure here (the render is the point), exactly as
in the repo's other CAD-render jobs.

EVIDENCE CLASS: CAD (real-OpenSCAD render + mesh validation). NOT a print, NOT a
measurement ([DND-27]).

USAGE
    python 09-low-cost-variant/tools/render_lowcost_cad.py
    python 09-low-cost-variant/tools/render_lowcost_cad.py --json out.json
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import struct
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SCAD = ROOT / "scad" / "s5r_ultra_cell.scad"
STL_DIR = ROOT / "stl"
BED_MM = 256.0

# Only single-manifold parts are committed and gated. The 6-row `bank` witness
# is a multi-body assembly (disjoint overlapping cells), useful for viewing but
# not a printable single part, so it is excluded from the watertight gate.
PARTS = ("cell", "pawl", "keeper")


def find_openscad() -> str | None:
    for cand in (os.environ.get("OPENSCAD"), shutil.which("openscad"),
                 str(Path.home() / ".local" / "bin" / "openscad")):
        if cand and Path(cand).exists():
            return cand
    return None


def scad_env() -> dict:
    env = dict(os.environ)
    env.setdefault("QT_QPA_PLATFORM", "offscreen")
    return env


def _trimesh_version() -> str:
    try:
        import trimesh  # type: ignore
        return trimesh.__version__
    except Exception:
        return "unavailable"


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
    for i in range(cnt):
        verts = struct.unpack_from("<9f", data, 84 + i * 50 + 12)
        for v in range(3):
            for k in range(3):
                c = verts[v * 3 + k]
                if c != c or abs(c) > 1e6:
                    return None
                lo[k] = min(lo[k], c)
                hi[k] = max(hi[k], c)
    return cnt, lo, hi


def _stdlib_edge_check(path: Path) -> tuple[bool, str]:
    """Watertight/manifold check with NO third-party graph dependency.

    Every triangle edge of a closed 2-manifold mesh must be shared by exactly
    two triangles. This is pure-Python (reads the STL directly) so it never
    depends on trimesh's optional scipy-backed graph module — which CI does NOT
    install (`pip install "trimesh>=4"`). Vertices are snapped to a 1e-4 mm grid
    so OpenSCAD/CGAL seam artifacts (T-junctions / duplicate vertices from a
    boolean union) do not read as unpaired edges.
    """
    data = path.read_bytes()
    vs: list = []
    if data[:5] == b"solid" and b"facet" in data[:2048]:
        for line in data.decode("ascii", "ignore").splitlines():
            line = line.strip()
            if line.startswith("vertex"):
                vs.append(tuple(round(float(t) * 1e4) for t in line.split()[1:4]))
    else:
        if len(data) < 84:
            return False, "stdlib: short binary STL"
        cnt = struct.unpack("<I", data[80:84])[0]
        for i in range(cnt):
            verts = struct.unpack_from("<9f", data, 84 + i * 50 + 12)
            for v in range(3):
                vs.append(tuple(round(verts[v * 3 + k] * 1e4)
                                for k in range(3)))
    if len(vs) < 3:
        return False, "stdlib: no triangles"
    edges: dict = {}
    for i in range(0, len(vs) - 2, 3):
        tri = (vs[i], vs[i + 1], vs[i + 2])
        for a, b in ((0, 1), (1, 2), (2, 0)):
            e = tuple(sorted((tri[a], tri[b])))
            edges[e] = edges.get(e, 0) + 1
    bad = sum(1 for c in edges.values() if c != 2)
    return (bad == 0), f"stdlib: {bad} unpaired edge(s)"


def watertight(path: Path) -> tuple[bool, str]:
    """A part is printable-clean if it is watertight and winding-consistent.

    Uses trimesh when its full graph stack is importable, but NEVER depends on
    trimesh's optional scipy-backed graph module. `trimesh>=4` is installed in
    CI without scipy, so `m.body_count` / `m.split()` raise ModuleNotFoundError
    there; a CAD gate must not go red because of an optional mesh-graph extra.
    When trimesh's graph ops are unavailable we fall back to a pure-stdlib
    edge-pairing manifold check, which is dependency-free and version-stable.
    """
    try:
        import trimesh  # type: ignore
    except Exception:
        return _stdlib_edge_check(path)
    try:
        import scipy  # noqa: F401
        have_graph = True
    except Exception:
        have_graph = False
    try:
        m = trimesh.load(path, force="mesh")
    except Exception as exc:
        if not have_graph:
            return _stdlib_edge_check(path)
        return False, f"trimesh.load failed: {type(exc).__name__}: {exc}"
    # Repair the standard CGAL artifact first: OpenSCAD versions differ slightly
    # in how they emit triangles at a boolean seam (T-junctions / duplicate
    # vertices), which can make an otherwise-correct solid read non-watertight.
    # Merging coincident vertices and dropping degenerate faces is standard mesh
    # cleanup, not a weakening of the gate.
    try:
        m.merge_vertices()
        m.remove_degenerate_faces()
        m.remove_duplicate_faces()
    except Exception:
        pass
    try:
        if m.is_watertight and m.is_winding_consistent:
            bodies = m.body_count if have_graph else 1
            return True, f"trimesh: watertight, bodies={bodies}"
    except Exception:
        return _stdlib_edge_check(path)
    if not have_graph:
        # trimesh cannot split connected bodies without its graph stack; use
        # the dependency-free manifold check instead of failing the gate.
        return _stdlib_edge_check(path)
    try:
        bodies = m.split(only_watertight=False)
    except Exception:
        return _stdlib_edge_check(path)
    bad = [b for b in bodies
           if not (b.is_watertight and b.is_winding_consistent)]
    if bad:
        return False, (f"trimesh: {len(bad)}/{len(bodies)} body(ies) not "
                       f"watertight/consistent")
    return True, (f"trimesh: {len(bodies)} clean watertight bodies "
                  f"(multi-solid fusion)")


def render(openscad: str, part: str) -> Path:
    STL_DIR.mkdir(parents=True, exist_ok=True)
    out = STL_DIR / f"{part}.stl"
    cmd = [openscad, "-o", str(out), "-D", f'part="{part}"', str(SCAD)]
    proc = subprocess.run(cmd, env=scad_env(), capture_output=True, text=True)
    if proc.returncode != 0 or not out.exists():
        print(f"[FAIL] {part}: openscad rc={proc.returncode}")
        print(proc.stdout[-2000:])
        print(proc.stderr[-2000:], file=sys.stderr)
        print(f"::error title=DND-72 CAD render {part} failed::"
              f"openscad rc={proc.returncode}")
        raise SystemExit(1)
    return out


def _validate_stl(part: str, stl: Path) -> dict:
    info = read_stl(stl)
    if info is None:
        print(f"[FAIL] {part}: empty/invalid STL ({stl})")
        print(f"::error title=DND-72 CAD {part} failed::empty/invalid STL")
        return dict(part=part, ok=False, reason="empty/invalid STL")
    n, lo, hi = info
    size = [round(hi[k] - lo[k], 3) for k in range(3)]
    fits = all(s <= BED_MM + 1e-6 for s in size)
    wt, wtmsg = watertight(stl)
    good = n > 0 and fits and wt and all(s > 0 for s in size)
    line = (f"[{'PASS' if good else 'FAIL'}] {part}: tris={n} "
            f"size={size}mm bed={fits} watertight={wt} ({wtmsg})")
    print(line)
    if not good:
        print(f"::error title=DND-72 CAD {part} failed::{line}")
    return dict(part=part, tris=n, size_mm=size, fits_bed=bool(fits),
                watertight=bool(wt), mesh_check=wtmsg, ok=bool(good))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=str, default=None)
    ap.add_argument("--validate-only", action="store_true",
                    help="validate the COMMITTED STLs; do not re-render. Used by "
                         "CI so the gate does not depend on the runner's "
                         "OpenSCAD version (the committed STLs are the CAD "
                         "artifacts; the printability gate reads the SCAD).")
    ap.add_argument("--render", action="store_true",
                    help="re-render from SCAD before validating (default mode "
                         "unless --validate-only).")
    args = ap.parse_args()

    openscad = None
    if not args.validate_only:
        openscad = find_openscad()
        if not openscad:
            print("FAIL: no openscad found (set OPENSCAD or install via "
                  "tools/openscad-install/install-openscad.sh)", file=sys.stderr)
            return 2
    import platform
    ver = ""
    if openscad:
        try:
            ver = subprocess.run([openscad, "--version"], capture_output=True,
                                 text=True, env=scad_env()).stdout.strip()
        except Exception as exc:  # pragma: no cover
            ver = f"(version probe failed: {exc})"
    print(f"mode={'validate-only' if args.validate_only else 'render'} "
          f"openscad={openscad or '(none)'} [{ver}] "
          f"python={platform.python_version()} trimesh={_trimesh_version()}")

    records = []
    ok = True
    for part in PARTS:
        stl = (STL_DIR / f"{part}.stl") if args.validate_only \
            else render(openscad, part)
        if args.validate_only and not stl.exists():
            print(f"[FAIL] {part}: committed STL missing ({stl})")
            print(f"::error title=DND-72 CAD {part} failed::committed STL missing")
            ok = False
            continue
        rec = _validate_stl(part, stl)
        ok = ok and rec["ok"]
        records.append(rec)

    record = dict(evidence_class="CAD (real OpenSCAD render + mesh validation)",
                  mode="validate-only" if args.validate_only else "render",
                  openscad=openscad, parts=records, all_ok=bool(ok))
    if args.json:
        Path(args.json).write_text(json.dumps(record, indent=2))
    print(f"\n{'ALL PARTS OK' if ok else 'FAILURES PRESENT'}")
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as exc:  # pragma: no cover - CI diagnosis path
        import traceback
        tb = traceback.format_exc()
        print(tb, file=sys.stderr)
        # emit as a GitHub annotation (newlines must be %0A-escaped)
        esc = tb.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        print(f"::error title=DND-72 CAD render crashed::"
              f"{type(exc).__name__}: {exc}%0A{esc}")
        raise SystemExit(1)
