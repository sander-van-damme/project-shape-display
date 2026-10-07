---
status: complete
builds-on: [E-023, E-018, E-022]
---

# E-024: drawing-level reader and actuator compatibility screen

Date basis: 2026-10-07. This is a drawing/calculation screen only. It does
not claim a reader measurement, actuator fit, force result, cycle-life result,
or hardware validation. E-022's canonical **$486.29–$872.29 reuse range** and
**$505.59–$921.59 fallback-reader range** are unchanged.

## Boundary and method

The authority for this screen is the E-018 coupon: 40 x 40 x 3.00 mm frame,
34 x 34 x 0.80 mm carriers, 5.08 mm cell pitch, 3 x 3 mm apertures, two
Ø2.00 mm fiducials at (-15,-15)/(15,15) mm, a centre reader target, and four
1.00 x 0.80 mm writer tabs on 2.00 mm centre pitch. The inherited DES-003
reader assumptions are only those recorded in E-023/DES-003: an optical
design point around a 0.44 mm aperture, 1.8 mm flag-target standoff, eight
head positions, and 71 cells/s/head lower rate. No DES-003 drawing with head
envelope, beam centre, connector, or tolerance is present in the evidence
screened here.

The overlay therefore uses a falsification rule: a gate is **pass** only when
the cited drawing or calculation closes it; **conditional** when the nominal
geometry is plausible but a bounded datum is missing; **fail** when the
candidate conflicts with an existing interface; and **unresolved** when only
supplier or physical evidence can close it.

## Reader-head overlay

| Gate | Drawing-level comparison | Disposition | Exact closing evidence |
|---|---|---|---|
| XY target | E-018 centre window is 3 x 3 mm at the 5.08 mm field pitch. DES-003 beam/aperture centre and head mount XY are not dimensioned. | **Unresolved** | DES-003 head and mount drawing overlaid to E-018 datums; calculated beam-centre residual and tolerance stack, with transformed active-aperture residual ≤0.20 mm. |
| Z stack | E-018 places the reader lower face 2.00 mm above the upper carrier. DES-003 assumes 1.80 mm above its flag target: nominal difference = 0.20 mm, but the target surface and tolerance are different. | **Conditional** | Dimensioned head-to-carrier stack including carrier flatness, clamp/reseat, head mount, and optical working-distance tolerance; prove no writer/tab collision through the full stack. |
| Optical field | DES-003's 0.44 mm reflective-flag aperture/spot is not evidence of usable contrast over an E-018 3 x 3 mm mask window or its material/finish. | **Unresolved** | Emitter/detector field drawing plus material reflectance/ambient margin and saturation limits for every selected plane state. |
| Plane identity / occlusion | Four carriers are separated by 1.20 mm and writer ports are 2.00 mm apart. E-018 requires exact four-plane state and rejects wrong/ambiguous/missing; DES-003 has no documented ray/occlusion overlay for this stack. | **Unresolved** | Ray/occlusion drawing for selected and adjacent planes, loaded N/E/S/W dummies, and a plane-specific calibration record. |
| Cabling/interface | E-022 assumes inherited loom/controller infrastructure, but E-023 has no DES-003 connector pinout, retention, bend-radius, strain-relief, or head-carrier drawing. | **Unresolved** | Connector/pinout and cable mechanical drawing; confirm no new PCB, harness, adapter, or uncosted strain relief. |
| Timing | E-017/E-022 analytical lower anchor is 71 cells/s/head. E-018 requires settle, complete 4 x 25 readback, fiducials, reject handling, and bounded retry. | **Conditional** | Controller pulse/sample/settle schedule and worst-case retry calculation. The inherited E-017 full-map accounting is 20.18 s, leaving 9.82 s analytical margin to 30 s before any new reader delay; this is not measured timing. |
| Calibration/fault | E-018 freezes reader threshold 0.85 and requires exact-state comparison; DES-003 calibration ID, threshold behavior, saturation and missing-signal fault map are absent. | **Unresolved** | Calibration record, threshold/ambient limits, missing/ambiguous fault mapping, and a software schema trace to the E-018 reject rule. |

No reader gate is a physical pass. A failed gate requires either a revised
DES-003 overlay or the explicitly costed E-022 fallback stack; it does not
authorize silently adding QRE1113 sensors, an ADC, or a new reader carrier to
the reuse case.

## Actuator screen

The required writer motion is not specified beyond a 1.00 mm nominal tab
overlap/insertion interface. Therefore stroke numbers cannot be accepted as
fit evidence: the missing quantities are required tab travel, hard-stop
location, return force, engagement force, and actuator envelope inside the
40 mm frame/loaded-neighbour boundary.

