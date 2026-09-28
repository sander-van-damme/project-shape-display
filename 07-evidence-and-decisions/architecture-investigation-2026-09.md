# Full-scale architecture investigation — 27 September 2026

## Decision

**No investigated architecture is yet convincingly compliant with all product
requirements. Do not build 6400 cells from this investigation.** The strongest
next experiment is **passive stepped rotary stops programmed by an 80-channel
travelling PM-stepper head, with a common lifting platen**. It has a conditional
26.25 s complete-map schedule at 80×80, but no qualified low-cost actuator supply,
no measured return-friction margin and no demonstrated coupling/detent reliability.
The working purchased BOM is **$432 / $518.40 with 20% contingency**, above the
$500 ceiling when contingency is included. This is a research recommendation,
not a product pass.

The useful result is a narrower, falsifiable engineering question: can an
unloaded 3 mm printed stepped cam, guided follower and cheap 8 mm PM motor deliver
reliable passive height memory at 5.08 mm pitch? A small coupon can reject that
idea before thousands of parts are printed.

Reproduction and evidence are in
[test08](../06-experiments/test08_architecture_search/README.md), including the
[architecture comparison](../06-experiments/test08_architecture_search/architectures.md),
[historical audit](../06-experiments/test08_architecture_search/history.md),
[source ledger](../06-experiments/test08_architecture_search/sources.md),
[parameters](../06-experiments/test08_architecture_search/params.json) and
[BOM](../06-experiments/test08_architecture_search/bom.csv).

## Scope and search

The design target and the request's **strictly less than 30 s end-to-end** limit
govern this investigation. Historical experiments are evidence, not constraints.
The comparison covers per-cell motors, single and parallel travelling writers,
shared screw drives, serial and parallel pneumatics, Jacquard-style catches,
mechanical coincidence addressing, binary weighted mechanical memory, thermal
actuators, passive molds and the new rotary-stop approach. The detailed comparison
records actuator counts, purchased components, timing, power, density and
manufacturing implications for each.

The recurring tradeoff is that cheap shared actuation saves motors but spends
time. Full-stroke row pushers still need both extension and retraction on every
row. A single writer would need about 213 completed cells/s before overhead;
at the modeled motion rates it takes roughly 76 minutes. Multiple row writers
can meet timing only by adding too many drives. Pneumatic designs move cost
and reliability into thousands of seals/valves. Scanned binary catches can meet
timing in principle, but the sourced 80-solenoid bank costs $356.80 and draws up
to 440 W before the rest of the machine is added.

After the rotary candidate exposed weaknesses, the search revisited fewer head
channels, different vertical level counts, servo gearing, solid columns, binary
catches and spring return. The quantitative rejection/iteration trail is kept
in the architecture comparison; the latest historical trial was not assumed best.

## What the proposed mechanism actually does

Each square column has an offset lower follower. Its toe rests on one of five
flat-height sectors of a freely selectable rotor. A guide constrains the slender
follower; a separate guide pair constrains the visible square body. The rotor
is not intended to lift a loaded column. Its flat plateau and thrust support
carry play loads after programming, without motor torque.

A common platen lifts every column to 41 mm above its zero height, clearing
even the tallest 40 mm cam sector. Below the stationary rotor shafts, a travelling
head engages 80 rotors at once with axially compliant friction face couplings.
It turns each rotor backwards against an individual home stop, then forwards
by 0, 4, 8, 12 or 16 full motor steps. It disengages so an independent printed
detent can seat the rotor. The head indexes to the next row. After all 80 rows
are programmed and the head is parked, the platen lowers; each column follows
by gravity until its toe reaches the programmed step.

This arrangement separates long-stroke motion, selection, mechanical memory
and load support. It also keeps the moving head below all stationary shafts,
avoiding the unresolved “head travels through the column field” interference
of some scanned-latch concepts. Nothing requires 6400 purchased motors, springs,
magnets, cables or bearings. **It does require 6400 reliable printed sliding and
rotating assemblies.**

