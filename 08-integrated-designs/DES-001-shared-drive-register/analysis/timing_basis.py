"""timing basis; CAD/calculation source, no physical validation."""
import math
ROWS=80
PITCH_MM=5.08
TRAVEL_MM=40
PROGRAM_STEPS=16
HOME_STEPS=22
TIMING={'rate_hz': 400, 'home_steps': 22, 'step_deg': 18, 'engage_s': 0.025, 'disengage_s': 0.025, 'home_settle_s': 0.015, 'write_settle_s': 0.015, 'seat_s': 0.015, 'command_s': 0.002, 'scan_v_mm_s': 250, 'scan_a_mm_s2': 4000, 'lift_v_mm_s': 35, 'lift_a_mm_s2': 200, 'clearance_mm': 1, 'reference_s': 0.5, 'ready_s': 0.4, 'inspection_s': 0, 'recovery_s': 0}

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
    """Closed-form full-map time. Cross-checked against the assumed motion model."""
    row = per_row_assumption_s(timing) + (HOME_STEPS + PROGRAM_STEPS) / rate_hz
    return (
        fixed_s(timing)
        + (ROWS - 1) * index_s(timing)
        + ROWS * row
        + inspection_s
    )


