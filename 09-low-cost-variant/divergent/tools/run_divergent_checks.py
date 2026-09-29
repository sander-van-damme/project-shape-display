#!/usr/bin/env python3
"""DND-75 runner: analytic screen + checks + CAD printability for the divergent
ultra-low-cost candidates.

Runs, in order:
  1. analysis/divergent_lowcost.py          (the machine screen -> JSON)
  2. analysis/divergent_lowcost_checks.py   (18 CI-style assertions)
  3. tools/validate/analytic_printability.py on the A1 cam cell
  4. tools/validate/analytic_printability.py on the A2/A3 media cell

A missing OpenSCAD is NOT fatal here: the printability checker is analytic
(CAD-declared constants vs sourced FDM limits), which is the evidence class
[DND-27] mandates. No print, no purchase, no measurement.

EVIDENCE CLASS: CALCULATION + CAD. Not a print, not a measurement.

USAGE
    python 09-low-cost-variant/divergent/tools/run_divergent_checks.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # 09-low-cost-variant/divergent/tools
DIVERGENT = HERE.parent                         # 09-low-cost-variant/divergent
ROOT = DIVERGENT.parent.parent                  # repo root
ANALYSIS = DIVERGENT / "analysis"
SCAD = DIVERGENT / "scad"
VALIDATE = ROOT / "tools" / "validate" / "analytic_printability.py"


def run(cmd: list[str]) -> int:
    print(f"\n$ {' '.join(str(c) for c in cmd)}")
    return subprocess.call([str(c) for c in cmd])


def main() -> int:
    rc = 0
    # 1. screen
    rc |= run([sys.executable, ANALYSIS / "divergent_lowcost.py"])
    # 2. checks
    rc |= run([sys.executable, ANALYSIS / "divergent_lowcost_checks.py"])
    # 3. CAD printability
    for scad in ("a1_cam_cell.scad", "a2a3_media_cell.scad"):
        rc |= run([sys.executable, VALIDATE, SCAD / scad])
    print(f"\nrunner exit code: {rc}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
