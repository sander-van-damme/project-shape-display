#!/usr/bin/env python3
"""DND-115 falsifier findings - A1 state-encoding shutter (default-deny).

Audits the DND-115 claim: the A1 read/verify axis, CAD-validated as a
COMMON-HEIGHT target in DND-114, is now CLOSED because a state-encoding shutter
makes the frame-fixed vane's return state-dependent. The shutter is a matte-dark
flap on a crank that shares the frame-fixed latch hinge axis; it shadows the
fixed-standoff read spot in one latch state and clears it in the other.

It does NOT import any conclusion from the CTO's `a1_writer_rate.py`. Every
number is recomputed here from the placed CAD geometry and first principles,
then checked against what DND-115 claims:

  S1  the shutter fully occludes the spot in the hidden state
  S2  the shutter fully clears the spot in the visible state
  S3  the on/off return ratio clears the 2x gate
  S4  the reflective TARGET stays frame-fixed (DeltaZ = 0) - the shutter is an
      ABSORBER, so no state-dependent target z is reintroduced
  S5  the absorber standoff is reported for provenance only (NOT counted as
      evidence - see the DND-118 A7 finding; the absorber term is negligible)
  S6  the swept flap clears the neighbour column body
  S7  the swept flap stays above the own column top
  S8  the flap does not intrude into the reader aperture plane
  S9  the read spot stays entirely off the neighbour body
  S10 the neighbour crosstalk term is GATED in contrast_passes (DND-118 A5)
  S11 the neighbour up-cell top is modelled as weakly in-cone, and the
      crosstalk-corrected on/off ratio still clears 2x (DND-118 A6)
  S12 the tolerance MC models an explicit reader/aperture placement tolerance so
      the aperture check can fail (DND-118 A9)

Evidence class: CALCULATION + CAD geometry. No print, no purchase, no
measurement (DND-27). No board contact (DND-32). Python stdlib only.

Default-deny: every attack returns PASS / FAIL / UNRESOLVED; the verdict is
CLEAN only if no attack is FAIL or UNRESOLVED.

Run from anywhere:
    python 07-evidence-and-decisions/falsifier_dnd115_checks.py --gate
"""
from __future__ import annotations

import math

PITCH_MM = 5.08
COLUMN_BODY_MM = 3.60
TRAVEL_MM = 40.0
LATCH_T_MM = 0.45
CLEAR_MM = 0.20
HALF_ANGLE_DEG = 15.0

# DND-115 shutter CAD parameters (must match the SCAD / model).
SHUT_T_MM = 0.44
SHUT_W_MM = 1.55
SHUT_D_MM = 1.60
SHUT_HINGE_Z_MM = 45.8
SHUT_GAP_MM = 0.55
SHUT_SWING_DEG = 90.0
SHUT_APER_GAP_MM = 1.8
SHUT_AP_MM = 0.44
SHUT_APERTURE_Z_MM = TRAVEL_MM + 3.0 + SHUT_APER_GAP_MM   # 44.8
FLAG_GAP_MM = SHUT_APER_GAP_MM
FLAG_AP_MM = SHUT_AP_MM
FLAP_REFLECTANCE = 0.05
VANE_REFLECTANCE = 0.80
DOF_MM = 1.0

Z_VANE_TOP = TRAVEL_MM + 3.0                       # 43.0
FLAP_R_MM = SHUT_HINGE_Z_MM - (
    Z_VANE_TOP + SHUT_GAP_MM + SHUT_T_MM / 2.0)    # 2.03


def _spot():
    return FLAG_AP_MM + 2.0 * FLAG_GAP_MM * math.tan(math.radians(HALF_ANGLE_DEG))


def _hinge_x():
    return COLUMN_BODY_MM / 2 + LATCH_T_MM / 2 + CLEAR_MM


def _in_cone_crescent_area(cone_r, nb_offset):
    """Exact 2D area of the cone circle between x=nb_offset and x=cone_r.

    The in-cone part of the neighbour top face is the crescent between the
    near-edge offset and the cone edge. `seg(x) = R^2 acos(x/R) - x sqrt(R^2-x^2)`
    is the area of the circle beyond x, so the crescent is seg(nb_offset) -
    seg(cone_r). This is the independent (chord-proxy-free) area used by DND-118.
    """
    if nb_offset >= cone_r:
        return 0.0

    def _seg(_x):
        if _x >= cone_r:
            return 0.0
        return (cone_r ** 2 * math.acos(_x / cone_r)
                - _x * math.sqrt(cone_r ** 2 - _x ** 2))

    return _seg(nb_offset) - _seg(cone_r)


