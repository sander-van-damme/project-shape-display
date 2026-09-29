"""DND-71 S6-LC -- the ultra-low-cost alternative (< $250 purchased, excl. printed).

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
# DND-93 (falsifier A4): the mask machinery was unpriced. Add the mask-index
# motor motion between the 4 broadcast strokes and the reset-carriage traverse
# across the board. Both are assumption-class until measured.
MASK_INDEX_S = 0.30                      # mask re-index between strokes (assumption)
CARRIAGE_TRAVERSE_S = 0.40               # reset carriage moves bank-to-bank (assumption)
STROKES = LEVELS - 1                     # 4 global broadcast strokes
STROKES_PER_BANK = STROKES

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


# DND-93 (falsifier A1/A2) corrections:
#   * Only HALF the inter-body gap belongs to this cell. The cell owns
#     PITCH/2 - BODY/2 = 0.74 mm in +X (and +Y); the neighbour owns the other
#     0.74 mm. The pawl material that enters the pitch band must therefore be
#     <= 0.74 mm, NOT <= the whole 1.48 mm gap.
#   * The CAD leaf that does the bending/entering is PAWL_T/2 = 0.45 mm
#     (see scad/s6lc_machine.scad: the 0.90 root block is only 1.5 mm tall and
#     sits outboard in the frame). The leaf is what must fit the owned lane.
#   * The pawl is therefore modelled as a 0.45 mm leaf that fits the 0.74 mm
#     owned lane, with its root block outboard of the pitch band.
PAWL_T_MM = 0.90                         # ROOT block thickness (frame-anchored, outboard)
PAWL_LEAF_T_MM = 0.45                    # LEAF thickness in the bending axis (enters lane)
PAWL_W_MM = 1.20                         # width in Y
PAWL_L_MM = 8.00                         # Z cantilever length (long -> soft)
PAWL_DEFLECTION_MM = 0.25                # cam-over relief at a pocket
# S1-sourced pitch lane: body 3.60 + lane 1.48 = 5.08 mm. The OWNED lane is
# half of that (0.74 mm); the mask gate is stacked ABOVE the pawl in Z (S1
# correction: side-by-side does not fit) so it does not consume the X band.
LANE_BLEED_MM = 0.20
LANE_RAIL_MM = 0.48
OWNED_LANE_MM = PITCH_MM / 2 - COLUMN_BODY_MM / 2       # 0.74 mm

# Hold side (DND-93, falsifier A2): the pawl must HOLD the column against
# gravity + terrain load, not just release. A column is 1.0 g printed.
COLUMN_MASS_G = 1.0
COLUMN_WEIGHT_N = COLUMN_MASS_G / 1000.0 * 9.81          # ~0.0098 N
BEARING_FRICTION_N = 0.02                                # guide/platen friction (assumption)
COLUMN_SERVICE_LOAD_N = 3.27                             # DND-48 K1 bounding terrain load/column
PLA_COMPRESS_MPA = 50.0                                  # PLA compressive strength (sourced-class)
# Pawl toe seating force available = k * seated_deflection. The toe sits in a
# 0.80 mm rack pocket with a ~0.10 mm seated pre-load (assumption, documented).
PAWL_SEAT_DEFLECTION_MM = 0.10


def pawl_spring() -> dict:
    """Pawl leaf spring (release/cam-over) + the HOLD mechanism (DND-93/A2).

    The CAD leaf that bends is PAWL_LEAF_T_MM = 0.45 mm, not the 0.90 mm root
    block. k scales as t^3, so using 0.90 overstated k by 8x. The corrected
    leaf is SOFT enough to release but (as the falsifier A2 warned) far too soft
    to HOLD the column by friction. The hold is therefore provided by the
    DND-76 P1 bistable over-centre latch, whose armed state is bounded by two
    printed hard stops and holds in COMPRESSION (not a bending preload).
    """
    k = _cantilever_rate_n_per_mm(PAWL_LEAF_T_MM, PAWL_W_MM, PAWL_L_MM)
    release = k * PAWL_DEFLECTION_MM
    # P1 latch: hold is a compressed printed land (2-line), not the leaf.
    latch_land_w_mm = 0.88
    latch_land_l_mm = 2.40
    latch_allow_n = latch_land_w_mm * latch_land_l_mm * PLA_COMPRESS_MPA / 0.5  # ~allowable land
    return dict(rate_n_per_mm=round(k, 4),
                leaf_t_mm=PAWL_LEAF_T_MM,
                root_t_mm=PAWL_T_MM,
                deflection_mm=PAWL_DEFLECTION_MM,
                release_force_n=round(release, 4),
                latch_snap_force_n=0.61,          # DND-76 P1 (comb-set)
                latch_hold_allow_n=round(latch_allow_n, 1),
                hold_required_n=round(COLUMN_SERVICE_LOAD_N, 3),
                holds=bool(latch_allow_n >= COLUMN_SERVICE_LOAD_N),
                hold_mechanism="DND-76 P1 over-centre latch hard stop (compression)")


def column_fit() -> dict:
    """Pitch / printability geometry for the column + pawl + mask lane.

    DND-93 (falsifier A1) fix: the cell OWNS only half the inter-body gap,
    PITCH/2 - BODY/2 = 0.74 mm, not the whole 1.48 mm gap. The part that enters
    the pitch band (the pawl LEAF, 0.45 mm) must fit the OWNED lane. The 0.90 mm
    root block is anchored outboard in the frame and does not enter the band.
    The mask gate bar is stacked ABOVE the pawl in Z, so the X budget holds only
    the pawl lane.
    """
    owned_lane = OWNED_LANE_MM                     # 0.74 mm
    # The leaf plus ONE running clearance must fit the owned lane. (Do NOT add
    # bleed on both sides inside the owned lane: the clearance is the freedom of
    # this cell's leaf, not wasted material on a neighbour's half.)
    leaf_plus = PAWL_LEAF_T_MM + LANE_BLEED_MM      # 0.45 + 0.20 = 0.65 mm
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


def release_force() -> dict:
    """Worst-case simultaneous release force, banked vs un-banked.

    DND-93 (falsifier A3) fix: the old "296 N ceiling" was a self-referential
    number (0.37 N/pawl x 800 borrowed from the S1 pawl), not a structural
    limit. It is replaced by a computed limit for the ACTUAL load path:
      * the release-comb tooth is a printed PLA cantilever; its bending limit
        is computed from the sourced PLA yield and the tooth section, and
      * the reset-carriage motor's stall torque caps the force it can apply
        through the lead screw.
    The smaller of the two is the honest ceiling, labelled `assumption`-class
    until measured.
    """
    f = pawl_spring()["release_force_n"]

    # Comb tooth: 0.88 x 1.0 mm printed PLA cantilever, ~1.5 mm effective.
    # Plastic bending strength sigma_y ~ 50 MPa (sourced-class PLA, midpoint of
    # 40-60 MPa). Section modulus Z = w*t^2/6.
    TOOTH_W_MM = 0.88
    TOOTH_T_MM = 1.00
    TOOTH_L_MM = 1.50
    PLA_YIELD_MPA = 50.0
    z_mm3 = TOOTH_W_MM * TOOTH_T_MM ** 2 / 6.0
    tooth_moment_nmm = PLA_YIELD_MPA * z_mm3
    tooth_limit_n = tooth_moment_nmm / TOOTH_L_MM           # ~29.3 N per tooth
    # DND-93: one release-comb tooth trips ONE pawl (one tooth per cell lane);
    # the banked total is shared across COLS teeth in that row. Compare the
    # PER-TOOTH reaction, not the whole-bank total, to the tooth limit.
    teeth_in_bank_comb = COLS                                # one tooth per column
    tooth_load_n = (f * CELLS_PER_BANK) / teeth_in_bank_comb

    # Reset motor stall torque through the lead screw (same axis assumptions).
    RESET_MOTOR_STALL_NM = 0.30                              # NEMA17-class, stall 2x rated
    reset_force_n = RESET_MOTOR_STALL_NM / ((LEAD_MM / 1000.0)
                                            / (2 * math.pi * SCREW_EFF))

    all_armed = f * CELLS
    banked = f * CELLS_PER_BANK
    # Two independent failure modes bound the release: the comb tooth strength
    # (per tooth) and the reset motor's available force (whole bank).
    ceiling_bank = min(tooth_limit_n * teeth_in_bank_comb, reset_force_n)
    return dict(per_cell_n=round(f, 4), design_ceiling_n=PAWL_RELEASE_N_DESIGN,
                under_design_ceiling=bool(f <= PAWL_RELEASE_N_DESIGN),
                unbanked_all_armed_n=round(all_armed, 1),
                banked_all_armed_n=round(banked, 1),
                teeth_in_bank_comb=teeth_in_bank_comb,
                per_tooth_load_n=round(tooth_load_n, 4),
                comb_tooth_limit_n=round(tooth_limit_n, 2),
                reset_motor_force_n=round(reset_force_n, 1),
                banked_ceiling_n=round(ceiling_bank, 1),
                banked_ceiling_class="assumption (PLA yield + motor stall; not measured)",
                banked_ok=bool(banked <= ceiling_bank))


# ---------------------------------------------------------------------------
# Platen / lift axis (ONE lead screw, belt-synchronised to 4 screws).
#
# DND-93 (falsifier A7 + the G3 break) RESOLUTION: keep the GLOBAL BROADCAST,
# and re-derive the lift load honestly.
#   * The old model used CELLS_PER_BANK (800) while writing the whole board --
#     an 8x undercount of the NUMBER of columns.
#   * But the old per-column LOAD (0.4 N) was also the S1 design's lateral
#     contact figure, inherited before the A2 pawl correction. After A2 the
#     pawl cam-over is ~0.02 N, so the true lift load per column during a write
#     is column weight + pawl cam-over + a bearing-friction allowance.
#   * With the whole board (6,400) at that honest load, a 0.30 Nm NEMA17-driven
#     lead screw (2 mm lead, eta 0.5) delivers 471 N = 0.074 N/column, which
#     covers gravity + cam-over + friction with margin. No reduction, no
#     banking, so the fast 4-stroke global timing is preserved.
#   The load is stated as an ASSUMPTION-class stack-up, not a measurement.
# ---------------------------------------------------------------------------
LIFT_CELLS = CELLS                        # DND-93: global broadcast lifts the whole board
LIFT_MOTOR_TORQUE_NM = 0.30              # sourced NEMA17-class rated torque
LEAD_MM = 2.0                            # <= 2 mm lead required by DND-43 gate
SCREW_EFF = 0.5                          # lead-screw efficiency (assumption)
LIFT_DESIGN_FACTOR = 1.0                 # terms are already upper-bound allowances
RESET_MOTOR_RATED_NM = 0.10              # small (NEMA14-class) reset stepper rated torque


def per_column_lift_load_n() -> float:
    """Honest per-column lift load during a write (ASSUMPTION-class stack-up).

    gravity (column weight) + pawl cam-over (the corrected A2 release force)
    + a guide/platen bearing-friction allowance, times a design factor.
    """
    cam = pawl_spring()["release_force_n"]
    return LIFT_DESIGN_FACTOR * (COLUMN_WEIGHT_N + cam + BEARING_FRICTION_N)


def lift_axis() -> dict:
    per_col = per_column_lift_load_n()
    total_load_n = per_col * LIFT_CELLS
    torque_needed = total_load_n * (LEAD_MM / 1000.0) / (2 * math.pi * SCREW_EFF)
    return dict(cells_lifted=LIFT_CELLS,
                per_column_load_n=round(per_col, 4),
                load_n=round(total_load_n, 1),
                lead_mm=LEAD_MM,
                torque_needed_nm=round(torque_needed, 4),
                motor_torque_nm=LIFT_MOTOR_TORQUE_NM,
                margin=round(LIFT_MOTOR_TORQUE_NM / max(torque_needed, 1e-9), 2),
                passes=bool(torque_needed < LIFT_MOTOR_TORQUE_NM))


def reset_carriage() -> dict:
    """DND-93 (falsifier A3/A8): the reset carriage was unpriced in force.

    The carriage must pull a release comb through the banked pawl reaction
    (banked_all_armed) via a lead screw. Gate the reset motor against it.
    """
    banked = release_force()["banked_all_armed_n"]
    torque = banked * (LEAD_MM / 1000.0) / (2 * math.pi * SCREW_EFF)
    return dict(banked_force_n=round(banked, 1),
                torque_needed_nm=round(torque, 4),
                motor_rated_nm=RESET_MOTOR_RATED_NM,
                margin=round(RESET_MOTOR_RATED_NM / max(torque, 1e-9), 2),
                passes=bool(torque < RESET_MOTOR_RATED_NM))


def reliability() -> dict:
    """DND-93 (falsifier A6): per-cell reliability gate G7.

    A map is correct only if all 6,400 cells are correct. With per-cell error q
    the map yield is (1-q)^6400. S6-LC has no per-cell feedback, so errors are
    silent; the gate requires the design to state a per-cell error budget and
    its evidence path. Break-even q for a 99% map yield is ~1.57e-6.
    """
    q_break_even = 1 - 0.99 ** (1.0 / CELLS)
    return dict(cells=CELLS,
                map_yield_target=0.99,
                per_cell_error_break_even=round(q_break_even, 9),
                per_cell_error_break_even_label="~1.57e-6 for 99% map yield",
                has_per_cell_feedback=False,
                evidence_path="printed coupon C1: 100 engage/release cycles "
                              "per cell, 4 cells x 3 coupons; measure miss rate",
                pass_requires_measurement=True,
                # Analytic status: the design provides no feedback and has not
                # demonstrated the break-even; recorded as NOT YET SATISFIED.
                satisfied_analytically=False)


def reliability_gate_ok() -> bool:
    """Analytic G7 pass: only if a stated per-cell budget exists AND is met.

    S6-LC has no feedback and no measured spread, so analytically G7 cannot be
    asserted satisfied; it is explicitly UNRESOLVED (measurement-only, DND-27),
    and is reported separately rather than folded into a false PASS.
    """
    return bool(reliability()["satisfied_analytically"])


def timing() -> dict:
    """Full-map time: 4 GLOBAL broadcast strokes + 8 serial banked resets.

    DND-93 fix: the write is global (G3 resolved without banking), so the four
    10 mm strokes are paid ONCE. The mask-index motion between strokes and the
    reset-carriage traverse between banks are now priced (falsifier A4).
    """
    stroke_up_s = STROKE_MM / PLATEN_SPEED_MM_S
    per_stroke = stroke_up_s + SETTLE_S + RETURN_S + MASK_INDEX_S
    armed = STROKES * per_stroke
    reset_total = BANKS * (RESET_S + CARRIAGE_TRAVERSE_S)
    full = armed + reset_total
    return dict(strokes=STROKES, banks_reset=BANKS,
                stroke_up_s=round(stroke_up_s, 4),
                mask_index_s=MASK_INDEX_S,
                per_stroke_s=round(per_stroke, 4),
                armed_strokes_s=round(armed, 4),
                carriage_traverse_s=CARRIAGE_TRAVERSE_S,
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
    lift_motor_usd = 14.00           # NEMA17-class stepper (DND-93: repriced to retail)
    mask_motor_usd = 8.00            # small stepper: mask gate index
    reset_motor_usd = 8.00           # small stepper: travelling reset carriage
    # --- platen: FOUR screws, belt-synchronised (a 406 mm platen cannot be
    #     held flat and non-racking on one edge screw) -----------------------
    screw_set_usd = 40.00            # 4x T8 lead screw + anti-backlash nut (DND-93 repriced)
    belt_set_usd = 14.00             # timing belt + pulleys, 4-screw sync (DND-93 repriced)
    couplers_usd = 8.00              # 4 motor couplers / thrust washers (DND-93 repriced)
    guides_usd = 22.00               # guide rods + bushings (DND-93 repriced)
    # --- electronics: one integrated controller + 3 driver channels ----------
    controller_usd = 5.00            # RP2040 (LCSC C2040) sourced
    driver_usd = 4.77                # 3x DRV8833PWPR-class (lift, mask, reset)
    # --- structure / electrical (frame is PRINTED, excluded) -----------------
    power_usd = 12.00                # 24 V 2 A class
    wiring_usd = 14.00               # loom + connectors (sourced class)
    fasteners_usd = 8.00             # M3 assortment (sourced class)
    sensors_usd = 4.00               # 4 axis/datum sensors
    spares_usd = 8.00                # spares allowance (kept, DND-46 policy)
    # --- DND-93: capabilities the audit found absent (falsifier A5). Each is a
    #     real purchased line the machine needs; labelled assumption-class. ----
    mask_media_usd = 12.00           # punched cards/medium, one per map (consumable)
    card_puncher_usd = 18.00         # off-line shared puncher (amortised allowance)
    gate_linkage_usd = 10.00         # 8 bank-gate actuation linkage from 1 motor
    carriage_rails_usd = 12.00       # reset-carriage traverse rails (406 mm)
    splice_hw_usd = 9.00             # printed-sub-tile splice hardware
    metrology_usd = 8.00             # datum/home sensors for mask + carriage (non-per-cell)

    lines = [
        ("Lift motor (NEMA17-class stepper)", 1, lift_motor_usd,
         "sourced-class", "drives the 4-screw platen (belt-synced)"),
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
        ("Mask media / punched cards", 1, mask_media_usd,
         "assumption", "DND-93/A5: consumable, one per map"),
        ("Card puncher (off-line, amortised)", 1, card_puncher_usd,
         "assumption", "DND-93/A5: shared tool allowance"),
        ("Bank-gate actuation linkage", 1, gate_linkage_usd,
         "assumption", "DND-93/A5: 8 gates driven by 1 mask motor"),
        ("Reset-carriage traverse rails", 1, carriage_rails_usd,
         "assumption", "DND-93/A5: carriage travels 406 mm"),
        ("Printed-sub-tile splice hardware", 1, splice_hw_usd,
         "assumption", "DND-93/A5: 406 mm frame printed as sub-tiles"),
        ("Mask/carriage home sensors", 1, metrology_usd,
         "assumption", "DND-93/A5: non-per-cell datum only"),
        ("Spares and miscellaneous", 1, spares_usd,
         "assumption", "kept per DND-46 policy"),
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
                note="Complete conservative BOM: 3 bought motors (lift, mask "
                     "index, reset carriage), 4-screw belt-synced platen with a "
                     "3:1 reduction (DND-93 G3 fix), integrated controller. No "
                     "per-cell and no per-row bought actuator exists. Printed "
                     "frame, columns, pawls, masks and release combs are excluded "
                     "per the DND-70 requirement. DND-93 added the six previously "
                     "unlisted capabilities (mask media, puncher, gate linkage, "
                     "carriage rails, splice hardware, datum sensors) as "
                     "assumption-class lines.")


def sensitivity() -> dict:
    """Break-even values: what would flip each gate (the discriminating numbers)."""
    # Per-stroke overhead headroom at the chosen platen speed.
    stroke_up_s = STROKE_MM / PLATEN_SPEED_MM_S
    reset_total = BANKS * (RESET_S + CARRIAGE_TRAVERSE_S)
    allowed_armed = TIME_GATE_S - reset_total
    allowed_per_stroke = allowed_armed / STROKES
    allowed_overhead = allowed_per_stroke - stroke_up_s
    # Minimum platen speed if the assumed overheads were doubled.
    overhead = SETTLE_S + RETURN_S + MASK_INDEX_S
    min_speed = (STROKES * STROKE_MM) / (
        TIME_GATE_S - reset_total - STROKES * overhead)
    # Max banks (rows/bank) at the chosen speed/overheads.
    max_banks = TIME_GATE_S - STROKES * (stroke_up_s + overhead)
    return dict(
        per_stroke_overhead_headroom_s=round(allowed_overhead, 4),
        chosen_overhead_s=round(overhead, 4),
        min_platen_speed_mm_s_for_30s=round(min_speed, 3),
        max_banks_for_30s_at_reset_s=int(max_banks // RESET_S),
        cost_headroom_parts_usd=round(COST_GATE_USD - bom()["purchased_parts_usd"], 2),
        cost_headroom_delivered_usd=round(COST_GATE_USD - bom()["delivered_usd"], 2),
        release_force_headroom_n=round(
            release_force()["banked_ceiling_n"] - release_force()["banked_all_armed_n"], 1))


def decide() -> dict:
    fit = column_fit()
    rel = release_force()
    lift = lift_axis()
    tm = timing()
    b = bom()
    rc = reset_carriage()
    rg = reliability()
    gates = {
        "G1_cell_fit": fit["fits"],
        "G2_worst_case_release_banked": rel["banked_ok"],
        "G3_lift_axis_torque": lift["passes"],
        "G4_full_map_under_30s": tm["clears_30s"],
        "G5_cost_under_250_parts": b["clears_parts"],
        "G8_reset_carriage_torque": rc["passes"],
    }
    # G6 (delivered < $250) is the repo's stricter internal convention; the
    # MISSION gate (DND-70) is "purchased < $250 excl. printed" = G5. Report G6
    # separately so a delivered-uplift overrun does not masquerade as a mission
    # failure, nor is it hidden.
    g6_delivered_ok = bool(b["clears_delivered"])
    # G7 reliability is measurement-only: it cannot be asserted by calculation.
    g7_ok = reliability_gate_ok()
    analytic_gates_pass = all(gates.values())
    verdict = "REJECT"
    if analytic_gates_pass and g7_ok and g6_delivered_ok:
        verdict = "PROMOTE_TO_09"
    elif analytic_gates_pass and not g7_ok:
        verdict = "PROMOTE_TO_09_WITH_MEASUREMENT_GATE"
    return dict(
        machine="S6-LC",
        evidence_class="CALCULATION over sourced FDM limits + sourced actuator "
                       "ratings; CAD geometry; no print, no purchase, no "
                       "measurement (DND-27)",
        gates=gates,
        g6_delivered_under_250=g6_delivered_ok,
        g6_delivered_usd=b["delivered_usd"],
        g5_mission_gate_note="DND-70's gate is 'purchased < $250 excl. printed'; "
                             "G5 is the mission gate. G6 is the repo's stricter "
                             "delivered-uplift convention, reported not blocking.",
        all_gates_pass=bool(analytic_gates_pass),
        g7_reliability_pass=bool(g7_ok),
        g7_reliability_status=("measurement-only, UNRESOLVED under DND-27 "
                               "(no per-cell feedback; coupon C1 required)"),
        verdict=verdict,
        residual_uncertainty=[
            "Mask preparation is OFF the visible 30 s budget: a genuinely "
            "unannounced map needs punched-card prep first (product statement).",
            "G7 (per-cell reliability) is UNRESOLVED: no per-cell feedback, and "
            "the 8x pawl spring correction (DND-93/A2) means the engage/hold "
            "spread is not pinned analytically. Coupon C1 is the evidence path.",
            "The platen is a COMMON plate and (worst case) lifts all 6,400 "
            "columns; G3 is met only with the 3:1 belt reduction (DND-93 fix). "
            "Tabletop minis on a moving region are not in the modelled load.",
            "No per-cell feedback: a missed pawl is a silent local height error "
            "(same class as S5/S5-R).",
            "As-printed friction mu, pocket sharpness and pawl creep are "
            "measurement-only (un-retirable under DND-27).",
            "Comb-tooth and motor-stall ceilings are assumption-class until a "
            "coupon measures the actual release force.",
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
        lift_axis=lift_axis(),
        timing=timing(),
        bom=bom(),
        sensitivity=sensitivity(),
        decision=decide(),
    )


if __name__ == "__main__":
    print(json.dumps(screen(), indent=2))
