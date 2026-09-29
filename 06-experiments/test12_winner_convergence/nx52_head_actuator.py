"""DND-52 K7 actuator-class / drive-topology pivot -- analytic option screen.

Question (DND-52). [DND-49] refuted K7 on sourced evidence: no matched 8 mm
18 deg bipolar PM stepper exists at <= $1.86 delivered, so the S5
machine-preserving cost path (which clears the $500 ceiling on the DND-48 E1-E6
basis) has no orderable motor. The board and [DND-27] forbid a purchase sample.
The remaining agent-reachable avenue is a different **actuator class** or
**drive topology** that keeps the S5 architecture (programmed stepped rotary
stops + one common lift) but removes the 80-channel bought-motor cliff.

This module does NOT re-derive the S5 head timing or BOM (those live in
`timing_closure.py`, `cost_closure.py`, `k7_motor_trace.py` and are imported so
the two cannot drift). It enumerates concrete head-actuator / drive options,
costs each against the S5 fixed non-motor basis and the 30 s cap, and reports
the single measurement (if any) that would decide it.

Evidence class: CALCULATION over sourced listings and stated assumptions. No
purchase, no print, no measurement ([DND-27]). Sourced prices are point-in-time.
"""
from __future__ import annotations

import json
from pathlib import Path

import cost_closure as cc  # noqa: E402
import k7_motor_trace as k7  # noqa: E402
import timing_closure as tc  # noqa: E402

HERE = Path(__file__).resolve().parent
CEILING = cc.CEILING
UPLIFT = cc.UPLIFT
CHANNELS = 80

# The machine-preserving base already carries the E1 TB6612 driver line for all
# 80 channels (80 x $0.7955 = $63.64). A pivot may touch only the motor + driver
# channel lines; everything else is held fixed. `S5_DRIVER_PARTS` is that driver
# block, and `FIXED_PARTS_NO_CHANNEL` is the base with both the motor and driver
# channel lines removed so each option can declare its own channel cost exactly
# once (no double-count).
import cost_closure as cc  # noqa: E402  (already imported; kept for clarity)

S5_DRIVER_PARTS = round(CHANNELS * cc.TB6612_SOURCED, 2)
FIXED_PARTS = k7._fixed_parts()
FIXED_PARTS_NO_CHANNEL = round(FIXED_PARTS - S5_DRIVER_PARTS, 2)
S5_MOTOR_BREAK_EVEN = k7.verdict()["break_even_motor_usd"]


def delivered(parts_usd: float) -> float:
    return round(parts_usd * UPLIFT, 2)


def _verdict_row(parts_no_channel: float, cost_parts: float) -> tuple[float, bool]:
    """Delivered total and clear flag for a fixed base plus an explicit channel cost."""
    d = delivered(parts_no_channel + cost_parts)
    return d, d < CEILING


