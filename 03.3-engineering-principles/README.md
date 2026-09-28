# 03.3 — Engineering principles

This stage captures transferable design logic that can appear across several mechanisms or disciplines.

Examples include global motion with local selection, passive state retention, mechanical matrix addressing, externalized mechanical memory and regional update isolation.

Principles are not complete solutions. They become useful when combined with mechanisms under the [design criteria](../02-design-criteria/) to form [Shape Display architecture candidates](../04-architecture-candidates/).

## P-005 — Double-buffered programming

### Statement
Prepare one mechanical memory medium while another controls visible terrain, then
swap them quickly.

### Caveat
This does not solve unexpected local reveals unless buffering is applied at tile
or module granularity.

## P-004 — Externalized mechanical memory

### Statement
Store terrain state in replaceable or rewriteable mechanical media rather than
inside the load-bearing cell.

### Why it matters
The display can read many states in parallel while a separate writer handles
programming.

### Caveat
Writer throughput and regional-update behavior become product constraints.

## P-008 — Functional separation

### Statement
Do not require one component to simultaneously select, move, remember and support
a cell.

Separate power delivery, addressing, state memory, load support, reset and
verification. This is a central synthesis lesson from Test08 and the broader
research.

## P-001 — Global motion with local selection

### Statement
Provide most mechanical energy globally or to a large group, while cheap local
selectors decide which outputs respond.

### Why it matters
It attacks purchased-actuator count directly.

### Caveat
The selector layer must not become thousands of expensive actuators in disguise.

## P-009 — Mechanical information throughput

### Statement
Evaluate how many independent cell states or state bits an architecture writes per
mechanical engagement and per second, not just actuator speed.

A five-level 6400-cell map contains at least about
`6400 × log2(5) ≈ 14,860 bits`, implying roughly 495 state bits/s over 30 s before
reset, motion, verification and recovery overhead.

This is a screening metric, not a complete machine model.

## P-003 — Mechanical matrix addressing

### Statement
Use row/column or other coincidence selection so a small number of control
members can address many intersections.

### Scaling consequence
An 80×80 grid suggests O(160) addressing members rather than O(6400), but only if
the intersections remain simple and arbitrary-pattern programming is fast enough.

## P-002 — Passive state retention

### Statement
After programming, geometry rather than continuous electrical power retains the
terrain state and preferably bears tabletop load.

### Caveat
Passive retention only helps if release/reset is also scalable and reliable.

## P-006 — Regional update isolation

### Statement
Update one spatial region while non-target regions remain mechanically supported,
stationary and usable with miniatures in place.

### Why it matters
Fog-of-war exploration is a product requirement.

### Evidence needed
Future tests must measure displacement and vibration transferred to untouched
regions.

## P-007 — Self-indexing and hard geometric stops

### Statement
Use geometry to seat mechanisms into discrete repeatable states instead of
depending only on open-loop motor position.

### Caveat
Wear, debris and print variation can shift the effective hard-stop state.


## P-010 — Reconfigure unlocked, carry load locked

### Statement
Perform programming or repositioning in a mechanically low-load/unlocked state,
then engage a geometric or frictional lock so service loads bypass the
programming actuator.

### Why it matters
This can separate the force and precision needed to **set** terrain from the
stiffness needed to **use** terrain. The writer may therefore be light and shared
while the completed structure is passive and load-bearing.

### Caveat
The lock itself must be cheap and dense, and unlocking one region must not disturb
neighboring terrain.

### Precedent
Reconfigurable fixture research uses lockable joints so the mechanism behaves as
a robot while moving and as a rigid structure after locking; see Lyu et al.,
*Design and Testing of a Highly Reconfigurable Fixture With Lockable Robotic
Arms*, Journal of Mechanical Design 138(8), 2016:
https://doi.org/10.1115/1.4033037
