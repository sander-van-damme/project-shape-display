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

Arithmetic correction: the base calculation includes the $30 service
allowance and is therefore **$684.97**, not $654.97. The low calculation is
correct because it uses the $10 low service allowance. The corrected base
expression is `370 + 175 + 45 + 37.68 + 4.38 + 4.59 + 18.32 + 30`.

## Rejected reductions and decision

The $3.34 solenoid, servo, PET/polyimide film, removal of readback, and
serialized writing are rejected as current reductions: force/life/stock,
added electronics and backlash, reusable-life risk, lost fault observability,
or timing-boundary violation outweigh their apparent savings. A full cassette
transport remains outside this local-clamp boundary.

## Drawing-level route disposition

**304 SS plane and standard clamp route: GO to RFQ, HOLD for compatibility.**
RFQ five identical planes plus one set against one controlled drawing. State:
304 SS; 0.76 mm nominal (or quoted 0.80 mm), actual thickness; 40 x 40 x 3
mm frame; 34 x 34 x 0.80 mm carrier; 25 3.00 x 3.00 mm apertures on 5.08
mm pitch; Ø2.00 mm fiducials at (-15,-15)/(15,15) mm; 2 x 6 mm datum rail;
32 x 2.5 mm clamp land; labelled 1 x 0.8 mm tabs on 2 mm stack pitch;
deburred, flat, cleanable surface; two locating dowels; adjustable preload;
and loaded-neighbour clearance. Require material/thickness, aperture and
fiducial tolerances, flatness, edge condition, MOQ, lead time, packaging,
and price. Acceptance remains conditional on E-018 envelope/no-collision
inspection and ≤0.20 mm transformed-aperture/reseat residual; ±0.127 mm
catalogue cut tolerance is not acceptance evidence.

**One exact writer actuator route: HOLD pending exact-part quote/sample.**
Request one Olimex PUSH-PULL-SOLENOID-5V sample and four-unit quote using
Digi-Key 1188-PUSH-PULL-SOLENOID-5V-ND; if unavailable or lacking data, use
one exact Delta DSML-0224-12 quote/sample. Require exact part, availability,
force-versus-stroke, 5.00 mm stroke, voltage/resistance, cycle life, duty
cycle, mounting/termination tolerances, and return or latching behavior.
Accept only if the force reaches 1.00 mm tab engagement within the 4 x 1 x
0.8 mm tongue and 0.20 mm parked-clearance envelopes, with existing-driver
compatibility and an E-018 engagement/cycle sample plan. Catalogue prices
($3.34 Olimex, $9.42 Delta family) remain non-committed observations.

## Source trail and bounded disposition

The linked SendCutSend, Digi-Key Olimex, and Delta pages are the reproducible
public source trail; they provide no drawing-specific quote, force/life data,
or fit-checked exact actuator. No authenticated RFQ channel was available.
Disposition: planes/clamp **RFQ-go / physical-compatibility hold**; actuator
**quote/sample hold**; reader reuse **E-018 compatibility hold**. Do not order
parts or claim procurement commitment.

## LAB-131 reader/actuator compatibility closure

This is the drawing-level screen for reuse of the existing DES-003 interfaces
against the frozen E-018 coupon. The dispositions below are analytical and
inherit no physical validation. A **GO** means the E-018 contract or a stated
calculation is internally closed; it does not mean that DES-003 hardware has
passed. **HOLD** means the interface is plausible but the minimum evidence is
missing. **REJECT** is limited to the stated bounded path.

### Reader gates

