---
status: complete
builds-on: [E-230, E-229, E-223, E-234]
---

# Thin command webs remove retained media parts but stopped writing misses scale

**Park the stopped-punch embodiment.** A consumable command web replaces
E-230's independently retained program bars with holes and solid material;
terrain loads remain on simple columns and reusable shared supports. One writer
already needs **37.059 s for feed and punch strokes alone** under the stated
motion bounds. The lowest sampled timing-feasible allocation uses **16 banks,
four writers, 320 data channels, 28.225 s and $755**. It consumes about **.91 m²
of fresh web per arbitrary full map**. These are calculated scenarios, not a
physical or economic impossibility theorem. No print or punch-tool development.

Input main `e7c33f5`. Reproduce:
`python3 tools/curated-experiment-checks/E-235/screen.py`.
Evidence: **architecture hypothesis, deterministic finite information layout,
inherited ideal support replay, and explicitly assumed dimensions/rates/costs**;
self-review. No sourced process distribution, supplier quote, finite mechanism
CAD, physical measurement or qualified reliability. Five 10-mm-spaced heights
remain a comparison workload, not a product resolution decision.

## Complete transaction and changed interface

Retain E-228/E-229 crossed row/column support and six signed subset pulses:
+10,+10,+20,−10,−10,−20 mm. Columns carry seven shelf levels; either grounded
row or column support holds an idle column. Each bank head has 80 reusable
pickups, column bars, low-force probes and backed output yokes. A mask selects
which pickups acquire load before resident support withdraws. After each pulse,
restore/prove support before releasing the pickups. Unchanged columns retain
support; moving cells follow the inherited ideal replay. No paired resident
bars, travelling load-bearing cassette or reset of unchanged terrain is added.

A **420-mm-wide fresh web** has 80 data positions at 5.08-mm pitch, plus two fixed edge
registration holes per mask. Each mask occupies a 4-mm longitudinal window with nominal 3-mm
holes read by 1-mm probes. A writer has 80 binary gate outputs, 82 punches and
die sites, one shared ram, stripper, optical reader, and feed/hold/takeup.
The low-force data gates select punches; the common ram supplies cutting force.
The web is single-use: punching cannot erase a hole. Rolls may be installed at
power-on, but all target-specific punching and transport occurs after map receipt.
Chad collection, blank stock and spent-web storage remain real hardware.

One web passes beneath several bank readers. Put its plane below every column
tail and resident support: it cannot pass through the stalk array. Each reader
travels with its row head. The route from that low plane to 80 output yokes is
**unconstructed**; E-231's narrow side-link warning is not escaped by a diagram.
Several writers partition the board into disjoint equal-row web groups.

Stop, register and clamp the web; insert/prove probes; use shared cams to move
and positively back the selected output states; then execute the supported
pulse. The sheet carries selector force only. It must never carry terrain load
or be relied upon to retain outputs during power loss. One common output clamp
per head must retain 80 different states; its 80 contacts, reset, return and
load isolation are **required interfaces, not proved mechanisms**. Probes are
withdrawn before web feed. Row and column supports hold terrain during feed.
Shared lift braking and local bank arrest downstream of transmission failure
remain required, as in E-230. Reader failure keeps supports engaged; a tear or
jam stops safely only if those interlocks and retained outputs actually work.

The writer prepares its next gate pattern while the web feeds or terrain service
continues. Punching itself requires a stopped web. When punch and bank service
positions coincide, the favorable schedule grants overlapping operation and
perfect reaction isolation. Optical mask read, probe state, actual column height
and support engagement are distinct proof obligations; fast allocations do not
establish coverage, occlusion immunity or false-accept rates.

## Executable material-coordinate layout and causal retry

At web advance s and reader coordinate y, the reader sees material `u=s−y`.
Every arbitrary phase/bank mask receives a separate 4-mm material window. A
monotone greedy allocator chooses the next s that avoids every prior window;
all 80-column masks are punched when that u passes the upstream writer. This
is a **sufficient layout**, not a globally optimal packing or universal minimum
stock requirement. Its intervals are exact integer micrometres, not FDM accuracy.

Naively advancing 4 mm per phase fails: at a row change the head advances
5.08 mm, so its material coordinate moves backwards 1.08 mm into used data.
Even fixed readers 50.8 mm apart conflict after thirteen 4-mm feeds (1.2-mm
center separation). Both distinguish this from E-223: unloaded probes can
withdraw during transport, whereas that experiment's loaded relief could not.
This escape removes the loaded-neighbor conflict, not information placement.

At B8/W1 the constructed normal-plus-retry web advance is **2.52904 m**.
Its 486 mask stops and 66 service stops combine into 546 distinct feed positions.
A 3/6-mm mask-pitch sensitivity gives 2.10744/3.72784 m; the 3-mm version has
zero nominal ligament between 3-mm holes and is only an optimistic timing control.

