---
status: complete
builds-on: [E-216, E-084]
---

# Shared setting energy does not remove arbitrary-data hardware

**Park both constructed writer embodiments; do not refine their contacts.**
Binary stop stacks replace multilevel setters with binary gates but multiply
retained media and require differential pushers. Spatially commutated cam tracks
remove those bits but exchange them for gates, contact acceleration and scan
length. Neither supplies a competitive complete E-216 row-head machine.
Rejection is scoped to these couplings.

Input main `12024b9`. Run `python3 tools/curated-experiment-checks/E-217/programming.py`
(standard library; imports E-216; stdout only). Evidence: **mechanism hypotheses,
logical replay and calculations using assumed bounds; self-review only**.
No CAD, measurements, quotes, process distributions or physical qualification.
Five heights 0/10/20/30/40 mm are a comparator, not a resolution decision.

## Physical constructions and finite transitions

Both inherit E-216 R's columns, 80 common comb releases and B row heads.
Each head has 160 command sliders at 3-mm spacing: 80 old/BYPASS values
(six states) and 80 targets (five states). Every visited row is rewritten.
During writing the comb stays seated and the head unloaded. Output decoding
to retained grip commands remains E-216's unbuilt cam/grip coupling.

**B — binary decisions, then one common setting stroke.** Each output has three
transversely sliding stepped blocks. Their two face positions add 0/3, 0/6 and
0/12 mm in a serial stop stack; common closure positions the output at 3×code.
The stack has 21-mm possible range; readback must reject codes 6/7 before a
15-mm useful output stroke. A common stripper first returns all outputs and
unloads their stops. A moving reset shoe erases all bits; three binary shoes
per stream set the desired endpoints with 2-mm throws. Each bit needs retained
endpoints until closure and under stop reaction: count one detent/keeper
function per bit, not a free Boolean. Three bit planes are written concurrently.

A rigid bar cannot stop 160 outputs at different distances. **160 independently
compliant, preloaded pushers/head** therefore bridge the common 15-mm stroke to
the selected stops. These are additional long-stroke compliance/wear sites,
not hidden in the common motor. Output keepers engage before bar retraction;
readback checks both bits and final slider position before enabling takeover.
Unload → strip → erase → write/retain → read bits → common close → keep/read
output → retract is the physical energy/state sequence. Cam profiles, block
nesting, detents, pusher force equalization and keeper transfer remain unbuilt;
no finite clearance or loaded compression-stack pass is claimed.

**C — mechanically commutated set/reset carrier tracks.** Two reusable carrier rails hold stationary old/target sliders under a travelling
writer; relative motion supplies feed without an assumed circulating belt. A nonselective
30-mm-long reset ramp drives all visiting sliders to zero. Five successive
stations, spaced 5.08 mm, each have a binary retractable gate selecting an
out-of-plane bypass or a rising cam. Track k pushes a zeroed slider to 3k mm;
exactly one track is enabled for nonzero commands, none for zero. After a
selected track, all later tracks bypass that carrier. Online commands follow the carrier identity at each station. Each slider needs
six retained positions through bypass and writer return.

Traverse supplies setting energy; gates route it. The trailing reader checks
outputs; shoes retract before return, then re-engage. Follower junctions,
retention through ramp departure, clearance and decoder remain unconstructed.
The logical model cannot prove those contacts or sensors.

Detected write faults stop before comb release; one full row rewrite is charged.
Power loss during writing leaves the comb supporting terrain; partial media
must be erased/replayed. Loaded-transfer faults still need E-216's unbuilt
retained grips/elevator arrest. There is no safe source-loss transfer claim.

## Necessary schedule, rate and packing

B heads serve contiguous banks, with s even streams/head dividing the 160 values
into n=160/s sites. Each stream requires **3 gates for B or 5 for C**, plus a
final value reader. Gate endpoint sensing is additional unpriced channel functionality. All data
is written online; no buffer or offline preparation credit.

