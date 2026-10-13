---
status: complete
builds-on: [E-272, E-271, E-255]
---

# Common rack drive: fewer motors, paid reset and phase compatibility

**A translating rack removes sixteen private motor/belt routes, but retains sixteen selective docking channels and adds substantial empty travel. Park this construction before gear/selector detail.** Its favorable coarse bought allocation is $1,116 versus E-271 bare16 $1,247, while the conditional worst four-square S50 reveal grows from E-270's 28.84 to **40.99 seconds**. Longer waits are permissible product tradeoffs; this modest saving with unresolved docking and a roughly 839-mm swept machine width does not currently earn development priority.

Reproduce `python3 tools/curated-experiment-checks/E-273/rack.py --check`; omit the flag for all workloads, allocations and sensitivities. Evidence is **calculation, bounded envelope checks and ideal state replay**, self-reviewed. No measured gear, process margin, safe RPM, reader, purchase or print follows.

## Changed physical construction

A single guided translating rack turns sixteen parallel pinions at adjacent cell pitch. Each pinion, shaft, tip and bearing carrier translates axially by 3 mm to dock only selected resident screws. A broad rack face stays meshed through that travel; there is **no sliding torque spline, private drive motor, private belt or local clutch**. Offset solenoids lift narrow horizontal carrier arms. Four coarse/five fine lanes put their wide bodies below all arms, avoiding E-271's neighboring motor/shaft conflict. Selection is independent; rotation is common and reversible. Different signed heights require stopped groups.

The resident load path remains pin → thread → screw collar → opaque bed → frame; the keeper reacts docking uplift. Unchanged screws are not deliberately docked or turned. There are still **4,096 / 6,400 resident pin–screw pairs, socket/thrust sites and keeper openings**, 8,192 / 12,800 guide apertures and the inherited 126 / 158 two-layer ribs. E-269's fine-frame and loaded-support uncertainties remain. No resident marks, optical bores, brakes or extra latches are added.

Shared ledger: one rack/drive/encoder and two rack-guide duties; sixteen pinions, shafts/tips, translating carriers/arms, selectors/returns; 32 bushings, docking guides, stops and switch duties. XY adds two drives. Rough wiring allocation is six conductors/channel plus six for the shared drive: 102 conductors / 204 end terminations before shared buses, versus E-271's up to 192/384. This is a count, not routed wiring. Selection still consumes the inherited **88-W all-on arithmetic**; duty/temperature and pull-force curves remain unqualified. One motor does not mean one actuator.

Necessary geometry assumptions: 4-mm pinion pitch diameter, 5-mm outer envelope, 2-mm tooth face, 6-mm rack face, 4.4-mm carrier width, independently bounded ±e faces. At e=.2 mm:

|Necessary clearance|6.35-mm pitch / 64²|5.08-mm pitch / 80²|
|---|---:|---:|
|Neighboring pinion envelopes|.95 mm|−.32 mm|
|Neighboring carrier envelopes|1.55 mm|.28 mm|
|Axial mesh reserve after 3-mm docking|.60 mm|.60 mm|
|Parked tip / intended insertion|.60 / 1.60 mm|.60 / 1.60 mm|

These are **bounds, not printer distributions**. Fine pitch fails this gear envelope under e=.2; do not repair it with smaller teeth. Coarse selection boxes have no cross-channel overlap at four lanes, with 120-mm longest arm and a 150-mm Y reservation; fine needs five lanes/150-mm arm/180-mm Y. Gear/rack contact is intentional and not tooth-profile CAD. Rack guides, arm stiffness, fork/bearing thrust, attachments, backlash, radial contact, mesh force and harness bends are unconstructed; within-channel overlaps reserve interfaces rather than prove them. At e=.6 the axial mesh reserve becomes negative.

Manufacturing alternatives are machined/reamed shared plates, cut shafts, and outsourced pinion/rack stock or tooling. The assumed diameter is **not a sourced available gear**. Molding/casting sixteen shared carriers may reduce handling only if shrinkage, release and finishing work; it does not solve resident thread manufacture. No demand for thousands of precision inserts follows. Park and secure the board before withdrawing the head for bench service; resident pair replacement retains the unloaded/openable-bed procedure.

