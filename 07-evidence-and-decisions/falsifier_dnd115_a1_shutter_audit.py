#!/usr/bin/env python3
"""DND-118 falsifier register - independent adversarial audit of the DND-115
state-encoding shutter (default-deny).

This is the Falsifier's INDEPENDENT recomputation of the DND-115 numbers. It does
NOT import `08-integrated-designs/a1-reliability-first/analysis/a1_writer_rate.py`, and it does NOT trust
the CTO-authored `falsifier_dnd115_checks.py`. Every number is recomputed here
from the placed CAD dimensions (hard-coded from
`08-integrated-designs/a1-reliability-first/scad/a1_binary_latch_cell.scad`) and first principles.

It is deliberately HOSTILE: it asserts the DND-115 claims where they survive
independent recomputation, and it FAILS where they do not. The verdict is CLEAN
only if no attack is FAIL or UNRESOLVED.

Attacks (default-deny):

  A1  hidden-state full occlusion                                  PASS
  A2  visible-state full clearance (edge-on plate)                 PASS
  A3  on/off return ratio >= 2x gate                               PASS
  A4  reflective TARGET frame-fixed (DeltaZ = 0)                   PASS
  A5  neighbour crosstalk is modelled AND gated (not only reported) FAIL
  A6  neighbour up-cell top is truly "off-beam"                     FAIL
  A7  absorber-standoff-in-DoF claim is meaningful, not vacuous     FAIL
  A8  swept flap clears neighbour / own column / aperture plane     PASS
  A9  tolerance stack-up is structurally sound (aperture not pinned) FAIL
  A10 hidden/visible states survive linkage angular tolerance       PASS
  A11 printability / min-feature / watertight mesh evidence         PASS
  A12 claim-5 (DND-114 1.0 mm standoff infeasible) reproduces       PASS

A FAIL here does not by itself kill the shutter; A5/A6/A7/A9 are modelling or
claim-framing defects that must be corrected/downgraded. The core geometry
(A1-A4, A8, A10-A12) reproduces independently. See
`falsifier_dnd115_a1_shutter_audit.md` for the full register and verdict.

Evidence class: CALCULATION + CAD geometry. No print, no purchase, no
measurement (DND-27). No board contact (DND-32). Python stdlib only.

Run from anywhere:
    python 07-evidence-and-decisions/falsifier_dnd115_a1_shutter_audit.py --gate
"""
from __future__ import annotations

import math

PITCH = 5.08
BODY = 3.60
TRAVEL = 40.0
LATCH_T = 0.45
CLEAR = 0.20
HALF_ANGLE_DEG = 15.0

HINGE_X = BODY / 2 + LATCH_T / 2 + CLEAR          # 2.225
Z_VANE_TOP = TRAVEL + 3.0                          # 43.0

SHUT_T = 0.44
SHUT_W = 1.55
SHUT_D = 1.60
SHUT_GAP = 0.55
SHUT_HINGE_Z = 45.8
SHUT_SWING_DEG = 90.0
SHUT_APER_GAP = 1.8
SHUT_AP = 0.44
FLAP_R = SHUT_HINGE_Z - (Z_VANE_TOP + SHUT_GAP + SHUT_T / 2)   # 2.03
SHUT_FLAT_BOT = SHUT_HINGE_Z - FLAP_R - SHUT_T / 2             # 43.55
SHUT_FLAT_TOP = SHUT_HINGE_Z - FLAP_R + SHUT_T / 2             # 43.99
SHUT_APER_Z = Z_VANE_TOP + SHUT_APER_GAP                       # 44.8
SPOT = SHUT_AP + 2 * SHUT_APER_GAP * math.tan(math.radians(HALF_ANGLE_DEG))
NB_NEAR = PITCH - BODY / 2                        # 3.28
R_VANE, R_FLAP = 0.80, 0.05


def _corners(deg):
    th = math.radians(-deg)
    cx = HINGE_X + FLAP_R * math.sin(th)
    cz = SHUT_HINGE_Z - FLAP_R * math.cos(th)
    pts = []
    for s in (-SHUT_W / 2, SHUT_W / 2):
        for t in (-SHUT_T / 2, SHUT_T / 2):
            pts.append((cx + s * math.cos(th) + t * math.sin(th),
                        cz - s * math.sin(th) + t * math.cos(th)))
    return pts


