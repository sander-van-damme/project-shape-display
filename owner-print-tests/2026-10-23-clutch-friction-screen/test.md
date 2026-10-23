# Print test — selectable-clutch friction screen

**Status:** DEFERRED — technically prepared and independently slice-verified; not added as a fourth READY job.  
**Priority:** none; no deadline or scheduled printing.  
**Last reviewed:** 2026-10-23.  
**Reason:** three existing READY offers remain untouched. This is the single optional physical package commissioned for E-303; its deferral is queue management, not a slicer failure.  
**Technical source:** [E-303 investigation](../../tools/curated-experiment-checks/E-303/engineering-report.md).

## 1. Why this test?

Can a small friction face give a useful difference between low-preload drag and loaded slip torque, without erratic grabbing? Analytical friction coefficients cannot answer that. This one reusable hand rig compares a pitch-sized annulus with a larger reference, including two identical nominal followers and two guide-clearance alternatives. It measures a **mechanical normal-force proxy**, not an electromagnetic or electrostatic actuator. There is no screw pin in this print: the E-295 thread geometry is not reinvented and its torque remains to be measured separately.

Stop at one finite comparison: plain PLA control, then steel against PLA; optionally PET on the 10-mm face if film is already available. Do not construct or energize a high-voltage circuit. No additional print series is automatically authorized. [Assembly and measurement drawing](images/assembly.svg).

**Decision:** a resolvable low-drag/high-grip window would justify the owner considering an actuator force test. Similar ON/OFF readings, erratic stick-slip, fast wear, or no useful torque within 50 g added load would weaken the friction-clutch proposal. An insensitive instrument gives an inconclusive result, not a pass.

## 2. Print package

Open **[clutch-friction-screen.3mf](clutch-friction-screen.3mf)** directly in Bambu Studio. CAD compilation and setting entry are not required.

| Included object | Count | Identification / dimensions |
|---|---:|---|
| Base | 1 | 28 × 28 mm; Ø6 boss; fixed Ø2 guide bore nominal Ø2.2 |
| Small input | 1 | Ø22 handwheel; raised contact OD4.7 / ID2.4 mm |
| Large input | 1 | Ø22 handwheel; raised contact OD10 / ID5.4 mm |
| Tight follower | 1 | One raised pip; guide bore Ø2.2 mm |
| Nominal followers | 2 | Two pips each; Ø2.3 mm; physically identical geometry |
| Loose follower | 1 | Three pips; Ø2.4 mm |

All bores are **CAD diameters**, not promised printed clearance. For an actual Ø2.0 guide the intended radial gaps are 0.10 / 0.15 / 0.20 mm. Each follower has a Ø22 body, centered weight cup and two opposing eyelets at nominal 20 mm radius. Measure the real perpendicular force arm. The full fixture does not fit the pin pitch. Only the small 4.7-mm contact face is within a 5.08-mm center spacing, leaving nominal 0.38 mm between neighboring contact circles; this says nothing about the actuator/housing fit.

**One plate:** approximately 93.5 × 78 mm; seven objects, none tall/slender. Bambu Studio **02.08.02.61**, X1 Carbon, 0.4-mm nozzle, Generic PLA, Textured PEI Plate. Initial saved slice estimates **8.52 g / 1 h 19 min 1 s total**; reopen/reslice **8.52 g / 1 h 19 min 5 s**. These are slicer estimates, not physical observations.

| Actual saved setting | Value |
|---|---|
| Layers / first layer | 0.16 / 0.20 mm |
| Walls | Arachne; 3 loops; nominal width0.42; inner0.45; first0.50 mm |
| Infill / solid skins | 20% gyroid; 5 top / 5 bottom layers |
| Speeds | outer20, inner30, first20, top20, infill50 mm/s |
| Acceleration | default1000; outer/first500 mm/s² |
| Supports / raft / brim | OFF / 0 / none; no support contact on specimens |
| XY / hole / elephant-foot compensation | 0 / 0 / 0 mm |
| Cooling | first layer fan0; full100% from layer2; slowdown enabled,8-s target,20 mm/s minimum |
| Temperatures | nozzle210°C; textured bed55°C, initial and later |
| Order / orientation | by layer; all parts flat as delivered |

