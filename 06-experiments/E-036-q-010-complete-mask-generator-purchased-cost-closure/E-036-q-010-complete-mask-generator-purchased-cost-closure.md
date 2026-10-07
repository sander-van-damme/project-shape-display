---
status: active
builds-on: [Q-010, E-022, E-023, A-011, ADR-006]
---
---
status: active
builds-on: [Q-010, E-022, E-023, A-011, ADR-006]
---

# E-036: Q-010 complete mask-generator purchased-cost closure

Date basis: 2026-10-07. Currency: USD. Scope is one 80 x 80 reference
machine and the complete arbitrary-map boundary: four reusable writing planes,
positive registration/clamp, four parallel writer channels, verification /
readback, service stock, and reusable media. The $370 DES-003 shared-machine
baseline is included because it carries the inherited gantry, eight head
positions, controller, drivers, power, loom, switches, fasteners, and spares.

This is a sourced-price and bounded-estimate screen, not a quote, CAD release,
procurement commitment, or hardware validation. Excluded: 3D-printed parts,
print material/time, labour, freight, tax, payment fees, validation fixtures,
and a full cassette transport. The selected boundary uses a local clamp; its
registration and debris gates remain open.

## Complete purchased BOM

Quantities are for one machine. Five media planes means four installed plus
one service/replacement plane. “Sourced” means a catalogue observation on the
date above; it does not establish fit, life, or future availability. All
allowances are estimates pending drawing-level RFQs.

| Item | Qty | Low | Base | High | Basis and unresolved gate |
|---|---:|---:|---:|---:|---|
| Reusable metal media planes | 5 | $20 | $60 | $150 | Estimate $4/$12/$30 each; material, thickness, aperture process, flatness, cleanability, life and delivered price unresolved |
| Local clamp, hard datum, latch | 1 set | $15 | $35 | $80 | Estimate; positive reseat registration and loaded-neighbour isolation need drawing/RFQ |
| Fiducial pins/shim stock | 1 set | $8 | $20 | $50 | Estimate separate from clamp; tolerance stack and burr control unresolved |
| Writer actuators | 4 | $36 | $60 | $120 | Planning allowance $9/$15/$30 each; current $3.34 Olimex catalogue item lacks force/life and was 0 in stock, so it is not accepted as the low case |
| DRV8833CRTER four-half-bridge drivers | 2 | $4.38 | $4.38 | $4.38 | Sourced: $2.19 each at qty 1, 2,930 in stock; Digi-Key 296-40079-1-ND. Existing actuator wiring/current compatibility unresolved |
| Raspberry Pi Pico SC0915 controller | 1 | $4.59 | $4.59 | $4.59 | Sourced: $4.59 qty 1, 43,292 in stock; Digi-Key 2648-SC0915CT-ND. Production carrier and firmware timing are not included |
| Fallback verification ADC MCP3008-I/SL | 1 | $2.90 | $2.90 | $2.90 | Sourced: $2.90 qty 1, 5,320 in stock; Digi-Key 150-MCP3008-I/SL-ND. Alternative only if inherited readback is rejected |
| Fallback reflective sensors QRE1113 | 8 | $6.40 | $6.40 | $6.40 | Sourced: $0.80 each qty 1, 12,547 in stock; Digi-Key QRE1113-ND. 1 mm sensing geometry is not fit evidence |
| Fallback reader optics/carrier/PCB | 1 set | $10 | $20 | $40 | Estimate; no selected optical stack, board, or carrier drawing |
| Channel/media interface cables | 8 | $18.32 | $18.32 | $18.32 | Sourced example: Pololu 5615 $2.29 each qty 1; final loom may differ after connector/strain-relief freeze |
| Cleaning and replacement service stock | 1 allowance | $10 | $30 | $75 | Estimate for cleaning consumables plus one damaged/rejected media event; media-life test unresolved |

The ADC, QRE1113, and reader carrier are mutually alternative to inherited
DES-003 readback, not additive in the reuse case. A compatible inherited
reader path contributes $0 incremental reader cost only after all eight heads
pass the E-018 XY, Z-stack, optical field, plane identity, cabling, timing,
calibration, and fault-rejection gates.

## Current source observations

Primary supplier pages checked 2026-10-07:

