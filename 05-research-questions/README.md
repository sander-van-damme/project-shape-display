# 05 — Research questions

This stage contains unresolved hypotheses, active investigations and research directions that sit between architecture ideas and experiments.

Research can propose, compare or decompose architectures, but it is not automatically established engineering knowledge. Durable conclusions should be fed back into stages 03 and 04. Falsifiable implementation work belongs in [`06-experiments/`](../06-experiments/), while consolidated findings and decisions belong in [`07-evidence-and-decisions/`](../07-evidence-and-decisions/).

The sections below contain the research backlog, broader investigations, and the current research direction.

## Architecture-search critical unknowns — September 2026 refresh

The [fresh broad search](../04-architecture-candidates/) changes the immediate
question from “which complete design looks best?” to a small set of discriminators
shared by several survivors. These questions are new hypotheses, not evidence.

### Q1 — Can passive threshold selection fit beside a load-bearing cell?

Can a 5.08 mm-pitch column contain a ratchet/escapement plus four independently
encoded threshold gates while retaining printable walls, 40 mm travel and a
useful downward load rating? The decisive test is not one hand-operated latch:
a 2×5 adjacent array must execute adversarial masks from one common stroke
without double steps, neighbor release or progressive phase error.

**Reject S1 if:** geometry cannot be packed at final pitch, or any tested
clearance/material setting that holds 5 N requires an unreliable selection force
window after print/process variation.

### Q2 — What is the fastest complete write-to-read path for planar media?

External planar memory is valuable only if unexpected terrain can be encoded,
installed, registered and read fast enough. Measure the entire path for one tile:
receive 100 five-state values, write/punch/set the medium, exchange it, move the
platen, settle and verify. Do not report punch or motor speed alone. Compare
disposable film, reusable shutters and row-profile strips using the same map.

**Reject S2 for surprise updates if:** a representative tile cannot complete the
path within a proportional share of 30 s, or exchange moves an adjacent loaded
cell/miniature unacceptably. It may remain useful for preplanned maps.

### Q3 — Can hundreds of choices be fanned out without hundreds of actuators?

S3 needs 320–400 decisions per station but cannot afford 320–400 conventional
solenoids. Investigate whether a printable shutter register, preloaded binary
mask, serial-to-parallel mechanical register or matrix can load choices while
the carriage moves, then release them in one powered dwell. Count state-load
time, common-drive force, reset and failure recovery.

**Reject S3 if:** a 2×4 coupon cannot repeatedly complete loaded
engage/write/disengage within 0.40–0.60 s, or extrapolated selector hardware and
drivers leave no credible <$500 BOM.

### Q4 — Is a cheap tile clutch actually independent under load?

S4 moves the bought selector boundary to about 64 tiles. Determine whether a
printed dog clutch, wrap spring, sliding key, compliant coupling or valve can
engage one tile, leave its loaded neighbor stationary, and allow all tiles to
engage synchronously without destructive torque accumulation.

**Reject the shared bus if:** one jam propagates into neighboring state loss,
phase error grows with bus length, or a complete protected coupler cannot fit an
average $3 ideal / $6 absolute per-channel allowance before the rest of the BOM.

### Q5 — How much isolation is enough for a regional reveal?

The requirement currently lacks a numerical disturbance limit. Establish a test
using a loaded untouched tile and a representative miniature: peak vertical and
lateral motion, residual height error, and whether the miniature moves or tips
while an adjacent tile resets. Sweep 5×5, 10×10 and 20×20-cell boundaries. This
single protocol discriminates S1, S2 and S4 and determines the practical tile
size.

### Q6 — Can inexpensive verification replace per-cell sensors?

Test a camera/structured-light or scanning-contact height check after programming.
Measure acquisition plus retry time, detection of one-level errors, occlusion by
miniatures, and whether verification can be limited to changed regions. This is
not required if mechanics prove intrinsically reliable, but it may relax costly
precision in S1–S4.

### Q7 — Can a multistable printed layer serve as dense reusable memory?

Do not require the metamaterial itself to make the 40 mm visible stroke. Test the
more promising role: a thin reusable memory/selector layer whose bistable cells
encode which terrain outputs should respond to a separate shared lift.

Measure minimum practical pitch, independent write force, state retention,
neighbor cross-talk, cycle life and print-to-print force variation. Compare one
binary layer with four unary threshold layers for five height states.

**Reject this role if:** independent states cannot be packed near final pitch, or
the safe write-force window collapses under realistic print variation and
neighbor coupling.

### Q8 — Can programming force be decoupled from service-load support?

Fixture mechanisms suggest a useful mode split: reconfigure while unlocked with
low actuator force, then lock so the passive structure carries the miniature load
with the writer removed or unpowered.

Build a small module that explicitly separates these modes. Measure programming
force, locked stiffness/load, unlock force, disturbance transferred to neighbors
and repeated lock/unlock consistency.

**Reject this family if:** the lock needs cell-scale purchased hardware, cannot
hold the required load, or unlocking a target region materially moves surrounding
terrain.

## Next experiment sequence

Run small experiments in rejection-value order rather than refining one design:

1. **Common isolation rig:** two adjacent loaded tiles and interchangeable drive
   fixtures. It supplies the Q5 disturbance baseline for every survivor.
2. **Threshold strip:** 2×5 final-pitch ratchets with two threshold layers and a
   common stroke. This can kill broadcast-memory families cheaply.
3. **Planar-media pair:** two 5×5 tiles, deliberately misregistered across a
   tolerance matrix, with timed exchange and 100 read cycles.
4. **Shared-bus pair:** two small tiles, selective and simultaneous coupling,
   including a forced jam. This tests S4 failure containment before a long shaft.
5. **Mechanical-register head:** only if the latch coupon works, add a 2×4
   preloaded selector register and measure a complete loaded dwell.
