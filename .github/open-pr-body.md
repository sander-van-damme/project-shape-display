## What changed

Closes the two conditional/open geometry killers on the S5 winner ([DND-44](/DND/issues/DND-44)) raised for [DND-45](/DND/issues/DND-45):

**K2 — detent repeatability at sourced friction.** Extended `detent_contact.py` with a
scallop-depth sweep (0.20 → 0.40 mm) inside the cam envelope (radius 1.5, core 1.0, max
step 0.50 mm), plus a finite-tip term. Named a geometry that passes at the sourced PLA–PLA
friction midpoint with a ≥ 1.25 margin.

**K9 — angular margin vs print tolerance.** New `k9_angular_margin.py` Monte-Carlo that
propagates the sourced ±0.05 mm FDM positional/dimensional tolerance through the
`toe_angle = atan2(toe_width/2, toe_x − center_x)` geometry and the level-count sweep.

Also: updated `DETENT_CONTACT.md`, added `K9_ANGULAR_MARGIN.md`, updated the K2/K9 rows in
`test12_winner_convergence/README.md`, `08-current-design/README.md`, `model.py`, and wired
both new gates into CI.

## Engineering question

1. Is there a scallop depth inside the cam envelope that makes the printed detent correct
   an 18° slipped step with a 25% margin at the sourced PLA–PLA friction midpoint μ = 0.35?
2. Does the ±0.05 mm FDM print tolerance eat the 5-level angular margin, and at how many
   levels does the margin actually go negative?

## Evidence produced (CALCULATION / MONTE-CARLO / CAD — no print, no measurement, [DND-27](/DND/issues/DND-27))

**K2.** Flank-tilt (wedge) decomposition reduces exactly to the existing flat baseline
`T_r/T_f = A·k/(μ·r)`; the finite-tip term is `sinc(k·β)`.

| Scallop depth | μ=0.20 | μ=0.35 | μ=0.50 | in envelope |
|---:|---:|---:|---:|:---:|
| 0.20 (nominal) | 1.613 | 0.922 ✗ | 0.645 ✗ | yes |
| 0.28 | 2.258 | 1.290 ✓ | 0.903 ✗ | yes |
| **0.40 (chosen)** | 3.226 | **1.843 ✓** | **1.290 ✓** | yes |

- Exact minimum depth for a 1.25 margin at μ = 0.35: **0.2712 mm**; at μ = 0.50: **0.3875 mm**.
- Chosen **0.40 mm** fits the 0.50 mm envelope (leaves 0.10 mm core wall). 0.55 mm is
  rejected as out-of-envelope.
- Conservative 8° blunt tip: exact minimum 0.2946 mm, still under 0.40 mm — not knife-edge.
- Chosen depth written to `test08 params.json` (`cam.detent_scallop_depth_mm`) → generated
  `results/parameters.scad`.

**K9** (200,000 draws, seed 20260928; bounded-uniform primary + Gaussian σ=0.05 conservative):

| Levels | nominal | bounded mean | bounded min | bounded P(<0) | Gaussian P(<0) |
|---:|---:|---:|---:|---:|---:|
| 4 | 21.50° | 14.53° | 10.76° | **0.00%** | **0.00%** |
| 5 | 12.50° | 5.52° | 1.72° | **0.00%** | **1.31%** |
| 6 | 6.50° | −0.47° | −4.28° | **65.6%** | **69.1%** |

- 5 levels keeps margin positive under the bounded tolerance reading but only ~1.7°
  worst-case; under a Gaussian tail it has a 1.3% failure probability.
- **6 levels fails outright; 4 levels is robust.**

## Assumptions

- ±0.05 mm is a sourced FDM positional/dimensional capability claim, not a measured
  distribution on these specific parts; both a bounded and a Gaussian interpretation are
  reported.
- The wedge model assumes the leaf force is radial; the finite-tip efficiency η = sinc(kβ)
  is a stated term, not measured.
- Existing model anchors (Test08/Test09) unchanged.

## What passed / failed

- **Passed:** K2 has a named geometry (0.40 mm) that clears 1.25 at μ = 0.35 (1.84) and
  μ = 0.50 (1.29) inside the envelope. K9 is bounded; 5 levels is conditionally safe,
  4 robust, 6 fails.
- **Failed / remains:** the as-printed μ, creep, tip sharpness, and the real tolerance
  distribution cannot be measured under DND-27, so K2's residual risk is print
  realisation; K9's residual is the real as-printed tolerance distribution.

## Checks run

- `detent_checks.py` (15 tests, +6 new), `k9_checks.py` (10 tests), `checks.py` (13 tests,
  killer labels updated), `model.py`, `ratify_bom.py --selftest`, `test08/checks.py`,
  `test09/run.py` — all green locally. CI adds both new gates.

## Next test

- Source or measure the as-printed scallop depth and tip geometry on a real part (gated by
  print authority); until then K2/K9 stay closed analytically only.
