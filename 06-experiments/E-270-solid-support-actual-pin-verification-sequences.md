---
status: complete
builds-on: [E-269, E-268, E-267]
---

# Top readback escapes opaque supports, but covered pins remain unknown

**Retain post-undock top sensing as a conditional architecture comparator.** A locally
centered narrow stereo view reaches low pins between high neighbors at both pitches, without
holes in any support or new resident sensing parts. A shared contact probe also reaches empty
tops, but introduces force and long serial inspection. Neither can verify a pin hidden under
an opaque miniature. Temporary exposure followed by a hidden move does not close that gap.
No head, sensor, print or purchase is selected; the screw campaign and solid support control
remain. This is new observation geometry and operating-sequence evidence, not a hardware pass.

Run `python3 tools/curated-experiment-checks/E-270/verification.py --check`; omit `--check` for
signed fault examples and complete schedule tables. Python plus inherited numpy dependencies.
**Evidence:** analytical bounds, finite ray/box calculations, fault witnesses and conditional
scheduling, self-reviewed. No optical performance, process distribution, safe RPM, contact-force
rating, loaded-neighbor isolation or physical qualification is established.

## Architecture discriminator

All routes retain E-269's opaque bed/keeper, solid screws, intact guides and proposed shared
ribs. Pin→thread→collar→fixed bed→frame remains the downward path; locked keeper→ribs handles
upward docking. Sensor movement does not release a keeper or take over the load. The fine
frame's adverse clearance failure remains; successful top visibility does not repair it.

|Route / sequence|Actual-pin information and finite access|Disposition|
|Underside reader after withdrawing drive|Removing the socket leaves the opaque bed/keeper between reader and pin; screw angle still aliases stripped threads.|Reject as sole height proof. More withdrawal does not make the support transparent.|
|Locally centered top stereo, after undock and settling|Two finite views of the integral terrain cap; clear deep-well construction below. Shared scanner or parallel entrance pupils.|Retain for visible tops, conditional on a real metric reader, identity and texture.|
|Top contact probe, after undock|Vertical stylus and independent measured probe Z find the actual cap; no inference from screw turns.|Retain as slow diagnostic/control for exposed tops; force and release behavior unqualified.|
|Lift to expose, read, then restore|A hidden final move can fail after a correct exposed reading; maximum-height neighbors also preclude lifting above them within stroke.|Reject as final proof. Direct observation must follow the last motion and release.|
|Extend a witness tail through the support|Would need 4096/6400 additional passages, long motion clearance and pin-to-witness integrity; a detached witness aliases terrain.|Reject under this task's repeated-interface/support constraints; no tail/hole refinement.|
|Remove miniature, inspect, replace|Exposes the cap but changes the load; replacing the miniature hides it again. Position restoration and load response are unknown.|Possible interrupted service workflow, not a qualified occupied-play update.|

A conventional overhead view is not automatically equivalent to locally centered pupils.
One stereo pair viewing an entire long row produces oblique edge rays; the per-cell ray
construction cannot be credited to that camera arrangement without its own coverage model.

## Finite top access: low wells and raised targets

Reuse E-261's 4.4-mm square pin and **assumed integral closed terrain cap**, including its
reserved cap thickness; an open tube or detachable cap is not this target. Normalize the
lowest cap to z=0, with highest neighbor z=S. Actual lowest tops are z88/98 for S40/S50,
above the guides and E-269 ribs. The reader therefore never crosses those supports.

Two pupils at x=±b/2, z=S+H view a .4-mm-square central cap patch. Pupil diameter .5 mm;
independent ±e lateral pupil/target placement and neighbor-face expansion. With t=S/(S+H),
a sufficient clearance to the nearest neighbor is

`m = pitch − 2.2 − e − [(b/2 + .25)t + .2(1−t) + e]`.

The affine ray envelope has its extreme at the high neighbor's top; all intermediate heights
are covered. Raising the target shortens the interval among neighbors. A conservative square
pupil envelope and exact solid-box intersections give the same clear/blocked classification
in the tested bounds. These are geometry assumptions, **not X1C or optical calibration priors**.

|Pitch, mm|S, mm|b4/H20/e.2 margin, mm|b4/H60/e.2 margin, mm|b20/H20/e.2 margin, mm|
|---|---:|---:|---:|---:|
|6.35|40|2.183|2.730|−3.150|
|6.35|50|2.086|2.618|−3.629|
|5.08|40|.913|1.460|−4.420|
|5.08|50|.816|1.348|−4.899|

The wide-view case has actual ray/neighbor intersections, not merely a failed sufficient bound.
The b4 construction also clears e=.4 in these cases. Common registration does not prove
correct cell identity: a whole-pitch indexing fault can read a perfectly valid wrong cap.

