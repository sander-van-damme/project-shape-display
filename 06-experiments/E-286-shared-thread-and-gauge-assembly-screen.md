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
or hardware measurements. Earlier detailed protocols remain in Git.

## Separate station: construction, detection and cost

Control geometry: E-277 integral136×10.3-mm closed column with10-mm nut; E-280
finished64-mm lead-3/90° screw,4-mm pilot, lower journal,4.4-mm collar/driver/socket.
Two side-opening nests restrain the body; a clamp reacts load without squeezing
the bore. A split collar cup and counterbalanced floating slide support the screw.
A reversible spindle seeks backward at most one turn, then threads under limited
preload/torque. No forced lead-matched Z: it could fake stripped-thread advance.
Measure actual collar-to-nut displacement, downstream angle and torque. Read2 then
16 turns; reverse2/return2; finish at nut bottom Z2. Full insertion owes62mm/20.67
turns plus pilot approach, not just pickup. Withdraw without rotation, open nests
laterally and transfer to operator. Catch falling parts; quarantine jams/unreadable
states, with at most one low-torque reverse. Stop repeated lot failures.

Per station: nests, clamp, cup, spindle/angle sensor, float/counterbalance, position
and torque channels, guard/controller/catch. Per cell remain body+screw, thread,
socket, collar support and two guide apertures:2048/12800 pieces at1024/6400.
Feeding would add two oriented streams, transfers, escapements and reject diversion;
none is credited. [DEPRAG's process overview](https://www.deprag.com/en/screwdriving-technology/deprag-apps/)
supports torque/angle/depth instrumentation, not this polymer application or accuracy.

**Assumed bounds:** lead3±.06mm/turn, gain±.2%, datum±.15mm, reading±.10mm,
lost motion±.30mm. Common datum cancels within segments, not final position.
Final±.7mm contains .15+.10+.124 gain+.30 seating. E-256's rough1-mm play does not
justify these tighter bounds. Two-/16-turn intervals5.368–6.633/46.445–49.559mm
admit all243 corners/reversals. Stall≤.5mm/turn fails;2.7-mm lead can pass2 turns
but fails16. No process prevalence is inferred. Damaged same-lead flanks can give
identical travel/low torque to good threads: these channels cannot distinguish them.
Entry burrs, tilt, offset and shared shrinkage remain unmodeled. Safe torque needs
`good maximum + error < trip < damage minimum − overshoot`; no measured window.

Manual allocations: three3-s handling actions +5/15/30s threading +4s gauge
=18/28/43s, five operations. Station: same handling +1s start =10s, four operations;
dwell19.33s from24.67 turns at assumed120rpm +7s overhead. Serial123 attempts/h
versus manual200/129/84. Dwell is maker time unless useful work overlaps it.
Station setup4–12h; table uses4h. Common work: frame/electrical8–16h, four channels
10–30min each, removal/gauge10–30s/component, install8–20s/pair,5min/plate in two
assumed289-up streams. Packing, yield, cleanup and repair are unqualified.

|N; all usable|Manual fast/mid/slow assembly h|Station active/serial h|Whole maker manual-mid/station-active h|
|---|---:|---:|---:|
|1024|5.12/7.96/12.23|6.84/12.34|25.26–49.39/24.14–48.27|
|6400|32/49.78/76.44|21.78/56.15|112.06–213.83/84.06–185.83|

At1024 only1.12h saving;12h setup reverses it. Ideal threading break-even11.06s.
Attending dwell adds5.50/34.37h. Touches5120→4096 or32000→25600 exclude external
work. At80% usable, ceil(N/.8) attempts plus60s/reject give whole maker
station30.71–57.68 versus manual33.11–60.08h at1024; at6400 station
124.89–244.44 versus manual160.89–280.44h. Equal usability is an assumption.
Unquoted station allowance$200–600 plus E-276 four-output$798–1768 =$998–2368
before exclusions. Reusing a spindle does not supply free gauges/calibration.

## Axial proof improves observation, not qualification

Add force applicator/load cell and differential nut-to-collar probe; react through
cup/frame, not spindle. Catch stays clear during measurement. Load/unload with
angle locked, then spindle withdrawn/screw free; independently observe collar
angle. Cup friction, frame flex, seating and drift need bounds. Unload into catch
on power loss; quarantine failures. No constructed fixture or physical proof.

Illustrative0.40±.02N, displacement error±.04mm, good stiffness10–40N/mm and
weak.5–2N/mm give bands−.0305….082/.150….880mm: threshold.116 separates corners;
±.08mm errors overlap. Original two±.10mm readings cannot discriminate. At20N/mm,
30° free rotation gives locked/free.020/.270mm; two±2° errors resolve it. Smaller
motion/cup restraint remain ambiguous. Safe destructive discrimination needs
`strongest_bad + error < command < weakest_good_nondamage − error − overshoot`.
Bad.30/good.80/error.02/overshoot.05N gives(.32,.73)N;bad.40/good.35 gives none.
Owner's near1kg loose-pair observation supplies neither bound. Identical immediate
stiffness/angle can conceal latent fatigue/creep. Endpoint nuts contact Z2…12 and
52…62; damage near30mm escapes both. Loaded traversal still cannot prove endurance.

Two-position S50 proof adds33.33 turns/16.67s at120rpm +24s static dwell and2s
active review. At1024/6400:11.57/72.30h dwell and.57/3.56h active; at80% usable:
14.46/90.37 and.71/4.44h. Optimistic1024 saving drops1.12→.55h before fixture
setup/hardware/damage. Park until measured process/force bounds or a construction
removes handling; no extra owner print.

## Install extended pairs and reuse the writer

At nut bottom Z52, four lead-3 turns from first contact engage the complete10-mm
nut at Z52…62. Two turns leave6mm engagement at Z58, beyond screened S50 travel.
Full engagement is geometry, not strength. During empty, unpowered assembly, a
cradle supports each started pair/collar while its column enters both guides.
Close journal/thrust/capture layers before releasing it. The4.4-mm collar cannot
pass a close2.8-mm journal aperture: split/open layers or ordered assembly are owed.
Cradle manufacture, handling and removal are unpriced. No miniatures at startup.
Writer lowers from S50 to minimum or true N20/N30; stop on jam/unreadable height.
Motor counts are not actual-height proof. Undocking still requires passive holding.
A mid-stroke jam remains a service fault. Empty-board assembly does not authorize
opening shared keepers on a played-on board or homing unchanged neighbors.

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

Speeds/overhead are assumptions, not E-276 route replay. Scale4/6.25 for4096/6400;
concurrency/fit are unqualified. Direct neutral descent avoids minimum-then-rise
but does not test full stroke. Do not add old minimum-to-neutral time on top.
Fully attending120rpm minimum startup leaves1.56h saving at1024 before extras,
conservatively charging all startup without prior commissioning credit. Separate
$200–600 station disappears only if existing writer/inspection can do its job.
Printing is unchanged: integral-U/closed completed-pair repetitions676.31/794.07h
at1024, not X1C forecasts. Retain this simpler assembly control, not fixture CAD.

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
radial envelope. This planar bound excludes locks/guides/frame stiffness. Collar
fits upward through illustrative10.8-mm body guide, not closed3.2-mm keeper.
Body straightness/yaw and any separate upper-bearing extraction remain owed.

Sequence: disable writer; keep bottom plate bolted; remove target miniature and
secure target; open rails; lift/replace pair; close/lock rails; verify height,
capture/rotation before enabling. Broken pairs may need separate screw retrieval
from below. Overhead access/avoiding neighboring terrain are unconstructed.
No row homing or neighbor motion is credited.31 neighbors (79 at80-wide) lose
lower radial guidance/upward capture; threads/column guides are unproven substitutes.
A temporary keeper must engage before opening if those constraints are required;
it is not constructed. A boolean graph does not prove the handoff. Plate settlement
changes surface height one-for-one at fixed angle. Power-off does not remove handling
loads. Park comb/latch/fit detail without a complete supported sequence.

Tool AF±.05mm, aperture/driver diameter±.10mm and eccentricity0… .10mm give16
assumed corners: minimum radial tool clearance.0664mm, annular width.600mm and
conservative ring area6.974mm². Not process tolerances, socket strength or rotating
contact proof. Uniform-pressure mean friction radius1.8296mm gives drag.0366…
.1464Nmm at.2N, assumed μ=.1… .4; at.338N,.0618… .2474Nmm. Rebuild torque before
claiming speed; avoid double-counting an existing thrust allowance. Numerical
annular quadrature agrees with the identity within3e-10mm; not friction validation.

At1024:2048 unchanged bodies+screws;64 half-rails,1024 annular contact/aperture
sites,2048 half-journal features, illustrative128 locks. At6400:160 rails,6400
annuli,12800 half-journals,320 locks; counts only, not fine-pitch fit. Sheet machining,
molding/modular FDM are unqualified options;400mm exceeds one X1C bed.10–30s per
rail placement/lock adds.53–1.60h at1024 or1.33–4h at6400 before alignment/tooling.
Material against1.56h attended-run-in savings, but manual assembly also owes support
installation: no net saving claimed. No per-cell latch components are added.

## Product boundary and decision

E-276's$798–1768 coarse allocation does not price this new support/lock/inspection
stack. Preserve~$500 reference/~$1000 finished/$1000–1500 demonstrator comparisons;
no new price or purchase claim. S40/S50 local26.84/31.07s,scene201/223s,paid neutral
271/332s,dense392/452s remain inherited conditional comparisons versus~30s; new thrust
friction has not earned their speed. Minimum/elevated neutral and real bidirectional
travel remain kinematic possibilities, not support qualification.

**New result:** opening a row need not transfer gravity load, but complete neighbor
restraint and damaged-pair extraction are unresolved. Reopen through a concrete
constraint-preserving service path or actual support/handling evidence. Closed-bore
failure, open-row control, finite corners, settlement and ledger checks are self-review.
No new owner print/purchase; E-281 remains optional.
