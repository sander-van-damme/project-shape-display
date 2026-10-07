---
status: complete
builds-on: [E-024, E-025]
---

# E-026: E-024 analytical release gate repair

Date basis: 2026-10-07. This is a drawing, catalogue, and calculation
correction only. No physical measurement, supplier commitment, fit test,
force test, life test, or hardware validation was performed.

## Scope and disposition

This successor corrects E-024's noncanonical base-screen arithmetic and makes
the next DES-003 reader/actuator release gate executable. E-024 remains the
screened compatibility record; E-025 remains the independent falsification
record. No new sensor, ADC, carrier, driver, power rail, fallback BOM item,
or procurement commitment is introduced.

The base-screen total is **$684.97**, calculated as:

`370 + 175 + 45 + 37.68 + 4.38 + 4.59 + 18.32 + 30 = 684.97`

The final `$30` service allowance is included. The low-screen comparison is
unchanged at `$535.65`. E-022's canonical ranges are unchanged:

| Conditional BOM case | Canonical E-022 range | Treatment here |
|---|---:|---|
| Reuse reader heads | $486.29–$872.29 | preserved; not accepted by this gate |
| Fallback reader stack | $505.59–$921.59 | preserved; added only after a separate fallback drawing |

The E-024 catalogue observations remain separate from those canonical ranges:
four Olimex units are `4 x $3.34 = $13.36`, and four Delta units are
`4 x $9.42 = $37.68`. These are catalogue arithmetic, not fit or availability
evidence.

## DES-003 reader overlay release gate

The overlay shall be a dimensioned drawing package registered to the E-018
coupon, not a nominal compatibility statement. Required common datum frame:
E-018 frame centre as origin, upper carrier surface as Z reference, and the
two fiducials at `(-15,-15)` and `(15,15) mm` as XY registration features.
The overlay must identify the centre target, all four plane surfaces, writer
tab keep-outs, clamp/hard-stop surfaces, head mounting datums, and cable exit
direction.

| Gate | Required inputs and calculation | Status | Closing evidence / acceptance |
|---|---|---|---|
| XY transform | Head-to-mount datum coordinates; E-018 fiducial coordinates; 2-D rigid transform (translation, rotation); as-built or bounded datum residuals | **Unresolved** | Drawing overlay plus transform table and residual stack. Active beam/aperture centre residual `<= 0.20 mm` at centre and corner/check points, with tolerance provenance. |
| Z working distance | Upper carrier, selected target, adjacent plane, head lower face, mount, clamp/reseat, flatness and stop surfaces; DES-003 1.80 mm target and E-018 nominal 2.00 mm lower-face relation kept as separate surfaces | **Conditional** | Section drawing and worst-case stack. Working-distance and focus/clearance limits close for every plane; no writer-tab or carrier collision through reseat tolerance. The nominal `2.00 - 1.80 = 0.20 mm` subtraction alone is insufficient. |
| Optical field and occlusion | Emitter/detector active field, spot/aperture, target reflectance/finish, ambient/saturation bounds; ray paths through four 1.20 mm plane separations and loaded N/E/S/W dummy geometry | **Unresolved** | Optical field drawing and bounded contrast/ambient calculation for each state; selected plane is readable while adjacent planes and tabs are occluded or classified unambiguously. |
| Connector and cable | Exact connector/pinout, mating retention, cable OD/bend radius, exit path, strain relief, moving/sliding envelope and head-carrier interface | **Unresolved** | Connector and cable mechanical/electrical drawing overlaid on the envelope; no uncosted adapter, harness, PCB, or strain-relief item. |
| Timing | Per-head pulse/sample/settle times, eight-head sequencing, transport, complete 4 x 25 readback, fiducials, reject and bounded retry schedule | **Conditional** | Worst-case timing table closes under 30 s. Existing inherited calculation `30.00 - 20.18 = 9.82 s` is a planning margin only and cannot absorb unspecified reader delay by assumption. |
| Calibration and fault semantics | Calibration ID, threshold/ambient/saturation limits, missing/ambiguous signal behavior, plane identity trace, and E-018 exact-state/reject schema | **Unresolved** | Calibration record and software trace demonstrate deterministic accept/reject and fault handling for all four planes and missing/ambiguous reads. |

No reader row is a physical pass. Analytical closure of a row does not prove
hardware performance; physical calibration and coupon testing remain separate
future gates.

## Actuator candidate gate

The writer interface is only known to require a nominal 1.00 mm tab
overlap/insertion. Candidate selection is prohibited until the exact
mechanical and electrical evidence below exists. Olimex and Delta therefore
remain **non-selectable candidates**.

| Gate | Olimex PUSH-PULL-SOLENOID-5V | Delta DSML-0224-12 latching solenoid | Required closing evidence |
|---|---|---|---|
| Exact identity and envelope | Open | Open | Exact part drawing, mounting holes, plunger axis, connector, parked/engaged envelope, neighbouring-tab and 40 mm frame overlay. |
| Stroke and stop geometry | Open | Open | Tab travel requirement, hard-stop datum, usable stroke and worst-case tolerance stack; prove no overtravel or jam. |
| Force and return/latch | Open | Open | Force-vs-stroke at contact geometry, friction/preload assumption, return force or latch reverse-pulse behavior, and defined power-loss parked state. |
| Duty, current and thermal margin | Open | Open | Coil resistance/current including inrush; pulse schedule; driver SOA/current margin and thermal calculation at worst-case duty. Olimex's nominal `5 V / 6 ohm = 0.833 A` is only arithmetic. |
| Life and positional repeatability | Open | Open | Exact-part life rating or measured cycle evidence at the E-018 schedule, plus repeatability/wear tolerance. Catalogue price is not evidence. |
| Driver and flyback | Conditional for existing low-voltage path; not closed | Fail for bounded existing DRV8833 path because the 12 V variant crosses the stated supply boundary | Selected schematic, flyback path, current limit, fault behavior and supply limits. Delta reconsideration requires a separately costed 12 V driver/power boundary. |
| Selection | **Not selectable** | **Not selectable** | All rows above closed by drawing/calculation/catalogue evidence, then separate physical verification before integration release. |

The Delta disposition is bounded to the no-added-parts path and is not a
universal mechanical rejection. The E-022 actuator allowance remains
`$9/$15/$30` per channel; these candidate observations do not replace it.

## Reproducibility and unresolved evidence

Run `python3 check_e026_release_gate.py` in this directory. It checks the
corrected totals, both E-022 range endpoints, catalogue arithmetic, and the
nominal timing/standoff calculations. The script contains only the stated
inputs and does not model sensor performance, force, life, or hardware fit.

The next analytical release package must supply the DES-003 overlay inputs and
the actuator evidence listed in the matrices. Until then, reader XY, optical
field/occlusion, connector/cable, calibration/fault, exact actuator envelope,
force/return, duty/thermal/current, life, and stop geometry remain unresolved.

## Integration and rollback

This record is an analytical successor only. It does not release integration
CAD, change E-022, authorize procurement, or modify DES-003. Integration may
consume this record after review of the listed evidence. Rollback is reverting
the commit containing E-026; E-024, E-025, E-022, E-018, and DES-003 remain
unchanged.
