# 02 — Design criteria

This stage translates the broad project description into the constraints that engineering work must design and test against. All accepted design criteria, scale assumptions, fabrication context, and qualification guidance live in this single document.

## Product design target

### Primary application

The goal of this project is to build a **physical Dungeons & Dragons battle-map
shape display**. Engineering decisions should therefore be judged first by
whether they help create a practical tabletop encounter map, rather than by how
well they fit a generic shape-display architecture.

The finished system should be able to raise and lower many closely packed
surface elements to form terrain, walls, stairs, pits, platforms, slopes, and
other encounter geometry while still allowing normal tabletop miniatures to be
placed and moved on top.

### Table footprint

Target an active display area of approximately **400 mm × 400 mm**.

This is a design target rather than a requirement for every prototype. Early
tests can be much smaller, but a proposed mechanism should discuss the scaling
consequences of reaching roughly this footprint.

### Horizontal resolution

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

**This is a column-count requirement, not a per-cell mechanism-size budget.** A
5.08 mm surface pitch does not require the selection, memory, locking or
programming machinery to fit inside each 5.08 mm cell; see **Surface pitch does
not constrain the internal mechanism** below. Column *tops* honor the pitch;
internal precision machinery should be as large, shared, sparse, external or
modular as the product allows.

This is an important scalability check. A mechanism that works beautifully for
a 5×5 prototype but cannot plausibly scale in actuator count, wiring, power,
mechanical density, speed, or cost toward this order of magnitude is not yet a
complete solution for the target application.

### Surface-element geometry

New designs should assume **square or rectangular moving columns** so neighboring
elements tile cleanly like square pixels and form a visually coherent battle-map
surface.

The word **pin** appears throughout older experiments and the current reference
template. Treat that as legacy/reference terminology, not as a requirement for a
circular cross-section. New work should prefer terms such as **column**,
**cell**, or **display element** unless it is specifically discussing a legacy
design.

### Vertical travel

The required usable height range should be **at least the full height of a
typical D&D miniature**. Current market references put normal human-sized
tabletop figures roughly in the 28–35 mm range depending on 28/32 mm scale,
measurement convention and sculpt.

Use **40 mm as the provisional minimum usable vertical travel** for architecture
work. It provides margin above that normal humanoid range without trying to size
the terrain stroke around unusually tall monsters, wings or raised weapons.

A design does not become qualified solely because its CAD contains 40 mm of
nominal travel. Experiments that claim compliance should identify a
representative physical D&D miniature, measure it from the bottom of the base to
its highest normal body/head feature, and verify that usable travel exceeds that
measurement. If the representative miniature is taller than 40 mm, update the
requirement and rerun affected timing, load and packaging calculations.

The research basis and measurement convention are documented in the **Miniature dimensions and vertical-travel basis** section below.

### Complete-map reconfiguration

During play, changing terrain should not create a long pause at the table. The
full-scale system therefore has a **hard target of strictly less than 30.0
seconds** to change from one battle-map state to another at the approximately
80×80 (~6,400-column) scale.

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

### Regional / on-demand updates

The battle map must support **partial, local terrain updates during play**.

A common D&D case is exploration or fog of war: part of the map is not yet
revealed, and when the party reaches that area the system should be able to
materialize only that region without unnecessarily resetting or disturbing
terrain that is already visible.

A viable architecture should therefore support updates to an arbitrary subset or
contiguous region of cells with these properties:

- unchanged cells should remain mechanically supported and should not require a
  deliberate reset, homing cycle or full-map lift;
- the update mechanism should minimize visible motion, vibration and accidental
  displacement outside the target region;
- miniatures and terrain already placed outside the target region should not need
  to be removed for a normal local reveal;
- partial-update time must remain below the full-map **30 s** cap and should
  ideally scale with the size of the affected region rather than with all 6400
  cells;
- experiments must explicitly report the disturbance induced in neighboring and
  non-target cells;
- any architecture that requires a full-board reset for every small reveal must
  identify that as a product-level weakness.

No stricter numeric local-update time is fixed yet. Future tests should measure
representative reveal workloads (for example one room, corridor, 10×10-cell
module and several separated regions) before a lower target is set.

**Trade-off against architecture simplicity.** Regional updates remain valuable
but are **not** a licence to add thousands of microscopic per-cell mechanisms.
Where a shared-mechanism or mask-based architecture supports only coarse
bank-local / segment-level / mask-strip updates rather than true arbitrary-subset
updates, that is an acceptable simplification **provided the trade-off is
quantified and surfaced as an explicit product decision**. Candidate mask
approaches worth evaluating include bank-local updates, replacing only one mask
segment, multiple independent mask strips, partial replay, and modular terrain
regions. Prefer the simplest mechanism that preserves practical fog-of-war use.

