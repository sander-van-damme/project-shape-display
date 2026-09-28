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


# --- DND-44 cost closure anchors -------------------------------------------------
# The honest EXPECTED baseline: the sourced S5 BOM's own `unit_expected` column,
# on the repo's additive x1.16 delivered basis. This is materially worse than the
# old $501.12 headline (which used a $0.80 TB6612 and a best-case motor).
BOM_EXPECTED_PARTS_USD = 510.40
BOM_EXPECTED_DELIVERED_USD = round(BOM_EXPECTED_PARTS_USD * DELIVERED_UPLIFT, 2)
# The machine-preserving source path from cost_closure.py (sourced TB6612FNG
# driver, sourced multipack motor, register/controller consolidation, spares
# allowance removal, sourced fixed-line repricing). Reproduced by checks.py.
SOURCED_PATH_PARTS_USD = 366.34
SOURCED_PATH_DELIVERED_USD = round(SOURCED_PATH_PARTS_USD * DELIVERED_UPLIFT, 2)


def expected_baseline_delivered() -> float:
    return BOM_EXPECTED_DELIVERED_USD


def sourced_path_delivered() -> float:
    return SOURCED_PATH_DELIVERED_USD


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
        # DND-44 closure (buckling_closure.py): the SERVICE (distributed miniature)
        # load is now bounded, not assumed. A miniature's base spreads its weight
        # over N columns at 5.08 mm pitch; even a 1 kg miniature on the smallest
        # 25.4 mm base gives only 0.39 N/column (7.9% of the 4.96 N core, 12.7x
        # margin). The 1 N working assumption was conservative. The 4.96 N core
        # still does not meet the LOCALIZED 5 N abuse screen; a core re-size to
        # 1.10 mm gives 5.60 N and clears it, at the cost of step height 0.5->0.4 mm.
        "status": "closed-analytically (service) / bounded (localized abuse)",
        "result": f"service load <= 0.39 N/column ({CAM_CRITICAL_BUCKLING_N:.2f} N core, "
                  "12.7x margin); localized 5 N abuse screen needs a 1.10 mm core (5.60 N)",
        "gate": "distributed tabletop load < core OR core re-sized for the abuse screen",
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
        # DND-44 closure (cost_closure.py): the honest EXPECTED delivered baseline
        # is $592.06 ($510.40 x1.16), materially worse than the earlier $501.12
        # (which used a $0.80 TB6612 and a best-case motor). A machine-preserving
        # reduction path (sourced TB6612FNG $0.7955 driver, sourced multipack
        # motor $1.05, register/controller consolidation, spares allowance
        # removal, sourced fixed-line repricing) lands at $424.95 delivered,
        # $75.05 below the ceiling. The path clears only for a motor <= $1.86.
        "status": "closed-analytically on the sourced path (K7 is the residual)",
        "result": f"expected baseline ${expected_baseline_delivered():.2f} (over); machine-preserving "
                  f"source path ${sourced_path_delivered():.2f} (${CEILING_USD - sourced_path_delivered():.2f} margin); "
                  "breaks even at a $1.86 motor",
        "gate": f"< ${CEILING_USD:.0f} delivered on a sourced path, machine unchanged",
    },
    {
        "id": "K6",
        "risk": "full-map time exceeds 30 s at the realised step rate",
        # DND-44 closure (timing_closure.py): the 45.07 s sweep worst corner is NOT
        # a step-rate problem. The per-row rate-independent floor (engage/settle
        # dwells + scan acceleration) is what binds; it is 18.65 s at the design
        # point and 34.47 s at the worst corner, above the 30 s cap for ANY rate.
        # The design point needs only ~268 pps for 30 s (400 pps is used). The
        # single quantity to verify is the loaded engagement/settle dwell and the
        # scanner's 4000 mm/s^2, not a "measured >=400 pps rate".
        "status": "conditional (bound to assumption dwells, not to a measured rate)",
        "result": f"{FULL_MAP_TIME_S:.2f} s design point vs {DEADLINE_S:.0f} s; rate-independent floor "
                  f"{'18.65'} s; ~268 pps required for 30 s; worst corner 45.07 s is not rate-recoverable",
        "gate": f"< {DEADLINE_S:.0f} s holds at the design dwells (>=268 pps); verify loaded dwell + scan accel",
    },
    # --- DND-41: six previously unstated killers (Falsifier review §6) ---
    {
        "id": "K7",
        "risk": "purchased-actuator cost cliff (80 motors + 80 drivers) at $40/ea matched part",
        # DND-44: the cost path clears the ceiling only for a motor <= $1.86
        # delivered (cost_closure.py break-even). The $1.05 multipack is still
        # untraced; the $40 MOONS matched part would put the machine at ~$4,156.
        "status": "open (binding residual of the K5 path)",
        "result": "sub-$1.05 8 mm PM stepper is an untraced multipack; only traceable matched part "
                  "(MOONS 8PM020S1) is $40/ea -> 80 x $40 = $3,200; source path breaks even at $1.86/motor",
        "gate": "a matched motor quote <= $1.86 delivered (or a sourced-equivalent under the ceiling)",
    },
    {
        "id": "K8",
        "risk": "lateral holding: a knocked miniature applies lateral load",
        # DND-44 closure (cross_cutting_closure.py): the lateral load path is the
        # column body against its GUIDE and its free-length bending, not the
        # detent. A 1 N lateral load deflects ~0.01 mm (< the 0.10 mm gate); the
        # governing limit is ~9.4 N guide shear. The detent never held lateral
        # load and never had to. The printed guide-wall shear strength is the one
        # unmeasured term (DND-27).
        "status": "closed-analytically (guide carries lateral; detent never did)",
        "result": "1 N lateral -> 0.01 mm tip (< 0.10 mm gate); governing limit ~9.4 N; detent holds only "
                  "~0.002 N and is not the lateral constraint; printed guide-wall shear is the residual",
        "gate": "lateral load carried by guide/bending, not detent; guide-wall shear verified analytically",
    },
    {
        "id": "K9",
        "risk": "angular margin vs print tolerance (mis-seated toe)",
        "status": "open (delegated)",
        "result": "5 levels have 12.50 deg nominal margin, 6.50 deg after a 6 deg seating error; toe envelope 23.50 deg; "
                  "a +/-0.05 mm print tolerance on the 1.5 mm-radius rotor is several degrees and is not propagated",
        "gate": "Monte-Carlo angular error from +/-0.05 mm print tolerance keeps margin positive (interacts with K1)",
    },
    {
        "id": "K10",
        "risk": "regional-update time is untested end to end",
        # DND-44 (cross_cutting_closure.py): the common platen means one full
        # 41 mm stroke per update regardless of region size. Bounded: 1 row
        # ~3.9 s, 10 rows ~6.3 s, 20 rows ~8.9 s, full 80 rows ~24.7 s.
        "status": "closed-analytically (bounded)",
        "result": "one full platen stroke per update: 1 row ~3.9 s, 10 rows ~6.3 s, 20 rows ~8.9 s, 80 rows ~24.7 s",
        "gate": "regional update bounded including homing + full platen stroke",
    },
    {
        "id": "K11",
        "risk": "cycle life of the printed detent/ratchet",
        # DND-44 (cross_cutting_closure.py): detent surface strain 0.169% vs an
        # assumed 0.3% endurance strain; Basquin m=8 gives ~1e8 cycles. An
        # order-of-magnitude bound, NOT a qualification (creep/layer adhesion
        # unmeasured).
        "status": "bounded (order-of-magnitude, not qualified)",
        "result": "detent surface strain 0.169% vs assumed 0.3% endurance; ~1e8 cycles by Basquin m=8; "
                  "creep/layer adhesion unmeasured",
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
            "note": "DND-44: rate-independent floor 18.65 s binds; ~268 pps meets 30 s; the "
                    "45.07 s corner is not rate-recoverable",
        },
        "cost": {
            "parts_subtotal_usd": winner_parts_subtotal_usd(),
            "sourced_pair_usd": winner_delivered_usd(),
            "reduced_usd": winner_reduced_delivered_usd(),
            # DND-44 anchors: the honest EXPECTED baseline and the machine-
            # preserving source path (cost_closure.py), on the additive x1.16 basis.
            "expected_baseline_delivered_usd": expected_baseline_delivered(),
            "sourced_path_delivered_usd": sourced_path_delivered(),
            "ceiling_usd": CEILING_USD,
            "sourced_path_pass": sourced_path_delivered() < CEILING_USD,
            "pass": winner_reduced_delivered_usd() < CEILING_USD,
            "range_usd": [round(expected_baseline_delivered(), 2), round(sourced_path_delivered(), 2)],
            "note": "honest expected baseline is over the ceiling; the machine-preserving source "
                    "path clears it, conditional on a <=$1.86 motor (K7)",
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