Let pitch p=5.08 mm, selective contact width w=2 mm, gate throw 2 mm and assumed
gate proof 1 ms. Rest-to-rest trapezoids use axis a=2,000/8,000 mm/s² and vmax
200 mm/s. A cycloidal cam of rise d has peak follower acceleration
`2*pi*d*(v/w)^2`. Competing follower acceleration ceilings are **20/100 m/s²**,
not allowable PLA/contact acceleration measurements. Necessary scan limits are
`v_gate=(p-w)/(move(2,a)+.001)` and `v_cam=w*sqrt(a_f/(2*pi*d))`.
Main tables use **v=.8*min(200,v_gate,v_cam)**, an explicit allowance against
running exactly at the gate/contact boundary, not a reliability model.
B uses d=2 mm and three simultaneous bit planes; C's worst track uses d=15 mm.

Active scan length is `(n-1)p + reset_length + stations*p + p`;
reset length is 4/30 mm and spatial stations 1/5 for B/C. Acceleration and
braking occur outside contact, adding `v²/a` stroke and `2v/a` time. Charge
full return travel, 2-mm shoe withdrawal/re-engagement and 10-ms terminal
read/clamp proof. B also charges both 15-mm common strokes plus 5-ms proof.
Thus reset, arbitrary writing, feed-equivalent scan, overrun and return are
explicit; computation/registration uncertainty still lives in stated allowances.

Add E-216's supported clearing/setting: at most eight 10-mm elevator moves,
20 ms/stop, .5 s/row for docking/comb/grip/output proof, actual row travel,
2 s common overhead and one full worst-row retry. No writing overlaps loaded
head use. Slowest contiguous bank controls completion. The 80×80 witness
contains all 25 old/new pairs per row. Its 80-mm/eight-stop service bounds all
five-height maps under this motion law, not finer/continuous heights.

| Writer | B | s/head | Axis a / follower limit (mm/s²) | Controlled gates/board | Calculated map s | $/gate left from $250 at $500 ceiling |
|---|---:|---:|---|---:|---:|---:|
| Binary | 8 | 20 | 8,000 / 100,000 | 480 | 29.973 | .521 |
| Binary | 16 | 8 | 8,000 / 20,000 | 384 | 25.517 | .651 |
| Binary | 16 | 8 | 8,000 / 100,000 | 384 | 23.929 | .651 |
| Commutated | 16 | 16 | 8,000 / 100,000 | 1,280 | 25.952 | .195 |
| Commutated | 16 | 80 | 8,000 / 20,000 | 6,400 | 29.332 | .039 |

Sweep: B=1/2/4/8/16, s=2/4/8/16/20/40/80/160, both accelerations and both
follower limits. No B<=4 timing survivor in this finite grid. At B=8/s=2,
a=2,000/a_f=20,000, B/C need **171.759/269.031 s**. At B=8/s=8 and faster
bounds, **42.204/59.429 s**. Scalar E-216 B=8/q=1/a=2,000 takes 646.672 s;
its B=16/q=16/a=8,000 multilevel writer uses **256 setting lanes, 21.167 s**.
Binary gates may eventually cost less than multilevel axes, but reducing gate
stroke has not demonstrated lower purchased cost or repeated complexity.

Without the .8 speed allowance, C at B=16/s=8 calculates 29.735 s with 640
gates; .8/.6 gives **33.325/39.326 s**. A buffer cannot restore sustained rate.
For C at B=8/s=16, widths 1/2/3/4 mm give 68.242/45.913/46.397/67.522 s:
wider cam contact helps acceleration while removing gate-switching time.
For B at B=8/s=16, row allowance .25/.5/1/2 s gives
29.261/32.011/37.511/48.511 s: near-boundary figures are not robust passes.

