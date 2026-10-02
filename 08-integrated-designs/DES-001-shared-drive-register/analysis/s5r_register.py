"""s5r register; CAD/calculation source, no physical validation."""
from __future__ import annotations

import json
import math
from pathlib import Path

UPLIFT = 1.16
BANK_DRIVER_USD = 0.7955
COST_CEILING_USD = 500.0
FIXED_PARTS_NO_CHANNEL = 218.70  # purchased base allowance; no bank channels
import timing_basis as tc

HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# Cell / register geometry at 5.08 mm pitch (mirrored in s5r_register.scad).
# ---------------------------------------------------------------------------
PITCH_MM = 5.08
ROTOR_RADIUS_MM = 1.5          # the rotor geometry (radius_mm)
ROTOR_CORE_RADIUS_MM = 1.0     # parameters.scad (core_radius_mm)
LEVELS = 5
LEVEL_ANGLE_DEG = 360.0 / LEVELS  # 72 deg per level
ROWS = tc.ROWS                 # 80
COLS = 80

# Pawl leaf: a vertical (Z) cantilever, so its length is NOT bounded by the
# 5.08 mm pitch band; only its thickness and width are in-band. The pawl is the
# LOAD-BEARING leaf, so it is 2 lines (0.90 mm) and long (8 mm) to keep the
# force low. A 0.45 mm leaf would be only 1 extrusion line (a print-risk).
PAWL_LENGTH_MM = 8.00          # Z extent of the cantilever
PAWL_T_MM = 0.90               # thickness in X (pitch direction); 2 lines
PAWL_W_MM = 0.70               # width in Y (row direction)
PAWL_DEFLECTION_MM = 0.10      # working deflection off the rack tooth
PAWL_TARGET_FORCE_N = 0.14     # design target; checked against the leaf calc

# Keeper latch: bistable over-centre leaf, 5-position gate.
# design calculation re-profile (residual-KEEPER): the design calculation keeper was 0.45 mm = 1
# extrusion line (RISK), and its hold was a bending-spring force set by the
# over-centre offset (tolerance-fragile). The keeper is now 0.90 mm = 2 lines
# (PASS) and its HOLD is a hard printed shoulder in compression; the leaf only
# trips the snap. A longer leaf (4.00 mm) keeps the snap strain low.
KEEPER_LEAF_T_MM = 0.90
KEEPER_LEAF_L_MM = 4.00
KEEPER_LEAF_W_MM = 0.70
KEEPER_OVER_CENTRE_MM = 0.06   # offset making the detent bistable
KEEPER_GATE_STEP_MM = 0.35     # spacing of the 5 gate positions
KEEPER_LEAF_T_PREVIOUS_MM = 0.45  # superseded (1 line); kept for the record
KEEPER_LEAF_L_PREVIOUS_MM = 3.00

# Drive rack on the shared bar.
# design calculation (design calculation bank close-out): the design calculation rack (pitch 0.60 / tooth 0.45)
# left a 0.15 mm inter-tooth gap that fuses at a 0.4 mm nozzle (< 0.44 mm one
# line). Re-dimensioned to pitch 1.00 / tooth 0.50 (gap 0.50 mm); the
# per-stroke advance (RACK_STROKE_MM) therefore becomes 1.00 mm, not 0.60 mm.
RACK_TOOTH_PITCH_MM = 1.00
RACK_TOOTH_HEIGHT_MM = 0.50
RACK_TOOTH_PITCH_PREVIOUS_MM = 0.60   # superseded (fused); kept for the record
RACK_TOOTH_HEIGHT_PREVIOUS_MM = 0.45
RACK_STROKE_MM = RACK_TOOTH_PITCH_MM   # one forward stroke advances one tooth
                                       # (was RACK_TOOTH_HEIGHT_MM = 0.45; the
                                       #  design calculation correction is pitch-driven)