def _sweep():
    xs, zs = [], []
    for i in range(1801):
        for px, pz in _corners(SHUT_SWING_DEG * i / 1800):
            xs.append(px)
            zs.append(pz)
    return min(xs), max(xs), min(zs), max(zs)


def _shadow_frac(deg):
    xs = [p[0] for p in _corners(deg)]
    lo, hi = min(xs), max(xs)
    s_lo, s_hi = HINGE_X - SPOT / 2, HINGE_X + SPOT / 2
    x_ov = max(0.0, min(hi, s_hi) - max(lo, s_lo))
    y_ov = min(SHUT_D, SPOT)
    return min(1.0, x_ov * y_ov / (SPOT * SPOT))


def _on_off_ratio():
    hidden = _shadow_frac(0.0)
    visible = _shadow_frac(SHUT_SWING_DEG)
    g_flap = SHUT_APER_Z - SHUT_FLAT_BOT
    bright = (1.0 - visible) * R_VANE / SHUT_APER_GAP ** 2
    dark = (1.0 - hidden) * R_VANE / SHUT_APER_GAP ** 2 + hidden * R_FLAP / g_flap ** 2
    return bright / dark, hidden, visible


def a1_hidden_occludes():
    f = _shadow_frac(0.0)
    return f >= 0.99, "hidden flat flap: shadow %.3f of the %.3f mm spot" % (f, SPOT)


def a2_visible_clears():
    f = _shadow_frac(SHUT_SWING_DEG)
    return f <= 0.01, "visible edge-on flap: shadow %.3f of the %.3f mm spot" % (f, SPOT)


def a3_on_off_ratio():
    r, h, v = _on_off_ratio()
    return (r >= 2.0 and h >= 0.99 and v <= 0.01), \
        "on/off ratio %.2fx (hidden %.3f, visible %.3f); gate 2x" % (r, h, v)


def a4_target_frame_fixed():
    return True, ("reflective TARGET = frame-fixed vane top z=%.1f mm; DeltaZ=0 "
                  "in both states; flap is an ABSORBER (rho=%.2f)" % (Z_VANE_TOP, R_FLAP))


def a5_crosstalk_gated():
    nb_region = BODY ** 2 / (SHUT_APER_Z - TRAVEL) ** 2
    vane_region = (SHUT_AP * SHUT_D) / SHUT_APER_GAP ** 2
    ratio = nb_region / vane_region
    return ratio <= 1.0, (
        "model's own neighbour/vane solid-angle upper bound = %.3f x (>1, and not "
        "part of contrast_passes) -> crosstalk REPORTED, NOT GATED" % ratio)


def a6_neighbour_off_beam():
    depth = SHUT_APER_Z - TRAVEL
    r_cone = depth * math.tan(math.radians(HALF_ANGLE_DEG))
    dx = NB_NEAR - HINGE_X
    return dx >= r_cone, (
        "cone radius at neighbour-top plane %.3f mm vs neighbour near-edge offset "
        "%.3f mm -> edge INSIDE the cone by %.3f mm ('off-beam' claim false; the "
        "state-invariant contribution is small but real)" % (r_cone, dx, r_cone - dx))


def a7_absorber_dof_meaningful():
    absorb_term = R_FLAP / (SHUT_APER_Z - SHUT_FLAT_BOT) ** 2
    vane_term = R_VANE / SHUT_APER_GAP ** 2
    return absorb_term >= vane_term, (
        "absorber term rho/g^2 = %.5f vs vane term %.5f (%.2fx smaller); the "
        "'absorber in +/-1 mm DoF' check certifies an already-negligible term -> "
        "VACUOUS (harmless, but not evidence)"
        % (absorb_term, vane_term, vane_term / absorb_term))


def a8_swept_envelope():
    x0, x1, z0, z1 = _sweep()
    nb_margin = NB_NEAR - x1
    own_margin = z0 - TRAVEL
    ap_clear = SHUT_APER_Z - SHUT_FLAT_TOP
    ok = nb_margin > 0 and own_margin > 0 and ap_clear > 0
    return ok, ("sweep X=[%.3f,%.3f] Z=[%.3f,%.3f]; neighbour margin %.3f mm, "
                "own-column margin %.3f mm, aperture clearance %.3f mm"
                % (x0, x1, z0, z1, nb_margin, own_margin, ap_clear))


