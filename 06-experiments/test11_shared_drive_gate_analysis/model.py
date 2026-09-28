#!/usr/bin/env python3
"""System-level arithmetic for the shared-drive / multi-row family (S3, S4, S5).

This module is deliberately arithmetic-first. It does not simulate a mechanism or
claim any physical validation. Its job is to answer the ten system functions with
counts, forces, times and prices so a candidate can be *rejected* before detailed
CAD or a purchased BOM exists.

Evidence words used in the accompanying README follow the project convention:

* calculated = a closed-form equation on stated inputs;
* sourced    = a documented supplier/config claim, cited where used;
* assumed    = an input still awaiting evidence;
* measured   = requires a physical record (none exist in this folder).

Run:
    python model.py            # print the tables used in README.md
    python checks.py           # assert the rejection thresholds in README.md
"""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil, sqrt

# ---------------------------------------------------------------------------
# Global target constants (from 02-design-criteria)
# ---------------------------------------------------------------------------

N = 80                      # cells per axis
PITCH_MM = 5.08             # cell pitch
CELLS = N * N               # 6400
LEVELS = 5                  # 0/10/20/30/40 mm
TRAVEL_MM = 40.0            # usable stroke
DEADLINE_S = 30.0           # strict full-map update budget
PER_CHANNEL_IDEAL_USD = 3.0
PER_CHANNEL_ABS_USD = 6.0

COLUMN_MAX_MM = 4.6         # assumed printable square column side at 5.08 pitch


def information_bits() -> float:
    from math import log2
    return CELLS * log2(LEVELS)


def serial_transaction_floor() -> float:
    return CELLS / DEADLINE_S


# ---------------------------------------------------------------------------
# S3 - multi-row mechanical DMA head + local passive memory
# ---------------------------------------------------------------------------

@dataclass
class S3Config:
    rows_per_station: int = 4
    columns: int = N
    stations: int = 20
    step_deg: float = 18.0
    increments: int = LEVELS - 1
    step_rate_hz: float = 400.0
    station_index_s: float = 0.30
    engage_s: float = 0.05
    write_s: float = 0.12
    disengage_s: float = 0.05
    verify_s: float = 0.20
    reset_s: float = 3.0
    park_s: float = 0.6
    motors_per_row: int = 2
    cam_bank_per_station: int = 2


def s3_channels(cfg: S3Config) -> int:
    return cfg.rows_per_station * cfg.columns


def s3_full_map_time(cfg: S3Config) -> dict:
    """Serial station budget, where a station writes via global bit-planes.

    The S3 invention: a station does not perform 320 separate cell writes. A
    4-row station is split into ``increments`` (4) *global bit-planes*; each
    plane is one row-parallel write sweep of a cam bank. The head dwells once
    and the two cam banks sweep four times. Per-station dwell is therefore
    ``engage + increments * write + disengage``, not ``cells * write``.
    """
    dwell = cfg.engage_s + cfg.increments * cfg.write_s + cfg.disengage_s
    travel = cfg.stations * cfg.station_index_s
    verify = cfg.stations * cfg.verify_s
    total = cfg.reset_s + travel + cfg.stations * dwell + verify + cfg.park_s
    return {
        "per_station_dwell_s": dwell,
        "total_travel_s": travel,
        "total_write_s": cfg.stations * dwell,
        "total_verify_s": verify,
        "total_s": total,
        "margin_to_30_s": DEADLINE_S - total,
        "cells_per_write_sweep": cfg.columns,
        "write_sweeps_per_station": cfg.increments,
    }


def s3_selector_force(cfg: S3Config, *, wrap_ratio: float = 1.15,
                      preload_n: float = 0.10, mu: float = 0.30) -> dict:
    """Force budget for one cam bank.

    The bank is a 5.08 mm-pitch face cam that rocks N=80 hinged selector
    fingers. Only fingers whose notch aligns engage; the rest ride a raised
    land. The driven force is dominated by friction at the engaged teeth, not
    the (very small) state-write force. Checkerboard = half engaged.
    """
    engaged = cfg.columns / 2
    per_finger_friction = mu * preload_n
    bank_friction = engaged * per_finger_friction
    return {
        "engaged_fingers_checkerboard": engaged,
        "per_finger_friction_n": per_finger_friction,
        "bank_friction_n": bank_friction,
        "motor_force_requirement_n": bank_friction * wrap_ratio,
        "note": "state-write force not counted; cam land crush is the real unknown",
    }


