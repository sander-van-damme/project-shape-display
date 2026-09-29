"""DND-104 A1 — render + mesh-validate the binary-latch cell parts (real OpenSCAD).

Fails hard if OpenSCAD is missing, so a skipped render can never be mistaken
for validated CAD (same convention as the S6-LC / primitives render tools).

Writes watertight STLs to 10-reliability-mask/cad/stl/ and a JSON record.

Run:
  export PATH="$HOME/.local/bin:$PATH"
  python 10-reliability-mask/analysis/render_a1_cad.py
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import trimesh

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SCAD = ROOT / "scad" / "a1_binary_latch_cell.scad"
SCAD_READER = ROOT / "scad" / "a1_reader_head.scad"
OUT = ROOT / "cad" / "stl"
RECORD = ROOT / "cad" / "render_record.json"

PARTS = ["column", "latch", "cradle"]

# Provisional FDM rules (DND-102 criteria): 1 line @ 0.4 mm nozzle, 2-line wall.
MIN_FEATURE_MM = 0.44
MIN_WALL_MM = 0.88
X1C_BED_MM = 256.0


def require_openscad() -> str:
    exe = shutil.which("openscad")
    if not exe:
        raise SystemExit(
            "FATAL: openscad not found on PATH. Install it with "
            "tools/openscad-install/install-openscad.sh and re-run. A skipped "
            "render must NOT be treated as validated CAD."
        )
    return exe


def render(exe: str) -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    record: dict = {"scad": str(SCAD.relative_to(ROOT.parent)), "parts": {}}
    for p in PARTS:
        stl = OUT / f"{p}.stl"
        cmd = [exe, "-o", str(stl), "-D", f'part="{p}"', str(SCAD)]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            raise SystemExit(f"OpenSCAD failed for {p}:\n{proc.stderr}")
        mesh = trimesh.load(stl)
        bbox = mesh.bounds[1] - mesh.bounds[0]
        watertight = bool(mesh.is_watertight)
        fits_bed = bool(max(bbox) <= X1C_BED_MM)
        record["parts"][p] = {
            "stl": str(stl.relative_to(ROOT.parent)),
            "triangles": int(len(mesh.faces)),
            "watertight": watertight,
            "bbox_mm": [round(float(x), 3) for x in bbox],
            "fits_x1c_bed": fits_bed,
            "echo": [ln for ln in proc.stderr.splitlines() if "ECHO" in ln],
        }
        if not watertight:
            raise SystemExit(f"FATAL: {p} is not watertight")
        if not fits_bed:
            raise SystemExit(f"FATAL: {p} exceeds the X1C bed")
    return record


def main() -> int:
    exe = require_openscad()
    record = render(exe)
    # DND-111: render + mesh-validate the shared reader-head / optical geometry.
    # Its echoes are the single-cell read-resolution self-checks (spot fits the
    # top face centre; corner reach and registration tolerance).
    reader_stl = OUT / "reader_head.stl"
    cmd = [exe, "-o", str(reader_stl), str(SCAD_READER)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(f"OpenSCAD failed for reader head:\n{proc.stderr}")
    rmesh = trimesh.load(reader_stl)
    rbbox = rmesh.bounds[1] - rmesh.bounds[0]
    record["reader_head"] = {
        "scad": str(SCAD_READER.relative_to(ROOT.parent)),
        "stl": str(reader_stl.relative_to(ROOT.parent)),
        "triangles": int(len(rmesh.faces)),
        "watertight": bool(rmesh.is_watertight),
        "bbox_mm": [round(float(x), 3) for x in rbbox],
        "echo": [ln for ln in proc.stderr.splitlines() if "ECHO" in ln],
    }
    if not rmesh.is_watertight:
        raise SystemExit("FATAL: reader head mesh is not watertight")
    # Assert the single-cell geometry fits (the decisive DND-111 check).
    echoes = " ".join(record["reader_head"]["echo"])
    if "spot fits top face at centre: true" not in echoes:
        raise SystemExit(
            "FATAL: reader spot does not fit the column top face at centre")
    record["evidence_class"] = (
        "CAD geometry rendered by real OpenSCAD + mesh validation (trimesh). "
        "NOT a print, NOT a measurement (DND-27)."
    )
    record["provisional_rules"] = {
        "min_feature_mm": MIN_FEATURE_MM,
        "min_wall_mm": MIN_WALL_MM,
        "x1c_bed_mm": X1C_BED_MM,
    }
    RECORD.write_text(json.dumps(record, indent=2) + "\n")
    for p, d in record["parts"].items():
        print(f"{p:8s} {d['triangles']:6d} tris  watertight={d['watertight']}  "
              f"bbox={d['bbox_mm']}  bed={d['fits_x1c_bed']}")
    rh = record["reader_head"]
    print(f"reader   {rh['triangles']:6d} tris  watertight={rh['watertight']}  "
          f"bbox={rh['bbox_mm']}")
    print(f"\nrecord -> {RECORD.relative_to(ROOT.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
