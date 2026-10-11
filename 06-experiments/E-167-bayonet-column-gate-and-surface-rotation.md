---
status: complete
builds-on: [E-166, E-054, E-056, E-131]
---

# Bayonet columns trade separate pawls for interlevel rotation and alignment

**Retain interlevel cap rotation as a conditional positive-seat combination;
stop the nominal short-lift rotating-cap embodiment.** A lugged round stem passes
through a fixed slot, turns 90 degrees and rests in a grounded pocket. The column
is the moving lock. A 4.8-mm square cap with .6-mm release lift hits its neighbor;
**2.3-mm lift between 10-mm levels** escapes without a swivel. Stem guidance,
angular alignment, head capture and timing remain gates; no machine is selected.

Input main `1a3cb2e`; LAB-272. Reproduce with standard Python:
`python3 tools/curated-experiment-checks/E-167/probe.py`.
Evidence: generated rigid polygon/prism transitions, analytical bounds and
self-review. No fabrication CAD, force/contact dynamics, calibrated process
priors, measurements or independent review. JSON is disposable. No printing or
purchase proposed; dimensions, loads and speeds are explicit scenarios.

## Search and causal combinations

Orthogonal backing was cross-checked against E-054/E-056: shelves outside the
rack's vertical sweep recreate their side-wing load path. A shared return can
change placements but not erase the repeated guides/contacts. No new pawl detail
was justified. Change the functional axis to **column-as-lock**, borrowing the
insert-turn-seat sequence of panel fasteners. [Southco's D2 guide](https://southco.com/en_any_int/fasteners/emdzusemreg-quarter-turn-fasteners/emdzusemreg-turn-to-close-turn-to-open-quarter-turn-fasteners/d2-dzus-rapier-quarter-turn-fasteners)
describes a cam stud, receptacle, detent and stop, with spring receptacle retention
(accessed 2026-10-11). This analogy supplies no part selection, dimensions,
material prior or inherited vibration resistance for our gravity pocket.

| Combination | Complete causal route / changed burden |
|---|---|
| Short-lift cap | Travelling rotary-linear head captures stem, lifts .6, turns, translates, returns and seats; pocket rails ground the lugs; prove actual height/seat before release. Fails cap collision. |
| Swivel cap | Same gate, with captured thrust swivel keeping square top still; adds 6,400 bearing/retaining interfaces. Swivel geometry is unbuilt. |
| Interlevel cap | Lift 2.3 before turning; thin cap/round stem exploit the gap between levels. Same positive seat; schedule neighboring rotations. No swivel needed for nominal geometry. |
| Pawl/comb | E-054/E-056/E-166 keep top orientation but need separate movable support/return. Their shorter service allowances are also unproven. |
| Screw | E-131/A-007 remains the continuous-height friction control. Released quarter-turn translation is not a 40-mm screw lead and does not reopen its throughput disposition. |

All bayonet variants owe a bidirectional load-bearing head before unlock, axial
and rotary reaction during motion, and capture retained on failed seating proof.
Retry once while captured, then stop the module is an intended recovery policy,
not an implemented sensor or input-loss arrest. Gravity neither proves seating
nor catches a stem released while slot-aligned. A false accepted seat can drop it.
One fastener analogy and one path inversion (turn in a height gap) yielded this
combination; no broad search or saturation claim. Cross-checks included E-101's
shared cam, not just keyword-equating all rotary mechanisms.

## Finite geometry and support sequence

Units mm, z upward, pitch 5.08. Round shaft radius .6; five transverse rectangular
lugs x=[−2,2], y=[−.45,.45], thickness 1.2, spaced 10 axially. A 4.8-square,
2-thick cap has top 44 above the lowest lug bottom. Stem shift −10k, k=0…4,
gives tops 44/34/24/14/4: 40 travel. Discrete levels are an embodiment choice,
not a requirement. Exposed round stems are essential; adding full-width square
skirts invalidates the clearance result.

Gate within one pitch cell: z=[−1.2,0], aperture union of full-width x slot
|y|<.65 and central square |x|,|y|<.8. Ten nominal solid boxes form base rails,
shoulders and raised pocket rails z=[0,.4], |y|≥.8, |x|≥.65. At theta=0 lugs
pass the slot; at 90 their two wings bear on base rails inside the 1.3-wide pocket.
Pocket walls constrain rotation while seated; lift above .4 permits turning.
This is a geometric seated stop, not friction assigned to a weak spring.

Captured seat → lift → turn 90→0 → translate → turn 0→90 → lower → prove → detach.
Twenty unequal transitions and five lug prisms give **8,500/32,500/128,500 poses**
at 16/64/256 steps per phase for .6 lift, with zero positive-volume collisions.
The changed 2.3 lift passes 32,500 poses at 64 steps. Fault controls collide for
seated 45-degree rotation and axial movement while still turned into the rails.
Independent continuous separation: aligned lugs lie inside the slot; turning
lug bottom exceeds .4 and next lower lug top stays below −1.2 (−6.5 at 2.3 lift);
lift/seat occurs inside the pocket. Other lugs stay 10 apart. The round shaft fits
the central aperture. These bounds certify only the nominal rigid gate path,
not elastic contact, angular error, head acquisition or support transfer.

Nominal bearing area **2.16 mm²** gives **4.63 MPa average at 10 N**, not peak
pressure or a PLA allowable. Symmetric wings admit an axial resultant within
the support polygon. Lug-root stress, gate bending, tilt, eccentric payload and
frame grounding remain unsolved. Slotted row rails need distributed support;
a drawn ground surface is not a proven 203-mm beam or assembly layout.

## Cap collision and changed escape

For vertically overlapping equal caps, first contact obeys
`(d/2)(cos(theta)+sin(theta))=p−d/2`: **7.1484 degrees** for d=4.8, p=5.08.
Polygon checks at 64/256/1024 steps find 8.4375/7.3828/7.2070 degrees. At 45,
projection intrusion is **.7141 mm**. Isolated coplanar rotation needs d≤**4.2084**;
arbitrary simultaneous coplanar neighbors need d≤**3.5921**. Shrinking changes
gaps/utility, not an invented gap requirement. ±.001 holdouts check the first bound.

A .6 lift leaves 2-thick caps overlapping in z: **4,300 intersections / 25,700
rotation-neighbor poses** across 25 selected/neighbor height pairs. At **2.3 lift,
the same checks give zero**, including all five neighboring lugs. Continuous
intervals explain it: cap bottom is .3 above same-height neighbor top; the next
higher cap bottom is 5.7 above the moving top. Moving cap lies 4.3…6.3 above a
10-mm lug datum; neighbor lugs at multiples of 10 with 1.2 thickness miss that
band. Axial travel, lift and seat are axis-aligned, retaining .28 cap-to-cap and
≥.68 cap-to-lug horizontal gaps throughout. No full manufactured assembly follows.

A turning-cap circular envelope clears neighbor shafts of radius up to 1.4 by
**.2859**; this larger shaft is not integrated into the nominal .8 aperture.
Adjacent active caps at equal heights still collide. Checkerboard active centers
are sqrt(2)p apart, exceeding two cap circumradii by **.3960**. Thus nonadjacent
rotation escapes nominal interference, not head-routing cost or an automatic
2× timing tax. Selected miniatures turn with caps and return; acceleration,
slipping, handling and terrain appearance around round stems need assessment.

## Manufacturing and structural sensitivity

No probabilities or X1C capability assumed. Let e bound moving/gate edges and
relative center offset; common bank bias can put all cells at one adverse corner,
while common rigid translation cancels. Slot/pocket/shaft clearances are .2−3e;
wing land 1.2−3e; short-lift vertical margin .2−2e for stroke/depth errors.

| e mm | Slot/pocket margin | Wing land | Slot / pocket failures among 64 geometry corners |
|---:|---:|---:|---:|
| .025 | .125 | 1.125 | 0 / 0 |
| .050 | .050 | 1.050 | 0 / 0 |
| .100 | −.100 | .900 | 16 / 16 |
| .150 | −.250 | .750 | 16 / 16 |

Each corner rebuilds x/y offset, lug half-length/width, aperture and slot/pocket
edges and checks locked/through-plate poses. Wider-than-central slots omit the
vanished shoulders; a holdout catches inverted-box artifacts. Counts are scenario
failures, not yield; no warped/elastic/angular sweep is implied. At e=.05,
angular error delta leaves `.55−.50 cos(delta)−2.05 |sin(delta)|` clearance:
**.0143 at 1 degree, −.0212 at 2**. Pocket uses the swapped-axis equivalent.
Widening needs new support geometry. A conservative four-error cap budget gives
`.3−4e`, retaining .1 at e=.05, failing at .10; it is an envelope, not a fit prior.

Ideal column diagnostic `Pcr=pi² E (pi r⁴/4)/(K*44)²`, E=2000 MPa:

| Radius mm | Pcr N, K=1 / K=2 | Wing land after aperture enlarged to r+.2 |
|---:|---:|---:|
| .6 | 1.038 / .259 | 1.2 |
| 1.2 | 16.605 / 4.151 | .6 |
| 1.4 | 30.763 / 7.691 | .4 |

Source sweeps E=1000/2000/3000 and K=1/2. Neither end restraint is established
by the short gate. Thin stem fails this 10-N diagnostic; larger stems consume
bearing land. These ideal elastic cases are not a lugged-column eigenmode,
creep limit or strength qualification. Any additional guide must permit cap/lug
travel, not silently restrain the moving stem. No thick-stem assembly passes.

Assumed 10-g mass has only **.03924 mJ** gravity lift energy through .4. This
is not a shock-release prediction; gravity pockets inherit no qualified detent.
Stiction can defeat seating, upward disturbance can unseat, and input loss during
release lacks arrest. Hole shrinkage, first layers, layer quantization, warp,
roughness, wear, anisotropy/interlayer strength, creep and fatigue remain
uncalibrated. False acceptance p implies 6,400p expected misses without requiring
independence; p is unknown. No board reliability or physical qualification claim.

## Board bounds and decision

The integral branch removes separate pawls/returns by assigning their function
to **6,400 rotating stems, 32,000 lug stations and 6,400 precision pocket/slot
sites**, plus guides and cap attachments. Fixed modular rails reduce neither
wear nor assembly effort by assertion. Swivels add 6,400 captured thrust interfaces.
At hypothetical $250 shared spend, resident bought inventory must average
<$0.0391/cell under $500, before extra head cost; no BOM/quote pass.

Optimistic service: 40-mm move at 300 mm/s, 3000 mm/s²; two lift/seat strokes;
two 90-degree turns at 7200 degree/s²; .05 s capture/proof/release; 6 s/map for
preparation, registration, remaining travel, settling, final verification and
bounded retry. Triangular/trapezoidal profiles and strict
`6+ceil(6400/H)*service<30` give:

| Rotary ceiling degree/s | .6 lift: service s / heads | 2.3 lift: service s / heads |
|---:|---:|---:|
| 360 | .93990 / 256 | .99409 / 267 |
| 720 | .78990 / 214 | .84409 / 229 |
| 1440 | .78712 / 214 | .84130 / 229 |

Acceleration limits the fastest case. These conditional capacity bounds provide
no achievable layout/timing pass: checkerboard conflicts, transport, retained
axial/rotary channels and correlated faults remain. E-166's unproven .45/.50/.55-s
services need 121/137/149 heads. Unchanged pockets retain support, but shared
rail deformation/vibration remain open. No timing advantage is earned.

**Stop** short-lift integral-cap detail and thin-free-stem 10-N claims. **Retain**
interlevel rotation, conditional on discrete heights, thin caps, round stems and
nonadjacent turns; do not add a swivel by default. Next construct **finite stem
guidance and captured rotary-linear head access**, comparing the side-wing pawl:
can high-position support coexist with every lug/cap transition and retained
axial/angular command through reseat? Stop if it restores equal or greater
repeated hardware with slower service. Slot calibration/printing is lower value
before this structural/access question is answered.

Self-review checks separating axes, touching/penetration controls, continuous
gate/cap bounds, surface threshold holdouts, sampled prisms, wrong-state faults,
coherent corners, units, Euler end-restraint sensitivity and strict integer timing.
They verify reduced models, not hardware.
