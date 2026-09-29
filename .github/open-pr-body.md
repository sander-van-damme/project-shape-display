# DND-121: record the shutter crosstalk modelling-convention residual + fix the own-column clearance typo

## What changed

No geometry change, no numeric change to any gated result. Two small doc-accuracy fixes
on top of the merged DND-119 + DND-122/123 state:

- **Own-column clearance typo:** `3.41 mm → 3.42 mm` in the DND-115 ADR §2/§9 and both
  READMEs. The model's `sweep_z_min − TRAVEL = 43.420 − 40 = 3.42 mm`; 3.41 was a
  hand-typed slip.
- **Documented residual (`§3` of the ADR):** the crosstalk term `rho·A_nb/g_nb²` is an
  **area-scaled** quantity added to the **unit-area** vane proxy `rho/g_vane²`. The quoted
  `~4.6%` neighbour/vane ratio (equivalently `6.37×`) therefore depends on the area
  reference; a dimensionally consistent treatment scaling both sources by the detector's
  actual read-spot area gives `2.1%` and `6.78×`. Every convention leaves the on/off ratio
  far above the 2× gate, so no gate outcome or design decision changes — recorded as an
  evidence-class residual.

## Engineering question

Is the DND-115 crosstalk correction's quoted ratio sensitive to a modelling convention in
a way that should be disclosed, and are the ADR's quoted geometric margins exact?

## Evidence produced (CALCULATION + CAD only)

- Dimensionally consistent recompute: neighbour `ρ·A_nb/g_nb²`, vane `ρ·A_spot/g_vane²` →
  2.1% ratio, 6.78× on/off. Range across defensible references ≈ 2.9–6.8×, all ≫ 2×.
- Own-column clearance = 3.42 mm (model `sweep_z_min`).
- Audit A13 (parses the ADR against the live model) remains MATCH; all gates green.

## Assumptions

Assumption-class optical constants unchanged; no print/measurement (DND-27); no board
contact (DND-32).

## Tests / gates run

- `falsifier_dnd115_a1_shutter_audit.py --gate` → CLEAN (14/14).
- `falsifier_dnd115_checks.py --gate` → 12/12; `falsifier_dnd114_checks.py --gate` → 7/7;
  `falsifier_dnd112_checks.py --gate` → 11/11.
- `reliability_mask_checks.py` → 78/78; `a1_writer_rate.py` → exit 0.

## What passed / failed

**Passed:** doc accuracy restored; the convention residual is disclosed; nothing regressed.
**Failed:** nothing.

## Remaining uncertain / next test

The crosstalk term's absolute magnitude remains convention-sensitive (disclosed). No
physical coupon is justified. If ever authorised, a single printed A1 cell + vane +
shutter + one LED/PD pair measured at 1.8 mm standoff (assert on/off ≥ 2×) is the cheapest
falsifier — a physical handoff (DND-27).
