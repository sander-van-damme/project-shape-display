"""DND-43 / convergence Step 6: load, structure and power.

Executable analytic model for the shared-lift structure of the S5 winner (and a
screening bound for the S3/S4 family), covering the four Step-6 questions the
convergence plan names:

    1. spliced full-span beam model + dummy platen at modelled column mass;
    2. lift torque-speed margin;
    3. flatness;
    4. power-cut behaviour (hold / descent).

Evidence class: CALCULATION / SIMULATION over sourced material properties and
stated assumptions. NOTHING here is a print or a physical measurement
([DND-27](/DND/issues/DND-27)). Every quantitative output is labelled with its
class and the residual unknowns are listed, not hidden.

Why a *spliced* beam (the point of this Step): the 406.4 mm field exceeds the
256 mm X1C build volume, so the frame and platen are printed as cartridges and
bolted at splices. A bolted splice is a stiffness discontinuity, so the plain
``5 w L^4 / 384 E I`` full-span result in Test09 (1.71 mm at E = 700 MPa) is an
optimistic upper bound that ignores the joint. This module models the splice
explicitly and reports the *support spacing* the 0.25 mm flatness budget
actually allows.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Sourced / inherited constants (all traced to repo artefacts or stated).
# ---------------------------------------------------------------------------
ROWS = 80
COLS = 80
CELLS = ROWS * COLS                 # 6400 cells
PITCH_MM = 5.08
SPAN_MM = (COLS - 1) * PITCH_MM     # 401.32 mm centre-to-centre field width
TRAVEL_MM = 40.0
UNLOAD_CLEARANCE_MM = 1.0
LIFT_STROKE_MM = TRAVEL_MM + UNLOAD_CLEARANCE_MM   # 41 mm
G = 9.81                            # m/s^2

# Column mass from Test08 geometry: 4.68 mm square x 80.2 mm, PLA 1.24 g/cm^3.
COLUMN_BODY_MM = 4.68
COLUMN_LENGTH_MM = 80.2
PLA_DENSITY_G_CM3 = 1.24

# Material (PLA) modulus: Test08/Test09 parametric range, source-typical PLA is
# 2.5-3.5 GPa but the programme deliberately screens down to a soft 700 MPa
# because printed infill is not bulk material.
PLA_MODULUS_BULK_MPA = 2500.0       # bulk-ish screening value
PLA_MODULUS_SOFT_MPA = 700.0         # pessimistic printed-infusion value
PLA_YIELD_MPA = 45.0                # typical PLA tensile yield (source-typical)

# Flatness / structural gates from Test08 README:265-312 and the S5 gate list.
FLATNESS_GATE_MM = 0.25
UNLOAD_GAP_GATE_MM = 0.50           # gap between lifted toe and any rotating part

# Support spacing options: 0.25 mm budget is achieved by supporting the field.
FULL_SPAN_MM = SPAN_MM              # 401.32 unsupported
SUPPORT_101_6_MM = 101.6            # 4 cartridges/axis
SUPPORT_203_2_MM = 203.2            # 2 cartridges/axis

# Lift drive: T8 lead-screw, 8 mm lead, 4 screws (Test09 params).
SCREW_LEAD_MM = 8.0
SCREW_COUNT = 4
SCREW_EFFICIENCY = 0.30
LIFT_V_MM_S = 35.0                  # Test09 lift_v_mm_s
LIFT_ACCEL_MM_S2 = 200.0
SCREW_BACKDRIVE_EFFICIENCY = 0.30   # self-locking analysis uses same eta

# Lift motor: sourced planetary NEMA17 allowance ($18, 24 V), representative
# holding torque 0.40 N*m (a common 42 mm planetary NEMA17 class figure; the
# *quantity* is not yet sample-verified -> stated assumption R4-adjacent).
LIFT_MOTOR_HOLD_NM = 0.40
LIFT_MOTOR_RUNNING_NM = 0.30        # at the design speed on a 24 V bus
LIFT_MOTOR_MASS_KG = 0.28


def column_mass_g() -> float:
    """One printed column's mass (solid body model, Test08 geometry)."""
    vol_mm3 = COLUMN_BODY_MM ** 2 * COLUMN_LENGTH_MM
    return vol_mm3 * PLA_DENSITY_G_CM3 / 1000.0


def field_mass_kg(platen_kg: float) -> dict:
    total_columns = CELLS * column_mass_g() / 1000.0
    return {
        "column_mass_each_g": round(column_mass_g(), 4),
        "columns_total_kg": round(total_columns, 3),
        "platen_kg": platen_kg,
        "moving_mass_kg": round(total_columns + platen_kg, 3),
    }


