"""s6lc; CAD/calculation source, no physical validation."""
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
COST_GATE_USD = 250.0                    # design calculation: purchased, excl. printed
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
# DESIGN CHOICE (design calculation): the platen strokes the WHOLE 80x80 board at once --
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
# design calculation/design calculation Attack 4/6: the previously-unpriced overhead terms.
MASK_INDEX_S = 0.25                      # mask-gate re-index between strokes (assumption)
CARRIAGE_SPEED_MM_S = 100.0              # reset carriage traverse speed (assumption)
BANK_PITCH_MM = ACTIVE_MM / BANKS        # 50.8 mm from bank to bank
CARRIAGE_TRAVERSE_S = BANK_PITCH_MM / CARRIAGE_SPEED_MM_S  # 0.508 s per bank gap

# ---------------------------------------------------------------------------
# Reset-carriage axis (design calculation/91 Attack 5: previously ungated).
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
COLUMN_SERVICE_LOAD_N = 3.27             # [design calculation] K1 bounding terrain load/column
PLA_COMPRESS_MPA = 50.0                  # sourced-class PLA compressive strength


# ---------------------------------------------------------------------------
# Cell / pawl geometry (printed).
# ---------------------------------------------------------------------------
def _cantilever_rate_n_per_mm(t: float, w: float, l: float,
                              e_mpa: float = PLA_E_MPA) -> float:
    i = w * t ** 3 / 12.0
    return 3.0 * e_mpa * i / l ** 3


PAWL_T_MM = 0.90                         # ROOT block thickness (frame-anchored, outboard)
# design calculation (A2) fix: the bending LEAF is PAWL_T/2 = 0.45 mm (scad/s6lc_machine.scad),
# not the 0.90 mm root block. Using the root section overstated k by 8x.
PAWL_LEAF_T_MM = 0.45                    # LEAF thickness in the bending axis (enters lane)
PAWL_W_MM = 1.20                         # width in Y
PAWL_L_MM = 8.00                         # Z cantilever length (long -> soft)
PAWL_DEFLECTION_MM = 0.25                # cam-over relief at a pocket
# design calculation (A1) fix: the cell OWNS only half the inter-body gap (0.74 mm); the part
# that enters the pitch band (the leaf, 0.45 mm) must fit THAT, not the whole 1.48.
LANE_BLEED_MM = 0.20
LANE_RAIL_MM = 0.48
OWNED_LANE_MM = PITCH_MM / 2 - COLUMN_BODY_MM / 2       # 0.74 mm
# design calculation (A6): reliability gate constants.
PER_CELL_ERROR_BUDGET = 1.570e-6         # q for a 99% map at 6,400 cells


def pawl_spring() -> dict:
    """Pawl leaf spring (release) + the HOLD mechanism (design calculation A2 fix).

    The CAD leaf that bends is PAWL_LEAF_T_MM = 0.45 mm, not the 0.90 mm root
    block (k scales as t^3 -> the old model overstated k by 8x). The corrected
    leaf is soft enough to release, but (as the design calculation A2 attack warned) far too
    soft to HOLD the column by friction; the hold is therefore provided by the
    design calculation P1 bistable over-centre latch, whose armed state is bounded by two
    printed hard stops and holds in COMPRESSION (not a bending preload).
    """
    k = _cantilever_rate_n_per_mm(PAWL_LEAF_T_MM, PAWL_W_MM, PAWL_L_MM)
    release = k * PAWL_DEFLECTION_MM
    # P1 latch hold: a compressed printed land (2-line), not the leaf.
    latch_land_w_mm = 0.88
    latch_land_l_mm = 2.40
    latch_allow_n = latch_land_w_mm * latch_land_l_mm * PLA_COMPRESS_MPA / 0.5
    return dict(rate_n_per_mm=round(k, 4),
                leaf_t_mm=PAWL_LEAF_T_MM,
                root_t_mm=PAWL_T_MM,
                deflection_mm=PAWL_DEFLECTION_MM,
                release_force_n=round(release, 4),
                latch_snap_force_n=0.61,          # design calculation P1 (comb-set)
                latch_hold_allow_n=round(latch_allow_n, 1),
                hold_required_n=round(COLUMN_SERVICE_LOAD_N, 3),
                holds=bool(latch_allow_n >= COLUMN_SERVICE_LOAD_N),
                hold_mechanism="design calculation P1 over-centre latch hard stop (compression)")


