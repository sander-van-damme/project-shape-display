---
status: complete
builds-on: [E-076, E-075]
---

# Retained routing dog fits a lateral section; withdrawal needs captive pullback

Retain a laterally translating dog with a row-local writer for further finite
contact synthesis. Reject spring-only pin return plus a drive-plate position
interlock as proof of safe shutter movement. A jammed pin can remain inside an
aperture while that plate returns. This is new geometric and pullback evidence,
not a complete selector, manufactured tolerance qualification or load rating.

Input main `9aaf86a`; reproduce with
`python3 tools/curated-experiment-checks/E-077/dog_route.py`.
Standard-library exhaustive rectangular-section corners, no random seed. Source
emits every survivor; output is reproducible and not retained. All dimensions
and error boxes below are assumptions in mm, not sourced X1C process priors.

## Finite cam-routing section

A command dog translates along x between centers 0 (bypass) and d (engaged).
A powered cam finger moves along y in a lane centered at x=d. Dog and finger
occupy the same z layer during work. In the engaged state their x sections
overlap, permitting a y-directed compression contact to an output follower;
in bypass the entire finger passes beside the dog. A separate guide carries
lateral reaction. The command pin acts from a lower z layer through a ramp;
it must be withdrawn before the cam approaches. A row reset comb pushes dogs
to bypass only while that row's cam is parked and its output load isolated.
The dog stores a command, not the column's height or service load.

Generate dog width b and cam width c in {0.6,0.8,1.0}, stroke d in
{1.2,1.5,1.8}; reserve 0.4 guide/frame width on each side of the 5.08 pitch.
Width errors and each independent x-center error lie in ±e. This includes
coherent strip shifts without assigning independent cell probabilities.
Exact worst-case margins are:

- Engaged overlap: `min(b-e,c-e,(b+c)/2-3e)`.
- Bypass clearance: `d-(b+c)/2-3e`.
- Remaining pitch after swept dog and guides: `5.08-d-b-3e-0.8`.

The swept dog union is an interval from its left bypass face to its right
engaged face; checking this union excludes same-layer adjacent dog collisions
for the bounded placement errors. This is a lateral section, not a claim that
ramps, springs, followers, guides and shutters fit together in three dimensions.
Cam y travel, parked clearance, z heights and output coupling are not synthesized.

At e=0.05/0.10/0.20, respectively 27/24/13 of 27 sections pass all three
strict inequalities. Counts describe selected parameter boxes, not yields.
Witness b=c=0.8, d=1.5, e=0.10 gives **0.50 mm engagement, 0.40 mm bypass,
1.68 mm packing reserve**. A dog between detents can still collide with the
cam; endpoints alone are insufficient to authorize cam motion. Retention force,
contact area/pressure, guide bending and edge wear are not inferred from overlap.

## Set/reset and withdrawal mechanism boundary

Retained sequence for each row: park cam and isolate output → reset dogs to
bypass → lower writer fully and unlock address strips → select shutters → lock
strips → raise selected command pins to set dogs → positively withdraw all pins
below both shutter layers → read dogs → enable cam only with valid endpoints.
A global reset of every dog during a local update is unnecessary; a row comb
can clear the changed row's command memory while independent column locks keep
unchanged heights. That requires the independent locks; this does not rehabilitate
A-022 or establish a complete lifting machine.

E-076's blocked pins require lost motion on the **push** stroke. Use captive
heads in individual drive-plate pockets so the return stroke pulls each pin,
including a previously blocked one. A key/blade tied to the plate can lock both
shutter actuators until the plate reaches its withdrawn position. An open spring
follower without captive heads fails: plate withdrawal and pin withdrawal are
independent in a jam. Readback of the plate cannot resolve that failure.

Let commanded tip withdrawal below the lowest shutter be R; bound return-pocket
lost motion L, elastic tip-to-plate displacement D, vertical registration Z,
and required remaining clearance C. Require `R-L-D-Z-C>0` before the mechanical
key releases. Illustrative R=1.0, L=0.15, D=0.15, Z=0.10, C=0.20 yields
**0.40 mm reserve**. D=0.60 gives **−0.05 mm**, so the same plate key can release
while a pin is still unsafe. These are bounds to be established by a finite
pullback load path, not measured stiffness or proof against a broken pin.
A hard jam must stall the return before key release; compliant, buckling or
fracturing paths invalidate that inference. Common plate flex is correlated
across the row and must be included in D, not divided by 80.

A cam preload must not remain on a dog during set/reset: sliding under that
load creates an unbounded friction/set-force demand and may release stored
energy during a shutter sweep. Parking the cam is a required mechanical phase,
not merely a software delay. Pin ramp angle, reset-comb travel, detent barrier,
key contact geometry and finite y/z collision sweeps remain the next gate.

## Return-force window: shared stiffness does not guarantee jam isolation

Continuation from main `cae1edf`; reproduce with
`python3 tools/curated-experiment-checks/E-077/return_load.py`.
A separate deterministic linear-elastic calculation tests the necessary force
window for the captive pullback. Assume a solid rectangular return beam,
10 mm wide × 4 mm deep, simply supported at spans 406.4/80/40/20 mm; an
8-mm-long axial pin neck with worst-case 0.7-mm square section; modulus
1,000/3,000 MPa and effective allowable stress 5/10/20 MPa. These are competing
**epistemic scenarios**, not sourced PLA properties or X1C distributions.
The allowable must ultimately include orientation, notch, creep and fatigue
reductions; it is not a tensile-test strength. Slots and captive-head bearing
can only weaken this idealized solid section.

