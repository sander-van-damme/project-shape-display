# Resident C-guide integration study

15 October 2026. This is a **conditional construction study**, not released whole-machine fabrication CAD or physical validation. It answers whether stationary resident memory can positively retain both actuation functions without thousands of compliant mask readers. The surviving answer is mechanically explicit, but requires thousands of small metal sliding interfaces, nearly 300 mm of vertical depth, and an unqualified joining/assembly process. It does not establish the product cost or reliability target. **Subsequent independent review found an admitted angular pose that jams the nominal dog against its pin. The frozen dimensioned embodiment therefore FAILED its angular-clearance guarantee. The separately named1-mm-guide/0.35-mm-penetration variant removes the tested planar failures and is the preferred conditional next study; it still has no vertical unloading margin after guide play. See [guide-escape.md](guide-escape.md) for the counterexample, independent finite-pose result and unresolved transfer/packaging limits.**

## Decision

Retain the **direct captured C-guide** topology as the strongest integrated form of the two-bank pulse concept. Park the earlier tall perforated mask with a separate compliant A reader: its blocked-reader forces and positive dog keeper were unconstructed. The replacement uses each stored bit to position a tall bilateral channel. Two T-feet slide independently in that channel: one carries the lift dog; the other operates the grounded-pawl release ramp. Both feet receive positive lateral constraint from the same retained channel, while their vertical movement remains independent. There is no logical inversion of A and B and no private motor or solenoid at a cell.

The CAD does **not** establish a buildable affordable complete display. Its weakest remaining interfaces are the tiny key guides and channel manufacture/joining, tolerance-dependent neighbor clearance, force-controlled support transfer, and the powered row/codebar assembly. A small adjacent-cell metal or enlarged mechanism test would change that decision; a full print of these nominal metal sections would not.

## Coordinate system and dimensions

Pitch is 6.35 mm in X and Y. Each bank has **64 X columns × 32 Y rows**, 2,048 sites. The A and B ladders each have 64 rails running in Y over approximately 203.2 mm; they join outside the active field. The row cassettes run in X below the terrain tails. The1-mm cassette in the cell CAD is a local interface plate, not a qualified406-mm beam: an end-supported steel strip of that section carrying~1.3 N of channel weight would deflect about12 mm before acquisition inertia. Distributed lifting or a stiffened cassette section and its fixed-floor clearance must be engineered; the row transmission is explicitly not released. Each of the 64 column setters drives a mechanically paired upper/lower set of Y-running code bars, each with **32 discrete acquisition pockets**, not an ineffective longitudinal slot. Two banks therefore retain the timing model's 32 addressed rows and 64 parallel data setters per bank.

| Interface | Nominal dimensions / location, mm |
|---|---|
| Terrain tail | 2.8 X × 2.4 Y; local Z −85 to45 |
| Broad upper body | 4.8 ×4.8; Z45..135 plus terrain height |
| Cap | 4.8 ×4.8 ×1.2; low top136.2, high top186.2 |
| Fixed upper guide planes | Z100 and130; assumed0.20 total hole clearance; complete plates not released |
| Ground pawl | Nose0.8 X ×1.2 Z; seated topZ1.2; groove faceY−1.2 |
| Rack | Grooves3.2 Z high,0.65 Y deep,1.0 X wide; centres−0.4 mod5 |
| A dog | Nose0.8 X ×2.6 Z;0.5 nominal depth overlap; centre homeZ−30.4 |
| A movement | Largest commanded pulse20; signed stroke with additional take-up/backlash movements |
| C-guide | Outer1.6 X ×2.4 Y; length136; bodyZ−104..32 |
| C-guide cavity | 1.0 X ×1.7 Y; front mouth1.0 Y |
| T-foot | 0.5 X ×1.5 Y;0.25 capture overlap per side;±0.10 Y play |
| Bit displacement | 1.60 Y; common A displacement0.85 Y |
| Guide centreY | ON/A engaged−2.20; OFF/A engaged−3.80; withdraw A subtracts0.85 |
| Ground release |0.85 Y from1.20 B Z stroke;0.35 approach plus0.85 ramp motion |
| B follower | Rounded fixed nose diameter0.40; not a bearing at every site |
| Ground spring | Reference steel leaf1.2 X ×0.4 Y ×40 Z; rigid seat carries vertical terrain load |
| Metal ladder rail |0.4 X ×20.45 Z for A;0.4 ×20 for B;203.2 Y bank span |
| Key guide |0.35 X key in0.45 slot;0.5 Y bearing length;0.10-mm wall/0.15-mm lip details |
| Positive bit registers | Lower atZ−104, upper atZ30; two pockets per register;1.2 engagement |
| Row acquisition |2.0 Z, releasing both end registers together |
| Writer | Upper barZ34.4..37.4; lower barZ−98..−95;0.6×0.6 pockets,0.4×0.4 lugs;1.6 Y motion |
| Paired writer links | Reference2.5 X ×3.5 Y ×133.4 Z steel at exterior bank ends; guided phase/assembly not released |
| Fixed spring roots | Z40, above B ladder and writer |
| Overall occupied height | Memory underside−107 to high cap186.2: **293.2 mm**, before enclosure/base |