H60 leaves 20 mm above an illustrative 40-mm prop on the highest pin **at the pupil plane**;
reader housing and projection/illumination remain unconstructed. Any miniature intersecting
the ray volume still blocks it. With assumed f1200 pixels and .1-pixel disparity error,
`D²*.1/(1200*b)` is .208/.252 mm at D100/110, b4. This is sensitivity arithmetic, not achieved
accuracy or noise. Smooth identical caps, correspondence, focus over full depth, calibration,
lighting, shadows and stale/foreign returns still need a demonstrated reader. Granting .1-s
readout below supplies no evidence that such measurements are possible at that rate.

A probe of .5-mm radius with separate .2-mm positioning and .2-mm bow bounds has .9-mm swept
radius. Its landing margin within a contracted cap is 1.1 mm; nearest-pin clearance is
3.05/1.78 mm at coarse/fine pitch. It can descend vertically to a low empty cap without moving
its high neighbors. With an empty-board travel plane S+5, length/reach must cover45/55 mm.
H60 prop clearance increases required reach to100/110 mm. This is only swept geometry;
stylus stiffness, tip shape, Z metrology, crash limits and contact detection are unqualified.
At illustrative .05-N probing force and effective stiffness .1/1/10 N/mm, displacement is
.5/.05/.005 mm, before backlash or shared-frame movement. No nonzero force is declared safe.
A reading under probe force is not a hands-off retention measurement.

## What the sequence can and cannot distinguish

Use: stop drive → withdraw it (.1-s allocation) → settle (.1 s) → observe the actual cap with
fresh cell identity → accept/reject/unknown → retry only from a known stable measured state.
Opaque supports remain locked throughout. A lost socket and a stripped thread can both leave
the cap at the old height; top readback detects wrong height but does not identify the root
cause. Signed 10→20 and20→10 witnesses both reject. A pin at target while still assisted by
the driver, then wrong after release, defeats in-drive proof but fails post-undock inspection.
Creep **after** that snapshot remains indistinguishable from correct operation: load retention
and power-loss safety require mechanical evidence, not another encoder assumption.

An opaque 25.4-mm miniature base held by neighboring pins can bridge a center pin. Center
heights0 and−1 mm have identical visible base position and identical contact-probe hits on
the base. This is an explicit loaded-neighbor/hidden-pin alias, even with perfect sensing of
the miniature. Observing or probing its top cannot certify every supporting pin. Mask the full
miniature/prop obstacle volume; a missing, stale, occluded or misidentified cap returns
**unknown**, never nominal height. Moving a camera to another exterior angle cannot see
through this covering. An intact lower witness would also fail to detect a separated top.

Exposure/reset is not free: moving a target10→50→10 adds80 mm and, at the conditional
850rpm/lead3, at least1.882 s rotation before acceleration, docking, reading and settling.
It may lift a miniature or move/reveal unintended terrain. With neighbors already at50,
side exposure above them requires additional unavailable travel. A successful exposed read
still aliases a failure during the final hidden lowering. Spreading/removing neighbor rows
would deliberately move unchanged loaded terrain; it is not this architecture's escape.

Removing/replacing m miniatures at assumed5–15 s per touch adds10m–30m seconds, plus placement
registration, sensing and checking after reloading. These are workflow bounds, not observed
player timings. They cannot be silently excluded from an update or assumed acceptable to Sander.
A broad base can obscure unchanged loaded pins even when every changed cap is visible.

## Complete conditional waiting

Reuse E-267's 16-output writer and actual map arrays: physical river/ravine, both pitches,
S40/N20 versus S50/N30. 133 nonempty four-square reveal windows per depth are scenarios, not
representative observed sessions. Retain850rpm, lead3 and acceleration1000 rev/s² **as assumptions**.
Replace its20-ms proof with the sequence above. All macro seeks/return, drive/dock,4-s common
allowance and a further1-s reader deployment/parking are paid. Grant a separate upper carrier
keeping pace with the lower writer; no overlapping proof/drive time is credited.

- **Stereo16:** 16 simultaneous cap measurements in100 ms, requiring32 registered pupil/relay
  duties, not a free whole-row camera. No inner scan motion.
- **Stereo1:** two locally centered pupils on one scanner,100 ms/cap; exact travel between
  selected columns and back to the station origin, minimum50 ms per nonzero inner move.
- **Probe1:** one stylus, same inner travel; conservative full45/55-mm search and retract at
  assumed50 mm/s,500 mm/s² plus100 ms/contact. A high target might shorten this bound; it is
  not an optimized probe-speed lower bound. No extra probe-force release observation is credited.

One immediate recoverable station retry is charged with **full S travel**, not its original
delta: after an observed release fault, a stable pin can be anywhere in stroke. Actual retry
commands must be regenerated from measured heights. Unknown position, persistent fault or lost
support stops the playable update and enters service; the table does not assign a finite recovery
time to damage. The second read is included; no blind homing of unchanged pins is allowed.

