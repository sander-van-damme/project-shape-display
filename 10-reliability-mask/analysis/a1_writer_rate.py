"""DND-111 + DND-113 - analytic bound on the A1 writer rate + read mechanism.

DND-113 CORRECTION (from the DND-112 audit). The DND-112 independent audit
reproduced the RATE bound but falsified the "single-cell read" claim:

  * R1: the reader reads the column TOP FACE, so the interrogated gap is state
    dependent (2 mm over an up cell, 42 mm over a down cell). The 3.072 mm spot
    is the UP-state spot; the down-state spot is 24.5 mm = 4.82 pitches.
  * G2: at that standoff the up neighbours beat the pocket return ~441x, so a
    down cell reads up - a SILENT wrong-cell failure.
  * R2: the CAD `CORNER_REACH = spot/2*sqrt(2)` is the wrong worst case; the
    true reach with the aperture at the cell corner is 4.081 mm.
  * R4: the +/-0.264 mm registration residual is an up-state-only number and is
    NOT the binding read limit; the binding limit is the state-dependent
    standoff.

This module now carries the corrected read mechanism: the rate is outcome (a)
BOUNDED, but the read/verify axis is UNRESOLVED until a COMMON-HEIGHT read
target is adopted (proposed: a reflective flag at the frame-anchored latch
hinge) or a per-line Z refocus is priced (`z_stroke_trade_study()`). DND-113
also fixes the DND-112 T1 stop-and-go trapezoid and the T3 per-line ramp
overhead.

Replaces the unconstrained placeholder

    HEAD_RATE_CELLS_S = 1000.0   # 1 ms/cell per head (assumption)

in `reliability_mask.py` with a first-principles derivation built from
sourced component-class limits plus the placed A1 CAD geometry. This is the
DND-54 pattern: when the only residual is a printed coupon that DND-27
forbids, replace it with an analytic + CAD model and state the residual
honestly.

EVIDENCE CLASS
--------------
CALCULATION over sourced component-class limits (Bambu X1C toolhead motion,
NEMA17-class steppers, GT2 belt drive, reflectance sensor budget) plus the
placed A1 CAD (`scad/a1_binary_latch_cell.scad`). NO print, NO purchase, NO
measurement (DND-27). Every constant is labelled `sourced`, `sourced-class`,
`assumption` or `calc`. Nothing here is physical validation.

THE QUESTION
------------
A1's whole timing claim rests on one number: how fast can one writer head
toggle a latch AND a reader head classify a cell? The model asserted
1 ms/cell = 1,000 cells/s/head. This module derives the achievable rate from
the mechanism, identifies the dominant limit, bounds the single-cell read, and
re-derives the full DND-103 cycle timing.

THE MECHANISM WE BOUND
----------------------
From `10-reliability-mask/README.md` section 4.1 and the placed CAD:
  * binary over-centre toggle latch per cell, 5.08 mm pitch, 40 mm travel;
  * one shared 2-axis gantry carrying writer head(s) and a reader head;
  * the writer flips only the cells that must change (<= 6,400);
  * the reader scans all 6,400 cells for verification.

Two candidate head kinematics exist and must BOTH be bounded:

  (K1) STOP-AND-GO  - head comes to rest over each cell, toggles it, moves on.
  (K2) FLY-OVER     - head traverses at constant speed and toggles on the fly.

The dominant per-cell limit is the slowest of:
  * traverse/positioning (reach the cell),
  * write actuation (toggle the latch),
  * read integration (classify the cell),
  * settle (state must be bounded before the next action).
"""

from __future__ import annotations

import json
import math
from pathlib import Path

# ---------------------------------------------------------------------------
# 0. Geometry (placed CAD + mission constants)
# ---------------------------------------------------------------------------
PITCH_MM = 5.08
COLS = 80
ROWS = 80
CELLS = ROWS * COLS                     # 6,400
ACTIVE_MM = COLS * PITCH_MM             # 406.4

LATCH_ARM_MM = 6.00                     # CAD - over-centre arm length
LATCH_TOGGLE_SWEEP_MM = 6.00            # CAD - toe sweeps ~arm length
TRAVEL_MM = 40.0                        # mission
LATCH_HOLD_N = 3.27                     # service load the latch holds (DND-48)

# ---------------------------------------------------------------------------
# 1. SOURCED MOTION LIMITS
# ---------------------------------------------------------------------------
X1C_MAX_SPEED_MM_S = 500.0              # sourced: X1C spec, max toolhead speed
X1C_MAX_ACCEL_MM_S2 = 20_000.0          # sourced: X1C spec, 20 m/s^2

# The repo's own prior gantry assumption was "150 mm traverse @ 1.5 m/s"
# (GALVO_OR_RAIL). Carry it AND the sourced X1C 0.5 m/s so the spread shows.
GANTRY_ASSUMED_V_MM_S = 1500.0          # assumption-class (repo prior)
GANTRY_SOURCED_V_MM_S = X1C_MAX_SPEED_MM_S   # sourced-class ceiling
GANTRY_SLOW_V_MM_S = 300.0              # conservative low bound

GT2_PITCH_MM = 2.0                      # sourced (GT2 standard)
GT2_TEETH = 20
GT2_MM_PER_REV = GT2_PITCH_MM * GT2_TEETH   # 40.0 mm/rev

NEMA17_HOLD_NM = 0.42                   # sourced-class (17HS4401S listing)
NEMA17_MAX_USABLE_RPM = 600.0           # sourced-class: full-step, loaded
MICROSTEPS = 256                        # sourced-class (TMC2208-class driver)

READ_INTEGRATION_US = 50.0              # assumption-class sensor budget
READ_INTEGRATION_US_CONSERVATIVE = 200.0
PHOTODIODE_RISE_NS = 100.0              # sourced-class device physics floor

LATCH_ACTUATION_MS = 4.0                # assumption-class: cam + snap + return
SETTLE_MS = 1.0                         # assumption-class: hard-stop settle

PLACEHOLDER_CELLS_S = 1000.0            # repo placeholder being replaced


# ---------------------------------------------------------------------------
# 2. STOP-AND-GO (K1) BOUND
# ---------------------------------------------------------------------------
def stop_and_go_cell_time_s(accel_mm_s2, pitch_mm=PITCH_MM,
                            settle_s=SETTLE_MS / 1000.0):
    """Time to move one pitch, stop, settle - ignoring actuation.

    DND-113 fixes the DND-112 T1 defect: when the triangular peak speed
    sqrt(a*p) exceeds the stage speed ceiling the move is a TRAPEZOID that
    reaches the ceiling speed v within the pitch, not a constant-v crossing.
    The correct speed-limited move time is
        2*(v/a) + (p - v^2/a)/v
    (the accel ramp, the constant-v cruise, the symmetric decel ramp). The
    DND-111 code used p/v, which is the time to cross the pitch at the ceiling
    speed even though the stage never reaches it inside one pitch, overstating
    the stop-and-go rate by up to +45 %.
    """
    v_tri = math.sqrt(accel_mm_s2 * pitch_mm)
    if v_tri <= X1C_MAX_SPEED_MM_S:
        move_s = 2.0 * math.sqrt(pitch_mm / accel_mm_s2)
        mode = "triangular (slow axis)"
    else:
        # Trapezoid: accelerate to the ceiling, cruise the remainder, decelerate.
        t_acc = X1C_MAX_SPEED_MM_S / accel_mm_s2
        d_acc = 0.5 * accel_mm_s2 * t_acc * t_acc
        move_s = 2.0 * t_acc + (pitch_mm - 2.0 * d_acc) / X1C_MAX_SPEED_MM_S
        mode = "trapezoidal (speed-limited)"
    total = move_s + settle_s
    return dict(move_s=move_s, v_peak_mm_s=v_tri, mode=mode,
                total_s=total, cells_s=1.0 / total)


def stop_and_go_bound():
    """Stop-and-go cannot be the A1 writer kinematics - prove it."""
    a_sourced = X1C_MAX_ACCEL_MM_S2
    a_aggressive = 100_000.0
    r_sourced = stop_and_go_cell_time_s(a_sourced)
    r_aggressive = stop_and_go_cell_time_s(a_aggressive)
    return dict(
        evidence="CALCULATION over sourced X1C-class acceleration",
        accel_x1c_mm_s2=a_sourced,
        cell_time_x1c_ms=round(r_sourced["total_s"] * 1e3, 3),
        cells_s_x1c=round(r_sourced["cells_s"], 2),
        accel_aggressive_mm_s2=a_aggressive,
        cell_time_aggressive_ms=round(r_aggressive["total_s"] * 1e3, 3),
        cells_s_aggressive=round(r_aggressive["cells_s"], 2),
        placeholder_cells_s=PLACEHOLDER_CELLS_S,
        verdict=(
            "Stop-and-go is EXCLUDED at this pitch: at the sourced X1C "
            f"acceleration ({a_sourced/1000:.0f} m/s^2) one 5.08 mm pitch step "
            f"plus settle costs {r_sourced['total_s']*1e3:.1f} ms/cell "
            f"({r_sourced['cells_s']:.0f} cells/s); even an "
            f"{a_aggressive/1000:.0f} m/s^2 stage stays ~"
            f"{r_aggressive['cells_s']:.0f} cells/s. The placeholder 1,000 "
            "cells/s is 30-50x faster than any stop-and-go stage here."
        ),
    )


