---
status: complete
builds-on: [E-285, E-277, E-279, E-280]
---

# Shared thread-and-gauge assembly screen

**Park this hand-fed station before fixture CAD.** It can conditionally save
threading labor, but travel/torque observations cannot reliably exclude damaged
same-lead engagement. It does not automate feeding or remove whole-pair finishing
and installation. This is a bounded construction and executable observation
screen, not contact simulation, a built station, measured throughput or yield.

## One complete construction

Use separately made E-277 integral 136×10.3-mm closed columns, 10-mm bottom nut,
and E-280 finished screws: 64-mm lead-3 thread, 4-mm upper pilot, lower journal,
4.4-mm collar and underside socket. Use the 90° profile without retuning fit.
The same station can accept U bodies with a changed nest; no benefit is credited.

1. Operator removes/externally inspects both parts, then loads the column into
   two spaced side-opening square nests. A shoulder locates its nut bottom;
   nest flats resist rotation. A broad clamp reacts axial force through the
   body, without clamping the bore. No permanent insert or individual adjustment.
2. Operator loads screw head-down into a retractable, split collar cup. It holds
   the screw captive and aligns the driver socket. The upper pilot enters the
   nut from below. Nests and cup share a datum; radial float accommodates approach
   but is **not** a demonstrated alignment envelope. No bevel exists to credit
   automatic starting. Close the guard; reject absence/mislocation.
3. A reversible shared spindle on a counterbalanced axial slide approaches with
   force-limited preload. Seek backward at most one turn, then forward at low
   torque. After pickup, let the thread pull the free axial slide: do **not**
   impose lead-matched Z motion that could fake advancement through a stripped nut.
   A direct collar-position probe, referenced to the fixed nut nest, observes
   actual screw travel. Spindle encoder counts actual spindle angle downstream
   of any slipping clutch; torque measurement/limiting is a separate channel.
4. Capture first engagement, advance two turns for initial discrimination, then
   measure 16 more turns (48 mm). Reverse two turns and return two, measuring both
   directions; finish at nut-bottom coordinate 2 mm above thread origin. The tip
   starts at nut entry: total axial insertion is **62 mm / 20.67 turns**, plus
   the initial 4-mm pilot approach and four proof turns. The body cavity accepts
   the final tip at62 mm; no end seating torque is needed or permitted.
5. Stop and verify final collar-to-nut distance, retract driver without turning,
   open the cup laterally, then open nests and remove the intact pair sideways.
   This avoids pulling the collar through the nut. A catch tray contains the pair
   on power loss; no free falling spindle. Transfer support to the operator before
   opening the last restraint. Station holding is not installed-column retention.
6. On missing travel, excess torque, unreadable datum or failed reverse: stop,
   attempt one low-torque reverse only. If still stuck, retain both parts, open
   the nest/cup and remove the jammed pair to a reject tray. No forced screw-out,
   automatic acceptance after retry, or recycling visibly damaged threads.
   Log lot and failure; repeated common bias requires stopping that lot. Reject
   handling assumes60s/pair below; destruction/reprinting may take longer.

Per station: two antirotation nests, one clamp/axial seat, one split cup, one
spindle/driver/angle channel, one floating axial guide and counterbalance, one
actual-position channel, one torque limiter/measurement path, guard/controller,
catch and reject trays. These are functional allocations, not a fabricated BOM.
Per cell remain one body, one screw, one working thread, socket, collar/bed support
and two installed guide apertures: 2048/12800 pieces at1024/6400. No new resident
part; no removed interface. Precision is shared but the nut still repeats N times.

A precision machined nest/slide is allowed in principle; cast/printed nests need
calibration and wear checks. Printed, cast or supplied parts still owe cleaning,
straightness and fit. A hand-loaded tray is a fixture. An automated feeder would
add two orientation/singulation streams, two transfers, presence sensing,
escapements and reject diversion; none is constructed or credited here.

## Observation bounds and decisive fault

