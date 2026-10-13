---
status: complete
builds-on: [E-273, E-272, E-271]
---

# Circulating shared drive: compact return, coupled traction and docking

**Park this friction-loop embodiment before tooth, clutch or selector refinement.** Circulation removes the straight rack's empty return, reducing coarse S50 swept X from838.93 to **452.85 mm** and conditional local waiting from40.99 to **29.80 s**. Favorable bought allocation is **$1,156**. However, fine-pitch band envelopes collide; coarse axial docking has only.10-mm bounded edge reserve; and drive tension makes the inherited axial selector inadequate in every tested friction/load scenario. Smooth drums also lack demonstrated preservation/recovery of rigid socket phases. The timing improvement is a model result, not an operable-machine pass.

Reproduce `python3 tools/curated-experiment-checks/E-274/loop.py --check`; omit the flag for full workloads, sensitivities, geometry and allocations. Requires NumPy. Evidence: **calculation, bounded geometry and ideal replay**, self-reviewed. No measured belt, calibrated friction, process yield, rated speed, print or purchase. E-271/272/273 failures remain unchanged.

## Finite contact and selection

One reversible motor drives one endless flat friction band around16 adjacent output drums. Fifteen interposed idlers create wrap; four larger end drums close the return, including the drive and an adjustable tension mount. Outputs turn together in the same direction. Each drum/shaft/tip/bearing carrier moves axially3 mm to dock selected resident screws while the band stays fixed on its broad drum face. There is no sliding torque spline, private belt/motor or granted tooth engagement. Axial sliding through the tensioned band is a real force duty.

Coordinates, mm: outputs `(i*p,0)`; idlers `((i+.5)*p,-6)`; end drums `(-18,0)`, `(15*p+18,0)`, `(15*p+18,-22)`, `(-18,-22)`. Output/idler physical radii2, end radii8; a .4-thick/2-wide band gives neutral-line radii2.2/8.2. Exact internal tangents join opposite-running output/idler drums, external tangents join the end turns, and contact arcs follow the declared winding. A straight tangent band across equal collinear drums has **zero interior wrap**: a loop alone supplies no finite torque contact there.

|Necessary geometry, independent face bounds ±.2 mm|64² / p6.35|80² / p5.08|
|---|---:|---:|
|Closed band length|656.05 mm|642.25 mm|
|Minimum / interior output wrap|83.05° /205.04°|90.06° /219.07°|
|Drive wrap|109.47°|109.47°|
|Nonlocal band clearance, including chord bound|1.149 mm|−.121 mm|
|Neighbor drum-body clearance|1.95 mm|.68 mm|
|Broad-face axial edge reserve|.10 mm|.10 mm|
|Parked tip gap / insertion|.60 /1.60 mm|.60 /1.60 mm|
|Loop-only XY reservation|148.05×38.8 mm|129.0×38.8 mm|
|Whole-board swept X|452.85 mm|454.12 mm|

The band consumes the fine-grid gap while bare drums still clear. No thinner-band/tiny-drum rescue is pursued. Bounds are not X1C distributions. Every nonadjacent band-path piece is checked;80-segment arcs have sagitta<.00063 mm, and40/80/160 refinement changes coarse clearance<.02 mm. This is finite path geometry, not complete solid CAD.

The moving drum face goes from z `[−18,−12]` to `[−15,−9]`; fixed band occupies `[−14.5,−12.5]`. Common face interval3 mm leaves.5 nominal reserve at each edge,.1 after errors;±.3 fails. A flange crossing the axial path would obstruct motion and is not assumed. Tracking and edge wear remain unqualified.

E-273 selector boxes clear:4 coarse/5 fine lanes,120/150-mm arms,150/180-mm rear reservation,90-mm depth. Arms lie below z−27; band and negative-Y idlers above, motor outside the row. Mounts, plate stiffness, guards, bearings and cable bends remain unconstructed. Band extends30.4 mm forward; enclosure/service is extra. Non-tip volumes stay below the bed. Support remains **pin→thread→screw collar→bed→frame**, with keeper reacting docking uplift; no writer load takeover.

## Traction conflicts with axial docking

