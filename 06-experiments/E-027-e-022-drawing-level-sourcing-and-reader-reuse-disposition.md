---
status: complete
builds-on: [E-022, E-018, DES-003, E-026]
---

# E-027: E-022 drawing-level sourcing and reader-reuse disposition

Date basis: 2026-10-07. This is a drawing-level sourcing and compatibility
screen, not an RFQ response, purchase, fit test, or physical-performance
claim. Purchased-component cost only; 3D-printed parts, labour, freight, tax,
payment fees, and validation fixtures are excluded unless explicitly shown.

## Bounded RFQ/sourcing screen

The requested package is five identical reusable planes (four installed plus
one service plane) and one local clamp/fiducial set. The supplier drawing
must preserve the E-018 interface: 40 x 40 x 3.00 mm frame, 34 x 34 x
0.80 mm planes, 3 x 3 mm apertures on 5.08 mm pitch, two Ø2 mm fiducials,
positive 2 x 6 mm datum, four 1 x 0.8 mm writer tabs on 2 mm centre pitch,
and the 2 mm reader-standoff target.

| RFQ field | Required record | Current screen disposition |
|---|---|---|
| Material/thickness | Grade, temper/finish, nominal and tolerance | 304 stainless at 0.76 mm is a sourced catalogue thickness observation; 0.80 mm E-018 nominal remains unresolved. 301/304 photo-etch at 0.10–0.20 mm and polymer film are alternatives, not drop-in selections. |
| Aperture process | Laser/chemical etch/other, kerf or taper, deburr, edge condition | Laser cut plus deburr is the preferred baseline. SendCutSend publicly states ±0.005 in cut tolerance and 2–4 business-day production; this does not close the E-018 residual or burr gate. Source: https://sendcutsend.com/materials/stainless-steel/ |
| Geometry/tolerances | Aperture position, fiducials, tab, datum, flatness, burr/edge, repeatability | Must be quoted against the supplied drawing; no supplier quote or tolerance stack exists. Acceptance target is transformed aperture residual ≤0.20 mm after reseat, not the catalogue cut tolerance alone. |
| Quantity/MOQ | Five identical planes and one clamp/fiducial set; MOQ and setup charge | MOQ 1 is publicly supported for the referenced laser-cut route; identical-five setup/quantity pricing is unresolved. Clamp estimate assumes MOQ 1. |
| Lead time | Production, queue, and any material lead | Public laser-cut observation: 2–4 business days; exact material, five-piece queue, and clamp lead time require RFQ. |
| Packaging | Flat protective packaging, separator, moisture/deburr protection | Supplier packaging specification is unresolved; require flat shipment with no aperture/tab deformation and identify packaging charge. |
| Price basis | Five-plane price, clamp-set price, tooling/setup, currency, validity | No quote exists. Planning estimates below are not delivered prices. |
| Exclusions and delivery | Explicit freight, tax, duty, payment fees, and delivery destination | All are excluded from this analytical screen; a real RFQ must state Incoterm/destination and delivered-price total separately. |

### Planning BOM, one reference machine

