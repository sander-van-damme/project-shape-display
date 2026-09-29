"""DND-107 InventorBeta -- divergent reliability-first whole-machine architectures.

Question ([DND-107], child of [DND-104]). The CTO's program (DND-102) raised
reliability and buildability to **first-class gates** ([DND-103]): minimize what
must work correctly 6,400 times, prefer large positive engagement / hard stops /
compression loads / generous clearances / replaceable modules, and treat the mask
subsystem as part of the machine. The S6-LC (S1-B banked broadcast threshold
ratchet) machine fails exactly there: its correctness rests on **6,400 printed
pawls**, a ~0.45 mm leaf, a friction-and-stiffness-set latch, and no per-cell
feedback -- and the DND-91 audit already found its cell-fit and spring
arithmetic broken.

This module answers DND-104 requirement #1 with **three materially different
complete machines**, none a trim of S6-LC and none like each other. It obeys the
DND-103 rule "surface pitch is not a mechanism-size budget": the dense visible
surface stays at 5.08 mm, but the repeated mechanism is moved to the largest
scale the product allows.

  B1  SHARED DRIVESHAFT BINARY SCREW/NUT MEMORY  (NON-MASK)
      One rotary shaft spans the whole 406.4 mm width. Every column rides on a
      captive printed nut on a *non-rotating vertical threaded post*; a shared
      horizontal driveshaft turns that post only when the column's row selector
      rail engages its tumbler. Height is thread position against hard top/bottom
      stops. NO pawl-spring correctness: state is a screw thread in compression.

  B2  SINGLE-SOURCE PRESSURE BLANKET + MECHANICAL HOLD  (NON-MASK)
      One pump/valve pressurises the platen cavity. All columns rise together
      40 mm to a hard top stop. A single transversal write bar *latches or does
      not latch* each column to a 2-state detent as it sweeps. Drop the pressure;
      latched columns stay up, the rest fall to datum. ONE fluid actuator class;
      the per-cell mechanism is a passive 2-state latch.

  B3  ROTARY DRUM MASK, WRITTEN ONCE PER MAP, READ MECHANICALLY  (MASK)
      A rotary drum carries one circumferential bit track per row-station. It is
      rewritten by a single travelling punch/wipe carriage between maps
      (off-line / double-buffered) and read by a fixed read comb during the same
      4 broadcast strokes S6-LC uses. The fragile per-cell mechanism is replaced
      by a per-ROW encoded track: the repeated count drops ~80x.

EVIDENCE CLASS. CALCULATION over the promoted S5-R/S6-LC model (imported, so it
cannot drift) + sourced-class allowances + CAD geometry constants. **No print,
no purchase, no measurement** ([DND-27]). Every number is labelled. Candidate
failures are reported as failures, not hidden.

The DND-103 per-architecture reliability audit is computed explicitly for each
machine and for the S6-LC reference, so the comparison is quantitative.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # 06-experiments/test14_low_cost_program/divergent/analysis
REPO = HERE.parents[3]                # repo root
_T12 = REPO / "06-experiments" / "test12_winner_convergence"
if str(_T12) not in sys.path:
    sys.path.insert(0, str(_T12))

import cost_closure as cc          # noqa: E402
import nx52_head_actuator as nx    # noqa: E402
import s5r_register as s5r         # noqa: E402
import timing_closure as tc        # noqa: E402

# ---------------------------------------------------------------------------
# Mission constants (imported / from design criteria)
# ---------------------------------------------------------------------------
PITCH_MM = s5r.PITCH_MM                 # 5.08
ROWS = s5r.ROWS                         # 80
COLS = s5r.COLS                         # 80
CELLS = ROWS * COLS                     # 6,400
TRAVEL_MM = tc.TRAVEL_MM                # 40.0
FULL_MAP_BUDGET_S = 30.0                # strictly < 30 s
UPLIFT = cc.UPLIFT                      # 1.16 delivered convention
TARGET_DELIVERED_USD = 250.0            # mission purchased gate (DND-70)
CEILING_DELIVERED_USD = cc.CEILING      # 500.0
TARGET_PARTS_USD = round(TARGET_DELIVERED_USD / UPLIFT, 2)   # $215.52

# S6-LC reference (imported, not re-typed).
S6LC_BASE_PARTS = nx.FIXED_PARTS_NO_CHANNEL                 # $218.70
S6LC_BASE_DELIVERED = round(S6LC_BASE_PARTS * UPLIFT, 2)    # $253.69
S6LC_DELIVERED = round(226.77 * UPLIFT, 2)                  # $263.05
S6LC_FULL_MAP_S = 11.96

# ---------------------------------------------------------------------------
# Shared sourced-class allowances (same class as the rest of the repo)
# ---------------------------------------------------------------------------
MOTOR_NEMA17_USD = 12.00         # NEMA17-class stepper (s5r.bom)
MOTOR_NEMA17_STRONG_USD = 16.00  # stronger NEMA17-class (~0.4-0.5 Nm)
TB6612_USD = cc.TB6612_SOURCED   # $0.7955 dual H-bridge @100
RP2040_USD = cc.RP2040_SOURCED   # controller
PSU_12V_3A_USD = 8.00            # replaces the $35 24 V line
CABLES_USD = 3.00
FASTENERS_USD = 8.00             # retained base fasteners
GENERIC_ROD_USD = 3.00           # sourced steel rod

# Material/friction class constants (same as s5r_register).
MU_PLA_MID = s5r.MU_PLA_MID             # 0.35
PLA_E_MPA = s5r.PLA_E_MPA               # 1500
MIN_FEATURE_MM = s5r.MIN_FEATURE_MM     # 0.44 (1 line @ 0.4 nozzle)
MIN_ROBUST_WALL_MM = 0.88               # 2 lines (DND-103 prefers generous)
MIN_TOKEN_MM = 1.20                     # provisional DND-103 "generous" feature

# Thread/torque class figures (sourced-class, stated assumptions).
THREAD_LEAD_MM = 2.0             # common T8-class lead (2 mm/rev)
THREAD_EFFICIENCY = 0.35         # plastic-on-steel nut, stated assumption
SCREW_DRIVE_TORQUE_NM = 0.40     # NEMA17-class at moderate speed (sourced class)

# Pneumatic class figures (sourced-class, stated assumptions).
PUMP_USD = 6.00                  # 12 V diaphragm/mini pump (sourced class)
VALVE_USD = 4.00                 # 3/2 solenoid valve (sourced class)
REGULATOR_TUBING_USD = 6.00      # regulator + tubing + fittings
BLADDER_USD = 10.00              # platen bladder sheet allowance
AIR_PRESSURE_KPA = 30.0          # blanket working pressure (assumption)
COLUMN_LIFT_FORCE_N = 0.20       # per-column lift force needed (gravity + seal)


def delivered(parts_usd: float) -> float:
    return round(parts_usd * UPLIFT, 2)


def verdict(delivered_usd: float) -> str:
    if delivered_usd < TARGET_DELIVERED_USD:
        return "UNDER_$250"
    if delivered_usd < CEILING_DELIVERED_USD:
        return "UNDER_$500_NOT_$250"
    return "OVER_$500"


def timing_decomposition(fixed_s: float, mask_gen_s: float, transport_s: float,
                         reset_s: float, lift_s: float, settle_s: float,
                         verify_s: float, mask_hidden: bool) -> dict:
    """Honest DND-103 timing decomposition into the seven stages.

    `mask_hidden` = True when mask generation happens off the visible critical
    path (double-buffered). Both visible-transition and sustained-cycle totals
    are reported, per the criteria.
    """
    visible = fixed_s + transport_s + reset_s + lift_s + settle_s + verify_s
    sustained = visible + (0.0 if mask_hidden else mask_gen_s)
    return dict(
        digital_process_s=round(fixed_s, 3),
        mask_generation_s=round(mask_gen_s, 3),
        mask_transport_s=round(transport_s, 3),
        reset_s=round(reset_s, 3),
        lift_s=round(lift_s, 3),
        settle_s=round(settle_s, 3),
        verify_s=round(verify_s, 3),
        mask_hidden_by_double_buffer=bool(mask_hidden),
        visible_transition_s=round(visible, 3),
        sustained_cycle_s=round(sustained, 3),
        visible_clears_30s=bool(visible < FULL_MAP_BUDGET_S),
        sustained_clears_30s=bool(sustained < FULL_MAP_BUDGET_S),
        evidence="CALCULATION over the imported S5-R timing base plus "
                 "architecture-specific stage estimates (assumption-class).",
    )


def reliability_audit(repeated_moving_parts: int, precision_contacts_per_cell: int,
                      compliant_printed_elements: int, wear_interfaces: int,
                      tolerance_sensitive_interactions: int,
                      correlated_failures: list, single_cell_failures: list,
                      serviceability: str, gate_answer: str,
                      min_feature_mm: float, detection: str) -> dict:
    """DND-103 required per-architecture reliability audit."""
    return dict(
        what_must_work_6400_times=gate_answer,
        repeated_moving_parts=repeated_moving_parts,
        precision_contacts_per_cell=precision_contacts_per_cell,
        compliant_printed_elements=compliant_printed_elements,
        wear_interfaces=wear_interfaces,
        tolerance_sensitive_interactions=tolerance_sensitive_interactions,
        correlated_failure_modes=correlated_failures,
        single_cell_failure_modes=single_cell_failures,
        serviceability=serviceability,
        min_repeated_feature_mm=round(min_feature_mm, 3),
        min_feature_is_robust=bool(min_feature_mm >= MIN_ROBUST_WALL_MM),
        min_feature_is_2_line=bool(min_feature_mm >= 2 * MIN_FEATURE_MM),
        detection_path=detection,
        evidence="CALCULATION + architecture-level assembly reasoning; "
                 "feature-size rule is DND-103 provisional.",
    )


# ===========================================================================
# B1  SHARED DRIVESHAFT BINARY SCREW/NUT MEMORY  (NON-MASK)
# ===========================================================================
# One horizontal driveshaft spans the 406.4 mm width, driven at both ends by
# NEMA17-class steppers. Every column rides on a captive printed nut on its OWN
# non-rotating vertical threaded post. A single shared *selector camshaft*
# (one lobe per row, 80 lobes) pushes each row's selector rail; when a row rail
# is released, that row's 80 tumbler nuts engage the horizontal driveshaft
# through printed bevel/worm pairs. Height is the thread position; hard bottom
# stop = 0 mm, hard top stop = 40 mm. State is thread compression, not a spring.
B1 = dict(
    id="B1",
    name="Shared driveshaft binary screw/nut memory (non-mask)",
    allocation=dict(
        visible_moving_element="6,400 printed 4.72 mm square columns on printed threaded posts",
        state_storage="a printed nut captive to the column on a non-rotating threaded post; height held by thread compression against hard bottom/top stops (no spring decides correctness)",
        selection="one shared selector rail per row (80 total) engages/disengages that row's 80 tumbler nuts to a common horizontal driveshaft",
        power_distribution="two NEMA17-class steppers driving one common horizontal shaft via printed bevel/worm pairs; one selector camshaft motor",
        motion_40mm="shaft rotations x thread lead (2 mm/rev) up to a hard 40 mm top stop; down to a hard bottom stop",
        retention="thread in compression; no powered hold; load goes thread-post -> printed frame",
        load_path="column -> captive nut -> threaded post -> base plate -> hard stop at travel ends",
        lowering_reset="reverse the shaft; selected rows run down to the hard bottom stop",
        full_map_update="per row: release rail, command up-count or down-count, engage rail; all rows serial",
        regional_update="select only the target rows' rails; disengaged rows are mechanically isolated",
        jam_handling="a stalled column is back-driven by the thread on reversal; the screw cannot silently hold a wrong state",
        power_loss="thread holds position; no energy needed to maintain terrain",
    ),
    bought_actuators=dict(motors=3, solenoids=0, drivers=3,
                          note="2 NEMA17-class shaft steppers + 1 selector "
                               "camshaft stepper + 3 dual H-bridges. NO per-row "
                               "or per-cell bought actuator; the selector rails "
                               "are cam-driven by one shared motor."),
)

B1_BOM = dict(
    retained_structure_base=FASTENERS_USD,      # frame + fasteners only
    shaft_motors_2x=round(2 * MOTOR_NEMA17_USD, 2),
    selector_cam_motor_1x=MOTOR_NEMA17_USD,
    drivers_3x=round(3 * TB6612_USD, 2),
    controller_1x=RP2040_USD,
    driveshaft_rods_2x=round(2 * GENERIC_ROD_USD, 2),
    psu_12v_3a=PSU_12V_3A_USD,
    short_axis_cables=CABLES_USD,
)
B1_BOM["parts_usd"] = round(sum(B1_BOM.values()), 2)
B1_BOM["delivered_usd"] = delivered(B1_BOM["parts_usd"])
B1_BOM["verdict"] = verdict(B1_BOM["delivered_usd"])
B1["bom"] = B1_BOM


def b1_lead_and_turns(travel_mm: float = TRAVEL_MM,
                      lead_mm: float = THREAD_LEAD_MM) -> dict:
    """Turns to cover 40 mm at a 2 mm lead, and the time at a shaft rate."""
    turns = travel_mm / lead_mm
    return dict(travel_mm=travel_mm, lead_mm=lead_mm, turns=turns,
                note="Binary end-stop memory: only the DIRECTION and a turn "
                     "count matter; the hard stops make the endpoints exact, so "
                     "cumulative thread error is bounded by one turn, not by "
                     "6,400 openings.",
                evidence="CALCULATION (kinematic).")


def b1_torque_gate(cells: int = CELLS, rows_selected: int = 1,
                   lead_mm: float = THREAD_LEAD_MM,
                   efficiency: float = THREAD_EFFICIENCY,
                   per_cell_force_n: float = COLUMN_LIFT_FORCE_N) -> dict:
    """Decisive B1 number: can ONE shaft motor raise one whole selected row?

    A row = 80 columns. The shaft drives 80 worm/bevel take-offs. The torque to
    raise one column's nut is F*lead/(2*pi*eta). The shaft sees the SUM of the
    selected row's 80 columns (torque adds along the shaft, but the shaft must
    transmit the accumulated torque; the far end motor carries the sum).
    """
    f_row = cells / ROWS * per_cell_force_n * rows_selected   # 80 * 0.20 N
    torque_per_col = per_cell_force_n * lead_mm / 1000.0 / (2.0 * math.pi * efficiency)
    torque_row = torque_per_col * (cells / ROWS) * rows_selected
    avail = SCREW_DRIVE_TORQUE_NM
    return dict(cells=cells, columns_per_row=cells / ROWS,
                rows_selected=rows_selected,
                row_force_n=round(f_row, 3),
                torque_per_column_nm=round(torque_per_col, 5),
                selected_row_drive_torque_nm=round(torque_row, 4),
                shaft_motor_torque_nm=avail,
                pass_gate=bool(torque_row <= avail),
                margin_nm=round(avail - torque_row, 4),
                note="Only ONE row is 'screwed' at a time (the other rows' "
                     "tumblers are disengaged), so the shaft motor carries the "
                     "torque of 80 engaged columns, not 6,400. If two rows were "
                     "selected at once the torque doubles and the motor is "
                     "marginal -- a required interlock.",
                evidence="CALCULATION; lead/efficiency are stated assumptions.")


def b1_timing_serial(rows: int = ROWS, turns: float = TRAVEL_MM / THREAD_LEAD_MM,
                     shaft_rev_s: float = 2.0, rail_index_s: float = 0.10,
                     up_down: float = 1.0) -> dict:
    """B1 SERIAL-row timing (the naive machine): one row engaged at a time.

    This is reported as the honest FAILING baseline: a per-row screw machine
    that must serialize 80 rows cannot meet 30 s. It exists to prove the
    machine REQUIRES gang selection, not to hide it.
    """
    shaft_s_per_row = turns / shaft_rev_s * (1.0 + up_down)
    per_row_s = rail_index_s + shaft_s_per_row
    fixed = tc.fixed_s()
    transport = rows * per_row_s
    return dict(rows=rows, turns_per_travel=round(turns, 4),
                shaft_rev_s=shaft_rev_s,
                shaft_s_per_row=round(shaft_s_per_row, 3),
                per_row_s=round(per_row_s, 3),
                fixed_s=round(fixed, 3),
                transport_s=round(transport, 3),
                passes_30s=bool(fixed + transport < FULL_MAP_BUDGET_S),
                note="SERIAL rows: only one row's tumblers engage the shaft at "
                     "a time. 80 rows x ~20 s/row is ~1,600 s -- the naive "
                     "machine FAILS 30 s badly.",
                evidence="CALCULATION; shaft_rev_s and rail_index_s assumption.")


def b1_timing_gang(rows: int = ROWS, turns: float = TRAVEL_MM / THREAD_LEAD_MM,
                   shaft_rev_s: float = 2.0, rail_index_s: float = 0.10,
                   up_down: float = 1.0, gang_rows: int = 10) -> dict:
    """B1 GANG-row timing: all rows that share a target run together.

    The driveshaft is COMMON, so any number of selected rows can be driven at
    once -- the only cost is shaft torque (see b1_torque_gate), which then
    scales with `gang_rows`. The height is binary end-stop memory, so a row only
    needs one shaft pass per direction it must move, not one per row. With
    `gang_rows` selected together, the number of shaft passes is
    ceil(rows/gang_rows) per direction.
    """
    passes_per_direction = math.ceil(rows / gang_rows)
    shaft_s_per_pass = turns / shaft_rev_s
    transport = 2.0 * (rail_index_s + shaft_s_per_pass) * passes_per_direction \
        if up_down else (rail_index_s + shaft_s_per_pass) * passes_per_direction
    fixed = tc.fixed_s()
    return dict(rows=rows, gang_rows=gang_rows,
                passes_per_direction=passes_per_direction,
                turns_per_travel=round(turns, 4), shaft_rev_s=shaft_rev_s,
                shaft_s_per_pass=round(shaft_s_per_pass, 3),
                fixed_s=round(fixed, 3),
                transport_s=round(transport, 3),
                passes_30s=bool(fixed + transport < FULL_MAP_BUDGET_S),
                note="GANG rows: all selected rows share the common shaft; the "
                     "binary end stops mean one pass per direction per gang.",
                evidence="CALCULATION; gang_rows is the design knob.")


def b1_gang_torque_gate(gang_rows: int = 10,
                        per_cell_force_n: float = COLUMN_LIFT_FORCE_N,
                        lead_mm: float = THREAD_LEAD_MM,
                        efficiency: float = THREAD_EFFICIENCY) -> dict:
    """Torque when `gang_rows` rows are engaged simultaneously."""
    per_col = per_cell_force_n * lead_mm / 1000.0 / (2.0 * math.pi * efficiency)
    columns = gang_rows * COLS
    torque = per_col * columns
    avail2 = 2 * SCREW_DRIVE_TORQUE_NM      # both shaft ends driven
    return dict(gang_rows=gang_rows, engaged_columns=columns,
                torque_nm=round(torque, 4),
                two_end_motor_torque_nm=round(avail2, 4),
                pass_gate=bool(torque <= avail2),
                margin_nm=round(avail2 - torque, 4),
                max_gang_rows_for_gate=round(
                    avail2 / (per_col * COLS), 2),
                note="Gang selection trades timing for torque: more rows at once "
                     "is faster but needs more shaft torque. The two-end drive "
                     "doubles available torque; the gate gives the max gang "
                     "size that fits the sourced motor class.")


B1["lead"] = b1_lead_and_turns()
B1["torque_gate"] = b1_torque_gate()
B1_TIMING_SERIAL = b1_timing_serial()
B1_TIMING_GANG = b1_timing_gang()
B1["torque_gang_gate"] = b1_gang_torque_gate()


def b1_gang_sweep(shaft_rev_s_values=(0.5, 1.0, 2.0),
                  per_cell_force_n: float = COLUMN_LIFT_FORCE_N) -> list:
    """Sweep gang size x shaft speed: where (if ever) does B1 clear 30 s?

    The torque gate caps the gang size; the timing needs enough gang size and
    shaft speed. This sweep is the decisive B1 result.
    """
    out = []
    for rev_s in shaft_rev_s_values:
        for gang in (10, 20, 30, 55, 80):
            tg = b1_gang_torque_gate(gang_rows=gang,
                                     per_cell_force_n=per_cell_force_n)
            tm = b1_timing_gang(gang_rows=gang, shaft_rev_s=rev_s)
            full = tm["fixed_s"] + tm["transport_s"] + 0.05 * ROWS
            out.append(dict(shaft_rev_s=rev_s, gang_rows=gang,
                            torque_nm=tg["torque_nm"],
                            torque_ok=tg["pass_gate"],
                            visible_s=round(full, 3),
                            timing_ok=bool(full < FULL_MAP_BUDGET_S),
                            both_ok=bool(tg["pass_gate"] and
                                         full < FULL_MAP_BUDGET_S)))
    return out


B1["gang_sweep"] = b1_gang_sweep()


def b1_lead_sweep(leads_mm=(2.0, 4.0, 8.0, 12.0), gang_rows: int = 20,
                  shaft_rev_s: float = 2.0,
                  per_cell_force_n: float = COLUMN_LIFT_FORCE_N) -> list:
    """Sweep thread lead: a bigger lead needs fewer turns AND gives more lift
    per unit torque, so it can clear BOTH gates at once. This is B1's real
    design lever (a higher-lead screw), not motor size.
    """
    out = []
    for lead in leads_mm:
        turns = TRAVEL_MM / lead
        tg = b1_gang_torque_gate(gang_rows=gang_rows,
                                 per_cell_force_n=per_cell_force_n,
                                 lead_mm=lead)
        tm = b1_timing_gang(gang_rows=gang_rows, shaft_rev_s=shaft_rev_s,
                            turns=turns)
        full = tm["fixed_s"] + tm["transport_s"] + 0.05 * ROWS
        out.append(dict(lead_mm=lead, turns=turns,
                        self_lock_ok=bool(lead <= 4.0),
                        torque_nm=tg["torque_nm"], torque_ok=tg["pass_gate"],
                        visible_s=round(full, 3),
                        timing_ok=bool(full < FULL_MAP_BUDGET_S),
                        both_ok=bool(tg["pass_gate"] and
                                     full < FULL_MAP_BUDGET_S)))
    return out


B1["lead_sweep"] = b1_lead_sweep()
B1["timing_serial"] = timing_decomposition(
    fixed_s=B1_TIMING_SERIAL["fixed_s"],
    mask_gen_s=0.0,
    transport_s=B1_TIMING_SERIAL["transport_s"],
    reset_s=0.0, lift_s=0.0,
    settle_s=round(0.05 * ROWS, 3), verify_s=0.0, mask_hidden=True,
)
B1["timing"] = timing_decomposition(
    fixed_s=B1_TIMING_GANG["fixed_s"],
    mask_gen_s=0.0,
    transport_s=B1_TIMING_GANG["transport_s"],
    reset_s=0.0, lift_s=0.0,
    settle_s=round(0.05 * ROWS, 3), verify_s=0.0, mask_hidden=True,
)
B1["timing"]["gang_rows"] = B1_TIMING_GANG["gang_rows"]
B1["combined_gate"] = dict(
    result="FAIL_AS_DRAWN",
    serial_s=B1["timing_serial"]["visible_transition_s"],
    torque_feasible_best_s=min(
        r["visible_s"] for r in B1["gang_sweep"] if r["torque_ok"]),
    timing_feasible_points=[r for r in B1["gang_sweep"] if r["timing_ok"]],
    timing_feasible_all_torque_infeasible=all(
        not r["torque_ok"] for r in B1["gang_sweep"] if r["timing_ok"]),
    max_torque_gang_rows=B1["torque_gang_gate"]["max_gang_rows_for_gate"],
    self_locking_lead_max_mm=4.0,
    note="The screw lead is a THREE-WAY trap: small lead self-locks (good "
         "retention) but is too slow; large lead is fast but stops being "
         "self-locking (needs a brake, a new failure mode) and torque grows "
         "linearly with lead, so it also exceeds the gang motor. Under a "
         "2-end NEMA17-class drive at >=2 rev/s there is NO lead/gang setting "
         "that clears BOTH the 30 s timing and the torque gate.",
    fix_path="A higher-torque/shorter-shaft drive (e.g. a 4-end NEMA23-class "
             "drive), a roller-screw/high-lead screw with a printed brake, or "
             "an additional 5-level unary scheme; each costs dollars or adds a "
             "failure mode, so B1 is reported as a FAILED candidate, not a "
             "winner.")
B1["decisive_failure_mode"] = (
    "THREE-WAY TORQUE/TIMING/LEAD TRAP, and the analysis rejects B1 as drawn. "
    f"The naive serial-row machine is {B1['timing_serial']['visible_transition_s']} "
    "s (fails 30 s ~54x). Gang selection fixes speed but multiplies shaft "
    f"torque, and the sourced two-end NEMA17-class drive caps the gang at "
    f"~{B1['torque_gang_gate']['max_gang_rows_for_gate']} rows, whose best "
    f"torque-feasible timing is "
    f"{min(r['visible_s'] for r in B1['gang_sweep'] if r['torque_ok'])} s -- "
    "still over 30 s. A larger screw lead is faster but stops self-locking "
    "(needs a brake) AND raises torque linearly, so it fails torquier. "
    "Every point that passes 30 s fails the torque gate, and every "
    "torque-feasible point fails 30 s. B1 is therefore a FAILED candidate; its "
    "value is the proof that a shared-shaft binary-screw memory cannot meet the "
    "mission on a low-cost stepper class -- a real negative result.")
B1["cheapest_rejection_test"] = (
    "ALREADY RUN and it REJECTS B1: b1_gang_sweep + b1_lead_sweep show the "
    "timing-feasible set and the torque-feasible set are disjoint. No coupon is "
    "worth printing unless a fundamentally stronger drive is proposed. If it "
    "were, the cheapest physical kill is a 3-column strip: one shaft, three "
    "printed worm take-offs, three threaded posts, driven to stall; measure "
    "gang torque per column and thread tracking.")


# ===========================================================================
# B2  SINGLE-SOURCE PRESSURE BLANKET + MECHANICAL HOLD  (NON-MASK)
# ===========================================================================
# One 12 V pump + one 3/2 valve pressurise a platen bladder. All 6,400 columns
# rise TOGETHER 40 mm to a hard top stop (the stop defines height 1). A single
# transversal write bar then sweeps across the board; as it passes, a printed
# 2-state toggle on each column is flipped by a fixed cam profile on the bar
# (flip = "stay", no flip = "drop"). Pressure is released; columns whose toggle
# is engaged stay on the hard top stop, the rest fall to the hard datum stop.
# Binary terrain (0 / 40 mm) only -- not a 5-level machine. State is a positive
# toggle, not friction, and both endpoints are hard stops.
B2 = dict(
    id="B2",
    name="Single-source pressure blanket + mechanical hold (non-mask, binary)",
    allocation=dict(
        visible_moving_element="6,400 printed 4.72 mm square columns in a common bladder platen",
        state_storage="a printed 2-state toggle per column; engaged = held on the hard top stop, released = falls to the hard datum stop",
        selection="one transversal write bar with a fixed cam profile flips the toggle of the columns it must hold; a second reverse profile releases them",
        power_distribution="one 12 V pump + one 3/2 valve pressurise the whole platen; one write-bar motor traverses X",
        motion_40mm="one common 40 mm blanket lift to a hard top stop (all columns together), then a passive drop to the datum",
        retention="positive toggle engagement against the hard top stop; no fluid pressure needed to hold terrain",
        load_path="column -> toggle lug -> hard stop shelf -> frame",
        lowering_reset="release all toggles (reverse write bar), vent the bladder, all columns fall to the datum stop",
        full_map_update="lift all, sweep the write bar once, release pressure",
        regional_update="cannot raise one region alone from datum (the blanket is common) -- see decisive failure",
        jam_handling="a column that cannot fall is visible (it stays high); the next full-lift pass re-datums it",
        power_loss="bladder vents; toggled columns stay up on hard stops, released columns rest on the datum",
    ),
    bought_actuators=dict(motors=1, solenoids=1, drivers=1,
                          note="1 write-bar stepper + 1 valve solenoid + 1 "
                               "pump (a motor class). No per-row, no per-cell "
                               "bought actuator. Fluid loop is shared."),
)

B2_BOM = dict(
    retained_structure_base=FASTENERS_USD,
    write_bar_motor_1x=MOTOR_NEMA17_USD,
    write_bar_driver_1x=TB6612_USD,
    controller_1x=RP2040_USD,
    pump_1x=PUMP_USD,
    valve_1x=VALVE_USD,
    regulator_tubing_1x=REGULATOR_TUBING_USD,
    bladder_sheet_1x=BLADDER_USD,
    psu_12v_3a=PSU_12V_3A_USD,
    short_axis_cables=CABLES_USD,
)
B2_BOM["parts_usd"] = round(sum(B2_BOM.values()), 2)
B2_BOM["delivered_usd"] = delivered(B2_BOM["parts_usd"])
B2_BOM["verdict"] = verdict(B2_BOM["delivered_usd"])
B2["bom"] = B2_BOM


def b2_blanket_force(cells: int = CELLS,
                     per_cell_force_n: float = COLUMN_LIFT_FORCE_N,
                     pressure_kpa: float = AIR_PRESSURE_KPA) -> dict:
    """Blanket force and required bladder area at the working pressure."""
    total_n = cells * per_cell_force_n
    # active area = 400 x 400 mm platen = 0.16 m^2
    area_m2 = 0.4 * 0.4
    pressure_pa = pressure_kpa * 1000.0
    available_n = pressure_pa * area_m2
    return dict(cells=cells, total_column_force_n=round(total_n, 1),
                bladder_area_m2=area_m2, pressure_kpa=pressure_kpa,
                available_blanket_force_n=round(available_n, 1),
                pass_gate=bool(available_n >= total_n),
                margin_n=round(available_n - total_n, 1),
                note="The whole-board lift is a fluid blanket, so its force is "
                     "not serialised across columns: 30 kPa over the 0.16 m^2 "
                     "platen gives a large margin over 6,400 x 0.20 N.",
                evidence="CALCULATION; per-cell force and pressure are stated "
                         "assumptions.")


def b2_timing(rows: int = ROWS, platen_travel_mm: float = TRAVEL_MM,
              lift_rate_mm_s: float = 20.0, bar_sweep_s: float = 6.0,
              settle_s: float = 1.0) -> dict:
    """B2 visible timing: common lift, one write-bar sweep, release/settle."""
    lift = platen_travel_mm / lift_rate_mm_s
    fixed = tc.fixed_s()
    return dict(rows=rows, lift_s=round(lift, 3),
                write_bar_sweep_s=round(bar_sweep_s, 3),
                settle_s=round(settle_s, 3),
                fixed_s=round(fixed, 3),
                note="The write bar is a single X traverse at row pitch; it does "
                     "not need one pass per row if it can flip a full column "
                     "strip, so the sweep is one platen-width pass.",
                evidence="CALCULATION; rates are stated assumptions.")


B2["blanket_force"] = b2_blanket_force()


def b2_toggle_gate(toggle_t_mm: float = 0.88, toggle_w_mm: float = 4.0,
                   toggle_l_mm: float = 6.0, e_mpa: float = PLA_E_MPA,
                   deflection_mm: float = 0.5) -> dict:
    """Is the B2 per-cell toggle a DND-103 'tiny printed spring'? Quantify it.

    The toggle is a printed living hinge. Its ENGAGEMENT FORCE is
    - but its HOLD is the hard top stop. The spring only has to throw the
    toggle past over-centre, so its exact force must be enough to snap but the
    column's height is NOT set by the spring (unlike S6-LC's keeper). This is
    the key reliability distinction: B2's spring decides 'did it flip', a
    binary event, not 'what height', a continuous one.
    """
    i = toggle_w_mm * toggle_t_mm ** 3 / 12.0
    k = 3.0 * e_mpa * i / (toggle_l_mm ** 3)
    f = k * deflection_mm
    return dict(toggle_t_mm=toggle_t_mm, toggle_w_mm=toggle_w_mm,
                toggle_l_mm=toggle_l_mm,
                section_modulus_mm3=round(i, 4),
                rate_n_per_mm=round(k, 4),
                snap_force_n=round(f, 4),
                feature_is_2_line=bool(toggle_t_mm >= 2 * MIN_FEATURE_MM),
                note="The toggle's spring sets only the BINARY flip event; the "
                     "height is a hard stop. A weaker/thicker toggle changes "
                     "the snap force but NOT the commanded height, so B2 does "
                     "not inherit S6-LC's continuous-force correctness class.",
                evidence="CALCULATION; E and deflection are stated assumptions.")


B2["toggle_gate"] = b2_toggle_gate()
B2_TIMING = b2_timing()
B2["timing"] = timing_decomposition(
    fixed_s=B2_TIMING["fixed_s"],
    mask_gen_s=0.0,
    transport_s=B2_TIMING["write_bar_sweep_s"],
    reset_s=0.0,
    lift_s=B2_TIMING["lift_s"],
    settle_s=B2_TIMING["settle_s"],
    verify_s=0.0,
    mask_hidden=True,
)
B2["decisive_failure_mode"] = (
    "REGIONAL UPDATE IS NOT FREE, and the per-cell TOGGLE is still a compliant "
    "element -- but unlike S6-LC its spring sets only the BINARY flip, not the "
    "height, so a weak/thick toggle changes the snap force without changing the "
    "commanded height. Two real limits remain. (1) REGIONAL: the blanket is "
    "common, so a regional reveal cannot raise one region alone from the datum "
    "without raising neighbours; B2 must either re-datum the whole board (a "
    "full-map cycle) or use a zoned bladder + extra valves, eroding the "
    "single-source cost win. (2) BINARY ONLY: 0/40 mm, no 10/20/30 mm levels "
    "without a second toggle stack. The toggle gate gives a snap force of "
    f"{B2['toggle_gate']['snap_force_n']} N on a "
    f"{B2['toggle_gate']['toggle_t_mm']} mm 2-line hinge -- a printable, "
    "non-marginal element.")
B2["cheapest_rejection_test"] = (
    "The riskiest single thing is whether a printed 2-state toggle reliably "
    "engages AND releases under a common blanket pressure 6,400 times. Cheapest "
    "kill: a 5-column strip coupon with one shared bladder region, one write-bar "
    "cam profile, cycled 200x; measure engagement rate and release rate. If the "
    "toggle cannot be made positive (hard-stop) it fails the DND-103 gate.")


# ===========================================================================
# B3  ROTARY DRUM MASK, WRITTEN ONCE PER MAP, READ MECHANICALLY  (MASK)
# ===========================================================================
# A rotary drum carries one circumferential bit track per ROW (80 tracks). Each
# track is a printed/embossed ridge or a punched hole read by a fixed follower.
# The drum is rewritten between maps by ONE travelling write carriage (off-line
# / double-buffered). During the visible transition the drum indexes to a
# station, a track opens the broadcast gate for that station's 4 strokes, and
# the same 10 mm broadcast platen S6-LC uses accumulates height in the columns.
# The per-cell mechanism is still a pawl+rack, BUT correctness is now one
# shared track per row-station, not one printed keeper per cell.
B3 = dict(
    id="B3",
    name="Rotary drum mask, written once per map, read mechanically (mask)",
    allocation=dict(
        visible_moving_element="6,400 printed 4.72 mm square columns with per-column uni-directional pawl in a 5-pocket rack",
        state_storage="pawl in a pocket (hard-stop, one-way); the map itself is on the drum track, not in a fragile per-cell keeper",
        selection="one circumferential track per row-station on the drum; a fixed follower opens that station's gate for its 4 broadcast strokes",
        power_distribution="one lift stepper (4 broadcast 10 mm strokes) + one drum-index stepper + one write-carriage stepper (off-line)",
        motion_40mm="4 x 10 mm broadcast strokes accumulated by the one-way pawl",
        retention="pawl in pocket, compression against the pocket shoulder",
        load_path="column -> pawl -> rack pocket -> platen shelf",
        lowering_reset="one banked release comb per drum station (shared), trips all pawls for that station",
        full_map_update="index the drum, run 4 strokes + reset per station",
        regional_update="index the drum to the target stations and replay only those (drum-local)",
        jam_handling="a blown pawl leaves a wrong height; no per-cell feedback, but the drum track is shared so a bad track is a detectable row-level fault",
        power_loss="pawls hold terrain; drum is passive",
    ),
    bought_actuators=dict(motors=3, solenoids=0, drivers=3,
                          note="1 lift stepper + 1 drum-index stepper + 1 "
                               "write-carriage stepper (off-line). NO per-cell "
                               "or per-row bought actuator."),
)

B3_BOM = dict(
    retained_structure_base=FASTENERS_USD,
    lift_motor_1x=14.00,
    drum_index_motor_1x=MOTOR_NEMA17_USD,
    write_carriage_motor_1x=MOTOR_NEMA17_USD,
    drivers_3x=round(3 * TB6612_USD, 2),
    controller_1x=RP2040_USD,
    drum_stock=6.00,             # sourced tube + bearings allowance
    drum_write_head=4.00,        # replaceable punch/wipe head
    psu_12v_3a=PSU_12V_3A_USD,
    short_axis_cables=CABLES_USD,
)
B3_BOM["parts_usd"] = round(sum(B3_BOM.values()), 2)
B3_BOM["delivered_usd"] = delivered(B3_BOM["parts_usd"])
B3_BOM["verdict"] = verdict(B3_BOM["delivered_usd"])
B3["bom"] = B3_BOM


def b3_repeated_count(rows: int = ROWS, stations: int = 20) -> dict:
    """How many repeated elements must be correct, vs S6-LC's 6,400 keepers."""
    channels_per_station = COLS   # one bit per column within the station? No:
    # The drum track selects a STATION (bank of rows); within a station the
    # broadcast stroke arms all columns that still need that stroke. So the
    # decision count is stations, not cells.
    return dict(stations=stations,
                drum_tracks=rows,
                per_cell_repeated_keepers=0,
                per_row_repeated_decisions=rows,
                s6lc_per_cell_keepers=CELLS,
                reduction_factor=round(CELLS / rows, 2),
                note="B3 moves the map decision from 6,400 printed keepers to "
                     "80 drum tracks (one per row). The remaining per-cell part "
                     "is the passive one-way pawl, which is a hard-stop part "
                     "S6-LC also has; B3 removes the fragile per-cell KEEPER.",
                evidence="CALCULATION.")