Assume all 80 pins require 0.05 N each for normal return: total 4 N. A single
jammed pin may receive the entire common drive force. A force limiter must
therefore satisfy `4 N < F_limit < min(F_deflection,F_pin,F_beam)`; normal
friction and limiter variation cannot be averaged over pins. Use the jam at
midspan, with key position referenced to the supported drive datum. With
`I=b h³/12`, beam displacement is `F L³/(48 E I)`, axial pin elongation is
`F l/(E a²)`, and beam maximum stress is `3 F L/(2 b h²)`. These follow from
integrating the central-load bending moment and axial strain. Reserve 0.05 mm
for key/support displacement in addition to the earlier loss/error/clearance
allowances, leaving 0.50 mm for beam plus pin elasticity. Support locations
must follow the writer through its return stroke; stationary lateral guides
alone do not supply this vertical reaction.

| Support span | E (MPa) | Effective allowable (MPa) | Maximum limiter force (N) | Window above 4 N |
|---|---:|---:|---:|---|
| 406.4 mm | 1,000–3,000 | 5–20 | 0.019–0.057 | None |
| 80 mm | 1,000 | 5–20 | 2.311 | None |
| 80 mm | 3,000 | 10 | 4.900 | 0.900 N |
| 40 mm | 1,000 | 5 | 2.450 | None |
| 40 mm | 1,000 | 10 | 4.900 | 0.900 N |
| 40 mm | 1,000 | 20 | 9.800 | 5.800 N |

Reject the end-supported full-width **specified section**, even at the high
modulus bound: its allowed deflection is reached below the force needed to
return the row. This rejects that embodiment, not thicker/metal/segmented
return structures. The rejection uses the small 0.50-mm displacement threshold;
large post-failure deflections from linear theory are not physical predictions.
At 40-mm support spacing the pin neck, not beam stiffness, sets the displayed
upper limits. With 10-MPa effective allowable, a nominal 4.45-N limiter would
need its entire tolerance, dynamic overshoot and extra friction to fit within
±0.45 N. Doubling normal return drag to 0.10 N/pin eliminates that scenario's
window. Reducing supports to 20 mm does not improve its pin-strength limit.
At 5 MPa there is no 4-N window at any tested span. Segmented force limitation
could reduce the normal force lower bound, but introduces additional drive/key
interfaces; it is a changed mechanism requiring a new load-path accounting.

This is a necessary screen, not sufficient interlock qualification: beam shear,
torsion, pocket/head bending, support compliance beyond the reserved allowance,
key location, fracture and impact are unmodelled. Their added compliance reduces
the window; survivor numbers are optimistic limits. The local 40-mm witness is
retained only for finite geometry and contact analysis. No probability, yield
or jam-safe hardware claim follows. The common beam distortion is correlated
across the row and is never divided by 80.

Self-review independently integrates the unit-load bending energy at 20/40/80
midpoint elements (error falls fourfold each refinement), checks cubic span
and inverse-cubic depth scaling, and exercises both open/closed force windows
and the doubled-drag failure. Next geometry must include the **supported return
beam, head/neck and force-limited drive**, in addition to ramp, retention and key.
Do not progress a freely spanning thin return plate into CAD as a safe interlock.

## Comparison with seated magnetic memory and strip consequence

An E-075 inelastic seat is not equivalent to a positive obstruction. A single
lower seat prevents negative excursion but leaves the forward switching path
open; arbitrary-pulse isolation remains unproved. Adding two retractable
blocking bolts to a magnetic flag gives physical coincidence only if **either**
closed bolt arrests the flag before the detent saddle, including compliance.
That changes its architecture: it inherits two mechanical gate interfaces and
release/withdrawal ordering, while still buying magnets/coils/returns. Do not
credit that hybrid with A-016's parts advantage or assume a seat supplies the
second input. Retain a seat-only magnetic route only conditionally pending a
finite contact and field solution; this section cannot rank its dynamics.

One temporally reused 80×80 command array needs 6,400 retained dogs and 12,800
shutter aperture sites. A moving row-local writer can reuse 80 captive pins and
80 push-compliance pockets, but adds row indexing, registration and access;
fixed writers duplicate them to 6,400 each. Two fixed command arrays double
the repeated memory/gate inventory and nominal 160 shutter lines to 320.
The reset comb and cam parking are additional mechanisms in either case.
Temporal reuse stores only one mask: two independent command decisions require
two programming scans unless a complete sequence proves reuse of the same mask.

With S serial scans, average all-inclusive row service must be less than
`(30-T_other)/(80 S)` seconds. At T_other=0 this is 375 ms for S=1 or 187.5 ms
for S=2; real reset, readback, cam work, indexing, settling and recovery consume
that budget. No detection/retry rates or purchase prices are invented here.
At the absolute $500 ceiling, 6,400 bought dog-level assemblies alone would
have to average below $0.078125 each; two arrays below $0.0390625, even before
all shared equipment. Printed dogs do not incur that bought-parts allocation,
but pins, magnets, springs and fasteners do. These are budget ceilings, not
quotes or an affordability verdict. Assembly burden remains thousands of
retention/guide contacts even with a shared writer.

## Decision and evidence limits

Do not fabricate from this section. Keep the dog route as a bounded geometric
survivor, and stop spring-only withdrawal as a safety argument. Next complete
one finite ramp/detent/captive-return/key/parked-cam geometry with force and
collision bounds; reject it if that fails rather than repeatedly tuning widths.
Compare against one seated magnetic geometry and finish conditional cost/scan
accounting. The campaign remains incomplete; no full machine or repeated-pulse
hardware acceptance follows.

Self-checks independently enumerate all 16 width/registration corners for each
section, verify witness margins and both pullback cases. No field/contact solver,
physical measurement, force calibration, fatigue evidence or reliability rate
is claimed. The uncertainty boxes cover only the stated coordinates, not
unmodelled tilt, z interference, plate distortion or retention physics.
