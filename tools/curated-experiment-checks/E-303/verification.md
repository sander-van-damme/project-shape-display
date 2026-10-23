# E-303 verification and evidence limits

[Atomic result](../../../06-experiments/E-303-selectable-friction-clutch-feasibility.md) · [Full report](engineering-report.md) · [Technical review](review.md) · [Print verification](../../../owner-print-tests/2026-10-23-clutch-friction-screen/verification.md)

Checked 23 October 2026 against repository baseline `c06a663`. All work is limited to the new E-303 result, its engineering assets and one new owner print pack. Existing DES-009, historical experiments and print offers remain unchanged.

## Calculations

**38 tests pass** with Python's standard-library unittest runner. Coverage includes SI/torque conversions, ideal screw work per revolution, V-thread raising/lowering and self-lock threshold, guide-load reversal, start/run sensitivity, numerical annular-friction integration, single/two-gap magnetic reluctance and pressure, current-squared force, saturation screening, fixed-joint reluctance, winding power and initial copper heating, finite-difference electrostatic virtual work, dielectric versus air-gap boundary conditions, floating/series capacitance and stray charge, field/voltage/gap scaling, conditional cubic scaling, charge/discharge energy, slip heat, two/four-tier lattice clearance, through-shaft collision and passive-addressing counterexamples.

```sh
python -m unittest discover -s tools/curated-experiment-checks/E-303/analysis -p 'test_*.py' -v
python tools/curated-experiment-checks/E-303/analysis/generate.py
```

The generated tables include 16 CSVs and four plots. These are scenario calculations, not measurements, FEA or statistical confidence intervals. The equations are independently checked through conservation laws, numerical integration/differentiation and counterexamples; tests do not qualify the assumed material properties. Inputs are documented both in `inputs.json` and explicit sweeps in `generate.py`.

## Concepts and physical print package

Both parametric A/B OpenSCAD concepts parse/compile to CSG. Dimensioned SVGs were rendered and visually inspected. Review corrected A capture overlap, collar shoulder clearance, keeper attachment, flexure clearance and input-drive access. These are **conceptual packaging checks**, not full collision qualification, FDM release, stress analysis or tested magnetic performance. The concept thread is an explicitly labelled E-295 envelope; no new screw profile is substituted.

The separate passive fixture has seven watertight STL components, parametric CadQuery source, two identical nominal samples, two additional clearances, assembly instructions, purchased-part requirements and a blank results CSV. The real **Bambu Studio02.08.02.61** executable saved a configured **X1 Carbon/0.4-mm/Generic PLA** project, reopened it in a fresh data directory without outside presets and sliced again. Graphical UI display was unavailable; this is verified **Bambu CLI** save/reopen/reslice plus independent actual-G-code review, not a claim of GUI inspection.

Both slices preserve all saved settings and pass mesh correspondence, archive integrity, temperature/start-code, contact ring continuity, open bore/eyelet/cup, bed-contact and unsupported-island checks. The deposited line-footprint method and its tolerance are documented in the print verification. G-code ordering is not byte-identical and the estimate differs by four seconds; both are independently reviewed. Initial/reopened estimates: **8.52 g, 1 h19 min1 s / 1 h19 min5 s**. Nominal repeated STL files are identical. Source and project SHA-256 values are recorded in the pack metadata.

No supports or threads occur in this test plate. Physical face flatness, fit, adhesive behavior, guide drag, wear and instrument sensitivity remain unknown. The delivered project is technically prepared, while the offer remains **DEFERRED** to keep three existing READY offers unchanged.

## Repository checks

The completed experiment is stored as a short atomic result with detailed assets in `tools/curated-experiment-checks/E-303`, following adjacent experiments. Runtime downloads and scratch are outside the repository in workspace `work/`. Local link and changed-file checks cover the new deliverables.

`./repo check` retains baseline warnings about oversized E-266, E-283, E-286, E-288 and E-293, and oversized `owner-print-tests/AGENTS.md`. These historical files are not rewritten for this task. The final check must introduce no E-303 structural warning. Exact final checks and existing-file integrity are recorded in [delivery-checks.json](delivery-checks.json).

## What the evidence does and does not establish

| Evidence class | Present here | Limitation |
|---|---|---|
| Existing owner physical evidence | E-295 hand fit; E-301 motorized up/down; later documented frame problems | No measured torque, coefficient, clutch isolation or array yield |
| Published measurements | Original electrostatic rotary/linear research and miniature EPM experiment | Different materials, geometry and fabrication; no automatic transfer |
| Manufacturer/catalogue evidence | Component dimensions, datasheets, prices and commercial drag behavior | No binding quotation, magnetic curve or delivered stock qualification |
| Mathematical estimates | Screw/friction/magnetics/electrostatics/heat/packing/addressing | Assumed geometry/material values; no verified device performance |
| CAD and slicer checks | Two concepts; one real configured/sliced/reopened fixture | No physical pass or production readiness |
| Owner experiment | Prepared, unperformed | All results blank/unknown |

No magnetic FEA, fabricated driver, energized electrostatic assembly, physical print, thermal experiment or new screw test is claimed. The finite recommendation is the passive friction screen and an owner decision. DES-009 remains primary.
