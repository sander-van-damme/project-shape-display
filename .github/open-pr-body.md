# DND-119: correct A5/A6/A7/A9 shutter claim-framing + gating (DND-118 audit; no geometry change)

## What changed

No CAD geometry change. The reflective target Δz stays 0. This repairs the four
claim-framing/method defects the DND-118 Falsifier found in the DND-115 shutter:

- **`a1_writer_rate.py` — `shutter_read_contrast()` (A5/A6):**
  - The neighbour return is now modelled **physically** (the in-cone crescent at the
    neighbour-top plane), not as the over-conservative whole-face body-area proxy. The old
    `2.589×` proxy is retained only as a labelled provenance field.
  - `contrast_passes` now **gates** it: requires `neighbour_crosstalk_gated`
    (physical ratio ≤ 1) and `on_off_return_ratio_with_crosstalk ≥ 2` (5.41×). The crosstalk is
    a margin, not a report — the same defect class DND-112 found in DND-111.
  - The false "off-beam" wording is replaced: the neighbour top is **weakly in-cone,
    state-invariant** (cone radius 1.286 mm vs 1.055 mm near-edge offset; in by 0.231 mm).
- **`a1_writer_rate.py` — `shutter_read_contrast()` (A7):** the "absorber Δz inside ±1 mm DoF"
  claim is downgraded to **provenance only**; the model verdict states it is **not counted as
  evidence** (the absorber term is 7.7× below the vane term). The real statements are "the
  reflective target is frame-fixed" and "the flap is a dark absorber".
- **`a1_writer_rate.py` — `shutter_tolerance_mc()` (A9):** the MC is de-tautologised. It now
  samples an **explicit reader/aperture-plane placement tolerance** (±0.10 mm; hostile
  ±0.20 mm) instead of pinning the aperture to the nominal vane top, so `aperture_clearance` can
  fail. `aperture_check_can_fail = True` records the fix.
- **`reliability_mask_checks.py`:** 3 new DND-119 checks (gated crosstalk, corrected on/off,
  provenance-only absorber) + 1 A9 check → **78/78**.
- **`falsifier_dnd115_checks.py`:** S5 relabelled to provenance; new S10 (crosstalk gated),
  S11 (neighbour in-cone, corrected on/off), S12 (MC aperture fail-able) → **12 attacks**.
- **`falsifier_dnd115_a1_shutter_audit.py`:** the four DND-118 attacks now assert the corrected
  state (A5/A6/A7/A9 PASS) → all **12 attacks PASS**.
- **ADR + both READMEs:** corrected wording and numbers; a DND-119 correction note added to the
  ADR and to the DND-118 audit register.
- **CI:** the DND-118 audit step is promoted from a report to a **hard gate** (`--gate`).

## Engineering question

Does the DND-115 state-encoding shutter still close the A1 read/verify axis at CAD + calculation
once the DND-118 findings are corrected — i.e. is the closure statement now honest and are the
gates real (able to fail)?

## Evidence produced (CALCULATION + CAD only)

- **A5:** physical in-cone neighbour/vane ratio **0.068** (≤ 1) is **gated** in `contrast_passes`.
- **A6:** neighbour near edge inside the 15° cone by **0.231 mm**; crosstalk-corrected on/off
  **5.41×** (> 2× gate). (This model's chord-area version is slightly more conservative than the
  Falsifier's ~4.6% estimate → 6.37×; both clear the gate.)
- **A7:** absorber term 0.032 vs vane term 0.247 → **7.7× smaller**; reported for provenance only.
- **A9:** worst sampled aperture clearance **+0.441 mm** nominal and **+0.336 mm** at ±0.20 mm
  reader placement — still positive, matching the Falsifier's independent +0.442 / +0.347 mm.
- Gate results: `falsifier_dnd115_checks.py --gate` **CLEAN (12/12)**;
  `falsifier_dnd115_a1_shutter_audit.py --gate` **CLEAN (12/12)**;
  `reliability_mask_checks.py` **78/78**; `falsifier_dnd114_checks.py --gate`,
  `falsifier_dnd112_checks.py --gate`, `a1_writer_rate.py` all exit 0.

## Assumptions

Assumption-class, unmeasured (as in DND-115): flap reflectance 0.05, standoff 1.8 mm, aperture
0.44 mm, printed tolerances, LED/PD optical constants. Measurement-only (DND-27): linkage
force/friction/wear over 6,400 cycles. No print, purchase, or measurement; no board contact
(DND-32). No CAD geometry change.

## Tests / gates run

```
python 08-integrated-designs/a1-reliability-first/analysis/a1_writer_rate.py
python 08-integrated-designs/a1-reliability-first/analysis/reliability_mask_checks.py
python 07-evidence-and-decisions/falsifier_dnd114_checks.py --gate
python 07-evidence-and-decisions/falsifier_dnd115_checks.py --gate
python 07-evidence-and-decisions/falsifier_dnd115_a1_shutter_audit.py --gate
```

## What passed / failed

All green. The mechanism is unchanged; only the claim framing, the crosstalk gate, and the MC
method are corrected.

## Remaining uncertain / next test

Residuals remain assumption-class optical constants and measurement-only linkage
force/friction/wear (DND-27). The DND-119 correction does not add new physical uncertainty. The
cheapest falsifier of the assumption-class reflectance combination remains a single-cell A1
coupon with a real LED/PD pair — a physical handoff (DND-27).
