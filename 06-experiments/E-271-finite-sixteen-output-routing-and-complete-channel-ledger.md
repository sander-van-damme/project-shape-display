---
status: complete
builds-on: [E-267, E-259, E-270]
---

# Finite sixteen-output routing and complete channel allocations

**Coarse offset channels have a conditional spatial route; the tested fine-pitch route fails. Sixteen catalog encoder channels exceed $1500 even at the favorable whole-machine allocation.** Bare motors preserve a conditional coarse $1500 research comparison, with substantial unquoted transmission, feedback, support and readback work. Stop before pulley, coupler or guide refinement. Retain one direct encoder spindle as a slower, simpler control. No hardware selection, print, purchase or safe RPM follows.

Reproduce `python3 tools/curated-experiment-checks/E-271/routing.py --check`; omit the flag for layouts/ledgers, add `--slower` for serial timing. Evidence: catalog inputs, conservative swept boxes and allocations; self-review, not CAD fit, manufacture or physical qualification.

## Actual catalog envelopes first

Checked 2026-10-13; USD before tax/shipping. Prices below apply to sixteen outputs/eight dual bridges, not the earlier 128-channel order.

|Catalog item|Relevant finite envelope|Quantity price / subtotal|
|---|---|---:|
|[Pololu5180 encoder gearmotor](https://www.pololu.com/product/5180), [drawing p1](https://www.pololu.com/file/0J949/micro-metal-gearmotors-dimensions.pdf)|10×12 gearbox; encoder/connector exceeds it. Use conservative16×16×33 body box, separate3×9 D shaft. Drawing OL maximum32.5mm for this ratio.|16×29.85 =477.60|
|[Pololu4763 cable](https://www.pololu.com/product/4763)|30cm, six28-AWG wires; insulation/bend radius unqualified. Cable is extra.|16×2.76 =44.16|
|[Adafruit711 bare motor](https://www.adafruit.com/product/711)|27.5×20×15 body,2×8 shaft,17.5g; no encoder/reduction.|16×1.76 =28.16|
|[Adafruit3297 dual bridge](https://www.adafruit.com/product/3297)|26×18×3 board before connectors; two reversible channels, default1A limiting.|8×5.95 =47.60|
|[Adafruit2776 selector](https://www.adafruit.com/product/2776)|20-mm body length,3-mm throw; reserve16×16×30 including terminals/armature, inside larger cartridge. Catalog80gf throw figure is not a force curve.|16×4.46 =71.36|

Encoder motor/cable/bridge/selector subtotal **$640.72**, bare motor/bridge/selector **$147.12**. The bare route still buys a separately constructed encoder/attachment; the incompatible E-259 encoder kit is not substituted. Encoder gearbox ratio9.96:1 is internal; proposed external transfer1:1 versus bare external1.5:1. No loaded speed, inertia or reversible backlash follows from either ratio.

## Finite routing discriminator

Coordinates: output centers `(i*p,0)`, i=0…15; resident socket mouth z=0. Every channel's *whole motor/transmission/spindle carrier* translates3mm, avoiding a tiny sliding torque spline. One fixed solenoid beneath each motor lifts its carrier; return spring and hard parked/engaged stops are separate duties. This is a proposed mechanism with allocated volumes, not an assembled channel.

Generate1…8 lanes with `lane=i modulo L`. Motor axes at y=`30+30*lane`; transmission deck z=`−30−12*(L−1−lane)`. Farther motors have higher decks: their belts pass **above** nearer motors. Motors, slides, guides, selector and connector exit occupy20×24×89mm (encoder) or25×24×89mm (bare) swept cartridges. Internal brackets/contacts remain unconstructed.

Each belt/pulley corridor is6mm wide, y=−3 through motor y+3, z=deck−1…deck+4 including travel. Output shaft diameter2mm; tip diameter3mm. Two bearing-carrier envelopes are4.4mm wide, one near the tip and one near the pulley. A4.4-mm-wide riser connects them to a4.4-mm-wide moving beam beneath the belt. These are finite structural reservations, not hollow-bearing CAD or stiffness proof. The external1.5:1 route reserves a smaller input pulley within the same6-mm corridor; belt pitch, tooth count, minimum bend radius, tension and hub construction remain unresolved. No catalog6-mm pulley is asserted.

Check all inter-channel volume pairs over independent0…3mm swept motion. Within-channel overlaps reserve interfaces, not assembled solids. AABB collision rejects this envelope, not every possible detailed shape.

Apply an independent±e bound to each box face, plus .05mm screening separation reserve. This contains adverse local/bank errors; common rigid translation cancels in pair gaps. Bounds e=.1/.2/.4 are **not X1C tolerances**. Angular runout, loaded bending, belt vibration, thermal drift and internal fits are outside the result.

|Pitch / route, e=.2mm|First separated lane count|Minimum residual separation|Head reservation X×Y×depth, mm|Swept machine X×Y, mm|
|---|---:|---:|---|---|
|6.35 / encoder|4|.750mm|127.25×215×200|438.4×621.4|
|6.35 / bare|5|.750mm|132.25×245×212|443.4×651.4|
|5.08 / either|None in1…8|Interference|No accepted envelope|No accepted envelope|

Bare4 has zero residual at e=.2; e=.1 admits it with.2mm. At e=.4 coarse encoder4/bare5 leave.35mm, docking only.2mm. Fine output-riser plus neighboring transmission needs at least `3+2.2+2e+.05=5.65mm` transverse separation at e=.2; pitch5.08 cannot provide it wherever Z overlaps. The finite construction also exposes moving beam/deck intersections. No narrowing of risers/pulleys follows. Larger12-mm pulley envelopes fail both pitches regardless of sampled lane count.

**Coaxial staggered-depth control fails:** even after separating bodies in Z, the deeper drive's shaft crosses an adjacent shallower motor. Even using the encoder's10.5-mm narrow projection, half-width+shaft radius+2e exceeds pitch at e=.2. The explicit body/shaft model reports15 inter-channel conflicts at the coarse accepted lane counts. Merely assigning three motor lanes was never sufficient.

Longest parked shaft70/82mm, with torsion, whirling and bearing loads unqualified. Depth excludes the resident stack above z=0. The motor pack overhangs the playing area; drawer/bench service needs extra access.

## Docking, wiring, support and repair

Parked tip top z=−1; selected z=+2. At e=.2 this leaves.6mm parked gap,1.6mm insertion, and2.25/.98mm clearance to an adjacent assumed4.4-mm resident socket envelope at coarse/fine pitch. Intended socket bore mating, phase capture and1-mm minimum effective torque engagement are **assumptions**. They require a compliant/force-limited approach and detection, not forced alignment. A common lift of all sixteen tips is rejected: it touches unselected sockets. Independent whole-channel lifts implement arbitrary subsets without intentionally engaging unchanged sockets.

Sequence: prove all tips parked → XY seek → select only changed outputs → prove docking → signed rotation → stop → retract selected outputs → settle → fresh actual-cap read. Failed/unknown docking inhibits rotation and XY motion; blind replay is prohibited. Spring return on power loss does not prove safe moving disconnect. E-256's reported passive hold is positive evidence; it does not qualify this transaction.

Resident load path stays pin→thread→screw collar→opaque bed→frame; keeper/frame reacts docking uplift. No writer load takeover or per-cell clutch/brake is introduced. Keep E-269's unresolved fine-frame clearance and loaded keeper/support qualification. The bed/keeper is an excluded plane: every non-tip head volume stays below it. Resident pairs/seats/sockets remain4096/6400, guide apertures8192/12800, two-layer ribs126/158. No marks, holes or witness tails are added.

Each cartridge has a3×4-mm cable-drop corridor to a lower tray;3-mm-wide comb lanes then run rearward to shared electronics. Eight dual boards occupy a4×2 array at30×24mm spacing; connectors/capture/control receive additional space. Six encoder/motor wires plus two selector and up to four docking-switch wires imply up to192 channel conductors,384 end terminations before shared buses. At .8-mm assumed wire OD and50% packing, twelve wires need12.06mm²: **the nominal12mm² drop is already marginal**, so wiring geometry is conditional on thinner insulation, fewer shared returns, or a larger rerouted harness. Actual cable OD, flex life, strain relief and EMI are unqualified. Do not call the spatial route a complete packaging pass.

Selection alone is17.6A/88W if all16 solenoids are energized. Bare motors add4A/24W at their catalog loaded condition; this is112W arithmetic, not a PSU rating or predicted map power. Encoder stall extrapolation1.5A exceeds the selected bridge's default1A limit; startup/thermal/current limiting must be resolved. Catalog80gf≈.785N minus an **assumed**.2N docking demand leaves only≈59.6g moving mass before guide friction/acceleration. Carrier mass and return force are unknown; solenoid duty and fail-safe return are not proven.

Head counts:16 each motors, selectors/returns, carriers/risers/beams, shafts/tips, belts/tensioners;32 each bushings, guide duties, stops, switches, pulleys;8 dual bridges. Motor internals are included in catalog assemblies. Bare adds16 feedback assemblies.

Service proposal: all tips parked, retain resident supports, withdraw the entire head as a side-access drawer, disconnect shared harness and open split carrier/comb plates on the bench. Removing one wide cartridge vertically through live harnesses is **not** assumed collision-free. Openable shared resident beds permit pair replacement only after the affected region is unloaded and secured; no loaded in-play repair claim. Machined/reamed split plates, cut shaft stock and batch-made pulley/slide sets concentrate precision in16 channels. Casting/molding can reduce repeated part handling only after shrinkage, tooling and hub attachment are qualified. FDM carrier shells remain an alternative; no thousands of fitted inserts or hand-trimmed couplers are authorized.

## Whole-machine allocation, not a complete quoted BOM

Replace E-267's lump reserve with **unquoted low/high allocations**, including tooling/rework; these are neither probabilities nor guaranteed bounds. Only the catalog amounts are sourced.

|Missing per channel|Low–high USD/channel|
|---|---:|
|Shaft, tip, two bushings|2.5–7|
|Two pulleys, belt, tensioner|4–12|
|Slide, two guides, stops, return, mount|3–8|
|Selector MOSFET/flyback|1–2|
|Harness, connectors, strain relief|1–3|
|Two docking-state switches|2–4|
|Bare-route encoder/attachment only|5–15|

Shared: precision plates/jig120–300; head distribution/capture40–100; XY guides/drives/limits120–240; chassis/service35–75; supply/protection/cooling80–150; controller35–70; resident beds/keepers/guides/ribs .02–.08/site; actual-cap reader/lighting/references80–250; reader mounting/carrier80–180. The source prints each quantity and amount. Reader allocations do not buy a demonstrated decoder; low resident-support costs are especially unquoted. Add explicit landed allowances10%+$20 /15%+$60, then report printing material and labor separately.

|Grid / route|Before landed allowance USD|Purchased USD range|Remaining at $500 / $1000 / $1500, favorable end only|
|---|---|---|---|
|64 / encoder16|1528.64–2909.40|1701.50–3405.81|−1201.50 / −701.50 / −201.50|
|64 / bare16|1115.04–2655.80|1246.54–3114.17|−746.54 / −246.54 / +253.46|
|80 / encoder16, failed route|1574.72–3093.72|1752.19–3617.78|−1252.19 / −752.19 / −252.19|
|80 / bare16, failed route|1161.12–2840.12|1297.23–3326.14|−797.23 / −297.23 / +202.77|
|64 / one direct encoder spindle|562.77–1393.03|639.05–1661.98|−139.05 / +360.95 / +860.95|
|80 / one direct encoder spindle|608.85–1577.35|689.74–1873.95|−189.74 / +310.26 / +810.26|

Upper allocations exceed every tier; source prints all residuals. These are **not market price floors**. Encoder motors/cables add$493.60 versus bare before its$80–240 feedback allocation. Neither$500 nor$1000 is established; favorable bare16 leaves$253.46 at$1500 for misses, not spending approval.

Printing material adds$60–160, with time/volume/yield still unmeasured. E-260's illustrative8–20s handling/pair,8–16h common build/calibration and10–30min/channel give19.77–46.76h at4096 pairs,24.89–59.56h at6400. Extra hand fitting or print support cleanup is outside this handling scenario and must be added, not called free. At illustrative$20/h plus material, coarse16 all-in is$2157–4501 encoder or$1702–4209 bare. Assembly can exceed the owner's2–4-day preference even before a failed lot; specialized manufacture must reduce real touches, not just purchase prices.

## Waiting and decision boundary

E-267's16/coarse conditional850rpm/lead3 waits remain18.61/22.61s local,173.33/200.62s scenes,175.50/235.97s neutral prep and296.44/356.91s dense for S40/N20 versus S50/N30. Minimum-rest and raised-neutral workloads remain distinct; no new software zero creates travel. **Those timings do not transfer as qualified results to this larger/heavier head.** Docking, power admission, inertia and actual-cap proof are unresolved. E-270's more explicit conditional exposed-cap readout raises local waits to24.84/28.84s and scenes226.69/253.98s; its tested patch decoder was rejected. Encoders cannot detect stripped threads, missed sockets or hidden cap heights. Covered pins remain unknown.

The simpler comparator has **one direct encoder spindle on XY plus one docking Z**, no inter-channel belts/lanes or sixteen selectors. Reuse the same physical-relief windows and a deliberately slower400rpm/lead3 scenario, .38s dock/retract/settle/read allocation,1s deployment and one full50-mm retry from a freshly known stable state. Coarse/fine S50 local maxima are about512/791s; paid neutral30 prep8030/12493s and dense50 stress12126/18893s. Homing, unknown faults and covered-cap recovery remain unbounded. It is a cost/qualification control, plainly far from the~30s play reference, not a recommended play experience or safe speed.

**Stop local refinement.** Coarse bare16 warrants only a conditional budget comparator; encoder16 fails these tiers, fine routing fails the tested envelopes, and neither has qualified wire clearance, force or readback. Reopening needs a complete channel allocation/quote with finite harness and measured or defensibly bounded lift/torque/retention, or a changed architecture that removes the belt/riser and selector burden. A useful next discriminator is whether fewer reusable *direct* spindles can preserve useful localized reveals while eliminating sixteen transmission/selector assemblies, with real readback limits charged. No new owner question or print is requested.

Checks: finite body/shaft collision witness; all cross-channel swept boxes; oversized-pulley and expanded-deck failures; e-bound transitions; docking clearances; budget identities. These verify a conservative model, not hardware. Advice about raised neutral/coarse pitch, accessible shared precision and batch assembly remains incorporated; no parked per-cell lock campaign is reopened.