The phase-independent friction coupling and detent are proposals, not qualified
hardware. Hard-stop homing can leave motor phase error after slip/stall. One
18° missed step exceeds the 12.50° geometric toe margin. The detent must reliably
correct that phase error while unloaded; assuming perfect step counting does
not solve it. The CAD contains the cam and detent wheel, but not a production
detent, stop, coupling head, bearing retention system or complete structural frame.

## Dimensions, counts and tabletop surface

| Item | Proposed value / status |
|---|---|
| Active area | 406.4 ×406.4 mm; 80×80 at 5.08 mm pitch |
| Moving square body | 4.68 mm wide ×80.2 mm long; lower 40.2 mm relieved for fixed guide; 0.40 mm top gaps |
| Projected top coverage | 84.87%; square cells retain the 1-inch / five-cells grid |
| Usable levels | 0, 10, 20, 30, 40 mm; five independently chosen heights |
| Miniature reference | **Not measured.** 40 mm is provisional; miniature-height compliance remains open |
| Cam | 3.0 mm outside diameter, 2.0 mm central core; five 72° sectors; 42 mm maximum top including 2 mm base |
| Follower | 42 mm tall, 0.7×1.8 mm stem; 1 mm wide, 1.5 mm thick toe; fixed slotted guide extends from z=4 to 84 mm |
| Body guidance | Two 4 mm guide tiers at z=110.2–114.2 and 118.2–122.2 mm in coupon coordinates |
| Vertical envelope | Surface z=124.2–164.2 mm; head, rails and frame below imply roughly 220–270 mm tabletop height, not a thin mat |
| External plan envelope | Allow roughly 460×500 mm for borders, rails and two staggered ranks; packaging not finalized |
| Actuators | 80 PM motors + one scan axis + one platen drive + one common coupling axis =83 |
| Printed memory parts | 6400 rotors, 6400 column/followers, 6400 independent detents, guides and frame modules |
| Motor electronics | 80 dual H bridges, 40 eight-bit control shift registers, ten proposed eight-channel boards, one controller |
| Harness | 320 short motor conductors confined to the head; shared power and serial connection to controller |

Eight-millimeter motors do not fit a single 5.08 mm row. Two staggered ranks
give 10.16 mm motor spacing. Their shafts need short compliant/flexible fan-in
connections to the 5.08 mm rotor grid. That packaging is an allowance, not CAD-
validated. The 80-channel head is expected to weigh order 1–2 kg; 4 m/s² scanning
therefore needs roughly 4–8 N before guide drag, reasonable for a belt axis but
still a test requirement.

Moving columns and the assumed platen alone total 15.24 kg. Rotors, guides,
frame, motors and power add more: plan for roughly 20–25 kg overall until a
complete mass model exists. This is a substantial tabletop appliance, not a
portable battle mat; the product target sets no mass ceiling, but usability
is worse than the original small prototypes suggest.

Five height levels suit walls, pits and terraces, but make coarse slopes and
stairs. Nine levels with the existing toe geometry **interfere**: the toe spans
more than a 40° sector. More vertical resolution requires another contact design,
not just changing a software parameter. Miniature bases need locally level
25.4 mm footprints or deliberately designed platforms. Cells cannot make an
arbitrary stepped surface stable for every base. Avoid isolated high support
cells beneath a miniature.

Global reset moves the whole surface. This is an encounter-map writer with a
cleared board, not a proven way to preserve miniatures on the surface during
transitions. Manual removal/replacement is unbounded and is not included in
26.25 s. If that is required as part of every transition, the complete use case
does not meet the timer. The mechanical timer ends after the new surface settles,
not after an operator repairs faults or repositions figures.

## Complete update timing

