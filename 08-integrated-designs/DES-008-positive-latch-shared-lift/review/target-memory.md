# E — bounded target-memory escape screen

Date: 2026-10-14. Question: can preprogramming reusable per-lane multilevel targets remove the binary-mask rewriting bottleneck and yield a credible approximately $1,500, approximately 30-second machine? This is a mechanism and timing screen, not a qualified design.

**Decision: preprogramming alone does not rescue the current stopped-retirement architecture at eight heads.** Even a favorable double-buffered programmer with only 1.5–2.5 seconds per complete 64-lane target register remains approximately 36.7–38.8 seconds for the 40-mm, 64² sampled scene suite. A required 80-mm Z clearance excursion on each row exchange raises the representative central case to approximately 57.5 seconds. The remaining bottleneck is actual capture, grounding, seating, dog withdrawal, motion and return. Promoting a target memory without changing those operations merely replaces one missing mechanism with several others.

The three memory families below are materially different and can reduce active writer count. None has a demonstrated complete speed/cost/manufacturing advantage. Preserve them as explicit alternatives; do not create a large print package for them before the basic supported pawl transfer and row-access topology pass.

## What information must actually be stored

At 40-mm range and 5-mm height increments there are nine absolute levels but **17 signed displacements**. A reset-free delta program therefore needs five binary bits per lane, or one 17-state element. Four bits cover the nine signed displacements of a five-level 10-mm-spaced terrain only. Storing the absolute nine-level target in four bits requires additional direction/unchanged information and a mechanism relating that target to the old column height. The existing common-datum dog understands displacement, not absolute height; changing a number format does not provide an absolute reader.

A reset-to-zero sweep is not free: columns at different initial heights require different downward displacements, or individual bottom-stop retirement that itself needs a complete retained support/release mechanism. Resetting unchanged pins also violates regional isolation. Do not use absolute target memory as a hidden all-board reset.

For B=8 heads, 64 lanes/head, five bits/lane:

| Memory | One target register/head | Two target registers/head |
|---|---:|---:|
| Lane words across machine | 512 | 1,024 |
| Binary storage bits | 2,560 | 5,120 |
| 17-state cams or indexed stop sliders | 512 | 1,024 |
| Active writers if eight/head | 64 | 64 |

These counts omit the 512 active operating lane controllers, their capture/release linkages, read contacts, buffer selector and reset hardware. One writer serving several slots is not one complete mechanical channel per stored word.

## 1. Binary latch register plus common mechanical threshold reader

Each lane has five positive two-position sliders in a compact stack: four magnitude bits plus a direction/enable code. A writer head with eight small actuators visits eight lateral addresses. At each address it writes the five sliders in five shared clock phases. A common reset comb first establishes a known state; each writer pushes a latch only for bits that differ from reset. Detents retain the sliders while the programmer moves away.

During terrain actuation a common threshold reader presents the current displacement code. Only a lane whose stored code matches that code admits a release probe. The release probe acts on the lane's operating controller: restore ground pawl, seat under retained dog support, then withdraw dog. The target bits carry command information only, never terrain load. A separate consumed/retired state prevents the lane from re-engaging during empty return or the opposite-sign sweep.

A positive equality reader needs either five serial blockers per lane or a stepped/keyed probe that cannot pass when any bit mismatches. It also needs separation between changing common code bars and applying release force. A logical comparison in software is not a physical decoder. Previous ADR-016 correctly warns that equality detection alone does not implement retained output state or reset; this proposal does not inherit a pass from it.

**Program bound:** eight addresses × five phases × 30–40 ms/phase is **1.20–1.60 s of write dwell alone**. Lateral indexing, clock indexing, reset, approach/withdrawal and state checking add time. Approximately 1.8–2.7 s/register is a useful favorable engineering scenario, not a specification. Simultaneous eight-writer operation and clean snap-through at those rates are unmeasured.

**Repeated burden:** 5,120 stored sliders for two buffers, their guides/detents, roughly the same number of equality interfaces, and at least 512 operating lane controllers. At ten seconds simply placing each stored slider, assembly alone is 14.2 hours, excluding making, testing and replacing them. The design reduces purchased actuators but recreates thousands of precision-sensitive mechanisms in the head layer. It is difficult to prefer over the one-piece cam below before a simple, tolerance-insensitive integrated register is shown.

