# SHA-12 T2 camera K2 verdict — T2 REJECTED, A7-V stays parked

> Status: K2 analytic test COMPLETE. T2 (overhead camera, zero motion) FAILS
> both kill lines. A7-V revisit path does NOT open.
> Evidence class: CALCULATION — exact shadow projection on the 80x80 grid +
> Lambertian contrast bounds. DND-27: no print, purchase, or measurement.
> Reproduce: `python 06-experiments/test17_t2_k2_camera/t2_k2.py --gate` (11/11).
> Source: [SHA-10 verdict](sha10-scan-costdown-verdict.md) (T2 advanced to
> analytic K2 only); task [SHA-12](/SHA/issues/SHA-12).

## Kill criteria (up front, per SHA-10/SHA-12)

| ID | Gate | Kill line |
|---|---|---|
| K2a occlusion | 0 occluded cells in either view on general terrain | any occluded cell kills |
| K2b contrast | >=2x on/off height contrast on 100% of cells, both angles | any cell below 2x kills |

PASS required both; either kills. Cheapest-rejecting analysis first: closed-form
shadow length before grid ray-march; occlusion (geometric impossibility) before
contrast (radiometric insufficiency).

## Geometry assumptions (nominal; swept)

- Pitch 5.08 mm, travel 40 mm (low top z=0, tall top z=40), 80x80 = 6400 cells,
  extent 406.4 mm, column top 4.8 mm (0.28 mm gap, gap-aware: rays through gaps
  credited as passing — a LOWER bound on occlusion; full-pitch boxes add more).
- Camera: pinhole, OV2640-class UXGA 1600x1200 (20.0 px/cell over the field).
- Top-down: vertical axis through array center; heights swept 500/700/1000 mm
  above low tops (nominal 700 mm).
- Oblique: axis 45 deg from vertical along +y; exact parallel shadow-rect
  projection (conservative: underestimates real pinhole occlusion) + one
  pinhole-oblique spot check at 900 mm slant range.
- Confidence: high for occlusion (closed-form projection; lens distortion/Bayer/
  noise unmodeled, none of which remove occlusion); medium-high for contrast
  (textbook Lambertian radiometry).

## Result 1 — occlusion (K2a: FAIL, both angles)

Closed form: 45-deg shadow length = 40 x tan(45 deg) = 40.0 mm = 7.87 pitches,
i.e. ~8 cells hidden behind each tall column — SHA-10's "~8 cells" CONFIRMED.

Grid counts (occluded low cells / 6400, gap-aware lower bound):

| Pattern | Oblique 45 (parallel bound) | Oblique 45 (pinhole, slant 900) | Top-down (500/700/1000 mm) |
|---|---|---|---|
| flat_low | 0 | — | 0 / 0 / 0 |
| single_tall_center | 8 | — | 0 / 0 / 0 |
| single_wall (full 80-col wall) | 640 | 640 | 0 / 0 / 0 |
| stripes (alternating rows) | 3200 | 3200 | 2640 / 2480 / 2158 |
| checker | 1600 | — | 2984 / 2828 / 2588 |
| random50 (seed 0) | 3128 | 3126 | 2517 / 2207 / 1747 |

Notes:

- The single-wall oblique count (640 = 8 rows x 80 cols) matches the closed
  form exactly. Pinhole spot check ~= parallel bound (perspective adds radial
  spread on top).
- Top-down is clean ONLY for flat/single-feature patterns (near-vertical
  center rays). General terrain hides 1700–3000 valley cells even top-down,
  because off-center chief rays are already oblique: at 700 mm height the edge
  chief ray tilts 16.2 deg (2.3-cell shadow) and the corner ray 22.3 deg
  (3.2-cell shadow); at 500 mm the corner shadow reaches 4.5 cells. "0 occluded"
  would require a telecentric lens or infinite working distance — a new,
  far more expensive optic outside the $11–18 T2 claim.
- K2a kill line (0 occluded) is missed by two to three orders of magnitude on
  every general-terrain pattern at both angles. This alone rejects T2.

## Result 2 — contrast (K2b: FAIL, top-down; moot oblique)

- Top-down: all column tops are coplanar-parallel Lambertian surfaces with the
  same albedo and normal, so under diffuse room light the tall/low brightness
  ratio is 1.00x — there is geometrically ~0 height cue. Best-case point light
  AT the camera (center field): 1.18x @ 500 mm, 1.13x @ 700 mm, 1.09x @ 1000 mm
  (inverse-square over the 40 mm height delta). Perspective size cue is 4–9%
  (0.8–1.7 px on a 20 px cell) — not a radiometric contrast, and it needs a
  calibrated absolute reference. Kill line needs >=2x: missed by ~2x margin.
- Gap/AO shading (the only other height-correlated top-down signal) lives in
  gap pixels (~5.5% of image area), is weakest at center where occlusion is
  best, and needs subpixel gap segmentation — not a per-cell 2x mechanism.
- Oblique: tall columns themselves are bright (side wall ~8x top area), but
  each wall projects onto image positions of the cells BEHIND it (correspondence
  ambiguous) while those cells are occluded (signal undefined, 0x). Single-view
  per-cell decode of 100% cells is geometrically impossible; two views still
  leave shadowed valleys ambiguous, and stereo/structured light is a new
  subsystem outside the T2 zero-motion single-camera claim.

## Comparison (ranges; confidence in parentheses)

| Dimension | A1 verify (record) | T2 camera (tested) |
|---|---|---|
| Verify subsystem | $12 reader, marginal scan $0 (high) | $11–18 camera (medium-low; now K2-killed) |
| Silent cells | 0, cell-local re-drive (calc) | 1700–3200 occluded on general terrain (high, this test) |
| Height contrast | contacting local read (proven-rate calc) | <=1.18x vs 2x kill line (medium-high) |
| Motion/disturbance | gantry traverse (counted) | zero (pass, irrelevant after K2 kill) |

## Verdict

**K2 FAIL → T2 REJECTED.** K2a fails by 10^2–10^3 cells on general terrain at
both angles; K2b fails by ~2x margin top-down and is geometrically moot
oblique. The failure is structural (single static view of a 40 mm-tall,
5.08 mm-pitch height field), not a tuning gap: no exposure, threshold, or
second-pose tweak inside the T2 claim restores 0-occlusion or 2x contrast.

**A7-V revisit path: CLOSED.** Per SHA-10, reopening needed T2 to pass K2 AND a
line-BOM reprice of A7 with margin. K2 failed, so no reprice question opens; no
follow-up issue created — the family stays parked, not queued. A1's $12 reader
and the $30.99 ceiling stand unchallenged.

## Residual uncertainty

- Nominal (not worst-case) gap 0.28 mm and binary 0/40 mm heights; mid-heights
  interpolate between the tested extremes. Full-pitch boxes and real lens
  distortion/Bayer/noise only worsen occlusion and contrast respectively.
- Contrast bounds assume monochrome matte PLA tops; colored/textured tops add
  albedo confounds, never height signal.
- Nothing here is physical validation (DND-27). S5-R, A1, S6-LC packages
  untouched; no CAD/BOM/procurement beyond this test per the task brief.