The event model uses rest-to-rest trapezoidal/triangular axis moves. It includes
every cell even for an all-zero target, homes every row's rotors, parks the head,
and lowers/settles the surface. It credits no overlap between operations.
The assumed PM rate is 400 full steps/s, below the archived motor's no-load
response specification, **but no loaded torque-speed curve validates it**.
The 25 ms coupling strokes and 15 ms settles also need measurement.

| Operation, complete board | Seconds |
|---|---:|
| Axis reference from defined parked state | 0.500 |
| Raise all columns clear, 41 mm | 1.346 |
| 79 row index moves, acceleration included | 5.631 |
| Commands/control | 0.160 |
| 80 engagements | 2.000 |
| 80 rotor home sweeps, 22 steps and settling | 5.600 |
| Worst-case writing, 16 steps and settling per row | 4.400 |
| 80 disengagements | 2.000 |
| Passive detent seating | 1.200 |
| Return head to park | 1.668 |
| Lower platen | 1.346 |
| Final settle before ready | 0.400 |
| **Total** | **26.251** |

All-high, checkerboard, stairs spanning all heights and seeded random full maps
all reach the worst-case bound because every row contains a maximum-height cell.
All-low still takes 23.051 s; alternating rows take 24.651 s. Arbitrary old maps
are covered by the global clearance stroke. All 25 old/new single-cell height
pairs are checked in the ideal support-state calculation.

Sensitivity matters more than the nominal pass: 200 pulses/s yields **33.851 s**;
800 pulses/s yields 22.451 s. Halving the head to 40 channels yields **39.725 s
even at 800 pulses/s**. At 400 pulses/s, increasing each engagement and
disengagement from 25 to 50 ms adds 4 s and fails. The available margin is only
3.749 s. Cold recovery from an arbitrary head position is not covered by the
0.5 s parked-state reference allowance; re-establishing park adds travel.

An update with a stuck follower or misindexed cam is **not ready for play**.
No bounded repair/detection loop is modeled. Consequently this is a fault-free
conditional timing estimate, not a reliable end-to-end performance guarantee.
Partial updates do not rescue this conclusion: the present mechanism still
globally lifts the surface, and the required full-map bound stands on its own.

## Loads, return, structure and power

The final candidate uses solid printed bodies rather than hollow bodies, since
printing is not the cost bottleneck. Geometry at the assumed material density
gives **2.069 g/cell**, 13.24 kg of moving columns, and 20.29 mN gravity force
per cell. The hollow alternative is 0.997 g and provides just 9.78 mN. At the
assumed 5 mN guide drag the margins are 15.29 and 4.78 mN respectively. Dirt,
warping and lateral loads can erase either margin. Test breakaway friction;
do not infer it from nominal CAD clearance.

With a 2 kg platen, 0.2 m/s² lift acceleration and 5 mN drag per cell, the
calculated peak lift force is **184.5 N**. An 8 mm lead at assumed 30% efficiency
needs **0.783 N·m total screw-drive torque at 262.5 rpm**. Require at least
1.57 N·m at that speed for a twofold qualification margin. The $18 lift motor
allowance is not a matched torque-speed selection; a larger motor or transmission
may increase the BOM. Four synchronized screws and four guides distribute load;
belt phase errors or one stuck corner can rack the platen.

The unsupported follower screens at only **0.108 N** Euler load using 1.5 GPa
effective modulus and a conservative fixed-free length. Reducing effective
unsupported length to 5 mm raises that screen to 7.62 N. This does **not** prove
the printed guide is rigid enough to provide that support. Toe contact area is
about 0.322 mm², giving 3.11 MPa at 1 N and 15.54 MPa at 5 N. Local layer
orientation, cam-edge crushing and creep may dominate. A 1 N per-cell service
test and a short 5 N accidental-load test are proposed, not passed.

