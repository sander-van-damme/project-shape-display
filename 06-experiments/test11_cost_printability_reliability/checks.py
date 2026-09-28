#!/usr/bin/env python3
"""Deterministic checks for the Test11 cost model and printability screens.

These assert the *arithmetic* properties other documents rely on. They do not
validate any physical claim. Run:
    python 06-experiments/test11_cost_printability_reliability/checks.py
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
CELLS = 6400
CONTINGENCY = 0.20


def load(key: str) -> list[dict[str, str]]:
    with (HERE / f"bom_{key}.csv").open(newline="") as fh:
        return list(csv.DictReader(fh))


def total(rows, col: str) -> float:
    return sum(int(r["quantity"]) * float(r[col]) for r in rows)


def check(name: str, condition: bool, detail: str = "") -> None:
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
    if not condition:
        raise SystemExit(1)


def main() -> None:
    s5 = load("S5")
    # Test08 reproduction anchor.
    check("S5 working base reproduces Test08 $432",
          math.isclose(total(s5, "unit_working_usd"), 432.0, abs_tol=0.01),
          f"{total(s5, 'unit_working_usd'):.2f}")
    check("S5 optimistic base reproduces Test08 $276",
          math.isclose(total(s5, "unit_optimistic_usd"), 276.0, abs_tol=0.01))
    check("S5 high base reproduces Test08 $783",
          math.isclose(total(s5, "unit_high_usd"), 783.0, abs_tol=0.01))

    # Every surviving candidate exists and is non-empty.
    for key in ("S1", "S2", "S3", "S4", "S5"):
        rows = load(key)
        check(f"{key} BOM loads with lines", len(rows) > 0, f"{len(rows)} lines")

    # S3 must be the expensive one (bought selectors dominate).
    s3 = total(load("S3"), "unit_working_usd")
    for key in ("S1", "S2", "S4", "S5"):
        check(f"S3 working total exceeds {key}",
              s3 > total(load(key), "unit_working_usd"),
              f"S3 ${s3:.0f}")

    # Per-cell arithmetic: $0.10/cell = $640.
    check("$0.10/cell adds exactly $640", math.isclose(0.10 * CELLS, 640.0))

    # Reliability anchors.
    check("q=1e-4 gives 52.7% perfect 6400-cell maps",
          math.isclose((1 - 1e-4) ** CELLS, 0.5273, abs_tol=5e-4),
          f"{(1 - 1e-4) ** CELLS:.4%}")
    q_goal = 1 - 0.99 ** (1 / CELLS)
    check("99% map goal needs q ~= 1.57e-6",
          math.isclose(q_goal, 1.57e-6, rel_tol=0.02),
          f"{q_goal:.3e}")
    n = math.ceil(math.log(0.05) / math.log(1 - q_goal))
    check("one-sided 95% bound needs ~1.91M zero-failure trials",
          n == 1907667, f"{n:,}")

    print("\nAll Test11 arithmetic checks passed.")


if __name__ == "__main__":
    main()
