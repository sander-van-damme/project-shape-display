# 03.2 — Engineering mechanisms

This stage extracts concrete reusable mechanisms from the disciplines in 03.1.

Each mechanism section should explain what the mechanism does, where it is used, what it solves well, what it does not solve, important parameters, known failure modes, fabrication implications and the hypothesis for transferring it to the Shape Display.

The next step is to abstract reusable [engineering principles](../03.3-engineering-principles/) and combine mechanisms into [architecture candidates](../04-architecture-candidates/).

## M-003 — Bistable mechanical latch

### Core principle
A mechanism has two stable states and changes only after crossing a mechanical
threshold.

### What it solves well
Passive state retention and potentially passive load support.

### What it does not solve
Addressing and programming energy remain external.

### Key risks
Toggle-force variation, creep, accidental release and manufacturing consistency
at 5.08 mm pitch.

### Cheapest discriminating experiment
Single-cell and 3×3 coupons measuring toggle force, holding load, repeatability
and cycle wear.

## M-009 — Cable / tendon mechanical bus

### Core principle
Remote actuators transmit force through flexible tension members, optionally with
shared or selectable couplers.

### What it solves well
Moves bulky hardware away from the dense cell region.

### What it does not solve
Dedicated one-cable-per-cell routing does not scale; selection must itself be
multiplexed.

### Key risks
Stretch, preload, friction, hysteresis and cable management.

### Cheapest discriminating experiment
Five outputs on one shared bus with selectable coupling; measure displacement
error and hysteresis under load.

## M-007 — Coded drum / pinwheel mechanical decoder

### Core principle
Rotating notches, pins or selectively active teeth mechanically encode or decode
state and sequence.

### What it solves well
Compact program representation and repeated sequencing.

### What it does not solve
Historic implementations are often read-only or slow to rewrite.

### Cheapest discriminating experiment
A small drum encoding selectable step counts and five dummy outputs; compare
code-setting overhead with direct programming.

## M-005 — Compliant snap-through multistable cell

### Core principle
Elastic geometry snaps between stable configurations without conventional
bearings or assembled springs.

### What it solves well
Potentially eliminates purchased cell-level memory parts.

### What it does not solve
Shared addressing and long-stroke energy delivery remain external.

### Key risks
PLA creep/fatigue, temperature, print variation and snap-force spread.

### Cheapest discriminating experiment
A replicated parameter sweep measuring snap force, stable displacement, creep and
cycle life.

## M-010 — Frequency-selective mechanical resonator

### Core principle
Elements with intentionally different resonances receive a common oscillatory
input while only the tuned class crosses a trigger threshold.

### What it solves well
Potential broadcast addressing with little spatial routing.

### What it does not solve
It supplies only a selection event; long-stroke motion and stable load support
must come from elsewhere.

### Key risks
Tolerance drift, modal coupling, load sensitivity and settling time.

### Cheapest discriminating experiment
5–10 printed resonators with separated targets, tested before and after added
load and print-to-print variation.

## M-006 — Geneva / intermittent-motion indexer

### Core principle
Input motion is converted into discrete indexed steps with dwell periods.

### What it solves well
Deterministic sequencing and geometric indexing.

### What it does not solve
Used one event per cell it remains too serial; it needs a group-level role.

### Cheapest discriminating experiment
A shared indexer driving 5–20 selector states at realistic speed and load.

## M-002 — Jacquard-style broadcast selector

### Core principle
A pattern medium or selector layer decides which members of a repeated array
respond to one shared motion.

### What it solves well
Large-scale selection with little local power.

### What it does not solve
It does not inherently provide dynamic rewriting, 40 mm motion or load support.

### Cheapest discriminating experiment
A 5×5 selector coupon with adversarial adjacent patterns and one common stroke.

## M-013 — Stacked perforated height plate

### Core principle
Aligned planar stop layers encode height by first obstruction: a follower passes
through holes until it reaches the first solid layer.

