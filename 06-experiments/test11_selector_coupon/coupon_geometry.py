#!/usr/bin/env python3
"""Test11 selector-fan-out coupon geometry (S3/S4 shared-drive family).

Pure-stdlib analytical model of a *printable* per-column selector at final
5.08 mm pitch.  It does NOT replace CAD or a print; it answers the cheapest
questions first so a bad idea dies before an STL is sliced:

  * Can a sliding-gate latch + a driving pawl + a drive bar physically share the
    row band beside a load-bearing 4.68 mm column at 5.08 mm pitch?
  * What is the smallest shared-stroke fraction of 40 mm that can program five
    levels (and therefore how few shared strokes are needed)?
  * What is the *actual* tooth overlap, from geometry, so the retaining-face
    abuse gate is not a guess?
  * How hard does the shared drive have to push (force partition)?
  * Can a rotary-solenoid driven gate survive a one-per-column `d`-line
    multiplexed bus: how many columns can be addressed in the 0.4-0.6 s dwell?

Every number is a CALCULATION from stated assumptions.  Nothing here is
measured.  The variables named in ``A_*`` are assumptions; they are the exact
things the printed coupon is meant to falsify.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict

# ---------------------------------------------------------------- fixed design
PITCH = 5.08          # mm, r=2.54 → 4 cells per 1" D&D square
BODY = 4.68           # mm, Test09 column body width
CLEAR = 0.10          # mm per side body-to-channel clearance (Test09 nominal)
CHANNEL = BODY + 2 * CLEAR          # 4.88 mm
WALL_TOTAL = PITCH - CHANNEL        # 0.20 mm split between adjacent cells

STROKE = 40.0         # mm usable travel
LEVELS = 5            # 0..4
LEVEL_PITCH = STROKE / (LEVELS - 1)  # 10.0 mm
TOOTH_PITCH = LEVEL_PITCH            # one tooth per level (Test07 scheme)

# ------------------------------------------------- assumptions (falsifiable)
A_GATE_WIDTH = 0.50    # mm gate finger width across the drive-bar channel
A_GATE_THICK = 1.20    # mm gate finger thickness (the thin blade dimension)
A_TOOTH_PROT = 1.20    # mm latch tooth protrusion from column face
A_TOOTH_LAND = 2.50    # mm vertical support land per tooth
A_GATE_OVERLAP = 0.90  # mm intended gate/latch overlap when engaged (= engagement)
A_BAR_THICK = 1.20     # mm drive-bar thickness
A_RECESS = 0.40        # mm tooth-tip recess below column face
A_FACTOR = 1.8         # drive force = A_FACTOR * sum(retaining face load)
A_ABUSE_LOAD = 5.0     # N, Test09 Stage-B 5 N abuse gate
A_SHARED_STROKE = 10.0 # mm travel of the common stroke (0.25 * 40)
A_PRINT_WALL_MIN = 0.40  # mm minimum reliable printed wall (0.4 mm nozzle, 0.12 mm)
A_MOTOR_TORQUE = 0.4e-3  # N m, sourced 8 mm PM stepper holding torque (Test09 M1)
A_MOTOR_ARM = 0.75      # mm effective gate/gate-crank arm
A_COLS_PER_DRIVE = 80   # columns sharing one drive-gear train (one row)
A_SOLENOID_CURRENT = 0.09  # A per rotary-solenoid gate while energised
A_SOLENOID_PRICE = 0.40    # USD speculative custom rotary solenoid + driver


@dataclass
class RowBand:
    """Pitch-direction (Y) budget of one row band.

    The drive bar and the electronic gate live in the inter-column wall band in
    Y, one per column.  For that to be a straight channel across the row, the
    gate stroke must equal the row pitch.  At 5.08 mm pitch that also forces a
    rotary rather than a linear gate.
    """
    pitch: float
    body: float
    clear: float
    gate_width: float
    gate_stroke_required: float
    gate_length: float          # radial extent of the one-blade gate
    rotor_radius: float         # commanded radius off which the blade extends
    cell_radius: float
    gate_clearance_to_neighbour: float
    max_contiguous_gate: float  # one blade only; symmetric rotor = half pitch

    @property
    def band(self) -> float:
        return self.pitch - self.body - 2 * self.clear

    @property
    def rotor_plus_blade(self) -> float:
        return self.rotor_radius + self.gate_length

    @property
    def must_configure_rotary(self) -> bool:
        return self.gate_stroke_required > self.band


def row_band() -> RowBand:
    gate_stroke = PITCH            # straight continuous d-line channel requires this
    gate_len = 1.20                # one blade is this long (radial)
    cell_radius = BODY / 2 + CLEAR             # 2.44 mm
    # Commanded radius is the cell centerline; one blade reaches outward.
    rotor_radius = PITCH / 2                   # 2.54 mm
    # As the blade crosses the inter-cell boundary it reaches into the neighbour
    # half-plane: clearance = pitch/2 - cell_radius - gate_length.
    clearance = (PITCH / 2) - cell_radius - gate_len
    return RowBand(
        pitch=PITCH, body=BODY, clear=CLEAR, gate_width=A_GATE_WIDTH,
        gate_stroke_required=gate_stroke, gate_length=gate_len,
        rotor_radius=rotor_radius, cell_radius=cell_radius,
        gate_clearance_to_neighbour=clearance,
        max_contiguous_gate=PITCH / 2,
    )


def gate_stroke_band() -> dict:
    """Can a LINEAR sliding gate survive at this pitch?

    A straight continuous gate-slot channel across a row requires the gate
    stroke to span the full row pitch (5.08 mm).  It cannot: only a 0.20 mm
    inter-cell band is free, and a printable slot wall is ~0.40 mm.  So the
    gate must either (a) rotary/blade-shaped (Test07's finger), or (b) the
    centre-to-centre pitch must grow, or (c) the body must shrink.
    """
    slot_wall = 0.40
    band = PITCH - BODY - 2 * CLEAR
    gate_slot = A_GATE_WIDTH + 0.30
    needed = gate_slot + 2 * slot_wall
    return {
        "inter_cell_band_mm": band,
        "linear_gate_stroke_required_mm": PITCH,
        "printable_slot_plus_walls_mm": needed,
        "blocked": needed > band,
        "narrow_body_band_if_clearance_005_mm": PITCH - 4.78,
        "required_printed_wall_min_mm": A_PRINT_WALL_MIN,
        "verdict": (
            "LINEAR gate blocked: slot+walls %.2f mm > %.2f mm band "
            "(min printable wall %.2f mm needs %.2f mm alone)"
            % (needed, band, A_PRINT_WALL_MIN, 2 * A_PRINT_WALL_MIN)
        ),
    }


def radial_budget() -> dict:
    rb = row_band()
    return {
        "band_mm": rb.band,
        "gate_stroke_required_mm": rb.gate_stroke_required,
        "band_exceeds_gate_stroke": rb.must_configure_rotary,
        "gate_blade_length_mm": rb.gate_length,
        "cell_radius_mm": rb.cell_radius,
        "rotor_radius_mm": rb.rotor_radius,
        "neighbour_clearance_limit_mm": PITCH / 2 - rb.cell_radius,
        "clearance_to_neighbour_mm": rb.gate_clearance_to_neighbour,
        "verdict": (
            "LINEAR gate blocked: stroke %.2f mm > %.2f mm band. Rotary gate "
            "fits with %.2f mm radial clearance, but the blade crosses the "
            "inter-cell boundary by %.2f mm"
            % (rb.gate_stroke_required, rb.band,
               rb.gate_clearance_to_neighbour, rb.gate_length - 0.10)
        ),
    }


def shared_stroke_partition() -> dict:
    """Smallest shared stroke that can program all LEVELS independent of count.

    A driving pawl engages a latch tooth once per shared stroke and advances it
    one tooth; the actuator can dwell on any subset per stroke.  With one tooth
    per level the number of strokes equals the number of levels, but the shared
    stroke is only ONE tooth pitch, not 40 mm.
    """
    strokes_needed = LEVELS - 1
    stroke_total = strokes_needed * TOOTH_PITCH
    return {
        "levels": LEVELS,
        "level_pitch_mm": LEVEL_PITCH,
        "shared_stroke_mm": A_SHARED_STROKE,
        "strokes_needed_to_reach_top": strokes_needed,
        "minimum_stroke_if_10mm": A_SHARED_STROKE,
        "fraction_of_40mm": A_SHARED_STROKE / STROKE,
        "if_6_4mm_stroke_strokes_needed": -(-STROKE // A_SHARED_STROKE),
        "note": "shared stroke = one tooth pitch; independent of column count",
        "unresolved": "printed tooth pitch must equal or exceed the platen stroke",
    }


def tooth_overlap() -> dict:
    """Actual engaged overlap = blade length - recess (NOT the intended 0.9 mm)."""
    actual = A_GATE_THICK - A_RECESS
    support = A_TOOTH_PROT        # latch tooth horizontal protrusion engaged
    return {
        "intended_overlap_mm": A_GATE_OVERLAP,
        "blade_thickness_mm": A_GATE_THICK,
        "tooth_tip_recess_mm": A_RECESS,
        "actual_blade_overlap_mm": actual,
        "latch_tooth_protrusion_mm": A_TOOTH_PROT,
        "effective_shear_overlap_mm": min(actual, support),
        "overlap_shortfall_vs_intent_mm": A_GATE_OVERLAP - actual,
        "warning": "small recess consumes almost all intended overlap",
    }


def retaining_face_abuse() -> dict:
    """Normal force and shear on the engaged latch tooth under the 5 N abuse gate."""
    load = A_ABUSE_LOAD
    # Test07 sawtooth: the flat face carries vertical load; a shallow ramp angle
    # pushes the gate sideways (release direction).  These are the abuse cases.
    return {
        "abuse_load_n": load,
        "vertical_support_load_n_per_tooth": load,
        "shear_area_mm2": A_GATE_THICK * A_GATE_WIDTH,
        "avg_shear_stress_mpa": load / (A_GATE_THICK * A_GATE_WIDTH),
        "note": "PLA shear yield ~ 30-40 MPa; margin needs a measured coupon",
    }


def force_partition(columns: int = A_COLS_PER_DRIVE) -> dict:
    load_each = 10.0e-3  # N guide drag per column (Test09 illustrative)
    return {
        "columns_per_drive": columns,
        "drag_per_column_n": load_each,
        "sum_drag_n": columns * load_each,
        "participation_assumed_n": 4.0,
        "design_force_n": A_FACTOR * 4.0,
        "note": "advance force is summed drag over participating columns only",
    }


def gate_bus(columns: int = A_COLS_PER_DRIVE) -> dict:
    """One-per-column rotary solenoid on a 2-wire commanded `d` bus.

    Worst time to address K of N columns, energise and mechanically toggle each:
    t = K*(K/N)*tau_rot + K*(K-1)*tau_cmd + K*t_write  (electrical settling).
    """
    tau_rot = 5.0e-3   # s, rotary toggle; must be <= measurable print resolution
    tau_cmd = 5.0e-5   # s, ~50 us addressed pulse
    k = columns
    t_rot = k * (k / columns) * tau_rot
    t_cmd = k * (k - 1) * tau_cmd
    t_write = k * 0.0
    total = t_rot + t_cmd
    current = k * A_SOLENOID_CURRENT
    return {
        "columns": columns,
        "rotary_toggle_s": tau_rot,
        "command_pulse_s": tau_cmd,
        "worst_subset_rotary_time_s": round(t_rot, 4),
        "worst_subset_command_time_s": round(t_cmd, 4),
        "worst_total_s": round(total, 4),
        "budget_dwell_s": 0.60,
        "fits_dwell": total <= 0.60,
        "simultaneous_current_a": current,
        "solenoid_price_usd": A_SOLENOID_PRICE,
        "gate_cost_full_head_400_usd": 400 * A_SOLENOID_PRICE,
        "gate_cost_full_board_6400_usd": 6400 * A_SOLENOID_PRICE,
        "note": (
            "solenoid must toggle the gate in %.1f ms; that is a print-and-measure "
            "gate, not a bought grade" % (tau_rot * 1e3)
        ),
    }


def main() -> None:
    result = {
        "pitch_mm": PITCH,
        "levels": LEVELS,
        "row_band": asdict(row_band()) | {"band_mm": row_band().band},
        "gate_stroke_band": gate_stroke_band(),
        "radial_budget": radial_budget(),
        "shared_stroke": shared_stroke_partition(),
        "tooth_overlap": tooth_overlap(),
        "retaining_face_abuse": retaining_face_abuse(),
        "force_partition": force_partition(),
        "gate_bus": gate_bus(),
        "assumptions": {k: v for k, v in globals().items() if k.startswith("A_")},
    }
    result["row_band"]["band_mm"] = row_band().band
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
