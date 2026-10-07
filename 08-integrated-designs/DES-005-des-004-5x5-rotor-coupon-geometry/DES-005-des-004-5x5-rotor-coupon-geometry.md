---
status: candidate
builds-on: [DES-004, Q-009, E-012]
---

# DES-005: DES-004 5x5 rotor coupon geometry

The executable coupon definition is retained with DES-004 because it is a
falsification article for that design:
`../DES-004-five-level-rotary-verified-successor/cad/des004_rotor_coupon_5x5.scad`.
The associated fit-gate report and script are in that design's `analysis/`
directory.

The E-012 geometry screen exposed and rejected one blocker: the original
1.70 mm pocket radius cleared the 3.00 mm rotor body but not the integral
coded vane (nominal outer corner radius 2.016 mm). The repaired candidate
uses a 2.20 mm pocket radius, leaving approximately 0.055 mm under the
documented worst-case vane/pocket tolerance stack and 0.70 mm nominal rotor
radial allowance. The 5.08 mm pitch still leaves a 0.68 mm nominal web
between adjacent enlarged pockets.

This is a CAD/tolerance-derived repair, not a physical fit result. The
candidate axle/bore worst-case diametral clearance remains 0.30 mm under the
E-012 assumed tolerance screen; actual process spread and pin tolerance are
unresolved. No production geometry or hardware-performance claim follows
until Q-009 physical measurements exist.
