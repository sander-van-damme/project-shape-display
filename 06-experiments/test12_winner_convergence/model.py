"""DND-35 winner convergence stack-up (S5 rotary stops + common lift).

This module is the single executable place that turns the *selected* architecture
into an end-to-end stack-up: full-map time, purchased cost, per-cell reliability,
regional-update isolation and travel. It reads no private state; all inputs are
named constants or read from the source artefacts it cites.

Evidence class: CALCULATION / SIMULATION over sourced and assumed inputs. Nothing
here is a print and nothing here is a physical measurement (DND-27).
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent

# ---------------------------------------------------------------------------
# 1. Winner selection. Every other candidate carries an explicit kill record.
# ---------------------------------------------------------------------------
WINNER = "S5"
# disposition: kill | park | win, with the binding evidence string.
# Two-bet framing (Falsifier): S1-S4 are Bet A (written passive memory); S5 is
# Bet B (absolute geometric stops - a homed rotor + gravity-following toe, no
# written bit). A Bet-A failure does not imply Bet-B failure. S1/S2/S4 cost is
# CONDITIONAL on the print gate, not a kill (their BOMs are fallback-inflated).
DISPOSITIONS = {
    "S1": ("kill", "Bet A: worst-case all-armed stroke 2368 N > 1500 N cap; mask write needs >=500 channels"),
    "S2": ("park", "Bet A: survives only double-buffered with an off-line writer; no surprise-map path; cost conditional on print gate"),
    "S3": ("kill", "Bet A: sourced selectors drive delivered $2880.98 (5.8x ceiling); fan-out fit gate is a separate DND-4 question"),
    "S4": ("park", "Bet A: printed dog clutch must carry tile torque; bus backlash fails 0.25 mm at 3 deg/joint; cost conditional on print gate"),
    "S5": ("win", "Bet B: absolute stops; only CAD+simulation+sourced-BOM candidate; 26.25 s best-corner; sourced cost path $501.12"),
}

# ---------------------------------------------------------------------------
# 2. Machine constants (sourced from Test08 params.json + Test09 validation).
# ---------------------------------------------------------------------------
ROWS = 80
COLS = 80
CELLS = ROWS * COLS           # 6400
PITCH_MM = 5.08
TRAVEL_MM = 40.0
LEVELS = 5
DEADLINE_S = 30.0             # hard product cap
ENGINEERING_S = 27.0          # internal target with margin
CEILING_USD = 500.0           # purchased-component ceiling
PRINT_FLOOR_USD = 400.0       # board "acceptable" band top

# Test08/Test09 selected motion + structure numbers (calculated).
FULL_MAP_TIME_S = 26.251292522118074   # Test09 summary.json:16
LIFT_STROKE_MM = TRAVEL_MM + 1.0       # 41 mm including unload clearance
CAM_CORE_RADIUS_MM = 1.0
CAM_CRITICAL_BUCKLING_N = 4.96488      # uniform-beam check, Test09
SERVICE_LOAD_N = 1.0                   # product: 1 N on one cell for 24 h (UNSOURCED, see K1)
ABUSE_SCREEN_N = 5.0                   # Test08 measurement-protocol gate; the 4.96 N core does not meet it
PER_CELL_ERROR = 0.0001                # q = 1e-4 conservative for the stack-up

# Test09 540-case timing sweep (results/timing_sweep.csv). Falsifier Finding B:
# the 26.251 s baseline is the best corner, not the operating point.
DESIGN_RATE_PPS = 400
TIMING_CASES_PER_RATE = 108
TIMING_PASS_400 = 17                   # under_30 == True at 400 pps
TIMING_WORST_400_S = 45.07             # max time_s at 400 pps

# ---------------------------------------------------------------------------
# 3. Cost model: the sourced winner BOM, plus a reduction path to clear $500.
# ---------------------------------------------------------------------------
# Fixed (non motor/driver) purchased subtotal from the sourced S5 delivered BOM
# (bom_S5_delivered.csv, expected scenario), excluding the PM motor and the
# Dual H-bridge line. Reproduced by checks.py from the CSV.
FIXED_SUBTOTAL_USD = 284.0
MOTOR_CHANNELS = COLS                  # 80, one per column of the head
DRIVER_CHANNELS = COLS
# Reduction path: fold the 40 discrete 74HC595 shift registers into the custom
# driver PCB (a line already in the BOM) and use the sourced RP2040 controller.
# DND-41 (Falsifier Finding A): the $14 register line is a *gross* allowance
# removal. The 40 x $0.35 = $14.00 expected allowance goes away, but the chips are
# still BOUGHT: sourced LCSC 74HC595D is $0.0925/ea, 40 x $0.0925 = $3.70. The NET
# register saving is $10.30, not $14.00.
REGISTER_ALLOWANCE_USD = 14.0          # 40 x $0.35 expected, removed
REGISTER_CHIP_COST_USD = 3.70          # 40 x $0.0925 sourced LCSC 74HC595D, still bought
REDUCTION_REGISTERS_USD = REGISTER_ALLOWANCE_USD - REGISTER_CHIP_COST_USD  # net = $10.30
REDUCTION_CONTROLLER_USD = 5.0         # $10 expected -> RP2040 $5 sourced

# Sourced candidate prices (USD/ea, delivered-inclusive uplift applied by checks).
SOURCED_MOTOR_USD = 1.05               # Amazon multipack listing, 2026-09-28
SOURCED_DRIVER_USD = 0.80              # TB6612FNG @100 (dual H-bridge, one bipolar motor)
# DND-41 (Falsifier Finding A): the repo's own delivered_cost_model.py applies the
# expected uplift ADDITIVELY (sub + sub*0.10 + sub*0.06 = sub*1.16). The prior
# 1.10*1.06 = 1.166 was a multiplicative double-count that inflated the headline.
DELIVERED_UPLIFT = 1.10 + 0.06         # expected scenario: +10% ship, +6% tax (additive)


def winner_delivered_usd(motor_usd: float = SOURCED_MOTOR_USD,
                         driver_usd: float = SOURCED_DRIVER_USD,
                         fixed_usd: float = FIXED_SUBTOTAL_USD) -> float:
    """Delivered purchased total for the winner (sourced pair, expected uplift)."""
    parts = fixed_usd + MOTOR_CHANNELS * motor_usd + DRIVER_CHANNELS * driver_usd
    return round(parts * DELIVERED_UPLIFT, 2)


def winner_parts_subtotal_usd(motor_usd: float = SOURCED_MOTOR_USD,
                             driver_usd: float = SOURCED_DRIVER_USD,
                             fixed_usd: float = FIXED_SUBTOTAL_USD) -> float:
    """Purchased parts subtotal, before the delivered uplift."""
    return fixed_usd + MOTOR_CHANNELS * motor_usd + DRIVER_CHANNELS * driver_usd


def winner_reduced_delivered_usd() -> float:
    """Winner with the two concrete BOM consolidations, delivered.

    Moves the discrete shift registers onto the driver PCB (net $10.30 saving
    after still buying the 40 chips at $0.0925) and uses the sourced RP2040
    controller ($5 saving). This brings the machine back under the ceiling; the
    margin is real but small. The <$400 ideal band is not demonstrated.
    """
    fixed = FIXED_SUBTOTAL_USD - REDUCTION_REGISTERS_USD - REDUCTION_CONTROLLER_USD
    return winner_delivered_usd(fixed_usd=fixed)


# ---------------------------------------------------------------------------
# 4. Reliability: probability that every one of 6400 cells is correct.
# ---------------------------------------------------------------------------
def p_perfect_map(q: float = PER_CELL_ERROR, cells: int = CELLS) -> float:
    return (1.0 - q) ** cells


def required_q_for(p_target: float = 0.99, cells: int = CELLS) -> float:
    return 1.0 - p_target ** (1.0 / cells)


# ---------------------------------------------------------------------------
# 5. Regional isolation: rail-coupled neighbour bound (J2 analytic gate).
# ---------------------------------------------------------------------------
NEIGHBOUR_GATE_MM = 0.10               # allowed displacement of an untouched cell
J2_NEIGHBOUR_MM = 0.017                # 20x20 rail-coupled bound from J2 analytic gate


# ---------------------------------------------------------------------------
# 6. Killer list + cheapest falsification for the winner.
# ---------------------------------------------------------------------------
KILLERS = [
    {
        "id": "K1",
        "risk": "cam buckling under handling load; service load not sourced",
        "status": "open",
        # DND-41 (Falsifier Finding D): the 5 N screen is a Test08
        # measurement-protocol gate with pass/fail; test08/README.md:263 says the
        # 4.96 N core does not meet it and to expect a redesign. The
        # reclassification to "handling screen" is only valid if the 1 N service
        # load is a true tabletop bound; the repo has NOT sourced it.
        "result": f"{CAM_CRITICAL_BUCKLING_N:.2f} N critical < {ABUSE_SCREEN_N:.0f} N screen; "
                  f"{SERVICE_LOAD_N:.0f} N service load is an UNSOURCED assumption",
        "gate": f">= {ABUSE_SCREEN_N:.0f} N abuse screen (Test08 measurement-protocol gate, not met) "
                f"OR a sourced <= 4.5 N tabletop-load bound",
    },
    {
        "id": "K2",
        "risk": "printed rotary detent holds height and repeats after a slipped step",
        "status": "conditional-analytically",
        "result": "nominal leaf corrects an 18 deg slip only for mu <= 0.323; at the "
                  "sourced PLA-PLA midpoint mu=0.35 torque/friction = 0.92 (fails); "
                  "closing levers: mu <= 0.32 or scallop depth >= 0.31 mm",
        "gate": "detent corrects one 18 deg step across the sourced friction range",
    },
    {
        "id": "K3",
        "risk": "gravity return vs guide friction across 6400 columns",
        "status": "closed-analytically",
        "result": "20.29 mN weight vs 5 mN assumed drag = 4.06x; 15.29 mN headroom (solid column)",
        "gate": "drag < 0.5 x weight",
    },
    {
        "id": "K4",
        "risk": "regional update disturbs a loaded neighbour",
        "status": "partially-closed",
        # DND-41 (Falsifier Finding C): the cited J2 gate returns INCONCLUSIVE for
        # each tile (J2-0 rig qualification missing by design). 0.017 mm is only a
        # rail-bending STRUCTURAL sub-bound; stiction release and wear drift are
        # measurement-only terms and stay open.
        "result": f"{J2_NEIGHBOUR_MM} mm structural (rail-bending) bound vs {NEIGHBOUR_GATE_MM} mm gate; "
                  "J2 engine returns INCONCLUSIVE (rig noise, stiction release, wear drift are measurement-only)",
        "gate": f"< {NEIGHBOUR_GATE_MM} mm for each boundable term; release/drift remain open measurement-class risks",
    },
    {
        "id": "K5",
        "risk": "purchased cost exceeds $500 delivered",
        "status": "closed-analytically (range)",
        "result": f"sourced pair ${winner_delivered_usd():.2f} (over ceiling); reduced "
                  f"${winner_reduced_delivered_usd():.2f}; real but small margin",
        "gate": f"< ${CEILING_USD:.0f} delivered",
    },
    {
        "id": "K6",
        "risk": "full-map time exceeds 30 s at the realised step rate",
        "status": "conditional",
        # DND-41 (Falsifier Finding B): 26.251 s is the best corner of the repo's
        # 540-case timing_sweep.csv. At 400 pps only 17/108 pass 30 s; worst
        # 45.07 s. No measured >=400 pps loaded rate exists; the 3.749 s margin is
        # withdrawn.
        "result": f"{FULL_MAP_TIME_S:.2f} s best-corner vs {DEADLINE_S:.0f} s; at {DESIGN_RATE_PPS:.0f} pps "
                  f"only {TIMING_PASS_400}/{TIMING_CASES_PER_RATE} sweep cases pass, worst {TIMING_WORST_400_S:.2f} s",
        "gate": f"< {DEADLINE_S:.0f} s requires a measured >= {DESIGN_RATE_PPS:.0f} pps loaded rate "
                "(or inspection>0 still under 30 s)",
    },
    # --- DND-41: six previously unstated killers (Falsifier review §6) ---
    {
        "id": "K7",
        "risk": "purchased-actuator cost cliff (80 motors + 80 drivers) at $40/ea matched part",
        "status": "open",
        "result": "the sub-$1.05 8 mm PM stepper is an untraced multipack; the only traceable matched part "
                  "(MOONS 8PM020S1) is $40/ea -> 80 x $40 = $3,200 (8x ceiling)",
        "gate": "a matched sub-$1.05 motor quote (or a sourced-equivalent matched part under the ceiling)",
    },
    {
        "id": "K8",
        "risk": "lateral holding: a knocked miniature applies lateral load resisted only by the detent/bushing",
        "status": "open",
        "result": "hard stop resists DOWNWARD load; detent peak restoring torque ~0.00139 mN.m (detent_torque.csv); "
                  "Test08 measurement protocol has a 'lateral handling 0.1 N / 1 N' gate with no analytic pass",
        "gate": "analytically bound lateral restoring torque >= worst-case lateral load, or an honest permitted side-load",
    },
    {
        "id": "K9",
        "risk": "angular margin vs print tolerance (mis-seated toe)",
        "status": "open",
        "result": "5 levels have 12.50 deg nominal margin, 6.50 deg after a 6 deg seating error; toe envelope 23.50 deg; "
                  "a +/-0.05 mm print tolerance on the 1.5 mm-radius rotor is several degrees and is not propagated",
        "gate": "Monte-Carlo angular error from +/-0.05 mm print tolerance keeps margin positive (interacts with K1)",
    },
    {
        "id": "K10",
        "risk": "regional-update time is untested end to end",
        "status": "open",
        "result": "regional rewrite still needs head home/reference (0.5 s axis reference + 0.4 s ready settle) and a "
                  "full 41 mm platen stroke (whole platen moves); reliability.regional_update_seconds is 'perfect-scaling'",
        "gate": "end-to-end regional-update timing bound including homing + full platen stroke",
    },
    {
        "id": "K11",
        "risk": "cycle life of the printed detent/ratchet",
        "status": "open",
        "result": "detent_torque is a single-cycle static model; creep/fatigue of a printed 0.45 mm leaf over thousands "
                  "of writes is unmodelled; cross-cutting with K2",
        "gate": "cycle-life bound for the printed leaf under repeated writes (or a spring detent)",
    },
    {
        "id": "K12",
        "risk": "coarse-slope / multi-level usability",
        "status": "open",
        "result": "5-level coarse steps (10 mm) over a battle map may be too coarse for terrain readability; a "
                  "product/usability assumption not yet tested",
        "gate": "product decision on level count vs angular margin (6 levels -> 0.50 deg after 6 deg seating error)",
    },
]


def stackup() -> dict:
    return {
        "winner": WINNER,
        "dispositions": DISPOSITIONS,
        "time": {
            "full_map_s": FULL_MAP_TIME_S,
            "deadline_s": DEADLINE_S,
            "engineering_target_s": ENGINEERING_S,
            # Best-corner only. CONDITIONAL: pass requires a measured >=400 pps
            # loaded rate. The prior 3.749 s "margin" is withdrawn (DND-41).
            "pass": FULL_MAP_TIME_S < DEADLINE_S,
            "conditional": True,
            "design_rate_pps": DESIGN_RATE_PPS,
            "sweep_pass_400": TIMING_PASS_400,
            "sweep_cases_per_rate": TIMING_CASES_PER_RATE,
            "sweep_worst_400_s": TIMING_WORST_400_S,
            "margin_s": round(DEADLINE_S - FULL_MAP_TIME_S, 3),
            "note": "best corner of the 540-case sweep; no measured loaded rate exists",
        },
        "cost": {
            "parts_subtotal_usd": winner_parts_subtotal_usd(),
            "sourced_pair_usd": winner_delivered_usd(),
            "reduced_usd": winner_reduced_delivered_usd(),
            "ceiling_usd": CEILING_USD,
            # Honest: the sourced pair is AT/OVER the ceiling; only the reduced
            # path clears it. The headline is a range at the ceiling.
            "sourced_pair_pass": winner_delivered_usd() < CEILING_USD,
            "pass": winner_reduced_delivered_usd() < CEILING_USD,
            "range_usd": [round(winner_delivered_usd(), 2), round(winner_reduced_delivered_usd(), 2)],
            "note": "sourced pairing is at/over the ceiling; reduction is real but small",
        },
        "reliability": {
            "q": PER_CELL_ERROR,
            "p_perfect_map": p_perfect_map(),
            "required_q_99pct": required_q_for(0.99),
            "note": "no per-cell feedback; q is an assumption, not measured",
        },
        "isolation": {
            "neighbour_mm": J2_NEIGHBOUR_MM,
            "gate_mm": NEIGHBOUR_GATE_MM,
            "pass": J2_NEIGHBOUR_MM < NEIGHBOUR_GATE_MM,
            "conditional": True,
            "note": "structural rail-bending sub-bound only; J2 engine returns INCONCLUSIVE",
        },
        "travel": {
            "travel_mm": TRAVEL_MM,
            "levels": LEVELS,
            "increment_mm": TRAVEL_MM / (LEVELS - 1),
            "pass": TRAVEL_MM >= 40.0,
        },
        "killers": KILLERS,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(stackup(), indent=2))
