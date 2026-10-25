# E-304 verification and readiness

**Print status: DRAFT. Do not treat the supplied 3MF as a READY print instruction.** The archive is a genuine configured Bambu Studio X1 Carbon project and has been reopened/resliced. The remaining blocker is its critical deposited geometry: the retained pin wall has a maximum nominal midwall discontinuity of **0.207 mm**; layers **12.48, 15.48 mm** still fail the closed-loop screen even after an 0.08-mm geometric buffer. This is a slicer finding, not an observed broken print. A continuous watertight STL does not establish continuous deposited walls.

The operator has not physically printed or assembled E-304. No failed or successful owner result is invented. The owner's requested DRAFT fallback and [owner-print-tests/AGENTS.md](../../../owner-print-tests/AGENTS.md) apply: successful saving/reopening alone does not establish print readiness. Existing READY offers and DES-009 remain unchanged. Stop here for the owner decision; no further design or print campaign is initiated.

## Calculated and geometric evidence

-15 structural section alternatives, 216 torque cases, 54 flexure cases, 1,440 representative tooth phases. The E-303 screw function is called directly with its original light/moderate assumptions.
- Independent single-member fixed-guided beam limit agrees with the frame-element solver; actual box/web/sleeve area and second moments are sampled at 0.01-mm grid spacing. These are numerical checks, not material measurements.
- Delivered meshes are watertight. Four supported screws deliberately form four bodies in one named print object. The frame's ten sacrificial rods are explicitly removed from the operating assembly.
- **32 nominal assembly configurations**:16 row/column masks, six sampled intermediate selector strokes, four common-drive positions in both directions, one blocked follower and one stalled output, plus four rack-end configurations (OFF and selected with compatible independent output phases). No unexpected nominal mesh interference above 0.001 mm³ was found. Matching cone surfaces show 0.004–0.0073 mm³ tessellation overlap at the nominal mathematical contact position; these are explicitly labelled contact, not silently discarded collisions.
-25 common-rack positions through one complete tooth pitch have no unexpected gear/frame intersections. A deliberately displaced rotor produces a detected interference, checking that the screen can fail. A separate+4.5-mm rack-overtravel case detects approximately0.070 mm³ interference between the shared shuttle crosspiece and hand pinion. The operating window is therefore restricted to−9.5…+2.8 mm, with the phase sweep beginning at−8.5 mm. The bench uses marked manual limits; unlimited knob rotation is not allowed.
- Actual faceted cone contact is sampled at 72 phases for nine offset/tilt cases (648 cases). Coaxial first contact varies about 0.596–0.597 mm due tessellation, versus 0.600 mm for exact ideal surfaces. At .1/.2/.27-mm imposed radial offset first contact advances to about .425/.252/.131 mm. Deliberately adverse .4-mm/3° and .7-mm/6° cases **interfere while OFF**. See the CSV and the explicit journal-clearance/axial-float corner calculation; these are not tolerance-qualified operating states.
- The actual thread handedness is retained: pin height changes−3 mm per positive screw revolution. The bench's±1.5-mm travel, phase offsets and both output guide planes are included. No full 80×80 model or full-stroke drive is claimed.

## Actual saved project

Bambu Studio **02.08.02.61**, official X1 Carbon 0.4-mm printer/machine-G-code preset, Generic PLA and process settings inherited from the physically tested E-295 compact-thread project, with the explicitly recorded E-304 process changes. This was an actual Bambu **command-line** save/reopen/reslice, not a claimed manual GUI action. No external printer/process/filament settings were loaded during reopen. Saved settings compare equal. The archive contains 33 named objects and actual G-code; it is not a mesh-only 3MF.

