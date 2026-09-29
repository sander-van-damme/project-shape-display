"""DND-111 - analytic bound on the A1 writer/reader rate + single-cell read.

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

    If the peak speed a triangular move can reach, sqrt(a*p), is below the
    stage speed ceiling the move is triangular and takes 2*sqrt(p/a); else it
    is speed-limited.
    """
    v_tri = math.sqrt(accel_mm_s2 * pitch_mm)
    if v_tri <= X1C_MAX_SPEED_MM_S:
        move_s = 2.0 * math.sqrt(pitch_mm / accel_mm_s2)
        mode = "triangular (slow axis)"
    else:
        move_s = pitch_mm / X1C_MAX_SPEED_MM_S
        mode = "speed-limited"
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

    The reader compares each cell's return against its neighbours. For a
    single wrong cell to be resolved, the up/down contrast must exceed noise
    by a margin, and the optical spot must not straddle neighbours.

    Two independent requirements:
      (R1) GEOMETRIC - the interrogated spot must be smaller than the pitch
           (with margin) so a down cell does not return an up neighbour's
           light. Spot <= pitch - 2*wall, and the working gap must keep the
           spot in focus.
      (R2) PHOTOMETRIC - the up/down return difference must exceed the noise
           floor with the chosen integration time.
    """
    # (R1) geometric: a lensless aperture of diameter d at gap g spreads by
    # geometry. Required: the returned spot must land on the target column's
    # TOP FACE, not spill onto a neighbour's face across the 0.74 mm lane.
    cell_top_mm = 3.60                  # CAD column body top face
    lane_mm = PITCH_MM / 2 - cell_top_mm / 2   # 0.74 mm owned half-lane
    half_face_mm = cell_top_mm / 2      # 1.80 mm from centre to top-face edge
    aperture_mm = 2.0                   # assumption-class single-cell aperture
    working_gap_mm = 2.0                # repo "~2 mm working gap"
    half_angle_deg = 15.0
    spot_at_target_mm = aperture_mm + 2 * working_gap_mm * math.tan(
        math.radians(half_angle_deg))
    # Worst case: aperture centred over a cell CORNER, so the spot reach is
    # diagonal. CAD check (scad/a1_reader_head.scad) reports CORNER_REACH.
    corner_reach_mm = spot_at_target_mm / 2 * math.sqrt(2)
    spot_fits_centre = bool(spot_at_target_mm / 2 <= half_face_mm)
    spot_fits_corner = bool(corner_reach_mm <= half_face_mm)
    # Registration tolerance: max head-centre offset for the CORNER-reach spot
    # to stay on the face. If the head is registered to cell centres better
    # than this, a centred spot never reaches the corner case.
    registration_needed_mm = max(0.0, half_face_mm - spot_at_target_mm / 2)
    # Gap ceiling for the corner case to fit at zero registration error: the
    # spot diameter must satisfy spot/2*sqrt(2) <= half_face.
    gap_for_corner_mm = (half_face_mm * math.sqrt(2) - aperture_mm / 2) / math.tan(
        math.radians(half_angle_deg))
    gap_for_centre_mm = (half_face_mm - aperture_mm / 2) / math.tan(
        math.radians(half_angle_deg))
    # (R2) photometric: SIGNAL = reflected optical power converted to current.
    # Photodiode responsivity R [A/W]. LED drive P_led [W]. Up vs down cell
    # return fraction rho_up / rho_down.
    resp = READ_PHOTODIODE_RESPONSIVITY_A_W
    p_w = READ_LED_POWER_MW / 1000.0
    i_up = p_w * READ_TARGET_REFLECTANCE_UP * resp      # signal current, up cell
    i_down = p_w * READ_TARGET_REFLECTANCE_DOWN * resp  # signal current, down cell
    contrast = i_up - i_down

    # Noise: (1) shot noise on the full photocurrent, bandwidth B set by the
    # integration time T (B ~ 1/(2T)); (2) ambient converted at the detector
    # and attenuated by the synchronous (modulated-LED) detection factor.
    # Si photodiode in the 500 lux class produces ~ order-1 uA of DC ambient
    # photocurrent; modulated detection rejects it by READ_DC_REJECTION.
    q = 1.602e-19
    T = READ_INTEGRATION_US * 1e-6
    B = 1.0 / (2.0 * T)
    ambient_dc_a = 1.0e-6                                # sourced-class Si PD
    ambient_effective_a = ambient_dc_a * READ_DC_REJECTION
    total_dc_a = i_up + ambient_effective_a
    shot_a = math.sqrt(2.0 * q * total_dc_a * B)
    # Johnson/amplifier input noise (TIA): ~10 nA/sqrt(Hz) at the input is a
    # conservative device-class figure; over B.
    amp_noise_a = 10e-9 * math.sqrt(B)
    noise_a = math.sqrt(shot_a ** 2 + amp_noise_a ** 2)
    snr = contrast / noise_a if noise_a > 0 else float("inf")
    resolves = bool(spot_fits_centre and snr >= 5.0 and registration_needed_mm > 0)
    return dict(
        evidence="CALCULATION + CAD over placed cell geometry + photometric budget",
        cad_source="10-reliability-mask/scad/a1_reader_head.scad",
        pitch_mm=PITCH_MM,
        cell_top_face_mm=cell_top_mm,
        owned_half_lane_mm=round(lane_mm, 3),
        half_face_mm=half_face_mm,
        working_gap_mm=working_gap_mm,
        aperture_mm=aperture_mm,
        half_angle_deg=half_angle_deg,
        spot_at_target_mm=round(spot_at_target_mm, 3),
        spot_fits_centre=spot_fits_centre,
        spot_fits_corner=spot_fits_corner,
        corner_reach_mm=round(corner_reach_mm, 3),
        registration_tolerance_mm=round(registration_needed_mm, 3),
        gap_for_centre_fit_mm=round(gap_for_centre_mm, 3),
        gap_for_corner_fit_mm=round(gap_for_corner_mm, 3),
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
        verdict=(
            "A single wrong cell among 6,400 IS resolvable by a single-cell "
            "contrast read IF (R1) the spot stays on the 3.60 mm top face and "
            "(R2) the up/down return difference clears noise. Photometrically "
            f"this is easy (SNR ~{snr:.0f} at 50 us, gate 5.0). Geometrically "
            f"the {aperture_mm:.0f} mm aperture at a {working_gap_mm:.0f} mm "
            f"gap makes a "
            f"{spot_at_target_mm:.2f} mm spot: it fits the face when "
            f"centre-aligned (reach {spot_at_target_mm/2:.2f} <= {half_face_mm:.2f} "
            f"mm: {spot_fits_centre}) but reaches "
            f"{corner_reach_mm:.2f} mm at worst-case corner alignment "
            f"(fits corner: {spot_fits_corner}). Therefore the head must be "
            f"registered to cell centres to within "
            f"{registration_needed_mm:.2f} mm (or the gap held to "
            f"{gap_for_corner_mm:.2f} mm for zero-error corner alignment). "
            "This is the real single-cell resolution limit: a REGISTRATION "
            "tolerance, not a contrast one."
        ),
        residual=(
            "The reflectance pair (0.80/0.15), aperture, LED power, half-angle "
            "and ambient level are assumption/sourced-class, not measured. The "
            "resolution verdict reduces to a bounded registration requirement "
            "(head-to-cell alignment) plus a bounded contrast requirement; "
            "neither is a rate question and neither needs a print to state."
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
            "is outcome (a); the residual is a gantry-registration / "
            "snap-force tolerance question, not an unconstrained placeholder."
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


def full_cycle(heads=8, v_mm_s=1000.0):
    """Re-derive the A1 full-map cycle from the analytically bounded rate.

    Raster geometry: the gantry bar carries `heads` writer heads. It sweeps
    the full 80-cell width once per lane group, so the pass time for the
    whole field is (cells / heads) * per-cell time. The head count is what
    compensates for the honest per-head rate being several times under the
    placeholder, and this function reports the head count that still clears
    <30 s.
    """
    t_trav_ms = PITCH_MM / v_mm_s * 1e3
    t_act_ms = _actuation_ms()
    t_read_ms = READ_INTEGRATION_US / 1000.0
    write_cell_s = (max(t_trav_ms, t_act_ms) + SETTLE_MS) / 1000.0
    verify_cell_s = (max(t_trav_ms, t_read_ms) + SETTLE_MS) / 1000.0
    write_all_s = CELLS * write_cell_s / heads
    verify_s = CELLS * verify_cell_s / heads
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
        stages=stages, full_cycle_s=total,
        clears_30s=bool(total < 30.0),
        margin_s=round(30.0 - total, 4),
        note="Pass time = cells/(heads) * per-cell time. The per-cell time is "
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
# Exactly one outcome is recorded per DND-111 task 4:
#   (a) Bounded  - rate analytically bounded, residual narrows to
#                  procurement/measurement detail.
#   (b) Coupon-only - cannot be settled without a printed coupon.
# The analysis above bounds the rate from sourced kinematics and the read from
# CAD + a contrast budget. It does NOT require a print to decide the RATE.
# The remaining uncertainty (gantry registration, as-printed latch snap force)
# is a TOLERANCE/WEAR question, not the decisive rate question, and is
# explicitly carried as residual.
OUTCOME = "a"

OUTCOME_STATEMENT = (
    "OUTCOME (a) BOUNDED. The A1 writer/reader rate is analytically bounded "
    "from sourced component-class kinematics + the placed CAD. The dominant "
    "limit is GANTRY TRAVERSE at the credible design point: at 1.0 m/s one "
    "head writes/reads 164.5 cells/s (credible band 71-228 cells/s across "
    "0.5-1.5 m/s and snap-trigger vs full-sweep toggle), a factor 4.4-14x "
    "below the placeholder 1,000 cells/s. Stop-and-go is excluded outright at "
    "5.08 mm pitch (30-90 cells/s). The full map still clears <30 s: at the "
    "primary rate 8 parallel heads give 16.28 s including verification, and "
    "even 4 heads give 26.0 s. Single-cell read resolution is bounded "
    "geometrically (a ~2 mm-gap spot is ~3.07 mm, inside the 3.60 mm top "
    "face) and photometrically (up/down contrast SNR ~1,460 against a gate of "
    "5 at 50 us). The residual is no longer an unconstrained placeholder; it "
    "is a gantry-registration + latch snap-force tolerance question, which is "
    "a coupon question but NOT the decisive rate question."
)


def report():
    return dict(
        issue="DND-111",
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
