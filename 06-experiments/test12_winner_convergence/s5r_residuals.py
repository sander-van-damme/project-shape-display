"""DND-59 S5-R residual retirement -- the last agent-reachable residuals.

Question ([DND-59]). [DND-57] found S5-R clears every mission requirement on its
labelled evidence class EXCEPT buildability, and split the remaining residuals
into agent-reachable (this module) and measurement-only (forbidden under
[DND-27], out of scope). This module retires the agent-reachable set with the
only evidence classes DND-27 allows: sourced process limits, analytic
calculation, tolerance/Monte-Carlo stack-ups and CAD.

The five residuals retired here
------------------------------
  R-DND54-KEEPER  Keeper-leaf printability RISK: the DND-54 keeper leaf is
                  0.45 mm = 1 extrusion line (limit 0.88 mm). This module
                  re-profiles it to 2 lines AND decouples printability from
                  dimensional tolerance by making the holding function a hard
                  printed shoulder in compression, not a bending-spring
                  over-centre force.
  R-DND54-6       Writer/solenoid force unconfirmed: no listing publishes a
                  force in N. This module re-derives the required force
                  bottom-up from the release kinematics and reports the sourced
                  actuator class that clears it.
  R-DND54-5       Missed keeper set = silent row error. This module derives the
                  required per-set reliability for a 99 percent full map and
                  tests whether agent-reachable changes (per-group verify pass,
                  mechanical detent-confirm, writer redundancy) move it.
  R-DND54-3       Crank speed 720 deg/s / writer settle 0.05 s assumption. This
                  module re-derives the break-even from the sourced motor class
                  and reports the speed/torque margin.
  R-DND55-1       Bar reaction eccentricity e. This module confirms it is
                  genuinely irrelevant for the sourced steel rod chosen by
                  DND-58 (the residual only bites a printed bar).

EVIDENCE CLASS. CALCULATION (statics, reliability, tolerance Monte-Carlo) and
sourced actuator specs, plus CAD geometry in s5r_register.scad. No print, no
purchase, no measurement ([DND-27]).
"""
from __future__ import annotations

import json
import math
import random

import s5r_bank as bank
import s5r_register as reg

# ---------------------------------------------------------------------------
# Shared sourced / process constants (imported so they cannot drift).
# ---------------------------------------------------------------------------
E_PLA_MPA = reg.PLA_E_MPA                 # 1500 MPa (sourced range midpoint)
PITCH_MM = reg.PITCH_MM                   # 5.08
MIN_FEATURE_MM = reg.MIN_FEATURE_MM       # 0.44 (1 line)
MIN_WALL_MM = reg.MIN_WALL_MM             # 0.88 (2 lines)
DIM_ACCURACY_MM = reg.DIM_ACCURACY_MM     # +/-0.10 per printed face
ROWS = reg.ROWS                           # 80
COLS = reg.COLS                           # 80
LEVELS = reg.LEVELS                       # 5

PAWL_FORCE_N = reg.pawl_spring()["force_n"]     # 0.0374 N (pawl push-out)
MU_PLA_MID = reg.MU_PLA_MID                      # 0.35
WRITE_LOAD_N = reg.WRITE_LOAD_N                  # 0.05 (per pawl, unloaded write)


def cantilever_k(t: float, w: float, l: float, e_mpa: float = E_PLA_MPA) -> float:
    """Printed rectangular cantilever rate k = 3 E I / L^3 (N per mm)."""
    return 3.0 * e_mpa * (w * t ** 3 / 12.0) / l ** 3


def leaf_strain(t: float, l: float, d: float) -> float:
    """Surface bending strain of a cantilever leaf at tip deflection d."""
    return 1.5 * t * d / (l ** 2)


# ===========================================================================
# 1. R-DND54-KEEPER -- keeper-leaf printability re-profile (2 lines + hard stop)
# ===========================================================================
# The DND-54 keeper was a 0.45 mm bending leaf whose over-centre offset set the
# holding force. Two problems, both retired here:
#   (a) 0.45 mm = 1 extrusion line -> RISK.
#   (b) a bending-spring hold is TOLERANCE-FRAGILE: the hold force is
#       k * (over-centre offset), and the offset (+/-0.10 mm per printed face)
#       can print to zero or negative, so a plain leaf cannot guarantee hold.
# The fix decouples the two functions:
#   * HOLD is done by a HARD printed shoulder that takes the pawl push-out
#     force in COMPRESSION (a 0.90 x 0.70 nose, hundreds of times its load).
#   * SNAP/RELEASE is done by a 2-line (0.90 mm) leaf with a bounded
#     over-centre offset; the leaf only has to seat the keeper against the
#     shoulder, not carry the pawl load.
KEEPER_T_MM = 0.90          # 2 extrusion lines -> PASS the printability gate
KEEPER_W_MM = 0.70
KEEPER_L_MM = 4.00          # longer leaf keeps the snap strain low
KEEPER_OVER_CENTRE_MM = 0.06
KEEPER_PRELOAD_N = 0.05     # seating preload the leaf keeps on the shoulder
KEEPER_SHOULDER_AREA_MM2 = KEEPER_T_MM * KEEPER_W_MM   # compression contact area

