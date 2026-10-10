---
status: complete
builds-on: [E-099, E-115, E-122]
---

# Direct pickup escapes tendon routing, but capture and lowering are separate gates

**Retain underside pickup and a shallow captured side shoe as conditional head
interfaces; do not admit a powered head or machine.** Generated side shoes can
acquire arbitrary old foot heights without touching neighboring columns under
the tighter translation/face-error scenarios. A continuous packing bound excludes
the declared compact side-shoe family at ±.10 mm. A common-datum rack pickup
escapes phase mismatch at discrete heights but crosses the tested closed guide.
The next discriminating work is finite guidance, power and controlled lowering,
including ground-lock transfer, rather than another tendon or nominal tooth sweep.

Input main `881f18f`. Reproduce:

```
python3 tools/curated-experiment-checks/E-123/acquisition.py
```

Evidence: generated box solids, exact axis-translation sweeps, deterministic
synthesis, analytical contact/packing bounds and self-review. No physical
measurements, sourced material allowables, process calibration, rigid-body solver,
qualified motors or sensors. All dimensions/errors/loads below are design
assumptions or explicitly bounded scenarios. Generated JSON is reproducible and
not retained. These are three pickup principles within travelling-head machines,
not three newly invented complete architectures.

## Geometry and state reach

Surface/column centers remain 5.08 mm apart. The selected column has a 4×2.8×1.2-mm
foot at z=h…h+1.2, a 1.6×1.2-mm stem extending to h+110, and h=0…40 mm.
Top caps, rack cavities, drive and assembled ground supports remain outside this
model. Fixed frame/lock bodies must stay above z=44.5 except the stem aperture;
that interface is an obligation, not an accepted guide. Indexed support positions
0/5/…/40 are provisional, not a new height-resolution requirement.

| Pickup | Selection/energy/load path | Distinct gate |
|---|---|---|
| Centered underside pad | Reusable private vertical coordinate; pad compresses foot; grounded lock supports inactive column | Cannot pull down against guide drag |
| Captured side shoe | Private vertical reach in inter-row aisle, common row-axis insertion, upper/lower lips around foot, web/spine to drive; separate ground-lock action still required | Tight aisle/shoulder fit and clearance-induced vertical play |
| Common-datum rack tab | Tab enters repeating rack pocket at fixed initial z, then private vertical travel; separate grounded lock | Following one pocket through 40 mm crosses the closed fixed guide |

The side shoe consists of two .8-mm-thick lips, a .6-mm web and a 50-mm spine.
Its slot gives .4 mm above and below the foot at entry. In y, engaged web spans
−2.25…−1.65 and lips reach −.9; the foot spans −1.4…1.4 and stem −.6… .6.
The head is 4 mm wide in x. Retracting **.965 mm** places its 1.35-mm-deep hull
centrally in the aisle at y=−2.54. The finite spine also remains in that aisle.
These bodies form one connected solid, not independent floating contact pads.

Transaction: all heads begin at reference H=−4, below every foot; index the row;
raise only active heads in the aisle to their old heights; insert using the
shared row axis; lift .4 to lower-lip contact, then .6 to unload ground support;
withdraw the ground lock; move to target+.6; insert ground lock; lower to target
and prove support; lower the shoe .4 to centered slot clearance; withdraw .965;
return below all feet before indexing. Inactive heads remain below the feet.
The ground-lock actuation, positive retention and proof are **not implemented**.
The .6-mm unload fits the conditional E-115 crossbolt section, not a qualified
assembly. A jam stops the transaction while the last verified support remains;
no sensor or recovery timing is inferred from this desired rule.

All 81 indexed old/target pairs have an ideal friction-free supported path.
Exact swept solids check continuous vertical acquisition, insertion and withdrawal,
all neighbor heights independently over 0…40, and simultaneous adjacent heads by
their separated x hulls. Returning to H=−4 permits arbitrary planar row travel
below the lowest foot. The maximum shoe height during unload is **43.4 mm**.
No common full-board lift or unchanged-column release is required by this route.
This is geometric isolation, not measured disturbance or a powered transaction.

## Manufactured geometry: bounded synthesis and finite failures

Each body has independent translation ±e per coordinate and each face has ±e
error. Thus opposing faces can close by **4e**. This deliberately permits coherent
adverse errors across a row/batch; common rigid translation cancels. No independent
cell probabilities or X1C accuracy are inferred. Rotations, guide play, column
bow/warp, layer quantization, roughness, creep/wear and load deflection are not
qualified by these face boxes and remain discrepancies for the next task.

Generate flange y width {2.4,2.8,3.2,3.6}, stem y {1.2,1.6,2}, overlap
{.3,.5,.7}, back gap {.15,.25,.45}, web {.6,.8} and vertical half-gap {.25,.4,.6}:
**648 variants per bound**, one topology. A .025-mm residual clearance/contact
reserve is a geometric screen, not a manufacturing or strength qualification.

| e mm | Admitted geometric sections / 648 |
|---:|---:|
| .025 | 180 |
| .05 | 81 |
| .10 | 0 |
| .20 | 0 |

Every admitted section also passes the generated swept-solid checks. The witness
above at e=.05 has aisle/web/stem clearance **.265/.050/.100 mm**, retained contact
overlap **.300 mm**, vertical insertion reserve .200 mm, and .900 mm below the
fixed-frame boundary after errors. Web clearance allows only .025 mm additional
relative drift while retaining the chosen reserve. Finite guides must establish
that envelope; ideal translational alignment cannot be inherited as hardware.

