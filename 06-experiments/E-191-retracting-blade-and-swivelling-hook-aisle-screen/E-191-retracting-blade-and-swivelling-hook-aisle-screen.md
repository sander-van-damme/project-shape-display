---
status: complete
builds-on: [E-190, E-125, E-124]
---

# A swivelling hook clears a straight aisle, but its shaft and handoff remain limiting

**Retain a rotating capture hook as a changed transport topology; no powered
head or machine passes.** A quarter-turn stores a rigid C hook lengthwise in the
same intercolumn aisle used by its shaft. This avoids both E-190's high-carriage
collision and the extra width required to translate the whole hook. The tested
sliding family has no passing central-bound section even before adding its
retaining slide. Rotation has finite rigid-body survivors, but little remaining
shaft clearance, large compliance sensitivity and an unresolved loaded handoff.
Do not resume the rejected shared-clearance-lift pair or request fabrication.

Input main `9ffae1f`. Reproduce with standard-library Python:

```
python3 tools/curated-experiment-checks/E-191/aisle.py
```

Evidence: generated primitive material, exact angular extrema, continuous
collision enclosures, deterministic parameter enumeration and analytical beam/
scheduling calculations; self-review only. No process distributions, sourced
material properties, measured loads, qualified actuators or reliability claims.

## What changed, and what the geometry actually contains

The new functional combination is **rotate the entire hook and its round support
shaft**, then scan only along y at fixed x. Each x column has its own setter.
E-190's two-gap contract was for a Manhattan route involving x crossover; it is
not necessary for this dedicated straight aisle. This is a changed capture/
transport combination, not a new retention principle or a novelty/saturation
claim. E-124/E-125's bilateral closing jaws remain a distinct rejected control.

At 5.08-mm pitch, the shaft axis is x=2.54. Each foot is f×2.8×1.2 mm on a
1.2-square stem. Two .5-mm-thick horizontal lips run from x=tip to 2.84, with
width b in y; a .6-mm web at x=[2.24,2.84] joins them. Relative to the foot
bottom, lower lip z=[−1,−.5], upper lip [1.7,2.2], web [−.5,1.7]. Rotate these
connected bodies 0→90° around the shaft axis; reverse to acquire. A round 90-mm
shaft connects to the underside of the lower lip. Its circumscribed square is
a conservative collision enclosure; its circular area/inertia enter mechanics.
The sliding comparator translates the same hook until its tip clears the foot.
It has no generated retained slide and receives no joint/power credit.

Exact extrema of every rotating vertex give conservative swept boxes over the
entire quarter-turn, including intermediate corner excursions. Compare each
body to the own foot/stem and all eight adjacent columns with independently
swept relative heights −40…40 mm. Once withdrawn, both hook and shaft fit wholly
between adjacent foot x envelopes; this proves the ideal straight route over
one, two or more rows at arbitrary relative heights. Adjacent-head swept x
envelopes also remain separated at independent angular/height states. It does not require a
neighbor's height to match the serviced column. Contact with the serviced foot
is not part of this free-flight sweep: acquisition/release occur with .5-mm
clearance above and below it.

Two nominal .8-mm-wall square sleeves surround the round shaft below the feet,
at z=−10 and −40, with .05-mm nominal radial gap. Their 3-mm outer width for a
1.3-mm shaft fits neighboring x stations. The shaft spans both sleeves through
h=−.5…40.5, reaching −91.5 mm at the low endpoint. This connects the hook to a
finite lower guide region, but **no axial drive, rotary transmission, sleeve
mount/frame or arrest is generated**. Sleeve fit is a nominal check, not a
manufacturing pass. Upper guides, surface caps and resident locks are outside
the generated assembly; their routing must still be integrated. The lower depth
already has a compactness cost before motors/frame are added.

## Bounded manufacturing and geometry results

Require separation/shoulder overlap exceeding `delta=4e+d+.025 mm`: opposing
centre/face bounds ±e, an additional relative point-pose bound d, and .025-mm
screening reserve. d must bound all relevant vertex excursions; it is not a
measured guide capability. Common rigid translation cancels; opposing size bias,
guide tilt and spatial warp may coherently consume the allowance across a bank.
No independent-cell distribution, yield or failure probability is inferred.

Enumerate f={2,2.2,…,3.4}, b={.6,.8,1}, shaft diameter={.8,1,1.3,1.6}, and
45 tip positions .7+.025k, discarding tips outside the nominal shoulder. This is
one parameter grid per topology, not thousands of invented mechanisms. Passing
counts certify only the specified conservative free-flight and overlap screen.

| e / d mm | delta mm | Sliding sections | Rotating sections |
|---|---:|---:|---:|
| .025 / .05 | .175 | 648 | 1,236 |
| .05 / .15 | .375 | 0 | 69 |
| .10 / .15 | .575 | 0 | 0 |

For the original 2-mm foot, the .4-mm shoulder cannot simultaneously provide
.375-mm stem clearance and .375-mm engagement: a rigid side hook needs shoulder
width at least 2delta. Enlarging the foot helps capture but narrows the aisle.
The .10 scenario also exceeds the chosen .5-mm vertical entry gap; its zero
count is not a universal rejection of larger-clearance hooks.

