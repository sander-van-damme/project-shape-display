---
status: complete
builds-on: [E-295, E-296, E-297, E-298, E-299, E-300, E-301, E-302]
---

# E-303 — Selectable friction-clutch feasibility

**Owner-commissioned investigation, 23 October 2026.** Baseline `c06a663`, matching fetched `origin/main`. DES-009 remains the active development direction. This experiment supplies research, calculations, conceptual CAD and one passive physical-test package; **no new physical clutch measurements**.

**Decision:** screen always-contact electromagnetic friction (A) with a small normal-force/torque fixture. Keep electrostatics (B) as a material/contact alternative and bistable magnetic actuation (C) as the mechanical fallback. No family currently justifies replacing the traveling motor bank or building 6,400 clutches.

## Deliverables

- [Owner decision summary](../tools/curated-experiment-checks/E-303/decision-summary.md): seven requested answers and the smallest next physical test.
- [Engineering report and reading route](../tools/curated-experiment-checks/E-303/engineering-report.md): source evidence, load paths, magnetic/electrostatic physics, support and pitch constraints.
- [A–H comparison](../tools/curated-experiment-checks/E-303/comparison.md): moving functions, full component accounting, manufacturing, torque/power bounds, cost and recommendations.
- [Reproducible calculations](../tools/curated-experiment-checks/E-303/calculations.md): Python, 38 tests, readable tables, 16 CSV datasets and four plots.
- [A magnetic concept](../tools/curated-experiment-checks/E-303/concepts/a-magnetic-concept.svg) and [B floating-electrode concept](../tools/curated-experiment-checks/E-303/concepts/B-floating-electrode.svg): dimensioned drawings, separate load supports and parametric CAD.
- [Supplier prices and costs](../tools/curated-experiment-checks/E-303/components-and-costs.md), [electrical addressing](../tools/curated-experiment-checks/E-303/addressing.md), and [verification](../tools/curated-experiment-checks/E-303/verification.md).
- [One passive print test](../owner-print-tests/2026-10-23-clutch-friction-screen/test.md): configured X1 Carbon/0.4-mm/PLA 3MF, seven parts, CAD/STL, assembly, measured-load protocol and blank results.

## Decision-changing findings

1. E-295 geometry and E-301 motorized movement are retained. Neither supplies measured screw torque. Illustrative light/moderate starting-torque scenarios are about **0.060/0.343 N mm**, not inferred owner measurements. Backdriving and height retention remain open.
2. A rigid washer fixed to an independently supported screw does not ensure magnetic force becomes clutch pressure. The concrete A concept needs a counted compliant carrier. Its 9-mm armature requires a **12.4-mm housing**, approximately **14 discrete pieces including baseline pin/screw and shim**, plus two bonding operations and electronics.
3. The larger A reference gives an ideal **0.1005 N mm at 0.547 W**, before leakage and elastic closure force; initial copper-only adiabatic heating is about **13 K/s**. This is not a continuous rating or demonstrated 10-mW actuator.
4. B2's floating electrode works electrostatically, but equal split halves give **one-quarter B1 force at equal terminal voltage**, and both powered input connections still rotate. A plain-PET 4.7-mm model at300 V gives **0.0428/0.00772 N mm at0/5-µm gap**. Specialized 20-mm published results do not establish commodity-film performance.
5. Two/four staggered heights give7.184/10.16-mm same-height spacing. Larger discs also encounter neighboring through-shafts. Neither complete concept is pitch-qualified. Passive row/column wiring likewise cannot provide arbitrary independent states; bipolar diagonal exceptions are explicitly tested.
6. C/D retain real moving/return functions. E lacks a credible ordinary hysteresis rotor/pole set; F's miniature evidence uses custom metal processing; G/H impose unsuitable containment/service burdens. No weak family receives an unnecessary prototype.

The normalized repeated-material/electronics examples are about **€0.80 for A / €0.59 for plain-PET B**, including baseline printed pin/screw and support allocations. These are uncertain planning estimates, not quotations; shared infrastructure, assembly, yield, tax and delivery are excluded. The source report exposes each allowance.

## Print and evidence status

The genuine Bambu Studio02.08.02.61 project was saved, reopened without external presets and resliced. Both toolpath reviews passed; settings match. Estimate **8.52 g / about1 h19 min**. The optional offer is **DEFERRED solely to preserve the existing three-READY-job limit**. No older offer was changed.

The test compares externally applied normal load with torque/drag on4.7-/10-mm contact faces. It can expose stick-slip, wear and measurement limits; it does **not** validate magnetic force, electroadhesion, dense packaging or the screw mechanism. Use weights or a restrained fixture, never a finger as the obstruction. An unresolved OFF reading is not zero.

**Stop condition reached:** all families assessed, leading models and concepts delivered, one finite print package prepared. Await an explicit owner decision; no purchases, issues, reminders or automatic follow-up.