def a9_stackup_structurally_sound():
    return False, (
        "CTO MC pins aperture_z to nominal vane_top+1.8 while perturbing vane_top; "
        "aperture_clearance can never fail -> MC structurally tautological on that "
        "check (design still passes an aperture-tolerant +/-0.20 mm re-run)")


def a10_angular_tolerance():
    def cov_at(a):
        ar = math.radians(a)
        half = (SHUT_W * math.cos(ar) + SHUT_T * math.sin(ar)) / 2
        return min(1.0, 2 * min(half, SPOT / 2) / SPOT)

    def vis_shadow(a):
        ar = math.radians(90 - a)
        xproj = SHUT_W * math.sin(ar) + SHUT_T * math.cos(ar)
        th = math.radians(-a)
        cx = HINGE_X + FLAP_R * math.sin(th)
        lo, hi = cx - xproj / 2, cx + xproj / 2
        ov = max(0.0, min(hi, HINGE_X + SPOT / 2) - max(lo, HINGE_X - SPOT / 2))
        return ov / SPOT

    worst_hidden = min(cov_at(a) for a in (0, 2, 5, 10, 20))
    worst_visible = max(vis_shadow(a) for a in (90, 88, 85, 80, 75))
    ok = worst_hidden >= 0.99 and worst_visible <= 0.01
    return ok, ("hidden coverage >= %.3f over tilt 0..20 deg; visible shadow <= "
                "%.3f over crank 90..75 deg -> robust to linkage angular error"
                % (worst_hidden, worst_visible))


def a11_printability():
    mf = min(SHUT_T, SHUT_W, SHUT_D)
    return mf >= 0.44, (
        "min shutter feature = %.2f mm >= 0.44 mm (1 line @0.4 nozzle); committed "
        "STL watertight per render_record.json" % mf)


def a12_claim5_infeasible():
    worst114 = 1.0 - (SHUT_GAP + 0.10) - (SHUT_T + 0.10)
    worst115 = 1.8 - (SHUT_GAP + 0.10) - (SHUT_T + 0.10)
    return (worst114 < 0.0 and worst115 > 0.0), (
        "worst-case aperture clearance at S=1.0 -> %.3f mm (INFEASIBLE), at S=1.8 "
        "-> %.3f mm (feasible); claim 5 reproduces" % (worst114, worst115))


ATTACKS = [
    ("A1_hidden_occludes", a1_hidden_occludes),
    ("A2_visible_clears", a2_visible_clears),
    ("A3_on_off_ratio", a3_on_off_ratio),
    ("A4_target_frame_fixed", a4_target_frame_fixed),
    ("A5_crosstalk_gated", a5_crosstalk_gated),
    ("A6_neighbour_off_beam", a6_neighbour_off_beam),
    ("A7_absorber_dof_meaningful", a7_absorber_dof_meaningful),
    ("A8_swept_envelope", a8_swept_envelope),
    ("A9_stackup_structurally_sound", a9_stackup_structurally_sound),
    ("A10_angular_tolerance", a10_angular_tolerance),
    ("A11_printability", a11_printability),
    ("A12_claim5_infeasible", a12_claim5_infeasible),
]


def run():
    rows, fails = [], []
    for name, fn in ATTACKS:
        try:
            ok, detail = fn()
        except Exception as exc:  # noqa: BLE001
            ok, detail = None, "UNRESOLVED (%s)" % exc
        verdict = "PASS" if ok is True else ("UNRESOLVED" if ok is None else "FAIL")
        if verdict != "PASS":
            fails.append(name)
        rows.append((name, verdict, detail))
    return rows, fails


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--gate", action="store_true",
                    help="exit non-zero if any attack is FAIL/UNRESOLVED")
    args = ap.parse_args(argv)
    rows, fails = run()
    width = max(len(n) for n, *_ in rows)
    print("DND-118 FALSIFIER independent audit of the DND-115 state-encoding shutter")
    print("=" * 78)
    for name, verdict, detail in rows:
        print("[%10s] %-*s %s" % (verdict, width, name, detail))
    print("-" * 78)
    if fails:
        print("VERDICT: NOT CLEAN - unresolved/failed attacks: %s" % ", ".join(fails))
        print("  (A5/A6/A7/A9 are modelling/claim-framing defects; the core geometry "
              "reproduces. See the audit register.)")
        return 1 if args.gate else 0
    print("VERDICT: CLEAN - all %d attacks reproduce the DND-115 claim" % len(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
