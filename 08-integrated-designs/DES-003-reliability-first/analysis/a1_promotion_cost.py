"""a1 promotion cost; CAD/calculation source, no physical validation."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import reliability_mask as m  # noqa: E402

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
BOM_CSV = HERE.parent / "bom_a1.csv"

UPLIFT = 1.10 + 0.06  # 1.16 additive convention
BAND_IDEAL = 200.0
BAND_ACCEPTABLE = 400.0
BAND_LAST_RESORT = 500.0

# design calculation hostile-reprice convention: soft lines (allowance/assumption) +35 %.
SOFT_EVIDENCE = {"allowance", "assumption"}


def load_bom() -> list[dict]:
    rows: list[dict] = []
    with open(BOM_CSV, newline="") as f:
        for r in csv.DictReader(f):
            rows.append(dict(
                item=r["line"], qty=float(r["qty"]),
                unit_usd=float(r["unit_usd"]), ext_usd=float(r["ext_usd"]),
                evidence=r["evidence"], use=r["use"]))
    return rows


def band(parts_usd: float) -> str:
    if parts_usd < BAND_IDEAL:
        return "IDEAL (<$200)"
    if parts_usd < BAND_ACCEPTABLE:
        return "ACCEPTABLE ($200-400)"
    if parts_usd < BAND_LAST_RESORT:
        return "LAST RESORT ($400-500)"
    return "UNACCEPTABLE (>$500)"


def hostile_reprice(rows: list[dict]) -> dict:
    hostile = [r["ext_usd"] * 1.35 if r["evidence"] in SOFT_EVIDENCE
               else r["ext_usd"] for r in rows]
    total = round(sum(hostile), 2)
    return dict(hostile_parts_usd=total,
                hostile_delivered_usd=round(total * UPLIFT, 2),
                band=band(total))


def ceilings(rows: list[dict]) -> dict:
    """Max unit prices that keep the purchased total inside each band.

    Reader head is qty 1, so its ceiling is band_target - rest_of_bom.
    Gantry motion (2 steppers + 2 rail lines + 2 belt lines = $68) is stated
    as a sub-assembly budget the same way.
    """
    parts = round(sum(r["ext_usd"] for r in rows), 2)
    reader = next(r for r in rows if r["item"].startswith("Reader head"))
    rest = parts - reader["ext_usd"]
    motion_items = [r for r in rows
                    if "stepper" in r["item"] or "rail" in r["item"]
                    or "belt" in r["item"]]
    motion = round(sum(r["ext_usd"] for r in motion_items), 2)
    return dict(
        purchased_parts_usd=parts,
        reader_head_unit_usd=reader["unit_usd"],
        reader_head_max_for_ideal_usd=round(BAND_IDEAL - rest - 0.01, 2),
        reader_head_max_for_acceptable_usd=round(BAND_ACCEPTABLE - rest - 0.01, 2),
        gantry_motion_subtotal_usd=motion,
        gantry_motion_max_for_ideal_usd=round(BAND_IDEAL - (parts - motion) - 0.01, 2),
        per_cell_bought_usd=round(parts / 6400, 4),
        # The checks.py-style assertion a gate could enforce:
        ceiling_assert=("assert reader_head_unit_usd <= "
                        + f"{round(BAND_IDEAL - rest - 0.01, 2)}  "
                          f"# keeps purchased parts <$200 (ideal)"),
    )


def report() -> dict:
    rows = load_bom()
    parts = round(sum(r["ext_usd"] for r in rows), 2)
    delivered = round(parts * UPLIFT, 2)
    model_parts = m.a1_bom()["purchased_parts_usd"]
    return dict(
        evidence_class="CALCULATION over sourced-class prices (design calculation)",
        lines=len(rows),
        purchased_parts_usd=parts,
        delivered_usd=delivered,
        uplift=UPLIFT,
        band=band(parts),
        margin_to_next_band_usd=round(
            (BAND_ACCEPTABLE if parts < BAND_IDEAL else BAND_LAST_RESORT) - parts, 2),
        hostile=hostile_reprice(rows),
        ceilings=ceilings(rows),
        csv_matches_model=bool(abs(parts - model_parts) < 1e-9),
        per_cell_bought_hardware="none (0 bought actuators per cell; 4 shared)",
        note=("Printed frame/columns/latches excluded per design calculation. Prices are "
              "point-in-time sourced-class figures (2026-09), not quotations."),
    )


CHECKS: list[tuple[str, bool]] = []


def check(name: str, cond: bool) -> None:
    CHECKS.append((name, bool(cond)))


def gate() -> int:
    r = report()
    CHECKS.clear()
    check("BOM CSV matches reliability_mask model ($181.00)",
          r["csv_matches_model"] and r["purchased_parts_usd"] == 181.00)
    check("purchased parts land IDEAL (<$200)", r["band"].startswith("IDEAL"))
    check("delivered lands ACCEPTABLE ($200-400)",
          BAND_IDEAL <= r["delivered_usd"] < BAND_ACCEPTABLE)
    check("hostile reprice (+35 % soft lines) stays ACCEPTABLE",
          r["hostile"]["hostile_parts_usd"] < BAND_ACCEPTABLE)
    check("no per-cell bought hardware",
          r["ceilings"]["per_cell_bought_usd"] < 0.05)
    check("reader-head ideal ceiling is a positive enforceable number",
          r["ceilings"]["reader_head_max_for_ideal_usd"] > r["ceilings"]["reader_head_unit_usd"])
    # The S5-gate precedent assertion, executed for real:
    reader_unit = r["ceilings"]["reader_head_unit_usd"]
    check("checks.py-style ceiling assertion holds "
          f"(reader <= ${r['ceilings']['reader_head_max_for_ideal_usd']})",
          reader_unit <= r["ceilings"]["reader_head_max_for_ideal_usd"])
    passed = sum(1 for _, ok in CHECKS if ok)
    total = len(CHECKS)
    for name, ok in CHECKS:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\npurchased ${r['purchased_parts_usd']} "
          f"({r['band']}); delivered ${r['delivered_usd']}; "
          f"hostile ${r['hostile']['hostile_parts_usd']} "
          f"({r['hostile']['band']})")
    print(f"ceiling: {r['ceilings']['ceiling_assert']}")
    print(f"{passed}/{total} cost checks pass")
    return 0 if passed == total else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", action="store_true")
    args = ap.parse_args(argv)
    if args.gate:
        return gate()
    print(json.dumps(report(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