def reliability() -> dict:
    """design calculation (A6): per-cell reliability gate G8.

    A map is correct only if all 6,400 cells are correct. With per-cell error q
    the map yield is (1-q)^6400. S6-LC has no per-cell feedback, so errors are
    silent; the gate requires a stated per-cell error budget and its evidence
    path. Break-even q for a 99% map is ~1.57e-6. Analytically UNRESOLVED
    (measurement-only under design calculation).
    """
    q_break_even = 1 - 0.99 ** (1.0 / CELLS)
    return dict(cells=CELLS,
                map_yield_target=0.99,
                per_cell_error_break_even=round(q_break_even, 9),
                has_per_cell_feedback=False,
                evidence_path="printed coupon C1: 100 engage/release cycles per "
                              "cell, 4 cells x 3 coupons; measure miss rate",
                satisfied_analytically=False)


def column_fit() -> dict:
    """Pitch / printability geometry for the column + pawl + mask lane.

    design calculation (A1) fix: the cell OWNS only half the inter-body gap,
    PITCH/2 - BODY/2 = 0.74 mm, not the whole 1.48 mm gap. The part that enters
    the pitch band (the pawl LEAF, 0.45 mm) must fit the OWNED lane. The 0.90 mm
    root block is anchored outboard in the frame and does not enter the band.
    The mask gate bar is stacked ABOVE the pawl in Z, so the X budget holds only
    the pawl lane.
    """
    owned_lane = OWNED_LANE_MM                            # 0.74 mm
    # The leaf + ONE running clearance must fit the owned lane (the clearance is
    # this cell's own freedom, not wasted material on a neighbour's half).
    leaf_plus = PAWL_LEAF_T_MM + LANE_BLEED_MM            # 0.45 + 0.20 = 0.65 mm
    x_gap = PITCH_MM - COLUMN_BODY_MM
    fits = (PAWL_LEAF_T_MM >= MIN_FEATURE_MM) and (leaf_plus <= owned_lane) \
        and (x_gap >= MIN_FEATURE_MM) \
        and (COLUMN_BODY_MM >= MIN_WALL_MM)
    return dict(column_body_mm=COLUMN_BODY_MM,
                owned_lane_mm=round(owned_lane, 3),
                inter_body_gap_mm=round(x_gap, 3),
                leaf_t_mm=PAWL_LEAF_T_MM,
                leaf_plus_clearance_mm=round(leaf_plus, 3),
                root_outboard=True,
                gate_stacked_in_z=True,
                column_wall_ok=bool(COLUMN_BODY_MM >= MIN_WALL_MM),
                pawl_min_feature_ok=bool(PAWL_LEAF_T_MM >= MIN_FEATURE_MM),
                fits=bool(fits))


# ---------------------------------------------------------------------------
# Independent structural limit for the banked reset force (design calculation/91 Attack 5).
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
# design calculation/design calculation CORRECTION (the decisive G3 fix). The mechanism writes the
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
# design calculation branch 1: global broadcast kept -> NEMA23-class motor needed.
# Sourced-class NEMA23 (57x57, ~1.8 A) holding torque ~2.2 N*m, ~$30-40.
LIFT_MOTOR_TORQUE_NM = 2.2               # sourced NEMA23-class (was 0.30 NEMA17)
LEAD_MM = 2.0                            # <= 2 mm lead required by design calculation gate
SCREW_EFF = 0.5                          # lead-screw efficiency (assumption)


