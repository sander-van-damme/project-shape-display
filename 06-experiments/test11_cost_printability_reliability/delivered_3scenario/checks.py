#!/usr/bin/env python3
"""Deterministic checks for the DND-11 three-scenario delivered BOM.

Asserts the arithmetic properties the README conclusions rely on. It does not
validate any physical or supplier claim. Run:
    python 06-experiments/test11_cost_printability_reliability/delivered_3scenario/checks.py
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
CEILING = 500.0
CELLS = 6400
SCENARIOS = ("best", "expected", "worst")
UPLIFT = {
    "best": ("ship", 0.05, "tax", 0.00),
    "expected": ("ship", 0.10, "tax", 0.06),
    "worst": ("ship", 0.18, "tax", 0.11),
}


def load(key: str) -> list[dict[str, str]]:
    with (HERE / f"bom_{key}_delivered.csv").open(newline="") as fh:
        return list(csv.DictReader(fh))


def parts(rows, scenario: str) -> float:
    return sum(int(r["quantity"]) * float(r[f"unit_{scenario}_usd"]) for r in rows)


def delivered(rows, scenario: str) -> float:
    sub = parts(rows, scenario)
    return sub * (1 + (0.05 if scenario == "best" else 0.10 if scenario == "expected" else 0.18)
                  + (0.00 if scenario == "best" else 0.06 if scenario == "expected" else 0.11))


def check(name: str, condition: bool, detail: str = "") -> None:
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
    if not condition:
        raise SystemExit(1)


def main() -> None:
    keys = ("S1", "S2", "S3", "S4", "S5")
    boms = {k: load(k) for k in keys}

    # Every candidate loads and is non-empty.
    for k in keys:
        check(f"{k} delivered BOM loads", len(boms[k]) > 0, f"{len(boms[k])} lines")

    # Scenario monotonicity: best <= expected <= worst on parts and delivered.
    for k in keys:
        p = [parts(boms[k], s) for s in SCENARIOS]
        d = [delivered(boms[k], s) for s in SCENARIOS]
        check(f"{k} parts best<=expected<=worst", p[0] <= p[1] <= p[2], f"{p}")
        check(f"{k} delivered best<=expected<=worst", d[0] <= d[1] <= d[2], f"{[round(x,2) for x in d]}")

    # The decisive conclusion: every survivor is OVER the $500 ceiling in the
    # expected scenario (delivered). If this ever becomes false the README must
    # change.
    for k in keys:
        d_exp = delivered(boms[k], "expected")
        check(f"{k} expected delivered > $500", d_exp > CEILING, f"${d_exp:.2f}")

    # S3 is decisively over: its expected delivered is > 2x the ceiling.
    check("S3 expected delivered > 2x ceiling",
          delivered(boms["S3"], "expected") > 2 * CEILING,
          f"${delivered(boms['S3'], 'expected'):.2f}")

    # S5 expected delivered headline value used in the README/issue.
    s5 = delivered(boms["S5"], "expected")
    check("S5 expected delivered ~= $592.06", math.isclose(s5, 592.06, abs_tol=0.05), f"${s5:.2f}")

    # Per-cell arithmetic anchors.
    check("$0.10/cell adds exactly $640", math.isclose(0.10 * CELLS, 640.0))
    check("$0.05/cell leaves $180 below ceiling",
          math.isclose(CEILING - 0.05 * CELLS, 180.0))

    # S5 critical-part cross-over counts: how many (motor,driver) pairs stay
    # below $500 delivered; only certain combinations.
    rows = boms["S5"]
    fixed = sum(
        int(r["quantity"]) * float(r["unit_expected_usd"])
        for r in rows
        if not r["item"].startswith(("PM motor", "Dual H-bridge"))
    )
    # expected uplift is ship 10% + tax 6% -> 1.16
    up = 1.16
    cheap = (fixed + 80 * 1.05 + 80 * 0.7955) * up
    costly = (fixed + 80 * 40.00 + 80 * 1.3338) * up
    # Even the most favourable sourced motor + cheapest sourced matched driver
    # lands essentially *on* the ceiling: there is no comfort margin anywhere.
    check("S5 cheapest sourced motor+driver hugs ceiling (within $5)",
          abs(cheap - CEILING) <= 5.0, f"${cheap:.2f}")
    check("S5 traceable motor blows ceiling", costly > 8 * CEILING, f"${costly:.2f}")

    print("\nAll DND-11 delivered-BOM arithmetic checks passed.")


if __name__ == "__main__":
    main()
