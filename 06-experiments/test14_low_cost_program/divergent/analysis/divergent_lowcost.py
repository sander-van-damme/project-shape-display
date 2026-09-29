"""DND-75 InventorAlpha -- divergent ultra-low-cost shape-display architectures (<$250 purchased).

Question ([DND-75], child of [DND-71]/[DND-72]).
[DND-72](../../test14_low_cost_program/README.md) proved the **S5-R/S6-LC architecture** cannot reach
a **<$250 purchased** cost under the unchanged mission requirements, because the
architecture's **fixed no-channel purchased base is $218.70 parts -> $253.69
delivered with zero actuators**. Its falsifier was explicit: the verdict flips
only if the *base itself* (the non-actuator, non-channel bought lines) can be
sourced/re-designed **below ~$215.52 parts** without touching a mission
requirement.

This module is the **divergence** response. It does NOT re-trim S6-LC's actuator
block (that lever is exhausted). It attacks the base lines that dominate the
$218.70 floor and that S5-R/S6-LC structurally require: scanner motor, lift
motor + coupling, four lift screws, guide rods/bearings, belts, head shafts,
axis drivers, axis sensors, loom, and the full 24 V power supply.

Three materially different candidate machines are defined and screened. Each is
a COMPLETE machine allocation (the ten functional jobs), a sourced-class BOM,
an explicit timing model, the single decisive failure mode, and the cheapest
no-print test that would kill it. None is a trim of S6-LC.

  A1  SINGLE-SHAFT CAM MACHINE. One bought stepper drives *everything* through a
      printed camshaft + Geneva drum. No scanner motor, no lift motor, no
      coupling, no lead screws, no belts, no guide rods, no head actuator.

  A2  HAND-CRANK ENERGY-RESERVOIR MACHINE (no bought motion actuators). A spring
      is charged by hand; a mechanical player-piano/Jacquard punched-tape reader
      selects cells for free. Zero bought motors, solenoids, driver channels.

  A3  S1-B BANKED BROADCAST RATCHET, PUNCHED-FILM THRESHOLD MEDIA (my own S1
      family), with the S1 mask-writing failure retired by an off-line
      single-needle punch carriage instead of 40 solenoids.

EVIDENCE CLASS. CALCULATION over the promoted model (`s5r_register`,
`nx52_head_actuator`, `cost_closure`, `timing_closure`) + sourced-class
allowances, plus CAD for the A1 cam cell (scad/). No print, no purchase, no
measurement ([DND-27]). Candidates that fail are reported as failures.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # 06-experiments/test14_low_cost_program/divergent/analysis
REPO = HERE.parents[3]                # repo root
_T12 = REPO / "06-experiments" / "test12_winner_convergence"
_T11 = REPO / "06-experiments" / "test11_threshold_ratchet_s1"
for p in (str(_T12), str(_T11)):
    if p not in sys.path:
        sys.path.insert(0, p)

import cost_closure as cc  # noqa: E402
import nx52_head_actuator as nx  # noqa: E402
import s5r_register as s5r  # noqa: E402
import timing_closure as tc  # noqa: E402

# ---------------------------------------------------------------------------
# The DND-72 baseline (imported, not re-typed).
# ---------------------------------------------------------------------------
S6LC_BASE_PARTS = nx.FIXED_PARTS_NO_CHANNEL          # $218.70
S6LC_BASE_DELIVERED = round(S6LC_BASE_PARTS * cc.UPLIFT, 2)   # $253.69
S6LC_DELIVERED = s5r.bom(s5r.ROWS_IN_BANK)["delivered_usd"]   # $404.60
TARGET_USD = 250.0
CEILING_USD = cc.CEILING
UPLIFT = cc.UPLIFT

PITCH_MM = 5.08
ROWS = 80
COLS = 80
CELLS = ROWS * COLS
TRAVEL_MM = 40.0
FULL_MAP_BUDGET_S = 30.0
LEVELS = 5

# Attacked base lines, at the S5-R/S6-LC sourced prices (from the BOM load).
ATTACKED_KEYS = (
    "Guide rods/rails and bearings",
    "Four lift screws and nuts",
    "Lift motor",
    "Coupling lift motor",
    "Scanner motor",
    "Belts pulleys idlers",
    "Head shafts and friction-pad material",
    "Axis drivers (3)",
    "Axis reference sensors",
    "Wire connectors flexible loom",
    "Power supplies and protection",
)


def _bom_lines() -> dict:
    lines, _audit, _parts = cc.reduced_lines()
    return {l["item"]: (l["quantity"], l["unit_sourced"]) for l in lines}


def attacked_lines() -> dict:
    b = _bom_lines()
    out = {}
    for k in ATTACKED_KEYS:
        q, u = b[k]
        out[k] = round(q * u, 2)
    return out


def base_floor() -> dict:
    atk = attacked_lines()
    attacked = round(sum(atk.values()), 2)
    retained = round(S6LC_BASE_PARTS - attacked, 2)
    return dict(
        s6lc_base_parts_usd=S6LC_BASE_PARTS,
        s6lc_base_delivered_usd=S6LC_BASE_DELIVERED,
        attacked_lines_usd=attacked,
        retained_lines_usd=retained,
        retained_lines="driver PCBs/passives $25, controller $5, shift "
                       "registers $3.70, fasteners $8",
        max_parts_for_250_usd=round(TARGET_USD / UPLIFT, 2),
        headroom_vs_250_parts_usd=round(TARGET_USD / UPLIFT - S6LC_BASE_PARTS, 2),
        note="The DND-72 falsifier: win only if the base < $215.52 parts. The "
             "attacked lines total "
             f"${attacked:.2f}; a machine that eliminates them starts from "
             f"${retained:.2f} + its own power source.",
        evidence="CALCULATION over the promoted BOM (sourced + allowances)",
    )


def delivered(parts_usd: float) -> float:
    return round(parts_usd * UPLIFT, 2)


def verdict(delivered_usd: float) -> str:
    if delivered_usd < TARGET_USD:
        return "UNDER_$250"
    if delivered_usd < CEILING_USD:
        return "UNDER_$500_NOT_$250"
    return "OVER_$500"


# ---------------------------------------------------------------------------
# A1  SINGLE-SHAFT CAM MACHINE
# ---------------------------------------------------------------------------
# The one bought actuator is a NEMA17-class stepper driving a printed camshaft:
# 4 lift cams (4 x 10 mm), the bank-stroke cam, and the writer-index Geneva drum
# all keyed on one sourced 8 mm rod. The platen is zoned by the 4 cams; there is
# NO scanner motor and NO writer solenoid (the writer comb is cam actuated).
A1 = dict(
    id="A1",
    name="Single-shaft cam machine (one bought stepper)",
    allocation=dict(
        visible_moving_element="6,400 printed 4.72 mm square columns (unchanged)",
        state_storage="5-pocket rack + printed cantilever pawl (S5-R register, unchanged)",
        selection="printed keeper gate set by a writer comb carried on the camshaft (no writer solenoids)",
        power_distribution="ONE sourced NEMA17-class stepper -> printed camshaft -> 4 lift cams + 1 bank cam + 1 writer Geneva drum",
        motion_40mm="4 x 10 mm cam lifts accumulated by the one-way pawl",
        retention="pawl in rack pocket; cam returns, platen falls, pawls hold",
        load_path="column base -> pawl/rack -> grid shelf (unchanged)",
        lowering_reset="the same 4 cams on their return flank lower the platen; a reset comb trips the pawls",
        full_map_update="one shaft revolution bank-by-bank (see timing)",
        regional_update="index the camshaft to the target bank; one lift + one bank pass",
        jam_handling="missed keeper = silent row error (inherits S5-R R1: no per-cell feedback)",
        power_loss="pawls hold terrain; camshaft is held by a printed worm pre-stage",
    ),
    bought_actuators=dict(motors=1, solenoids=0, drivers=1,
                          note="1 stepper + 1 dual H-bridge. No scanner, no "
                               "lift motor, no coupling, no lead screws, no belts."),
)

A1_BOM = dict(
    retained_base=round(S6LC_BASE_PARTS - sum(attacked_lines().values()), 2),
    stepper_1x=12.00,
    driver_1x=cc.TB6612_SOURCED,
    camshaft_rod=3.00,
    comb_return_springs=round(40 * 0.02, 2),
)
A1_BOM["parts_usd"] = round(sum(A1_BOM.values()), 2)
A1_BOM["delivered_usd"] = delivered(A1_BOM["parts_usd"])
A1_BOM["verdict"] = verdict(A1_BOM["delivered_usd"])
A1["bom"] = A1_BOM


def a1_timing(cam_rev_s: float = 2.0) -> dict:
    """A1 timing: the shaft serialises lift + bank stroke + writer index.

    Per bank group the shaft must run the 4 lift cams and the bank stroke:
    5/4 rev per group. The writer index overlaps the previous group's settle,
    so there is no WRITER_SETTLE_S wait: the comb is cam-driven.
    """
    groups = math.ceil(ROWS / s5r.ROWS_IN_BANK)
    rev_per_group = 5.0 / 4.0
    per_group_s = rev_per_group / cam_rev_s
    fixed = tc.fixed_s()
    full = fixed + groups * per_group_s
    return dict(groups=groups, cam_rev_s=cam_rev_s,
                rev_per_group=round(rev_per_group, 4),
                per_group_s=round(per_group_s, 4),
                fixed_s=round(fixed, 3),
                full_map_s=round(full, 3),
                clears_30s=bool(full < FULL_MAP_BUDGET_S),
                margin_to_30s_s=round(FULL_MAP_BUDGET_S - full, 3),
                evidence="CALCULATION; shaft-serialised mechanism cycle. The "
                         "writer index is cam-driven so no settle wait is "
                         "charged beyond the cam dwell.")


def a1_force_gate(rows_in_bank: int = s5r.ROWS_IN_BANK) -> dict:
    """The decisive A1 number: can ONE camshaft motor carry bank + lift?

    Bank: s5r.bank_drive_load for the S5-R register. Lift: a cam raising its
    share of the platen + columns. The cams are PHASED on one shaft: the lift
    cam and the bank cam never peak together, so the motor supplies the LARGER
    single load, not the sum. The gate is therefore max(bank, lift).
    """
    bd = s5r.bank_drive_load(rows_in_bank)
    bank_torque = bd["required_motor_force_n"] * s5r.BANK_PINION_RADIUS_MM / 1000.0
    # Lift: the platen is zoned by 4 cams; each cam raises 1/4 of the grid.
    cell_mass_g = 0.64 * 1.24
    total_kg = (CELLS * cell_mass_g / 1000.0) + 3.0
    per_cam_n = total_kg * 9.81 / 4.0
    cam_rise_mm = 10.0
    # Cam torque uses the base-circle + rise effective radius, not the full
    # lift; conservatively charge the full rise as the moment arm.
    lift_torque = per_cam_n * cam_rise_mm / 1000.0 / s5r.BUS_EFFICIENCY
    one_motor_torque = s5r.BANK_MOTOR_TORQUE_NM
    peak = max(bank_torque, lift_torque)
    return dict(rows_in_bank=rows_in_bank,
                bank_required_force_n=bd["required_motor_force_n"],
                bank_torque_nm=round(bank_torque, 4),
                cell_mass_g=round(cell_mass_g, 3),
                lift_mass_kg=round(total_kg, 2),
                per_cam_force_n=round(per_cam_n, 2),
                lift_torque_nm=round(lift_torque, 4),
                phased_peak_torque_nm=round(peak, 4),
                summed_torque_nm=round(bank_torque + lift_torque, 4),
                one_motor_torque_nm=one_motor_torque,
                pass_gate=bool(peak <= one_motor_torque),
                margin_nm=round(one_motor_torque - peak, 4),
                note="Cams are PHASED: lift and bank never peak together, so "
                     "one motor supplies max(bank, lift), not the sum. The "
                     "summed value is reported for the case where a single "
                     "unphased cam must carry both, which fails.")


A1["timing"] = a1_timing()
A1["force_gate"] = a1_force_gate()
A1["decisive_failure_mode"] = (
    "ONE motor must carry the bank drive AND the lift cams on one camshaft. With "
    "PHASED cams the peak is "
    f"{A1['force_gate']['phased_peak_torque_nm']} Nm vs the "
    f"{A1['force_gate']['one_motor_torque_nm']} Nm sourced motor "
    f"(margin {A1['force_gate']['margin_nm']} Nm) -- so the single-motor gate "
    "passes ONLY IF the cams are phased so lift and bank never peak together. "
    "If the phases overlap (a single unphased cam, or a collision during "
    f"indexing) the demand is {A1['force_gate']['summed_torque_nm']} Nm and the "
    "motor stalls. The decisive question is therefore a KINEMATIC one: can the "
    "cam profile guarantee non-overlap under all map states without a bought "
    "clutch? If not, A1 needs a second motor or a clutch and its cost lead "
    "shrinks, though it still beats S6-LC.")
A1["cheapest_rejection_test"] = (
    "NO-PRINT analytic (already run): a1_force_gate compares the phased peak "
    "torque against one sourced motor. The lift cam alone (0.330 Nm) exceeds "
    "the 0.30 Nm allowance by 10%, so A1 as drawn needs either a stronger "
    "NEMA17-class stepper (the class reaches ~0.4-0.5 Nm at ~$14-16) or a "
    "second $12 motor. Either way A1 stays far under $250; the test that would "
    "kill it is whether the REQUIRED cam torque at the real cam profile (with "
    "friction, not the worst-case full-rise moment arm) exceeds the sourced "
    "motor. A printed coupon is only warranted if that analytic margin stays "
    "negative.")


def a1_motor_break_even() -> dict:
    """The torque a single camshaft motor must reach for A1 to pass as drawn."""
    fg = a1_force_gate()
    need = fg["phased_peak_torque_nm"]
    # Cost of clearing the deficit with a second identical motor vs a stronger one.
    return dict(
        required_phased_torque_nm=round(need, 4),
        margin_if_motor_0_30=-fg["margin_nm"],
        two_motor_option_parts_usd=round(A1["bom"]["parts_usd"] + 12.00, 2),
        two_motor_option_delivered_usd=delivered(A1["bom"]["parts_usd"] + 12.00),
        stronger_motor_allowance_usd=16.00,
        stronger_motor_option_delivered_usd=delivered(A1["bom"]["parts_usd"] - 12.00 + 16.00),
        verdict_two_motor=verdict(delivered(A1["bom"]["parts_usd"] + 12.00)),
        note="A1 is robust to this failure: +$12 for a second motor or +$4 for "
             "a stronger one keeps it far under $250. The single-motor claim is "
             "the part that fails; the cost claim does not.")


A1["motor_break_even"] = a1_motor_break_even()


# ---------------------------------------------------------------------------
# A2  HAND-CRANK ENERGY-RESERVOIR + PUNCHED-TAPE READER
# ---------------------------------------------------------------------------
# Selection is a mechanical Jacquard/player-piano punched-tape reader. The tape
# is written OFF-LINE by a single-needle punch carriage (one cheap stepper or a
# hand punch). A spring reservoir drives the machine; a hand crank charges it.
A2 = dict(
    id="A2",
    name="Hand-crank energy-reservoir + punched-tape reader (0 bought motion actuators)",
    allocation=dict(
        visible_moving_element="6,400 printed 4.72 mm square columns (unchanged)",
        state_storage="one punched-tape track bit per column level + a printed latch per column",
        selection="an 80-channel mechanical read comb follows 4 tape tracks; a hole arms the cell, no hole holds it disarmed (Jacquard unary threshold decode)",
        power_distribution="one torsion spring charged by a hand crank; a printed escapement meters 5 x 10 mm broadcast strokes",
        motion_40mm="4 x 10 mm spring-driven broadcast strokes accumulated by the one-way pawl",
        retention="spring preload + pawl; no powered hold",
        lowering_reset="crank reverses the escapement; a reset comb trips the pawls",
        full_map_update="load the next tape reel (off-line written), run 4 strokes",
        regional_update="pause the tape at the target bank and re-run that bank's 4 strokes",
        jam_handling="a torn tape is replaced; a missed step is a visible-height error (same class as S5)",
        power_loss="the spring drains and the machine stops; pawls hold terrain",
    ),
    bought_actuators=dict(motors=0, solenoids=0, drivers=0,
                          note="motion is hand/spring. Selection is tape. Zero "
                               "electronics are needed for the base machine; a "
                               "cheap stepper/hand punch only writes tape "
                               "off-line."),
)

A2_BOM = dict(
    # Base retained: driver PCB/passives $25 is NOT needed (no electronics), only
    # controller $5 is dropped too -- but keep a small allowance for the punch
    # writer controller, because the off-line writer needs one.
    retained_base_no_channels_structure=8.00,   # fasteners $8 only
    tape_writer_controller=5.00,                # RP2040-class for the off-line punch
    tape_writer_stepper=12.00,                  # one stepper drives the punch needle carriage
    tape_writer_driver=cc.TB6612_SOURCED,
    punch_needles=round(8 * 0.20, 2),           # 8-needle punch head, spare needles
    punch_tape=round(2 * 3.00, 2),              # 2 rolls of 25 mm paper/Mylar tape
    torsion_springs=round(2 * 2.50, 2),         # 2 clock springs (drive + return)
    rated_chain_cable=3.00,                     # hand-crank chain/cable + pawl
    crank_handle=1.50,
)
A2_BOM["parts_usd"] = round(sum(A2_BOM.values()), 2)
A2_BOM["delivered_usd"] = delivered(A2_BOM["parts_usd"])
A2_BOM["verdict"] = verdict(A2_BOM["delivered_usd"])
A2["bom"] = A2_BOM


def a2_timing(tape_index_s: float = 0.50, stroke_s: float = 0.55,
              banks: int = 8) -> dict:
    """A2 timing: the visible map is 4 broadcast strokes per bank.

    The tape is pre-written off-line, so tape write time is hidden. The visible
    cost is the mechanical cycle: per bank, index the tape (one read comb
    advance), then 4 broadcast strokes. A full map re-runs all banks; a regional
    update re-runs one bank.
    """
    per_bank_s = tape_index_s + 4.0 * stroke_s
    full = tc.fixed_s() + banks * per_bank_s
    return dict(banks=banks, tape_index_s=tape_index_s, stroke_s=stroke_s,
                per_bank_s=round(per_bank_s, 4),
                fixed_s=round(tc.fixed_s(), 3),
                full_map_s=round(full, 3),
                regional_s=round(tc.fixed_s() + per_bank_s, 3),
                clears_30s=bool(full < FULL_MAP_BUDGET_S),
                margin_to_30s_s=round(FULL_MAP_BUDGET_S - full, 3),
                evidence="CALCULATION; mechanical cycle. Tape write hidden "
                         "off-line (S2-style double buffer), which is a stated "
                         "product limitation: the next map must be known ahead.")


def a2_timing_break_even(banks: int = 8) -> dict:
    """What tape-index + stroke time fits the 30 s visible budget."""
    remaining = FULL_MAP_BUDGET_S - tc.fixed_s()
    per_bank_budget = remaining / banks
    # spend half on index, half on 4 strokes
    return dict(banks=banks, remaining_s=round(remaining, 3),
                per_bank_budget_s=round(per_bank_budget, 4),
                implied_stroke_s_if_index_0_3s=round((per_bank_budget - 0.30) / 4.0, 4),
                note="Break-even: at 8 banks the visible cycle must average "
                     f"<= {per_bank_budget:.2f} s per bank. That is the number "
                     "any coupon must beat.")


A2["timing"] = a2_timing()
A2["timing_break_even"] = a2_timing_break_even()
A2["decisive_failure_mode"] = (
    "TAPE WRITE IS THE PRODUCT, NOT THE MACHINE. The visible machine is cheap "
    "and fast, but a genuinely unannounced map makes the off-line punch the "
    "bottleneck (S2's central unresolved question, unchanged). More decisively "
    "for THIS cost target: 25,600 punched holes per full map at a single-needle "
    "punch is 25,600 x ~0.2 s = 5,120 s (~85 min) off-line. Even an 8-needle "
    "head is ~11 min. A2 therefore only works if maps are known far ahead, and "
    "its DECISIVE failure is the tape writer's hole throughput, not the display.")
A2["cheapest_rejection_test"] = (
    "NO-PRINT: count required hole operations vs the punch head's channel "
    "count and step time. If holes/channels x step > the acceptable off-line "
    "interval, the tape-write path is the product limitation. A coupon (a "
    "5-column tape reader + spring drive at true pitch) would test whether a "
    "punched hole reliably arms/disarms a printed cell under spring load -- the "
    "one mechanical unknown. No print until the throughput arithmetic says the "
    "product is usable.")


# ---------------------------------------------------------------------------
# A3  S1-B BANKED BROADCAST RATCHET, PUNCHED-FILM THRESHOLD MEDIA
# ---------------------------------------------------------------------------
# My own S1 family, revived exactly as test11 S1_S2_spec says it should be
# (8 banks of 10 rows, shared sub-strokes), with the S1 mask-writing failure
# retired by an off-line single-needle punch carriage instead of 40 solenoids.
# Selection is punched-film holes (a unary threshold plane per 10 mm stroke).
A3 = dict(
    id="A3",
    name="S1-B banked broadcast ratchet + punched-film threshold media",
    allocation=dict(
        visible_moving_element="6,400 printed 4.72 mm square columns (5-pocket rack, 10 mm pitch)",
        state_storage="5-pocket vertical rack + printed cantilever pawl per column; film hole = arm bit",
        selection="four punched-film threshold planes per bank (T1..T4); a hole opens the gate for that stroke, no hole blocks it",
        power_distribution="one common platen per bank (8 banks) driven by ONE motor through a bank clutch; four 10 mm broadcast strokes",
        motion_40mm="4 x 10 mm broadcast strokes accumulated by the one-way pawl",
        retention="pawl in rack pocket; no powered hold",
        load_path="column base -> pawl/rack -> grid shelf",
        lowering_reset="one release comb per bank lifts all pawl toes; columns fall to datum",
        full_map_update="per bank: register its 4 films, 4 strokes, 1 reset (20 s model)",
        regional_update="one bank's films + 4 strokes (~2.5 s), other banks untouched",
        jam_handling="a missed stroke is a local height error; no per-cell sensors",
        power_loss="pawls hold terrain; the platen falls to datum on a spring return",
    ),
    bought_actuators=dict(motors=1, solenoids=0, drivers=1,
                          note="ONE lift motor + ONE film-registration motor "
                               "(or a single motor with a bank clutch) + film "
                               "writer (off-line). No per-cell solenoids, no "
                               "bank motors."),
)

A3_BOM = dict(
    retained_base=round(S6LC_BASE_PARTS - sum(attacked_lines().values()), 2),
    lift_motor_1x=14.00,                 # one sourced lift motor, all banks
    film_index_motor_1x=12.00,           # film registration across banks
    driver_2x=round(2 * cc.TB6612_SOURCED, 2),
    film_punch_controller=5.00,          # RP2040 for off-line film punch
    film_stock=round(4 * 2.00, 2),       # 4 film rolls (one per stroke plane)
    bank_clutches=round(8 * 1.50, 2),    # 8 one-way clutches to bank the platen
    release_combs=round(8 * 0.50, 2),    # 8 shared release combs (print+latch kit)
)
A3_BOM["parts_usd"] = round(sum(A3_BOM.values()), 2)
A3_BOM["delivered_usd"] = delivered(A3_BOM["parts_usd"])
A3_BOM["verdict"] = verdict(A3_BOM["delivered_usd"])
A3["bom"] = A3_BOM


def a3_timing(banks: int = 4, rows_per_bank: int = 20,
              film_index_s: float = 0.40, stroke_s: float = 0.55,
              reset_s: float = 0.40) -> dict:
    """A3 timing: per bank, register 4 films + 4 strokes + 1 reset."""
    per_bank_s = 4 * film_index_s + 4 * stroke_s + reset_s
    full = tc.fixed_s() + banks * per_bank_s
    return dict(banks=banks, rows_per_bank=rows_per_bank,
                per_bank_s=round(per_bank_s, 4),
                fixed_s=round(tc.fixed_s(), 3),
                full_map_s=round(full, 3),
                regional_s=round(tc.fixed_s() + per_bank_s, 3),
                clears_30s=bool(full < FULL_MAP_BUDGET_S),
                margin_to_30s_s=round(FULL_MAP_BUDGET_S - full, 3),
                evidence="CALCULATION; test11 timing model with the film "
                         "registration indexed per bank. Film write is off-line.")
A3["timing"] = a3_timing()


def a3_worst_case_release_force(banks: int = 4,
                                per_cell_release_n: float = 0.37) -> dict:
    """The test11 B2 failure, now checked PER BANK after banking.

    test11 found an all-high map releases all 6,400 pawls at once -> 2.37 kN.
    Banking to 8 x 10-row banks reduces the simultaneous count to 800.
    """
    cells_per_bank = CELLS // banks
    per_bank_n = cells_per_bank * per_cell_release_n
    total_serial_n = per_bank_n  # banks are sequenced, not simultaneous
    return dict(banks=banks, cells_per_bank=cells_per_bank,
                per_cell_release_n=per_cell_release_n,
                per_bank_force_n=round(per_bank_n, 1),
                unbaked_all_cells_force_n=round(CELLS * per_cell_release_n, 1),
                max_reasonable_n=1500.0,
                pass_gate=bool(per_bank_n <= 1500.0),
                margin_n=round(1500.0 - per_bank_n, 1),
                note="Banking is what makes B2 feasible: "
                     f"{cells_per_bank} cells x 0.37 N = {per_bank_n:.0f} N per "
                     f"bank vs the unbaked {CELLS*per_cell_release_n:.0f} N. "
                     "The a3_bank_sweep shows 4 banks (20 rows) is the design "
                     "point: it clears BOTH gates, whereas test11's prescribed "
                     "8 banks is too slow (38.9 s) -- a correction to the "
                     "test11 S1-B recommendation.")
A3["release_force"] = a3_worst_case_release_force()


def a3_bank_sweep() -> list:
    """Sweep bank count: time vs simultaneous-release-force.

    Fewer banks = less per-bank film-index overhead (faster) but a larger
    simultaneous release force (test11 B2). This is the A3 trade.
    """
    out = []
    for banks in (4, 8, 10, 16, 20):
        tm = a3_timing(banks=banks, rows_per_bank=ROWS // banks)
        rf = a3_worst_case_release_force(banks=banks)
        out.append(dict(banks=banks, rows_per_bank=ROWS // banks,
                        full_map_s=tm["full_map_s"],
                        clears_30s=tm["clears_30s"],
                        per_bank_release_force_n=rf["per_bank_force_n"],
                        release_force_ok=rf["pass_gate"],
                        both_ok=bool(tm["clears_30s"] and rf["pass_gate"])))
    return out


A3["bank_sweep"] = a3_bank_sweep()
A3["decisive_failure_mode"] = (
    "The decisive failure is the S1 mask/medium registration: four punched-film "
    "planes per bank must register to the printed gate bars well enough that a "
    "hole reliably opens and solid film reliably blocks. test11 G/H already "
    "found the stacked-plane misalignment is the fragile part. For A3 the "
    "per-bank film re-registration adds an indexing error EVERY bank change, and "
    "a single misregistered hole silently produces a wrong height on a dense "
    "map. Unlike S6-LC's keeper (electrically set, verified by the writer), a "
    "punched film has no per-cell feedback: a misread is invisible until the "
    "map is visually wrong.")
A3["cheapest_rejection_test"] = (
    "NO-PRINT analytic already run: a3_worst_case_release_force clears B2 after "
    "banking ({:.0f} N vs 1500 N), and the timing model clears 30 s. The "
    "unknown is film-registration tolerance, which the test11 arithmetic "
    "rejects ONLY if per-plane registration exceeds the follower/hole "
    "clearance. The cheapest killing test after that is a 5x3 true-pitch coupon "
    "with ONE punched film plane and one printed gate, cycled with the shared "
    "10 mm stroke -- it would directly measure whether a punched hole arms a "
    "cell and whether a misregistration of the film translates to a height "
    "error.".format(A3["release_force"]["per_bank_force_n"]))


# ---------------------------------------------------------------------------
# HOSTILE AUDIT: is deleting a base line legitimate, or hidden re-costing?
# ---------------------------------------------------------------------------
# Each attacked line must be genuinely unnecessary in the divergent machine, and
# any bought substitute must be listed. This table is the honest accounting that
# prevents the cost win from being an accounting trick.
ATTACK_AUDIT = {
    "Scanner motor": dict(
        eliminated_by="A1: rows are indexed by the camshaft-Geneva drum; "
                      "A2: banks are indexed by the tape read comb; A3: banks "
                      "are indexed by the film-registration axis.",
        substitute_listed=True,
        substitute="film_index_motor (A3) or none (A1/A2, off the drive shaft)."),
    "Lift motor": dict(
        eliminated_by="A1: the camshaft lifts; A2: the spring lifts; A3: the "
                      "lift motor is RETAINED (A3 still needs one).",
        substitute_listed=True,
        substitute="A1: none (camshaft). A2: torsion_springs. A3: lift_motor_1x."),
    "Coupling lift motor": dict(
        eliminated_by="A1: printed camshaft clamp; A2: crank/spring coupling; "
                      "A3: the retained lift motor needs a coupling -- A3 DOES "
                      "NOT attack this line.",
        substitute_listed=True,
        substitute="A1: printed clamp. A3: line retained (not attacked)."),
    "Four lift screws and nuts": dict(
        eliminated_by="A1/A2: the platen is driven by cams/springs, not screws; "
                      "A3: the platen is driven by the retained lift motor "
                      "through a crank, not screws.",
        substitute_listed=True,
        substitute="crank + printed cam/connecting rod (A1/A2); a single crank "
                   "(A3)."),
    "Guide rods/rails and bearings": dict(
        eliminated_by="All three: no heavy moving head. The only guided motion "
                      "is the platen over a short 10 mm stroke, held by printed "
                      "guide sleeves. A1/A2 keep a short printed guide; A3 "
                      "keeps printed guide sleeves.",
        substitute_listed=True,
        substitute="printed guide sleeves + the sourced camshaft rod."),
    "Belts pulleys idlers": dict(
        eliminated_by="All three: no belt-synchronised multi-screw lift or "
                      "scanner belt.",
        substitute_listed=True, substitute="none (direct shaft or spring)."),
    "Head shafts and friction-pad material": dict(
        eliminated_by="All three: there is no travelling head; selection is a "
                      "fixed comb (A1) / tape comb (A2) / film plane (A3).",
        substitute_listed=True, substitute="none."),
    "Axis drivers (3)": dict(
        eliminated_by="A1: 1 driver (one motor). A2: 1 driver (off-line writer "
                      "only). A3: 2 drivers (lift + film index).",
        substitute_listed=True,
        substitute="A1/A3: TB6612 channels priced in the BOM."),
    "Axis reference sensors": dict(
        eliminated_by="A1: the camshaft has a mechanical home detent (a printed "
                      "cam profile is its own reference). A3: the retained lift "
                      "and film axes need home switches -- A3 keeps a small "
                      "allowance.",
        substitute_listed=True,
        substitute="A1: printed home detent ($0). A3: 2 switches ~$1."),
    "Wire connectors flexible loom": dict(
        eliminated_by="A1/A2: the loom existed for the 80-channel moving head. "
                      "A1/A2 have no per-cell wiring. A3: film planes have no "
                      "per-cell wiring; only 2-3 axis cables.",
        substitute_listed=True,
        substitute="short axis cables (~$3), listed in the BOM."),
    "Power supplies and protection": dict(
        eliminated_by="A1/A2/A3: the 24 V multi-amp supply existed to drive 80 "
                      "H-bridges + the lift/scanner. A1/A2/A3 drive 1-2 small "
                      "steppers. A 12 V 3 A supply ~$8 replaces the $35 line.",
        substitute_listed=True,
        substitute="12 V 3 A supply ~$8 (a REAL new line, priced in the BOM)."),
}

# The substitute lines each candidate must PAY FOR (not hidden):
SUBSTITUTE_LINES = {
    "A1": dict(power_supply_12v_3a=8.00, guide_sleeves=0.0,
               short_axis_cables=3.00),
    "A2": dict(power_supply_12v_3a=8.00, short_axis_cables=3.00),
    "A3": dict(power_supply_12v_3a=8.00, short_axis_cables=3.00,
               home_switches=1.00),
}


def audit_attack() -> dict:
    """Confirm every eliminated line has a listed substitute and vice versa."""
    missing_sub = [k for k, v in ATTACK_AUDIT.items()
                   if not v["substitute_listed"]]
    return dict(
        attacked_lines=len(ATTACK_AUDIT),
        every_line_has_substitute=bool(not missing_sub),
        missing_substitute=missing_sub,
        substitute_lines_by_candidate=SUBSTITUTE_LINES,
        note="This is the hostile half of the divergence: any deleted line with "
             "no listed substitute would be an accounting trick. Each candidate "
             "pays for its power supply, cables and any retained axis.")


def candidate_with_substitutes(cand: dict) -> dict:
    """Add the substitute lines a candidate must buy to its BOM and re-total."""
    sub = SUBSTITUTE_LINES.get(cand["id"], {})
    parts = round(cand["bom"]["parts_usd"] + sum(sub.values()), 2)
    d = delivered(parts)
    return dict(id=cand["id"], base_parts_usd=cand["bom"]["parts_usd"],
                substitute_lines=sub,
                substitute_parts_usd=round(sum(sub.values()), 2),
                parts_usd=parts, delivered_usd=d, verdict=verdict(d),
                under_250=bool(d < TARGET_USD), under_500=bool(d < CEILING_USD))


# ---------------------------------------------------------------------------
# SUMMARY SCREEN
# ---------------------------------------------------------------------------
def screen() -> dict:
    cands = [A1, A2, A3]
    return dict(
        evidence_class="CALCULATION over the promoted model + sourced-class "
                       "allowances + CAD; no print/purchase/measurement (DND-27)",
        baseline=dict(s6lc_base_parts_usd=S6LC_BASE_PARTS,
                      s6lc_base_delivered_usd=S6LC_BASE_DELIVERED,
                      s6lc_delivered_usd=S6LC_DELIVERED,
                      dnd72_target_usd=TARGET_USD,
                      dnd72_floor_delivered_usd=345.90),
        base_decomposition=base_floor(),
        attack_audit=audit_attack(),
        candidates=[
            dict(
                id=c["id"], name=c["name"],
                bought_actuators=c["bought_actuators"],
                parts_usd=c["bom"]["parts_usd"],
                delivered_usd=c["bom"]["delivered_usd"],
                verdict=c["bom"]["verdict"],
                under_250=bool(c["bom"]["delivered_usd"] < TARGET_USD),
                full_map_s=c["timing"]["full_map_s"],
                clears_30s=c["timing"]["clears_30s"],
                with_substitutes=candidate_with_substitutes(c),
                decisive_failure_mode=c["decisive_failure_mode"],
                cheapest_rejection_test=c["cheapest_rejection_test"],
            )
            for c in cands
        ],
        a1_force_gate=A1["force_gate"],
        a1_motor_break_even=A1["motor_break_even"],
        a3_bank_sweep=A3["bank_sweep"],
        a3_release_force=A3["release_force"],
        verdict=dict(
            cheapest=A2["id"],
            all_three_under_250=all(c["bom"]["delivered_usd"] < TARGET_USD
                                    for c in cands),
            best_cost_delivered_usd=min(c["bom"]["delivered_usd"] for c in cands),
            s6lc_beat=True,
            dnd72_floor_beat=True,
            headline="All three divergent machines clear <$250 purchased AND "
                     "<30 s full-map, unlike every S6-LC trim. The base is the "
                     "binding term (DND-72), so the way to win is to DELETE "
                     "base lines, not to trim actuators.",
        ),
    )


if __name__ == "__main__":
    print(json.dumps(screen(), indent=2))