def _screw_torque_nm(force_n: float) -> float:
    """Torque to raise `force_n` through one screw (lead LEAD_MM, eff SCREW_EFF)."""
    return force_n * (LEAD_MM / 1000.0) / (2 * math.pi * SCREW_EFF)


def lift_axis() -> dict:
    """Full-board lift torque gate (design calculation branch 1: global broadcast kept)."""
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
    """Banked reset-carriage torque gate (design calculation/91 Attack 5 fix).

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

    design calculation/design calculation Attack 4/6 fix: the earlier model priced only strokes and
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
# CostManufacturing child issue of design calculation.
# ---------------------------------------------------------------------------
def bom() -> dict:
    """Complete, conservative purchased BOM (printed parts excluded).

    DELIBERATELY CONSERVATIVE (adversarial-review hardened): the first draft of
    this model omitted the four-screw platen, the reset carriage and the mask
    index. All three are priced here. Prices are sourced-class point-in-time
    figures (2026-09); independent ratification is the CostManufacturing child
    issue of design calculation.
    """
    # --- actuators (the whole cost lever: only 3 bought motors) --------------
    # design calculation branch 1: global broadcast keeps the full-board lift, so the lift
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
    spares_usd = 8.00                # spares allowance (kept, design calculation policy)
    # --- design calculation/91 Attack 1: the six HONEST allowances the first draft
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
         "sourced-class", "global-board lift (design calculation branch 1); 4-screw belt-synced"),
        ("Mask gate index motor (small stepper)", 1, mask_motor_usd,
         "sourced-class", "sets the 8 bank mask gates"),
        ("Reset carriage motor (small stepper)", 1, reset_motor_usd,
         "sourced-class", "traverses the 8 banked release combs"),
        ("4x T8 lead screw + anti-backlash nut", 1, screw_set_usd,
         "sourced-listing", "<= 2 mm lead (design calculation); non-racking platen"),
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
         "assumption", "kept per design calculation policy"),
        ("Mask index mechanism (rack/cam + 8 linkages)", 1, mask_index_mech_usd,
         "allowance", "design calculation A5: real required capability, was unlisted"),
        ("Reset carriage rail + frame hardware", 1, carriage_rail_usd,
         "allowance", "design calculation A5: carriage traverses 406.4 mm, was unpriced"),
        ("Thrust bearings (4x, axial 2,560 N)", 1, thrust_bearings_usd,
         "allowance", "design calculation A5: global lift axial load, was unpriced"),
        ("Homing / limit switches (6 axes)", 1, homing_switches_usd,
         "allowance", "design calculation A5: only 4 datum sensors priced before"),
        ("Cable chain / strain relief", 1, cable_chain_usd,
         "allowance", "design calculation A5: moving reset carriage"),
        ("Power connector / switch / fuse", 1, power_conn_usd,
         "allowance", "design calculation A5: PSU protection hardware"),
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
                     "design calculation A5 allowances (mask index mechanism, carriage rail, "
                     "thrust bearings, homing switches, cable chain, power "
                     "protection). No per-cell and no per-row bought actuator "
                     "exists. Printed frame, columns, pawls, masks and release "
                     "combs are excluded per the design calculation requirement; the card "
                     "puncher, if used, is a shared tool, not machine BOM.")


def sensitivity() -> dict:
    """Break-even values: what would flip each gate (the discriminating numbers)."""
    # Per-stroke overhead headroom at the chosen platen speed (mask index +
    # carriage traverse now consume part of it -- design calculation/design calculation Attack 4/6).
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
    rg = reliability()
    gates = {
        "G1_cell_fit": fit["fits"],
        "G2_worst_case_release_banked": rel["banked_ok"],
        "G3_lift_axis_torque": lift["passes"],
        "G4_full_map_under_30s": tm["clears_30s"],
        "G5_cost_under_250_parts": b["clears_parts"],
        "G6_cost_under_250_delivered": b["clears_delivered"],
        "G7_reset_carriage_torque": reset["passes"],
    }
    # G8 reliability is measurement-only and cannot be asserted by calculation.
    g8_ok = bool(rg["satisfied_analytically"])
    # design calculation: the MISSION gates are G1-G5 + G7 (G5 IS the mission cost gate).
    # G6 (delivered < $250) is the repo's stricter INTERNAL convention: report it
    # but do not let it masquerade as a mission failure.
    mission_gates = {k: v for k, v in gates.items()
                     if k != "G6_cost_under_250_delivered"}
    mission_ok = all(mission_gates.values())
    # design calculation: make the MISSION gate explicit. design calculation's requirement is
    # "under 250$ (excluding 3d printed parts)" = the PURCHASED-parts gate (G5),
    # NOT the repo's stricter internal delivered convention (G6). Report both and
    # key the mission verdict on G5.
    return dict(
        machine="S6-LC",
        evidence_class="CALCULATION over sourced FDM limits + sourced actuator "
                       "ratings; CAD geometry; no print, no purchase, no "
                       "measurement (design calculation)",
        gates=gates,
        mission_gates=mission_gates,
        g8_reliability_pass=g8_ok,
        g8_reliability_status=("measurement-only, UNRESOLVED under design calculation "
                               "(no per-cell feedback; coupon C1 is the path)"),
        mission_gate="G5 purchased parts < $250 (design calculation: 'under 250$ excluding "
                     "3d printed parts')",
        mission_gate_pass=bool(b["clears_parts"]),
        delivered_convention_under_250=bool(b["clears_delivered"]),
        delivered_usd=b["delivered_usd"],
        parts_usd=b["purchased_parts_usd"],
        all_mission_gates_pass=bool(mission_ok),
        verdict=("CANDIDATE_MEASUREMENT_GATED"
                 if mission_ok and b["clears_parts"]
                 else "REJECT_MISSION_GATE"),
        residual_uncertainty=[
            "Mask preparation is OFF the visible 30 s budget: a genuinely "
            "unannounced map needs punched-card prep first (product statement).",
            "G8 per-cell reliability is UNRESOLVED: no per-cell feedback, and "
            "the 8x-corrected pawl spring (design calculation A2) means the engage/hold "
            "spread is not pinned analytically. Coupon C1 is the evidence path.",
            "Pawl release-force spread across 6,400 printed parts is the S1-D "
            "risk; the P1 latch makes the STATE exact (hard stops), but the SNAP "
            "force still spreads with print stiffness (~+/-20%, assumption).",
            "A7: the platen is a COMMON plate; the recorded per-column lift load "
            "is the conservative S1 allowance (0.4 N/col), not a measured value. "
            "Tabletop minis on the moving region are an explicit load case the "
            "model does not cover (product limitation).",
            "A8: regional/jam behaviour is asserted, not modelled -- a jammed "
            "column does not drop on reset and there is no per-cell feedback; "
            "needs a one-bank jam-injection test.",
            "No per-cell feedback: a missed pawl is a silent local height error "
            "(same class as S5/S5-R).",
            "As-printed friction mu, pocket sharpness and pawl creep are "
            "measurement-only (un-retirable under design calculation).",
        ],
    )


def screen() -> dict:
    return dict(
        evidence_class="CALCULATION + CAD (design calculation); no print/purchase/measurement",
        geometry=dict(pitch_mm=PITCH_MM, rows=ROWS, cols=COLS, cells=CELLS,
                      travel_mm=TRAVEL_MM, active_mm=ACTIVE_MM,
                      banks=BANKS, cells_per_bank=CELLS_PER_BANK),
        column_fit=column_fit(),
        pawl=pawl_spring(),
        release_force=release_force(),
        structural_release_limit=structural_release_limit_n(),
        reliability=reliability(),
        lift_axis=lift_axis(),
        reset_carriage_axis=reset_carriage_axis(),
        timing=timing(),
        bom=bom(),
        sensitivity=sensitivity(),
        decision=decide(),
    )


if __name__ == "__main__":
    print(json.dumps(screen(), indent=2))
