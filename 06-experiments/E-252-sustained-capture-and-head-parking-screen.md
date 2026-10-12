---
status: complete
builds-on: [E-222, E-251, E-236]
---

# Sustained capture saves turns but introduces parked outputs and empty reset

**Park this shared-drive embodiment before capture, dog, rack or guide detail.**
Retaining changed columns in transit orientation reduces ten quarter-turns per
row to two. An ideal two-stage handoff lets opposite coupling changes overlap.
Nevertheless, the explicit empty-slide reset gives **10 banks / 800 loaded
channels / 28.627 s / $811** in an inherited favorable allocation that makes
added parking hardware free. Even **zero-time reset** needs **six banks / 480
channels / 29.668 s / $564.60**. These are conditional scenarios, not price or
speed lower bounds. No selected architecture or justified print.

Input main `666efe6`. Reproduce:
`python3 tools/curated-experiment-checks/E-252/screen.py` (stdlib; imports E-251).
Evidence: **mechanism hypothesis, ideal support replay, finite enumeration and
calculations under explicitly labelled bounds**. Self-review, not independent
validation. No finite head assembly, measured friction, FDM prior, circuit/BOM,
physical reader or arrest qualification. Five heights 0/10/20/30/40 mm are the
comparison grammar, not a product resolution decision.

## Changed machine and supported transaction

Retain E-251's fixed resident rails and global checkerboard release offsets
3.2/6.4 mm. A reusable head now has **80 independently translating output slides**.
Each has a retained bilateral column capture, a drive coupling to a common
moving rack, and a parking dog grounded to its color frame. The color frame has
its own arrest/load path to ground. A stopped/braked drive rack permits overlap
of the two output support paths. Unlike E-222, there are no screw/nut axes;
unlike E-251, the captured outputs move independently of the common datum.

1. With all columns seated and outputs parked at zero, write/read the changed
   mask, capture/prove only changed columns, lift both color frames by their
   offsets, and turn changed columns 90 degrees. U columns keep their original
   fixed primary contact throughout. Captures remain retained until final deposit.
2. Use E-251's five strokes `[-20,+10,+10,-20,+20]` mm. Before each stroke,
   physically write/read membership commands while existing support is retained.
   At the stopped carrier, **add incoming support and prove it, then remove
   outgoing support**. A 0→1 channel gains drive before losing park; a 1→0 channel
   gains park before losing drive. Those operations can share two global stages
   across opposite transitions. Continuing channels keep their existing path.
3. Only then move the common carrier. Driven slides follow; parked slides hold
   their independently accumulated displacement. After the fifth stroke, transfer
   every output to park, turn captured columns back, lower the color frames,
   prove resident support and actual target heights, and detach captures.
4. **Reset empty slides:** replay the same five memberships in reverse order
   with negated strokes. This returns every slide and the carrier to zero using
   the same supported handoffs. It adds no local return springs, but consumes
   five writes, six handoffs and 80 mm of common motion. Then index the row.

Capture retention and drive membership are **different state duties**. Rewriting
commands must not release a loaded capture or its current support; output
isolation/retention hardware is unconstructed. A single actuator may eventually
sequence duties, but a digital bit does not implement them. Common yaw coupling
must work across an 80-mm spread of slide positions. Sliding torque transmission,
frame routes, rail bypass, readers, fixtures and contact interlocks are unknown.

Power loss requires each loaded output to retain its capture and either its
park or its drive coupling plus common brake; both color frames also need arrest.
A spring-open drive coupling defeats that graph. A broken branch, false proof,
jam or off-grid output has no guaranteed automatic recovery. Stop the coupled
bank motion. At a **detected stable integer state**, return-turn/seat/detach,
invert the executed empty-slide prefix, read actual heights and regenerate the
remaining program. Do not replay the original delta from an unknown height.

## What the executable establishes

- **15,625 three-cell maps / 234,375 loaded support observations** preserve an
  ideal load path and unchanged height; empty reverse replay returns all slides
  to zero. This grants retained contacts and arrested frames, not contact dynamics.
- **150 single-cell stable-prefix retries** reset the executed displacement and
  reach the target with regenerated codes. Midstroke arrest/repair is excluded.
- A release-before-engage fault is rejected. Removing drive retention exposes
  an unsupported output. Logical overlap does not prove low-impact transfer.