# ---------------------------------------------------------------------------
# 1. Shared-drive one-time programmable rotary register / Geneva-cam bank.
#
# A single drive motor rotates a bank of 80 rotors in lockstep through a
# Geneva-style index; printed registration pins or one mechanical single-turn
# clutch per column drop that column out of the drive path at its selected stop
# while the rest of the bank keeps rolling. Selection is a printable pin set by
# a small bank of "writer" solenoids OUTSIDE the dense region, not 80 bought
# motors inside the head. This is the project's stated preference: move cost
# from 80 bought motors to printed selection.
# ---------------------------------------------------------------------------
def shared_register_option() -> dict:
    index_motors = 2          # bank drive + release/index drive
    writers = 8               # off-pitch writer solenoids
    index_motor_usd = 12.00   # a fully orderable NEMA17-class stepper
    writer_usd = 2.50         # small 5 V solenoid, sourced-class allowance
    # No per-column bought motor or per-channel driver: those lines leave.
    parts = index_motors * index_motor_usd + writers * writer_usd
    # Replace the 80 per-cell step writes with a shared bank roll. Assumed
    # 300 rpm roll (5 x 72 deg = 1 rev) plus 0.05 s Geneva engage and 0.05 s
    # disengage per station (assumption; the repo has no measured roll).
    bank_roll_s = 1.0 / (300.0 / 60.0)
    station_s = 0.05 + bank_roll_s + 0.05
    stations = 20.0
    base = tc.full_map_s(400)
    per_cell_steps_s = CHANNELS * (tc.HOME_STEPS + tc.PROGRAM_STEPS) / 400.0
    full = base - per_cell_steps_s + stations * station_s
    d, clears = _verdict_row(FIXED_PARTS_NO_CHANNEL, parts)
    return dict(
        id="shared-rotary-register",
        one_line="1-2 motors roll a coupled 80-rotor bank through a Geneva index; "
                 "printed pins/clutches drop each column out at its selected stop.",
        actuator_count=index_motors + writers,
        actuator_cost_parts_usd=round(parts, 2),
        delivered_usd=d,
        clears_cost=clears,
        est_full_map_s=round(full, 2),
        clears_time=full < 30.0,
        pitch_feasibility="register lives in the head above the 5.08 mm field; "
                          "columns keep their 5-level rotors - pitch unchanged",
        deciding_quantity="whether 80 ganged rotors can be indexed and selectively "
                          "dropped/re-engaged reliably at 5.08 mm pitch -- a printed "
                          "coupon, forbidden under DND-27; the re-engage sync is an "
                          "unmodelled failure mode",
        verdict="COST+TIME FEASIBLE, MECHANISM UNPROVEN (needs a coupon)",
    )


# ---------------------------------------------------------------------------
# 2. Fewer bought channels + wider parallel head (80 -> 20 or 40).
#
# The decisive cost term is CHANNELS x unit. If each head station services R
# rows with a mechanical cam-bank programmer (the S3 topology, but writing S5's
# printed rotary-stop memory), the bought motor count falls to 80/R.
# ---------------------------------------------------------------------------
def wider_head_option(rows_per_station: int = 4) -> dict:
    stations = CHANNELS // rows_per_station
    # The cheapest MATCHED source is CCHT 07-005-032 at $8.20 only at the 3,001+
    # tier; a 20-40 piece order sits in the $11.20 (100-1,000) tier. Use the
    # realistic tier for the actual order quantity (honesty over the headline).
    motor_unit = 11.20
    # One bought motor + one dual H-bridge per station, not per column.
    parts = stations * (motor_unit + cc.TB6612_SOURCED)
    # A station's cam bank programs its R rows in PARALLEL in one pass, so the
    # program cost is per-station (one engage/write/settle), not R row-times.
    # The carriage indexes station-to-station; each step advances R rows.
    per_station = tc.per_row_assumption_s() + (tc.HOME_STEPS + tc.PROGRAM_STEPS) / 400.0
    index_step_s = tc._travel(rows_per_station * 5.08, tc.TIMING["scan_v_mm_s"],
                              tc.TIMING["scan_a_mm_s2"])
    full = (tc.fixed_s() + stations * per_station
            + (stations - 1) * index_step_s)
    d, clears = _verdict_row(FIXED_PARTS_NO_CHANNEL, parts)
    return dict(
        id=f"wider-head-R{rows_per_station}",
        one_line=f"{stations} stations x {rows_per_station} rows, each station a "
                 "mechanical cam-bank programmer over S5 rotary stops.",
        actuator_count=stations,
        actuator_cost_parts_usd=round(parts, 2),
        delivered_usd=d,
        clears_cost=clears,
        est_full_map_s=round(full, 2),
        clears_time=full < 30.0,
        pitch_feasibility=f"{rows_per_station} rows share one 5.08 mm band = "
                          f"{5.08 / rows_per_station:.2f} mm per row; S3's killed "
                          "1.27 mm land problem returns at R=4",
        deciding_quantity="same as the S3 fan-out: whether R printed selectors fit a "
                          "5.08 mm row band (DND-4 gate); analytically printable at "
                          "0.4 mm only as a journal-fit pivot, unproven in a machine",
        verdict="COST VIABLE ONLY WITH A MATCHED MOTOR AND A WIDER HEAD",
    )