Packing is **not** hidden in s. Split each old/target array into s/2 isolated
scan segments. At B=16/s=8 the binary stroke is 111.393 mm versus a segment's
101.6-mm site pitch allocation. C at s=16 needs 106.540 mm versus 50.8 mm:
its reset/track train overhangs neighboring segments. Same-plane adjacent
tracks would strike the wrong media. Separate staggered decks and output
bridges are mandatory in this construction; hypothetical 8-mm deck spacing
requires 32/64 mm for four/eight decks per array before frame, slider stroke,
retention and head motion. These are envelope allocations, not clearance CAD.
There are 160 mechanical output routes/head regardless of segmentation; their
collision-free fanout to full-pitch grips is unresolved. Increasing s cannot
be treated as free packing or zero assembly.

## Whole-machine replication, economics and manufacturing

Inherited resident ledger: each cell has one column, two lateral guide stations,
five groove shelves and one comb tooth; multiply by 80/400/6,400 per row,
B=16 bank/board. Board totals remain 12,800 guide stations, 32,000 shelves,
6,400 teeth and 80 common comb/keeper axes. No new resident lock is added.

| Functional inventory | Per head / visited row | B=16 board | Added manufacturing/service consequence |
|---|---:|---:|---|
| Common inherited grips | 160; >=320 jaw faces | 2,560 grips; >=5,120 faces | 160 retained grip states/head; clamp load/proof/arrest unresolved |
| Both: output media | 160 sliders/retentions/guides | 2,560 each | Six endpoint contacts each: 15,360 state positions, not separately assembled stops |
| Binary weighted bit blocks | 480 two-position slides/retentions | 7,680 each | 960 alternative stop faces/head, 15,360 board; **same blocks as bits**, not another part count |
| Binary differential pushers | 160 independent compliant functions | 2,560 | Up to 15-mm compression range; wear, creep, force spread and keeper transfer |
| Binary at s=8 | 24 gate channels +8 value-reader channels | 384 +128 | Three bit sites/value must also be read; reader channel is not a qualified sensor |
| C at s=16 | 80 gate channels +16 value-reader channels | 1,280 +256 | 80 selective ramp/bypass junctions/head; return retraction cannot be omitted |
| Both: output paths | 160 bridges to grip decoding | 2,560 | Deck fanout, joints/contacts, grip command retention still unbuilt |

Springs, detent inserts, sockets and bearings have **no selected BOM**; printed
retention still counts. Bought inventory includes data actuators/drivers, gate
proof, readers, wiring, power, frame/rails/bearings/fasteners, grip hardware and
arrest. No case is cost-qualified. Each head additionally has scan, shoe-retraction,
row travel, elevator, comb transfer and grip-closure drive functions; B adds
common stripper/pusher and output-keeper functions. Mechanical cam sharing may
reduce motors only after its actual phasing is constructed. Six/eight shared
drive functions per C/B head are not six/eight qualified motors or complete BOMs.

The $250 non-gate reserve is an **allocation**, not a price estimate: at B=16
it leaves only $15.625/head for shared mechanisms and all other board hardware.
At a $400 ceiling gate allowances shrink by 40%. This establishes no affordable
BOM and does not exclude every custom actuator; no current quotes are used.

E-216 column stock remains 4,608 cm³ and 85–256 h at assumed 15–5 mm³/s.
Added stock scenarios: 20×4×3-mm bit blanks and 25×4×3-mm output blanks give
**1,843.2+768=2,611.2 cm³** at B=16, excluding pushers/guides/cams/frame.
At 5–15 mm³/s that adds 145.1–48.4 h; C outputs alone add 42.7–14.2 h.
These are not CAD volumes or minima. Ten percent scrap multiplies by 1/.9;
stop-face orientation matters even in monolithic arrays.

Assumed assembly at B=16: 10 s/bit adds 21.33 h; 30 s/pusher another 21.33 h;
10 s/output adds 7.11 h; inherited 30 s/grip adds 21.33 h, before wiring,
inspection and calibration. Columns at 5 s already cost 8.89 h. Monolithic
printing exchanges placements for shared scrap/replacement. Head removal must
leave combs seated; a failed head strands 400 cells, shared reader bias all
6,400 commands. Accessibility and correlated yield remain unqualified.

