# DND-88: "everything assembled" renders — full S5-R machine + S6-LC

The board asked ([DND-68](/DND/issues/DND-68) comment `430f2c19`): **"I also want images of
everything assembled."** The [DND-69](/DND/issues/DND-69) gallery showed only one 3 × 3 per-cell
register and single-part views; it did **not** show the whole machine, and the S6-LC low-cost
candidate had **zero** PNGs.

**Evidence class: CAD render of the committed OpenSCAD meshes. NOT a print and NOT a measurement**
([DND-27](/DND/issues/DND-27)). No part has been printed, purchased or measured. This PR visualises
geometry only.

## What this adds

### S5-R (promoted machine) — full machine assembled

New [`08-current-design/fabrication/tools/render_machine.py`](08-current-design/fabrication/tools/render_machine.py)
composes the **whole machine** from the committed part STLs at their real assembly offsets and
rasterizes it with the DND-69 software renderer (**imported, not forked**):

- the **3 × 3 cartridge field** (411.48 × 411.48 mm = the real 81 × 81 cell envelope; 80 × 80 =
  6,400 used);
- the **3 × 3 platen lift deck** under it;
- the perimeter **lift-frame rails** and corner **guide brackets**;
- three witness **rack strip + sourced steel rod** rows;
- the **bank drive housing** (−X edge) and the **writer carriage** (+X edge).

Views: iso / top / front → `assembly_full_machine_{iso,top,front}.png`.

A **documented installed-register 9 × 9 sub-block** (81 of the 6,400 cells, 45.72 × 45.72 mm) at
iso/top/front → `assembly_register_9x9_*.png`. The full 6,400 installed cells are **not**
individually modelled and every image label states the cell count it shows.

### S6-LC (low-cost exploration) — assembled machine

New [`09-low-cost-variant/s6lc/analysis/render_s6lc_images.py`](09-low-cost-variant/s6lc/analysis/render_s6lc_images.py)
rasterizes the committed S6-LC STLs into assembled iso/top/front views:

- the **8-bank field strip** (406.4 × 406.4 mm, 80 × 80 = 6,400 cells); each bank renders **3 of its
  10 rows** at true 5.08 mm pitch (stated on every label);
- the `s6lc_platen` broadcast deck, a per-bank `s6lc_gate` and a `s6lc_comb`;
- an installed representative column sub-block.

→ `09-low-cost-variant/s6lc/images/s6lc_machine_assembled_{iso,top,front}.png`.

### Reproducibility

Both tools regenerate headlessly and write machine-readable records
(`render_machine_record.json`, `s6lc/cad/render_images_record.json`). CI now regenerates and verifies
both sets (valid, non-blank PNG, real dimensions).

## Acceptance criteria

- [x] New full-machine assembled PNGs, valid and non-blank with real pixel dimensions.
- [x] READMEs link the new assembled images; labels distinguish **S5-R (promoted)** from
  **S6-LC (low-cost exploration)**.
- [x] Representative-sub-block renders explicitly labelled with the cell count shown.
- [x] Render tools + record JSON added and reproducible; existing coherence gates still green.
- [x] Evidence class stated: CAD render of committed meshes, not a print, not a measurement.

## Verification (run locally on this branch)

- `render_machine.py` + `--check` → PASS (6 images); `render_s6lc_images.py` + `--check` → PASS
  (3 images); `render_images.py --check` → PASS (45 images).
- `08-current-design/fabrication/tools/fab_package_checks.py` → **GATE: PASS**.
- `tools/validate/readme_s5r_coherence.py` → **GATE: PASS**.
- `09-low-cost-variant/s6lc/analysis/s6lc_checks.py` → 29/29 PASS.
- No design numbers changed; `08-current-design/` machine definition untouched.