# ---------------------------------------------------------------------------
# 3. Servo class (hobby micro servo per channel).
# ---------------------------------------------------------------------------
def servo_option(unit_usd: float = 2.50) -> dict:
    # Sourced datapoints in the repo: FS90 $7.90@5, SG90 23x12.2x29 mm. The
    # $2.50 is an optimistic 80-piece clone price ASSUMPTION. A servo replaces
    # both the motor and the per-channel dual H-bridge.
    parts = CHANNELS * unit_usd
    servo_move_s = 0.12 * (72.0 / 60.0)   # FS90 0.12 s/60 deg, 72 deg = 5 levels
    per_row = tc.per_row_assumption_s() + servo_move_s
    full = tc.fixed_s() + CHANNELS * per_row + (CHANNELS - 1) * tc.index_s()
    d, clears = _verdict_row(FIXED_PARTS_NO_CHANNEL, parts)
    return dict(
        id="servo-head",
        one_line=f"{CHANNELS} micro servos, one per column, angle-commanded.",
        actuator_count=CHANNELS,
        actuator_cost_parts_usd=round(parts, 2),
        delivered_usd=d,
        clears_cost=clears,
        est_full_map_s=round(full, 2),
        clears_time=full < 30.0,
        pitch_feasibility="standard micro servo body 12.2-23 mm wide; one per "
                          "5.08 mm column is physically impossible inside the head "
                          "band (repo datapoint: SG90 23 x 12.2 x 29 mm)",
        deciding_quantity="none -- a bought servo cannot fit a 5.08 mm column "
                          "channel; the class is rejected on geometry, not cost",
        verdict="REJECTED ON PITCH (cannot place one servo per 5.08 mm column)",
    )


# ---------------------------------------------------------------------------
# 4. Printed pancake / axial-flux stepper: a printed axial multipole rotor plus a
#    small bought stator coil set per column (no bought complete motor).
# ---------------------------------------------------------------------------
def printed_pancake_option() -> dict:
    coil_unit = 0.60            # wound bobbin + magnet, sourced-class allowance
    # The printed rotor replaces the bought motor; the per-channel dual H-bridge
    # is retained (still a 2-phase bipolar channel).
    parts = CHANNELS * (coil_unit + cc.TB6612_SOURCED)
    full = tc.full_map_s(400)   # still a per-column step-programmed head
    d, clears = _verdict_row(FIXED_PARTS_NO_CHANNEL, parts)
    return dict(
        id="printed-pancake",
        one_line="printed axial multipole rotor + a small bought stator coil per "
                 "column (no bought complete motor).",
        actuator_count=CHANNELS,
        actuator_cost_parts_usd=round(parts, 2),
        delivered_usd=d,
        clears_cost=clears,
        est_full_map_s=round(full, 2),
        clears_time=full < 30.0,
        pitch_feasibility="coil bobbin must fit 5.08 mm pitch; a hand-wound coil is "
                          "plausible but its torque at 5.08 mm is tiny",
        deciding_quantity="printed-rotor axial torque per ampere at 5.08 mm -- a "
                          "printed-pole coupon (forbidden under DND-27); meeting the "
                          "0.15 mN.m running torque cannot be shown analytically "
                          "without a magnetic FEA the repo does not have",
        verdict="UNPROVEN TORQUE CLASS (needs magnetic FEA + coupon)",
    )


# ---------------------------------------------------------------------------
# 5. Eliminate the travelling head: global lift + printable mechanical memory
#    (the S1/S2 broadcast family). The repo already killed this on force (S1)
#    and mask-write time (S2). Recorded so the option space is closed.
# ---------------------------------------------------------------------------
def global_memory_option() -> dict:
    parts = 3 * 12.00           # 2-4 shared lift/index motors; no per-channel parts
    d, clears = _verdict_row(FIXED_PARTS_NO_CHANNEL, parts)
    return dict(
        id="global-lift-printed-memory",
        one_line="2-4 shared lift motors + a printable rewritable pattern medium "
                 "(punched film / shutter sheet / threshold plates).",
        actuator_count=3,
        actuator_cost_parts_usd=round(parts, 2),
        delivered_usd=d,
        clears_cost=clears,
        est_full_map_s=56.0,
        clears_time=False,
        pitch_feasibility="media lives outside the dense column field; pitch unchanged",
        deciding_quantity="mask-write time for 12,800 unary decisions -- the repo shows "
                          ">=500 parallel writer channels (~9 s) or an off-line writer "
                          "(~56 s); no cheap writer exists, so surprise maps fail",
        verdict="KILLED EARLIER (S1 force / S2 mask write)",
    )


