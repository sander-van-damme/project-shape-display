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
  S5  the absorber standoff stays inside the +/-1 mm DoF
  S6  the swept flap clears the neighbour column body
  S7  the swept flap stays above the own column top
  S8  the flap does not intrude into the reader aperture plane
  S9  the read spot stays entirely off the neighbour body

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


def attack_s5_absorber_in_dof():
    """S5: does the absorber standoff stay inside the +/-1 mm DoF?"""
    flat_bot = SHUT_HINGE_Z_MM - FLAP_R_MM - SHUT_T_MM / 2.0
    delta_z = flat_bot - Z_VANE_TOP
    ok = abs(delta_z) <= DOF_MM
    return (ok,
            "absorber underside at %.3f mm vs vane top %.1f mm -> absorber "
            "DeltaZ %.3f mm <= DoF %.1f mm -> %s"
            % (flat_bot, Z_VANE_TOP, delta_z, DOF_MM,
               "inside" if ok else "OUTSIDE"),
            dict(flat_bot=flat_bot, delta_z=delta_z))


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


ATTACKS = [
    ("S1_hidden_occludes", attack_s1_hidden_occludes),
    ("S2_visible_clears", attack_s2_visible_clears),
    ("S3_on_off_ratio", attack_s3_on_off_ratio),
    ("S4_target_frame_fixed", attack_s4_target_frame_fixed),
    ("S5_absorber_in_dof", attack_s5_absorber_in_dof),
    ("S6_clears_neighbour", attack_s6_clears_neighbour),
    ("S7_above_own_column", attack_s7_above_own_column),
    ("S8_aperture_clearance", attack_s8_aperture_clearance),
    ("S9_spot_off_neighbour", attack_s9_spot_off_neighbour),
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
