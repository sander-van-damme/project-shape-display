"""DND-71 S6-LC -- the ultra-low-cost alternative (< $250 purchased, excl. printed).

STATUS (DND-93): G3 lift-axis corrected to size on the whole 6,400-cell board
(NEMA23-class motor). With the six honest DND-91 allowances the delivered cost is
$263.05, so **G6 FAILS** and the verdict is REJECT. See
07-evidence-and-decisions/dnd93-s6lc-g3-fix.md. A1/A2/A6/A7/A8 remain open.

Question ([DND-71]/[DND-70]). The promoted machine S5-R is **$404.60 delivered**
(`08-current-design/`). The board now requires the same product, same gates, at
**< $250 purchased parts, excluding 3D-printed parts**. This module defines that
machine and shows, on the DND-27 evidence classes, whether it closes.

WHY A NEW MACHINE, NOT A TRIM (the honest problem statement)
-----------------------------------------------------------
The S5-R purchased BOM decomposes as:

    fixed legacy base (S5 lift/scan/frame stock)   $218.70  (62.7 %)
    actuators: 2 NEMA17 bank motors + 40 solenoids $124.00  (35.6 %)
    driver channels + steel rod                    $  6.09  ( 1.7 %)
    ----------------------------------------------------------
    purchased parts                                $348.79

The $250 ceiling is a **delivered** budget of $250, i.e. a **parts ceiling of
$250 / UPLIFT = $215.52** at the repo's additive 1.16 delivered uplift
(DND-41: +10 % ship, +6 % tax). The legacy fixed base ALONE ($218.70) already
exceeds the entire parts budget. Shaving pennies cannot close this: the machine
must be re-conceived so that (a) there is no 40-solenoid writer bank and no
2-motor bank drive, and (b) the lift/scan/frame bought stock is replaced by a
single-lead-screw axis over a printed frame.

THE COST CLIFF IS ACTUATOR COUNT, NOT PART QUALITY
--------------------------------------------------
S5-R's $124 actuator block is 1 motor per 3.2 columns-equivalent plus 40
solenoids. Every bought actuator removed is ~$2.50-$12 saved. The cheapest
machine is the one with the FEWEST bought actuators. The architectural family
that achieves this is already screened in `04-architecture-candidates/`:

  * S1  = broadcast threshold ratchet + global incremental lift:
          passive printed pawls, 4 broadcast 10 mm strokes, a planar mask.
  * S2  = planar first-stop memory tiles (perforated plates).

Both eliminate per-cell/per-row bought actuation. S1's open failure was the
**mask write time** (serial punching 2560 s; an 80-channel writer 56 s) and its
worst-case **release force** (2.4 kN all-armed). This module adopts S1-B (the
banked broadcast variant, 8 banks of 10 rows = 800 cells) -- which fixes the
release force to ~296 N/bank -- and pairs it with a **pre-written punched
mask medium** so the mask write is OFF the visible 30 s budget, exactly as the
S1/S2 screen permits. That is the S6-LC machine.

MECHANISM DEFINITION (CAD: ../scad/s6lc_machine.scad)
-----------------------------------------------------
One common platen is raised by **one NEMA17-class lead screw**. The board is
split into **8 banks of 10 rows** (800 cells each). Each bank has:
  * 800 square printed columns, each a 5-pocket vertical rack (10 mm pockets);
  * 800 printed cantilever pawls that hold the column against gravity;
  * a bank **threshold mask gate** (one printed sliding comb per bank) whose
    boss/hole pattern is read from a removable **punched card**;
  * a bank **release comb** that lifts all pawl toes for reset.
A full map = 4 broadcast 10 mm strokes (one per threshold level). On stroke k,
only cells whose mask gate is OPEN for that level are advanced. A target height
of n*10 mm (n = 0..4) means the cell is armed for strokes 1..n and blocked
thereafter. Four binary masks = five heights.

The mask is a **punched card** prepared by a cheap shared card puncher at
program time. Card preparation is deliberately OFF the visible 30 s budget (a
board-facing product statement, carried honestly: an *unannounced* map needs
card prep first; a card can also be reused/pre-written). This is the S2
"double-buffered medium" trade, made explicit.

EVIDENCE CLASS. Geometry + force + timing = CALCULATION over sourced FDM
process limits and sourced actuator ratings; CAD is real OpenSCAD
(`../scad/s6lc_machine.scad`). No print, no purchase, no measurement (DND-27).
"""
from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent

# ---------------------------------------------------------------------------
# Product gates (unchanged from the programme; 02-design-criteria).
# ---------------------------------------------------------------------------
PITCH_MM = 5.08
ROWS = 80
COLS = 80
CELLS = ROWS * COLS                      # 6400
LEVELS = 5
LEVEL_MM = 10.0                          # 10 mm per level -> 4 strokes = 40 mm
TRAVEL_MM = (LEVELS - 1) * LEVEL_MM      # 40.0
PITCH_CLEARANCE_MM = 1.48                # S1-sourced lane (body 3.60 + 1.48)
COLUMN_BODY_MM = PITCH_MM - PITCH_CLEARANCE_MM   # 3.60 mm square (S1 coupon)
ACTIVE_MM = ROWS * PITCH_MM              # 406.4 mm
TIME_GATE_S = 30.0
COST_GATE_USD = 250.0                    # DND-70: purchased, excl. printed
UPLIFT = 1.10 + 0.06                     # repo additive delivered uplift

# ---------------------------------------------------------------------------
# Banking (S1-B): 8 banks of 10 rows = 800 cells. Bounds release force.
# ---------------------------------------------------------------------------
ROWS_PER_BANK = 10
BANKS = ROWS // ROWS_PER_BANK            # 8
CELLS_PER_BANK = COLS * ROWS_PER_BANK    # 800

# ---------------------------------------------------------------------------
# Global-stroke / banked-reset timing (mechanism cycle, every term explicit).
#
# DESIGN CHOICE (DND-71): the platen strokes the WHOLE 80x80 board at once --
# that is the point of a broadcast architecture. All 6,400 cells see all four
# 10 mm strokes. The MASK (punched card) decides which cells advance, so no
# per-bank platen is needed for writing. Only the RESET is banked: eight
# staggered release combs trip the pawls one bank at a time, which is what
# bounds the worst-case simultaneous release force (S1-B). This is both faster
# and force-feasible than a serial per-bank platen (see sensitivity()).
# ---------------------------------------------------------------------------
PLATEN_SPEED_MM_S = 20.0                 # sourced-class lead-screw axis speed
STROKE_MM = LEVEL_MM                     # 10 mm broadcast stroke
SETTLE_S = 0.15                          # mechanism settle at stroke top (assumption)
RETURN_S = 0.20                          # platen returns to datum per stroke (assumption)
RESET_S = 0.50                           # release comb + drop per BANK (assumption)
STROKES = LEVELS - 1                     # 4 global broadcast strokes
STROKES_PER_BANK = STROKES
# DND-74/DND-91 Attack 4/6: the previously-unpriced overhead terms.
MASK_INDEX_S = 0.25                      # mask-gate re-index between strokes (assumption)
CARRIAGE_SPEED_MM_S = 100.0              # reset carriage traverse speed (assumption)
BANK_PITCH_MM = ACTIVE_MM / BANKS        # 50.8 mm from bank to bank
CARRIAGE_TRAVERSE_S = BANK_PITCH_MM / CARRIAGE_SPEED_MM_S  # 0.508 s per bank gap

# ---------------------------------------------------------------------------
# Reset-carriage axis (DND-74/91 Attack 5: previously ungated).
# The carriage hauls one banked release comb at a time: load = banked release
# force, through the same <=2 mm lead, on the $8 small stepper.
# ---------------------------------------------------------------------------
RESET_MOTOR_TORQUE_NM = 0.16             # sourced-class 42 mm small stepper (~$8)