An initial short guide ended at z=40 mm; inspection caught that the stem left it
at full extension. The final guide extends to z=84 mm. Clearance slots through
the lower body and lift plate let that stationary guide pass; a narrow bridge
crosses the guide's open slot to transmit load to the stem. The body was lengthened
to leave 40 mm of uninterrupted square upper column, keeping the guide relief
below adjacent terrain even with a 40 mm step. This fixes nominal interference
and support coverage, at the cost of a taller, heavier machine. The relieved
body and bridge need load tests; a short guide must not be reinstated to simplify
the print while keeping the improved Euler figure.

An additional variable-section beam buckling model screens the cam itself,
using a geometric-stiffness eigenproblem and sampled cross-sectional principal
inertias. The original 0.45 mm core radius gives an idealized 2.45 N critical
load; enlarging it to 1.0 mm improves that to **4.96 N**, while retaining 0.15 mm
toe/core clearance. Cross-section sampling and beam-mesh refinement are recorded,
and the solver recovers the uniform-cantilever Euler solution. This is still
not a 5 N rating: actual toe load is eccentric, the root is not a perfect clamp,
and print defects/creep are excluded. The 5 N abuse gate is therefore an explicit
red flag, even after the improvement. A measured stronger support/material or
another cam structure is needed before claiming tolerance of hand pressure.

Guide-wall arithmetic originally gave zero thickness. The revision leaves
0.20 mm walls with 0.10 mm clearance per side. It needs a fine-nozzle or resin
coupon and structural backing; it is not ordinary 0.4 mm-nozzle geometry.
Nominal 0.4 mm top gaps leave only 0.05 mm after the explicitly modeled width,
pitch and ±0.1 mm deflection allowances. Those deflections are limits, not measured
values. A simple solid-body cantilever screen at 42 mm exposure gives about
0.041 mm deflection under 0.1 N lateral load, but about 0.41 mm under 1 N.
Neighbor contact and guide compliance require testing under real handling.

The CAD's 2 mm lift plate is a **coupon**, not a full-width structural platen.
A 406 mm unsupported printed sheet would deflect far too much. The full device
needs a ribbed/box platen and supported modular guide cartridges (provisionally
64 modules of 10×10 cells). Platen flatness should stay within 0.25 mm and the
1 mm unloading clearance must remain positive everywhere under load. No FEA or
validated full-frame CAD establishes that yet.

At 3.3 V and 40 Ω per phase, 80 two-phase motors dissipate **43.56 W** when all
energized, about 13.2 A on the motor rail. Although motion is serialized, the
platen must remain raised during writing. Without a qualified passive brake,
count a60 W lift holding allowance concurrently with the43.56 W head and15 W
auxiliaries: **118.56 W nominal peak**; specify and test roughly a150 W protected
supply arrangement. Assuming the lift consumed nothing while stationary would
understate the power requirement. A qualified passive holding device could
reduce this, but its hardware cost must then be added.
This excludes fault current and unknown lift-motor sizing changes. Holding the
completed terrain requires no powered head torque. Lift screws with an 8 mm
lead must not be assumed self-locking: loss of power during reset needs a brake,
self-locking transmission or controlled descent, none yet fully designed/costed.

## Purchased cost

The detailed 18-line BOM explicitly includes drivers, PCBs, wiring, head shafts,
power, rails, four lift screws, belts, sensors and spares. It uses printed cell
bearings; adding even $0.10 of bought hardware per cell would add $640.

| Scenario | Before contingency | With 20% |
|---|---:|---:|
| All-low allowances | $276 | $331.20 |
| Working allowances | $432 | $518.40 |
| High allowances | $783 | $939.60 |

These are not three supplier quotations. In particular the 80 PM motors are
allowed at $1.25 each, without a current matched delivered quote. The working
non-motor total is $332. To stay below $500 with 20% contingency, motors would
need to average at most **$1.058** with every other allowance unchanged. To reach
$400, merely discounting the motors is insufficient in practical terms: roughly
$99 must be removed from the $432 base estimate. Under $200 has no demonstrated
path. A $276 optimistic combination is not evidence of an available machine.

