---
status: complete
builds-on: [E-024, E-023, E-022, E-018, DES-003, ADR-005, ADR-006]
---

# E-025: independent falsification review of E-024

Date basis: 2026-10-07. This is an independent review of drawing-,
calculation-, and catalogue-derived claims. No physical measurement, supplier
commitment, sample, fit test, force test, life test, or hardware validation was
performed.

## Verdict

E-024 is a useful and appropriately skeptical screen, but it is **not a
compatibility acceptance** and does not support procurement or CAD integration.
Its reader gates are mostly correctly unresolved/conditional, and its Delta
decision is correctly bounded to the existing-driver path. The Olimex item is
only an electrical/interface candidate for the next falsification; it is not a
selectable actuator. The screen contains one arithmetic defect: its stated
base screening total is low by the $30 service allowance.

Correct base arithmetic is:

`370 + 175 + 45 + 37.68 + 4.38 + 4.59 + 18.32 + 30 = $684.97`.

The E-024 value `$654.97` omits the final `+30`, despite describing the same
service allowance immediately above it. The low value `$535.65` is correct.
This does not alter E-022's canonical `$486.29–$872.29` reuse range or
`$505.59–$921.59` fallback range; the E-024 table is a noncanonical screening
case with different media, clamp, and actuator terms.

## Claim audit

| Claim or gate | Falsifier finding | Disposition |
|---|---|---|
| Reuse of eight DES-003 heads | No head envelope, beam centre, connector/pinout, tolerance, optical field, plane-occlusion drawing, or calibration/fault record is present. E-018 nominal CAD cannot supply those missing head data. | **Unresolved; reuse must remain $0 only as a conditional BOM alternative.** |
| XY and transformed residual | The required `≤0.20 mm` residual is stated, but no transform, tolerance stack, head datum, or measured/as-built input is available. | **No analytical pass.** |
| Z compatibility | `2.00 − 1.80 = 0.20 mm` is valid nominal subtraction, but the two dimensions reference different target surfaces. Carrier flatness, clamp/reseat, mount, and working-distance tolerance are absent. | **Conditional only; not fit evidence.** |
| Optical field and plane identity | DES-003's `0.44 mm` design point and reflective-vane model do not demonstrate contrast or selective classification through the E-018 four-plane stack and its materials. No ray/occlusion or ambient/saturation bound closes this. | **Unresolved.** |
| Cabling and timing | Inherited loom/controller compatibility is assumed but no connector, retention, bend-radius, strain-relief, pulse/sample/settle schedule, or retry schedule is supplied. `30 − 20.18 = 9.82 s` is correct arithmetic, but it is a full-field inherited model, not a coupon timing result and not proof that reader delay fits. | **Conditional planning bound, not measured or acceptance timing.** |
| E-018 protocol applicability | E-018 defines a 4-plane, 5×5 coupon and explicitly requires complete 100-cell readback, fiducials, reject semantics, and physical port/wear references. E-024 does not claim these are measured, correctly preventing a false pass. | **Analytical handoff is adequate; physical gate remains open.** |
| Olimex 5 V actuator | `5 V / 6 ohm ≈ 0.833 A` nominal coil current is calculable, but driver current margin, inrush, duty thermal behavior, flyback, force, return, stroke coupling, package, life, stock, and stop geometry are not closed. | **Conditional candidate for next screen, not selectable.** |
| Delta 12 V actuator | A 12 V variant cannot use the bounded existing DRV8833 low-voltage path without a new power/driver boundary. The family observation is not an exact-part fit or force/life result. | **Fail for no-added-parts path; not a universal mechanical rejection.** |
| Alternatives and BOM | E-024 keeps Olimex/Delta catalogue arithmetic separate from E-022 allowances and does not silently add fallback QRE1113/ADC/carrier items. Its new base-screen row is nevertheless arithmetically wrong as noted above. | **Treatment is otherwise correct; correct the displayed base total.** |

## Reproduced calculations

* Plane stack: `4 × 0.80 + 3 × 1.20 = 6.80 mm`, before frame, clamp,
  flatness, and process tolerances. This is a nominal stack height, not a
  reader working-distance result.
* Nominal standoff difference: `2.00 − 1.80 = 0.20 mm`. It is not an
  interchangeable datum because E-018 and DES-003 describe different target
  surfaces.
* Catalogue arithmetic: `4 × 3.34 = $13.36`; `4 × 9.42 = $37.68`.
  These observations do not establish availability, force, life, or fit.
* E-024 timing margin: `30.00 − 20.18 = 9.82 s`. The margin is inherited
  analytical budget and must not be reported as measured throughput.
* E-024 low screening case: `370 + 75 + 20 + 13.36 + 4.38 + 4.59 +
  18.32 + 30 = $535.65`.
* E-024 base screening case, corrected: `370 + 175 + 45 + 37.68 + 4.38 +
  4.59 + 18.32 + 30 = $684.97`.

## Required corrections and release gate

1. Correct E-024's `$654.97` base-screen display to `$684.97`, or remove the
   service allowance from both the formula and its stated scope. Preserve
   E-022's canonical arithmetic and nominal defaults.
2. Label the Olimex row and any future candidate table as **not selectable**
   until exact part dimensions, force-versus-stroke, return behavior, duty,
   life, driver thermal/current margin, stock, and 1:1 tab/stop envelope are
   evidenced.
3. Do not call the reader Z or timing gates passes. The required DES-003
   overlay must include head/mount datums, optical working distance, cable
   mechanics, full tolerance stack, and controller timing/retry trace.
4. Do not procure, release integration CAD, add fallback sensors/ADC/carrier,
   or contact suppliers from E-024. A future physical or sourcing task must
   record measured evidence separately from these analytical claims.

## Disposition

The falsification review is complete with an adverse arithmetic finding and
no compatibility acceptance. E-024 may remain the analytical handoff, after
the base-total correction is applied in its owning change. The cheapest
decisive next evidence is the dimensioned DES-003 reader overlay and a
bounded Olimex force/return/driver/stop screen; neither is authorized here.