# ---------------------------------------------------------------------------
# Sourced process / material limits (as used across Test11/Test12).
# ---------------------------------------------------------------------------
MIN_FEATURE_MM = 0.44                    # 1 extrusion line @ 0.4 mm nozzle
MIN_WALL_MM = 0.88                       # 2 lines, robust
PLA_E_MPA = 1500.0                       # sourced modulus range 700-2500, midpoint
MU_PLA_MID = 0.35
COLUMN_MASS_G = 1.0                      # printed 4.68 x 4.68 x 44 mm column (calc)
PAWL_RELEASE_N_DESIGN = 0.234            # S1 study break-even; design under it


# ---------------------------------------------------------------------------
# Cell / pawl geometry (printed).
# ---------------------------------------------------------------------------
def _cantilever_rate_n_per_mm(t: float, w: float, l: float,
                              e_mpa: float = PLA_E_MPA) -> float:
    i = w * t ** 3 / 12.0
    return 3.0 * e_mpa * i / l ** 3


PAWL_T_MM = 0.90                         # 2 extrusion lines (robust)
PAWL_W_MM = 1.20                         # width in Y
PAWL_L_MM = 8.00                         # Z cantilever length (long -> soft)
PAWL_DEFLECTION_MM = 0.25                # cam-over relief at a pocket
# S1-sourced pitch lane: body 3.60 + lane 1.48 = 5.08 mm
# (pawl 0.80 + clearance 0.20 + rail 0.48). Our pawl is up to ~1.48 mm thick
# lane-compatible; the leaf itself is 0.90 mm, the rest is clearance. The
# mask gate is stacked ABOVE the pawl in Z (S1 correction: side-by-side does
# not fit).
LANE_BLEED_MM = 0.20
LANE_RAIL_MM = 0.48


def pawl_spring() -> dict:
    k = _cantilever_rate_n_per_mm(PAWL_T_MM, PAWL_W_MM, PAWL_L_MM)
    return dict(rate_n_per_mm=round(k, 4),
                deflection_mm=PAWL_DEFLECTION_MM,
                release_force_n=round(k * PAWL_DEFLECTION_MM, 4))


def column_fit() -> dict:
    """Pitch / printability geometry for the column + pawl + mask lane.

    Uses the S1 coupon's closed pitch budget (body 3.60 + lane 1.48 = 5.08 mm),
    which is the only side-by-side arrangement shown to fit at this pitch. The
    mask gate bar is stacked ABOVE the pawl in Z, so the X budget holds only
    the pawl lane; the gate does not consume the pitch band.
    """
    lane_free = PITCH_MM - COLUMN_BODY_MM                 # 1.48 mm
    pawl_plus = PAWL_T_MM + 2 * LANE_BLEED_MM             # 1.30 mm
    gate_plus = 0.80 + 2 * LANE_BLEED_MM                  # stacked in Z, not X
    x_gap = PITCH_MM - COLUMN_BODY_MM
    fits = (PAWL_T_MM >= MIN_FEATURE_MM) and (pawl_plus <= lane_free) \
        and (gate_plus <= lane_free) and (x_gap >= MIN_FEATURE_MM) \
        and (COLUMN_BODY_MM >= MIN_WALL_MM)
    return dict(column_body_mm=COLUMN_BODY_MM, lane_free_mm=round(lane_free, 3),
                x_gap_mm=round(x_gap, 3),
                pawl_plus_bleed_mm=round(pawl_plus, 3),
                gate_plus_bleed_mm=round(gate_plus, 3),
                gate_stacked_in_z=True,
                column_wall_ok=bool(COLUMN_BODY_MM >= MIN_WALL_MM),
                pawl_min_feature_ok=bool(PAWL_T_MM >= MIN_FEATURE_MM),
                fits=bool(fits))