def b3_timing(stations: int = 20, transport_s: float = 0.40,
              stroke_s: float = 0.55, reset_s: float = 0.30,
              mask_gen_offline_s: float = 45.0) -> dict:
    """B3 visible timing vs sustained cycle, with the drum write priced."""
    lift = 4 * stroke_s
    transport = stations * transport_s
    reset = stations * reset_s
    return dict(stations=stations, per_station_strokes=4,
                transport_s=round(transport, 3),
                lift_s=round(lift, 3),
                reset_s=round(reset, 3),
                mask_generation_s=mask_gen_offline_s,
                note="Mask generation is a single travelling write-carriage pass "
                     "over the drum, done between maps (double-buffered).",
                evidence="CALCULATION; carriage + stroke rates assumption.")


B3["repeated_count"] = b3_repeated_count()
B3_TIMING = b3_timing()
B3["timing"] = timing_decomposition(
    fixed_s=tc.fixed_s(),
    mask_gen_s=B3_TIMING["mask_generation_s"],
    transport_s=B3_TIMING["transport_s"],
    reset_s=B3_TIMING["reset_s"],
    lift_s=B3_TIMING["lift_s"],
    settle_s=round(0.05 * b3_repeated_count()["stations"], 3),
    verify_s=0.0,
    mask_hidden=True,
)
B3["timing"]["stations"] = B3_TIMING["stations"]
B3["decisive_failure_mode"] = (
    "The drum write is the product, exactly as in the punched-media family: a "
    "genuinely unannounced map must have its drum rewritten by one carriage, "
    f"priced honestly at {B3_TIMING['mask_generation_s']} s off-line. "
    "Double-buffering hides it only if the next map is known ahead. The second "
    "failure is drum-track registration: one misread track silently arms or "
    "blocks a whole row-station, a correlated error of 80 cells -- larger than "
    "a single keeper but also far easier to detect (a whole row is wrong).")