The flexible-band limiting relation `T_high/T_low <= exp(mu*wrap)` and tension-difference torque follow [MIT 2.72 Lecture12, pp.12–16](https://ocw.mit.edu/courses/2-72-elements-of-mechanical-design-spring-2009/83d81a6f63d1c6f0fb775c08b207bc51_MIT2_72s09_lec12.pdf). That source supplies the relation, **not** our dimensions, coefficients or allowable loads. Bending, creep, centrifugal effects and tracking are not qualified by this approximation.

Scenario:16×.35 Nmm output torque,1e−8 kg m²/output inertia,5 m/s² band acceleration, effective radius2.2 mm. Total tension difference **2.711 N** excludes band/idler/drive inertia, bearings and bending losses. Drive torque22.23 Nmm at radius8.2; mechanical power.542 W at.2 m/s before losses. At circumferential mu=.3, actual109.47° drive wrap requires **at least3.503 N slack tension**;2 N supplies only1.548 N difference and fails. Output traction alone needs.311 N, so the common drive is stricter. Effective neutral radii2.2/8.2 are used consistently throughout.

With the bus stopped and unloaded pretension at least equal to that required slack tension, integrated contact normal force is `T*wrap`; axial sliding drag is `mu_axial*T*wrap`. At mu_axial=.3 an interior drum needs **3.760 N**, before weight, guides, return or socket insertion. The inherited catalog.785-N throw figure minus assumed.2-N insertion leaves **.585 N**—already not a qualified force curve. The favorable comparison fails by6.43×.

|Circumferential= axial mu, assumed|Drag at .1 Nmm/output|At .35 Nmm|At1 Nmm|
|---|---:|---:|---:|
|.1|1.517 N|4.608 N|12.643 N|
|.3|1.238 N|3.760 N|10.318 N|
|.6|.893 N|2.711 N|7.439 N|

All nine deterministic scenarios exceed.585 N; they are not material priors or a universal loop impossibility proof. The middle case needs axial mu≤**.0467** while circumferential mu stays.3, with other axial duties omitted. Directional friction, a stronger selector, active tension release or a fixed rotor with a separate sliding torque coupling would be **changed hardware**, requiring a new ledger. De-tensioning also releases angular registration and adds re-tension/phase work; it is not a free cure.

Minimum high-side tension6.213 N gives nominal7.77 MPa stress in the2×.4 section. Geometric bending strain `.4/(2*2.2)` is9.1% on small drums. No allowable stress/life is assigned to an unspecified band. Preload loads every output bearing/carrier and the shared plate, including unselected outputs; resident pin support stays separate.

## Stopped transaction, phase and recovery

Prove tips parked → seek → index known common phase while disengaged → stop/dock compatible changed subset/prove docking → rotate to successive signed height thresholds, stopping to retire completed tips → retract before new sign/phase acquisition or XY travel → settle → fresh identified actual-cap read. Selected heights move monotonically in ideal replay; unchanged screws remain unselected. Continuous circulation gives unlimited rotary travel, **not** moving engagement/disengagement.

No rack reset is needed. Band travel in height-equivalent units is `max(up)+max(down)`, versus E-273's `2*max(up,down)`. Balanced signs gain no return saving. Every threshold stop, selection/proof, retract/settle/read, XY seek/return and one compatible full-stroke retry remains paid.

Rigid sixfold sockets retain E-273's condition: selected socket phases relative to driven tips must fit a10° common arc for assumed±5° capture. Ideal heights on lead/6 spacing can share a group;10-mm workload increments are commensurate at leads2/3. The0/.25-mm witness at lead3 spans30° and defeats common docking. Known incompatible phases can be serialized; unknown phases cannot be searched by forced insertion.

Smooth drums add differential drift. A5° one-sided budget over50 mm at lead3 permits only **.0833% differential speed ratio**, equivalent to.00183-mm effective-radius difference at2.2 if radius is the sole error. Initially registered radii2.2±.002 already span>10° after nominal50-mm travel in exact replay. This is an operating sensitivity, **not a requirement to print micrometre-accurate drums**. Slip, creep and lead variation add uncertainty. A common encoder does not observe each output phase or cap height. Positive teeth could change slip, but still owe socket commissioning, corrections, finite contact and docking; no tooth refinement follows.

Optimistic timing grants known compatible phases and pays up to30° nearest-sixfold indexing/acquisition (~30 ms). Serializing changed outputs into separate known phases gives: coarse S50 local/scene maxima become **235.08 /1444.09 s**. Not every fault needs16 groups. Unknown phases, hidden caps, lost support and persistent faults have **unbounded completion**. Stable known errors retry from observed actual state after compatibility checks.

E-270's cap decoder remains rejected; encoders cannot prove socket/thread integrity or loaded-neighbor isolation. Owner-reported static screw hold remains positive specimen evidence, not safe moving-loss arrest or creep qualification. Unknown docking inhibits rotation; XY remains inhibited until retraction is proven.

## Complete conditional timing

Reuse E-267 adjacent16 interval cover, shorter row/column serpentine route and E-273 workloads. Both grids span406.4 mm. S40/N20 has20-mm walls/depressions; S50/N30 keeps shallow20/deep30 presets. Owner-selected physical river/ravine remain in the three-map convenience sample;133 nonempty four-square windows are spatial tests, not measured typical play. Minimum rest and paid raised neutral remain separate.

Assumed rates:850 rpm; band≤200 mm/s and5,000 mm/s² (361.72 rev/s² at radius2.2); XY200 mm/s,5,000 mm/s² and50-ms minimum seek. Charge5 s common handling/read deployment,80 ms/threshold selection-retirement-proof,100 ms each retract/settle/simultaneous actual-cap read per station, known phase indexing and one compatible full-stroke retry. No rate/read slot is qualified and no new optics is designed.

Seconds, **S40 /S50**. Loop rows grant traction/docking/phase compatibility; fine also grants its failed envelope:

|Grid|Four-square local max|Scene max|Paid neutral prep|One-sign dense stress|Mixed-sign dense stress|
|---|---:|---:|---:|---:|---:|
|64² loop|25.80 /29.80|251.35 /281.75|263.16 /323.63|383.63 /444.10|662.85 /783.55|
|80² loop, failed envelope|48.89 /58.53|359.96 /404.14|403.50 /497.85|591.73 /686.09|1028.01 /1216.48|
|64² rack, E-273|33.43 /40.99|338.71 /393.30|372.79 /487.09|600.50 /714.79|646.33 /767.24|

Mixed-sign stress is slightly worse than the rack: no empty-return benefit, plus phase indexing and lower angular acceleration from larger effective radius. Dense timing is diagnostic, not a30-s gate.

Worst coarse S50 local:137 changed (18 up/119 down),3,959 unchanged,16 rows/stations. **5 common +2.094 seek +1.056 XY return +13.019 rotation +1.600 switching +.607 phase +4.800 retract/settle/read +1.626 retry =29.802 s**. Known pre-positioning saves.802 s at this specific case and is separately paid preparation. All133 coarse windows fit30 s optimistically, with only.198 s worst-case slack. Lead2 gives36.51 s;400rpm44.45;200-ms switching32.32. Corresponding scene maxima348.57/426.02/316.91 s.

Minimum-rest first-map maxima343.98/404.45 s coarse,518.41/612.77 fine. Cold neutral plus first map427.74/493.05 coarse,616.74/748.97 fine. These begin at known mechanical zero; homing/commissioning is additional and unbounded.

At the same conditional850-rpm/lead3/read boundary, private16 E-271/E-270 gives coarse local24.84/28.84 s and scenes226.69/253.98. E-272 direct8 gives46.25/55.66 local and433.18/492.24 scenes, removing transmission belts. The loop recovers much of private16's local speed, not independent signed motion or phase search.

## Repetition, economics and disposition

Unchanged resident hardware:4,096/6,400 pin–screw pairs, sockets, thrust/keeper sites;8,192/12,800 guide apertures;126/158 two-layer ribs. Each row has64/80 passive pairs, no local motor/selector. E-269 fine-frame and loaded-support failures remain. No latch, optical mark or bore is added.

Shared head: one drive/encoder/band/tension adjustment;16 drums/shafts/tips, carriers/arms/selectors/returns;32 bushings, guide duties, stops and switches;15 idler and four end-drum bearing/mount assemblies; two XY drives. Band contacts and axial rubs are wear/critical interfaces. Wiring duties102 conductors/204 terminations before buses; selector all-on arithmetic88 W. Relative to E-271, remove15 motors and16 private belts, add19 roller assemblies and a common-band failure affecting all16 outputs. Resident holding and safe stop cannot depend on belt survival.

All new costs are **unquoted allocations**, not current quotations or market floors. Preserve E-273 resident supports, shared plates, XY, supply, controller, cap reader/mount and service. Replace rack drive/guides with drive/encoder40–120, band10–40,15 idler sets at2–6, four end sets at4–10, tension/tracking/guards15–50 USD. Per channel: shaft/tip/drum/bushings5–14; carrier/arm/return4–12; selector4.46–8; electronics1–2; harness1–3; switches2–4. Landed10%+$20 /15%+$60. Stronger selection or phase recovery is **not** hidden in this failed base machine.

|Grid|Bought low–high|Favorable residual at $500 /$1000 /$1500|Maker hours|
|---|---:|---|---:|
|64²|$1155.51–3108.28|−655.51 /−155.51 /+344.49|21.77–51.76|
|80², failed envelope|$1206.20–3320.25|−706.20 /−206.20 /+293.80|26.89–64.56|

Coarse favorable controls: rack$1115.91, private bare16$1246.54 (encoder16$1701.50), direct8$1145.52 (direct1$639.60). Loop saves~$91 versus bare16, costs~$40 above rack. No$500/$1000 product or purchase authority follows from the$1500 research comparison.

Labor:8–20 s/pair,8–16 h common build,10–30 min/output,2–5 h loop assembly. Material$60–160; print duration/cleanup, scrap and phase commissioning are extra. Machined plates, cut stock or molded parts remain unqualified alternatives to FDM. Secure/unload the board and park tips before bench service; resident repair retains openable-bed access.

**Discriminator:** circulation removes finite rack excursion and one-sign empty travel, but does not grant traction, cheap axial selection or recoverable phases. Coarse band geometry clears; fine fails; every tested traction/docking scenario exceeds the inherited selector. Modest savings do not earn tiny tooth/clutch/optics development or printing. Reopen only with a materially changed drive/docking interface removing axial belt rub and an explicit phase acquisition/recovery path, with a complete revised ledger. This rejects the constructed friction loop, not all circulating or threaded mechanisms.

Checks:1,296 signed replays, final/monotonic/unchanged states and travel identity; tangents/contact angles/nonlocal band clearance with refinement; dense/no-op/reversal timing anchors; force–work identity; zero-wrap and docking failures; incompatible socket and differential-radius phase witnesses; serial known-phase control. Advice favoring simple resident hardware, accessible shared machinery, coarse pitch, real downward travel and honest assembly remains incorporated. Optional printing stays retired; no new owner question.