# ---------------------------------------------------------------------------
# Independent structural limit for the banked reset force (DND-74/91 Attack 5).
#
# The old model compared its banked force to `296 N`, which is S1's own banked
# *output* (0.37 N/cell x 800) -- a circular "ceiling". Replace it with a real
# limit derived from the weakest member of the release load path: the printed
# PLA release-comb tooth that pushes each pawl toe. The tooth is a short
# cantilever in bending; the bank force is shared across COLS teeth.
# ---------------------------------------------------------------------------
PLA_YIELD_MPA = 50.0                     # sourced-class PLA tensile yield (conservative)
COMB_TOOTH_SF = 2.0                      # design safety factor on yield (assumption)
COMB_TOOTH_W_MM = 1.60                   # tooth width in Y (CAD release_comb: 1.6)
COMB_TOOTH_T_MM = 0.88                   # tooth bending thickness in X (2 lines, CAD)
COMB_TOOTH_L_MM = 1.00                   # tooth cantilever length in Z (CAD)


def structural_release_limit_n() -> dict:
    """Independent banked-reset limit from comb-tooth bending (Attack 5 fix)."""
    i = COMB_TOOTH_W_MM * COMB_TOOTH_T_MM ** 3 / 12.0
    sigma_allow = PLA_YIELD_MPA / COMB_TOOTH_SF
    c = COMB_TOOTH_T_MM / 2.0
    p_tooth = sigma_allow * i / (COMB_TOOTH_L_MM * c)
    bank_limit = p_tooth * COLS
    return dict(tooth_section_mm=f"{COMB_TOOTH_W_MM}x{COMB_TOOTH_T_MM}",
                second_moment_mm4=round(i, 5),
                allow_stress_mpa=round(sigma_allow, 1),
                per_tooth_limit_n=round(p_tooth, 3),
                teeth_per_bank=COLS,
                bank_limit_n=round(bank_limit, 1),
                evidence="CALCULATION (PLA beam bending, sourced yield 50 MPa, SF 2)")


def release_force() -> dict:
    """Worst-case simultaneous release force, banked vs un-banked (S1 study)."""
    f = pawl_spring()["release_force_n"]
    all_armed = f * CELLS
    banked = f * CELLS_PER_BANK
    limit = structural_release_limit_n()["bank_limit_n"]
    return dict(per_cell_n=round(f, 4), design_ceiling_n=PAWL_RELEASE_N_DESIGN,
                under_design_ceiling=bool(f <= PAWL_RELEASE_N_DESIGN),
                unbanked_all_armed_n=round(all_armed, 1),
                banked_all_armed_n=round(banked, 1),
                banked_ceiling_n=limit,
                banked_ceiling_evidence=structural_release_limit_n()["evidence"],
                banked_ok=bool(banked <= limit),
                banked_margin=round(limit / max(banked, 1e-9), 2))


# ---------------------------------------------------------------------------
# Platen / lift axis (ONE lead screw, four belt-synced).
#
# DND-74/DND-91 CORRECTION (the decisive G3 fix). The mechanism writes the
# WHOLE board in one global platen stroke -- `timing()` uses 4 global strokes
# and banks only the reset. So the lift axis must carry all CELLS = 6,400
# cells, not one bank's 800. The earlier draft sized the motor on
# `CELLS_PER_BANK`, wrong by the 8x bank factor. Here the axis is sized on the
# full 6,400 cells at the model's own 0.4 N/cell write allowance.
#
# The four screws are belt-synchronised at 1:1, so the single lift motor must
# supply the sum of the four per-screw torques = the total global torque
# (belt losses ignored -> optimistic; the margin absorbs them).
# ---------------------------------------------------------------------------
LIFT_LOAD_N = 0.4                        # N per column during a write stroke
LIFT_SCREWS = 4                          # four belt-synced screws (non-racking)
# DND-74 branch 1: global broadcast kept -> NEMA23-class motor needed.
# Sourced-class NEMA23 (57x57, ~1.8 A) holding torque ~2.2 N*m, ~$30-40.
LIFT_MOTOR_TORQUE_NM = 2.2               # sourced NEMA23-class (was 0.30 NEMA17)
LEAD_MM = 2.0                            # <= 2 mm lead required by DND-43 gate
SCREW_EFF = 0.5                          # lead-screw efficiency (assumption)