# ---------------------------------------------------------------------------
# 1. Spliced full-span beam model.
# ---------------------------------------------------------------------------
@dataclass
class BeamSection:
    width_mm: float = 20.0          # outer square section (Test09 coupon)
    height_mm: float = 30.0
    wall_mm: float = 2.0


def second_moment_mm4(s: BeamSection) -> float:
    """Hollow square-tube second moment (Test09 structure formula)."""
    w, h, t = s.width_mm, s.height_mm, s.wall_mm
    return (w * h ** 3 - (w - 2 * t) * (h - 2 * t) ** 3) / 12.0


def spliced_beam_defl_mm(
    *,
    span_mm: float,
    total_force_n: float,
    beams: int,
    E_mpa: float,
    section: BeamSection = BeamSection(),
    joint_stiffness_ratio: float = 0.25,
) -> dict:
    """Midspan deflection of a *spliced* beam, with the joint at midspan.

    Model: the field is carried by ``beams`` parallel rails, each a series of
    spans with bolted splices. The worst case for a splice is one placed at the
    point of maximum curvature (midspan). We model the splice as a short segment
    of length l_j at midspan whose EI is reduced by ``joint_stiffness_ratio``,
    and add the extra curvature it contributes to the midspan deflection by
    moment-area (area-moment of a curvature bump at midspan across a pinned
    span).

      * ``uniform``: distributed load w on a simply-supported span,
                     5 w L^4 / 384 E I.
      * ``spliced``: uniform + the midspan curvature-bump area-moment term.

    The joint ratio 0.25 is a stated assumption for a single bolted PLA lap
    splice (2 bolts, friction + bolt shear): it is *not* measured, and it is the
    dominant unknown of this Step. A printed/lapped splice with a spigot should
    beat 0.25; a bare butt joint would be far worse.
    """
    I = second_moment_mm4(section)
    force_per_beam = total_force_n / beams
    w = force_per_beam / span_mm                      # N/mm, distributed
    uniform = 5.0 * w * span_mm ** 4 / (384.0 * E_mpa * I)

    l_j = 2.0 * section.height_mm                     # weakened plug length
    EI = E_mpa * I
    M_mid = w * span_mm ** 2 / 8.0                    # N*mm
    extra_curv = M_mid * (1.0 / (joint_stiffness_ratio * EI) - 1.0 / EI)
    # Deflection contribution of a curvature bump of width l_j at midspan
    # across a pinned span L (area-moment): delta = (l_j/8) * kappa * L.
    spliced = uniform + (l_j / 8.0) * extra_curv * span_mm

    sigma_mid = M_mid * (section.height_mm / 2.0) / I

    return {
        "beams": beams,
        "I_each_mm4": round(I, 2),
        "force_per_beam_n": round(force_per_beam, 3),
        "midspan_bending_stress_mpa": round(sigma_mid, 4),
        "uniform_defl_mm": round(uniform, 4),
        "spliced_defl_mm": round(spliced, 4),
        "joint_stiffness_ratio": joint_stiffness_ratio,
        "E_mpa": E_mpa,
        "span_mm": span_mm,
    }


def required_support_spacing_mm(
    *,
    total_force_n: float,
    beams: int,
    E_mpa: float,
    section: BeamSection = BeamSection(),
    joint_stiffness_ratio: float = 0.25,
    flatness_gate_mm: float = FLATNESS_GATE_MM,
) -> dict:
    """Largest *spliced* span that still meets the flatness gate.

    Solve ``spliced_defl(span) <= gate`` by bisection. Returns the spacing and
    the equivalent full-span result for contrast.
    """
    lo, hi = 20.0, FULL_SPAN_MM

    def defl(L):
        return spliced_beam_defl_mm(
            span_mm=L, total_force_n=total_force_n, beams=beams,
            E_mpa=E_mpa, section=section,
            joint_stiffness_ratio=joint_stiffness_ratio,
        )["spliced_defl_mm"]

    if defl(hi) <= flatness_gate_mm:
        best = hi
    else:
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            if defl(mid) <= flatness_gate_mm:
                lo = mid
            else:
                hi = mid
        best = lo
    return {
        "max_spliced_span_mm": round(best, 1),
        "defl_at_best_mm": round(defl(best), 4),
        "flatness_gate_mm": flatness_gate_mm,
        "full_span_spliced_defl_mm": round(defl(FULL_SPAN_MM), 4),
    }


