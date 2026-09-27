# Shape-display design target

## Primary application

The goal of this project is to build a **physical Dungeons & Dragons battle-map
shape display**. Engineering decisions should therefore be judged first by
whether they help create a practical tabletop encounter map, rather than by how
well they fit a generic shape-display architecture.

The finished system should be able to raise and lower many closely packed
surface elements to form terrain, walls, stairs, pits, platforms, slopes, and
other encounter geometry while still allowing normal tabletop miniatures to be
placed and moved on top.

## Table footprint

Target an active display area of approximately **400 mm × 400 mm**.

This is a design target rather than a requirement for every prototype. Early
tests can be much smaller, but a proposed mechanism should discuss the scaling
consequences of reaching roughly this footprint.

## Horizontal resolution

Use the traditional **1-inch / 25.4 mm D&D battle-map square** as the reference
map scale.

A useful target is the ability to represent a wall or similarly narrow map
feature at about **one-fifth of one battle-map square**:

```text
25.4 mm / 5 = 5.08 mm
```

That makes **approximately 5.08 mm or finer pitch** the full-scale horizontal
resolution target.

For a 400 mm active width:

```text
400 mm / 5.08 mm ≈ 78.7
```

So the full display is likely to require on the order of **79–80 independently
height-adjustable columns per axis**, or roughly **6,200–6,400 columns total**.

This is an important scalability check. A mechanism that works beautifully for
a 5×5 prototype but cannot plausibly scale in actuator count, wiring, power,
mechanical density, speed, or cost toward this order of magnitude is not yet a
complete solution for the target application.

## Surface-element geometry

New designs should assume **square or rectangular moving columns** so neighboring
elements tile cleanly like square pixels and form a visually coherent battle-map
surface.

The word **pin** appears throughout older experiments and the current reference
template. Treat that as legacy/reference terminology, not as a requirement for a
circular cross-section. New work should prefer terms such as **column**,
**cell**, or **display element** unless it is specifically discussing a legacy
design.

## Vertical travel

The required usable height range should be **at least the full height of a
typical D&D miniature**. This gives the display enough relief to create elevation
changes that are visually and mechanically meaningful during play.

Because miniature height varies by model and scale, experiments that claim to
meet this requirement should identify a representative miniature and record its
measured height. The target should then be at least that much usable column
travel, not merely total part length.

## Map reconfiguration time

During play, changing terrain should not create a long pause at the table. The
full-scale system therefore has a **hard target of less than 30.0 seconds** to
change from one battle-map state to another.

Measure this end to end: start when the controller begins applying the new map
and stop only when all columns required by that map are in their commanded
positions, mechanically settled or locked as required, and the surface is ready
for normal play. Any reset, per-map homing or positioning, actuation, and
settling steps belong inside the 30-second budget. One-time power-on setup does
not need to count unless the mechanism requires it for every map change.

Experiments should state the workload used for timing. A partial update can be
reported as an additional useful metric, but it should not be presented as proof
of the full-map target without a justified full-scale estimate. With roughly
6,400 columns, a purely serial architecture that must independently service
every column would need to average more than about **213 column updates per
second before overhead** to meet 30 seconds. This is a scalability sanity check,
not a requirement to use any particular actuation architecture.

Small prototypes should report measured or simulated reconfiguration time and,
when relevant, a clearly stated extrapolation toward the full 400 mm × 400 mm
target.

## Component-cost envelope

The cost constraint applies to **purchased/non-3D-printed components**. Examples
include electronics, motors, servos, steppers, bearings, guide rods, sensors,
PCBs, connectors, power supplies, fasteners, and other bought-in hardware.

| Purchased component cost | Interpretation |
| --- | --- |
| **< $200** | Ideal target |
| **$200–$400** | Acceptable |
| **$400–$500** | Last resort; avoid if a credible lower-cost design exists |
| **> $500** | Unacceptable |

### 3D-printed parts

There is **no design cost ceiling for 3D-printed parts** in this project.
Printable geometry can therefore be used aggressively when it replaces purchased
mechanisms or simplifies assembly. Do not reject an otherwise strong design
because it requires a large amount of printable structure.

This exception is intentional: the practical decision constraint is the cost of
hardware that must be bought, not a modeled commercial price for parts that can
be printed at home.

## How to compare engineering concepts

When evaluating a mechanism, explicitly discuss how it affects:

1. **D&D usefulness:** can it represent encounter terrain and still support
   miniatures?
2. **Resolution:** can it approach ~5.08 mm pitch at useful scale?
3. **Table size:** can it scale toward ~400 mm × 400 mm without becoming
   impractical?
4. **Vertical travel:** can it reach at least one representative miniature
   height?
5. **Surface quality:** do square/rectangular columns tile with small, controlled
   gaps?
6. **Purchased-component cost:** where does the full design land in the cost
   bands above?
7. **Scalability:** what happens around ~6,400 elements, especially for
   actuation, locking, wiring, power, and control complexity?
8. **Reconfiguration time:** can a complete new battle map become playable in
   **less than 30 seconds** at full target scale, including required reset,
   positioning, actuation, and settling?
9. **Buildability and reliability:** can it actually be fabricated, assembled,
   calibrated, maintained, and used repeatedly?

A prototype does not need to satisfy every full-scale target immediately. Its
documentation should make clear which target it tests and what remains unsolved.
