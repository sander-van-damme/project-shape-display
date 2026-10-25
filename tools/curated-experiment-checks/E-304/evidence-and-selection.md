# E-304 — evidence, alternatives and selection

Owner-directed parallel research, 25 October 2026. Repository baseline `1071f695b93951246a2865038e7fb9de9bdf2a05`. **DES-009 remains active and is unchanged.** No terrain, scheduling or update-scenario research is repeated. No independently powered short rows are proposed.

## What actually failed

The decisive physical record is [the complete E-298 owner report](../../../owner-print-tests/2026-10-16-self-aligning-point-matrix/test.md), including its later stop-block update. Its observations outrank the earlier experiment summaries saying “not yet tested.”

| Evidence | What it establishes | What it does not establish |
|---|---|---|
| E-295: five compact pairs, three nominal 0.175-mm relief pairs reportedly very smooth | This specific 3.2-mm, 3-mm-lead, 90° thread in a 4.4-mm pin can print and move by hand | Measured running/start torque, self-locking, array yield or long stroke |
| E-298 owner: partial kit, auto-orientation and auto-placement used; four unspecified parts not printed | Assembly was incomplete; saved orientation cannot reconstruct the print | A controlled comparison of the supplied nominal variants |
| Owner: slender screws produced spaghetti; brim cleanup awkward | The actual unsupported screw print and cleanup failed | Failure of the thread principle or all upright screw prints |
| Owner: points directly opposite blocked; only one pair tested | This printed contact pair did not self-align at that alignment | Universal failure of every pointed, toothed, asymmetric or compliant coupling |
| Owner: selectors already bent; limited travel prevented complete closure; notches bent easily | Global bending and local notch deformation independently reduced engagement | Exact cause of initial warp, modulus, force or dimensional error |
| Owner: substantial wobble; shallow hand socket wore quickly | The assembled constraint chain and test input were inadequate | Which individual bearing clearance caused what fraction of wobble |
| Later owner update: stop blocks used, one pin moved up/down smoothly | Positive one-pin motion after manual assembly/setting | Automatic engagement, simultaneous selection or neighbor isolation |
| E-299 | Wider dogs, 3-mm stroke, larger holders, screw braces, split frame exist in CAD/slicer | No completed E-299 physical report was found |
| E-300 | 45° cones, stronger vertical section, two-contact rocking row; calculated thrust loss | No physical cone result was found; a blank form is unknown, not a failure |
| E-301 / DES-009 | One compact pin moved using a microstepper and improvised tape coupling | A traveling bank, automatic docking or this new mechanism |

Actual geometry inspected: E-297 `cad/generate.py`, E-298 `contact-analysis.md` and point geometry, E-299 CAD/report, E-300 `cad/generate.py`, `parameters.json`, actual mesh-derived section drawing, and the retained E-295 thread/pin STLs. The old double-D is Ø2.2/AF1.6 in an approximately Ø2.5/AF1.9 socket. Its axial sliding fit, rotor capture play and incomplete guide sectors accumulate tilt; selector flanges cannot substitute for two spaced stationary journals. E-297's 0.96-mm comb blades and E-300's 0.46-mm spine expose the local weakness at the openings. E-300's taller section improves one bending axis while weakening another; height alone does not establish torsional stiffness.

The new design removes the sliding torque spline entirely. The input gear, shaft and male cone are one part. The output cup, neck, thrust collar and screw are one part. Round stationary guides locate each shaft; selector movement never supplies radial location. This addresses a specific tolerance chain, not an assertion that double-D couplings are generally unusable.

## Candidate architectures

Counts below include the resident pin/screw and the local input distribution rotor. Shared selectors, guide decks and bus are additional. A printed flexure remains a moving mechanical function even when no separate spring is bought.

| Candidate | Concrete torque/support arrangement | Printed parts/cell | Purchased parts/cell | Local functions and main tradeoff |
|---|---|---:|---:|---|
| A1: guided single cone, cam + roof gate, integral compliant follower **selected** | One axially moving input rotor in two stationary journals; fixed output cup/screw in two journals and captured thrust collar; follower has central thrust pad and withdrawal lip | **4** | **0** | Input spin + axial shift, output spin, pin translation, follower cam motion, elastic differential travel. One elastic function. Conical traction and guide drag unmeasured. |
| A2: same guided selector, flat annular face | Same four parts and guides; no wedge effect | 4 | 0 | Phase-independent geometry and simpler release, but half the gross torque of the 30° cone at equal wear radius/force. Best fallback if cone sticking dominates. No extra prototype prepared. |
| A3: guided sliding dog/face clutch | Fixed driven shaft, sliding keyed sleeve, output screw, compliant gate follower, pin | 5 | 0 | Positive torque, less sustained clamp force after seating; one sliding torque fit returns. Tested representative teeth retain blocked phases or resistance-dependent self-indexing. |
| B: two independent clutches in series | Fixed input rotor → row-controlled keyed sleeve → independently supported intermediate shaft with two clutch faces → column-controlled sleeve keyed to output screw; two guided followers; pin | **8** | **0** | Two elastic functions; intermediate shaft needs two radial journals and two thrust faces. Each selector can engage a simple independent clutch. Phase-independent if both are frictional. No logical roof gate; more assembly and two slip interfaces. |
| C1: bidirectional radial collet | Shared driven cage, radially closing slotted collet on screw tail, tapered axial sleeve and row/column gate | At least 5 | 0–1 | Continuous angular grip and possible torque multiplication; thin slotted fingers, radial pressure and release hysteresis become repeated functions. At 5.08 mm, guide/cage/collet walls compete for the same radius. Not disproved; less convincing FDM first test. |
| C2: bidirectional wrap/roller wedge clutch | Opposed wraps or opposed roller paths, supported race, controlled release | At least 5 plus wraps/rollers | Several | Compact torque possible, but direction reversal and release add repeated precision contacts. A one-way bearing is not a bidirectional selector. |
| C3: row-level upstream clutch plus column clutches | One row clutch feeds a full-length rotating bus, each column enables its local output | ~4 plus row hardware | Bus-dependent | Can amortize the first clutch; continuous row transmission and its off-drag still require a concrete compact right-angle drive. Retained as a comparison, not silently substituted for the requested full-length mechanical selectors. |

