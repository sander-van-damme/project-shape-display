#!/usr/bin/env python3
"""End-to-end timing and transaction budget for S1 and S2.

Arithmetic with stated assumptions. Exposes every term rather than hiding a
"selector" behind a word. Produces pass/fail against the strict < 30.0 s cap.

S1 (broadcast threshold ratchet): four 10 mm global strokes advance only the
columns whose target >= threshold_k. A ratchet stores height; a pawl holds load.

S2 (swappable planar-memory tiles): a shared lift reads a set of perforated
first-stop planes per tile. Tile-local memory can be exchanged/rewritten while
other tiles stay loaded.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict, field

PITCH_MM = 5.08
N = 80
CELLS = N * N
DEADLINE_S = 30.0
LEVELS = 5
STROKES = LEVELS - 1  # four binary decode strokes


@dataclass
class S1Timing:
    stroke_mm: float = 10.0
    stroke_time_s: float = 0.45          # one 10 mm platen stroke, rest to rest
    stroke_settle_s: float = 0.10
    gate_switching_s: float = 0.30       # swap mask layer / set interlocks per stroke
    global_reset_s: float = 1.20         # release all ratchets + return to datum
    mask_frame_swap_s: float = 0.0       # 0 if reusable shutters, else per-map media
    verify_s: float = 0.60               # post-write height sanity, not per-cell
    controller_s: float = 0.10
    regional_overhead_s: float = 0.80    # lock/unlock a tile bank; not the whole board

    def full_map(self) -> dict[str, float]:
        terms: dict[str, float] = {}
        terms["reset_and_datum"] = self.global_reset_s
        for k in range(STROKES):
            terms[f"stroke_{k + 1}_gate"] = self.gate_switching_s
            terms[f"stroke_{k + 1}_lift"] = self.stroke_time_s + self.stroke_settle_s
        terms["verify"] = self.verify_s
        terms["controller"] = self.controller_s
        total = sum(terms.values())
        return {**terms, "total_s": total, "deadline_s": DEADLINE_S,
                "pass": total < DEADLINE_S, "margin_s": DEADLINE_S - total}

    def regional(self, tiles: int = 1) -> dict[str, float]:
        """One tile replayed through the same four threshold strokes."""
        per_tile = self.regional_overhead_s + STROKES * (
            self.gate_switching_s + self.stroke_time_s + self.stroke_settle_s
        )
        total = per_tile * tiles
        return {"tiles": tiles, "total_s": total, "deadline_s": DEADLINE_S,
                "pass": total < DEADLINE_S, "margin_s": DEADLINE_S - total}


@dataclass
class S2Timing:
    tile_cells: int = 10
    tiles_axis: int = 8
    lift_mm: float = 41.0
    lift_speed_mm_s: float = 60.0
    lift_accel_mm_s2: float = 300.0
    settle_s: float = 0.40
    clear_all_s: float = 0.0             # derived
    # full-map read: all tiles lifted together on the shared platen
    full_lift_s: float = 0.0
    verify_s: float = 0.60
    controller_s: float = 0.10
    # regional: one tile cleared/re-read while others stay loaded
    tile_isolation_s: float = 0.50       # engage clutch / seat dock
    tile_swap_s: float = 0.0             # exchange medium if not rewrite-in-place
    rewrite_in_place_s: float = 0.0      # off-line writer time, hidden by double buffer
    lower_s: float = 0.0

    def _trapezoid_s(self, dist_mm: float, v: float, a: float) -> float:
        t_acc = v / a
        d_acc = 0.5 * a * t_acc * t_acc
        if 2 * d_acc >= dist_mm:
            return 2 * (dist_mm / a) ** 0.5
        return 2 * t_acc + (dist_mm - 2 * d_acc) / v

    def full_map(self) -> dict[str, float]:
        lift = self._trapezoid_s(self.lift_mm, self.lift_speed_mm_s, self.lift_accel_mm_s2)
        terms = {
            "lift_clear": lift,
            "settle_onto_stops": self.settle_s,
            "verify": self.verify_s,
            "controller": self.controller_s,
        }
        total = sum(terms.values())
        return {**terms, "total_s": total, "deadline_s": DEADLINE_S,
                "pass": total < DEADLINE_S, "margin_s": DEADLINE_S - total}

    def regional(self, tiles: int = 1) -> dict[str, float]:
        lift = self._trapezoid_s(self.lift_mm, self.lift_speed_mm_s, self.lift_accel_mm_s2)
        per_tile = (
            self.tile_isolation_s + lift + self.settle_s + self.rewrite_in_place_s
        )
        total = per_tile * tiles
        return {"tiles": tiles, "total_s": total, "deadline_s": DEADLINE_S,
                "pass": total < DEADLINE_S, "margin_s": DEADLINE_S - total,
                "note": "rewrite_in_place_s excludes off-line writer time (double buffer)"}


def full_map_bits() -> float:
    import math
    return CELLS * math.log2(LEVELS)


def mask_writer_throughput() -> dict[str, float]:
    """How fast must ANY mask writer be to fit S1 in-budget?"""
    # If media must be written during the visible transition, it eats the budget.
    s1 = S1Timing().full_map()
    s2 = S2Timing().full_map()
    return {
        "bits_full_map": full_map_bits(),
        "s1_visible_budget_s": DEADLINE_S,
        "s1_terms_excl_media_s": s1["total_s"],
        "s2_visible_read_s": s2["total_s"],
    }


def main() -> None:
    print("=== S1 full-map ===")
    print(json.dumps(S1Timing().full_map(), indent=2))
    print("=== S1 regional ===")
    print(json.dumps(S1Timing().regional(1), indent=2))
    print("=== S2 full-map ===")
    print(json.dumps(S2Timing().full_map(), indent=2))
    print("=== S2 regional ===")
    print(json.dumps(S2Timing().regional(1), indent=2))
    print("=== info budget ===")
    print(json.dumps(mask_writer_throughput(), indent=2))


if __name__ == "__main__":
    main()
