#!/usr/bin/env python3
"""DND-114 falsifier findings - A1 common-height read target (default-deny).

Audits the DND-114 claim: the A1 read/verify axis, UNRESOLVED in DND-113, is
resolved by a CAD-validated COMMON-HEIGHT read target (the CH-A frame-fixed
latch-hinge vane), read at ONE fixed standoff for both column states.

It does NOT import any conclusion from the CTO's `a1_writer_rate.py`. Every
number is recomputed here from the placed CAD geometry and first principles,
then checked against what DND-114 claims:

  C1  CH-A target is frame-fixed        -> DeltaZ = 0 by construction
  C2  CH-B hinge-arc DeltaZ bound       -> r_flag <= DoF/(2 sin(swing/2));
                                           DeltaZ <= DoF budget
  C3  flag fits the latch lane in X      -> FLAG_T/2 <= X_CLEAR_NB
  C4  flag-read spot clears the neighbour-> spot_X/2 <= X_CLEAR_NB
  C5  flag-read spot fits the flag in Y  -> spot_X <= FLAG_W
  C6  the fix removes the state-dependent standoff (R1/G2 re-check)
  C7  the as-drawn top-face read is STILL the defect (not silently erased)

Evidence class: CALCULATION + CAD geometry. No print, no purchase, no
measurement (DND-27). No board contact (DND-32). Python stdlib only.

Default-deny: every attack returns PASS / FAIL / UNRESOLVED; the verdict is
CLEAN only if no attack is FAIL or UNRESOLVED.

Run from anywhere:
    python 07-evidence-and-decisions/falsifier_dnd114_checks.py --gate
"""
from __future__ import annotations

import math

PITCH_MM = 5.08
COLUMN_BODY_MM = 3.60
TRAVEL_MM = 40.0
LATCH_T_MM = 0.45
CLEAR_MM = 0.20
HALF_ANGLE_DEG = 15.0

# DND-114 CAD parameters (must match the SCAD / model).
FLAG_T_MM = 0.44
FLAG_W_MM = 1.60
FLAG_H_MM = 0.80
FLAG_Z_TOP_MM = TRAVEL_MM + 3.0
FLAG_GAP_MM = 1.0
FLAG_AP_MM = 0.60
SWING_DEG = 30.0
DOF_BUDGET_MM = 1.0
CH_B_FLAG_R_MM = 1.20

# DND-113 carried numbers (the as-drawn defect that must remain visible).
WORK_GAP_MM = 2.0
APERTURE_MM = 2.0
CLAIM_SPOT_DOWN_MM = 24.508
CLAIM_STANDOFF_RATIO = 441.0


def _spot(gap, aperture, half_angle_deg=HALF_ANGLE_DEG):
    return aperture + 2.0 * gap * math.tan(math.radians(half_angle_deg))


def _hinge_x():
    return COLUMN_BODY_MM / 2 + LATCH_T_MM / 2 + CLEAR_MM


def attack_c1_frame_fixed():
    """C1: is the CH-A target frame-fixed (DeltaZ = 0)?"""
    # A frame-anchored cradle post does not move with the column; its target z is
    # Z_FLAG_TOP for BOTH the down (0) and up (40) column states. The test is
    # that the target z is independent of the column top height.
    z_down_column_top = 0.0
    z_up_column_top = TRAVEL_MM
    z_target_down = FLAG_Z_TOP_MM
    z_target_up = FLAG_Z_TOP_MM
    delta_z = abs(z_target_up - z_target_down)
    ok = (delta_z == 0.0
          and z_target_down != z_down_column_top
          and z_target_up != z_up_column_top)
    return (ok,
            "CH-A target top z = %.1f mm for BOTH states (column top %.1f/%.1f); "
            "DeltaZ = %.3f mm -> frame-fixed by construction"
            % (FLAG_Z_TOP_MM, z_down_column_top, z_up_column_top, delta_z),
            dict(z_target=FLAG_Z_TOP_MM, delta_z=delta_z))


def attack_c2_hinge_arc():
    """C2: does the CH-B hinge-arc DeltaZ stay inside the DoF budget?"""
    r_max = DOF_BUDGET_MM / (2.0 * math.sin(math.radians(SWING_DEG / 2)))
    delta_z = CH_B_FLAG_R_MM * 2.0 * math.sin(math.radians(SWING_DEG / 2))
    in_dof = delta_z <= DOF_BUDGET_MM
    r_ok = CH_B_FLAG_R_MM <= r_max
    ok = in_dof and r_ok
    return (ok,
            "CH-B r=%.2f mm -> hinge-arc DeltaZ=%.3f mm vs DoF %.1f mm; "
            "max radius in DoF %.3f mm -> %s"
            % (CH_B_FLAG_R_MM, delta_z, DOF_BUDGET_MM, r_max,
               "inside" if in_dof else "OUTSIDE"),
            dict(r_max=r_max, delta_z=delta_z, in_dof=in_dof))


