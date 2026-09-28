"""DND-44 K5/K7 cost closure — a machine-preserving path below the $500 ceiling.

Question (DND-44 §1). The reconciled `08-current-design` reports the S5 winner as
"$501.12 sourced / $483.37 reduced". Both figures used the $0.80 TB6612 driver
and the $1.05 best-case motor, and the reduced figure only cleared by moving the
shift registers onto the PCB. Re-derived from the BOM's own `unit_expected`
column, the *honest expected* delivered total is **$592.06** ($510.40 parts
x1.16). K5 is therefore materially worse than documented, and the task asks for
a sourced path below $500 with margin.

Method. Start from the repo's sourced S5 delivered BOM and apply only
**machine-preserving** changes, each labelled with its evidence class:

  E1  driver: expected DRV8833PWR $1.5828 -> sourced LCSC TB6612FNG C88224
      $0.7955 @100 (SOURCED-live). One dual-H-bridge channel per bipolar motor.
  E2  motor: expected allowance $1.25 -> sourced Amazon multipack $1.05
      (SOURCED-listing). *This is the K7 unqualified-multipack risk; if only a
      $2.66 AliExpress part is real, the row is re-priced and the machine is
      over the ceiling.*
  E3  shift registers: the $14.00 expected allowance is removed, but the 40
      chips are still bought (LCSC 74HC595D $0.0925). Net -$10.30 (DND-41).
  E4  controller: expected $10.00 -> sourced RP2040 $5.00 (SOURCED-live). -$5.00.
  E5  spares/misc: the $15.00 spares *allowance* is deleted; spares are not part
      of the machine definition. Replacement stock is a purchasing choice, not a
      design BOM line. -$15.00.
  E6  pinned sourced fixed lines are repriced at their own sourced listing price
      (guide rods/bearings, belts/idlers, head shafts, fasteners) where the BOM's
      expected column carried an allowance above the sourced listing. Each
      reduction is bounded by the BOM's own `unit_best_usd`.

Every change leaves the mechanism, pitch, travel, cell count and drive topology
untouched. The result is reported against the ceiling, and the residual is stated.

Evidence class: CALCULATION over sourced listings. No purchase, no print.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
BOM = (REPO / "06-experiments" / "test11_cost_printability_reliability"
       / "delivered_3scenario" / "bom_S5_delivered.csv")

CEILING = 500.0
IDEAL_BAND = 400.0
# The repo's additive expected delivered uplift (DND-41): +10% ship, +6% tax.
UPLIFT = 1.10 + 0.06

# E6: fixed-line repricing. Map item -> price to use. Each is the BOM's own
# `unit_best_usd` (a sourced listing price) for a line whose expected column was
# an allowance. qty for these lines is 1, so the change is the unit delta.
SOURCED_FIXED_REPRICE = {
    "Guide rods/rails and bearings": 25.00,
    "Belts pulleys idlers": 12.00,
    "Head shafts and friction-pad material": 12.00,
    "Fasteners": 8.00,
}

MOTOR_MATCH = "PM motor (8 mm 18deg bipolar micro stepper)"
DRIVER_MATCH = "Dual H-bridge channel (DRV8833PWPR bare IC or module)"
REG_MATCH = "8-bit shift registers (74HC595)"
CTRL_MATCH = "Controller (RP2040 / ESP32)"
SPARES_MATCH = "Spares and miscellaneous"

# Sourced prices chosen (evidence classes documented above).
TB6612_SOURCED = 0.7955          # LCSC C88224 @100, SOURCED-live
MOTOR_SOURCED_MULTIPACK = 1.05   # Amazon multipack, SOURCED-listing (K7 risk)
RP2040_SOURCED = 5.00            # LCSC C2040, SOURCED-live
MOTOR_ALIEXPRESS = 2.66          # SOURCED-listing; the pessimistic real part


def load_lines():
    with BOM.open(newline="") as fh:
        return [dict(r, quantity=int(r["quantity"]),
                     unit_best=float(r["unit_best_usd"]),
                     unit_expected=float(r["unit_expected_usd"]))
                for r in csv.DictReader(fh)]


def expected_baseline(lines=None) -> dict:
    lines = lines or load_lines()
    parts = sum(l["quantity"] * l["unit_expected"] for l in lines)
    return dict(parts=round(parts, 2), delivered=round(parts * UPLIFT, 2),
                verdict=verdict(parts * UPLIFT))


def verdict(delivered: float) -> str:
    if delivered < IDEAL_BAND:
        return "IDEAL (<$400)"
    if delivered < CEILING:
        return "BELOW CEILING (<$500)"
    return "OVER CEILING (>=$500)"


def reduced_lines(motor_price: float = MOTOR_SOURCED_MULTIPACK):
    """Rebuild the BOM with E1-E6 applied and report every delta."""
    lines = load_lines()
    out, audit = [], []
    for l in lines:
        item = l["item"]
        q = l["quantity"]
        new_unit = l["unit_expected"]
        reason = None
        if item.startswith(DRIVER_MATCH):
            new_unit, reason = TB6612_SOURCED, "E1 driver -> TB6612FNG sourced @100"
        elif item.startswith(MOTOR_MATCH):
            new_unit, reason = motor_price, "E2 motor -> sourced multipack listing"
        elif item.startswith(REG_MATCH):
            new_unit, reason = 0.0925, "E3 registers folded to PCB, chips still bought"
        elif item.startswith(CTRL_MATCH):
            new_unit, reason = RP2040_SOURCED, "E4 controller -> sourced RP2040"
        elif item.startswith(SPARES_MATCH):
            new_unit, reason = 0.0, "E5 spares allowance deleted (not machine definition)"
        elif item in SOURCED_FIXED_REPRICE:
            new_unit, reason = SOURCED_FIXED_REPRICE[item], "E6 fixed line -> its sourced listing"
        if reason:
            audit.append(dict(item=item, qty=q, old_unit=l["unit_expected"], new_unit=new_unit,
                              line_delta=round(q * (new_unit - l["unit_expected"]), 2), change=reason))
        out.append(dict(l, unit_sourced=new_unit))
    parts = sum(l["quantity"] * l["unit_sourced"] for l in out)
    return out, audit, parts


def closure():
    _, audit, parts = reduced_lines()
    delivered = parts * UPLIFT
    pess = reduced_lines(MOTOR_ALIEXPRESS)[2] * UPLIFT
    return dict(
        expected_baseline=expected_baseline(),
        reduction_audit=audit,
        total_reduction_usd=round(sum(a["line_delta"] for a in audit), 2),
        sourced_parts_usd=round(parts, 2),
        sourced_delivered_usd=round(delivered, 2),
        margin_usd=round(CEILING - delivered, 2),
        verdict=verdict(delivered),
        downside_motor_2p66_delivered_usd=round(pess, 2),
        downside_verdict=verdict(pess),
        k7_residual=("clears only with the unqualified $1.05 marketplace motor; at the "
                     "sourced $2.66 AliExpress part the machine is over the ceiling"),
    )


if __name__ == "__main__":
    print(json.dumps(closure(), indent=2))
