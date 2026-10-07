---
status: active
builds-on: [E-017, E-018, DES-003]
---

# E-022: complete mask-generator boundary BOM sourcing screen

Date basis: 2026-10-07. Currency: USD. This is a purchased-component
calculation for one 80 x 80 reference machine and its minimum arbitrary-map
mask-generator boundary. It is not a supplier quote, manufacturing release,
or hardware validation. 3D-printed parts, print material/time, labour,
freight, tax, payment fees, and validation fixtures are excluded.

## Boundary and inherited term

The complete boundary is the surviving E-017/ADR-006 architecture: reusable
four-plane media, positive registration, local clamp or transport, four
independent writer channels, per-cell verification/readback, bounded retry,
and replacement/cleaning service stock. This screen chooses local clamping;
a full cassette transport is not silently assumed or costed.

DES-003 contributes a separate **$370.00 purchased-component baseline**. It
already contains the shared gantry, eight writer/reader head positions,
controller, drivers, power, loom, switches, fasteners, and spares. The
$370.00 is retained as a separate term below; it is not a mask-generator BOM
and must not be used as a complete-boundary cost by itself.

## BOM

The low/base/high columns are bounded engineering allowances unless marked
`sourced`. A sourced price is a catalogue observation, not a guaranteed
future price; availability was captured from the linked listing and can
change. Quantities are for one machine, with five plane sheets meaning four
installed plus one service/replacement set.

