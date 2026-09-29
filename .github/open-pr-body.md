# DND-121: crosstalk-normalization fix + A13 self-enforcement for the DND-115 shutter

## What changed

No CAD geometry change (reflective target Δz stays 0). This resolves the residual
[DND-122](/DND/issues/DND-122) A13 finding and hardens the crosstalk model.

- **Area-consistent crosstalk normalization (A13 root cause).** DND-119 added
  `rho · A_nb / g_nb²` (an area-scaled term) to `rho / g_vane²` (a unit-area proxy)
  — a dimensional mismatch, so the corrected on/off depended on an arbitrary area
  reference. DND-121 scales the neighbour and the vane by their **actual
  illuminated areas** (the read-spot area the detector integrates). The crosstalk
  ratio becomes a dimensionless, convention-invariant **2.1%** of the vane return;
  the corrected on/off is **6.78×** (gate 2×).
- **A14 hardening.** `shutter_tolerance_mc()`'s on/off check now carries the same
  state-invariant crosstalk term as `contrast_passes` (worst MC on/off **4.18×**),
  so the stack-up gates the quantity the ADR quotes.
- **A13 attack added.** The independent audit now **parses the ADR** and asserts
  every decisive quoted figure equals the live `shutter_read_contrast()` /
  `shutter_tolerance_mc()` output. The "stated a number no artifact supports"
  defect class (DND-112/DND-111) can no longer recur silently.
- **Stale margins fixed to model values:** own-column clearance `3.41 → 3.42 mm`;
  ±0.20 mm aperture clearance `+0.325 → +0.425 mm`; MC on/off `4.48 → 4.18×`;
  on/off incl. crosstalk `6.37 → 6.78×`; neighbour crosstalk `4.6% → 2.1%`.

## Engineering question

Was the DND-119 crosstalk correction (a) dimensionally consistent with the model's
photometric proxy, and (b) are the ADR/README numbers demonstrably the model's own
output — closing the DND-122 A13 finding?

## Evidence produced (CALCULATION + CAD only)

- **Normalization:** neighbour return `ρ·A_nb/g_nb²`, vane return `ρ·A_spot/g_vane²`,
  flap return `ρ_flap·A_spot/g_flap²`. Ratio `2.1%`; on/off **6.78×**. Independent
  audit A5 recomputes the same ratio (0.0210). The read axis is off-centre at
  `hinge_x = 2.225 mm`, so only the +x neighbour is in-cone — the single-neighbour
  worst case is correct.
- **A13:** the audit parses `dnd115-a1-state-encoding-shutter.md` §2/§3/§5 and
  asserts each quoted figure against the live model (MATCH).
- **Unchanged geometry reproduced:** hidden occlusion 100%, visible 0%, frame-fixed
  target, sweep clearances 0.280 / 3.420 / 0.810 mm, in-cone crescent 0.2311 mm²
  (4.45% of the cone), claim-5 (−0.190 mm infeasible / +0.610 mm feasible).

## Assumptions

Assumption-class, unmeasured: flap reflectance 0.05, standoff 1.8 mm, aperture
0.44 mm, printed tolerances, LED/PD optical constants. The neighbour is modelled as
a bright (up-state) Lambertian patch — the worst case. Measurement-only (DND-27):
linkage force/friction/wear. No print, no measurement, no board contact (DND-32).

## Tests / gates run

- `falsifier_dnd115_a1_shutter_audit.py --gate` → **exit 0, CLEAN (13/13)** incl. A13.
- `falsifier_dnd115_checks.py --gate` → exit 0 (12/12).
- `falsifier_dnd114_checks.py --gate` → exit 0; `falsifier_dnd112_checks.py --gate` → exit 0;
  `falsifier_dnd104_checks.py` → exit 0.
- `reliability_mask_checks.py` → **80/80**; `a1_writer_rate.py` → exit 0;
  `reliability_mask.py convergence` → exit 0; `make_table.py` → exit 0.
- CI hard-gates the audit step.

## What passed / failed

**Passed:** the A13 residual is closed; the crosstalk normalization is now
area-consistent and self-checked; all gates green. **Failed:** nothing.

## Remaining uncertain / next test

Residuals remain assumption-class optical constants and measurement-only
linkage wear (DND-27). No physical coupon is justified by this correction. The
cheapest falsifier, if ever authorised, is a single printed A1 cell + vane +
shutter + one LED/PD pair measured at 1.8 mm standoff asserting on/off ≥ 2×
(physical handoff, DND-27).