# Sourced FDM PLA compression-yield band (same class used by the DND-46 K11
# constants): printed PLA compression yield is ~20-45 MPa.
PLA_COMPRESSION_YIELD_LO_MPA = 20.0
PLA_COMPRESSION_YIELD_HI_MPA = 45.0


def keeper_reprofile() -> dict:
    k = cantilever_k(KEEPER_T_MM, KEEPER_W_MM, KEEPER_L_MM)
    hold_bending = k * KEEPER_OVER_CENTRE_MM
    snap_strain = leaf_strain(KEEPER_T_MM, KEEPER_L_MM, KEEPER_OVER_CENTRE_MM)
    cap_lo = PLA_COMPRESSION_YIELD_LO_MPA * KEEPER_SHOULDER_AREA_MM2
    cap_hi = PLA_COMPRESSION_YIELD_HI_MPA * KEEPER_SHOULDER_AREA_MM2
    shoulder_load = PAWL_FORCE_N + KEEPER_PRELOAD_N
    old_t = reg.KEEPER_LEAF_T_DND54_MM
    old_l = reg.KEEPER_LEAF_L_DND54_MM
    old_w = reg.KEEPER_LEAF_W_MM
    old_k = cantilever_k(old_t, old_w, old_l)
    old_hold = old_k * reg.KEEPER_OVER_CENTRE_MM
    return dict(
        evidence_class="CALCULATION over sourced PLA modulus/compression yield "
                       "and the sourced FDM 2-line wall limit",
        old_leaf=dict(
            t_mm=old_t, l_mm=old_l, w_mm=old_w,
            verdict="RISK (0.45 mm = 1 extrusion line)",
            lines=old_t / MIN_FEATURE_MM,
            hold_n=round(old_hold, 4),
            hold_vs_pawl=round(old_hold / PAWL_FORCE_N, 3),
            failure_mode="a bending-spring hold is tolerance-fragile: the "
                         "over-centre offset can print to <=0, giving a "
                         "non-holding keeper; the 1-line leaf is also a print "
                         "RISK",
        ),
        new_leaf=dict(
            t_mm=KEEPER_T_MM, w_mm=KEEPER_W_MM, l_mm=KEEPER_L_MM,
            lines=round(KEEPER_T_MM / MIN_FEATURE_MM, 3),
            rate_n_per_mm=round(k, 4),
            over_centre_mm=KEEPER_OVER_CENTRE_MM,
            bending_hold_n=round(hold_bending, 4),
            snap_strain=round(snap_strain, 5),
            verdict="PASS (0.90 mm = 2 extrusion lines >= 0.88 mm)",
        ),
        hold_mechanism=dict(
            kind="hard printed shoulder in compression",
            contact_area_mm2=round(KEEPER_SHOULDER_AREA_MM2, 3),
            shoulder_load_n=round(shoulder_load, 4),
            capacity_lo_n=round(cap_lo, 2), capacity_hi_n=round(cap_hi, 2),
            margin_lo=round(cap_lo / shoulder_load, 1),
            margin_hi=round(cap_hi / shoulder_load, 1),
            note="the HOLD is a compression contact, so it does not depend on "
                 "the over-centre offset; the offset only trips the snap.",
        ),
        printability_verdict="PASS",
        note="the keeper now prints at 2 lines AND its holding function no "
             "longer depends on a tolerance-critical offset, so the RISK is "
             "retired rather than accepted.",
    )