# Shared drive bar section. design calculation/design calculation replaced the printed 3x2 placeholder
# (which failed bar torsion by ~28x) with a SOURCED steel rod d=6 mm.
BAR_D_MM = 6.0                 # sourced steel drive rod diameter
BAR_D_OPTION_MM = 8.0          # printed round PLA fallback (or sourced rod d=5)
BAR_MATERIAL = "sourced steel rod"   # or "printed PLA round d=8"

# FDM process (sourced limits, tools/fdm-limits/fdm_process_limits.py).
MIN_FEATURE_MM = 0.44          # 1 extrusion line @ 0.4 mm nozzle
MIN_WALL_MM = 0.88             # 2 lines, robust
DIM_ACCURACY_MM = 0.10         # per printed face (assumption, [R4])

# Sourced material / friction constants (DETENT_CONTACT.md / historical sourced estimates).
MU_PLA_MID = 0.35
MU_PLA_LOW = 0.20
MU_PLA_HIGH = 0.50
PLA_E_MPA = 1500.0             # sourced modulus range 700-2500, midpoint

# Service load already bounded by [design calculation]/design calculation (robust register). The latch
# never carries terrain load (the rotor hard stop does), so this is inherited.
K1_SERVICE_BOUNDING_N = 3.27
K1_SERVICE_DISTRIBUTED_N = 0.39

# Unloaded-write resistance per pawl beyond its own spring (rotor detent torque
# reflected to the rack at the unloaded write point). Stated assumption. During
# a write the platen is unloaded, so this is the light rotor detent only.
WRITE_LOAD_N = 0.05

# Bank drive: a fully-orderable NEMA17-class stepper (design calculation). The chosen
# design drives the bar from BOTH ends (BANK_MOTORS=2): that doubles the
# available force and removes bar torsion across a 4-row bank.
BANK_MOTOR_TORQUE_NM = 0.30    # sourced class figure (same as lift motor R7)
BANK_MOTORS = 2
BANK_PINION_RADIUS_MM = 6.0
BUS_EFFICIENCY = 0.6           # stated assumption for the bar/crank bus

# Writer solenoid: small 5 V push solenoid (design calculation writer class).
WRITER_FORCE_N = 1.2
WRITER_SETTLE_S = 0.05         # one comb actuation + settle (assumption)

# Chosen design point (the design calculation correction to design calculation's R=1, W=8).
ROWS_IN_BANK = 4               # bank spans 4 rows -> 20 groups, no pitch penalty
WRITERS = 40                   # 2 stations/groups of 40: writer index < bank pass

# Bank crank speed (assumed; the dominant time assumption, like S5's K6 dwell).
BANK_CRANK_DEG_S = 720.0       # 2 rev/s

# Endurance: same defensible FDM span as design calculation/K11.
ENDURANCE_EPS_SPAN = (0.0020, 0.0030)
ENDURANCE_BASQUIN_M = 8
ENDURANCE_LEAF_STRAIN = (0.05 + 0.20) * 1.5 * 0.45 / (10.0 ** 2)


def _cantilever_rate_n_per_mm(t: float, w: float, l: float,
                              e_mpa: float = PLA_E_MPA) -> float:
    """Printed rectangular cantilever rate k = 3 E I / L^3 (N per mm)."""
    i = w * t ** 3 / 12.0
    return 3.0 * e_mpa * i / l ** 3


def pawl_spring() -> dict:
    k = _cantilever_rate_n_per_mm(PAWL_T_MM, PAWL_W_MM, PAWL_LENGTH_MM)
    f = k * PAWL_DEFLECTION_MM
    return dict(rate_n_per_mm=round(k, 4),
                working_deflection_mm=PAWL_DEFLECTION_MM,
                force_n=round(f, 4), target_n=PAWL_TARGET_FORCE_N,
                within_target=bool(f <= PAWL_TARGET_FORCE_N * 1.5))