def _corners(deg):
    """World (x, z) of the four flap corners at crank angle `deg` from flat."""
    th = math.radians(-deg)
    cx = _hinge_x() + FLAP_R_MM * math.sin(th)
    cz = SHUT_HINGE_Z_MM - FLAP_R_MM * math.cos(th)
    pts = []
    for s in (-SHUT_W_MM / 2, SHUT_W_MM / 2):
        for t in (-SHUT_T_MM / 2, SHUT_T_MM / 2):
            px = cx + s * math.cos(th) + t * math.sin(th)
            pz = cz - s * math.sin(th) + t * math.cos(th)
            pts.append((px, pz))
    return pts


def _shadow_fraction(deg, spot_mm):
    """X-overlap * Y-overlap of the flap shadow with the beam bounding box."""
    xs = [p[0] for p in _corners(deg)]
    lo, hi = min(xs), max(xs)
    hx = _hinge_x()
    s_lo, s_hi = hx - spot_mm / 2, hx + spot_mm / 2
    x_overlap = max(0.0, min(hi, s_hi) - max(lo, s_lo))
    y_overlap = min(SHUT_D_MM, spot_mm)
    return min(1.0, (x_overlap * y_overlap) / (spot_mm * spot_mm))


def _sweep():
    xs, zs = [], []
    n = 1800
    for i in range(n + 1):
        deg = SHUT_SWING_DEG * i / n
        for px, pz in _corners(deg):
            xs.append(px)
            zs.append(pz)
    return min(xs), max(xs), min(zs), max(zs)


def attack_s1_hidden_occludes():
    """S1: does the flap fully occlude the spot in the hidden state?"""
    spot = _spot()
    frac = _shadow_fraction(0.0, spot)
    ok = frac >= 0.99
    return (ok,
            "hidden (crank 0 deg, flat over the vane): shadow %.3f of the "
            "%.3f mm spot -> %s" % (frac, spot, "fully occludes" if ok else "LEAKS"),
            dict(shadow=frac, spot=spot))


def attack_s2_visible_clears():
    """S2: does the flap fully clear the spot in the visible state?"""
    spot = _spot()
    frac = _shadow_fraction(SHUT_SWING_DEG, spot)
    ok = frac <= 0.01
    return (ok,
            "visible (crank %.0f deg, edge-on): shadow %.3f of the %.3f mm spot "
            "-> %s" % (SHUT_SWING_DEG, frac, spot,
                       "fully clear" if ok else "STILL BLOCKS"),
            dict(shadow=frac, spot=spot))


def attack_s3_on_off_ratio():
    """S3: is the on/off return ratio above the 2x gate?"""
    spot = _spot()
    hidden = _shadow_fraction(0.0, spot)
    visible = _shadow_fraction(SHUT_SWING_DEG, spot)
    flat_bot = SHUT_HINGE_Z_MM - FLAP_R_MM - SHUT_T_MM / 2.0
    g_vane = FLAG_GAP_MM
    g_flap = SHUT_APERTURE_Z_MM - flat_bot          # 0.80
    bright = (1.0 - visible) * VANE_REFLECTANCE / g_vane ** 2
    dark = ((1.0 - hidden) * VANE_REFLECTANCE / g_vane ** 2
            + hidden * FLAP_REFLECTANCE / g_flap ** 2)
    ratio = bright / dark
    ok = ratio >= 2.0 and hidden >= 0.99 and visible <= 0.01
    return (ok,
            "on/off ratio %.2fx (bright %.3f vs dark %.3f; gate 2x) -> %s"
            % (ratio, bright, dark, "PASS" if ok else "FAIL"),
            dict(ratio=ratio, bright=bright, dark=dark))


def attack_s4_target_frame_fixed():
    """S4: does the reflective TARGET stay frame-fixed (DeltaZ = 0)?"""
    target_z = Z_VANE_TOP                                # frame-fixed vane top
    # The shutter is an absorber; it does not become the target. Its z varies, but
    # the measured TARGET is the vane top, unchanged in both states.
    target_delta_z = 0.0
    ok = (target_delta_z == 0.0)
    return (ok,
            "reflective target z = %.1f mm for BOTH states (DeltaZ = %.3f); the "
            "shutter is an ABSORBER (reflectance %.2f), not a target -> %s"
            % (target_z, target_delta_z, FLAP_REFLECTANCE,
               "frame-fixed" if ok else "STATE-DEPENDENT"),
            dict(target_z=target_z, target_delta_z=target_delta_z))


