# Sander's ideas

## [PRIORITY] Owner's north star — fun, readable, uninterrupted D&D play

**The product exists to make Dungeons & Dragons more enjoyable at the table.** Players and the Game Master need legible terrain, safe places for miniatures, revealing rooms and walls without a tedious pause, and an intuitive picture of the battlefield. An impressive mechanical height field is not useful if it looks wrong in play. The roughly 30-second target means *the players should not have to wait long before play can resume*, not that there is a sacred physical 30-second constant. Technical targets are useful proxies for the experience; change them only with evidence and a deliberate product decision, not to make an inconvenient mechanism pass.

**The physical pins are primarily for actual terrain geometry**, especially solid ground, hills, substantial earth/rock masses, stairs, cliffs/chasms where elevation matters, and thin, clear walls/barriers. **Do not automatically model trees, foliage, tiny stones, small decorative boulders, textures and props as elevated pins.** A row of trees rendered as pins may look like a solid wall, which is visually misleading and can hinder play. If a tree or small object is rules-relevant, consider a conventional removable prop or clear game marker; if it is mainly visual, consider printed/overlaid or optional projected imagery. Projection is an unvalidated option, not assumed hardware. Some larger rocks/cliffs genuinely are terrain and may deserve height; classify by *function in play*, not by an object's label alone.

**The map-to-height conversion is itself a design hypothesis.** In E-254, 69.52% of the Riverside Road map is raised because the surrounding *land* was elevated to make water lower; trees and foliage were explicitly excluded. A flattened-water interpretation raises only 2.77% but removes bank relief. Similarly, an actual deep ravine may need a large physical height difference while a decorative stream may look and play better as flat projected water. Compare deliberately chosen encodings by how they look from a player's perspective, whether miniature placement and movement work, and what the Game Master gains. Do not infer required moving-pin fractions directly from an illustrated picture or a single arbitrary zero-height datum.

Before ranking actuation architectures by updated pin counts, **decide which shapes genuinely need mechanical elevation** and show alternatives (e.g. 3D walls and cliffs plus 2D foliage; a river with or without physical banks). If game conventions or player preferences are unclear, consult useful D&D play sources or create a **concise concrete Paperclip question for Sander**, with clear options and their consequences. Sander may answer later; keep progressing on conditional scenarios in the meantime rather than quietly turning assumptions into requirements.

## Idea 1 — Self-recovering mechanisms through automatic reset or homing

Perhaps a relatively complex mechanism for each pin could still be viable if the overall machine is designed to **automatically recover to a known-good state** whenever it is activated or reprogrammed.

The thought is that, during operation, individual pins or small mechanical components might gradually slip, become slightly misaligned, lose synchronization, or otherwise end up outside their intended position because of tolerances and mechanical interactions. Instead of insisting that every mechanism remains perfectly positioned indefinitely, we could deliberately include a recovery/reset phase.

Possible approaches:

- **Home all pins:** lower every pin to a shared zero position so they start the next operation from a consistent height.
- **Reset internal mechanisms:** return locks, latches, couplings, or other small mechanical parts to a known starting configuration before the next actuation.
- **Automatic re-synchronization:** design the machine so recoverable positioning or indexing errors are cleared as part of its normal operating cycle, rather than needing manual adjustment.

The central question is whether **automatic recoverability can make a more intricate repeated mechanism practical and reliable at full-display scale**. A reset can correct recoverable state or alignment errors; it would not automatically repair actual wear, deformation, or broken components. Its consequences for update time, unchanged regions, and objects resting on the display would need to be examined.

*Status: personal concept to explore, not a proven design.*

## Idea 2 — Simple pins, shared mechanisms, and software-first design

**Sander's main design preference:** make the thousands of repeated pins as "dumb", simple, and cheap as possible: ideally just ordinary 3D-printed plastic rods, with no complex individual mechanisms built into them. Put the intelligence, movement, positioning, and control in a comparatively small number of shared mechanisms underneath or around the array.

