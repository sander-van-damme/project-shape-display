# S5-R fabrication package (DND-60)

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
  manifests/
    print_manifest.md/.csv/.json     per-part print manifest
    assembly_manifest.md/.csv        exploded assembly + fasteners + BOM
    render_record.json               the real-OpenSCAD render + mesh record
  tools/
    part_set.py             the part list (drives everything below)
    render_fab_parts.py     render + mesh-validate the full set
    gen_manifests.py        generate the print + assembly manifests
    fab_package_checks.py   CI coherence gate (C1-C6)
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

> **The STLs are CAD witnesses, not yet board print files.** Every part is real
> OpenSCAD geometry, watertight, and fits the bed. Two parts (`cell_cartridge`,
> `platen_module`) are **reduced witness blocks** of a periodic tile (see §5);
> the full-tile footprint and cell count are carried analytically. This is
> stated plainly so the board is not surprised.

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

- **Reduced witness blocks.** `cell_cartridge` (8 × 8 cells) and `platen_module`
  (27 × 27) render reduced representatives because a full 729-cell CGAL render
  is ~30× the practical budget. The geometry is periodic in the cell; the full
  footprint, cell count and mass are carried analytically in `tools/part_set.py`.
  This mirrors the repo's existing `s5r_bank.scad` reduced-model precedent. The
  board's slicer will see the true part, so this is a CAD-witness simplification,
  not a fabrication gap.
- **Mass / print time are estimates.** Mass is a solid-fill upper bound from the
  analytic volume; print time is a volumetric estimate
  (~11 mm³/s), not a slicer preview.
- **What only a physical build can retire** (the DND-27 residue the board's own
  build/measure closes): as-printed PLA–PLA friction μ and scallop/tip sharpness
  (K2 class), printed-leaf creep/fatigue (K11 class), as-printed per-set keeper
  reliability q (R1 class), and the real loaded NEMA17 torque-speed curve
  (K6 class). These are named, bounded, and cannot be retired analytically.

## 6. Reproduce (software only)

```sh
export PATH="$HOME/.local/bin:$PATH"   # rootless OpenSCAD (tools/openscad-install)
python 08-current-design/fabrication/tools/render_fab_parts.py
python 08-current-design/fabrication/tools/gen_manifests.py
python 08-current-design/fabrication/tools/fab_package_checks.py
python tools/validate/analytic_printability.py \
      08-current-design/fabrication/scad/s5r_parts.scad
```

These run in CI (`engineering-checks` / `fab-package`) with a real OpenSCAD.
