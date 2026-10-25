# E-304 — guided 2×2 row/column cone clutch

**Status:** DRAFT — genuine X1C project saved/reopened/resliced, but retained pin wall paths contain up to 0.207-mm discontinuities at two critical layers. Do not print as a READY job; see the engineering verification record.

**Priority:** none. **Reviewed:** 2026-10-25.

**Source:** [E-304](../../06-experiments/E-304-guided-full-length-row-column-clutch.md). DES-009 remains the primary design. No print is scheduled and no purchase is requested.

## 1. Why this test?

**Question:** can four properly guided, friction-coupled screw pins engage from stationary arbitrary initial phases, drive from one common input, isolate half-selected neighbors and release at the same follower setting?

The cone has no ideal tooth-phase obstruction. Its printed friction, guide drag and elastic preload cannot be established by CAD. Earlier owner feedback demonstrated wobble, bent selectors and blocked tooth contact, but only one coupled pin. This experiment tests the complete interaction of four cells at the actual 5.08-mm pitch. It does not qualify 80×80 hardware.

**Decision:** continue only if all four cells repeatedly engage and release without touching their couplers, while an obstructed output does not stop the others. Owner feedback decides whether further work is worthwhile. Stop at binding, visible spring whitening, cracked feet, gear skipping, permanent bending, a stuck cone or unselected pin motion. Do not overcome a jam with pliers or a motor.

## 2. Prepared print

Primary project: [guided-matrix-clutch .3mf](guided-matrix-clutch.3mf). Open it as a project; keep its saved placement and orientation. **Do not auto-orient.** No CAD compilation is required. Review [plate map](images/plate-map.svg), [sections](images/sections.svg), [assembly/exploded view](images/assembly-exploded.svg) and [selection states](images/selection-states.svg).

One plate, 33 named objects: one fixed frame; two lower and two upper shared keepers; two row bases and two caps; two columns; four nominal followers plus one thinner and one thicker sample; four nominal input rotors plus one loose and one tight sample; one two-rack shuttle; one hand pinion; four supported output screws in one scaffold object; four terrain pins; one 100-mm beam and two supports. Four screw scaffolds are intentionally separate connected bodies inside one named object. The frame also has two thin sacrificial rods under the stationary follower guides and eight transverse sacrificial rods outside the working raster. Cut their tabs/end contacts and remove all ten rods before assembly; they support print bridges, not the working mechanism. Remove sacrificial screw bases, eight small tabs per screw and side struts after printing. They are not assembled mechanism parts.

Variants are identified by the saved object names and plate map, not tiny unreadable embossed labels. Bag them separately before moving parts: follower-soft t=.35 mm, nominal .40, stiff .45 (depth 3.6); rotor-loose shaftØ1.70, nominal 1.80, tight 1.90. The four nominal copies are the principal 2×2 test. Only change a variant after recording the nominal result.

- **Printer:** Bambu Lab X1 Carbon, 0.4-mm nozzle; Bambu Studio 02.08.02.61. Generic PLA, saved profile inherited from the completed E-295 compact-thread project and official Bambu presets. Exact settings and estimates are in `metadata/slicer-review.json`.
- **Process:** .12-mm layers and first layer, Arachne, two walls, minimum bead 75%, minimum feature 10%;100% zig-zag infill; nominal line widths 0.45 mm. Outer/inner wall speed 15/20 mm/s; first layer 15; bridge 15 with saved 90° bridge direction and 0% seam gap. Nozzle 220°C, textured PEI bed 55°C. Fan 100% after the first layer, auxiliary fan 0, cooling minimum speed 10 mm/s. Acceleration 1000 general/500 outer and first layer. Supports OFF, raft 0, outer brim 2 mm with .12-mm gap, print by layer. XY contour, hole and elephant-foot compensation 0. Cooling/temperatures and all line widths are retained in the saved project and recorded in the review.
- **Orientation:** row caps and columns roof-down; followers flat back-down so ligaments contact the bed; input rotors cone-tip-down; terrain pins closed-top-down/bore-up; output screws upright cup-up on their supplied scaffold; frame and keeper strips laid on their specified sides; row bases and the 100-mm beam base-down. Threaded cavities have no slicer supports.
- **Estimated time/material:** 7 h 34 min 27 s /21.60 g PLA, from the saved slice; not physical observations.
- **Extra items:** ordinary tape for external keeper/cap tabs, fine marker, ruler; optional scale and known small masses. Rods are **not needed** for the 2×2 test. Optional stock for the beam is twoØ2-mm rods about 100 mm long; record material and diameter. Do not buy rods solely because they appear in CAD.
- **Validation blocker:** the nominal pin bore remains open, but two wall layers have unresolved deposited-path gaps. The file is supplied for review, not as a verified printable pass. See [verification](../../tools/curated-experiment-checks/E-304/verification.md). **Validation:** see `metadata/guided-matrix-clutch-build.json`, `geometry-review.json`, `slicer-review.json` and `reslice-comparison.json`. Printability and mechanism performance remain different evidence levels.