6. **Verification trial:** introduce known one-level errors into the preceding
   coupons and compare camera/scan detection and retry time.
7. **Mechanical-memory lattice coupon:** test a small final-pitch bistable array as a reusable selector layer, including adversarial neighbor writes and cycling.
8. **Reconfigure-then-lock coupon:** compare low-force programming with locked service load and measure disturbance during selective unlock.

Do not build a complete 10×10 tile until at least two different survivor coupons
have been tested with the same load and disturbance protocol. That comparison is
more informative than polishing the first mechanism that moves.

## Research backlog

Underlying mechanism and discipline knowledge is normalized in the
[engineering knowledge](../03-engineering-knowledge/). Backlog entries are project
hypotheses; tests provide evidence; durable mechanism knowledge should be fed
back into the knowledge base.

This section records engineering ideas that are worth testing but are **not yet
validated project architectures**. An idea belongs here when it is plausible
enough to deserve a quantitative or physical test, even if a related earlier
architecture performed poorly.

A backlog entry should only move to "rejected" after its specific hypothesis has
been tested against the current design target. Earlier tests are evidence, not a
blanket rejection of every variant in the same family.

### R01 — high-speed travelling multi-row actuator

**Test09 follow-up:** the [separate quantitative screen](../06-experiments/test09_test08_validation/)
now covers 1–5 rows, 20/40/80 parallel columns, independent full-stroke drives
and shared motion with local selectors. Four/five full-width shared rows have
conditional timing windows, but no measured selector or qualified <$500 BOM.
Retain a later 2×4 dynamic selector/latch coupon; do not build a full head from
the optimistic screen. The original hypothesis below remains unvalidated.

#### Hypothesis

Revisit travelling/shared actuation, but do **not** restrict the concept to one
cell or one row per carriage stop.

A travelling head could service **2, 3, 4 or 5 rows in parallel** before moving
to the next row group. The mechanism may use multiple independent actuators,
mechanical fan-out, a common stroke plus local selection, or another way of
programming several rows during one carriage dwell.

This is deliberately broader than the previously screened "one XYZ writer" and
"row bank of independent full-stroke pushers". Those estimates showed that their
specific serial/full-stroke transactions were too slow; they do not prove that a
much faster multi-row head is impossible.

#### Why it may matter

At 80 rows, grouping rows reduces carriage stations to roughly:

| Rows serviced per station | Stations for 80 rows | Raw average station budget inside 30 s |
|---:|---:|---:|
| 1 | 80 | 0.375 s |
| 2 | 40 | 0.750 s |
| 3 | 27 | 1.111 s |
| 4 | 20 | 1.500 s |
| 5 | 16 | 1.875 s |

The last column is only a sanity bound: reset, parking, settling and any global
lift also consume time. The useful question is whether increased parallelism can
reduce transaction time enough without making actuator count, packaging, power
or cost unacceptable.

A particularly interesting variant is a compact head that spans five adjacent
rows and all 80 columns, then advances by five rows. Another variant is a smaller
head that covers only a subset of columns but uses very fast indexed motion.
Neither should be accepted or rejected without a complete end-to-end schedule.

#### Test proposal

Create a future numbered test that sweeps at least:

- rows per carriage station: 1, 2, 3, 4, 5;
- columns actuated in parallel;
- actuator stroke and whether the actuator must perform the full 40 mm travel;
- carriage speed and acceleration;
- engagement/disengagement time;
- reset/homing strategy;
- old-map to new-map worst cases, not only sparse edits;
- purchased actuator/driver count and wiring;
- moving-head mass and required carriage force;
- estimated purchased BOM;
- pitch/fan-out feasibility at 5.08 mm;
- failure recovery and whether one jam blocks an entire row group.

The full-map model must include all reset, positioning, actuation, settling and
parking operations and remain strictly below 30 seconds.

#### Physical decision gate

If the analytical sweep produces a credible region, build only the smallest
full-pitch coupon/head that tests the bottleneck. Measure loaded actuation time
and repeatability instead of extrapolating from no-load motor speed.

Keep this research direction open unless quantitative timing, packaging, cost or
reliability bounds rule it out.


### R02 — Jacquard-style broadcast selector

#### Hypothesis

Borrow the central idea from Jacquard textile machinery: a **single selector
operation can decide which members of a dense array respond to a shared motion**.

For this project, do not interpret that narrowly as "swap a punched card for
every D&D map". The useful research question is whether a thin mechanical
selection layer — plate, pins, hooks, sliding bars, orthogonal selector strips or
another programmable mask — can select many cells simultaneously while a global
lift or programming stroke supplies the actual energy.

A selector only needs to distinguish selected from unselected cells; it does not
necessarily need to support terrain load or provide the 40 mm stroke.

#### Why it may matter

Jacquard mechanisms historically use a pattern medium, pins and hooks to control
many warp threads from shared machine motion. That separation of **selection**
from **power/motion** is directly relevant to a 6400-cell display.

If a printable selector can operate an entire row, column, module or full layer
at once, actuator count could be much lower than architectures that individually
drive each cell.

The major unresolved problem is dynamic programmability: a fixed punched plate
is useful as a proof of mechanical fan-out but is not itself an acceptable
general-purpose map programmer.

#### Cheapest discriminating test

Build a 5×5 full-pitch selector coupon with:

- 25 followers/hooks;
- one common lift stroke;
- interchangeable binary selector masks;
- several adversarial neighboring patterns.

Measure selection force, false selections, neighbor movement, reset behavior and
tolerance sensitivity. If the passive fan-out works, the next test should
replace the fixed mask with a dynamically programmable selector layer.

#### Research priority

**High.** This attacks the central actuator-count problem using a mechanism family
proven to mechanically select large numbers of outputs.

Reference inspiration: Science Museum Group documentation of Jacquard punched
cards, pins and hooks controlling which warp threads respond to the loom motion.

### R03 — bistable latch plus global lift

