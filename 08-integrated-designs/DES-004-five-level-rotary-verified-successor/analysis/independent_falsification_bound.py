"""Independent checks for DES-004's stated timing and reliability bounds."""

from __future__ import annotations

import math

CELLS = 80 * 80
HEADS = 8
TRAVERSE_MS = 5.08
VERIFY_S = 5.864
FIXED_S = 3.0 + 0.05 + 1.5
RETRY_1PCT_S = 1.3472
TIME_GATE_S = 30.0


def total_s(detent_ms: float, retry_s: float = RETRY_1PCT_S) -> float:
    """Recompute the DES-004 equation without importing its implementation."""
    per_cell_ms = max(TRAVERSE_MS, 4.0 * detent_ms) + 1.0
    write_s = (CELLS / HEADS) * per_cell_ms / 1000.0 + 1.0
    return write_s + VERIFY_S + FIXED_S + retry_s


def retry_s(first_try_miss: float) -> float:
    expected = CELLS * first_try_miss
    return expected * (0.020 + 0.00105)


def main() -> None:
    threshold_ms = (TIME_GATE_S - total_s(5.0) + 3.2 * 5.0) / 3.2
    # Equivalent direct solution for the linear region: total=13.5612+3.2*d.
    threshold_ms = (30.0 - 13.5612) / 3.2
    q_map = 1.0 - 0.99 ** (1.0 / CELLS)
    print(f"d=5.0 ms total={total_s(5.0):.4f} s")
    print(f"d=5.2 ms total={total_s(5.2):.4f} s")
    print(f"detent threshold={threshold_ms:.6f} ms")
    print(f"5% miss retry={retry_s(0.05):.4f} s")
    print(f"5.0 ms + 5% miss total={total_s(5.0, retry_s(0.05)):.4f} s")
    print(f"map-yield per-cell error limit={q_map:.9e}")
    assert abs(total_s(5.0) - 29.5612) < 1e-9
    assert abs(total_s(5.2) - 30.2012) < 1e-9
    assert abs(threshold_ms - 5.137125) < 1e-6
    assert total_s(5.0, retry_s(0.05)) > TIME_GATE_S
    assert q_map < 1.6e-6


if __name__ == "__main__":
    main()