Saved complete settings: [metadata/saved-settings.json](metadata/saved-settings.json). Reopening without outside presets preserved every project-setting value. The two G-codes are **not byte identical**: seams/toolpath ordering and estimates differ slightly. Both passed the same independent feature checks; see [verification](verification.md). No thread or long unsupported bore exists in this coupon. Real bed adhesion, face flatness and friction remain unknown. Inspect actual printed parts before using them.

**Layout:** root holds the 3MF and instructions/results; `components/` holds the plate STL and seven separate STLs; `cad/rig.py` is parametric CAD; `scripts/` builds/reviews; `metadata/` holds settings/provenance; `images/` holds assembly and toolpath SVGs.

### Extra parts — nothing has been purchased

| Item | Quantity for this manual test | Requirement |
|---|---:|---|
| Smooth steel rod | 1 | Measured Ø2 mm, length30 mm, straight/deburred; plain shank rather than threaded contact |
| Tape or a small amount of adhesive | as needed | Fix rod in base; optional washer attachment only; keep off friction faces and guide |
| Tangential force gauge | 1 | Prefer resolution≤0.001 N; a 0.01 N gauge resolves only0.2 Nmm at20 mm and is usually insufficient here |
| Small mass scale and centered weights | 1 + handful | Weigh follower/washer assembly and increments0,5,10,20,50 g; use nuts/washers fitting cup without touching guide |
| Steel washer, optional first metal test | 1 each size | M2 DIN125 nominal2.2×5×0.3 mm; M5 DIN125 nominal5.3×10×1 mm; inspect actual size/flatness/material |
| PET film, optional | small scrap | Known thickness, preferably12–25 µm; use10-mm reference first; adhesive is included in stack and recorded |
| Thread, ruler/caliper, fixed support | as needed | Fine low-stretch thread to eyelet; tangential force; keep small parts away from children |

The rod, follower guide and base are explicit test supports; there are **no hidden ball bearings**. Manual assembly has base + input + follower + rod (four bodies), optional metal washer and adhesive (counted separately), external weights and gauge. Two rotating bodies are input/follower; the fixed guide supplies radial reaction. Only one of the four followers is assembled at a time.

An energized magnetic test would additionally need the separately specified standard steel core/return pieces, copper coil, current-limited low-voltage supply, current and temperature measurement, and an independently supported armature. They are **not supplied or validated by this 3MF**. An energized electrostatic test would require a properly engineered enclosed, current-limited HV source, insulation, voltage-rated switching/bleeders and verified discharge; this manual protocol does not request one.

## 3. Assembly and finite procedure

1. Print only if you choose to. Let parts cool; inspect flat faces, intact cup walls and open eyelets/bores. Record cleanup. Do not drill a binding nominal guide bore and still call that the original fit result. Test the loose follower instead. Remove loose debris; do not polish away the comparison unknowingly.
2. Fix the Ø2 guide vertically in the base with a removable adhesive/tape joint. Check perpendicularity; no metal burrs. Fit the small input and rotate it freely on the base boss. The base's friction affects hand effort, not the independent output reading when input rotation is maintained.
3. Fit each unloaded follower. Select the loosest version that does not visibly rock; retain both nominal samples for comparison. Check that the cup/added weights do not touch the guide. No follower is attached axially: it rests under gravity on the input contact ring.
4. Start PLA against PLA. Weigh the complete follower (and washer/film if fitted), recording to the actual scale resolution. No added mass is the **OFF proxy**: its own mass still preloads the contact. Total normal load is approximately `N = 0.00980665 × total_supported_mass_g` when the guide is vertical and no extra vertical force is applied.
5. Hold the input fixed. Pull a level thread tangentially from an eyelet with the gauge at measured arm radius. Slowly increase force until the output starts moving. Record peak, direction and minimum resolvable value, three repeats each way. This **breakaway reading includes journal resistance** and is an upper bound on interface-only static drag; do not subtract an invented tare.
6. With no extra load, hold the output via the gauge and turn input by hand at about one revolution per5 s for three revolutions. Record force range and erratic jumps. The journal can share the reaction, so the gauge reading is conservative available output torque, not a pure friction-coefficient measurement. Maintain the same thread height and avoid tilting. If it rocks or rubs, mark invalid.
7. Add centered5,10,20 g, repeating step5–6;50 g maximum only if assembly remains flat/stable. Record actual total mass. Keep the output restrained and verify the input can continue turning by hand. This demonstrates slip in this coupon only; it does not prove a shared transmission cannot stall or that a finger is safe.
8. Repeat no-added-mass reading after load removal. Make only20 slow revolutions at the chosen highest stable load, inspect wear/debris, then repeat no-load and one loaded reading. Stop for heating, scratches, tilt, sudden grabbing, permanent damage, binding or adhesive migration.
9. Repeat the key low/high load points on the second nominal follower. For steel against PLA, center and attach the matching washer under the follower so only its clean lower face meets the printed ring; adhesive must not protrude. A M5 washer needs careful visual centering (its hole is larger than the guide). Measure eccentricity and reject visible overhang/edge-only seating. Record changed total mass and any washer rocking. The larger inner diameter of the10-mm test is intentional.
10. If already available, bond a known PET film to the10-mm input ring, trim to both annular boundaries, keep adhesive beneath it and record the full stack. Repeat only the key low/high points. This tests tribology/attachment, **not electroadhesion**. Do not trim film while installed around fingers or rod.

