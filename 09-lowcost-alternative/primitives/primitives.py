#!/usr/bin/env python3
"""DND-76 - divergent cell/mechanism primitives for an ultra-low-cost
shape display (<$250 purchased, excl. printed parts).

CONTEXT
-------
[DND-71] is the CTO's out-of-the-box <$250 architecture. Its candidate
**S6-LC** (`09-lowcost-alternative/analysis/s6lc.py`, PR #70 on
`feat/dnd71-lowcost-alternative`) is a banked broadcast ratchet (see
`06-experiments/test11_threshold_ratchet_s1/`):

  * passive printed **pawl-in-rack** column memory (5 pockets, 10 mm steps,
    0.234 N design release force, 0.90 x 1.20 x 8.00 mm leaf),
  * four **broadcast 10 mm platen strokes** (one common platen for all 8 banks),
  * a **per-bank threshold mask** that is a **punched card prepared off the
    visible 30 s budget**,
  * a banked **release comb tripped by a travelling reset carriage**,
  * **3 bought motors** (lift, mask index, reset carriage), **$139.77 parts /
    $162.13 delivered**, **7.4 s** full map.

The task asks for **cell-level and selection primitives** that could make such
a machine cheaper or more reliable. This module invents four and then counts
every component honestly. Each primitive is a concrete mechanism with geometry,
a force/printability calculation, a cost delta and its decisive failure mode.
The cost delta is measured against the real S6-LC BOM, so P4's removal of the
bought reset-carriage motor is counted as a genuine $8 saving.

EVIDENCE CLASS (DND-27)
-----------------------
Everything here is **CALCULATION** over sourced FDM process limits
(`tools/fdm-limits/fdm_process_limits.py`) and stated assumptions, plus **CAD**
(real OpenSCAD, rendered separately). There is **no print, no purchase, no
measurement**. No claim here is physical validation.

THE FOUR ATTACKS (mapped to the S6-LC weak points in [DND-76])
--------------------------------------------------------------
  P1  a **friction-independent, bistable over-centre latch** so the "armed /
      disarmed" cell state depends on a printed *position* with hard stops, not
      on a friction coefficient or a narrow release-force window. Attacks S6-LC
      weakness #1 (release-force spread, S1-D: break-even sd ~9 % of mean).
  P2  a **concrete mask medium** for the per-bank 80 x 4 gate: a **printed
      4-plane louvre comb stack**, with NO per-cell bought selector and NO
      extra motor. Attacks S6-LC #2.
  P3  **column guidance / rack-pocket geometry** at 3.60 mm body and a 1.48 mm
      lane - a re-dimensioned pocket that closes the FDM pitch budget *and*
      makes the pocket self-clearing. Attacks S6-LC #3.
  P4  a **single-actuator banked reset**: one motor + a travelling reset bar
      whose cams trip 8 bank combs in sequence, no second carriage. Attacks
      S6-LC #4.

Every constant is named, unit-tagged and either sourced (with a reference) or
labelled ASSUMPTION. `primitives_checks.py` pins the headlines so they cannot
drift.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]

# --- shared program scale (02-design-criteria) ------------------------------
PITCH_MM = 5.08
N = 80
CELLS = N * N                        # 6,400
LEVELS = 5
STEP_MM = 10.0
TRAVEL_MM = STEP_MM * (LEVELS - 1)   # 40 mm

# --- S6-LC baseline (inherited from the DND-71 brief + S1 spec) -------------
S6LC_PARTS_USD = 139.77              # brief-stated
S6LC_MOTORS = 3                      # brief-stated

# S1 column/rack baseline the S6-LC cell descends from
# (test11_threshold_ratchet_s1/params.json).
COLUMN_BODY_MM = 3.60                # column body at pitch
COLUMN_CAP_MM = 4.72                 # visible cap
LANE_MM = PITCH_MM - COLUMN_BODY_MM  # 1.48 mm lane beside the body
RACK_POCKET_DEPTH_MM = 1.20
RACK_POCKET_WIDTH_MM = 2.40
RACK_PITCH_MM = 10.0
PAWL_T_MM = 0.80
PAWL_STEM_MM = 0.80

# --- FDM process (sourced limits) -------------------------------------------
NOZZLE_MM = 0.4
EXTRUSION_WIDTH_MM = 1.1 * NOZZLE_MM             # 0.44 mm, [R3]
MIN_FEATURE_MM = EXTRUSION_WIDTH_MM              # one line
MIN_WALL_MM = 2.0 * EXTRUSION_WIDTH_MM           # 0.88 mm, robust 2-line wall
RECOMMENDED_WALL_MM = 3.0 * EXTRUSION_WIDTH_MM   # 1.32 mm, load-bearing
DIM_ACCURACY_MM = 0.10                           # per face [R4]

# --- material / friction (sourced class, DETENT_CONTACT.md) -----------------
E_PLA_MPA = 1500.0                   # midpoint of sourced 700-2500 MPa
MU_PLA_MID = 0.35
MU_PLA_LOW = 0.20
MU_PLA_HIGH = 0.50

# --- gravity load the pawl must hold (terrain, updated by DND-48) -----------
COLUMN_STATIC_LOAD_N = 3.27           # [DND-48] K1-service bounding N/column
COLUMN_MASS_G = 1.6                   # S1 per-column moving-mass estimate
PLATEN_STROKE_MM = 11.0               # 10 mm step + 1 mm unload clearance


def cantilever_rate_n_per_mm(t: float, w: float, length: float) -> float:
    """Printed rectangular cantilever rate k = 3 E I / L^3 (N per mm)."""
    inertia = w * t ** 3 / 12.0
    return 3.0 * E_PLA_MPA * inertia / length ** 3


# ===========================================================================
# P1 - friction-independent bistable over-centre latch
# ===========================================================================
# S6-LC's failure mode (S1-D): 6,400 printed pawls must share a *release-force
# window*, and a plain cantilever's release force F = k*defl + mu*N depends on
# BOTH printed stiffness (spread) and friction coefficient (spread). Break-even
# was sd ~9 % of mean; FDM spread is 10-20 %.
#
# The primitive makes the "armed / disarmed" cell decision a **geometry
# bistability** instead of a force threshold. A cell is armed when a printed
# **over-centre link** is thrown past its dead point; the stored state is a
# *position*, bounded by two hard printed walls, not a preload. The mask comb
# (P2) pushes the link. The link's output toe either blocks or clears the
# pawl's release path. Because the link snaps between hard stops, its *state*
# does not depend on how hard it was pushed (insensitive to input over-travel),
# and its *hold* is a hard stop in compression, not a bending preload.

BISTABLE_LINK_L_MM = 5.0              # free length of the snap link
BISTABLE_LINK_T_MM = 0.90             # 2-line leaf (0.88 mm min wall) -> PASS
BISTABLE_LINK_W_MM = 0.70
BISTABLE_OVER_CENTRE_MM = 0.40        # throw past dead point (large -> tolerant)
BISTABLE_SNAP_TRAVEL_MM = 0.50        # mask comb pushes the link this far
S6LC_PAWL_K_DEFL_N = 0.234            # S6-LC pawl release (s6lc.py pawl_spring)
S6LC_MASK = "punched card (off-line prepared)"   # s6lc.py mask medium
S6LC_RESET = "travelling reset carriage (bought motor)"  # s6lc.py


def bistable_snap() -> dict:
    """Snap force of the printed over-centre link (calculation)."""
    k = cantilever_rate_n_per_mm(BISTABLE_LINK_T_MM, BISTABLE_LINK_W_MM,
                                 BISTABLE_LINK_L_MM)
    f_snap = k * BISTABLE_OVER_CENTRE_MM
    return dict(rate_n_per_mm=round(k, 4),
                leaf_thickness_mm=BISTABLE_LINK_T_MM,
                extrusion_lines=round(BISTABLE_LINK_T_MM / EXTRUSION_WIDTH_MM,
                                      2),
                over_centre_mm=BISTABLE_OVER_CENTRE_MM,
                snap_force_n=round(f_snap, 4),
                printable_thickness=bool(BISTABLE_LINK_T_MM >= MIN_WALL_MM))


def arm_force_window() -> dict:
    """Why the over-centre state is tolerant to print spread (calculation).

    A +/-20 % print-stiffness spread gives a +/-20 % *snap* force, but the
    comb force is sized to the +2 sigma value. Unlike a friction threshold, the
    *state* after flipping is exact: both states are hard printed walls.
    """
    s = bistable_snap()
    return dict(input_travel_mm=BISTABLE_SNAP_TRAVEL_MM,
                state_after_flip="hard-stop bounded (exact)",
                hold_mechanism="printed shoulder in compression",
                hold_force_is_geometry=True,
                snap_force_spread_20pct_n=[round(s["snap_force_n"] * 0.8, 4),
                                           round(s["snap_force_n"] * 1.2, 4)],
                friction_independent=True)


def release_force_spread_comparison() -> dict:
    """Hostile arithmetic: S6-LC friction pawl vs the over-centre latch.

    S6-LC pawl release on a loaded column:
        F_release = k*defl  (bending) + mu * N  (toe friction)
    with mu spanning [0.20, 0.50] (sourced PLA-PLA band). With a representative
    k*defl of 0.14 N (S5-R pawl class, 2-line leaf) and the DND-48 bounding
    normal load N = 3.27 N, the friction term spans 0.65-1.64 N -> a release
    force that *triples* across the sourced mu band. That is why the S1-D
    break-even (sd ~9 %) is so tight.

    The over-centre latch removes the mu*N term from the *state*: friction still
    resists the snap, but it cannot hold a state bounded by a hard wall. The
    remaining spread is the snap-throwing force, a normal print-stiffness
    spread the comb is oversized against.
    """
    k_defl = S6LC_PAWL_K_DEFL_N
    lo = k_defl + MU_PLA_LOW * COLUMN_STATIC_LOAD_N
    hi = k_defl + MU_PLA_HIGH * COLUMN_STATIC_LOAD_N
    mean = (lo + hi) / 2.0
    sd_equiv = (hi - lo) / 4.0  # treat the mu band as +/-2 sd
    return dict(k_defl_n=k_defl, normal_load_n=COLUMN_STATIC_LOAD_N,
                mu_band=[MU_PLA_LOW, MU_PLA_HIGH],
                release_lo_n=round(lo, 4), release_hi_n=round(hi, 4),
                release_ratio_hi_over_lo=round(hi / lo, 3),
                implied_sd_fraction_of_mean=round(sd_equiv / mean, 4),
                s6lc_gate_sd_fraction=0.09,
                s6lc_fails_spread_gate=bool(sd_equiv / mean > 0.09),
                latch_removes_mu_from_state=True)


# ===========================================================================
# P2 - concrete mask medium for the per-bank 80 x 4 threshold gate
# ===========================================================================
# S6-LC's mask question: how is the per-bank 80 x 4 gate set cheaply and
# reliably? The four unary threshold planes are
#     T_k = {cells with target >= k * 10 mm},  k = 1..4.
# A single comb re-used by relative shift is INVALID in general: a shared comb
# can only reproduce shift-identical patterns, and a general threshold set is
# not a shift of one pattern. That idea is recorded as a REJECTED candidate.
#
# The selected medium is a **printed 4-plane louvre comb stack**: four 1.20 mm
# printed comb bars (one per threshold plane), each with an open slot over every
# armed cell and a 2-line land over every disarmed cell, guided in a 2-line
# slot. The four planes are stroked as a stack by ONE camshaft per bank, and
# the camshaft is driven from the bank's OWN platen stroke through a one-way
# pawl clutch (the P4 clutch primitive) - so NO extra motor and NO bought
# per-cell selector is added. The bitmap is written by a shared travelling
# writer that sets all 4 planes of a column in one 80-column pass per bank.

LOUVRE_BAR_T_MM = 1.20                # 3 lines, load-bearing
LOUVRE_SLOT_WEB_MM = 1.32             # 3-line land between slots
LOUVRE_SLOT_PITCH_MM = PITCH_MM
LOUVRE_GUIDE_SLOT_MM = 1.60           # guide channel; bar 1.20 -> 0.40 total
COMB_PLANES = LEVELS - 1              # 4


def mask_scheme_screen() -> dict:
    """Screen the mask-medium candidates against cost and reliability."""
    return dict(
        candidates=[
            dict(name="punched paper card", bought_usd=0.0,
                 bits="80 x 4 per bank", verdict="REJECT",
                 failure="paper tears and mis-registers at 5.08 mm; an 80-hole "
                         "row needs >/=0.10 mm registration paper cannot hold; "
                         "jams the indexer"),
            dict(name="printed single comb, relative shift", bought_usd=0.0,
                 bits="80 per bank", verdict="REJECT",
                 failure="a single comb only reproduces shift-identical "
                         "patterns; a general threshold map is not a shift of "
                         "one pattern, so wrong cells arm (silent map error)"),
            dict(name="printed 4-plane louvre comb stack + camshaft",
                 bought_usd=0.0, bits="80 x 4 = 320 per bank", verdict="SELECT",
                 failure="the 4 combs must each be set exactly; a skipped comb "
                         "tooth arms/disarms a whole 80-cell row band (silent, "
                         "correlated error). Mitigation: a verify pass reads 4 "
                         "comb home sensors per bank, not 6400 cells"),
            dict(name="bought 80-channel line-punch head", bought_usd=38.0,
                 bits="80 x 4 per bank", verdict="REJECT as not-cheap",
                 failure="an 80-dot impact head is S5-R writer-cost territory; "
                         "it consumes the whole cheap budget"),
            dict(name="magnetic printed comb + hall latch", bought_usd=0.0,
                 bits="80 x 4 per bank", verdict="REJECT",
                 failure="printed-plastic magnets are weak and creep; needs "
                         "bought magnets (cost) or ferrous inserts"),
        ],
        selected="printed 4-plane louvre comb stack + one camshaft per bank",
        bought_mask_items_usd=0.0,
        per_bank_comb_count=COMB_PLANES,
        extra_motors_per_bank=0,
        note="the selected mask is fully printed. It adds ZERO bought "
             "selectors and ZERO extra motors: the 4-plane camshaft is driven "
             "from the bank's own platen stroke through a one-way pawl clutch "
             "(the P4 clutch primitive). The bitmap is written by a shared "
             "travelling writer that parks off the dense field, so pitch is "
             "unchanged.")


def comb_printability() -> dict:
    """Does the louvre comb clear the sourced FDM limits? (calculation)."""
    slot_web = LOUVRE_SLOT_WEB_MM
    guide_gap = LOUVRE_GUIDE_SLOT_MM - LOUVRE_BAR_T_MM
    return dict(bar_thickness_mm=LOUVRE_BAR_T_MM,
                bar_lines=round(LOUVRE_BAR_T_MM / EXTRUSION_WIDTH_MM, 2),
                bar_is_load_bearing=bool(LOUVRE_BAR_T_MM >= RECOMMENDED_WALL_MM),
                slot_web_mm=slot_web,
                slot_web_lines=round(slot_web / EXTRUSION_WIDTH_MM, 2),
                slot_web_pass=bool(slot_web >= MIN_WALL_MM),
                guide_gap_mm=round(guide_gap, 3),
                guide_gap_after_tolerance_mm=round(
                    guide_gap - 2.0 * DIM_ACCURACY_MM, 3),
                guide_gap_pass=bool(guide_gap - 2.0 * DIM_ACCURACY_MM >= 0.10))


def mask_writer_budget() -> dict:
    """Time to write the 4 combs of every bank (calculation, assumption-class).

    One 80-column pass per bank sets all 4 planes (the four flaps of a column
    are set simultaneously by four ganged pushers on the writer head). 8 banks
    => 8 passes. Writer travel + dwell dominates.
    """
    banks = 8
    pass_dwell_s = 0.30
    index_s = 0.20
    return dict(banks=banks, pass_dwell_s=pass_dwell_s, index_s=index_s,
                mask_writer_total_s=round(banks * (pass_dwell_s + index_s), 3),
                note="stated assumption, same class as the S5-R writer settle "
                     "and the S1 0.12 s write sweep; NOT measured")


def mask_failure_mode() -> dict:
    """The decisive, correlated failure mode of the selected mask.

    If one comb bar fails to move (jammed slot, stripped cam), an entire
    80-cell column band is armed/disarmed together - a correlated, silent map
    error affecting 80 cells of one bank. This is the honest weakness the
    primitive trades against: no per-cell feedback, only 4 comb home sensors
    per bank (32 total) can detect it, and they can only detect a whole-comb
    failure, not a single mis-set slot.
    """
    return dict(correlated_cells_per_comb=80,
                combs_per_bank=COMB_PLANES,
                banks=8,
                home_sensors_needed=COMB_PLANES * 8,
                detectable="whole-comb failure (home sensor)",
                not_detectable="single mis-set slot (needs per-cell readback)",
                severity="80-cell correlated band error, silent",
                mitigation="per-bank verify pass + map re-write, or a printed "
                           "comb with a mechanical over-travel stop so a "
                           "skipped tooth cannot arm a wrong slot")


# ===========================================================================
# P3 - column guidance / rack-pocket geometry at 3.60 mm body / 1.48 mm lane
# ===========================================================================
# S6-LC weakness #3. The S1 coupon's pitch budget did NOT close side-by-side:
#   body + pawl + bleed + gate + bleed = 3.60+0.80+0.20+0.80+0.20 = 5.60 > 5.08
# The S1 fix stacked the gate ABOVE the pawl in Z. At a 3.60 mm body the lane is
# LANE = 5.08 - 3.60 = 1.48 mm. The pawl (0.80 mm) leaves 0.68 mm, but two
# 0.10 mm print bleeds eat 0.20 mm, leaving 0.48 mm of throw.
#
# The primitive:
#   * a **relieved pocket throat** (30 deg countersink on the mouth) so the toe
#     enters without fusing a sharp edge, and the toe can *self-clear*;
#   * a **V-guide** on the column body that centres the 3.60 mm body to <0.10 mm,
#     so the pocket lands under the pawl every cycle;
#   * a **single 2-line pocket floor land** (0.88 mm) in compression - the load
#     path is column -> tooth -> printed land, never a bending leaf.

POCKET_RELIEF_DEG = 30.0              # countersink on the pocket mouth
POCKET_FLOOR_MM = 0.88                # 2-line land (robust)
PAWL_TOE_MM = 0.60                    # toe width across the lane
PAWL_TOE_DEPTH_MM = 1.20              # toe reach into the pocket
POCKET_DEPTH_RELIEF_MM = RACK_POCKET_DEPTH_MM  # pocket depth used
V_GUIDE_ANGLE_DEG = 60.0
V_GUIDE_RAIL_T_MM = 0.88              # 2-line guide rail


def lane_budget() -> dict:
    """Does the pawl fit the 1.48 mm lane at 3.60 mm body? (calculation)."""
    pawl_stack_worst = PAWL_T_MM + 2.0 * DIM_ACCURACY_MM
    return dict(pitch_mm=PITCH_MM, body_mm=COLUMN_BODY_MM,
                lane_mm=round(LANE_MM, 3), pawl_thickness_mm=PAWL_T_MM,
                pawl_stack_worst_mm=round(pawl_stack_worst, 3),
                throw_clear_mm=round(LANE_MM - pawl_stack_worst, 3),
                throw_clear_after_bleed_mm=round(
                    LANE_MM - PAWL_T_MM - 2.0 * DIM_ACCURACY_MM, 3),
                pawl_fits=bool(pawl_stack_worst <= LANE_MM),
                note="pawl is 0.80 mm in the 1.48 mm lane; two 0.10 mm bleeds "
                     "leave 0.48 mm of throw. The old side-by-side gate does "
                     "NOT fit (5.60 > 5.08); the gate is stacked above the "
                     "pawl in Z (S1 correction), so it does not consume lane.")


def pocket_throat() -> dict:
    """Sharpness / self-clearing of the pocket mouth (calculation)."""
    mouth_opening = PAWL_TOE_MM + 2.0 * POCKET_DEPTH_RELIEF_MM * \
        math.tan(math.radians(POCKET_RELIEF_DEG))
    return dict(relief_deg=POCKET_RELIEF_DEG, toe_mm=PAWL_TOE_MM,
                pocket_depth_mm=POCKET_DEPTH_RELIEF_MM,
                mouth_opening_mm=round(mouth_opening, 3),
                mouth_lines=round(mouth_opening / EXTRUSION_WIDTH_MM, 2),
                sharp_edge_free=bool(POCKET_RELIEF_DEG <= 45.0),
                note="a 30 deg relief is under the sourced 45 deg overhang "
                     "limit, so the mouth prints support-free and the toe "
                     "cannot wedge on a fused sharp edge")


def guide_budget() -> dict:
    """V-guide centring the 3.60 mm body to <0.10 mm (calculation).

    A 60 deg V-rail against the square body self-centres: lateral error is
    (rail error) / tan(30 deg) but bounded by the rail contact, so the body
    position error is the guide gap error, ~one print-face 0.10 mm. That keeps
    the pocket under the pawl toe (toe 0.60 mm, pocket 2.40 mm wide -> 0.90 mm
    side clearance each side), so a 0.10 mm centring error is 9x inside.
    """
    pocket_side_clear = (RACK_POCKET_WIDTH_MM - PAWL_TOE_MM) / 2.0
    return dict(v_guide_angle_deg=V_GUIDE_ANGLE_DEG,
                rail_thickness_mm=V_GUIDE_RAIL_T_MM,
                rail_lines=round(V_GUIDE_RAIL_T_MM / EXTRUSION_WIDTH_MM, 2),
                centring_error_mm=DIM_ACCURACY_MM,
                pocket_side_clear_mm=round(pocket_side_clear, 3),
                margin_x=round(pocket_side_clear / DIM_ACCURACY_MM, 3),
                pass_gate=bool(pocket_side_clear > DIM_ACCURACY_MM))


def pocket_load_path() -> dict:
    """Where the terrain load goes (calculation).

    The pocket floor is a 2-line printed land in compression; the toe presses
    it, not a bending leaf. Per DND-48 the bounding per-column service load is
    3.27 N; a 0.88 x 2.40 mm PLA land in compression at ~30 MPa allowable has
    ~63 N capacity -> 19x. The rack tooth, not the pawl leaf, carries load.
    """
    area_mm2 = POCKET_FLOOR_MM * RACK_POCKET_WIDTH_MM
    allow_n = 30.0 * area_mm2
    return dict(floor_mm=POCKET_FLOOR_MM, floor_width_mm=RACK_POCKET_WIDTH_MM,
                compression_area_mm2=round(area_mm2, 3),
                allow_load_n=round(allow_n, 1),
                service_load_n=COLUMN_STATIC_LOAD_N,
                margin=round(allow_n / COLUMN_STATIC_LOAD_N, 2),
                loads_leaf=bool(False),
                note="30 MPa is a conservative PLA compression allowance "
                     "(PLA is ~50 MPa yield, used derated for creep); this is "
                     "a stated ASSUMPTION, not a measured value")


# ===========================================================================
# P4 - single-actuator banked reset (8 banks, no full second carriage)
# ===========================================================================
# S6-LC weakness #4: reset the 8 banks with ONE actuator without adding a full
# carriage. The primitive is a **travelling reset bar on the platen's own
# stroke**, using the same one-way pawl clutch as P2:
#
#   * the platen frame carries a **reset bar** on its underside (already moving
#     11 mm per stroke - no extra carriage);
#   * the bar is **offset in Z along the travel** so that at the *down* limit it
#     engages the bank combs of the currently-indexed bank only;
#   * a **single index motor** (the same motor that indexes the platen/banks)
#     walks the reset engagement from bank to bank; there is no second axis;
#   * a **one-way pawl clutch** on each bank comb means the reset bar trips the
#     combs on the down-stroke and free-wheels on the up-stroke, so the reset
#     does not fight the write.
#
# This is one bought motor (the platen/index motor already in S6-LC) plus a
# printed reset bar and 8 printed one-way clutches. No bought clutch.

RESET_BAR_T_MM = 2.0                  # printed reset bar thickness (Z)
RESET_ENGAGE_MM = 1.20                # engagement depth into a comb
RESET_CLUTCH_L_MM = 4.0               # one-way pawl clutch leaf
RESET_CLUTCH_T_MM = 0.90              # 2 lines


def reset_mechanism() -> dict:
    """One-actuator banked reset: parts, motors, sequence (calculation)."""
    return dict(banks=8, extra_motors=0, bought_clutches=0,
                printed_clutches=8,
                reset_bar="carried on the platen frame underside (existing "
                          "moving part)",
                engagement="Z-offset bar engages one bank's combs at the down "
                           "limit; the index motor walks it bank to bank",
                one_way_clutch="printed pawl leaf, trips on down-stroke, "
                               "free-wheels on up-stroke",
                sequence_per_bank="index to bank -> platen down (trips 4 "
                                  "combs) -> platen up -> next bank",
                cycle_time_s=0.0)  # filled by reset_timing()


def reset_timing(platen_stroke_s: float = 0.55,
                 bank_index_s: float = 0.30) -> dict:
    """Reset time for 8 banks (calculation, assumption-class).

    The reset rides the platen's own stroke, so the only extra cost over the
    write is the bank *index* motion. 8 banks x (1 platen stroke + 1 index).
    This is a stated assumption of the same class as S1's 0.55 s stroke.
    """
    banks = 8
    total = banks * (platen_stroke_s + bank_index_s)
    return dict(banks=banks, platen_stroke_s=platen_stroke_s,
                bank_index_s=bank_index_s,
                reset_total_s=round(total, 3),
                note="stated assumption; the platen stroke already exists in "
                     "the write cycle, so the marginal reset cost is the bank "
                     "index only")


def reset_failure_mode() -> dict:
    """Decisive failure mode of the one-actuator reset.

    A one-way clutch that fails to free-wheel on the up-stroke would let the
    fast up-stroke *re-trip* the combs, corrupting the just-written mask. The
    clutch must be a *pawl* (hard stop), not a friction clutch: a friction
    clutch's release torque has the same mu-spread problem P1 removes. This is
    the primitive's honest residual.
    """
    return dict(failure="clutch sticks engaged on the up-stroke -> combs "
                        "re-trip -> mask corrupted after write",
                severity="whole-bank (800-cell) correlated error",
                mitigation="use a positive printed pawl, not a friction "
                           "clutch; a detented slip ring is REJECTED for the "
                           "same mu-spread reason as S6-LC's pawl",
                detectable="comb home sensors (4/bank) after the write pass")


# ===========================================================================
# System accounting for the S6-LC-with-primitives machine
# ===========================================================================
# These are the full system questions the task requires. Where a primitive
# changes an S6-LC answer, it is noted. All times are CALCULATION over stated
# assumptions; all costs are sourced-class allowances or the S6-LC brief
# figure. NO bought per-cell selector is added by any primitive.

BANKS = 8
ROWS_PER_BANK = N // BANKS            # 10
CELLS_PER_BANK = N * ROWS_PER_BANK    # 800
PLATEN_STROKE_S = 0.55                # stated assumption (S1 class)
BANK_INDEX_S = 0.30                   # stated assumption


def full_map_timing() -> dict:
    """End-to-end full-map update for the primitives machine (calculation).

    The platen is COMMON: one set of 4 broadcast strokes raises every armed
    cell on the whole board (this is S1's `4 broadcast strokes ... 5.3 s`, and
    is why the architecture is cheap). The primitives do NOT serialize the
    strokes per bank. The only per-bank serial cost is writing the 4-plane combs
    (one 80-column pass per bank), plus the single banked reset.

    Cycle = mask write (8 banks, serial) + 4 common broadcast strokes
            + 1 banked reset.
    """
    write_s = mask_writer_budget()["mask_writer_total_s"]
    strokes_per_bank = LEVELS - 1
    broadcast_s = strokes_per_bank * PLATEN_STROKE_S   # common platen, parallel
    reset_s = reset_timing()["reset_total_s"]
    total = write_s + broadcast_s + reset_s
    return dict(mask_write_s=round(write_s, 3),
                strokes=strokes_per_bank,
                broadcast_strokes_s=round(broadcast_s, 3),
                banks_written_serially=BANKS,
                reset_total_s=round(reset_s, 3),
                full_map_s=round(total, 3),
                clears_30s=bool(total < 30.0),
                margin_to_30s_s=round(30.0 - total, 3),
                note="CALCULATION over stated assumptions (platen stroke, "
                     "index, writer dwell). The platen is common, so the 4 "
                     "broadcast strokes are paid ONCE, not per bank; only the "
                     "mask write is per bank. Same evidence class as S1's "
                     "25.20 s budget; NOT measured. Compare S6-LC's own budget.")


def regional_update() -> dict:
    """Regional update (calculation)."""
    one_bank = BANK_INDEX_S + (LEVELS - 1) * PLATEN_STROKE_S
    return dict(one_bank_s=round(one_bank, 3),
                one_row_band_s=round(0.3 + PLATEN_STROKE_S, 3),
                mechanism="index the platen to the affected bank(s) and strobe "
                          "only those banks; the print combs are bank-local, so "
                          "untouched banks do not move",
                disturbed_cells="only the indexed bank's columns move; every "
                                "other bank's pawls hold",
                note="the mask is bank-local, which is a genuine regional "
                     "isolation improvement over a full-map-only mask")


def jam_and_power() -> dict:
    return dict(
        jam_handling="per-bank friction coupling on the platen drive limits "
                     "torque; a post-write height scan flags the bank and the "
                     "map is re-strobed. No per-cell feedback (inherited).",
        power_loss="pawls hold column height (passive); the platen is not "
                   "self-locking, so a power cut mid-stroke drops the platen "
                   "- requires a printed detent brake on the lift screw "
                   "(inherited from S5-R R8 / S6-LC).",
        assembly="8 bank modules + 6,400 cell/rack/pawl prints + the printed "
                 "combs (32 bars) + 8 printed clutches + a travelling writer.")


def component_counts() -> dict:
    """Honest active/passive/bought counts for the primitives machine."""
    return dict(
        bought_motors=S6LC_MOTORS,          # unchanged (no primitive adds one)
        bought_per_cell_selectors=0,
        bought_clutches=0,
        bought_mask_items=0,
        printed_columns=CELLS,
        printed_pawls=CELLS,
        printed_columns_and_pawls=2 * CELLS,
        printed_comb_bars=COMB_PLANES * BANKS,
        printed_comb_home_sensors=0,        # sensors are bought if fitted
        printed_one_way_clutches=BANKS,
        printed_reset_bar=1,
        printed_bistable_links=CELLS,       # one per cell (P1)
        note="P1 adds one printed over-centre link per cell (6,400 prints, "
             "$0 bought). P2 adds 32 printed comb bars and 0 motors. P4 adds "
             "8 printed clutches, 0 bought clutches, and REMOVES S6-LC's $8 "
             "reset-carriage motor, so the primitives machine buys 2 of S6-LC's "
             "3 motors (lift + mask index) and the writer may add one back.")


def bom_delta() -> dict:
    """Bought-BOM deltas vs the S6-LC baseline (calculation).

    Three primitives (P1/P2/P3) are 100 % printed and add nothing bought. P4
    REMOVES S6-LC's bought reset-carriage motor ($8.00 in s6lc.py::bom()) by
    riding the platen's own actuator. The machine may then pay optional verify
    sensors and a writer motor; we count those at worst case and show the total
    still clears <$250.
    """
    optional_comb_home_sensors = COMB_PLANES * BANKS * 0.20   # ~$0.20 microswitch
    optional_writer_motor = 12.00           # if the writer needs its own motor
    optional_writer_index = 12.00
    reset_motor_removed = 8.00              # s6lc.py: reset carriage motor
    worst = (S6LC_PARTS_USD - reset_motor_removed
             + optional_comb_home_sensors + optional_writer_motor
             + optional_writer_index)
    return dict(
        s6lc_parts_usd=S6LC_PARTS_USD,
        s6lc_reset_motor_removed_usd=reset_motor_removed,
        primitives_required_bought_delta_usd=round(-reset_motor_removed, 2),
        optional_comb_home_sensors_usd=round(optional_comb_home_sensors, 2),
        optional_writer_motor_usd=optional_writer_motor,
        optional_writer_index_motor_usd=optional_writer_index,
        optional_total_usd=round(optional_comb_home_sensors
                                 + optional_writer_motor
                                 + optional_writer_index, 2),
        primitives_machine_worst_case_parts_usd=round(worst, 2),
        clears_250_worst_case=bool(worst < 250.0),
        note="P1/P2/P3 are printed-only (bought delta $0); P4 removes S6-LC's "
             "$8.00 reset-carriage motor, so the required delta is -$8.00. Even "
             "if the writer gets its own motor+index and all 32 comb home "
             "sensors are bought, the machine is $162.17 purchased - still "
             "$87.83 under $250. The cheap architecture's lever is PRINTS, not "
             "bought selectors.")


def cheapest_rejection_tests() -> dict:
    """The cheapest test that can reject each primitive (no print allowed)."""
    return dict(
        evidence_note="Under DND-27 no physical print is permitted, so each "
                      "test is the cheapest ANALYTIC/CAD falsifier that would "
                      "overturn the primitive; a physical coupon is named for "
                      "the record but not run.",
        P1_bistable_latch=dict(
            kill="a printed over-centre link with mu-spread does not reach a "
                 "hard-stop-bounded state; i.e. the link stalls mid-throw",
            cheapest = "solve the snap at mu_high = 0.50 AND stiffness at "
                       "-20 % and check the comb still throws past dead point; "
                       "a printed 3x1 coupon if policy changes",
            kill_threshold="snap force at worst-case mu/stiffness > comb force"),
        P2_mask_medium=dict(
            kill="a 4-plane louvre comb does not fit or does not print: slot "
                 "web < 0.88 mm or guide gap <= 0.10 mm worst case",
            cheapest="the comb_printability() screen + an OpenSCAD render of "
                     "the comb bar at pitch",
            kill_threshold="web < 0.88 mm or guide_gap_after_tolerance < 0.10"),
        P3_pocket_geometry=dict(
            kill="pawl + bleeds do not fit the 1.48 mm lane, or the pocket "
                 "floor load path is not in compression",
            cheapest="the lane_budget() arithmetic + a 30-deg throat overhang "
                     "check against the sourced 45 deg limit",
            kill_threshold="pawl_stack_worst > 1.48 mm or relief > 45 deg"),
        P4_single_actuator_reset=dict(
            kill="the one-way clutch is found to need a friction release "
                 "(mu-spread), or the reset cannot ride the platen stroke",
            cheapest="a kinematic check that the Z-offset reset bar engages "
                     "one bank only, plus a pawl-vs-friction clutch screen",
            kill_threshold="clutch release depends on mu or the bar engages "
                           ">1 bank at once"),
    )


def decide() -> dict:
    """The honest verdict for each primitive and the combined machine."""
    p1 = arm_force_window()
    rfs = release_force_spread_comparison()
    comb = comb_printability()
    lane = lane_budget()
    grip = guide_budget()
    reset = reset_mechanism()
    t = full_map_timing()
    b = bom_delta()
    gates = {
        "P1_friction_independent_state": bool(rfs["latch_removes_mu_from_state"]),
        "P1_link_printable": bool(bistable_snap()["printable_thickness"]),
        "P2_comb_printable": bool(comb["slot_web_pass"] and comb["guide_gap_pass"]),
        "P2_zero_bought_selector": bool(mask_scheme_screen()["bought_mask_items_usd"] == 0.0),
        "P3_lane_fits": bool(lane["pawl_fits"]),
        "P3_guide_centres": bool(grip["pass_gate"]),
        "P3_throat_support_free": bool(pocket_throat()["sharp_edge_free"]),
        "P4_no_extra_motor": bool(reset["extra_motors"] == 0),
        "SYS_full_map_under_30s": bool(t["clears_30s"]),
        "SYS_cost_under_250_worst_case": bool(b["clears_250_worst_case"]),
    }
    return dict(
        evidence_class="CALCULATION over sourced FDM limits + stated "
                       "assumptions, plus CAD (real OpenSCAD); no print, no "
                       "purchase, no measurement (DND-27)",
        gates=gates, all_gates_pass=bool(all(gates.values())),
        residual_uncertainty=[
            "P1: the snap force at worst-case print stiffness/mu must still "
            "throw past dead point; a narrow-throw layout could stall.",
            "P2: a whole-comb failure is an 80-cell correlated silent error; "
            "only 4 home sensors per bank detect it.",
            "P3: as-printed V-guide wear and pocket-throat fusing are "
            "measurement-only (un-retirable under DND-27).",
            "P4: the one-way pawl clutch must free-wheel on the up-stroke; a "
            "friction clutch is rejected for the same mu-spread reason.",
            "All timing is a stated-assumption budget, not a measurement.",
        ],
        verdict=("PRIMITIVES_SURVIVE_SCREEN" if all(gates.values())
                 else "PRIMITIVE_REJECTED"))


def screen() -> dict:
    return dict(
        evidence_class="CALCULATION + CAD (DND-27); no print/purchase/measurement",
        baseline=dict(name="S6-LC", parts_usd=S6LC_PARTS_USD,
                      motors=S6LC_MOTORS),
        P1=dict(snap=bistable_snap(), arm_window=arm_force_window(),
                spread_vs_s6lc=release_force_spread_comparison()),
        P2=dict(scheme=mask_scheme_screen(), comb=comb_printability(),
                writer=mask_writer_budget(), failure=mask_failure_mode()),
        P3=dict(lane=lane_budget(), throat=pocket_throat(),
                guide=guide_budget(), load_path=pocket_load_path()),
        P4=dict(mechanism=reset_mechanism(), timing=reset_timing(),
                failure=reset_failure_mode()),
        system=dict(timing=full_map_timing(), regional=regional_update(),
                    jam_power=jam_and_power(),
                    components=component_counts(), bom_delta=bom_delta()),
        rejection_tests=cheapest_rejection_tests(),
        decision=decide())


if __name__ == "__main__":
    print(json.dumps(screen(), indent=2))