The precision metal dimensions are an honest warning about construction cost. They are not ordinary FDM tolerances. Finer5.08-mm pitch is **not** packaged by this study; scaling the numbers down is not justified.

## Power, selection and support paths

**A lateral engagement:** the common A subframe carries both lower and upper bit registers, row cassettes, codebars and stored channels. It moves0.85 mm in Y. For an ON bit, the T-foot takes the dog from0.35 mm clear of the pin face to0.50 mm engagement. An OFF bit is1.60 mm farther withdrawn and never enters the rack. The moving dog remains positively captured by the C-slot throughout its vertical excursion. Terrain load goes from rack to dog, key guide, longitudinal rail, exterior ladder frame and bank drive. C-guide lips carry lateral reaction, not the principal terrain weight. The common A subframe itself must be positively held in its engaged pose by a common latch/cam or equivalent arrested drive; T-foot capture is not enough if the entire selection frame can retreat. That common hold and its load capacity are not released in this CAD. An energized selector coil is not credited as anti-drop support.

**B release:** the B T-foot follows the same bit position, above the A travel. A separate B ladder descends1.20 mm. Its ON nose approaches the grounded pawl's45° ramp for0.35 mm, then retracts the pawl0.85 mm. OFF noses miss their ramps. Raising B lets the ground springs restore their pawls. The grounded pawl sits on a rigid shelf immediately outside the pin; only the short nose overhang bends under vertical terrain load. Its long leaf supplies lateral return bias.

The B ladder is above its T-foot so it does not intersect the A ladder at its highest pose. Codebars sit above the B ladder; fixed pawl roots sit above those codebars. This is why a compact-looking local sketch grows into the documented293-mm stack. Ordinary X crossbeams through the central channel field collide with channels or terrain tails. Ladder end connections outside the field are required; they are not drawn as nonexistent internal bridges.

**Channel backing:** both ends are positively registered in OFF/ON pockets while lifting. A long free-Y slot would not suffice: a channel could move toward the other bit under lateral force. Both end feet rise from their pockets together during writing. The middle channel section is a steel beam between these registers. Plain PLA at these dimensions is rejected by the deflection screen.

## Row writing without ghost intersections

At A withdrawn, every A dog is clear and B is raised. Set the64 paired codebar sets to the addressed row's OLD pattern at BOTH ends. Raise only that row's cassette2 mm. Its upper and lower lugs start entering their discrete codebar pockets after0.4 mm; both positive registers release after1.2 mm, leaving0.8 mm nominal acquisition overlap. Move both codebars in each pair together to NEW data, then lower the cassette and reseat both end registers. Other rows' lugs stay0.4 mm below the bars and cannot be moved by them.

The earlier TOP-only writer is rejected: after both end registers release, a short top lug does not prevent the channel tilting while its bottom stays OLD. It could reseat inconsistent bits at the two ends. The added bottom codebar directly commands the lower lug, with the same electrical actuator through external paired links. Both OLD acquisitions must agree before either end register releases. The lower bar sits outside the channel in X and above the fully raised cassette, so it does not cross the cassette X beam.

Discrete pockets are essential because these bars move along their own Y length. A continuous longitudinal channel would let the lug slide freely instead of setting it. This is a different physical codebar from the small continuous-channel memory coupon. Its friction, acquisition yield and80-ms full-row transaction are untested.

The CAD shows cassette shoulders and register feet. It does not release the32-row selector/indexer, cassette external guides/returns, common-frame bearings/actuators, or codebar supports and powered acquisition mechanism. Simultaneously releasing both end registers without skew is an actual remaining task. Wrong OLD data should obstruct acquisition, and must not be forced.

## Coherent bidirectional support sequence

