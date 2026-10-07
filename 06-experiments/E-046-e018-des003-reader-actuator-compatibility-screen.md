---
status: complete
builds-on: [E-023, E-018, DES-003]
---

# E-046: E-018/DES-003 reader and actuator compatibility screen

Date basis: 2026-10-07. This is a drawing-level compatibility gate only. It
does not claim physical testing, supplier commitment, procurement, reader
reuse, actuator fit, force, life, or hardware validation.

## Scope and controlled datums

E-018 is the frozen compatibility authority: 40 x 40 x 3.00 mm frame,
34 x 34 x 0.80 mm independent carriers, 5.08 mm cell pitch, 3 x 3 mm
apertures, fiducials at (-15,-15) and (15,15) mm, reader lower face 2.00 mm
above the upper carrier, and four 4 x 1 x 0.80 mm writer tongues on 2.00 mm
centre pitch. E-018's north rail is the positive seating datum; the reader is
not a datum.

DES-003 evidence available to this screen is only its integrated-design
summary and inherited analytical references: eight reader/writer heads,
0.44 mm reflective-flag aperture, 1.8 mm flag-target standoff, modelled
1.405 mm spot, 7.72x on/off return, 71 cells/s/head lower rate, and a 20.18 s
inherited full-cycle accounting. No dimensioned DES-003 head/mount drawing,
beam-centre datum, connector/pinout drawing, or exact 5 V actuator mechanical
drawing is present in the screened repository evidence.

## Gate method and disposition

| Gate | Analytical screen | Disposition | Minimum closure evidence |
|---|---|---|---|
| XY overlay | Transform each DES-003 optical axis and mount datum into the E-018 frame. Evaluate centre, four field corners, and both fiducials. Acceptance is transformed active-aperture residual <=0.20 mm after reseat. No DES-003 XY datum exists. | **HOLD** | Dimensioned head/mount drawing, controlled E-018 datum overlay, 2-D transform, tolerance stack, residual table. |
| Z working distance / collision | E-018 reader relation is 2.00 mm to the upper carrier; DES-003's 1.80 mm is to a different flag target. Nominal difference is `2.00 - 1.80 = 0.20 mm`, not a stack closure. Four 0.80 mm carriers plus three 1.20 mm gaps give `6.80 mm` carrier stack before frame/clamp tolerances. Writer tongues must clear in engaged and parked states. | **HOLD** | Section overlay including carrier flatness, clamp/reseat, head mount, optical working distance, all tongue states, and worst-case collision margins. |
| Optical isolation / plane identity | E-018 requires four-plane identity and rejects wrong/ambiguous/missing reads. The DES-003 flag aperture, spot, and return model are for reflective flags; they do not establish contrast or occlusion through E-018's 2.00 mm port pitch, 1.20 mm plane gaps, or loaded N/E/S/W neighbours. | **HOLD** | Ray/occlusion drawing, actual emitter/detector field, mask optical assumptions, ambient/saturation bounds, and per-plane calibration record. |
| Cable / pinout / envelope | E-022's inherited loom allowance does not identify connector, polarity, pinout, retention, cable OD, bend radius, exit, strain relief, or head-carrier envelope. No adapter, harness, PCB, or strain relief is added by assumption. | **HOLD** | Connector and mechanical cable drawing plus pin-to-controller table and head envelope overlay. |
| Full readback timing / retry | E-018 requires all 100 plane/cell values, two fiducials, settle, reject handling, and bounded retry. Inherited DES-003 accounting is 20.18 s, leaving `30.00 - 20.18 = 9.82 s` analytical margin. This is not an E-018 timing trace and unspecified reader delay is outside it. | **HOLD** | Timestamped pulse/sample/settle schedule, 100-value compare, fiducials, reject/fault trace, and worst-case one-retry total <=30.00 s. |
| Calibration / fault observability | E-018 contract is analytically **GO as an input**: calibration threshold 0.85, exact 4 x 25 comparison, and wrong/ambiguous/missing rejection are frozen. DES-003 calibration ID, saturation/ambient limits, stale-read behavior, and plane-specific fault codes are absent. | **HOLD for DES-003 implementation** | Calibration record and deterministic trace for wrong, ambiguous, missing, stale, and wrong-plane cases. |
| Exact 5 V actuator envelope / force-driver | The only exact candidate named in available evidence is Olimex PUSH-PULL-SOLENOID-5V, Digi-Key 1188-PUSH-PULL-SOLENOID-5V-ND: catalogue observations 5.00 mm stroke, 5-6 V, 6 ohm. These do not define body/mount/plunger envelope, usable travel, stop, force, return, life, or tolerance. | **HOLD** | Exact mechanical drawing, 1:1 tab/stop overlay, force at 1.00 mm engagement, return/park state, life/repeatability, and driver current/duty/thermal evidence. |

No gate is promoted to reader-reuse GO. E-018 geometry, schema, and rejection
rules are GO only as frozen analytical inputs. The complete reuse path is
**REJECT for acceptance now; retain HOLDs** because the missing DES-003
drawings prevent a bounded fit claim. This is a bounded evidence rejection,
not a claim that the hardware can never be adapted.

## Calculations and assumptions

The reproducible arithmetic is in `analysis/compatibility_screen.py`:

* carrier stack: `4 x 0.80 + 3 x 1.20 = 6.80 mm`;
* nominal standoff difference: `2.00 - 1.80 = 0.20 mm`;
* one Olimex coil, if the catalogue voltage/resistance observations apply,
  `5 V / 6 ohm = 0.833 A` and `5 V x 0.833 A = 4.167 W`;
* four-coil steady-state arithmetic is `3.333 A` and `16.667 W`; and
* inherited timing margin is `30.00 - 20.18 = 9.82 s`.

The actuator current and power are Ohmic calculations, not inrush or thermal
measurements. The 20.18 s value is an inherited analytical planning value, not
a measured timing result. The E-018 0.20 mm residual and threshold 0.85 are
acceptance-contract inputs, not evidence that DES-003 satisfies them.

## Reproducibility and local results

Commands run from the repository root:

```sh
python3 06-experiments/E-018-four-plane-mask-generator-coupon-package/analysis/coupon_protocol.py --check
openscad --export-format binstl -o /dev/null -D 'part="assembly"' 06-experiments/E-018-four-plane-mask-generator-coupon-package/cad/four_plane_mask_coupon.scad
python3 tools/curated-experiment-checks/E-046/compatibility_screen.py
./repo check
```

Expected analytical output from the new script:

```text
plane_stack_mm=6.80
nominal_standoff_delta_mm=0.20
actuator_nominal_current_A=0.833
actuator_nominal_power_W=4.167
four_actuator_steady_current_A=3.333
four_actuator_steady_power_W=16.667
complete_readback_bits=100
fiducial_reads=2
bounded_retries=1
inherited_cycle_s=20.18
analytical_margin_s=9.82
physical_validation=False
```

The coupon checker and OpenSCAD export are CAD/geometry/schema checks only;
the script is calculation only. None is physical validation.

## Handoff and rollback

Handoff to the DES-003 mechanical/controls owner: release the missing
dimensioned reader head/mount and cable/pinout drawings, then produce the
one-head E-018 overlay before expanding it to eight heads. In parallel,
release the exact Olimex body/mount/stop drawing and driver-duty evidence.
Do not procure, add a sensor/ADC/harness/driver/spring/carrier, or claim
reader reuse from nominal dimensions.

Integration is limited to this result and its reproducible analysis script;
E-018, E-023, and DES-003 are unchanged. Rollback is reverting this commit;
the prior evidence remains available through Git history.
