#!/usr/bin/env python3
"""Three-scenario DELIVERED purchased-BOM for shape-display survivors S1-S5.

This is the DND-11 deliverable: a best / expected / worst *delivered* cost per
survivor, where "delivered" applies a scenario uplift for shipping, import duty
and forex to the assembled parts subtotal, so the number compared against the
$500 ceiling is what you actually pay to get the parts on the table.

  best      = highest-volume / most-favourable sourcing (marketplace multipacks,
              group-buy tiers, single consolidated shipment from one region)
  expected  = realistic single-quantity retail (small-bundle list prices, one or
              two shipments, nominal import)
  worst     = low-volume / expedited / single-source (branded distributor parts,
              split shipments, air freight, full import + handling)

Inputs: `bom_S{1..5}_delivered.csv` in this folder. Each row carries:
  item, quantity, vendor, evidence, unit_{best,expected,worst}_usd, basis.
`evidence` is one of:
  SOURCED-live      a live distributor price retrieved (LCSC JSON API)
  SOURCED-listing   a live marketplace/maker listing observed 2026-09-28
  MIXED-...         the line mixes sourced and assumed sub-decisions
  ASSUMPTION        an engineering allowance with no matched quote

Printed parts are excluded from the purchased total by design
(02-design-criteria). Print time, tooling, creep and assembly workload are
handled separately in the parent test write-up; they are real but not purchased
hardware.

Deterministic, standard library only. Run:
    python 06-experiments/test11_cost_printability_reliability/delivered_3scenario/delivered_cost_model.py
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
CELLS = 6400
CEILING = 500.0
BAND_IDEAL = 200.0
BAND_ACCEPTABLE = 400.0

SCENARIOS = ("best", "expected", "worst")

# Delivered uplift applied to the parts subtotal, split into shipping and
# import/tax. These are *assumptions*, not quotes: they reflect how a
# marketplace single-vendor shipment versus a split branded-distributor order
# behaves. A single consolidated AliExpress/Amazon order from one region is the
# cheap case; several distributor shipments + air freight + duty is the bad case.
UPLIFT = {
    "best": {"shipping": 0.05, "import_tax": 0.00},
    "expected": {"shipping": 0.10, "import_tax": 0.06},
    "worst": {"shipping": 0.18, "import_tax": 0.11},
}


@dataclass
class Line:
    item: str
    quantity: int
    vendor: str
    evidence: str
    unit: dict[str, float]
    basis: str


@dataclass
class Candidate:
    key: str
    lines: list[Line]

    def parts_subtotal(self, scenario: str) -> float:
        return sum(l.quantity * l.unit[scenario] for l in self.lines)

    def delivered(self, scenario: str) -> dict[str, float]:
        sub = self.parts_subtotal(scenario)
        up = UPLIFT[scenario]
        shipping = sub * up["shipping"]
        import_tax = sub * up["import_tax"]
        return {
            "parts": sub,
            "shipping": shipping,
            "import_tax": import_tax,
            "delivered": sub + shipping + import_tax,
        }

    def sourced_share(self) -> float:
        """Fraction of the expected-case delivered total that has a live source."""
        total = self.parts_subtotal("expected")
        if total == 0:
            return 0.0
        sourced = sum(
            l.quantity * l.unit["expected"]
            for l in self.lines
            if l.evidence.startswith("SOURCED") or l.evidence.startswith("MIXED")
        )
        return sourced / total


def load(path: Path) -> Candidate:
    lines: list[Line] = []
    with path.open(newline="") as fh:
        for row in csv.DictReader(fh):
            lines.append(
                Line(
                    item=row["item"],
                    quantity=int(row["quantity"]),
                    vendor=row["vendor"],
                    evidence=row["evidence"],
                    unit={s: float(row[f"unit_{s}_usd"]) for s in SCENARIOS},
                    basis=row["basis"],
                )
            )
    return Candidate(path.stem.split("_")[1], lines)


def verdict(delivered: float) -> str:
    if delivered < BAND_IDEAL:
        return "IDEAL (<$200)"
    if delivered < BAND_ACCEPTABLE:
        return "ACCEPTABLE (<$400)"
    if delivered < CEILING:
        return "LAST-RESORT (<$500)"
    return "OVER CEILING (>$500)"


def per_line_table(cand: Candidate) -> None:
    print(f"\n{cand.key} — per-line delivered BOM (expected case)")
    print(
        f"  {'item':<50}{'qty':>4}  {'vendor':<26}{'unit':>8}{'line':>9}  evidence"
    )
    print("  " + "-" * 118)
    for l in cand.lines:
        unit = l.unit["expected"]
        line = l.quantity * unit
        vendor = (l.vendor[:23] + "..") if len(l.vendor) > 25 else l.vendor
        print(
            f"  {l.item[:48]:<50}{l.quantity:>4}  {vendor:<26}{unit:>8.2f}{line:>9.2f}  {l.evidence}"
        )


def main() -> None:
    candidates = [load(HERE / f"bom_{k}_delivered.csv") for k in ("S1", "S2", "S3", "S4", "S5")]

    print("=" * 112)
    print("THREE-SCENARIO DELIVERED PURCHASED BOM — S1..S5 (printed parts excluded by project rule)")
    print("=" * 112)
    print(
        "Delivered uplift assumptions: "
        + "  ".join(
            f"{s}: ship {UPLIFT[s]['shipping']*100:.0f}% + tax/import {UPLIFT[s]['import_tax']*100:.0f}%"
            for s in SCENARIOS
        )
    )

    print()
    header = f"{'Candidate':<11}{'parts(b)':>10}{'deliv(b)':>10}{'parts(e)':>10}{'deliv(e)':>11}{'parts(w)':>10}{'deliv(w)':>11}{'headroom(e)':>13}  verdict(e)"
    print(header)
    print("-" * len(header))
    rows = {}
    for c in candidates:
        b, e, w = (c.delivered(s) for s in SCENARIOS)
        rows[c.key] = (b, e, w)
        print(
            f"{c.key:<11}{b['parts']:>10.2f}{b['delivered']:>10.2f}"
            f"{e['parts']:>10.2f}{e['delivered']:>11.2f}"
            f"{w['parts']:>10.2f}{w['delivered']:>11.2f}"
            f"{CEILING - e['delivered']:>13.2f}  {verdict(e['delivered'])}"
        )

    print()
    print("Cost bands: <$200 ideal | $200-400 acceptable | $400-500 last resort | >$500 unacceptable")
    print("Headroom = $500 - expected delivered (negative = over ceiling).")

    print()
    print("Evidence mix (expected-case delivered total):")
    print(f"  {'Candidate':<11}{'sourced share':>15}{'assumed share':>15}")
    for c in candidates:
        s = c.sourced_share()
        print(f"  {c.key:<11}{s:>14.0%}{1 - s:>15.0%}")

    for c in candidates:
        per_line_table(c)

    print()
    print("=" * 112)
    print("CRITICAL-PART SENSITIVITY — the two lines that decide every candidate")
    print("=" * 112)
    print(
        "Any bought part required on all 6,400 cells dominates. The reference S5 BOM needs\n"
        "80 motors + 80 drivers; its expected delivered cost swings by hundreds of dollars on\n"
        "the motor/driver unit price alone."
    )
    s5 = next(c for c in candidates if c.key == "S5")
    fixed = sum(
        l.quantity * l.unit["expected"]
        for l in s5.lines
        if l.item not in ("PM motor (8 mm 18deg bipolar micro stepper)", "Dual H-bridge channel (DRV8833PWPR bare IC or module)")
    )
    print(f"\n  S5 fixed expected parts base (all non-motor/non-driver lines): ${fixed:.2f}")
    motor_cases = {
        "amazon_multipack 1.05 (sourced)": 1.05,
        "test08_allowance 1.25": 1.25,
        "aliexpress 2.66": 2.66,
        "aliexpress 3.00 (worst)": 3.00,
        "moons_traceable 40.00": 40.00,
    }
    driver_cases = {
        "TB6612 0.80": 0.80,
        "DRV8833PWPR 1.33": 1.3338,
        "test08 0.60": 0.60,
        "DRV8833PWR@1 2.39": 2.3873,
    }
    print(f"  {'motor $/ea':>30}  " + "  ".join(f"{k:>22}" for k in driver_cases))
    up = 1 + UPLIFT["expected"]["shipping"] + UPLIFT["expected"]["import_tax"]
    for mname, mprice in motor_cases.items():
        cells = []
        for dprice in driver_cases.values():
            parts = fixed + 80 * mprice + 80 * dprice
            cells.append(f"${parts*up:>8.2f}")
        print(f"  {mname:>30}  " + "  ".join(cells))
    print(
        "\n  Only the sourced multipack motor + a <=$1.33 driver stays under $500 delivered.\n"
        "  The single traceable matched motor (MOONS, $40 ea) puts S5 at >$5,000 delivered."
    )

    print()
    print("PER-CELL BOUGHT-HARDWARE SENSITIVITY (independent of mechanism):")
    print(f"  {'$/cell':>8}{'added':>12}{'room left below $500':>24}")
    for c in (0.05, 0.10, 0.25, 0.50, 1.00):
        added = c * CELLS
        print(f"  {c:>8.2f}{added:>12.0f}${CEILING - added:>23.2f}")
    print(
        "\n  Because the board is 6,400 cells, $0.10/cell of bought hardware adds $640 —\n"
        "  already over budget before motors, power or structure. Any survivor that needs a\n"
        "  bought per-cell part has no sub-$500 path regardless of which scenario is used."
    )


if __name__ == "__main__":
    main()