def _screw_torque_nm(force_n: float) -> float:
    """Torque to raise `force_n` through one screw (lead LEAD_MM, eff SCREW_EFF)."""
    return force_n * (LEAD_MM / 1000.0) / (2 * math.pi * SCREW_EFF)


def lift_axis() -> dict:
    """Full-board lift torque gate (DND-74 branch 1: global broadcast kept)."""
    total_load_n = LIFT_LOAD_N * CELLS
    torque_total = _screw_torque_nm(total_load_n)
    per_screw_n = total_load_n / LIFT_SCREWS
    torque_per_screw = _screw_torque_nm(per_screw_n)
    return dict(cells_lifted=CELLS, load_n=round(total_load_n, 1),
                screws=LIFT_SCREWS,
                load_per_screw_n=round(per_screw_n, 1),
                torque_per_screw_nm=round(torque_per_screw, 4),
                lead_mm=LEAD_MM, torque_needed_nm=round(torque_total, 4),
                motor_torque_nm=LIFT_MOTOR_TORQUE_NM,
                margin=round(LIFT_MOTOR_TORQUE_NM / max(torque_total, 1e-9), 2),
                passes=bool(torque_total < LIFT_MOTOR_TORQUE_NM))


def reset_carriage_axis() -> dict:
    """Banked reset-carriage torque gate (DND-74/91 Attack 5 fix).

    The carriage hauls ONE banked release comb at a time, so its load is the
    banked all-armed release force (not the global board). Previously the
    reset motor was never gated at all.
    """
    load_n = release_force()["banked_all_armed_n"]
    torque = _screw_torque_nm(load_n)
    return dict(cells_released=CELLS_PER_BANK, load_n=round(load_n, 1),
                lead_mm=LEAD_MM, torque_needed_nm=round(torque, 4),
                motor_torque_nm=RESET_MOTOR_TORQUE_NM,
                margin=round(RESET_MOTOR_TORQUE_NM / max(torque, 1e-9), 2),
                passes=bool(torque < RESET_MOTOR_TORQUE_NM),
                evidence="CALCULATION over the banked release force + small-stepper rating")


def timing() -> dict:
    """Full-map time: 4 GLOBAL broadcast strokes + 8 serial banked resets.

    DND-74/DND-91 Attack 4/6 fix: the earlier model priced only strokes and
    reset dwells. The mask gate must re-index between the four threshold
    strokes, and the travelling reset carriage must *traverse* the 406.4 mm
    board between banks. Both are now explicit assumption-class terms.
    """
    stroke_up_s = STROKE_MM / PLATEN_SPEED_MM_S
    per_stroke = stroke_up_s + SETTLE_S + RETURN_S
    armed = STROKES * per_stroke
    mask_index = STROKES * MASK_INDEX_S
    traverse = (BANKS - 1) * CARRIAGE_TRAVERSE_S
    reset_total = BANKS * RESET_S
    full = armed + mask_index + traverse + reset_total
    return dict(strokes=STROKES, banks_reset=BANKS,
                stroke_up_s=round(stroke_up_s, 4),
                per_stroke_s=round(per_stroke, 4),
                armed_strokes_s=round(armed, 4),
                mask_index_s=round(mask_index, 4),
                carriage_traverse_s=round(traverse, 4),
                reset_total_s=round(reset_total, 4),
                full_map_s=round(full, 3),
                clears_30s=bool(full < TIME_GATE_S),
                margin_s=round(TIME_GATE_S - full, 3))