| Gate | Controlled comparison and calculation | Disposition | Minimum missing evidence |
|---|---|---|---|
| XY target / field | E-018 centre target is a 3 x 3 mm window on the 5.08 mm field; acceptance is transformed aperture residual ≤0.20 mm after reseat. DES-003 beam centre and head/mount datum are not dimensioned in the available evidence. | **HOLD** | Dimensioned head-to-mount overlay in the E-018 frame datum, 2-D transform, tolerance stack, and residual table at centre/corner checks. |
| Z stack | E-018 upper-carrier reader lower-face relation is 2.00 mm; DES-003 flag design point is 1.80 mm. `2.00 - 1.80 = 0.20 mm` is a valid nominal difference but references different target surfaces, so it is not an interchangeable stack. | **HOLD** | Section drawing including carrier flatness, clamp/reseat, head mount, working-distance tolerance, and writer/tab collision clearance for every selected plane. |
| Plane identity / optical isolation | E-018 has four 0.80 mm carriers with three 1.20 mm gaps, so nominal carrier stack is `4 x 0.80 + 3 x 1.20 = 6.80 mm`; ports are on a 2.00 mm pitch and loaded N/E/S/W neighbours remain installed. DES-003’s 0.44 mm reflective-flag aperture/1.8 mm flag gap does not prove contrast or occlusion through this stack. | **HOLD** | Ray/occlusion overlay, emitter/detector field, material reflectance/ambient/saturation bounds, and per-plane calibration record. |
| Cabling / pinout | E-022 only carries inherited loom/controller infrastructure. No DES-003 connector identity, polarity/pinout, retention, cable OD/bend radius, exit path, strain relief, or head-carrier envelope is recorded against E-018. | **HOLD** | Connector and cable drawing plus electrical pinout and mechanical overlay; no uncosted adapter, harness, PCB, or strain relief may be assumed. |
| Timing | E-018 requires four-plane complete readback, fiducials, reject handling, and bounded retry. The inherited full-field DES-003 accounting leaves `30.00 - 20.18 = 9.82 s`, but that is a modelled planning margin, not a coupon timing result and does not include unspecified reader delay. | **HOLD** | Pulse/sample/settle schedule, eight-head sequencing, full 4 x 25 readback, fiducial/reject/retry trace, and worst-case total under 30 s. |
| Calibration / fault observability | **GO at contract level:** E-018 freezes calibration threshold `0.85`, requires exact 4 x 25 state comparison, and defines wrong/ambiguous/missing as reject. **Not GO for DES-003 implementation:** its calibration ID, saturation/ambient limits, missing-signal codes, and plane-identity trace are absent. | **HOLD** | Calibration record and software trace showing deterministic accept/reject and fault code for every missing, ambiguous, wrong-plane, and stale-read case. |

The E-018 geometry/protocol checks therefore receive **GO as frozen inputs**;
all six DES-003 reader reuse gates remain **HOLD**. No reader-head reuse cost
may be treated as closed until the listed overlay package exists. If a gate
fails, use the separately costed E-022 fallback reader boundary; do not add a
sensor, ADC, carrier, or harness implicitly to this experiment.

### Actuator and existing-driver gates

The frozen writer interface exposes a 4 x 1 x 0.8 mm tongue, 1.00 mm nominal
tab insertion, 2.00 mm plane pitch, and 0.20 mm parked clearance outside the
frame. Those are interface coordinates, not a required actuator stroke. The
candidate 5.00/5.08 mm strokes therefore cannot be accepted without a defined
hard stop and usable-travel stack.

| Gate | Olimex PUSH-PULL-SOLENOID-5V | Delta DSML-0224-12 family observation | Disposition |
|---|---|---|---|
| Exact envelope, stroke, tab engagement, parked clearance | Exact body/mount/plunger drawing, usable travel, stop, return, and tolerance absent; catalogue 5.00 mm stroke is not proof of 1.00 mm engagement or 0.20 mm park. | Exact part/envelope absent; 5.08 mm family stroke is not a motion requirement. | **HOLD** both; require 1:1 E-018 tab/stop overlay and worst-case travel. |
| Force, return/latch, life, repeatability | No force curve, return behaviour, cycle life, or position tolerance. | No exact-part force/latch/life/repeatability evidence. | **HOLD** both; require force-vs-stroke at contact, return/power-loss state, duty/life, and repeatability evidence. |
| Existing DRV8833 path | `5 V / 6 ohm = 0.833 A` nominal coil-current arithmetic is only a candidate screen. Current limit, inrush, flyback, duty thermal margin, and fault behavior are not closed. | The observed 12 V variant crosses the existing DRV8833 low-voltage supply boundary and would require a new driver/power path. | Olimex **HOLD**; Delta **REJECT for bounded existing-driver/no-added-parts path**. |
| Servo alternative | MG90D adds PWM, servo power, horn/linkage, backlash and stall-duty interfaces. | — | **REJECT for this reuse screen**; it is not a drop-in existing-driver actuator. |

