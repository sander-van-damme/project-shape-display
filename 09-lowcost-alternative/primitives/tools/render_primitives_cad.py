#!/usr/bin/env python3
"""DND-76 — render the primitive CAD with a REAL OpenSCAD, or fail hard.

EVIDENCE CLASS: CAD (this script only renders; it does not simulate or
measure). Under DND-27 no print is produced.

Usage:
    python 09-lowcost-alternative/primitives/tools/render_primitives_cad.py

Writes watertight ASCII STLs to ../stl/. Exits non-zero if OpenSCAD is not on
PATH or if any part fails to render, so the absence of a real CAD kernel can
never be mistaken for a validated part.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCAD = HERE.parent / "scad"
STL = HERE.parent / "stl"

PARTS = {
    "s6lc_cell": SCAD / "s6lc_cell.scad",
    "mask_comb": SCAD / "mask_comb.scad",
    "reset_bar": SCAD / "reset_bar.scad",
}


def main() -> int:
    openscad = shutil.which("openscad") or shutil.which("openscad-nightly")
    if not openscad:
        print("FAIL: OpenSCAD is not on PATH. This tool renders real CAD; it "
              "will not fabricate a mesh from box arithmetic. Install OpenSCAD "
              "(>=2021.01) or skip CAD rendering — do NOT treat the SCAD source "
              "as a validated part.")
        return 2
    STL.mkdir(parents=True, exist_ok=True)
    failures = []
    for name, src in PARTS.items():
        if not src.exists():
            failures.append(f"{name}: missing source {src}")
            continue
        out = STL / f"{name}.stl"
        cmd = [openscad, "-o", str(out), str(src)]
        print(f"render: {name} ...")
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0 or not out.exists():
            failures.append(f"{name}: {r.stderr.strip()[:200]}")
            continue
        size = out.stat().st_size
        # ASCII STL sanity: must contain facets
        head = out.read_text(errors="ignore")[:200]
        if "facet" not in head and "solid" not in head:
            failures.append(f"{name}: STL looks empty")
            continue
        print(f"  ok: {out.name} ({size} bytes)")
    if failures:
        print("\nFAILURES:")
        for f in failures:
            print(" -", f)
        return 1
    print("\nAll primitive CAD parts rendered.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
