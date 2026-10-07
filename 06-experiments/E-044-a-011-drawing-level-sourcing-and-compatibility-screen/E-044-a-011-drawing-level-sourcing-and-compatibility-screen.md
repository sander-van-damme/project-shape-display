---
status: active
builds-on: [E-022, E-023, E-040, E-018, DES-003, ADR-005, ADR-006]
---

# E-044: A-011 drawing-level sourcing and compatibility screen

Date basis: 2026-10-07. Currency: USD. This is a quote-ready purchased-component screen for one A-011 reference machine. It is not a supplier quote, procurement authorization, CAD release, or physical validation. Exclude 3D-printed parts, print material/time/failures, labour, freight, tax, payment fees, and validation fixtures, consistent with ADR-005.

## Controlled boundary and source classes

The controlled interface is E-018: five reusable planes (four installed plus one service plane), a 40 x 40 x 3 mm frame, 34 x 34 x 0.80 mm plane carriers, 25 square 3.00 mm apertures on 5.08 mm pitch, two Ø2.00 mm fiducials at diagonal ±15 mm offsets, four labelled 1 x 0.80 mm writer tabs on 2.00 mm pitch, local positive datum/clamp, four writer ports, and a frame-fixed reader target nominally 2.00 mm above the upper carrier. These are CAD/interface requirements, not measurements.

`Sourced` means a dated public catalogue or capability observation already recorded in E-022/E-023/E-040; it is not a quote or compatibility evidence. `Estimate` is a bounded planning allowance. `Assumption` is an inherited design or arithmetic premise. No exact supplier quote or physical measurement was available for this screen.

## Quote-ready purchased BOM

