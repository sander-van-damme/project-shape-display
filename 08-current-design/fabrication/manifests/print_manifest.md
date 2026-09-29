# S5-R print manifest (DND-61)

**Evidence class: CAD + sourced limits + calculation. This is NOT a print and NOT a slicer run** ([DND-27](https://github.com/sander-van-damme/project-shape-display)); print times are labelled estimates.

Process: **Bambu X1C, PLA, 0.40 mm nozzle, 0.20 mm layers.** Sourced limits from `tools/fdm-limits/fdm_process_limits.py` (min feature 0.44 mm = 1 line; min wall 0.88 mm = 2 lines).

| Part | Qty | Material | Nozzle/Layer | Orientation | Supports | STL | Watertight | Bed | Est. mass | Est. time | Critical feature | Value | Sourced limit | Verdict |
|---|---:|---|---|---|---|---|---|---|---:|---|---:|---:|---|
| `cell_cartridge` | 9 | PLA | 0.4/0.20 | floor DOWN, cells open +Z; frame lip up | none (all walls vertical; bores vertical) | `cell_cartridge.stl` | True | True | 1577.44 (mesh) | 35.34 h | cell wall / pawl chamber (WALL) | 0.9 | 0.88 | **PASS** |
| `rotor` | 6400 | PLA | 0.4/0.20 | axis +Z (upright) | none (round, self-supporting) | `rotor.stl` | True | True | 236.18 (mesh) | 5.29 h | rotor core diameter (2 x 1.0) | 2.0 | 0.88 | **PASS** |
| `drive_pawl` | 6400 | PLA | 0.4/0.20 | cantilever Z, tip down; flat on its 0.70 face | none | `drive_pawl.stl` | True | True | 61.33 (mesh) | 1.37 h | pawl leaf thickness (PAWL_T) | 0.9 | 0.88 | **PASS** |
| `keeper` | 6400 | PLA | 0.4/0.20 | leaf upright; shoulder bearing DOWN | none | `keeper.stl` | True | True | 41.07 (mesh) | 0.92 h | keeper leaf thickness (KEEPER_T) | 0.9 | 0.88 | **PASS** |
| `detent_leaf` | 6400 | PLA | 0.4/0.20 | leaf upright, scallop toward rotor | none | `detent_leaf.stl` | True | True | 30.18 (mesh) | 0.68 h | detent leaf wall | 0.9 | 0.88 | **PASS** |
| `rack_strip` | 12 | PLA | 0.4/0.20 | teeth UP, base web DOWN | none (teeth on top) | `rack_strip.stl` | True | True | 13.78 (mesh) | 0.31 h | rack tooth gap (pitch - tooth) | 0.5 | 0.44 | **PASS** |
| `bank_drive_housing` | 1 | PLA | 0.4/0.20 | motor bosses horizontal, bed flat on the base | none (bores vertical in print orientation) | `bank_drive_housing.stl` | True | True | 58.61 (mesh) | 1.31 h | housing wall (60-2x11-... ) | 18.0 | 0.88 | **PASS** |
| `reset_comber` | 3 | PLA | 0.4/0.20 | body rail DOWN, tines +Z | none | `reset_comber.stl` | True | True | 2.22 (mesh) | 0.05 h | comber tine thickness | 0.9 | 0.88 | **PASS** |
| `writer_carriage` | 1 | PLA | 0.4/0.20 | pockets +Z, travels in X | none (pockets vertical) | `writer_carriage.stl` | True | True | 15.37 (mesh) | 0.34 h | carriage wall | 1.2 | 0.88 | **PASS** |
| `platen_module` | 9 | PLA | 0.4/0.20 | plate flat, ribs UP | none | `platen_module.stl` | True | True | 898.82 (mesh) | 20.13 h | stiffening rib width | 3.0 | 0.88 | **PASS** |
| `lift_frame_rail` | 16 | PLA | 0.4/0.20 | rail lengthwise on bed, pockets UP | none | `lift_frame_rail.stl` | True | True | 185.96 (mesh) | 4.17 h | rail wall / pocket wall | 6.0 | 0.88 | **PASS** |
| `guide_bracket` | 8 | PLA | 0.4/0.20 | bores horizontal, bracket on its back face | none | `guide_bracket.stl` | True | True | 5.71 (mesh) | 0.13 h | bracket wall (16-2x(4.2+... )) | 3.0 | 0.88 | **PASS** |
| `solenoid_mount` | 1 | PLA | 0.4/0.20 | pockets vertical | none | `solenoid_mount.stl` | True | True | 0.92 (mesh) | 0.02 h | pocket plate wall | 1.2 | 0.88 | **PASS** |
| `comber_cam` | 1 | PLA | 0.4/0.20 | axis +Z, flat | none | `comber_cam.stl` | True | True | 0.78 (mesh) | 0.02 h | cam web | 2.8 | 0.88 | **PASS** |

## Notes and honesty

- **No reduced witness blocks remain (DND-61).** Both structural tiles render at their TRUE size: `cell_cartridge` is the full 27x27 / 137.16 x 137.16 x 14 mm block and `platen_module` the full 27x27 / 137.16 x 137.16 x 7 mm plate, each a single watertight solid. If a board's useful bed is under 137.16 mm, a documented 3x3 sub-tile route (9x9 cells, 45.72 mm) is given in `scad/s5r_parts.scad` (`cell_cartridge_tile`) and the assembly manifest.
- Masses are the real committed-mesh solid volume (labelled `(mesh)`) times the part quantity; the tag names the volume source (`(mesh)` = trimesh signed volume of the committed STL, `(analytic)` = the analytic volume in `part_set.py`). Both are solid-fill upper bounds -- the sliced part is lighter.
- Print times are a volumetric estimate at ~11 mm^3/s; a real slicer preview will refine them. They are **not** a slicer run.
- **No part has been printed and none will be** ([DND-27](https://github.com/sander-van-damme/project-shape-display)).