### Fabrication baseline

Prototype and small-batch fabrication is expected to use a **Bambu Lab X1
Carbon**, normally with **PLA**. The printer supports 0.4 mm and optional 0.2 mm
nozzles, but published printer specifications do not provide a universal
finished-part dimensional tolerance.

Mechanisms at the 5.08 mm pitch must therefore validate critical clearances with
physical calibration coupons on the actual printer/material process. Do not
treat fine motion or lidar sensor resolution as equivalent to printed-part
accuracy.

The ~400 mm map is larger than the X1C build volume and should be designed as
modular printable cartridges/tiles rather than a single monolithic print.

Detailed printer, nozzle, material and qualification guidance is documented in the **Fabrication context** section below.

### Component-cost envelope

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

### How to compare engineering concepts

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
9. **Regional updates:** can part of the map be revealed or changed without a
   full-board reset or disturbing unrelated terrain?
10. **Buildability and reliability:** can it actually be fabricated, assembled,
    calibrated, maintained, and used repeatedly? Run the **Repeated-mechanism
    reliability criteria** and per-architecture reliability audit below; answer
    the gate question "what has to work correctly 6,400 times?" and minimize it.
11. **Prototype testability:** can the repeated mechanism be validated in a small
    coupon before scaling (see **Prototype ladder requirement** below)?

Items 10 and 11 are **gates**, not tie-breakers: a design that wins on
spreadsheet cost, pitch or timing but loses on repeated-mechanism reliability is
not a viable product.

A prototype does not need to satisfy every full-scale target immediately. Its
documentation should make clear which target it tests and what remains unsolved.

## Surface pitch does not constrain the internal mechanism (reliability-first rule)

The 5.08 mm figure is a **visible surface resolution** requirement. It is the
center-to-center spacing of the columns that form the terrain, so that map
features tile like square pixels.

It is **not** a requirement that the selection, memory, locking, reset or
programming machinery physically fit inside a single 5.08 × 5.08 mm cell
footprint. Treating surface pitch as an internal mechanism-size budget is the
single most damaging pattern observed in earlier architecture work: it forces
sub-millimetre pawls, keepers, springs, teeth and clearances that are
theoretically printable but unlikely to be reliable when repeated ~6,400 times.

Mechanisms may live:

- underneath several cells;
- beside the display;
- at row / bank / module level;
- in a moving external mechanism;
- in a replaceable mask;
- in a tape, card or film;
- in a separate mask-generation subsystem.

**Rule:** keep the dense visible surface at its required pitch, and make the
precision machinery controlling it **as large, shared, sparse, external, or
modular as the product allows**. Design at whatever scale makes the repeated
mechanism robust; only the column *top* needs to honor the surface pitch.

Explicitly prefer, as a program principle:

> **Thousands of simple things + a few sophisticated shared mechanisms.**

and reject:

> Thousands of tiny sophisticated mechanisms that happen to fit in CAD.

This applies regardless of whether the machine is mask-based. Any architecture
that pushes precision, compliance or tolerance-critical interaction into every
cell should be challenged and justified against a shared-mechanism alternative.

## Repeated-mechanism reliability criteria

Reliability and real-world buildability are **first-class design gates**, not
tie-breakers. An architecture that passes analytic, CAD, cost and pitch gates can
still be the wrong answer if it depends on thousands of fragile micro-mechanisms.

For every architecture, answer this gate question explicitly:

> **What has to work correctly 6,400 times?**

Minimize that answer. An architecture with one complicated but accessible shared
mechanism and 6,400 extremely simple passive columns is generally preferable to
one with 6,400 sophisticated per-cell mechanisms.

### Strongly discouraged

- Critical moving features that are a single extrusion line wide.
- Tiny printed springs whose **exact force** determines correctness.
- Sub-millimetre precision interactions repeated thousands of times.
- Friction-sensitive state retention where a **positive hard stop** is possible.
- Mechanisms that require extremely tight tolerances across all 6,400 cells.
- Architectures where one **silent microscopic failure** yields an incorrect
  cell with no practical recovery or detection path.

### Preferred

- Large positive engagement features (pins in slots, teeth of generous module,
  pegs in detents) rather than relying on friction.
- Hard stops and mechanical end-of-travel rather than force balance.
- Compression-loaded structures rather than tiny bending members.
- Generous clearances that tolerate normal FDM print variation.
- Replaceable modules and accessible wear parts.
- Repeated parts that can be tested individually as a coupon.
- Architecture-level redundancy or an explicit error-recovery / re-home path.

