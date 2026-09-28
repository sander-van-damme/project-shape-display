#!/usr/bin/env python3
"""Sensitivity sweeps: what would have to be TRUE for S1/S2 to survive?

For each failed rejection test, sweep the plausible parameter range and report
the break-even value and whether it is physically reachable. This separates a
fundamental failure from a fixable one, which is the actual decision input.
"""

from __future__ import annotations

import math

PITCH_MM = 5.08
CELLS = 6400
LEVELS = 5


def force_break_even(max_n: float = 1500.0) -> float:
    """Max per-cell release force if all 6400 pawls release in one stroke."""
    return max_n / CELLS


def force_sweep() -> None:
    print("=== B2: all-armed stroke (worst-case all-high map) ===")
    print(f"break-even per-cell pawl release force: {force_break_even():.3f} N")
    for f in (0.05, 0.10, 0.15, 0.20, 0.25, 0.37):
        total = f * CELLS
        print(f"  {f:.3f} N/cell -> {total:6.0f} N board-wide "
              f"({'ok' if total <= 1500 else 'FAIL'})")
    print("  mitigation: split into 4 staggered sub-strokes x 10 mm, or")
    print("  subdivide the board into banks lifted in a short sequence.")


def variation_break_even(n: int = CELLS, window_low: float = 0.30,
                         window_high: float = 0.80,
                         target: float = 0.45) -> float:
    """Largest sigma (fraction) that still gives P(all 6400 good) > 0.5."""
    from math import erf, sqrt
    def p_out(sig_frac: float) -> float:
        s = target * sig_frac
        def phi(x: float) -> float:
            return 0.5 * (1 + erf(x / sqrt(2)))
        return phi((window_low - target) / s) + (1 - phi((window_high - target) / s))
    lo, hi = 1e-6, 1.0
    for _ in range(80):
        mid = (lo + hi) / 2
        p_all = (1 - p_out(mid)) ** n
        if p_all > 0.5:
            lo = mid
        else:
            hi = mid
    return lo


def variation_sweep() -> None:
    print("\n=== D: print variation (Gaussian on 0.45 N nominal, window 0.30-0.80 N) ===")
    be = variation_break_even()
    print(f"break-even sigma fraction for P(all 6400 good) > 0.5: {be*100:.2f}%")
    for s in (0.02, 0.03, 0.05, 0.10, 0.15, 0.20):
        sf = s
        from math import erf, sqrt
        def phi(x: float) -> float:
            return 0.5 * (1 + erf(x / sqrt(2)))
        sig = 0.45 * sf
        p_out = phi((0.30 - 0.45) / sig) + (1 - phi((0.80 - 0.45) / sig))
        p_all = (1 - p_out) ** CELLS
        print(f"  sigma={sf*100:4.1f}% ({sig:.3f} N): P(all good)={p_all:.2e} "
              f"({'ok' if p_all > 0.5 else 'FAIL'})")
    print("  mitigation: per-cell calibration/test is economically impossible at")
    print("  6400 cells; a GLOBAL enabling mechanism (shared stroke) must not rely")
    print("  on tight per-part force windows. Design margin, not sorting.")


def mask_break_even(channels: int = 80, holes: int = 12800,
                    visible_s: float = 30.0) -> float:
    """Required per-step time for an 80-channel writer to write within budget."""
    return visible_s * channels / holes


def mask_sweep() -> None:
    print("\n=== C: mask programming inside the visible 30 s ===")
    be = mask_break_even()
    print(f"80 channels, {12800} hole/set ops: required step time "
          f"<= {be*1000:.1f} ms/step")
    for ch in (80, 200, 500, 12800):
        t = 12800 / ch * 0.35
        print(f"  {ch:5d} channels -> {t:7.1f} s "
              f"({'ok' if t < 30 else 'FAIL'})")
    print("  conclusion: within-budget writing needs ~500+ simultaneous channels")
    print("  or a double-buffered off-line writer. This is the S1/S2 core trade.")


def main() -> None:
    force_sweep()
    variation_sweep()
    mask_sweep()


if __name__ == "__main__":
    main()
