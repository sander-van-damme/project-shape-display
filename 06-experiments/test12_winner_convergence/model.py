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
# Two-bet framing (Falsifier DND-36): S1-S4 are Bet A (written passive memory);
# S5 is Bet B (absolute geometric stops). A Bet-A failure does not imply Bet-B
# failure. S1/S2/S4 cost is CONDITIONAL on the print gate, not a kill.
DISPOSITIONS = {
    "S1": ("kill", "Bet A: worst-case all-armed stroke 2368 N > 1500 N cap; mask write needs >=500 channels"),
    "S2": ("park", "Bet A: survives only double-buffered with an off-line writer; no surprise-map path"),
    "S3": ("kill", "Bet A: analytic printability FAIL (pivot 0.80<5.0, min web 0.24<0.88); delivered $2880.98 (sourced selectors)"),
    "S4": ("park", "Bet A: printed dog clutch must carry tile torque; bus backlash fails 0.25 mm at 3 deg/joint"),
    "S5": ("win", "Bet B: absolute stops; only CAD+simulation+sourced-BOM candidate; 26.25 s best corner; sourced pair $501.12 at/over ceiling, reduced $491.03 (additive basis)"),
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
# Reduction path: fold the 40 discrete 74HC595 shift registers onto the custom
# driver PCB and use the sourced RP2040 controller.
#
# Corrected twice, and reconciled with the DND-37 BOM ratification:
#  - the register line LEAVES the BOM entirely, so the saving is the *sourced*
#    value you would actually have paid (40 x $0.0925 = $3.70), not the $14
#    expected allowance (Falsifier promotion review DND-36; CostManufacturing
#    DND-37). Previously the model subtracted the full $14 allowance.
#  - the controller line's saving is the real delta $10 expected -> $5 sourced.
#  - the delivered uplift is ADDITIVE (the repository's own
#    delivered_cost_model.py: parts * (1 + 0.10 + 0.06) = parts * 1.16), not the
#    multiplicative 1.10 * 1.06 used by ratify_bom.py.
REGISTER_SOURCED_LINE_USD = 40 * 0.0925   # = $3.70, value removed when on-PCB
CONTROLLER_EXPECTED_USD = 10.0            # fixed-subtotal controller allowance
CONTROLLER_SOURCED_USD = 5.0              # sourced RP2040

# Sourced candidate prices (USD/ea). Corrected uplift: the repository's own cost
# model (delivered_3scenario/delivered_cost_model.py) applies shipping+tax
# ADDITIVELY to the parts subtotal: parts * (1 + 0.10 + 0.06) = parts * 1.16.
# DELIVERED_UPLIFT = 1.10 * 1.06 = 1.166 was inconsistent with that model and
# overstated the margin (Falsifier promotion review, DND-36).
SOURCED_MOTOR_USD = 1.05               # Amazon multipack listing, 2026-09-28
SOURCED_DRIVER_USD = 0.80              # TB6612FNG @100 (dual H-bridge, one bipolar motor)
SHIPPING_FRACTION = 0.10               # expected scenario
TAX_FRACTION = 0.06                    # expected scenario
DELIVERED_UPLIFT = 1.0 + SHIPPING_FRACTION + TAX_FRACTION   # = 1.16, additive


def winner_delivered_usd(motor_usd: float = SOURCED_MOTOR_USD,
                         driver_usd: float = SOURCED_DRIVER_USD,
                         fixed_usd: float = FIXED_SUBTOTAL_USD) -> float:
    """Delivered purchased total for the winner (sourced pair, expected uplift)."""
    parts = fixed_usd + MOTOR_CHANNELS * motor_usd + DRIVER_CHANNELS * driver_usd
    return round(parts * DELIVERED_UPLIFT, 2)


def winner_reduced_delivered_usd() -> float:
    """Winner with the two concrete BOM consolidations, delivered.

    The register line leaves the BOM (saving its sourced value $3.70), and the
    controller allowance $10 is replaced by the sourced RP2040 $5. This is the
    path to clear $500 with a small margin; the <$400 ideal band is not
    demonstrated. Reconciled with DND-37 (CostManufacturing) on the additive
    project basis: parts $423.30 -> $491.03 delivered.
    """
    fixed = (
        FIXED_SUBTOTAL_USD
        - REGISTER_SOURCED_LINE_USD
        - CONTROLLER_EXPECTED_USD
        + CONTROLLER_SOURCED_USD
    )
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
        "status": "open/contestable",
        "result": f"{CAM_CRITICAL_BUCKLING_N:.2f} N critical vs 5 N abuse screen (fails by 0.8%); "
                  f"1 N service load is an unsourced assumption (miniature_measured:false)",
        "gate": "closes only on a SOURCED <=4.5 N tabletop-vertical-load bound",
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
        "status": "partially-closed (structural bound only)",
        "result": f"{J2_NEIGHBOUR_MM} mm rail-coupled structural sub-bound vs {NEIGHBOUR_GATE_MM} mm gate; "
                  f"cited rig returns INCONCLUSIVE; stiction release + wear drift are measurement-class",
        "gate": "< 0.10 mm, but failure-relevant terms unclosable under DND-27",
    },
    {
        "id": "K5",
        "risk": "purchased cost exceeds $500 delivered",
        "status": "conditional",
        "result": f"additive basis: sourced pair ${winner_delivered_usd():.2f} (at/over ceiling); "
                  f"reduced ${winner_reduced_delivered_usd():.2f}",
        "gate": f"< ${CEILING_USD:.0f} delivered; small real margin on the reduced path only",
    },
    {
        "id": "K6",
        "risk": "full-map time exceeds 30 s at the realised step rate",
        "status": "conditional",
        "result": f"{FULL_MAP_TIME_S:.2f} s is the best corner of the Test09 540-case sweep; "
                  f"at 400 pps only 17/108 cases pass, worst 45.07 s",
        "gate": "< 30 s; needs a measured >=400 pps loaded rate",
    },
    {
        "id": "K7",
        "risk": "motor-cost cliff (80 motors + 80 drivers)",
        "status": "open",
        "result": "only traceable matched 8 mm PM stepper is $40/ea -> 80 x $40 = $3,200 (8x ceiling); "
                  "$1.05 price is an untraced marketplace multipack",
        "gate": "needs a sourced matched sub-$1.05 motor quote",
    },
    {
        "id": "K8",
        "risk": "lateral holding of a knocked miniature",
        "status": "open",
        "result": "hard stop resists downward load; lateral load resisted only by detent "
                  "(peak restoring torque ~0.0014 mN.m) and printed bushing",
        "gate": "Test08 lateral handling gate (0.1 N / 1 N) has no analytic closure",
    },
    {
        "id": "K9",
        "risk": "angular margin vs print tolerance",
        "status": "open",
        "result": "12.50 deg nominal margin falls to 6.50 deg after a 6 deg seating error; "
                  "+/-0.05 mm print tolerance on a 1.5 mm rotor is not propagated",
        "gate": "Monte-Carlo angular error from +/-0.05 mm tolerance",
    },
    {
        "id": "K10",
        "risk": "regional-update time not bounded end to end",
        "status": "open",
        "result": "any write needs a full 41 mm platen stroke and head home/reference "
                  "(0.5 s axis reference + 0.4 s settle per activation)",
        "gate": "bound regional update time in Test12",
    },
    {
        "id": "K11",
        "risk": "printed detent/ratchet cycle life",
        "status": "open",
        "result": "detent torque is a single-cycle static model; creep/fatigue of the 0.45 mm "
                  "leaf over thousands of writes unmodelled (cross-cuts K2)",
        "gate": "permanently qualitative under DND-27",
    },
]

# The winner is NOT presented as print-ready while K1/K4/K5/K6 are contestable and
# K7-K11 are open. A printable-board test is only justified once K1, K5 and K7 close.
PRINT_READY_AS_STATED = False


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
            "uplift_basis": "additive +10% ship +6% tax (project-consistent)",
            "sourced_pair_over_ceiling": winner_delivered_usd() >= CEILING_USD,
            "pass": winner_reduced_delivered_usd() < CEILING_USD,
            "note": "sourced pair is AT/OVER the ceiling; only the reduced path clears, "
                    "with a small real margin (Falsifier promotion review, DND-36)",
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