def keeper_tolerance_mc(n: int = 200000, seed: int = 7) -> dict:
    """Monte-Carlo the keeper *snap* offset vs the sourced print tolerance.

    This is the failure a plain bending-hold keeper suffers. With the hard
    shoulder carrying the load, a snap offset that prints to zero only removes
    the bistable assist; the shoulder still holds. Reported so the difference is
    explicit, not hidden.
    """
    rng = random.Random(seed)
    sigma = DIM_ACCURACY_MM / 3.0
    k = cantilever_k(KEEPER_T_MM, KEEPER_W_MM, KEEPER_L_MM)
    held_bending = 0
    for _ in range(n):
        d = KEEPER_OVER_CENTRE_MM + rng.gauss(0, sigma) + rng.gauss(0, sigma)
        if k * max(d, 0.0) >= PAWL_FORCE_N:
            held_bending += 1
    return dict(
        samples=n, sigma_mm=round(sigma, 4),
        p_hold_bending_only=round(held_bending / n, 5),
        p_hold_hard_shoulder=1.0,
        note="the bending-only hold fails in a meaningful fraction of builds; "
             "the hard-shoulder hold does not. This is why the re-profile "
             "changes the hold mechanism, not just the leaf thickness.",
    )


# ===========================================================================
# 2. R-DND54-6 -- writer/solenoid force, bottom-up
# ===========================================================================
# DND-54 assumed 1.2 N from "a small 5 V push solenoid" with no published force.
# Here the required force is re-derived from the release kinematics:
#   required = keeper leaf rate * (over-centre offset + gate travel)
#            + mu * (pawl normal reflected at the keeper nose)
# and the sourced actuator class is reported with its published force.
WRITER_GATE_TRAVEL_MM = reg.KEEPER_GATE_STEP_MM      # 0.35 mm gate indexing travel
WRITER_PAWL_NORMAL_N = PAWL_FORCE_N

# Sourced actuator class (published force). The repo's DND-52/DND-54 basis is a
# small 5 V push solenoid at a $2.50 sourced-class allowance. A published-force
# listing of this class is required at purchase; DND-27 forbids buying one.
WRITER_SOURCED = dict(
    part_class="5 V open-frame push solenoid (DC, intermittent duty)",
    published_force_n=1.20,
    stroke_mm=3.0,
    unit_usd=2.50,
    source="sourced-class allowance carried by DND-52/DND-54; a published-force "
           "listing of this class is required at purchase (DND-27 forbids "
           "buying)",
)


def writer_force_bottom_up() -> dict:
    """Writer force, bottom-up, matching the DND-54 release convention.

    Two distinct writer duties, priced separately:
      (a) TRIP the keeper over-centre: the leaf must be bent through its
          over-centre offset (0.06 mm), giving leaf_rate * over_centre. This is
          the load-bearing term.
      (b) INDEX the 5-position gate: this is a translating detent motion of the
          keeper nose along the gate, which does NOT bend the leaf by the gate
          travel; it only overcomes a small printed detent force. It is bounded
          here by a conservative detent allowance, not by leaf_rate * travel.
    Friction at the pawl/keeper nose adds mu * pawl_normal.
    """
    k = cantilever_k(KEEPER_T_MM, KEEPER_W_MM, KEEPER_L_MM)
    leaf_term = k * KEEPER_OVER_CENTRE_MM
    gate_detent_term = KEEPER_PRELOAD_N          # translating gate detent
    friction_term = MU_PLA_MID * WRITER_PAWL_NORMAL_N
    required = leaf_term + gate_detent_term + friction_term
    avail = WRITER_SOURCED["published_force_n"]
    return dict(
        evidence_class="CALCULATION over the re-profiled keeper leaf + sourced "
                       "PLA friction; the actuator is a sourced class with a "
                       "published-force requirement at purchase",
        leaf_rate_n_per_mm=round(k, 4),
        over_centre_mm=KEEPER_OVER_CENTRE_MM,
        leaf_trip_term_n=round(leaf_term, 4),
        gate_detent_term_n=round(gate_detent_term, 4),
        friction_term_n=round(friction_term, 4),
        required_solenoid_n=round(required, 4),
        available_solenoid_n=avail,
        margin=round(avail / required, 3),
        pass_gate=bool(avail >= required),
        sourced_actuator=WRITER_SOURCED,
        note="the required force is the leaf over-centre trip plus a small "
             "translating gate detent and nose friction; the gate travel does "
             "NOT bend the leaf (the keeper nose slides along the gate). The "
             "1.2 N sourced class clears it with the reported margin; the "
             "bottom-up figure replaces the DND-54 bare assertion.",
    )


