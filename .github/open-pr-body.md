# DND-61: full-tile S5-R structural tiles — remove reduced witness blocks

Recover and land the full-tile geometry that the dead Fabricator run produced
but never committed, so the S5-R fabrication package is a slicer-ready print set
for every structural part ([DND-61](/DND/issues/DND-61)).

**Evidence class:** CAD (real OpenSCAD render + mesh validation) + sourced FDM
process limits + calculation. **No print, no purchase, no measurement**
([DND-27](/DND/issues/DND-27)).

## Engineering question

Was the S5-R "printable package" actually printable for its two structural
tiles, or did it still ship reduced witness blocks that the board cannot slice?

**Answer:** the committed `platen_module` was already full geometry (a
documentation mislabel); `cell_cartridge` was a genuinely reduced 8×8 witness.
This PR replaces the cartridge with the true 27×27 full-tile solid and adds a
gate so the regression cannot return silently.

## What changed

- `scad/s5r_parts.scad` — `cell_cartridge`/`platen_module` render at the full
  `CARTRIDGE_COLS × CARTRIDGE_ROWS`; documented 9×9 / 45.72 mm sub-tile route
  (`cell_cartridge_tile`) for a bed under 137.16 mm.
- `stl/cell_cartridge.stl` — restored the true full-tile render: **11,726,140
  bytes, 67,488 tris, bbox 137.16 × 137.16 × 14.0 mm, watertight,
  winding-consistent**, matching `render_record.json`. (The other 13 STLs are
  unchanged; the platen mesh is byte-identical to `main` in content.)
- `tools/fab_package_checks.py` — new **C7** gate: fail if a committed STL bbox
  ≠ its declared real envelope, or a reduced witness lacks a documented route.
- `tools/gen_manifests.py` — mass/time from the real committed mesh volume
  (trimesh signed volume), tagged `(mesh)`; sub-tile route section in the
  assembly manifest.
- `tools/part_set.py` — `witness_of` / `subtile_route` fields; true full-tile notes.
- `tools/render_fab_parts.py`, `tools/validate/validate_geometry.py` — 30-min
  render budget for the ~10.5 min full-tile CGAL render.
- `.github/workflows/ci.yml` — `fab-package` gate C1–C7.
- `README`s + `07-evidence-and-decisions/dnd61-full-tile-completion.md` —
  document the completion and the measurement-only residual.

## Evidence produced (local, on the recoverable render)

| check | result |
|---|---|
| `gen_manifests.py` | idempotent; manifests reflect full-tile mesh |
| `fab_package_checks.py` | **GATE: PASS (C1–C7)** |
| `analytic_printability.py --fail-on-design-fail` | **VERDICT PASS** |
| `cell_cartridge.stl` trimesh | watertight, winding-consistent, 67,488 tris, 137.16 × 137.16 × 14.0 mm |

## Assumptions / uncertainty

- The full-tile render is a heavier CAD job (~10.5 min/part); CI `fab-package`
  re-renders it from source with a 30-min budget.
- Mass/print time remain solid-fill **upper bounds** (CAD, not a slicer run).
- No physical part exists; the DND-27 measurement-only residue (as-printed μ,
  leaf creep, per-set reliability, loaded torque-speed) is unchanged.

## Most informative next test

CI `fab-package` on this PR re-renders the full 27×27 cartridge from source and
runs C1–C7 — it is the discriminating test that the recovery is reproducible,
not just a copied artifact.
