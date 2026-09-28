"""DND-38 - analytic detent contact sweep for the S5 winner (closes or bounds K2).

K2 is the one quantitative residual on the S5 risk register: whether the printed
rotary detent holds height and *repeats* after a slipped motor step. The issue
asks for the analytically attackable part - the detent force window as a function
of geometry and a **sourced** PLA contact-friction range - plus a +/-0.05 mm
print-tolerance stack-up.

Physics modelled here (and only this; every assumption is named):

  Rim      r(theta) = R0 - A*(1 + cos(k*theta))          (test09 params.json)
  Leaf     F(delta) = K*delta, K = E*b*t^3/(4*L^3)       (test09 analyse.py detent())
  Contact  delta(theta) = preload + A*(1 - cos(k*theta))
  Restoring torque (energy-consistent, T = dU/dtheta):
           T_r(theta) = F(theta) * A * k * sin(k*theta)
  Friction when the tip slides on the rim:
           |T_f| = mu * F * r(theta), opposing motion.

Stable rest positions (valleys) are theta = m*(2*pi/k); the unstable crests
(where the leaf is most deflected) sit half a basin away at pi/k = 36 deg. A
rotor that slips one 18 deg motor step is pulled back toward the valley only
while |T_r| > mu*F*r. Where the restoring torque falls below the friction moment
the tip sticks and the rotor stays put - the K2 failure mode.

The model answers three concrete questions:
  1. Toggle / peak restoring torque and the leaf force at the toggle point.
  2. Whether the detent corrects a one-step (18 deg) slip: it does only while
     |T_r(18 deg)| > mu*F*r, i.e. mu < A*k/r (independent of E and preload).
  3. Holding dead-band at the seated valley versus the disturbance anchor.

Result (CALCULATION): at the sourced PLA-PLA friction midpoint mu = 0.35 the
nominal leaf does NOT correct a step (torque/friction = 0.92). It closes only for
mu <= 0.323 or a deepened scallop (>= 0.31 mm). Verdict: conditional - the
printed detent as dimensioned is not sufficient across the sourced friction
range, but the fix is a geometry/friction change, not a new architecture.
"""
from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent

# --- Sourced parameters -----------------------------------------------------
# Dry PLA-on-PLA static friction: sourced range and midpoint already used by the
# J2 analytic isolation gate in this repo (textbook 0.2-0.5):
# 06-experiments/test11_falsification_library/analytic/j2_analytic_gate.py:87-88
MU_LOW = 0.20
MU_MID = 0.35
MU_HIGH = 0.50
MU = (MU_LOW, MU_MID, MU_HIGH)

# PLA elastic modulus envelope, test09 params.json material.modulus_mpa.
E_LOW_MPA = 700.0
E_MID_MPA = 1500.0
E_HIGH_MPA = 2500.0

# Detent / rim geometry, test09 params.json detent{}.
DETENT_LENGTH_MM = 10.0
DETENT_WIDTH_MM = 1.0
DETENT_THICKNESS_MM = 0.45
DETENT_PRELOAD_MM = 0.05
DETENT_DEPTH_MM = 0.20            # peak-to-valley scallop depth = 2*A
RIM_OUTER_RADIUS_MM = 1.65        # R0
LEVELS = 5                        # k scallops per revolution
# The leaf rides between the 1.45 mm valley and the 1.65 mm crest; friction arm
# uses the mid radius. The +-0.10 mm swing is reported as a sensitivity.
RIM_MID_RADIUS_MM = (RIM_OUTER_RADIUS_MM + (RIM_OUTER_RADIUS_MM - DETENT_DEPTH_MM)) / 2.0

# Design gates (test08/09).
STEP_ANGLE_DEG = 18.0             # one motor step; the slip the detent must correct
SEATING_GATE_DEG = 6.0            # residual seating error gate (test09 README:162)
HEIGHT_GATE_MM = 0.25             # permitted level-height error (test09 README:533)
WIDTH_PER_DEG_MM = 10.0 / 18.0    # level height per rotor degree: 10 mm / 18 deg

# Existing anchors the K2 answer must reconcile against.
ANCHOR_PEAK_RESTORING_MNM = 0.00298     # E=1500 MPa ideal leaf
ANCHOR_DISTURBANCE_MNM = 0.02356        # 1 N, 1 deg plateau, r=1.35 mm
ANCHOR_LEAF_FORCE_MN = 6.8              # test08 detent_leaf_force_n
ANCHOR_LEAF_STRAIN = 0.00135            # 0.135 %