- All 25 old/target pairs fit within one color's 40 lanes. For each of the six
  membership boundaries (including initial/final park), exhaustive alternative
  code enumeration finds at least one pair that cannot omit that boundary.
  Thus the six global handoffs cannot be deleted by choosing different masks
  **for this stroke sequence**. This is not a universal decoder lower bound.
- Common-rack engagement uses seven relative phases, −20…+40 mm. Parking must
  accommodate nine output positions, −40…+40 mm. Reverse reset retraces these
  phases. Fixed phase stations are not separately moving latches.

E-251's cap-separation argument still applies to the **two endpoint turns**:
all changed heights are integer-grid heights, their color offsets differ, and
U remains seated. The inherited 6,800 nominal cap-pose check is rerun. During
all intervening translations caps remain square-aligned at 90 degrees, so their
nominal XY footprints are disjoint even as neighboring heights cross. Banks
must synchronize turns; an off-grid neighboring bank defeats that guarantee.
Nominal .28-mm lateral cap gap remains unqualified. Axial margin is `1.2-E` mm,
where E is total adverse axial-gap error, not a calibrated printer distribution.

**New routing consequence:** the old −20-mm capture datum rises to **+26.4 mm**
for a +40-mm output and the higher color. E-251 kept its carrier below the
resident rail; this machine cannot inherit that plane-separation argument.
A deliberately deeper **−60-mm capture plane** bounds its highest point at
−13.6 mm, but initial old heights need lug indices 6…10 as well as resident
indices 0…4. That is **ten fixed forms/column, 64,000 total**, with index 5
unneeded. It is an axial allocation, not routed jaws or a manufacturable stem.
Original-depth jaws instead need an actual resident-rail crossing escape.
No narrow-finger repair is licensed by this observation.

## Complete schedule and comparison

Assume linear v=200 mm/s, a=8,000 mm/s²; yaw v=720 degrees/s,
a=7,200 degrees/s²; 2-mm contact strokes and 3-ms stage proofs, all unqualified.
Let `C=move(2)+.003=.0346228 s`.

```
ends = 3C + 2[move(6.4)+.003] + 2[yaw(90)+.003] = .679868 s
loaded = .525 + 5C + 12C = 1.113587 s
empty reverse reset = loaded
row = ends + loaded + empty + move(5.08) = 2.957443 s
T = 2 + .010 + [ceil(80/B)+1] row
```

The three endpoint contact stages are changed-mask write, capture and detach;
lift/seat and both turns are separately charged. The 12 stages are six
add/remove handoffs. Final all-park is a common action, not another arbitrary
mask write. Two common seconds allocate receipt, map computation, initial
registration and final settling. One complete extra service pays for a stable
partial-row recovery: completed prefix plus the retry never exceeds two full
services; prefix reverse replaces full empty reset. Extra .010 s allocates
fault read/regeneration. Actual sensing, controller latencies and motion are
not qualified. All physical writing begins after receipt.

| Protocol | Banks / outputs | Time | Bought allocation or remaining allowance |
|---|---:|---:|---:|
| Sustained capture, reverse reset | 10 / 800 | 28.627 s | $811, added hardware free |
| Sustained capture, entirely free reset | 6 / 480 | 29.668 s | $564.60, added hardware free |
| E-251 repeated turn/reseat | 16 / 1,280 | 26.073 s | $1,180.60 |
| E-236, different unchanged-support scope | 5 / 400 | 26.681 s | $503 lean shared |
| E-251 independent Z/yaw control | 5 / 400 pairs | 26.708 s | <$0.5125/pair after $295 reserve |

The first two reuse `$195 + $20B + $.52(80B)` from E-251 and deliberately add
**nothing** for independent slides, dogs, torque transmission or extra retained
capture state. At B10 only **$0.13125 per entire output** remains under $500
after common/head allowances; the assumed $.52 already exceeds it. This is not
a procurement lower bound. A credible different allocation could change it.
The direct control remains unbuilt; its low pair allowance is not a motor quote.

Sensitivity over contact strokes 1/2/4 mm and proof 0/3/10 ms needs **8–14
banks** with reverse reset. Free reset gives **5–8**, its best case still $503
before new hardware. No tiny-contact or speed refinement is justified by these
scenarios. Keeping five banks with base free reset takes **33.356 s**. Even
solving empty reset alone therefore does not reopen this particular machine.