Keep every gauge reading and the guide/tilt observations. Reverse directions to expose bias. A conditional side-load estimate is `Tguide ≲ μguide Fgauge × 1 mm` for a2-mm guide; even with μguide=1 this can be5% of a20-mm gauge moment. That is **not a certified uncertainty bound**: a wedged/tilted follower can be much worse. Strong clearance/direction dependence invalidates a pure interface conclusion. There is no claimed perfect tare method here.

### Torque and resolution

`T [Nmm] = F [N] × actual perpendicular arm [mm]`. A1 mN force resolution gives0.020 Nmm at20 mm;0.1 mN gives0.0020 Nmm. The mass of a typical printed follower may alone produce less than0.01 Nmm, so low-preload results can fall below the instrument limit. Write **“< resolution; unresolved”**, never zero torque. A mass scale is for normal load; it is not automatically a horizontal force gauge.

If using hanging torque weights instead, route thread horizontally through a **freely turning, independently calibrated pulley** at eyelet height, then down to the mass. Do not drag thread over a table edge. Ideal moment is `T[Nmm]=mass_g ×0.00980665 × arm_mm`:0.1 g at20 mm gives0.0196 Nmm;10 mg gives0.00196 Nmm. Weigh the thread/hanger too. Pulley breakaway and bearing losses must be separately bounded at the same small tension and in both directions; otherwise report only an instrument-limited estimate. Prefer the gauge if it can resolve the required force. No pulley is hidden in the printed BOM.

Before declaring a useful clutch window, compare the **resolved** loaded conservative torque to an independently measured starting torque of the existing screw under the intended load; this package does not supply that missing number. No force/torque threshold is called a finger-safety limit. Slipping dissipation is `P[W]=T[Nmm] ×0.001 ×2π × rpm/60`; the slow manual test is not a high-speed thermal qualification.

## 4. Owner results

Use [results.csv](results.csv), or fill below. An empty field means untested.

- Date: ___ ; actual project printed / changes: ___ ; printer/PLA/bed: ___
- Print success: [ ] yes [ ] partly [ ] no [ ] not printed
- Actual guide diameter / straightness: ___ ; chosen follower and measured bore: ___
- Instrument model / resolution / calibration and actual arm: ___
- Surface pair / washer dimensions / PET+adhesive thickness: ___
- Follower assembly mass / scale resolution: ___ ; cleanup: ___
- Low/high/load-removed torque readings, directions, repetitions: see CSV.
- Binding / rocking / wear / debris / visible damage / warmth: ___
- Input continued rotating with blocked output? ___ ; limits/confounders: ___
- Two nominal samples compared? ___ ; photograph (optional): ___

## 5. Interpretation after owner feedback

**Physical result:** unknown. **GO / NO-GO / further owner choice:** not made. The print pack, successful slices and arithmetic are not physical evidence that a clutch works. The task stops with this prepared test; no reminder, deadline, purchase or automatic follow-up is created.
