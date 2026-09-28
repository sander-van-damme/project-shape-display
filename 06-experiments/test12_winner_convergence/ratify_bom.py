#!/usr/bin/env python3
"""DND-37 — independent re-derivation of the S5 winner purchased BOM.

This module does NOT trust `model.py`'s convenience constants. It reads the
sourced BOM CSV line-by-line and re-computes every headline figure the ADR-002
ratification rests on, so a discrepancy is visible rather than hidden.

Three questions it answers, all in CALCULATION evidence class:

  Q1  Does `model.py`'s fixed subtotal ($284.00) actually reproduce the
      `bom_S5_delivered.csv` expected column?  (It is asserted by checks.py;
      re-derive it here without importing the constant.)
  Q2  Is the "sourced-pair, unchanged fixed" delivered figure $501.12?
  Q3  Are the two consolidation savings real and non-double-counted?

Two corrections are pinned here so neither can silently regress:

  1. Delivered uplift basis [DND-41 / Falsifier Finding A]. The repo's own
     `delivered_3scenario/delivered_cost_model.py` applies the expected uplift
     ADDITIVELY: sub + sub*0.10 (shipping) + sub*0.06 (tax) = sub*1.16. The
     earlier multiplicative `(1.10)*(1.06)=1.166` double-counts by compounding
     and inflated every headline by ~0.5%. The sourced-pair delivered figure on
     the repo's own basis is therefore `$432.00 * 1.16 = $501.12`, NOT $503.71.

  2. Register consolidation [DND-41 / Falsifier Finding A]. `model.py` subtracts
     the *expected-allowance* value of the shift-register line ($14) from the
     fixed base. But the discrete line leaves the BOM and the 40 chips are still
     BOUGHT at their sourced LCSC price ($0.0925/ea = $3.70). The NET saving is
     $14.00 - $3.70 = $10.30, not $14.00. Likewise the controller line: the $10
     expected allowance leaves and a $5 sourced RP2040 enters -> net $5.00.
     The honest reduced fixed subtotal is thus
     `284.00 - 10.30 - 5.00 = $268.70`, parts `$416.70`, delivered
     `$416.70 * 1.16 = $483.37`.
"""
from __future__ import annotations

import csv
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

# Expected-scenario delivered uplift, matching delivered_cost_model.py / model.py.
# [DND-41] ADDITIVE basis: +10% shipping, +6% tax/import on the parts subtotal.
# The prior multiplicative (1.10)*(1.06)=1.166 double-counted by compounding.
UPLIFT = 1.0 + 0.10 + 0.06  # = 1.16

# Sourced unit prices re-confirmed 2026-09-28 (see sourcing_notes.md).
MOTOR_SOURCED = 1.05           # Amazon "Abovehill" multipack, sourced listing
DRIVER_TB6612_SOURCED = 0.80   # TB6612FNG @100, LCSC C88224
DRIVER_DRV_SOURCED = 1.3338    # DRV8833PWPR @100, LCSC C50506
REGISTER_SOURCED = 0.0925      # 74HC595D @50, LCSC C5947
CONTROLLER_SOURCED = 5.00      # RP2040 / Pico sourced


def load_rows() -> list[dict]:
    with BOM.open(newline="") as fh:
        return list(csv.DictReader(fh))


def is_motor(item: str) -> bool:
    return item.startswith("PM motor")


def is_driver(item: str) -> bool:
    return item.startswith("Dual H-bridge")


def is_register(item: str) -> bool:
    return "shift register" in item.lower()


def is_controller(item: str) -> bool:
    return item.startswith("Controller")


def fixed_expected(rows: list[dict]) -> float:
    """Non motor/driver lines, expected column. Re-derives model.FIXED_SUBTOTAL_USD."""
    return round(
        sum(
            int(r["quantity"]) * float(r["unit_expected_usd"])
            for r in rows
            if not is_motor(r["item"]) and not is_driver(r["item"])
        ),
        2,
    )


def delivered(parts: float) -> float:
    return round(parts * UPLIFT, 2)


