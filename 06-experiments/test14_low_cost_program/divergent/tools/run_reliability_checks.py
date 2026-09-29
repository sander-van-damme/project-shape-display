#!/usr/bin/env python3
"""DND-106 runner: analytic screen + checks + printability for the
reliability-first cell/mechanism primitives.

Runs, in order:
  1. analysis-equivalent `reliability_primitives_alpha.py`     (screen -> JSON)
  2. `reliability_primitives_alpha_checks.py`                  (30 assertions)
  3. tools/validate/analytic_printability.py on reliability_cell.scad

A missing OpenSCAD is NOT fatal here: the printability checker is analytic
(CAD-declared constants vs sourced FDM limits), which is the evidence class
[DND-27] mandates. No print, no purchase, no measurement.

EVIDENCE CLASS: CALCULATION + CAD. Not a print, not a measurement.

USAGE
    python 06-experiments/test14_low_cost_program/divergent/tools/run_reliability_checks.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # 06-experiments/test14_low_cost_program/divergent/tools
DIVERGENT = HERE.parent                         # .../test14_low_cost_program/divergent
ROOT = DIVERGENT.parents[2]                     # repo root
SCAD = DIVERGENT / "scad"
VALIDATE = ROOT / "tools" / "validate" / "analytic_printability.py"


def run(cmd: list[str]) -> int:
    print(f"\n$ {' '.join(str(c) for c in cmd)}")
    return subprocess.call([str(c) for c in cmd])


def main() -> int:
    rc = 0
    # 1. screen
    rc |= run([sys.executable, DIVERGENT / "reliability_primitives_alpha.py"])
    # 2. checks
    rc |= run([sys.executable,
               DIVERGENT / "reliability_primitives_alpha_checks.py"])
    # 3. CAD printability
    rc |= run([sys.executable, VALIDATE, SCAD / "reliability_cell.scad"])
    print(f"\nrunner exit code: {rc}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
