# DND-114: CAD-design + validate the A1 common-height read target (latch-hinge flag)

## What changed

[DND-113](/DND/issues/DND-113) left the A1 **read/verify axis UNRESOLVED**: the
as-drawn reader targets the **column top face**, which moves `TRAVEL = 40 mm`
with the state, so a down cell is read at a ~42 mm gap with a ~24.5 mm spot
(4.82 pitches) swamped ~441× by up neighbours — a **silent wrong-cell failure**
that defeats A1's readback/retry reliability advantage. DND-114 turns the DND-113
**PROPOSED** common-height target into a **CAD-validated artifact**.

- **Cell CAD** (`10-reliability-mask/scad/a1_binary_latch_cell.scad`): a
  parameterised common-height flag. **CH-A (adopted)** — a frame-fixed reflective
  vane on the frame cradle in the latch lane, top face at
  `z = TRAVEL + 3 = 43 mm`; because the cradle is frame-anchored, the target z
  does **not** move with the column, so **Δz = 0 by construction** for both
  states. **CH-B (fallback)** — an arm-carried flag at radius `r` whose mean z
  shifts by the hinge arc. New `part="flag"` printable selector and self-checks.
- **Reader CAD** (`10-reliability-mask/scad/a1_reader_head.scad`): the flag is
  read at **one fixed standoff** (1.0 mm, dedicated 0.60 mm aperture); the
  schematic DND-113 flag is replaced by the real target + `flag_reader_head()`,
  with flag-vs-neighbour self-checks.
- **Model** (`10-reliability-mask/analysis/a1_writer_rate.py`):
  `common_height_read_target()` now reports the **adopted** CH-A target (Δz=0)
  and the CH-B bound; new `flag_read_contrast()` computes the fixed-standoff
  geometry; `read_resolution_bound()` records both the as-drawn defect and
  `resolves_single_cell_with_common_height_target = True`.
- **Render** (`10-reliability-mask/analysis/render_a1_cad.py`): renders +
  mesh-validates the `flag` part and **fails hard** if the common-height checks
  do not pass.
- **Docs:** new ADR
  [`07-evidence-and-decisions/dnd114-a1-common-height-read-target.md`](https://github.com/sander-van-damme/project-shape-display/blob/main/07-evidence-and-decisions/dnd114-a1-common-height-read-target.md);
  README §4.2a / §4.7 / §7 / §9 / §10 and the evidence index updated from
  "proposed" to "adopted + CAD-validated".
- **Gate/CI:** new
  [`falsifier_dnd114_checks.py`](https://github.com/sander-van-damme/project-shape-display/blob/main/07-evidence-and-decisions/falsifier_dnd114_checks.py)
  (7 attacks, `--gate` exits 0), CI-wired; the DND-113
  `reliability_mask_checks.py` "no artifact" check is superseded by DND-114
  checks (64/64 pass).

## Engineering question addressed

Can A1 read a **single cell at one fixed standoff for both states**, removing the
state-dependent-standoff defect that DND-112/DND-113 identified?

## Evidence produced (CALCULATION + CAD — no print, no purchase, no measurement; DND-27)

| Item | Value | Check |
|---|---:|---|
| CH-A target | frame-fixed vane, top z = 43 mm | **Δz = 0.000 mm** |
| CH-B hinge-arc Δz (r = 1.20 mm, 30° swing) | 0.621 mm | inside the ±1.0 mm DoF |
| Max CH-B radius in DoF | 1.932 mm | `DoF / (2·sin15°)` |
| Flag-read spot (a = 0.60 mm, g = 1.0 mm) | 1.136 mm | — |
| Spot X half-width vs neighbour clearance | 0.568 vs 1.055 mm | **PASS**, margin 0.487 mm |
| Spot vs flag Y width | 1.136 vs 1.60 mm | **PASS** |
| R1/G2 re-check | fixed standoff | 42 mm gap / 24.5 mm spot / 441× ratio **eliminated** |

- Watertight meshes rendered by **real OpenSCAD + trimesh validation**
  (`flag.stl` 0.44 × 1.6 × 0.82 mm; reader head re-rendered).
- `falsifier_dnd114_checks.py --gate` exits 0; the DND-112 gate and the
  reliability-mask regression suite (64/64) still pass.

## Assumptions

- Latch toggle swing 30° (assumption-class); flag-read aperture 0.60 mm and
  standoff 1.0 mm (assumption-class); all optical/device constants unchanged
  (assumption-class).

## What passed / failed

- **Passed:** CH-A Δz=0; CH-B Δz-in-DoF; flag fits the lane in X; flag spot
  clears the neighbour body; flag spot fits the flag footprint; the as-drawn
  top-face defect is still recorded (not erased).
- **Failed:** the naive reuse of the 2.0 mm top-face aperture at the flag does
  **not** clear the neighbour (2.54 mm spot > 2.11 mm lane) — hence the dedicated
  0.60 mm flag-read aperture. This is captured in the CAD self-checks.

## What remains uncertain

- The **state-encoding shutter** geometry (how the latch arm's silhouette
  modulates the CH-A vane) is identified but not yet dimensioned — a bounded CAD
  detail, not a physics risk.
- The flag standoff/aperture are assumption-class; no physical validation (DND-27).
- The ±0.264 mm gantry registration is now a **secondary** concern, not the
  binding read limit.

## Most informative next test

Dimension the **state-encoding shutter** in the cell CAD (arm silhouette vs the
CH-A vane at the fixed standoff) and confirm the binary bright/dark contrast
margin at 1.0 mm — still CALCULATION + CAD only (DND-27).

## Cross-references

- Parent: [DND-113](/DND/issues/DND-113), PR #89 (read-mechanism correction).
- Program: [DND-102](/DND/issues/DND-102); gate: [DND-110](/DND/issues/DND-110).
- Evidence class: CALCULATION + CAD only; no print/purchase/measurement
  ([DND-27](/DND/issues/DND-27)); no board contact ([DND-32](/DND/issues/DND-32)).
