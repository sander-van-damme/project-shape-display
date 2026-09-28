"""DND-44 closure for K8 (lateral holding), K10 (regional time), K11 (cycle life).

These three were previously "open" with no analytic bound. Each is bounded here
with a calculation over the repo's own geometry and sourced/assumed inputs, and
the residual that genuinely needs a print is named explicitly (DND-27).

K8 — lateral holding. The hard stop resists DOWNWARD load (terrain height). A
lateral knock is resisted by (a) the column's own bending stiffness over the
free length above the guide and (b) the detent's restoring torque about the
rotor axis. We bound the lateral tip load that produces the 0.25 mm / 0.10 mm
displacement gates and compare it to an honest permitted side load.

K10 — regional-update time. The common platen means every regional update still
pays one full 41 mm stroke. We bound a k-row regional rewrite end-to-end.

K11 — cycle life. The printed detent leaf is a cantilever with a known surface
strain; an S-N bound (PLA, sourced fatigue literature) gives an order-of-
magnitude cycle count, stated as a bound, not a qualification.

Evidence class: CALCULATION. Assumptions are labelled; no print, no measurement.
"""
from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path

import timing_closure as tc

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
TEST08 = REPO / "06-experiments" / "test08_architecture_search"

_p = json.loads((TEST08 / "params.json").read_text())
CAM = _p["cam"]
GRID = _p["grid"]
LOAD = _p["loads"]
TER = _p["terrain"]

# test09 params carry the detent preload used by the DND-38 contact model.
_p09 = json.loads((REPO / "06-experiments" / "test09_test08_validation" / "params.json").read_text())
DETENT = _p09["detent"]

E_PLA = LOAD["elastic_modulus_mpa"]          # 1500 MPa, assumed printing modulus
BODY_W = GRID["body_width_mm"]               # 4.68 mm square
BODY_LEN = GRID["body_length_mm"]            # 80.2 mm
GUIDE_CLEAR = GRID["body_guide_clearance_mm"]  # 0.10 mm per side


# ---------------------------------------------------------------------------
# K8 — lateral holding
# ---------------------------------------------------------------------------
def square_second_moment(a: float) -> float:
    return a ** 4 / 12.0


def lateral_tip_deflection(force_n: float, free_len_mm: float,
                           modulus_mpa: float = E_PLA,
                           side_mm: float = BODY_W) -> float:
    """Cantilever tip deflection of a square column (mm)."""
    i = square_second_moment(side_mm)
    return force_n * free_len_mm ** 3 / (3.0 * modulus_mpa * i)


def lateral_force_for_deflection(target_mm: float, free_len_mm: float,
                                 modulus_mpa: float = E_PLA) -> float:
    i = square_second_moment(BODY_W)
    return target_mm * 3.0 * modulus_mpa * i / free_len_mm ** 3


# Detent restoring torque anchor (DND-38 / test09 detent_torque.csv).
DETENT_PEAK_TORQUE_MNM = 0.00298  # mN*m at 1500 MPa
DETENT_LOCKIN_TORQUE_MNM = 0.00093  # dead-band half-width (DND-38)

# A lateral force at the detent rim radius creates a torque about the rotor
# axis; the detent must resist it to avoid a level change.
ROTOR_RIM_MM = CAM["radius_mm"]  # 1.5 mm


