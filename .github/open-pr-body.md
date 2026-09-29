# DND-113: CTO response to the DND-112 read finding — A1 read mechanism correction

> **Stacked PR.** This branch is based on the DND-112 audit branch
> (`falsifier/dnd112-a1-rate-audit`, PR #88), which is based on the DND-111
> branch (`cto/dnd111-writer-rate-bound`, PR #87). Until #87 and #88 merge, the
> diff against `main` includes their commits. The **DND-113 delta** is the read
> mechanism correction described below.

## What changed

DND-113 responds to the DND-112 independent audit ([DND-112], PR #88), which
returned **NOT CLEAN (default-deny)** on the DND-111 *single-cell read* claim
while reproducing the *rate* bound.

- **Read model corrected** (`10-reliability-mask/analysis/a1_writer_rate.py`):
  `read_resolution_bound()` now reports the **state-dependent standoff** (up-state
  spot 3.072 mm; **down-state spot 24.508 mm = 4.824 pitches** at the 42 mm gap),
  the corrected **corner reach 4.081 mm**, the neighbour-edge threshold, and the
  **~441x** up-neighbour/down-pocket return ratio. `resolves_single_cell = False`
  for the as-drawn fixed-height, top-face reader, and
  `binding_read_limit = "state_dependent_standoff"`. The ±0.264 mm registration
  number is retained **only as up-state provenance**.
- **One new function answers question (a)** — `common_height_read_target()`:
  **no** existing A1 artifact reads a common-height target; a concrete fix is
  **proposed** (a reflective flag at the frame-anchored latch hinge, read at one
  standoff for both states), pending CAD.
- **Question (b) rate trade study** — `z_stroke_trade_study()`: a reader Z stroke
  per **cell** is rate-fatal (**5.4 cells/s, > 2,380 s cycle**); per **line**
  (refocus) costs **~29.8 s** and must be priced.
- **Bundled small fixes from the audit:** the stop-and-go **trapezoid** (T1:
  61.9 cells/s at 100 m/s², was 89.6 V-shaped) and the **per-line ramp** now
  priced into `full_cycle` (T3: honest 8-head cycle **18.278 s**, was the
  idealised 16.278 s; still < 30 s).
- **CAD corrected** (`10-reliability-mask/scad/a1_reader_head.scad`): the
  `CORNER_REACH = spot/2·√2` error is replaced with the true
  `√2·(BODY/2) + spot/2 = 4.081 mm`; the down-state ~24.5 mm cone and a schematic
  common-height flag are rendered; the render record now carries both spots.
- **ADR:** new
  [`07-evidence-and-decisions/dnd113-a1-read-mechanism.md`](07-evidence-and-decisions/dnd113-a1-read-mechanism.md);
  DND-111's ADR is banner-corrected on the read axis; README §4.2/§4.2a/§4.3/
  §4.7/§7/§10 updated; the criteria-of-record remains `02-design-criteria/`.
- **DND-112 checker re-baselined to the resolution** (the DND-93/97 convention):
  `falsifier_dnd112_checks.py --gate` now exits **0**, asserting the corrected
  state (R2 fixed, T1/T3 fixed, R1/R4/G2 carried). CI is wired to the `--gate`.

## Engineering question addressed

**Is A1's single-cell read claim sound?** The DND-112 audit says no, and DND-113
**accepts it**. The read is *state-dependent-standoff* bound, not registration
bound: a down cell is read at a ~42 mm gap, its ~24.5 mm spot is swamped ~441x by
up neighbours, so **a down cell reads up** — a silent wrong-cell failure that
defeats A1's readback/retry advantage. The rate bound is unaffected.

## Evidence produced (class: CALCULATION + CAD; no print, purchase or measurement — DND-27)

- `a1_writer_rate.py` report: down spot 24.508 mm / 4.824 pitches; corner reach
  4.081 mm; ratio 441.0; `resolves_single_cell=False`; Z trade study values.
- CAD render: `SPOT_DOWN_diameter=24.5077`,
  `CORNER_REACH_corrected=4.08148`, `down-state single-cell read resolvable:
  false` (watertight reader mesh).
- `reliability_mask_checks.py`: **60/60** pass (10 new DND-113 checks).
- `falsifier_dnd112_checks.py --gate`: **exit 0**, 11/11 attacks assert the
  resolution.
- `falsifier_dnd104_checks.py`: 26/26 (unchanged).

## Assumptions / uncertainty

- All optical constants (5 mW LED, 0.45 A/W, 0.80/0.15 reflectance, 15°
  half-angle, 2 mm aperture/gap, TIA noise) remain assumption/sourced-class. They
  are **not** the deciding numbers for R1/G2 — those are geometric.
- The **common-height read target is PROPOSED, not validated**: it needs a CAD
  model, a flag-vs-neighbour contrast check, and a hinge-arc Δz-in-DoF bound.
- The **read/verify axis is UNRESOLVED**; DND-110's "SUCCESS-eligible on the rate
  axis" must **not** extend to it.

## Most informative next test

CAD-design and validate the proposed **latch-hinge read flag** (common-height
target), then re-check R1/G2 against it. If that fails, re-run the per-line Z
refocus trade study against the full cycle. Both are CALCULATION + CAD; no print
(DND-27).

## Passed / failed

- **Passed:** rate bound (18.278 s < 30 s at 8 heads); CAD watertight; 60/60
  checks; DND-112 `--gate` clean; DND-104 26/26.
- **Failed / carried:** the as-drawn single-cell read (accepted as the audit's
  finding; carried as the state-dependent-standoff residual).
