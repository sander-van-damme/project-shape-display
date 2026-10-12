---
status: complete
builds-on: [E-228, E-216, E-217, E-220]
---

# Pulse-by-pulse writers exchange actuators for banks and retained interfaces

**Park the tested direct, scanning and matrix writers before local refinement.**
E-228's six-bank result fails this explicit four-stage 2-mm support transfer,
even with free writing. More banks and physical double buffering recover
conditional timing, but no sampled complete bought allocation approaches $500.
Next change the transaction: **retain one signed-displacement program per row
and decode it through all six strokes**, rather than rewriting each pulse mask.
This is a hypothesis, not a selected machine.

Input main `adcb870`. Run `python3 tools/curated-experiment-checks/E-229/screen.py`.
Evidence: **architecture hypotheses, ideal state replay and bounded calculations;
self-review**. All non-product numerical inputs are assumptions, including
prices, motion, force, errors and proof time. No CAD, process prior, measurements,
market quotes or physical qualification. Five 10-mm-spaced heights remain a
comparison workload, not an approved product resolution restriction.

## Reconstructed failures and physical transactions

E-216 R needs 160 retained grips/head and two multilevel arrays. E-217's binary
writer adds 480 bits and 160 differential pushers/head; its commutated writer
pays for five selective ramps, finite gate time, cam acceleration, clears and
scan returns. Neither qualified the grip-to-load path. Their source remains
consistent with those scoped failures. Here height stays on E-228 crossed
supports, with 80 positive pickup fingers/head: **no 160-grip head, old-height
array or independently captured frictional holding state is restored**.

Each bank register has 80 transverse binary slides selecting broad stop/bypass
lands. Frame backing takes normal reader-cam reaction; endpoint retention must
resist lateral reaction, vibration and writer departure. Hard endpoints alone
do not retain a bit. During shared phase motion, each bit routes two outputs:
selected pickup in, then selected column bar out. A common row drive moves its
comb. Return phases seat supports before releasing pickups. This two-output
routing, retained endpoints, pickup arrest, finite engagement and actual support
readback remain **unbuilt interfaces**, not free mechanisms.

| Writer | Actual overwrite and feed | Extra command/read hardware |
|---|---|---|
| D: direct | 80 independent actuators command retained slides in parallel to either endpoint | 80 actuator/proof channels; shared optical view granted, actual coverage unresolved |
| S: scanning reset/set shoes | q lanes visit 80/q stationary bits; leading 4-mm reset ramp, 2-mm selective cam and trailing reader; retract shoes, return empty, re-engage | q gates/read lanes, common scan and shoe axes, endpoint retention at every bit |
| M: mechanically addressed matrix | Common stripper erases 80 bits. q data rails serve m=80/q groups. With rails home, indexed dogs couple one group; selected rails extend/retract; dogs disconnect before cyclic index | 80 coupling dogs/register, q data actuators/read lanes, group-coupling and address drives, retained bits |

M's dogs couple pushing motion only: rail retraction leaves written bits at
retained endpoints; erase supplies 1→0. Each group is read after rail retraction.
Index errors can write a wrong group despite correct data rails. Mechanical
crosspoint dogs and reset force are counted; electrical multiplexing is not
mistaken for a physical coupling.

An active register cannot be rewritten while it controls the last support.
Double buffering means **two physical 80-bit registers**, a writer selector
reaching the inactive register, and a separate service selector routing the
active register to output cams. Each selector owes a 2-mm stroke plus 3-ms proof.
They cannot be one axis during concurrent service/writing. Arbitrary programming
starts after map receipt; the schedule charges startup, transport and drain.

## Causal support and timing

At rest row AND column combs support every column. Write only there or into
the disconnected inactive register. Each pulse has four ordered contact stages:

1. Insert selected fingers on the arrested lift; prove takeover.
2. Withdraw row comb and selected column bars together. Unselected cells retain
   column supports; other rows retain their row combs.
3. After the loaded height stroke and arrest, seat/prove both comb paths together.
4. Retract/prove fingers, then return the lift empty.

Parallel paired withdrawal/seating is granted. With inherited v=200 mm/s,
a=8,000 mm/s², `t(d)=2√(d/a)` below v²/a, else `d/v+v/a`, contact overhead is
`H=4[t(2)+.003]=.138491 s`. The proof allowance must include actual support,
not merely command flags; no real reader is qualified to meet it.
E-228's six-bank total pulse allowance is **<.11937778 s**. Even W=0 gives
**31.7202 s**. At 1/4-mm contact throws, W=0 gives 28.3858/36.4357 s; six-bank
zero-write tipping throw is 1.441 mm at this acceleration/proof. This is a
model threshold, **not justification to shrink contacts**, nor a universal
lower bound on every possible crossed-support mechanism.