TOL_MM = 0.05                     # +/- print tolerance on each printed dimension


@dataclass(frozen=True)
class Geometry:
    length_mm: float = DETENT_LENGTH_MM
    width_mm: float = DETENT_WIDTH_MM
    thickness_mm: float = DETENT_THICKNESS_MM
    preload_mm: float = DETENT_PRELOAD_MM
    depth_mm: float = DETENT_DEPTH_MM
    rim_radius_mm: float = RIM_MID_RADIUS_MM
    levels: int = LEVELS


def stiffness_n_per_mm(e_mpa: float, g: Geometry) -> float:
    """Cantilever leaf stiffness K = E*b*t^3/(4*L^3)  [N/mm]."""
    return e_mpa * g.width_mm * g.thickness_mm ** 3 / (4.0 * g.length_mm ** 3)


def deflection_mm(theta: float, g: Geometry) -> float:
    a = g.depth_mm / 2.0
    return g.preload_mm + a * (1.0 - math.cos(g.levels * theta))


def torque_curve(e_mpa: float, mu: float, g: Geometry,
                 samples_per_deg: int = 8) -> list[dict]:
    """Restoring torque, friction moment and net driving torque over one basin."""
    k = stiffness_n_per_mm(e_mpa, g)
    a = g.depth_mm / 2.0
    half = 180.0 / g.levels
    n = int(2 * half * samples_per_deg) + 1
    rows = []
    for i in range(n):
        deg = -half + 2 * half * i / n
        th = math.radians(deg)
        delta = deflection_mm(th, g)
        force = k * delta                                   # N
        t_r = force * a * g.levels * math.sin(g.levels * th)  # N mm = mN m
        t_f = mu * force * g.rim_radius_mm                    # N mm
        net = t_r - math.copysign(t_f, t_r)
        rows.append(dict(
            angle_deg=deg,
            deflection_mm=delta,
            force_n=force,
            restoring_torque_mnm=t_r,
            friction_torque_mnm=t_f,
            net_driving_torque_mnm=net,
            surface_strain=1.5 * g.thickness_mm * delta / g.length_mm ** 2,
        ))
    return rows


def peak_restoring(e_mpa: float, g: Geometry) -> dict:
    """Peak restoring torque (the toggle point), force, deflection and strain."""
    rows = torque_curve(e_mpa, 0.0, g, samples_per_deg=64)
    best = max(rows, key=lambda r: abs(r["restoring_torque_mnm"]))
    return dict(
        peak_restoring_mnm=abs(best["restoring_torque_mnm"]),
        toggle_angle_deg=abs(best["angle_deg"]),
        toggle_force_n=best["force_n"],
        toggle_deflection_mm=best["deflection_mm"],
        toggle_surface_strain=best["surface_strain"],
    )


