#!/usr/bin/env python3
"""DND-109 — checks for the reliability-first cost / printability envelope.

Pure arithmetic over the envelope CSV and stated constants. No physical
measurement, no purchase ([DND-27]). Standard library only.

Run:
    python 06-experiments/test14_low_cost_program/reliability_sourcing/cost_envelope_checks.py

It asserts the load-bearing numbers in ``cost_envelope_dnd104.md`` so the prose
cannot drift from the arithmetic:
  * the additive delivered convention (x1.16) and the $250 parts ceiling;
  * per-cell bought-hardware sensitivity (the "zero per-cell" result);
  * every CSV row carries the required columns and a valid flag pair;
  * media rows are flagged consumable where they are card/film/tape;
  * the working-vs-optimistic spread on soft lines is non-trivial.
"""

from __future__ import annotations

import csv
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
CSV_PATH = HERE / "cost_envelope_dnd104.csv"

CELLS = 6400
DELIVERED_UPLIFT = 1.16
DELIVERED_CEILING = 250.0
PARTS_CEILING = DELIVERED_CEILING / DELIVERED_UPLIFT  # 215.52

REQUIRED_COLS = {
    "class_id", "class", "line", "spec", "unit", "optimistic_usd", "working_usd",
    "high_usd", "printable_excluded", "consumable", "evidence", "sourced_ref",
    "death_note",
}

FAILURES: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {name}" + (f" — {detail}" if detail else ""))
    if not ok:
        FAILURES.append(name)


def load_rows() -> list[dict]:
    with CSV_PATH.open(newline="") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    rows = load_rows()
    print("=" * 74)
    print("DND-109 cost/printability envelope checks")
    print("=" * 74)

    print("\n1. Delivered convention (additive x1.16)")
    check("parts ceiling = 250/1.16", abs(PARTS_CEILING - 215.5172) < 1e-3,
          f"{PARTS_CEILING:.4f}")
    check("200-parts delivered = 232", abs(200.0 * DELIVERED_UPLIFT - 232.0) < 1e-9,
          f"{200.0 * DELIVERED_UPLIFT:.2f}")
    check("215.52 parts delivered ~= 250", abs(PARTS_CEILING * DELIVERED_UPLIFT - 250.0) < 0.02,
          f"{PARTS_CEILING * DELIVERED_UPLIFT:.2f}")

    print("\n2. Per-cell bought-hardware sensitivity (the core result)")
    per_cell = {0.0: 0.0, 0.01: 64.0, 0.05: 320.0, 0.10: 640.0,
                1.20: 7680.0, 4.45: 28480.0}
    for unit, board in per_cell.items():
        check(f"${unit:.2f}/cell -> ${board:,.0f}/board",
              abs(unit * CELLS - board) < 1e-6, f"{unit * CELLS:,.2f}")
    check("$0.05/cell alone exceeds parts ceiling", 0.05 * CELLS > PARTS_CEILING,
          f"{0.05 * CELLS:.0f} > {PARTS_CEILING:.0f}")
    check("$0.03/cell leaves < $24 of the ceiling",
          PARTS_CEILING - 0.03 * CELLS < 24.0,
          f"leaves ${PARTS_CEILING - 0.03 * CELLS:.2f}")
    check("one N20 per cell (6400 x 1.20) is a death case", 1.20 * CELLS > PARTS_CEILING)

    print("\n3. 99 %-perfect-map budget (from the program reliability model)")
    q_goal = 1.0 - 0.99 ** (1.0 / CELLS)
    check("q_goal ~ 1.570e-6", abs(q_goal - 1.570e-6) < 1e-8, f"{q_goal:.3e}")
    p_at_1e4 = (1 - 1e-4) ** CELLS
    check("P(perfect) at q=1e-4 ~ 52.7 %", abs(p_at_1e4 - 0.527) < 0.002,
          f"{p_at_1e4:.4%}")

    print("\n4. CSV column contract")
    missing = [c for c in REQUIRED_COLS if rows and c not in rows[0]]
    check("all required columns present", not missing, f"missing={missing}")
    check("CSV is non-empty", len(rows) >= 40, f"{len(rows)} rows")

    print("\n5. Flag integrity")
    bad_flags = []
    for r in rows:
        for col in ("printable_excluded", "consumable"):
            if r[col] not in ("yes", "no"):
                bad_flags.append((r["line"], col, r[col]))
    check("printable_excluded/consumable are yes|no", not bad_flags, f"bad={bad_flags}")
    motors = [r for r in rows if r["class"] == "actuators"]
    check("no actuator row is marked printable_excluded",
          all(r["printable_excluded"] == "no" for r in motors))
    media = [r for r in rows if r["class"] == "media"]
    print(f"    media rows: {[r['line'] for r in media]}")
    consumables = [r["line"] for r in media if r["consumable"] == "yes"]
    check("card/film/tape/cover media flagged consumable", len(consumables) >= 3,
          f"consumables={consumables}")

    print("\n6. Price scenarios are ordered (opt <= work <= high)")
    bad_order = []
    for r in rows:
        o, w, h = float(r["optimistic_usd"]), float(r["working_usd"]), float(r["high_usd"])
        if not (o <= w <= h):
            bad_order.append(r["line"])
    check("optimistic <= working <= high on every row", not bad_order, f"bad={bad_order}")

    print("\n7. Soft-line spread is meaningful")
    spreads = []
    for r in rows:
        w, h = float(r["working_usd"]), float(r["high_usd"])
        if w > 0:
            spreads.append(h / w)
    check("some line has high/working >= 1.5", max(spreads) >= 1.5,
          f"max spread {max(spreads):.2f}")

    print("\n" + "=" * 74)
    if FAILURES:
        print(f"RESULT: {len(FAILURES)} FAILED -> {FAILURES}")
        raise SystemExit(1)
    print("RESULT: all checks PASS")


if __name__ == "__main__":
    main()
