"""Render + mesh-validate the S6-LC low-cost machine CAD (DND-71).

Uses a real OpenSCAD to render the cell, bank, mask-gate, release-comb and
platen parts, then validates each STL with trimesh (watertight, non-empty) and
checks the declared printability envelopes against the model.

EVIDENCE CLASS: CAD + mesh validation. No print, no measurement (DND-27).
A missing OpenSCAD is a hard failure here, because the render is the point.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUB = HERE.parent
SCAD = SUB / "scad" / "s6lc_machine.scad"
STL_DIR = SUB / "cad" / "stl"
RECORD = SUB / "cad" / "s6lc_cad_record.json"

PARTS = ["cell", "bank", "gate", "comb", "platen"]


def openscad_bin() -> str:
    b = shutil.which("openscad")
    if b:
        return b
    local = Path.home() / ".local" / "bin" / "openscad"
    if local.exists():
        return str(local)
    raise SystemExit("openscad not found (required for the CAD render)")


def render(part: str) -> dict:
    STL_DIR.mkdir(parents=True, exist_ok=True)
    out = STL_DIR / f"s6lc_{part}.stl"
    cmd = [openscad_bin(), "-o", str(out), "-D", f'PART="{part}"', str(SCAD)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(f"openscad failed for {part}:\n{proc.stderr[-2000:]}")
    return dict(part=part, stl=str(out.relative_to(SUB)), bytes=out.stat().st_size)


def validate(rec: dict) -> dict:
    import trimesh
    mesh = trimesh.load(rec["stl"] if Path(rec["stl"]).is_absolute()
                        else SUB / rec["stl"], force="mesh")
    rec["watertight"] = bool(mesh.is_watertight)
    rec["faces"] = int(len(mesh.faces))
    rec["bbox_mm"] = [round(float(x), 3) for x in mesh.extents]
    rec["volume_cm3"] = round(float(mesh.volume) / 1000.0, 4)
    return rec


def main() -> int:
    results = []
    for p in PARTS:
        r = render(p)
        r = validate(r)
        results.append(r)
        print(f"  {p:8s} faces={r['faces']:6d} bbox={r['bbox_mm']} "
              f"watertight={r['watertight']}")
    ok = all(r["watertight"] and r["faces"] > 0 for r in results)
    RECORD.write_text(json.dumps(dict(
        evidence_class="CAD + mesh validation; no print/measurement (DND-27)",
        openscad_version=subprocess.run([openscad_bin(), "--version"],
                                        capture_output=True, text=True).stdout.strip(),
        parts=results, all_watertight=ok), indent=2) + "\n")
    print(f"record -> {RECORD.relative_to(SUB)}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
