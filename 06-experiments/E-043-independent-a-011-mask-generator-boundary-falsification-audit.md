---
status: complete
builds-on: [A-011, Q-010, E-017, E-018, E-022, E-023, E-040, ADR-006]
---

# E-043: independent A-011 mask-generator boundary falsification audit

Date basis: 2026-10-07. This is an independent document review and arithmetic/
geometry check. No physical testing, supplier quote, hardware measurement, or
production evidence was available.

## Verdict

**Retain A-011 as the leading arbitrary-map product-boundary candidate, but
hold it before integration planning.** It is analytically more complete than
the prepared-mask, cassette-only, buffered, or serial alternatives. That does
not establish that a buildable, affordable, reliable implementation exists.

The smallest decisive hold condition is the absence of one controlled E-018
coupon result (or equivalent evidence) closing parallel four-plane engagement,
reseat registration, exact readback, actuator compatibility, and loaded-neighbour
isolation. If no mechanism can write all four planes in one addressed
engagement, or if exact state readback cannot reject a blocked/wrong-plane
aperture, reject A-011 for the 30 s arbitrary-map mode rather than relaxing the
boundary.

## Gate dispositions

| Gate | Independent disposition | Basis and falsifier |
|---|---|---|
| Product boundary | **PASS analytically; HOLD for integration** | E-017 correctly includes medium, writer, clamp/transport, registration, verification, recovery, and service media. Prepared or buffered media cannot create an unseen map. The boundary is not a selected geometry or validated product. |
| Update semantics | **PASS as a contract; HOLD in hardware** | Four binary planes, full-map and local-update semantics, exact 4 x 25 readback, bounded retry, and quarantine are specified in A-011/E-018. The 20.18 s full-field and 0.72/1.72 s local values are calculations, not measured execution. A serial fallback is decisively incompatible: 360.6 s for four planes, or 90.1 s even for one serial 5-state code, at the inherited rate. |
| Reader/actuator compatibility | **HOLD; reuse path presently fails acceptance** | E-023/LAB-131 leaves all six DES-003 reader reuse gates unresolved: XY overlay, Z stack, optical field, plane isolation, cabling, timing, and calibration/fault behavior. The nominal 2.00 versus 1.80 mm relation is not interchangeable because the target surfaces differ. Candidate actuator stroke does not prove 1 mm tab force, stop, return, life, or parked clearance; the 0.833 A value is only `5 V / 6 ohm` candidate arithmetic. Delta 12 V is rejected for the existing-driver path. |
| Sourcing/cost | **HOLD; no cost pass** | E-040's $486.29–$872.29 reuse range and $505.59–$921.59 fallback range combine allowances with catalogue observations, exclude freight/tax/labour/fixtures, and depend on unresolved medium, clamp, actuator, and reader fit. E-023's corrected $684.97 screen is explicitly not a replacement baseline. No quote or selected exact actuator exists. |
| Observability | **HOLD for implementation; contract is adequate** | E-018's threshold 0.85, exact-state comparison, and wrong/ambiguous/missing reject rule are strong acceptance requirements. DES-003 calibration IDs, saturation/ambient limits, missing-signal codes, plane identity, and timing trace are absent. A reader part price cannot prove discrimination. |

## Reproducible checks and failure pressure

1. Recompute the inherited timing: `6400 / (8 x 71) = 11.27 s`; adding the
   stated 0.05 + 1.50 + 5.864 + 0.50 + 1.00 s terms gives 20.18 s and leaves
   `30.00 - 20.18 = 9.82 s`. This margin is model slack, not a measured
   reader/actuator schedule, and unspecified reader delay consumes it.
2. Recompute E-023's plane stack: `4 x 0.80 + 3 x 1.20 = 6.80 mm`. The
   inherited 0.44 mm reflective-flag aperture and 1.8 mm flag gap do not prove
   optical isolation through that stack or through loaded neighbours.
3. Compare published stainless cut tolerance ±0.127 mm with the E-018
   transformed residual limit ±0.20 mm. The catalogue capability consumes most
   of the residual allowance before burr, flatness, reseat, datum, and assembly
   errors; it cannot be treated as acceptance evidence.
4. Recompute E-040's canonical reuse base: `370+60+35+20+60+4.38+4.59+18.32+30
   = $602.29`. This is internally consistent, but the $60/$35/$20/$30 terms
   are allowances. The sourced subset and inherited $370 do not close the
   boundary cost.

These checks falsify any stronger claim that A-011 is already compatible,
under-30-second in hardware, procurement-ready, or production-ready. They do
not falsify the product-boundary comparison itself.

## Evidence gaps, tradeoffs, and next action

The cheapest decisive next action is the frozen E-018 5 x 5 coupon protocol:
four independent channels, two fiducials, loaded N/E/S/W neighbours, complete
4 x 25 readback, reseat tags, adversarial maps, and the predeclared 1,000-cycle
plan. Record as-built port dimensions, transformed residuals, reader calibration
and rejection codes, actuator force/return/thermal evidence, cycle/wear state,
and neighbour displacement. Analytical acceptance must remain separate from
physical performance.

**Next owner:** DES-003 mechanical/controls owner, with Cost & Sourcing.
They must return the E-018 overlay/timing/calibration package, an exact
actuator quote or sample data package, and a drawing-level media/clamp quote.
Until then, keep DES-003/DES-004 as the current display baselines; do not
procure or integrate A-011.

## Integration and rollback

If the coupon and compatibility package pass, promote A-011 only as a
controlled implementation candidate with the measured limits and selected
parts added to the design record. If any critical gate fails, retain the
failure evidence, remove A-011's candidate status from integration planning,
and revert to the current DES-003/DES-004 baseline; do not silently substitute
serial writing, unverified reader reuse, or prepared-mask buffering.