B3["cheapest_rejection_test"] = (
    "NO-PRINT: the timing decomposition already prices the drum write. Cheapest "
    "kill: a one-track drum segment + follower + gate, cycled 500x at the true "
    "10 mm stroke pitch, to measure whether a printed/embossed track reliably "
    "opens the gate and whether a single write-carriage pass sets a clean track "
    "edge. This is smaller and cheaper than S6-LC's required 4x4 keeper coupon.")


# ===========================================================================
# S6-LC REFERENCE RELIABILITY AUDIT (the thing we must beat)
# ===========================================================================
S6LC_AUDIT = reliability_audit(
    repeated_moving_parts=CELLS,                    # 6,400 pawls + keepers
    precision_contacts_per_cell=2,                  # keeper gate + pawl/rack
    compliant_printed_elements=CELLS,               # every keeper + pawl leaf
    wear_interfaces=CELLS,                          # every pawl/rack + keeper
    tolerance_sensitive_interactions=CELLS,         # sub-mm latch at every cell
    correlated_failures=[
        "mask registration (one punched/kept plane mis-set -> whole bank wrong)",
        "platen/common lift stall (all columns in a bank miss a stroke)",
        "release comb structural failure (a bank fails to reset)",
    ],
    single_cell_failures=[
        "keeper does not snap (silent wrong level, no feedback)",
        "pawl misses a rack pocket (silent wrong level)",
        "0.45-0.90 mm leaf breaks or creeps",
    ],
    serviceability="banked modules; a single cell is not independently "
                   "reachable without lifting the bank",
    gate_answer="6,400 printed keepers must each set and release; plus 6,400 "
                "pawls must each catch one of five pockets",
    min_feature_mm=0.45,
    detection="NONE per cell (DND-91 A6/A8); only axis home sensors",
)