# ---------------------------------------------------------------------------
# 2. Lift torque-speed margin.
# ---------------------------------------------------------------------------
def lift_force_n(platen_kg: float, drag_n_per_cell: float,
                 guide_drag_n: float = 0.005) -> dict:
    """Total lift force: weight (with accel) + guide drag on every column."""
    fm = field_mass_kg(platen_kg)
    mass = fm["moving_mass_kg"]
    drag = CELLS * (drag_n_per_cell + guide_drag_n)
    weight = mass * (G + LIFT_ACCEL_MM_S2 / 1000.0)
    return {
        **fm,
        "drag_n": round(drag, 3),
        "total_lift_force_n": round(weight + drag, 3),
        "per_screw_force_n": round((weight + drag) / SCREW_COUNT, 3),
    }


def lift_torque_margin(platen_kg: float, drag_n_per_cell: float) -> dict:
    """Torque required at the screws vs the sourced lift-motor allowance.

    T_screw_total = F * lead / (2*pi*eta). With 4 screws the motor torque is
    divided across them; the worst-case single-screw-bears-all bound is reported
    too (2x the balanced per-screw figure). Compares against a representative
    planetary NEMA17 figure.
    """
    f = lift_force_n(platen_kg, drag_n_per_cell)
    total_torque = f["total_lift_force_n"] * (SCREW_LEAD_MM / 1000.0) / (
        2.0 * math.pi * SCREW_EFFICIENCY
    )
    worst_screw = total_torque / SCREW_COUNT * 2.0
    rpm = LIFT_V_MM_S / SCREW_LEAD_MM * 60.0
    run_margin = LIFT_MOTOR_RUNNING_NM / worst_screw
    hold_margin = LIFT_MOTOR_HOLD_NM / worst_screw
    return {
        "total_lift_force_n": f["total_lift_force_n"],
        "screw_total_torque_nm": round(total_torque, 5),
        "worst_screw_torque_nm": round(worst_screw, 5),
        "motor_torque_running_nm": LIFT_MOTOR_RUNNING_NM,
        "motor_torque_hold_nm": LIFT_MOTOR_HOLD_NM,
        "screw_rpm_at_35mms": round(rpm, 1),
        "running_torque_margin": round(run_margin, 2),
        "hold_torque_margin": round(hold_margin, 2),
        "passes_running": run_margin >= 1.5,
        "passes_hold": hold_margin >= 1.5,
    }


# ---------------------------------------------------------------------------
# 3. Flatness under a distributed terrain load (loaded tiles, not only the
#    lifted mass). A miniature load is reaction-forced into the hard stops, so
#    the frame sees a local top-grid patch, not a whole-platen load.
# ---------------------------------------------------------------------------
def terrain_load_bending(load_n_per_cell: float, loaded_fraction: float,
                         section: BeamSection = BeamSection()) -> dict:
    """Top-grid bending under a representative loaded patch."""
    t = int(loaded_fraction * CELLS)
    patch_n = t * load_n_per_cell
    patch_width = 20 * PITCH_MM
    I = second_moment_mm4(section)
    M = patch_n * patch_width / 8.0
    sigma = M * (section.height_mm / 2.0) / I
    return {
        "loaded_cells": t,
        "patch_load_n": round(patch_n, 2),
        "rib_bending_stress_mpa": round(sigma, 3),
        "yield_mpa": PLA_YIELD_MPA,
        "stress_ratio": round(sigma / PLA_YIELD_MPA, 4),
        "passes": sigma < PLA_YIELD_MPA,
    }


