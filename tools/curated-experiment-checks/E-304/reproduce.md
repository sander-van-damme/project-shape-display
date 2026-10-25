# Reproduce E-304

Run from the repository root. Python package versions are recorded in the print pack's `metadata/software.json`. CAD uses CadQuery, trimesh, manifold 3d, shapely and NumPy; calculations/review also use SciPy and Matplotlib. It does not require proprietary CAD. Bambu Studio 02.08.02.61 and its matching official `resources/` are external tools; their preset sources/hashes are in the build report.

```bash
python tools/curated-experiment-checks/E-304/analysis/calculate.py
python owner-print-tests/2026-10-25-guided-matrix-clutch/cad/generate.py
python owner-print-tests/2026-10-25-guided-matrix-clutch/scripts/check_geometry.py
python owner-print-tests/2026-10-25-guided-matrix-clutch/scripts/drawings.py
```

All dimensions are millimetres; force N, modulus MPa, torque Nmm. `cad/generate.py` is the parameter authority, not an independent approximate drawing. Mechanical-position STLs and STEP solids are in `tools/curated-experiment-checks/E-304/cad/`; bed-oriented component STLs are in the owner pack. `output-interface.step` is the new cup/neck/collar, while the final threaded screw STL unions that interface with the exact archived E-295 mesh. No newly approximated thread is substituted. `assembly-*.stl` are inspection assemblies, **not** print plates. Elastic assembly shapes use a linear beam deformation field and do not constitute nonlinear FEA.

Set `BAMBU_BIN`, `BAMBU_RESOURCES` and `E 304_SCRATCH` to local paths (scratch outside versioned deliverables). On a headless Linux installation, provide a working display such as Xvfb; GUI installation and runtime libraries are environment-specific.

```bash
python owner-print-tests/2026-10-25-guided-matrix-clutch/scripts/build_project.py \
  --bambu "$BAMBU_BIN" --resources "$BAMBU_RESOURCES" --scratch "$E 304_SCRATCH" \
  --stl owner-print-tests/2026-10-25-guided-matrix-clutch/components/plate.stl \
  --out owner-print-tests/2026-10-25-guided-matrix-clutch/guided-matrix-clutch.3mf
python owner-print-tests/2026-10-25-guided-matrix-clutch/scripts/review_project.py \
  --project owner-print-tests/2026-10-25-guided-matrix-clutch/guided-matrix-clutch.3mf \
  --report owner-print-tests/2026-10-25-guided-matrix-clutch/metadata/slicer-review.json \
  --atlas owner-print-tests/2026-10-25-guided-matrix-clutch/images/toolpath-atlas.svg
python owner-print-tests/2026-10-25-guided-matrix-clutch/scripts/review_project.py \
  --project "$E 304_SCRATCH/reopen/guided-matrix-clutch.3mf" \
  --report owner-print-tests/2026-10-25-guided-matrix-clutch/metadata/reopened-slicer-review.json
python tools/curated-experiment-checks/E-300/printing/compare_reslice.py \
  --project owner-print-tests/2026-10-25-guided-matrix-clutch/guided-matrix-clutch.3mf \
  --reopened "$E 304_SCRATCH/reopen/guided-matrix-clutch.3mf" \
  --out owner-print-tests/2026-10-25-guided-matrix-clutch/metadata/reslice-comparison.json
./repo check
```

The builder imports official printer, process, filament and machine-G-code presets, plus the historical E-295 saved settings. It calls the actual Bambu executable to slice/save, then reopens **only the saved 3MF**, without loading the external profiles, and reslices it. This is a Bambu command-line reopen/reslice, not a claimed manual GUI observation. The saved project contains embedded geometry, presets and toolpaths. Review parses its actual extrusion paths, checks all named objects and compares archived vertices with the delivered plate. Original/reopened G-code may differ in ordering or flow; the independent comparison reports material-footprint differences rather than hiding a changed hash.

Reproducible evidence:

- `analysis/results/*.csv`: section, force, flexure, torque and angular-profile sweeps.
- `model-checks.json`: the frame-element solver against an independent fixed-guided beam closed form and sampled actual row-core section properties.
- `metadata/geometry-review.json`:16 selector masks, intermediate motion, both drive directions, one blocked follower, one stalled output, permanent gear cycle, actual cone phase/offset/tilt sweep and a deliberately invalid interference control.
- `metadata/cone-phase-clearance.csv`: actual tessellated cone first-contact heights at 72 angles for nine specified offset/tilt cases, including deliberately adverse clearance corners. Offset is imposed at the cone, not a complete guide tolerance Monte Carlo simulation.
- `metadata/meshes.json`: watertightness, body counts, volume, bounds and source hashes. Sacrificial frame/screw scaffolds are explicit; they are excluded from the operating assembly.
- `metadata/*slicer-review.json`: saved settings, actual model paths, bores, layer continuity, island/bridge screens and slicer estimates. These are screens, not a guarantee of adhesion or functional fit.
- `images/`: actual mesh sections/exploded projection and actual G-code path drawings. One artifact per illustration; optional PNG previews stay outside the deliverable tree.

Do not call the absence of a detected collision a physical pass. The geometry threshold, intentional faceted cone contacts, unsupported-feature exceptions, print risks and unmeasured friction are stated in the verification record. The full 80×80 assembly and motor selection have intentionally not been generated.

For the focused human inspection figure, run `python owner-print-tests/2026-10-25-guided-matrix-clutch/scripts/detail_paths.py`. An optional `--preview-dir` keeps raster previews outside the repository. The delivered test remains DRAFT because the final path review found unresolved pin-wall gaps; reproducing a successful slice does not promote its status.