The actuator interface consequently has no GO selection. The cheapest next
falsifier is a drawing-only 1:1 tab/stop and driver-current/thermal screen for
one exact 5 V candidate; force, return, life, and hardware fit remain separate
future evidence. No actuator, driver, power rail, return spring, or carrier is
added to the E-023 boundary by this result.

### Final LAB-131 disposition

**REJECT compatibility acceptance; HOLD the reuse path.** E-018’s frozen
envelope, interface coordinates, complete-readback schema, and reject rule are
analytically GO as inputs. Existing DES-003 reader heads are not reusable yet
because XY, Z, optical isolation, cabling, timing, calibration, and fault
implementation are not drawing-closed. The Olimex actuator is a conditional
next-screen candidate; Delta and the servo are rejected for the bounded
existing-driver path. The next owner is the DES-003 mechanical/controls owner,
with Cost & Sourcing support, to supply the overlay and exact-actuator evidence
listed above. This screen authorizes no procurement, CAD change, or physical
validation claim.

## Next falsification/procurement action and owner

Next owner: **DES-003 mechanical/controls owner**, with Cost & Sourcing
support. Send the controlled plane/clamp RFQ and exact-actuator sample/quote
request above; then record eight reader-head dimensions, optical stack,
pinout, timing, and calibration margin against E-018. This is the next
falsifier; do not order parts, redesign CAD, or claim compatibility.

## E-023-OVL-001: LAB-133 drawing-level overlay closure

Date basis: 2026-10-07. Analytical overlay disposition only: not CAD
release, procurement, or physical validation. E-018 is the frozen interface
authority; DES-003 dimensions are reused only where explicitly recorded.

### Reader-head gates against E-018

The eight-head reuse case remains **HOLD**. The E-018 frame, two Ø2.00 mm
fiducials, and 2.00 x 6.00 mm north rail establish the coordinate frame; a
reader head is not a datum. Each head needs a datum, optical-axis, connector,
and tolerance overlay.

| Gate | Drawing-level acceptance condition | Disposition and evidence class | Cheapest next falsifier |
|---|---|---|---|
| XY | Transform optical axis into E-018 frame; 3.00 x 3.00 mm windows at 5.08 mm pitch; transformed residual after reseat ≤0.20 mm. Check centre, four field corners, and both fiducials. | **HOLD; calculated requirement:** DES-003 head/mount XY is absent. | One dimensioned head/mount overlay with transform and residual table. |
| Z / collision | E-018 reader lower face 2.00 mm above upper 0.80 mm carrier. Include flatness, clamp/reseat, mount, all 4 x 1 x 0.80 mm tongues, and 0.20 mm parked clearance. DES-003 1.80 mm flag gap is a different target. | **HOLD; calculated requirement:** `2.00 - 1.80 = 0.20 mm` is not a tolerance closure. | One section overlay with worst-case Z and engaged/parked collision planes. |
| Optical field / plane identity | Show emitter/detector field at the E-018 target, mask surface/reflectance, adjacent 2.00 mm port planes, and loaded N/E/S/W neighbours; adjacent classification rejects. | **HOLD; inferred risk:** DES-003 0.44 mm aperture, 1.405 mm spot, and 7.72× modelled return ratio were for its flag geometry. | One ray/occlusion section using actual head and selected mask optical assumptions. |
| Cabling | Connector, pinout, polarity, retention, cable OD/bend radius, exit, and strain relief fit without adapter, new PCB, or unpriced harness. | **HOLD; unresolved interface:** E-022 carries only inherited loom/controller allowance. | One connector/loom overlay and pin-to-controller table. |
| Timing | Eight heads in parallel; complete 4 × 25 readback, fiducials, settle, reject, bounded retry ≤30.00 s. DES-003 planning margin is `30.00 - 20.18 = 9.82 s`, excluding unspecified reader delay. | **HOLD; calculated planning margin:** no E-018-specific timing trace. | Timestamped worst-case schedule including 100-cell compare and one retry. |
| Calibration / faults | Freeze calibration ID and threshold 0.85; exact 4 × 25 comparison; wrong, ambiguous, missing, stale, and wrong-plane results reject with fault code. | **GO as E-018 contract input; HOLD for DES-003 implementation.** | Calibration record plus deterministic trace for each fault class. |

If a reader gate fails, use E-022's explicit QRE1113/ADC/carrier fallback;
those rows are not added to a reuse case.