- [DRV8833CRTER at Digi-Key](https://www.digikey.com/en/products/detail/texas-instruments/DRV8833CRTER/5039360): $2.19 cut-tape qty 1; 2,930 in stock; active; 16-week standard lead time shown.
- [Raspberry Pi SC0915 at Digi-Key](https://www.digikey.com/en/products/detail/raspberry-pi/SC0915/13684020): $4.59 cut-tape qty 1; 43,292 in stock; active; 18-week standard lead time shown.
- [MCP3008-I/SL at Digi-Key](https://www.digikey.com/en/products/detail/microchip-technology/MCP3008-I-SL/319423): $2.90 qty 1; 5,320 in stock; active.
- [QRE1113 at Digi-Key](https://www.digikey.com/en/products/detail/onsemi/QRE1113/2175990): $0.80 qty 1; 12,547 in stock; active; 1 mm nominal sensing distance.
- [Pololu 5615](https://www.pololu.com/product/5615): $2.29 qty 1; price breaks begin at five; active/preferred listing.
- [Olimex 5 V push-pull solenoid at Digi-Key](https://www.digikey.com/en/products/detail/olimex-ltd/PUSH-PULL-SOLENOID-5V/23330937): $3.34 qty 1, but 0 in stock with one estimated 2026-10-15 and five-week standard lead time; stroke is 5 mm, while force/life data and E-018 fit remain unresolved.
- [Delta DSML family at Digi-Key](https://www.digikey.com/en/product-highlight/d/delta-electronics/dsml-series-latching-solenoids): DSML-0224-12 is listed at $9.42 each with 898 available and 5.08 mm stroke; exact force, mounting, duty, and engagement fit remain unresolved.

The listing observations support availability and unit-price inputs only. They
do not prove mechanical compatibility, timing, reliability, or procurement
closure.

## Scenario totals

The complete electronics/harness subset including the fallback reader is
`2×2.19 + 4.59 + 2.90 + 8×0.80 + 8×2.29 = $36.59`. Inherited-reader reuse
uses only drivers, controller, and harness: `4.38 + 4.59 + 18.32 = $27.29`.
Calculated totals are:

| Case | Calculation summary | Purchased total |
|---|---|---:|
| Reuse / low | $370 baseline + media 20 + clamp 15 + fiducials 8 + actuators 36 + reuse electronics/harness 27.29 + service 10 | **$486.29** |
| Reuse / base | $370 + 60 + 35 + 20 + 60 + 27.29 + 30 | **$602.29** |
| Reuse / high | $370 + 150 + 80 + 50 + 120 + 27.29 + 75 | **$872.29** |
| Fallback reader / low | reuse low + ADC 2.90 + sensors 6.40 + carrier 10 | **$505.59** |
| Fallback reader / base | reuse base + 2.90 + 6.40 + 20 | **$631.59** |
| Fallback reader / high | reuse high + 2.90 + 6.40 + 40 | **$921.59** |

These totals retain E-022's corrected inclusion of the separately listed
fiducial set. The complete boundary is therefore bounded at **$486–$872 with
inherited readback** or **$506–$922 with the explicitly costed fallback
reader**, before freight/tax and without 3D-printed parts. The base estimate
is $602/$632 respectively. The $370 baseline alone is incomplete.

## Cost-driver and reduction disposition

The dominant uncertainty is reusable media plus clamp/fiducial and actuator
fit, not the catalogue electronics. The preferred reductions remove parts or
mechanisms:

- Reuse DES-003 readers if the E-018 overlay/calibration/timing gate passes:
  removes the fallback stack, about $19/$29/$49 from low/base/high, and
  reduces unique parts and assembly. It is conditional, not a $0 assumption.
- Keep one Pico and two DRV8833 devices for four channels: low part count and
  low sourced cost, but current, thermal, fault isolation, and actuator
  wiring must close.
- Keep local clamp rather than adding a cassette transport: likely removes
  moving parts and an unbounded purchased subsystem, but increases datum,
  debris, and operator reseat sensitivity.
- Do not use disposable media, remove verification, serialize writing, or
  assume bulk actuator/media pricing. Those options add recurring waste,
  remove fault observability, violate the analytical 30 s boundary, or rely
  on unsupported price/fit claims.

## Closure and next owner

Q-010's purchased-cost boundary is reproducibly bounded, but not physically
or commercially closed. Prepared-mask, cassette-only, buffer-only, and
serial-writer comparisons are rejected because they omit the arbitrary-map
write path or verification boundary. Analytical 30 s/full-field and local
update timing remains a separate gate; this cost result does not prove it.

Next owner: DES-003 mechanical/controls owner, with Cost & Sourcing support.
Issue one RFQ for five identical cut/debur planes, one clamp/fiducial set,
and four exact writer actuators. Require material/thickness, aperture and
fiducial tolerances, flatness, force-versus-stroke, return/latching behavior,
cycle life, duty, MOQ, lead time, packaging, freight, and delivered price.
In parallel, record the eight inherited-reader dimensions, optical stack,
pinout, timing, and calibration margin against E-018. Do not order parts or
claim compatibility until those gates pass.

## Verification record

Commands run from the project root:

```text
./repo check
```

Result: `OK: 107 objects; structure and builds-on references valid`.
`git diff --check` also passed before commit.
