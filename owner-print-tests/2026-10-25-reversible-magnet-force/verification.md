# Print verification — 25 October 2026

**Digital checks passed. Physical fit, winding and forces remain unknown.** This is a force-fixture release, not a released clutch.

Bambu Studio 02.08.02.61, official Ubuntu22.04 AppImage from the [vendor release](https://github.com/bambulab/BambuStudio/releases/tag/v02.08.02.61), executed with locally extracted Linux dependencies. No printer was connected. The project was generated with real machine/filament/process presets, sliced and exported by Bambu Studio, then reopened in a fresh data directory **without external presets** and resliced/exported. This was CLI project reopening in the actual Bambu engine, not a claim of manually clicking through the GUI.

- [Build/reopen provenance](metadata/build-and-reopen.json): both archive hashes, profile hashes and zero saved-setting differences. Path planning changes by~1 second; it is not falsely described as byte-identical.
- [Original path review](metadata/slice-review.json) and [reopened path review](metadata/slice-review-reopened.json): ZIP CRC valid,6 instances, original STL vertices retained to<0.000015 mm; X1C start G-code,210°C/55°C confirmed. No supports; critical bores free in every applicable layer; all-layer island-to-prior-layer overlap checked. Bobbin thin barrel has continuous deposited material across the checked inner band, not merely a closed mesh.
- [Actual path figure](images/toolpaths.svg) was visually reviewed: open bobbin/core sleeve, blind dowel sockets open above their floors, solid magnet post, and open cable-tie slots. All6 STLs are single connected watertight positive-volume bodies. Plate68×53.9 mm, highest11 mm. No slender upright screw or threaded bore in this test.
- Slicer estimates: original3.63 g,50m11 s total; reopened3.63 g,50m12 s. G-code's filament-volume comment labels its value inconsistently with its numerical magnitude; this handoff uses reported filament mass/length, not that mislabeled volume field.
- No tolerance-variant array is warranted for this force fixture: it contains no functional screw fit or precision sliding clutch. Wooden dowel fits can be checked before adhesive; the0.4-mm bobbin wall and actual insulated wire diameter remain physical inspection points.

Reproduce from repository root (Python3 +cadquery, numpy, trimesh, scipy, matplotlib, shapely):

```sh
python owner-print-tests/2026-10-25-reversible-magnet-force/cad/rig.py
python owner-print-tests/2026-10-25-reversible-magnet-force/scripts/build_project.py --bambu /path/to/bambu-studio --resources /path/to/resources --scratch work/e304-slice
python owner-print-tests/2026-10-25-reversible-magnet-force/scripts/review_slice.py owner-print-tests/2026-10-25-reversible-magnet-force/reversible-magnet-force.3mf owner-print-tests/2026-10-25-reversible-magnet-force/metadata/slice-review.json --plot
python owner-print-tests/2026-10-25-reversible-magnet-force/scripts/review_slice.py work/e304-slice/reopen/reversible-magnet-force.3mf owner-print-tests/2026-10-25-reversible-magnet-force/metadata/slice-review-reopened.json
```

The build script reuses the repository's shared preset resolver. The supplied3MF is self-contained for the owner; reconstruction needs the repository and the specified Bambu release. System libraries/workspace paths are not embedded as requirements in the delivered project.