#### Hypothesis

Give every column a very small **passive bistable latch** while one shared lift
mechanism provides the large vertical motion.

During one or more global height passes, only selected latches change state.
After programming, the latches mechanically support the columns without powered
holding.

Multi-level terrain might be produced by repeating a global lift at several
height planes and selectively capturing/releasing cells at each plane.

#### Why it may matter

This cleanly separates three expensive functions:

1. global energy for moving the surface;
2. local selection;
3. passive load holding.

The local cell would not need a motor, screw or continuously powered actuator.
The selector only needs enough force and travel to toggle a latch.

This differs from test08 because height memory would be stored by latch state and
global height passes rather than by programming a five-sector rotor angle.

#### Cheapest discriminating test

Print several single-cell and 3×3 latch coupons at true 5.08 mm pitch. Measure:

- toggle force;
- supported vertical load;
- accidental release under lateral load and vibration;
- reset force;
- positional repeatability;
- wear and PLA creep;
- at least thousands of repeated toggles before considering scale-up.

Then test whether one shared selector motion can toggle only chosen neighboring
latches.

#### Research priority

**High.** If a tiny printable latch is reliable, it could become a reusable
building block for several different multiplexing architectures.

### R04 — ratchet / escapement height memory

#### Hypothesis

Store column height with a **rack-and-pawl, ratchet, escapement or equivalent
one-way indexed mechanism** instead of a rotary stepped cam.

A global or row-level stroke could advance selected columns by one height
increment while the pawl holds all other cells. A separate shared release action
could reset cells or allow downward movement.

The important variant is not 6400 purchased ratchets: the cell-side ratchet,
rack and pawl should be predominantly printable geometry.

#### Why it may matter

An indexed rack naturally combines discrete height memory and load support. It
could also allow the expensive actuator to make only a short repeated stroke
rather than directly position every column through its complete 40 mm range.

For five terrain levels, for example, the architecture could investigate a small
number of global increment passes plus mechanical selection instead of writing
an absolute analog position to every cell.

The main risks are pawl size at 5.08 mm pitch, release/reset complexity, noise,
wear, backlash and the possibility that one shared stroke must overcome too much
aggregate force.

#### Cheapest discriminating test

Print a one-cell rack/pawl coupon and then a 1×5 row. Test:

- tooth pitch versus achievable height resolution;
- force needed for one increment;
- holding force;
- release force;
- missed/double steps;
- reset behavior;
- neighbor cross-talk when a common drive stroke is used;
- wear over repeated cycling.

Do not proceed to a large array until a credible shared-release mechanism exists.

#### Research priority

**Medium-high.** Mechanically simple and naturally load-holding, but reset and
selective addressing may become the dominant difficulty.

### R05 — monolithic compliant bistable / multistable cell

#### Hypothesis

Replace assembled latches, springs or detents with a **3D-printed compliant
snap-through mechanism** whose geometry provides two or more stable mechanical
states.

Several bistable stages could potentially be stacked or composed to encode
multiple terrain heights. Shared motion or a selector could provide the short
trigger stroke while the compliant geometry stores the state without continuous
power.

#### Why it may matter

Compliant mechanisms can remove purchased springs, bearings, pins and fasteners
from thousands of repeated cells. Recent research demonstrates monolithic
3D-printed serial snap-through structures with programmable multistage mechanical
response.

This approach is particularly attractive for this project because printed-part
complexity is inexpensive relative to 6400 purchased components.

The risks are substantial: PLA fatigue and creep, variation in snap force,
sensitivity to print orientation and dimensions, limited space at 5.08 mm pitch,
and the need to support miniature loads without accidentally changing state.

#### Cheapest discriminating test

Create a parameter sweep of single bistable coupons that fit inside the available
cell envelope. Print multiple copies of each geometry on the actual X1C/PLA
process.

Measure:

- snap-through and reset force;
- displacement;
- dimensional variation between copies;
- stable-state holding force;
- creep under sustained load;
- cycle life;
- temperature sensitivity.

Only after a repeatable bistable element exists should a multistable stack or
array selector be designed.

#### Research priority

**High for coupon research, unproven for the final architecture.** A successful
printable mechanical bit could remove many purchased cell-level parts even if it
is eventually combined with a different addressing system.

Reference inspiration: 2026 work on monolithic 3D-printed serial snap-through
architectures using bistable von Mises truss units.

### R06 — global pressure/force field with local mechanical selection

#### Hypothesis

Keep fluidic/pneumatic ideas only in a fundamentally different form from the
earlier one-valve-per-cell concepts.

Investigate whether **one or a few global pressure chambers, membranes or other
distributed force sources** can provide bulk lifting force while purely
mechanical local selectors/latches determine which columns move or remain at a
height.

The fluid system would provide shared energy, not 6400 independently valved
positions.

#### Why it may matter

A single pressure source can distribute force over a large area with very little
moving purchased hardware. If all fine-grained state selection and holding is
mechanical, it may avoid the valve-count problem that made conventional
pneumatic architectures unattractive.

This direction should remain secondary because seals, flexible membranes,
leakage, compliance and controllability introduce failure modes that the project
would prefer to avoid.

#### Cheapest discriminating test

Do not build a valve matrix.

Instead, test a small sealed common chamber or membrane underneath a 3×3 or 5×5
mechanically latched array. Determine whether a single global pressure event can
reliably move selected cells while unselected cells remain isolated.

Stop early if leakage, membrane cross-talk, force nonuniformity or sealing effort
already makes the coupon less attractive than a purely mechanical global lift.

#### Research priority

**Low / conditional.** Keep only as a scalable shared-energy fallback. Do not
return to per-cell valves or thousands of seals without fundamentally new
evidence.


### R07 — Geneva / intermittent shared-shaft indexing

#### Hypothesis