def keeper_hold() -> dict:
    k = _cantilever_rate_n_per_mm(KEEPER_LEAF_T_MM, KEEPER_LEAF_W_MM,
                                  KEEPER_LEAF_L_MM)
    hold = k * KEEPER_OVER_CENTRE_MM
    return dict(rate_n_per_mm=round(k, 4),
                over_centre_offset_mm=KEEPER_OVER_CENTRE_MM,
                hold_n=round(hold, 4), release_n=round(hold, 4))


def cell_fit() -> dict:
    """Two-axis geometry: does the pawl + keeper fit the 5.08 mm cell?

    design calculation re-profile (residual-KEEPER): the keeper was 1 line (0.45 mm) and sat
    BEHIND the pawl in the pitch direction (X), so the X-band held pawl+keeper.
    Re-profiling it to 2 lines (0.90 mm) there would consume the free band
    (worst-case gap 0.02 mm < 0.20 mm). The keeper is therefore re-profiled into
    the ROW direction (Y), beside the pawl, where the cell has room: the X-band
    then holds only the pawl, and the Y-band holds pawl+keeper. Both axes clear.

    X-band free width = PITCH - 2R (between rotor edges).
    Y-band free width = PITCH - 2R too (row pitch = column pitch), but the
    pawl+keeper pair is 0.70 + 0.90 = 1.60 mm, inside 2.08 mm.
    """
    rotor_dia = 2.0 * ROTOR_RADIUS_MM
    free_band = PITCH_MM - rotor_dia
    # X: pawl only (keeper moved to Y).
    stack_x = PAWL_T_MM
    stack_x_worst = stack_x + 2.0 * DIM_ACCURACY_MM
    # Y: pawl + keeper side by side.
    stack_y = PAWL_W_MM + KEEPER_LEAF_T_MM
    stack_y_worst = stack_y + 2.0 * DIM_ACCURACY_MM
    # Bounding (worst) axis for the crosstalk gate.
    worst_gap = min(free_band - stack_x_worst, free_band - stack_y_worst)
    return dict(
        pitch_mm=PITCH_MM, rotor_dia_mm=round(rotor_dia, 3),
        free_band_mm=round(free_band, 3),
        keeper_direction="Y (row direction), beside the pawl",
        x_stack_nominal_mm=round(stack_x, 3),
        x_stack_worst_mm=round(stack_x_worst, 3),
        x_tip_gap_worst_mm=round(free_band - stack_x_worst, 3),
        y_stack_nominal_mm=round(stack_y, 3),
        y_stack_worst_mm=round(stack_y_worst, 3),
        y_tip_gap_worst_mm=round(free_band - stack_y_worst, 3),
        in_band_stack_nominal_mm=round(stack_y, 3),
        in_band_stack_worst_mm=round(stack_y_worst, 3),
        stack_inside_band=bool(stack_y_worst <= free_band),
        tip_gap_worst_mm=round(worst_gap, 3),
        fits_worst_case=bool(worst_gap > 0.0),
    )


def neighbour_crosstalk() -> dict:
    """A dropped-out pawl carries zero rack force; cross-talk is a gap."""
    drift = 2.0 * DIM_ACCURACY_MM
    gap = cell_fit()["tip_gap_worst_mm"]
    return dict(dropped_pawl_rack_force_n=0.0, keeper_holds_pawl_clear=True,
                detent_lash_mm=round(drift, 3), worst_tip_gap_mm=gap,
                gap_after_lash_mm=round(gap - drift, 3),
                no_contact=bool(gap - drift > 0.0),
                note="a dropped-out pawl is held clear of the rack by its "
                     "keeper and carries zero drive force; the shared bar "
                     "transmits no per-cell load to a dropped pawl, so "
                     "neighbour cross-talk is a geometry gap, not a force.")


def writer_budget() -> dict:
    kh = keeper_hold()
    pawl = pawl_spring()
    friction = MU_PLA_MID * pawl["force_n"]
    required = kh["release_n"] + friction
    return dict(keeper_release_n=kh["release_n"],
                pawl_normal_n=pawl["force_n"],
                guide_friction_n=round(friction, 4),
                required_solenoid_n=round(required, 4),
                available_solenoid_n=WRITER_FORCE_N,
                margin=round(WRITER_FORCE_N / required, 4) if required else None,
                pass_gate=bool(WRITER_FORCE_N >= required))