# ---------------------------------------------------------------------------
# 4. Power-cut behaviour.
# ---------------------------------------------------------------------------
def power_cut_behaviour(platen_kg: float,
                        drag_n_per_cell: float = 0.01) -> dict:
    """What happens when power is cut at the top of a stroke.

    Failure questions:
      (a) does gravity back-drive the lead screws (uncontrolled drop)?
      (b) if it does, does the 1 mm unload clearance absorb the fall before the
          column toes land, or do the rotors crash?
      (c) is the resting state safe without holding current?

    Lead-screw self-locking test: a screw back-drives under an axial load F when
    the friction angle is below the lead angle, i.e. tan(lambda) > mu. For a T8
    screw, lambda = atan(lead / (pi * d_nominal)). With d = 8 mm and lead 8 mm,
    lambda = 17.7 deg -- far above any plausible mu (tan 17.7 = 0.319), so this
    screw is NOT self-locking: the raised platen will back-drive down on a power
    cut under gravity unless a friction brake or detent holds it.
    """
    f = lift_force_n(platen_kg, drag_n_per_cell)
    mass = f["moving_mass_kg"]
    lead_angle_deg = math.degrees(math.atan(SCREW_LEAD_MM / (math.pi * 8.0)))
    mu_self_lock = math.tan(math.radians(lead_angle_deg))
    # Back-drive condition: tan(lambda) > mu. Use a printed PLA on steel screw
    # nominal mu = 0.15 (sourced range 0.1-0.3).
    mu_contact = 0.15
    self_locking = mu_self_lock <= mu_contact
    # If it back-drives, the descent acceleration is bounded by gravity and the
    # screw's reflected inertia; time to fall the 1 mm unload clearance from
    # rest is t = sqrt(2s/a) with a ~ g (screw threads limit but assume worst).
    fall_s = math.sqrt(2.0 * (UNLOAD_CLEARANCE_MM / 1000.0) / G)
    impact_v_m_s = G * fall_s
    return {
        "moving_mass_kg": mass,
        "lead_angle_deg": round(lead_angle_deg, 2),
        "self_lock_threshold_mu": round(mu_self_lock, 4),
        "contact_mu_assumed": mu_contact,
        "screw_self_locking": self_locking,
        "fall_time_over_clearance_s": round(fall_s, 4),
        "impact_speed_m_s": round(impact_v_m_s, 3),
        "requires_brake_or_detent": not self_locking,
        "resting_hold_current_needed": not self_locking,
    }


# ---------------------------------------------------------------------------
# 5. Dummy platen / cartridge splice block (print readiness + mass budget).
# ---------------------------------------------------------------------------
def dummy_platen_blocks(platen_kg: float, cartridge_mm: float = 203.2) -> dict:
    """Count printed cartridges and splices for the supported platen/frame.

    Field width 401.32 mm (80 cells); each cartridge <= 256 mm X1C diagonal and
    the support spacing chosen is 203.2 mm, so 2 cartridges/axis -> a 2x2 frame
    of cartridges and one bolted splice line per axis.
    """
    cartridges_axis = max(1, int(math.ceil(SPAN_MM / cartridge_mm)))
    splices_axis = cartridges_axis - 1
    return {
        "cartridge_mm": cartridge_mm,
        "cartridges_axis": cartridges_axis,
        "cartridges_total": cartridges_axis ** 2,
        "splices_per_axis": splices_axis,
        "splice_lines_total": 2 * splices_axis + cartridges_axis ** 2 - 1,
        "platen_kg_model": platen_kg,
    }


# ---------------------------------------------------------------------------
# 6. Full Step-6 disposition for the shared-lift candidates.
# ---------------------------------------------------------------------------
CANDIDATES = ("S3", "S4", "S5")

# S3/S4 use a shared lift exactly as S5 does (Test11 shared-drive model): the
# lift/structure question is a *family* question, so Step 6 screens all three.
# S3 additionally carries a moving head mass on the rails; S4 carries tile lifts
# on a shared bus. Both add moving mass / structural load beyond the S5 platen.
S3_HEAD_MASS_KG = 1.2               # 320-400 channel head + 2 rows of selectors
S4_TILE_MASS_KG = 0.25              # one actuated tile module (local decoder+mem)


def step6_disposition(platen_kg: float = 4.0,
                      drag_n_per_cell: float = 0.01) -> dict:
    f = lift_force_n(platen_kg, drag_n_per_cell)
    torque = lift_torque_margin(platen_kg, drag_n_per_cell)
    splice = dummy_platen_blocks(platen_kg)

    # Unsupported full-span (no cartridge splice): the test09 optimistic number.
    full_soft = spliced_beam_defl_mm(
        span_mm=FULL_SPAN_MM, total_force_n=f["total_lift_force_n"],
        beams=8, E_mpa=PLA_MODULUS_SOFT_MPA, joint_stiffness_ratio=1.0,
    )["spliced_defl_mm"]

    # Spliced at 203.2 mm and 101.6 mm, soft and bulk modulus.
    supported = {}
    for label, span in (("203.2", SUPPORT_203_2_MM), ("101.6", SUPPORT_101_6_MM)):
        supported[label] = {
            "soft_E700": spliced_beam_defl_mm(
                span_mm=span, total_force_n=f["total_lift_force_n"],
                beams=8, E_mpa=PLA_MODULUS_SOFT_MPA),
            "bulk_E2500": spliced_beam_defl_mm(
                span_mm=span, total_force_n=f["total_lift_force_n"],
                beams=8, E_mpa=PLA_MODULUS_BULK_MPA),
        }

    spacing = required_support_spacing_mm(
        total_force_n=f["total_lift_force_n"], beams=8,
        E_mpa=PLA_MODULUS_SOFT_MPA,
    )

    return {
        "platen_kg": platen_kg,
        "drag_n_per_cell": drag_n_per_cell,
        "lift_force": f,
        "lift_torque": torque,
        "unsupported_full_span_defl_mm": full_soft,
        "supported": supported,
        "required_support_spacing": spacing,
        "power_cut": power_cut_behaviour(platen_kg, drag_n_per_cell),
        "platen_blocks": splice,
        "terrain_1N_20pct": terrain_load_bending(1.0, 0.20),
    }