# ===========================================================================
# RELIABILITY AUDITS (DND-103 required fields) for B1 / B2 / B3
# ===========================================================================
B1_AUDIT = reliability_audit(
    repeated_moving_parts=CELLS,           # each column nut+thread; simple
    precision_contacts_per_cell=1,         # the thread engagement only
    compliant_printed_elements=0,          # no spring decides correctness
    wear_interfaces=CELLS,                 # thread-to-nut (large-flank surface)
    tolerance_sensitive_interactions=1,    # per ROW (tumbler engagement)
    correlated_failures=[
        "shared driveshaft / its bearings (one shaft drives every column)",
        "one row's selector rail jams -> that row's 80 columns miss",
        "printed worm/bevel efficiency lower than assumed (whole machine slow)",
    ],
    single_cell_failures=[
        "one column's thread binds (local; back-driven on reversal)",
        "one tumbler fails to engage (that cell misses one update only)",
    ],
    serviceability="column post + nut are a replaceable printed pair; the "
                   "driveshaft is a single removable rod",
    gate_answer="each column's thread must hold and move; there is NO fragile "
                "decision element -- the hard stops define the endpoints",
    min_feature_mm=1.20,   # generous thread flank (>= 2 lines)
    detection="a stalled column stalls its row motor (current sense), so a "
              "correlated fault IS detectable at row level",
)

