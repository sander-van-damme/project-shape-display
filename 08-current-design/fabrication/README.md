# S5-R fabrication package (DND-61)

**This is the printable part set for the promoted S5-R machine** — the
shared-drive programmable rotary register (R = 4) — plus the print and assembly
manifests the board needs to physically print and build it.

**Evidence class: CAD (real OpenSCAD renders + mesh validation) + sourced FDM
process limits + calculation. It is NOT a print and NOT a measurement. No part
has been printed and none will be** ([DND-27](/DND/issues/DND-27)); the board
performs the first physical print ([DND-32](/DND/issues/DND-32)).

Machine definition and evidence: [`../README.md`](../README.md) and
[`../../07-evidence-and-decisions/`](../../07-evidence-and-decisions/).

---

## 1. What is in this directory

```
fabrication/
  scad/
    s5r_parts_common.scad   shared part constants (single source of truth)
    s5r_parts.scad          every distinct printed part (part= selector)
  stl/                      14 rendered, mesh-validated STLs (CAD witnesses)
  images/                   board-viewable PNG renders (DND-69/DND-88): 14 parts
                            + assembled/exploded register + full machine
  manifests/
    print_manifest.md/.csv/.json     per-part print manifest
    assembly_manifest.md/.csv        exploded assembly + fasteners + BOM
    render_record.json               the real-OpenSCAD render + mesh record
    render_images_record.json        the PNG render record (DND-69)
    render_machine_record.json       the full-machine PNG render record (DND-88)
  tools/
    part_set.py             the part list (drives everything below)
    render_fab_parts.py     render + mesh-validate the full set
    render_images.py        render board-viewable PNGs (DND-69)
    render_machine.py       render the whole machine assembled (DND-88)
    gen_manifests.py        generate the print + assembly manifests
    fab_package_checks.py   CI coherence gate (C1-C8)
```

## 2. How to print and build (board route)

1. **Read the print manifest:** [`manifests/print_manifest.md`](manifests/print_manifest.md).
   It gives, per printed part: quantity, material (PLA), nozzle (0.40 mm) /
   layer (0.20 mm), orientation, supports, the sourced FDM limit it satisfies,
   and an estimated mass and print time.
2. **Slice the STLs** in [`stl/`](stl/) with the manifest's orientation. The
   parts are **modular**: the 406.4 mm field is 3 × 3 cartridges of
   137.16 × 137.16 mm so every part fits the 256 mm X1C bed.
3. **Assemble per** [`manifests/assembly_manifest.md`](manifests/assembly_manifest.md):
   exploded ordering, fastener list, and the purchased BOM
   ($404.60 delivered working; [DND-56](/DND/issues/DND-56) ratified).

> **The STLs are the real printable parts (DND-61).** Every part is real
> OpenSCAD geometry, watertight, and fits the 256 mm bed. The two structural
> tiles render at their **true full size** — `cell_cartridge` is the real
> 27 × 27 / 137.16 × 137.16 × 14 mm block and `platen_module` the real
> 27 × 27 / 137.16 × 137.16 × 7 mm plate, each a single manifold solid. No
> reduced witness blocks remain. A documented 3 × 3 **sub-tile route**
> (45.72 mm tiles) is provided only as a fallback for a board whose useful bed
> is under 137.16 mm (see §5).

## 3. The printed part set

14 distinct printed parts, **25,661 pieces** for one machine at the 80 × 80
field and R = 4 bank. The four highest-count parts (rotor, pawl, keeper,
detent — 6,400 each) are the passive per-cell register; the rest are machine
structure, drive, and carriage parts. Full table: print manifest.

| Group | Parts |
|---|---|
| Per-cell register (×6400) | `rotor`, `drive_pawl`, `keeper`, `detent_leaf` |
| Field structure | `cell_cartridge` (×9), `platen_module` (×9), `lift_frame_rail` (×16), `guide_bracket` (×8) |
| Drive / bank | `rack_strip` (×12), `bank_drive_housing` (×1), `reset_comber` (×3), `comber_cam` (×1) |
| Writer | `writer_carriage` (×1), `solenoid_mount` (×1) |

## 4. Sourced printability — every part passes

Every critical printed feature is checked against the sourced FDM limits in
[`../../tools/fdm-limits/fdm_process_limits.py`](../../tools/fdm-limits/fdm_process_limits.py)
(min feature 0.44 mm = 1 line at a 0.4 mm nozzle; min robust wall 0.88 mm = 2
lines). The full-set printability gate
(`tools/validate/analytic_printability.py` on `scad/s5r_parts.scad`) reports
**PASS** — no FAIL, no RISK. In particular the DND-59 keeper re-profile (0.90 mm,
2 lines) and the DND-58 rack (1.00 / 0.50 mm, 0.50 mm printable gap) are carried
forward.

