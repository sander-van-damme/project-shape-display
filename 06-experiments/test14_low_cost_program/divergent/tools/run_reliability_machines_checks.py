#!/usr/bin/env python3
"""DND-107 runner: analytic screen + checks + reliability-cell CAD printability.

Runs, in order:
  1. analysis/reliability_machines_beta.py        (the machine screen -> JSON)
  2. analysis/reliability_machines_beta_checks.py (28 CI-style assertions)
  3. tools/validate/analytic_printability.py on scad/b2b3_reliability_cell.scad

A missing OpenSCAD is NOT fatal: the printability checker is analytic
(CAD-declared constants vs sourced FDM limits), the evidence class [DND-27]
mandates. No print, no purchase, no measurement.

EVIDENCE CLASS: CALCULATION + CAD. Not a print, not a measurement.

USAGE
    python 06-experiments/test14_low_cost_program/divergent/tools/run_reliability_machines_checks.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # .../divergent/tools
DIVERGENT = HERE.parent                         # .../divergent
ROOT = DIVERGENT.parents[2]                     # repo root
ANALYSIS = DIVERGENT / "analysis"
SCAD = DIVERGENT / "scad"
VALIDATE = ROOT / "tools" / "validate" / "analytic_printability.py"


def run(cmd: list[str]) -> int:
    print(f"\n$ {' '.join(str(c) for c in cmd)}")
    return subprocess.call([str(c) for c in cmd])


def main() -> int:
    rc = 0
    rc |= run([sys.executable, ANALYSIS / "reliability_machines_beta.py"])
    rc |= run([sys.executable, ANALYSIS / "reliability_machines_beta_checks.py"])
    rc |= run([sys.executable, VALIDATE, SCAD / "b2b3_reliability_cell.scad"])
    print(f"\nrunner exit code: {rc}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