| Item | Qty | Low USD | Base USD | High USD | Classification |
|---|---:|---:|---:|---:|---|
| Reusable 304-SS planes, five total | 5 | 20 | 60 | 150 | E-022 allowance; not a fit-selected quote |
| Local clamp, hard datum, latch, fiducial set | 1 | 15 | 35 | 80 | E-022 allowance; laser-cut/dowel baseline is estimated at $20–45 |
| Four writer actuators | 4 | 36 | 60 | 120 | E-022 allowance; candidate observations below do not replace it |
| DRV8833CRTER | 2 | 4.38 | 4.38 | 4.38 | Sourced catalogue observation: $2.19 each at Digi-Key listing, 2,930 shown in stock when recorded. [Source](https://www.digikey.com/en/products/detail/texas-instruments/DRV8833CRTER/5039360) |
| Raspberry Pi Pico SC0915 | 1 | 4.59 | 4.59 | 4.59 | Sourced catalogue observation: $4.59, 43,224 shown in stock when recorded. [Source](https://www.digikey.com/en/products/detail/raspberry-pi/SC0915/2648-SC0915CT-ND/13684020) |
| Pololu 5615 3-pin cable example | 8 | 18.32 | 18.32 | 18.32 | Sourced catalogue observation: $2.29 each, 118 shown in stock when recorded. [Source](https://www.pololu.com/product/5615) |
| Cleaning/service allowance | 1 | 10 | 30 | 75 | E-022 allowance |

The inherited DES-003 purchased baseline is $370.00 and remains separate.
The canonical E-022 totals remain **$486.29–$872.29** for reader reuse and
**$505.59–$921.59** with the explicitly costed fallback reader stack. The
fallback QRE1113/ADC/carrier rows are alternatives and are not additive to a
reuse case.

### Controlled RFQ payload and acceptance gates

Send one controlled request with the plane and clamp portions quoted
separately, including all setup/tooling charges. Specify five identical
reusable planes plus one clamp/fiducial set against the E-018 nominal datum:
40 x 40 x 3.00 mm frame, 34 x 34 x 0.80 mm carrier, twenty-five 3.00 x
3.00 mm apertures on 5.08 mm pitch, two Ø2.00 mm fiducials at (-15,-15)
and (15,15) mm, positive 2 x 6 mm datum rail, four labelled 1 x 0.80 mm
writer tabs on 2.00 mm centre pitch, and reader target 2.00 mm above the
upper carrier. Request deburred 304 stainless at nominal 0.76 mm or a
supplier-recommended stock that preserves the envelope; require actual
grade, temper, thickness, tolerance, aperture/fiducial/tab/datum positional
tolerances, flatness, burr/edge condition, process/kerf or etch taper, MOQ,
setup/tooling, lead time, flat protective packaging, unit/extended price,
quote validity, freight/delivery basis, and drawing exceptions. Quote the
clamp plate, two locating dowels, latch hardware, and any shim separately.

Technical acceptance requires the mechanical owner to close the E-018
envelope/no-collision overlay, clamp reseat residual ≤0.20 mm after 100
reseats, and loaded-neighbour isolation. The published ±0.127 mm catalogue
cut-tolerance observation is a process input, not acceptance evidence. The
mechanical owner owns overlay/reseat gates; Cost & Sourcing owns quote
completeness and price normalization.

## Exact actuator candidate and sample path

The one exact candidate carried forward is Olimex
`PUSH-PULL-SOLENOID-5V`, Digi-Key `1188-PUSH-PULL-SOLENOID-5V-ND`.
The recorded public listing showed 5.00 mm stroke, 5–6 V, 6 ohm coil,
$3.34 each, zero stock and one estimated 2026-10-15 availability date when
screened; manufacturer standard lead time was shown as five weeks. These are
catalogue observations tied to the listing, not a supplier commitment:
https://www.digikey.com/en/products/detail/olimex-ltd/PUSH-PULL-SOLENOID-5V/23330937

The four-unit price observation is `4 × $3.34 = $13.36`. The 6 ohm/5 V
nominal current calculation is `0.833 A`; it is not a driver-margin result.
The candidate/sample path is: obtain one exact part or manufacturer data
package, make a 1:1 E-018 tab/stop gauge, then record force-versus-stroke,
return force/park behaviour, usable stroke at the hard stop, envelope,
insertion coupling, pulse duty/current/thermal margin, and life/repeatability.
No sample was ordered and no sample result exists.

The actuator request is controlled to this exact candidate only: Olimex
`PUSH-PULL-SOLENOID-5V`, Digi-Key `1188-PUSH-PULL-SOLENOID-5V-ND`, quantity
one sample plus a four-unit price break. Require the exact manufacturer part
number, not a family substitute. Acceptance requires documented force at the
1.00 mm tab engagement, usable-stroke/stop stack, mounting envelope and
parked clearance, return behaviour, coil current/driver thermal margin, and
cycle-life/repeatability evidence. The controls/mechanical owner closes fit,
force, return, and driver gates; Cost & Sourcing closes exact-part identity,
availability, price, lead time, and evidence provenance. If any gate remains
open, retain the existing $9/$15/$30 actuator allowance and do not replace it
with the $3.34 observation.

| Actuator gate | Status | Why it remains open |
|---|---|---|
| Force vs stroke | Unresolved | Public listing has no force curve at the 1 mm tab interface. |
| Life/repeatability | Unresolved | No exact-part life or positional tolerance evidence recorded. |
| Stroke coupling | Conditional only | 5 mm catalogue stroke exceeds the 1 mm nominal tab overlap; a stop and travel stack are required. |
| Envelope | Unresolved | Mounting, plunger axis, parked clearance, frame and neighbour overlay are absent. |
| Return/latching | Unresolved | Push-pull wording does not close spring return or power-loss parked state. |
| Drive | Conditional only | 5 V/6 ohm is electrically plausible for the existing low-voltage H-bridge; current limit, flyback, duty and thermal margin are not calculated. |
| Availability/price | Sourced observation only | $3.34 and listing availability were time-bound; no quote or commitment. |

The Delta DSML-0224-12 family remains a non-selected alternative: its
recorded 12 V family observation conflicts with the bounded DRV8833 supply
path and would require a separately costed driver/power boundary. An MG90D
servo is also non-selected because it adds PWM/power and horn/linkage parts.

## DES-003 reader reuse overlay and timing checklist

Reuse is **not accepted** and contributes $0 only as a conditional BOM
alternative. The inherited DES-003 $370 baseline supplies the eight heads,
but no dimensioned DES-003 head/mount/connector drawing or calibration record
was found in the evidence reviewed.

| Gate | E-018 comparison and required closing evidence | Disposition / provenance |
|---|---|---|
| XY target | Centre 3 x 3 mm window, 5.08 mm pitch, two fiducials; overlay beam centre and mount datums, then calculate centre/corner residual ≤0.20 mm | **Unresolved** — E-018 is CAD-derived; DES-003 head data absent |
| Z stack | E-018 lower face nominal 2.00 mm above upper carrier versus DES-003 1.80 mm design point; stack carrier flatness, clamp/reseat, mount and collision clearances | **Conditional, not pass** — 0.20 mm subtraction is a calculation on different target surfaces |
| Optical field/contrast | Compare emitter/detector field and spot to 3 x 3 mm mask window, material finish, ambient and saturation limits | **Unresolved** — DES-003 optical point is an assumption/model, not mask contrast evidence |
| Plane identity/isolation | Ray/occlusion overlay for four 1.20 mm plane separations, tabs, and loaded N/E/S/W dummies; exact four-plane state required | **Unresolved** — no plane-specific optical drawing/calibration |
| Cabling/pinout | Connector, polarity, retention, cable OD/bend radius, strain relief and carrier exit must fit without uncosted adapter/PCB | **Unresolved** — inherited loom is an assumption |
| Timing | Include pulse/sample/settle, eight-head schedule, complete 100-value readback, fiducials, reject and retry; inherited `30.00 - 20.18 = 9.82 s` is planning margin only | **Conditional planning bound, not measured** |
| Calibration/fault | Frozen calibration ID/threshold and deterministic wrong/ambiguous/missing = reject trace for all four planes | **Unresolved** — no calibration/fault record |

If any reader gate fails, add the E-022 fallback allowance only after a
separate fallback optical drawing. Do not add QRE1113, MCP3008, or a reader
carrier to this reuse BOM by assumption.

## Cost reduction disposition and cheapest next falsifier

The preferred reductions are component-removing: reuse DES-003 readers if
the overlay passes, and retain local clamping instead of introducing a full
cassette transport. Both reduce unique purchased parts and assembly, but
increase dependence on optical margin, registration, debris control, and
service access. The $3.34 actuator is not a valid saving until force, stop,
return, life, driver thermal margin, and availability close. Thin etched or
polymer planes may lower unit price but add buckling, creep, wear, cleaning,
and writer-contact risk; they remain experiments, not baseline reductions.

The cheapest decisive next falsifier is a drawing-only DES-003 overlay plus
one exact-actuator force/return/stop-data package (or one sample if data are
unavailable). It closes the highest-value reuse and actuator gates without
ordering a five-plane set, adding fallback electronics, or claiming hardware
compatibility.

## Result

The bounded disposition is: **E-018 sourcing is feasible only as an RFQ
target, not a sourced quote; the Olimex actuator is a conditional,
non-selectable candidate; DES-003 reader reuse is unresolved; canonical E-022
reuse/fallback ranges are preserved.** Analytical geometry and timing do not
prove hardware performance. No procurement, supplier commitment, CAD release,
or physical test is authorized by this record.