**Disposition:** park. It reduces repeated whole-row mask writes but is action-limited afterward, and adds substantial latch/decoder complexity.

## 2. One indexed stepped cam per lane

Each lane carries one narrow independently rotatable cam wheel on a common support shaft. A 17-position detent encodes signed displacement; a direction track distinguishes up, down and unchanged, and a magnitude track positions a lightweight trip follower. The wheel does not transmit terrain force. During programming, eight reusable rotary writers dock with eight wheels, set their detented angles, withdraw, and index to the next eight. A detent/clamp holds the wheel after the writer leaves.

An illustrative approximately 24–30-mm diameter, 4–5-mm-wide wheel can fit axially at 6.35-mm lane pitch while occupying real depth under the board. There is no requirement that all internal parts fit within 6.35 mm in every direction. A cam radial range of roughly 5 mm with an 8:1 follower lever represents 40 mm of trip displacement, but also magnifies a 0.10-mm radial/assembly error into 0.8 mm of trip error. That is comparable with the entire pawl capture margin. Direct full-range memory avoids this amplification but makes the mechanism much taller. A cam is thus not automatically a tolerant analog decoder.

A writer must acquire the independent wheel phase or couple through a friction drive while a positive detent captures the requested position. A rigid common key cannot dock arbitrary cam angles without phase seeking. A cheap servo's travel time alone omits docking, detent release and confirmation. Gear amplification can shorten servo travel but magnifies backlash and reduces torque; it is a trade-off, not free speed.

**Program scenario:** 0.12–0.25 s per complete coupled word operation gives **0.96–2.00 s** for eight addresses, before roughly 0.5–1.0 s of lateral indexing/reset/checking. This is a favorable 1.5–3.0-s register scenario. The lower end needs a fast, lightly loaded, positively indexed writer with a real coupling geometry. No catalog specification currently establishes it.

**Repeated burden:** 1,024 cam wheels for double buffering, pivots/bearing interfaces, detents, followers and direction/consumed-state routing, plus the 512 operating lane controllers. The reduced number of stored moving bodies makes this the strongest memory candidate of the three, but it is not a complete affordable actuator by itself. Wheel material cost cannot stand in for the full register BOM.

**Disposition:** retain only as a later conditional escape if a changed retirement and row-index mechanism makes its 1.5–3.0-s programming useful. Do not build 1,024 cams to discover that the unchanged support sequence still misses the benchmark.

## 3. Indexed linear stop memory or reusable Jacquard-style carrier

Each lane has a long indexed slider holding a physical trip stop. The slider moves only during programming and is locked afterward. A follower attached to the common lift reaches that stop at the desired displacement and triggers the same retained local retirement sequence. A separate sign flag routes the lane into the up or down sweep. Direct 40-mm magnitude travel is geometrically transparent and avoids cam amplification. At 5-mm magnitude spacing it has nine detents that are much easier to print than submillimeter binary equality features.

Eight reusable linear writers set eight sliders at once, then index through the row. At 200 mm/s and 2,000 mm/s² a rest-to-rest 40-mm excursion alone takes 0.30 s; eight worst-case addresses therefore need **2.4 s of setting motion** before coupling, locking, lateral index and checks. A 3.0–4.0-s complete register is a more honest central scenario than a subsecond assertion. Shortening the physical stop travel with a lever brings back the same error amplification as the cam. Simultaneous global reset plus selectively stopping sliders during a common sweep needs per-lane stop/release memory, so it cannot be counted as a simpler writer until that hardware is included.

A removable/perforated card can carry the same information, as Jacquard machinery demonstrates, but arbitrary online maps require manufacturing or rewriting that card. A reusable physical pin card becomes another array of retained bits. Paper punching adds consumables and deletion/replacement; pre-made cards only help pre-known maps. Double-buffered media still owe initial preparation and sustained production. The industrial analogy validates program-carrier separation, not an affordable rewritable display interface.

**Repeated burden:** 1,024 sliding stops, their long guides/detents, sign/retirement state, followers, and a two-bank shuttle. Direct stops are easier to interpret and may be easier to diagnose than a five-bit equality stack, but their full travel and writer time are unfavorable.

**Disposition:** park for the approximately 30-second eight-head target. It remains an understandable slow demonstrator mechanism, not the preferred next physical question.

## Double buffering: real benefit, finite boundary