def main() -> None:
    print("Step 6 - load, structure and power (S3/S4/S5 shared lift)")
    print("=" * 68)
    d = step6_disposition()
    f = d["lift_force"]
    print(f"column mass each      : {f['column_mass_each_g']:.3f} g")
    print(f"columns total mass    : {f['columns_total_kg']:.3f} kg")
    print(f"moving mass +platen   : {f['moving_mass_kg']:.3f} kg")
    print(f"total lift force      : {f['total_lift_force_n']:.2f} N")
    print("-" * 68)
    t = d["lift_torque"]
    print(f"screw total torque    : {t['screw_total_torque_nm']:.4f} N*m")
    print(f"worst screw torque    : {t['worst_screw_torque_nm']:.4f} N*m")
    print(f"running torque margin : {t['running_torque_margin']:.2f} x "
          f"({'PASS' if t['passes_running'] else 'FAIL'})")
    print(f"hold torque margin    : {t['hold_torque_margin']:.2f} x "
          f"({'PASS' if t['passes_hold'] else 'FAIL'})")
    print("-" * 68)
    print(f"UNSUPPORTED full span : {d['unsupported_full_span_defl_mm']:.3f} mm "
          f"(gate {FLATNESS_GATE_MM} mm)")
    for label, s in d["supported"].items():
        print(f"supported {label}mm     : "
              f"E700 {s['soft_E700']['spliced_defl_mm']:.3f} mm / "
              f"E2500 {s['bulk_E2500']['spliced_defl_mm']:.3f} mm")
    sp = d["required_support_spacing"]
    print(f"max spliced span      : {sp['max_spliced_span_mm']:.1f} mm "
          f"@ {sp['defl_at_best_mm']:.3f} mm")
    print("-" * 68)
    pc = d["power_cut"]
    print(f"screw self-locking    : {pc['screw_self_locking']} "
          f"(tan lambda {pc['self_lock_threshold_mu']:.3f} vs mu {pc['contact_mu_assumed']})")
    print(f"requires brake/detent : {pc['requires_brake_or_detent']}")
    print(f"fall over 1mm clearenc: {pc['fall_time_over_clearance_s']*1000:.1f} ms "
          f"at {pc['impact_speed_m_s']:.3f} m/s")
    print("=" * 68)


if __name__ == "__main__":
    main()


def lift_lead_sweep(platen_kg: float = 4.0, drag_n_per_cell: float = 0.01,
                    leads_mm=(2.0, 4.0, 8.0)) -> list:
    """Required torque and screw rpm vs lead, for the sourced motor allowance.

    Exposes the torque-speed trade the first model hid: a lower lead buys torque
    margin at the cost of screw rpm (and reflected inertia / whine).
    """
    f = lift_force_n(platen_kg, drag_n_per_cell)
    out = []
    for lead in leads_mm:
        total = f["total_lift_force_n"] * (lead / 1000.0) / (
            2.0 * math.pi * SCREW_EFFICIENCY)
        worst = total / SCREW_COUNT * 2.0
        out.append({
            "lead_mm": lead,
            "screw_total_torque_nm": round(total, 5),
            "worst_screw_torque_nm": round(worst, 5),
            "running_margin": round(LIFT_MOTOR_RUNNING_NM / worst, 2),
            "hold_margin": round(LIFT_MOTOR_HOLD_NM / worst, 2),
            "screw_rpm_at_35mms": round(LIFT_V_MM_S / lead * 60.0, 1),
            "passes_1p5": (LIFT_MOTOR_RUNNING_NM / worst) >= 1.5,
        })
    return out
