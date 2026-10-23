# E-303 print-pack verification

2026-10-23. **Physical test not performed.** The package is DEFERRED only because three other READY offers already exist. No existing offer was retired or modified.

## CAD, configuration and actual slicing

- Parametric source: [cad/rig.py](cad/rig.py), CadQuery2.7.0, seven watertight component meshes plus a plate mesh. Plate bounds93.499 ×78 ×5 mm; source volume6808.49 mm³. The two nominal followers have identical untransformed geometry. Ring dimensions OD/ID4.7/2.4 and10/5.4 mm; guide bores2.2/2.3/2.3/2.4 mm. No support-dependent overhang, thread, inaccessible cavity or tall slender part is designed.
- Real executable: **Bambu Studio02.08.02.61**, official [Ubuntu22.04 release asset](https://github.com/bambulab/BambuStudio/releases/tag/v02.08.02.61), extracted into untracked runtime scratch. Missing Linux runtime libraries were extracted locally; no system configuration or printer connection was used.
- The project builder resolved the official **Bambu Lab X1 Carbon0.4 nozzle**, **Generic PLA** and **0.16mm Optimal @BBL X1C** presets and explicitly overrode the fixture settings listed in [test.md](test.md). It embeds the seven meshes, fixed plate placement, X1C start/end code, material and full process settings in the saved Bambu project.
- Actual Bambu CLI slicing saved [clutch-friction-screen.3mf](clutch-friction-screen.3mf). The saved project was independently reopened by Bambu Studio CLI with a fresh data directory and **without loading outside presets**, then resliced and exported. This is an actual Bambu save/reopen/reslice, not a geometry-only ZIP masquerading as a configured project. Graphical UI display was unavailable; CLI reported display-initialization warnings but both slicing/export calls returned success and valid G-code. Review used that G-code independently.
- Initial estimate: **8.52 g,1 h19 min1 s total**; reopened estimate **8.52 g,1 h19 min5 s**. Model-only time1 h6 min41/45 s.31 layers. No physical timing or consumed filament is claimed.
- Every project-setting value was preserved on reopen. The G-codes are **not byte-identical**. They differ in short toolpath/seam ordering and a four-second estimate; the unrounded filament-length estimates differ by0.09 mm. Independent feature checks were run separately on both archives rather than asserting identical files.

Evidence: [build/reopen provenance](metadata/build-and-reopen.json), [initial review](metadata/slice-review.json), [reopened review](metadata/slice-review-reopened.json), [all saved settings](metadata/saved-settings.json), [CAD dimensions](metadata/geometry.json), [part layout](metadata/layout.json). Reopened binary remains reproducible scratch, not a second redundant owner project.

## Independent checks and inspected toolpaths

[Review script](scripts/review_slice.py) checks source-vs-project meshes, actual nominal deposited line footprints and critical functions:

| Check | Initial and reopened result |
|---|---|
| Embedded components | Seven; correct X1C/0.4-mm selected |
| Source mesh preservation | Maximum bidirectional vertex deviation<0.000018 mm after rigid placement |
| Startup temperatures / archive integrity | Actual pre-layer M109 S210 / M190 S55; X1-0.4 start marker and ZIP CRC valid |
| Supports | None enabled; no support extrusion paths |
| Layer continuity | No newly unsupported disconnected deposited islands in any component |
| Central guide bores | Nominal1.0-mm-radius core remains open on every printed layer |
| Small contact ring | Interior annular-band coverage100% on every contact-ring layer checked |
| Large contact ring | Interior annular-band coverage≥99.85% on checked layers |
| Followers | Both eyelet cores open through body; cup center empty above body; cup-wall band continuous |
| Bed contact | Base~775 mm²; each input~368 mm²; followers~481 mm²; flat orientation, no raft/brim |

[Actual path illustration](images/toolpaths.svg) shows the small/large contact rings, open base bore and load cup. The algorithm uses slicer-reported line widths and a0.01-mm overlap allowance. It establishes nominal continuity, not measured deposited bead width, face flatness, fitting yield, bed adhesion or strength. The top nominal CAD heights are rounded to layer planes (input4.04, follower4.52 mm in sliced output). These small thickness variations do not license a precision axial-preload claim.

The fixture has **no threaded part**. Its critical features are the contact annuli, guide bores, balanced arm/eyelets, and cup. Avoiding thread recreation is deliberate: E-295 screw torque must be measured separately. Two nominal samples reveal only within-plate variation; they do not qualify6,400 clutches.

## Reproduce

From repository root, with dependencies installed and the official executable/resources available:

```sh
python owner-print-tests/2026-10-23-clutch-friction-screen/cad/rig.py
python owner-print-tests/2026-10-23-clutch-friction-screen/scripts/build_project.py \
  --bambu /path/to/bambu-studio \
  --resources /path/to/BambuStudio/resources \
  --scratch work/e303-print-rebuild
python owner-print-tests/2026-10-23-clutch-friction-screen/scripts/review_slice.py \
  owner-print-tests/2026-10-23-clutch-friction-screen/clutch-friction-screen.3mf \
  owner-print-tests/2026-10-23-clutch-friction-screen/metadata/slice-review.json --plot
python owner-print-tests/2026-10-23-clutch-friction-screen/scripts/review_slice.py \
  work/e303-print-rebuild/reopen/clutch-friction-screen.3mf \
  owner-print-tests/2026-10-23-clutch-friction-screen/metadata/slice-review-reopened.json
```

Python requirements: CadQuery2.7, NumPy, trimesh, SciPy, Shapely, matplotlib. `build_project.py` reuses the repository's official-preset resolver; `review_slice.py` reuses its G-code parser. Runtime binaries and temporary logs belong in `work/`, not the print pack. No machine-specific absolute runtime path is stored in source.

## What remains unresolved

Real print fit/flatness, washer burrs and eccentricity, adhesive thickness/creep, PET attachment, guide wedging, instrument resolution, static/dynamic friction, wear and repeatability are all unknown. Gauge-side load can cause journal drag or tilt; the protocol preserves raw readings, uses conservative interpretations and requires an inconclusive result where sensitivity is inadequate. The rotor's mass produces a known-after-weighing nonzero OFF-proxy preload. This is not a complete axial-load-bypass clutch and supplies no actuator magnetic-force, electrostatic-force, release-time or electrical-safety qualification.
