---
status: active
builds-on: [Q-010, Q-011, ADR-006, DES-006, E-047]
---

# ADR-009: bounded challenge of A-011 escape routes

## Decision

**Retain A-011 as the sole leading arbitrary-map candidate pending the E-018
coupon. Do not switch candidate or start a parallel architecture campaign.**
The three materially different escape routes below remove or redistribute part
of A-011's rail/shaft risk, but each has a first-order product failure before
it has evidence strong enough to displace A-011. This is an analytical
comparison; no architecture passes hardware, reliability, cost, or
manufacturability qualification.

## Comparison

| Route | Operating principle and changed load path | Timing / regional independence / observability | Product screen and disposition |
|---|---|---|---|
| Distributed bistable pin cells | One local actuator selects a mechanically latched five-state pin; a rigid local stop, not the actuator, carries tabletop load. This removes the long shaft and most shared reaction load. | O(changed cells), naturally regional; per-cell position sensor or a verification pass is required. | At 80 x 80 cells, even one actuator per cell means 6,400 purchased actuators, local wiring/driver interfaces, and 6,400 precision assemblies (calculation from the canonical field size). A deliberately optimistic $1 per actuator is already $6,400 before drivers, sensors, structure, and assembly (assumption/calculation, not a quote). **Killed on purchased-part and assembly scaling.** |
| Non-contact XY magnetic writer with passive bistable latches | A travelling magnet toggles local ferromagnetic or permanent-magnet latches; the selected pin rests on a hard stop. Writer force need not enter the terrain rail/shaft if the air gap and magnetic circuit remain controlled. | Regional in principle, but a shared carriage serializes changed sites unless multiple heads are used. Readback needs Hall/optical sensing or a second magnetic pass; a missed toggle can be silent. | It escapes A-011's shaft torque only by accepting unresolved gap, field cross-talk, latch-force, and carriage-registration constraints. With the inherited 71 cells/s/head and eight positions, the optimistic write term is still 11.27 s before carriage settling, magnetic settle time, and verification (calculation inherited from Q-010; not measured). **Conditional research direction only; not a replacement.** |
| Fluidic/manifold bistable tile | Each cell is a bistable fluid chamber or diaphragm stack; shared pressure/valve manifolds write selected regions and a local hard stop carries the height load. No long mechanical shaft is required. | Potentially parallel row/column updates; local changes depend on valve isolation and pressure settling. Pressure, bubble, leak, or diaphragm state requires per-cell optical/electrical readback. | Four binary planes imply 25,600 state sites at the canonical field size (calculation). A shared pressure source/manifold creates correlated failures; row/column addressing risks sneak flow and cross-talk. Printed seals, long-term creep, cleaning, and tabletop load retention are unqualified. **Killed for the tabletop product on sealing/state-retention risk before detailed design.** |

The magnetic route is the only concrete escape route that remains physically
plausible on paper: it can separate selection force from terrain load without
requiring thousands of purchased actuators. It is nevertheless not
competitive evidence. Its central advantage is an inference from the proposed
load path, not a measured result or a sourced component capability.

## Why this does not displace A-011

ADR-006 requires an on-demand arbitrary-map generator, not a prepared-mask or
buffer-only accessory. A distributed cell array meets that boundary but fails
the product's purchased-part and assembly scaling by direct count. The fluidic
tile may reduce mechanical parts but replaces them with a 25,600-site sealing,
addressing, and verification problem; no evidence bounds it. The magnetic
writer preserves a reusable parallel medium and regional updates, but its
registration, field cross-talk, latch retention, and readback are the same
class of unresolved physical gates that E-018 is already designed to expose,
while adding a new non-contact gap problem.

Q-011's current global 100 N rail-plus-shaft baseline is 0.12919 mm before
omitted compliance (calculation recorded in E-047), so A-011 remains on HOLD
against the current stiffness screen. That failure is not evidence that any
escape route passes: the alternatives have not demonstrated a bounded local
load path, and changing the load path without revisiting the declared screen
would be a requirement change rather than an architecture result.

## Cheapest discriminating test if A-011 fails

Keep the E-018 coupon as the first decision gate. If it fails specifically on
rail/shaft reaction or loaded-neighbour disturbance, build one final-pitch 5 x
5 magnetic-latch coupon with a passive hard-stop plate, one reused XY writer
head, two deliberate air-gap conditions, loaded adjacent pins, and a simple
Hall or optical readback channel. Test arbitrary 5 x 5 maps for 100 write/read
cycles, including alternating states and one-cell changes beside loaded
neighbours. Measure toggle force versus gap, missed-toggle rate, neighbour
motion, readback confusion, and complete regional update time.

Reject the route if any gap needs a precision interaction tighter than the
available printed/assembled tolerance, if magnetic cross-talk moves an
untouched loaded neighbour beyond the existing regional-isolation criterion,
if missed toggles are not detected, or if the measured complete update cannot
meet the canonical regional timing bound. This coupon tests the claimed
escape directly; an analogy to magnetic latches or a geometric CAD layout
would not be acceptance evidence.

## Ranking and handoff

1. **Retain A-011 pending coupon:** run E-018 and preserve its rejection gates.
2. **Do not modify A-011 yet:** first use the coupon failure mode to determine
   whether a load-path change is actually needed; do not relax arbitrary-map
   or verification requirements.
3. **Do not switch candidate:** distributed bistable cells and fluidic tiles
   are killed by first-order scaling/risk; the magnetic route is a conditional
   fallback research direction, not a promoted architecture.

Evidence classes: canonical field size and A-011/Q-011 timing and displacement
values are inherited calculations; actuator/site and four-plane counts are
calculations; the $1 actuator screen is an explicit assumption; all magnetic,
fluidic, durability, tolerance, and failure-behaviour statements are
analytical inferences or unresolved unknowns. No physical validation or
supplier quote is claimed.