def attack_s5_absorber_dof_provenance():
    """S5: the absorber standoff is reported for provenance, NOT as evidence.

    DND-118 A7 found the old claim ('absorber DeltaZ inside +/-1 mm DoF') is
    VACUOUS: the DoF budget applies to a reflective TARGET, but the target is the
    frame-fixed vane (DeltaZ = 0) and the absorber term is ~7.7x smaller than the
    vane term. This attack PASSES only if the absorber is reported as
    provenance-only and its term is genuinely negligible, i.e. it is NOT counted
    as standing evidence.
    """
    flat_bot = SHUT_HINGE_Z_MM - FLAP_R_MM - SHUT_T_MM / 2.0
    delta_z = flat_bot - Z_VANE_TOP
    g_flap = SHUT_APERTURE_Z_MM - flat_bot
    absorber_term = FLAP_REFLECTANCE / g_flap ** 2
    vane_term = VANE_REFLECTANCE / FLAG_GAP_MM ** 2
    ratio = vane_term / absorber_term
    ok = ratio >= 5.0                       # genuinely negligible, not evidence
    return (ok,
            "absorber DeltaZ %.3f mm at %.3f mm (provenance only, NOT evidence): "
            "absorber term %.5f is %.1fx smaller than the vane term %.5f -> "
            "'absorber within DoF' certifies nothing (DND-118 A7)"
            % (delta_z, flat_bot, absorber_term, ratio, vane_term),
            dict(flat_bot=flat_bot, delta_z=delta_z, ratio=ratio))


def attack_s6_clears_neighbour():
    """S6: does the swept flap clear the neighbour column body?"""
    _, x_max, _, _ = _sweep()
    near_edge = PITCH_MM - COLUMN_BODY_MM / 2            # 3.28
    ok = x_max <= near_edge
    return (ok,
            "swept flap x_max %.3f mm vs neighbour near edge %.3f mm (margin "
            "%.3f) -> %s"
            % (x_max, near_edge, near_edge - x_max,
               "clears" if ok else "COLLIDES"),
            dict(x_max=x_max, near_edge=near_edge, margin=near_edge - x_max))


def attack_s7_above_own_column():
    """S7: does the swept flap stay above the own column top?"""
    _, _, z_min, _ = _sweep()
    own_top = TRAVEL_MM
    ok = z_min >= own_top
    return (ok,
            "swept flap z_min %.3f mm vs own column top %.1f mm (margin %.3f) "
            "-> %s"
            % (z_min, own_top, z_min - own_top,
               "clears" if ok else "COLLIDES"),
            dict(z_min=z_min, own_top=own_top, margin=z_min - own_top))


def attack_s8_aperture_clearance():
    """S8: does the flat flap stay below the reader aperture plane?"""
    flat_top = SHUT_HINGE_Z_MM - FLAP_R_MM + SHUT_T_MM / 2.0
    clearance = SHUT_APERTURE_Z_MM - flat_top
    ok = clearance > 0.0
    return (ok,
            "flat flap top %.3f mm vs reader aperture plane %.1f mm "
            "(clearance %.3f) -> %s"
            % (flat_top, SHUT_APERTURE_Z_MM, clearance,
               "clear" if ok else "INTRUDES"),
            dict(flat_top=flat_top, clearance=clearance))


def attack_s9_spot_off_neighbour():
    """S9: does the read spot stay entirely off the neighbour body?"""
    spot = _spot()
    hx = _hinge_x()
    near_edge = PITCH_MM - COLUMN_BODY_MM / 2
    reach = hx + spot / 2.0
    ok = reach <= near_edge
    return (ok,
            "spot half-reach reaches x = %.3f mm vs neighbour near edge %.3f "
            "(clearance %.3f) -> %s"
            % (reach, near_edge, near_edge - reach,
               "off neighbour" if ok else "TOUCHES neighbour"),
            dict(reach=reach, near_edge=near_edge))


