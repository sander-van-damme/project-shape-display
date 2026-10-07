---
status: complete
builds-on: [E-022, E-023, E-018]
---

# E-040: E-022/E-023 quote-ready mask-generator sourcing and compatibility handoff

Date basis: 2026-10-07. Currency: USD. Purchased components only; 3D-printed
parts, labour, freight, tax, payment fees, and validation fixtures are excluded.
This is a quote/RFQ package and arithmetic reconciliation, not a supplier quote,
purchase commitment, CAD release, or physical validation.

## Reconciled baseline and terminology

E-022 remains the canonical planning baseline. The separate DES-003 shared
machine term is **$370.00**, not the complete mask-generator BOM. Its inherited
reader heads contribute $0 only if the E-018 compatibility gates close. The
QRE1113/MCP3008/carrier rows are a fallback reader path and are alternatives,
not additions to a reader-reuse case.

The E-022 arithmetic is reproducible:

| Case | Calculation | Total | Classification |
|---|---|---:|---|
| Reader reuse / low | `370+20+15+8+36+4.38+4.59+18.32+10` | **$486.29** | canonical allowance + catalogue observations |
| Reader reuse / base | `370+60+35+20+60+4.38+4.59+18.32+30` | **$602.29** | canonical allowance + catalogue observations |
| Reader reuse / high | `370+150+80+50+120+4.38+4.59+18.32+75` | **$872.29** | canonical allowance + catalogue observations |
| Fallback reader / low | reuse low `+6.40+2.90+10` | **$505.59** | alternative fallback allowance |
| Fallback reader / base | reuse base `+6.40+2.90+20` | **$631.59** | alternative fallback allowance |
| Fallback reader / high | reuse high `+6.40+2.90+40` | **$921.59** | alternative fallback allowance |

E-023's stainless/clamp/actuator screening arithmetic is not a new baseline.
Its stated base expression is corrected to **$684.97**:
`370+175+45+37.68+4.38+4.59+18.32+30`. Its stated $535.65 low-screen
number also uses the $30 service allowance. If “low” means E-022's $10 service
allowance, the corresponding calculation is **$515.65**; this is the remaining
documented discrepancy. Do not silently substitute either screening value for
E-022's canonical range, because the $13.36 Olimex price and the stainless and
clamp bands are not fit-accepted selections.

## Quote-ready package

Issue one RFQ with separate extended-price lines, setup/tooling, MOQ, lead time,
packaging, freight, quote validity, and drawing exceptions. The supplier must
return exact manufacturer/material identification, not a family substitute.

| RFQ line | Qty and required identity | Minimum acceptance record before procurement |
|---|---|---|
| Reusable media planes | **5 identical planes**: four installed plus one service/replacement plane; controlled E-018 drawing | Material grade/temper/finish; actual thickness and tolerance; 40 x 40 x 3.00 mm frame; 34 x 34 x 0.80 mm carrier; 25 square 3.00 mm apertures on 5.08 mm pitch; two Ø2.00 mm fiducials at diagonal ±15 mm; positive 2 x 6 mm datum rail; four labelled 1 x 0.80 mm writer tabs on 2.00 mm centre pitch; flatness, aperture/fiducial/tab/datum positional tolerance, burr/edge condition, cleaning compatibility, process/kerf or etch taper, life or wear evidence, MOQ, lead time, flat protective packaging, unit/extended price. Acceptance additionally requires E-018 overlay, no collision, and ≤0.20 mm transformed aperture/reseat residual; catalogue tolerance alone is insufficient. |
| Clamp/fiducials | **1 set**: hard datum, latch/preload, two locating dowels or specified equivalent, shim if required | Exact material/process and envelope; pin diameter and location; datum and stop geometry; clamp preload/adjustment; tolerance stack and flatness; service access; loaded-neighbour clearance; price and setup separately. Mechanical owner must close repeatability and isolation by the E-018 reseat/loaded-neighbour gates. |
| Writer actuators | **4 identical exact parts**, preferred quote target Olimex `PUSH-PULL-SOLENOID-5V`, Digi-Key `1188-PUSH-PULL-SOLENOID-5V-ND`; Delta DSML-0224-12 is a separately quoted fallback, not a substitution | Exact part number, envelope/mounting/termination, nominal 5.00 mm usable stroke, force-versus-stroke at 1.00 mm tab engagement, voltage/resistance/current, return or latching behaviour, duty/thermal limit, cycle life, positional/repeatability tolerance, availability, lead time, sample price and four-unit price. Existing DRV8833 compatibility is conditional on current/flyback/thermal evidence and the E-018 stop/parked-clearance stack. |
| Service stock | **1 allowance** covering cleaning consumables and one damaged/rejected plane event | Identify cleaner/wipes and media replacement basis, quantity, shelf/life assumptions, storage/packaging, and recurring replenishment price. Keep as an allowance until the medium and life test are selected. |
| Inherited reader reuse | **8 DES-003 heads**, no new purchase only if reuse gates pass | Dimensioned head/mount/connector data; XY/Z overlay; optical field/contrast; plane identity/isolation; pinout/cabling; complete-readback timing; calibration and wrong/ambiguous/missing reject record for all heads. If any gate fails, do not count $0; price the separate fallback optical drawing. |