A related, particularly important principle is **software first whenever it can genuinely replace hardware complexity**. Hardware is costly and cumbersome to design, manufacture, change, and repair, especially when repeated thousands of times. Software can be modified and tested much more quickly, including with AI-assisted development. Instead of adding elaborate mechanical calibration and sensing interfaces for every pin, explore shared sensing, software calibration, error detection, and closed-loop correction.

This does **not** mean software can create physical support or repair broken parts by itself; it is a design preference to investigate, not a claim that every hardware function is optional. Combine with Idea 1's automatic reset/homing where useful.

## Idea 3 — Row-wise lateral gripping or braking with a shared mask/strip

Use simple plastic pins and hold their heights with an external **row-based gripping/braking system** rather than individual pin locks. One possible implementation is a long mask, strip, or frame spanning one row, two rows, or perhaps three rows. Pulling or shifting it laterally presses the rods firmly against a side surface so friction prevents them from falling. Release the row/bank to reposition pins, then re-engage the grip.

The grouping and construction are open choices: one row versus several, mask versus strip, exactly how lateral force is distributed, and how the pins are subsequently driven. The idea is shared retention with simple repeated pins, not a finished clamp design.

## Idea 4 — A movable actuator arm serving one or several rows

One possible counterpart to the row-grip is a **long actuator arm/head** that services a complete row or several rows at once (perhaps two, three, or four). Small vertically moving pushers on the arm would set individual rod heights. The arm may travel over or under the display to address different rows.

Explore the number of rows served, number and type of motors, the geometry of the pushers, and how the arm moves. One speculative packaging approach is **flexible cable transmissions** from remotely placed motors to the pushers, allowing motors to lie flat instead of using up valuable vertical depth. This is a candidate, not a commitment to cable drive or a particular motor count.

## Idea 5 — Punched-hole masks for selective lifting and height programming

A different (or complementary) approach uses **perforated physical masks**, inspired by punch cards. Slide a mask beneath the pins or the lifting interface. In the proposed selection logic, a hole at a location permits the relevant lifting pin/pusher to pass through and move the corresponding display rod upward by a prescribed increment; a closed location does not produce that upward movement. The exact contact geometry and motion sequence remain to be invented and checked.

Repeated strokes, or different masks used in succession, could create multiple final pin heights. Investigate how many masks/passes are needed, how height increments are generated and retained, and how the mask is aligned and rewritten. This **lifting-selection mask** is distinct in purpose from Idea 3's lateral gripping mask; they might be combined.

**Disposable or consumable mask media is acceptable for an initial experiment.** For example, feed an inexpensive plastic roll through a quick side-mounted punching/perforating station, make the required holes, present the perforated section to the display, then advance the roll to a new section for the next programming pattern. Material waste need not rule out a simple, fast prototype. Reuse, recycling, or a less wasteful rewritable medium can be explored later *if this principle works*. Account for the complete punching, feeding, and actuation cycle when evaluating eventual performance.

## Idea 6 — Pneumatics or hydraulics, preferably at practical channel sizes

Do not automatically rule out **air or liquid pressure** for pin actuation. Leakage, holding position, valves, and control are obvious concerns, but those are problems to explore rather than grounds for immediate dismissal.

Avoid relying on niche **microfluidic** fabrication with tiny, precision channels as the default. More conventional, comparatively large pipes/tubes and rapidly switched pressure outputs may offer a more practical route. Investigate shared pressure sources and switching between outputs rather than thousands of complex local mechanisms.

In combination with Idea 7, one can imagine commanding pressure, observing the resulting pin height, then stopping or adjusting the drive when the target is reached—without requiring an individually calibrated pressure-to-height relationship for each pin. How position is held after stopping, and how independently pins can be selected, remain open.

## Idea 7 — Shared cameras, depth sensing, and software closed-loop correction

Use **external optical feedback** to measure pin heights and correct errors in software rather than integrating a dedicated height sensor in every pin. Possibilities include:

- A depth camera, such as a Kinect-style device.
- One or more ordinary smartphone cameras viewed from different angles, with 3D reconstruction.
- Lasers or other shared optical measurement methods if they are simpler or more accurate.

Measure heights during or after actuation, compare with the desired terrain profile, and command corrections. This can complement hydraulics, the row actuator, punched masks, and the automatic recovery of Idea 1.

Sander considers shared cameras especially interesting because they may be readily available and reusable for unrelated projects; their cost should not immediately discourage trying the concept. Whether a particular camera can see and distinguish all pins accurately enough, particularly under occlusion or with miniatures on top, is still to be tested. The **software-feedback philosophy** is more important than any one specific camera implementation.

## Idea 8 — The one-kilometre-long display thought experiment

Imagine needing to build a shape display **one kilometre long**. It is deliberately unrealistic, but a useful test for architectural priorities. At that scale, would we really manufacture an elaborate mechanism for each pin? More likely we would want every pin to be an extremely simple stick—even, metaphorically, a twig—while a travelling machine or shared mechanism underneath performs all the intelligent work of setting its height.

Use this thought experiment to challenge where the complexity belongs: **what becomes unacceptably expensive, fragile, or troublesome when repeated enormous numbers of times, and what can instead be shared, moved, programmed, sensed, or corrected centrally?** It is a heuristic to generate ideas, not evidence that any particular moving-head or shared-mask design works.

---

*These are Sander's personal exploration ideas, not validated mechanisms, mandatory tasks, or replacements for the project's engineering criteria. The alternatives can be combined where physically sensible; the CTO should test feasibility rather than assume it.*

## Sander's reported hands-on prototypes (informal physical observations)

Sander has **already printed** small plastic pins/rods and a matching grid that holds them. Adjusting fit was feasible, but his prints showed rod-to-rod variation in thickness: some were thicker or thinner than others. This experience strongly motivates keeping the 6,400 repeated columns simple and tolerant rather than relying on tight per-column fits. He has not supplied caliper datasets, printer settings, sample count, cycle count, pictures, loads or documented failure statistics. Do not translate the experience into a quantified accuracy or reliability guarantee.

He has also **already 3D-printed and manually tried** a near-reference-scale screw-driven pin: a hollow pin with a nut/internal thread at the bottom and a mating threaded bolt/screw. Turning the screw from below while the pin does not rotate translated the pin up or down, and he reports that this worked reasonably well. The direction depends on the thread hand and viewing convention. **Additional owner clarification (2026-10-12): he specifically tested whether the screw-driven pin remained at its set height under load, and reports that it did, in his latest physical trial.** This is a **positive firsthand physical observation of holding behavior**, not just a theoretical suggestion. Sander emphasizes that ordinary D&D miniatures are very light; future holding tests should include realistic miniature loads rather than treating large assumed per-pin loads as typical. The load mass, duration, cycles, position, measured torque, printer settings and precise successfully printed CAD/calibration variant were not recorded. Therefore it is not a quantified 40-mm travel, fatigue, worst-case back-drive or 80x80-array reliability qualification.

## [PRIORITY] Idea 9 — Simple threaded pins, driven from underside screw heads

Use a dense grid of roughly pitch-sized **hollow plastic columns with an internal nut/thread at the lower end**, each riding on an underlying screw/bolt. Restrain the column from rotating while allowing vertical motion; turning the screw at its accessible underside head changes column height. The top remains a simple terrain cell, potentially with little more complexity than its threaded insert or printable internal thread.