Unbuffered row cycle: `1.1+6(H+W)+t(5.08)`; map:
`2+(ceil(80/B)+1)*cycle`. The 2 s covers initial registration/commands/final
settling; +1 charges a complete worst-row rewrite/replay after detected failure.
An 80-wide row containing all 25 old/new pairs needs all six signed pulses.
Full overwrite is 38,400 commands/map, plus retry. Reads, clears, row feed and
writer return are included. Hard faults safely stop; there is no <30-s repair
claim. Detection is assumed complete by the row's final proof, not deferred.

Writer equations, p=5.08 and n=80/q:

- D: `W=t(2)+.003`.
- S: speed is .8 times the minimum of 200, `(p−2−2e)/(t(2)+.001)` and
  `2√[20,000/(2π·2)]`. The latter is an assumed 20-m/s² follower ceiling,
  not PLA qualification. Contact span `L=(n−1)p+4+2p`; charge `L/v+2v/a`,
  return `t(L+v²/a)`, two shoe strokes `2t(2)` and .010-s terminal read.
  Acceleration/braking are outside contact. ±e adjacent errors erode headway;
  common x bias does not, but still threatens absolute registration.
- M: `W=2t(2)+n[4t(2)+.006+t(p)]+.010`. Four strokes connect dogs, extend
  data, retract data, disconnect. Cyclic index includes return to group zero.
  A circumferential address cam is granted the effective pitch/acceleration;
  finite routing, mass and dog forces are unbuilt.

Buffered pulse service is `2t(d)+H`, plus feed every sixth pulse and
`t(2)+.003` service-register selection. Each write takes W plus its own
inactive-register selection. Write j starts after both write j−1 and service
j−2 finish; service j starts after write j and service j−1 finish. This exact
two-buffer recurrence enforces retention and writer capacity. Independent
writer/service drives and collision-free routing are granted, not demonstrated.

Sweep B=1…80, q=1/2/4/5/8/10/16/20/40/80 (D only 80), both buffer choices.
Distinct smallest-channel and lowest-allocation timing survivors:

| Case | B / q | Data actuators | Retained bits | Calculated s | Bought allocation |
|---|---:|---:|---:|---:|---:|
| D unbuffered; lowest allocation overall | 8 / 80 | 640 | 640 | 26.080 | $1,002 |
| S unbuffered; fewest channels | 40 / 10 | 400 | 3,200 | 28.541 | $3,730 |
| S buffered; fewest channels | 16 / 20 | 320 | 2,560 | 29.796 | $1,970 |
| S buffered; lowest allocation | 9 / 80 | 720 | 1,440 | 29.380 | $1,435 |
| M buffered; fewest channels | 10 / 40 | 400 | 1,600 | 28.051 | $1,380 |
| M buffered; lowest allocation | 8 / 80 | 640 | 1,280 | 26.371 | $1,290 |

Finite-grid results, not global optima. Fewer data actuators do not necessarily
mean a cheaper machine. Neither 480 actuators nor six banks survives by fiat.

## Replication, manufacturing, force and economics

Per cell: one moving column, two guide/wear stations, seven shelf levels,
two positive support sites; no private motor, grip or spring. Per row: 80
columns, 160 guide/support sites, 560 shelves, one comb axis. Per bank: up to
ceil(80/B) rows, 80 column bars, 80 pickup slides, one lift/arrest/carriage.
A bar fault affects up to ceil(80/B) cells. Per head: 80/160 retained slides
(single/double), two endpoint lands each, 160 mask-to-bar/pickup routing contacts.
M adds 80/160 coupling dogs. Monolithic retention still repeats failure sites.

Board: 6,400 columns, 12,800 guides, 44,800 shelves, 12,800 bearing sites,
80 row axes, **80B column axes +80B pickups**, B lift/arrest systems. S/M add
2B writer axes; buffers add 2B selector axes. Smallest-channel S has 1,280
bars, 1,280 pickups, 2,560 retentions, 5,120 endpoint lands, 2,560 routing
contacts and 64 additional writer/buffer axes. Smallest-channel buffered M
has 800 bars/pickups, 1,600 retentions and **1,600 extra coupling dogs**.
Springs, inserts, sockets and assembly fixtures have no selected BOM; printed
retention does not erase functional interfaces or service burden.

Complete bought **allocations**, not quotes or force-qualified parts:
shared controller20+power30+frame/mounts35+wiring25+freight/spares20=$130;
per bank transport20+phase/dock5+reader15+lift motor/driver12+brake8+
shafts/bearings5=$65. Add $.50/data channel including driver/wiring share,
$.05/retained-bit hardware, $8/writer axis and $8/buffer selector. Reader
allocation favorably grants all lanes; real resolution/occlusion and loaded
support proof may cost more. Printed mechanisms are assumed where bought
items are not allocated. Source emits every line item. **Not market floors**:
even free data/bit/writer hardware cannot rescue `130+65B` at B≥6. An alternative
$250 reserve leaves $.390625 per complete D channel at 640 channels under $500,
before other retention/writer purchases. Cost progress needs a changed shared
drive/reader architecture; declaring cheap gates is insufficient.