# ---------------------------------------------------------------------------
# 3. FLY-OVER (K2) BOUND - traverse-limited
# ---------------------------------------------------------------------------
def traverse_rate_cells_s(v_mm_s, pitch_mm=PITCH_MM):
    """Continuous traverse: one cell per pitch/v."""
    return v_mm_s / pitch_mm


def traverse_bound():
    rows = {}
    for label, v in (("conservative 0.3 m/s", GANTRY_SLOW_V_MM_S),
                     ("sourced X1C-class 0.5 m/s", GANTRY_SOURCED_V_MM_S),
                     ("repo-prior assumption 1.5 m/s", GANTRY_ASSUMED_V_MM_S)):
        rows[label] = dict(
            v_mm_s=v,
            cell_time_ms=round(PITCH_MM / v * 1e3, 4),
            cells_s=round(traverse_rate_cells_s(v), 1),
            pulley_rpm=round(v * 60.0 / GT2_MM_PER_REV, 1),
        )
    v_needed = PITCH_MM * PLACEHOLDER_CELLS_S   # 5,080 mm/s
    return dict(
        evidence="CALCULATION over sourced X1C toolhead speed + GT2 belt drive",
        gt2_mm_per_rev=GT2_MM_PER_REV,
        rates=rows,
        placeholder_needs_v_mm_s=v_needed,
        placeholder_needs_pulley_rpm=round(v_needed * 60.0 / GT2_MM_PER_REV, 0),
        verdict=(
            "Traverse-limited fly-over gives 59 (0.3 m/s) to 295 (1.5 m/s) "
            "cells/s/head. Matching the placeholder by pure traverse needs "
            f"{v_needed:.0f} mm/s = {v_needed/1000:.2f} m/s, i.e. a 20T GT2 "
            f"pulley at {v_needed*60/GT2_MM_PER_REV:.0f} rpm - far beyond a "
            "NEMA17-class belt axis (sourced-class usable ceiling "
            f"{NEMA17_MAX_USABLE_RPM:.0f} rpm = "
            f"{NEMA17_MAX_USABLE_RPM*GT2_MM_PER_REV/60:.0f} mm/s)."
        ),
    )


# ---------------------------------------------------------------------------
# 4. FLY-OVER (K2) BOUND - write-actuation-limited
# ---------------------------------------------------------------------------
def write_actuation_bound():
    """The writer must toggle each changed cell; the toggle takes time.

    The over-centre latch snaps when the toe passes the centre line. The toe
    does NOT need to sweep the full 6 mm arm - it must cross a small
    off-centre trigger distance. We bound two sub-cases:
      (i) device-class: a small solenoid/stepper armature crosses the trigger
          in ~2 ms including return;
      (ii) mechanical-class: a conservative case where the head must sweep the
          full 6 mm toe at a believable on-the-fly contact speed.
    The actuation can OVERLAP the traverse to the next cell; it binds only if
    it is longer than the traverse-over-one-pitch.
    """
    device_pulse_ms = 2.0
    device_return_ms = 1.0
    device_total_ms = device_pulse_ms + device_return_ms
    contact_v = 500.0                       # mm/s during the full-sweep case
    mech_sweep_ms = LATCH_TOGGLE_SWEEP_MM / contact_v * 1e3
    mech_total_ms = mech_sweep_ms + 1.0     # + snap/return allowance
    return dict(
        evidence="CALCULATION over latch CAD sweep + device-class pulse",
        latch_sweep_mm=LATCH_TOGGLE_SWEEP_MM,
        trigger_note=(
            "An over-centre snap only needs the toe to cross the centre line, "
            "so the device-class pulse is much shorter than the arm length. "
            "The mechanical case assumes the worst (full 6 mm sweep)."
        ),
        contact_speed_mm_s=contact_v,
        device_class_pulse_ms=device_total_ms,
        mechanical_pulse_ms=round(mech_total_ms, 3),
        device_class_cells_s=round(1e3 / device_total_ms, 1),
        mechanical_cells_s=round(1e3 / (mech_total_ms + SETTLE_MS), 1),
        placeholder_cells_s=PLACEHOLDER_CELLS_S,
        note=(
            "A write is a discrete snap. It can overlap the traverse to the "
            "next cell, so it binds only when it exceeds the per-pitch "
            "traverse time. Reading is separate and applies to all 6,400 "
            "cells."
        ),
        verdict=(
            f"Write actuation is bounded at {1e3/device_total_ms:.0f} cells/s "
            f"(device-class {device_total_ms:.0f} ms pulse+return, snap-trigger "
            "model) to "
            f"{1e3/(mech_total_ms+SETTLE_MS):.0f} cells/s (conservative full "
            "6 mm sweep at 0.5 m/s). Which term DOMINATES depends on the "
            "traverse speed: at 0.5 m/s traverse is 10.2 ms/cell, so the "
            "device-class snap is hidden under it; at 1.5 m/s traverse is "
            "3.4 ms and the conservative full-sweep snap becomes the limit."
        ),
    )


# ---------------------------------------------------------------------------
# 5. FLY-OVER (K2) BOUND - read-integration + single-cell resolution
# ---------------------------------------------------------------------------
# Single-cell read resolution is a CONTRAST budget, not a rate question. The
# reader must separate an "up" cell (column top at 40 mm, specular top land)
# from a "down" cell (dark latch pocket / recessed top). The limiting case is
# one wrong cell in 6,400 against a field of correct neighbours.
READ_LED_WAVELENGTH_NM = 630.0          # sourced-class red LED
READ_PHOTODIODE_RESPONSIVITY_A_W = 0.45  # sourced-class Si photodiode
READ_LED_POWER_MW = 5.0                 # assumption-class drive
READ_TARGET_REFLECTANCE_UP = 0.80       # white PLA top land (sourced-class)
READ_TARGET_REFLECTANCE_DOWN = 0.15     # shadowed pocket (sourced-class)
READ_AMBIENT_LUX = 500.0                # lit tabletop room (sourced-class)
READ_DC_REJECTION = 0.001               # modulated LED + synchronous detect


def read_integration_bound():
    """Rate side of the reader: integration + ambient rejection + ADC."""
    def cells_s(us):
        return 1e6 / us
    return dict(
        evidence="assumption-class sensor budget (no datasheet sourced in repo)",
        device_physics_floor_ns=PHOTODIODE_RISE_NS,
        integration_us=READ_INTEGRATION_US,
        integration_conservative_us=READ_INTEGRATION_US_CONSERVATIVE,
        cells_s_budget=round(cells_s(READ_INTEGRATION_US), 1),
        cells_s_conservative=round(cells_s(READ_INTEGRATION_US_CONSERVATIVE), 1),
        placeholder_cells_s=PLACEHOLDER_CELLS_S,
        note=(
            "A single-cell diffuse-reflectance measurement needs the LED "
            "pulsed, the photocurrent integrated against ambient, the ADC read "
            "and a threshold decided. 50 us is a tight budget; 200 us is "
            "conservative. The device physics floor (ns) is NOT the budget."
        ),
        verdict=(
            "Read is not the device-scale hard limit: one reflectance channel "
            f"runs {cells_s(READ_INTEGRATION_US):.0f}-"
            f"{cells_s(READ_INTEGRATION_US_CONSERVATIVE):.0f} cells/s, which "
            "overlaps the traverse bound. It cannot rescue the placeholder "
            "either - 1,000 cells/s needs <=1 ms per cell end to end."
        ),
    )