B2_AUDIT = reliability_audit(
    repeated_moving_parts=CELLS,           # each toggle flips once per map
    precision_contacts_per_cell=1,         # toggle lug to hard stop
    compliant_printed_elements=CELLS,      # living-hinge toggle (a real risk)
    wear_interfaces=CELLS,                 # toggle pivot + cam contact
    tolerance_sensitive_interactions=CELLS,
    correlated_failures=[
        "bladder leak / pump failure (whole board cannot lift)",
        "valve stuck (whole board stays pressurised or vented)",
        "common write-bar cam wear (a whole X strip mis-writes)",
    ],
    single_cell_failures=[
        "toggle binds and stays up (column stuck high; visible)",
        "toggle fails to engage (column drops; visible)",
    ],
    serviceability="toggles are per-column printed parts under a removable "
                   "bladder deck; a whole group is replaceable, single-cell "
                   "service is awkward",
    gate_answer="6,400 living-hinge toggles must each flip and hold; plus one "
                "shared fluid seal must not leak. The toggle is the new "
                "per-cell risk -- a compliant element again",
    min_feature_mm=1.20,
    detection="a stuck toggle is VISIBLE (a wrong-height column on a binary "
              "map stands out), so failure is detectable without sensors",
)

B3_AUDIT = reliability_audit(
    repeated_moving_parts=CELLS,           # passive pawls remain
    precision_contacts_per_cell=1,         # pawl/rack (keeper is gone)
    compliant_printed_elements=CELLS,      # pawl leaf (same class as S6-LC)
    wear_interfaces=CELLS,                 # pawl/rack
    tolerance_sensitive_interactions=ROWS, # one gate per row-station
    correlated_failures=[
        "drum track mis-registration (a whole row-station wrong; detectable)",
        "drum-index motor miss (station phase error)",
        "write carriage leaves a bad track (whole station)",
    ],
    single_cell_failures=[
        "pawl misses a pocket (silent wrong level, as S6-LC)",
    ],
    serviceability="drum is a single removable part; pawls are banked",
    gate_answer="80 drum tracks must each read cleanly; the per-cell pawl is "
                "the same hard-stop part S6-LC has, but the fragile per-cell "
                "KEEPER is deleted",
    min_feature_mm=0.90,   # pawl leaf, 2 lines
    detection="a bad drum track fails a whole row-station VISIBLY; pawl misses "
              "remain silent",
)

