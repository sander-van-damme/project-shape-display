# DND-61 — Full-tile completion of the S5-R fabrication package

**Status:** closed — the S5-R fabrication package is now a slicer-ready print set
for every structural part (no reduced witness blocks).
**Owner:** Fabricator.
**Evidence class:** CAD (real OpenSCAD renders + mesh validation) + sourced FDM
process limits + calculation. **No print, no purchase, no measurement**
([DND-27](/DND/issues/DND-27)).

## The gap (from [DND-60](/DND/issues/DND-60) / [DND-57](/DND/issues/DND-57))

`08-current-design/fabrication/` shipped 14 rendered parts, but two structural
tiles were **reduced witness blocks**, not the real part geometry:

- `cell_cartridge.stl` — an **8 × 8 cell / 40.64 × 40.64 mm** witness of a
  **27 × 27 cell / 137.16 × 137.16 mm** cartridge.
- `platen_module.stl` — **labelled** a "27 × 27 witness" of the platen tile.

A board member could not slice these into the actual machine part, so the
package was an honest CAD witness but not yet a print set for the structural
tiles.

## What was actually true (CAD finding)

Measuring the committed STLs:

| part | committed bbox (mm) | verdict |
|---|---|---|
| `cell_cartridge` | 40.64 × 40.64 × 14.0 | **genuinely reduced** (8×8 cells) |
| `platen_module` | **137.16 × 137.16 × 7.0** | **already full geometry** — mislabelled, not reduced |

`platen_module` was never reduced: the module's defaults were already
`CARTRIDGE_COLS, CARTRIDGE_ROWS`. The witness label was a documentation error,
not a geometry gap.

## Fix

- **`scad/s5r_parts.scad`** — `cell_cartridge` now renders at
  `cell_cartridge(CARTRIDGE_COLS, CARTRIDGE_ROWS)`; `platen_module` renders
  explicitly at the full tile too. Both are committed as **single manifold
  solids**.
- **Full-tile cartridge render** is genuinely feasible: OpenSCAD 2023.09.11
  renders the 27 × 27 block to a watertight mesh in ~**10.5 min** (67,488
  triangles, 11.7 MB ASCII STL, bbox 137.16 × 137.16 × 14.0 mm). Reported
  `Simple: yes`, `Volumes: 2` (one solid + its internal void), trimesh
  `is_watertight = True`, `is_winding_consistent = True`. It fits the 256 mm
  X1C bed. No sub-tile split was required.
- **Documented sub-tile fallback** — `cell_cartridge_tile` (9 × 9 cells,
  45.72 × 45.72 mm; 9 per cartridge, 81 per field) with a `FRAME_RAIL` bolted
  lap and `SLOT_CLEAR = 0.15 mm` joint, for a board whose useful bed is under
  137.16 mm. This is a route, not a required step.
- **Real masses** — the mass line now uses the **real committed-mesh solid
  volume** (trimesh signed volume) for the tiles:
  - `cell_cartridge`: 141,347.5 mm³ × 1.24 g/cm³ ≈ **175.27 g** solid (each).
  - `platen_module`: 80,539.5 mm³ × 1.24 g/cm³ ≈ **99.87 g** solid (each).
  These remain solid-fill **upper bounds** (a sliced part is lighter), labelled
  `(mesh)`.
- **CI gate C7** (`tools/fab_package_checks.py`) — fails if any part's committed
  STL bbox does not equal its declared real envelope, or if a part is still a
  reduced witness without a documented sub-tile route. This makes the DND-60
  regression impossible to reintroduce silently.

## Residual

None added. The package was already CAD/calculation only; the DND-27
measurement-only residue (as-printed μ, leaf creep, per-set reliability, loaded
torque-speed) is unchanged. The full-tile render is a heavier CAD job
(~10.5 min/part) but is bounded and CI-runnable.
