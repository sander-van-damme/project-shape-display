#!/usr/bin/env python3
"""Purchased-BOM cost model for shape-display architecture survivors S1-S5.

This script reads the per-candidate BOM CSVs in this folder and produces:
  - optimistic / working / high purchased totals, each with and without 20% contingency;
  - the distance to the $200 ideal / $400 acceptable / $500 ceiling bands;
  - per-cell bought-hardware sensitivity (what a $0.10 or $1.00 per-cell part adds);
  - a pass/fail verdict on whether a credible <$500 purchased path exists.

Evidence level: this is a *cost model driven by sourced and assumed line items*.
It is not a supplier quotation. Every line carries a basis string in the CSV that
says whether it is sourced, a working allowance, or speculative. Printed parts are
excluded from the purchased total by design (02-design-criteria), but print time,
tolerance, wear and assembly workload are treated separately in the write-up.

Standard library only. Run:
    python 06-experiments/test11_cost_printability_reliability/cost_model.py
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent

CELLS = 6400
CONTINGENCY = 0.20

# 02-design-criteria component-cost bands (purchased only).
BAND_IDEAL = 200.0
BAND_ACCEPTABLE = 400.0
BAND_CEILING = 500.0

SCENARIOS = ("optimistic", "working", "high")


@dataclass
class Line:
    item: str
    quantity: int
    unit: dict[str, float]
    category: str
    basis: str


@dataclass
class Candidate:
    key: str
    lines: list[Line]

    def total(self, scenario: str) -> float:
        return sum(l.quantity * l.unit[scenario] for l in self.lines)

    def total_with_contingency(self, scenario: str) -> float:
        return self.total(scenario) * (1.0 + CONTINGENCY)


def load(path: Path) -> Candidate:
    lines: list[Line] = []
    with path.open(newline="") as fh:
        for row in csv.DictReader(fh):
            lines.append(
                Line(
                    item=row["item"],
                    quantity=int(row["quantity"]),
                    unit={
                        "optimistic": float(row["unit_optimistic_usd"]),
                        "working": float(row["unit_working_usd"]),
                        "high": float(row["unit_high_usd"]),
                    },
                    category=row["category"],
                    basis=row["basis"],
                )
            )
    return Candidate(path.stem.replace("bom_", ""), lines)


def per_cell_sensitivity(unit_costs=(0.05, 0.10, 0.25, 0.50, 1.00)) -> list[tuple[float, float, float]]:
    """Return (unit_cost, added_total, implied_ceiling_room) for a bought per-cell part.

    'Ceiling room' is how much non-cell hardware could remain below $500 once the
    per-cell part is bought for all 6400 cells.
    """
    out = []
    for c in unit_costs:
        added = c * CELLS
        out.append((c, added, BAND_CEILING - added))
    return out


def verdict(working_with_contingency: float) -> str:
    if working_with_contingency < BAND_IDEAL:
        return "ideal band (<$200 with contingency)"
    if working_with_contingency < BAND_ACCEPTABLE:
        return "acceptable band (<$400 with contingency)"
    if working_with_contingency < BAND_CEILING:
        return "last-resort band (<$500 with contingency)"
    return "no credible <$500 path at working allowances"


def category_totals(cand: Candidate, scenario: str) -> dict[str, float]:
    totals: dict[str, float] = {}
    for line in cand.lines:
        totals[line.category] = totals.get(line.category, 0.0) + line.quantity * line.unit[scenario]
    return dict(sorted(totals.items(), key=lambda kv: -kv[1]))


def main() -> None:
    candidates = [load(HERE / f"bom_{k}.csv") for k in ("S1", "S2", "S3", "S4", "S5")]

    print("=" * 78)
    print("PURCHASED-BOM COST MODEL - S1..S5 (no printed-part cost; 20% contingency)")
    print("=" * 78)
    print(f"{'Candidate':<10}{'optimistic':>13}{'working':>13}{'high':>13}")
    print("-" * 78)
    summary: dict[str, dict[str, float]] = {}
    for cand in candidates:
        row = {s: cand.total(s) for s in SCENARIOS}
        summary[cand.key] = row
        print(
            f"{cand.key:<10}"
            f"{row['optimistic']:>12.2f} "
            f"{row['working']:>12.2f} "
            f"{row['high']:>12.2f}"
        )
    print()
    print("With 20% contingency:")
    print(f"{'Candidate':<10}{'optimistic':>13}{'working':>13}{'high':>13}  verdict (working)")
    print("-" * 78)
    for cand in candidates:
        row = summary[cand.key]
        vals = {s: row[s] * (1 + CONTINGENCY) for s in SCENARIOS}
        print(
            f"{cand.key:<10}"
            f"{vals['optimistic']:>12.2f} "
            f"{vals['working']:>12.2f} "
            f"{vals['high']:>12.2f}  {verdict(vals['working'])}"
        )

    print()
    print("Working-scenario category breakdown (largest first):")
    for cand in candidates:
        print(f"\n  {cand.key}:")
        for cat, total in category_totals(cand, "working").items():
            print(f"    {cat:<16} ${total:>8.2f}")

    print()
    print("Print-intent floor (what the purchased total becomes if the parts the design")
    print("intends to PRINT really are printed, i.e. drop fallback bought allowances):")
    fallback_categories = {"module_coupler", "media", "module_decoder", "programmer"}
    for cand in candidates:
        floor = {
            s: sum(
                l.quantity * l.unit[s]
                for l in cand.lines
                if l.category not in fallback_categories
            )
            for s in SCENARIOS
        }
        fallback = {s: cand.total(s) - floor[s] for s in SCENARIOS}
        print(
            f"  {cand.key}: floor working ${floor['working']:7.2f} "
            f"(bought fallback dropped ${fallback['working']:6.2f}); "
            f"floor +20% ${floor['working'] * (1 + CONTINGENCY):7.2f}"
        )
    print(
        "\n  Note: this floor is NOT a qualification. It assumes every fallback part\n"
        "  is successfully printed and reliable. That is exactly the printability and\n"
        "  reliability question this test must still answer."
    )

    print()
    print("Per-cell bought-hardware sensitivity (any bought part required on all 6400 cells):")
    print(f"  {'$/cell':>8}{'added total':>14}{'room left below $500':>24}")
    for unit, added, room in per_cell_sensitivity():
        flag = "  <- only micro-fasteners fit" if room <= 0 else ""
        print(f"  {unit:>8.2f}{added:>13.0f} ${room:>21.2f}{flag}")
    print(
        "\n  Key result: because the full board is 6,400 cells, even $0.10 of bought\n"
        "  hardware per cell adds $640. Any survivor with a per-cell bought part is\n"
        "  already over the $500 ceiling before motors, power or structure."
    )

    print()
    print("Cost-band check at working allowances with contingency:")
    for cand in candidates:
        w = summary[cand.key]["working"] * (1 + CONTINGENCY)
        print(f"  {cand.key}: ${w:7.2f}  ->  {verdict(w)}")

    print()
    print("S5 critical-item sourcing sensitivity (80 motors + 80 drivers):")
    motor_cases = {
        "test08_target_1.25": 1.25,
        "amazon_multipack_1.00": 1.00,
        "amazon_multipack_0.70": 0.70,
        "aliexpress_low_2.66": 2.66,
        "moons_retail_40.00": 40.00,
    }
    driver_cases = {
        "test08_allowance_0.60": 0.60,
        "drv8833pwpr_lcsc_100_1.33": 1.3338,
        "drv8833pwr_lcsc_1_2.39": 2.3873,
        "drv8833_board_amazon_0.66": 0.66,
    }
    # Non-motor, non-driver working lines in S5 (everything except the two lines).
    s5 = next(c for c in candidates if c.key == "S5")
    fixed = sum(
        l.quantity * l.unit["working"]
        for l in s5.lines
        if l.item not in ("PM motor", "Dual H bridge channel")
    )
    print(f"  S5 fixed working non-motor/non-driver base: ${fixed:.2f}")
    print(f"  {'motor $/ea':>14}  " + "  ".join(f"{k:>26}" for k in driver_cases))
    for mname, mprice in motor_cases.items():
        cells = []
        for dprice in driver_cases.values():
            total = fixed + 80 * mprice + 80 * dprice
            cells.append(f"${total:>8.2f} (+20% ${total * 1.2:>8.2f})")
        print(f"  {mname:>14}  " + "  ".join(cells))
    print(
        "\n  The $1.25 motor target is NOT a current matched quote. At the one\n"
        "  traceable 8 mm PM part (MOONS, $40 ea) the purchases explode past any\n"
        "  band. The only sub-$500 path uses untraced multipack/marketplace motors\n"
        "  whose winding, shaft and lot are not yet confirmed."
    )


if __name__ == "__main__":
    main()
