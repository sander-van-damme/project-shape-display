---
status: complete
builds-on: [E-018]
---

# E-019: E-018 writer engagement and reader stack falsification

## Question and evidence boundary

Does the executable E-018 coupon CAD satisfy its own declared writer-port
engagement and frame-fixed reader geometry? This is a static CAD/coordinate
calculation only. No physical measurement, actuation, supplier fact, or
hardware-performance claim is made.

## Reproducible checks

Source: `06-experiments/E-018-four-plane-mask-generator-coupon-package/cad/four_plane_mask_coupon.scad`.

The repaired plane tab occupies, in Y,

```
plane tab:       -PLANE_Y/2 - PORT_T/2 +/- PORT_T/2 = [-18.0, -17.0] mm
writer tongue:   -PLANE_Y/2 - PORT_T/2 +/- PORT_T/2 = [-18.0, -17.0] mm
```

Therefore the tab and its matching writer tongue have **1.00 mm positive
overlap** in Y, matching the declared nominal insertion. This is a coordinate
repair; it does not claim a physical force/stroke margin.

The repaired stack uses `plane_z(3)` to place the upper plane
at centre z = 9.5 mm, with its 0.8 mm thickness ending at z = 9.9 mm.
`reader_target()` now places its 4 mm body from z = 11.9 to 15.9 mm, giving
2.00 mm clearance above the carrier. Its subtractive 3 x 3 x 0.4 mm window is
at the lower face, centred over the frame/plane centre aperture.

`analysis/coupon_protocol.py --check` now checks field span, web, fiducial
placement, writer overlap, reader clearance, case count, and required log
fields. OpenSCAD export completes with a pre-existing non-manifold warning;
export success remains supplementary to the coordinate assertions.

## Verdict and smallest corrective requirement

**Original gate failure repaired analytically.** The CAD now places each writer
tongue over its matching tab with 1.00 mm positive overlap, and places the
reader body 2.00 mm above the upper carrier with its 3 x 3 mm window at the
lower face over the centre aperture. The protocol check asserts both
relationships and passes. Preserve the four-plane boundary claim as
conditional: this static repair does not establish physical engagement,
reader discrimination, or architecture performance.

The corrective CAD/protocol revision is complete. Physical engagement,
non-interference under actuation, reader alignment margin, and reader
classification remain future tests before fabrication approval.

## Remaining bounded risks

After this geometry repair, parallel write yield, plane cross-talk, reseat
registration, reader classification margin, regional isolation, wear, and
the 20.18 s update calculation remain unresolved physical or assumption-bound
claims. The purchase screen remains an allowance, not a supplier commitment.
