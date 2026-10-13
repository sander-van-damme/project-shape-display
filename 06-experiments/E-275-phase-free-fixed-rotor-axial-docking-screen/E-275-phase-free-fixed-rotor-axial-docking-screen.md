---
status: complete
builds-on: [E-274, E-273, E-272, E-270, E-269]
---

# Phase-free axial contact removes phase indexing, but does not earn a machine

**PARK the fixed-rotor, sliding-square-shaft, axial friction construction.** Fixing the band drums removes E-274's axial band rub; circular underside friction removes E-273's common rigid-socket phase condition. Those are real topology changes. They do not supply adequate contact force, a no-lift resident reaction, tolerant internal coupling or recoverable height readback. At assumed torque .35 Nmm and friction .3, the optimistic effective radius1.5 mm requires **.778 N** with frictionless supports, versus an inherited .785-N throw figure before any losses. A uniform-pressure3.2-mm full face instead requires **1.094 N**. Neither is a measured friction result or force rating.

Reproduce `python3 tools/curated-experiment-checks/E-275/docking.py --check`; omit the flag for the force, geometry and replication tables. Requires Python and NumPy through the preserved E-274 geometry. Evidence: **assumptions, analytical contact bounds, finite envelope calculations and ideal fault replay**, self-reviewed. No CAD fit, safe speed, hardware performance, print or purchase. Contact/selection fails, so this result deliberately does **not** regenerate gameplay/local/preparation/stress schedules or whole bought/assembly prices. E-270–274 retain their original scopes.

## Constructed selectable power path

Keep E-274's one motor, one circulating band,16 output drums,15 intervening idlers and four end drums at their existing XY coordinates. **Each output drum is now axially fixed to the head frame in two radial bearing/support stations**, rather than lifted through the band. An explicit square bore in its hub drives a rigid square-section sliding output shaft. This is a real additional sliding torque coupling, not a free spline or compliant shaft. A nonrotating selector arm acts through a rotary thrust interface on the shaft's lower collar. The selector raises only the requested shafts; return springs and parked stops pull them away. Parked shafts can still rotate with the bus, but have no intended contact with resident screws.

Power path: motor → band → fixed drum/hub → square-bore flanks → sliding rigid shaft → flat friction pad → resident screw end → thread → guided pin. Axial actuation path: selector → arm → rotary thrust interface → shaft → pad → screw → bed/keeper/frame. The band provides torque, **not axial squeeze**. Rotor radial reactions go through its own fixed bearings/frame. Carrier thrust friction increases bus torque; its geometry and rating are not hidden in the pad coefficient.

Finite initial dimensions, mm, with resident underside at z=0:

- Fixed4-mm-OD drum spans z−20…−14;2-mm-wide band occupies−18…−16. Its4-mm-OD hub spans−24…−10 with a2.4-mm square through bore.
- A2-mm square shaft segment spans−27…−7 at park and translates q=0…3. It covers the full14-mm hub length throughout. Round2-mm upper/lower stems connect to a3.2-mm circular pad at−2…−1 and the lower thrust collar near−40.
- Fixed bearing envelopes OD4.4 occupy stations near−25…−22 and−12…−9; mounting plates sit outside the band face and above the selector arms. The inherited4.4-mm-wide carrier/arm corridor and four coarse/five fine offset selector lanes reserve their route. Internal bearing, square-to-round transitions, mounts and rotary thrust fit are unqualified.
- Face contact occurs at **q=1 nominal**, within0.6…1.4 for independent±.2 axial bounds. Stop on contact; do not command the full3-mm stroke into a fixed screw. The remaining stroke is neither friction-pad compression nor permission to lift the screw. Selector force at this partial travel is unknown.

A flat3.2-mm resident face replaces the socket, adding flatness, wear, contamination and contact duties at every screw. The inspected trial-5 actuator/calibration/frame source at41484f9699 does not construct this dock. E-255 and the owner's unquantified holding observation remain unchanged.

|Necessary finite margin, independent e=.2-mm bounds|6.35 pitch /64²|5.08 pitch /80²|
|---|---:|---:|
|Inherited nonlocal band-path gap|1.149 mm|−.121 mm|
|Fixed band axial edge reserve|1.60 mm|1.60 mm|
|Neighbor rotor /bearing envelope separation|1.95 /1.55 mm|.68 /.28 mm|
|Parked pad axial gap|.60 mm|.60 mm|
|Pad to adjacent resident3.2-mm end|2.75 mm|1.48 mm|
|Square-shaft side clearance|−.20 mm|−.20 mm|
|Hub wall at bore corner|−.180 mm|−.180 mm|

Coarse external band routing survives; fine keeps E-274's collision. The fixed drum removes its moving-face .10-mm edge reserve problem and3.760-N axial band rub. But the **explicit internal coupling does not pass the same error box**: nominal side clearance .20 mm reaches zero at opposing .10-mm face errors; nominal corner wall .303 mm shrinks to .062 at e=.1 and disappears at e=.2. These are competing geometry bounds, not X1C distributions. Precision manufacture of16 shared couplings is more plausible than6,400 local splines, but no process is selected or qualified. Stop before a smaller shaft, thinner wall or fit sweep.

