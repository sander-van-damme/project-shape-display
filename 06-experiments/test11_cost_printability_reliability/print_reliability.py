#!/usr/bin/env python3
"""Printability, tolerance-stack and reliability scaling checks for 5.08 mm pitch.

Pure arithmetic under stated assumptions. No physical measurement. Everything here
is a screen: it tells you which geometry and reliability claims are arithmetically
implausible, not which ones are proven.

Run:
    python 06-experiments/test11_cost_printability_reliability/print_reliability.py
"""

from __future__ import annotations

import math

PITCH_MM = 5.08
CELLS = 6400
TILES_10x10 = 64

# Bambu Lab X1C / PLA baseline (02-design-criteria).
NOZZLE_STD_MM = 0.40
NOZZLE_FINE_MM = 0.20
MIN_WALL_STD_MM = 0.42  # ~1 line width plus a hair, a practical 0.4-nozzle floor
MIN_WALL_FINE_MM = 0.22


def cell_web(pitch: float, body_width: float) -> float:
    """Web between two neighboring printed bodies at a given pitch."""
    return (pitch - body_width) / 2.0


def tolerance_stack(
    nominal_gap: float,
    contributors: dict[str, float],
) -> tuple[float, float]:
    """Worst-case and RSS residual of a clearance stack.

    contributors are *symmetric* +/- values (mm). Worst-case subtracts the sum of
    magnitudes; RSS subtracts sqrt(sum of squares).
    """
    worst = nominal_gap - sum(contributors.values())
    rss = nominal_gap - math.sqrt(sum(v * v for v in contributors.values()))
    return worst, rss


def rows() -> list[str]:
    out: list[str] = []
    ap = out.append

    ap("=" * 78)
    ap("PRINTABILITY + TOLERANCE + RELIABILITY SCREEN — 5.08 mm pitch")
    ap("=" * 78)

    ap("\n1. Printed web between bodies at 5.08 mm pitch")
    for body in (4.68, 4.48, 4.40):
        web = cell_web(PITCH_MM, body)
        verdict = (
            "OK for 0.4 mm nozzle" if web >= 0.45
            else ("marginal on 0.4 mm; fine-nozzle/resin preferred"
                  if web >= MIN_WALL_FINE_MM
                  else "NOT printable as a single wall")
        )
        ap(f"   body {body:.2f} mm -> web {web * 1000:.0f} um/side: {verdict}")
    ap("   A 4.68 mm body leaves a 200 um web: below a 0.4 mm line width, so this")
    ap("   is a FINE-NOZZLE / resin feature, not ordinary 0.4 mm geometry.")
    ap("   4.48 mm leaves 300 um and 4.40 mm leaves 340 um: still narrower than a")
    ap("   clean 0.4 mm wall but printable as a thin single wall; both are marginal.")
    ap("   4.40 mm lowers surface fill from 84.9% to 75.0%.")

    ap("\n2. Nominal top-gap stack (Test08 published: 0.40 mm nominal, 0.05 mm after)")
    contributors = {
        "printed width error  +/-0.10": 0.10,
        "pitch/index error     +/-0.05": 0.05,
        "deflection allowance  +/-0.10": 0.10,
    }
    worst, rss = tolerance_stack(0.40, contributors)
    ap(f"   contributors: {contributors}")
    ap(f"   worst-case residual {worst * 1000:.0f} um; RSS residual {rss * 1000:.0f} um")
    ap("   At 5.08 mm pitch a nominal 0.40 mm gap can vanish before any glue, dust")
    ap("   or creep. This is why the pitch is a coupon problem, not a CAD constant.")

    ap("\n3. Guide-wall clearance budget (Test08 revised: 0.20 mm wall, 0.10 mm/side)")
    af = 0.0
    ap("   wall 0.20 mm < 0.22 mm fine-nozzle floor with any XY compensation.")
    ap("   => needs 0.2 mm nozzle or resin. It is NOT 0.4 mm-nozzle geometry.")

    ap("\n4. Print-farm throughput and assembly scale")
    for part_seconds, label in ((45, "fast small part"), (120, "medium part"), (300, "slow fine part")):
        for n_parts in (2, 3):
            per_cell = n_parts
            total_parts = CELLS * per_cell
            printer_hours = total_parts * part_seconds / 3600.0
            ap(f"   {label}: {n_parts} parts/cell, {total_parts} parts, "
               f"{printer_hours:,.0f} printer-hours")
    ap("   At 120 s/part and 2 parts/cell, 12,800 parts is ~427 printer-hours")
    ap("   (~18 days continuous). One X1C cannot print the whole board in one")
    ap("   sitting; print yield across thousands of parts is a real risk.")

    ap("\n5. Reliability scaling: P(perfect map) = (1-q)^6400")
    ap(f"   {'q per cell-update':>20}{'P(perfect map)':>18}{'cells correct':>16}")
    for q in (1e-2, 3e-3, 1e-3, 1e-4, 1e-5, 1.57e-6, 1e-6):
        p = (1 - q) ** CELLS
        ap(f"   {q:>20.2e}{p:>17.4%}{CELLS * (1 - q):>16.1f}")
    ap("   A 99% perfect-map goal needs q <= 1.57e-6 per cell-update (independent).")
    ap("   Per-cell bought hardware with a per-part 0.1% reject rate already")
    ap("   consumes the entire allowance for the whole board.")

    ap("\n6. Independent-trial bound for a one-sided 95% confidence at 99% map")
    q_goal = 1.0 - 0.99 ** (1.0 / CELLS)
    n_trials = math.ceil(math.log(0.05) / math.log(1 - q_goal))
    ap(f"   q_goal = {q_goal:.3e};  n >= {n_trials:,} zero-failure independent trials")
    ap("   A six-cell or eight-channel demonstration cannot reach this. Detection")
    ap("   with bounded recovery is required, or the goal must be relaxed.")

    ap("\n7. Assembly burden")
    for sec_per_part in (10, 20, 30):
        parts_per_cell = 4  # column, rotor, guide, detent
        total = CELLS * parts_per_cell
        hours = total * sec_per_part / 3600.0
        ap(f"   {parts_per_cell} parts/cell @ {sec_per_part}s each: {hours:,.0f} hands-on hours")
    ap("   100–200 h is the documented planning range; thousands of fine parts make")
    ap("   cartridge/tile strategy (not monolithic gluing) mandatory.")

    return out


def main() -> None:
    print("\n".join(rows()))


if __name__ == "__main__":
    main()
