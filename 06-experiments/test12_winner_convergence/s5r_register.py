"""DND-54 S5-R shared-drive programmable rotary register -- analytic + CAD model.

Question ([DND-54]). [DND-52] found the program's only cost+time-viable pivot
(S5-R) but left its decisive quantity -- selective dropout / re-engage of an
80-rotor bank at 5.08 mm pitch -- as "coupon-only" because a physical coupon is
forbidden ([DND-27]). [DND-27] mandates the replacement evidence class:
**sourced process limits + analytic calculations + CAD/mesh validation**. This
module is that replacement, and it also *redesigns* the register concretely
because the DND-52 option-1 description does not survive an honest per-row
cycle count (see the DND-54 ADR).

MECHANISM DEFINITION (this module's geometry; CAD in s5r_register.scad)
----------------------------------------------------------------------
The S5 five-level stepped rotor is UNCHANGED (radius 1.5 mm, core 1.0 mm,
72 deg/level, from `test08/results/parameters.scad`). S5-R removes the 80 bought
head motors and replaces them with a **shared oscillating drive bar**:

  1. Each rotor hub carries a printed **drive pawl** (a vertical cantilever leaf,
     length PAWL_LENGTH_MM along Z, thickness PAWL_T_MM across the pitch
     direction) that is spring biased INTO a toothed rack cut into the shared
     bar (the "engaged" state).
  2. The bar is stroked by ONE bank motor through a crank/pinion. One forward
     stroke of RACK_STROKE_MM advances every engaged pawl -- and therefore every
     coupled rotor -- by exactly one level (72 deg).
  3. Each column carries a **keeper latch**: a bistable over-centre leaf with a
     "run" detent (pawl engaged) and a "stop" detent (pawl cammed clear of the
     rack). The keeper is a **5-position gate** (one stop position per target
     level, plus run) set by a bank of writer solenoids. 8 solenoids on a
     travelling writer carriage cover a row's 80 columns in 10 stations; the
     carriage is off the dense field so pitch is unchanged.
  4. SELECT (one bank group): the writer carriage sets each column's keeper to
     the gate position for its target level. The bank then makes ONE continuous
     forward pass through (LEVELS-1) rack steps; each pawl is cammed out of the
     rack the first time it reaches its keeper gate, then latches dropped-out and
     skips the remaining steps.
  5. RESET (one bank group): a single reverse pass with a **reset comber** trips
     every dropped-out pawl back over centre to the "run" position. Re-engage is
     one shared kinematic motion, not a per-column actuator.

WIDTH INSIGHT (the DND-54 correction to DND-52). Rows run along Y. The bank bar
can span **R rows in depth at no pitch penalty**, because the row pitch (5.08 mm)
is independent of the in-row column pitch. A single bank pass therefore writes
**R rows at once**, and the map needs ROWS/R bank groups instead of ROWS. DND-52
described a single-row (R=1) bank: an honest per-row cycle count shows R=1 only
clears 30 s at an aggressive bank speed and with many writers, so the register
must be multi-row. R is the one new design variable this model adds.

EVIDENCE CLASS. Geometric definition = CAD. Force / timing / endurance =
CALCULATION over sourced FDM process limits and sourced actuator ratings. No
print, no purchase, no measurement ([DND-27]).
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import cost_closure as cc
import nx52_head_actuator as nx
import timing_closure as tc

HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# Cell / register geometry at 5.08 mm pitch (mirrored in s5r_register.scad).
# ---------------------------------------------------------------------------
PITCH_MM = 5.08
ROTOR_RADIUS_MM = 1.5          # test08 results/parameters.scad (radius_mm)
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

# Keeper latch: bistable over-centre leaf, 5-position gate. The keeper is a
# lightly loaded latch, so 1 line (0.45 mm) is acceptable; its force is small.
KEEPER_LEAF_T_MM = 0.45
KEEPER_LEAF_L_MM = 3.00
KEEPER_LEAF_W_MM = 0.70
KEEPER_OVER_CENTRE_MM = 0.06   # offset making the detent bistable
KEEPER_GATE_STEP_MM = 0.35     # spacing of the 5 gate positions

# Drive rack on the shared bar.
RACK_TOOTH_PITCH_MM = 0.60
RACK_TOOTH_HEIGHT_MM = 0.45
RACK_STROKE_MM = RACK_TOOTH_HEIGHT_MM   # one forward stroke advances one tooth

# FDM process (sourced limits, tools/fdm-limits/fdm_process_limits.py).
MIN_FEATURE_MM = 0.44          # 1 extrusion line @ 0.4 mm nozzle
MIN_WALL_MM = 0.88             # 2 lines, robust
DIM_ACCURACY_MM = 0.10         # per printed face (assumption, [R4])

# Sourced material / friction constants (DETENT_CONTACT.md / test11 sourcing).
MU_PLA_MID = 0.35
MU_PLA_LOW = 0.20
MU_PLA_HIGH = 0.50
PLA_E_MPA = 1500.0             # sourced modulus range 700-2500, midpoint

# Service load already bounded by [DND-44]/DND-48 (robust register). The latch
# never carries terrain load (the rotor hard stop does), so this is inherited.
K1_SERVICE_BOUNDING_N = 3.27
K1_SERVICE_DISTRIBUTED_N = 0.39

# Unloaded-write resistance per pawl beyond its own spring (rotor detent torque
# reflected to the rack at the unloaded write point). Stated assumption. During
# a write the platen is unloaded, so this is the light rotor detent only.
WRITE_LOAD_N = 0.05

# Bank drive: a fully-orderable NEMA17-class stepper (DND-52). The chosen
# design drives the bar from BOTH ends (BANK_MOTORS=2): that doubles the
# available force and removes bar torsion across a 4-row bank.
BANK_MOTOR_TORQUE_NM = 0.30    # sourced class figure (same as lift motor R7)
BANK_MOTORS = 2
BANK_PINION_RADIUS_MM = 6.0
BUS_EFFICIENCY = 0.6           # stated assumption for the bar/crank bus

# Writer solenoid: small 5 V push solenoid (DND-52 writer class).
WRITER_FORCE_N = 1.2
WRITER_SETTLE_S = 0.05         # one comb actuation + settle (assumption)

# Chosen design point (the DND-54 correction to DND-52's R=1, W=8).
ROWS_IN_BANK = 4               # bank spans 4 rows -> 20 groups, no pitch penalty
WRITERS = 40                   # 2 stations/groups of 40: writer index < bank pass

# Bank crank speed (assumed; the dominant time assumption, like S5's K6 dwell).
BANK_CRANK_DEG_S = 720.0       # 2 rev/s

# Endurance: same defensible FDM span as DND-46/K11.
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
    """Geometry: does the pawl + keeper stack fit the 5.08 mm cell band?"""
    rotor_dia = 2.0 * ROTOR_RADIUS_MM
    free_band = PITCH_MM - rotor_dia
    stack_nom = PAWL_T_MM + KEEPER_LEAF_T_MM
    stack_worst = stack_nom + 2.0 * DIM_ACCURACY_MM
    return dict(
        pitch_mm=PITCH_MM, rotor_dia_mm=round(rotor_dia, 3),
        free_band_mm=round(free_band, 3),
        in_band_stack_nominal_mm=round(stack_nom, 3),
        in_band_stack_worst_mm=round(stack_worst, 3),
        stack_inside_band=bool(stack_worst <= free_band),
        tip_gap_worst_mm=round(free_band - stack_worst, 3),
        fits_worst_case=bool((free_band - stack_worst) > 0.0),
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
    number of station moves scales with R (this is the term DND-52 omitted).
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
                writer_s_per_group=round(writer_s, 4),
                select_pass_s=round(select_s, 4), reset_pass_s=round(reset_s, 4),
                per_group_s=round(per_group, 4),
                full_map_s5r_s=round(full, 3),
                full_map_s5_reference_s=round(tc.full_map_s(400), 3),
                clears_30s=bool(full < 30.0),
                margin_to_30s_s=round(30.0 - full, 3))


def delivered(parts_usd: float) -> float:
    return round(parts_usd * cc.UPLIFT, 2)


def bom(rows_in_bank: int) -> dict:
    bank_motors = BANK_MOTORS
    motor_usd = 12.00
    writers = WRITERS
    writer_usd = 2.50
    actuator_parts = bank_motors * motor_usd + writers * writer_usd
    parts = nx.FIXED_PARTS_NO_CHANNEL + actuator_parts
    d = delivered(parts)
    return dict(rows_in_bank=rows_in_bank,
                fixed_no_channel_parts_usd=nx.FIXED_PARTS_NO_CHANNEL,
                bank_motors=bank_motors, writers=writers,
                actuator_parts_usd=round(actuator_parts, 2),
                actuator_count=bank_motors + writers,
                parts_usd=round(parts, 2), delivered_usd=d,
                ceiling_usd=cc.CEILING, clears=bool(d < cc.CEILING),
                margin_usd=round(cc.CEILING - d, 2),
                note="actuator count is 2 bank motors + %d writer solenoids; "
                     "the 80-motor head and its 80-channel driver block are "
                     "removed. Sourced point-in-time prices." % writers)


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
                       "purchase, no measurement (DND-27)",
        gates=gates, all_mechanical_gates_pass=bool(all_pass),
        promotable=bool(all_pass),
        residual_uncertainty=[
            "G8 cycle life is reported, not gated: '>=1e6, order unknown' on "
            "the same DND-46 FDM constants as every other printed leaf.",
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
        evidence_class="CAD + CALCULATION (DND-27); no print/purchase/measurement",
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
# Sensitivity / break-even: the DND-54 analogue of the wider-head boundary.
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
    # (c) Print tolerance at which the pawl/keeper stack still fits the band
    free_band = PITCH_MM - 2.0 * ROTOR_RADIUS_MM
    stack_nom = PAWL_T_MM + KEEPER_LEAF_T_MM
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
        cost_headroom_usd=round(cc.CEILING - bom(rows_in_bank)["delivered_usd"], 2),
        note="Each figure is the single-assumption break-even at which the "
             "S5-R verdict flips. They are the discriminating quantities for "
             "the next (analytic/CAD) test; none requires a coupon.",
    )


if __name__ == "__main__":
    print(json.dumps(screen(), indent=2))