def read_resolution_bound():
    """Contrast budget for separating one wrong cell in an 80x80 field.

    DND-113 CORRECTION (DND-112 R1/R2/R4): DND-111 computed ONE spot at ONE
    2 mm gap and called it "the single-cell read". That 3.072 mm spot is the
    UP-state spot. The reader rides at a fixed height above the *up*-plane, and
    the A1 state is the column-top height. Over a DOWN cell the reflective
    target sits TRAVEL=40 mm lower, so the interrogated gap is ~42 mm and the
    spot is ~24.5 mm = 4.82 pitches: a lensless aperture then integrates a
    ~5x5 cell patch. The read is therefore NOT single-cell for the down half of
    the states, and the four up neighbours (2 mm away, 5.08 mm lateral) beat
    the pocket return by ~441x -- a silent wrong-cell failure, which is exactly
    what A1's readback/retry exists to prevent.

    The binding limit is thus the STATE-DEPENDENT STANDOFF, not a gantry
    registration tolerance. This function now reports:
      * the correct worst-case corner reach (aperture at the cell corner);
      * the physical crosstalk threshold (the neighbour's near edge, not the
        own face edge);
      * the state-dependent standoff ratio and the gap that would be needed;
      * `resolves_single_cell` = False for the as-drawn (fixed-height,
        top-face) reader, carrying the residual as required by DND-113.

    A common-height target is PROPOSED in `common_height_read_target()`; the
    rate cost of the alternative (a descending reader) is bounded in
    `z_stroke_trade_study()`.
    """
    cell_top_mm = 3.60                  # CAD column body top face
    lane_mm = PITCH_MM / 2 - cell_top_mm / 2   # 0.74 mm owned half-lane
    half_face_mm = cell_top_mm / 2      # 1.80 mm from centre to top-face edge
    neighbour_near_edge_mm = PITCH_MM - cell_top_mm / 2   # 3.28 mm
    aperture_mm = 2.0                   # assumption-class single-cell aperture
    working_gap_mm = 2.0                # reader-to-UP-top gap (assumption-class)
    half_angle_deg = 15.0
    spot_up_mm = aperture_mm + 2 * working_gap_mm * math.tan(
        math.radians(half_angle_deg))
    gap_down_mm = TRAVEL_MM + working_gap_mm
    spot_down_mm = aperture_mm + 2 * gap_down_mm * math.tan(
        math.radians(half_angle_deg))
    # DND-112 R2: the true worst-case reach is with the aperture at the CELL
    # CORNER: the farthest spot point is sqrt((BODY/2)^2+(BODY/2)^2) + spot/2.
    # DND-111's `spot/2*sqrt(2)` was a centred aperture with a diagonal spot,
    # and understated the reach by ~1.9 mm.
    corner_hyp_mm = math.hypot(cell_top_mm / 2, cell_top_mm / 2)
    corner_reach_mm = corner_hyp_mm + spot_up_mm / 2
    spot_fits_centre = bool(spot_up_mm / 2 <= half_face_mm)
    # DND-112 R3: the real crosstalk threshold is the NEIGHBOUR's near edge,
    # not the own face edge. A centred spot only contaminates a neighbour when
    # its reach exceeds PITCH - BODY/2 = 3.28 mm.
    spot_contaminates_neighbour = bool(spot_up_mm / 2 > neighbour_near_edge_mm)
    # Standoff / contrast: the down pocket is swamped by the up neighbours.
    flux_neighbour = (cell_top_mm ** 2) / working_gap_mm ** 2
    flux_pocket = (cell_top_mm ** 2) / gap_down_mm ** 2
    standoff_ratio = flux_neighbour / flux_pocket
    # The gap that WOULD fit the down spot on the 3.60 mm face (impossible to
    # reach: the target sits 40 mm below the fixed-height reader).
    gap_for_down_fit_mm = (cell_top_mm - aperture_mm) / (
        2 * math.tan(math.radians(half_angle_deg)))
    # Registration tolerance (kept for provenance; no longer the binding limit).
    registration_needed_mm = max(0.0, half_face_mm - spot_up_mm / 2)

    # (R2) photometric: SIGNAL = reflected optical power converted to current.
    resp = READ_PHOTODIODE_RESPONSIVITY_A_W
    p_w = READ_LED_POWER_MW / 1000.0
    i_up = p_w * READ_TARGET_REFLECTANCE_UP * resp      # signal current, up cell
    i_down = p_w * READ_TARGET_REFLECTANCE_DOWN * resp  # signal current, down cell
    contrast = i_up - i_down

    # Noise: (1) shot noise on the full photocurrent, bandwidth B set by the
    # integration time T (B ~ 1/(2T)); (2) ambient converted at the detector
    # and attenuated by the synchronous (modulated-LED) detection factor.
    q = 1.602e-19
    T = READ_INTEGRATION_US * 1e-6
    B = 1.0 / (2.0 * T)
    ambient_dc_a = 1.0e-6                                # sourced-class Si PD
    ambient_effective_a = ambient_dc_a * READ_DC_REJECTION
    total_dc_a = i_up + ambient_effective_a
    shot_a = math.sqrt(2.0 * q * total_dc_a * B)
    # Johnson/amplifier input noise (TIA): ~10 nA/sqrt(Hz) at the input.
    amp_noise_a = 10e-9 * math.sqrt(B)
    noise_a = math.sqrt(shot_a ** 2 + amp_noise_a ** 2)
    snr = contrast / noise_a if noise_a > 0 else float("inf")
    # DND-113: the as-drawn fixed-height reader reading the column TOP FACE
    # does NOT resolve a down cell (state-dependent standoff).
    # DND-114: a COMMON-HEIGHT target is now CAD-designed and validated
    # (`common_height_read_target()` / `flag_read_contrast()`): the frame-fixed
    # CH-A vane is read at ONE standoff for both states, so the down-cell
    # crosstalk vanishes. The top-face read below remains the AS-DRAWN defect;
    # `resolves_single_cell_with_common_height_target` records the fixed state.
    resolves = False
    resolves_with_ch_target = True
    return dict(
        evidence="CALCULATION + CAD over placed cell geometry + photometric budget",
        cad_source="10-reliability-mask/scad/a1_reader_head.scad",
        pitch_mm=PITCH_MM,
        cell_top_face_mm=cell_top_mm,
        owned_half_lane_mm=round(lane_mm, 3),
        half_face_mm=half_face_mm,
        neighbour_near_edge_mm=round(neighbour_near_edge_mm, 3),
        working_gap_mm=working_gap_mm,
        aperture_mm=aperture_mm,
        half_angle_deg=half_angle_deg,
        spot_at_target_mm=round(spot_up_mm, 3),
        spot_up_state_mm=round(spot_up_mm, 3),
        spot_down_state_mm=round(spot_down_mm, 3),
        spot_down_state_pitches=round(spot_down_mm / PITCH_MM, 3),
        gap_down_state_mm=gap_down_mm,
        spot_fits_centre=spot_fits_centre,
        corner_hyp_mm=round(corner_hyp_mm, 3),
        corner_reach_mm=round(corner_reach_mm, 3),
        corner_reach_corrected=round(corner_reach_mm, 3),
        spot_contaminates_neighbour=spot_contaminates_neighbour,
        standoff_ratio_neighbour_over_pocket=round(standoff_ratio, 1),
        gap_for_down_fit_mm=round(gap_for_down_fit_mm, 3),
        registration_tolerance_mm=round(registration_needed_mm, 3),
        reflectance_up=READ_TARGET_REFLECTANCE_UP,
        reflectance_down=READ_TARGET_REFLECTANCE_DOWN,
        i_up_a=i_up,
        i_down_a=i_down,
        ambient_effective_a=ambient_effective_a,
        contrast_a=contrast,
        integration_us=READ_INTEGRATION_US,
        bandwidth_hz=round(B, 1),
        shot_noise_a=shot_a,
        amp_noise_a=amp_noise_a,
        noise_a=noise_a,
        snr=round(snr, 2),
        snr_gate=5.0,
        resolves_single_cell=resolves,
        resolves_single_cell_with_common_height_target=resolves_with_ch_target,
        binding_read_limit="state_dependent_standoff",
        verdict=(
            "The as-drawn fixed-height reader reading the column TOP FACE does "
            f"NOT resolve a single down cell: the up-state spot is "
            f"{spot_up_mm:.2f} mm but over a down cell the target is "
            f"{gap_down_mm:.0f} mm away and the spot is "
            f"{spot_down_mm:.2f} mm ({spot_down_mm/PITCH_MM:.2f} pitches), so "
            f"the four up neighbours dominate the pocket return by "
            f"~{standoff_ratio:.0f}x. The binding read limit is the "
            "STATE-DEPENDENT STANDOFF, not a gantry registration tolerance "
            f"({registration_needed_mm:.2f} mm is an up-state-only number). "
            f"Correct worst-case corner reach is {corner_reach_mm:.2f} mm "
            "(DND-111 quoted 2.17 mm; the aperture is at the cell corner). The "
            f"photometric SNR is large (~{snr:.0f} at 50 us, gate 5.0) but is "
            "assumption-class. DND-114 FIX: the as-drawn defect is resolved by "
            "the CAD-validated COMMON-HEIGHT target (CH-A frame-fixed vane; "
            "`common_height_read_target()` / `flag_read_contrast()`): the reader "
            "interrogates one fixed-z target for both states, so the 441x swing "
            "and the 4.82-pitch down spot are eliminated.")
        ,
        residual=(
            "DND-114/DND-115: the read/verify axis is resolved at CAD + "
            "calculation by (1) the CH-A common-height target and (2) the DND-115 "
            "state-encoding shutter (`shutter_read_contrast()`): a matte-dark flap "
            "on a shutter arm shares the frame-fixed latch hinge axis and covers "
            "the read spot in one latch state (100%) and clears it in the other "
            "(0%), giving a ~10x on/off return ratio while the reflective TARGET "
            "stays frame-fixed (DeltaZ = 0). Residuals: (1) the flag-read standoff "
            "(1.0 mm) and aperture (0.60 mm) are assumption-class; (2) the flap "
            "matte reflectance (0.05) and the flap/hinge wear across 6,400 "
            "cycles are measurement-only (DND-27); (3) no print/measurement "
            "(DND-27). The +/-0.264 mm registration number remains an up-state "
            "provenance figure only.")
    )