The appeal is that every cell can remain mechanically simple, height may be stored by screw angle/thread friction, and the array presents many similar drive sockets **underneath** the board that a shared mechanism could access. **Sander notes that, even if a future screw variant back-drives too easily, he expects that tightening the fit slightly to increase friction could be a simple remedy.** Treat this as a promising *adjustment hypothesis*, not a proven or universally reliable fix: added friction also raises the actuator torque, may worsen print-to-print binding and wear, and must be evaluated across the repeated population. The positive manual hold test reduces concern about the feasibility of basic passive holding in the tested prototype, but does not eliminate these scale-up questions. Important unresolved details: guiding/anti-rotation, support and thrust bearing, thread fabrication variability, alignment, quantitative back-driving margins for realistic miniatures, acceptable backlash and wear, preventing over-travel or unthreading, and the turns/RPM needed for ~40 mm travel.

Height could be monitored by calibrated commanded turns from a known starting state, by a shared depth/stereo camera, or by both. Software estimates are not automatically proof of true height after skipped engagements, slip or deformation; physical end limits and safe torque/stop behavior still matter.

**Possible actuator layout A: moving screwdriver row.** A row-length head travels below the board. It carries a bank of reversible rotary drive tips that engage the screw heads. Either the whole head moves vertically for insertion or each tip uses a compliant/self-aligning docking motion. Choose how many rows/columns to operate at once, how to select tips, how to disengage safely while preserving support, and where motors are packaged; flexible cable transmissions are one possible alternative, not a requirement.

Existing canonical **A-007** describes an analytically rejected scanning-screw implementation, and E-050/E-131/E-156 and later work contain additional thread/friction/throughput lessons. The manual printed concept does not erase those results. **Revisit only a materially distinct topology or a newly justified representative-play workload, and compare complete-machine consequences.**

## [PRIORITY] Idea 10 — One shared reversible motor with row/column mechanical selection

**Possible actuator layout B:** avoid motorizing all 6,400 screws separately. Instead use **one substantial reversible rotary motor** as a shared power source, and a mechanical transmission/selector analogous to clutches in a car or a clockwork mechanism. Independently command a selected row and a selected column; only their intersection should engage the main drive and turn the addressed screw. Conceptually, for an 80x80 grid, this suggests one main drive and up to ~80 row plus ~80 column selectable control channels (potentially small motors, other actuators or mechanical controls), rather than 6,400 independent motors.

Sander considers even a system with roughly one selector motor per row and per column potentially worthwhile to investigate despite its apparent bought-hardware cost. He is not claiming the mechanism, component prices or 161-motor implementation have been solved.

The key engineering question is **how to realize a true mechanical AND at exactly the row/column intersection**, carrying useful bidirectional torque without inadvertently rotating other sites. Investigate clutch engagement, positive selection and half-selected states, rotary power distribution, safe disconnect under load, thread holding/anti-backdrive, torque sharing, reset, backlash, fault recovery, update sequencing and budget. A count of row/column addresses alone is not an implemented selector. Alternative layouts can use fewer actual motors even if they retain 160 logical selection lines.

Sander's intent is to search a different actuation architecture around the threaded-pin prototype, not to force a specific clutch, gearbox or row-matrix geometry. Compare it with the moving-row rotary head (Idea 9) and earlier row/column and shared-drive evidence instead of assuming that either succeeds.

## Idea 11 — Put precision and specialized manufacturing into a few shared parts

Ordinary FDM parts vary, as Sander noticed with his printed pin grid. Do not assume demanding tolerances will work on 6,400 tiny columns. **Concentrate tolerance-sensitive or complicated geometry in a small number of reusable actuator/selector components** if that reduces total costs and failure sites.

For those limited shared parts, explore outsourced high-accuracy 3D printing (possibly metal), machining, or suitable 3D-printed tooling/molds for casting selected materials, including elastomers where appropriate. Tooling temperature compatibility, shrinkage, release and precision are real constraints; merely printing a mold does not qualify it for casting metal. These options are financially implausible for thousands of individually expensive parts, but may be reasonable for a few shared heads or couplers.

An exception to "completely dumb columns" remains possible if a slightly more complex printed repeated pin is *intrinsically tolerant* of realistic manufacturing variation. Do not ban it just because it has a thread or local geometry; require proof that the large replicated population stays robust.

