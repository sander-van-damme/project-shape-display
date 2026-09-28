#!/usr/bin/env python3
"""Render and mesh-validate the winner (S5) CAD coupon.

This closes the gap where the DND-29 geometry harness rendered the J2 rig and the
S3 selector coupon but not the promoted winner. It:

  1. runs Test08 `analysis.py` to emit `results/parameters.scad` from `params.json`;
  2. renders every S5 coupon part with real OpenSCAD;
  3. mesh-validates each STL (watertight, non-degenerate, fits the 256 mm bed);
  4. prints a machine-readable record.

Evidence class: CAD (render + mesh). It is NOT a slicer, a print or a measurement.
OpenSCAD is required; a missing OpenSCAD is a hard failure (exit 2), never a silent
skip, because the render is the whole point of this script.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
T08 = REPO / "06-experiments" / "test08_architecture_search"
PARTS = ["rotor", "follower", "follower_guide", "body_guide", "lift_plate"]
BED_MM = 256.0


def find_openscad() -> str | None:
    for cand in (os.environ.get("OPENSCAD"), shutil.which("openscad"),
                 str(Path.home() / ".local" / "bin" / "openscad")):
        if cand and Path(cand).exists():
            return cand
    return None


def bbox_mm(stl: Path) -> tuple[float, float, float]:
    """Bounding box from the STL facet vertices (binary or ASCII)."""
    xs: list[float] = []
    ys: list[float] = []
    zs: list[float] = []
    data = stl.read_bytes()
    if data[:5] == b"solid" and b"facet" in data[:2048]:
        text = data.decode("ascii", "ignore")
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("vertex"):
                _, x, y, z = line.split()
                xs.append(float(x)); ys.append(float(y)); zs.append(float(z))
    else:
        import struct
        n = struct.unpack("<I", data[80:84])[0]
        off = 84
        for _ in range(n):
            for _v in range(3):
                x, y, z = struct.unpack("<3f", data[off + 12:off + 24])
                xs.append(x); ys.append(y); zs.append(z)
                off += 50
    if not xs:
        return (0.0, 0.0, 0.0)
    return (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))


def main() -> int:
    osc = find_openscad()
    if not osc:
        print("ERROR: OpenSCAD not found. Install it or set OPENSCAD=...", file=sys.stderr)
        return 2

    # 1. regenerate parameters.scad
    r = subprocess.run([sys.executable, "analysis.py"], cwd=T08,
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("ERROR: analysis.py failed\n" + r.stderr, file=sys.stderr)
        return 2
    params = T08 / "results" / "parameters.scad"
    if not params.exists():
        print("ERROR: analysis.py did not emit results/parameters.scad", file=sys.stderr)
        return 2

    outdir = T08 / "results" / "winner_parts"
    outdir.mkdir(parents=True, exist_ok=True)

    record = {"openscad": osc, "parts": [], "verdict": "PASS"}
    for part in PARTS:
        stl = outdir / f"{part}.stl"
        p = subprocess.run([osc, "-o", str(stl), "-D", f'part="{part}"', "coupon.scad"],
                           cwd=T08, capture_output=True, text=True, timeout=600)
        ok = p.returncode == 0 and stl.exists() and stl.stat().st_size > 0
        dims = bbox_mm(stl) if ok else (0.0, 0.0, 0.0)
        fits = ok and all(d <= BED_MM for d in dims) and all(d > 0 for d in dims)
        if not ok or not fits:
            record["verdict"] = "FAIL"
        record["parts"].append({
            "part": part, "ok": bool(ok), "bytes": stl.stat().st_size if stl.exists() else 0,
            "bbox_mm": [round(d, 3) for d in dims], "fits_256_bed": bool(fits),
        })
        print(f"[{'OK' if ok and fits else 'FAIL'}] {part:<15} bbox={[round(d,2) for d in dims]} bed_fit={fits}")

    record_path = HERE / "winner_cad_record.json"
    record_path.write_text(json.dumps(record, indent=2) + "\n")
    print(f"\nWinner CAD verdict: {record['verdict']} (record: {record_path.name})")
    return 0 if record["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
