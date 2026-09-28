#!/usr/bin/env python3
"""DND-37 — independent re-derivation of the S5 winner purchased BOM.

This module does NOT trust `model.py`'s convenience constants. It reads the
sourced BOM CSV line-by-line and re-computes every headline figure the ADR-002
ratification rests on, so a discrepancy is visible rather than hidden.

Three questions it answers, all in CALCULATION evidence class:

  Q1  Does `model.py`'s fixed subtotal ($284.00) actually reproduce the
      `bom_S5_delivered.csv` expected column?  (It is asserted by checks.py;
      re-derive it here without importing the constant.)
  Q2  Is the "sourced-pair, unchanged fixed" delivered figure $503.71?
  Q3  Are the two consolidation savings real and non-double-counted?

The interesting finding is Q3. `model.py` subtracts the *expected-allowance*
value of the shift-register line ($14) and the controller line ($5) from a base
that then swaps the motor/driver to *sourced best* prices. The shift-register
line's expected allowance is $0.35/ea but its **sourced** LCSC price is
$0.0925/ea ($3.70 for 40). Removing the line can only remove the *sourced* value
you would actually have spent, so the honest register saving is $3.70, not $14.
The model therefore understates the delivered total by ~$10 on that line.
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
UPLIFT = (1.0 + 0.10) * (1.0 + 0.06)  # +10% shipping, +6% tax/import

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
          f"(ADR/README claim $503.71)")

    # Q3 — consolidation savings, model vs honest.
    #
    # model.py's reduced path subtracts $14 (registers, expected allowance) and
    # $5 (controller expected $10 -> sourced $5) from the fixed base, then adds
    # the sourced motor/driver. That returns 284 - 14 - 5 + 84 + 64 = 413 parts
    # -> $481.56 delivered.
    print()
    print("Q3  consolidation savings")
    model_parts = fixed - 14.0 - 5.0 + 80 * MOTOR_SOURCED + 80 * DRIVER_TB6612_SOURCED
    print(f"    model.py path : parts ${model_parts:.2f}  delivered ${delivered(model_parts):.2f}   "
          f"(README claim $481.56)")

    # Honest: the register line leaves the BOM entirely, so the saving is the
    # *sourced* value you would actually have paid ($3.70), not the $14 expected
    # allowance. The controller saving is the real delta $10 -> $5.
    reg_sourced_value = 40 * REGISTER_SOURCED
    honest_parts = (
        fixed - reg_sourced_value - ctrl_expected + CONTROLLER_SOURCED
        + 80 * MOTOR_SOURCED + 80 * DRIVER_TB6612_SOURCED
    )
    print(f"    honest path   : parts ${honest_parts:.2f}  delivered ${delivered(honest_parts):.2f}")
    print(f"    -> model overstates the register saving by ${reg_expected - reg_sourced_value:.2f}")
    print(f"    -> model understates delivered total by "
          f"${delivered(honest_parts) - delivered(model_parts):.2f}")

    # Sensitivity on the driver choice (the real cliff).
    print()
    print("Driver sensitivity at sourced motor $1.05, honest fixed:")
    for label, dprice in (
        ("TB6612FNG @100 $0.80", DRIVER_TB6612_SOURCED),
        ("DRV8833PWPR @100 $1.33", DRIVER_DRV_SOURCED),
    ):
        parts = fixed - reg_sourced_value - ctrl_expected + CONTROLLER_SOURCED + 80 * MOTOR_SOURCED + 80 * dprice
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

    # Q2 - the sourced-pair delivered figure is unchanged.
    q2 = delivered(fixed + 80 * MOTOR_SOURCED + 80 * DRIVER_TB6612_SOURCED)
    assert q2 == 503.71, f"sourced-pair delivered drifted: {q2}"

    # Q3 - the correction: model path overstates the register saving by $10.30.
    model_parts = fixed - reg_expected - 5.0 + 80 * MOTOR_SOURCED + 80 * DRIVER_TB6612_SOURCED
    honest_parts = (
        fixed - reg_sourced_value - ctrl_expected + CONTROLLER_SOURCED
        + 80 * MOTOR_SOURCED + 80 * DRIVER_TB6612_SOURCED
    )
    overstatement = reg_expected - reg_sourced_value
    assert round(overstatement, 2) == 10.30, f"overstatement drifted: {overstatement}"
    assert delivered(honest_parts) == 493.57, f"honest reduced drifted: {delivered(honest_parts)}"

    # The corrected path still clears $500 - if this fails the winner is over.
    assert delivered(honest_parts) < 500.0, "corrected reduced path no longer clears $500"

    # The <$400 ideal band is NOT reachable: the corrected figure must be > $400.
    assert delivered(honest_parts) > 400.0, "unexpected: corrected path claims <$400"

    print("DND-37 ratify_bom selftest OK")
    print(f"  fixed subtotal        : ${fixed:.2f}")
    print(f"  sourced-pair delivered: ${q2:.2f}")
    print(f"  model reduced (claim) : ${delivered(model_parts):.2f}")
    print(f"  corrected reduced     : ${delivered(honest_parts):.2f}")
    print(f"  register overstatement: ${overstatement:.2f}")


if __name__ == "__main__":
    import sys

    if "--selftest" in sys.argv:
        selftest()
    else:
        main()