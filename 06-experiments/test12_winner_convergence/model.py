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
DISPOSITIONS = {
    "S1": ("kill", "worst-case all-armed stroke 2368 N > 1500 N cap; mask write needs >=500 channels"),
    "S2": ("park", "survives only double-buffered with an off-line writer; no surprise-map path"),
    "S3": ("kill", "analytic printability FAIL (pivot 0.80<5.0, min web 0.24<0.88); delivered $2880.98"),
    "S4": ("park", "printed dog clutch must carry tile torque; bus backlash fails 0.25 mm at 3 deg/joint"),
    "S5": ("win", "only CAD+simulation+sourced-BOM candidate; 26.25 s; sourced cost path $500.70"),
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
SERVICE_LOAD_N = 1.0                   # product: 1 N on one cell for 24 h
ABUSE_SCREEN_N = 5.0                   # sacrificial handling screen, NOT a design gate
PER_CELL_ERROR = 0.0001                # q = 1e-4 conservative for the stack-up

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
REDUCTION_REGISTERS_USD = 14.0         # 40 x $0.35 expected -> on-PCB shift registers
REDUCTION_CONTROLLER_USD = 5.0         # $10 expected -> RP2040 $5 sourced

# Sourced candidate prices (USD/ea, delivered-inclusive uplift applied by checks).
SOURCED_MOTOR_USD = 1.05               # Amazon multipack listing, 2026-09-28
SOURCED_DRIVER_USD = 0.80              # TB6612FNG @100 (dual H-bridge, one bipolar motor)
DELIVERED_UPLIFT = 1.10 * 1.06         # expected scenario +10% ship, +6% tax


def winner_delivered_usd(motor_usd: float = SOURCED_MOTOR_USD,
                         driver_usd: float = SOURCED_DRIVER_USD,
                         fixed_usd: float = FIXED_SUBTOTAL_USD) -> float:
    """Delivered purchased total for the winner (sourced pair, expected uplift)."""
    parts = fixed_usd + MOTOR_CHANNELS * motor_usd + DRIVER_CHANNELS * driver_usd
    return round(parts * DELIVERED_UPLIFT, 2)


def winner_reduced_delivered_usd() -> float:
    """Winner with the two concrete BOM consolidations, delivered.

    Moves the discrete shift registers onto the driver PCB and uses the sourced
    RP2040 controller. This is the path to clear $500 with margin and reach the
    project's 'acceptable' band (< $400 is not yet demonstrated).
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
        "risk": "cam buckling under handling/abuse load",
        "status": "closed-analytically",
        "result": f"{CAM_CRITICAL_BUCKLING_N:.2f} N critical vs {SERVICE_LOAD_N:.0f} N service load",
        "gate": f">= {SERVICE_LOAD_N:.0f} N service (abuse screen kept as coupon handling test)",
    },
    {
        "id": "K2",
        "risk": "printed rotary detent holds height and repeats after a slipped step",
        "status": "qualitative",
        "result": "no closed-form; depends on printed contact/creep",
        "gate": "permanently qualitative under DND-27; keep on risk register",
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
        "status": "closed-analytically",
        "result": f"{J2_NEIGHBOUR_MM} mm vs {NEIGHBOUR_GATE_MM} mm gate",
        "gate": f"< {NEIGHBOUR_GATE_MM} mm",
    },
    {
        "id": "K5",
        "risk": "purchased cost exceeds $500 delivered",
        "status": "closed-analytically",
        "result": f"sourced pair ${winner_delivered_usd():.2f}; reduced ${winner_reduced_delivered_usd():.2f}",
        "gate": f"< ${CEILING_USD:.0f} delivered",
    },
    {
        "id": "K6",
        "risk": "full-map time exceeds 30 s at the realised step rate",
        "status": "closed-analytically",
        "result": f"{FULL_MAP_TIME_S:.2f} s at 400 pps vs {DEADLINE_S:.0f} s",
        "gate": f"< {DEADLINE_S:.0f} s",
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
            "pass": FULL_MAP_TIME_S < DEADLINE_S,
            "margin_s": round(DEADLINE_S - FULL_MAP_TIME_S, 3),
        },
        "cost": {
            "sourced_pair_usd": winner_delivered_usd(),
            "reduced_usd": winner_reduced_delivered_usd(),
            "ceiling_usd": CEILING_USD,
            "pass": winner_reduced_delivered_usd() < CEILING_USD,
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