def capture_basin(e_mpa: float, mu: float, g: Geometry,
                  samples_per_deg: int = 720) -> dict:
    """Friction-limited capture: can the detent pull a slipped rotor home?

    The rim is periodic with k = 5 scallops/rev, so valleys (stable rest) lie
    72 deg apart, the unstable crests 36 deg from each valley, and one 18 deg
    motor step parks a slipped rotor *mid-basin* on the steep flank. The rotor's
    HEIGHT reference is the hard stop; K2 is whether the detent can (a) pull a
    rotor that slipped one motor step back to the correct valley (else it lands
    one 10 mm level wrong) and (b) hold the seated rotor against disturbance.

    Two friction effects, both from the sliding tip (normal force F):
      * the tip sticks where |T_r| < mu*F*r; inward of that angle the rotor is
        frozen (fine for holding - the hard stop is the reference);
      * on the approach to the valley the detent must overpower mu*F*r, so a
        slipped rotor is corrected only while |T_r(theta_slip)| > mu*F*r.

    T_r/T_f = A*k*|sin(k*theta)| / (mu*r), independent of E and preload, because
    both torques carry F. At the 18 deg slip sin(k*theta)=1, so correction needs
    A*k/mu/r > 1, i.e. mu < A*k/r = 0.323 for the nominal A=0.10 mm, k=5,
    r=1.55 mm.
    """
    rows = torque_curve(e_mpa, mu, g, samples_per_deg=samples_per_deg)
    half = 180.0 / g.levels
    inner = [r for r in rows if abs(r["angle_deg"]) <= half / 2.0 * 1.05]
    # Inner lock angle: scan outward from the valley; the tip is frozen while
    # restoring torque cannot beat the friction moment.
    theta_lock = 0.0
    for r in sorted(inner, key=lambda r: abs(r["angle_deg"])):
        if abs(r["restoring_torque_mnm"]) > r["friction_torque_mnm"]:
            break
        theta_lock = abs(r["angle_deg"])
    # Restoring vs friction exactly at one slipped motor step.
    th = math.radians(STEP_ANGLE_DEG)
    force = stiffness_n_per_mm(e_mpa, g) * deflection_mm(th, g)
    t_r_step = abs(force * (g.depth_mm / 2.0) * g.levels * math.sin(g.levels * th))
    t_f_step = mu * force * g.rim_radius_mm
    recovers = t_r_step > t_f_step
    # Diagnostic residual: if the detent cannot drive at the slip angle the rotor
    # stops a full step from the correct valley (one level = 10 mm). If it can,
    # the rotor advances to the inner stick boundary, which the *hard stop*
    # (the height reference) then removes; that sub-level angle is reported as a
    # diagnostic, not as the K2 height error.
    residual_deg = STEP_ANGLE_DEG if not recovers else theta_lock
    return dict(
        lock_in_deg=theta_lock,
        step_slip_restoring_mnm=t_r_step,
        step_slip_friction_mnm=t_f_step,
        step_slip_margin_mnm=t_r_step - t_f_step,
        torque_to_friction_ratio=t_r_step / t_f_step if t_f_step else math.inf,
        recovers_one_step=recovers,
        residual_deg=residual_deg,
        residual_height_error_mm=residual_deg * WIDTH_PER_DEG_MM,
        within_seating_gate=theta_lock <= SEATING_GATE_DEG,
    )


def holding_deadband(e_mpa: float, mu: float, g: Geometry) -> dict:
    """Disturbance the seated rotor absorbs before it creeps."""
    k = stiffness_n_per_mm(e_mpa, g)
    f0 = k * g.preload_mm
    t_f0 = mu * f0 * g.rim_radius_mm
    th = math.radians(SEATING_GATE_DEG)
    fr = k * deflection_mm(th, g)
    tr = abs(fr * (g.depth_mm / 2.0) * g.levels * math.sin(g.levels * th))
    tf = mu * fr * g.rim_radius_mm
    return dict(
        deadband_at_valley_mnm=t_f0,
        hold_at_seating_gate_mnm=tr + tf,
        disturb_anchor_mnm=ANCHOR_DISTURBANCE_MNM,
        holds_disturbance=t_f0 >= ANCHOR_DISTURBANCE_MNM,
    )


def sweep_geometry(g: Geometry) -> dict:
    """Peak torque, capture basin and dead-band over the E x mu envelope."""
    peak, basin, hold = {}, {}, {}
    for e in (E_LOW_MPA, E_MID_MPA, E_HIGH_MPA):
        peak[e] = peak_restoring(e, g)
        for mu in MU:
            basin[(e, mu)] = capture_basin(e, mu, g)
            hold[(e, mu)] = holding_deadband(e, mu, g)
    return dict(peak=peak, basin=basin, hold=hold)


def tolerance_corners() -> list[Geometry]:
    """+/-TOL_MM on each printed detent dimension, worst-case for retention.

    A thinner/shorter/shallower leaf is the weak direction; a thicker/longer one
    is the strong direction. Corners enumerate the extremes of E separately.
    """
    base = Geometry()
    corners = [base]
    for field, sign in (("thickness_mm", -1), ("length_mm", +1),
                        ("depth_mm", -1), ("preload_mm", -1)):
        kw = asdict(base)
        kw[field] = kw[field] + sign * TOL_MM
        corners.append(Geometry(**kw))
    # Worst combined corner: thin, long, shallow, light preload.
    worst = asdict(base)
    worst["thickness_mm"] -= TOL_MM
    worst["length_mm"] += TOL_MM
    worst["depth_mm"] -= TOL_MM
    worst["preload_mm"] -= TOL_MM
    corners.append(Geometry(**worst))
    return corners