Two registers/head allow the inactive register to be programmed while the current register controls a row. They must be physically distinct and mechanically disconnected from the live release path. At row completion, a shuttle/reader switch couples the new register, resets the consumed lane controllers, then starts the next row. The old register can be rewritten only after it is positively disconnected. This adds a real buffer-switch motion, support for both registers, read coupling and collision checks.

For row execution times a_i, programming times p_i and switch times s_i, an ideal sequential two-stage pipeline is computed using independent completion clocks, not by deleting preparation. The first row pays its complete programming. In the simple equal-time case the sustained period approaches `max(a,p)+s`, with startup and final drain still present. Unknown next updates cannot be programmed before their data exists; ongoing known rows of one submitted scene can.

Independent check by workstream C: [`analysis/timing_target_pipeline.py`](../analysis/timing_target_pipeline.py) uses the existing finite stopped support sequence with no repeated mask-write charge, target programming as a separate pipelined stage, 0.15 s/register swap, 4 s common preparation/check allowance and one whole-row retry including reprogramming. At eight heads, 64² cells and 40-mm range:

| Assumed target programming per row | Favorable Y-only row access |
|---:|---:|
| 1.5 s | approximately 36.69 s |
| 2.0 s | approximately 37.69 s |
| 2.5 s | approximately 38.76 s |

At 50-mm range the same cases are approximately 38.07–40.50 s. If each row exchange must lower and raise through 80 mm to clear arbitrary-height tails, the central 40-mm case is approximately 57.49 s and the 50-mm case approximately 58.87 s. The physical row-access topology must determine which timing case is permissible; the lower number is not a claim that a Y-only head has been packaged.

## Cost screening: active writers are only part of the bill

A useful transparent budget equation is `C = C_rest + 64*C_writer + 1024*C_word + 512*C_operating_lane`, where `C_rest` includes all terrain pins/pawls, frame/guides, eight lift/transport/arrest systems, power/control, shipping and waste. It is not legitimate to call those quantities zero because the memory itself is passive.

For an explicitly hypothetical $800 remainder allocation and a $1,500 ceiling, a $4 complete writer leaves $444 for all 1,024 words and 512 operating lanes; a $9.35 actuator alone leaves $101.60 before its drivers/linkage. Even setting operating lanes to zero gives only $0.434 or $0.099 per complete memory word. These are allowance calculations, not supplier prices or lower bounds. A cheaper proven common-powered writer and integrated molded/stamped registers could change the result, but neither has been constructed or quoted here. The five-bit register especially cannot inherit a one-cent-per-bit manufacturing assertion from bulk plastic price.

The one-piece cam has the best part-count prospect, but its detent, reader, shaft, phase-acquiring writer and consumed-state output still require a real BOM. No method currently demonstrates the approximately $1,500 complete-machine case. More favorable hypothetical prices would not repair the independently calculated action-time failure.

## What could materially reopen it

1. **A proved continuous local retirement mechanism.** Ground pawl insertion precedes dog withdrawal, with both operations imposed by positive cams, and a consumed state prevents recapture. At 80 mm/s, a 0.8-mm geometric window lasts only 10 ms; a 1.6-mm window lasts 20 ms. A 0.2–1.0-mm deliberate seating drop might be physically retained by an already inserted pawl, but it is not the existing controlled seating sequence, and must be tested with loaded selected columns. It cannot be silently modeled as instant, zero-impact retirement.
2. **A common cam sequence that actually combines operations.** If one camshaft replaces several independently timed strokes while preserving support overlap, fewer timing events may be justified. The complete cam geometry, load path and return must show that combination. Merely counting three motions as one named event is invalid.
3. **A row-index topology that stays clear without the full tail-length Z excursion.** Offset/staggered stems and retracted dogs might achieve this, but all arbitrary neighboring heights, operating fingers, release tongues and supporting frame must clear. An empty animation of the head reference point does not establish it.
4. **More banks with a complete cost comparison.** This is not forbidden, but every extra bank repeats lift/arrest, scan mechanism, writers, double memory and lane controllers. At eight heads the approximately $1,500 case already needs a credible shared-hardware and register BOM; no mass-production discount can substitute for it.

None is presently qualified. The useful next physical work remains the small positive-pawl/shared-dog transfer. The useful next architectural work is row-access and retirement topology, not another large target-memory optimization sweep.