B is a genuine alternative: it replaces a mechanically gated follower with two independent ordinary engagements, and can tolerate a poorly functioning gate better than A. Its disadvantage is quantified repeated hardware and support, not merely “two is worse than one.” For a series path, torque capacity is the **smaller** capacity; the two interfaces do not add torque. Both normal-force systems, all journal friction, and the intermediate shaft count. Approximately 8–12 mm additional active stack height is required even before increasing journal separation. The selected A fixture is already taller than E-300; more height is possible but not free.

## Engagement investigation

[Executable model](analysis/calculate.py) samples **1,440 relative angles over 360°** for four explicitly defined three-tooth height profiles: flat dogs, triangular crowns, rounded sinusoidal crowns and asymmetric ramps. It computes

`D(φ) = maxθ [h(θ) + h(φ−θ)]`.

These are reproducible representative profiles, not claimed replicas of every historical solid. E-298's separate mesh-envelope calculation remains the evidence for its actual two-point parts. New solid cone geometry is checked separately by the mesh review.

A fixed angular phase cannot move axially past an overlapping solid volume. Allowing either rotor to turn under contact changes that condition: on a descending separation envelope axial force can do rotational work. For a single ideal contact at radius `r`, slope `s=|dD/dφ|/r`, a Coulomb screening estimate is `T/F = r(s−μ)/(1+μs)`, clipped at zero. Real multiple contacts, shaft resistance and FDM steps can only be assessed with a fuller contact model or a test; this equation is not an automatic-engagement proof.

The representative envelopes have maxima or plateaus. At a smooth extremum, `dD/dφ=0`, so axial force supplies no first-order indexing torque. At a pointed maximum, opposing admissible contact normals can support axial force without selecting a rotational direction. A wider printed tip creates a finite plateau. Asymmetric crowns move or change these regions; the model does not assume that they eliminate them. Friction and a resisting screw widen the problematic set. This result applies to these rigid, coaxial, axial-insertion profiles and their permitted motion. **It is not a theorem excluding all toothed, guided, multi-stage or compliant mechanisms.** A tooth design with an independently imposed indexing path has changed the kinematics and deserves its own analysis; it cannot be credited with zero indexing motion.

The selected cone is a surface of revolution. In ideal coaxial geometry its first-contact lift is **0.60 mm for every real relative angle**, not just the sampled angles. No angular search, purposeful input rotation or output indexing is required to make geometric contact. Static closing therefore need not change screw height. This establishes **phase-independent contact geometry**, not torque capacity or reliable physical engagement. FDM seam, ovality, concentricity, tilt, contamination, contact pressure and friction remain phase-dependent physical effects. A shared stationary input is used during the angular engagement test; hand-setting each cup is explicitly disallowed.

At a 30° half angle, the simple taper self-wedging screen is `μ ≥ tan(30°)=0.577`. The assumed 0.10–0.40 range lies below that boundary, but printed ridges, wedged debris, adhesive wear and tilted multi-point contact need not obey a smooth-cone Coulomb model. Both row return and column roof motion provide a positive withdrawal path through the captured follower/rotor flange. They are tested after both directions of torque; gravity alone is not counted as release.

Reversal changes friction direction without requiring another tooth phase. Slip can occur in either direction. Slip at one obstructed output allows the common input to continue only if the motor/bus has enough torque and the clutch releases below damaging load. An obstruction in the **cam track itself** can still jam a whole row; local compliance is not universal fault isolation.

## Selection criterion

Hard requirements were: retain full-length row/column control; stationary radial/tilt support; continuous-angle contact without intentional phase searching; bidirectional operation; explicit mechanical AND; no uncounted per-cell purchased bearings/springs; and a useful FDM-scale test. A1 meets these as a concrete, testable design. A2 meets them but requires approximately twice the gross pressure. B meets the phase and logic requirements with friction faces but doubles local printed part count. A3 trades clamp pressure for an unresolved engagement condition. C1/C2 add more difficult repeated interfaces before offering a clearer test.

**Select A1 for one validation, not for an 80×80 build.** If moderate torque cannot be transmitted in a pressure band that also gives clean release and neighbor isolation, do not continue merely because its CAD looks phase-free. The owner decides whether to continue after the single focused physical result.
