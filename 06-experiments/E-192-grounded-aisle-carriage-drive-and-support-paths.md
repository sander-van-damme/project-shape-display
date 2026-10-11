---
status: complete
builds-on: [E-191, E-190, E-185]
---

# A short aisle carriage still needs a narrow grounded structure

**Stop the generated retained slide and nested sleeve; do not promote the stacked
sleeve to a machine.** Finite material intersects neighboring feet, including at
nominal dimensions for the nested sleeve. Axially stacking the thrust interface
saves radial width, but the central-bound geometric survivors require thin ground
rails; all but two use experimental 0.2-mm walls. A short carriage does not itself shorten the
rail's bending span. Retain this changed load-path result, not another bare-hook
optimization or a fabrication request.

Input main `633292b` (includes E-191 after this task's original `9ffae1f` input).
Reproduce with standard-library Python:

```
python3 tools/curated-experiment-checks/E-192/grounded.py
```

Evidence: generated polygon/box geometry, exact planar clipping of finite solids,
conservative continuous sweep enclosures, bounded enumeration, analytical elastic
and scheduling calculations; self-review only. No measurements, process priors,
material allowables, motor qualification, reliability or independent review.

## Material, grounding and counterexamples

All variants use 5.08-mm pitch, a 1.2-mm-square stem and a foot 2.8 mm deep and
1.2 mm thick. Foot width varies. A 40-mm vertical stroke is required. The hook
lips are 0.5 mm thick and 0.6 mm wide, with neutral gaps of 0.5 mm above/below the
foot. A quarter-turn folds the whole rigid C hook into the straight y aisle;
this is E-191's swivel, not a new hinged-finger mechanism. The new question is
whether a finite guide, thrust interface and grounded drive fit that aisle.

- **Retained sliding blade:** E-191's translating hook gains a 0.4-mm retaining
  channel wall. At foot width 2.8, tip x=1.0 and 0.8-mm withdrawal, its right wall
  occupies x=3.64…4.04, y=±0.7, z=−4…2.2 mm. The adjacent foot starts at x=3.68.
  Their nominal intersection is **0.6048 mm³**. A grounded underfoot actuator
  and pushrod cannot repair this wall collision. This rejects this retained
  channel, not telescopic segmentation or every translating capture principle.
- **Nested guided swivel:** a 0.6-mm ground rail, 0.15-mm radial running gap,
  0.4-mm carrier wall, 0.1-mm rotary gap and 0.4-mm outer wall make a 2.7-mm OD
  package. A 2.8-mm foot leaves a 2.28-mm aisle. Generated 64-sided annular
  material intersects a neighbor by **0.2450 mm³** at each of y=5.08 and 10.16 mm,
  with identical nominal foot heights. This is an actual solid intersection,
  not merely an overlapping bounding box or a tolerance shortfall.
- **Axially stacked swivel:** carrier z=[−4,−1] and rotor z=[−1,2.2] meet at a
  thrust face, avoiding the second radial wall. The same rail/gap/0.4-mm wall
  gives 1.7-mm OD. Nominal transport fits; coherent relative closure of 0.35 mm
  makes the generated sleeve intersect a foot by **0.02980 mm³** at either row.
  The closure is 4e+d with e=.05, d=.15; it excludes the .025-mm reserve.
  A bore is genuinely empty: intersection is computed on annular material.

The two-row witnesses occur inside the requested continuous route. They do not
need a special acceleration or an independently random cell defect. Foot and
sleeve share z=[0,1.2] in each witness. Arbitrary maps permit this height choice.
For passing sections, exact angular vertex extrema enclose every lip angle;
withdrawn x envelopes fit continuously through both rows and arbitrary foot
heights. Conservative enclosure failures are not themselves intersection proofs.

The axial-drive construction has two 0.3-mm strands at y=2 and 3.2, from
z=−10 to 50, a 0.6-mm-radius upper idler and lower drive wheel, each 0.6 mm wide
in x. A carrier throat reaches the active strand at y=2 below the rotor. The
return is a real second strand. Finite rail brackets connect both wheel regions
to a rail clamped into a 3×3-mm ground block at z=−14…−10. Loop centreline length
is **123.77 mm**. Side cheeks clear wheel width by .1 mm; crosspieces clear
the .3-mm cord wraps by .25 mm. Their positive-x reach of .7 mm is included in the route
screen. Axle/bore contact remains unqualified. These moving-bank components
stay in the x aisle or below all feet during two-row indexing; the source gives their envelopes and checks
vertical end clearance through head height −.5…40.5. Circular wheels/strands use
conservative boxes for external clearance. No belt/tooth strength is inferred.

This is a connected candidate force route to a grounded input wheel, not a
powered head: capstan traction/termination, wheel shafts/bearings, preload,
carrier antirotation, rotary command, motor packaging and outage arrest remain
unbuilt. A circular sleeve alone supplies no antirotation. The stacked thrust
face permits yaw only with appropriate contact/drive; it is not a free spline.
Stopping at the demonstrated collisions avoids designing those missing parts
for a failed section. Retention at 6,400 sites is still independent hardware.

## Uncertainty and structural discrimination

Use E-191's explicit envelope `delta=4e+d+.025 mm`. Require bore gap greater than
`2e+.025 mm` for the two radial size errors and an additional guide-alignment
bound. These are engineering scenarios, not distributions for X1C/PLA. The d
bound must include all relevant point-pose motion; correlated tilt, warp and
opposing print biases can affect an entire bank. Common rigid translation cancels.

The finite grid uses foot widths {2.6,2.8,3,3.2,3.4}, rail diameters .4…1.3 in
.1-mm increments, radial gaps {.05,.1,.15,.25}, walls {.2,.4,.8}, and 56 tip
positions .8…1.35 in .01-mm increments. Nested sections add .5 mm to outer radius.
Only bore-fit, conservative external sweep and shoulder-overlap screens are
counted; a geometric count is not a mechanism or manufacturing pass.

| e / d mm | Stacked sections (wall ≥.4) | Nested sections (wall ≥.4) |
|---|---:|---:|
| .025 / .05 | 5,639 (1,809) | 96 (0) |
| .05 / .15 | 18 (2) | 0 (0) |
| .10 / .15 | 0 (0) | 0 (0) |

A coarse .1-mm tip grid missed the two central .4-mm-wall sections; refinement
found tip=1.01/1.02, foot=2.8, rail=.4, gap=.15, wall=.4. This changes the
geometric conclusion from none to conditional sections, not to a viable head.
Their route margin is only .015 mm. The best central free-compliance ratio uses
foot=2.8, rail=.7, gap=.15, wall=.2, tip=1.02: route margin .065 mm and shoulder
reserve only .005 mm. Counts remain finite-grid results, not exhaustive search.

Ground clamping is deliberately favorable. At maximum contact height 40.5, the
rail still has L=50.5 mm above ground. With E-191's assumed moving force
F=.13405 N and contact eccentricity a, its free response is
`u=F*a*L²/(2*E*I)`, `I=pi*d_rail⁴/64`. This ignores additional pulley load,
bracket bending, clearance and ground compliance. The central best response /
remaining route margin is **2.968** (u=.19289 mm) at E=100,000 N/mm²; E=2,000 multiplies
that ratio by 50. Large responses invalidate small-displacement prediction;
the ratio is a warning, not a claim that loaded columns actually penetrate.
The two .4-mm-wall sections have a best ratio **120.606** at the same modulus.
Response scales linearly with the assumed load; a 1-N case multiplies it by
7.46. Neither force is a measured service load. Column guide reactions and
contact can alter the free response. No coupled
contact or stress/fatigue acceptance follows.

A top support is not free either: a transverse bank bar at z=48…50, y=±.4
intersects each 1.2-square stem by **1.92 mm³**, even at the highest foot setting.
A y-directed aisle portal grounded outside the array is a different topology
and is not rejected here. It would need its own finite long beam, supports and
transport route. Further bare-rail diameter tuning has low value; a changed
grounding route or removal of tall moving capture is the reopening condition.

0.2-mm walls remain experimental with the optional 0.2-mm nozzle. No combination
here bounds layer quantization, roughness, hole bias, orientation strength, creep,
fatigue or wear. Shrinkage/warp enter only the explicit envelopes; no yield or
board failure probability is claimed. Tighter errors materially change the
geometric disposition, so counts cannot be treated as calibrated production data.

## Handoff, finite time and complete-machine comparison

At neutral neither lip supports the foot. Releasing the resident stop there
leaves a **0.5-mm unsupported gap** before lower-lip contact. Opposite lip contact
requires 1 mm total travel. The required order is ground support → rotate in →
0.5-mm take-up and force proof → unload/release stop → travel → reseat/prove
stop → neutralize 0.5 mm → rotate out. A favorable scalar ordering cannot prove
physical stop release, loaded seating, sign reversal or power-loss support.
Drive traction, resident-stop geometry and actual proof are not generated, so no
successful supported transaction is claimed. E-125/E-191's arrest/readback
obligations remain.

Retain E-190's original .05-s transfer slots, six-second map allowance, final
vertical/y returns and kinematic limits. Conservatively charge an additional
.020-s half-mm motion plus one quarter-turn per transfer. This avoids treating
new motion as already funded by the old slots, but may overcharge if a future
implemented transaction proves overlap. Rotation times are scenarios, not motors.

| Quarter-turn | Added time/transfer | Two-bank map | First passing bank count; map |
|---|---:|---:|---:|
| .020 s | .040 s | 31.222 s | 3 / 240 vertical drives; 23.104 s |
| .050 s | .070 s | 33.622 s | 3 / 240; 24.724 s |
| .100 s | .120 s | 37.622 s | 3 / 240; 27.424 s |

These are conditional schedule calculations, not deadline passes for the rejected
geometry. In E-190 the home-return direct control needs 240 drives / 22.963 s at
the same central motion/slot settings; ideal height-preserving direct needs
160 / 28.022 s before these extra operations. The new route therefore loses its
motor-count advantage under this additive timing model. Under an integrated
slot model, all capture, take-up, stop relief, proof, rotation and settling must
fit strictly below .074731 s/transfer to keep two banks; this remains unproven.

E-185's different motor-limited/addressing model gives **82 direct-return heads,
131 resident-screw heads and 214 resident-Geneva heads** at its base load. Those
are distinct controls, not 82 fixed-datum heads and not interchangeable with
E-190's 80-wide bank schedule. Fixed-datum screw/indexer machines avoid tall-head
transport but replicate resident transmission, thrust support and arrest;
no control is qualified or selected by this investigation.

At 240 branches the illustrative $250 shared reserve leaves <$1.0417 per entire
branch below the $500 ceiling. Each aisle branch now includes a ground rail,
carrier/rotor thrust interface, two wheels, tensioned loop, capture, axial drive,
rotary command, arrest and observation. Independent rotary drives would add
another 240 channels; bank-shared rotation needs an actual transmission and
within-row capture barriers. It cannot inherit private-event timing for free.
No sourced BOM is asserted. At least 480 loop wheels and 240 sleeve assemblies
are repeated, alongside 6,400 resident stops. One ten-second resident assembly
operation is 17.8 h. Do not infer print material/time or service life from these
primitive envelopes.

Unchanged cells require their own retained support; no deliberate global reset
is included. Adjacent displacement through the shared frame is unbounded.
Capture/support/withdrawal proof gives at least 19,200 full-map proof events;
false acceptance and common bank faults are not assigned invented probabilities.
A persistent failed proof keeps the last support and stops the bank; six seconds
is not an arbitrary-fault recovery guarantee.

## Decision and verification

Close this bounded investigation at its collision gate. Stop the retained channel,
nested collar and the explicitly colliding .6-mm-rail stacked section; retain
the two .4-mm-wall/.4-mm-rail geometric sections as unresolved compliance cases.
Do not reject every aisle, folding capture or grounded-portal principle. Do not reopen the opposed-pair
machine, select a winner, purchase or fabricate. The next useful architecture
comparison is a changed ground route (longitudinal portal/distributed guide)
against fixed-datum resident transmission, including finite support crossings,
source-loss behavior and repeated hardware; not another optimized bare hook.

Self-review: independent polygon rectangle clipping cases; annular witnesses at
32/64/128/256 facets (positive at every resolution); both successive rows;
zero-load/inverse-modulus limits and independently integrated beam curvature;
explicit no-contact handoff; inherited rest-to-rest schedule equations. The
nested witness converges .238884→.246894 mm³, stacked .028172→.030300 mm³.
These checks verify the stated models and counterexamples only. Keep executable
source, discard reproducible JSON, and retain E-191 as the prior bare-hook screen.