def s3_bom(cfg: S3Config, *, bought_selector_usd: float = 0.0,
           motor_usd: float = 1.25, driver_usd: float = 0.60) -> dict:
    """Purchased BOM by count, not by word.

    S3 is only viable if almost nothing is bought per channel. The one place a
    cheap bought part is allowed is the drive side.
    """
    total_motors = cfg.stations * cfg.motors_per_row + 1
    bought_channels = 0
    cost = (
        total_motors * motor_usd
        + total_motors * driver_usd
        + bought_channels * bought_selector_usd
        + 10.0
        + 8.0
    )
    return {
        "head_motor_count": total_motors,
        "printable_selector_count": s3_channels(cfg),
        "bought_selector_count": bought_channels,
        "purchased_allowance_usd": cost,
        "cars_per_bought_channel": float("inf"),
    }


def s3_printable_fanout_feasibility(cfg: S3Config, *, min_feature_mm: float = 0.4) -> dict:
    """Can the mechanical fan-out be printed at final pitch?

    Each of the 4 rows in a station must own an independent selector notch on
    the same 5.08 mm band, so the land width per row is PITCH/rows. On a 0.4 mm
    nozzle the usable feature count is land/0.4.
    """
    pitch_available = PITCH_MM / cfg.rows_per_station
    return {
        "cam_land_width_mm_per_row": pitch_available,
        "features_per_cam_land_at_0p4mm": pitch_available / 0.4,
        "features_per_cam_land_at_0p2mm": pitch_available / 0.2,
        "verdict": "printable but dense" if pitch_available / 0.4 < 3 else "plausible",
    }


# ---------------------------------------------------------------------------
# S4 - distributed passive tiles on a shared power bus
# ---------------------------------------------------------------------------

@dataclass
class S4Config:
    tile_cells: int = 10
    tiles_axis: int = 8
    bit_planes: int = 4
    bus_revs_per_plane: float = 1.0
    bus_rpm: float = 600.0
    per_tile_engage_s: float = 0.15
    settle_s: float = 0.20


def s4_full_map_time(cfg: S4Config) -> dict:
    tiles = cfg.tiles_axis ** 2
    plane_s = cfg.bit_planes * cfg.bus_revs_per_plane * 60.0 / cfg.bus_rpm
    bus_warm_s = 0.5
    total = bus_warm_s + plane_s + cfg.settle_s
    return {
        "tiles": tiles,
        "bus_plane_sweep_s": plane_s,
        "full_map_s": total,
        "regional_tile_s": cfg.per_tile_engage_s + plane_s / cfg.tiles_axis,
        "margin_to_30_s": DEADLINE_S - total,
    }


def s4_clutch_reality_check(cfg: S4Config, *, bought_clutch_usd: float = 6.0) -> dict:
    tiles = cfg.tiles_axis ** 2
    bought_total = tiles * bought_clutch_usd
    return {
        "tiles": tiles,
        "bought_clutch_usd": bought_clutch_usd,
        "bought_clutch_total_usd": bought_total,
        "within_abs_ceiling": bought_total <= 500.0,
        "fits_per_channel_ideal": bought_total / tiles <= PER_CHANNEL_IDEAL_USD,
        "printable_clutch_required": bought_total > 200.0,
        "verdict": "printed clutch mandatory" if bought_total > 200.0 else "bought clutch affordable",
    }


