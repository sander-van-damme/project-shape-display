---
status: active
builds-on: [DES-003]
---
---
status: active
builds-on: [E-022, E-018, DES-003]
---

# E-023: mask-generator drawing-level sourcing and compatibility screen

Date basis: 2026-10-07. Currency: USD. This is a bounded catalogue and
fabrication-route screen for one reference machine. It excludes 3D-printed
parts, labour, freight, tax, payment fees, and validation fixtures. It is not
a quote, procurement commitment, CAD release, or physical validation.

## Drawing boundary

The screen covers five reusable media planes (four installed plus one service
plane), one local clamp/fiducial set, four writer actuators, and reuse of the
eight DES-003 reader heads. The E-018 drawing envelope is the compatibility
authority: 40 x 40 x 3 mm frame, 34 x 34 x 0.8 mm plane carriers, 3 x 3 mm
apertures on 5.08 mm pitch, two 2 mm fiducials at diagonal 15 mm offsets,
four 1 x 0.8 mm writer tabs on 2 mm stack pitch, and a frame-fixed reader
target with nominal 2 mm standoff above the upper carrier. These are CAD
nominals, not measured capability.

## Media candidates

| Candidate / process | Material and thickness | Aperture/process capability | Tolerance / life implication | MOQ / lead time / packaging | Price basis for five planes | Screen result |
|---|---|---|---|---|---:|---|
| Laser-cut 304 stainless sheet | 304 SS, nearest public catalogue thickness 0.76 mm (0.030 in); E-018 carrier nominal is 0.80 mm | Laser cut plus deburr; 3 mm apertures are geometrically large, but 2.08 mm webs must satisfy the vendor's minimum-feature rules | SendCutSend states ±0.005 in (±0.127 mm) cut tolerance and 2–4 business-day production; this is too loose to assume the ±0.20 mm reseat/aperture residual gate without a drawing quote | MOQ 1 is supported by instant-quote size range; normal cut packaging; custom quote for five identical planes | Sourced capability observation; **$15–35/plane allowance**, $75–175 total, not a quote | **Preferred rigid baseline**, but thickness mismatch, edge burr, flatness, and aperture positional tolerance remain gates. Source: https://sendcutsend.com/materials/stainless-steel/ |
| Photo-etched spring stainless | 301/304 spring SS, target 0.10–0.20 mm; carrier/backing needed to retain E-018 0.8 mm envelope | Chemical etch is a plausible fine-aperture process; vendor-specific minimum web, taper, and positional tolerance must be quoted | Lower mass and potentially better aperture fidelity; thin sheet can buckle, crease, or wear under writer contact; no life data selected | Usually quote/MOQ dependent; assume 1–4 weeks and flat protective packaging until supplier confirms | **Estimate $20–60/plane**, $100–300 total; no public fit price used | **Candidate for a coupon only**; do not cost as a drop-in plane until carrier, springback, and writer contact are specified |
| Laser-cut PET/polyimide film | PET or polyimide, target 0.10–0.25 mm; not self-supporting at E-018 span without a frame | Laser/knife-cut apertures are feasible in principle; heat-affected edge, curl, and opaque/reflective optical finish are unresolved | Lowest mass and likely lowest piece price, but creep, tear, blocked aperture, and cleaning compatibility threaten reusable life | MOQ and lead time supplier-specific; protective film or flat bag required | **Estimate $3–10/plane**, $15–50 total; not a sourced price | **Rejected as first reusable baseline**; retain only as a cost-down experiment after metal coupon evidence |

The five-plane requirement is not five arbitrary loose sheets: each candidate
must retain the E-018 datum, fiducials, labelled plane tab, aperture position,
flatness, and cleanable surface after writer engagement. The stainless public
capability is useful for process screening, but its published tolerance is not
evidence that the assembled mask meets the 0.20 mm transformed-aperture gate.

## Clamp and fiducial candidates