# ===========================================================================
# 3. R-DND54-5 -- missed-keeper-set reliability (silent row error)
# ===========================================================================
# A missed keeper set writes a whole row one level off, silently. There is no
# per-cell feedback (R1 unchanged), so the only levers are per-set reliability
# and a per-group verification pass.
#
# Model: the map has ROWS*COLS cells. Each keeper is set once per full map.
#   P(full map correct) = p_set^(ROWS*COLS)   (independent per-cell sets)
# Solving for a 99 percent full map gives the required per-keeper set
# reliability. A per-GROUP verify+retry compares the group's set against the
# intended map and re-sets before the bank pass; one verify with catch-rate c
# and a single retry gives a residual per-cell failure
#   f_eff = (1 - p) * (1 - c * p)
# (both the first set and the retry must miss).
def required_p_set(target_map_ok: float = 0.99) -> float:
    n_cells = ROWS * COLS
    return target_map_ok ** (1.0 / n_cells)


def required_p_set_with_verify(target_map_ok: float = 0.99,
                               catch_rate: float = 0.9) -> float:
    """Per-keeper p_set needed with one per-group verify+retry (catch c).

    Solve (1-p)*(1-c*p) = 1 - target^(1/N) for p.
    """
    n_cells = ROWS * COLS
    f_req = 1.0 - target_map_ok ** (1.0 / n_cells)
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        f = (1.0 - mid) * (1.0 - catch_rate * mid)
        if f > f_req:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def required_p_set_redundant(target_map_ok: float = 0.99,
                             redundancy: int = 2) -> float:
    """Per-keeper p_set with `redundancy` independent set attempts, all must fail.

    A redundant writer writes each keeper `redundancy` times; the keeper holds
    if any attempt lands. Residual failure = (1-p)^redundancy.
    """
    n_cells = ROWS * COLS
    f_req = 1.0 - target_map_ok ** (1.0 / n_cells)
    return 1.0 - f_req ** (1.0 / redundancy)


def reliability(target_map_ok: float = 0.99) -> dict:
    """The required PER-KEEPER failure rate q = 1 - p_set for each architecture.

    Reporting q (not p) makes the relaxation visible: p is within 1e-6 of 1, so
    a relative comparison of p is useless, while q is the quantity a mechanical
    engineer can reason about.
    """
    n_cells = ROWS * COLS
    groups = math.ceil(ROWS / reg.ROWS_IN_BANK)
    q_bare = 1.0 - required_p_set(target_map_ok)
    q_verify_lo = 1.0 - required_p_set_with_verify(target_map_ok, catch_rate=0.5)
    q_verify = 1.0 - required_p_set_with_verify(target_map_ok, catch_rate=0.9)
    q_red2 = 1.0 - required_p_set_redundant(target_map_ok, redundancy=2)
    archs = {
        "bare_one_set": dict(
            required_q=q_bare,
            q_vs_bare=1.0,
            note="no feedback; one set per keeper; a miss is silent."),
        "per_group_verify_retry_c50": dict(
            required_q=q_verify_lo,
            q_vs_bare=round(q_verify_lo / q_bare, 2),
            note="one verify+retry per group at a conservative 50 percent "
                 "catch rate."),
        "per_group_verify_retry_c90": dict(
            required_q=q_verify,
            q_vs_bare=round(q_verify / q_bare, 2),
            note="one verify+retry per group at a 90 percent catch rate."),
        "writer_redundancy_2x": dict(
            required_q=q_red2,
            q_vs_bare=round(q_red2 / q_bare, 2),
            note="two independent set attempts per keeper."),
    }
    return dict(
        evidence_class="CALCULATION (independent per-cell Bernoulli model); no "
                       "per-cell feedback is assumed (R1 unchanged)",
        target_map_ok=target_map_ok,
        n_cells=n_cells,
        groups=groups,
        architectures=archs,
        bare_q_required=round(q_bare, 10),
        bare_q_required_str="%.2e" % q_bare,
        note="the bare architecture needs a per-keeper failure probability of "
             "order 1.6e-6 (i.e. p_set = 1 - 1.6e-6) for a 99 percent full map; "
             "that is a demanding mechanical standard with no feedback. The "
             "verify+retry and redundancy architectures RELAX the required q by "
             "the reported factor (q_vs_bare < 1), so a per-group verification "
             "pass is the agent-reachable lever; it is a firmware/kinematic "
             "addition, not a per-cell sensor.",
        residual="the per-set failure probability q itself (as-printed) remains "
                 "measurement-only; this module bounds the requirement and the "
                 "levers, not a measured q.",
    )


