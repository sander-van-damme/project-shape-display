#!/usr/bin/env python3
"""Deterministic arithmetic checks for E-044; no hardware claims."""

from decimal import Decimal


def money(*terms):
    return sum((Decimal(str(term)) for term in terms), Decimal("0.00"))


assert money(370, 175, 45, 37.68, 4.38, 4.59, 18.32, 30) == Decimal("684.97")
assert money(370, 75, 20, 13.36, 4.38, 4.59, 18.32, 30) == Decimal("535.65")
assert money(486.29, 386.00) == Decimal("872.29")
assert money(505.59, 416.00) == Decimal("921.59")
assert Decimal("4") * Decimal("3.34") == Decimal("13.36")
assert Decimal("4") * Decimal("9.42") == Decimal("37.68")
assert Decimal("30.00") - Decimal("20.18") == Decimal("9.82")
assert Decimal("2.00") - Decimal("1.80") == Decimal("0.20")

print("E-044 arithmetic: PASS")
print("base=$684.97 low=$535.65 canonical_reuse=$486.29-$872.29 canonical_fallback=$505.59-$921.59")
