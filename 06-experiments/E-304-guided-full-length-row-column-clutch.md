---
status: complete
builds-on: [E-295, E-296, E-297, E-298, E-299, E-300, E-303, DES-009]
---

# E-304 — guided full-length row/column clutch

**PRINT TEST: DRAFT — unresolved pin-wall toolpath gaps; physical operation untested.**

Owner-directed parallel mechanical investigation, 25 October 2026, based on commit `1071f695b93951246a2865038e7fb9de9bdf2a05`. **DES-009 remains the active primary design and is unchanged.** No physical E-304 test has been performed. Completion means the investigation and one DRAFT physical-validation package, not a qualified mechanism. The configured 3MF reopens/reslices successfully, but unresolved approximately 0.207-mm pin-wall toolpath gaps prevent print readiness.

## Decision

Select **one guided 30° friction cone per pixel**, with a captured full-length row cam, a full-length column ceiling gate and one integral compliant follower. A permanently meshed common rack drive turns the inputs. Two stationary journals locate each input and each output; the moving selectors supply force and logic, not shaft alignment. This is the strongest practical candidate for one test, not authorization to build 80×80.

| Owner question | Result and evidence level |
|---|---|
| What improves on E-297–E-300? | Sliding double-D torque fit removed; input gear/shaft/cone integrated; output cup/screw integrated; two stationary guide planes per shaft; lower thrust-contact radius; local compliance for unequal contact heights; deep guided selector beams and positive withdrawal. These are design/CAD improvements, not measured reliability gains. |
| Components per pin? | Four printed moving bodies including the terrain pin: pin, output screw/cup, input gear/cone, follower. Zero purchased parts per pin; one integral spring function. Four radial bearing lands, two pin guides and axial/withdrawal contacts are still repeated functions in shared structures. |
| Arbitrary initial angle? | An ideal coaxial cone makes contact at every real relative angle without deliberate indexing .1,440-angle representative tooth-envelope analysis and 72-angle actual cone mesh sweeps are supplied. Printed friction, seam, eccentricity, tilt and drag remain unproved. This is not a universal rejection of toothed couplings. |
| Full-length stiffness? | Longitudinal 2.54-mm selector motion permits fixed guides every 25.4 mm. Use a closed printed box/cam beam with continuous inserted stock; two 2-mm steel rods are the conservative default at the calculated force; carbon saves weight but needs measured modulus and joint evidence. Loose rods do not earn bonded-composite stiffness. Steel and other stock are compared. No separately powered short rows. |
| Plausible at 5.08-mm pitch? | The actual 4.4-mm pins and retained 3.2-mm/3-mm-lead thread fit in a complete neighboring 2×2 CAD model. Cup gap .48 mm and gear gap .88 mm. The fixture is 80.2 mm overall at neutral (pin top Z79 mm) and tests±1.5-mm travel. Full-array assembly, long-stroke drive, guide manufacture and economic advantage remain unresolved. |
| Torque/force? | Nominal linear follower model predicts 1.10 N selected, 1.79 N half-selected. A stated friction/drag case predicts .400 Nmm net versus E-303's assumed .343 Nmm moderate start; less favorable friction removes that margin. A fully loaded 80-cell row can require roughly 113–183 N at the chosen cam friction. These are calculations, not measured loads. |
| What remains unknown? | Actual clamp force, cone grip and release, radial rubbing (adverse guide/axial-clearance corners can interfere), creep/fatigue, unselected height retention, small printed gear quality, assembly yield, neighbor isolation under obstruction and large-array maintenance. |
| Single continuation result? | All four cells repeatedly engage from sampled stationary phases, move bidirectionally under the stated light/moderate load and release at one setting; half-selected cells stay still and one restrained output does not stop the others. Seek that result once, then await an explicit owner decision. |

## Evidence and delivery

[Downloadable engineering report PDF](../tools/curated-experiment-checks/E-304/E-304-engineering-report.pdf) combines the investigation, drawings, verification limits and owner test instructions.

- [Previous failures and architecture/engagement comparison](../tools/curated-experiment-checks/E-304/evidence-and-selection.md): physical owner observations separated from CAD and untested hypotheses; single cone, flat face, guided teeth, two clutches in series, collet and wrap alternatives.
- [Full-length selector study](../tools/curated-experiment-checks/E-304/selector-study.md): bending, torsion, local shear, buckling, axial shortening, supports, manufacturing, rod joints and thermal effects.
- [Concrete mechanism, tolerances, force paths, component and cost budget](../tools/curated-experiment-checks/E-304/mechanism-and-budget.md). Broad full-system screening allowance€1,300–3,800 excludes labour and is not a vendor-qualified actuator/BOM quote.
- [Primary sources and observed stock prices](../tools/curated-experiment-checks/E-304/sources.md), [reproducible calculations/CAD/checks](../tools/curated-experiment-checks/E-304/reproduce.md), [verification record](../tools/curated-experiment-checks/E-304/verification.md).
- [One owner test package](../owner-print-tests/2026-10-25-guided-matrix-clutch/test.md), including actual STLs, configured X1 Carbon Bambu 3MF, tolerance samples, shared drive, drawings and blank results form. Its explicit status governs printing; a generated archive alone is not READY.

**Stop:** one meaningful validation package prepared. No issue, purchase, automatic print campaign or further development is initiated. Owner feedback and an explicit decision are required before continuation.
