#!/usr/bin/env python3
"""render fab parts; CAD/calculation source, no physical validation."""
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
FAB = HERE.parent
SCAD = FAB / "scad" / "s5r_parts.scad"
STL_DIR = FAB / "stl"
BED_MM = 256.0

sys.path.insert(0, str(HERE))
from part_set import PARTS  # noqa: E402


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


def watertight(path: Path) -> tuple[bool, str]:
    """Watertight/manifold check. trimesh if available, else edge-pair count."""
    try:
        import trimesh  # type: ignore
        m = trimesh.load(path, force="mesh")
        if not m.is_watertight:
            return False, "trimesh: not watertight"
        if m.is_winding_consistent is False:
            return False, "trimesh: winding inconsistent"
        return True, "trimesh: watertight"
    except ImportError:
        pass
    # stdlib fallback: every triangle edge must appear exactly twice.
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
                vs.append(tuple(round(verts[v * 3 + k] * 1e4) for k in range(3)))
    edges: dict = {}
    for i in range(0, len(vs) - 2, 3):
        tri = (vs[i], vs[i + 1], vs[i + 2])
        for a, b in ((0, 1), (1, 2), (2, 0)):
            e = tuple(sorted((tri[a], tri[b])))
            edges[e] = edges.get(e, 0) + 1
    bad = sum(1 for c in edges.values() if c != 2)
    return (bad == 0), f"stdlib: {bad} unpaired edges"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", metavar="PATH", help="write the render record here",
                    default=str(FAB / "manifests" / "render_record.json"))
    ap.add_argument("--only", help="render only this part key")
    args = ap.parse_args()

    osc = find_openscad()
    if not osc:
        print("ERROR: OpenSCAD not found. Install: "
              "your system package manager to install OpenSCAD", file=sys.stderr)
        return 2
    print(f"OpenSCAD: {osc}")
    STL_DIR.mkdir(parents=True, exist_ok=True)

    parts = [p for p in PARTS if not args.only or p.key == args.only]
    record = {"openscad": osc, "scad": str(SCAD), "evidence_class": "CAD",
              "parts": [], "verdict": "PASS"}
    for p in parts:
        stl = STL_DIR / f"{p.key}.stl"
        stl.unlink(missing_ok=True)
        # design calculation: the full 27x27 cartridge is a single ~10.5 min CGAL render on
        # this container, so the per-part budget is 30 min (was 15 min when the
        # cartridge was an 8x8 witness).
        proc = subprocess.run(
            [osc, "-o", str(stl), "-D", f'part="{p.scad_part}"', str(SCAD)],
            capture_output=True, text=True, timeout=1800, env=scad_env())
        log = (proc.stdout + proc.stderr).strip()
        if proc.returncode != 0 or not stl.exists() or stl.stat().st_size == 0:
            print(f"[FAIL] {p.key}: render failed: {log[-200:]}")
            record["parts"].append({"part": p.key, "ok": False, "log": log[-300:]})
            record["verdict"] = "FAIL"
            continue
        got = read_stl(stl)
        if got is None:
            print(f"[FAIL] {p.key}: unreadable/empty mesh")
            record["parts"].append({"part": p.key, "ok": False,
                                    "reason": "unreadable mesh"})
            record["verdict"] = "FAIL"
            continue
        n, lo, hi = got
        size = [round(hi[k] - lo[k], 2) for k in range(3)]
        fits = all(s <= BED_MM for s in size)
        nondeg = all(s > 0 for s in size)
        wt, wtmsg = watertight(stl)
        ok = fits and nondeg and wt
        if not ok:
            record["verdict"] = "FAIL"
        print(f"[{'PASS' if ok else 'FAIL'}] {p.key:<20} bbox={size} "
              f"tris={n} bed={fits} watertight={wt} ({wtmsg})")
        record["parts"].append({
            "part": p.key, "ok": bool(ok), "file": stl.name,
            "bytes": stl.stat().st_size, "tris": n, "bbox_mm": size,
            "fits_256_bed": bool(fits), "nondegenerate": bool(nondeg),
            "watertight": bool(wt), "mesh_check": wtmsg,
        })

    Path(args.json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json).write_text(json.dumps(record, indent=2) + "\n")
    print(f"\nRender verdict: {record['verdict']}  (record: {args.json})")
    print("CAD evidence only: not a print, not a measurement.")
    return 0 if record["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