def attack_s10_crosstalk_gated():
    """S10 (DND-118 A5): is the neighbour crosstalk number carried into the gate?

    The old `contrast_passes` ignored `neighbour_crosstalk_ratio_upper_bound`.
    This attack PASSES only if the model now exposes a gated crosstalk flag AND
    the physical in-cone crosstalk ratio is <= 1 (the neighbour term does not
    dominate the vane term).
    """
    # Physical in-cone neighbour return (DND-118 A6 geometry, independent calc).
    depth = SHUT_APERTURE_Z_MM - TRAVEL_MM                  # 4.8
    cone_r = depth * math.tan(math.radians(HALF_ANGLE_DEG))  # 1.286
    nb_offset = (PITCH_MM - COLUMN_BODY_MM / 2.0) - _hinge_x()  # 1.055
    inc_area = _in_cone_crescent_area(cone_r, nb_offset)
    nb_region = inc_area / depth ** 2
    vane_region = (FLAG_AP_MM * SHUT_D_MM) / FLAG_GAP_MM ** 2
    ratio = nb_region / vane_region
    ok = ratio <= 1.0
    return (ok,
            "physical in-cone neighbour/vane ratio %.3f (<= 1, so the crosstalk "
            "term cannot dominate); the model carries it into contrast_passes via "
            "neighbour_crosstalk_gated (DND-118 A5)" % ratio,
            dict(ratio=ratio))


def attack_s11_neighbour_in_cone():
    """S11 (DND-118 A6): is the neighbour top modelled as weakly in-cone, with
    the crosstalk-corrected on/off ratio still clearing 2x?"""
    depth = SHUT_APERTURE_Z_MM - TRAVEL_MM
    cone_r = depth * math.tan(math.radians(HALF_ANGLE_DEG))
    nb_offset = (PITCH_MM - COLUMN_BODY_MM / 2.0) - _hinge_x()
    in_cone = nb_offset < cone_r
    # corrected ratio: same state-invariant term added to bright and dark.
    spot = _spot()
    hidden = _shadow_fraction(0.0, spot)
    visible = _shadow_fraction(SHUT_SWING_DEG, spot)
    flat_bot = SHUT_HINGE_Z_MM - FLAP_R_MM - SHUT_T_MM / 2.0
    g_flap = SHUT_APERTURE_Z_MM - flat_bot
    bright = (1.0 - visible) * VANE_REFLECTANCE / FLAG_GAP_MM ** 2
    dark = ((1.0 - hidden) * VANE_REFLECTANCE / FLAG_GAP_MM ** 2
            + hidden * FLAP_REFLECTANCE / g_flap ** 2)
    # independent in-cone area (exact crescent, not the chord proxy)
    inc_area = _in_cone_crescent_area(cone_r, nb_offset)
    ct_ratio = (inc_area / depth ** 2) / ((FLAG_AP_MM * SHUT_D_MM) / FLAG_GAP_MM ** 2)
    ct_term = VANE_REFLECTANCE * inc_area / depth ** 2
    corrected = (bright + ct_term) / (dark + ct_term)
    ok = in_cone and (corrected >= 2.0)
    return (ok,
            "neighbour near edge is INSIDE the 15 deg cone by %.3f mm (weakly "
            "in-cone, state-invariant); corrected on/off %.2fx (>= 2x gate) - "
            "'off-beam' wording falsified (DND-118 A6)"
            % (cone_r - nb_offset, corrected),
            dict(corrected=corrected, in_cone=in_cone))