The historical surplus motor price suggests a procurement experiment is worth
doing. Conversely, sourced FS90 servos cost $632 for 80 alone, and current
industrial micro-steppers are much more expensive. No purchases were made.
Unresolved brake, better lift motor, failed prints, extra feedback or structural
metal can invalidate the current allowance; they must be added when specified.

## Reliability, assembly and maintenance

At an independent per-cell error rate of 0.01%, the probability that all 6400
cells are correct is only **52.7%**. Even 0.001% yields 93.8%. A 99% perfect-map
goal requires approximately **1.57×10⁻⁶ errors per cell-update**, before correlated
faults such as a warped guide tile or misaligned head. About 1.91 million zero-
failure independent trials would be needed for a one-sided 95% bound at that
rate. A successful six-cell demonstration cannot establish it.

Likely faults and consequences:

- A sticking column remains too high during lowering. The platen cannot pull it
  down; the map is wrong and the timer has not validly ended.
- A missed rotor step or a detent that does not seat can land the toe on an edge,
  select the wrong height or drop later under a miniature. No per-cell sensor
  presently detects this.
- One misaligned coupling can slip while the other 79 succeed. Spring compliance
  distributes engagement height, but creates another tolerance and wear variable.
- Axial coupling force can unseat a rotor unless its thrust retention is designed.
  At just 0.5 N/coupling the beam must distribute 40 N; this is not negligible.
- Dust, stringing and filament swelling can turn an initially free guide into a
  jam. Dry cleanable cartridges and replaceable followers are required.
- One large servo/motor-bank power or communication failure affects a whole row.
  A controller must keep “ready” false on detected faults; undetected cell faults
  remain the central reliability problem.
- Power loss during play leaves the mechanical stops holding. Power loss during
  the common lift is not safely resolved by that fact; reset recovery rehomes
  every rotor and requires preventing uncontrolled platen descent.

Even at 20 seconds per insertion/check, two separate parts per cell cost about
71 hours. Add detents, wiring, guide calibration and debugging: **100–200 hours
of hands-on work is a planning range**, not a measured assembly study. Fine-feature
printing and thousands of inspections make this a demanding one-person hobby
project. Use detachable 10×10 cartridges and a replaceable head driver module;
do not glue thousands of critical cells into a monolithic board.

## Evidence level and limits

| Evidence | What was established | What was not |
|---|---|---|
| Parameterized OpenSCAD | Real cam sectors, follower/toe, slotted guide, two upper guide plates and lift coupon; STL/CSG export | Complete production mechanism or frame |
| CSG intersections | Named cam/follower/guide/plate pairs at five seating heights and 20 raised rotor angles | Manufacturing tolerance, elastic interference, head/frame collisions or positive retention |
| Analytic geometry | Swept rotor radius, 1 mm unloaded clearance, 12.50° angular margin, contact area and thin walls | Contact stability or printed feature quality |
| Event simulation | All 6400 writes, 80 row homes, acceleration, coupling, park, lower and settle; six maps and 48 sensitivity cases | Loaded motor capability, fault detection or repair time |
| Force/structure screens | Weight, friction limits, follower Euler bounds, variable-section cam buckling, contact stress, lift torque and electrical load | Material allowables, fatigue, wear, creep, layer adhesion or full-frame stiffness |
| BOM and reliability scaling | Complete categories and sensitivity to per-cell hardware/error | Qualified quotes or measured reliability |

This work does not use a kinematic animation as proof. Tests ensure the known
weak cases remain failures. The proposed detent, hard stop, rotor retention and
head still need detailed prototype design and physical qualification. The
[prototype protocol](../06-experiments/test08_architecture_search/prototype.md) gives
measurable continuation/abandonment gates. That is the next decision point;
neither a full-scale purchase nor a 6400-part print batch is justified yet.
