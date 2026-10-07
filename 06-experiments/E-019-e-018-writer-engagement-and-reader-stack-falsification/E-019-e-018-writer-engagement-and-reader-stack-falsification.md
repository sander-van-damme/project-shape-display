---
status: active
---
---
status: active
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

The plane tab occupies, in Y,

```
plane tab:       -PLANE_Y/2 - PORT_T/2 +/- PORT_T/2 = [-17.9, -16.9] mm
writer tongue:   -FRAME_Y/2 - PORT_T/2 +/- PORT_T/2 = [-21.0, -20.0] mm
```

Therefore the tab and its matching writer tongue have a **3.0 mm air gap**;
their solids do not touch. The E-018 interface instead declares 1.00 mm
nominal insertion. This is a direct geometry contradiction, not tolerance
uncertainty. The four channels consequently cannot engage the four carriers
in the exported assembly, so the parallel-write and plane-isolation gates
cannot be exercised by this coupon as currently defined.

There is a second static stack conflict. `plane_z(3)` places the upper plane
at centre z = 9.5 mm, with its 0.8 mm thickness ending at z = 9.9 mm.
`reader_target()` places its 4 mm body from z = 9.8 to 13.8 mm, overlapping
the upper plane by 0.1 mm. Its subtractive 3 x 3 x 0.4 mm window is centred at
the reader body's local z = 0, i.e. world z = 11.8 mm, so it is not a window
at the top-plane surface. This makes the stated 2.00 mm reader standoff
ambiguous and, as modelled, mechanically intersecting rather than a verified
readout interface.

The existing checks pass because `analysis/coupon_protocol.py --check`
checks field span, web, fiducial placement, case count, and required log
fields; it does not check writer-to-tab overlap or reader-plane clearance.
OpenSCAD export also completes with a non-manifold warning, so export success
is not a substitute for these interface checks.

## Verdict and smallest corrective requirement

**Gate failure: reject E-018 as an executable writer/readout coupon until
geometry is repaired.** Preserve the four-plane boundary claim as conditional;
this finding does not falsify the architecture itself.

The smallest correction is to revise the CAD and protocol together so that
each writer tongue has a documented positive overlap/insertion with its tab
(at least the declared 1.00 mm, with a non-interfering parked state), and to
define a reader datum/surface with positive clearance from the upper carrier
and a window actually aligned to the selected aperture. Add deterministic
assertions for those conditions to the E-018 analytical check, then rerun the
CAD export and check before any physical coupon is fabricated.

## Remaining bounded risks

After this geometry repair, parallel write yield, plane cross-talk, reseat
registration, reader classification margin, regional isolation, wear, and
the 20.18 s update calculation remain unresolved physical or assumption-bound
claims. The purchase screen remains an allowance, not a supplier commitment.
