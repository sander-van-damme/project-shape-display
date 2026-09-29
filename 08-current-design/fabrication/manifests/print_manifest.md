# S5-R print manifest (DND-60)

**Evidence class: CAD + sourced limits + calculation. This is NOT a print and NOT a slicer run** ([DND-27](https://github.com/sander-van-damme/project-shape-display)); print times are labelled estimates.

Process: **Bambu X1C, PLA, 0.40 mm nozzle, 0.20 mm layers.** Sourced limits from `tools/fdm-limits/fdm_process_limits.py` (min feature 0.44 mm = 1 line; min wall 0.88 mm = 2 lines).

| Part | Qty | Material | Nozzle/Layer | Orientation | Supports | STL | Watertight | Bed | Est. mass | Est. time | Critical feature | Value | Sourced limit | Verdict |
|---|---:|---|---|---|---|---|---|---|---:|---|---:|---:|---|
| `cell_cartridge` | 9 | PLA | 0.4/0.20 | floor DOWN, cells open +Z; frame lip up | none (all walls vertical; bores vertical) | `cell_cartridge.stl` | True | True | n/a (witness block) | estimate via STL volume at slice time | cell wall / pawl chamber (WALL) | 0.9 | 0.88 | **PASS** |
| `rotor` | 6400 | PLA | 0.4/0.20 | axis +Z (upright) | none (round, self-supporting) | `rotor.stl` | True | True | 236.85 | 5.31 h | rotor core diameter (2 x 1.0) | 2.0 | 0.88 | **PASS** |
| `drive_pawl` | 6400 | PLA | 0.4/0.20 | cantilever Z, tip down; flat on its 0.70 face | none | `drive_pawl.stl` | True | True | 61.33 | 1.37 h | pawl leaf thickness (PAWL_T) | 0.9 | 0.88 | **PASS** |
| `keeper` | 6400 | PLA | 0.4/0.20 | leaf upright; shoulder bearing DOWN | none | `keeper.stl` | True | True | 28.57 | 0.64 h | keeper leaf thickness (KEEPER_T) | 0.9 | 0.88 | **PASS** |
| `detent_leaf` | 6400 | PLA | 0.4/0.20 | leaf upright, scallop toward rotor | none | `detent_leaf.stl` | True | True | 30.0 | 0.67 h | detent leaf wall | 0.9 | 0.88 | **PASS** |
| `rack_strip` | 12 | PLA | 0.4/0.20 | teeth UP, base web DOWN | none (teeth on top) | `rack_strip.stl` | True | True | n/a (witness block) | estimate via STL volume at slice time | rack tooth gap (pitch - tooth) | 0.5 | 0.44 | **PASS** |
| `bank_drive_housing` | 1 | PLA | 0.4/0.20 | motor bosses horizontal, bed flat on the base | none (bores vertical in print orientation) | `bank_drive_housing.stl` | True | True | n/a (witness block) | estimate via STL volume at slice time | housing wall (60-2x11-... ) | 18.0 | 0.88 | **PASS** |
| `reset_comber` | 3 | PLA | 0.4/0.20 | body rail DOWN, tines +Z | none | `reset_comber.stl` | True | True | n/a (witness block) | estimate via STL volume at slice time | comber tine thickness | 0.9 | 0.88 | **PASS** |
| `writer_carriage` | 1 | PLA | 0.4/0.20 | pockets +Z, travels in X | none (pockets vertical) | `writer_carriage.stl` | True | True | n/a (witness block) | estimate via STL volume at slice time | carriage wall | 1.2 | 0.88 | **PASS** |
| `platen_module` | 9 | PLA | 0.4/0.20 | plate flat, ribs UP | none | `platen_module.stl` | True | True | n/a (witness block) | estimate via STL volume at slice time | stiffening rib width | 3.0 | 0.88 | **PASS** |
| `lift_frame_rail` | 16 | PLA | 0.4/0.20 | rail lengthwise on bed, pockets UP | none | `lift_frame_rail.stl` | True | True | n/a (witness block) | estimate via STL volume at slice time | rail wall / pocket wall | 6.0 | 0.88 | **PASS** |
| `guide_bracket` | 8 | PLA | 0.4/0.20 | bores horizontal, bracket on its back face | none | `guide_bracket.stl` | True | True | n/a (witness block) | estimate via STL volume at slice time | bracket wall (16-2x(4.2+... )) | 3.0 | 0.88 | **PASS** |
| `solenoid_mount` | 1 | PLA | 0.4/0.20 | pockets vertical | none | `solenoid_mount.stl` | True | True | n/a (witness block) | estimate via STL volume at slice time | pocket plate wall | 1.2 | 0.88 | **PASS** |
| `comber_cam` | 1 | PLA | 0.4/0.20 | axis +Z, flat | none | `comber_cam.stl` | True | True | n/a (witness block) | estimate via STL volume at slice time | cam web | 2.8 | 0.88 | **PASS** |

## Notes and honesty

- The `cell_cartridge` and `platen_module` STLs are **reduced witness blocks** (8x8 cells), not the full 27x27 tile: the geometry is periodic in the cell and a full-tile CGAL render is ~30x the practical budget. The full 137.16 x 137.16 mm footprint and the cell count are carried analytically (see `part_set.py`), exactly as `s5r_bank.scad` renders a reduced bank and covers the full span analytically.
- Masses for witness-block parts are `n/a` here; the rotor/pawl/keeper/detent masses use the analytic solid volume (a solid-fill upper bound).
- Print times are a volumetric estimate at ~11 mm^3/s; a real slicer preview will refine them. They are **not** a slicer run.
- **No part has been printed and none will be** ([DND-27](https://github.com/sander-van-damme/project-shape-display)).