Printer: X1 Carbon 0.4 mm; PLA220°C, textured PEI55°C; layers/first layer .12 mm; Arachne, two walls, 100% zig-zag infill, nominal line widths .45 mm, minimum bead 75%, minimum feature 10%. Outer/inner speed 15/20 mm/s, first layer 15, bridge 15; general acceleration 1000, outer/first 500 mm/s². Supports OFF, raft 0, outer brim 2 mm with .12-mm gap, by-layer order. XY/hole/elephant-foot compensation 0. Fan 100% after first layer, auxiliary fan 0, cooling minimum speed 10 mm/s. Bridge direction 90°, seam gap 0%. Full values and source hashes are retained in JSON.

**Original slicer estimate:7 h 34 min 27 s /21.60 g PLA.** Reopened estimate:7 h 34 min 17 s /21.60 g. These are slicer estimates, not physical consumption or time. The combined one-plate test is small in material, but deliberately slow for fine threads, gears and thin flexures.

Archive geometry matches the bed-oriented source plate to a maximum bidirectional vertex error of 0.00002254 mm, with equal facet counts. This is a coordinate fidelity check, not a printer accuracy specification. All 33 objects have deposited paths through their interior height. Source orientations, supports and brims are saved rather than left to automatic placement.

## Critical toolpath review and remaining blockers

The [focused path figure](../../../owner-print-tests/2026-10-25-guided-matrix-clutch/images/critical-toolpaths.svg) and full atlas are drawn from the actual archived G-code. Model-path analysis excludes brim/skirt, so brim is not incorrectly credited as part of a structural wall.

- The six follower ligaments print on their flat back. The short lower-neck bridge is about 2.4 mm. Clearance between folded ligaments remains visible; integral compliance is not physically calibrated.
- The permanent gear has 12 deposited teeth. This establishes representation of the tooth geometry, not tooth strength, backlash or a successful mesh in plastic.
- Both rod-channel roofs and box roofs have transverse bridge paths after specifying the 90° direction; the upper rod sleeve has a supporting internal web. The 100-mm beam no longer starts a large detached upper-sleeve island.
- The frame has no fully isolated new deposited components in the screened layers after adding sacrificial supports. Its largest screened remaining free overhang/bridge centreline is about 16.2 mm. This still needs real print evidence; the screen is not a structural guarantee for a thin bridge.
- Small isolated end beads remain on the row base and cap, approximately 0.15–0.16 mm² each. They are at inactive outer ends, not the two active coupling positions, but they are recorded rather than called a perfect slice. Cleanup and cap retention remain untested.
- Screw scaffolds appear as connected paths at their selected tab levels; no whole screw/rotor/follower component begins unsupported in the all-layer footprint screen. Actual tab removal, scar depth and adhesion remain unknown.
- The pin bore stays open, with minimum nominal axis-to-material clearance about 0.839 mm. Nevertheless, 22 of the sampled pin layers lack an enclosed footprint loop and two critical layers retain roughly 0.207-mm outer-midwall gaps. Setting seam gap to zero did not remove those two gaps. **This prevents a READY claim.** No further profile or thread modification is hidden in the delivered file.

Original and reopened G-code are not byte-identical. Independent comparison finds a maximum per-layer nominal deposited-footprint difference of **1.227%**. Segment counts/order and small geometric choices differ; both archives receive separate object/path reports. This is reported as a limit rather than presented as exact toolpath reproducibility.

## Repository validation and delivery integrity

Python sources compile. Model checks, mesh/phase reviews, both Bambu slices, ZIP integrity and source/archive coordinate comparison were run. New relative documentation links are checked. Every pre-existing tracked file, including DES-009 and historical owner results, is unchanged.

`./repo check` exits nonzero on six **pre-existing** size-policy findings: atomic objects E-266, E-283, E-286, E-288 and E-293, plus owner-print-tests/AGENTS.md. Running the same check in a clean worktree at baseline 1071f 695b 93951246a 2865038e 7fb 9de 9bdf 2a 05 yields the identical six findings. They are not fixed in this unrelated task. No new E-304 structure/reference finding is introduced.

The experiment is delivered on a review branch and draft pull request. Nothing is merged into main, and no physical validation or further development is authorized by producing the files.
