---
status: complete
builds-on: [E-285, E-277, E-279, E-280]
---

# Shared assembly, proof and installed run-in

**Park the separate hand-fed station; retain installed run-in and separate bottom
thrust as conditional controls.** Neither qualifies support, process yield, torque,
speed or repair. `tools/curated-experiment-checks/E-286.py` preserves observation
cases, force windows, labor/startup replays and service-access bounds. Evidence is
self-reviewed analytical identities and allocated operations, not contact simulation
or hardware measurements. 

## Separate station and axial proof

E-277 body/E-280 screw use side nests, split collar cup and limited-torque
spindle with axial float. Source preserves seek/thread/reverse observations,
load paths and instrument assumptions; oriented feed/reject automation is unbuilt.
[DEPRAG](https://www.deprag.com/en/screwdriving-technology/deprag-apps/) supports
instrumentation concepts, not polymer qualification.

Assumed lead3±.06mm/turn,gain±.2%,datum±.15mm,reading±.10mm,lost motion±.30mm
admit243 good corners/reversals:2/16turn bands5.368–6.633/46.445–49.559mm.
Datum cancels within segments; final±.7mm covers .15+.10+.124+.30.
E-256 rough1-mm play does not justify tighter bounds. Stall≤.5mm/turn fails;
2.7-mm lead passes2turns but fails16. Damaged same-lead flanks duplicate good
travel/torque. Entry burr/tilt/elastic twist/strip/creep remain unbounded;
no qualified safe torque window or prevalence.

Manual handling/thread/gauge allocations give18/28/43s; station10s active+19.33s
at120rpm,4–12h setup. Source retains whole-machine overhead and yield scenarios.
At4h setup/all usable, whole maker manual-mid/station-active:25.26–49.39/
24.14–48.27h at1024;112.06–213.83/84.06–185.83h at6400. Attending dwell adds
5.50/34.37h;12h setup reverses the1024 saving. At80% usable with60s/reject,
station/manual:30.71–57.68/33.11–60.08h at1024 and124.89–244.44/160.89–280.44h
at6400. Equal usability/overlap unqualified. Unquoted station$200–600 plus
E-276$798–1768=$998–2368 before exclusions; reused spindle is not free inspection.

**Axial proof adds observability, not qualification.** Load cell/applicator and
nut/collar differential probe react through cup/frame, not spindle. Test locked
then free angle; bound cup friction/frame seating/drift; catch on power loss.
Illustrative.40±.02N,error±.04mm,good stiffness10–40N/mm,weak.5–2N/mm yield
−.0305….082/.150….880mm bands; .116 threshold separates corners. Error±.08mm
or original two±.10mm readings do not. At20N/mm,30° free rotation gives.020/.270mm
locked/free travel; two±2° errors resolve it, smaller movement/restraint may not.
Safe force window requires strongest_bad+error < command < weakest_good_nondamage
−error−overshoot. Bad.30/good.80/error.02/overshoot.05N gives(.32,.73)N;
bad.40/good.35 gives none. Owner's near1kg observation supplies neither bound.
Identical immediate response can conceal fatigue/creep. Endpoint nuts atZ2…12/
52…62 miss damage near30mm; loaded traversal still cannot prove endurance.

Two-position S50 proof adds33.33turns/16.67s at120rpm+24s dwell+2s active review.
At1024/6400:11.57/72.30h dwell,.57/3.56h active;80% usable14.46/90.37h and
.71/4.44h. Optimistic1024 saving drops1.12→.55h before fixture/setup/damage.
Park station/proof CAD pending measured bounds or fewer handling operations.

## Install extended pairs and reuse the writer

Four turns engage the complete10-mm nut at Z52…62; two leave6mm at Z58,
outside S50. Empty-board cradle supports pair/collar through both guides until
journal/thrust/capture closure. The4.4-mm collar cannot pass2.8-mm journal:
ordered/open assembly remains owed. Unpriced cradle must be removed safely.
Writer descends from S50 to minimum/N20/N30; jams/unreadable heights stop motion.
Motor counts are not height proof; undocking requires passive holding. Startup
never authorizes shared keeper opening or neighbor homing during play.

Split15s manual threading into5s pickup +10s rotation for20.67 turns. Four-turn
starting costs6.94s, saving8.06s/pair. At1024:2.29h theoretical saving and whole
maker22.97–47.09h before cradle/setup, extra inspection, rejects and attendance.
At4096/6400:9.18/14.34h saving; whole65.71–134.20/97.72–199.50h. These are count
controls:10.3-mm bodies do not fit6.35/5.08-mm pitch.

|1024; four spindles, ideal batches,2s visit overhead|Turns/cell|120rpm startup min|850rpm min|
|---|---:|---:|---:|
|Minimum|16.67|44.09|13.55|
|N20|10|29.87|11.55|
|N30|6.67|22.76|10.54|

Speeds/overhead/routing/concurrency are assumptions; scale4/6.25 for4096/6400.
Direct descent to neutral avoids minimum-then-rise, not full-stroke testing.
Fully attended120rpm minimum startup leaves1.56h/1024 saving before cradle/setup,
inspection/rejects. Existing writer removes$200–600 station only if it can inspect.
Integral-U/closed completed-pair print repetitions stay676.31/794.07h at1024,
not X1C forecasts. Retain assembly control; no fixture CAD.

## Separate bottom thrust from the opening row keeper

**A fixed bottom plate preserves gravity support while a row keeper opens, but
not radial guidance or upward restraint.** E-280's collar and driver both have
4.4-mm diameter: no lower collar shoulder. Support the actual driver bottom Z−10
on a fixed plate with2.8-mm aperture. It admits the2-mm-AF hex tool (2.309mm corner
diameter), leaving an annular thrust face. Load: nut→screw→driver end→plate→frame.
Socket burrs, flatness, wear, sag and friction remain repeated obligations.
Two locked row half-rails surround2.8-mm journals at Z−4…0 with3.2-mm bores; their
underside captures the collar upward. Axial clearance/preload is unqualified.

At12.7-mm pitch, assumed4.5-mm rail half-width and2.4-mm outward travel leave1.3mm
to the neighboring closed rail. Opening exceeds2.2-mm collar radius plus.1-mm
radial envelope. Collar fits10.8-mm guide, not3.2-mm keeper. Locks/frame, straightness/yaw and
upper-bearing extraction remain unproven.

With writer disabled and target secured, open rails, replace pair, close/verify
before enabling. Broken screws may need below-board retrieval.31/79 neighbors
lose radial/upward restraint; thread/column guides are unproven substitutes.
Temporary keeper must engage first where required, but no contacts are constructed.
Plate settlement shifts height one-for-one; power-off does not remove handling load.

Tool AF±.05mm, aperture/driver diameter±.10mm and eccentricity0… .10mm give16
assumed corners: minimum radial tool clearance.0664mm, annular width.600mm and
conservative ring area6.974mm². Not process tolerances, socket strength or rotating
contact proof. Uniform-pressure mean friction radius1.8296mm gives drag.0366…
.1464Nmm at.2N, assumed μ=.1… .4; at.338N,.0618… .2474Nmm. Rebuild torque before
claiming speed; avoid double-counting an existing thrust allowance. Numerical
annular quadrature agrees with the identity within3e-10mm; not friction validation.

At1024/6400:2048/12800 bodies+screws,64/160 half-rails,1024/6400 annuli,
2048/12800 half-journals,128/320 allocated locks. Fine-pitch counts are not fit.
Manufacture is unqualified;400mm exceeds X1C bed. Rail placement/lock10–30s adds
.53–1.60/1.33–4h before alignment/tooling. Both assembly routes owe support;
no net saving claimed against1.56h run-in advantage. No per-cell latch added.

## Single-pair service: path and closure screen

**Stop before local CAD.** Fixed4.4-mm collar cannot exit3.2-mm keeper upward or
2.8-mm plate downward: favorable±.1-mm diameter bounds leave1.0/1.4-mm interference.
Enlarging the keeper removes capture; removing only the column leaves the screw
trapped. Cutting it owes debris/tool access, not intact replacement.

An optimistic4.6-mm row-traversing window admits one collar even at5.08-mm pitch,
but releases restraint at every crossed center: worst15/39 neighbors from nearer
end of32/80-site rows,31/79 from one end. This grants perfect restraint elsewhere
and ignores moving-plate collisions. Lifting keeper also releases restraint.

Repair: disable writer; clear/secure target; engage/prove neighbor bypass;
open keeper; replace; close/prove permanent restraints before releasing bypass;
verify target. Eight common+12 keeper actions; each neighbor adds4 bypass/proof/
release actions. Fragment recovery/setup unpaid; actions may need multiple touches.

|Sites; segment width|Halves / allocated locks|Neighbors needing bypass|Actions/repair; all-site-once diagnostic|
|---|---:|---:|---:|
|1024;32|64 /128|31|144;147456|
|1024;4|512 /1024|3|32;32768|
|1024;1|2048 /4096|0|20;20480|
|6400;80|160 /320|79|336;2150400|
|6400;4|3200 /6400|3|32;204800|
|6400;1|12800 /25600|0|20;128000|

Locks are allocations, not fabricated closures. Row bypass repeats31/79 radial
and capture functions even if monolithic. All-site-once is scaling, not predicted
maintenance. Bypass/access/frame reaction and overhead extraction are unconstructed;
power-off/thrust cannot replace radial capture. Park closure/window detail.

## Detachable shank with captive driver

**Conditional body/shank repair, not complete single-cell service.** Split the
screw above its collar; leave4.4-mm collar/driver captive between unchanged keeper
and bottom plate. A2.8-mm keyed tail enters from above: key transmits reversible
torque, internal shoulder transmits gravity, axial fastener resists upward loads.
Access fastener through bottom aperture while independently counter-holding driver.
Wall/key/tail strength, access, anti-loosening and joint manufacture are unknown;
a simple threaded coupling is not credited for reversing drive.

Secure target and counter-hold driver; release retainer, lift body/shank,
seat/key replacement, secure/prove retention and height. Only the released tail
crosses keeper. Nominal.20mm radial clearance reaches zero under assumed±.10mm
diametric errors/.10mm eccentricity; no fit-tuning mandate. Source retains corner
checks. Access/fragments remain unresolved; screw-only withdrawal from held
minimum body owes62mm/20.67turns.

Driver remains trapped by3.2/2.8-mm apertures; socket/thrust/keeper faults remain.
Body/shank coverage is two fault classes, not a reliability fraction; joint adds
jam/strip modes. Body+shank+driver+retainer doubles pieces to4096/25600 at1024/6400.
Key/compression seat/tensile retention/proof repeat per site. Seven assembly actions:
present driver,orient tail,seat,present retainer,counter-hold,tighten,verify.
Assumed15–45s adds4.27–12.80/17.07–51.20/26.67–80h at1024/4096/6400.
At1024 installed-run-in22.97h becomes27.24–35.77h before tooling/rejects/exclusions;
32h leaves9.03h for all additions. Cost=N×delivered driver/retainer/joint+tools,
unquoted. Integral-screw slices do not qualify split fabrication; molding/machining
change cost/yield, not counts. No automated feed credited.

Park local joint CAD pending robust reversible access and whole-process evidence.

## Offline repair versus detachable shanks

For body/shank faults only, avoiding15–45s/site split-joint assembly saves
4.27–12.80h/1024 before bench-fixture setup. Extra10/30/60 hands-on minutes per
bench episode erase this after25.6–76.8/8.53–25.6/4.27–12.8 episodes;
at6400 and30min:53.33–160. Identity: N*assembly_seconds/(60*extra_minutes).
Driver/socket faults are excluded: split shanks never solved them. No fault rates.
The source retains reconstruction-only S50 stress: four ideal spindles,2s/visit,
lead3,120/850rpm give44.09/13.55min per1024 cells before reset/proof/routing.
The following closure comparison adds explicit affected-row work and reset.

## Bench versus repeated cell closures

**Retain offline service as a conditional simpler control, not accepted UX.**
Compare integral pairs with row keepers versus independent cell keepers, not
split shanks. Normal gameplay regional isolation remains mandatory. Calculations
below allocate actions/time; no fault rates, closure/fit CAD or hardware proof.

Save absolute heights, address/datum/calibration identity and miniature locations;
clear all pieces; disable/park writer; secure board upright on bench stand.
Engage/prove whole-row restraint before opening keeper. Independently support
target, extract pair upward, insert replacement onto bottom thrust, close/lock/prove
keeper before releasing fixture. Remove fragments before homing; never force jams.
The136-mm body owes overhead guide-withdrawal/handling clearance and collar passage
through every layer. If access requires removing a shared guide, affected cells
expand to that layer's footprint. Restraint/access construction remains unproven.
Local closures also owe target/tool clearance, possibly nearby miniature removal.

Each keeper owes12 actions:4 unlock+2 open+2 close+4 lock. Add2 extraction/insertion
per failed pair; bench adds4 restraint/proof/release actions per affected site.
Monolithic fixtures earn no free gang proof. Common diagnosis, replacement
manufacture, access and target testing remain unpriced on both routes.
At assumed5s/action plus600s extra bench recording/unloading/stand/reloading:

|32² faults per episode|Rows/cells|Bench/local actions|Extra bench hands min|
|---|---:|---:|---:|
|One|1/32|142/14|20.67|
|Eight same row|1/32|156/112|13.67|
|Eight rows|8/256|1136/112|95.33|

This replaces, not adds to, the earlier20-action schematic. Eight co-repaired
faults are one episode; separate calls repay setup. Initial closures owe2N halves/
4N locks versus2w/4w for w rows,N=w². Avoided6(N−w) actions at10–30s each,
less assumed4h bench-fixture setup, save12.53–45.60/63.20–197.60/101.33–312h
at1024/4096/6400. These unbuilt closure allocations are not demonstrated savings.
Break-even=`max(0,6(N−w)*initial_action_s−fixture_setup_s)/extra_bench_hands_s`.
At1024:36.39–132.39 single-fault episodes,55.02–200.20 clustered-eight episodes,
7.89–28.70 scattered-eight episodes; at6400:165.82–510.55/204.94–631.01/27.22–83.82.
Changing5s/action or600s overhead changes the denominator directly. Nonpositive
numerator means no initial advantage. Correlation changes affected rows; no fault
frequency/lifetime winner follows. Do not add these savings to split-joint savings.

Saved commands are not actual state. After restraint loss assume affected rows
unknown; after uncertain transport/guide disturbance assume whole board unknown.
Stale datum/address identity or unreadable heights stops restoration. Safe homing
and actual-height proof remain unqualified. Replay fixed four-site row groups:
S50 maximum reset then saved absolute height h owes
`4+(50+max(h))*60/(3*rpm)` seconds/group (lead3,2s/phase visit).
This adds reset to the reconstruction-only table, still excludes routing,
retries, settling, proof and manual work. Flat N30 is a diagnostic, not typical play:

|32² faults|Bench min120/850rpm|Local min120/850rpm|
|---|---:|---:|
|One|2.31/.78|.29/.10|
|Eight same row|2.31/.78|.58/.20|
|Eight rows|18.49/6.27|2.31/.78|

Whole1024 unknown at850rpm:22.09/24.09/25.10/27.11min for minimum/N20/N30/S50;
6400:138.04/150.59/156.86/169.41min. Actual maps use batch maxima; true signed
travel and paid neutral remain owed. Unattended time is still interruption;
attended time must also enter labor break-even. Fine/quarter counts do not fit
10.3-mm bodies. These are not30s gameplay passes. Next useful evidence is accessible
shared restraint/extraction plus measured complete service labor/interruption,
not closure detail or guessed fault frequencies. No print or purchase.

## Product boundary

E-276 coarse$798–1768 excludes new support/joint/inspection costs; compare~$500,
~$1000 finished/$1000–1500 demonstrator without purchase authority. Inherited
S40/S50 local26.84/31.07s,scene201/223s,neutral271/332s,dense392/452s are conditional
versus~30s; new thrust drag has not earned speed. Minimum/elevated neutral and
signed travel remain unqualified. Retain empty-board run-in; parked service
variants require concrete restraint-preserving access/process evidence.
E-281 remains the only optional print; no new purchase or print request.