Central example with the thickest passing shaft: f=3, b=.6, diameter=1.3,
tip=1.025 mm. Residual margin beyond delta is **.015 mm** for the route and
**.100 mm** for overlap. A .8-mm shaft/f=3.2/tip=1.125 variant has .100-mm minimum
margin, at much lower bending stiffness. These are bare hook/shaft envelopes;
adding a slide, key, collar, wire or return element spends real space.

## Support, stiffness and time: why the envelope is insufficient

A C hook has **1 mm axial free play**, not a clamp. From its neutral orientation,
move +.5 mm for lower-lip contact or −.5 mm for upper-lip contact. During service,
load reversal may transfer between lips through that free play; unchanged
columns require independent ground stops. Prove capture before unloading a
stop, reseat/prove the stop before neutralizing and rotating away. Those are
obligations, not a generated successful state machine. E-125's false ground
proof and unlocked power-loss counterexamples still apply. This hook does not
supply resident retention, continuous arrest or output proof.

For the central 1.3-mm shaft, I=.1401985 mm⁴. Use E-124's explicitly assumed
.13405-N moving load, guide span 30 mm, maximum loaded overhang 50.5 mm and
1.2775-mm eccentricity to the nominal contact midpoint. With end moment M,
`u=M(L²/2+30L/3)/(EI)` gives the **free** shaft response:

| Modulus scenario N/mm² | Free tip response mm | Optimistic clamped Euler load N |
|---:|---:|---:|
| 500 | 4.34875 | .06782 |
| 2,000 | 1.08719 | .27129 |
| 100,000 | .02174 | 13.56439 |

These are scenario moduli, not PLA/metal allowables. Values above .5 mm exceed
the chosen small-displacement screen. All exceed the .015-mm residual route
margin, even before hook bending, guide play or torsion. This flags a coupled
contact/stiffness problem, **not actual loaded penetration or proof of a jam**:
column reactions change the free response. The Euler comparator assumes a
clamped overhang, optimistically neglecting lower-guide rotation; it is not a
stability rating. Modulus, orientation, creep, wear, roughness, contact and
assembly alignment remain uncalibrated. No stress or fatigue acceptance follows.

E-190's attained continuous worst-case direct bank schedule at two banks/160
vertical motors is 28.02153 s with two .05-s transfer slots per row, final y/z
return and a 6-s preparation/verification/retry allowance. Its **total available
transfer budget** is strictly below **.0747309 s per transfer**, if every other
assumption holds. A .5-mm rest-to-rest take-up at its unqualified motion limits
costs .020 s. A .020-s quarter-turn leaves <.034731 s for all remaining transfer
operations; a .050-s turn leaves <.004731 s. Extra unload motion, proof latency,
angular acceleration/settling or recovery cannot disappear inside a slot.

As a separate additive sensitivity, keep the original .05-s slots and charge
two additional turns per row: .020-s turns give 160 vertical motors/29.62153 s;
.050/.100-s turns require 240 motors/23.64388 and 26.34388 s. These numbers
exclude additional take-up if not paid by the original slots. They are schedule
bounds, not motor capability or finished-machine deadline passes.

## Portfolio decision and next discriminator

Rotation earns a component investigation because it changes the width tradeoff;
it does not earn a preferred architecture. A shared grounded rack turning
axially sliding keyed shafts could command a bank's hooks together, but requires
actual finite key, bearings, load/return path and observation. Private rotary
actuators would instead add 160–240 channels to the vertical drives. Both remain
unbuilt. The opposed pair needs separate capture timing and cannot inherit a
single common turning axis without a new schedule.

At 160 branches, $250 remaining after an assumed shared reserve allows <$1.5625
per complete bought branch; at 240, <$1.0417. This includes the shaft, two guides,
axial/rotary coupling, actuation, arrest and sensing. Even $.02 per resident
support costs another $128 across 6,400 cells. These are budget allocations,
not supplier prices. Printed .5/.6-mm lips/web, 90-mm shaft alignment, sleeve
assembly and accessibility need process qualification; no print mass/time or
lifetime is claimed. Regional motion retains untargeted ground stops only by
assumption, and common frame disturbance is unbounded.

Next, test a **short guided rotating head on a stationary aisle spine** against
this long moving shaft and the fixed-datum rotary control. The potential gain is
shortening the bending span while routing rotary/axial power below; the risk is
that real bearings/transmission consume the entire aisle. Stop at a finite
packing/load-path contradiction, or construct a supported take-up/release cycle
and priced-channel bound before deeper dynamics. Do not spend another iteration
optimizing the bare .015-mm margin. No purchase, print or approval dependency.

Self-review: exact arc extrema against 16/64/256/1,024-step rotated-vertex
holdouts (final difference 9.0e−8 mm), zero-angle limit, independently integrated
beam curvature with refinement, zero-force/inverse-modulus limits, finite sleeve
travel and connected lip/shaft projection. Collision passes are conservative
enclosures; enclosure failures alone are not finite intersection witnesses.
