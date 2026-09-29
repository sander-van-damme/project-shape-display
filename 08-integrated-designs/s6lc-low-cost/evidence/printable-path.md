# S6-LC printable-path statement

**Evidence class: CAD + CALCULATION over sourced FDM limits. No print, no
measurement** ([DND-27](/DND/issues/DND-27)). This is the "what to print" scope
for the S6-LC ultra-low-cost machine; it is deliberately **separate from
[`08-integrated-designs/s5r-shared-drive-register/fabrication/`](../../../08-integrated-designs/s5r-shared-drive-register/fabrication/)****, which
belongs to S5-R and is not modified.

## 1. What is printed vs bought

Per [DND-70](/DND/issues/DND-70), the cost ceiling applies to **purchased parts
excluding 3D-printed parts**. S6-LC moves as much structure as possible into the
printed set:

| Printed (excluded from the cost ceiling) | Bought (counted in the <$250 BOM) |
|---|---|
| 6,400 columns with 5-pocket racks | 1 lift stepper |
| 6,400 pawls | 1 mask-index stepper |
| 8 bank mask gates + their media | 1 reset-carriage stepper |
| 8 bank release combs | 4 lead screws + nuts, belt + pulleys |
| frame, tiles, platen plate, carriage, brackets | controller, 3 drivers, PSU, loom, guides, fasteners, sensors |
| mask medium (printed comb or punched card) | — |

## 2. Print envelope

- **Printer/material:** Bambu Lab X1C, PLA, 0.4 mm nozzle, 0.2 mm layers
  (sourced process limits: `tools/fdm-limits/fdm_process_limits.py`).
- **Feature floor:** 0.44 mm = one extrusion line; 0.88 mm = two lines (robust).
- **Active area:** 406.4 × 406.4 mm. The 256 mm X1C bed does **not** fit a full
  406.4 mm row or bank, so the frame and the 80-wide bank are printed as
  **sub-tiles** (e.g. 4 tiles of 20 columns ≈ 101.6 mm) that bolt to a spliced
  frame. Column-level seams are handled by the same pitch budget below.
- **Orientation:** columns and pawls print flat/growing up as straight prisms
  (no supports); the frame grows up; the mask gate and release comb print flat.

## 3. Sourced-FDM-limit table (`analysis/printability_s6lc.py`)

| Feature | Value | Limit | Verdict |
|---|---:|---:|---|
| Column body | 3.60 mm | 0.88 (2 lines) | PASS |
| Inter-column lane | 1.48 mm | 0.44 (1 line) | PASS |
| Pawl leaf thickness | 0.90 mm | 0.44 | PASS |
| Pawl leaf width | 1.20 mm | 0.44 | PASS |
| Pawl + bleed in lane | 1.30 mm ≤ 1.48 | — | PASS |
| Gate + bleed in lane (stacked in Z) | 1.20 mm ≤ 1.48 | — | PASS |
| Rack pocket depth (X) | 0.80 mm | 0.44 | PASS |
| Rack pocket height (Z) | 3.00 mm | 0.20 | PASS |
| Release comb tooth | 0.88 mm | 0.44 | PASS |
| Mask boss | 0.88 mm | 0.44 | PASS |

**Overall: PASS** (no FAIL, no RISK). Record:
[`../cad/s6lc_printability_record.json`](../cad/s6lc_printability_record.json).

## 4. CAD evidence (real OpenSCAD)

`analysis/render_s6lc_cad.py` renders five parts with a real OpenSCAD and then
mesh-validates them with `trimesh`:

| Part | Faces | BBox (mm) | Watertight |
|---|---:|---|---|
| `s6lc_cell.stl` | 104 | 4.60 × 3.60 × 44.0 | yes |
| `s6lc_bank.stl` | 20,160 | 404.92 × 13.76 × 44.0 (3-row preview) | yes |
| `s6lc_gate.stl` | 972 | 406.4 × 2.0 × 2.2 | yes |
| `s6lc_comb.stl` | 1,612 | 406.4 × 2.4 × 2.0 | yes |
| `s6lc_platen.stl` | 12 | 406.4 × 50.8 × 2.0 | yes |

Record: [`../cad/s6lc_cad_record.json`](../cad/s6lc_cad_record.json).

## 5. Honest residual (measurement-only)

This statement is **CAD + calculation only**. The board performs the first
physical print. The measurement-only residue is: as-printed pawl release-force
spread (S1-D), friction μ, pocket sharpness, pawl creep, and platen flatness.
None is retirable under [DND-27](/DND/issues/DND-27).