[DEPRAG's process overview](https://www.deprag.com/en/screwdriving-technology/deprag-apps/)
identifies torque, angle and screw-in depth as monitoring variables and distinguishes
manual from automated assembly. That supports the instrumentation principle,
not its suitability, price or accuracy for these polymer parts.

`tools/curated-experiment-checks/E-286.py` uses explicit **assumed bounds**:
lead3±.06 mm/turn, common position gain±.2%, common datum bias±.15 mm,
each reading error±.10 mm, segment lost motion±.30 mm. Bias cancels within a
segment but not absolute final seating. No X1C distribution or failure frequency
is inferred. An absolute final-position window of±.7 mm would contain .15 datum
bias +.10 read error +.124 gain error over62 mm +.30 seating allowance; this is
a required bound, not calibrated sensor or nest performance. The acceptance intervals are approximately5.368–6.633 mm over two
turns and46.445–49.559 mm over16 turns. Broadening error expands ambiguity;
backlash beyond.30 mm can reject good parts. E-256's rough1-mm play observation
is **not** permission to assume this tighter bound is achieved by new parts.

243 corner combinations of lead, gain, bias, read error and lost motion pass the
bounded good-trace model. A stalled/slipping engagement advancing≤.5 mm/turn
fails; a2.7-mm/turn fault can pass two turns but fails16. Both reverse directions
are included. Full-length roughness/dynamic faults are not reduced to this grid.

**Counterexample:** damaged/cross-cut flanks that follow the same3-mm helix can
produce exactly the good displacement trace in both directions at the same low
running torque. All such observations are identical to a good pair; this detector
must accept both or reject both. This is an admissible fault hypothesis, not an
observed incidence or proof that every cross-thread behaves so. Direct travel
removes the motor-count-only false proof but cannot establish intact flanks,
load retention or remaining strength. Even an axial proof test would need an
independently justified load, deformation limit and damage margin.

Torque examples .7 Nmm accepted /1.6 rejected at1.5 limit demonstrate controller
logic only. No measured running/damage torque window exists. A viable limit needs
`good maximum + sensing error < trip < damage minimum − overshoot`; neither
side is established. Radial offset, axis tilt, entry burrs and batch shrinkage
can generate these fault classes; no finite alignment/contact pass is claimed.
Thus increasing precision or merely reducing speed does not close rejection.

## Labor, throughput and cost

All times below are **operation allocations**, not observations. Manual assembly:
load body3s + load screw3s + unload3s + threading5/15/30s + functional gauge4s
=18/28/43s and five operations/pair. Station: the same three handling operations
plus guard/start1s =10s/four operations. Nominal automation dwell is19.33s:
24.67 turns at120rpm plus7s for seek, approach, reads and retraction. No120rpm
hardware rating is claimed. Rate is123 attempted pairs/h serially, versus manual
200/129/84. Fully attending the dwell counts as maker time; parallel work is a
lower-bound opportunity, not unattended feeder throughput.

Station setup/fabrication/calibration allocation4–12h; table uses optimistic4h.
Other whole-machine work is counted freshly, **not deducted from an aggregate**:
8–16h frame/electrical commissioning, four channels at10–30min each, external
removal/gauging10–30s per component, installation8–20s/accepted pair, and5min per
plate in two assumed289-up streams. Packing/stability, cleanup, scrap material,
print machine occupancy and repairs remain unqualified. Two external handling
operations per attempted pair and one installation per accepted pair remain in
addition to the assembly operations above. Functional gauging is separate.

|N; all pairs usable|Manual assembly h fast/mid/slow|Station active h / serial elapsed h|Whole maker h, manual mid / station active|
|---|---:|---:|---:|
|1024|5.12 /7.96 /12.23|6.84 /12.34|25.26–49.39 /24.14–48.27|
|6400|32.00 /49.78 /76.44|21.78 /56.15|112.06–213.83 /84.06–185.83|

Station-active totals require useful common work during dwell; otherwise add
5.50/34.37h attendance at1024/6400. At1024 the mid-case saving is only1.12h;
12h setup reverses it. Ideal break-even manual threading is11.06s at1024;
at6400 the modeled handling/gauging saving alone repays4h setup. This is conditional
labor benefit, not a reason to accept unreliable output. Assembly touches are
5120→4096 /32000→25600, before external work and rejects: still thousands.

At80% usable, ceil(N/.8) attempts and60s/reject, manual-mid/station active assembly
become14.22/11.82h at1024 and88.89/52.89h at6400. Whole maker ranges become
33.11–60.08/30.71–57.68h and160.89–280.44/124.89–244.44h respectively. This charges
replacement-part handling, not reprint occupancy; shared-lot rejection is possible.
Equal usability is only a comparison scenario: no evidence that either method
finds all faults. A false accepted pair must not be counted as useful yield.

Unquoted station hardware allowance: spindle/control/torque path$80–250,
slide/nests/cup$60–200, position sensing/guard$60–150 = **$200–600**, plus maker
setup and calibration standards. Reusing a display spindle does not make the
slide, gauge or calibration free. Against E-276 four-output$798–1768 allocation,
combined tooling+machine is$998–2368 before other exclusions; tooling may serve
many boards but the first maker pays it. Preserve ~$500 reference, ~$1000 finished
value and$1000–1500 demonstrator comparisons; no quote or purchase authorization.

The6400 row is replication only:10.3-mm bodies do not fit5.08-mm pitch (nor6.35).
No gameplay improvement follows. E-276 coarse S40/S50 local26.84/31.07s,
scene201/223s, paid N20/N30 neutral271/332s and dense392/452s remain conditional
against~30s. This factory operation neither changes real downward reach nor makes
neutral preparation free. E-279/E-285 separate completed integral-U/closed print
repetitions676.31/794.07h at1024 also remain; station dwell is not printing time.

**Decision:** no local fixture CAD, feeder promise, print request or purchase.
Reopen only with actual-process evidence bounding good/fault separation and a
safe torque window, or a materially different assembly/inspection construction
that eliminates the indistinguishable fault while saving whole-pair labor.
E-281 remains optional and cannot qualify long screws or this station.
Verification: analytical lead/travel identities, finite bound corners, jam/wrong
lead controls and identical-observation fault witness, full operation-ledger
replay; self-review only. No hardware qualification or new owner task.


## Axial proof extension: changed observability, insufficient labor benefit

A shared load cell/applicator and differential nut-to-collar probe could reject
some weak engagement that passes travel checks. React axial load through the
captured collar/cup into the frame, not the driver. Keep body antirotation nests;
a clearance catch limits failed-pair drop without carrying test load. Apply/unload
load first with screw angle locked, then with driver retracted and screw free.
Observe collar rotation independently: the disconnected driver encoder cannot do
this. Cup friction can hide back-driving and must be bounded. Charge seating,
frame flex and probe drift in the differential error. On power loss unload into
the catch; quarantine failures. This functional construction adds shared tooling,
no resident parts; it has no built/contact/clearance proof.

**Illustrative competing bounds, not selected test settings:** force0.40±0.02 N,
total differential error±0.04 mm, good stiffness10–40 N/mm, weak0.5–2 N/mm.
`displacement=force/stiffness` yields observed bands−0.0305…0.082 and0.150…0.880 mm.
A0.116-mm threshold separates replayed corners; negative readings represent error.
At±0.08-mm error bands overlap. E-286's original two±0.10-mm readings cannot do
this: a better gauge is a real requirement. No evidence locates real good/bad
populations in these stiffness bands. At20 N/mm and30° free rotation, lead3 gives
locked/free readings0.020/0.270 mm; two±2° angle bounds distinguish that event.
Smaller rotation, cup restraint, creep and crushing remain ambiguous.

A safe fracture-discrimination interval requires
`strongest_bad + force_error < command < weakest_good_nondamage − error − overshoot`.
Assumed bad.30/good.80/error.02/overshoot.05 N leaves(.32,.73) N; bad.40/good.35
leaves no interval. These are not measured strength bounds. The owner's loose-pair
near1-kg observation cannot supply them for new parts. **Do not select a proof
load from these examples.** Identical immediate stiffness/rotation can also hide
a latent fatigue/creep fault; the script preserves that indistinguishable witness.

Final insertion loads screw coordinates2…12 mm through the10-mm nut; S50 extension
loads52…62 mm. A damaged zone near30 mm is tested at neither endpoint. Loaded
full-stroke traversal or extra positions would cost further time; finite endpoint
proof does not qualify the intervening stroke or durability.

Two-position S50 inspection owes50 mm out/back:33.33 turns,16.67 s at assumed
120 rpm. Allocate12 s/position for locked/free loading, unloading and reading:
**40.67 s extra automatic dwell**, plus2 s active review/handling per attempt.
At1024/6400 usable pairs:11.57/72.30 station hours and0.57/3.56 active maker hours.
At80% usability:14.46/90.37 station hours and0.71/4.44 active hours. Attending dwell
adds those hours to maker time. The1024 optimistic labor saving falls1.12→0.55 h
before added fixture fabrication/calibration. Force/probe/angle hardware, setup,
reject damage and loaded traversal are unpriced additions to the$200–600 station
allowance. The$500/$1000/$1000–1500 comparisons and gameplay waits above persist.

**Retain locked/free axial inspection as a conditional diagnostic; keep the
assembly station parked.** It improves gross weak-contact/back-drive observability,
not general damaged-thread qualification. No fixture/feeder CAD, print, purchase
or owner question. Reopen with measured process/force/cup-restraint bounds or a
whole-pair process that materially removes handling. E-281 remains optional.
Verification in the existing script: force/compliance corners, overlapping-error
control, safe/no-window cases, latent-fault and unsampled-zone witnesses, and
operation ledger. Self-review; no hardware validation.