# ---------------------------------------------------------------------------
# Sourced BOM (purchased parts only; printed parts excluded by requirement).
# Every line is a sourced class or a stated allowance. Prices are point-in-time
# sourced-class figures (2026-09). Independent ratification is the
# CostManufacturing child issue of DND-71.
# ---------------------------------------------------------------------------
def bom() -> dict:
    """Complete, conservative purchased BOM (printed parts excluded).

    DELIBERATELY CONSERVATIVE (adversarial-review hardened): the first draft of
    this model omitted the four-screw platen, the reset carriage and the mask
    index. All three are priced here. Prices are sourced-class point-in-time
    figures (2026-09); independent ratification is the CostManufacturing child
    issue of DND-71.
    """
    # --- actuators (the whole cost lever: only 3 bought motors) --------------
    # DND-74 branch 1: global broadcast keeps the full-board lift, so the lift
    # motor is a NEMA23-class (>=2.2 N*m) at ~$30, not the $12 NEMA17.
    lift_motor_usd = 30.00           # NEMA23-class stepper (global-board lift)
    mask_motor_usd = 8.00            # small stepper: mask gate index
    reset_motor_usd = 8.00           # small stepper: travelling reset carriage
    # --- platen: FOUR screws, belt-synchronised (a 406 mm platen cannot be
    #     held flat and non-racking on one edge screw) -----------------------
    screw_set_usd = 24.00            # 4x T8 lead screw + anti-backlash nut, <=2 mm lead
    belt_set_usd = 12.00             # timing belt + 2 pulleys for 4-screw sync
    couplers_usd = 6.00              # 4 motor couplers / thrust washers
    guides_usd = 14.00               # guide rods + bushings, platen guidance
    # --- electronics: one integrated controller + 3 driver channels ----------
    controller_usd = 5.00            # RP2040 (LCSC C2040) sourced
    driver_usd = 4.77                # 3x DRV8833PWPR-class (lift, mask, reset)
    # --- structure / electrical (frame is PRINTED, excluded) -----------------
    power_usd = 12.00                # 24 V 2 A class
    wiring_usd = 14.00               # loom + connectors (sourced class)
    fasteners_usd = 8.00             # M3 assortment (sourced class)
    sensors_usd = 4.00               # 4 axis/datum sensors
    spares_usd = 8.00                # spares allowance (kept, DND-46 policy)
    # --- DND-74/91 Attack 1: the six HONEST allowances the first draft
    #     omitted. Each is a real required capability, priced at
    #     allowance-class retail (2026-09).                            ---------
    mask_index_mech_usd = 15.00      # mask rack/pinion/cam + 8 gate linkages
    carriage_rail_usd = 20.00        # reset carriage rail + carriage frame
    thrust_bearings_usd = 18.00      # 4x thrust bearings (axial ~2,560 N global)
    homing_switches_usd = 3.00       # homing/limit switches (>=6 axes)
    cable_chain_usd = 8.00           # cable chain / strain relief (moving carriage)
    power_conn_usd = 5.00            # power connector / switch / fuse

    lines = [
        ("Lift motor (NEMA23-class stepper)", 1, lift_motor_usd,
         "sourced-class", "global-board lift (DND-74 branch 1); 4-screw belt-synced"),
        ("Mask gate index motor (small stepper)", 1, mask_motor_usd,
         "sourced-class", "sets the 8 bank mask gates"),
        ("Reset carriage motor (small stepper)", 1, reset_motor_usd,
         "sourced-class", "traverses the 8 banked release combs"),
        ("4x T8 lead screw + anti-backlash nut", 1, screw_set_usd,
         "sourced-listing", "<= 2 mm lead (DND-43); non-racking platen"),
        ("Timing belt + 2 pulleys (4-screw sync)", 1, belt_set_usd,
         "sourced-class", "synchronises the four screws"),
        ("Motor couplers + thrust washers", 1, couplers_usd,
         "sourced-class", "axial take-out"),
        ("Guide rods + bushings (platen)", 1, guides_usd,
         "sourced-class", "lateral guidance"),
        ("Controller (RP2040/ESP32)", 1, controller_usd,
         "sourced-live", "RP2040 C2040"),
        ("Stepper driver module (DRV8833-class)", 3, driver_usd / 3,
         "sourced-live", "lift + mask + reset; no 80-channel head"),
        ("Power supply + protection (24 V)", 1, power_usd,
         "sourced-listing", "smaller than S5's 35 VA"),
        ("Wire / connectors / loom", 1, wiring_usd,
         "sourced-class", "few actuators -> small loom"),
        ("Fasteners (M3 assortment)", 1, fasteners_usd,
         "sourced-class", "assortment"),
        ("Axis reference sensors", 4, sensors_usd / 4,
         "sourced-class", "datum only; no per-cell feedback"),
        ("Spares and miscellaneous", 1, spares_usd,
         "assumption", "kept per DND-46 policy"),
        ("Mask index mechanism (rack/cam + 8 linkages)", 1, mask_index_mech_usd,
         "allowance", "DND-91 A5: real required capability, was unlisted"),
        ("Reset carriage rail + frame hardware", 1, carriage_rail_usd,
         "allowance", "DND-91 A5: carriage traverses 406.4 mm, was unpriced"),
        ("Thrust bearings (4x, axial 2,560 N)", 1, thrust_bearings_usd,
         "allowance", "DND-91 A5: global lift axial load, was unpriced"),
        ("Homing / limit switches (6 axes)", 1, homing_switches_usd,
         "allowance", "DND-91 A5: only 4 datum sensors priced before"),
        ("Cable chain / strain relief", 1, cable_chain_usd,
         "allowance", "DND-91 A5: moving reset carriage"),
        ("Power connector / switch / fuse", 1, power_conn_usd,
         "allowance", "DND-91 A5: PSU protection hardware"),
    ]
    rows = [dict(item=n, qty=q, unit=round(u, 4), ext=round(q * u, 2),
                 evidence=e, use=use) for (n, q, u, e, use) in lines]
    parts = round(sum(r["ext"] for r in rows), 2)
    delivered = round(parts * UPLIFT, 2)
    return dict(lines=rows, purchased_parts_usd=parts,
                delivered_usd=delivered,
                printed_parts_excluded=True,
                bought_actuators=3,
                cost_gate_usd=COST_GATE_USD,
                clears_parts=bool(parts < COST_GATE_USD),
                clears_delivered=bool(delivered < COST_GATE_USD),
                margin_delivered_usd=round(COST_GATE_USD - delivered, 2),
                note="Honest conservative BOM: 3 bought motors (NEMA23-class "
                     "global-board lift, mask index, reset carriage), 4-screw "
                     "belt-synced platen, integrated controller, PLUS the six "
                     "DND-91 A5 allowances (mask index mechanism, carriage rail, "
                     "thrust bearings, homing switches, cable chain, power "
                     "protection). No per-cell and no per-row bought actuator "
                     "exists. Printed frame, columns, pawls, masks and release "
                     "combs are excluded per the DND-70 requirement; the card "
                     "puncher, if used, is a shared tool, not machine BOM.")


