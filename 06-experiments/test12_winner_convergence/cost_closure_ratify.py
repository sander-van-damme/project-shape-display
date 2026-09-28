#!/usr/bin/env python3
"""DND-47 — INDEPENDENT ratification of the DND-44 machine-preserving cost closure.

This module does NOT import `cost_closure.py` (DND-44's own auditor). It reads the
committed sourced BOM (`bom_S5_delivered.csv`) line-by-line from `main` and
re-derives every headline the DND-44 cost path rests on, so a discrepancy between
the claim and the data is visible rather than inherited.

Questions answered (all CALCULATION over sourced listings; no purchase, no print):

  Q1  Does the "honest expected" baseline reproduce at $592.06 parts $510.40?
  Q2  Does the E1-E6 path reproduce at $424.95 delivered / $75.05 margin?
  Q3  Is the $1.86 motor break-even reproducible from the CSV?
  Q4  Is each E1-E6 reduction legitimate *and* scenario-consistent? In particular
      E6 reprices fixed lines from the `unit_expected` to the `unit_best` column;
      we quantify exactly how much of the margin depends on that best-case mix.
  Q5  Does any reduction remove a structural line, change the cell count, pitch,
      travel, topology, or the motor/driver count?
  Q6  (independent finding) The dual-H-bridge line is priced per *dual* IC at
      qty 80 = motor count; the honest dual-IC count is 40. Quantify the surplus.

Verdicts are printed; `--selftest` asserts them so they cannot silently regress.

Run:
    python cost_closure_ratify.py
    python cost_closure_ratify.py --selftest
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
BOM = (
    REPO
    / "06-experiments"
    / "test11_cost_printability_reliability"
    / "delivered_3scenario"
    / "bom_S5_delivered.csv"
)

CEILING = 500.0
IDEAL_BAND = 400.0
# Repo's additive expected delivered uplift (DND-41): +10% ship, +6% tax.
UPLIFT = 1.10 + 0.06  # 1.16

# --- DND-44 claimed constants, re-entered here by hand (not imported) ---------
CLAIMED_BASELINE_PARTS = 510.40
CLAIMED_BASELINE_DELIVERED = 592.06
CLAIMED_PATH_PARTS = 366.34
CLAIMED_PATH_DELIVERED = 424.95
CLAIMED_MARGIN = 75.05
CLAIMED_DOWNSIDE_2P66 = 574.36
CLAIMED_MOTOR_BREAK_EVEN = 1.86

# Sourced prices re-entered by hand.
TB6612_SOURCED = 0.7955   # LCSC C88224 @100
MOTOR_MULTIPACK = 1.05    # Amazon multipack listing (K7 risk)
MOTOR_ALIEXPRESS = 2.66   # AliExpress micro listing
RP2040_SOURCED = 5.00     # LCSC C2040
REGISTER_CHIP_SOURCED = 0.0925  # LCSC C5947 @50

MOTOR = "PM motor (8 mm 18deg bipolar micro stepper)"
DRIVER = "Dual H-bridge channel (DRV8833PWPR bare IC or module)"
REGISTERS = "8-bit shift registers (74HC595)"
CONTROLLER = "Controller (RP2040 / ESP32)"
SPARES = "Spares and miscellaneous"

# E6 fixed-line repricing as claimed by DND-44: item -> its own unit_best value.
E6_REPRICE = {
    "Guide rods/rails and bearings": 25.00,
    "Belts pulleys idlers": 12.00,
    "Head shafts and friction-pad material": 12.00,
    "Fasteners": 8.00,
}


def load_rows() -> list[dict]:
    with BOM.open(newline="") as fh:
        return [
            dict(
                r,
                quantity=int(r["quantity"]),
                unit_best=float(r["unit_best_usd"]),
                unit_expected=float(r["unit_expected_usd"]),
                unit_worst=float(r["unit_worst_usd"]),
            )
            for r in csv.DictReader(fh)
        ]


def delivered(parts: float) -> float:
    return round(parts * UPLIFT, 2)


def baseline(rows: list[dict]) -> dict:
    parts = sum(r["quantity"] * r["unit_expected"] for r in rows)
    return dict(parts=round(parts, 2), delivered=delivered(parts))


def path(rows: list[dict], motor_price: float = MOTOR_MULTIPACK) -> tuple[float, list[dict]]:
    """Apply E1-E6 independently and return (parts, audit rows)."""
    audit = []
    total = 0.0
    for r in rows:
        item, q, old = r["item"], r["quantity"], r["unit_expected"]
        new = old
        tag = None
        if item == DRIVER:
            new, tag = TB6612_SOURCED, "E1 driver -> sourced TB6612FNG @100"
        elif item == MOTOR:
            new, tag = motor_price, "E2 motor -> sourced multipack listing"
        elif item == REGISTERS:
            new, tag = REGISTER_CHIP_SOURCED, "E3 registers on PCB, chips still bought"
        elif item == CONTROLLER:
            new, tag = RP2040_SOURCED, "E4 controller -> sourced RP2040"
        elif item == SPARES:
            new, tag = 0.0, "E5 spares allowance deleted"
        elif item in E6_REPRICE:
            new, tag = E6_REPRICE[item], "E6 fixed line -> its unit_best"
        total += q * new
        if tag:
            audit.append(
                dict(item=item, qty=q, old=old, new=new, delta=round(q * (new - old), 2), tag=tag)
            )
    return round(total, 2), audit


def path_without_e6(rows: list[dict], motor_price: float = MOTOR_MULTIPACK) -> float:
    """E1-E5 only, fixed lines left at their expected value."""
    p, _ = path(rows, motor_price)
    e6_delta = sum(
        r["quantity"] * (E6_REPRICE[r["item"]] - r["unit_expected"])
        for r in rows
        if r["item"] in E6_REPRICE
    )
    return round(p - e6_delta, 2)


def motor_break_even(rows: list[dict]) -> float:
    """Motor unit price at which the full E1-E6 path hits $500 delivered.

    Total parts is linear in the motor price m: fixed_other + 80*m. Recover both
    from the path evaluated at m = 0 and m = 1.
    """
    p_lo, _ = path(rows, 0.0)
    p_hi, _ = path(rows, 1.0)
    slope_per_unit = (p_hi - p_lo) / 1.0  # = motor channel count
    fixed_other = p_lo
    target_parts = CEILING / UPLIFT
    return (target_parts - fixed_other) / slope_per_unit


def run() -> dict:
    rows = load_rows()
    base = baseline(rows)
    p_parts, audit = path(rows)
    p_deliv = delivered(p_parts)
    no_e6_parts = path_without_e6(rows)
    e6_contribution_deliv = round((p_parts - no_e6_parts) * UPLIFT, 2)
    be = motor_break_even(rows)
    downside = delivered(path(rows, MOTOR_ALIEXPRESS)[0])

    # Q6: dual-H-bridge surplus. The line name is "Dual H-bridge channel" but the
    # priced part (DRV8833/TB6612) is a *dual* bridge; 80 motors need 40 ICs.
    drv_rows = [r for r in rows if r["item"] == DRIVER]
    drv_qty = drv_rows[0]["quantity"] if drv_rows else 0
    drv_ic_surplus_units = drv_qty - drv_qty // 2
    drv_surplus_delivered = round(
        drv_ic_surplus_units * TB6612_SOURCED * UPLIFT, 2
    )

    # Machine-preservation: every structural line must still be present.
    structural = {
        "Lift motor",
        "Scanner motor",
        "Guide rods/rails and bearings",
        "Four lift screws and nuts",
        "Belts pulleys idlers",
        "Power supplies and protection",
        "Wire connectors flexible loom",
        "Head shafts and friction-pad material",
        "Fasteners",
        "Custom driver PCBs and passives",
    }
    present = {r["item"] for r in rows} - {SPARES}
    missing = structural - present

    return dict(
        baseline_parts=base["parts"],
        baseline_delivered=base["delivered"],
        path_parts=p_parts,
        path_delivered=p_deliv,
        margin=round(CEILING - p_deliv, 2),
        downside_2p66=downside,
        break_even=round(be, 4),
        e6_contribution_delivered=e6_contribution_deliv,
        path_without_e6_delivered=delivered(no_e6_parts),
        path_without_e6_margin=round(CEILING - delivered(no_e6_parts), 2),
        driver_qty=drv_qty,
        driver_ic_surplus_units=drv_ic_surplus_units,
        driver_surplus_delivered=drv_surplus_delivered,
        structural_missing=sorted(missing),
        audit=audit,
    )


def report() -> None:
    r = run()
    print("DND-47 independent ratification of the DND-44 cost closure")
    print("=" * 68)
    print(f"Q1 honest expected baseline : parts ${r['baseline_parts']:.2f}  "
          f"delivered ${r['baseline_delivered']:.2f}   "
          f"({'MATCH' if abs(r['baseline_delivered']-CLAIMED_BASELINE_DELIVERED)<0.01 else 'MISMATCH'})")
    print(f"Q2 E1-E6 path               : parts ${r['path_parts']:.2f}  "
          f"delivered ${r['path_delivered']:.2f}  margin ${r['margin']:.2f}   "
          f"({'MATCH' if abs(r['path_delivered']-CLAIMED_PATH_DELIVERED)<0.01 else 'MISMATCH'})")
    print(f"   downside @ $2.66 motor   : ${r['downside_2p66']:.2f}   "
          f"({'MATCH' if abs(r['downside_2p66']-CLAIMED_DOWNSIDE_2P66)<0.01 else 'MISMATCH'})")
    print(f"Q3 motor break-even /ea     : ${r['break_even']:.4f}  "
          f"(claimed ${CLAIMED_MOTOR_BREAK_EVEN})")
    print()
    print("Q4 scenario consistency of the reduction path")
    print(f"   E6 (expected->best fixed) : ${r['e6_contribution_delivered']:.2f} of the "
          f"${r['margin']:.2f} margin")
    print(f"   path WITHOUT E6           : delivered ${r['path_without_e6_delivered']:.2f}  "
          f"margin ${r['path_without_e6_margin']:.2f} "
          f"({'still clears' if r['path_without_e6_margin']>0 else 'FAILS'})")
    print()
    print("Q5 machine preservation")
    print(f"   structural lines missing  : {r['structural_missing'] or 'none'}")
    print()
    print("Q6 independent finding: dual-H-bridge count")
    print(f"   line qty {r['driver_qty']} priced per DUAL IC; 80 motors need "
          f"{r['driver_qty']//2} ICs -> surplus {r['driver_ic_surplus_units']} ICs")
    print(f"   surplus delivered cost    : ${r['driver_surplus_delivered']:.2f} "
          f"(conservatism against the design, not a threat)")
    print()
    print("Per-reduction audit (E1-E6):")
    for a in r["audit"]:
        print(f"   {a['tag']:<52} {a['item'][:34]:<36} {a['delta']:>+8.2f}")


def selftest() -> None:
    r = run()
    assert abs(r["baseline_parts"] - CLAIMED_BASELINE_PARTS) < 0.01, r["baseline_parts"]
    assert abs(r["baseline_delivered"] - CLAIMED_BASELINE_DELIVERED) < 0.01, r["baseline_delivered"]
    assert abs(r["path_parts"] - CLAIMED_PATH_PARTS) < 0.01, r["path_parts"]
    assert abs(r["path_delivered"] - CLAIMED_PATH_DELIVERED) < 0.01, r["path_delivered"]
    assert abs(r["margin"] - CLAIMED_MARGIN) < 0.01, r["margin"]
    assert abs(r["downside_2p66"] - CLAIMED_DOWNSIDE_2P66) < 0.01, r["downside_2p66"]
    assert 1.85 <= r["break_even"] <= 1.87, r["break_even"]
    # The path survives E6 removal only because the motor is at best-case.
    assert r["path_without_e6_margin"] > 0, "E6 removal drops the path over the ceiling"
    # No structural line is removed by any reduction.
    assert r["structural_missing"] == [], r["structural_missing"]
    # The dual-IC surplus is a real conservatism of shape ~$37 delivered.
    assert 35.0 < r["driver_surplus_delivered"] < 40.0, r["driver_surplus_delivered"]
    print("DND-47 cost-closure ratify selftest OK")
    print(f"  baseline ${r['baseline_delivered']:.2f}  path ${r['path_delivered']:.2f}  "
          f"margin ${r['margin']:.2f}  break-even ${r['break_even']:.2f}")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        report()