One visited row, including conservative full retry, is **7.925 s** at base
rates; remote seek adds actual travel. Unchanged columns retain fixed primary
support ideally, unlike E-222's all-row takeover. Frame deflection, vibration,
reader false acceptance and actual non-target displacement remain unmeasured.

## Replication, manufacture and service

B10 serves eight rows/640 resident columns per bank; each head handles 80.

| Duty | Cell / row | Bank or shared head | Board |
|---|---|---|---:|
| Column / assumed lateral guide stations | 1/2; 80/160 | 640/1,280 resident | 6,400 /12,800 |
| Fixed lug forms, deeper-capture allocation | 10; 800 | 6,400 | 64,000 |
| Fixed primary seat / resident yaw restraint | 1 each; 80 each | 640 each | 6,400 each |
| Reusable slide / retained bilateral capture | shared | 80 each | 800 each |
| Drive coupling / parking dog | shared | 80 each | 800 each; 1,600 switched load paths |
| Output slide guide duties | shared | 160 | 1,600 |
| Drive phase / park phase stations | shared | 560 /720 | 5,600 /7,200 fixed stations |
| Capture retention / current support-selection state | shared | 80 each | 800 each |
| Color frame and frame-arrest duty | shared | 2 each | 20 each |
| Common stroke drive/arrest, feed, reader systems | shared | 1 each | 10 each |

No resident hinge, spring or individually assembled latch is introduced. Head
returns, pivots, sockets, inserts, wear faces, wiring and calibration fixtures
remain unknown counts; monolithic construction cannot erase their functional
sites. Captures service separately only after columns are seated and proved.
One head failure blocks 640 cells; a color-frame failure can expose 40 live
columns. Buried column/rail repair still needs a prop and extraction route.

A 4-mm slot/2-mm tooth **hypothesis** has `1-E` half-clearance: .85/.65/.30 mm
for total adverse registration errors .15/.35/.70. Separate support height
errors ±e permit up to 2e=.30/.70/1.40-mm transfer displacement. These are
competing bounds, not FDM priors, bearing-strength results or acceptable motion.
Common rack pitch bias, frame warp and shared reader error correlate failures.
Long sliding torque links add friction/backlash not represented by this slot.

Nominal E-251 radius-.8 stem stock extended to 142 mm with ten lug forms gives
**2.198 L**, about **45–136 extrusion hours** at assumed 15–5 mm³/s and 10%
scrap. This slender stock is not structurally accepted or sliced. An additional
assumed 1–5 cm³/output bundle adds **.8–4 L** before head frames. At five seconds
per column insertion and ten seconds per output installation, assembly is at
least **8.89 + 2.22 h**, excluding wiring, individual support proof and alignment.
Modular 406.4-mm rows must fit the 256-mm printer bed; joint and layer-direction
qualification remains necessary. No realistic complete fabrication yield follows.

With assumed .5-kg moving structure/head, 3-g columns, 5–20-g output slides,
.005-N guide drag/channel and 8-m/s² acceleration, all 800 channels active and
0–5 kg total external payload in the active rows gives **207–510 N**, or
**59–146 W** at .2 m/s and .7 efficiency. This sums common frame/slide demands;
it is not a force-rated transmission or a uniform board-load requirement.
Torque at 10-mm radius is 2.07–5.10 N m. Positive captures avoid assuming gravity
alone drives a light column downward, but their reaction loads remain unbuilt.

## Decision

Retain changed-only sustained capture and concurrent opposite handoffs as
conditional building blocks. Stop this implementation: it moves E-222's
independent arrest problem to head sliders and adds costly empty-state reset.
It improves E-251's channel count by 37.5% but does not earn deep development.
Neither self-homing nor a second small contact adjustment removes these duties.

Next architecture question: can each changed column choose a continuously
supported motion path **once**, with no independent mid-program parking? Use
E-247's nine signed-displacement rails as the explicit comparator and first
reconstruct its selector-writing and 80-mm transverse-routing failures. Only a
concrete change to assignment or routing warrants another experiment; a renamed
rail selector or narrower tooth does not. Preserve U's fixed primary contact
and include the complete write, capture, motion, reset and readback boundary.