| Gate | Olimex PUSH-PULL-SOLENOID-5V | Delta DSML-0224-12 latching solenoid | Disposition / evidence |
|---|---|---|---|
| Stroke | Catalogue observation: 5.00 mm. The E-018 interface only proves 1.00 mm overlap; 5.00 mm may overtravel the tab. | Catalogue family observation: 5.08 mm. Same missing travel coupling; nominal equality to 5.08 mm pitch is not a motion requirement. | Both **conditional**. Dimension writer tab travel and hard stop; calculate usable stroke and tolerance. |
| Force | Public listing provides no force curve. | Exact part number and force curve are not identified. | Both **unresolved**. Obtain force-vs-stroke at the E-018 contact geometry, including friction and clamp preload. |
| Envelope / writer-tab geometry | Body, mounting, plunger axis, and return clearance are not in E-023. | Family page does not close exact body/mount dimensions; 5.08 mm is stroke, not package clearance. | Both **unresolved**. CAD envelope overlay against tabs, frame edge, dummy neighbours, and parked 0.20 mm clearance. |
| Return / latch | Push-pull description does not establish spring return, neutral position, or fail-safe parked state. | Latching behavior can hold state without continuous power, but requires a reverse pulse and defined power-loss state. | Olimex **unresolved**; Delta **conditional at mechanism level**, unresolved at fail-safe level. Supply return/latch schematic and power-loss behavior. |
| Driver/interface | 5–6 V, 6 Ω coil is electrically plausible with the existing DRV8833 low-voltage H-bridge; current, inrush, thermal duty, and flyback behavior are not calculated from a selected driver layout. | 12 V variant conflicts with the existing DRV8833 motor-supply boundary; accepting it requires a new 12 V-compatible H-bridge/power path, which would add parts. | Olimex **conditional**; Delta **fail for the bounded no-added-parts path**. Exact coil current and driver thermal/duty calculation required for Olimex. |
| Duty cycle / life | No cycle-life or positional tolerance data. | No exact-part cycle-life or positional tolerance data. | Both **unresolved**. Require life rating or supplier evidence at the E-018 pulse schedule; unit price is not acceptance. |
| Price | $3.34 each, $13.36/4 catalogue observation; listing showed zero stock in E-023. | $9.42 each, $37.68/4 family observation for 12 V variant. | Prices are **not fit evidence** and do not change E-022. |

### Bounded actuator disposition

For the requested bounded option, carry the Olimex 5 V solenoid only as a
**conditional candidate for the next drawing/force falsification**. It is the
only listed candidate that is electrically compatible with the existing
low-voltage H-bridge without adding a voltage rail or driver class. It is not
selected, because stroke coupling, force, return behavior, envelope, duty,
life, and availability remain open.

The Delta 12 V latching solenoid is a **fail for this bounded integration
path**, not a claim that the part is mechanically unsuitable in all designs.
Its 5.08 mm stroke and latching feature are insufficient to overcome the
12 V/DRV8833 interface conflict. Reconsideration requires a separately
costed 12 V driver/power assembly and exact-part drawing; that would be a
new integration boundary, not a silent substitution. The MG90D servo remains
rejected from this screen because it needs PWM/power and horn/linkage parts.

## Cheapest credible next falsification

The cheapest credible action is a drawing-only DES-003 owner handoff before
any purchase: release the reader head/mount envelope, beam centre and optical
working-distance data, connector/pinout, and timing trace; overlay them on the
E-018 CAD/datum coordinates. In parallel, make a 1:1 tab/stop gauge from the
E-018 1 mm tab and obtain one Olimex force-vs-stroke/return/life data package.
This closes the highest-risk reuse and actuator gates without ordering parts.

If supplier-dependent evidence is needed after the drawing screen, request
one Olimex sample or manufacturer data for force, return, duty, life and
exact dimensions. This is a handoff for future physical/supplier work, not
physical validation. Do not request or place an order as part of E-024.

## Cost, integration, and rollback

The $13.36 Olimex and $37.68 Delta four-unit arithmetic is recorded only as
catalogue observation. Neither replaces E-022's $9/$15/$30 actuator planning
allowance or changes its canonical total. A reader reuse failure adds the
E-022 fallback allowance only after a separate fallback optical drawing is
made. No extra driver, return spring, carrier, harness, ADC, or power rail is
included implicitly.

Integration is limited to a conditional drawing update and an evidence
attachment to E-023/E-018. Rollback is deleting this E-024 result and
reverting its commit; E-018, E-022, E-023, and DES-003 remain unchanged.

## Reproducibility and result

The numerical checks in this object are reproducible directly from the
recorded inputs:

* four-plane stack separation count: `4 × 0.80 + 3 × 1.20 = 6.80 mm`, before
  frame/clamp tolerances;
* inherited timing margin: `30.00 − 20.18 = 9.82 s` analytical margin;
* four-unit catalogue arithmetic: `4 × 3.34 = $13.36` and
  `4 × 9.42 = $37.68`;
* nominal DES-003/E-018 standoff difference: `2.00 − 1.80 = 0.20 mm`.

These calculations do not prove fit, force, optical classification, life, or
hardware performance. Final gate disposition is: reader XY, optical field,
plane identity, cabling, and calibration **unresolved**; reader Z and timing
**conditional**; Olimex **conditional candidate**; Delta **fail for the
bounded existing-driver path**. The next owner is the DES-003
mechanical/controls owner with Cost & Sourcing support.