The directory also contains component STLs, parametric CAD in `cad/`, reproducible build/review tools in `scripts/`, metadata and SVG illustrations. Engineering STEP/assembly geometry and calculations live under `tools/curated-experiment-checks/E-304/` in the repository.

## 3. Assembly and test

### Assemble without forcing fits

Use the actual [beam/contact section](images/beam-and-contact.svg) to identify reinforcement channels and the [assembly drawing](images/assembly-exploded.svg) for the operating frame after removal of sacrificial rods.

1. Remove brims from outer edges, especially the small cone-tip bed contacts. Cut scaffold tabs at the **strut** first; trim the remaining nub carefully. Keep the six-millimetre working thread region intact. Do not sand every thread or cone until it fits: record any required cleanup first.
2. Hand-thread each retained terrain pin onto its screw and check smooth bidirectional motion independently. At neutral the pin's bottom is 6 mm above the thread's bottom. Only use±1.5 mm around that position. Do not run the pin off its guide or to a hard thread stop.
3. Place the two row bases into the frame's bottom longitudinal openings, handles on the same side. Fit each input rotor flange into its follower's open cage before inserting the pair through the row's open side. Place follower lower cross-feet in the row cam tracks. The upper stem stays in the stationary guide. First row opens toward−Y; second toward+Y. Use the exploded drawing to identify the sides.
4. Lower the two cam caps over the feet. The end bridges lie outside the active field. Tape cap to base at the exposed ends; keep tape out of all sliding faces. Confirm the bottom feet are captured but free. Set rows fully OFF; do not compress springs while installing columns.
5. Insert the two column rails around the follower stems, roof above each upper cross-foot. Insert the four pin/screw assemblies into the open output/terrain guides. The output collar belongs **below** the stationary thrust deck. Fit the paired shared keeper strips into their locating slots and retain at external tabs with tape. Confirm all shafts have two supported journal levels. No keeper may lift during operation.
6. Engage both permanent racks with the four input gears and fit the side hand pinion in its frame hole. Initial gear meshing is an assembly step, not clutch engagement. With all selectors OFF, the single knob must rotate all four input rotors while the four output pins remain still. Mark a rotor/cup if motion is hard to see. If a rack catches, a rotor wobbles visibly or an output drags, stop and record the fit before trying variants. The output collar has 0.2-mm axial play; record any height jog on closing. Adverse radial/tilt/axial clearance combinations can rub even though the nominal CAD clears.

The sliders have 2.54-mm travel between corresponding low/high cam dwells. Mark the OFF and ON end positions with a ruler; handles move toward the positive CAD axis for ON. Do not keep moving through successive cam periods. A10° knob notch ideally moves a selected pin 0.25 mm. The delivered fixture is a short-stroke hand demonstration: keep every pin within±1.5 mm of neutral. Mark a rack travel window from−9.5 to+2.8 mm relative to its CAD assembly position (at zero, the rack right end projects about 12.9 mm beyond the frame right edge). Stay inside that window to retain the side-pinion mesh; the knob is not a continuously rotating unlimited-travel drive.