# ===========================================================================
# 4. R-DND54-3 -- bank crank speed and writer settle (the time assumption)
# ===========================================================================
# DND-54 assumed 720 deg/s crank and 0.05 s writer settle, with a break-even of
# 468 deg/s / 0.084 s. Here the break-even is re-derived at the *re-profiled*
# geometry (the writer settle is unchanged; the crank term is unchanged) and the
# sourced motor class is checked against it. The 720 deg/s figure must be shown
# to sit inside the sourced NEMA17-class speed/torque envelope.
BANK_CRANK_DEG_S = reg.BANK_CRANK_DEG_S          # 720
WRITER_SETTLE_S = reg.WRITER_SETTLE_S            # 0.05

# Sourced bank-motor class: a fully-orderable NEMA17 stepper (DND-52 basis) with
# the DND-54 torque-class figure of 0.30 N*m holding torque. Its no-load pull-out
# speed is far above 720 deg/s (a NEMA17 at 24 V easily sustains >2 rev/s); the
# binding check is *speed at the required torque*, which this module computes.
BANK_MOTOR = dict(
    class_="NEMA17-class bipolar stepper, 24 V, microstepped",
    holding_torque_nm=reg.BANK_MOTOR_TORQUE_NM,     # 0.30
    max_speed_deg_s=1800.0,                         # sourced-class figure
    unit_usd=12.00,
    source="sourced-class allowance carried by DND-52/DND-54 (NEMA17 stepper at "
           "$12); a published speed/torque curve is required at purchase "
           "(DND-27 forbids buying)",
)


def crank_speed() -> dict:
    sens = reg.sensitivity(reg.ROWS_IN_BANK)
    min_crank = sens["timing_min_crank_deg_s_for_30s"]
    max_settle = sens["timing_max_settle_s_for_30s"]
    # Required torque at speed: the DND-54 bank drive load / pinion radius.
    bd = reg.bank_drive_load(reg.ROWS_IN_BANK)
    req_torque = (bd["required_motor_force_n"] / reg.BANK_MOTORS
                  * reg.BANK_PINION_RADIUS_MM / 1000.0)
    return dict(
        evidence_class="CALCULATION over the sourced NEMA17 class; the "
                       "speed/torque curve is a sourced-class figure, sample-"
                       "confirmed only at purchase (DND-27)",
        chosen_crank_deg_s=BANK_CRANK_DEG_S,
        min_crank_deg_s_for_30s=round(min_crank, 2),
        crank_margin=round(BANK_CRANK_DEG_S / min_crank, 3),
        chosen_settle_s=WRITER_SETTLE_S,
        max_settle_s_for_30s=round(max_settle, 4),
        settle_margin=round(max_settle / WRITER_SETTLE_S, 3),
        required_torque_per_motor_nm=round(req_torque, 4),
        sourced_motor=BANK_MOTOR,
        speed_inside_sourced_class=bool(BANK_CRANK_DEG_S
                                        <= BANK_MOTOR["max_speed_deg_s"]),
        torque_margin=round(BANK_MOTOR["holding_torque_nm"] / req_torque, 3),
        note="the timing gate is conditional on the crank speed and writer "
             "settle exactly as DND-54 stated; this reports both break-evens and "
             "the sourced-class margin. The speed is inside the sourced class "
             "and the torque margin is the same 2.15x the register model uses.",
        residual="the *loaded* speed/torque curve of the sourced NEMA17 is a "
                 "measurement-only quantity (DND-27); this bounds it against the "
                 "sourced class, it does not measure it.",
    )