| Candidate | Material / process | Geometry and tolerance target | MOQ / lead time / packaging | Price basis for one set | Engineering screen |
|---|---|---|---|---:|---|
| Standard dowel pins + laser-cut datum plate + latch hardware | Hardened stainless dowels, 304 plate, deburred laser cut; purchased pins and fasteners | Two Ø2 mm fiducial locations and one positive 2 x 6 mm datum rail; drawing target ±0.05 mm pin location, clamp preload adjustable | MOQ 1 for plate quote; 2–4 business days for standard laser cut, pins from stock; bagged/boxed hardware | **Estimate $20–45**; no fit-selected part numbers | **Preferred sourcing route**: few unique parts, serviceable, but pin/plate stack and burr control need inspection |
| Custom machined clamp/fiducial block | 6061-T6 or stainless, CNC/drilled/reamed | Better datum control and hard stop; tolerance can be quoted against E-018, but adds mass and machining features | MOQ 1; quote/lead time typically supplier-specific; protective packaging | **Estimate $45–90** | Reliability fallback if laser-cut stack cannot hold reseat repeatability; higher cost and unique part count |
| Printed clamp or printed fiducial substitute | Printed polymer | Nominal geometry is easy, but creep, wear, and hole repeatability are unresolved | No purchased-component cost | Excluded from comparable BOM | **Rejected for this cost screen**: it silently transfers registration risk to an unvalidated printed mechanism |

The local clamp is retained over a full cassette/transport. That removes moving
transport parts but makes positive seating, loaded-neighbour isolation, and
cleaning access acceptance gates; it is not a free reliability improvement.

## Four-actuator sourcing screen

| Candidate / source observation | Force / stroke / life / tolerance | MOQ / lead time / packaging | Four-unit price basis | Interface and compatibility |
|---|---|---|---:|---|
| Olimex PUSH-PULL-SOLENOID-5V, Digi-Key 1188-PUSH-PULL-SOLENOID-5V-ND | 5.00 mm stroke, 5–6 V, 6 ohm; public listing does **not** provide force, cycle life, or positional tolerance | Digi-Key listing observed 0 in stock with 1 estimated 2026-10-15; manufacturer standard lead time 5 weeks; bulk | **Sourced catalogue observation: $3.34 each, $13.36/4** | Coil can be driven by an H-bridge, but E-018 only provides a 1 mm tab overlap and no 5 mm travel/force envelope. Requires a rigid stop, return strategy, force/stroke test, and duty-cycle check. **Not selectable yet.** Source: https://www.digikey.com/en/products/detail/olimex-ltd/PUSH-PULL-SOLENOID-5V/23330937 |
| Delta DSML-0224-12 latching solenoid, Digi-Key family page | 5.08 mm stroke; latching behavior can reduce hold power; force, life, package envelope, and positional tolerance remain part-number-specific | Family page showed 898 available for the 12 V variant; immediate listing; bulk packaging | **Sourced family observation: $9.42 each, $37.68/4** | H-bridge-compatible pulse actuation is attractive, but 5.08 mm is not proof of the required tongue motion or force. Requires exact datasheet, mounting/envelope check, and cycle-life evidence. **Candidate fallback.** Source: https://www.digikey.com/en/product-highlight/d/delta-electronics/dsml-series-latching-solenoids |
| Adafruit MG90D metal-gear servo, product 1143 | 90° nominal motion, 2.1 kg-cm stall torque at 4.8 V, 0.1 s/60°; no guaranteed cycle life or repeatability tolerance on listing | Listing observed out of stock; quantity discounts shown; includes cable/horns, retail packaging | **Sourced catalogue observation: $9.95 each, $39.80/4** | **Not a drop-in DRV8833 option**: needs four PWM channels and servo power/interface, plus horn-to-tab linkage. Rotation can provide stroke, but backlash, stall duty, and link tolerance must be tested. **Rejected for current BOM, retained as alternative.** Source: https://www.adafruit.com/product/1143 |

The existing E-022 actuator allowance ($9/$15/$30 each) remains the
comparable planning term. The catalogue prices do not collapse it by
themselves: the $3.34 solenoid has no force/life data and uncertain stock,
the $9.42 latching solenoid lacks the exact fit data, and the $9.95 servo
would add electronics and assembly. A cheaper unit price is not a saving if
it adds a carrier, return spring, driver, or early-life replacement path.

## DES-003 reader-head reuse checklist

Reuse contributes $0 incremental cost only after all eight heads pass a
drawing-level and timing screen. The following is the required record; no
item is currently physically verified.