## 5. Honesty / residual uncertainty (measurement-only residue)

- **No reduced witness blocks (DND-61).** Both structural tiles render at their
  true full size as single manifold solids. `cell_cartridge` is a 27 × 27 /
  137.16 × 137.16 × 14 mm block (~67.5k triangles, ~10.5 min CGAL render);
  `platen_module` is a 27 × 27 / 137.16 × 137.16 × 7 mm plate. `fab_package_checks.py`
  **C7 fails if any part is a reduced witness without a declared real envelope
  or a documented sub-tile route**, so this cannot silently regress.
- **Purchased BOM reconciled to the promoted model (DND-65).** The assembly
  manifest's purchased-BOM table carries the **working** figures and the
  **$404.60 delivered** total (DND-54 allowance units + the block's own channels
  + the DND-58 sourced steel drive rod), equal to
  `s5r_register.bom(rows_in_bank=4)["delivered_usd"]`. The optimistic-sourced
  $387.18 and the superseded $388.10 header are shown only as explicitly labelled
  non-working references. `fab_package_checks.py` **C8 fails if the manifest BOM
  total contradicts the promoted model, if the steel-rod line is absent, or if
  $388.10 is headlined as working**, so this cannot silently regress.
- **Sub-tile fallback route.** If a board's useful bed is under 137.16 mm, the
  cartridge prints as a 3 × 3 set of `cell_cartridge_tile` parts (9 × 9 cells =
  45.72 × 45.72 mm each; 9 tiles per cartridge, 81 per field) bolted on the
  `FRAME_RAIL` lap with 0.15 mm joint clearance. This is a documented route, not
  a required step on a 256 mm X1C.
- **Mass / print time are estimates.** Mass is a solid-fill upper bound taken
  from the committed mesh volume (labelled `(mesh)`); print time is a volumetric
  estimate
  (~11 mm³/s), not a slicer preview.
- **What only a physical build can retire** (the DND-27 residue the board's own
  build/measure closes): as-printed PLA–PLA friction μ and scallop/tip sharpness
  (K2 class), printed-leaf creep/fatigue (K11 class), as-printed per-set keeper
  reliability q (R1 class), and the real loaded NEMA17 torque-speed curve
  (K6 class). These are named, bounded, and cannot be retired analytically.

## 6. Renders (DND-69 / DND-88)

Board-viewable PNGs of every part, the assembled register, and the **whole
machine assembled** are in [`images/`](images/) — see the
[image gallery](images/README.md) for the full-machine views, the installed
register sub-block, and a table of every part render.

- **Part renders:** one PNG per part (14) in `iso` / `front` / `top` views.
- **Assembly renders:** an assembled 3 × 3 cell cluster (rotor + pawl + keeper +
  detent on the rack strip + sourced steel rod) and an exploded view.
- **Full machine assembled (DND-88):** the 3 × 3 cartridge field + platen deck +
  frame rails + witness drive rows + bank housing + writer carriage, with the
  installed register shown in a documented representative 9 × 9 sub-block
  (**81 of the 6,400 cells** — labelled on every image). Generated by
  [`tools/render_machine.py`](tools/render_machine.py).
- **Generators:** [`tools/render_images.py`](tools/render_images.py) and
  [`tools/render_machine.py`](tools/render_machine.py), rasterizing the committed
  OpenSCAD STLs with a software renderer (the container has no GL for OpenSCAD's
  own PNG backend — see the [gallery notes](images/README.md)).
- **Evidence class: CAD render. NOT a print, NOT a measurement**
  ([DND-27](/DND/issues/DND-27)).

## 7. Reproduce (software only)

```sh
export PATH="$HOME/.local/bin:$PATH"   # rootless OpenSCAD (tools/openscad-install)
python 08-current-design/fabrication/tools/render_fab_parts.py
python 08-current-design/fabrication/tools/gen_manifests.py
python 08-current-design/fabrication/tools/fab_package_checks.py
python 08-current-design/fabrication/tools/render_images.py   # PNG renders (pip numpy pillow)
python 08-current-design/fabrication/tools/render_images.py --check
python tools/validate/analytic_printability.py \
      08-current-design/fabrication/scad/s5r_parts.scad
```

These run in CI (`engineering-checks` / `fab-package`) with a real OpenSCAD.
