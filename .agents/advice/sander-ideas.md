# Sander's ideas

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