def s4_correlated_fault(cfg: S4Config, *, bus_length_m: float = 0.406,
                        backlash_deg: float = 1.0, lead_mm: float = 10.0) -> dict:
    joints = cfg.tiles_axis + 2
    accumulated_deg = backlash_deg * sqrt(joints)
    height_error_mm = lead_mm * accumulated_deg / 360.0
    return {
        "joints_in_bus": joints,
        "accumulated_backlash_deg": accumulated_deg,
        "height_error_at_last_tile_mm": height_error_mm,
        "decoder_margin_mm": 0.25,
        "verdict": "within margin" if height_error_mm <= 0.25 else "CORRELATED MISTATEMENT RISK",
    }


# ---------------------------------------------------------------------------
# S5 - rotary stepped stops + travelling programmer, gate-by-gate
# ---------------------------------------------------------------------------

@dataclass
class S5Gate:
    name: str
    status: str
    cheapest_coupon: str
    kill_threshold: str
    passed: bool


S5_GATES = [
    S5Gate("low-cost qualified motor supply", "open",
           "buy ONE traceable 8 mm PM sample + delivered quote for 80+spares",
           "no same-winding/shaft/step-angle 80+spares quote under $1.06 each delivered", False),
    S5Gate("detent / coupling reliability", "open",
           "flat leaf/wheel bench: 10k cycles, capture +/-18 deg unpowered",
           "restoring torque <80% after 10k or capture <+/-18 deg", False),
    S5Gate("return-friction margin", "open",
           "30 interchangeable 5.08 mm cells, tilt 0/1/3 deg, drag+uncert <0.5x weight",
           "drag+uncertainty >=0.5x measured weight in >1 of 30 sets", False),
    S5Gate("structural frame", "open",
           "two 203.2 mm printed beams + splice + 406.4 mm dummy platen, 8-beam load",
           "midspan deflection+racking >0.25 mm at representative load", False),
    S5Gate("regional isolation", "open",
           "adjacent 5x5 tiles, one updates while neighbour loaded",
           "neighbour peak vertical motion >0.10 mm or miniature tips", False),
]


def s5_gate_summary() -> dict:
    return {
        "total": len(S5_GATES),
        "passed": sum(1 for g in S5_GATES if g.passed),
        "open": sum(1 for g in S5_GATES if not g.passed),
    }


def s5_cost_ceiling() -> dict:
    """Reproduce the Test08/Test09 cost boundary.

    Test08 working non-motor total is $332. To stay below $500 with 20%
    contingency, 80 motors must average at most ($500/1.2 - 332)/80.
    """
    working_non_motor = 332.0
    budget_with_contingency = 500.0
    max_motor_before_contingency = budget_with_contingency / 1.2 - working_non_motor
    return {
        "working_non_motor_allowance_usd": working_non_motor,
        "max_motor_each_usd": max(0.0, max_motor_before_contingency / 80.0),
        "test08_claimed_motor_allowance_usd": 1.25,
        "passes": max_motor_before_contingency / 80.0 >= 1.25,
    }


def main() -> None:
    print("Shape display shared-drive family - arithmetic (no mechanism simulated)")
    print(f"cells={CELLS} bits={information_bits():.1f} serial_floor={serial_transaction_floor():.2f}/s")
    print()

    cfg3 = S3Config()
    print("S3 multi-row DMA head")
    for k, v in s3_full_map_time(cfg3).items():
        print(f"  {k}: {v}")
    for k, v in s3_selector_force(cfg3).items():
        print(f"  {k}: {v}")
    for k, v in s3_bom(cfg3).items():
        print(f"  {k}: {v}")
    for k, v in s3_printable_fanout_feasibility(cfg3).items():
        print(f"  {k}: {v}")
    print()

    cfg4 = S4Config()
    print("S4 shared-bus tiles")
    for k, v in s4_full_map_time(cfg4).items():
        print(f"  {k}: {v}")
    for k, v in s4_clutch_reality_check(cfg4).items():
        print(f"  {k}: {v}")
    for k, v in s4_correlated_fault(cfg4).items():
        print(f"  {k}: {v}")
    print()

    print("S5 rotary-stop gates")
    for g in S5_GATES:
        print(f"  [{'PASS' if g.passed else 'OPEN'}] {g.name}: {g.cheapest_coupon}")
    print()

    print("S5 cost ceiling")
    for k, v in s5_cost_ceiling().items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