def bank_drive_load(rows_in_bank: int) -> dict:
    """Force to stroke a bank of COLS*R ganged pawls through the rack."""
    pawl = pawl_spring()
    per_pawl = pawl["force_n"] + WRITE_LOAD_N
    n = COLS * rows_in_bank
    total = n * per_pawl
    req = total / BUS_EFFICIENCY
    avail = BANK_MOTORS * (BANK_MOTOR_TORQUE_NM * 1000.0) / BANK_PINION_RADIUS_MM
    return dict(rows_in_bank=rows_in_bank, n_pawls=n,
                per_pawl_n=round(per_pawl, 4), total_rack_n=round(total, 3),
                bus_efficiency=BUS_EFFICIENCY, bank_motors=BANK_MOTORS,
                required_motor_force_n=round(req, 3),
                available_motor_force_n=round(avail, 3),
                margin=round(avail / req, 3), pass_gate=bool(avail >= req))


def latch_holding_vs_service() -> dict:
    return dict(terrain_carried_by="rotor hard stop / follower toe (K1 path)",
                latch_load_in_service_n=0.0,
                k1_service_bounding_n=K1_SERVICE_BOUNDING_N,
                k1_service_distributed_n=K1_SERVICE_DISTRIBUTED_N,
                inherits_k1_bound=True,
                note="the latch is dormant while the machine holds terrain "
                     "load; it only holds the pawl clear of the rack during an "
                     "unloaded write. The K1 bound is inherited, not changed.")


def endurance(rows_in_bank: int) -> dict:
    steps_per_group = LEVELS - 1
    groups = math.ceil(ROWS / rows_in_bank)
    strokes_per_map = groups * (steps_per_group + 1)  # +1 reset pass
    strain = ENDURANCE_LEAF_STRAIN
    seen = [(eps / strain) ** ENDURANCE_BASQUIN_M * 1e6
            for eps in ENDURANCE_EPS_SPAN]
    return dict(rows_in_bank=rows_in_bank, groups=groups,
                strokes_per_map=strokes_per_map,
                leaf_strain=round(strain, 6),
                cycles_span=[round(min(seen), 1), round(max(seen), 1)],
                maps_span=[round(min(seen) / strokes_per_map, 1),
                           round(max(seen) / strokes_per_map, 1)],
                label=">=1e6, order unknown")


def timing(rows_in_bank: int) -> dict:
    """Full-map time for the R-row register, built from the mechanism cycle.

    The writer carriage must set every column in the group (COLS * R), so the
    number of station moves scales with R (this is the term design calculation omitted).

    design calculation timing note: the pass is *angular* -- the crank turns LEVEL_ANGLE_DEG
    (72 deg) per level regardless of the rack pitch. The rack re-dimension
    (0.60 -> 1.00 mm pitch, RACK_STROKE_MM = 1.00 mm) changes the per-stroke
    *linear* travel, not the crank angle, so the select/reset times are
    UNCHANGED. It is carried in `rack_stroke_mm` for traceability.
    """
    groups = math.ceil(ROWS / rows_in_bank)
    cells_per_group = COLS * rows_in_bank
    stations = math.ceil(cells_per_group / WRITERS)
    writer_s = stations * WRITER_SETTLE_S
    select_s = (LEVELS - 1) * LEVEL_ANGLE_DEG / BANK_CRANK_DEG_S
    reset_s = LEVEL_ANGLE_DEG / BANK_CRANK_DEG_S
    per_group = writer_s + select_s + reset_s
    full = (tc.fixed_s() + (groups - 1) * tc.index_s() + groups * per_group)
    return dict(rows_in_bank=rows_in_bank, groups=groups,
                cells_per_group=cells_per_group, stations=stations,
                writers=WRITERS,
                rack_stroke_mm=RACK_STROKE_MM,
                crank_deg_per_level=LEVEL_ANGLE_DEG,
                writer_s_per_group=round(writer_s, 4),
                select_pass_s=round(select_s, 4), reset_pass_s=round(reset_s, 4),
                per_group_s=round(per_group, 4),
                full_map_s5r_s=round(full, 3),
                full_map_s5_reference_s=round(tc.full_map_s(400), 3),
                clears_30s=bool(full < 30.0),
                margin_to_30s_s=round(30.0 - full, 3))