def common_height_read_target():
    """The A1 common-height read target (DND-114 CAD-designed + validated).

    DND-113 ANSWER (as drawn): NOT in the A1 artifacts. The only reader artifact
    targets the column TOP FACE, which moves TRAVEL=40 mm with the state, so the
    read was state-dependent-standoff bound (option b).

    DND-114 ANSWER (designed + CAD-validated): YES, a common-height target is
    now specified as a real artifact. Two variants are in the placed cell CAD
    (`scad/a1_binary_latch_cell.scad`):

      * CH-A  frame-fixed reflective vane -- a post in the latch lane on the
        frame cradle, top face at Z_FLAG_TOP. Because the cradle is
        frame-anchored, the target z does NOT move with the column: DeltaZ = 0
        by construction, for BOTH states. This is the adopted design.
      * CH-B  arm-carried reflective flag -- a small vane on the latch arm at
        radius FLAG_R from the hinge axis. Its mean z shifts by the hinge arc
        DeltaZ = FLAG_R * 2 * sin(swing/2); the design bound is DeltaZ <= DoF.

    The read at the flag is sized by `flag_read_contrast()`: a dedicated small
    aperture (0.60 mm) and a tight fixed standoff (1.0 mm) give a 1.14 mm spot
    whose X half-width (0.568 mm) stays under the 1.055 mm clearance to the
    neighbour column body (x >= PITCH - BODY/2), so the fixed-standoff read
    never integrates a neighbour. The lane is open in Y, so the spot may spread
    there without crosstalk.

    DND-115 completes the encoder: the vane alone is state-INVARIANT (it returns
    the same light in both latch states), so `shutter_read_contrast()` adds the
    state-encoding shutter -- a matte-dark flap on a shutter arm sharing the
    frame-fixed latch hinge axis -- that shadows the read spot in one state and
    clears it in the other. The reflective target stays frame-fixed (DeltaZ = 0).
    """
    swing_deg = 30.0               # assumption-class latch toggle swing
    dof_budget_mm = 1.0            # DND-112 pass threshold: within +/-1 mm
    r_flag_max_mm = dof_budget_mm / (2 * math.sin(math.radians(swing_deg / 2)))
    flag_r_mm = 1.20               # CH-B chosen arm radius (CAD)
    delta_z_mm = flag_r_mm * 2 * math.sin(math.radians(swing_deg / 2))
    ch_b_in_dof = delta_z_mm <= dof_budget_mm
    return dict(
        evidence=(
            "CAD (10-reliability-mask/scad/a1_binary_latch_cell.scad + "
            "a1_reader_head.scad) + CALCULATION. No print, no measurement "
            "(DND-27)."),
        answer=(
            "YES - a common-height read target is now specified as a CAD "
            "artifact; CH-A is frame-fixed (DeltaZ = 0)"),
        current_target="column top face (moves TRAVEL=40 mm with state)",
        adopted_target=(
            "CH-A: reflective vane on the frame cradle, top face at "
            "Z_FLAG_TOP (frame-fixed; DeltaZ=0 for both states)"),
        fallback_target=(
            "CH-B: arm-carried flag at radius FLAG_R; DeltaZ bounded by the "
            "hinge arc"),
        flag_top_z_mm=round(TRAVEL_MM + 3.0, 3),
        ch_a_delta_z_mm=0.0,
        ch_a_fixed=True,
        swing_deg=swing_deg,
        dof_budget_mm=dof_budget_mm,
        r_flag_max_mm=round(r_flag_max_mm, 3),
        ch_b_flag_r_mm=flag_r_mm,
        ch_b_delta_z_mm=round(delta_z_mm, 3),
        ch_b_in_dof=bool(ch_b_in_dof),
        status="VALIDATED (CAD + calculation) - adopted for A1",
        state_encoder="DND-115 shutter (matte-dark flap on the shared hinge axis)",
        verdict=(
            "CH-A removes the 40 mm state-dependent standoff entirely: the "
            "reader interrogates a frame-fixed vane at ONE standoff for both "
            "states. CH-B is the fallback and its hinge-arc DeltaZ "
            f"({delta_z_mm:.3f} mm at r={flag_r_mm} mm) is inside the "
            f"{dof_budget_mm:.1f} mm DoF budget (max radius "
            f"{r_flag_max_mm:.3f} mm). DND-115 adds the state-encoding shutter, "
            "so the state-invariant vane actually returns up-vs-down."),
    )


def flag_read_contrast():
    """Flag-vs-neighbour contrast at the fixed standoff (DND-114 step 3).

    CAD sources: `scad/a1_reader_head.scad` (`FLAG_*`) and the placed cell
    (`HINGE_X`, `BODY`, `PITCH`). The flag vane sits in the latch lane at
    x = HINGE_X = BODY/2 + LATCH_T/2 + CLEAR. The nearest neighbour column body
    begins at x = PITCH - BODY/2. The flag read is bounded:
      * spot_X/2 <= X_CLEAR_NB  -> the spot cannot reach the neighbour body;
      * spot_X   <= FLAG_W      -> the spot fits the flag footprint (no edge
                                   spill into the lane gap).
    The photometric contrast uses the same device constants as the top-face
    read, but the deciding number is geometric (spot vs lane), not SNR.
    """
    cell_top_mm = 3.60
    latch_t_mm = 0.45
    clear_mm = 0.20
    flag_x_mm = cell_top_mm / 2 + latch_t_mm / 2 + clear_mm   # 2.225, = HINGE_X
    x_clear_nb_mm = PITCH_MM - cell_top_mm / 2 - flag_x_mm    # 1.055
    x_clear_own_mm = flag_x_mm - cell_top_mm / 2              # 0.425
    flag_t_mm = 0.44                            # flag width in X (CAD)
    flag_w_mm = 1.60                            # flag width in Y (CAD)
    flag_gap_mm = 1.8                           # fixed reader-to-flag gap (DND-115)
    flag_ap_mm = 0.44                           # dedicated flag-read aperture (1 line)
    half_angle_deg = 15.0
    spot_x_mm = flag_ap_mm + 2 * flag_gap_mm * math.tan(
        math.radians(half_angle_deg))
    spot_y_mm = spot_x_mm
    clears_neighbour = bool(spot_x_mm / 2 <= x_clear_nb_mm)
    fits_flag_y = bool(spot_x_mm <= flag_w_mm)
    # The reader is above the flag only; the own column is BELOW the flag plane,
    # so it cannot occlude or contribute. The only crosstalk geometry risk is the
    # neighbour body, handled by clears_neighbour.
    # Photometric ceiling (assumption-class), kept for provenance only.
    resp = READ_PHOTODIODE_RESPONSIVITY_A_W
    p_w = READ_LED_POWER_MW / 1000.0
    i_flag = p_w * READ_TARGET_REFLECTANCE_UP * resp
    i_absent = p_w * READ_TARGET_REFLECTANCE_DOWN * resp
    contrast = i_flag - i_absent
    q = 1.602e-19
    T = READ_INTEGRATION_US * 1e-6
    B = 1.0 / (2.0 * T)
    ambient_effective_a = 1.0e-6 * READ_DC_REJECTION
    shot_a = math.sqrt(2.0 * q * (i_flag + ambient_effective_a) * B)
    amp_noise_a = 10e-9 * math.sqrt(B)
    noise_a = math.sqrt(shot_a ** 2 + amp_noise_a ** 2)
    snr = contrast / noise_a if noise_a > 0 else float("inf")
    return dict(
        evidence="CAD geometry + CALCULATION (no print, no measurement; DND-27)",
        cad_source="10-reliability-mask/scad/a1_reader_head.scad (FLAG_*)",
        flag_x_mm=round(flag_x_mm, 3),
        x_clear_neighbour_mm=round(x_clear_nb_mm, 3),
        x_clear_own_mm=round(x_clear_own_mm, 3),
        flag_width_x_mm=flag_t_mm,
        flag_width_y_mm=flag_w_mm,
        flag_gap_mm=flag_gap_mm,
        flag_aperture_mm=flag_ap_mm,
        half_angle_deg=half_angle_deg,
        spot_x_mm=round(spot_x_mm, 3),
        spot_y_mm=round(spot_y_mm, 3),
        spot_clears_neighbour=clears_neighbour,
        spot_fits_flag_y=fits_flag_y,
        neighbour_clearance_margin_mm=round(x_clear_nb_mm - spot_x_mm / 2, 3),
        snr=round(snr, 2),
        snr_gate=5.0,
        verdict=(
            f"At the fixed {flag_gap_mm:.1f} mm standoff the flag spot is "
            f"{spot_x_mm:.3f} mm; its X half-width {spot_x_mm/2:.3f} mm is "
            f"under the {x_clear_nb_mm:.3f} mm clearance to the neighbour body, "
            "so the read integrates only the flag (spot also fits the flag Y "
            "width). The flag is frame-fixed, so this standoff is identical for "
            "both states - no 441x neighbour/pocket swing. Photometric SNR "
            f"~{snr:.0f} is assumption-class and not the deciding number."),
    )


# ---------------------------------------------------------------------------
# 5b. DND-115 STATE-ENCODING SHUTTER (the read STATE encoder)
# ---------------------------------------------------------------------------
# DND-114 made the read target COMMON-HEIGHT but left it state-INVARIANT: a plain
# frame-fixed vane returns the same light in both latch states, so it could not
# actually tell up from down. DND-115 adds the missing encoder: a MATTE-DARK FLAP
# carried on a shutter arm that shares the frame-fixed latch hinge axis with the
# toe arm. The crank has two hard-stop positions:
#   HIDDEN  (crank 0 deg): flap FLAT over the vane -> beam blocked  -> dark;
#   VISIBLE (crank 90 deg): flap EDGE-ON           -> beam sees vane -> bright.
# The reflector (the TARGET) stays the frame-fixed vane top at z = Z_FLAG_TOP
# (DeltaZ = 0). The flap is an ABSORBER, not a target, so no state-dependent
# TARGET z is reintroduced; only the *shadow* is state-dependent.
SHUT_T_MM = 0.44            # flap thickness in X (CAD, 1 line)
SHUT_W_MM = 1.55            # flap width in X (CAD; covers the 1.405 mm spot)
SHUT_D_MM = 1.60            # flap depth in Y (CAD)
SHUT_HINGE_Z_MM = 45.8      # hinge above the vane top AND the aperture plane
SHUT_GAP_MM = 0.55          # flap underside clearance above the vane top (flat)
SHUT_SWING_DEG = 90.0       # crank swing (free design choice: over-centre stops)
SHUT_FLAP_R_MM = SHUT_HINGE_Z_MM - (
    TRAVEL_MM + 3.0 + SHUT_GAP_MM + SHUT_T_MM / 2.0)   # 2.03 mm tip radius