One stable wrong final row is detected, read and reprogrammed from actual heights;
replaying original deltas is forbidden. Its six new masks start **after** the
current writer coordinate, then travel to the faulted bank. The farthest B8/W1
reader is 421.32 mm downstream, requiring at least **425.32 mm** additional
advance before the first recovery mask arrives. Prefetched recovery is invalid.
The model charges one full retry in the critical group, while other groups may
finish and remain supported. Off-grid hangs, structural faults and web jams
require supported service; no bounded-time repair claim covers them.

Regional masks can skip inactive banks, but share the same web and require actual
seek/registration. Idle probes stay out and their row/column supports remain
engaged. Other loaded regions ideally do not move; shared frame and punch shock
remain unbounded. One changed cell still invokes the visited row's transfer
hardware. Sparse update speed is not claimed from full-map arithmetic.

## Whole-machine timing, economics and force

Rest-to-rest motion is triangular/trapezoidal: `t(d)=2√(d/a)` below v²/a,
otherwise `d/v+v/a`. Base v=200 mm/s, a=8,000 mm/s². A stopped punch cycle
requires down/up .5-mm ram strokes plus .005 s proof. Binary gate throw is
2 mm; all available feed/service time is credited to gate preparation.
For a 10/20-mm pulse, stopped service is
`2t(d)+4[t(2)+.003]+2[t(2)+.003]+.010`;
the extra pair is probe/clamp approach and withdrawal. Add `t(5.08)` per row
and 2 s per map for command/registration/final settlement. These are allocations.

A single writer processes 480 normal masks plus six retry masks. A generated
80-row workload has 480 distinct nonempty masks, preventing reuse of identical
words from hiding the arbitrary-map writer demand (seed 235; rejected rows are
reported by the source).
Even granting free selection, proof and terrain motion, 485 inter-mask feeds
and 486 down/up punches take
`485t(4)+486·2t(.5)=37.058529 s` at base rates. This lower bound is for the
**specified stopped writer and nonoverlapping windows**, not all punch mechanisms.
Full B8/B16/B80 one-writer schedules take 72.338/59.470/51.546 s.

Enumerate B=1…80, W in the divisors of 80 with W dividing B; banks inside a
web group have balanced row counts. This includes uneven bank sizes, not just
convenient divisors. Favorable simultaneous punch/service isolation is granted.

| Least allocation under 30 s in each scenario | B / W / data channels | Time | Assumed bought allocation |
|---|---:|---:|---:|
| Base | 16 / 4 / 320 | 28.225 s | $755 |
| Gate throw reduced to .25 mm | 16 / 4 / 320 | 28.225 s | $755 |
| Web/writer a=32,000, v=400; .25-mm gate | 16 / 2 / 160 | 28.265 s | $635 |

Shorter gates do not help the base result: preparation is already hidden in
feed. Do not start a tiny-gate campaign. The fast variant retains base terrain
motion and unqualified cutter force. Base fewest-channel result B80/W2 has
160 channels but costs $1,915 at 29.645 s; fewer writers alone is not a win.

Allocation is E-230's **$195 shared +$20B**, plus **$.50×80W data channels
+$20W web machinery**. The latter partitions $8 feed/hold/takeup, $8 ram/die/
stripper, $4 writer readback. It excludes no known hardware category deliberately,
but these extremely lean amounts are **not quotes, a purchasable BOM or cost
floors**; fresh stock and force-driven upgrades must be added. B16/W4 already
exceeds $500 with free data gates ($595). B16/W2 does too ($555). Head fabrication,
reader optics, 80-site precision cutting and safe arrest are not qualified by
small dollar allocations. No claim that every differently costed web must fail.

Peak punch shear model is `F=n·π·D·t·τ`: n≤82 (80 data + two registration), D=3 mm, thickness t=.05… .2 mm,
shear stress τ=10…40 N/mm², all **competing assumptions**, not material data.
Peak all-hole force spans **386…6,183 N**; .1 mm/20 N/mm² gives **1,546 N**.
A mixed ±40 row punches 42 holes at a time, but all-one phases are reachable on
other maps. Sequential or rotary shear changes the time/force interface and
needs a new model. The $8 ram/die allocation has no demonstrated capacity.
Terrain drive still owes E-230's frame, torque, twist, gravity-following and
local arrest checks. At B16, 1,280 simultaneously moving cells alone represent
1.28/4.186/12.8 kN at assumed 1/3.27/10 N per cell, before head mass/friction.

## Replication, manufacture and consumption

At B16/W4, each bank holds five rows and serves one 80-output head:

| Functional item | Cell / row | Bank or head | Board |
|---|---|---|---|
| Columns / guide stations | 1/2; 80/160 | 400/800 | 6,400/12,800 |
| Shelf levels / resident support contacts | 7/2; 560/160 | 2,800/800 | 44,800/12,800 |
| Moving row combs | shared; one/row | five | 80 |
| Head column bars / pickups / probes | shared | 80 each | 1,280 each |
| Output routing links / clamp contacts | shared | 160/80 | 2,560/1,280 |
| Probe return functions / guide wear sites | shared | at least 80 each | at least 1,280 each |
| Data gates / punch pins / die sites | shared writer | 80/82/82 per writer | 320/328/328 |
| Feed, ram, stripper, writer reader, takeup | shared writer | one each/writer | four each |
| Web clamps / local arrest / head reader paths | shared | one each/head | 16 each |

No permanent per-cell spring, insert, latch or actuator is added. This does not
mean zero springs: probe/punch return functions, keeper resets, gates, fixtures,
bearings, fasteners and readers need actual implementations. Punch-die alignment
has 328 wear-critical sites. Every site on a monolithic return comb still counts.
Compared with E-230's B9 nine-position program, retained media bars/notches/lands
fall from 1,440/12,960/77,760 to zero, while head bars/pickups/probes grow from
720 each to 1,280 each and fresh holes replace reusable memory. The stopped web
therefore loses the overall comparison despite simpler stored information.

Column stock stays approximately 8.192 L under E-230's blank assumption; web
handling, guide, head and tool volumes lack finite geometry. At an assumed
10 mm³/s that stock alone takes 227.6 h before scrap/support/frame. Columns
alone need 17.8 h placement at 10 s each. Another 7,680 bars/pickups/probes/links/
clamp functional sites at 10 s each would add 21.3 h **if individually handled**;
monolithic manufacturing may reduce assembly, not functional failure sites.
Modular 256-mm builds require joints and alignment across the 406-mm row.

3-mm holes and 1-mm probes leave `1−e` radial margin for total registration error:
.85/.65/.30/0 mm at e=.15/.35/.70/1 mm. These are generous selector bounds,
not qualified web tolerances or cutting clearances. Punch/die clearance, burrs,
tear strength, stripping, curl, creep and probe puncture resistance are unknown.
A 4-mm longitudinal pitch leaves 1 mm nominal ligament. Opposing per-hole
center errors .15/.35/.70 mm leave .70/.30/−.40 mm, before diameter error;
positive probe clearance alone does not establish an intact sheet. End-referenced width
scale errors .1/.25/.5% produce .401/1.003/2.007 mm at the far data column;
center registration halves those extremes. Common roll stretch/skew, batch
shrinkage, feed slip and punch-reader alignment can corrupt entire words/banks.
No independent-cell distribution or board-yield claim is assigned.

420-mm stock consumption is **.90942 m²/full map**, or **.96844 m² with one
critical-group retry**, including the modelled leader/delivery travel, excluding
roll-change waste. At .1-mm thickness this is 90.94/96.84 cm³; 100 nominal maps
consume **9.094 L of sheet** before packaging. Maximum normal data holes are 19,200 (three selected pulses per ±40 cell),
plus 960 registration holes; 38,400 is binary data sites, not cut holes.
Stock prices remain unknown: at an assumed $1/m², 100 maps add about $90.94.
Consumable inventory/takeup capacity and chad extraction impair D&D practicality.
A serviceable punch module is accessible, but a torn web affects several banks;
continued support and replacing/rethreading stock are required service paths.

## Decision and changed reopening condition

Stop this **stopped, consumable punched-web interface**, preserving its coordinate
allocator and causal-delivery accounting. No cutter, return spring or probe
refinement follows. Neither all reusable masks nor every shared writer is ruled out.

A separate **free flying-writer relaxation** deletes all punch stops/time/force,
while retaining finite fast feed, reader stops, six pulses and causal retry. B12/W1
then gives **29.498 s/$495 assumed**, versus B10's 31.034 s/$455. This is not a
survivor: it has only .502 s additional map allowance, no actual continuous writer,
no stock purchase and unchanged heavy service/readback assumptions. It identifies
the required architectural escape rather than authorizing smaller punches.

Next discriminating invention should reduce **both** persistent information
handling and the six supported pulse transactions, or construct a reusable
shared writer with a materially different timing/force path. Do not investigate
flying perforation solely because its zero-cost oracle narrowly clears a target.
Compare a complete alternative before local tooling or print work.

Checks: 625 exhaustive two-cell old/target support replays inherited from E-229;
80 generated full-row replays and 480 actual material-coordinate word reads;
exact nonoverlap and writer-before-reader assertions across the bank/writer grid;
naive stream failure witnesses; causal retry placement; schedule sum identities,
coincident-operation control, independent triangular-motion formula and the
feed/punch-only bound. These verify this reduced model. They do not validate
web routing, manufactured holes, retained output clamps, lift arrest or hardware.