The zero count at .10 is not merely an optimizer/grid failure. Let d=4e, reserve r,
flange depth f, stem s, overlap o, back gap b and web w. Robust entry needs
`o,b ≥ d+r`, `f ≥ s+2o+2(d+r)` and
`pitch ≥ f+(o+b+w)+2(d+r)`. Eliminating f,o,b gives

`pitch ≥ s+w+8(d+r)`.

For s≥1.2,w≥.6,r=.025,e=.10 this requires **5.20 mm > 5.08 mm**. The corresponding
necessary e ceiling is **.09625 mm**, not a process capability or sufficient fit.
This excludes full-box coverage by the specified single-aisle compact shoe.
Larger/staggered internal pitch, thinner members, split jaws or changed contact
routes remain legal but require real full-density routing and load support.

A reconstructable .10-mm corner of the witness shifts the shoe +.1 in y, grows
its web front +.1, shifts the foot −.1 and grows its rear −.1. The remaining
.25-mm gap becomes **−.15 mm**, producing **.720 mm³** actual web/foot intersection.
This failure can repeat coherently across a bank; a common alignment offset
cannot repair opposing size errors. The centered underside pad instead clears
neighbors even at e=.20, with x/y margins .28/1.48 mm. Its force gate remains.

## Clearance is not continuous loaded capture

For a centered pad descending at acceleration a, upward guide drag D and moving
mass m, unilateral contact requires `N=m(g−a)−D ≥ 0`. A labelled m=.005 kg,
D=.060 N scenario fails even at zero downward acceleration: mg=.04905 N.
Static friction of that capacity can instead hold the column. This does not predict actual
PLA drag, but disproves an unconditional lowering claim from geometry alone.
Contact force, binding and miniature acceleration must be resolved together.

A C shoe adds a tensile direction but leaves **.8 mm nominal vertical play**;
face-size errors expand the slot-minus-foot difference to **1.0 mm at e=.05**.
Rigid body translation cancels from this play. If a descending column sticks,
the lower lip separates before the upper lip can pull it. If the restraint then
vanishes, the column can fall through the gap. A stationary-head, friction-free
1-mm fall reaches **.1401 m/s**; this is a conditional consequence, not observed
impact or a product rejection threshold. The interval constraint is
`H−gap ≤ h ≤ H+gap`; enclosure alone is not continuous contact. Positive take-up,
a changed gripping action or demonstrated controlled contact with output readback
must resolve this behavior before machine admission.

The side contact is also eccentric: nominal load line is 1.15 mm behind the
stem. At an assumed 10-N head force and 30-mm guide spacing, the balancing guide
couple requires **.3833 N at each station**, before other loads/clearance effects.
A finite moment-reacting guide, web/lip strength and spine drive are missing.
No generic PLA allowable, tiny printed wall or prescribed actuator coordinate is
credited as a solution. Lower forces remain competing scenarios, not evidence
that higher service loads have been qualified.

## Rack alternative and architectural consequences

A 5-mm-period rack with 3-mm-high pockets and .8-mm tab admits a 2.2-mm nominal
phase window, 1.8 mm after the e=.05 face/translation bounds. All indexed heights
can share one acquisition phase: arbitrary continuously varying phase must not
be used to reject this discrete design. At a common datum z=43, pockets centered
at material z=3+5k cover all nine old heights without cutting the foot.

But an old=0→40 move carries the tab to z=83. The fixed guide rear wall
x=±1.7, y=−1.7…−.9, z=44.5…45.5 intersects a .8×1.8×.8-mm pickup tab centered
at z=45 by **.512 mm³**. More generally, acquisition above the highest foot needs
z≥41.2, while a +40 move staying below that wall needs z≤4.1. A slit/open guide,
variable-height pickup or disengage/regrip route can escape; each changes the
load/guide/sequence, and none is implemented or rejected here. Do not optimize
rack phase against an unresolved fixed-body crossing.

For the E-099 four-bank comparison, 320 reusable shoes replace 6,400 local loops;
6,400 feet/stems and ground supports remain. The generated shoe boxes total
72 mm³ each (23.04 cm³ for 320), **not** whole-head print volume. Their thin
50-mm spines, linear guides, drive/reader/wiring and independent lock setting
are unqualified. The stem/foot and home geometry span z=−54…150 (204 mm) before
actuator packaging. Twenty rows per bank require 38.6 mm total side insertion/
withdrawal per full update, in addition to vertical acquisition and row travel.
Allocate those motions within, or in excess of, E-099's engagement slots explicitly;
do not silently inherit its 18.854-s timing. With a $250 elsewhere reserve the
<$500 ceiling still allows **<$0.78125 per complete reusable head** and no free
bought cell parts. This is a budget allowance, not a price or economic rejection.

**Continue:** task 2 must construct guidance and powered support transfer, compare
positive closeable capture against the pad/C-shoe limits, and implement ground
lock set/return plus output proof. Retain the .10 packing witness; a tighter
error box alone is not an admission. No print is justified while these missing
mechanisms can decide the architecture computationally. Cost/timing task 3 stays
dependent. No complete feasible Pareto winner or reliability estimate is selected.

Self-review: exact box limiting cases; continuous parameter-elimination bound
checked by independently constructing equality dimensions; finite deformed-solid
and fixed-guide witnesses; 16/64/256-step nominal insertion/contact holdouts;
81 supported transactions under the stated friction-free grants; potential/kinetic
energy check; all admitted candidates' exact sweeps. Sampled holdouts complement,
not replace, the axis-aligned swept-volume proof. No independent reviewer or
physical validation is claimed.