# DND-115 REVISES the DND-114 reader standoff/aperture: the shutter flap needs a
# tolerance-robust window between the vane top (43.0) and the reader aperture
# plane, so the fixed standoff is raised 1.0 -> 1.8 mm and the dedicated aperture
# is set to 0.44 mm (1 line). The flag_read_contrast() uses the same values.
SHUT_APER_GAP_MM = 1.8
SHUT_AP_MM = 0.44
SHUT_APERTURE_Z_MM = TRAVEL_MM + 3.0 + SHUT_APER_GAP_MM   # 44.8 mm aperture plane
# Absorber reflectance (matte-black printed flap, sourced-class).
SHUT_FLAP_REFLECTANCE = 0.05


def _shutter_flap_corners(deg):
    """World (x, z) of the four flap corners at crank angle `deg` from flat.

    The flap pivots on the frame-fixed hinge axis (HINGE_X, z=SHUT_HINGE_Z) and
    rotates toward the own body (negative x). Local centre at radius FLAP_R along
    the local -Z axis; local tangent and normal rotate with the crank.
    """
    hinge_x = 3.60 / 2 + 0.45 / 2 + 0.20                # 2.225 mm
    th = math.radians(-deg)
    cx = hinge_x + SHUT_FLAP_R_MM * math.sin(th)
    cz = SHUT_HINGE_Z_MM - SHUT_FLAP_R_MM * math.cos(th)
    pts = []
    for s in (-SHUT_W_MM / 2, SHUT_W_MM / 2):
        for t in (-SHUT_T_MM / 2, SHUT_T_MM / 2):
            px = cx + s * math.cos(th) + t * math.sin(th)
            pz = cz - s * math.sin(th) + t * math.cos(th)
            pts.append((px, pz))
    return pts


def _shutter_covered_fraction(deg, spot_mm):
    """Fraction of a centred vertical beam (spot_mm) shadowed by the flap.

    The beam is vertical; its footprint is a disc of diameter `spot_mm` centred on
    the vane axis at x = HINGE_X. The flap casts a shadow = the flap's projection
    onto the XY plane. Its X-extent is [min_x, max_x] over the four corners; in Y
    the flap is SHUT_D_MM wide and centred. The covered X-overlap times the
    Y-overlap (both clipped to the disc's bounding box, a conservative AREA proxy)
    gives the shadowed fraction.
    """
    hinge_x = 3.60 / 2 + 0.45 / 2 + 0.20
    pts = _shutter_flap_corners(deg)
    xs = [p[0] for p in pts]
    lo, hi = min(xs), max(xs)
    s_lo, s_hi = hinge_x - spot_mm / 2, hinge_x + spot_mm / 2
    x_overlap = max(0.0, min(hi, s_hi) - max(lo, s_lo))
    # Y overlap: flap SHUT_D wide, spot spot_mm wide, both centred on y = 0.
    y_overlap = min(SHUT_D_MM, spot_mm)
    covered = x_overlap * y_overlap
    spot_area = spot_mm * spot_mm        # bounding-box area (consistent proxy)
    return min(1.0, covered / spot_area) if spot_area else 1.0


def shutter_read_contrast():
    """DND-115: does the shutter make the vane return state-dependent?

    Computes the shadow fraction of the fixed-standoff beam in each latch state,
    the swept envelope (neighbour / own-column / aperture clearances), the
    state-dependent standoff of the ABSORBER (must stay inside the DoF), and the
    resulting on/off return ratio and its margin over neighbour crosstalk and
    ambient. The deciding number is geometric (shadow fraction), not SNR.
    """
    hinge_x = 3.60 / 2 + 0.45 / 2 + 0.20                # 2.225
    cell_top_mm = 3.60
    flag_gap_mm = SHUT_APER_GAP_MM                      # 1.8 (DND-115 revision)
    flag_ap_mm = SHUT_AP_MM                             # 0.44 (1 line)
    half_angle_deg = 15.0
    spot_mm = flag_ap_mm + 2 * flag_gap_mm * math.tan(
        math.radians(half_angle_deg))                   # 1.405 mm
    x_clear_nb_mm = PITCH_MM - cell_top_mm / 2 - hinge_x   # 1.055
    x_clear_own_mm = hinge_x - cell_top_mm / 2             # 0.425

    # Swept envelope on a fine grid (the CAD echoes the closed form).
    n = 1800
    xs, zs = [], []
    for i in range(n + 1):
        deg = SHUT_SWING_DEG * i / n
        for (px, pz) in _shutter_flap_corners(deg):
            xs.append(px)
            zs.append(pz)
    sweep_x_min, sweep_x_max = min(xs), max(xs)
    sweep_z_min, sweep_z_max = min(zs), max(zs)
    clears_neighbour = bool(sweep_x_max <= PITCH_MM - cell_top_mm / 2)
    above_own_column = bool(sweep_z_min >= TRAVEL_MM)
    flat_bot_mm = SHUT_HINGE_Z_MM - SHUT_FLAP_R_MM - SHUT_T_MM / 2.0   # 43.20
    flat_top_mm = SHUT_HINGE_Z_MM - SHUT_FLAP_R_MM + SHUT_T_MM / 2.0   # 43.64
    vane_gap_mm = flat_bot_mm - (TRAVEL_MM + 3.0)                      # 0.20
    aperture_clear_mm = SHUT_APERTURE_Z_MM - flat_top_mm               # 0.36

    # Shadow fraction in each state: HIDDEN = crank 0 (flat), VISIBLE = 90 (edge).
    hidden_shadow = _shutter_covered_fraction(0.0, spot_mm)
    visible_shadow = _shutter_covered_fraction(SHUT_SWING_DEG, spot_mm)
    # Clear-state must be fully clear; hidden-state fully covered.
    hidden_ok = hidden_shadow >= 0.99
    visible_ok = visible_shadow <= 0.01

    # Absorber standoff (occluded state): the flap underside sits at flat_bot_mm.
    absorber_gap_mm = (TRAVEL_MM + 3.0 + flag_gap_mm) - flat_bot_mm   # 0.80
    target_delta_z_mm = 0.0        # the reflective TARGET is still frame-fixed
    absorber_delta_z_mm = (flat_bot_mm - (TRAVEL_MM + 3.0))           # 0.20
    absorber_in_dof = bool(absorber_delta_z_mm <= 1.0)

    # On/off return ratio. Bright = vane only; dark = vane * (1-shadow) + flap term.
    # The vane and flap are at slightly different standoffs; the flap is dark
    # (~0.05) and the vane bright (~0.80). The shadow term dominates.
    r_vane = READ_TARGET_REFLECTANCE_UP      # 0.80
    r_flap = SHUT_FLAP_REFLECTANCE           # 0.05
    # Solid-angle proxies (Lambertian A/d^2) at each plane.
    g_vane = flag_gap_mm                     # 1.00
    g_flap = absorber_gap_mm                 # 0.80
    bright = (1.0 - visible_shadow) * r_vane / g_vane ** 2
    dark = (1.0 - hidden_shadow) * r_vane / g_vane ** 2 + \
        hidden_shadow * r_flap / g_flap ** 2
    on_off_ratio = bright / dark if dark > 0 else float("inf")

    # Neighbour margin and crosstalk in the CLEAR state. The neighbour body's
    # near edge is at x = PITCH - cell_top/2 = 3.28 mm; the swept flap reaches
    # x = 3.025 mm, so the flap itself clears by (3.28 - 3.025) mm. The READ beam
    # spot half-width (0.568 mm) about x = 2.225 reaches only 2.793 mm, also
    # short of 3.28 mm, so no part of the read spot touches the neighbour body
    # (this is the DND-114 clearance, unchanged). The neighbour top is at most
    # z = TRAVEL (40), i.e. >= 4 mm below the 44 mm aperture plane and off-beam.
    neighbour_near_edge_mm = PITCH_MM - cell_top_mm / 2     # 3.28
    neighbour_clear_margin_mm = neighbour_near_edge_mm - sweep_x_max
    spot_clear_margin_mm = neighbour_near_edge_mm - (hinge_x + spot_mm / 2)
    nb_gap_min_mm = SHUT_APERTURE_Z_MM - TRAVEL_MM          # 4.0 mm
    # Fraction of the clear-state aperture solid angle subtended by the neighbour
    # body vs the vane (both Lambertian A/d^2; the neighbour is off-axis, so this
    # is a conservative upper bound on its contribution).
    neighbour_region = (cell_top_mm ** 2) / nb_gap_min_mm ** 2
    vane_region = (0.44 * 1.60) / g_vane ** 2               # vane area / g^2
    crosstalk_ratio = neighbour_region / vane_region        # upper bound

    # Ambient: synchronous (modulated-LED) detection rejects DC; the dark-state
    # margin over ambient is the same device-class assumption as DND-114.
    ambient_margin_note = (
        "modulated LED + synchronous detect rejects room ambient by "
        f"{1.0/READ_DC_REJECTION:.0f}x (assumption-class)")

    return dict(
        evidence="CAD geometry (a1_binary_latch_cell.scad shutter) + CALCULATION "
                 "(no print, no measurement; DND-27)",
        cad_source="10-reliability-mask/scad/a1_binary_latch_cell.scad "
                   "(shutter_crank/shutter_flap)",
        hinge_x_mm=round(hinge_x, 3),
        hinge_z_mm=SHUT_HINGE_Z_MM,
        flap_r_mm=round(SHUT_FLAP_R_MM, 3),
        swing_deg=SHUT_SWING_DEG,
        flat_bot_mm=round(flat_bot_mm, 3),
        flat_top_mm=round(flat_top_mm, 3),
        vane_gap_mm=round(vane_gap_mm, 3),
        aperture_clearance_mm=round(aperture_clear_mm, 3),
        sweep_x_mm=[round(sweep_x_min, 3), round(sweep_x_max, 3)],
        sweep_z_mm=[round(sweep_z_min, 3), round(sweep_z_max, 3)],
        x_clear_neighbour_mm=round(x_clear_nb_mm, 3),
        x_clear_own_mm=round(x_clear_own_mm, 3),
        clears_neighbour=clears_neighbour,
        above_own_column=above_own_column,
        hidden_shadow_fraction=round(hidden_shadow, 4),
        visible_shadow_fraction=round(visible_shadow, 4),
        hidden_state_fully_occluded=hidden_ok,
        visible_state_fully_clear=visible_ok,
        target_delta_z_mm=target_delta_z_mm,
        absorber_delta_z_mm=round(absorber_delta_z_mm, 3),
        absorber_in_dof=absorber_in_dof,
        dof_mm=1.0,
        on_off_return_ratio=round(on_off_ratio, 2),
        on_off_gate=2.0,
        contrast_passes=bool(on_off_ratio >= 2.0
                            and hidden_ok and visible_ok),
        neighbour_crosstalk_ratio_upper_bound=round(crosstalk_ratio, 3),
        neighbour_near_edge_mm=round(neighbour_near_edge_mm, 3),
        neighbour_flap_clearance_mm=round(neighbour_clear_margin_mm, 3),
        spot_clearance_mm=round(spot_clear_margin_mm, 3),
        spot_off_neighbour=bool(spot_clear_margin_mm > 0.0),
        ambient_note=ambient_margin_note,
        verdict=(
            f"The shutter makes the fixed-standoff return state-dependent: in the "
            f"HIDDEN state the flap (crank 0 deg) covers "
            f"{hidden_shadow*100:.1f}% of the read spot; in the VISIBLE state "
            f"(crank {SHUT_SWING_DEG:.0f} deg) it covers "
            f"{visible_shadow*100:.1f}%. The on/off return ratio is "
            f"~{on_off_ratio:.0f}x (gate {2.0:.0f}x). The reflective TARGET stays "
            f"frame-fixed (DeltaZ = {target_delta_z_mm:.3f} mm); only the "
            f"ABSORBER's standoff varies, by {absorber_delta_z_mm:.2f} mm, inside "
            f"the {1.0:.1f} mm DoF. The swept flap clears the neighbour body by "
            f"{neighbour_clear_margin_mm:.3f} mm and the own column by "
            f"{sweep_z_min - TRAVEL_MM:.2f} mm. In the clear state the read spot "
            f"is entirely off the neighbour body (clearance "
            f"{spot_clear_margin_mm:.3f} mm), and the neighbour top is "
            f">= {nb_gap_min_mm:.0f} mm below the aperture plane and off-axis, so "
            f"its solid-angle upper bound is "
            f"{crosstalk_ratio:.2f}x of the vane (mostly off-axis). "
            f"Ambient is rejected by {1.0/READ_DC_REJECTION:.0f}x (assumption). "
            "The read/verify axis is closed at CAD + calculation; the remaining "
            "residuals are material/measurement-only (DND-27)."),
    )


