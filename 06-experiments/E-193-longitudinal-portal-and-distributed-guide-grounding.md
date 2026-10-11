---
status: complete
builds-on: [E-192, E-185, E-131]
---

# Distributed top guidance escapes the crossing, but running play remains decisive

**Retain the offset-post routing result; stop detailing the tested unpreloaded
aisle guide.** A longitudinal guide supported between rows can avoid stems and
the travelling head. It is not geometrically excluded by E-192's transverse-bar
witness. The inherited moving ground block does collide, and must change.
At the constructed .15-mm radial guide gap, none of E-192's 18 central sections
stays within its route margin in the sampled elastic model. No complete machine
or hardware performance is established; fixed-datum transmission remains a
different, costly control rather than an automatic fallback.

Input main `71e1e36`. Reproduce with standard-library Python:

```
python3 tools/curated-experiment-checks/E-193/portal.py
```

Evidence: finite solid envelopes, annular material clipping, continuous rigid
sweep bounds and analytical elastic contact with deterministic scenarios.
Self-review only; no calibrated process data, structural CAD/contact validation,
physical measurement, purchased BOM or independent review.

## Changed ground topology and actual crossings

Retain 5.08-mm pitch, 2.8-mm feet, 40-mm travel and E-192's swivel/stacked sleeve.
The inherited 18 sections use its central external bound `.375=4*.05+.15+.025`
mm. Only two have .4-mm walls; the others have experimental .2-mm walls.

Three arrangements distinguish the ground path:

- **Edge portal:** two longitudinal .4×4-mm guide cheeks at z=54…58 mm,
  supported outside the array. No bar crosses a stem lane. The long weak-axis
  span is 411.48 mm in the elastic comparison.
- **Posts directly in the head aisle:** a .4-mm-square post on the rail route
  intersects the moving rail by **10.24 mm³**. Shifting it into the sleeve wall
  also produces positive annular-material intersection, not merely a hollow-box
  overlap. A stationary post in the passage is not a distributed support solution.
- **Offset distributed posts:** 2.4×1-mm posts are centered on column x positions
  and halfway between successive rows, extending z=−14…58. Bridges at z=58…60
  reach sideways to the longitudinal cheeks. Posts avoid feet because they occupy
  row gaps; bridges pass above the moving head and below the lowest cap. The
  extended vertical rail tip enters the open channel between the cheeks at z=57.
  Its nominal radial gap is .15 mm. These are finite members and connected face
  interfaces, not ideal support points placed through the columns.

The old 3-mm-wide moving ground block intersects each adjacent offset post by
**.64 mm³** at a crossing. Narrowing that block to **1.6 mm** gives a geometric
escape, conditional on an unproved clamp and lower-carriage load path. Do not
silently inherit the old block's fixity after this change.

Generated repeated neighborhoods enclose every independent foot position
z=0…41.2, stem position z=1.2…121.2 and a 5-mm-square cap swept through
z=81.2…123.2. The new frame's external reserve is **.265 mm** to columns,
**.165 mm** to the withdrawn head's continuous two-row route and **.11568 mm**
to its exact quarter-turn envelope, after the .375-mm bound. Both the .4- and
.7-mm rail representatives pass this selected-component route check. Translation
repeats the interior motif; exterior terminations must stay outside these sweeps.
Intentional guide/rail clearance is evaluated separately, not charged the external
reserve. Bonded face joins and point bearing restraint remain assumptions.

This escapes a specific crossing failure, not every assembly interaction. Motor,
reader, antirotation, clamp drive, longitudinal bottom carriage and module-joint
geometry are absent. The original cord wheels and brackets are retained in the
route envelopes. Bridges sit 6 mm above their highest bracket, leaving a real
vertical separation. Caps do not receive free holes.

## Clearance and compliance are coupled

The vertical rail is favorably clamped at z=−10; its upper guide's equivalent
lateral contact is at z=56, so `L=66 mm`. A sleeve at `a=h+10`, with
`h=−.5…40.5`, applies the E-192 eccentric couple `M=F*eccentricity`, with
`F=.13405 N`. This is an assumed motion load, not a service-load requirement.
Let `EI=Ecore*pi*d^4/64`, upper radial play `g`, and frame compliance `C` in mm/N.
The signed guide reaction and rail response follow directly from superposition:

```
v_free_top = M*a*(2L-a)/(2EI)
R = -max(0, v_free_top-g)/(L^3/(3EI)+C)
u(a) = M*a^2/(2EI) + R*a^2*(3L-a)/(6EI)
theta(a) = M*a/EI + R*a*(2L-a)/(2EI)
```

The unilateral contact satisfies nonpenetration and complementarity. Compare
`abs(u)+3.1*abs(theta)` with the section's route reserve, including sleeve-end
rotation. This is the free response of a rail/sleeve with a point couple and
lateral guide. It does **not** predict loaded penetration into a neighboring
column: contact, changed force distribution and guide friction would change it.

For the portal use one loaded cheek's `I=4*.4^3/12`, not a fictitious composite
wide section. A central point load on a simply supported span contributes
`span^3/(48 Eframe I)`. Two perfectly rooted posts share the reaction; their
68-mm cantilevers add `68^3/(6 Eframe Ipost)`, with `Ipost=1*2.4^3/12`.
A favorable axial bridge term is included; joints, contact indentation and
other bridge modes are omitted. Distributed support uses one 5.08-mm span;
real beam continuity/load spreading can change the result in either direction.

At `Eframe=2000 MPa`, compliance is **34,041.33 mm/N** for the edge portal and
**22.8098 mm/N** for the distributed surrogate. Ideally clamping both edge-beam
ends instead reduces its beam term fourfold, still leaving a very compliant
path. These are reference structural models, not rigorous manufactured bounds.

