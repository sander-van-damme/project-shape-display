"""Reproducible analytical screen for the DES-004 successor; no physical validation."""

from __future__ import annotations

CELLS = 80 * 80
HEADS = 8
PITCH_MM = 5.08
TRAVERSE_MM_S = 1000.0
RAMP_S = 1.0
VERIFY_S = 5.864
FIXED_S = 3.0 + 0.05 + 1.5
RETRY_S = 1.3472
INCREMENT_MS = (2.0, 4.0, 5.0, 5.2)


def rotary_cycle(increment_ms: float) -> dict[str, float | bool]:
    """Worst-case four-detent write plus DES-003 verification/retry allowances."""
    traverse_ms = 1000.0 * PITCH_MM / TRAVERSE_MM_S
    actuation_ms = 4.0 * increment_ms
    per_cell_ms = max(traverse_ms, actuation_ms) + 1.0
    write_s = CELLS / HEADS * per_cell_ms / 1000.0 + RAMP_S
    total_s = write_s + VERIFY_S + FIXED_S + RETRY_S
    return {
        "increment_ms": increment_ms,
        "traverse_ms": traverse_ms,
        "per_cell_ms": per_cell_ms,
        "write_s": write_s,
        "total_s": total_s,
        "margin_s": 30.0 - total_s,
        "clears_30s": total_s < 30.0,
    }


def main() -> None:
    print("DES-004 five-level rotary bound; calculation only")
    print(f"cells={CELLS} heads={HEADS} pitch_mm={PITCH_MM} traverse_mm_s={TRAVERSE_MM_S}")
    for increment_ms in INCREMENT_MS:
        print(rotary_cycle(increment_ms))
    assert rotary_cycle(2.0)["total_s"] == 19.9612
    assert rotary_cycle(5.0)["clears_30s"]
    assert not rotary_cycle(5.2)["clears_30s"]


if __name__ == "__main__":
    main()