def closure_levers(g: Geometry | None = None) -> dict:
    """The concrete changes that would make the printed detent correct a step.

    Correction needs T_r/T_f > 1 at the 18 deg slip. Because both torques carry
    the leaf force F, the ratio is A*k/(mu*r) - independent of E, preload and
    leaf thickness. So the design levers are exactly:
      * reduce contact friction to mu_max = A*k/r;
      * deepen the scallop to A_min = mu*r/k.
    Reported for the nominal geometry and for the sourced worst-case mu=0.5.
    """
    g = g or Geometry()
    a = g.depth_mm / 2.0
    mu_max = a * g.levels / g.rim_radius_mm
    depth_min_for_mu_high = 2.0 * MU_HIGH * g.rim_radius_mm / g.levels
    return dict(
        ratio_expression="A*k/(mu*r), independent of E and preload",
        mu_max_for_correction=mu_max,
        mu_low=MU_LOW, mu_mid=MU_MID, mu_high=MU_HIGH,
        closes_at_midpoint=MU_MID < mu_max,
        closes_at_high=MU_HIGH < mu_max,
        nominal_depth_mm=g.depth_mm,
        depth_min_mm_for_mu_high=depth_min_for_mu_high,
        depth_recommended_mm_for_mu_high=1.10 * depth_min_for_mu_high,
        depth_multiple_for_mu_high=depth_min_for_mu_high / g.depth_mm,
    )


def classify() -> dict:
    """Decide K2: closed, needs-spring, or inconclusive with the named term."""
    base = Geometry()
    nominal_peak = peak_restoring(E_MID_MPA, base)
    nominal_basin = capture_basin(E_MID_MPA, MU_MID, base)
    nominal_hold = holding_deadband(E_MID_MPA, MU_MID, base)
    # Sensitivity over the full E x mu envelope.
    worst_residual_deg = None
    worst_basin_key = None
    all_recover = True
    for e in (E_LOW_MPA, E_MID_MPA, E_HIGH_MPA):
        for mu in MU:
            b = capture_basin(e, mu, base)
            if not b["recovers_one_step"]:
                all_recover = False
            if worst_residual_deg is None or b["residual_deg"] > worst_residual_deg:
                worst_residual_deg = b["residual_deg"]
                worst_basin_key = (e, mu)
    # Tolerance stack-up at the weakest envelope corner. At E=700 MPa the leaf
    # force is smallest AND mu=0.5 friction is highest; both hurt correction.
    tol = tolerance_corners()
    tol_results = []
    for g in tol:
        b_e = capture_basin(E_LOW_MPA, MU_HIGH, g)
        if not b_e["recovers_one_step"]:
            all_recover = False
        tol_results.append(dict(g=asdict(g), **b_e))
    worst_tol = max(tol_results, key=lambda r: r["residual_deg"])
    worst_residual_deg = max(worst_residual_deg, worst_tol["residual_deg"])
    levers = closure_levers(base)
    # The K2 gate is the binary step-recovery, not the sub-level residual (the
    # hard stop removes that). It closes only if the detent corrects a step
    # across the *whole sourced* friction range and the tolerance stack-up.
    recovers_range = all(
        capture_basin(e, mu, base)["recovers_one_step"]
        for e in (E_LOW_MPA, E_MID_MPA, E_HIGH_MPA) for mu in MU
    )
    recovers_low_mu = capture_basin(E_MID_MPA, MU_LOW, base)["recovers_one_step"]
    if recovers_range and all(r["recovers_one_step"] for r in tol_results):
        verdict = "closed"
    elif recovers_low_mu:
        # Adequate only at the low-friction end of the sourced range; the sourced
        # midpoint does not correct a step. A design change (deeper scallop or a
        # proven low-friction contact) is required - it does not kill S5.
        verdict = "conditional"
    else:
        verdict = "needs-spring"
    return dict(
        nominal_peak=nominal_peak,
        nominal_basin=nominal_basin,
        nominal_hold=nominal_hold,
        worst_residual_deg=worst_residual_deg,
        worst_residual_height_error_mm=worst_residual_deg * WIDTH_PER_DEG_MM,
        worst_basin_key=worst_basin_key,
        worst_tolerance=worst_tol,
        all_slips_recovered=all_recover,
        recovers_across_full_sourced_range=recovers_range,
        closure_levers=levers,
        verdict=verdict,
    )


def main() -> None:
    print(json.dumps(classify(), indent=2, default=str))


if __name__ == "__main__":
    main()