Use a **Geneva-style or related intermittent-motion mechanism** as a module-level
mechanical sequencer. A continuously or rapidly rotating shared shaft could
produce discrete, self-indexed programming events while the driven element is
mechanically constrained between events.

The useful hypothesis is not one Geneva wheel per cell. Instead, test whether
one intermittent indexer can sequence a row, module, selector drum, clutch bank
or other shared mechanism that changes many cells per indexed event.

#### Why it may matter

Intermittent-motion mechanisms convert simple rotary input into repeatable dwell
and move phases. That could reduce sensing/homing requirements and make a
programming mechanism geometrically self-indexing.

This is materially different from test08's per-rotor angular programming: the
indexer would organize the **shared programming process**, not necessarily store
the final terrain height.

The main scaling risk is transaction count. If the architecture still needs one
indexed event per cell, it cannot meet the 30 s target. It is only interesting if
each event services a useful group of cells.

#### Cheapest discriminating test

Model a shared indexer driving 5–20 outputs or selector states, then print the
smallest module that exposes:

- dwell accuracy;
- impact/shock at realistic speed;
- missed indexes;
- backlash and wear;
- achievable cycle rate;
- how many cells can actually be affected per event.

Reject the architecture if the required number of sequential events already
makes the full-map lower-bound timing implausible.

#### Research priority

**Medium.** Valuable as a sequencing building block, but not a solution by itself.

### R08 — coded drum / combination-lock mechanical decoder

#### Hypothesis

Use **rotating coded drums, disks, pinwheels or combination-lock-like gates** to
mechanically decode a small number of shaft positions into many selectable
outputs.

Instead of commanding every cell directly, a module could contain a compact
mechanical code surface. Rotation of one or a few shared shafts would align
notches/pins/gates so that only selected followers can respond to a global lift
or programming stroke.

#### Why it may matter

Mechanical calculators, locks, automata and pattern machinery demonstrate that
rotating geometry can store or decode many discrete states with few external
inputs.

For this project, the important question is whether such a decoder can be
**rewritable quickly enough**. A fixed code drum is mechanical ROM and is not an
acceptable general map memory, but it may reveal a compact selector topology
that can be made programmable.

#### Cheapest discriminating test

Build a 1×5 or 2×5 decoder coupon with two or three independently positioned
code disks and one common actuation stroke. Test every code state and measure:

- false positives/negatives;
- required angular accuracy;
- selector force;
- neighbor interference;
- reset/reprogram time;
- sensitivity to printed clearance.

Stop if arbitrary output patterns require nearly as many independently
programmed mechanical variables as there are cells.

#### Research priority

**Medium-high.** Promising for module-level decoding; random programmability is
the key uncertainty.

### R09 — shared power shaft with selectable clutches

#### Hypothesis

Treat mechanical power like a bus: use **one or a few continuously available
rotating/linear power sources and selectively couple outputs through clutches**.

Candidate coupling principles include printed dog clutches, wrap/capstan
clutches, friction clutches, compliant engagement, or low-cost electrostatic
clutches where their voltage, fabrication and cost are acceptable.

Selection and power transmission would be separate. Multiple clutches could
engage simultaneously so one motor can actuate several outputs at once.

#### Why it may matter

Mechanical-multiplexing research has demonstrated the general principle of one
motor serving multiple degrees of freedom through selectable clutches, including
simultaneous output actuation and powerless holding when paired with
self-locking output mechanisms.

This attacks purchased motor count directly and differs from R01 because the
power source can remain stationary while a mechanical transmission network
routes its motion.

The central risks are clutch density at 5.08 mm pitch, engagement force/time,
slip, wear, routing complexity and the cost of thousands of selectors if the
clutch cannot be shared at row/module level.

#### Cheapest discriminating test

Build a four-output power-bus coupon:

- one motor/shared shaft;
- four independently selectable outputs;
- at least two outputs engaged simultaneously;
- representative output load.

Measure engagement latency, slip, transmitted torque/force, disengagement,
holding behavior, heat/wear and energy per transaction. Then calculate how many
selectors and engagements a full arbitrary 80×80 update would require.

#### Research priority

**High.** It is a fundamentally different route to reducing motor count and has
direct modern mechanical-multiplexing precedent.

Reference inspiration: Timothy E. Amish et al., *Electrostatic Clutches Enable
High-Force Mechanical Multiplexing: Demonstrating Single-Motor Full-Actuation of
a 4-DoF Hand* (2025), arXiv:2501.08469.

### R10 — cable / tendon mechanical bus

#### Hypothesis

Distribute motion through **shared cables, tendons, belts or Bowden-like members**
and use local or module-level engagement to decide which outputs receive that
motion.

The interesting version is not one dedicated cable from a motor to every cell.
It is a mechanically multiplexed bus in which relatively few tension members
serve many outputs through selectable couplers, differential routing or
row/column coincidence.

#### Why it may matter

Cable systems can move the heavy actuator away from the dense 5.08 mm cell
region. Thin flexible transmission elements may also route through modular
structures more easily than thousands of gears or motors.

The main risks are stretch, preload, friction, hysteresis, cable management,
unequal force distribution and correlated failures when one shared member jams
or loses tension.

#### Cheapest discriminating test

Build a five-output cable-bus coupon with one drive and selectable couplers.
Measure:

- displacement error under representative load;
- hysteresis and return error;
- simultaneous multi-output behavior;
- tension required to avoid slack;
- coupling/uncoupling time;
- wear after repeated cycles.

Reject dedicated-cable topologies whose cable count still grows approximately
one-for-one with 6400 cells.

#### Research priority

**Medium.** Packaging could be attractive, but routing and calibration may erase
the actuator-count advantage.

### R11 — resonance / frequency-selective mechanical addressing

#### Hypothesis

Give groups of selector elements deliberately different mechanical resonances so
that a **global vibration or oscillating drive preferentially triggers only the
elements tuned to a commanded frequency**.

