---
status: active
builds-on: [DES-002, DES-003, DES-004, A-010]
---

# Purchased-component cost comparison references

Date basis: 2026-10-07. Currency: USD. Scope is one current tabletop unit;
3D-printed parts, print material/time/failures, and assembly labor are
excluded. Shipping, tax, and live availability are excluded unless explicitly
stated. `sourced-class`, `allowance`, and `estimate` in the source BOMs are
not supplier quotes.

## Decision

Retain the following historical arithmetic as comparison inputs under ADR-009, not an active architecture ranking. No design is selected here. DES-002 omits a complete arbitrary-map generator/readback; DES-003 is binary-only; DES-004's five-stop mechanism and axle sourcing are unqualified; A-010 is retired. Recheck complete quantities, implementation costs and sourcing for any new candidate.

## Reproducible comparison

The comparable source machines are 80x80 cells, i.e. 6,400 cells or 256
5x5-cell modules. The 5x5-module values below are arithmetic allocation of
the whole-machine purchase total, not a claim that each module can be built
independently. A 20x20-cell tile allocation is also shown as total/16; it is
not a standalone 20x20-board BOM because gantry, power, controller, and
reader/writer costs are shared.

| Candidate/scenario | Purchased total | 5x5 module allocation (total/256) | 20x20-cell tile allocation (total/16) | Evidence boundary |
|---|---:|---:|---:|---|
| DES-002 low-cost mask | $226.77 | $0.886 | $14.173 | Source BOM estimate; delivered illustration $263.05 uses x1.16, not a quote |
| DES-003 reliability-first | $370.00 | $1.445 | $23.125 | Sum of 17 BOM rows; rows are sourced-class/allowance values, not live quotes |
| DES-004 nominal rotary | $498.00 | $1.945 | $31.125 | `370 + 6400 x 0.020`; axle price is an engineering target, availability unresolved |
| DES-004 conservative rotary | $729.00 | $2.848 | $45.563 | `370 + 6400 x 0.050 + 320 x 0.050 + 9 + 12 + 2`; allowance, not quote |
| A-010 translating gate | >=$370 plus unspecified purchased parts | >=$1.445 plus unspecified parts | >=$23.125 plus unspecified parts | DES-004 retained system less axle allowance; sheet/fastener/cartridge needs unresolved |

The DES-002 and DES-004 source CSVs contain component rows plus total/subtotal
rows; do not sum all `ext_usd` values blindly. For DES-002, summing only rows
whose item is not `TOTAL` gives $226.77; the explicit delivered total is
$263.05. Reproduce the intended DES-004 totals with the formulas above and
the source files:

- `08-integrated-designs/DES-002-low-cost-mask/bom_s6lc.csv`
- `08-integrated-designs/DES-003-reliability-first/bom_a1.csv`
- `08-integrated-designs/DES-004-five-level-rotary-reference/bom_des004.csv`
- `06-experiments/E-013-des-004-axle-pin-sourcing-and-fit-screen.md`

No independent 20x20-cell design quantity is defined in the current inputs;
the tile column is therefore a transparent normalization, not a purchasing
recommendation.

## Cost drivers and reduction screen

DES-002's largest documented lines are the NEMA23 lift ($30), lead-screw
system ($24), reset carriage/frame hardware ($20), and axial thrust bearings
($18). Removing or simplifying the reset carriage could lower purchased cost,
but the retired global-reset variant/ADR-003 records that global reset is unimplemented and can disturb
loaded terrain; it is not an accepted saving. Removing readback is a major
DES-002 cost advantage, but it sacrifices fault observability and
maintainability rather than being a free optimization.

DES-003's dominant purchased lines are eight reader heads ($96), eight writer
actuators ($72), and the two guide/gantry lines ($38 combined). Reusing the
shared gantry and heads is the main reason DES-004 adds only the axle line;
reducing head count or feedback channels would reduce cost but changes the
timing and reliability assumptions and is not accepted by this baseline.

DES-004's sole new purchased class is 6,400 axle pins. The nominal $0.020/pin
target gives $498 total; the conservative $0.050/pin plus 5% stock and service
spares gives $729. E-013's dated catalogue observations are much higher than the target and do not establish a delivered bulk quote. Bulk cut/debur pins and pre-cut precision pins are possible future quote comparators if a concrete mechanism retains these axles. Integral printed axles are excluded from the cost pass
because they trade purchase cost for unresolved wear, creep, fit, and
replacement risk.

