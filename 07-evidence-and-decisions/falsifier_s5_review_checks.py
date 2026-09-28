#!/usr/bin/env python3
"""Falsifier DND-36 checks: reproduce the four material findings against repo inputs.

Run from anywhere:  python 07-evidence-and-decisions/falsifier_s5_review_checks.py

Evidence class: CALCULATION / sourced-fact reading of repository files. No print,
no measurement (DND-27). These checks are deliberately *hostile* to the DND-35
promotion: they assert the discrepancies the review reports, so the review can be
verified rather than trusted.
"""
from __future__ import annotations

import csv
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
S5_BOM = (REPO / "06-experiments" / "test11_cost_printability_reliability"
          / "delivered_3scenario" / "bom_S5_delivered.csv")
SWEEP = (REPO / "06-experiments" / "test09_test08_validation"
         / "results" / "timing_sweep.csv")

MOTOR_USD, DRIVER_USD, N = 1.05, 0.80, 80
CEILING = 500.0


def fixed_expected_subtotal() -> float:
    with S5_BOM.open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    return sum(int(r["quantity"]) * float(r["unit_expected_usd"]) for r in rows
               if not r["item"].startswith(("PM motor", "Dual H-bridge")))


def main() -> int:
    fixed = fixed_expected_subtotal()
    parts = fixed + N * MOTOR_USD + N * DRIVER_USD
    additive = parts * 1.16          # repo basis (delivered_cost_model.py:86)
    mult = parts * (1.10 * 1.06)     # DND-35 model basis (model.py:73)

    print("Finding A — cost uplift basis")
    print(f"  fixed expected subtotal (from BOM)   = ${fixed:.2f}")
    print(f"  sourced-pair parts                   = ${parts:.2f}")
    print(f"  delivered additive x1.16 (repo)      = ${additive:.2f}  "
          f"{'OVER' if additive > CEILING else 'under'} ceiling")
    print(f"  delivered multiplicative x1.166      = ${mult:.2f}  (DND-35 model)")

    reduced = (fixed - 14.0 - 5.0) + N * MOTOR_USD + N * DRIVER_USD
    # realistic register saving: chips still bought at sourced $0.0925 each
    realistic = (fixed - 40 * 0.0925 - 5.0) + N * MOTOR_USD + N * DRIVER_USD
    print(f"  reduced parts (claimed -14 -5)       = ${reduced:.2f} -> "
          f"${reduced * 1.16:.2f} additive")
    print(f"  realistic register saving only -{40 * 0.0925:.2f} = "
          f"${realistic:.2f} -> ${realistic * 1.16:.2f} additive")

    # Finding B — timing sweep
    with SWEEP.open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    at400 = [r for r in rows if r["rate_hz"] == "400"]
    ok = [r for r in at400 if r["under_30"] == "True"]
    worst = max(float(r["time_s"]) for r in at400)
    print("\nFinding B — timing sweep at 400 pps")
    print(f"  under 30 s: {len(ok)}/{len(at400)}   worst = {worst:.2f} s")

    print("\nFinding C — J2 isolation gate verdict")
    j2 = (REPO / "06-experiments" / "test11_falsification_library" / "analytic"
          / "README.md")
    text = j2.read_text()
    print(f"  source README contains 'INCONCLUSIVE': {'INCONCLUSIVE' in text}")

    # Assertions: the review's findings are true as stated.
    assert abs(fixed - 284.0) < 1e-9
    assert additive > CEILING, "additive sourced-pair must be over ceiling"
    assert mult > additive, "multiplicative uplift must exceed additive"
    assert len(ok) < len(at400) / 4, "most 400pps sweep cases must fail 30 s"
    assert "INCONCLUSIVE" in text
    print("\nAll DND-36 review assertions hold.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