The resonant element would only perform a tiny selection/release action; a
separate global lift, stored spring energy or gravity would provide the 40 mm
terrain motion.

#### Why it may matter

Frequency selection could replace some spatial wiring or mechanical routing with
a broadcast signal. In principle many selectors can receive the same excitation
while only one frequency class responds.

This is intentionally speculative. At thousands of printed elements, tolerance,
temperature, wear, load changes and mode coupling may make resonances too broad
or unstable for reliable addressing.

#### Cheapest discriminating test

Print 5–10 mechanically similar resonators designed for separated frequencies.
Drive the common frame through a sweep and measure whether one resonator can
reliably cross a latch threshold without false triggering its neighbors.

Repeat after print-to-print variation, added cell load and many cycles.

Kill the idea early if usable frequency bands overlap excessively or if enough
unique frequency channels cannot coexist with fast settling.

#### Research priority

**Low / exploratory.** Very high multiplexing upside, but unusually high
sensitivity to manufacturing variation and dynamics.

### R12 — sliding selector plate / track-and-latch matrix

#### Hypothesis

Use one or more **thin sliding plates, bars or perforated tracks** underneath a
module to create temporary mechanical paths or constraints. Orthogonal motions
could form row/column coincidence selection: a cell moves only when both its row
and column gates align.

The plates perform selection only. A global lift or shared short-stroke actuator
provides the energy and a separate latch stores height.

#### Why it may matter

A small number of long planar members can geometrically interact with many cells
at once, which is attractive at 80×80 scale. It also moves most actuator hardware
to the edge of the display.

The key question is whether arbitrary selection can be obtained without a huge
number of plate states, excessive sliding friction, or a combinatorial sequence
that violates the 30 s limit.

#### Cheapest discriminating test

Build a 5×5 full-pitch matrix with orthogonal selector strips and a common lift.
Exercise all single-cell selections plus difficult adjacent/checkerboard
patterns.

Measure selector force, false selection, plate deflection, accumulated friction,
required clearance and the number of selector transactions needed for an
arbitrary pattern.

#### Research priority

**High.** This directly explores true mechanical matrix addressing with very few
edge actuators.

### R13 — pinwheel / stepped-drum mechanical programming

#### Hypothesis

Borrow from mechanical calculators and automata: use **pinwheels, stepped drums
or selectively active teeth** to convert a compact rotary setting into a known
number of incremental output actions.

A row or module programmer could set a small number of mechanical digits/bits,
then one shared revolution would generate the required sequence of lift/release
events.

#### Why it may matter

This mechanism family separates *setting a code* from *executing a repeated
mechanical sequence*. If one programmed drum can service many cells during one
fast rotation, it could reduce expensive actuator precision and exploit printed
geometry.

It is only useful if the code-setting overhead is substantially smaller than
directly programming the cells.

#### Cheapest discriminating test

Create a drum that can represent several selectable step counts and drive five
dummy outputs. Quantify:

- code-setting time;
- output repeatability;
- maximum reliable rotation rate;
- tooth/pin size at printable scale;
- wear and missed engagements;
- number of independently programmable outputs per drum.

Compare the complete set-and-execute transaction count with direct test08-style
rotor programming.

#### Research priority

**Medium.** Strong historical precedent for compact mechanical sequencing, but
the mapping to arbitrary 2D terrain remains unproven.

### Cross-cutting research lesson

The broader mechanism survey suggests that future tests should avoid treating
"actuator", "selector", "height memory" and "load support" as one component.

Promising architectures increasingly separate these functions:

1. **power delivery** — global lift, shared shaft, cable bus or travelling head;
2. **selection/addressing** — masks, matrix strips, coded drums, clutches or
   broadcast selectors;
3. **state storage** — cam stop, latch, ratchet, compliant bistable or another
   passive memory;
4. **load support** — hard stop or self-locking structure that does not rely on
   the selector remaining energized;
5. **reset/reprogramming** — preferably global or module-parallel rather than
   one-cell-at-a-time.

Future numbered tests should therefore be allowed to combine backlog items. For
example, R12 matrix selection could be tested with R03 latches, while R09 shared
power could drive a module whose final state is held by R04 or R05.

### R14 — stacked perforated height plates

#### Hypothesis

Use several thin, aligned **planar selector plates** as passive height memory.
Each plate corresponds to one discrete stop height. A narrow follower beneath
each display column either passes through a programmed hole or stops on solid
material.

For five terrain levels (0/10/20/30/40 mm), four selector plates plus a bottom
floor are sufficient: the desired height is the first plate that does not contain
a hole at that XY position.

This is a concrete, manufacturable specialization of R02 rather than a generic
Jacquard analogy.

#### Why it may matter

The display can read the whole map mechanically with one global lift/release.
The expensive functions become plate alignment and pattern writing rather than
6400 powered height actuators. The plates can be supported by a dense printed
grid so their unsupported span is local, not 400 mm.

The main weakness is that a punched plate is cheap to read but may be slow or
consumable to write.

#### Cheapest discriminating test

Build a true-pitch 5×5 stack with four height plates and a bottom stop. Test all
five heights, checkerboards and maximum adjacent height differences. Measure
hole-edge catching, registration tolerance, plate deflection, follower friction,
repeat insertion and supported load.

#### Research priority

**High.** Very low purchased-part count and unusually simple passive readout.
The programming medium is the central unknown.

### R15 — reprogrammable planar aperture memory

#### Hypothesis

Replace destructive punched holes in R14 with reusable **shutters, tabs, sliding
strips, rotating apertures or interleaved slats** that create open/closed states
in a thin planar layer.

A separate writer programs the planar medium; the display only reads it.

#### Why it may matter

This preserves the strongest property of stacked selector plates — passive,
parallel mechanical readout — while avoiding one-use punched media.