Carry E-216's adverse **common bias + local error + alignment** bounds of
.15/.35/.70 mm, not probability distributions. A hypothesized 1-mm-wide
capture window has .5-mm half-clearance: remaining margins .35/.15/−.20 mm.
Three serial stop blocks accumulate errors: if each has same-signed .35 mm,
1.05 mm consumes much of the 1.5-mm half state spacing before output/reader
error; .70 mm/block gives 2.1 mm and overlaps states. Common correlated bias
must add, not shrink by sqrt(3). Direct C avoids that serial stack but still
needs accurate gate entry and retained output contact. Finer features or more
preload are not authorized escapes. Warp, friction, fatigue, roughness, first
layers, retention creep and route misalignment have no measured envelope.

## Force, support and what the executable establishes

With assumed resisting force R=.3/1/3 N per follower, cycloidal peak cam slope
is `2d/w`; peak quasistatic scan demand is 1.8/6/18 N per binary stream.
Conservatively summing all five commutated tracks plus the reset ramp gives
13.8/46/138 N per stream. This is an envelope when different carriers occupy
all tracks, not their time-average or a dynamic force ceiling. At s=16 and
R=.3 N, C already demands up to **220.8 N/head**, or 2.208 N·m at a 10-mm drive
radius before losses. A 2-g follower at 100 m/s² adds .2 N inertial force at
peak acceleration; actual reflected gate/cassette mass and contact loss matter.

Binary shared closure has a further demand: preload .3 N, spring k=.02/.06/.18
N/mm and 15-mm compression produce aggregate worst-case **96/192/480 N/head**.
These explicitly count the spring energy stored while zero-coded outputs stop
early; no common-stroke free work. Output clamp and stop contact forces remain
unqualified. During column movement the inherited friction head still needs
`80F/mu` summed normal force: F=3.27 N and mu=.1/.2/.4 means
2,616/1,308/654 N per row, before inertia/moments. Writer success cannot fix that.

The executable checks all 36 initial→target code overwrites for each coupling,
six injected read/retention faults, both writers across 12,800 commanded values
per 6,400-cell map, E-216's 625 two-cell support cases and three missing-support
faults, and cam acceleration by convergent finite differences. These are ideal
logical proofs with perfect stated readback, not sensor coverage or finite
contact dynamics. A 5×5 patch within one bank at B=8/s=16/fast bounds calculates
17.560/25.142 s for B/C. All 80 columns of every touched row still undergo grip
handoff even if unchanged. Ideal replay preserves their height; real clamp/
frame displacement and comb reseating remain unbounded. No regional-disturbance
exception, safe power-loss transfer or physically supported handoff is established.

## Decision and materially changed next coupling

Do not shrink these gates, increase acceleration again, or tune detents/pushers.
They have not escaped the hundreds-of-channels burden, and B increases retained
functional sites substantially. Neither justifies local CAD, printing or purchase.

Next change the load path: broad stepped row cassettes could store height
**and support columns directly**, eliminating old-code media, mask-to-grip
conversion and 160 friction retention functions/head. A common keeper would
arrest cassette translation while a shared machine writes/exchanges unloaded
supports. This is a hypothesis, not a free supported swap.
First construct a three-column old/new witness (40→0, 0→40, 20→20), with explicit
positive support at every intermediate position, writer access, unequal-height
handoff and power-loss arrest. Count resident movable stops, media inventory,
all arbitrary-map rewriting and exchange travel at 6,400 cells immediately;
E-084 still forbids hiding programming in a prepared second cassette. Stop if
exchange requires the same independently retained friction pickups, motion of
unchanged loaded columns, precision resident locks or uncounted media handling.
No direct-support survivor is assumed.