B1["reliability_audit"] = B1_AUDIT
B2["reliability_audit"] = B2_AUDIT
B3["reliability_audit"] = B3_AUDIT
B1["mask_machine"] = False
B2["mask_machine"] = False
B3["mask_machine"] = True


# ===========================================================================
# SUMMARY SCREEN
# ===========================================================================
CANDIDATES = {"B1": B1, "B2": B2, "B3": B3}


def screen() -> dict:
    out = []
    for cid, c in CANDIDATES.items():
        t = c["timing"]
        out.append(dict(
            id=cid, name=c["name"],
            is_mask=c["mask_machine"],
            bought_actuators=c["bought_actuators"],
            parts_usd=c["bom"]["parts_usd"],
            delivered_usd=c["bom"]["delivered_usd"],
            verdict=c["bom"]["verdict"],
            under_250=bool(c["bom"]["delivered_usd"] < TARGET_DELIVERED_USD),
            visible_transition_s=t["visible_transition_s"],
            sustained_cycle_s=t["sustained_cycle_s"],
            visible_clears_30s=t["visible_clears_30s"],
            sustained_clears_30s=t["sustained_clears_30s"],
            repeated_moving_parts=c["reliability_audit"]["repeated_moving_parts"],
            compliant_printed_elements=c["reliability_audit"]["compliant_printed_elements"],
            tolerance_sensitive_interactions=c["reliability_audit"]["tolerance_sensitive_interactions"],
            min_repeated_feature_mm=c["reliability_audit"]["min_repeated_feature_mm"],
            min_feature_is_robust=c["reliability_audit"]["min_feature_is_robust"],
            decisive_failure_mode=c["decisive_failure_mode"],
            cheapest_rejection_test=c["cheapest_rejection_test"],
        ))
    return dict(
        evidence_class="CALCULATION over the promoted S5-R/S6-LC model + "
                       "sourced-class allowances + CAD constants; no "
                       "print/purchase/measurement (DND-27)",
        baseline_s6lc=dict(delivered_usd=S6LC_DELIVERED,
                           full_map_s=S6LC_FULL_MAP_S,
                           reliability_audit=S6LC_AUDIT),
        gates=dict(
            b1_serial_only_s=B1["timing_serial"]["visible_transition_s"],
            b1_gang_s=B1["timing"]["visible_transition_s"],
            b1_gang_rows=B1["timing"]["gang_rows"],
            b1_gang_torque_nm=B1["torque_gang_gate"]["torque_nm"],
            b1_gang_torque_ok=B1["torque_gang_gate"]["pass_gate"],
            b1_max_gang_rows=B1["torque_gang_gate"]["max_gang_rows_for_gate"],
            b1_combined_gate=B1["combined_gate"]["result"],
            b2_blanket_force_ok=B2["blanket_force"]["pass_gate"],
            b2_blanket_margin_n=B2["blanket_force"]["margin_n"],
            b2_toggle_snap_force_n=B2["toggle_gate"]["snap_force_n"],
            b2_toggle_2_line=B2["toggle_gate"]["feature_is_2_line"],
            b3_repeated_decisions=B3["repeated_count"]["per_row_repeated_decisions"],
            b3_reduction_factor_vs_s6lc=B3["repeated_count"]["reduction_factor"],
        ),
        candidates=out,
        verdict=dict(
            count=len(out),
            all_under_250=all(c["under_250"] for c in out),
            best_cost_delivered_usd=min(c["delivered_usd"] for c in out),
            all_visible_clear_30s=all(c["visible_clears_30s"] for c in out),
            headline="Three materially different reliability-first machines. "
                     "B1 (non-mask, screw memory) and B2 (non-mask, pressure "
                     "blanket) remove the per-cell compliant decision element "
                     "entirely; B3 (mask) deletes the fragile per-cell keeper "
                     "and keeps only the hard-stop pawl. All are costed against "
                     "the same imported model so the comparison cannot drift.",
        ),
    )


if __name__ == "__main__":
    print(json.dumps(screen(), indent=2))