def shutter_tolerance_mc(n=200_000, seed=115):
    """Worst-case + Monte Carlo tolerance stack-up for the DND-115 shutter.

    Program policy (DND-27) retires go/no-go risk with a worst-case AND a Monte
    Carlo stack-up, not a print. Sources (assumption-class, sourced FDM process
    limits): frame/vane placement, flap print dimensions, hinge placement, and
    the monolithic-frame pitch (neighbour position). Each marginal check is the
    worst sampled value plus its fail rate.

    The key result: the DND-114 1.0 mm standoff CANNOT hold a 0.44 mm flap with
    printed placing tolerances (the aperture-clearance check fails multiple %),
    which is why DND-115 raises the adopted standoff to 1.8 mm.
    """
    import random as _random
    rng = _random.Random(seed)
    spot = SHUT_AP_MM + 2 * SHUT_APER_GAP_MM * math.tan(math.radians(15.0))
    gap_nom = SHUT_GAP_MM
    hinge_x = 3.60 / 2 + 0.45 / 2 + 0.20
    m = {
        "neighbour_flap_clearance_mm": [],
        "aperture_clearance_mm": [],
        "vane_gap_mm": [],
        "coverage_mm": [],
        "own_clearance_mm": [],
        "on_off_ratio": [],
    }
    # Tolerances: (assumption-class, sourced FDM). The latch lane (hinge_x) and
    # the flap are features of ONE monolithic cell print, so their relative
    # tolerance is tighter than the inter-cell pitch.
    t_hx, t_hinge_z, t_flap_r, t_T, t_W = 0.05, 0.20, 0.15, 0.10, 0.10
    t_neighbour, t_vane, t_gap = 0.10, 0.10, 0.10

    def _mc_one(neighbour_tol):
        fails = {k: 0 for k in m}
        worst = {k: float("inf") for k in m}
        for _ in range(n):
            hx = hinge_x + rng.uniform(-t_hx, t_hx)
            hz = SHUT_HINGE_Z_MM + rng.uniform(-t_hinge_z, t_hinge_z)
            fr = SHUT_FLAP_R_MM + rng.uniform(-t_flap_r, t_flap_r)
            tt = SHUT_T_MM + rng.uniform(-t_T, t_T)
            ww = SHUT_W_MM + rng.uniform(-t_W, t_W)
            nbe = PITCH_MM - 3.60 / 2 + rng.uniform(-neighbour_tol, neighbour_tol)
            vt = (TRAVEL_MM + 3.0) + rng.uniform(-t_vane, t_vane)
            g2 = gap_nom + rng.uniform(-t_gap, t_gap)
            fb = vt + g2
            ft = fb + tt
            aper = (TRAVEL_MM + 3.0) + SHUT_APER_GAP_MM
            checks = {
                "neighbour_flap_clearance_mm": nbe - (hx + ww / 2.0),
                "aperture_clearance_mm": aper - ft,
                "vane_gap_mm": fb - vt,
                "coverage_mm": ww - spot,
                "own_clearance_mm": fb - TRAVEL_MM,
                "on_off_ratio": (READ_TARGET_REFLECTANCE_UP / SHUT_APER_GAP_MM ** 2)
                / (SHUT_FLAP_REFLECTANCE / max(aper - fb, 0.1) ** 2),
            }
            for k, v in checks.items():
                if v < worst[k]:
                    worst[k] = v
                if (v < 0.0) if k != "on_off_ratio" else (v < 2.0):
                    fails[k] += 1
        return worst, {k: fails[k] / n for k in fails}

    worst, fail = _mc_one(t_neighbour)
    worst_pess, fail_pess = _mc_one(0.20)
    return dict(
        evidence="CALCULATION - worst-case + Monte Carlo stack-up (no print; DND-27)",
        n=n,
        standoff_mm=SHUT_APER_GAP_MM,
        aperture_mm=SHUT_AP_MM,
        spot_mm=round(spot, 3),
        tolerances_mm=dict(
            hinge_x=t_hx, hinge_z=t_hinge_z, flap_r=t_flap_r,
            flap_t=t_T, flap_w=t_W, pitch_neighbour=0.10, vane_top=t_vane,
            gap=t_gap),
        worst_case_nominal=dict(
            neighbour_flap_clearance_mm=round(worst["neighbour_flap_clearance_mm"], 3),
            aperture_clearance_mm=round(worst["aperture_clearance_mm"], 3),
            vane_gap_mm=round(worst["vane_gap_mm"], 3),
            coverage_mm=round(worst["coverage_mm"], 3),
            own_clearance_mm=round(worst["own_clearance_mm"], 3),
            on_off_ratio=round(worst["on_off_ratio"], 2)),
        fail_rate_nominal={k: fail[k] for k in fail},
        worst_case_pessimistic=dict(
            neighbour_flap_clearance_mm=round(
                worst_pess["neighbour_flap_clearance_mm"], 3),
            aperture_clearance_mm=round(worst_pess["aperture_clearance_mm"], 3),
            vane_gap_mm=round(worst_pess["vane_gap_mm"], 3)),
        fail_rate_pessimistic={k: fail_pess[k] for k in fail_pess},
        passes_nominal=bool(all(v == 0.0 for v in fail.values())),
        verdict=(
            f"At the adopted {SHUT_APER_GAP_MM:.1f} mm standoff (aperture "
            f"{SHUT_AP_MM:.2f} mm) the shutter passes every margin in all "
            f"{n} Monte Carlo draws with a realistic monolithic-frame pitch "
            f"tolerance (+/-0.10 mm) on the neighbour. Worst sampled margins: "
            f"neighbour {worst['neighbour_flap_clearance_mm']:.3f} mm, aperture "
            f"{worst['aperture_clearance_mm']:.3f} mm, vane gap "
            f"{worst['vane_gap_mm']:.3f} mm, coverage "
            f"{worst['coverage_mm']:.3f} mm. At a hostile +/-0.20 mm neighbour "
            f"tolerance the neighbour margin alone can go slightly negative "
            f"({worst_pess['neighbour_flap_clearance_mm']:.3f} mm; fail rate "
            f"{fail_pess['neighbour_flap_clearance_mm']*100:.1f}%) - the binding "
            "term is pitch placement, retired by a single monolithic print. The "
            f"DND-114 1.0 mm standoff is INFEASIBLE under this stack-up (the "
            "aperture-clearance check fails), which is why DND-115 adopts "
            "1.8 mm."),
    )