The risk is that making every aperture reprogrammable simply recreates 6400
miniature actuators or latches in another form. A useful design must share
selection/programming hardware across many aperture states.

#### Cheapest discriminating test

Build one 5×5 reusable aperture plane and program several adversarial patterns.
Measure write time, force, state retention, false openings, reset behavior and
cycle wear. Reject variants whose purchased selector count grows approximately
one-for-one with cells.

#### Research priority

**High but conditional.** Worth pursuing only if the planar state can be written
with strongly shared hardware.

### R16 — double-buffered mechanical map cartridge

#### Hypothesis

Decouple **visible map-change time** from **map-programming time**.

Use two removable mechanical memory cartridges or pattern stacks:

1. cartridge A controls the current terrain;
2. cartridge B is programmed separately;
3. globally lift/clear the columns;
4. swap cartridges;
5. globally lower/settle the columns;
6. program the now-idle cartridge for the following map.

This can be combined with R14, R15 or another passive memory medium.

#### Why it may matter

Most candidate architectures struggle because all 6400 states must be written
inside the same 30-second user-visible transition. Double buffering changes the
system topology: the transition can be dominated by lift, swap, registration and
settling, while the next map is written during gameplay.

This is only valid when the next map is known early enough. A genuinely
unannounced arbitrary map still depends on writer throughput.

#### Cheapest discriminating test

Model the timing boundary first, then build two small cartridges. Measure
lift-clear, eject, insert, registration, lower and settle time independently from
programming time.

Also quantify how long an external writer may take if typical maps are known
5, 10, 20 or 30 minutes before the swap.

#### Research priority

**Very high as a system strategy.** It attacks the repeated system-level timing
bottleneck rather than proposing another cell actuator.

See the **Next research direction** section below for
the proposed architecture and information-throughput framing.

### R17 — independently updateable mechanical map tiles

#### Hypothesis

Partition the full display into **mechanically independent local modules** whose
height memory can be changed without resetting the rest of the board.

A module could contain 5×5, 8×8, 10×10, 16×16 or another number of display cells
and use R14/R15 planar memory internally. Only the selected module is cleared,
reprogrammed/swapped and lowered.

The module itself does not need a dedicated motor. A travelling docking head,
shared lift with selective clutch, or row/column module selector may service many
modules.

#### Why it may matter

This directly addresses exploration and fog of war. A hidden room can appear
while already revealed terrain and miniatures elsewhere remain supported.

It also improves fault isolation and makes the plastic memory medium smaller,
stiffer and easier to register than a 400×400 mm full-board sheet.

The trade-off is module frames, surface seams and a new module-selection layer.
Very small modules may recreate the original high-channel-count problem at the
module level.

#### Cheapest discriminating test

Build two adjacent true-pitch modules, initially 5×5 or 10×10 each.

Hold one module in a non-flat terrain state with representative miniature load.
Then repeatedly clear, change and settle only the neighboring module.

Measure:

- unintended displacement of the untouched module;
- vibration and cross-talk;
- update time;
- cartridge insertion/registration repeatability;
- seam behavior at maximum adjacent height differences;
- force required to select and lift one module;
- whether a miniature outside the target module can remain in place.

Then analytically sweep module sizes from 5×5 through 20×20 and include module
count, selector count, seams, update granularity, actuator cost and timing.

#### Research priority

**Very high.** Regional updates are now a product requirement, and modular
mechanical memory is the most direct way to preserve R14/R16 advantages without
forcing full-board resets.

### Research sources to revisit

These backlog entries are hypotheses, not validations. Useful starting sources
from the research pass include:

- Amish et al. (2025), *Electrostatic Clutches Enable High-Force Mechanical
  Multiplexing: Demonstrating Single-Motor Full-Actuation of a 4-DoF Hand*,
  arXiv:2501.08469.
- Santos (2026), *3D-Printed Serial Snap-Through Architectures for Programmable
  Mechanical Response*, Advanced Engineering Materials, DOI
  10.1002/adem.202502854.
- historical and modern mechanism literature on Geneva/intermittent motion,
  pinwheel calculators, combination-lock decoding, textile selectors, cable
  robotics and compliant mechanism synthesis.

### Adding future ideas

Add each new idea as R18, R19, ... with:

1. the hypothesis;
2. why existing tests do or do not already address it;
3. the cheapest test that could reject it;
4. the product-level gates it must eventually meet.

## Mechanical multiplexing research — September 2026

This document records the results of the second broad mechanism survey. It is a
research input, not a validated architecture. The detailed hypotheses live in
the **Research backlog** section above.

### Summary

The survey looked across historical and modern mechanism families including
Jacquard/textile selection, horology, mechanical calculators, printers and
coding drums, compliant mechanisms, tendon/cable systems and mechanical
multiplexing.

The recurring useful idea is to stop treating the cell actuator as one indivisible
component. The strongest mechanism families separate:

1. **selection/addressing** — decide which cells respond;
2. **power delivery** — provide motion/energy to many cells;
3. **height/state memory** — preserve the programmed state;
4. **load support** — hold miniatures without powered holding;
5. **reset/reprogramming** — preferably global or group-parallel.

### Relevant disciplines

- **Jacquard and textile machinery:** punched media and selector mechanisms can
  choose many outputs from shared machine motion.
- **Horology and intermittent-motion mechanisms:** Geneva wheels, escapements,
  detents and indexed sequencing provide repeatable mechanical states.
- **Mechanical calculators and automata:** coded drums, pinwheels and mechanical
  program media show how a small number of inputs can sequence many outputs.
- **Printer and office machinery:** travelling heads, impact pins and coded
  mechanical selection show high-cycle, repeated addressing.
- **Compliant mechanisms:** monolithic snap-through elements may provide passive
  state retention with few or no purchased cell-level parts.
- **Cable/tendon robotics:** remote power routing moves expensive actuators away
  from a dense output region.