| Line | Qty | Unit / extended USD | Basis and source identity | Minimum evidence before pass |
|---|---:|---:|---|---|
| Reusable media planes | 5 | 4 / 12 / 30 each; 20 / 60 / 150 low/base/high | Estimate. Preferred route is deburred 304 SS; SendCutSend public capability observation: 0.76 mm nearest listed thickness, ±0.005 in cut tolerance, 2–4 business-day production ([source](https://sendcutsend.com/materials/stainless-steel/)); not a fit quote | Exact material/temper/finish and actual thickness; aperture, fiducial, datum, tab and flatness tolerances; burr/kerf or etch taper; cleanability and wear/life; MOQ, lead time, packaging and delivered price; E-018 overlay and ≤0.20 mm transformed/reseat residual |
| Local clamp, hard datum, latch | 1 set | 15 / 35 / 80 | Estimate; standard dowels + deburred datum plate + adjustable latch preferred over cassette transport | Dimensioned part/process, preload, stop and service access; tolerance stack, flatness, loaded-neighbour clearance, and reseat record |
| Fiducial/datum pins or shim stock | 1 set | 8 / 20 / 50 | Estimate; separate term prevents registration hardware omission | Exact pin/shim size, material, location and tolerance against E-018; no printed substitute assumed |
| Four writer actuators | 4 | 9 / 15 / 30 each; 36 / 60 / 120 | Base term is DES-003 $9/head anchor, not a selected part. Sourced candidates: Olimex PUSH-PULL-SOLENOID-5V, Digi-Key 1188-PUSH-PULL-SOLENOID-5V-ND, $3.34 each, observed out of stock with estimated 2026-10-15 availability; Delta DSML family $9.42 each, 12 V family observation; alternatives, not additive ([Olimex source](https://www.digikey.com/en/products/detail/olimex-ltd/PUSH-PULL-SOLENOID-5V/23330937)) | Exact part drawing, envelope/mount/termination, usable travel and hard-stop stack, force at 1.00 mm tab engagement, return/latch state, repeatability, duty/thermal/current, cycle life and availability; DRV8833 compatibility. Olimex is HOLD; Delta is REJECT for bounded existing-driver/no-added-parts path |
| DRV8833CRTER driver IC | 2 | 2.19 each; 4.38 | Sourced Digi-Key 296-40079-1-ND, listing observed 2,930 in stock ([source](https://www.digikey.com/en/products/detail/texas-instruments/DRV8833CRTER/5039360)) | Four-channel wiring, coil current/inrush, flyback, PCB thermal margin and fault behavior; IC price does not include carrier |
| Raspberry Pi Pico SC0915 controller | 1 | 4.59 | Sourced Digi-Key 2648-SC0915CT-ND, listing observed 43,224 in stock ([source](https://www.digikey.com/en/products/detail/raspberry-pi/SC0915/2648-SC0915CT-ND/13684020)) | I/O map, pulse/settle schedule, complete readback and bounded retry timing; carrier and firmware remain assumptions |
| Example channel/media harness | 8 | 2.29 each; 18.32 | Sourced example Pololu 5615 / Digi-Key 2183-5615-ND, listing observed 118 in stock ([source](https://www.pololu.com/product/5615)); final loom is not locked | Connector/pinout, polarity, retention, cable OD/bend radius, strain relief and no-adapter overlay |
| Cleaning/replacement stock | 1 allowance | 10 / 30 / 75 | Estimate for cleaner/wipes plus one damaged/rejected plane event | Selected cleaner, storage, replenishment price, media life and replacement-event basis |

The inherited DES-003 shared-machine baseline is **$370.00**, counted once. It contains the existing gantry, eight writer/reader head positions, controller, drivers, power, loom, switches, fasteners and spares. It is not an A-011-only BOM. The four actuator row above is the A-011 boundary term; inherited reader heads are treated separately below to avoid counting them twice.

## Reader reuse and fallback accounting

Reuse of the eight DES-003 reader heads is **$0 incremental only if** all reuse gates pass. Required evidence is one dimensioned overlay package for all heads covering:

| Gate | Minimum drawing/interface evidence | Disposition |
|---|---|---|
| XY target and reseat | Head/mount datum transform to E-018, centre/corner residual table, ≤0.20 mm transformed aperture residual | HOLD |
| Z stack and collision | Section drawing for 2.00 mm reader relation, carrier flatness, clamp/reseat, writer and loaded-neighbour clearance | HOLD |
| Optical field and plane identity | Emitter/detector field, mask reflectance/contrast, adjacent 2 mm planes and loaded-neighbour occlusion | HOLD |
| Cabling | Connector, pinout, polarity, retention, bend radius, exit and strain relief without unpriced adapter/PCB/loom | HOLD |
| Timing | Timestamped four-plane complete 4 x 25 readback, fiducials, retry and worst case ≤30 s | HOLD |
| Calibration/faults | Calibration ID and threshold 0.85; wrong, ambiguous, missing, stale and wrong-plane results reject deterministically | HOLD |

If any reuse gate fails, add only the separate fallback allowance: eight QRE1113 sensors at $0.80 each ($6.40 sourced observation), one MCP3008-I/SL at $2.90 (sourced observation), and one reader optics/carrier/PCB allowance of $10 / $20 / $40. This fallback is not added to the reuse case. The QRE1113 1 mm nominal sensing distance and MCP3008 interface do not prove optical compatibility. The fallback remains HOLD pending its own optical, carrier, cabling and calibration drawing.

## Reproducible cost sensitivity

The canonical planning bounds are inherited from E-022 and remain the most honest range because the lower actuator observation and stainless/clamp bands are not fit-accepted selections:

| Scenario | Calculation | Purchased total |
|---|---|---:|
| Reader reuse, low/base/high | `370 + (20/60/150) + (15/35/80) + (8/20/50) + (36/60/120) + 4.38 + 4.59 + 18.32 + (10/30/75)` | **$486.29 / $602.29 / $872.29** |
| Reader fallback, low/base/high | reuse total + `(6.40 + 2.90 + 10/20/40)` | **$505.59 / $631.59 / $921.59** |

Fallback deltas are **$19.30 / $29.30 / $49.30**, not additional costs when reuse passes. The observed reuse electronics/harness subset is `2 x 2.19 + 1 x 4.59 + 8 x 2.29 = $27.29`; QRE1113 and MCP3008 are excluded from reuse. The earlier $36.59 subset includes fallback QRE1113 and must not be presented as a reuse BOM. All totals are planning calculations, not delivered prices.

Highest sensitivity is the unresolved media/clamp/actuator/service span ($366 from reuse low to high), followed by reader compatibility: failing reuse adds $19.30–$49.30 but also creates new optical/carrier assembly and calibration burden. Catalogue unit-price optimism is less valuable than removing purchased terms.

## Reduction and candidate disposition

| Candidate/reduction | Cost and engineering effect | Disposition |
|---|---|---|
| Reuse DES-003 readers | Removes fallback sensors, ADC and carrier; lowers unique parts and assembly, but depends on optical margin, reseat, cabling, timing and calibration evidence | Preferred reduction; HOLD until overlay |
| Local clamp instead of cassette transport | Removes transport parts and simplifies assembly; increases datum, debris and service sensitivity | Retained boundary assumption; HOLD for tolerance/reseat evidence |
| 304 SS rigid plane | More durable and maintainable than film; public cut tolerance is not enough for the 0.20 mm gate and 0.76 vs 0.80 mm thickness needs closure | RFQ-go; HOLD for drawing/sample |
| Olimex $3.34 actuator | Apparent saving versus four $9 anchors, but force/life/return/fit/availability and 0.833 A per-coil electrical burden are unresolved | HOLD; do not use as cost reduction |
| Delta 12 V actuator | $37.68/4 observation, but crosses existing 5 V driver boundary and lacks exact-part fit/life data | REJECT for bounded path |
| PET/polyimide or photo-etched thin media | Potentially cheaper/lighter; creep, buckle, tear, cleaning and writer-contact life add failure/assembly risk | Reject as first reusable baseline; experiment only |
| Remove readback or serialize writing | Apparent electronics/timing saving, but loses fault observability or violates E-017 timing boundary | REJECT |

## Gate conclusion and required next evidence

**A-011 remains HOLD for integration and procurement.** The screen is RFQ-ready, not procurement-ready. Minimum next package is: (1) released E-018-controlled plane/clamp drawing with datums, material/finish, stops, inspection points and revision; (2) supplier response for five identical planes, one clamp/fiducial set and four identical actuators with setup, MOQ, lead time, packaging, freight and delivered price separated; (3) exact actuator force/stroke/return/life/current data; and (4) eight-head DES-003 reader overlay and timing/calibration record. Physical coupon evidence is still required after those analytical records.

No external quote, purchase, CAD modification, or hardware validation was performed. Analytical agreement with E-018 does not prove performance.