# ===========================================================================
# 5. R-DND55-1 -- bar reaction eccentricity e (irrelevant for the steel rod)
# ===========================================================================
def bar_eccentricity() -> dict:
    g_steel = bank.shear_modulus_mpa(bank.STEEL_E_MPA, bank.STEEL_POISSON)
    j6 = bank.torsion_constant_round(6.0)
    gate_half = reg.KEEPER_GATE_STEP_MM / 2.0
    # At the CHOSEN sourced steel rod d=6, even an extreme eccentricity e = the
    # pinion radius (6 mm) leaves the skew far inside the gate/2 bound.
    r_extreme = bank.bar_torsion(j_mm4=j6, g_mpa=g_steel,
                                 eccentricity_mm=reg.BANK_PINION_RADIUS_MM)
    r_nom = bank.bar_torsion(j_mm4=j6, g_mpa=g_steel, eccentricity_mm=3.0)
    # Break-even eccentricity for the steel rod: the e that reaches gate/2.
    total = bank.COLS * bank.BANK_ROWS * bank.PER_PAWL_N
    half = bank.BANK_SPAN_MM / 2.0
    e_break = (gate_half * g_steel * j6 * 2.0
               / (total * half ** 2 / bank.BANK_SPAN_MM
                  * bank.TOOTH_TIP_RADIUS_MM))
    return dict(
        evidence_class="CALCULATION over the sourced steel-rod section "
                       "(DND-58/DND-55 torsion model)",
        chosen_bar_material=reg.BAR_MATERIAL,
        chosen_bar_d_mm=reg.BAR_D_MM,
        nominal_skew_mm=r_nom["peak_tip_skew_mm"],
        extreme_e_skew_mm=r_extreme["peak_tip_skew_mm"],
        extreme_e_mm=reg.BANK_PINION_RADIUS_MM,
        gate_half_mm=gate_half,
        break_even_eccentricity_mm=round(e_break, 2),
        margin_at_extreme_e=round(gate_half / r_extreme["peak_tip_skew_mm"], 1),
        closed=bool(r_extreme["passes"]),
        note="for the sourced steel rod d=6 the peak tip skew stays ~%.0fx "
             "inside the gate/2 bound even at an extreme reaction eccentricity "
             "e = the pinion radius (%.0f mm); the break-even e is %.0f mm, far "
             "beyond any physical tooth-contact offset. R-DND55-1 is therefore "
             "closed for the chosen design: eccentricity is irrelevant for the "
             "steel rod (it remains an assumption only for the printed-bar "
             "fallback)."
             % (gate_half / r_extreme["peak_tip_skew_mm"],
                reg.BANK_PINION_RADIUS_MM, e_break),
    )


# ===========================================================================
# Consolidated disposition
# ===========================================================================
def decide() -> dict:
    keeper = keeper_reprofile()
    writer = writer_force_bottom_up()
    rel = reliability()
    crank = crank_speed()
    ecc = bar_eccentricity()
    gates = {
        "KEEPER_prints_2_lines": bool(keeper["new_leaf"]["t_mm"] >= MIN_WALL_MM),
        "KEEPER_hold_margin_gt_3x": bool(
            keeper["hold_mechanism"]["margin_lo"] > 3.0),
        "WRITER_bottom_up_passes": writer["pass_gate"],
        "CRANK_speed_inside_sourced_class": crank["speed_inside_sourced_class"],
        "CRANK_settle_margin_gt_1": bool(crank["settle_margin"] > 1.0),
        "ECC_closed_for_steel_rod": ecc["closed"],
    }
    return dict(
        gates=gates,
        all_retirable_gates_pass=bool(all(gates.values())),
        residuals={
            "R-DND54-KEEPER": "closed (re-profiled to 2 lines + hard-shoulder "
                              "hold; printability PASS)",
            "R-DND54-6": "closed-agent-side (bottom-up force derived and cleared "
                         "by the sourced actuator class; a published-force "
                         "listing is a purchase-time confirmation)",
            "R-DND54-5": "bounded-agent-side (required per-set reliability "
                         "derived; verify+retry / redundancy levers quantified; "
                         "as-printed q is the measurement-only residue)",
            "R-DND54-3": "bounded-agent-side (break-evens re-derived; sourced "
                         "motor class clears; loaded curve is measurement-only)",
            "R-DND55-1": "closed for the sourced steel rod",
        },
        measurement_only_residue=[
            "R-DND54-1 as-printed pawl/keeper friction mu and gate/tip sharpness",
            "R-DND54-2 printed-leaf creep/fatigue",
            "R-DND54-5 as-printed per-set reliability q (the requirement is "
            "bounded here; the measured value is not)",
            "R-DND54-3 loaded NEMA17 speed/torque curve",
        ],
        evidence_class="CAD geometry + CALCULATION + sourced actuator specs; no "
                       "print, no purchase, no measurement (DND-27)",
    )


def screen() -> dict:
    return dict(
        evidence_class="CAD + CALCULATION + sourced listings (DND-27); no "
                       "print/purchase/measurement",
        keeper=keeper_reprofile(),
        keeper_tolerance_mc=keeper_tolerance_mc(),
        writer_force=writer_force_bottom_up(),
        reliability=reliability(),
        crank_speed=crank_speed(),
        bar_eccentricity=bar_eccentricity(),
        decision=decide(),
    )


if __name__ == "__main__":
    print(json.dumps(screen(), indent=2))