- **Mechanical multiplexing:** shared shafts plus selectively engaged outputs
  separate the power source from output selection.

### Architecture families screened

| Family | Main advantage | Main concern |
|---|---|---|
| Jacquard-style selector | Broadcast selection; potentially very low actuator count | Dynamic reprogramming and tolerances |
| Global lift + bistable latch | One large motion source, passive cell memory | Tiny reliable latches at 5.08 mm pitch |
| Ratchet / escapement | Indexed height plus passive holding | Reset, wear and accumulated actuation force |
| Printed multistable cell | Very low purchased part count | Print variation, fatigue and creep |
| Geneva / coded drum | Self-indexed sequencing | May remain too serial |
| Shared shaft + clutch | One motor can power multiple outputs | Dense clutch/selector implementation |
| Cable / tendon bus | Remote actuation and flexible routing | Hysteresis, preload, routing and wear |
| Frequency-selective addressing | Broadcast signal can theoretically select outputs | Manufacturing variation and cross-coupling |
| Sliding selector matrix | Edge-driven mechanical row/column selection | Friction and combinatorial transaction count |
| Pinwheel / stepped drum | Compact mechanical sequencing | Arbitrary 2D programmability |

None of these was established as product-qualified. The useful output of the
survey is a broader library of selection, memory and power-routing mechanisms,
not a claim that one of them already satisfies the full product target.

### Cheap falsification experiments

The survey recommends small, mechanism-specific coupons before any full-scale
build:

- a 5×5 Jacquard/selector plate with several adversarial patterns;
- a 2×2 or 3×2 global-lift/bistable-latch coupon;
- a single ratchet cell followed by a 1×5 shared-drive row;
- a parameter sweep of printed snap-through elements;
- a small Geneva/indexer under realistic speed and load;
- a four-output shared-shaft/clutch demonstrator;
- a five-output cable/tendon bus.

These experiments should record force, displacement error, cross-talk, missed
states, reset behavior, wear and print-to-print variation.

### Interpretation

The most interesting families are those that move complexity away from purchased
cell-level hardware and into inexpensive repeated geometry. The survey therefore
supports continuing work on Jacquard-like broadcast selection, passive latching
and mechanical multiplexing, but it does not resolve the hardest combination:
**arbitrary 6400-cell programming, under 30 seconds, under the purchased-cost
limit, with sufficiently low failure probability.**

