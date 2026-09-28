#!/usr/bin/env python3
"""Geometry and density bounds for the S1 broadcast-threshold ratchet.

This is analytic geometry + arithmetic. It is NOT a mechanism simulation and
NOT physical validation. Every number is a stated assumption or a derived
bound, produced so a cheap coupon can reject the architecture before CAD/BOM.

Reference scale (see 02-design-criteria):
  pitch P = 5.08 mm, 80x80 = 6400 cells, travel 40 mm, 5 levels (0/10/20/30/40).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict

# ---- fixed project scale ---------------------------------------------------
PITCH_MM = 5.08
N = 80
CELLS = N * N
LEVELS = 5
STEP_MM = 10.0
TRAVEL_MM = STEP_MM * (LEVELS - 1)

# ---- S1 mechanism assumptions (hypothesis, not measured) -------------------
# Per-cell moving column.
COLUMN_TOP_MM = 4.72          # square visible cap, leaves 0.36 mm total top gap
COLUMN_WALL_MM = 0.60         # printed shell for a 40 mm tall column
COLUMN_MASS_G = 1.6           # estimated from solid/relieved PLA at 1.24 g/cm3

# Rack: 5 pockets at 10 mm vertical spacing on the column's rear face.
RACK_TOOTH_MM = 2.0           # vertical pocket pitch used for the pawl, NOT 10 mm
RACK_POCKET_DEPTH_MM = 1.2
RACK_POCKET_WIDTH_MM = 3.2    # across the 4.72 mm face, leaves 0.76 mm side rails
RACK_POCKET_UNDERCUT_DEG = 8  # pocket roof angled to give one-way holding

# Pawl: printable cantilever with a wedge toe that drops into a pocket.
PAWL_STEM_MM = 0.80
PAWL_THICKNESS_MM = 0.60
PAWL_LENGTH_MM = 5.0          # free cantilever length
PAWL_DEFLECTION_MM = 0.35     # toe must retract > pocket depth to clear
PAWL_WEDGE_LEAD_DEG = 30      # release/advance ramp angle

# Threshold gate: a thin sliding bar per cell, actuated by two planar mask
# plates. Bar travels ~1.2 mm between "blocked" and "armed".
GATE_BAR_W_MM = 3.0
GATE_BAR_T_MM = 0.50
GATE_TRAVEL_MM = 1.20
GATE_CLEARANCE_PER_SIDE_MM = 0.075
MASK_PLATE_T_MM = 0.30
MASK_LAYERS = LEVELS - 1      # four unary threshold planes


def column_gap_mm() -> float:
    return PITCH_MM - COLUMN_TOP_MM


def pitch_breakdown() -> dict[str, float]:
    """Explain where the 5.08 mm goes, per cell, in the moving column zone."""
    gap = column_gap_mm()
    return {
        "pitch_mm": PITCH_MM,
        "column_cap_mm": COLUMN_TOP_MM,
        "total_top_gap_mm": gap,
        "gap_per_side_mm": gap / 2,
    }


def gate_clearance_ok() -> tuple[bool, float]:
    """Can a sliding gate bar + its guides fit across the 5.08 mm cell?"""
    used = GATE_BAR_W_MM + 2 * GATE_CLEARANCE_PER_SIDE_MM
    return used <= PITCH_MM, PITCH_MM - used


def pawl_force_n(k_spring_n_per_mm: float, detent_hold_n: float) -> dict[str, float]:
    """Cantilever release force to push the pawl toe out of a rack pocket.

    F = deflection * k. The spring constant is a stated printable-cantilever
    assumption; the pocket shear must be overcome in addition to pure bending
    because the toe sits under a loaded column.
    """
    bending = PAWL_DEFLECTION_MM * k_spring_n_per_mm
    return {
        "bending_n": bending,
        "pocket_shear_n": detent_hold_n,
        "total_release_n": bending + detent_hold_n,
    }


@dataclass
class MaskBudget:
    """Planar mask geometry for the four unary threshold planes."""
    cells: int
    moving_holes_per_plane: int
    static_material_fraction: float

    def area_mm2(self) -> float:
        return self.cells * PITCH_MM * PITCH_MM


def mask_budget(fraction_armed: float = 0.5) -> MaskBudget:
    """A hole (or a shutter opening) must sit over every armed gate."""

    n = round(CELLS * fraction_armed)
    return MaskBudget(CELLS, n, 1.0 - fraction_armed)


def main() -> None:
    out = {
        "pitch_breakdown": pitch_breakdown(),
        "gate_clearance": {
            "fits": gate_clearance_ok()[0],
            "spare_mm": gate_clearance_ok()[1],
        },
        "pawl_release_example": pawl_force_n(0.35, 0.25),
        "mask_per_plane": asdict(mask_budget()),
        "active_width_mm": N * PITCH_MM,
        "mask_decision_count": CELLS * (LEVELS - 1),
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
