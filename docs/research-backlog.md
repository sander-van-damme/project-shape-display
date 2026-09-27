# Research backlog

This file records engineering ideas that are worth testing but are **not yet
validated project architectures**. An idea belongs here when it is plausible
enough to deserve a quantitative or physical test, even if a related earlier
architecture performed poorly.

A backlog entry should only move to "rejected" after its specific hypothesis has
been tested against the current design target. Earlier tests are evidence, not a
blanket rejection of every variant in the same family.

## R01 — high-speed travelling multi-row actuator

### Hypothesis

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

### Why it may matter

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

### Test proposal

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

### Physical decision gate

If the analytical sweep produces a credible region, build only the smallest
full-pitch coupon/head that tests the bottleneck. Measure loaded actuation time
and repeatability instead of extrapolating from no-load motor speed.

Keep this research direction open unless quantitative timing, packaging, cost or
reliability bounds rule it out.


## R02 — Jacquard-style broadcast selector

### Hypothesis

Borrow the central idea from Jacquard textile machinery: a **single selector
operation can decide which members of a dense array respond to a shared motion**.

For this project, do not interpret that narrowly as "swap a punched card for
every D&D map". The useful research question is whether a thin mechanical
selection layer — plate, pins, hooks, sliding bars, orthogonal selector strips or
another programmable mask — can select many cells simultaneously while a global
lift or programming stroke supplies the actual energy.

A selector only needs to distinguish selected from unselected cells; it does not
necessarily need to support terrain load or provide the 40 mm stroke.

### Why it may matter

Jacquard mechanisms historically use a pattern medium, pins and hooks to control
many warp threads from shared machine motion. That separation of **selection**
from **power/motion** is directly relevant to a 6400-cell display.

If a printable selector can operate an entire row, column, module or full layer
at once, actuator count could be much lower than architectures that individually
drive each cell.

The major unresolved problem is dynamic programmability: a fixed punched plate
is useful as a proof of mechanical fan-out but is not itself an acceptable
general-purpose map programmer.

### Cheapest discriminating test

Build a 5×5 full-pitch selector coupon with:

- 25 followers/hooks;
- one common lift stroke;
- interchangeable binary selector masks;
- several adversarial neighboring patterns.

Measure selection force, false selections, neighbor movement, reset behavior and
tolerance sensitivity. If the passive fan-out works, the next test should
replace the fixed mask with a dynamically programmable selector layer.

### Research priority

**High.** This attacks the central actuator-count problem using a mechanism family
proven to mechanically select large numbers of outputs.

Reference inspiration: Science Museum Group documentation of Jacquard punched
cards, pins and hooks controlling which warp threads respond to the loom motion.

## R03 — bistable latch plus global lift

### Hypothesis

Give every column a very small **passive bistable latch** while one shared lift
mechanism provides the large vertical motion.

During one or more global height passes, only selected latches change state.
After programming, the latches mechanically support the columns without powered
holding.

Multi-level terrain might be produced by repeating a global lift at several
height planes and selectively capturing/releasing cells at each plane.

### Why it may matter

This cleanly separates three expensive functions:

1. global energy for moving the surface;
2. local selection;
3. passive load holding.

The local cell would not need a motor, screw or continuously powered actuator.
The selector only needs enough force and travel to toggle a latch.

This differs from test08 because height memory would be stored by latch state and
global height passes rather than by programming a five-sector rotor angle.

### Cheapest discriminating test

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

### Research priority

**High.** If a tiny printable latch is reliable, it could become a reusable
building block for several different multiplexing architectures.

## R04 — ratchet / escapement height memory

### Hypothesis

Store column height with a **rack-and-pawl, ratchet, escapement or equivalent
one-way indexed mechanism** instead of a rotary stepped cam.

A global or row-level stroke could advance selected columns by one height
increment while the pawl holds all other cells. A separate shared release action
could reset cells or allow downward movement.

The important variant is not 6400 purchased ratchets: the cell-side ratchet,
rack and pawl should be predominantly printable geometry.

### Why it may matter

An indexed rack naturally combines discrete height memory and load support. It
could also allow the expensive actuator to make only a short repeated stroke
rather than directly position every column through its complete 40 mm range.

For five terrain levels, for example, the architecture could investigate a small
number of global increment passes plus mechanical selection instead of writing
an absolute analog position to every cell.

The main risks are pawl size at 5.08 mm pitch, release/reset complexity, noise,
wear, backlash and the possibility that one shared stroke must overcome too much
aggregate force.

### Cheapest discriminating test

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

### Research priority

**Medium-high.** Mechanically simple and naturally load-holding, but reset and
selective addressing may become the dominant difficulty.

## R05 — monolithic compliant bistable / multistable cell

### Hypothesis

Replace assembled latches, springs or detents with a **3D-printed compliant
snap-through mechanism** whose geometry provides two or more stable mechanical
states.

Several bistable stages could potentially be stacked or composed to encode
multiple terrain heights. Shared motion or a selector could provide the short
trigger stroke while the compliant geometry stores the state without continuous
power.