| Boundary item | Quantity | Low USD | Base USD | High USD | Price basis and source | Completeness / risk |
|---|---:|---:|---:|---:|---|---|
| Reusable four-plane media, four installed + one service plane | 5 planes | 20 | 60 | 150 | Allowance: $4 / $12 / $30 per plane; no fit-selected medium or quote | Highest unresolved term: thickness, wear, aperture process, cleanability, and replacement format |
| Local clamp, hard datum, latch, and two-fiducial hardware | 1 set | 15 | 35 | 80 | Allowance; no drawing-level purchased set | Must preserve reseat registration and loaded-neighbour isolation |
| Precision datum/fiducial pins or shim stock | 1 set | 8 | 20 | 50 | Allowance; catalogue family exists but fit/tolerance is unresolved | Separate from clamp so registration hardware is not omitted |
| Four independent writer-channel actuators | 4 | 36 | 60 | 120 | Allowance derived from DES-003 $9/head anchor; $9 / $15 / $30 each, no selected part number | Force, stroke, cycle life, and channel parking remain open |
| Writer-channel driver ICs, TI DRV8833CRTER | 2 | 4.38 | 4.38 | 4.38 | **Sourced:** Digi-Key 296-40079-1-ND, $2.19 each at quantity 1; listing showed 2,930 in stock; [catalogue](https://www.digikey.com/en/products/detail/texas-instruments/DRV8833CRTER/5039360) | Two ICs provide four half-bridge channels only if the selected actuator wiring is compatible; PCB/carrier is not included here |
| Mask-generator controller, Raspberry Pi Pico SC0915 | 1 | 4.59 | 4.59 | 4.59 | **Sourced:** Digi-Key 2648-SC0915CT-ND, $4.59; listing showed 43,224 in stock; [catalogue](https://www.digikey.com/en/products/detail/raspberry-pi/SC0915/2648-SC0915CT-ND/13684020) | I/O timing and firmware are assumptions; a production carrier is not included |
| Verification ADC, Microchip MCP3008-I/SL | 1 | 2.90 | 2.90 | 2.90 | **Sourced:** Digi-Key 150-MCP3008-I/SL-ND, $2.90; listing showed 5,320 in stock; [catalogue](https://www.digikey.com/en/products/detail/microchip-technology/MCP3008-I-SL/319423) | Interface part only; does not prove reader discrimination |
| Verification/readback sensors, onsemi QRE1113 (fallback stack) | 8 | 6.40 | 6.40 | 6.40 | **Sourced:** Digi-Key QRE1113-ND, $0.80 each; listing showed 12,547 in stock; [catalogue](https://www.digikey.com/en/products/detail/onsemi/QRE1113/2175990) | **Alternative, not additive in reuse case:** 1 mm sensing distance may not fit the mask optical stack |
| Reader optics/carrier/PCB for fallback stack | 1 set | 10 | 20 | 40 | Allowance; no board, emitter geometry, or carrier drawing selected | Only needed if DES-003 reader heads fail compatibility check |
| Channel/media interface harness, Pololu 5615 3-pin cable | 8 | 18.32 | 18.32 | 18.32 | **Sourced:** Digi-Key 2183-5615-ND / Pololu item 5615, $2.29 each; listing showed 118 in stock; [supplier](https://www.pololu.com/product/5615) | Example connector family; final loom may use a cheaper crimped harness after interface freeze |
| Cleaning and replacement service stock | 1 allowance | 10 | 30 | 75 | Allowance for wipes/cleaning agent plus one damaged/rejected media event | Required service term; media-life test and consumable are unresolved |

The DES-003 reader heads are an inherited verification/readback path at
$0 incremental cost **only if** their optical stack, cabling, and timing pass
a drawing-level compatibility check. The QRE1113/ADC/carrier rows are the
explicit fallback replacement stack and must not be double-counted with a
compatible inherited reader.

## Arithmetic and sensitivity

The sourced incremental subset is:

`2 x 2.19 + 1 x 4.59 + 1 x 2.90 + 8 x 0.80 + 8 x 2.29 = $36.59`.

For the reuse-verified case, omit the three fallback rows (QRE1113, ADC,
and reader carrier) from the incremental total because the $370 baseline
already carries the reader heads and controller infrastructure:

| Case | Calculation | Total purchased cost |
|---|---|---:|
| Reuse / low | `370 + 20 + 15 + 8 + 36 + 4.38 + 4.59 + 18.32 + 10` | **$486.29** |
| Reuse / base | `370 + 60 + 35 + 20 + 60 + 4.38 + 4.59 + 18.32 + 30` | **$602.29** |
| Reuse / high | `370 + 150 + 80 + 50 + 120 + 4.38 + 4.59 + 18.32 + 75` | **$872.29** |
| Fallback reader / low | reuse low + `6.40 + 2.90 + 10` | **$505.59** |
| Fallback reader / base | reuse base + `6.40 + 2.90 + 20` | **$631.59** |
| Fallback reader / high | reuse high + `6.40 + 2.90 + 40` | **$921.59** |

The range is therefore **$486–$872** if the inherited readback heads are
compatible, or **$506–$922** with the explicitly costed fallback sensor
stack. These are not delivered prices. The earlier ADR-005 preliminary
screen's $505.59 / $631.59 / $921.99 line should be corrected: its high
case rounded the controller inconsistently and did not clearly identify the
reader-stack double-counting risk. This E-022 calculation uses the observed
$4.59 controller price and gives the corrected high value of $921.59.

## Boundary comparison and disposition

The two credible purchased-component paths are alternatives for the reader
subsystem; both retain the complete arbitrary-map boundary, four parallel
writer channels, local registration, verification, and service stock.

| Path | Purchased range | Cost/sourcing advantage | Compatibility and engineering risk | Disposition |
|---|---:|---|---|---|
| A-011 boundary with DES-003 reader reuse | **$486–$872** | Removes a new reader stack and its carrier; lowest unique-part count and assembly burden | Eight inherited heads must meet the E-018 optical, Z-stack, cabling, calibration, and timing gates; $0 reader increment is conditional | **Preferred path to falsify** |
| A-011 boundary with QRE1113/ADC/carrier fallback | **$506–$922** | Public catalogue observations provide a concrete replacement path; adds only $19.30 / $29.30 / $49.30 to low/base/high reuse cases | 1 mm sensor geometry, carrier/PCB, optical contrast, and threshold margin are unresolved; new parts add calibration and service burden | **Credible contingency, not a saving** |

The cost screen therefore **proceeds to drawing-level sourcing and
compatibility falsification**, but does not authorize procurement or claim a
production-ready low-cost implementation. The current boundary is credible
as a purchased-component path only if the inherited-reader overlay passes and
the media, clamp, and actuator allowances close to quotes. If reader reuse
fails, retain the fallback range until its optical stack is demonstrated;
do not replace it with optimistic bulk pricing.

| Unresolved question | Next owner | Smallest closing action |
|---|---|---|
| Can DES-003 readers resolve the four-plane E-018 stack after reseat? | Reader/verification owner | Drawing overlay plus calibration/threshold and timing review for all eight heads |
| What medium, thickness, aperture process, life, and delivered price meet the five-plane envelope? | Cost & Sourcing | RFQ for five cut/debur planes including tolerance, MOQ, lead time, packaging, freight, and replacement price |
| Can four writer actuators meet force, stroke, return, life, and driver limits? | Mechanical/controls owner | Exact-part data package or sample-level force/return/stop screen, with DRV8833 current and thermal check |
| Does the local clamp preserve datum repeatability and loaded-neighbour isolation? | Mechanical owner | Dimensioned clamp/fiducial RFQ and reseat tolerance stack against the E-018 gate |

## Reduction screen

| Proposal | Cost effect | Engineering effect / disposition |
|---|---|---|
| Reuse DES-003 reader heads after optical/timing compatibility check | Removes $19.30 / $29.30 / $49.30 fallback allowance | Reduces unique parts and assembly; preserves maintainability only if margin and calibration remain adequate. **Preferred first reduction; coupon check required.** |
| Use one controller and two shared driver ICs | Keeps sourced electronics at $11.87 before harness | Lowers unique part count; requires four-channel timing, current, thermal, and fault isolation checks. Already used in this BOM. |
| Local clamp instead of full transport/cassette | Avoids an unbounded transport term | Simplifies assembly and lowers moving-part count; increases registration and debris sensitivity. **Chosen boundary assumption, not validated.** |
| Replace reusable planes with disposable sheets | May lower initial media cost | Adds recurring cost, waste, feed/registration faults, and service burden; rejected for complete reusable boundary. |
| Remove per-cell verification or serialize writing | Apparent electronics/mechanism saving | Removes fault observability or violates the E-017 30 s analytical bound; rejected. |
| Assume bulk actuator/media pricing before a drawing-level quote | Could reduce allowance | Not credible until force/stroke, tolerances, MOQ, life, lead time, and delivered price are quoted; do not use as savings. |

## Conclusion and next falsification action

ADR-006's complete-boundary cost claim needs revision from an unpriced
`370 + Ctile + Cclamp + C4write + Cservice` form to the explicit conditional
range above. ADR-005 should retain $370 as the shared-machine baseline, but
should distinguish the reuse-verified range from the fallback-reader range
and correct its high-case arithmetic. No architecture or procurement
approval follows from this screen.

The next falsification/procurement action is one drawing-level request for
five cut/debur media planes, one clamp/fiducial set, and four writer
actuators, plus a compatibility measurement of the eight DES-003 reader
heads against the E-018 coupon optical stack. Request material, thickness,
aperture process, force/stroke, life, tolerances, MOQ, lead time, packaging,
freight, and delivered price. This should collapse the $366 allowance span
between the reuse low/high cases before any CAD or purchase decision.

Source observations are linked above; all other prices are explicitly
allowances or inherited calculations. Analytical acceptance in E-017/E-018
does not establish hardware performance.

## LAB-134 cost and sourcing refresh

Date basis: 2026-10-07. E-043 independently rechecked the E-022 boundary,
timing arithmetic, and cost arithmetic. No supplier quote, procurement record,
physical measurement, actuator force/life result, or reader-performance result
was added. This refresh therefore preserves E-022 as the canonical purchased-
component baseline and does not promote A-011 to integration or procurement.

### Canonical BOM and reproducible floor

The inherited DES-003 shared-machine term remains **$370.00**. It is not a
mask-generator-only cost and is counted once. The incremental boundary BOM is
the five-plane reusable medium, local clamp/datum/fiducials, four writer
actuators, two DRV8833 ICs, one SC0915 controller, eight example interface
cables, and cleaning/replacement stock. The fallback reader rows are an
alternative path, not additive to inherited-reader reuse.

| Scenario | Reproducible calculation | Purchased total | Price classification |
|---|---|---:|---|
| Inherited-reader reuse / low | `370 + 20 + 15 + 8 + 36 + 4.38 + 4.59 + 18.32 + 10` | **$486.29** | Allowances plus catalogue observations; reuse gates open |
| Inherited-reader reuse / base | `370 + 60 + 35 + 20 + 60 + 4.38 + 4.59 + 18.32 + 30` | **$602.29** | Same; canonical planning midpoint, not a quote |
| Inherited-reader reuse / high | `370 + 150 + 80 + 50 + 120 + 4.38 + 4.59 + 18.32 + 75` | **$872.29** | Same; unresolved media/actuator/clamp span remains |
| Fallback reader / low | `486.29 + 6.40 + 2.90 + 10` | **$505.59** | Alternative QRE1113/ADC/carrier path |
| Fallback reader / base | `602.29 + 6.40 + 2.90 + 20` | **$631.59** | Alternative path; no reader reuse assumed |
| Fallback reader / high | `872.29 + 6.40 + 2.90 + 40` | **$921.59** | Alternative path; corrected controller arithmetic |

The observed catalogue subset is **$36.59** (`2 x $2.19` DRV8833,
`1 x $4.59` SC0915, `1 x $2.90` MCP3008, `8 x $0.80` QRE1113, and
`8 x $2.29` example cables). The QRE1113 and MCP3008 values are excluded from
the reuse totals; they are only fallback-reader terms. Digi-Key/Pololu listing
prices and captured stock figures in this document are catalogue observations,
not live availability guarantees, delivered prices, or compatibility evidence.
All media, clamp, actuator, reader-carrier, and service values remain
allowances. Freight, tax, labour, payment fees, and 3D-printed parts remain
excluded.

### LAB-134 disposition

**Product boundary: GO analytically / HOLD for integration.** A reusable,
rewritable four-plane medium with parallel writing, registration, verification,
bounded retry, and service stock remains the minimum complete arbitrary-map
boundary. Prepared-mask, cassette-only, buffered, and serial alternatives are
REJECTED as substitutes: they either cannot create an unseen map or violate
the inherited timing boundary.

**Purchased BOM: HOLD; RFQ-ready, not procurement-ready.** The reuse range is
the preferred cost path only if all eight reader overlays/gates and the exact
four-actuator interface close. The fallback range is a contingency, not a
saving, and must not be added to the reuse case. No cost pass is granted from
catalogue observations or optimistic bulk pricing.

The preferred reductions remain removal/simplification of purchased terms:
reuse the inherited reader heads after the E-018 overlay and retain local
clamping rather than adding cassette transport. These reduce unique parts and
assembly, but increase dependence on optical margin, datum repeatability,
debris control, and service access. Removing readback or serializing the
writer would reduce apparent cost while sacrificing fault observability or
breaking timing, so both remain rejected. Thin etched/polymer media and the
$3.34 Olimex actuator observation remain experiment/quote candidates only;
their wear, fit, force, return, life, stop, thermal, and availability evidence
is not closed.

Next owner: **DES-003 mechanical/controls owner**, with Cost & Sourcing.
Return one controlled RFQ/data package for five media planes, one
clamp/fiducial set, and four exact actuators, plus the eight-head E-018
overlay/timing/calibration record. Until that package exists, retain the
canonical ranges above, keep A-011 as candidate/HOLD, and do not purchase or
integrate.