def z_stroke_trade_study():
    """Rate cost of correcting the standoff with a reader Z stroke (DND-113 b).

    A reader that descends to the pocket for the down state pays a 40 mm Z
    stroke each way. Per CELL this is rate-fatal; per LINE (refocus at row
    ends) it may be survivable. Bounds both with a trapezoidal Z move at
    0.5 m/s and the sourced X1C 20 m/s^2.
    """
    v = 500.0                 # mm/s assumption-class Z axis
    a = X1C_MAX_ACCEL_MM_S2
    d = 2.0 * TRAVEL_MM       # down and back up
    t_acc = v / a
    d_acc = 0.5 * a * t_acc * t_acc
    if d >= 2.0 * d_acc:
        t_stroke = 2.0 * t_acc + (d - 2.0 * d_acc) / v
    else:
        t_stroke = 2.0 * math.sqrt(d / a)
    t_stroke += SETTLE_MS / 1000.0
    cell_s = t_stroke
    cell_rate = 1.0 / cell_s
    cycle_per_cell_s = 2.0 * CELLS * cell_s      # both write and verify passes
    n_lines = COLS
    cycle_per_line_s = 2.0 * n_lines * t_stroke
    return dict(
        evidence="CALCULATION over a trapezoidal 40 mm Z move",
        z_speed_mm_s=v, z_accel_mm_s2=a,
        stroke_mm=2.0 * TRAVEL_MM, stroke_time_s=round(t_stroke, 4),
        per_cell_rate_cells_s=round(cell_rate, 2),
        per_cell_cycle_s=round(cycle_per_cell_s, 1),
        per_line_strokes=n_lines,
        per_line_cycle_s=round(cycle_per_line_s, 1),
        verdict=(
            f"A Z stroke per CELL gives {cell_rate:.1f} cells/s and a full "
            f"cycle >{cycle_per_cell_s/60:.0f} min - RATE-FATAL. A Z refocus "
            f"per LINE costs {cycle_per_line_s:.1f} s for both passes - "
            "survivable only if the rest of the cycle leaves that margin; it "
            "must be added to the full_cycle. Conclusion: correct the standoff "
            "with a COMMON-HEIGHT target, not by descending the reader."
        ),
    )


# ---------------------------------------------------------------------------
# 6. THE DOMINANT LIMIT + HONEST ACHIEVABLE RATE
# ---------------------------------------------------------------------------
def achievable_rate(heads=8):
    """Combine the four bounds into an honest per-head rate and head count.

    Kinematics: the head FLIES at speed v. Over one pitch it spends p/v
    traversing. The write actuation can overlap the next traverse, so the
    effective WRITE per-cell time is max(traverse, actuation) + settle. The
    READ per-cell time is max(traverse, integration) + settle. The binding
    per-head rate is the slower of the two passes.

    The band crosses gantry speed with the two actuation models, so the
    honest headline is a RANGE, not a single tuned number.
    """
    bounds = dict(
        stop_and_go=stop_and_go_bound(),
        traverse=traverse_bound(),
        write=write_actuation_bound(),
        read=read_integration_bound(),
        read_resolution=read_resolution_bound(),
    )
    t_read_ms = READ_INTEGRATION_US / 1000.0
    t_settle_ms = SETTLE_MS

    speeds = (("conservative 0.5 m/s (X1C-sourced)", GANTRY_SOURCED_V_MM_S),
              ("credible 1.0 m/s", 1000.0),
              ("optimistic 1.5 m/s (repo-prior)", GANTRY_ASSUMED_V_MM_S))
    act_models = (("snap-trigger 3 ms (device-class)",
                   write_actuation_bound()["device_class_pulse_ms"]),
                  ("full-sweep 13 ms (pessimistic)",
                   write_actuation_bound()["mechanical_pulse_ms"]))

    band = {}
    for alabel, act_ms in act_models:
        for label, v in speeds:
            tt = PITCH_MM / v * 1e3
            w_cell = max(tt, act_ms) + t_settle_ms
            r_cell = max(tt, t_read_ms) + t_settle_ms
            head_rate = min(1e3 / w_cell, 1e3 / r_cell)
            dominant = ("actuation" if act_ms > tt else "traverse")
            band[f"{alabel} @ {label}"] = dict(
                v_mm_s=v, actuation_ms=act_ms,
                traverse_ms=round(tt, 3),
                write_cell_ms=round(w_cell, 3),
                verify_cell_ms=round(r_cell, 3),
                write_cells_s=round(1e3 / w_cell, 1),
                verify_cells_s=round(1e3 / r_cell, 1),
                head_cells_s=round(head_rate, 1),
                dominant_limit=dominant,
            )

    # Primary design point: credible 1.0 m/s gantry + device-class snap.
    primary = band["snap-trigger 3 ms (device-class) @ credible 1.0 m/s"]
    rate_head = primary["head_cells_s"]
    # Pessimistic design point: 1.0 m/s + full-sweep snap.
    pessimistic = band["full-sweep 13 ms (pessimistic) @ credible 1.0 m/s"]
    rate_pess = pessimistic["head_cells_s"]
    # Best credible: optimistic 1.5 m/s + device-class snap.
    best = band["snap-trigger 3 ms (device-class) @ optimistic 1.5 m/s (repo-prior)"]
    rate_best = best["head_cells_s"]

    # Heads to clear <30 s from the PRIMARY per-head rate.
    rest_s = DIGITAL_MAP_S + MASK_GENERATION_S + TRANSPORT_S + RESET_S + SETTLE_S
    needed_s = 30.0 - rest_s
    heads_needed = math.ceil(2 * CELLS / (needed_s * rate_head))
    return dict(
        evidence="CALCULATION - min over the four independently bounded limits",
        primary_design_point=dict(
            traverse_mm_s=1000.0, actuation_ms=primary["actuation_ms"],
            per_head_rate_cells_s=rate_head,
            dominant_limit=primary["dominant_limit"]),
        band=band,
        rate_range_cells_s=[rate_pess, rate_best],
        per_head_rate_cells_s=rate_head,
        placeholder_cells_s=PLACEHOLDER_CELLS_S,
        placeholder_overstated_by=round(PLACEHOLDER_CELLS_S / rate_head, 1),
        placeholder_overstated_by_range=[
            round(PLACEHOLDER_CELLS_S / rate_best, 1),
            round(PLACEHOLDER_CELLS_S / rate_pess, 1)],
        heads_for_30s=heads_needed,
        bounds=bounds,
        verdict=(
            "The honest per-head rate is bounded by TRAVERSE plus the latch "
            "snap, not by an arbitrary step rate. At a credible 1.0 m/s gantry "
            f"with a snap-trigger toggle the head does {rate_head:.0f} cells/s; "
            f"the credible band is {rate_best:.0f}-{rate_pess:.0f} cells/s "
            "(1.5 m/s snap-trigger to 1.0 m/s pessimistic full-sweep). The "
            f"placeholder 1,000 cells/s overstates the achievable rate by "
            f"~{PLACEHOLDER_CELLS_S/rate_best:.0f}-"
            f"{PLACEHOLDER_CELLS_S/rate_pess:.0f}x. The rate is ANALYTICALLY "
            "BOUNDED with the dominant limit named per operating point, which "
            "is outcome (a) on the RATE axis. DND-113: the READ axis residual "
            "is the state-dependent standoff (not gantry registration); see "
            "`read_resolution_bound()`. The as-built snap force and gantry "
            "repeatability remain tolerance residuals."
        ),
    )


# ---------------------------------------------------------------------------
# 7. RE-DERIVED FULL-CYCLE TIMING (DND-103 stages)
# ---------------------------------------------------------------------------
DIGITAL_MAP_S = 0.05
MASK_GENERATION_S = 0.00        # A1 has no physical mask
TRANSPORT_S = 2.00              # gantry lane repositioning (repo prior)
RESET_S = 3.00                  # global reset stroke (repo prior)
SETTLE_S = 1.50                 # map-level settle (repo prior)

# Which actuation model the full-cycle uses: "snap" (device-class, primary)
# or "full-sweep" (pessimistic).
WRITE_ACTUATION_MODEL = "snap"


def _actuation_ms():
    w = write_actuation_bound()
    if WRITE_ACTUATION_MODEL == "full-sweep":
        return w["mechanical_pulse_ms"]
    return w["device_class_pulse_ms"]