### Why it may matter

Compliant mechanisms can remove purchased springs, bearings, pins and fasteners
from thousands of repeated cells. Recent research demonstrates monolithic
3D-printed serial snap-through structures with programmable multistage mechanical
response.

This approach is particularly attractive for this project because printed-part
complexity is inexpensive relative to 6400 purchased components.

The risks are substantial: PLA fatigue and creep, variation in snap force,
sensitivity to print orientation and dimensions, limited space at 5.08 mm pitch,
and the need to support miniature loads without accidentally changing state.

### Cheapest discriminating test

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

### Research priority

**High for coupon research, unproven for the final architecture.** A successful
printable mechanical bit could remove many purchased cell-level parts even if it
is eventually combined with a different addressing system.

Reference inspiration: 2026 work on monolithic 3D-printed serial snap-through
architectures using bistable von Mises truss units.

## R06 — global pressure/force field with local mechanical selection

### Hypothesis

Keep fluidic/pneumatic ideas only in a fundamentally different form from the
earlier one-valve-per-cell concepts.

Investigate whether **one or a few global pressure chambers, membranes or other
distributed force sources** can provide bulk lifting force while purely
mechanical local selectors/latches determine which columns move or remain at a
height.

The fluid system would provide shared energy, not 6400 independently valved
positions.

### Why it may matter

A single pressure source can distribute force over a large area with very little
moving purchased hardware. If all fine-grained state selection and holding is
mechanical, it may avoid the valve-count problem that made conventional
pneumatic architectures unattractive.

This direction should remain secondary because seals, flexible membranes,
leakage, compliance and controllability introduce failure modes that the project
would prefer to avoid.

### Cheapest discriminating test

Do not build a valve matrix.

Instead, test a small sealed common chamber or membrane underneath a 3×3 or 5×5
mechanically latched array. Determine whether a single global pressure event can
reliably move selected cells while unselected cells remain isolated.

Stop early if leakage, membrane cross-talk, force nonuniformity or sealing effort
already makes the coupon less attractive than a purely mechanical global lift.

### Research priority

**Low / conditional.** Keep only as a scalable shared-energy fallback. Do not
return to per-cell valves or thousands of seals without fundamentally new
evidence.


## R07 — Geneva / intermittent shared-shaft indexing

### Hypothesis

Use a **Geneva-style or related intermittent-motion mechanism** as a module-level
mechanical sequencer. A continuously or rapidly rotating shared shaft could
produce discrete, self-indexed programming events while the driven element is
mechanically constrained between events.

The useful hypothesis is not one Geneva wheel per cell. Instead, test whether
one intermittent indexer can sequence a row, module, selector drum, clutch bank
or other shared mechanism that changes many cells per indexed event.

### Why it may matter

Intermittent-motion mechanisms convert simple rotary input into repeatable dwell
and move phases. That could reduce sensing/homing requirements and make a
programming mechanism geometrically self-indexing.

This is materially different from test08's per-rotor angular programming: the
indexer would organize the **shared programming process**, not necessarily store
the final terrain height.

The main scaling risk is transaction count. If the architecture still needs one
indexed event per cell, it cannot meet the 30 s target. It is only interesting if
each event services a useful group of cells.

### Cheapest discriminating test

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

### Research priority

**Medium.** Valuable as a sequencing building block, but not a solution by itself.

## R08 — coded drum / combination-lock mechanical decoder

### Hypothesis

Use **rotating coded drums, disks, pinwheels or combination-lock-like gates** to
mechanically decode a small number of shaft positions into many selectable
outputs.

Instead of commanding every cell directly, a module could contain a compact
mechanical code surface. Rotation of one or a few shared shafts would align
notches/pins/gates so that only selected followers can respond to a global lift
or programming stroke.

### Why it may matter

Mechanical calculators, locks, automata and pattern machinery demonstrate that
rotating geometry can store or decode many discrete states with few external
inputs.

For this project, the important question is whether such a decoder can be
**rewritable quickly enough**. A fixed code drum is mechanical ROM and is not an
acceptable general map memory, but it may reveal a compact selector topology
that can be made programmable.

### Cheapest discriminating test

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

### Research priority

**Medium-high.** Promising for module-level decoding; random programmability is
the key uncertainty.

## R09 — shared power shaft with selectable clutches

### Hypothesis

Treat mechanical power like a bus: use **one or a few continuously available
rotating/linear power sources and selectively couple outputs through clutches**.

Candidate coupling principles include printed dog clutches, wrap/capstan
clutches, friction clutches, compliant engagement, or low-cost electrostatic
clutches where their voltage, fabrication and cost are acceptable.

Selection and power transmission would be separate. Multiple clutches could
engage simultaneously so one motor can actuate several outputs at once.

### Why it may matter

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

### Cheapest discriminating test

Build a four-output power-bus coupon:

- one motor/shared shaft;
- four independently selectable outputs;
- at least two outputs engaged simultaneously;
- representative output load.

Measure engagement latency, slip, transmitted torque/force, disengagement,
holding behavior, heat/wear and energy per transaction. Then calculate how many
selectors and engagements a full arbitrary 80×80 update would require.

### Research priority

**High.** It is a fundamentally different route to reducing motor count and has
direct modern mechanical-multiplexing precedent.

Reference inspiration: Timothy E. Amish et al., *Electrostatic Clutches Enable
High-Force Mechanical Multiplexing: Demonstrating Single-Motor Full-Actuation of
a 4-DoF Hand* (2025), arXiv:2501.08469.

## R10 — cable / tendon mechanical bus

### Hypothesis

Distribute motion through **shared cables, tendons, belts or Bowden-like members**
and use local or module-level engagement to decide which outputs receive that
motion.

The interesting version is not one dedicated cable from a motor to every cell.
It is a mechanically multiplexed bus in which relatively few tension members
serve many outputs through selectable couplers, differential routing or
row/column coincidence.

### Why it may matter

Cable systems can move the heavy actuator away from the dense 5.08 mm cell
region. Thin flexible transmission elements may also route through modular
structures more easily than thousands of gears or motors.

The main risks are stretch, preload, friction, hysteresis, cable management,
unequal force distribution and correlated failures when one shared member jams
or loses tension.

### Cheapest discriminating test

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

### Research priority

**Medium.** Packaging could be attractive, but routing and calibration may erase
the actuator-count advantage.

## R11 — resonance / frequency-selective mechanical addressing

### Hypothesis

Give groups of selector elements deliberately different mechanical resonances so
that a **global vibration or oscillating drive preferentially triggers only the
elements tuned to a commanded frequency**.

The resonant element would only perform a tiny selection/release action; a
separate global lift, stored spring energy or gravity would provide the 40 mm
terrain motion.

### Why it may matter

Frequency selection could replace some spatial wiring or mechanical routing with
a broadcast signal. In principle many selectors can receive the same excitation
while only one frequency class responds.

This is intentionally speculative. At thousands of printed elements, tolerance,
temperature, wear, load changes and mode coupling may make resonances too broad
or unstable for reliable addressing.

### Cheapest discriminating test

Print 5–10 mechanically similar resonators designed for separated frequencies.
Drive the common frame through a sweep and measure whether one resonator can
reliably cross a latch threshold without false triggering its neighbors.

Repeat after print-to-print variation, added cell load and many cycles.

Kill the idea early if usable frequency bands overlap excessively or if enough
unique frequency channels cannot coexist with fast settling.

### Research priority

**Low / exploratory.** Very high multiplexing upside, but unusually high
sensitivity to manufacturing variation and dynamics.

## R12 — sliding selector plate / track-and-latch matrix

### Hypothesis

Use one or more **thin sliding plates, bars or perforated tracks** underneath a
module to create temporary mechanical paths or constraints. Orthogonal motions
could form row/column coincidence selection: a cell moves only when both its row
and column gates align.

The plates perform selection only. A global lift or shared short-stroke actuator
provides the energy and a separate latch stores height.

### Why it may matter

A small number of long planar members can geometrically interact with many cells
at once, which is attractive at 80×80 scale. It also moves most actuator hardware
to the edge of the display.

The key question is whether arbitrary selection can be obtained without a huge
number of plate states, excessive sliding friction, or a combinatorial sequence
that violates the 30 s limit.

### Cheapest discriminating test

Build a 5×5 full-pitch matrix with orthogonal selector strips and a common lift.
Exercise all single-cell selections plus difficult adjacent/checkerboard
patterns.

Measure selector force, false selection, plate deflection, accumulated friction,
required clearance and the number of selector transactions needed for an
arbitrary pattern.

### Research priority

**High.** This directly explores true mechanical matrix addressing with very few
edge actuators.

## R13 — pinwheel / stepped-drum mechanical programming

### Hypothesis

Borrow from mechanical calculators and automata: use **pinwheels, stepped drums
or selectively active teeth** to convert a compact rotary setting into a known
number of incremental output actions.

A row or module programmer could set a small number of mechanical digits/bits,
then one shared revolution would generate the required sequence of lift/release
events.

### Why it may matter

This mechanism family separates *setting a code* from *executing a repeated
mechanical sequence*. If one programmed drum can service many cells during one
fast rotation, it could reduce expensive actuator precision and exploit printed
geometry.

It is only useful if the code-setting overhead is substantially smaller than
directly programming the cells.

### Cheapest discriminating test

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

### Research priority

**Medium.** Strong historical precedent for compact mechanical sequencing, but
the mapping to arbitrary 2D terrain remains unproven.

## Cross-cutting research lesson

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

## Research sources to revisit

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

## Adding future ideas

Add each new idea as R14, R15, ... with:

1. the hypothesis;
2. why existing tests do or do not already address it;
3. the cheapest test that could reject it;
4. the product-level gates it must eventually meet.
