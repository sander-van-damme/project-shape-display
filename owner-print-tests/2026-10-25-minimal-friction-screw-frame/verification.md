# Digital verification — 25 October 2026

**Release:** READY for the bounded physical experiments in `test.md`. **Physical result: NOT PERFORMED.** Primary A and optional BC are genuine configured X1C projects, not mesh-only wrappers. The motor shaft load, print adhesion, fit, friction, holding force and wear remain unmeasured.

## Source and CAD

`git fetch origin main` established HEAD=origin/main=`1071f695b93951246a2865038e7fb9de9bdf2a05`. Required mission, priorities, experiment reports, v3 CAD/STLs/settings, motor measurements and23-October diagnosis were read. No electronics/firmware, actuation architecture, issues or scheduled tasks were added. The two older selector print offers are marked DEFERRED solely to prioritize these two requested jobs within the owner's maximum of three READY jobs; their designs/results are preserved. The owner-reported v3 fit/binding and uncertain IRUN are preserved as physical observations; the later knife modification is not treated as their original cause.

`metadata/source.json` records hashes of the inherited profiles/meshes. `generate.py` uses OpenSCAD plus manifold mesh booleans. Every component is one closed, consistently wound solid. The source screw is cropped/translated, not re-profiled. Working thread symmetric difference and C radial-profile symmetric difference are effectively zero. The small junction union and terminal chamfer are excluded from the working-profile comparison and described in `engineering.md`.

`verify_geometry.py` checks:

- Proper rigid assembly of opposite-handed frame halves; no half-to-half overlap.
- **122 screw/pin poses**,0–15 mm in0.25 mm increments, both0/0.30 mm float endpoints, correct helix phase. All nominal moving-pair intersections below1e−4 mm³;6 mm thread overlap and2+2 mm guide overlap throughout.
- Continuous rigid pin/frame and rotational rotor/frame envelope clearance, not merely a few endpoint screenshots. Sampled thread mating is not a proof against arbitrary elastic/printed errors.
- Actual downward washer/deck and upward flange/stop contact using small penetration probes; nominal nonintersection alone was not accepted as proof of a load path.
- Motor8/8.2 mm envelopes, body9.2, L shaft/boss, PCB and explicitly labeled glue/wire/tab allowances. The unmeasured real gear teeth are not replaced by a claimed accurate tooth mesh; gear envelope/rib intersection is intentional.
- Small misalignment sensitivity and the0.6 mm loose radial land's contact onset. No inferred motor-side-load guarantee.
- Square-polygon neighbor rotation calculations; deck/liner/boundary assembly at equal and staggered heights; nonintersecting print layouts. Four additional40 mm-pin endpoint checks preserve the same thread and full guides.

See `metadata/geometry-review.json`, `meshes.json`, and the dimensioned SVG. The source is parameterized, but only the delivered parameter set is checked; changing it requires regeneration/review.

## Bambu Studio and actual paths

Official Linux Bambu Studio **02.08.02.61**, X1 Carbon0.4, with locally extracted runtime libraries. Runtime and scratch files stay outside the deliverable. `build_projects.py` resolves official printer/filament/process presets, carries forward the tested family profile, explicitly applies the listed settings, saves the Bambu project, and **reopens/reslices it with no external profiles**.

Original and reopened archives match saved settings and object overrides. G-code ordering differs; the second slice was independently reviewed instead of assuming identical files. Four JSON reports (`A/BC-slice-review[-reopened].json`) record the actual paths and hashes. All exported meshes match the project vertices within0.00004 mm. There are no automatic support paths and no deposited islands meeting the review's>0.005 mm² /<0.001 mm² previous-layer-overlap criterion. This footprint criterion is a reproducible screening calculation, not a layer-adhesion test.

A's socket retains all inspected C lobe layers, minimum tip/valley radial contrast about0.140 mm, open shaft space and a continuous roof. The screw core has nominal minimum r0.5 bead coverage about0.828; v3's short reference was about0.830 under inherited bead settings. All nine turns retain tip radii about1.597–1.598 mm; adjacent core footprints overlap by at least0.625 mm². This is deposited-bead coverage, not an inferred solid strength. Short external thread supports are connected and printed; their four necks remain real cleanup contacts. Both upright reference bores stay open. The90°-roll horizontal duplicates avoid the other rolls' detached islands, but roof bridges remain physically unqualified. A local180° bridge angle reduces their maximum individual free segment from5.35 to2.57 mm. Toolpath plots show the socket, roof, screw, guide and both pin orientations.

The frame prints flat, without floating upper portions. Local bridges exist (up to about3.59 mm individual free segments in the frame), including curved/stepped cavity regions; the screw roof has segments up to1.96 mm. No support-free geometry is declared physically successful simply because the slicer accepts it. The tall B pins retain3 mm brims, conservative acceleration and cooling; their55 mm overall height /25 mm slender stems need owner adhesion/straightness inspection.

## Reproduction in the repository

Python dependencies: numpy, trimesh, manifold3d, shapely, scipy, matplotlib. OpenSCAD and official Bambu Studio02.08.02.61 with resources are required. No source dependency is fetched automatically.

```sh
python owner-print-tests/2026-10-25-minimal-friction-screw-frame/scripts/generate.py
python owner-print-tests/2026-10-25-minimal-friction-screw-frame/scripts/verify_geometry.py
python owner-print-tests/2026-10-25-minimal-friction-screw-frame/scripts/build_projects.py --bambu /path/to/bambu-wrapper --resources /path/to/resources --scratch work/slice-A --plate A-first
python owner-print-tests/2026-10-25-minimal-friction-screw-frame/scripts/build_projects.py --bambu /path/to/bambu-wrapper --resources /path/to/resources --scratch work/slice-BC --plate BC-comparisons
python owner-print-tests/2026-10-25-minimal-friction-screw-frame/scripts/draw_section.py
```

`review_toolpaths.py PROJECT PLATE OUT.json [--plot]` reviews a saved project. Apply it separately to both saved and scratch/reopen archives. `--baseline` reviews the original v3 project with its historical layout. Historical meshes, profile and the shared Bambu parser/builder in the repository are required for reproduction; the supplied3MFs are self-contained for printing.

The repository-wide `./repo check` reports six pre-existing size-limit findings: E-266, E-283, E-286, E-288, E-293 and owner-print-tests/AGENTS.md. A pristine main documentation snapshot reports the identical six; this task adds none. `git diff --check` is clean. See `metadata/delivery-checks.json` for final check outcome, status and file manifest. The optional print offers are finite; no follow-on design, firmware change, physical result or production-array qualification is implied.


## File delivery

The source package remains in the repository. A private ChatGPT Page provides downloadable copies because the configured chat output directory is not writable in the managed cloud environment. The CAD drawing and PDF were visually inspected. Native Page rendering has no available preview tool; file access and saved references can be checked independently.