That unresolved combination motivates the next research direction:
[externalized mechanical memory and double-buffered programming](#next-research-direction--externalized-mechanical-memory-and-double-buffered-programming).

## Next research direction — externalized mechanical memory and double-buffered programming

### Why change strategy

The existing research has produced many plausible cell mechanisms, but the same
system-level bottleneck keeps returning: independently programming roughly 6400
cells quickly enough without buying thousands of actuators, selectors, sensors
or precision components.

The next research pass should therefore test a different assumption:

> **The display does not necessarily need to create the map state inside each
> cell during the visible 30-second map transition.**

Instead, investigate architectures where the terrain state is first written into
a cheap **mechanical memory medium**, then the display reads that medium with a
small number of global motions.

### Primary architecture: stacked perforated height plates

A concrete starting point is a stack of thin plastic selector plates beneath the
column array.

For a five-level terrain system (0/10/20/30/40 mm), four selector plates plus a
bottom floor are sufficient:

| Target height | 40 mm plate | 30 mm plate | 20 mm plate | 10 mm plate | Bottom |
|---|---|---|---|---|---|
| 40 mm | stop | — | — | — | — |
| 30 mm | hole | stop | — | — | — |
| 20 mm | hole | hole | stop | — | — |
| 10 mm | hole | hole | hole | stop | — |
| 0 mm | hole | hole | hole | hole | stop |

A narrow lower follower passes through programmed holes. The first plate without
a hole becomes the hard mechanical stop. The upper display column remains square;
the selector medium can therefore be much thinner and simpler than the load
surface.

This is **mechanical unary height encoding**: four binary aperture planes encode
five discrete heights.

### Why this may be interesting

- The expensive display may need only a global lift/release plus alignment.
- Height memory lives in cheap planar media rather than 6400 precision rotors or
  latches.
- The stop can be passive and hard, requiring no holding power.
- Pattern media can potentially be swapped very quickly.
- A plate can be supported by a dense printed grid so it spans only a few
  millimetres locally rather than the full 400 mm width.
- The programming system can be mechanically and physically separate from the
  display.

### The central trade-off

A disposable punched plate is cheap to *read* but potentially slow to *write*.

That suggests three distinct research branches:

#### A. Disposable or reusable punched media

Punch/cut the required holes in PET/PETG/polycarbonate/card-like sheet and insert
the four height planes. This is mechanically simple and may be very cheap, but
arbitrary map creation time and consumable material become product questions.

#### B. Reprogrammable planar memory

Replace destructive holes with reusable shutters, tabs, sliding strips,
rotating apertures or interleaved slats. A separate programmer changes these
small states; the display itself only reads the finished pattern.

#### C. Double-buffered mechanical cartridges

Use two pattern cartridges:

1. cartridge A drives the currently displayed terrain;
2. cartridge B is programmed off-line while A remains in use;
3. one global lift clears the columns;
4. cartridges swap;
5. columns lower onto the new mechanical program.

This separates **programming time** from **visible map-change time**. The 30 s
transition can then be dominated by lift, swap, alignment and lower/settle,
rather than by 6400 individual programming transactions.

The critical product question becomes whether arbitrary maps are normally known
early enough to exploit that pipeline, and whether the off-line writer can
prepare the next cartridge within the interval between map changes.

### Research questions

The next deep research/test should quantify:

- plate material, thickness, sag and creep;
- follower shape and hole-edge chamfering;
- required hole clearance at 5.08 mm pitch;
- local support-grid spacing and load capacity;
- four-sheet alignment and registration;
- manual versus motorized insertion force;
- worst-case friction with thousands of nearby followers;
- sheet/cartridge swap time;
- failure behavior if one hole is undersized or misregistered;
- whether patterned belts/tapes are better than full plates;
- whether row strips can reduce material handling;
- whether reusable shutters can be written row-parallel;
- fastest plausible low-cost mechanical writer;
- lifecycle and cost per map for consumable media;
- end-to-end timing for pre-known maps and genuinely new maps;
- local reveal timing for one and several modules;
- displacement/vibration induced in unchanged neighboring modules;
- module size versus seam count, selector count, cost and update granularity.

### New requirement: local reveals without disturbing the board

The double-buffered full-cartridge concept is not sufficient by itself.

During play, the system must be able to reveal or change **only part of the
map** while already visible terrain remains in place. This changes the preferred
topology from one monolithic mechanical memory stack toward **spatially
partitioned memory and actuation**.

#### Preferred system topology: independently readable map tiles

Partition the 80×80 display into mechanical modules, for example 8×8 or 10×10
cells per tile. A 10×10-cell tile is about 50.8×50.8 mm, giving 8×8 = 64 modules
for an 80×80 display.

Each module should have:

- its own passive planar height-memory cartridge or local aperture stack;
- mechanically independent load support from neighboring modules;
- a way to clear/lift only that module's columns;
- registration features that allow its memory medium to be replaced or
  rewritten without moving adjacent modules;
- surface geometry that keeps seams small enough for normal miniature use.

The expensive actuator does **not** need to be duplicated 64 times. Candidate
ways to service modules include:

1. a travelling lift/programming head that docks under one selected module;
2. one shared lift drive with module-selective clutches/latches;
3. row/column coincidence selection that couples the shared lift to only the
   requested module;
4. a small bank of parallel module actuators if the purchased-cost model allows
   it.

This hybrid is materially different from a full-board travelling writer. The
travelling or multiplexed hardware only needs to perform **module-level clearing
and cartridge handling**; the planar memory still determines the hundreds of
individual cell heights in parallel.

#### Why modular memory is currently more attractive than a full cartridge

A monolithic punched stack is excellent at parallel readout but poor at local
change: replacing it can require clearing the whole board.

A tiled memory system preserves most of that readout simplicity while allowing:

- one unexplored room to be revealed on demand;
- several modules to update while all others remain locked;
- pre-programmed replacement tiles for likely next areas;
- background preparation/double buffering at tile level;
- fault isolation and easier replacement of damaged parts;
- smaller, stiffer plastic sheets with easier registration.

The trade-off is additional seams, module frames and module-selection hardware.

#### Fog-of-war operating sequence

A representative reveal sequence should be:

1. existing non-target modules remain locked and load-bearing;
2. select one or more hidden target modules;
3. locally clear/lift only those columns;
4. change or rewrite the target module's mechanical memory;
5. lower/settle only the selected columns;
6. release the module-selection mechanism;
7. verify that surrounding terrain has not moved.

This sequence should not require removing miniatures from unaffected modules.

#### Recommended module-size sweep

Do not assume 10×10 is optimal. A future test should compare at least:

| Module cells | Approx. width at 5.08 mm | Module count for 80×80 |
|---:|---:|---:|
| 5×5 | 25.4 mm | 256 |
| 8×8 | 40.64 mm | 100 |
| 10×10 | 50.8 mm | 64 |
| 16×16 | 81.28 mm | 25 |
| 20×20 | 101.6 mm | 16 |

Small modules improve reveal granularity but increase frames, seams, selectors
and cartridge count. Large modules simplify hardware but disturb more already
visible terrain for each local update.

The research question is therefore not merely "can a module update locally?"
but **which module granularity minimizes total cost and disturbance while
retaining fast update speed?**

### Mechanism-independent lower-bound study

Run this in parallel with the physical concept.

For every future architecture, calculate the required **mechanical information
throughput**. A five-level 6400-cell map contains at least:

```text
6400 × log2(5) ≈ 14,860 bits
```

A 30 s arbitrary-map update therefore corresponds to roughly 495 bits/s of state
change before accounting for motion, reset, verification and error recovery.

The useful metric is not merely actuator speed, but:

- cells or state-bits changed per mechanical engagement;
- engagements per complete arbitrary map;
- purchased cost per parallel channel;
- error probability per written state;
- time hidden by pipelining/double buffering.

This should help reject mechanisms before detailed CAD if their transaction
topology cannot plausibly meet the target.

### Recommended next numbered test

The next new architecture test should be named by **domain + mechanism + question**,
for example:

`test10_planar_memory_selective_tile_lift`

Its first coupon should use **two adjacent true-pitch tiles**, initially 5×5 cells
each, with four selector planes and a bottom stop per tile. One tile remains in a
non-flat loaded state while the neighboring tile is independently lifted,
reprogrammed/swapped and lowered.

Test all five heights, adjacent height extremes, checkerboards, repeated
insertion, follower-edge catching, plate deflection and load, but also measure
motion/vibration transferred into the untouched tile.

The preferred actuation experiment is a **shared vertical power source with
selective tile coupling**, not one dedicated motor per tile. Include a simple
'all tiles' coupling mode in the analytical model so the same architecture can
support a fast full-map reset as well as local reveals.

If the two-tile coupon works, sweep 8×8, 10×10, 16×16 and 20×20 module sizes and
then build a removable 10×10 cartridge to measure actual local insertion,
selection, lift and settle time.

### Decision criterion

This direction is worth continuing only if it demonstrates a credible path to:

- reliable five-level decoding at 5.08 mm pitch;
- passive load support;
- low-cost planar media;
- a cartridge exchange comfortably inside the 30 s map-change budget;
- and a plausible method to write/rewrite pattern media without recreating the
  original 6400-actuator cost problem;
- local updates that do not require clearing the complete board or disturbing
  unrelated terrain.