At `Ecore=100000 MPa`, `Eframe=2000 MPa`, sampled over all 18 sections:

| Top path | g mm | Sections below route reserve | Best response / reserve |
|---|---:|---:|---:|
| Perfectly rigid support | 0 | 10 | .2111 |
| Perfectly rigid support | .05 | 8 | .4339 |
| Perfectly rigid support | .15 | 0 | 1.3017 |
| Edge portal | 0 | 0 | 3.3236 |
| Edge portal | .15 | 0 | 3.3276 |
| Distributed surrogate | 0 | 8 | .6186 |
| Distributed surrogate | .05 | 0 | 1.0691 |
| Distributed surrogate | .15 | 0 | 1.9351 |

Every section below the reserve in this table has an experimental .2-mm wall.
The .4-mm-wall control retains only .015-mm route margin; with ideal zero-gap
support its best envelope is **.12869 mm**, including .10094-mm center movement
in the opposite direction to the original cantilever. Support changes the
deformation shape; increasing stiffness does not monotonically reduce every
point's absolute displacement. Ideal support is therefore a sensitivity control,
not a proof that every intermediate stiffness must be worse.

At g=.15 the distributed best ratio is **10.3106 / 1.9351 / 1.6258** for
`Ecore=2000 / 100000 / 200000 MPa`, respectively, at Eframe=2000. Raising Eframe
to 100000 gives best ratio **1.3070** at Ecore=100000; no sampled section passes.
The selected .7-mm rail's distributed response grows from .12578 to **.39290 mm**
when F changes from .13405 to 1 N. Because contact engages after finite play,
force response is piecewise linear, not globally proportional.

## Uncertainty, complete-machine comparison and disposition

All E, F, gap, pose and dimensional values are **labelled bounds/scenarios**,
not material allowables or X1C priors. The constructed .15-mm gap is only .025 mm
above the inherited `2e+.025` bore-fit threshold at e=.05. Zero/.05-mm effective
play would require a changed preload/contact mechanism or tighter qualified
errors; they cannot be claimed for that same free-running fit. The .3-mm case
tests additional play. Coherent warp, guide offset, hole/shrink bias and module
misalignment can affect a whole bank; no independent-cell random averaging is
used. Layer texture, anisotropy, creep, wear and guide stiction remain unbounded.
The model ignores pulley compression, axial buckling, actual sleeve contact and
finite bearing length. Large low-modulus responses are warnings outside a
validated small-deflection regime. No yield or lifetime prediction follows.

| Architecture | What this changes | Full-machine obligations retained |
|---|---|---|
| Swivel head + edge portal | A collision-free nominal upper route, weak long beam | E-192's 240 vertical branches under additive timing, rotation command, input arrest, resident stops and proof; portal is not a vertical lock |
| Swivel head + distributed guide | Short guide spans via offset posts, narrowed moving block | **6,480 posts/bridges**, 160 cheek runs (~65.84 m), existing 6,400 stops, 240 sleeve/loop heads and at least 480 loop wheels; no channel or timing saving |
| Fixed-datum resident screw | Motion stays at each cell; reusable rotary input docks at one plane; no tall travelling capture | 6,400 screw/nut/thrust/antirotation paths; E-131 friction/lead and E-185 coast, speed, motor and docking limits remain |

The distributed posts alone contain **1.119744 L** in the literal solid geometry;
one ten-second post assembly operation totals **18 h**. These are not print-time
or scrap estimates; integral modular printing changes assembly but needs joints
and print orientation. Both 411.48-mm portal spans and full guide runs exceed
the recorded 256-mm build volume. No sourced hardware purchase is proposed.

E-192's additive timing still needs three banks / 240 vertical drives, with
rotation, handoff, reset, verification and one bounded retry charged as there.
The illustrative $250 shared reserve leaves <$1.0417 per whole branch at $500;
adding stationary support cannot improve that allocation. E-185's different
motor-limited schedule has 82 direct-return and 131 resident-screw heads at its
base load. Do not interchange those head counts with the bank schedule or claim
that a nominal fixed-datum route qualifies threads, docking or arrest.

Source loss still requires head arrest while the resident stop is open. A lateral
portal supplies no axial retention, and E-192's .5-mm take-up gap remains. A failed
support proof keeps capture and stops the bank. Resident screw retention remains
friction/lead dependent, with moving-loss behavior distinct from static hold.
Unchanged cells keep their resident supports; shared-post motion can disturb
neighbors. The elastic calculation loads one head, not all three banks or a jam,
and is not a regional-disturbance qualification. No perfect readback is assumed.

**Decision:** retain the offset-post topology and the ground-block collision;
stop further size tuning of this unpreloaded slender-guide construction. Reopen
only with an explicit contact/preload route, materially different cross-section
or a load path escaping the same foot corridor and accounting for its channels.
Do not fabricate, select a machine or reinstate a rejected resident screw solely
because it avoids this carriage. After three narrow capture investigations,
the more useful next comparison removes travelling capture: fixed-datum rotary
versus permanent tensile/strip coupling, reconstructing E-120–E-122/E-156 first.
Require real routing, signed motion, local isolation, source-loss support and
full-board inventory; stop a candidate that merely relocates the missing dock
or arrest. This changes the search axis, not the product requirements.

Self-review checks exact solid overlap, continuous envelope separation, guide
complementarity, independent curvature integration, unit-load beam energy,
zero force, recovered cantilever limit and inverse-modulus limit. The 1,025
height samples per scenario are a finite screen, not a proof of all intersample
extrema. An interior maximum is checked at 65/257/1,025/4,097 samples; retain the
source and discard generated JSON. No independent challenge is claimed.