def sensitivity() -> dict:
    """Break-even values: what would flip each gate (the discriminating numbers)."""
    # Per-stroke overhead headroom at the chosen platen speed (mask index +
    # carriage traverse now consume part of it -- DND-74/DND-91 Attack 4/6).
    stroke_up_s = STROKE_MM / PLATEN_SPEED_MM_S
    travel_s = STROKES * MASK_INDEX_S + (BANKS - 1) * CARRIAGE_TRAVERSE_S
    allowed_armed = TIME_GATE_S - BANKS * RESET_S - travel_s
    allowed_per_stroke = allowed_armed / STROKES
    allowed_overhead = allowed_per_stroke - stroke_up_s
    # Minimum platen speed if the assumed overheads were doubled.
    min_speed = (STROKES * STROKE_MM) / (
        TIME_GATE_S - BANKS * RESET_S - STROKES * (SETTLE_S + RETURN_S) - travel_s)
    # Max banks (rows/bank) at the chosen speed/overheads.
    max_banks = TIME_GATE_S - STROKES * (stroke_up_s + SETTLE_S + RETURN_S) - travel_s
    return dict(
        per_stroke_overhead_headroom_s=round(allowed_overhead, 4),
        chosen_settle_plus_return_s=round(SETTLE_S + RETURN_S, 4),
        mask_plus_traverse_s=round(travel_s, 4),
        min_platen_speed_mm_s_for_30s=round(min_speed, 3),
        max_banks_for_30s_at_reset_s=int(max_banks // RESET_S),
        cost_headroom_parts_usd=round(COST_GATE_USD - bom()["purchased_parts_usd"], 2),
        cost_headroom_delivered_usd=round(COST_GATE_USD - bom()["delivered_usd"], 2),
        release_force_headroom_n=round(
            structural_release_limit_n()["bank_limit_n"]
            - release_force()["banked_all_armed_n"], 1))


def decide() -> dict:
    fit = column_fit()
    rel = release_force()
    lift = lift_axis()
    reset = reset_carriage_axis()
    tm = timing()
    b = bom()
    gates = {
        "G1_cell_fit": fit["fits"],
        "G2_worst_case_release_banked": rel["banked_ok"],
        "G3_lift_axis_torque": lift["passes"],
        "G4_full_map_under_30s": tm["clears_30s"],
        "G5_cost_under_250_parts": b["clears_parts"],
        "G6_cost_under_250_delivered": b["clears_delivered"],
        "G7_reset_carriage_torque": reset["passes"],
    }
    return dict(
        machine="S6-LC",
        evidence_class="CALCULATION over sourced FDM limits + sourced actuator "
                       "ratings; CAD geometry; no print, no purchase, no "
                       "measurement (DND-27)",
        gates=gates, all_gates_pass=bool(all(gates.values())),
        verdict="PROMOTE_TO_09" if all(gates.values()) else "REJECT",
        residual_uncertainty=[
            "Mask preparation is OFF the visible 30 s budget: a genuinely "
            "unannounced map needs punched-card prep first (product statement).",
            "Pawl release-force spread across 6,400 printed parts is the S1-D "
            "risk; break-even sd ~9% of mean, typical FDM spread 10-20% "
            "(assumption) -- per-bank masks bound the force, not the spread.",
            "The platen is assumed unloaded while writing (miniatures off the "
            "region being written), otherwise hold and lift compete.",
            "No per-cell feedback: a missed pawl is a silent local height error "
            "(same class as S5/S5-R).",
            "As-printed friction mu, pocket sharpness and pawl creep are "
            "measurement-only (un-retirable under DND-27).",
            "The pawl spring is computed on the 0.90 mm root block, not the "
            "0.45 mm CAD leaf (DND-91 A2, 8x); there is no hold-force gate. "
            "This is a real open defect (tracked as a follow-up fix issue).",
            "The CAD pawl overflows the 5.08 mm pitch band by 0.260 mm "
            "(DND-91 A1); the G1 lane check is a geometry budget, not a "
            "placement check. Real open defect (follow-up fix issue).",
        ],
    )


def screen() -> dict:
    return dict(
        evidence_class="CALCULATION + CAD (DND-27); no print/purchase/measurement",
        geometry=dict(pitch_mm=PITCH_MM, rows=ROWS, cols=COLS, cells=CELLS,
                      travel_mm=TRAVEL_MM, active_mm=ACTIVE_MM,
                      banks=BANKS, cells_per_bank=CELLS_PER_BANK),
        column_fit=column_fit(),
        pawl=pawl_spring(),
        release_force=release_force(),
        structural_release_limit=structural_release_limit_n(),
        lift_axis=lift_axis(),
        reset_carriage_axis=reset_carriage_axis(),
        timing=timing(),
        bom=bom(),
        sensitivity=sensitivity(),
        decision=decide(),
    )


if __name__ == "__main__":
    print(json.dumps(screen(), indent=2))