A-010 may remove the axle purchase, but its gates, laminations, guides, and
possible reinforcement are not costed. That makes its apparent saving a
lower bound, not a cheaper architecture conclusion. Its main benefit is
potentially simpler state/load separation and cartridge serviceability; its
risks move to planar friction, registration, debris, and assembly yield.

## Conditional sourcing threshold

If a new complete mechanism retains purchased axles, the historical screen allows at most $0.02031 delivered per installed pin for the nominal $500 ceiling, or $0.01592 per delivered pin for 6,720 pieces after the $23 service allowance. These are calculated thresholds, not quotes. First establish geometry, quantity and complete-system feasibility; request a fit-specific delivered quote only when it can change selection. No automatic sourcing task follows for the superseded designs.

## ADR-006 complete mask-generator boundary screen

E-044 supersedes the preliminary screen below for the complete
mask-generator boundary. Retain the $370.00 DES-003 amount as an inherited
shared-machine baseline, not as the mask-generator BOM. The complete-boundary
increment is conditional on whether the inherited reader heads pass an
optical-stack, cabling, and timing compatibility check:

| Case | Low | Base | High | Reader treatment |
|---|---:|---:|---:|---|
| Reuse verified | $486.29 | $602.29 | $872.29 | DES-003 reader heads reused; fallback QRE1113/ADC/carrier omitted |
| Fallback reader | $505.59 | $631.59 | $921.59 | Explicit QRE1113/ADC/carrier stack added only if reuse fails |

These are purchased-component allowances and observed catalogue prices, not
delivered supplier quotes. E-044 corrects the preliminary $921.99 high case:
the controller is $4.59, not $5.00. The fallback stack must not be added to
the reuse-verified case, because the inherited $370 baseline already carries
the reader heads and controller infrastructure. No physical validation,
procurement commitment, or complete-boundary performance claim follows.

The unresolved terms remain the medium and five-plane price, clamp/fiducial
fit, four actuator part and life, reader compatibility, reader carrier/PCB
if needed, harness interface, and cleaning/media-life allowance.

The next useful cost evidence depends on defining the missing state-changing medium and complete actuator/reader implementation. Compare system quantities and allowance sensitivity computationally before choosing targeted compatibility calibration or drawing-specific sourcing.

Date basis: 2026-10-07. This is a purchased-component planning screen for the
minimum complete arbitrary-map boundary in ADR-006/E-017, not a supplier quote
or hardware validation. The inherited DES-003 amount is **$370.00** (the sum
of its 17 BOM rows); it already includes the shared gantry, eight writer
actuators, eight reader heads, controller, drivers, power, loom, switches,
fasteners, and spares. The additions below are therefore only terms that the
mask-generator boundary cannot omit. 3D-printed parts, print consumables,
labour, freight, tax, and payment fees remain excluded.

### Incremental BOM