|Pitch / S|Sequence|Local maximum, s|Scene maximum, s|Cold neutral, s|Dense stress, s|
|---|---|---:|---:|---:|---:|
|6.35 /40|Stereo16|24.84|226.69|248.93|369.40|
|6.35 /50|Stereo16|28.84|253.98|309.40|429.87|
|5.08 /40|Stereo16|46.62|328.48|381.30|569.54|
|5.08 /50|Stereo16|56.26|368.48|475.65|663.89|
|6.35 /40|Stereo1|77.30|657.83|1041.87|1162.34|
|6.35 /50|Stereo1|81.30|683.95|1102.34|1222.81|
|5.08 /40|Stereo1|125.68|950.01|1535.07|1723.31|
|5.08 /50|Stereo1|135.33|990.01|1629.43|1817.66|
|6.35 /40|Probe1|621.30|5055.83|9265.87|9386.34|
|6.35 /50|Probe1|734.10|5961.55|10971.14|11091.61|
|5.08 /40|Probe1|957.68|7792.01|14367.07|14555.31|
|5.08 /50|Probe1|1133.73|9200.41|17027.83|17216.06|

These are **exposed changed-cap conditional schedules**, not occupied-play certificates.
The coarse parallel case remains near the30-s reference; the fine case exceeds it. Dense
stress and cold neutral are separate; first use pays preparation **plus** its actual map update.
E-268's granted optical schedule cannot be copied unchanged: this model pays extra settling,
reader deployment, actual inner scans and full-stroke recovery. Probe1 with H60 adds2.2 s/cap
relative to H5 in this motion law, also paid again on retry.

If mechanical isolation is not established, reading only changed cells cannot verify unchanged
neighbors. An additional **entire-board** post-update Stereo16 scan costs73.62/110.26 s at
64/80 grids, including seeks, settle, return and one reread; Stereo1 costs866.56/1264.04 s.
A pre-update baseline scan costs the same again. These still cannot certify miniature-covered
pins and do not prove behavior under later load. No mandatory whole-board sweep is hidden
behind sparse-cell timing; choosing a narrower inspection set requires independent mechanical
isolation evidence. E-269's unqualified common-frame compliance supplies none yet.

## Replication, manufacture and decision

Top sensing adds **zero per-cell holes, marks, mirrors, bores, tail guides or sensors** to the
4096/6400 integral caps/pairs/seats and8192/12800 guide apertures already assumed. Those existing
parts and E-269's126/158 two-layer ribs remain unqualified. It adds one shared upper XY carrier,
registration/lighting and either32 entrance-pupil/relay duties or2 plus a local X scanner.
Stereo16 adjacent nominal pupil envelopes span4.5 mm before independent placement bounds;
this does not show that lens barrels/electronics fit. Precision shared relays may be machined
or outsourced; no catalog camera, manufacturing route or rate is selected. Probe1 adds one
Z metrology/force-limited axis, stylus and calibration/cleaning duty. No extra private latches.
Accessible shared reader repair is preferable to removing thousands of embedded sensors, but
upper access, transport height and frame registration must be paid. Cap finishing must remain
batch work: even10 extra seconds per cap would add11.38/17.78 maker hours.

E-267's dated16-output motor/driver subset plus unquoted reserve is$497.68: only$2.32 below
$500, versus$502.32/$1002.32 under$1000/$1500. At the latter tiers the entire remainder would
allow$31.40/$62.65 per16 read channel **if all other missing costs were zero**. They are not:
frame, optics, lighting, top carrier, transmission, docking and electrical work remain unquoted.
Two shared pupils reduce replicated optical duties but give much longer waits. No current
market quote, finished-price claim, affordable reader or purchase authorization follows.

**Decision:** stop through-support and lift/read/restore refinements. Keep narrow post-undock
noncontact top observation as the least invasive geometric escape, with serial probing as a
calibration/control comparison. Neither is a selected head or an occupied-board solution.
The next useful discriminator is a finite shared optical field with real height/identity evidence
and an explicit observable-cell contract, paired with mechanical isolation evidence for loaded
unobserved neighbors. Do not substitute miniature-top sensing, motor turns or a claimed cheap
camera. No new owner question or print is necessary for this bounded negative/conditional result.

Verification:196608 exact ray/neighbor-box checks against continuous extrema, raised/low and
wide-view controls, explicit opaque-base alias, both movement signs and post-release failures,
rejection when stale/wrong-cell flags are supplied (not a classifier test), dense retry identities, no-op/sign symmetry and a separate
sparse event-ledger sum. These checks validate this model, not actual optics or hardware.