def main() -> None:
    rows = load_rows()

    motor_expected = sum(
        int(r["quantity"]) * float(r["unit_expected_usd"]) for r in rows if is_motor(r["item"])
    )
    driver_expected = sum(
        int(r["quantity"]) * float(r["unit_expected_usd"]) for r in rows if is_driver(r["item"])
    )
    reg_expected = sum(
        int(r["quantity"]) * float(r["unit_expected_usd"]) for r in rows if is_register(r["item"])
    )
    ctrl_expected = sum(
        int(r["quantity"]) * float(r["unit_expected_usd"]) for r in rows if is_controller(r["item"])
    )

    print("DND-37 independent S5 BOM re-derivation")
    print("=" * 60)
    print(f"register line qty x expected unit : {reg_expected/0.35:.0f} x $0.35 = ${reg_expected:.2f}")
    print(f"controller line (expected)        : ${ctrl_expected:.2f}")
    print()

    # Q1 — fixed subtotal.
    fixed = fixed_expected(rows)
    print(f"Q1  fixed expected subtotal       : ${fixed:.2f}   "
          f"({'matches' if fixed == 284.00 else 'MISMATCH vs'} model $284.00)")

    # Q2 — sourced pair, unchanged fixed.
    q2 = fixed + 80 * MOTOR_SOURCED + 80 * DRIVER_TB6612_SOURCED
    print(f"Q2  sourced-pair parts subtotal   : ${q2:.2f}")
    print(f"    sourced-pair delivered (x1.16): ${delivered(q2):.2f}   "
          f"(DND-41 corrected; over the $500 ceiling)")

    # Q3 — consolidation savings, model vs honest.
    #
    # [DND-41] The register line leaves the BOM and the 40 chips are still bought
    # at their sourced price, so the NET register saving is the allowance minus
    # the sourced chip cost: $14.00 - $3.70 = $10.30. The controller line swaps a
    # $10 expected allowance for a $5 sourced RP2040 -> net $5.00.
    print()
    print("Q3  consolidation savings (net of still-bought chips)")
    reg_net = reg_expected - 40 * REGISTER_SOURCED           # 14.00 - 3.70 = 10.30
    ctrl_net = ctrl_expected - CONTROLLER_SOURCED            # 10.00 - 5.00 = 5.00
    honest_fixed = fixed - reg_net - ctrl_net
    honest_parts = honest_fixed + 80 * MOTOR_SOURCED + 80 * DRIVER_TB6612_SOURCED
    print(f"    net register saving : ${reg_net:.2f}   net controller saving: ${ctrl_net:.2f}")
    print(f"    honest fixed        : ${honest_fixed:.2f}")
    print(f"    honest path         : parts ${honest_parts:.2f}  delivered ${delivered(honest_parts):.2f}")

    # Sensitivity on the driver choice (the real cliff).
    print()
    print("Driver sensitivity at sourced motor $1.05, honest fixed:")
    for label, dprice in (
        ("TB6612FNG @100 $0.80", DRIVER_TB6612_SOURCED),
        ("DRV8833PWPR @100 $1.33", DRIVER_DRV_SOURCED),
    ):
        parts = honest_fixed + 80 * MOTOR_SOURCED + 80 * dprice
        print(f"  {label:<24} parts ${parts:7.2f}  delivered ${delivered(parts):7.2f}")

    # Fully expected (no sourcing at all), for the honest upper bound.
    fully_expected = fixed + motor_expected + driver_expected
    print()
    print(f"Fully expected (BOM as written): delivered ${delivered(fully_expected):.2f}")

    # Per-cell bought hardware sensitivity (the portable result).
    print()
    print("Per-cell bought-hardware sensitivity (6,400 cells):")
    for c in (0.05, 0.10, 0.25, 0.50, 1.00):
        print(f"  ${c:.2f}/cell -> ${c*6400:7.0f} added, ${500 - c*6400:8.0f} left below $500")


def ctrl_controller_offset() -> float:
    """Controller line, sourced price, replacing its expected allowance."""
    return CONTROLLER_SOURCED


def selftest() -> None:
    """Assert the DND-37 findings so the correction cannot silently regress.

    Exits 0 with a summary on success; raises AssertionError on any drift.
    """
    rows = load_rows()
    fixed = fixed_expected(rows)
    reg_expected = sum(
        int(r["quantity"]) * float(r["unit_expected_usd"]) for r in rows if is_register(r["item"])
    )
    ctrl_expected = sum(
        int(r["quantity"]) * float(r["unit_expected_usd"]) for r in rows if is_controller(r["item"])
    )
    reg_sourced_value = 40 * REGISTER_SOURCED

    # Q1 - the fixed subtotal really is reproduced from the CSV.
    assert fixed == 284.00, f"fixed subtotal drifted: {fixed}"

    # Q2 - the sourced-pair delivered figure on the ADDITIVE basis [DND-41].
    q2 = delivered(fixed + 80 * MOTOR_SOURCED + 80 * DRIVER_TB6612_SOURCED)
    assert q2 == 501.12, f"sourced-pair delivered drifted: {q2}"

    # Q3 - the correction: net register saving is $10.30, not the full $14.
    reg_net = reg_expected - reg_sourced_value            # 14.00 - 3.70 = 10.30
    ctrl_net = ctrl_expected - CONTROLLER_SOURCED         # 10.00 - 5.00 = 5.00
    overstatement = reg_expected - reg_sourced_value
    assert round(overstatement, 2) == 10.30, f"overstatement drifted: {overstatement}"
    honest_fixed = fixed - reg_net - ctrl_net
    honest_parts = honest_fixed + 80 * MOTOR_SOURCED + 80 * DRIVER_TB6612_SOURCED
    assert delivered(honest_parts) == 483.37, f"honest reduced drifted: {delivered(honest_parts)}"

    # The corrected path still clears $500 - if this fails the winner is over.
    assert delivered(honest_parts) < 500.0, "corrected reduced path no longer clears $500"

    # The <$400 ideal band is NOT reachable: the corrected figure must be > $400.
    assert delivered(honest_parts) > 400.0, "unexpected: corrected path claims <$400"

    print("DND-37 ratify_bom selftest OK")
    print(f"  fixed subtotal        : ${fixed:.2f}")
    print(f"  sourced-pair delivered: ${q2:.2f}")
    print(f"  net register saving   : ${reg_net:.2f}")
    print(f"  net controller saving : ${ctrl_net:.2f}")
    print(f"  corrected reduced     : ${delivered(honest_parts):.2f}")


if __name__ == "__main__":
    import sys

    if "--selftest" in sys.argv:
        selftest()
    else:
        main()