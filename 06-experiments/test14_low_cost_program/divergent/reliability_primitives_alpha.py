#!/usr/bin/env python3
"""DND-106 (child of DND-104) -- InventorAlpha: reliability-first cell / mask primitives.

QUESTION
========
[DND-104] is the CTO's **reliability-first** program. The S1/S2 mask family already
removes the cost problem (no per-cell and no per-row bought actuator), but its
weakest claim is the **reliability gate** ([DND-91] A6/G8):

    A map is correct only if all 6,400 cells are correct.  With per-cell error q
    the map yield is (1-q)^6400; a 99 % map needs q <= 1.57e-6.  The S6-LC cell
    has NO per-cell feedback, so a missed latch is a silent, undetectable,
    unrecoverable height error.

This module does **not** re-trim S6-LC and does **not** re-cost the machine. It
attacks the ONE question the reliability gate asks:

    > What has to work correctly 6,400 times?

...and tries to drive that count as close to **zero** as the mask family allows,
by inventing concrete cell / selection / reset primitives that are:

  * **binary** cells with **positive hard stops** (two states only, no 5-pocket
    continuous pawl whose release force is a threshold);
  * **shared mechanical state** so one failure is bounded to a row / bank, not a
    silent per-cell miss;
  * **detectable / recoverable** if a mechanical read path or a home feature can
    be had cheaply;
  * **mask media** that is printed or cheap and can be rewritten inside the
    visible budget.

WHAT IS HERE
============
Three materially different primitives (R1, R2, R3) plus a shared **conformance
harness** that runs every one of them through the **required reliability-audit
schema** (the DND-103 repeated-mechanism criteria) and the **ten functional
jobs**, so no primitive can hide a scaling word like "selector" or "latch":

  R1  **TOGGLE-ROCKER ROW-SHARED STATE ("one rocker = one row").** Replace the
      per-cell pawl-and-rack with a single **bistable rocker per row** whose
      hard-stop angle selects a stair step for that row's height class; each of
      the 80 cells in the row is a passive **tooth** on its column that rests on
      the selected step. Failure of the one rocker is a **whole-row** (80-cell),
      *detectable* event, not a silent per-cell miss. Cuts repeated moving parts
      from 6,400 latches to **80 rockers**.

  R2  **DOUBLE-ACTING WEDGE-GATE CELL (positive both ways).** Keep a per-cell
      state, but make it a **two-position sliding wedge gate** with a **positive
      printed hard stop in BOTH the raised and the lowered direction**, driven
      down by the platen on the reset stroke rather than "released" and trusted
      to drop. This is the direct answer to the S6-LC "jammed column does not
      drop on reset" (A8) failure. Attacks the *single-cell* failure class.

  R3  **MECHANICAL READ-ROD READBACK ("state is an edge, not a hidden tooth").**
      A cheap **mechanical read comb** seats against every cell's gate state and
      turns "did the gate seat?" into a **measurable edge** at a sparse set of
      sense points, without a bought sensor per cell. This is the
      **detectable / recoverable** primitive: it cannot make a cell more
      reliable, it makes the residual error **findable and correctable** (re-run
      the affected row/bank). It is what makes R1's correlated failure tolerable.

A fourth, **failed** candidate is recorded honestly:

  R4 (REJECTED) **one shared return bar as the reset** -- removes the state
      *detection* problem but the bar must overcome the **sum** of all cell
      forces (6,400 contacts), and a single jam anywhere stalls the whole bar.
      Recorded as a negative result (`r4_rejection`).

EVIDENCE CLASS (DND-27)
=======================
Everything here is **CALCULATION** over sourced FDM process limits and the
program's own DND-91/A6 reliability arithmetic, plus **CAD** geometry
(`scad/reliability_cell.scad`, analytic printability checked by
`tools/validate/analytic_printability.py`). There is **no print, no purchase, no
measurement**, and nothing here promotes an architecture, changes
`08-integrated-designs/s5r-shared-drive-register/`, or claims physical validation.

REPRODUCE
=========
    python 06-experiments/test14_low_cost_program/divergent/reliability_primitives_alpha.py
    python 06-experiments/test14_low_cost_program/divergent/reliability_primitives_alpha_checks.py
    python tools/validate/analytic_printability.py \
        06-experiments/test14_low_cost_program/divergent/scad/reliability_cell.scad
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent          # 06-experiments/test14_low_cost_program/divergent
REPO = HERE.parents[2]                       # repo root

# ---------------------------------------------------------------------------
# Shared program scale (02-design-criteria).  Named here, not re-typed from the
# machine model, so a drift is a deliberate, reviewable change.
# ---------------------------------------------------------------------------
PITCH_MM = 5.08
ROWS = 80
COLS = 80
CELLS = ROWS * COLS                              # 6,400
LEVEL_MM = 10.0
LEVELS = 5                                       # five binary masks -> five heights
TRAVEL_MM = LEVEL_MM * (LEVELS - 1)              # 40.0
ACTIVE_MM = ROWS * PITCH_MM                      # 406.4
TIME_GATE_S = 30.0
COST_GATE_USD = 250.0

# ---------------------------------------------------------------------------
# Sourced FDM process limits (same convention as primitives.py / s6lc.py).
# ---------------------------------------------------------------------------
NOZZLE_MM = 0.4
EXTRUSION_WIDTH_MM = 1.1 * NOZZLE_MM             # 0.44 mm, one line
MIN_FEATURE_MM = EXTRUSION_WIDTH_MM              # hard floor: 1 line
MIN_WALL_MM = 2.0 * EXTRUSION_WIDTH_MM           # 0.88 mm, robust 2-line wall
RECOMMENDED_WALL_MM = 3.0 * EXTRUSION_WIDTH_MM   # 1.32 mm, load-bearing
DIM_ACCURACY_MM = 0.10                           # per face (assumption class)
FEATURE_EPS_MM = 1e-6                            # float-comparison tolerance


def ge_feature(value_mm: float, limit_mm: float) -> bool:
    """`value >= limit` for sourced FDM limits, float-safe at the boundary.

    `0.44 * 2` is `0.8800000000000001` in binary float, so a literal `>= 0.88`
    would wrongly reject a part that is exactly the 2-line wall.  All printed
    feature comparisons go through this helper so the boundary is exact.
    """
    return value_mm >= limit_mm - FEATURE_EPS_MM


# ---------------------------------------------------------------------------
# Sourced material / load / friction class (as used across the programme).
# ---------------------------------------------------------------------------
E_PLA_MPA = 1500.0                               # sourced modulus 700-2500, mid
MU_PLA_LOW = 0.20
MU_PLA_MID = 0.35
MU_PLA_HIGH = 0.50
PLA_YIELD_MPA = 50.0                             # sourced conservative yield
PLA_COMPRESS_MPA = 50.0
COLUMN_SERVICE_LOAD_N = 3.27                     # [DND-48] K1 bounding terrain load
COLUMN_MASS_G = 1.6                              # S1 per-column moving-mass estimate
GRAVITY_MPS2 = 9.81

# ---------------------------------------------------------------------------
# Reliability-gate arithmetic (the ONE thing this module exists to minimize).
#
# DND-91/A6:  map yield = (1-q)^6400;  a 99 % map needs q <= 1.57e-6.
# ---------------------------------------------------------------------------
CELLS_TOTAL = CELLS
Q_BREAK_EVEN_99 = 1.0 - 0.99 ** (1.0 / CELLS_TOTAL)     # ~1.570e-6


def map_yield(q_per_repeated_unit: float, units: int) -> float:
    """Probability all `units` repeated functional units are correct."""
    return (1.0 - q_per_repeated_unit) ** units


def q_for_map_yield(target_yield: float, units: int) -> float:
    """Per-unit error budget for a target map yield across `units` units."""
    return 1.0 - target_yield ** (1.0 / units)


def correlated_uniformity_lesson() -> dict:
    """The reliability arithmetic every primitive here is built around.

    A **per-cell independent** error budget is punishing: to get a 99 % map the
    per-cell q must be <= 1.57e-6. But if the same mechanism's error is
    **correlated** across a whole row (one rocker), the number of *independent*
    units collapses from 6,400 to 80, and the same 99 % map only needs
    q <= ~1.26e-4 per row -- an ~80x looser requirement. Correlation is normally
    a *bad* thing (a bigger blast radius); here it is only acceptable because it
    is paired with **detectability and re-runnability** (R3): a whole row that
    fails together can be seen and re-driven; a single cell that fails silently
    cannot.
    """
    q_row = q_for_map_yield(0.99, ROWS)          # per row if rows independent
    q_bank = q_for_map_yield(0.99, 8)            # per bank of 10 rows
    return dict(
        cells=CELLS_TOTAL,
        q_per_cell_break_even_99=round(Q_BREAK_EVEN_99, 9),
        rows=ROWS,
        q_per_row_break_even_99=round(q_row, 9),
        row_vs_cell_looseness=round(q_row / Q_BREAK_EVEN_99, 1),
        q_per_bank_break_even_99=round(q_bank, 9),
        bank_vs_cell_looseness=round(q_bank / Q_BREAK_EVEN_99, 1),
        evidence="CALCULATION (DND-91/A6 yield algebra)",
        note="correlation is only acceptable when paired with R3 detection + "
             "bank re-run; a correlated error with NO read path is strictly "
             "worse than an independent one at the same q.")


# ===========================================================================
# The reliability-audit schema (02-design-criteria "Per-architecture
# reliability audit (required)" + the ten functional jobs + a decisive
# falsifier and a coupon test).  EVERY primitive is passed through audit() so
# none can omit a field.
# ===========================================================================
AUDIT_FIELDS = (
    "mechanism_plain_english",
    "diagram",
    "bought_delta_usd",
    "repeated_moving_parts",
    "precision_contacts_per_cell",
    "compliant_printed_elements",
    "wear_interfaces",
    "tolerance_sensitive_interactions",
    "correlated_failure_modes",
    "single_cell_failure_modes",
    "serviceability",
    "decisive_falsifier",
    "coupon_test",
    "what_must_work_6400_times",
)

JOB_FIELDS = (
    "visible_moving_element",
    "state_storage",
    "selection",
    "power_distribution",
    "motion_40mm",
    "retention",
    "lowering_reset",
    "full_map_update",
    "regional_update",
    "jam_handling",
    "power_loss",
    "assembly",
)


# ===========================================================================
# R1 -- TOGGLE-ROCKER, ONE PER ROW (shared state, whole-row correlation)
# ===========================================================================
# WHY.  S6-LC asks 6,400 independent printed latches to each seat.  Replace them
# with **one two-state rocker per row** (80 rockers total).  The rocker is a
# printed toggle with positive hard stops at two angles; it carries a **ledge
# staircase** with one step per height class (0/10/20/30/40 mm).  Each cell in
# the row is a purely **passive tooth** on its column that rests on the step the
# rocker presents.  The shared state is the *rocker angle*; the per-cell state
# is the column's rest position on the staircase, which is not a latch at all.
#
# WHAT THIS BUYS.  Repeated moving parts = 80 rockers (not 6,400 latches).  A
# rocker that fails to toggle takes out ONE ROW, and R3 reads the rocker angle
# directly, so the failure is **visible and re-runnable**.  The per-cell
# mechanism is a tooth and a stationary staircase -- no per-cell spring, no
# per-cell release-force threshold.
#
# HONEST COST.  The rocker must present each step as a positive stop; the column
# tooth loads that step in COMPRESSION (column -> tooth -> step -> post).  A
# row whose rocker jams costs 80 cells but is detectable.  The rocker toggle is
# set by the shared mask-gate stack (DND-76 P2 class), not a bought actuator.

R1 = {
    "id": "R1",
    "name": "Toggle-rocker row-shared state (one rocker = one row)",
    "family": "shared mechanical state / whole-row correlation",
    "rockers": ROWS,                             # 80, one per row
    "columns": CELLS,                            # 6,400 passive
    "rocker_states": 2,                          # binary toggle, hard stops
    "rocker_ledge_steps": LEVELS - 1,            # 4 height steps (0/10/20/30/40)
    "step_tooth_w_mm": 0.90,                     # 2-line ledge tooth
    "step_tooth_l_mm": 2.40,
    "rocker_arm_t_mm": 1.32,                     # 3-line load-bearing arm
}

R1_JOBS = {
    "visible_moving_element": "6,400 square printed columns (passive)",
    "state_storage": "rocker angle (2 hard-stopped states) selects a staircase "
                     "step; the column rests on the step (no per-cell latch)",
    "selection": "one mask bit per (row, level) toggles the row rocker; 80x4 "
                 "= 320 bits total (vs 6,400 cell-decisions)",
    "power_distribution": "shared platen broadcast strokes; rockers switched by "
                          "the mask-gate stack (shared, bank-local)",
    "motion_40mm": "4 broadcast 10 mm platen strokes (common, paid once)",
    "retention": "column tooth in compression on a stationary printed step",
    "lowering_reset": "platen lowers; columns follow the staircase down as the "
                      "rocker re-toggles per level (positive, not released)",
    "full_map_update": "mask write (bank-local) + 4 broadcast strokes; see timing",
    "regional_update": "row-local: one rocker + its staircase is a row segment",
    "jam_handling": "a jammed column stops its own tooth; other columns in the "
                    "row still reach their steps (independent verticals). A "
                    "jammed ROCKER is detected by R3 (rocker-angle read).",
    "power_loss": "columns rest on the staircase; no power holds the state",
    "assembly": "80 row rocker modules + 6,400 passive column/tooth prints; "
                "no per-cell two-part latch",
}


def r1_geometry() -> dict:
    """Printability + pitch budget for the row rocker and its staircase.

    The rocker sits BESIDE the row, not inside the 5.08 mm cell pitch, so it is
    not pitch-constrained (02-design-criteria: internal machinery may be larger,
    shared, external).  Only the staircase step that the column tooth rests on
    is at the column, and it is a 2-line compression land.
    """
    step_ok = ge_feature(R1["step_tooth_w_mm"], MIN_WALL_MM)
    arm_ok = ge_feature(R1["rocker_arm_t_mm"], RECOMMENDED_WALL_MM)
    tooth_allow_n = R1["step_tooth_w_mm"] * R1["step_tooth_l_mm"] * PLA_COMPRESS_MPA
    return dict(
        step_tooth_width_mm=R1["step_tooth_w_mm"],
        step_tooth_is_2line=bool(step_ok),
        rocker_arm_thickness_mm=R1["rocker_arm_t_mm"],
        rocker_arm_is_3line=bool(arm_ok),
        tooth_compression_allow_n=round(tooth_allow_n, 1),
        cell_service_load_n=COLUMN_SERVICE_LOAD_N,
        tooth_load_margin=round(tooth_allow_n / COLUMN_SERVICE_LOAD_N, 1),
        rocker_off_pitch=True,
        printable=bool(step_ok and arm_ok),
        evidence="CALCULATION (PLA compression + sourced FDM wall rules)")


def r1_failure_arithmetic() -> dict:
    """Correlated vs silent: what R1 changes about the 6,400-times question."""
    repeated_decisions = ROWS
    return dict(
        repeated_moving_decisions=repeated_decisions,
        s6lc_repeated_decisions=CELLS,
        decision_reduction=round(CELLS / repeated_decisions, 1),
        correlated_blast_radius_cells=COLS,
        detectability="R3 reads the rocker angle mechanically (1 read point "
                      "per row -> 80 points), so a bad row is FINDABLE",
        recovery="re-toggle the row rocker and re-run its stroke <= 1 s",
        residual_risk="the rocker's own toggle can stick; a stuck rocker is a "
                      "whole-row error, bounded and visible",
        honest_verdict="R1 turns 6,400 silent independent decisions into 80 "
                       "detectable row decisions.  It does not eliminate "
                       "failure; it makes failure bounded and visible.")


# ===========================================================================
# R2 -- DOUBLE-ACTING WEDGE-GATE CELL (positive hard stop in BOTH directions)
# ===========================================================================
# WHY.  S6-LC's reset (DND-91 A8) releases the pawls and TRUSTS gravity to drop
# the columns; a jammed column silently keeps its stale height.  R2 replaces the
# release-and-hope with a **positive, driven** reset: a two-position sliding
# wedge gate whose LOW stop is reached by the platen PUSHING it down, and whose
# HIGH stop is a printed wall.  The gate's position is set by the mask comb; its
# state is a *position bounded by two hard stops*, so neither friction nor a
# spring's exact force decides it.
#
# This is the per-cell primitive (the opposite bet from R1's shared state): keep
# a per-cell state but make BOTH transitions positive events.  It attacks the
# *single-cell* failure class rather than the correlated class.

R2 = {
    "id": "R2",
    "name": "Double-acting wedge-gate cell (positive hard stops both ways)",
    "family": "per-cell positive hard stops / driven reset",
    "states": 2,
    "gate_throw_mm": 1.40,                       # full travel between hard stops
    "gate_body_t_mm": 0.90,                      # 2-line sliding wedge
    "gate_lane_mm": 1.48,
    "gate_clearance_worst_mm": round(1.48 - 0.90 - 2 * DIM_ACCURACY_MM, 3),
    "high_stop": "printed wall (raised state)",
    "low_stop": "printed wall (lowered state), reached by the platen push",
}

R2_JOBS = {
    "visible_moving_element": "6,400 square printed columns",
    "state_storage": "sliding wedge gate between two printed hard stops; each "
                     "cell owns its 2-state gate",
    "selection": "per-cell gate set by the printed mask comb (bank-local); the "
                 "gate blocks or clears the column's lift tooth",
    "power_distribution": "shared platen broadcast strokes",
    "motion_40mm": "4 broadcast 10 mm platen strokes",
    "retention": "column tooth on the gate's raised hard stop (compression)",
    "lowering_reset": "the platen's DOWN stroke PUSHES every gate to its low "
                      "stop (positive reset); a column cannot stay high",
    "full_map_update": "comb write + 4 strokes + driven reset",
    "regional_update": "comb is bank-local; neighbours hold",
    "jam_handling": "a sticky gate is driven through by the platen (the wedge "
                    "self-clears toward the low stop); a hard-wedged gate is "
                    "found by R3",
    "power_loss": "gate is a position between walls; columns rest on it",
    "assembly": "6,400 column + gate prints + shared combs",
}


def r2_geometry() -> dict:
    """Pitch budget + printability for the double-acting wedge gate."""
    lane = R2["gate_lane_mm"]
    body = R2["gate_body_t_mm"]
    clear = lane - body - 2 * DIM_ACCURACY_MM
    return dict(
        lane_mm=lane, gate_body_mm=body,
        gate_is_2line=bool(ge_feature(body, MIN_WALL_MM)),
        worst_case_running_clearance_mm=round(clear, 3),
        clearance_pass=bool(clear >= 0.10),
        throw_mm=R2["gate_throw_mm"],
        note="the gate slides in the 1.48 mm lane beside a 3.60 mm column body; "
             "the pitch band sees only the gate body (0.88 mm), and the gate is "
             "BESIDE the column, not in the neighbour's half-lane",
        evidence="CALCULATION (sourced wall + +/-0.10 mm/face print error)")


def r2_reset_positive() -> dict:
    """Why a driven reset removes the A8 jam failure class."""
    return dict(
        s6lc_reset="release pawls, trust gravity to drop (A8: a jam keeps stale "
                   "height, silent)",
        r2_reset="platen down-stroke pushes the wedge gate to a printed low "
                 "stop; the gate position is forced, not released",
        jam_class_removed="a gate that is merely sticky is driven through; only "
                          "a hard wedge (debris) resists, and that is detectable",
        residual_risk="a gate hard-wedged by foreign debris is still a single-"
                      "cell error; R3 finds it",
        reset_force_per_cell_n=0.61,             # DND-76 P1 class snap
        reset_force_6400_n=round(0.61 * CELLS, 1),
        reset_force_note="driven by the platen, whose global lift axis is "
                         "already sized for the whole board",
        evidence="CALCULATION + mechanism argument (assumption-class force)")


# ===========================================================================
# R3 -- MECHANICAL READ-ROD READBACK (detectable / recoverable state)
# ===========================================================================
# WHY.  Every primitive above leaves a residual error possibility.  The gate's
# whole complaint about S6-LC is not that errors happen -- it is that errors are
# SILENT (A6).  R3 adds a **read path**: a comb of compliant read fingers sweeps
# over a row; a finger that cannot seat (because the gate is in the wrong state)
# transmits an edge to a shared **read-out rod / mechanical memory bar**.  One
# per-row read point, 80 total, turns a silent per-cell error into a **row/
# bank alarm**.  It is deliberately mechanical so it buys NO sensor per cell.
#
# This primitive does not reduce q; it converts "undetectable" into "detectable
# and re-runnable", which is the specific reliability criterion DND-103 names
# ("detectable, recoverable, local and repairable").

R3 = {
    "id": "R3",
    "name": "Mechanical read-rod readback (detectable / recoverable state)",
    "family": "detection + recovery, no per-cell sensor",
    "read_fingers_per_row": COLS,                # 80 fingers, one comb per row
    "read_points": ROWS,                         # 80 mechanical read points total
    "compliant_elements": COLS * ROWS,           # one finger per cell
    "read_force_per_finger_n": 0.05,             # tiny sensing only (assumption)
    "bought_sensors": 2,                         # one read-rod edge sensor + home
    "bought_delta_usd": 2.00,
}

R3_JOBS = {
    "visible_moving_element": "6,400 columns (unchanged by readback)",
    "state_storage": "unchanged (R1 rocker or R2 gate)",
    "selection": "unchanged",
    "power_distribution": "read comb is driven by the same platen/index motion "
                          "(no new bought axis)",
    "motion_40mm": "unchanged",
    "retention": "unchanged",
    "lowering_reset": "after reset, the read pass runs before the next map is "
                      "accepted",
    "full_map_update": "read pass adds one row-sweep per row; budget below",
    "regional_update": "read only the affected rows",
    "jam_handling": "a non-seating finger flags its row; the controller re-runs "
                    "that row and reports it; a persistent flag = serviceable cell",
    "power_loss": "state holds; readback is repeatable after power returns",
    "assembly": "80 read combs + 1 shared read-out mechanism",
}


def r3_detection_arithmetic() -> dict:
    """What a 1-bit-per-row read path does to the effective failure count.

    A detector lets the controller re-run a flagged row.  If a row re-run
    succeeds with probability p, the residual SILENT error per row is
    q_row*(1-p).  Even p=0.9 turns a 1.26e-4 row error into 1.26e-5 of silent
    error, and the flagged 10 % is visible and correctable at the table.
    """
    q_row = q_for_map_yield(0.99, ROWS)
    p_recovered = 0.90
    return dict(
        read_points=ROWS,
        detects_whole_row=True,
        detects_single_cell=False,
        row_flagged_error_q=round(q_row, 9),
        p_row_rerun_recovers=p_recovered,
        silent_error_after_readback=round(q_row * (1.0 - p_recovered), 9),
        effective_decision_units=ROWS,
        bought_sensors=R3["bought_sensors"],
        sensor_delta_usd=R3["bought_delta_usd"],
        honest_limit="R3 cannot see WHICH cell in the row is wrong (that needs "
                     "80 read points / row); it flags the ROW, which is enough "
                     "to re-run and to call a human for a persistent cell",
        evidence="CALCULATION (yield algebra with a recovery factor, "
                 "assumption-class for p)")


def r3_readback_budget() -> dict:
    """Visible-budget cost of a full read pass (calculation, assumption-class)."""
    per_row_s = 0.25                             # sweep + seat + release
    full_s = ROWS * per_row_s
    return dict(
        per_row_s=per_row_s,
        full_map_read_pass_s=round(full_s, 2),
        note="a read pass is a diagnostic, not every map; it can be run on the "
             "affected bank(s) only (8 rows = 2.0 s) after a regional update",
        evidence="ASSUMPTION-class timing, same class as the S5/S6 dwells")


# ===========================================================================
# R4 (REJECTED) -- one shared return bar as the reset (recorded negative result)
# ===========================================================================
# The attractive-looking idea: one rigid bar lifts EVERY cell's gate at once, so
# there is no per-cell reset at all and the state is trivially uniform.  It is
# REJECTED because it moves the reliability problem from "per-cell" to "one huge
# shared member" without any detection path, and the force concentrates: the bar
# must sum every cell's release force and any single jam stalls the whole bar
# (a 6,400-cell correlated stall with no read path).  This is the failure mode
# DND-103 explicitly warns about ("one cause taking out many cells" with "no
# practical recovery or detection path").

R4_REJECTION = {
    "id": "R4",
    "name": "Shared return bar (one bar resets every cell)",
    "verdict": "REJECTED",
    "reasons": [
        "force concentrates: the bar must overcome the SUM of all cell release "
        f"forces ({round(0.61 * CELLS, 1)} N at a 0.61 N/cell class snap), "
        "which no cheap printed bar/motor can drive reliably",
        "a single jammed cell stalls the entire 6,400-cell bar (correlated "
        "whole-board stall) with no detection path",
        "the bar is a long slender printed member across 406.4 mm: its own "
        "bending/straightness becomes a tolerance-critical shared failure",
        "it removes neither the cell state nor the need to set the per-cell "
        "selection; it only removes the per-cell reset actuator, which was not "
        "the bottleneck",
    ],
    "recorded_as_evidence": True,
    "lesson": "shared state is only a win when the shared member can TOLERATE a "
              "local jam (R1's per-row rockers can; R4's single bar cannot).",
}


# ===========================================================================
# The audit harness: run any primitive through the required schema + jobs.
# ===========================================================================
def audit(primitive_id: str, mechanism: dict, audit_fields: dict,
          jobs: dict, geometry: dict) -> dict:
    """Conformance-check one primitive against the required reliability audit.

    Returns the merged record plus explicit `missing_fields` / `unanswered_jobs`
    lists, so a primitive that hides a field or a functional job FAILS the
    conformance gate instead of silently passing.
    """
    merged = dict(primitive_id=primitive_id, name=mechanism["name"],
                  family=mechanism["family"])
    for f in AUDIT_FIELDS:
        merged[f] = audit_fields.get(f)
    merged["missing_fields"] = [f for f in AUDIT_FIELDS
                                if merged.get(f) in (None, "")]
    merged["unanswered_jobs"] = [j for j in JOB_FIELDS
                                 if jobs.get(j) in (None, "")]
    merged["jobs"] = {j: jobs.get(j) for j in JOB_FIELDS}
    merged["geometry"] = geometry
    merged["conforms"] = bool(not merged["missing_fields"]
                              and not merged["unanswered_jobs"])
    return merged


def r1_audit() -> dict:
    g = r1_geometry()
    fa = r1_failure_arithmetic()
    return audit(
        "R1", R1, jobs=R1_JOBS, geometry=g,
        audit_fields=dict(
            mechanism_plain_english=(
                "One two-state printed rocker per row (80 total) toggles between "
                "two hard-stopped angles. Each rocker carries a 4-step staircase; "
                "a column's passive tooth rests on the step exposed for that "
                "row's commanded height class (0/10/20/30/40 mm). 6,400 columns "
                "are passive; only 80 rockers move."),
            diagram=(
                "   row (80 cells, 5.08 mm pitch)\n"
                "   [col][col][col] ... [col]      <- passive columns + tooth\n"
                "      \\   \\   \\       /          <- teeth rest on steps\n"
                "   === staircase (4 steps) ===    <- one shared rocker/row\n"
                "            ||\n"
                "      rocker pivot -> 2 hard stops\n"
                "            ||  set by mask-gate stack (shared, bank-local)\n"),
            bought_delta_usd=0.0,
            repeated_moving_parts="80 rockers (1 per row); 6,400 passive columns",
            precision_contacts_per_cell=1,
            compliant_printed_elements="0 per-cell springs; rocker toggle is a "
                                       "2-line printed link (1 per row, 80 total)",
            wear_interfaces="rocker pivot journal (80), column-tooth/step land "
                            "(one per cell, in compression); service life "
                            "measurement-only",
            tolerance_sensitive_interactions="the step heights (4 per rocker) "
                                             "must be printed accurately; each "
                                             "is a 10 mm class step so a 0.5 mm "
                                             "error is 5 % of a level, not a "
                                             "make/break fit",
            correlated_failure_modes="a stuck rocker takes out its whole row "
                                     "(80 cells) -- DETECTABLE by R3",
            single_cell_failure_modes="a column tooth that fails to rest on the "
                                      "step (worn tooth, debris) -- local, "
                                      "flagged by R3 as a row event",
            serviceability="rocker modules are off-pitch row cartridges and are "
                           "replaceable individually; columns are drop-in",
            decisive_falsifier="if the rocker cannot present a reliable hard "
                               "stop under a full row load (80 x 3.27 N = "
                               f"{round(80 * COLUMN_SERVICE_LOAD_N, 1)} N) "
                               "without deflecting past a step, R1 dies",
            coupon_test="3x1 row coupon: one rocker + 3 columns at true 5.08 mm "
                        "pitch; cycle the rocker to each of 4 steps 100x and "
                        "measure which step each column rests on",
            what_must_work_6400_times=(
                f"{fa['repeated_moving_decisions']} row-rocker decisions "
                "(the 6,400 columns are passive)")))


def r2_audit() -> dict:
    g = r2_geometry()
    rp = r2_reset_positive()
    return audit(
        "R2", R2, jobs=R2_JOBS, geometry=g,
        audit_fields=dict(
            mechanism_plain_english=(
                "Each cell has a 2-position sliding wedge gate between two "
                "printed hard stops. Up = the gate's shoulder blocks the column's "
                "lift tooth (cell stays low); down = the tooth passes (cell "
                "advances). The mask comb sets the gate up; the platen's DOWN "
                "stroke PUSHES every gate to its low stop, so reset is a driven, "
                "positive event (not a release-and-hope)."),
            diagram=(
                "   high stop (printed wall)\n"
                "     |==| <- wedge gate body (0.88 mm)\n"
                "     |==|    slides in the 1.48 mm lane\n"
                "     |==| -> pushed DOWN by the platen reset stroke\n"
                "   low stop  (printed wall)\n"
                "   column tooth rides / clears the gate shoulder\n"),
            bought_delta_usd=0.0,
            repeated_moving_parts="6,400 sliding wedge gates (6,400 columns "
                                  "passive in Z, gates move ~1.4 mm)",
            precision_contacts_per_cell=2,
            compliant_printed_elements="0 critical springs; a return leaf may be "
                                       "printed but the LOW stop is driven, not "
                                       "spring-held",
            wear_interfaces="gate slide faces (6,400), gate shoulder/column tooth "
                            "contact (6,400); a low-friction slide is the wear "
                            "concern -- service life measurement-only",
            tolerance_sensitive_interactions="gate body 0.88 mm in a 1.48 mm lane "
                                             "leaves 0.40 mm worst-case, so the "
                                             "slide is tolerant, but the gate "
                                             "throw is 1.40 mm and must clear the "
                                             "tooth; a 0.2 mm error is 14 % of "
                                             "the throw (robust)",
            correlated_failure_modes="none by design: each gate is independent; a "
                                     "shared comb that fails to set a bank is "
                                     "detected by R3",
            single_cell_failure_modes="a gate hard-wedged by debris keeps its "
                                      "state; a gate that slips high blocks a "
                                      "cell wrongly -- both local, flagged by R3",
            serviceability="columns lift out; gates are replaceable cell inserts",
            decisive_falsifier="if the platen down-stroke cannot drive all gates "
                               "to the low stop (force x friction) or the gate "
                               "does not clear the tooth within +/-0.10 mm print "
                               "error, R2 dies",
            coupon_test="3x1 cell coupon at true 5.08 mm pitch: 3 gates, cycle "
                        "set/drive-reset 100x, measure gate seating and residual "
                        "column height error",
            what_must_work_6400_times=(
                "6,400 gate set/reset events -- but every RESET is a driven "
                "positive stop, so the failure needs a HARD wedge, not a sticky "
                "release (the A8 class is removed)")))


def r3_audit() -> dict:
    da = r3_detection_arithmetic()
    return audit(
        "R3", R3, jobs=R3_JOBS, geometry=r3_readback_budget(),
        audit_fields=dict(
            mechanism_plain_english=(
                "A read comb of 80 compliant fingers sweeps one row. Each finger "
                "tries to seat against its cell's gate; if the gate is not in the "
                "expected state the finger cannot seat and overloads a shared "
                "read-out rod, which trips one mechanical edge per row. 80 read "
                "points total (one per row), no per-cell sensor."),
            diagram=(
                "   read comb (80 compliant fingers)\n"
                "   v v v v v v v v v ... v\n"
                "   [c][c][c][c][c][c][c][c]   <- cell gates\n"
                "        \\  one non-seating finger\n"
                "         --> shared read-out rod --> 1 edge / row\n"
                "   80 rows => 80 read points, 2 bought sensors total\n"),
            bought_delta_usd=R3["bought_delta_usd"],
            repeated_moving_parts="80 read combs (one per row) + 1 shared read-out "
                                  "rod; the read fingers are compliant, not "
                                  "load-bearing",
            precision_contacts_per_cell=1,
            compliant_printed_elements="80 x 80 compliant read fingers (one per "
                                       "cell) -- deliberately SOFT, only sensing",
            wear_interfaces="finger tips against gate faces (6,400 contacts per "
                            "read pass); the fingers are the sacrificial part and "
                            "are printed/replaceable",
            tolerance_sensitive_interactions="the finger must not seat on a "
                                             "WRONG gate but must seat on a RIGHT "
                                             "one; the gate throw (1.40 mm) is "
                                             "far larger than the +/-0.10 mm "
                                             "print error, so the sense is robust",
            correlated_failure_modes="a bent shared read-out rod could false-flag "
                                     "a whole bank; a rod is a large accessible "
                                     "part and is the intended service item",
            single_cell_failure_modes="a single non-seating finger correctly FLAGS "
                                      "its cell's row; that is the point",
            serviceability="read combs and the read-out rod are off-pitch and "
                           "replaceable; a flagged cell is located by re-reading "
                           "the row with the gate forced",
            decisive_falsifier="if a compliant finger cannot distinguish a seated "
                               "gate from an unseated one at the 1.40 mm gate "
                               "throw and +/-0.10 mm print error, R3 provides no "
                               "usable signal and dies",
            coupon_test="3x1 readback coupon: 3 gates set to a known mix of "
                        "states, sweep the read comb 100x and measure the "
                        "detection rate and false-positive rate",
            what_must_work_6400_times=(
                "1 read decision per row (80/read-pass); it exists so that the "
                "6,400 cell events do not have to be perfect silently. "
                f"Silent per-row error after one re-run: "
                f"{da['silent_error_after_readback']:.2e}")))


# ===========================================================================
# End-to-end timing budget (CALCULATION, assumption-class -- NOT a measurement)
# ===========================================================================
# Reuses the S6-LC broadcast structure (its 11.96 s full-map model) and adds the
# primitive-specific terms: R2's driven reset reuses the platen stroke, R1's
# rocker toggle is set during the mask write, R3's read pass is optional /
# regional and is NOT counted in the every-map visible budget.
STROKE_MM = LEVEL_MM
PLATEN_SPEED_MM_S = 20.0
STROKES = LEVELS - 1
SETTLE_S = 0.15
RETURN_S = 0.20
MASK_WRITE_PER_BANK_S = 0.50
BANKS = 8
RESET_PER_BANK_S = 0.55                          # driven reset, platen-driven
READ_PASS_PER_ROW_S = 0.25


def timing() -> dict:
    """Honest visible-transition budget for the R1+R2 machine (no R3 read pass)."""
    per_stroke = STROKE_MM / PLATEN_SPEED_MM_S + SETTLE_S + RETURN_S
    armed = STROKES * per_stroke
    mask_write = BANKS * MASK_WRITE_PER_BANK_S
    reset = BANKS * RESET_PER_BANK_S                # driven, platen-uses-own-axis
    full = armed + mask_write + reset
    return dict(
        strokes=STROKES,
        per_stroke_s=round(per_stroke, 3),
        armed_strokes_s=round(armed, 3),
        mask_write_s=round(mask_write, 3),
        driven_reset_s=round(reset, 3),
        full_map_visible_s=round(full, 3),
        clears_30s=bool(full < TIME_GATE_S),
        margin_s=round(TIME_GATE_S - full, 3),
        read_pass_s=round(ROWS * READ_PASS_PER_ROW_S, 2),
        read_pass_in_visible_budget=False,
        read_pass_note="the R3 read pass is a verify/regional step, reported "
                       "separately (DND-103: report visible transition and "
                       "sustained cycle separately); a full read pass is "
                       f"{round(ROWS * READ_PASS_PER_ROW_S, 2)} s and a regional "
                       "read of one bank (8 rows) is "
                       f"{round(8 * READ_PASS_PER_ROW_S, 2)} s",
        evidence="CALCULATION (assumption-class dwells, same class as S6-LC)")


# ===========================================================================
# Purchased BOM delta (vs the S6-LC baseline) -- printed parts excluded (DND-70)
# ===========================================================================
def bom_delta() -> dict:
    """The bought-component delta of the primitive set against S6-LC."""
    lines = [
        dict(item="Read-out edge sensor (R3)", qty=1, unit=1.00,
             evidence="allowance",
             use="one mechanical edge per read-out rod"),
        dict(item="Read-out rod home sensor (R3)", qty=1, unit=1.00,
             evidence="allowance", use="datum for the read pass"),
        dict(item="Extra wiring for read-back (R3)", qty=1, unit=2.00,
             evidence="allowance", use="2-3 signal lines, no per-cell loom"),
    ]
    delta = round(sum(l["qty"] * l["unit"] for l in lines), 2)
    return dict(lines=lines, bought_delta_usd=delta,
                per_cell_bought_hardware=0,
                printed_parts_excluded=True,
                note="R1 and R2 add ZERO bought parts (all printed). R3 adds one "
                     "read-out edge sensor line at the bank level, not per cell.",
                evidence="CALCULATION + allowance-class pricing (DND-27)")


# ===========================================================================
# Convergence: can R1 + R2 + R3 be combined into one machine?  (Yes, and how.)
# ===========================================================================
def combination() -> dict:
    """How the three primitives compose (they are not alternatives)."""
    return dict(
        cell_state="R1 (row rocker + staircase) OR R2 (per-cell wedge gate) -- "
                   "they are the two cell bets and are mutually exclusive; the "
                   "rest compose with either",
        reset="R1 follows the staircase down (positive); R2 is driven by the "
              "platen down-stroke (positive) -- BOTH remove the A8 gravity-drop "
              "failure class",
        detection="R3 composes with either R1 or R2; it is the readability that "
                  "makes a correlated error acceptable",
        recommended_combo="R2 + R3 (per-cell positive stops + detectability): "
                          "keeps the smallest blast radius (1 cell) while "
                          "removing both the silent-failure (R3) and the "
                          "gravity-drop (R2) failure classes",
        alternative_combo="R1 + R3 (80 moving decisions): best on the 'what must "
                          "work 6,400 times' gate, at the cost of an 80-cell "
                          "blast radius per rocker and a stricter rocker-stiffness "
                          "requirement",
        not_composed="R1 and R2 are not both used on the same cell (they are two "
                     "different cell states)")


def decide() -> dict:
    audits = [r1_audit(), r2_audit(), r3_audit()]
    tm = timing()
    bd = bom_delta()
    lesson = correlated_uniformity_lesson()
    return dict(
        issue="DND-106 (child of DND-104)",
        evidence_class="CALCULATION + CAD; no print, no purchase, no measurement "
                       "(DND-27)",
        primitives_defined=3,
        primitives_conforming=[a["primitive_id"] for a in audits if a["conforms"]],
        primitives_failed_conformance=[a["primitive_id"] for a in audits
                                       if not a["conforms"]],
        rejected_recorded=[R4_REJECTION["id"]],
        reliability_lesson=lesson,
        timing=tm,
        bom_delta=bd,
        combination=combination(),
        gates={
            "reliability_audit_complete": all(a["conforms"] for a in audits),
            "full_map_under_30s": tm["clears_30s"],
            "bought_delta_zero_or_negligible": bd["bought_delta_usd"] <= 5.0,
            "at_least_three_materially_different": len(
                {a["family"] for a in audits}) >= 3,
            "failed_ideas_recorded": bool(R4_REJECTION["recorded_as_evidence"]),
        },
        decisive_next_test=(
            "3x1 / 5x5 true-pitch coupon (DND-27 forbids the print): one row "
            "(R1) and three cells (R2) exercised 100x each, plus the R3 read "
            "comb detection-rate test. This is the cheapest experiment that can "
            "reject the whole family BEFORE any CAD/BOM detail."),
        residual_uncertainty=[
            "Every force number is CALCULATION over sourced PLA class values; "
            "the rocker toggle force and the gate slide friction are "
            "assumption-class until a coupon is measured (forbidden under "
            "DND-27).",
            "R3's detection and false-positive rates are unmeasured; the "
            "1-read-per-row granularity is a design claim, not a result.",
            "The row-staircase step-height accuracy of an FDM print is not "
            "measured; it is the R1 decisive falsifier.",
            "Timing is assumption-class dwells, not a measured cycle.",
        ])


def screen() -> dict:
    return dict(
        evidence_class="CALCULATION + CAD (DND-27); no print/purchase/measurement",
        question="What has to work correctly 6,400 times?",
        correlated_uniformity_lesson=correlated_uniformity_lesson(),
        R1=r1_audit(),
        R2=r2_audit(),
        R3=r3_audit(),
        R4_rejected=R4_REJECTION,
        timing=timing(),
        bom_delta=bom_delta(),
        combination=combination(),
        decision=decide(),
    )


if __name__ == "__main__":
    print(json.dumps(screen(), indent=2))