### Exact 5 V actuator and tab-stop overlay

The one exact candidate is **Olimex PUSH-PULL-SOLENOID-5V, Digi-Key
1188-PUSH-PULL-SOLENOID-5V-ND**. Catalogue observations are 5.00 mm nominal
stroke, 5–6 V, and 6 Ω. Body/mount/plunger envelope, usable travel, return,
life, and positional tolerance drawings are absent; exact identity is not
fit or performance evidence.

The E-018 overlay datum is tab x = -10.16 mm; four ports have 2.00 mm centre
pitch; each tongue envelope is 4.00 x 1.00 x 0.80 mm; nominal tab insertion is
1.00 mm; parked nearest face is 0.20 mm outside the 40 mm frame. Add rigid
engaged and parked stops. The drawing checks are:

```
usable travel at tab = actuator travel - stop/link losses
engaged travel >= 1.00 mm + worst-case tab/stop clearance
parked position >= 0.20 mm outside frame + worst-case tolerance
neighbour/adjacent-plane clearance > 0 in both states
```

Thus the 5.00 mm stroke is a **calculated candidate input**, not proof of
1.00 mm engagement or parked position. Missing body/mount overlay leaves the
candidate **HOLD**.

Electrical screen from the voltage/resistance observation:

```
I_nominal = 5 V / 6 ohm = 0.833 A per coil
P_nominal = 5 V x 0.833 A = 4.167 W per coil
four-coil simultaneous upper arithmetic = 3.333 A, 16.667 W
```

These are steady-state Ohmic calculations, not measured inrush or thermal
results. DRV8833 current limit, flyback, duty, PCB copper, and junction
temperature are not evidenced; no duty/thermal model is present. The
driver/current/thermal gate is **HOLD**, with no new driver, power rail, or
thermal allowance silently added.

Return and life are **HOLD**: no spring/power-loss state, force-versus-stroke,
cycle-life rating, repeatability, or duty limit is recorded. Do not assume a
return spring, latch, or replacement actuator. Required evidence is the exact
mechanical drawing, force at 1.00 mm engagement, return/park behaviour,
repeatability, duty/temperature screen, and life evidence against E-018's
1,000-cycle handoff. Physical testing remains future work.

### LAB-133 disposition and BOM consequence

| Item / gate | Disposition | Basis |
|---|---|---|
| E-018 geometry/protocol/reject rule | **GO as frozen input** | E-018 checker and schema define the contract; not hardware validation. |
| DES-003 reader reuse | **HOLD** | XY, Z/collision, optical isolation, cabling, timing, and implementation calibration evidence missing. |
| Olimex exact 5 V actuator | **HOLD** | Identity and nominal electrical arithmetic exist; envelope/stop, force, return, life, repeatability, and thermal evidence do not. |
| Delta DSML-0224-12 family | **REJECT for bounded path** | Observed 12 V route needs new supply/driver and lacks exact-part overlay. |
| MG90D servo | **REJECT for bounded path** | Adds PWM, servo power, horn/linkage, backlash, and stall-duty interfaces; not DRV8833 drop-in. |
| Complete DES-003/E-018 compatibility acceptance | **REJECT for now; retain HOLDs** | No unsupported reuse or unpriced adapter is closed. |

Retain E-022's conditional reuse range **$486.29 / $602.29 / $872.29** only
if readers and the four-actuator boundary close. Keep fallback-reader range
**$505.59 / $631.59 / $921.59** if reader reuse fails. Do not add QRE1113,
MCP3008, or reader-carrier rows to reuse, and do not count the inherited
DES-003 $370 reader/controller/driver baseline twice. The `$13.36 = 4 x
$3.34` Olimex arithmetic is a sourced catalogue observation only, not a viable
BOM line until HOLD evidence closes. No adapter, return spring, replacement
stock, new driver, or power rail is priced.

Owner and handoff: **DES-003 mechanical/controls owner**, with Cost & Sourcing
support. Cheapest reader falsifier: one-head dimensioned E-018
XY/Z/optical/cable/timing/calibration overlay. Cheapest actuator falsifier:
one exact Olimex 1:1 tab/stop drawing plus DRV8833 current/duty/thermal
calculation. These actions may promote or reject HOLDs; they do not authorize
procurement or CAD release.