### One focused evidence sequence

1. **Logic and isolation:** with input stopped, choose columns, then rows. Check each of the four single cells, each pair in one row, each pair in one column, and all four. Also turn the common input with rows ON/columns OFF and rows OFF/columns ON. Only row-AND-column intersections may move. Record each failed/unknown state; the 16 selector masks are listed in `images/selection-states.svg` locally as the four cell truth cases and in `metadata/geometry-review.json` as full 2×2 masks.
2. **Stationary phase engagement:** set outputs at neutral and the rack about 8.5 mm left of its zero mark. The twelve phase positions then span−8.5 to about+1.87 mm, leaving room for the short forward/back test. With clutches OFF, advance the common knob one 10° notch to change input phase 30°. Hold the knob still, select, then test one notch forward and back. Return selectors OFF. Repeat through 12 input phases spanning a full rotor revolution, initially one cell and then all four. Do not wiggle the knob, push a cone or spin an output to help seating. Record “needed wiggle” as failure of stationary engagement, even if it subsequently drives.
3. **Different phases simultaneously:** use individually selected moves to leave the four outputs at different phase/height offsets (e.g .0, 30, 60, 90°; never exceed stroke limits), then return the shared input to the same mark with clutches OFF. Engage all four from rest and move forward/back one notch. This tests independent contacts rather than four artificially matched pairs.
4. **Load, reversal and release:** first use free-running pins. If a scale is available, place one protruding pin against it with the other pins clear and increase axial resistance gently to approximately 5 g then 20 g indicated (.05/.20 N). Record orientation, actual scale reading and other contact/friction; this is an approximate axial-load test, not a torque measurement. Without a scale report finger resistance as qualitative. At each setting move in both directions, return rows OFF and verify the input turns without moving outputs. Also observe loaded OFF pins for about 10 seconds: no holding brake is included, so gravity-driven descent is possible. Record slow drift; stop for rapid falling or uncontrolled motion. Try a gentle column-only release once and record its force/behavior; normal operation unloads rows before changing columns.
5. **Obstruct one:** restrain one output lightly while all four are selected, turn only far enough to see whether the other three move and the restrained clutch slips. Stop if rack teeth skip, frame flexes, spring whitens or force rises sharply. Return all rows OFF and check release. A blocked output differs from a jammed cam. Do not insert a hard foreign object into the moving rack to simulate a jam.
6. **Repeat and inspect:** at least five cycles per sampled phase if the first pass works (record the actual count). Note settling, wear dust, changed force, permanent follower set and loose keeper/cap tape. Repeat only the failed comparison with one labelled fit/preload variant; changing several variables together obscures the result.

**Optional beam check on the same plate:** orient the 100-mm beam as in the assembly (deep section vertical), supports 50 then 75 mm apart. Apply a known central load (e.g .100–300 g), measure midpoint deflection relative to unloaded height, and remove load. Repeat with two loose rods in the channels. Record support span, load, measurement resolution and whether any permanent set occurred. A ruler may only bound deflection; do not report unresolvable hundredths of a millimetre. Bonding rods changes the experiment and must be recorded separately. Loose rods do not establish full-composite stiffness.

**Single continuation result:** all four guided cells repeatedly engage at sampled stationary phases, transmit the chosen light/moderate load in both directions and release at one common follower setting, with half-selected cells still and one obstructed output not stopping its neighbors. That is a physical result to seek, not a pass already obtained. A failed assembly or missing test is also useful evidence; no additional print is automatically authorized.

## 4. Owner results

Use [results.md](results.md); blank means unknown. Include the actual printed 3MF if settings/orientation changed. Photos/video are optional.

## 5. Interpretation after feedback

**Physical observations:** none yet.

**GO / NO-GO:** undecided.

**Next action:** await the owner's explicit decision; no further development, issue, purchase or print campaign is initiated.
