---
status: complete
builds-on: [E-038, E-035, E-033, A-010]
---

# E-039: A-010 bounded-geometry rejection after E-038

## Disposition

**REJECTED as a repair within the frozen E-032/E-033 interface.** The
existing E-035 CAD package is retained as the auditable rejected artifact;
this result does not authorize fabrication, hardware testing, or A-010
integration.

The rejection is precise rather than a claim that A-010 is impossible in all
forms: a translating slider carrying a 3.00 mm square aperture and traversing
the declared 3.20 mm S0-to-S4 travel needs at least `3.00 + 3.20 = 6.20 mm`
of longitudinal envelope. The frozen guide pocket is 4.90 mm. Therefore no
single bounded slider can both contain the declared square aperture and reach
all five states while remaining in that pocket. This is a calculated
geometric contradiction, not a tolerance or physical-fit result.

## Direct E-038 defect evidence

The rejection checker inspects the E-035 SCAD text and shared parameters:

* `gate_slider()` creates a body with y length `field`, where `field =
  cartridge = 30.48 mm`, rather than the declared `slider_y = 4.60 mm`.
  That body cannot fit the 4.90 mm guide span.
* The top-level CAD invokes `gate_slider(state_y[2])` once. The four other
  state carriages are reference load-path geometry; they do not create four
  additional physical apertures.
* The stop plate ends at z=1.50 mm and the frame ends at z=0.20 mm. No CAD
  support member bridges that 1.00 mm gap, so the stop-plate-to-frame path is
  prose-only in E-035.

These are CAD/text-derived observations. The checker deliberately does not
claim solid-topology validation. OpenSCAD export only establishes that the
source parses and generates a mesh; it does not establish assembly fit or
load capacity.

## What is closed and what remains

Closed for this bounded gate: the E-038 rejection is reproduced, the
interface contradiction is calculated, and the three requested defects are
explicitly identified. Unresolved: any revised architecture with a larger
guide/travel envelope or a different multi-aperture mechanism; tolerance,
physical fit, force, friction, wear, reader, timing, isolation, and
fabrication performance. A-010 remains unintegrated.

## Reproduction

From the repository root:

```sh
python3 tools/curated-experiment-checks/E-039/a010_e038_rejection_check.py
openscad --export-format binstl -o /dev/null tools/curated-experiment-checks/E-035/a010_bounded_carriage.scad
./repo check
git diff --check
```

The first command must print `PASS rejection evidence` and the calculated
6.20 mm minimum versus 4.90 mm guide span. It passes because the expected
disposition is rejection; it would fail if the E-035 source no longer
contained the audited defects or if the contradiction ceased to hold.

Observed outputs on 2026-10-07:

```text
minimum_slider_envelope_mm=6.20
frozen_guide_span_mm=4.90
defects=oversized_slider single_aperture missing_stop_support
PASS rejection evidence
OpenSCAD: exit 0; top level object is a 3D object
./repo check: OK: 110 objects; structure and builds-on references valid
git diff --check: clean
```