Assume bit resistance R=.3/1/3 N, not a measured detent force. M reset demands
80R=24/80/240 N before inertia; each active data rail moves one bit at R while
the address axis manages q dogs. S reset+set cams demand up to 3R=.9/3/9 N per
lane; a 2-g follower at 20 m/s² adds .04 N. Actual reflected writer mass is
unknown. At q=20/R=1, S needs up to 60 N quasistatic scan force, .6 N·m at
10-mm radius before losses. Loaded heads still require 80/261.6/800 N for
assumed 1/3.27/10 N per selected cell. Bit forces do not rate lift, pickup or
brake. Bar withdrawal and frame deflection still need characterization.
A $.50 actuator is granted, not shown to deliver those forces.

Inherited column-stock scenario: 8.192 L. Bit blanks of 20×4×3 mm add .154 L
for D's 640, .614 L for S's 2,560, .384 L for M's 1,600, excluding guides,
cams, dogs, pickups and frame. At assumed 10 mm³/s S bits add 17.1 h;
10% scrap multiplies by 1/.9. Ten seconds/retention placement gives S 7.11 h,
M 4.44 h; M dog placement at another 10 s adds 4.44 h. Fixtures, wiring,
calibration and cell installation are extra. Side printing endpoint lands
avoids unsupported overhang faces; anisotropy, roughness, creep and wear remain
unmeasured. Monolithic modules trade assembly for correlated replacement.

S's ten-site lane needs 60.39-mm scan stroke versus 50.8-mm allocation;
the q=20 four-site lane also overruns its 20.32-mm allocation. Staggered bays
and output bridges are owed, not a packing pass. M needs q data rails crossing
m address groups with dog/output escape routes. External pitch may exceed
5.08 mm, but spreading must pay for bridges and service access. Bank head
replacement is performed with resident supports seated and lift unloaded;
buried support-bar faults may need temporary support and module removal.

## Error, isolation, source loss and decision

Competing **bounds**, not distributions: combined functional local/batch error
e=.15/.35/.70 mm leaves .85/.65/.30 mm in an assumed 4/2-mm engagement.
Retention/reaction force is a separate unknown. S at q=8 gives W=1.354/1.440/
1.862 s at these bounds. Common bias cancels headway but may misregister all
cams. Warp, reader bias, address phase slip or one register-selector fault
can defeat many correct bits; no iid yield claim. Opposing support-height
errors still permit E-220's 2e settling. Logical invariance does not qualify
loaded-neighbor disturbance.

During writing, power loss leaves terrain on combs; partial media must be
invalidated and rewritten. During motion, safety needs mechanically retained
pickup selection and an arrested lift until resident support is proved. No
spring-open command return is credited. Ideal write/pickup proof stops bad
commands before withdrawal; false proof can still lose support. An optical
bit reader alone cannot prove shelf contact or braking. If eventual per-command
undetected-error bound were u, the union bound for 38,400 writes is ≤38,400u
without independence. u=10⁻⁶ gives .0384, **not an estimated fault rate**.
Common-mode faults need separate qualification and may require service.

Regional updates idle other banks with combs seated; unchanged active-row
cells retain column support. A five-row patch in one bank takes 15.134 s for
D/B8, 29.796 s for buffered S/B16, 19.525 s for buffered M/B10, including one
retry but excluding extra nonadjacent seeks. Five rows occupy an entire B16
bank. No bank-wide unloading or neighbor reset is authorized by buffering.

Checks: 15,625 three-cell old/new maps, 256 four-bit overwrites, five injected
write/pickup/brake/active-rewrite/reseat faults; independently recover E-228's
28.256-s arithmetic; compare serial schedule with its closed form and buffered
schedules with writer/service capacity bounds. These check the ideal model,
not finite contacts, dynamics, readback performance or hardware reliability.

**Stop all three tested pulse-by-pulse embodiments.** No detent/dog/finger/cam
refinement or printing. E-228's 38,400 figure counts **commands, not independent
information bits**: each column has nine signed deltas. A four-bit or nine-position
program written once per visited row could drive a common six-phase decoder,
with row-scale writing overlap and no old-height capture/grips. It adds 320
binary sites or 80 nine-position sites/head plus decoder contacts, so it must
earn its advantage. Next screen that retained-program transaction together
with synchronized shared power, counting all writers, drive force/torque,
phase isolation, actual output proof, source-loss support and whole-board BOM.
Keep these writers as controls. Stop if decoder/storage or common-load coupling
recreates the present burden; a changed command count alone is not acceptance.