## Additional product priorities from Sander

- **Incremental research success matters.** The eventual bought-hardware target is still at most $500, but a working full-system mechanism/design at roughly $1,000 or $1,500 would be a much better starting point than no functioning machine. Demonstrate feasibility first where rational, then develop a credible path toward affordability. This does not authorize a purchase or imply $1,500 is an acceptable final-product cost.
- **The 30-second goal is a gameplay promise, not an all-cells-move promise.** Ordinary D&D maps are expected to have many floor pins at baseline and comparatively few raised walls or other important structures. The **actual percentages are unknown**; investigate representative maps and map-to-map changes rather than inventing a figure. Dense arbitrary-height maps still deserve separate stress and reliability analysis.
- **Visual detail need not be mechanical detail.** Show essential walls/large terrain physically, but small objects, textures or icons can potentially be shown by an overhead projector even if it is impractical to sculpt each of them with pins. Projection is optional and must still be checked on uneven geometry.

These personal priorities are also reflected in the authoritative mission and stage-02 criteria. This advice file records why Sander requested the change, rather than superseding the criteria.

## [PRIORITY] Historical screw models recovered from Git history

The original CAD files **are preserved in repository history**. A useful complete historical snapshot is commit [`41484f9699`](https://github.com/sander-van-damme/project-shape-display/tree/41484f96999847c139b9010e73009d73e9459c89), which predates the later agent-driven repository reorganization:

- [`trial-1-threaded-rods/`](https://github.com/sander-van-damme/project-shape-display/tree/41484f96999847c139b9010e73009d73e9459c89/trial-1-threaded-rods): early hollow cuboid/nut and threaded-bolt models (e.g., `cube-v2.scad`, `bolt-v3.scad`).
- [`trial-3-new-threaded-rods/`](https://github.com/sander-van-damme/project-shape-display/tree/41484f96999847c139b9010e73009d73e9459c89/trial-3-new-threaded-rods): new `actuator.scad`, `calibrate_screw.scad`, `calibrate_rect_tube.scad`, frame components.
- [`trial-5-grid-and-cubes-and-rod/`](https://github.com/sander-van-damme/project-shape-display/tree/41484f96999847c139b9010e73009d73e9459c89/trial-5-grid-and-cubes-and-rod): later compact rod/screw and grid experiments with explicit calibration geometry, likely worth inspecting first but **not proven to be the successfully printed variant**.

The trial-5 OpenSCAD source defines approximately **4.4-mm outer rod width**, **0.44-mm tube wall**, **3.2-mm screw diameter**, **3-mm thread pitch**, **50-mm screw length**, and a frame with **4.64-mm openings + 0.44-mm webs = 5.08-mm pitch**. Its separate tolerance coupon explores `4.64 +/- 0.3 mm` in 0.1-mm steps. These values document design intent; they are **not measured print error or evidence of passing fits**. The models call BOSL2 routines, so reproducing them requires checking compatible library versions.

Sander remembers personally printing/testing simple rods, a mating guide grid and a working screw-raised rod. **He confirms that the latest physical screw-pin iteration was positively tested for retaining height under load without continued driving.** He does **not** remember which exact calibration variant was the successfully printed assembly or the applied load value. It is reasonable to investigate the latest trial-series CAD first, but **do not equate the committed trial-5 source with the precise tested print without evidence**. The CTO should inspect the historical sources before inventing replacement geometry, recognize the positive but unquantified physical holding observation, and avoid claiming measured load margin, production reliability or endurance from it.

## [PRIORITY] Idea 12 — Rotary writing heads optimized for D&D walls and fog of war

Sander wants the threaded-rod family investigated **first**. Most D&D terrain geometry might consist of straight wall stretches, possibly mostly aligned with a grid's two axes. This is a personal observation/hypothesis; **look at real battle maps and measure** wall orientation, length, clustering and the sequence in which geometry is revealed before designing around it.

Possible shared actuation variants:
- A **full-row rotary actuator head** that moves like a 3D-printer carriage and can turn 90 degrees at a suitable parking position, changing between writing horizontal and vertical lines of screws/pins.
- Separate horizontal and vertical actuator heads, avoiding the time/clearance cost of reorienting one long head.
- **Four independent smaller heads**, perhaps 16 driven pins each, serving different portions of the map in parallel. The exact 4×16 arrangement is illustrative, not a throughput proof.
- A mechanically multiplexed row/column rotary bus (Idea 10) as a comparator, even if selection cost initially runs above the ideal product BOM.

D&D's **fog of war** means that walls/rooms may be revealed as players move, often in small regions. A head could potentially pre-position near a known future wall before revealing it, then write the new heights quickly. This may improve player-perceived reveal latency but must not alter visible terrain too early, disturb existing miniatures or conceal preparation time as free throughput. Unknown future player choices and worst-placed target walls need to be included.

Compare each layout for docking accuracy and per-pin time, reverse rotation, travel, turn count, rotation/exchange clearance, safe simultaneous operation, collision, isolation, height verification, full bought-hardware cost and realistic gameplay update durations. A long row of screwdriver tips is a mechanical proposal, not a solution just because its motors fit on one moving bridge.

## Idea 13 — Other manufacturing methods and realistic maker assembly time

Sander asks that the engineering search **go well beyond '3D print it or buy a catalog part'**. He can imagine molds/casting to batch-manufacture repeated plastic or metal screws and rods, formed parts, machinable feedstocks, specialized services offering custom polymer/metal components and inexpensive automated processes. A 3D-printed mold may be useful with suitable casting media; compatibility with hot metal and casting shrinkage must be checked, not assumed.

He is happy to spend a weekend, or perhaps **two to four days**, building a promising prototype, but not weeks manually preparing, individually trimming or adjusting thousands of parts. The question is not only price per item but tooling, print time, automated production, number of human touches per part, assembly effort, calibration and later repair. Save expensive/precision processes for a limited shared actuator layer if that is the strongest cost/benefit choice. Favor compact packaging when comparable options work, but do not delay proving a robust mechanism for thinness.

## Sander's earlier resin pneumatic trial — negative practical experience

Sander previously used a **resin/SLA-style printer** for tiny air/fluid channels. He strongly disliked the messy resin handling and rinsing workflow. Small passages resisted flow enough that significant pressure seemed necessary to push air or liquid through, and tiny switching valves appeared to make the problem worse. No actual channel dimensions, pressures, flow curves or quantitative outcomes survive in this report. This is a practical warning about tiny resin-printed fluid networks, **not** measured proof that all pneumatic or hydraulic systems are impractical. He remains more interested in larger tubing if pressure-based designs are later reconsidered.

## Idea 14 — Narrow, lengthwise-inflatable rubber pins (deferred)

A possible **low-stack-height** shape display uses small inflatable rubber/silicone/elastomer column sleeves that extend mainly **vertically** with pressure rather than becoming wider. The unsolved questions are how to constrain circumferential expansion, fabricate thousands of tiny, repeatable sealed compliant parts (flexible-filament printing or suitable molding/casting), meter and hold the pressure, avoid leaks and support D&D miniatures safely. Sander did not find a satisfactory earlier answer and has not tested a working inflatable pin. This idea is **lower priority** and should be retained for future comparative exploration, not displace the renewed screw investigation.

## [PRIORITY] Explicit near-term priority (12 October 2026)

**First: resume the original screw/rod concept using the preserved OpenSCAD source and Sander's personal print experience.** Then distinguish the passive threaded lift/holding feasibility from the unresolved motorized selector/docking/throughput problem. Compare credible shared rotary heads and row/column selection on D&D fog-of-war wall workloads, costed for a working research prototype, against historical failures. Preserve engineering independence to reject a specific configuration if tests warrant it, but do not silently return to unrelated microscopic mechanism refinements before giving this physically explored family a meaningful new assessment.