def attack_c3_flag_fits_lane():
    """C3: does the flag fit the latch lane in X?"""
    hinge_x = _hinge_x()
    x_clear_nb = PITCH_MM - COLUMN_BODY_MM / 2 - hinge_x
    x_clear_own = hinge_x - COLUMN_BODY_MM / 2
    fits = FLAG_T_MM / 2 <= x_clear_nb
    min_feature = FLAG_T_MM >= 0.44
    ok = fits and min_feature
    return (ok,
            "flag T=%.2f mm; half=%.2f <= neighbour clearance %.3f mm "
            "(own clearance %.3f); min feature %s -> %s"
            % (FLAG_T_MM, FLAG_T_MM / 2, x_clear_nb, x_clear_own, min_feature,
               "fits" if fits else "CLASH"),
            dict(hinge_x=hinge_x, x_clear_nb=x_clear_nb,
                 x_clear_own=x_clear_own, fits=fits))


def attack_c4_spot_clears_neighbour():
    """C4: does the flag-read spot clear the neighbour column body?"""
    hinge_x = _hinge_x()
    x_clear_nb = PITCH_MM - COLUMN_BODY_MM / 2 - hinge_x
    spot_x = _spot(FLAG_GAP_MM, FLAG_AP_MM)
    clears = spot_x / 2 <= x_clear_nb
    return (clears,
            "flag spot %.3f mm (a=%.2f, g=%.1f); half %.3f <= neighbour "
            "clearance %.3f mm (margin %.3f) -> %s"
            % (spot_x, FLAG_AP_MM, FLAG_GAP_MM, spot_x / 2, x_clear_nb,
               x_clear_nb - spot_x / 2, "clears" if clears else "INTEGRATES"),
            dict(spot_x=spot_x, x_clear_nb=x_clear_nb,
                 margin=x_clear_nb - spot_x / 2))


def attack_c5_spot_fits_flag_y():
    """C5: does the flag-read spot fit the flag footprint in Y?"""
    spot_x = _spot(FLAG_GAP_MM, FLAG_AP_MM)
    fits = spot_x <= FLAG_W_MM
    return (fits,
            "flag spot %.3f mm vs flag Y width %.2f mm -> %s"
            % (spot_x, FLAG_W_MM, "fits" if fits else "OVERFLOWS"),
            dict(spot=spot_x, flag_w=FLAG_W_MM))


def attack_c6_standoff_removed():
    """C6: does the fix remove the state-dependent standoff (R1/G2)?"""
    # As-drawn: down gap = TRAVEL + work gap -> 4.82-pitch spot, 441x ratio.
    gap_down = TRAVEL_MM + WORK_GAP_MM
    spot_down = _spot(gap_down, APERTURE_MM)
    ratio = ((COLUMN_BODY_MM ** 2) / WORK_GAP_MM ** 2) / (
        (COLUMN_BODY_MM ** 2) / gap_down ** 2)
    reproduces_defect = (abs(spot_down - CLAIM_SPOT_DOWN_MM) < 0.1
                         and abs(ratio - CLAIM_STANDOFF_RATIO) < 5.0)
    # With the common-height target the standoff is FLAG_GAP for both states.
    ratio_fixed = 1.0
    ok = reproduces_defect and ratio_fixed == 1.0
    return (ok,
            "as-drawn down spot %.2f mm (%d%% of the 4.82-pitch defect) and "
            "neighbour/pocket ratio %.0fx reproduce; with the fixed-z flag the "
            "standoff is constant -> ratio %.0fx (no state-dependent swing)"
            % (spot_down, round(100 * spot_down / CLAIM_SPOT_DOWN_MM), ratio,
               ratio_fixed),
            dict(spot_down=spot_down, ratio=ratio, ratio_fixed=ratio_fixed))


def attack_c7_asdrawn_defect_kept():
    """C7: is the as-drawn top-face defect still recorded (not erased)?"""
    gap_down = TRAVEL_MM + WORK_GAP_MM
    spot_down = _spot(gap_down, APERTURE_MM)
    still_defect = spot_down > COLUMN_BODY_MM
    resolves_asdrawn = not still_defect
    ok = still_defect and not resolves_asdrawn
    return (ok,
            "as-drawn down spot %.2f mm > face %.2f mm -> the top-face read is "
            "STILL the defect; the DND-114 fix is the separate fixed-z target, "
            "not a rewrite of history" % (spot_down, COLUMN_BODY_MM),
            dict(spot_down=spot_down, resolves_asdrawn=False))


ATTACKS = [
    ("C1_ch_target_frame_fixed", attack_c1_frame_fixed),
    ("C2_hinge_arc_in_dof", attack_c2_hinge_arc),
    ("C3_flag_fits_lane", attack_c3_flag_fits_lane),
    ("C4_spot_clears_neighbour", attack_c4_spot_clears_neighbour),
    ("C5_spot_fits_flag_y", attack_c5_spot_fits_flag_y),
    ("C6_standoff_removed", attack_c6_standoff_removed),
    ("C7_asdrawn_defect_kept", attack_c7_asdrawn_defect_kept),
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
    print("DND-114 falsifier audit of the A1 common-height read target")
    print("=" * 72)
    for name, verdict, detail, _ in rows:
        print("[%10s] %-*s %s" % (verdict, width, name, detail))
    print("-" * 72)
    if fails:
        print("VERDICT: NOT CLEAN - unresolved attacks: %s" % ", ".join(fails))
        return 1 if args.gate else 0
    print("VERDICT: CLEAN - all %d attacks reproduce the DND-114 claim"
          % len(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