### Per-architecture reliability audit (required)

Report, with an evidence class for each:

1. Number of repeated moving parts.
2. Number of precision contacts **per cell**.
3. Number of compliant printed elements.
4. Number of wear interfaces (and their expected service life).
5. Number of tolerance-sensitive interactions.
6. Likely **correlated** failure modes (one cause taking out many cells).
7. Likely **single-cell** failure modes.
8. Serviceability: can a failed cell or wear part be reached and replaced?

Prefer failure modes that are **detectable, recoverable, local and repairable**.
Avoid designs where a hidden latch silently fails and can never be found.

### Provisional design rule for minimum repeatable feature size

Where a numerical minimum feature size cannot be honestly established without
physical testing, define a conservative engineering rule and **clearly label it
provisional**. Do not invent false precision around printer tolerances:

- Bambu's 7 µm lidar figure is a sensor specification, not a part tolerance.
- Published X1C specifications do **not** give a universal finished-part
  dimensional tolerance.
- Any claimed minimum feature or clearance is a **provisional design rule**
  until a calibration-coupon batch on the actual X1C + PLA process confirms it.

## Mask subsystem and honest timing

The mask generator is **part of the machine, not an external assumption**. If an
architecture relies on a physical mask, tape, film or comb, the subsystem that
produces it is inside the product boundary and must be designed, costed, timed
and tested alongside the display.

Mask-selection medium may be disposable, reusable, rewritable, continuously
generated, cassette-stored, or generated while the previous terrain is
displayed. All of these are in scope and should be compared quantitatively.

### Timing decomposition (report every stage)

Full arbitrary-map change must still target **< 30 s**, reported honestly. Do not
claim a fast arbitrary-map update while hiding substantial mask preparation.
Report each stage separately:

1. Digital map processing.
2. Physical mask generation.
3. Mask transport / indexing.
4. Display reset.
5. Broadcast lift operations.
6. Settling / locking.
7. Verification (if used).

If double buffering hides mask preparation from the visible transition, report
**both**:

- **visible transition time** (what the player sees), and
- **sustained arbitrary-map cycle time** (throughput between arbitrary maps).

A design that requires minutes of uncounted preparation between arbitrary maps is
a product problem even if the visible motion takes ten seconds.

## Prototype ladder requirement

No architecture may jump from calculations to a 6,400-cell machine. Every
selected architecture must define a prototype ladder as part of its design:

- **Prototype A — single cell:** validate the fundamental latch / ratchet /
  support principle.
- **Prototype B — small full-pitch array (e.g. 5×5):** validate neighbouring
  cells, tolerances, friction, assembly, repeated cycling.
- **Prototype C — one complete bank/module:** validate mask selection, reset,
  lift load, correlated failures.
- **Prototype D — multiple banks:** validate scaling and timing.
- **Full machine:** only after the repeated mechanism has survived A–D.

A mechanism that cannot be meaningfully tested in a small, inexpensive coupon is
**less attractive** and should be scored down accordingly.

## Miniature dimensions and vertical-travel basis

Research checked **27 September 2026**.

### What "standard miniature height" means

There is no single exact height shared by every Dungeons & Dragons miniature.
Miniature "scale" is a reference size, and the final physical height changes
with race, pose, weapons, hats, wings, scenic bases and sculpting style.

Useful current references:

- WizKids describes its D&D Icons of the Realms Yawning Portal environment as
  **28 mm scale** and says it works with existing D&D Icons of the Realms
  miniatures and sets.
- Modern tabletop/RPG miniature sellers also commonly use **32 mm scale**.
  A current scale guide aimed at D&D/RPG play describes a human-sized 32 mm
  character as typically about **28–35 mm** tall, depending on sculpt and
  measurement convention.
- Scale labels are not maximum overall heights. Raised weapons and poses can
  extend above the nominal figure height, and larger D&D creatures can be far
  taller than a player-character miniature. For example, WizKids' Gargantuan
  Tarrasque is advertised as more than 11 inches tall.

Sources:

- https://wizkids.com/dd-icons-of-the-realms-the-yawning-portal-inn/
- https://novanvil.com/pages/miniature-scale-guide
- https://wizkids.com/dd-nolzurs-marvelous-miniatures-gargantuan-tarrasque/

### Engineering interpretation for this project

The terrain display should not attempt to match the height of the largest monster
miniature. The vertical-travel requirement is intended to give a meaningful
terrain step comparable to a **normal human-sized player/NPC miniature**.

Use the following project rule:

- **Minimum provisional usable vertical travel: 40 mm.**
- 40 mm is intentionally above the common 28–35 mm human-sized figure range and
  leaves some margin for bases, headgear and sculpt variation.
- A design does **not** become qualified solely because it has 40 mm nominal
  geometry. Before claiming compliance, measure at least one representative
  physical D&D player-character/NPC miniature from the bottom of its base to its
  highest normal body/head feature and record the model and measured height.
- If the measured representative miniature exceeds 40 mm, increase the required
  travel and rerun timing, load, packaging and structural calculations.
- Oversized monsters, raised weapons, wings and display poses are useful
  usability cases but are not the reference that sets minimum terrain travel.

This keeps the current test08 40 mm assumption as a reasonable provisional
target while converting it from an arbitrary number into a sourced design rule.

## Fabrication context — Bambu Lab X1 Carbon

Research checked **27 September 2026**.

This project is expected to be prototyped primarily on a **Bambu Lab X1 Carbon
(X1C)**.

### Printer capabilities relevant to the project

Bambu Lab's current X1C specifications list:

- FDM/CoreXY printer;
- build volume: **256 × 256 × 256 mm**;
- included **0.4 mm hardened-steel nozzle**;
- optional **0.2, 0.6 and 0.8 mm** nozzles;
- all-metal hotend, up to **300 °C**;
- maximum toolhead speed **500 mm/s**;
- maximum toolhead acceleration **20 m/s²**;
- supported materials including PLA, PETG, TPU, ABS, ASA, PVA and PET;
- PA, PC and carbon/glass-fibre-reinforced polymers are explicitly within the
  X1C's intended advanced-material capability.

Bambu's X1-series hotend documentation describes the **0.2 mm nozzle** as the
high-fineness option for small/intricate models. Reinforced/particle-filled
filaments are restricted or discouraged with the 0.2 mm nozzle because of clog
and abrasion risk.

Sources:

- https://eu.store.bambulab.com/products/x1-carbon-3d-printer
- https://eu.store.bambulab.com/en/collections/consumables-x1-series/products/complete-hotend-assembly-x1-series

### Dimensional accuracy: do not confuse sensor resolution with part tolerance

Bambu advertises **7 µm lidar resolution**, but that is a sensor specification,
not a guarantee that an arbitrary FDM part will be dimensionally accurate to
7 µm.

The published X1C technical specifications cited above do **not** state a general
guaranteed dimensional tolerance for finished printed parts. Actual fit depends
on nozzle, filament, flow calibration, feature orientation, cooling, shrinkage,
wall count and the specific geometry.

Therefore:

- do not use a blanket ±0.05 mm or similar assumption merely because the printer
  is capable of fine motion/sensing;
- every sliding, rotating, snap or press-fit mechanism at the 5.08 mm pitch must
  have a calibration coupon before its clearance is treated as qualified;
- critical fits should be tested as a small clearance matrix rather than as one
  nominal CAD dimension;
- record nozzle, layer height, filament type/lot, orientation and any XY/hole
  compensation used for every mechanical test.

For the test08 geometry, a **0.20 mm wall is an experimental feature**, even when
using the 0.2 mm nozzle. Being nominally printable as one extrusion-width feature
does not establish yield, stiffness, straightness or repeatability across
thousands of parts.

### Project material baseline

The normal project material is **PLA**. Treat PLA as the baseline for geometry,
timing, mass and assembly experiments unless a test documents a reason to change.

Color is not a mechanical design requirement. Do not assume one PLA color is
stronger than another without material/batch data or a coupon test. Prefer
consistent material and lot for comparative measurements.

Other X1C-compatible materials may be introduced when they solve a measured
problem, for example wear, impact resistance, temperature, creep or compliant
features. A material change is an engineering variable and must be requalified
for friction, shrinkage, fit and printability.

For very fine 0.2 mm-nozzle geometry, avoid assuming carbon/glass-filled
filaments are available as a drop-in strength upgrade; Bambu's nozzle guidance
limits those combinations.

### Consequences for the full display

The ~400 mm active map cannot be printed as one monolithic X1C part because it is
larger than the 256 mm build volume. Full-scale structure should therefore be
modular.

This is compatible with the current test08 direction: small guide cartridges,
row modules or other replaceable tiles are preferred to one large printed frame.
Modularity also makes failed cells and wear parts serviceable.

Before scaling a mechanism to thousands of cells, require repeatable full-pitch
coupon batches printed on the actual X1C and PLA process intended for production.

## Flow forward

These criteria define **what a solution must achieve and the environment it must work in**. The next stage asks which existing engineering disciplines, mechanisms and principles can help satisfy them.