| Boundary term | Supplier / part or basis | Qty | Unit USD | Ext. USD | Evidence type | Availability / risk |
|---|---|---:|---:|---:|---|---|
| Reusable four-plane media plus one service set (five plane sheets) | No catalogue fit/material selected; planning allowance | 5 planes | 4 / 12 / 30 | 20 / 60 / 150 | allowance; low/nominal/high assumption | Highest unresolved term: thickness, wear, aperture process, cleanability, and replacement format |
| Clamp, hard datum, latch, and two-fiducial hardware | No drawing-level purchased set exists; planning allowance | 1 set | 15 / 35 / 80 | 15 / 35 / 80 | allowance; low/nominal/high assumption | Must not trade away reseat registration or loaded-neighbour isolation |
| Precision datum/fiducial pins or shim stock | Fit-specific hardware not selected; planning allowance | 1 set | 8 / 20 / 50 | 8 / 20 / 50 | allowance; low/nominal/high assumption | Catalogue stock is available, but cut size and tolerance are unresolved |
| Independent writer-channel actuators | DES-003's $9/head row is the only existing cost anchor; exact force/stroke part unresolved | 4 | 9 / 15 / 30 | 36 / 60 / 120 | allowance derived from prior estimate, not quote | Actuator fit and cycle life can dominate; do not replace with printed flexures without wear testing |
| Writer-channel driver ICs | Texas Instruments DRV8833CRTER, Digi-Key 296-38587-1-ND, [catalogue page](https://www.digikey.com/en/products/detail/texas-instruments/DRV8833CRTER/5039360) | 2 | 2.19 | 4.38 | sourced catalogue price, USD, observed 2026-10-07 | 2,930 in stock in the captured listing; bare IC still needs PCB/carrier and thermal/layout work |
| Mask-generator controller | Raspberry Pi Pico SC0915, Digi-Key 2648-SC0915CT-ND, [catalogue page](https://www.digikey.com/en/products/base-product/raspberry-pi/1690/RP2040/659562) | 1 | 4.59 | 4.59 | sourced catalogue price, USD, observed 2026-10-07 | 42,627 in stock in the captured listing; controller bandwidth and I/O mapping remain engineering assumptions |
| Verification ADC | Microchip MCP3008-I/SL, Digi-Key 150-MCP3008-I/SL-ND, [catalogue page](https://www.digikey.com/en/products/detail/microchip-technology/MCP3008-I-SL/319423) | 1 | 2.90 | 2.90 | sourced catalogue price, USD, observed 2026-10-07 | 5,320 in stock in the captured listing; this is an interface part, not evidence of reader discrimination |
| Verification optical sensors | onsemi QRE1113, Digi-Key QRE1113-ND, [catalogue page](https://www.digikey.com/en/products/detail/onsemi/QRE1113/2175990) | 8 | 0.80 | 6.40 | sourced catalogue price, USD, observed 2026-10-07 | 12,547 in stock in the captured listing; 1 mm nominal sensing distance may not fit the mask optical stack |
| Reader optics/carrier and PCB allowance | Sensor carrier, emitter/geometry, resistors, and board fabrication are not specified | 1 set | 10 / 20 / 40 | 10 / 20 / 40 | allowance; low/nominal/high assumption | Could be avoided only if DES-003 reader heads pass a drawing-level compatibility check |
| Channel/media interface harness | Pololu 5615 3-pin JST-PH-style cable, Digi-Key 2183-5615-ND, [catalogue page](https://www.digikey.com/en/products/detail/pololu/5615/26887362) | 8 | 2.29 | 18.32 | sourced catalogue price, USD, observed 2026-10-07 | 118 in stock in the captured listing; connector family is an example, not a locked interface |
| Cleaning and replacement allowance | Wipes/cleaning agent plus one damaged/rejected media event | 1 allowance | 10 / 30 / 75 | 10 / 30 / 75 | allowance; low/nominal/high assumption | Required service term; exact consumable and media-life test are unresolved |

The sourced subset is $36.59 under the dated observations. E-044 is canonical for corrected controller price and conditional reader accounting; obsolete totals are retained in Git history. These values do not establish reader discrimination, writer timing or media life.

### Cost-reduction and sourcing-risk screen

The strongest credible reductions remove terms: reuse the eight DES-003 reader
heads if their optical stack and timing are compatible; use one controller and
shared driver/power infrastructure; and use local clamping rather than adding
a full cassette transport. These reduce unique purchased part count and
assembly, but require coupon evidence for registration, reader margin, and
loaded-neighbour disturbance. Replacing four independent writer channels with
serial writing is cheaper in parts but fails the current arbitrary-map timing
bound; removing verification improves price and assembly effort but hides
wrong-map and maintenance faults. Replacing reusable media with disposable
sheets moves cost to every update and adds waste, feed, registration, and
cleaning failure modes. Optimistic bulk pricing for the media or actuators is
not a cost reduction until a drawing-level quote includes tolerances, MOQ,
debur/chamfer, lead time, and delivered cost.

Explicitly unresolved: the exact medium and five-sheet price, four actuator
part number and life, clamp/fiducial drawing and price, whether DES-003 reader
heads can be reused without the eight QRE1113 sensors, PCB/carrier fabrication,
and delivered availability after freight/tax. Resolve a complete mechanism and sensitivity first; select a quote or physical compatibility test only if it can change its ranking. Do not spend on interfaces for an undefined medium.