def options() -> list[dict]:
    return [
        shared_register_option(),
        wider_head_option(4),
        wider_head_option(2),
        servo_option(),
        printed_pancake_option(),
        global_memory_option(),
    ]


def s5_reference() -> dict:
    return dict(
        id="s5-bought-head",
        actuator_count=CHANNELS,
        matched_unit_usd=11.20,
        matched_delivered_usd=delivered(FIXED_PARTS + CHANNELS * 11.20),
        break_even_unit_usd=round(S5_MOTOR_BREAK_EVEN, 4),
        untraced_multipack_delivered_usd=delivered(
            FIXED_PARTS + CHANNELS * cc.MOTOR_SOURCED_MULTIPACK),
        note="the incumbent; refuted on sourced evidence by DND-49",
    )


def wider_head_cost_boundary(rows_per_station: int = 4) -> dict:
    """The per-station motor price at which the wider head clears the ceiling.

    This is the discriminating quantity for option 2: at the 100-qty matched
    tier ($11.20) it is over; only the 3,001+ tier ($8.20) would clear, and that
    tier is not reachable for a 20-40 piece order.
    """
    stations = CHANNELS // rows_per_station
    # fixed_no_channel + stations*(motor + driver) <= ceiling/uplift
    max_parts = CEILING / UPLIFT
    max_motor = (max_parts - FIXED_PARTS_NO_CHANNEL) / stations - cc.TB6612_SOURCED
    return dict(rows_per_station=rows_per_station, stations=stations,
                max_station_motor_usd=round(max_motor, 4),
                matched_100qty_usd=11.20, matched_3001qty_usd=8.20,
                clears_at_100qty=11.20 <= max_motor,
                clears_at_3001qty=8.20 <= max_motor)


def screen() -> dict:
    rows = options()
    survivors = [r["id"] for r in rows if r["clears_cost"] and r["clears_time"]]
    return dict(
        evidence_class="CALCULATION over sourced listings and stated assumptions; "
                       "no purchase, print or measurement (DND-27)",
        ceiling_usd=CEILING,
        s5_fixed_parts_usd=round(FIXED_PARTS, 2),
        s5_driver_block_usd=S5_DRIVER_PARTS,
        fixed_no_channel_usd=FIXED_PARTS_NO_CHANNEL,
        s5_motor_break_even_usd=round(S5_MOTOR_BREAK_EVEN, 4),
        s5_reference=s5_reference(),
        wider_head_boundary=wider_head_cost_boundary(4),
        options=rows,
        cost_time_survivors=survivors,
        mission_target_reachable=(
            "NOT DEMONSTRATED. No enumerated option is a proven buildable machine "
            "today. The shared rotary register clears cost and time analytically but "
            "rests on an unproven 80-rotor selective-dropout mechanism; the wider "
            "head clears only at a higher unit price and re-opens the S3 pitch gate; "
            "servo and pancake classes fail on pitch/torque; the global-memory family "
            "was already killed. The S5 incumbent is cost-closed only on an untraced "
            "multipack motor."
        ),
        recommendation=(
            "Adopt the shared-drive rotary register as the single serious pivot and "
            "define it as the next machine-definition target (S5-R); keep S5 as the "
            "fallback contingent on a matched <=$1.86 motor. The deciding quantity "
            "for S5-R is the selective-dropout/re-engage reliability of an 80-rotor "
            "bank at 5.08 mm pitch, which DND-27 forbids measuring, so the terminal "
            "state remains 'one printed coupon or one purchase sample away'."
        ),
    )


if __name__ == "__main__":
    print(json.dumps(screen(), indent=2))
