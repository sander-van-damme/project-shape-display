---
status: active
builds-on: [E-044, E-022, E-023, E-040, E-018, E-043, DES-003, ADR-005, ADR-006]
---

# E-045: independent falsification of E-044 sourcing and compatibility screen

Date basis: 2026-10-07. This is an independent document, arithmetic, and
geometry audit. No supplier quote, procurement action, physical measurement,
or hardware-performance result was obtained.

## Verdict

**HOLD retained; E-044 is internally reproducible as a planning screen, but
not procurement-authorized or integration-ready.** The arithmetic and
reuse/fallback separation pass. The evidence does not support promoting any
catalogue candidate to a selected component or treating the RFQ-ready label
as a closed interface.

No E-044 conclusion requires reversal. One wording correction is required
before curation: E-044's statement that the Olimex listing was observed
out-of-stock with an estimated availability date is a time-sensitive source
observation from E-023, while E-040 explicitly limits its source record to
catalogue observations and says no live availability was verified. It must be
read as a dated, non-live observation, not current availability evidence.

## Independent arithmetic check

The inherited DES-003 term is counted once. The fallback reader rows are
alternative to inherited-reader reuse, not additive to it.

| Scenario | Recalculation | Result | Check |
|---|---|---:|---|
| Reuse low | `370+20+15+8+36+4.38+4.59+18.32+10` | $486.29 | pass |
| Reuse base | `370+60+35+20+60+4.38+4.59+18.32+30` | $602.29 | pass |
| Reuse high | `370+150+80+50+120+4.38+4.59+18.32+75` | $872.29 | pass |
| Fallback low | `486.29+6.40+2.90+10` | $505.59 | pass |
| Fallback base | `602.29+6.40+2.90+20` | $631.59 | pass |
| Fallback high | `872.29+6.40+2.90+40` | $921.59 | pass |

Fallback deltas independently recompute to `$19.30 / $29.30 / $49.30`.
The observed electronics/harness subset is
`2x2.19 + 1x4.59 + 8x2.29 = $27.29` for reuse; adding QRE1113 and MCP3008
produces the separate fallback subset `$36.59`. This catches the older
$36.59 reuse presentation but does not change E-044's corrected totals.
The $370 value is an inherited calculation, not a complete-machine quote.

## Falsification attempts

### Transformed/reseat residual gate

E-018 defines a maximum transformed active-aperture residual of 0.20 mm after
every reseat, with two Ø2 mm fiducials, a positive datum, and a 5.08 mm field.
The public stainless capability carried into E-023/E-044 is ±0.005 in, or
±0.127 mm. This leaves only 0.073 mm of one-sided numerical allowance before
datum location, material thickness/flatness, burr/kerf, clamp preload,
transformation estimation, and reseat error are added. It is not valid to
subtract the published tolerance from the gate as a complete stack without a
defined error model; however, the comparison decisively falsifies any claim
that the catalogue capability alone closes the gate. E-044 correctly lists
the overlay and reseat record as required evidence, but its RFQ-ready label
must not be interpreted as tolerance acceptance.

The nominal 0.80 mm carrier and nearest public 0.76 mm sheet thickness are
also not interchangeable evidence: the 0.04 mm nominal difference is only a
geometry comparison, not a flatness, preload, or optical-Z result.

### Actuator/electrical compatibility boundary

E-023 identifies the Olimex candidate as 5--6 V, 6 ohm, 5 mm stroke. Ohmic
inrush arithmetic is `5 V / 6 ohm = 0.833 A` per coil, or `3.33 A` for four
coils if energized simultaneously. This is a calculation from the listed
resistance, not a measured current waveform. E-018 only defines 1.00 mm tab
insertion and a 0.20 mm parked clearance; it does not define actuator force,
linkage, hard stop, return state, duty, thermal margin, or whether four
channels are energized concurrently. Therefore the DRV8833 two-IC count and
the $36 actuator allowance do not establish electrical or mechanical
compatibility. E-044's required force-at-1-mm, current/inrush, flyback,
thermal, return, life, stop, and clearance evidence is necessary and
correctly remains HOLD.

The Delta family observation is not a bounded substitute: its 12 V family
voltage crosses the existing 5 V path, and a family listing is not an exact
part envelope/force/life record. Keeping it rejected for the current boundary
is supported.

## Source traceability and omitted purchased terms

The source identities are traceable to E-022/E-023/E-040: Digi-Key part IDs
for DRV8833CRTER, SC0915, QRE1113 and Olimex; Pololu 5615; and SendCutSend's
stainless capability page. They are dated catalogue observations, not
immutable quotations. E-040's statement that live availability was not
verified controls any stronger interpretation of current stock or lead time.

The following remain omitted or explicitly excluded rather than silently
closed: freight, tax, labour, payment fees, 3D-printed parts, validation
fixtures, PCB/carrier fabrication, actuator mounting/linkage and return
hardware, final loom/strain relief/adapters, media packaging and delivered
price, setup/tooling/MOQ, cleaning selection and replenishment basis, and
reader carrier/optics/calibration if reuse fails. Their omission is
consistent with ADR-005 only because E-044 labels the result a planning
screen and lists the terms as pre-pass evidence. It would be incorrect to
call the totals landed cost or a procurement budget.

## Disposition

**E-044: HOLD.** Keep its canonical reuse/fallback arithmetic and RFQ package,
but correct or annotate the Olimex availability sentence as a dated
non-live observation. Do not authorize purchase, integration, or reader
reuse from this audit. The smallest decisive next evidence remains: a
controlled E-018 drawing/overlay and reseat residual record; exact actuator
force/stroke/return/life/current/thermal data against the DRV8833 path; and
supplier responses with delivered-price, MOQ, setup, packaging, and lead-time
terms. Analytical agreement with E-018 remains CAD/interface evidence only.
