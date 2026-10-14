---
status: complete
builds-on: [E-285, E-277, E-279, E-280]
---

# Shared assembly, proof and installed run-in

**Park the hand-fed assembly/proof station; retain installed run-in as a simpler
conditional control.** Travel/torque cannot exclude damaged same-lead threads;
axial proof adds limited discrimination and substantial dwell. No construction
qualifies support, process yield, safe torque, speed or repair. Evidence is
self-reviewed analytical identities, bounded observations and operation ledgers,
not contact simulation or hardware measurements.

`tools/curated-experiment-checks/E-286.py` preserves all observation/fault cases,
force windows and full labor replays. Earlier prose is archived in Git.

## Separate station: construction and observation

Use E-277 integral136×10.3-mm closed columns with10-mm bottom nuts and E-280
finished screws:64-mm lead-3/90° thread,4-mm pilot, lower journal,4.4-mm collar
and underside socket. Unchanged geometry; a U body needs a different nest.

- Two side-opening square nests locate the nut bottom and resist body rotation;
  a broad clamp reacts axial load without squeezing the bore.
- A retractable split collar cup captures/aligns the screw. A reversible spindle
  and counterbalanced floating axial slide approach under limited preload. Seek
  backward at most one turn, then forward at low torque. No entry bevel or
  demonstrated radial-float alignment envelope is credited.
- Let the thread pull the slide; imposed lead-matched Z could fake advancement
  through a stripped nut. Probe actual collar-to-nut travel; measure spindle angle
  downstream of slip and torque independently.
- After pickup, measure2 turns then16 turns, reverse2 and return2. Finish at nut
  bottom Z2: insertion is62mm/20.67 turns plus4-mm pilot approach, not just pickup.
- Verify final position, withdraw driver without rotation, open cup/nests laterally
  and transfer support to the operator. A catch prevents falling parts on power
  loss. On jam/unreadable datum/excess torque, stop; at most one low-torque reverse,
  otherwise remove the intact jammed pair sideways to quarantine. No forced release.
  Repeated lot failures stop that lot;60s reject handling below excludes reprinting.

Per shared station: two nests, clamp, cup, spindle/angle channel, float guide and
counterbalance, actual-position channel, torque sensing/limiter, guard/controller,
catch/reject trays. Precision machining is permissible but costed; printed/cast
fixtures need calibration/wear evidence. Per cell remain body+screw, thread,
socket, collar/bed support and two guide apertures:2048/12800 pieces at1024/6400.
No resident interface removed. Automated feeding would add two orientation streams,
transfers, presence sensing, escapements and reject diversion; none is credited.