## Finite transaction and phase constraint

At a station, all tips are parked before seeking. Let A be the largest upward delta and B the largest downward magnitude. Start with rack at zero; with every tip disengaged, preposition by `max(B−A,0)`. Select positive movers, stop at each ascending height threshold and retire finished tips. Then select negative movers and stop/retire similarly. Finally park all tips and return empty by `max(A−B,0)`. Distances here are height-equivalent; multiply by `π D / lead` for rack travel.

Every selected cell moves monotonically to its target in the ideal replay; unchanged cells remain unselected. The rack stays in `[0,max(A,B)]`, and the complete travel is **2 max(A,B)** in height-equivalent units. Balanced signs eliminate empty return but require both signed loaded sweeps. A dense same-direction move pays an equally long empty return. It is not a free continuous power bus.

With D=4 / lead=3, S40/S50 need **167.55 / 209.44 mm rack excursion**. Sixteen coarse outputs need 282.80 / 324.69 mm toothed stock including a 20-mm end allowance; rack swept unions are 450.35 / 534.13 mm. Combined with full-board XY access, the X reservation is **755.15 / 838.93 mm**, before enclosure or additional stops. Compactness is secondary, but travel and mass must be counted. Lead2 makes S50 excursion314.16 mm.

**Rigid socket phase is an additional condition.** A common drive cannot independently search sixteen socket angles. For an illustrative sixfold socket, ideal common registration permits heights separated by `lead/6`: .5 mm at lead3, .333 mm at lead2. The inherited 10-mm target increments are commensurate. However, two screw phases corresponding to heights0 and.25 mm at lead3 span30° modulo60°. A common tip angle cannot engage both within an assumed±5° allowance. This exact witness disproves arbitrary simultaneous docking for that rigid interface, not the screw principle.

Commissioning, mounting phase, wear, slip and actual-height correction can break the ideal registration. Retaining an angle grid could be a useful controller restriction, but then nearest-grid height error, actual lead variation and recovery must be assessed. Neither forced engagement nor individual phase compliance is granted. The timing below assumes compatible phases and correct docking; phase search/commissioning is **unbounded**, not paid by a fictional small overhead. Any alternative shared rotary bus inherits this question.

Docking must be proven before rotation; unknown engagement inhibits both rack motion and XY travel. Stop the rack before changing masks. After full retraction, allow settling and fresh identified actual-cap readback. A recoverable stable wrong result may retry from its newly observed height only if phase-compatible; other errors stop. E-270's tested decoder remains rejected, covered caps remain unknown, and encoders do not prove thread/height integrity. Spring return and reported zero-speed screw hold do not establish safe moving power loss or later creep. No hidden-neighbor or load-transfer safety qualification is asserted.

## Complete conditional timing

Reuse the sourced three-map convenience sample and owner-selected physical river/ravine relief; these are not measured typical-play frequencies. S40/N20 uses20-mm depression and20-mm walls. S50/N30 includes shallow20/deep30 software presets. Both grids span406.4 mm; actual physical neutral preparation is charged. The fine-grid rows below are **routing-granted controls despite their failed envelope**.

The same E-267 adjacent interval cover, shorter row/column path,200-mm/s XY,5,000-mm/s² acceleration and50-ms minimum station seek are used. Common handling/reader deployment costs5 s. Each threshold group gets an assumed80-ms docking/retirement/proof slot, then final100-ms retract,100-ms settling and100-ms simultaneous read per station. Rack rotation is capped at850 rpm and by200-mm/s rack speed; rack acceleration limits it to397.89 rev/s². Empty rack moves use the same linear limits. One immediate compatible full-stroke retry is charged. No motion/read rate is physically rated, and unknown faults have no finite completion bound.

Seconds; entries **S40 / S50**:

|Grid|Four-square reveal max|Scene transition max|Paid neutral prep|Dense one-sign stress|Mixed-sign dense stress|
|---|---:|---:|---:|---:|---:|
|64²|33.43 / 40.99|338.71 / 393.30|372.79 / 487.09|600.50 / 714.79|646.33 / 767.24|
|80², failed envelope|66.73 / 84.96|485.91 / 565.57|574.33 / 752.66|930.11 / 1108.45|1001.72 / 1190.40|

Worst coarse S50 local:150 lowered cells,3,946 unchanged,16 rows/stations. Ledger:5 s common +2.63 seek +2.04 return +11.86 loaded rotation +10.69 empty rack +1.28 switching +4.80 retract/settle/read +2.68 retry =40.99 s. Known preposition only removes1.56 s. Deleting the empty-return term alone would still leave30.30 s **within this schedule**, not a universal lower bound. A loop drive would have its own reversal, tension and selection costs.

Minimum-rest first-map maxima are508.78/623.08 s coarse and767.85/946.19 s fine; paid neutral plus first map gives589.89/724.96 and858.23/1108.17 s. These begin from a known mechanical zero; unresolved homing is not a claimed bounded setup. Dense stress remains separate from the~30-s gameplay reference. Slower updates can still be valuable, but the savings must earn their player cost.

Coarse S50 local/scene sensitivity: lead2 gives52.77/515.84 s;400 rpm gives54.72/538.13;200-ms group switching gives43.03/428.46. Conditional rack-force scenario:16×.35 Nmm tip torque,2-mm pitch radius,.5-kg rack and1e−8 kg m²/output inertia at5 m/s² give2.8+2.5+.2=**5.5 N** before friction/mesh/guide losses. This favorable1.1-W mechanical bound at.2 m/s does not rate a drive, a tooth or the88-W selectors. Loads/inertia/mass are explicit bounds, not measured miniatures or calibrated priors.

## Economics and disposition

All new amounts are **unquoted allocations**, including inherited dated selector-price comparisons, not current quotes or market floors. The executable ledger removes private motors, belts and feedback but pays per-output shaft/tip/pinion/bushings $5–14, carrier/arm/guides/return $4–12, selector $4.46–8, driver $1–2, harness $1–3 and switches $2–4. Shared rack/drive/encoder $40–120 and rack guides/stops $35–110 join plates/jigs, distribution, XY, chassis/service, protected supply, controller, resident supports and cap reader/mount. Add10%+$20 or15%+$60 landed allowances.

|Grid|Bought low–high|Favorable residual at $500 / $1000 / $1500|Maker-hour scenario|
|---|---:|---|---:|
|64²|$1115.91–2981.78|−615.91 / −115.91 / +384.09|20.77–49.76|
|80², failed envelope|$1166.60–3193.75|−666.60 / −166.60 / +333.40|25.89–62.56|

Printing material adds$60–160. Maker time uses8–20 s/resident pair,8–16 h common build/calibration,10–30 min/output and1–3 h rack assembly. Print duration, support cleanup, failures and phase commissioning are unmeasured additions. No two-to-four-day manufacturing pass is established. The$1,500 demonstrator case stays distinct from a finished~$1,000 product and authorizes no spending.

**Decision:** preserve the shared-drive simplification and stop this straight-rack embodiment. It saves fifteen rotary motors and sixteen belt routes, but only~$131 at the favorable complete allocation, while adding long empty returns, a wide sweep and rigid phase constraints. Do not refine pinion teeth, selectors or socket fits. The next distinct independent discriminator is a compact continuously circulating shared drive with selective axial docking: first bound finite contact/routing and transmitted torque, phase-compatible states/recovery and complete latency/cost. A loop is not automatically superior. Retain direct spindles and independent16 as controls; no optional print or owner question is needed for this conclusion.

Checks:1,296 exhaustive four-output signed replays, monotonic/unchanged-state assertions, finite rack position and closed-form distance, dense/no-op timing anchors, force–work equality, coarse/fine clearance witnesses, offset-selector cross-channel boxes and rigid-phase counterexample. They verify the declared model only. Advice favoring simple repeated hardware, coarse pitch, real downward travel, practical assembly and software feedback remains incorporated; no dormant micro-lock campaign reopens.
