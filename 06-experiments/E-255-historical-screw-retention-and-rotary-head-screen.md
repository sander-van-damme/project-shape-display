---
status: complete
builds-on: [E-254, E-050, E-131, E-156, E-182, E-222]
---

# Historical screw support and complete rotary programming screen

**The screw supports the pin through its engaged thread.** Sander's clarification
refers to that pin, not a platform. Preserve his reported working physical mechanism;
the writer need not lift or take over the pin's axial load. Fixed screw angle and
intact engagement give fixed pin height. Whether an undriven screw maintains that
angle is a separate friction/rotation question, not an absent pin-support path.

**Retain two independent row heads as the conditional reference.** Signed moves and
mask rewrites need three shared heads/240 selectors versus two independent heads/160
spindles on E-254's nine main transitions. Neither has qualified retention, running
drives or a complete purchasable BOM. Trial5 is not the identified successful print.

Evidence: source inspection, analytical bounds, schedules, ideal replay and supplier
observations; **self-review, no new physical tests**. Reproduce with
`python3 tools/curated-experiment-checks/E-255/screen.py`; stdout is disposable.
Rates/costs are assumptions; E-254's convenience sample is not representative play.

## Recovered mechanism and dependency boundary

Inspected trial1/3 SCAD and trial5 actuator/frame/calibration files at41484f96999847c139b9010e73009d73e9459c89 (2025-01-04). BOSL2 is unpinned. Comparison:
[BOSL2 136e636](https://github.com/BelfrySCAD/BOSL2/blob/136e6367e65d52196a3ea51d03156f8b622c60fc/threading.scad),
last upstream commit before that snapshot (2024-12-30, version2.0.716), **not the
identified print dependency**. No new CAD or wholesale restoration.

| Source | Recovered CAD facts, not measured fits |
|---|---|
| Trial 1 | v1 screw: OD2/pitch1/length70, collars/neck/gear. v2/v3: OD4/pitch2/length50, one collar. cube-v2: width4.9/length50/top cap/10-mm nut, nut `$slop=.1`. Different variants. |
| Trial 3 | Width6/length50/wall.9/cap/10-mm nut; OD4/pitch2/length50 screw, `$slop=.65`, slotted drive. OD4.5 collars/2-mm-long OD2.5 neck can straddle 1.9-mm plank with 3-mm edge-open holes: .1-mm axial/.5-mm diametral allowances. Plank pitch6.35, 1-mm edges in frame slots1.1. Possible thrust reaction, not assembled proof or target pitch. |
| Trial 5 | Width4.4/length50.8/wall.44/10-mm embedded nut, no cap. Screw OD3.2/length50/pitch3/depth.9; nut ID3.4/depth1.35; `$slop=.65`. No collars/socket/thrust plate/end stops. Grid45×45: opening4.64/web.44/height55.8, pitch5.08, exterior229.04; .12-mm nominal side gap. Relative axial placement unspecified. |
| Calibration | Trial3 screw coupon OD4/pitch2/length10/slop.95; trial5 OD4/pitch2 with no slop override: neither matches trial5 actuator. Trial5 tube widths4.64±.3 in .1 steps; trial3 walls1/.84/.43. Intentional variations, not process errors. |

Comparison-library defaults: one start, right handed, included flank angle30°,
radial depth=pitch/2. Lead is therefore **3 mm**, 13⅓ turns/40 mm. Negative
`zdistribute` sizes embed the nut in the tube end, not a negative nut length.

**Dependency failure witness:** the internal cutter adds `2*get_slop()` radially.
Trial5 minimum radius is `3.4/2+2*.65-1.35=1.65 mm` > screw crest1.60. Faceting
does not close it: no concentric flank engagement in this reconstruction. Trial3
minimum radius2.00 already equals its screw crest before faceting. This does not
contradict the successful print; its actual variant/library remains unidentified.

An engaged 50-mm screw/10-mm nut permits at most40-mm full-overlap travel before
bevel/runout/end margins. More length is needed to retain that travel with margins.
The torque driver may withdraw while the resident screw supports the pin;
withdrawing the screw itself requires another support.

## Hold, source loss, disconnect and repair

Path: **pin → nut flank → screw flank → resident thrust seat → frame**; square
guides react torque. Trial3 suggests the seat; trial5 omits it. No separate pin latch
is inherent. Breakage/unthreading/loss of thrust seat are distinct from backdrive.

For a sliding trapezoidal-thread approximation, half-angle15°, mean radius r,
`s=lead/(2πr)`, effective friction `u=μ/cos(15°)`, lowering torque per axial force is
`T/W=r(u-s)/(1+u*s)`. Positive T requires applied lowering torque; negative T can
backdrive. Add collar resistance `μc*rc` when a loaded grounded collar actually
exists. [Roton's screw explanation](https://www.roton.com/screw-university/screw-actions/screw-backdriving-efficiency/)
supports distinguishing driving from backdriving; this model is not a PLA friction prior.

Mean diameter3 gives thread-only μ>.3075; the trial5 external-depth midpoint d2.3
needs **μ>.4010**. Actual contact is unestablished. At d2.3/μ=.3, lowering torque is
−.1066 N mm/N; assumed collar μc=.1/radius2 adds .2 and can hold. At thread μ=.1
that collar is insufficient. Do not discard the collar in assessing a successful
print, or assume its friction without evidence.

The labelled μstatic=.5/μkinetic=.1 corner holds at rest yet may continue lowering
after source loss. At 3,000 rpm/lead3, 1/5/20-ms delay before deceleration adds
.15/.75/3 mm. These are delay distances, not stopping distances: source inertia,
coupler release and dynamic friction remain unknown. A head brake cannot stop a
disconnected backdriving screw. E-156's rotating-nut coast values do not transfer
numerically to this rotating screw. Static hold and moving loss are separate tests.

Nominal sequence: dock without unloading, verify engagement, turn selected screws,
decelerate, check height/retention, withdraw torque tool and check drift. A camera
cannot certify hidden flank strength; turns cannot detect skipped sockets. Retry
from observed supported heights. Prop a broken/jammed pin before replacing its
underside screw/cartridge; re-home only that site. Damage repair has no <30-s promise.

## Whole-machine schedules and true selection

E-254 rates: translation200 mm/s/5,000 mm/s²; rotation3,000 rpm/60,000 rpm/s.
Independent row dwell: .08-s dock/release + .02-s proof + rest-to-rest spin of
max|delta|/3. Add4 common seconds, actual seeks, empty return and one immediate
station retry. Parallel selective docking, actual-height proof and these deadlines
are unqualified assumptions.

**Stopped reusable-mask head:** one reversible power shaft/head, 80 selectable rotary
outputs. An 80-bit physical mask selects head couplings; it carries commands, not pin
weight. For each sign, sort requested magnitudes; rotate to the first height, stop,
retire finished outputs, then continue the remaining subset. Every stop rewrites all
80 mask bits in an assumed10 ms with 80 parallel writers, plus20 ms for command proof
and stationary coupling transfer. Clear the mask after the last segment. Both signs
are serialized. E.g. deltas `[+10,+40,-20,0]` use +10,+30,−20 with different masks;
the unchanged output stays uncoupled. **15,625 three-cell transitions** replay exact
final heights, monotonic changed-cell paths and unchanged cells ideally. A physical
bidirectional dog/gear path, tooth phasing, torsional compliance and mis-selection
remain unbuilt. No synchronizer or loaded clutch has been credited as free.

| E-254 transition | Independent B2/160 s | Mask B2/160 s | Mask B3/240 s | Four 16-output heads s |
|---|---:|---:|---:|---:|
| Flat→ruins | 18.30 | 22.56 | 16.43 | 40.62 |
| Flat→road | 17.45 | 21.11 | 15.99 | 65.31 |
| Flat→ravine | 22.98 | 26.72 | 19.80 | 87.36 |
| Ruins↔road | 17.98 | 28.63 | 20.70 | 72.49 |
| Ruins↔ravine | 22.78 | 35.16 | 26.18 | 86.76 |
| Road↔ravine | 21.65 | 33.48 | 25.23 | 81.23 |
| Local ruins/road/ravine reveal | 11.77/8.89/14.14 | 12.85/9.67/15.40 | 9.97/7.84/10.90 | 11.77/16.85/30.07 |
| Separate dense flat→40 | 24.65 | 27.11 | 19.75 | 93.70 |
| Separate dense alternating +40/−40 | 24.65 | 41.32 | 29.46 | 93.70 |

Four smaller heads each own a 40×40 quadrant, processing 16/16/8-cell strips with
simultaneous XY travel and return. Other tilings are not excluded. Two orthogonal
80-tip heads, conservatively only one active, choose the faster whole-map direction:
principal-sample maximum 41.42 s; local reveals 9.81/8.89/14.14 s. One reorientable
80-tip head adds .5-s total outbound/return yaw plus two 401.32-mm parking legs for
vertical orientation: maximum 41.42 s; local 11.77/8.89/14.14 s. An 80-tip line spans
401.32 mm and sweeps radius ≥200.66 mm plus width/clearance. No collision-cleared yaw
assembly is inferred. Concurrent crossing heads or mixed-direction covers remain
unbuilt alternatives, not rejected by this conservative schedule.

B3 main mask decisions: 14,880/14,720/15,040 for initial ruins/road/ravine and 26,080
for ruins↔ravine, **plus retry masks**. Independent initial changed sockets number
867/4,449/4,575. Unchanged pins keep resident support; frame flexure, accidental
socket contact and guide drag still need disturbance bounds.

Mask write50 rather than10 ms needs B4/320 (24.46-s sample maximum); proof100 rather
than20 ms gives B3/28.34 s. At1,500 rpm independent needs B3/240 (22.84 s), mask
B4/320 (26.33 s). This sensitivity makes running speed and real proof/writing time
decision-relevant; nominal 3,000 rpm alone is not a motor selection.

**Row-column AND:** two normally open serial torque interruptions/site could implement
bidirectional coincidence, but repeat 12,800 clutch contacts and 6,400 output paths
besides distribution. Two selected rows and columns activate four intersections:
the two-diagonal witness produces two unwanted outputs. Serial addressing avoids
this but inherits E-254's thousands of visits. Flux selection retains E-182's
half-selection issue. Neither 160 logical lines nor a mask is a torque-path proof;
stop resident clutch CAD.

**Pre-positioning:** for known local reveals, B2 visible times become11.15/8.35/13.59 s
by moving to the first station before submission. Sustained preparation-inclusive
times remain11.77/8.89/14.14 s. Return/retry/checking stay counted. Unknown or wrongly
predicted targets receive no credit; an adverse full-bank relocation adds up to1.031 s
to the ordinary schedule. This is a declared route bound, not observed play behavior.

## Replication, manufacture and complete bought allocation

Resident board: 6,400 each pins/screws/thread pairs/thrust seats/sockets/antirotation
duties, 12,800 spaced guide duties. They need not be separately bought bearings or
nuts. B2 repeats160 drive/dock/angle-feedback duties. Mask B3 repeats240 outputs,
mask states, writers and couplings plus three shafts/motors/brakes. Unspecified
springs/inserts/selective docks are implementation costs, not proven zero.

Favorable **allocation**, not sourced BOM: common controller20 + power/protection40 +
frame/datum60 + shared optics/lighting50 + harness20 + fasteners20 + freight/spares40
= **$250**. Resident purchased stock allowance$.02×6,400=$128. Per head:$55 for
transport motor/driver/rails/belts/bearings35, docking10 and wiring/registration10.
Mask adds$35/head for motor/driver15, shaft/journals10 and brake10.
Complete independent channel allocation$4: motor1.5, driver/angle sensing1,
socket/transmission.75, selective docking/returns.5, wiring/fasteners.25.
The mask$4/channel comparator allocates selector2.25, drive.50, coupling.75,
feedback.25 and wire/fasteners.25. These duties must all be supplied; the values do
not establish compatible parts.

| Architecture | Reserve before channels | $4 complete-channel scenario | Channel ceiling under $1,000 / $1,500 |
|---|---:|---:|---:|
| Independent B2/160 | $488 | **$1,128** | $3.20 / $6.325 |
| Stopped mask B3/240 | $648 | **$1,608** | $1.467 / $3.55 |

Under$500 leaves$.075/independent channel; mask reserve alone exceeds it. These are
allocations, not price floors. Free independent motors still give$888; cost-down
must reduce shared/resident/interface duties too. Research feasibility remains
conditional on rated motor/feedback/docking hardware, not a purchasable BOM.

[Adafruit2776](https://www.adafruit.com/product/2776), checked2026-10-12, lists$3.96
at100+ for the bare selector solenoid, above the mask's entire$3.55/channel allowance.
It draws1.1 A at5 V:240 continuously energized selectors would draw264 A/1.32 kW,
incompatible with the favorable power allowance. Latching masks/pulsed writers could
reduce duty but add real capture/reset mechanisms. The catalog solenoid route is
therefore not a viable$1,500 implementation; it does not establish a universal floor.

Manufacturing bounds, not priors: opposite ±.12-mm rod/opening biases close the
.24-mm diametral guide gap. Comparison-library slop must be below roughly.625 for
any trial5 radial engagement. Lead, friction and dimensions can correlate by batch;
independent-cell yield multiplication is unjustified. Wear, creep, debris, straightness
and head/frame alignment remain unmeasured.

Two 5/10-second placements per cell mean 17.8/35.6 maker hours before inspection;
even one 5-second insertion is 8.9 hours. Automatic run-in and tray loading require
jigs and batch rejection. E-254's ~6-L/111–333 extrusion-hour scenario is not sliced
production time. Compare FDM trays with machined masters/split polymer molds and
unscrewing cores; release, shrinkage and core handling can erase savings. Rolled or
machined metal screws need quotes, burr control and matching nuts; $.10/site already
costs $640. Precision couplers/bearings belong in shared heads where feasible.
Tooling, outsourcing, scrap and jig setup are extra; no 2–4-day assembly route is
established. Printed tooling alone does not establish metal-casting compatibility.

## Disposition

E-050/E-131 thread-friction and dense-rate bounds remain scoped; this workload and
coarse lead change their timing premise. E-156/E-182 preserve the moving-loss and
half-selection cautions, not a blanket ban on threaded pins. E-222's stopped-transfer
cost appears again in the mask schedule, although these pins retain their resident
threads and avoid its head-supported vertical load takeover. New evidence is the
historical dependency/engagement mismatch and the signed-mask/full-machine ranking.

**Stop before thread/head CAD, printing and purchases.** Do not add 6,400 brakes from
unknown friction alone. Next discriminator: identify/reuse the successful threaded
pair and its screw seat, then measure zero-speed drift, moving disconnect, torque
and travel under bounded loads. This can preserve lead3/B2 without extra resident
hardware or reveal the need for another lead/support arrangement. No new print is
selected while the recovered settings cannot identify that pair. Sander's holding
observation remains informal physical evidence; measured limits are not invented.

Verification:15,625 ideal transitions, no-op and dense controls, exact signed masks,
partial-move retry regeneration, Cartesian-product half-selection witness, E-254
B2/22.9835-s reproduction, independent
spin arithmetic, explicit budgets and library-source arithmetic. No finite routed
machine, process distribution, fault-stop distance or physical support qualification.