| Gate | E-018 / inherited requirement | Required evidence | Status |
|---|---|---|---|
| XY target | E-018 centre 3 x 3 mm window at 5.08 mm pitch; two fiducials and transformed residual ≤0.20 mm | DES-003 aperture/beam centre and head mount overlay against E-018 drawing | Unresolved |
| Z stack | E-018 reader lower face nominal 2.00 mm above upper carrier; DES-003 optical design used 1.8 mm standoff above its flag target | Dimensioned head-to-plane stack with tolerance; confirm no carrier or writer collision | Unresolved; 0.2 mm nominal difference is not interchangeable |
| Optical field | DES-003 reader aperture/spot was designed around a 0.44 mm aperture and reflective flag; E-018 target is a 3 x 3 mm mask window and may have different contrast/texture | Emitter/detector aperture, spot/field, working distance, reflectance/ambient margin against each mask material | Unresolved |
| Plane identity | Four-plane stack has 2.00 mm port pitch and plane-specific tabs; reader must not classify adjacent planes or loaded neighbours | Drawing ray/occlusion check and per-plane optical isolation record | Unresolved |
| Cabling | DES-003 loom/controller pinout and connector retention must match the E-018 reader position without new uncosted harness/PCB | Pinout, connector, polarity, cable bend radius, strain relief, and carrier drawing | Unresolved |
| Timing | E-017 lower anchor is 71 cells/s/head; complete readback and retry must remain inside the 30 s analytical boundary | Controller pulse width, settle time, ADC/sample timing, eight-head parallel schedule, and worst-case retry arithmetic | Unresolved |
| Calibration/fault behavior | E-018 requires exact four-plane readback and wrong/ambiguous/missing = reject | Calibration ID, threshold, saturation/ambient test plan, and fault-code mapping | Unresolved |

No fallback QRE1113, MCP3008, or reader-carrier cost is added to the reuse
case. If any gate fails, add E-022's fallback allowance only after a separate
sensor/optics drawing is made; catalogue availability alone does not show that
the 1 mm nominal QRE1113 sensing distance fits this stack.

## Bounded arithmetic

The inherited DES-003 purchased baseline remains $370.00. The following
incremental numbers are comparable purchased-component arithmetic only:

| Screen case | Calculation | Result |
|---|---|---:|
| Four Olimex actuators, sourced price only | `4 x 3.34` | $13.36 |
| Four Delta actuators, sourced family price only | `4 x 9.42` | $37.68 |
| Four MG90D servos, sourced price only | `4 x 9.95` | $39.80 |
| Five stainless planes, planning allowance | `5 x (15 / 35)` low/base planning band | $75 / $175 |
| Clamp/fiducial, standard stack planning band | `1 x (20 / 45)` low/base planning band | $20 / $45 |

These rows are alternatives, not additive. A reuse-verified boundary using the
E-022 sourced electronics/harness and the above *screening* bands would be:

`$370 + media ($75/$175) + clamp ($20/$45) + actuators ($13.36/$37.68) + 4.38 + 4.59 + 18.32 + service allowance ($30)`

which calculates to **$535.65 low-screen / $654.97 base-screen** before any
fallback reader stack. This is not a replacement for E-022's $486.29–$872.29
range: the stainless and clamp bands are estimates with unresolved fit, and
the low actuator is not yet viable. Keep E-022 canonical until drawings and
quotes replace these planning bands.

## Rejected reductions and decision

* The $3.34 solenoid is not accepted solely on unit price: force, life,
  stroke coupling, stock, and duty cycle are missing.
* The servo is not accepted as a cheap substitute because it needs a new
  four-channel PWM/power interface and introduces backlash/linkage parts.
* PET/polyimide film is not accepted as the reusable baseline because tear,
  creep, aperture-edge damage, and cleaning life are unresolved.
* Removing readback or serializing the four writers is rejected: it removes
  fault observability or violates the inherited arbitrary-map timing boundary.
* A full cassette transport is not priced or added; local clamping remains
  the bounded architecture assumption.

The preferred next screen is five identical 304 SS planes plus a standard
dowel/laser-cut clamp set, quoted against the E-018 drawing, and one exact
actuator sample of the Delta or Olimex family with a force-vs-stroke and
cycle-life request. In parallel, the DES-003 owner should complete the
reader overlay/timing checklist before any fallback-reader purchase is
considered.

## Next falsification/procurement action and owner

Next owner: **DES-003 mechanical/controls owner**, with Cost & Sourcing
support. Send one drawing-level RFQ for five planes, one clamp/fiducial set,
and four actuator samples or a manufacturer quote. Require material,
thickness, aperture process, force/stroke, life, tolerances, MOQ, lead time,
packaging, freight, and delivered price. Record all eight reader-head
dimensions, optical stack, connector/pinout, sample/settle timing, and
calibration margin against the E-018 checklist. This is the next falsifier;
do not order parts, redesign CAD, or claim hardware compatibility from this
document.
