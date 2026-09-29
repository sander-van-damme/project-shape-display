# DND-121: correct the DND-115 shutter closure framing per the DND-118 falsifier audit (A5/A6/A7/A9)

## What changed

- **Model** `08-integrated-designs/a1-reliability-first/analysis/a1_writer_rate.py`:
  - `shutter_read_contrast()` adds the **state-invariant in-cone neighbour crosstalk term** to
    **both** states, and `contrast_passes` now **gates** the worst-case (crosstalk-included) ratio
    (**A5/A6**). The "off-beam" wording is removed; `absorber_in_dof` and its vacuous check are
    **dropped** (**A7**); `absorber_delta_z_mm` is retained for transparency only.
  - `shutter_tolerance_mc()` models the **aperture plane as its own frame feature** with an explicit
    `±0.10 mm` placement tolerance, so the `aperture_clearance` check is no longer pinned to the
    nominal vane top and can genuinely fail (**A9**).
- **Checks** `analysis/reliability_mask_checks.py`: DND-121 checks added (**78/78**).
- **Falsifier register** `07-evidence-and-decisions/falsifier_dnd115_a1_shutter_audit.py` + `.md`:
  attacks A5/A6/A7/A9 now assert the corrected state; the verdict is **CLEAN** (12/12) on the
  corrected artifacts.
- **CTO checker** `07-evidence-and-decisions/falsifier_dnd115_checks.py`: S3 gates the crosstalk
  term; S5 renamed to assert the weakly-in-cone / negligible-absorber facts (9/9).
- **ADR** `dnd115-a1-state-encoding-shutter.md`: §3/§3a/§5/§7/§8/§9 corrected; new §3a documents the
  A5/A6/A7 corrections.
- **CI** `.github/workflows/ci.yml`: the DND-118 audit step is **promoted from report to `--gate`**.
- **Docs**: `07-evidence-and-decisions/README.md` (DND-115 + DND-118 entries corrected, new DND-121
  entry) and `08-integrated-designs/a1-reliability-first/README.md` updated.

## Engineering question

Are the four over-claimed / structurally weak statements the DND-118 audit found (A5/A6/A7/A9)
corrected in the DND-115 ADR and model — with **no geometry change** — and does the independent
audit then reproduce CLEAN?

## Evidence produced (CALCULATION + CAD only)

- **A6 corrected:** the reader is a coaxial 15° cone; at the neighbour-top plane the cone radius is
  `4.8·tan15° = 1.286 mm` vs the `1.055 mm` near-edge offset → the neighbour is **inside the cone by
  0.231 mm**, i.e. **weakly in-cone**, not off-beam. Overlap of the neighbour footprint with the cone
  disc = **4.45% of the cone**, term `0.00154` vs vane term `0.24691`.
- **A5 corrected:** the term is added to both states and **gated**; on/off **7.72× ideal → 7.41×**
  (gate 2×). *Arithmetic note:* the first-pass audit quoted 6.37×, but that value did not reconcile
  with its own geometry (a "4.6% of the vane return" divisor gives 2.89×; its `0.008` term implies a
  0.184 mm² in-cone area, ~8× the 0.231 mm² strip it cited). DND-121 recomputes it **geometrically**.
- **A7 corrected:** the ±1 mm DoF is a *target* budget; the target (vane) is frame-fixed (`Δz = 0`)
  and the absorber term is **7.7×** below the vane term. The vacuous claim is **dropped**.
- **A9 corrected:** MC aperture plane modelled as its own feature (±0.10 mm) → worst aperture
  clearance **+0.441 mm** (was a tautological +0.610 mm); ±0.20 mm → **+0.355 mm**. Design passes;
  method now demonstrates it.
- **Unchanged geometry reproduced:** hidden occlusion 100%, visible 0%, frame-fixed target, sweep
  clearances 0.280 / 3.420 / 0.810 mm, min feature 0.44 mm, claim-5 (−0.190 mm infeasible / +0.610 mm
  feasible), angular robustness 0–20°.

## Assumptions

Assumption-class, unmeasured: flap reflectance 0.05, standoff 1.8 mm, aperture 0.44 mm, printed
tolerances, LED/PD constants. Measurement-only (DND-27): linkage force/friction/wear over 6,400
cycles. No print, purchase, or measurement; no board contact (DND-32).

## Tests / gates run

- `falsifier_dnd115_a1_shutter_audit.py --gate` → **exit 0, CLEAN (12/12)**.
- `falsifier_dnd115_checks.py --gate` → exit 0 (9/9); `falsifier_dnd114_checks.py --gate` → exit 0;
  `falsifier_dnd112_checks.py --gate` → exit 0; `falsifier_dnd104_checks.py` → exit 0.
- `reliability_mask_checks.py` → **78/78**; `a1_writer_rate.py` → exit 0.
- CI YAML updated: audit step is now a hard gate.

## What passed / failed

**Passed:** all four corrections independently re-verified on the corrected artifacts; the core
mechanism geometry is unchanged. **Failed:** nothing — the previous four FAILs are now resolved.

## Remaining uncertain / next test

Residuals remain assumption-class optical constants and measurement-only linkage force/friction/wear
(DND-27). No physical coupon is justified by this audit alone. If the program ever authorises a
coupon, the cheapest falsifier is a single printed A1 cell + frame vane + shutter + one LED/PD pair,
measured at 1.8 mm standoff, asserting on/off ≥ 2× — a physical handoff (DND-27).