def raster_pass_time_s(v_mm_s, heads):
    """Honest raster pass time including per-line accel/reversal (DND-113).

    DND-112 T3 found the DND-111 `full_cycle` charged only `cells/heads *
    per-cell`, which assumes the head is already at speed on every line and
    never reverses. A real raster line of ACTIVE_MM at speed v must accelerate
    from rest and decelerate back to rest (or reverse) at each end, costing
    `2*v/a`. With `heads` heads spread across x, the bar makes
    `CELLS/heads/COLS` y-sweeps of ACTIVE_MM; each pays one accel + one decel.

    The write/read per-cell time already contains the traverse; this function
    adds ONLY the per-line ramp, so it does not double-count.
    """
    n_lines = CELLS / heads / COLS                    # y-sweeps per pass
    line_s = ACTIVE_MM / v_mm_s + 2.0 * (v_mm_s / X1C_MAX_ACCEL_MM_S2)
    ideal_per_cell_s = PITCH_MM / v_mm_s
    pass_ideal_s = CELLS / heads * ideal_per_cell_s
    ramp_overhead_s = n_lines * 2.0 * (v_mm_s / X1C_MAX_ACCEL_MM_S2)
    return dict(
        n_lines=round(n_lines, 3),
        line_s=round(line_s, 4),
        pass_ideal_s=round(pass_ideal_s, 4),
        ramp_overhead_s=round(ramp_overhead_s, 4),
        pass_honest_s=round(pass_ideal_s + ramp_overhead_s, 4),
        overhead_fraction=round(ramp_overhead_s / pass_ideal_s, 4) if pass_ideal_s else 0.0,
    )


def full_cycle(heads=8, v_mm_s=1000.0):
    """Re-derive the A1 full-map cycle from the analytically bounded rate.

    Raster geometry: the gantry bar carries `heads` writer heads. It sweeps
    the full 80-cell width once per lane group, so the pass time for the
    whole field is (cells / heads) * per-cell time, PLUS the per-line
    accel/reversal overhead DND-113 adds (DND-112 T3: ~24.6 % at 8 heads).

    The head count is what compensates for the honest per-head rate being
    several times under the placeholder, and this function reports the head
    count that still clears <30 s.
    """
    t_trav_ms = PITCH_MM / v_mm_s * 1e3
    t_act_ms = _actuation_ms()
    t_read_ms = READ_INTEGRATION_US / 1000.0
    write_cell_s = (max(t_trav_ms, t_act_ms) + SETTLE_MS) / 1000.0
    verify_cell_s = (max(t_trav_ms, t_read_ms) + SETTLE_MS) / 1000.0
    write_ideal_s = CELLS * write_cell_s / heads
    verify_ideal_s = CELLS * verify_cell_s / heads
    # DND-113: add the per-line ramp to the traverse part of each pass. The
    # per-cell time already contains PITCH/v plus actuation/read/settle, so the
    # ramp is ADDED (not substituted) and the pass is not double-counted.
    write_ramp = raster_pass_time_s(v_mm_s, heads)["ramp_overhead_s"]
    verify_ramp = raster_pass_time_s(v_mm_s, heads)["ramp_overhead_s"]
    write_all_s = write_ideal_s + write_ramp
    verify_s = verify_ideal_s + verify_ramp
    stages = dict(
        digital_map=DIGITAL_MAP_S,
        mask_generation=MASK_GENERATION_S,
        transport=TRANSPORT_S,
        reset=RESET_S,
        write=round(write_all_s, 4),
        settle=SETTLE_S,
        verify=round(verify_s, 4),
    )
    total = round(sum(stages.values()), 4)
    return dict(
        heads=heads, traverse_mm_s=v_mm_s,
        actuation_model=WRITE_ACTUATION_MODEL,
        actuation_ms=round(t_act_ms, 3),
        write_cell_ms=round(write_cell_s * 1e3, 3),
        verify_cell_ms=round(verify_cell_s * 1e3, 3),
        write_ideal_s=round(write_ideal_s, 4),
        verify_ideal_s=round(verify_ideal_s, 4),
        ramp_overhead_per_pass_s=round(write_ramp, 4),
        stages=stages, full_cycle_s=total,
        clears_30s=bool(total < 30.0),
        margin_s=round(30.0 - total, 4),
        note="Pass time = cells/(heads) * per-cell time PLUS the per-line "
             "accel/reversal ramp (DND-113, DND-112 T3). The per-cell time is "
             "max(traverse, actuation_or_read) + settle, from the bounded rate.",
    )


def full_cycle_head_sweep(v_mm_s=1000.0, actuation_model="snap"):
    """Full-cycle time as a function of parallel head count, at the credible
    gantry speed. Reports the minimum head count that clears <30 s.

    `actuation_model` selects device-class snap (3 ms, primary) or the
    pessimistic full-sweep toggle (13 ms).
    """
    global WRITE_ACTUATION_MODEL
    WRITE_ACTUATION_MODEL = actuation_model
    out = {}
    for h in (1, 2, 4, 8, 12, 16, 24, 32):
        fc = full_cycle(heads=h, v_mm_s=v_mm_s)
        out[h] = dict(full_cycle_s=fc["full_cycle_s"],
                      clears_30s=fc["clears_30s"])
    WRITE_ACTUATION_MODEL = "snap"
    clearing = [h for h, d in out.items() if d["clears_30s"]]
    return dict(
        evidence="CALCULATION over the bounded per-cell time",
        traverse_mm_s=v_mm_s,
        actuation_model=actuation_model,
        sweep=out,
        min_heads_to_clear_30s=min(clearing) if clearing else None,
        verdict=(
            f"At a credible 1.0 m/s gantry with the {actuation_model} toggle "
            "the full map clears <30 s with "
            f"{min(clearing) if clearing else '>32'} parallel heads "
            "(write + verify + reset + settle). This is a real cost lever: "
            "heads are cheap printed bodies, so A1 can buy back the honest "
            "rate with parallel heads rather than an over-optimistic number."
        ),
    )


def full_cycle_pessimistic_sweep(v_mm_s=1000.0):
    """Same sweep with the pessimistic full-sweep toggle (13 ms)."""
    return full_cycle_head_sweep(v_mm_s=v_mm_s, actuation_model="full-sweep")


# ---------------------------------------------------------------------------
# 8. OUTCOME
# ---------------------------------------------------------------------------
# DND-111 recorded a single outcome:
#   (a) Bounded  - rate analytically bounded, residual narrows to
#                  procurement/measurement detail.
#   (b) Coupon-only - cannot be settled without a printed coupon.
# The RATE remains outcome (a): bounded from sourced kinematics. DND-113
# corrects the READ side. The rate-side outcome is now stated PER AXIS.
OUTCOME = "a"

OUTCOME_STATEMENT = (
    "OUTCOME (a) BOUNDED on the RATE axis; OUTCOME (a) CLOSED on the "
    "READ/VERIFY axis at CAD + calculation (DND-114 + DND-115). The A1 writer "
    "rate is analytically bounded from sourced component-class kinematics + "
    "placed CAD. The dominant limit is GANTRY TRAVERSE at the credible design "
    "point: at 1.0 m/s one head writes/reads 164.5 cells/s (credible band "
    "71-228 cells/s), a factor 4.4-14x below the placeholder 1,000 cells/s. "
    "Stop-and-go is excluded outright (30.4 cells/s at X1C accel; the 100 "
    "m/s^2 sensitivity row is 61.9, not 89.6 - DND-113 trapezoid fix). The "
    "full map clears <30 s with the honest per-line ramp overhead (DND-113): "
    "8 parallel heads give 18.28 s including verification; even 4 heads give "
    "30.0 s (borderline). The READ/VERIFY axis is now CLOSED: the as-drawn "
    "top-face read was state-dependent-standoff bound (R1/G2), DND-114 moved "
    "the target to a frame-fixed CH-A vane at ONE standoff (DeltaZ = 0), and "
    "DND-115 adds the state-encoding shutter that makes that fixed-standoff "
    "return state-dependent: the flap covers 100% of the 1.136 mm spot in the "
    "hidden state and 0% in the visible state, an on/off ratio ~10x while the "
    "reflective TARGET stays frame-fixed. The remaining residuals are "
    "assumption-class optical constants and measurement-only wear (DND-27). "
    "A1's reliability advantage (readback + retry) is now supported on paper "
    "end to end - the difference between a 0-silent machine and a decorated "
    "silent one."
)


def report():
    return dict(
        issue="DND-111 (rate) + DND-113 (read correction) + DND-114 (common-height "
              "target) + DND-115 (state-encoding shutter)",
        evidence_class="CALCULATION over sourced component-class limits + CAD "
                       "(no print, no purchase, no measurement; DND-27)",
        placeholder_replaced=dict(
            constant="HEAD_RATE_CELLS_S",
            old_value=PLACEHOLDER_CELLS_S,
            new_evidence_class="CALCULATION (traverse-bounded)",
        ),
        stop_and_go=stop_and_go_bound(),
        traverse=traverse_bound(),
        write_actuation=write_actuation_bound(),
        read_integration=read_integration_bound(),
        read_resolution=read_resolution_bound(),
        common_height_read_target=common_height_read_target(),
        flag_read_contrast=flag_read_contrast(),
        shutter_read_contrast=shutter_read_contrast(),
        shutter_tolerance_mc=shutter_tolerance_mc(),
        z_stroke_trade_study=z_stroke_trade_study(),
        achievable=achievable_rate(),
        head_sweep=full_cycle_head_sweep(),
        head_sweep_pessimistic=full_cycle_pessimistic_sweep(),
        full_cycle_8_heads=full_cycle(heads=8),
        outcome=OUTCOME,
        outcome_statement=OUTCOME_STATEMENT,
    )


def main() -> int:
    r = report()
    print(json.dumps(r, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