def delivered(parts_usd: float) -> float:
    return round(parts_usd * UPLIFT, 2)


# --- Purchased driver channels for the S5-R actuator block -------------------
# The fixed no-channel base (FIXED_PARTS_NO_CHANNEL) has BOTH the 80-motor
# line AND the 80-channel TB6612 driver block removed, by the nx52 contract:
# "every option declares its own channel cost exactly once (no double-count)".
# The S5-R block therefore OWNS its channels:
#   * 2 bank steppers (bipolar) need 2 H-bridge channels. Priced conservatively
#     at 1 dual TB6612 IC per motor (2 ICs) -- the working figure used by the
#     design calculation ratification; the optimistic 1-IC shared case is carried alongside.
#   * 40 writer solenoids are ON/OFF loads: a ULN2803-class 8-channel darlington
#     (~$0.30) switches 8 each -> 5 chips. No H-bridge is needed (design calculation).
# These are marginal-bought-channel parts; the `Custom driver PCBs and passives`
# line stays in the fixed base but was sized for the 80-motor H-bridge head, so
# pricing the S5-R channels explicitly makes the BOM auditable.
BANK_ICS_WORKING = BANK_MOTORS          # 1 dual H-bridge IC per bank motor
BANK_ICS_OPTIMISTIC = 1                 # both motors share one dual IC
BANK_IC_USD = BANK_DRIVER_USD         # $0.7955, LCSC C88224 (E1 source)
WRITER_CHIP_USD = 0.30                  # ULN2803-class 8-ch darlington
WRITER_CHIPS = (WRITERS + 7) // 8       # 5 chips for 40 writers
# The shared drive bar is a SOURCED steel rod (design calculation/design calculation), not a printed
# part. One 6 mm x 406.4 mm ground steel rod is a single commodity line; the
# allowance is a stated sourced-class figure (rod stock ~$6/m retail, cut).
STEEL_ROD_USD = 3.00                    # sourced-class allowance, 1 rod


