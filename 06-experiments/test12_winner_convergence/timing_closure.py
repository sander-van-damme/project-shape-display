"""DND-44 K6 timing closure — analytic per-row budget and required loaded rate.

Question (DND-44 §2). The S5 timing sweep (`test09/results/timing_sweep.csv`)
passes < 30 s in only 17/108 cases at 400 pps, with a 45.07 s worst corner. Is
the 30 s cap reachable, and what exactly bounds the passing region?

Method. `schedule()` in `test09/analyze.py` is a deterministic sum of per-row
durations. This module re-derives that sum in closed form, splits it into
**rate-independent** (assumption-bound) and **step-rate-dependent** terms, and
solves for the required loaded step rate. It cross-checks the closed form against
`test09/analyze.py` to the microsecond so the two cannot drift.

Evidence class: CALCULATION over stated assumptions. No print, no measurement
([DND-27](/DND/issues/DND-27)). Every timing input here is an *assumed* value
(the repo has never measured a loaded micro-stepper rate); the module therefore
reports the passing condition as a function of the rate, not a qualified claim.
"""
from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
TEST09 = REPO / "06-experiments" / "test09_test08_validation"

# ---------------------------------------------------------------------------
# The design point, read from the repo's own params.json so it cannot drift.
# ---------------------------------------------------------------------------
_p = json.loads((TEST09 / "params.json").read_text())
GRID = _p["grid"]
TIMING = _p["timing"]
ROWS = GRID["rows"]
COLS = GRID["columns"]
LEVELS = GRID["levels"]
PITCH_MM = GRID["pitch_mm"]
TRAVEL_MM = GRID["travel_mm"]
STEP_DEG = TIMING["step_deg"]

# Program cost at the worst map: the highest level needs (LEVELS-1) full steps.
PROGRAM_STEPS = (LEVELS - 1) * 360.0 / LEVELS / STEP_DEG  # = 16 full steps
HOME_STEPS = TIMING["home_steps"]                          # = 22


def _travel(d: float, v: float, a: float) -> float:
    """Trapezoidal move time for distance d at cruise v, accel a (mm, mm/s, mm/s^2)."""
    peak = min(v, math.sqrt(d * a))
    return 2 * peak / a + (d - peak * peak / a) / v


def per_row_assumption_s(timing: dict = TIMING) -> float:
    """The rate-independent per-row dwells: command + engage + 2 settles + disengage + seat."""
    return (
        timing["command_s"]
        + timing["engage_s"]
        + timing["home_settle_s"]
        + timing["write_settle_s"]
        + timing["disengage_s"]
        + timing["seat_s"]
    )


def fixed_s(timing: dict = TIMING) -> float:
    """One-off costs: reference, raise, park, lower, ready (all rate-independent)."""
    lift = _travel(TRAVEL_MM + timing["clearance_mm"], timing["lift_v_mm_s"], timing["lift_a_mm_s2"])
    park = _travel((ROWS - 1) * PITCH_MM, timing["scan_v_mm_s"], timing["scan_a_mm_s2"])
    return timing["reference_s"] + lift + park + lift + timing["ready_s"]


def index_s(timing: dict = TIMING) -> float:
    return _travel(PITCH_MM, timing["scan_v_mm_s"], timing["scan_a_mm_s2"])


def full_map_s(rate_hz: float, timing: dict = TIMING, inspection_s: float = 0.0) -> float:
    """Closed-form full-map time. Cross-checked against test09/analyze.schedule()."""
    row = per_row_assumption_s(timing) + (HOME_STEPS + PROGRAM_STEPS) / rate_hz
    return (
        fixed_s(timing)
        + (ROWS - 1) * index_s(timing)
        + ROWS * row
        + inspection_s
    )


def rate_independent_floor_s(timing: dict = TIMING) -> float:
    """Time as rate -> inf. This is the hard floor no motor can beat."""
    return fixed_s(timing) + (ROWS - 1) * index_s(timing) + ROWS * per_row_assumption_s(timing)


def required_rate_pps(target_s: float, timing: dict = TIMING, inspection_s: float = 0.0) -> float:
    """Loaded step rate needed to finish in <= target_s. inf if the floor exceeds target."""
    floor = rate_independent_floor_s(timing) + inspection_s
    if floor >= target_s:
        return math.inf
    step_seconds = (ROWS * (HOME_STEPS + PROGRAM_STEPS))
    return step_seconds / (target_s - floor)


# ---------------------------------------------------------------------------
# Loaded-rate scenarios: the engagement/seat dwells are *assumed*, so the honest
# question is "for which assumption sets does a plausible rate clear 30 s?"
# Central = the design point. Pessimistic = the sweep's slowest engagement.
# ---------------------------------------------------------------------------
SCENARIOS = {
    # name                       (engage/disengage, settle, scan_accel, inspection)
    "design_point":              (0.025, 0.015, 4000, 0.0),
    "sweep_grid_best_mid":       (0.015, 0.015, 4000, 0.0),
    "pessimistic_engagement":    (0.050, 0.040, 4000, 0.0),
    "slow_scan":                 (0.025, 0.015, 1000, 0.0),
    "worst_corner":              (0.050, 0.040, 1000, 3.0),
}


def scenario_timing(engage: float, settle: float, accel: float) -> dict:
    t = dict(TIMING)
    t.update(engage_s=engage, disengage_s=engage, home_settle_s=settle,
             write_settle_s=settle, seat_s=settle, scan_a_mm_s2=accel)
    return t


def sweep():
    rows = []
    for name, (engage, settle, accel, inspect) in SCENARIOS.items():
        t = scenario_timing(engage, settle, accel)
        floor = rate_independent_floor_s(t)
        rows.append(dict(
            scenario=name,
            engage_disengage_s=engage,
            settle_s=settle,
            scan_accel_mm_s2=accel,
            inspection_s=inspect,
            rate_independent_floor_s=round(floor, 3),
            time_at_400pps_s=round(full_map_s(400, t, inspect), 3),
            time_at_800pps_s=round(full_map_s(800, t, inspect), 3),
            required_rate_30s_pps=round(required_rate_pps(30.0, t, inspect), 1),
            required_rate_27s_pps=round(required_rate_pps(27.0, t, inspect), 1),
        ))
    return rows


def cross_check() -> dict:
    """Prove the closed form equals the repo's own schedule() to 1e-9 s."""
    spec = importlib.util.spec_from_file_location("test09_analyze", TEST09 / "analyze.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    p = json.loads((TEST09 / "params.json").read_text())
    target = mod.maps(p)["high"]
    reference = mod.schedule(p, target)["time_s"]
    closed = full_map_s(TIMING["rate_hz"], TIMING, TIMING["inspection_s"])
    return dict(reference_s=reference, closed_form_s=closed, abs_error_s=abs(reference - closed))


if __name__ == "__main__":
    cc = cross_check()
    out = {
        "evidence_class": "CALCULATION over assumed timing inputs; no measured loaded rate",
        "cross_check_vs_test09_schedule": cc,
        "rate_independent_floor_s": round(rate_independent_floor_s(), 3),
        "design_point": {
            "rate_pps": TIMING["rate_hz"],
            "full_map_s": round(full_map_s(TIMING["rate_hz"]), 3),
            "margin_to_30s_s": round(30.0 - full_map_s(TIMING["rate_hz"]), 3),
            "required_rate_30s_pps": round(required_rate_pps(30.0), 1),
            "required_rate_27s_pps": round(required_rate_pps(27.0), 1),
        },
        "scenarios": sweep(),
    }
    print(json.dumps(out, indent=2))
