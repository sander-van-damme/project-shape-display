# DND-58 — S5-R register reconciliation: corrected 1.00 mm rack pitch + sourced steel drive rod

## What changed

Applies the [DND-55] bank close-out corrections to the register definition
(residual **R-DND55-4**). Evidence classes [DND-27] permits only: **CAD +
CALCULATION; no print, no purchase, no measurement**.

- `06-experiments/test12_winner_convergence/s5r_register.scad` — rack re-dimensioned to
  **pitch 1.00 / tooth 0.50 mm**; drive bar rendered as a **round sourced steel rod
  Ø6 mm** (replaces the printed 3 × 2 placeholder).
- `s5r_register.py` — `RACK_TOOTH_PITCH_MM = 1.00`, `RACK_TOOTH_HEIGHT_MM = 0.50`,
  `RACK_STROKE_MM = 1.00` (was keyed to the 0.45 mm tooth height); `BAR_D_MM = 6.0`,
  `BAR_MATERIAL = "sourced steel rod"`; `timing()` reports `rack_stroke_mm` /
  `crank_deg_per_level`; `bom()` adds the rod line and retains the earlier totals.
- `s5r_register_checks.py` — 19 gates (adds DND-58 rack/rod/BOM gates + ADR gates).
- `s5r_bom_ratify.py` — reconcile now reads the rod-aware register fields; `--selftest`
  checks the +$3.00 rod delta.
- `07-evidence-and-decisions/dnd58-s5r-register-reconcile.md` — the ADR;
  `dnd54-s5r-register-latch.md` §11 amendment; `dnd55-s5r-bank-assembly.md` R-DND55-4
  closed; `08-current-design/README.md`, test12 `README.md` folded in.

> Branched from `main` (DND-54 / DND-55 / DND-56 present).

## Engineering question

Do the DND-55 corrections (rack pitch, drive-bar section) reconcile cleanly at the
register level — per-stroke advance, timing and BOM — without moving the 30 s verdict?

## Result

**Rack re-dimension (CALCULATION).** The DND-54 rack (0.60/0.45) left a 0.15 mm
inter-tooth gap that fuses at a 0.4 mm nozzle. Re-dimensioned to **1.00/0.50** (gap
0.50 mm). The per-stroke advance is re-derived from the **pitch**: `RACK_STROKE_MM =
1.00` (was `RACK_TOOTH_HEIGHT_MM = 0.45`).

**Timing unchanged.** The bank pass is *angular* — 72°/level — so the linear rack pitch
does not enter the timing: **24.62 s** full map (< 30 s, +5.39 s), select 0.400 s, reset
0.100 s per group.

**Drive bar (CALCULATION, inherited from DND-55).** Printed 3 × 2 placeholder skew
**4.96 mm** vs gate/2 = **0.175 mm** (~28×). Adopted the **sourced steel rod Ø6 mm**
(skew **0.0026 mm**, ~67× under the gate; Ø8 printed round bar is the fallback).

**BOM delta.** +1 steel rod Ø6 × 406.4 mm = **$3.00 parts → $3.48 delivered**. Honest
working total **$401.12 → $404.60 delivered** (margin **$95.40**). Both earlier figures
retained as `delivered_no_rod_usd` / `delivered_claim_usd`.

## Verdict

**R-DND55-4 closed.** R-DND54-4 remains closed for the bank envelopes/pitch and sharpened
to a sourced-steel-rod requirement (not a printed part). Not a print-ready claim, not
board contact.

## Assumptions / what passed / what is uncertain

- **Passed:** 19 register gates, 16 bank gates, 11 BOM-ratification gates, register
  printability, `s5r_bank.py --cad` (6 positives + 5 empty interference queries), and the
  full `validate_geometry.py` harness (real OpenSCAD + mesh) — all green.
- **Assumed:** the reaction eccentricity `e` (DND-55; irrelevant for the steel rod); the
  $3.00 rod allowance is a sourced-class figure, not a quote (purchase-gated under DND-27).
- **Uncertain:** as-printed friction / gate sharpness / leaf creep remain measurement-only,
  unchanged by this reconciliation.

## Most informative next test

Integrate the reconciled register + bank into the single `08-current-design` machine
definition (rack, steel rod, comber and carriage as one assembly), since the register unit
cell and the bank are now each CAD-closed but not yet joined.

[DND-27]: /DND/issues/DND-27
[DND-54]: /DND/issues/DND-54
[DND-55]: /DND/issues/DND-55
[DND-56]: /DND/issues/DND-56
