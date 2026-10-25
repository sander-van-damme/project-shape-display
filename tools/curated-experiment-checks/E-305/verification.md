# Evidence, reproduction and limits

Repository baseline **1071f695b93951246a2865038e7fb9de9bdf2a05**, read25 October 2026. DES-009 remains the primary architecture and its files are unchanged.

**Numbering correction:** pulled `main` at `e130fcc02d31135fbf9022f84266a1d25e6fd000` and assigned this investigation **E-305**. The existing E-304 guided full-length selector study and all files from that main revision are preserved byte-for-byte. Updated local links, diagram labels, reproduction paths and embedded Bambu process name. STL geometry is unchanged. The renamed print project was rebuilt, reopened without external presets and resliced; both archives were checked again. The earlier baseline above remains the provenance of the original research.

## Evidence trail read

- Root[AGENTS.md](../../../AGENTS.md),[mission](../../../01-project-description/shape-display-mission.md),[current priorities](../../../02-design-criteria/current-prototype-priorities.md),[experiment instructions](../../../06-experiments/AGENTS.md),[print instructions](../../../owner-print-tests/AGENTS.md) and template.
- [DES-009](../../../08-integrated-designs/DES-009-traveling-motor-bank-screw-pins/DES-009-traveling-motor-bank-screw-pins.md) and[components](../../../08-integrated-designs/DES-009-traveling-motor-bank-screw-pins/components.md): provisional4.4-mm pins,5.08-mm pitch, Ø3.2 screw,3-mm lead, independent resident support; no fabricated motor torque.
- [E-295](../../../06-experiments/E-295-compact-screw-drive-development.md),[E-296](../../../06-experiments/E-296-compact-matrix-clutch-selection.md),[E-297](../../../06-experiments/E-297-two-half-row-column-clutch-print-tests.md),[E-298](../../../06-experiments/E-298-self-aligning-point-clutch.md),[E-299](../../../06-experiments/E-299-supported-two-cell-selector-retest.md),[E-300](../../../06-experiments/E-300-conical-friction-selector.md): geometry, support, phase plateaus, tolerance/strength and stationary selector friction lessons.
- [E-302](../../../06-experiments/E-302-improved-microstepper-test-frame.md),[latest physical diagnosis](../../../owner-print-tests/2026-10-23-low-friction-motor-frame/diagnosis.md): actual owner report of rising-position resistance and closure sensitivity. That evidence supersedes older “untested” summaries; the rubbing surface and printed revision are still unknown.
- [E-303](../../../06-experiments/E-303-selectable-friction-clutch-feasibility.md) and its calculation/addressing/print files:0.059665/0.342944/2.196316-N-mm provisional starting scenarios, ~0.547-W magnetic friction reference and passive matrix limitations. No renewed eight-technology survey.

## New evidence classes

| Class | What this delivery establishes | What it does not |
|---|---|---|
| Published/supplier | Material/stock dimensions, prices and published specimen magnetic measurements, linked at claims | Purchased lot verification or measured clutch forces |
| Analytical/numerical | Finite air-coil force, finite PM neighbor force, electrical/thermal scales, cone force balance, phase envelopes | Calibrated field simulation, nonlinear hysteretic core FEA, physical performance |
| Parametric CAD | Force fixture manufacturing geometry; dimensioned clutch envelopes and load-path concept | Production gear/screw meshes or fully tolerance-qualified clutch |
| Actual Bambu output | Configured saved/reopened X1C project, real per-layer paths, bores/support checks, print estimates | Physical adhesion, winding success, force or torque |
| Physical | Existing owner evidence only; new result form blank | No new built prototype, measured current/temperature/force/torque or cycle test |

Air-coil model assumptions are explicit in[model.py](analysis/model.py) and[generated winding data](analysis/results/winding.json): SI units; uniform axial magnetization;Br1.395 T;0.15-mm copper;0.18-mm insulated-turn pitch;140 turns;nonmagnetic bobbin. The low-carbon core surrogate explicitly has no measured B-H loop and is not treated as a validated force prediction. The neighbor solver is finite surface-charge integration rather than a near-field dipole-only claim. No FEA mesh or physical calibration is claimed.

Reproduce calculations:

```sh
python tools/curated-experiment-checks/E-305/analysis/generate.py
python -m unittest discover -s tools/curated-experiment-checks/E-305/analysis -v
python tools/curated-experiment-checks/E-305/analysis/drawings.py
openscad -o work/e305-concept.csg tools/curated-experiment-checks/E-305/cad/concept.scad
```

Ten meaningful numerical checks passed: exact loop-axis field, current reversal/zero, quadrature convergence, independent energy gradient, coil-center equilibrium, finite-neighbor convergence/far-field limit, neighbor symmetry, cone force balance, phase periodicity, and circuit-state constraints. They do not establish material/friction accuracy. The drawings generator makes the section, exploded assembly and test instructions;[flux.svg](images/flux.svg) is a hand-authored qualitative field diagram. There is no image-generation inference of engineering dimensions.

[Print reconstruction and validation](../../../owner-print-tests/2026-10-25-reversible-magnet-force/verification.md) gives the exact commands. All6 parts are watertight, single connected solids. Actual thin-wall, open-bore, layer-connection and saved-setting checks passed for both archives. The optional MicroPython helper is syntax/logic-reviewed, not hardware-tested; external current limiting and manual temperature/scale validation are mandatory to interpret the experiment.

`./repo check` reports the same6 pre-existing size findings as baseline: oversized E-266, E-283, E-286, E-288, E-293 and owner-print-tests/AGENTS.md. None is modified. Local links within this delivery are checked separately. Existing tracked files are preserved; no DES-009 status change, issue, purchase, scheduler or additional task is created.

**Stop condition:** this finite research report and one force-test package. A material/geometry blocker has not been concealed as a working clutch: only the force fixture is READY. The full clutch is gated by a real force result and an explicit owner decision.