The drawing uses a seated pin height0 with the ground-pawl topZ1.2 against the groove's upper surface. A dog at home−30.4 is centred in a groove with0.30 mm clearance on each vertical flank. Let d be a positive commanded terrain increment.

1. Write mask with A withdrawn and B raised. Move common A to engage selected dogs. Other pins remain on their original ground pawls.
2. Raise the A ladder0.40 mm:0.30 closes dog backlash,0.10 raises selected pins and unloads their ground pawls. Lower B to release only those pawls.
3. For an upward pulse, raise A by d. Restore B, then lower A0.70. A free pin seats after0.10 and the dog crosses the remaining0.60 backlash; a sticky pin remains0.10 high until the dog crosses0.60 and then positively pulls it down0.10. Raise A0.30 to centre the dog, withdraw A and return the empty ladder by d.
4. For a downward pulse, lower A by **d only**. A freely following pin ends0.10 mm above target; a sticky pin reaches the opposite dog flank and can end0.70 mm above target. Restore B while both limits still permit pawl insertion. Lower A0.70: the free pin seats after0.10 and the dog then crosses its remaining clearance; the sticky pin is positively driven through0.70 to its seat. **Raise A0.30** to centre the dog, withdraw A, and return the empty ladder by d.

A previous proposal to command−(d+0.60) before restoring the ground pawl is **rejected**: it handles a sticky pin but puts a free pin0.50 mm below target, preventing pawl insertion. Both limits must be modeled. The earlier UP seating−0.40 is also rejected: it centres the dog but does not positively pull a sticky pin through its last0.10 onto the ground pawl. The robust nominal sequence uses the SAME post-grounding−0.70/+0.30 for both signs. Simply commanding−d and assuming gravity follows is incorrect. Restoring the ground pawl at the wrong point and then lowering a hard dog beyond contact can crush or jam the support. The nominal0.10 insertion allowance is not a qualified error budget: printed rack error, frame flexure, groove wear and elastic load changes can consume it. Controlled-force seating or a designed compliance/load-limiting element is still needed. Thus this sequence closes the kinematic accounting but does not constitute a support-transfer pass.

For a cell initially at height h, the engaged A groove's pin-relative coordinate is **home−h** and stays constant during the pulse because dog and pin move together. It is wrong to multiply independent terrain and carriage envelopes. For H50, the A acquisition centres occupy−80.4..−30.4; ground centres−50.4..−0.4. Each separate face would need H of groove range; this one-face version uses their union, H+|home−ground phase|=80 mm, plus groove and end margins. Empty withdrawn dogs may pass below a high pin's tail. The fixed C-guide, however, must cover the entire moving-foot excursion.

## Manufacturing and assembly

See [resident-manufacture.md](resident-manufacture.md) for actual masses, force and stiffness screens, repeated interfaces, assembly closures, cassette stiffness and the bank-junction failure. These are unresolved construction obligations, not free infrastructure.

## Reproduction and result classification

Frozen CAD SHA256: `780423514ddddcf11fb456d94cdb64d852cbc42908f92bf5494faaf326dda157`. The original and separately named bounded guide variant each have270 centred nominal checks, including two deliberately obstructed wrong-OLD cases. Fifteen basic component meshes are watertight and single connected bodies. These are nominal geometry checks, not a fabricated assembly result.

From the repository root, run `python 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/check_resident.py` with OpenSCAD, NumPy, trimesh and manifold3d installed; it exports component meshes, checks nominal interference pairs and writes `checks.json`. Run `python 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/draw_resident.py` for the dimensioned section PDF/PNGs. Source is `cad/resident_cell.scad`; exported meshes are analysis products, **not ready-to-slice owner print jobs**.

Computationally demonstrated: connected nominal cell solids after review fixes; row addressing geometry at the sampled states; T-foot positive-capture dimensions; corrected signed kinematics; material/beam sensitivity; explicit resident part inventory. Supported by physical measurements: **none of this integrated mechanism**. Failed: the frozen embodiment's angular-clearance guarantee, thin unsupported PLA channel stiffness, top-only writer constraint and the earlier simplistic compliant-reader construction claim. Unresolved: tolerance/yield, contact force and wear, powered row write time, support-transfer margin, joining/repair method, complete frame/actuator integration and cost. D&D walls/corridors remain separately failed or unresolved as in the main DES-008 report.

The appropriate decision boundary is a small neighboring-cell captured-guide/ramp and support-transfer test with known loads and deliberate clearance variation, followed by a powered pocketed-bar row write. Do not order a full channel array or print hundreds of these sections on the strength of the model.