For five terrain levels, four binary aperture planes plus a bottom stop can encode
0/10/20/30/40 mm.

### What it solves well
Parallel passive readout, cheap planar memory and potentially hard load support.

### What it does not solve
The pattern still needs a fast write/rewrite method, and full-board sheets are
poor for local fog-of-war updates.

### Cheapest discriminating experiment
Two adjacent 5×5 tile stacks; repeatedly change one while measuring disturbance,
registration, edge catching and load in the untouched tile.

## M-004 — Ratchet / pawl / escapement height memory

### Core principle
An indexed member moves incrementally while a pawl prevents reverse motion until
release.

### What it solves well
Discrete position memory, indexing and load support.

### What it does not solve
Selective addressing and fast scalable reset remain separate problems.

### Cheapest discriminating experiment
One cell followed by a 1×5 shared-drive row; measure missed/double steps, holding
force, release force and wear.

## M-014 — Reprogrammable planar aperture layer

### Core principle
Reusable shutters, tabs, sliding strips, rotating apertures or compliant features
replace destructive punched holes in a planar memory layer.

### What it solves well
Retains parallel planar readout while allowing repeated programming.

### What it does not solve
If every aperture needs its own bought actuator, the architecture recreates the
original 6400-channel problem.

### Cheapest discriminating experiment
One 5×5 reusable aperture plane, written through shared hardware, with adversarial
patterns and cycle testing.

## M-012 — Rotary stepped stop / cam memory

### Core principle
A small rotor presents one of several discrete support heights to a follower.

### What it solves well
Compact passive multi-level memory and hard load support.

### Project evidence
Test08 found five levels geometrically plausible and a conditional 26.25 s
full-map schedule with an 80-channel programming head. Test09 reproduced timing
but exposed unresolved detent, coupling, sourcing and structural gates.

### What it does not solve
The rotor still needs fast reliable programming and return motion.

### Decision state
Worth mechanism-level study, but not product-qualified.

## M-015 — Shared pressure / global force source

### Core principle
One or a few global pressure chambers or membranes provide bulk force while local
mechanical selectors determine which elements respond.

### What it solves well
Potentially distributes force with very few bought actuators.

### What it does not solve
Selection and state retention remain separate.

### Project warning
Conventional per-cell pneumatic valves/plumbing are poor fits because of leakage,
sealing and component count. Keep only architectures that avoid those scaling
modes.

## M-008 — Shared shaft with selectable clutches

### Core principle
A common power bus is selectively coupled to outputs through clutches.

### What it solves well
Reduces motor count and can power several outputs simultaneously.

### What it does not solve
The clutch/selector itself must be cheap and dense enough not to recreate the
cost problem.

### Cheapest discriminating experiment
One motor and four independently selected loaded outputs; measure engagement,
slip, torque and wear.

## M-011 — Sliding selector plate / matrix

### Core principle
Thin sliding bars or plates create temporary mechanical paths or constraints.
Orthogonal row/column motion can form coincidence selection.

### What it solves well
Many intersections can be addressed from a small number of edge actuators.

### What it does not solve
State retention and power delivery are separate.

### Key risks
Accumulated friction, plate deflection, combinatorial transactions and clearance.

### Cheapest discriminating experiment
A 5×5 orthogonal selector matrix plus common lift, including checkerboard and
single-cell patterns.

## M-001 — Travelling multi-row programming head

### Core principle
Move a shared head between row groups and change several rows and/or columns
during each dwell.

### What it solves well
Concentrates precision and active hardware in one serviceable assembly.

### What it does not solve
Passive height memory and load support still need another mechanism.

### Project evidence
Test09 screened 1–5 rows and 20/40/80 parallel columns. Four/five full-width
shared rows retain conditional timing windows, but selector cost and loaded
dynamics remain unqualified.

### Cheapest discriminating experiment
A 2×4 full-pitch dynamically selected head/latch coupon with measured loaded
engagement and repeatability.