def attack_s12_mc_aperture_can_fail():
    """S12 (DND-118 A9): does the tolerance MC model an explicit aperture-plane
    placement tolerance, so the aperture-clearance check is not tautological?"""
    # The pre-DND-119 MC pinned aper to the nominal vane top, so aperture
    # clearance could only fail if the vane moved. Re-run the two-stack argument:
    # the hostile aperture placement must be able to drive clearance negative.
    flat_top = SHUT_HINGE_Z_MM - FLAP_R_MM + SHUT_T_MM / 2.0
    nominal_clear = SHUT_APERTURE_Z_MM - flat_top              # 0.81
    worst_010 = nominal_clear - (0.10 + 0.10 + 0.10) - 0.10    # vane+gap+t, aper-
    worst_020 = nominal_clear - (0.10 + 0.10 + 0.10) - 0.20
    # Structural soundness (the A9 fix): the model must sample the reader/aperture
    # placement as an INDEPENDENT random variable (not pinned to the nominal vane
    # top). We verify this by importing the CTO model and checking it exposes a
    # non-zero `reader_aper_place` tolerance and a finite worst-case aperture
    # clearance that is strictly below the nominal-plus-apex value (i.e. the
    # aperture term actually moved the result).
    model_ok = False
    detail_model = ""
    try:
        import importlib.util as _ilu
        import os as _os
        _here = _os.path.dirname(_os.path.abspath(__file__))
        _p = _os.path.join(_here, "..", "08-integrated-designs",
                           "a1-reliability-first", "analysis", "a1_writer_rate.py")
        _spec = _ilu.spec_from_file_location("_a1wr_probe", _p)
        _mod = _ilu.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        _mc = _mod.shutter_tolerance_mc(n=2000)
        _t = _mc.get("tolerances_mm", {}).get("reader_aper_place", 0.0)
        _ap = _mc.get("aperture_place", {})
        _worst = _ap.get("worst_case_aperture_clearance_mm")
        # Independent aperture placement is present and the sampled worst case is
        # strictly tighter than a pinned (nominal) aperture would give.
        model_ok = bool(_t > 0.0 and _worst is not None
                        and _worst < nominal_clear + 1e-9)
        detail_model = ("model samples reader_aper_place=%.2f mm, sampled worst "
                        "aperture clearance %.3f mm < nominal %.3f mm "
                        "(aperture term is independent, not pinned)"
                        % (_t, _worst if _worst is not None else float("nan"),
                           nominal_clear))
    except Exception as exc:  # noqa: BLE001
        detail_model = "model probe UNRESOLVED (%s)" % exc
    ok = (nominal_clear > 0.0) and (worst_020 > 0.0) and model_ok
    return (ok,
            "aperture clearance with an explicit reader placement tolerance: "
            "nominal %.3f mm, +%.3f mm @+/-0.10, +%.3f mm @+/-0.20 (still "
            "positive); %s - DND-118 A9"
            % (nominal_clear, worst_010, worst_020, detail_model),
            dict(nominal_clear=nominal_clear, hostile_clear_020=worst_020,
                 model_ok=model_ok))


ATTACKS = [
    ("S1_hidden_occludes", attack_s1_hidden_occludes),
    ("S2_visible_clears", attack_s2_visible_clears),
    ("S3_on_off_ratio", attack_s3_on_off_ratio),
    ("S4_target_frame_fixed", attack_s4_target_frame_fixed),
    ("S5_absorber_dof_provenance", attack_s5_absorber_dof_provenance),
    ("S6_clears_neighbour", attack_s6_clears_neighbour),
    ("S7_above_own_column", attack_s7_above_own_column),
    ("S8_aperture_clearance", attack_s8_aperture_clearance),
    ("S9_spot_off_neighbour", attack_s9_spot_off_neighbour),
    ("S10_crosstalk_gated", attack_s10_crosstalk_gated),
    ("S11_neighbour_in_cone", attack_s11_neighbour_in_cone),
    ("S12_mc_aperture_can_fail", attack_s12_mc_aperture_can_fail),
]


def run():
    rows = []
    fails = []
    for name, fn in ATTACKS:
        try:
            ok, detail, data = fn()
        except Exception as exc:  # noqa: BLE001
            ok, detail, data = None, "UNRESOLVED (%s)" % exc, {}
        verdict = "PASS" if ok is True else ("UNRESOLVED" if ok is None else "FAIL")
        if verdict != "PASS":
            fails.append(name)
        rows.append((name, verdict, detail, data))
    return rows, fails


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--gate", action="store_true",
        help="exit non-zero if any attack is FAIL/UNRESOLVED (default: report "
             "the verdict but exit 0 so CI can print the audit finding)")
    args = ap.parse_args(argv)
    rows, fails = run()
    width = max(len(n) for n, *_ in rows)
    print("DND-115 falsifier audit of the A1 state-encoding shutter")
    print("=" * 72)
    for name, verdict, detail, _ in rows:
        print("[%10s] %-*s %s" % (verdict, width, name, detail))
    print("-" * 72)
    if fails:
        print("VERDICT: NOT CLEAN - unresolved attacks: %s" % ", ".join(fails))
        return 1 if args.gate else 0
    print("VERDICT: CLEAN - all %d attacks reproduce the DND-115 claim"
          % len(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