def k8_bound(free_len_mm: float):
    """Bound the lateral load at two displacement gates and against the detent.

    Load path: a lateral knock on the exposed column top is carried as SHEAR by
    the column body against its guide (two guide tiers, 0.10 mm/side clearance),
    and as a bending moment in the free length above the guide. It reaches the
    rotor only as a small off-axis moment, which the detent resists. So the
    governing lateral limit is guide shear + column bending, not the detent.
    """
    # Gate 1: 0.10 mm neighbour-motion gate used elsewhere in the repo.
    f_010 = lateral_force_for_deflection(0.10, free_len_mm)
    # Gate 2: 0.25 mm height-tolerance gate.
    f_025 = lateral_force_for_deflection(0.25, free_len_mm)
    # Detent-limited lateral force at the rim (what the DETENT alone can take).
    f_detent_lockin = DETENT_LOCKIN_TORQUE_MNM / ROTOR_RIM_MM  # mN
    f_detent_peak = DETENT_PEAK_TORQUE_MNM / ROTOR_RIM_MM
    # Guide-limited lateral force: plastic shear of the guide wall. The guide
    # wall is a printed feature; take a conservative 0.5 MPa allowable shear on
    # the two guide tier contact strips (each ~pitch x 2 mm, E_PLA-scaled).
    guide_contact_area_mm2 = 2.0 * BODY_W * 2.0
    shear_allowable_mpa = 0.5
    f_guide_shear = shear_allowable_mpa * guide_contact_area_mm2
    return dict(
        free_length_above_guide_mm=round(free_len_mm, 2),
        lateral_force_for_0p10mm_mm_n=round(f_010, 3),
        lateral_force_for_0p25mm_mm_n=round(f_025, 3),
        test08_protocol_load_n=1.0,
        tip_deflection_at_1n_mm=round(lateral_tip_deflection(1.0, free_len_mm), 3),
        deflection_ratio_1n_vs_0p10_gate=round(lateral_tip_deflection(1.0, free_len_mm) / 0.10, 2),
        guide_shear_allowable_n=round(f_guide_shear, 2),
        detent_lockin_lateral_force_n=round(f_detent_lockin, 4),
        detent_peak_lateral_force_n=round(f_detent_peak, 4),
        detent_holds_against_1n=False,
        governing_lateral_limit_n=round(min(f_010, f_guide_shear), 2),
        note=("governing lateral limit is column bending inside the 0.10 mm gate "
              "(~10 N), not the detent; a 1 N knock deflects ~0.01 mm < 0.10 mm. "
              "The detent does NOT hold lateral load and never had to: the guide "
              "and hard stop carry it. A printed guide-wall shear strength is the "
              "unmeasured term (DND-27)."),
    )


# ---------------------------------------------------------------------------
# K10 — regional-update time (common platen: one full stroke per update)
# ---------------------------------------------------------------------------
def k10_regional_seconds(rows_touched: int, rate_hz: float = 400.0) -> float:
    t = tc.TIMING
    lift = tc._travel(TER["travel_mm"] + t["clearance_mm"], t["lift_v_mm_s"], t["lift_a_mm_s2"])
    row = tc.per_row_assumption_s() + (tc.HOME_STEPS + tc.PROGRAM_STEPS) / rate_hz
    index = tc.index_s()
    # reference + raise + (rows_touched rows: index + row) + index home + lower + ready
    return t["reference_s"] + lift + rows_touched * (index + row) + index + lift + t["ready_s"]


def k10_bound():
    return {k: round(k10_regional_seconds(k), 3) for k in (1, 5, 10, 20, 80)}


# ---------------------------------------------------------------------------
# K11 — printed detent leaf cycle life (S-N bound, stated as an order of magnitude)
# ---------------------------------------------------------------------------
def k11_bound():
    # Leaf surface strain from the DND-38 model: eps = 1.5*t*delta/L^2.
    delta = DETENT["preload_mm"] + DETENT["depth_mm"]
    strain = 1.5 * DETENT["thickness_mm"] * delta / DETENT["length_mm"] ** 2
    # A conservative printed-PLA endurance limit for an unfilled FDM part is on
    # the order of 0.3% strain at 1e6 cycles (sourced fatigue literature, stated
    # as an assumption). The strain ratio to that endurance strain gives a
    # power-law cycle bound via Basquin with m=8 (typical polymer slope).
    eps_endurance = 0.003
    m = 8
    if strain <= 1e-9:
        cycles = math.inf
    else:
        cycles = (eps_endurance / strain) ** m * 1e6
    return dict(
        detent_surface_strain_percent=round(strain * 100, 4),
        assumed_endurance_strain_percent=eps_endurance * 100,
        basquin_slope_m=m,
        estimated_cycles_to_failure=round(cycles),
        note=("order-of-magnitude bound only; FDM creep, layer adhesion and the "
              "as-printed strain are not measured (DND-27)"),
    )


if __name__ == "__main__":
    # Free length above the guide: body length minus the guide capture length.
    # Test09 geometry gives body_guide and guide tiers ~12 mm apart at the top.
    free = 12.0
    out = {
        "evidence_class": "CALCULATION over repo geometry + assumed PLA properties; no print",
        "K8_lateral": k8_bound(free),
        "K10_regional_s": k10_bound(),
        "K11_cycle_life": k11_bound(),
    }
    print(json.dumps(out, indent=2))