def bom(rows_in_bank: int) -> dict:
    bank_motors = BANK_MOTORS
    motor_usd = 12.00
    writers = WRITERS
    writer_usd = 2.50
    actuator_parts = bank_motors * motor_usd + writers * writer_usd
    # Channels the S5-R block owns (priced exactly once; not in the fixed base).
    channel_parts = round(BANK_ICS_WORKING * BANK_IC_USD
                          + WRITER_CHIPS * WRITER_CHIP_USD, 2)
    channel_parts_optimistic = round(BANK_ICS_OPTIMISTIC * BANK_IC_USD
                                     + WRITER_CHIPS * WRITER_CHIP_USD, 2)
    # Sourced drive rod (replaces the printed 3x2 placeholder; design calculation).
    rod_parts = STEEL_ROD_USD
    # The design calculation claim (channels unpriced, rod unpriced).
    parts_claim = FIXED_PARTS_NO_CHANNEL + actuator_parts
    delivered_claim = delivered(parts_claim)
    # design calculation ratified claim (channels priced, rod unpriced) and honest total.
    parts_no_rod = round(parts_claim + channel_parts, 2)
    delivered_no_rod = delivered(parts_no_rod)
    parts = round(parts_no_rod + rod_parts, 2)
    d = delivered(parts)
    return dict(rows_in_bank=rows_in_bank,
                fixed_no_channel_parts_usd=FIXED_PARTS_NO_CHANNEL,
                bank_motors=bank_motors, writers=writers,
                actuator_parts_usd=round(actuator_parts, 2),
                actuator_count=bank_motors + writers,
                bank_ic_count=BANK_ICS_WORKING, bank_ic_unit_usd=BANK_IC_USD,
                writer_chip_count=WRITER_CHIPS,
                writer_chip_unit_usd=WRITER_CHIP_USD,
                channel_parts_usd=channel_parts,
                channel_parts_optimistic_usd=channel_parts_optimistic,
                steel_rod_count=1, steel_rod_unit_usd=STEEL_ROD_USD,
                rod_parts_usd=round(rod_parts, 2),
                parts_claim_usd=round(parts_claim, 2),
                delivered_claim_usd=delivered_claim,
                parts_no_rod_usd=parts_no_rod,
                delivered_no_rod_usd=delivered_no_rod,
                parts_usd=round(parts, 2), delivered_usd=d,
                ceiling_usd=COST_CEILING_USD, clears=bool(d < COST_CEILING_USD),
                margin_usd=round(COST_CEILING_USD - d, 2),
                note="actuator count is 2 bank motors + %d writer solenoids; "
                     "the 80-motor head and its 80-channel driver block are "
                     "removed, but the S5-R block's OWN %d bank H-bridge IC(s) "
                     "and %d writer darlington chip(s) are priced here "
                     "(design calculation; no double-count). design calculation adds the 1 sourced "
                     "steel drive rod d=6 (priced here, not previously in the "
                     "printed-placeholder lines). Sourced point-in-time prices."
                     % (writers, BANK_ICS_WORKING, WRITER_CHIPS))


def decide(rows_in_bank: int = ROWS_IN_BANK) -> dict:
    fit = cell_fit()
    xtalk = neighbour_crosstalk()
    wb = writer_budget()
    bd = bank_drive_load(rows_in_bank)
    lat = latch_holding_vs_service()
    tm = timing(rows_in_bank)
    bom_ = bom(rows_in_bank)
    gates = {
        "G1_cell_fit_worst_case": fit["fits_worst_case"],
        "G2_no_neighbour_crosstalk": xtalk["no_contact"],
        "G3_writer_force": wb["pass_gate"],
        "G4_bank_drive_force": bd["pass_gate"],
        "G5_latch_inherits_K1": lat["inherits_k1_bound"],
        "G6_full_map_under_30s": tm["clears_30s"],
        "G7_cost_under_500": bom_["clears"],
    }
    all_pass = all(gates.values())
    return dict(
        rows_in_bank=rows_in_bank,
        evidence_class="CAD geometry + CALCULATION over sourced FDM process "
                       "limits and sourced actuator ratings; no print, no "
                       "purchase, no measurement (design calculation)",
        gates=gates, all_mechanical_gates_pass=bool(all_pass),
        promotable=bool(all_pass),
        residual_uncertainty=[
            "G8 cycle life is reported, not gated: '>=1e6, order unknown' on "
            "the same design calculation FDM constants as every other printed leaf.",
            "The bank crank speed (720 deg/s) and writer settle (0.05 s) are "
            "assumptions; the time gate is conditional on them, exactly as "
            "S5's K6 is conditional on its dwell.",
            "As-printed friction mu, gate/tip sharpness and leaf creep remain "
            "measurement-only (K2/K11 class), unchanged by this pivot.",
            "A missed keeper set is a silent row error, the same failure class "
            "as S5's missed step. No per-cell feedback exists (R1 unchanged).",
            "The R-row bar drive and the writer-carriage indexing are "
            "kinematically plausible but not CAD-interference-checked in a "
            "full multi-row assembly; only the unit cell is modelled here.",
        ],
        verdict=("PROMOTE_TO_08" if all_pass else "REJECT"),
    )


