# DND-4: close M4 land reach analytically + fix two printability-validator mis-scopes

Resolves the follow-up on [DND-4](/DND/issues/DND-4) (S3/S4 shared-drive family).
Bases on the merged pivot-clearance work (PR #30) and closes the last thin S3
analytic gate term. **Calculation/CAD only — no print, no measurement**
([DND-27](/DND/issues/DND-27)).

## Engineering question

1. Is the S3 fan-out **M4 "land reach"** gate a real design failure, or a
   modelling artefact?
2. Why did the unified printability validator report the S3 coupon as `FAIL`
   while the experiment's own analytic gate reported it printable?

## What changed

- `06-experiments/test11_shared_drive_gate_analysis/analytic/t11a_analytic_gate.py`
  — M4 is now the **finger angular throw** `asin(land/FINGER_H)` from the CAD
  land height (`LAND_H_NOMINAL = 0.90 mm` → 16.3°) plus an explicit contact
  floor, replacing `|land − 0.50| > 0.20`. Adds an `ANALYTIC_FAIL_LAND_REACH`
  verdict path.
- `.../t11a_fit_check.py` — gates `M4_land_mm` on the contact floor
  (≥ 0.30 mm) and finger half-height band instead of the old ±0.20 window.
- `tools/validate/analytic_printability.py` — stop applying the **inserted-pin**
  rule (`min_pin_dia = 5.0 mm`) to a **printed-in-place** boss; classify it as a
  printed feature and add the designed journal free-play check.
- Regenerated analytic record; README / protocol / analytic README updated to the
  corrected M4 definition.

## Results

- M4 land reach: worst-case margin **+0.35 mm**, Monte Carlo pass **1.0000**
  (was −0.05 mm / 0.9077). The old number compared the land against an arbitrary
  window around a 0.50 mm protocol artefact, not a physical reach condition.
- Fit engine on the analytic record: **`S3_DENSITY_PRINTABLE`** at the 0.4 mm
  baseline (analytic screen, explicitly not a print).
- Unified validator on the coupon: **RISK**, not FAIL. The 0.47 mm web is
  between one and two extrusion lines — a genuine thin-feature finding, honestly
  classified, not a kill.

## Passed / failed

- PASS: full `engineering-checks` command set locally (**18/18**), including
  test08–test11, the fit engine self-test/validate/predict, the analytic gate
  self-test/record/replay, and the sourced-limit printability table.
- No design FAIL remains asserted-passing; the coupon's thin web stays a
  reported RISK.

## Assumptions / limits

- Dimensional stack-up only. This is **not** a print: it cannot see fusion,
  stringing, layer adhesion, elephant-foot or warp. The printed-in-practice
  journal/land behaviour remains a permanent qualitative risk.
- Land height tolerance ±0.20 mm and free-gap floors are stated assumptions.

## Remaining uncertainty / next test

- T11-B loaded engage/write/disengage dwell (analytic) and Step 6
  load/structure/power. If S3 is to be un-killed, the CTO's flat cost rejection
  should be re-read against the **0 bought per-channel selectors / ~$94 motor
  allowance** spec rather than the fallback-inflated number.
