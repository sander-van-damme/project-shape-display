#!/usr/bin/env python3
"""Test11 — adversarial reliability and isolation arithmetic.

This module contains NO measured inputs. Every number here is a *calculation*
from explicit assumptions. It exists to turn the project's central qualitative
fear ("thousands of cells cannot all be right") into falsifiable, reproducible
bounds that a small physical coupon can be judged against.

Three independent questions are addressed:

1. Per-cell reliability -> probability of a perfect 6400-cell map
   (`perfect_map_probability`, `cell_error_budget`).
2. Regional updates: how many cells a reveal touches, and whether a jam can
   spread outside the target region (`regional_fraction`, `jam_containment`).
3. Friction / contamination margins: the ratio of return force to modelled
   drag, and how little extra drag breaks it (`return_margin`).

Nothing in this file establishes that any architecture works. A gate that is
"satisfied" here is satisfied only *as arithmetic on assumed inputs*; the
physical coupon protocols in the same folder are what produce measured truth.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

CELLS_FULL = 6400  # 80 x 80 at 5.08 mm pitch over a 406.4 mm active width
ROWS_FULL = 80
PITCH_MM = 5.08


def perfect_map_probability(q: float, cells: int = CELLS_FULL) -> float:
    """P(all cells correct) for independent per-cell error probability q."""
    if not 0.0 <= q <= 1.0:
        raise ValueError("q must be a probability in [0, 1]")
    return (1.0 - q) ** cells


def cell_error_budget(target: float, cells: int = CELLS_FULL) -> float:
    """Maximum independent per-cell error probability q for a perfect-map target.

    Solve (1-q)^cells = target  ->  q = 1 - target^(1/cells).
    """
    if not 0.0 < target < 1.0:
        raise ValueError("target must be in (0, 1)")
    return 1.0 - target ** (1.0 / cells)


def zero_failure_trials(
    q: float,
    confidence: float = 0.95,
    *,
    convention: str = "upper_bound",
) -> int:
    """Zero-failure independent trials n of a per-cell failure rate bound.

    Two conventions exist and they differ by a large factor; the caller must
    state which is intended. The default matches the project's headline gate
    (a one-sided *upper* confidence bound):

    - ``"upper_bound"`` (default): n such that observing **zero** failures lets
      us exclude a rate at or above q with probability ``confidence``. Requires
      ``P(0 failures) = (1-q)^n <= 1-confidence``
      -> ``n >= ln(1-confidence)/ln(1-q)``. At q=1.570e-6, conf=0.95 this is the
      project's 1,907,667-trials figure. This is the only convention valid for
      a "demonstrated reliability" claim.
    - ``"zero_failure_probability"``: the legacy formula ``ln(conf)/ln(1-q)``,
      i.e. the n at which zero failures would still occur with probability
      ``confidence`` at rate q. This is NOT a confidence bound and is ~58x
      smaller than the upper bound at q=1.570e-6. It is kept only for backward
      compatibility with the pre-2026-09 call sites; do not use it to bound q.
    """
    if not 0.0 < q < 1.0:
        raise ValueError("q must be in (0, 1)")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must be in (0, 1)")
    if convention == "upper_bound":
        # n >= ln(1-confidence) / ln(1-q); e.g. conf=0.95 -> ln(0.05)
        return math.ceil(math.log(1.0 - confidence) / math.log(1.0 - q))
    if convention == "zero_failure_probability":
        return math.ceil(math.log(confidence) / math.log(1.0 - q))
    raise ValueError(
        "convention must be 'upper_bound' or 'zero_failure_probability'"
    )


def regional_fraction(tiles_per_side: int, touched_tiles: int) -> float:
    """Fraction of the full board's cells disturbed by a regional update.

    A tile is `tiles_per_side` x `tiles_per_side` cells; the board has
    `tiles_per_side**2` tiles. `touched_tiles` updates are assumed contiguous.
    """
    if tiles_per_side < 1:
        raise ValueError("tiles_per_side must be >= 1")
    total = tiles_per_side ** 2
    if not 0 <= touched_tiles <= total:
        raise ValueError("touched_tiles out of range")
    return touched_tiles / total


def regional_update_seconds(
    full_update_seconds: float,
    fixed_overhead_seconds: float,
    touched_fraction: float,
) -> float:
    """Linear regional timing model: overhead + fraction of the per-cell work.

    This deliberately gives regional updates the *benefit of the doubt* (perfect
    scaling). It is a screening bound, not a measured schedule. If the modelled
    time already exceeds the regional budget, no measurement can rescue it.
    """
    if not 0.0 <= touched_fraction <= 1.0:
        raise ValueError("touched_fraction must be in [0, 1]")
    variable = max(full_update_seconds - fixed_overhead_seconds, 0.0)
    return fixed_overhead_seconds + variable * touched_fraction


def jam_containment(
    cells_in_target: int,
    cells_boundary_shared: int,
    jam_spreads_beyond_target: bool,
) -> str:
    """Classify a single-jam failure as contained or correlated.

    `cells_boundary_shared` is the number of cells whose mechanism is physically
    shared with the target region (same row comb, same shaft, same mask, ...).
    """
    if jam_spreads_beyond_target:
        return "CORRELATED_FAIL"
    if cells_boundary_shared > 0:
        return "BOUNDED_BUT_EXPOSED"
    return "CONTAINED"


@dataclass(frozen=True)
class ReturnMargin:
    """Gravity-vs-drag return screen for one column."""

    mass_g: float
    drag_mn: float
    gravity_mn: float

    @property
    def net_mn(self) -> float:
        return self.gravity_mn - self.drag_mn

    @property
    def ratio(self) -> float:
        """Return force / drag. ratio <= 1 means the column cannot return."""
        return self.gravity_mn / self.drag_mn

    def passes(self, min_ratio: float) -> bool:
        # Strict: ratio == min_ratio is a boundary, not a qualified pass.
        return self.ratio > min_ratio

    def extra_drag_to_fail(self) -> float:
        """Additional uniform drag (mN) that erases the net return margin."""
        return self.net_mn


def gravity_mn(mass_g: float) -> float:
    return mass_g * 1e-3 * 9.80665 * 1000.0


def return_margin(mass_g: float, drag_mn: float) -> ReturnMargin:
    return ReturnMargin(mass_g=mass_g, drag_mn=drag_mn, gravity_mn=gravity_mn(mass_g))


def tolerance_yield(
    nominal_clearance_mm: float,
    sigma_mm: float,
    min_clearance_mm: float,
) -> float:
    """Probability a printed feature keeps clearance above `min_clearance_mm`.

    Assumes clearance ~ Normal(nominal, sigma). This is a *model*, not a printer
    tolerance. It forces the register to state a sigma instead of a nominal.
    Uses an erf-based normal CDF from the standard library only.
    """
    if sigma_mm <= 0:
        raise ValueError("sigma must be positive")
    z = (nominal_clearance_mm - min_clearance_mm) / sigma_mm
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def board_yield(per_cell_yield: float, cells: int = CELLS_FULL) -> float:
    """Probability every cell on the board clears a tolerance gate (independence)."""
    if not 0.0 <= per_cell_yield <= 1.0:
        raise ValueError("per_cell_yield must be in [0, 1]")
    return per_cell_yield ** cells


def assumed_failures_per_map(q: float, cells: int = CELLS_FULL) -> float:
    """Expected number of wrong cells in one map at independent rate q."""
    return q * cells