The loop-only XY reservation remains148.05×38.8 /129×38.8 mm; selector reservation extends150/180 mm rearward with120/150-mm longest arms and90-mm depth allowance. Whole-board X sweep remains452.85/454.12 mm before enclosure. Non-tip equipment stays below the bed. Bounds check neighboring envelopes, not stiffness, bearing retention, full harness, tracking or complete solid assembly.

## Contact, keeper drag and forbidden screw lift

For a Coulomb contact, integrate `dT = mu*r*dN`. A uniform-pressure annulus has `r_eff=(2/3)*(Ro³−Ri³)/(Ro²−Ri²)`. The [MIT 2.972 clutch derivation](https://web.mit.edu/2.972/www/reports/clutch/clutch.html) supplies the friction-interface model; it supplies **none** of our coefficients, sizes, loads or allowable stresses. Here integration gives r_eff1.067 mm for a solid radius1.6 face. The prompt's1.5-mm effective radius corresponds approximately to a narrow1.4…1.6 annulus (1.502 mm), a favorable pressure distribution, not the whole face's radius by default. Misalignment and wear can change it.

At .35 Nmm and mu=.3, even granting frictionless supports:

- Optimistic rim requires .7778 N, leaving **.0072 N** of the inherited .785 N for carrier weight, guide drag and return. Uniform full face requires1.0938 N and already exceeds it.
- A separately labelled **.20-N combined carrier/return/guide allowance** leaves .585 N. This is not E-274's .20-N socket-insertion term; the socket is removed. The required effective radius becomes1.994 mm, larger than the entire radius1.6 drive end. Even concentrating all pressure at the physical edge cannot meet that scenario. Enlarging a resident end has service/bed consequences, not a free pad enlargement.
- Sixteen optimistic contacts react12.44 N into the resident structure, before keeper drag. E-269's illustrative .2-N/site frame calculation is not a rating for .778 N/site. Contact pressure, tilt and pad life remain unqualified.

Let F be upward contact force, W the effective downward resident load, T0 torque excluding thrust surfaces, and `kb=mu_b*r_b`, `kk=mu_k*r_k`. Favorably neglect bearing preload and head losses:

`Trequired(F) = T0 + kb*max(W−F,0) + kk*max(F−W,0)`

`Tcapacity(F) = mu_face*r_eff*F`.

This explicitly credits unloading the lower bed before loading the upper keeper. Use an illustrative **W=.2 N**, not a measured miniature load or a guaranteed minimum. Radius2 mm is inside the inherited collar's1.8…2.2-mm contact region; the asymmetric keeper pressure distribution is unknown. With both thrust coefficients .3, kb=kk=.6 mm. Face slope .45 (optimistic rim) or .32 (uniform disk) is **less** than keeper drag slope .6. At F=W, capacity is only.09/.064 Nmm versus T0=.35. Above that point increasing squeeze makes the deficit worse: **no finite F suffices in this scenario**, even with an arbitrarily stronger selector.

If the inherited .35 Nmm instead included .12 Nmm of original bed drag, use T0=.23. The no-solution result still holds. This sensitivity avoids silently charging that old bed drag twice. Static breakaway, speed dependence and head thrust losses are outside the favorable calculation.

|Assumed face /thrust friction; effective radius|Required F at T0=.35, W=.2|Within .585-N allowance?|
|---|---:|---|
|.3 /0;1.5-mm rim|.778 N|No|
|.3 /0;1.067-mm full face|1.094 N|No|
|.3 /.3; either face|No finite solution|No|
|.3 /.1;1.5-mm rim|1.240 N|No|
|.6 /.3;1.5-mm rim|.767 N|No|
|.6 /.1;1.5-mm rim|.443 N|Necessary force inequality only|

The last row demonstrates a possible friction-contrast escape, **not a selected material pair or machine survivor**. None of these rows meets F≤W=.2. E-269's keeper has .2-mm axial float: in the freely guided rigid-pair limit, an F>W contact raises the screw/pin until the keeper seats, then it settles on release. Guide sticking must not be counted as a deliberate axial reaction. The force table grants the keeper *already seated* only to bound torque; **the proposed mechanism is not allowed that screw lift**. Zero-float opposing thrust support or a tool that closes its axial force locally would be changed construction with its own drag, manufacturing and replication costs. They are not supplied here. No extra resident spring, bearing, preload or head clamp is silently installed.

Conical contacts might change normal-force amplification but add wedging, separation and resident profiles; moving the squeeze reaction to the tool changes the power/load path. Both require a distinct architecture argument. Stop before cone angle, tooth, clutch or keeper refinement.

## Selection, loss and recovery

Intended stopped sequence: prove all pads parked → XY seek → stop bus → raise only changed shafts with force limitation → establish contact → rotate a same-sign group, stopping at each retirement threshold → unload torque and retract finished shafts → reverse for opposite-sign targets → prove full park → settle → fresh identified actual-pin read. The flat contact accepts arbitrary resident angular phases; the E-2730/.25-mm witness no longer obstructs **docking**. Mixed signs still need separate common-drive groups. Differential band speed or face slip becomes height error rather than an insertion-phase jam.

Square couplings are permanently engaged and paid at16 locations; they do not require rediscovering screw phase after each dock. They can bind on axial withdrawal under torque. A two-flank approximation at effective1-mm torque arm gives sliding resistance `mu_slide*T/r`: .105 N at mu_slide=.3 and T=.35 Nmm, before head-thrust drag. Stopping speed does not prove zero flank torque. Residual motor torque, screw back-drive or a wedged guide can defeat spring retraction. No force curve, return preload or power-loss arrest is qualified.

A parked .60-mm bounded gap isolates untouched resident ends geometrically; all rotating hardware, debris, plate deflection and neighboring loads still require qualification. A stuck-up pad inhibits XY and later bus rotation. On loss of power/band, the selector should return and the screw should retain its state, but neither moving disconnect nor safe stopping distance follows from the owner's zero-speed holding observation. A bus encoder cannot prove that a particular pad retracted or a screw stopped. No common-drive brake substitutes for passive resident holding after separation.

For stable observed slip, stop, retract, settle, identify the actual height and recompute the remaining signed displacement. A commanded10-mm move ending at8 mm needs2 mm correction; replaying10 mm overshoots. Circular contact permits this off-grid retry without rigid socket rephasing. **Unknown/covered/stale/wrong-cell height or persistent slip stops completion.** E-270's failed pixel decoder, miniature occlusion and unobserved loaded-neighbor limitations remain; no new optics or hypothetical read slot is promoted. The source's1,458 signed/partial-slip replays test arithmetic and unchanged commands only, not detection, pressure or safe arrest.

## Replication, simpler control and final boundary

Resident counts remain4,096 /6,400 pin–screw pairs, collar/bed/keeper/journal sites and drive ends,8,192 /12,800 guide apertures and126/158 two-layer ribs. Each row has64/80 pairs; a16×16 region has256. Replace rigid socket geometry with the same count of friction faces; add no resident moving parts in the screened construction. Surface consistency and cleaning become board-scale duties. The no-lift remedy remains absent, not zero-cost.

One16-output head has one common motor/encoder/band/tensioner,16 fixed hollow rotors,32 fixed rotor-bearing duties,16 rigid translating shafts/pads and square sliding pairs (64 flank surfaces),16 rotary thrust interfaces,16 carrier arms/selectors/returns and32 guide/stop/park-contact sensing duties each. Fifteen idlers plus four end-turn assemblies and two XY drives remain. Relative to E-274, split rotating/translated bodies and add16 sliding torque pairs plus fixed rotor supports; the moving-band interface disappears. Hardware can be integrated, but functional contacts remain. Selection retains the inherited88-W all-on arithmetic and102 conductors/204 terminations before buses, not a new supply rating or complete wiring route.

Shared-part service is bench removal with all tips parked and the resident board secured; square-bore cleaning and pad replacement add16 accessible maintenance duties. Resident face damage still requires the unloaded openable-bed pair replacement route. Machined/broached shared hubs and cut shafts are possible process classes, not quoted parts; molding/FDM do not automatically supply the shown wall/clearance. No whole bought or maker-time ledger is updated after this gate failure.

**Simpler control: E-272's independently driven direct spindle.** Moving its entire motor/coupler/tip on Z removes the shared band, idlers, fixed hollow rotor and square sliding transfer. Independent angle control can search its own rigid socket without the common-phase constraint, though safe acquisition still needs evidence. A positive socket carries torque without a friction clamp force proportional to torque; axial insertion/holding and moving-loss behavior remain unqualified. Giving a direct spindle the *same flat friction face* does **not** cure the keeper/contact-force problem. Keep both facts distinct.

E-271's independent16 routing, E-272's slower direct-spindle timings/allocations, E-273's rack/phase failures and E-274's band/tension failures are unchanged. No new gameplay, preparation, stress or bought-cost claim is justified here.

**Canonical decision:** do not reopen E-274. The changed construction escapes axial band rub and keyed socket phase, but fails baseline contact force, no-lift reaction and bounded internal geometry; fine pitch additionally retains the band collision. Force-only sensitivity survivors are insufficient. Reopening requires a concrete reaction/drive construction with adequate pad torque, finite no-lift retention, real return/isolation and a defensible manufacturing route. Only then update complete timing, bought/assembly and recovery ledgers. No local fit/clutch iteration, new optics, print, purchase or owner answer follows.

Verification:486 contact regimes cross-checked against independent normal-force sampling; uniform-pressure radius checked by numerical ring integration; full3-mm coupling-overlap sweep; inherited band and selector envelope checks at both pitches; internal nominal/adverse geometry witnesses; unchanged rigid-phase counterexample;1,458 ideal signed slip/retry cases and unknown-read inhibit. Advice favoring simple resident hardware and practical assembly supports stopping here; optional printing remains retired.
