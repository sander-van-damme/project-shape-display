---
status: active
builds-on: [Q-010, Q-011, ADR-006, ADR-009, DES-006, E-047]
---

# ADR-010: bounded architecture escape-route screen

## Decision and scope

Retain the following early comparisons without selecting a leader. ADR-009 and the mission supersede the former sole-A-011 and coupon-first prescriptions. Reject the one-purchased-actuator-per-cell embodiment under its stated cost assumption; do not extend that rejection to shared actuation or all bistable cells. Keep magnetic and fluidic principles available for bounded computational exploration. No hardware, reliability, cost or manufacturability qualification is established.

| Route | Operating principle and changed load path | Timing / regional independence / observability | Product screen and disposition |
|---|---|---|---|
| Distributed bistable pin cells | One local actuator selects a mechanically latched five-state pin; a rigid local stop, not the actuator, carries tabletop load. This removes the long shaft and most shared reaction load. | O(changed cells), naturally regional; per-cell position sensor or a verification pass is required. | At 80 x 80 cells, even one actuator per cell means 6,400 purchased actuators, local wiring/driver interfaces, and 6,400 precision assemblies (calculation from the canonical field size). A deliberately optimistic $1 per actuator is already $6,400 before drivers, sensors, structure, and assembly (assumption/calculation, not a quote). **Killed on purchased-part and assembly scaling.** |
| Non-contact XY magnetic writer with passive bistable latches | A travelling magnet toggles local ferromagnetic or permanent-magnet latches; the selected pin rests on a hard stop. Writer force need not enter the terrain rail/shaft if the air gap and magnetic circuit remain controlled. | Regional in principle, but a shared carriage serializes changed sites unless multiple heads are used. Readback needs Hall/optical sensing or a second magnetic pass; a missed toggle can be silent. | It escapes A-011's shaft torque only by accepting unresolved gap, field cross-talk, latch-force, and carriage-registration constraints. With the inherited 71 cells/s/head and eight positions, the optimistic write term is still 11.27 s before carriage settling, magnetic settle time, and verification (calculation inherited from Q-010; not measured). **Conditional research direction only; not a replacement.** |
| Fluidic/manifold bistable tile | Each cell is a bistable fluid chamber or diaphragm stack; shared pressure/valve manifolds write selected regions and a local hard stop carries the height load. No long mechanical shaft is required. | Potentially parallel row/column updates; local changes depend on valve isolation and pressure settling. Pressure, bubble, leak, or diaphragm state requires per-cell optical/electrical readback. | Four binary planes imply 25,600 state sites at the canonical field size (calculation). A shared pressure source/manifold creates correlated failures; row/column addressing risks sneak flow and cross-talk. Printed seals, long-term creep, cleaning, and tabletop load retention are unqualified. **Unscreened: sealing/state-retention risks require a defined manifold and bounded leakage/creep model; risk alone does not reject the fluidic family.** |

## Evidence limits and reopening

The $1 actuator value is an optimistic scenario, not a quote. The magnetic 71 cells/s/head rate is borrowed from a different mechanism, not a magnetic capability. Four binary planes are one encoding assumption, not a lower bound for fluidic state storage. Neither timing nor site count ranks these undefined mechanisms against A-011.

A-011's inherited 20.18 s estimate and DES-006's 0.12919 mm combined structural screen remain conditional calculations. The latter exceeds its assumed 0.10 mm screen before omitted compliance; it does not prove an alternative passes.

Next useful evidence is a complete selection/energy/isolation/reset mechanism and full-board schedule: magnetic force and cross-talk over labelled gap bounds, or manifold selection and sneak-flow/pressure-settling bounds. Include positive support, arbitrary transitions, readback false acceptance and recovery. Compare against simple shared-writer mechanisms and the product constraints before choosing an informative physical calibration. Stop embodiments that fail conservative cost, reach or timing bounds; reopen only with changed mechanism or assumptions supported by evidence. No mandatory 5×5 article or fixed cycle count follows from this screen.
