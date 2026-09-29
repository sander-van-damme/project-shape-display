# DND-69: board-viewable renders of the S5-R parts + assembled register

Child of [DND-68](/DND/issues/DND-68). Adds **PNG renders** so a human can see the
current design without CAD tooling. Evidence class: **CAD render — not a print, not a
measurement** ([DND-27](/DND/issues/DND-27)).

## What this adds

- **`08-current-design/fabrication/images/`** — board-viewable renders:
  - **14 parts × 3 views** (`iso` / `front` / `top`) = 42 PNGs, one set per part in
    `tools/part_set.py`.
  - **3 assembly views**: an assembled 3 × 3 cell cluster (rotor + drive pawl + keeper +
    detent leaf on the rack strip with the sourced Ø6 steel rod) and an exploded view.
  - **`images/README.md`** gallery with the assembly + per-part tables embedded, so they
    render inline on GitHub.
- **`tools/render_images.py`** — regenerates the images headlessly, writes
  `manifests/render_images_record.json`, and supports `--check` (CI guard). No GL, no X,
  no OpenSCAD needed.
- **`scad/s5r_assembly.scad`** — assembled/exploded scene placement (mirrors the Python
  placement; adds **no** new part geometry).
- **CI** (`fab-package` job): regenerates + verifies the images.
- **Docs**: referenced from `08-current-design/README.md` §6a and
  `fabrication/README.md`.

## How the images are made (honest note)

The committed `stl/*.stl` are produced by **real OpenSCAD** (`render_fab_parts.py`) and
every PNG is rasterized from **those exact meshes**, so the images are true to the shipped
geometry. OpenSCAD's *own* PNG backend needs an OpenGL context; the agent container has
no display/GPU (`Can't create OffscreenView: Unable to obtain GL Context`), so
`render_images.py` uses a small software rasterizer (numpy + Pillow): z-buffered,
flat-Lambert shaded, deterministic camera. This is documented in the tool docstring and
the gallery README.

## Verification

- `render_images.py --check` → **PASS** (45 images present, valid PNG).
- `fab_package_checks.py` (C1–C8) → **GATE: PASS** (unchanged).
- `readme_s5r_coherence.py` → **GATE: PASS**.
- `analytic_printability.py` on the part set → **VERDICT: PASS**.
- `ci.yml` parses as valid YAML.

No part is printed or measured; a render validates nothing physical.