The controlled drawing package must include the E-018 nominal geometry above,
plane labels, datum IDs, reader target at nominal 2.00 mm above the upper
carrier, writer stop and parked-clearance surfaces, material/finish callouts,
inspection datums, and revision/date. The minimum data package before A-011
integration is the released drawing plus supplier quote, actual material and
tolerance declaration, actuator datasheet/sample evidence, and the DES-003
reader overlay record. No integration or purchase is authorized by this record.

## Source classification

The following are catalogue observations recorded in E-022/E-023, not live
availability claims or quotes: DRV8833CRTER at $2.19 each; Raspberry Pi Pico
SC0915 at $4.59; Pololu 5615 cable example at $2.29; QRE1113 at $0.80; Olimex
PUSH-PULL-SOLENOID-5V at $3.34; Delta DSML family observation at $9.42; and
MG90D servo at $9.95. Source pages recorded with those observations are
[Digi-Key DRV8833](https://www.digikey.com/en/products/detail/texas-instruments/DRV8833CRTER/5039360),
[Digi-Key Pico](https://www.digikey.com/en/products/detail/raspberry-pi/SC0915/2648-SC0915CT-ND/13684020),
[Pololu cable](https://www.pololu.com/product/5615),
[Digi-Key Olimex](https://www.digikey.com/en/products/detail/olimex-ltd/PUSH-PULL-SOLENOID-5V/23330937),
and [SendCutSend stainless capability](https://sendcutsend.com/materials/stainless-steel/).
These pages do not establish current stock, delivered price, force/life,
drawing fit, or compatibility for this task. No external quote or live
availability was verified here.

All E-022 low/base/high media, clamp, actuator, and service values are
allowances. The $370 DES-003 amount is an inherited calculation. E-018 nominal
dimensions and gates are CAD/interface requirements; they are not physical
measurements. No catalogue observation may replace the acceptance evidence in
the RFQ table.

## Cost-reduction disposition

The preferred reductions remove parts: reuse the eight DES-003 readers after
the overlay/falsification screen, and retain local clamping instead of adding
a full cassette transport. These reduce purchased part count and assembly but
increase dependence on optical margin, reseat repeatability, debris control,
and service access. The $3.34 actuator observation is not a saving until force,
return, life, stop, driver thermal margin, and availability close. Thin etched
or polymer media may lower unit price but add buckling, creep, wear, cleaning,
and writer-contact risks; they remain experiment candidates. Removing readback
or serializing writing is rejected because it removes fault observability or
violates the E-017 timing boundary.

## Closure gate: exact status of the boundary

This table is the reconciled disposition for E-022/E-023. “Closed” means
closed as an analytical BOM/interface term only; it does not mean physically
qualified or supplier-committed.

| Term | Status | What is closed | What remains held or rejected |
|---|---|---|---|
| DES-003 inherited baseline | **Closed for calculation** | One $370.00 shared-machine term, counted once; it includes the inherited heads, controller, drivers, loom, and spares. | Delivered price and present availability are not established. |
| E-018 geometry/protocol | **Closed as interface input** | The 40 x 40 x 3 mm frame, 34 x 34 x 0.80 mm carrier, 3 mm apertures on 5.08 mm pitch, fiducials, four writer tabs, 2 mm reader relation, exact 4 x 25 readback, and reject rule are the controlled coupon contract. | CAD release and hardware acceptance remain open; dimensions are not measurements. |
| DRV8833, SC0915, and example harness | **Closed as catalogue observations** | Quantities and observed prices used in the arithmetic: 2 x $2.19, 1 x $4.59, 8 x $2.29. | Part-to-actuator wiring, PCB/carrier, thermal/current margin, final connector choice, availability, and delivered cost remain held. |
| Reusable media: 5 planes | **HOLD: quote + sample** | Quantity is fixed at four installed plus one service plane; the E-018 feature list is quoteable. | Material/thickness/process, burr/flatness, aperture and datum tolerance, cleaning compatibility, wear/media life, MOQ, lead time, packaging, freight, and delivered price. |
| Local clamp, datum, fiducials | **HOLD: quote + reseat sample** | One local-clamp set is the selected boundary assumption; full cassette/transport is not part of this BOM. | Drawing-level tolerance, preload, service access, loaded-neighbour isolation, and reseat repeatability. |
| Four writer actuators | **HOLD: exact-part quote/sample** | Quantity four and existing-driver path are the comparison basis; $9/$15/$30 each remains an allowance. | Exact envelope, usable stroke/stop, force, return or latch, life, repeatability, duty/thermal margin, and availability. The $3.34 Olimex observation is not a closed BOM selection. |
| DES-003 reader reuse | **HOLD: eight-head overlay** | Reuse is the preferred cost-reduction path and is not additive with the fallback rows. | XY/Z/optical isolation, cabling/pinout, timing, calibration, wrong/ambiguous/missing rejection, and physical coupon evidence. No $0 reader increment is accepted before these gates close. |
| QRE1113/ADC/carrier fallback | **Contingency only** | Conditional range arithmetic is closed: add $19.30/$29.30/$49.30 to the reuse low/base/high cases if reuse fails. | Optical geometry, carrier/PCB, threshold margin, compatibility, availability, and delivered cost. Rejected as an additive reuse cost. |
| Cleaning/replacement stock | **HOLD: allowance** | It is retained as a required service term at $10/$30/$75 low/base/high. | Cleaner, replacement event rate, media life, storage, and recurring delivered cost. |
| Cost bounds | **Closed as planning bounds** | Reuse: **$486.29 / $602.29 / $872.29** low/base/high. Fallback: **$505.59 / $631.59 / $921.59**. | These are not quotes, do not include freight/tax/labour/3D prints, and cannot authorize purchase or integration. |
| Delta 12 V actuator and MG90D servo alternatives | **REJECTED for bounded path** | Their apparent prices are retained only as source observations. | Delta adds a new supply/driver path; servo adds PWM power, linkage, backlash, and assembly. Reconsider only under a changed architecture boundary. |

### Quote/sample and coupon handoff gate

The next handoff is **quote-ready, not procurement-ready**. The smallest
package that can be issued by the DES-003 mechanical/controls owner, with Cost
& Sourcing normalizing the response, is:

1. One controlled E-018 drawing revision containing the plane labels, datum
   IDs, material/finish callouts, reader target, writer stop and parked
   clearance, inspection datums, and revision/date.
2. One quote request for five identical planes, one clamp/fiducial set, and
   four identical exact actuators, with separate setup/tooling, MOQ, lead
   time, packaging, freight, quote validity, and delivered-price lines.
3. One actuator data/sample request covering force at 1 mm engagement,
   usable travel and stop, return/power-loss state, duty/thermal limit, life,
   repeatability, and existing DRV8833 compatibility.
4. One eight-head DES-003 overlay record against the E-018 frame covering
   XY, Z/collision, optical isolation/contrast, cabling, timing, calibration,
   and deterministic fault rejection.
5. One coupon record for reseat residual, loaded-neighbour displacement,
   four-plane write/readback, and media wear/cleanability. This is the
   physical gate; analytical agreement alone does not close it.

Until items 1–4 exist, the handoff is only a prepared request. Until item 5
and returned supplier data exist, A-011 remains **HOLD for integration** and
the canonical bounds above remain unchanged. No RFQ has been sent, no sample
has been ordered, and no supplier commitment or physical-validation claim is
made by E-040.

## Local verification record

Run on 2026-10-07 from branch `cost/e022-e023-compatibility-closure`:

- `./repo check` — exit 1; reports the repository's existing warnings for
  oversized E-022/E-023 objects and completed E-031/E-032/E-033/E-034/E-035/
  E-037/E-038/E-039/E-041/E-042 workspaces requiring collapse. No warning names
  E-040.
- `git diff --check` — pass.
- Direct arithmetic recomputation — pass: reuse totals 486.29, 602.29,
  872.29; fallback totals 505.59, 631.59, 921.59; fallback deltas 19.30,
  29.30, 49.30.

## Bounded disposition and owner

**RFQ-ready with holds.** The plane/clamp request is ready to send against the
controlled E-018 drawing. The actuator request is ready for an exact-part
quote/sample but remains on force/stroke/life/fit hold. Reader reuse remains on
the eight-head geometry, optical, cabling, timing, and calibration hold. There
is no purchase commitment, no supplier commitment, and no physical-validation
claim.

Next external action owner: **DES-003 mechanical/controls owner**, with Cost &
Sourcing normalizing the returned prices and evidence. The owner must send the
plane/clamp RFQ and exact-actuator request, then return the signed quote/data
package and eight-head E-018 overlay record. Until those records exist, retain
E-022's canonical reuse/fallback ranges and do not integrate A-011.