[DEPRAG's process overview](https://www.deprag.com/en/screwdriving-technology/deprag-apps/)
supports torque/angle/depth monitoring as an instrumentation principle, not this
polymer application, its price or accuracy.

**Assumed bounds:** lead3±.06mm/turn, common gain±.2%, datum±.15mm, per-reading
error±.10mm, lost motion±.30mm. Common datum cancels within segments, not final
position. Required final window±.7mm contains .15 datum+.10 reading+.124 gain+
.30 seating allowance. E-256's rough1-mm play does not justify this tighter bound.
Two-/16-turn acceptance intervals:5.368–6.633/46.445–49.559mm. All243 bounded
corners pass including reverse directions. Stall≤.5mm/turn fails;2.7-mm lead can
pass two turns but fails16. Broader error expands ambiguity; no process prevalence.

**Decisive witness:** damaged same-lead flanks can have identical forward/reverse
travel and low torque to a good thread. Any classifier using only these channels
accepts both or rejects both. This admissible fault is not a measured incidence.
Entry burrs, offsets, tilt and shared shrinkage remain unmodeled. Example torque
.7 accepted/1.6 rejected at1.5Nmm demonstrates logic only. Safe operation requires
`good maximum + error < trip < damage minimum − overshoot`; no bounds establish
that window. More sensor precision or lower RPM alone does not resolve the fault.

## Station economics

All times are allocations. Manual: load body3s, screw3s, unload3s, threading5/15/30s,
functional gauge4s =18/28/43s and five operations/pair. Station has the same three
handling operations plus1s guard/start=10s/four operations. Automatic dwell19.33s
is24.67 turns at assumed120rpm plus7s seek/approach/read/retraction. Serial rate123
attempts/h versus manual200/129/84. Dwell counts as maker time unless useful work
actually overlaps it; a hand-loaded tray is not a feeder.

Station setup4–12h; table uses4h. Common whole-machine work:8–16h frame/electrical,
four channels10–30min each, removal/gauge10–30s/component, install8–20s/pair,
and5min/plate in two assumed289-up streams. Packing/stability, cleanup, material
scrap, printing occupancy and repair remain unqualified.

|N; all usable|Manual assembly fast/mid/slow h|Station active/serial h|Whole maker manual-mid/station-active h|
|---|---:|---:|---:|
|1024|5.12/7.96/12.23|6.84/12.34|25.26–49.39/24.14–48.27|
|6400|32.00/49.78/76.44|21.78/56.15|112.06–213.83/84.06–185.83|

Attending dwell adds5.50/34.37h. At1024 saving is only1.12h;12h setup reverses it.
Ideal threading break-even11.06s; at6400 handling/gauge savings alone repay4h.
Touches5120→4096 and32000→25600 exclude external work/rejects. At80% usable,
ceil(N/.8) attempts+60s/reject give manual-mid/station assembly14.22/11.82h and
88.89/52.89h; whole maker33.11–60.08/30.71–57.68h and160.89–280.44/124.89–244.44h.
Equal usability is a scenario, not evidence of fault detection or independent lots.

Unquoted tooling allowance: spindle/control/torque$80–250, slide/nests/cup$60–200,
position/guard$60–150 =$200–600. With E-276 four-output$798–1768, total$998–2368
before exclusions. Reusing a spindle does not supply gauges/calibration for free.
Against~$500 reference/~$1000 finished/$1000–1500 demonstrator, no purchase or
selection.10.3-mm bodies do not fit5.08/6.35 pitch;6400 is replication only.
E-276 coarse S40/S50 conditional local26.84/31.07s,scene201/223s,paid N20/N30
neutral271/332s,dense392/452s remain against~30s. Completed integral-U/closed
print repetitions676.31/794.07h at1024 are unchanged, not X1C forecasts.

## Axial proof: better observability, limited benefit

Add shared force applicator/load cell and differential nut-to-collar probe.
React through collar/cup into frame, not driver; nests resist rotation. A clearance
catch limits failure drop without carrying test load. Load/unload with angle locked,
then driver retracted/screw free. Observe collar angle independently; disconnected
encoder cannot do so. Bound cup friction, seating, frame flex and drift. Unload into
catch on power loss; quarantine failures. No geometry or physical proof.

**Illustrative bounds, not chosen proof settings:**0.40±.02N, displacement error
±.04mm, good stiffness10–40N/mm, weak.5–2N/mm yield bands−.0305….082 and.150….880mm.
Threshold.116 separates the corners;±.08mm error overlaps. Original two±.10mm
readings cannot discriminate these cases. At20N/mm and30° free rotation, lead3
produces locked/free.020/.270mm; two±2° angle errors resolve it. Smaller motion,
cup restraint, crushing/creep remain ambiguous. Real populations are unmeasured.

Safe fracture discrimination requires
`strongest_bad + error < command < weakest_good_nondamage − error − overshoot`.
Bad.30/good.80/error.02/overshoot.05N yields(.32,.73)N;bad.40/good.35 gives no window.
The owner's loose-pair near1kg observation supplies neither bound for these parts.
Identical immediate stiffness/angle can hide latent fatigue/creep: preserved fault
witness. Endpoint nuts contact screw Z2…12 and52…62; damage near30mm escapes both.
Full-stroke loaded traversal costs extra and still does not establish durability.

Two-position S50 proof adds50mm out/back=33.33 turns/16.67s at120rpm plus12s per
position locked/free load/unload/read=40.67s dwell, plus2s active review per attempt.
At1024/6400:11.57/72.30 extra station h and.57/3.56 active h; at80% usable:
14.46/90.37 and.71/4.44h. Attending dwell adds it to maker work. Optimistic1024
saving falls1.12→.55h before new fixture setup/force/probe/angle hardware, damage or
loaded traversal. Retain axial inspection as a diagnostic, not a qualification
station. Reopen with measured process/force/cup-restraint bounds or a construction
that removes material handling. No new print; E-281 remains optional.

## Install extended pairs; use the display writer for run-in

**Retain as a conditional assembly control, not a qualified installation route.**
This removes the separate station by moving most initial threading into the
existing writer. It does not remove resident parts, inspection or support access.
The existing script now checks insertion identities and a fresh operation ledger;
no new CAD, physical evidence, loaded RPM or sensor capability is claimed.

Start each pair manually with nut bottom at screw Z52: four lead-3 turns from
first thread contact, excluding the separate pilot approach. The entire10-mm nut
then engages Z52…62 within the64-mm thread, at the existing S50 upper position.
Two turns instead put the nut at Z58 with only6-mm engagement and exceed that
screened travel by6mm. Do not use the owner's broken, lightly engaged specimen
as permission to install at arbitrary partial engagement. Full nominal engagement
is a geometry result, not a strength or static-holding qualification.

Construction for an **empty, unpowered first assembly**: hold each started pair
in a reusable cradle, support the screw collar independently, and introduce its
column through both antirotation guides without turning it. Assemble the shared
journal/thrust/capture layers around the screw ends before releasing the cradle.
The E-280 lower journal is2.8mm but collar/driver is4.4mm: an intact close journal
bore cannot admit that collar axially. Split/open layers or an ordered frame
assembly are therefore necessary, not already constructed. This access obligation
also exists for fully inserted pairs; it is not a newly invented incremental cost.
A reusable row cradle must contain a slipping column without loading neighbors,
and remain until passive holding and capture are established. Its manufacture,
handling, clearance and removal are unpriced. No miniatures during commissioning.

With capture closed, the writer reversibly lowers columns from S50 to minimum
or an actual N20/N30 neutral. Stop on jam, unreadable height or failed motion;
do not force through. Encoder turns alone still cannot distinguish E-286's
same-lead damage. After undocking, the thread/bed must hold each column; a catch
or cradle cannot silently substitute for demonstrated holding. Final commanded
height is not a gauge. The independent travel/axial-proof limitations above remain.
A mid-stroke jam retains the pair for service, not automatic acceptance after retry.

A replacement in a played-on board cannot inherit this empty-board procedure:
opening a shared keeper may compromise unchanged neighbors. Independent extraction
and capture, or supported removal of a module, remain unconstructed. No whole-board
homing is allowed as a local repair substitute. These are reasons not to advance
installation CAD from this labor calculation alone.

**Assumed labor:** split the existing15-s manual threading allocation into5-s
pickup plus10-s rotation for20.67 turns. Four-turn starting then costs6.94s;
saving8.06s/pair, rather than scaling pickup away. Retain all other E-286 manual
handling/gauging and common work. At1024, theoretical saving is2.29 maker h and
whole maker labor22.97–47.09h **before cradle/setup, inspection additions, rejects
and startup attendance**. At4096/6400 the savings are9.18/14.34h and whole maker
65.71–134.20/97.72–199.50h. These are replication controls:10.3-mm columns still do
not fit6.35/5.08-mm pitch. No yield or handling measurements justify the allocations.

A separate commissioning scenario uses four simultaneous spindles, ideal batches,
and2s per visit for motion/docking/read/retraction. This is not E-276's route replay.

|1024 cells; destination|Run-in turns/cell|120rpm startup min|850rpm startup min|
|---|---:|---:|---:|
|Minimum|16.67|44.09|13.55|
|N20|10|29.87|11.55|
|N30|6.67|22.76|10.54|

Both speeds and visit overhead are assumptions. Multiply durations by4/6.25 for
4096/6400; four-way concurrency and physical compatibility are not qualified there.
Direct descent to neutral avoids minimum-then-rise but does not visit the whole
stroke, prove height or test every thread zone. Do not add the old minimum-to-neutral
time on top of this alternative startup; do not hide it as free preparation either.
If the entire120rpm minimum run-in is attended, the1024 saving falls to1.56h before
extra setup/cradle work (conservatively charging all run-in without credit for prior
commissioning). That is the extra-work break-even ceiling, not a measured benefit.

No separate$200–600 station is needed *if* existing writer and added inspection
can perform the job; their capability is not earned by this substitution. E-276's
$798–1768 bought allocation, ~30-s/local versus scene/dense comparisons above,
~$500 reference and$1000–1500 demonstrator distinction remain. Printing is unchanged.
**Decision:** keep this simpler boundary choice beside the separate-station control;
do not build another dedicated assembly fixture. Reopen implementation through a
shared support/service construction that admits completed screws and preserves
neighbor support, or actual-process evidence. No new print or purchase; E-281
remains optional. Verification: exact turn/engagement identities, two-turn failure
control, aperture-order obstruction and full labor/startup replay; self-review only.


## Separate bottom thrust from the opening row keeper

**A fixed bottom plate preserves gravity support while a row keeper opens, but
not radial guidance or upward restraint.** Retain this support decomposition;
park repair-fixture detail. This changes shared structure, not per-cell latches.
The script checks finite aperture bounds, transverse opening, constraint states,
friction and replication; no CAD/contact/deflection or physical qualification.

E-280's collar and driver both have4.4-mm diameter: **no lower collar shoulder**
exists between them. Support the driver bottom at Z−10 on a fixed plate with a
2.8-mm aperture. It admits the2-mm-AF hex tool (2.309mm corner diameter), leaving
an annular thrust face. Load: nut→screw→driver end→plate→frame. Socket burrs,
end flatness, wear, plate sag and friction remain repeated-interface obligations.
Two locked row half-rails surround the2.8-mm journals at Z−4…0 with3.2-mm bores;
their underside captures the collar upward. Clearance/preload is unqualified.

Retract both rails sideways for service. At12.7-mm pitch, assumed4.5-mm half-width
and2.4-mm outward travel leave1.3mm to the neighboring closed rail; opening exceeds
collar radius2.2mm plus an illustrative.1mm radial envelope. This planar bound
excludes locks, transverse guides, end access and frame stiffness. No fine-pitch
fit claim. The4.4-mm collar can move upward through an illustrative10.8-mm body
guide, but not the closed3.2-mm keeper. Body straightness/yaw remain unqualified;
any separate fixed upper bearing must also admit extraction.

Sequence: disable writer; leave bottom plate bolted; remove target miniature and
secure target; open rails; lift/replace pair; close/lock rails; verify actual height,
capture and free rotation before enabling writer. Broken/stripped pairs may require
separate screw retrieval from below. Overhead extraction clearance and avoiding
nearby terrain/miniatures are unconstructed. No row homing or neighbor motion is
credited. Unlike a load-bearing clamshell, opening does not remove gravity support.
However,31 neighbors (79 at80-wide) lose lower radial guidance/upward capture.
Their threads/column guides are not proven substitutes. A temporary keeper could
restore those constraints **only if constructed and engaged before withdrawal**;
a boolean support graph is not that construction. Do not add comb/latch/fit detail
without an earned support handoff. Bottom-plate settlement changes surface height
one-for-one even at fixed screw angle. Power-off does not eliminate handling loads.

**Assumed bounds, not printer tolerances:** tool AF±.05mm, aperture/driver diameter
±.10mm and eccentricity0… .10mm give16 corners. Minimum tool radial clearance
.0664mm, annular width.600mm and conservative complete-ring area6.974mm² are
positive; no socket-strength or continuous rotating-envelope proof. Uniform-pressure
mean friction radius1.8296mm gives drag.0366… .1464Nmm at.2N and assumed μ=.1… .4;
at.338N,.0618… .2474Nmm. Rebuild the torque budget before claiming speed; do not
add this twice if an older allowance already includes a thrust bearing. Actual
preload, contact, friction and wear are unknown.

At1024 sites: unchanged2048 bodies+screws;64 half-rails,1024 thrust apertures/contact
sites,2048 half-journal features and illustrative128 rail locks. At6400:160 rails,
6400 annuli,12800 half-journals,320 locks; replication only, not5.08/6.35-mm fit.
Sheet machining, molding or modular FDM are unqualified process options;400mm
exceeds one X1C bed. At10–30s per rail placement/lock, assembly adds.53–1.60h at1024
or1.33–4h at6400 before alignment/gauging/tooling. This is material against1.56h
attended-run-in savings; net savings require charging equivalent support assembly
to the manual control too. No thousands of individual latch components are added.

The existing$798–1768 coarse allocation does not price this support/lock/inspection
stack. Keep~$500/~$1000 finished/$1000–1500 demonstrator comparisons without claiming
a new price. Inherited S40/S50 local26.84/31.07s,scene201/223s,neutral271/332s and
dense392/452s remain conditional versus~30s: this friction has not earned their
speed. Minimum/elevated neutral and real bidirectional travel remain kinematic
possibilities, not support qualification. No new print/purchase; E-281 optional.
**New decision:** a row opening need not transfer gravity load, but complete neighbor
restraint and damaged-pair extraction remain unresolved. Reopen through a concrete
constraint-preserving service path or actual support/handling evidence. Closed-bore
failure, open-row control, finite corners, settlement and ledger checks are self-review.
