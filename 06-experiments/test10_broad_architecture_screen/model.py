#!/usr/bin/env python3
"""Transparent scale bounds for the broad architecture screen.

This is arithmetic, not a mechanism simulation or physical validation.
"""

from math import ceil, log2


N = 80
CELLS = N * N
LEVELS = 5
DEADLINE_S = 30.0
PITCH_MM = 5.08
TILE_CELLS = 10


def results() -> dict[str, float | int]:
    tiles_axis = ceil(N / TILE_CELLS)
    return {
        "cells": CELLS,
        "active_width_mm": N * PITCH_MM,
        "minimum_state_bits": CELLS * log2(LEVELS),
        "fixed_width_state_bits": CELLS * ceil(log2(LEVELS)),
        "minimum_cell_transactions_per_s": CELLS / DEADLINE_S,
        "tile_count_10x10": tiles_axis**2,
        "unary_threshold_decisions": CELLS * (LEVELS - 1),
    }


def station_time(rows_per_station: int, dwell_s: float) -> float:
    return ceil(N / rows_per_station) * dwell_s


def main() -> None:
    r = results()
    print("Shape Display scale bounds (calculation only)")
    for key, value in r.items():
        print(f"{key}: {value:.3f}" if isinstance(value, float) else f"{key}: {value}")
    print("\nParallel writer sweep at assumed 0.40 s station dwell (excludes reset):")
    for rows in (1, 2, 4, 5, 8, 10):
        print(f"  {rows:2d} rows/station: {station_time(rows, 0.40):5.2f} s")
    print("\nPurchased selector cost bounds:")
    for count in (80, 160, 320, 6400):
        costs = ", ".join(f"${count * unit:,.0f}" for unit in (0.50, 2.00, 5.00))
        print(f"  {count:4d} selectors at $0.50/$2/$5: {costs}")


if __name__ == "__main__":
    main()