def screen(rows_in_bank: int = ROWS_IN_BANK) -> dict:
    return dict(
        evidence_class="CAD + CALCULATION (design calculation); no print/purchase/measurement",
        cell_fit=cell_fit(),
        neighbour_crosstalk=neighbour_crosstalk(),
        writer_budget=writer_budget(),
        bank_drive_load=bank_drive_load(rows_in_bank),
        latch_vs_service=latch_holding_vs_service(),
        endurance=endurance(rows_in_bank),
        timing=timing(rows_in_bank),
        bom=bom(rows_in_bank),
        sensitivity=sensitivity(rows_in_bank),
        decision=decide(rows_in_bank),
    )




# ---------------------------------------------------------------------------
# Sensitivity / break-even: the design calculation analogue of the wider-head boundary.
# These are the *discriminating* numbers: each is the value of one assumption at
# which the S5-R verdict flips. They are cheap to compute and they tell the next
# test where to concentrate.
# ---------------------------------------------------------------------------
def sensitivity(rows_in_bank: int = ROWS_IN_BANK) -> dict:
    groups = math.ceil(ROWS / rows_in_bank)
    cells = COLS * rows_in_bank
    stations = math.ceil(cells / WRITERS)
    # (a) Timing: crank speed needed at the chosen writer settle.
    def full_at(crank_deg_s: float, settle: float) -> float:
        writer = stations * settle
        select = (LEVELS - 1) * LEVEL_ANGLE_DEG / crank_deg_s
        reset = LEVEL_ANGLE_DEG / crank_deg_s
        return tc.fixed_s() + (groups - 1) * tc.index_s() + groups * (writer + select + reset)
    # solve for crank speed that hits exactly 30 s at current settle
    target = 30.0
    fixed_part = tc.fixed_s() + (groups - 1) * tc.index_s() + groups * stations * WRITER_SETTLE_S
    if fixed_part < target:
        deg_per_group = LEVELS * LEVEL_ANGLE_DEG  # 4 select + 1 reset = 5 levels
        min_crank = groups * deg_per_group / (target - fixed_part)
    else:
        min_crank = math.inf
    # (b) Bank motor torque needed at the chosen tolerance/force, one motor off
    pawl = pawl_spring()
    req_one_motor = (COLS * rows_in_bank * (pawl["force_n"] + WRITE_LOAD_N)
                     / BUS_EFFICIENCY) * BANK_PINION_RADIUS_MM / 1000.0  # N.m
    # (c) Print tolerance at which the pawl/keeper stack still fits the band.
    # design calculation: the bounding axis is the Y-band (pawl + keeper side by side).
    free_band = PITCH_MM - 2.0 * ROTOR_RADIUS_MM
    stack_nom = PAWL_W_MM + KEEPER_LEAF_T_MM
    max_accuracy = (free_band - stack_nom) / 2.0
    # (d) Writer settle needed at the chosen crank speed
    fixed_nosettle = (tc.fixed_s() + (groups - 1) * tc.index_s()
                      + groups * ((LEVELS) * LEVEL_ANGLE_DEG / BANK_CRANK_DEG_S))
    max_settle = (target - fixed_nosettle) / (groups * stations) if fixed_nosettle < target else 0.0
    return dict(
        rows_in_bank=rows_in_bank,
        timing_max_settle_s_for_30s=round(max_settle, 4),
        timing_min_crank_deg_s_for_30s=round(min_crank, 2),
        bank_min_motor_torque_nm_single_off=round(req_one_motor, 4),
        bank_torque_margin_at_chosen=round(BANK_MOTOR_TORQUE_NM / req_one_motor, 3)
        if req_one_motor else None,
        max_dim_accuracy_for_fit_mm=round(max_accuracy, 4),
        chosen_dim_accuracy_mm=DIM_ACCURACY_MM,
        cost_headroom_usd=round(COST_CEILING_USD - bom(rows_in_bank)["delivered_usd"], 2),
        note="Each figure is the single-assumption break-even at which the "
             "S5-R verdict flips. They are the discriminating quantities for "
             "the next (analytic/CAD) test; none requires a coupon.",
    )


if __name__ == "__main__":
    print(json.dumps(screen(), indent=2))
