---
status: complete
builds-on: [E-247, E-251, E-252]
---

# Offset-radius crank: continuous support, large writer, row-sensitive latency

**Retain as a conditional comparator; defer local mechanism development.** One
programmed crank radius eliminates E-252's intermediate parking and E-247's
bridge over nine moving rails. It pays for a long radius-writing stroke and a
compensating carrier. Three planar heads have **177.424-s dense stress latency**;
under the same assumptions, **up to three visited rows per bank** have a
conservative **29.609-s** bound including seek, return and one retry.
No measured gameplay workload establishes which case matters. Do not reject
this architecture solely by the dense time or select it from the sparse bound.

Engineering input `6fde094`; reconciled with mission/stage-02 changes in
`2591458`: representative gameplay is the <30-s target; dense stress is separate;
a credible $1,000–$1,500 demonstrator can merit research, without meeting the
final $500 goal. Reproduce:
`python3 tools/curated-experiment-checks/E-253/screen.py` (stdlib; imports E-251).
Evidence: **mechanism hypothesis, analytical section geometry, ideal replay and
scenario calculations; self-review**. No finite assembly, measured tolerances,
procurement BOM or physical qualification. Five 10-mm-spaced heights are a
comparison grammar, not a resolution requirement.

## Mechanism and routing escape

A shaft along row x rotates 80 radial arms in the yz plane through theta=0…alpha.
Each arm carries an adjustable, positively locked follower. A horizontal slot
in a vertically guided yoke accepts follower y motion and transmits vertical
force to a reusable column capture. Finished columns retain E-251's fixed
bayonet supports; unchanged columns never transfer support.

The tempting signed radius r=d/sin(alpha), d=target−old, has a routing failure:
at theta=0 a connected yoke slot spanning negative and positive radii crosses
the continuous shaft at y=z=0. An interrupted slot owes a different load route.
The changed construction puts all radii on one side and translates the shaft:

```
r = rmid + d/sin(alpha); rmid = rmin + 40/sin(alpha)
shaft z = -rmid sin(theta)
output displacement = (r-rmid) sin(theta) = d sin(theta)/sin(alpha)
```

Lambda=sin(theta)/sin(alpha) increases 0→1 for 0<alpha<90 degrees, so all
outputs stay between their endpoints without midstroke parking. A shared cam
could couple the two motions, but must supply both grounded reactions. The
radial program lock carries load, despite being programmed while unloaded.

Assume an **8-mm shaft-center exclusion** for the follower and **4-mm outer
frame allowance**, neither a qualified part dimension nor a printer tolerance.
Keeping rmin cos(alpha)>=8 yields the head-width section bound:

`W=8/cos(alpha)+80/sin(alpha)+4 >=111.1993 mm`.

Differentiation gives tan(alpha)^3=80/8, optimum 65.1012 degrees. At most three
nonoverlapping bays fit 406.4 mm, before transport/structure. At alpha60:
rmin=16, rmid=62.188, rmax=108.376, radius span=92.376, index step=11.547,
width=112.376 and compensating stroke=53.856 mm. This removes E-247's 80-mm
relative-rail obstruction, not every assembly interference. Axial yoke/arm
separation at 5.08-mm pitch, resident stem passages, cross-arm stiffness,
modular shaft joints and guides remain unconstructed. External or stacked heads
escape the planar count but owe extensions, handling and service access.

## Supported operation and recovery

One shaft/head services checkerboard colors **serially**. Program all 80 radii,
lock and read them while columns remain on resident seats. Neutral radius
inhibits capture; color gating enables only changed outputs. For each color:
capture/prove, lift frame 3.2 mm, quarter-turn captured columns, execute the
crank/compensation stroke, turn back, lower onto resident seats, prove, detach,
reverse the empty crank/carrier. Then service the other color and index the row.
The physical neutral-code gate, bilateral capture and radius reader are unbuilt.

Load path: lug → retained capture → yoke → follower/locked radial slider →
arm/shaft bearings and compensating carrier → arrested frame. All loaded
coordinates need retention on source loss. One brake cannot ground two uncoupled
motions; broken follower, radial lock or downstream shaft remains a support
fault. No moving-arrest or support-proof hardware is qualified.

E-252's −60-mm pickup allocation limits the highest serial pickup to −16.8 mm
and still needs ten fixed lug forms/column. Actual jaws and stem routing are
not inherited as a pass. During turns the other color is at integer heights;
during translations square caps are aligned. Banks synchronize color stages.
Independent off-grid neighboring turns remain inadmissible. E-251's 6,800
nominal cap checks are rerun; this is not loaded contact evidence.

Replay covers **15,625 three-cell map pairs / 1,593,750 support observations**,
2,525 coordinate checks and four deliberately broken interlocks. Continuous
convex interpolation independently bounds intermediate heights. 125 stable
wrong-result/retry cases regenerate the radius from actual supported height.
One complete extra row service covers a completed wrong row; off-grid arrest,
jam and damaged parts have no promised <30-s repair. They require retained
support and controlled completion or supported service. Height feedback does
not prove lock or seat engagement. All 79 unchanged neighbors retain their
primary seat ideally; vibration and actual non-target motion remain unmeasured.

## Writing, dense stress and sparse changes

Assumptions: linear v=200 mm/s, a=8,000 mm/s²; 2-mm contact throws; 3-ms stage
proof; inherited quarter-turn time .225 s. Crank outer-point tangential speed
is limited to 200; use tangential acceleration `8000-200²/rmax` so the sum of
tangential and centripetal accelerations stays <=8000. Rotation time
`R=t(rmax*alpha)` at that acceleration is .593665 s at 60 degrees.

For q writers, n=80/q, D=80/sin(alpha), J=t(2)+.003:

```
Wwrite=2t(D)+2J+.010+n[8t(D/8)+10J+t(D)]
       +(n-1)t(5.08)+t((n-1)5.08)
ends=3J+2[t(3.2)+.003]+2[.225+.003]
row=Wwrite+2[ends+2R]+t(5.08)
Tdense=2.010+[ceil(80/B)+1]row
```

The stopped sweep resets radii, carries them through eight positions, releases
selected channels, returns, clamps and reads. Temporary holding before the
common lock is unbuilt. Eight masks still mean **51,200 decisions/dense map**.
The three endpoint stages allocate capture-enable, capture and detach. First
physical writing, two colors, all empty resets, feed, one causal row retry,
receipt/registration/final settling (2 s) and fault regeneration (.010 s) are
inside the boundary. Expanded timelines cross-check the formula.

Scan alpha20…80 degrees by 1 degree plus the analytic optimum; B1…80 and q
all divisors of 80. Best allocated cases satisfying the *dense comparison* <30 s:

| Construction | B / writers / outputs | Seconds | Assumed dollars |
|---|---:|---:|---:|
| Serial colors, stopped writer, routing granted | 27 / 2,160 / 2,160 | 26.983 | $1,858.20 |
| Parallel color decks granted, stopped writer | 16 / 1,280 / 1,280 | 28.769 | $1,180.60 |
| Serial, absolute writer oracle | 27 / 1,080 / 2,160 | 29.362 | $1,318.20 |
| Parallel, absolute writer oracle | 20 / 800 / 1,600 | 26.986 | $1,027.00 |
| Three planar bays, 60°, serial/stopped | 3 / 240 / 240 | 177.424 | $379.80 |

Parallel grants two arbitrarily packable 3.2/6.4-mm color decks and their extras
for free. Absolute writing replaces each group bracket with 2t(D)+.010,
granting independent multilevel positioning at binary-channel cost. Neither
is constructed. Deleting writing entirely leaves the best planar/parallel
case at **50.662 s/42°**. With shaft exclusion reduced to 4/0 mm it is
42.015/38.259 s (20…89° scan); zero exclusion reintroduces shaft interference.
These results are scoped to the rates and topology, not universal speed bounds.

At base60, Wwrite=2.547994 s and serial row=6.264790 s. Programming still spans
the full radius even when few cells change. Sparse timing therefore depends on
**visited rows**, not only changed fraction. The source schedules synchronous
color services, monotonic seeks in each bank and empty return to bank row zero;
an immediate retry adds service but no seek. For B3, largest bank 27 rows,
let n be the maximum number visited in any bank. A conservative envelope is:

`Tsparse <=2.010+(n+1)[row-t(5.08)]+(n+1)t(26*5.08)`.

Every synchronized seek is bounded by the bank span, including initial seek
and final return. The bound deliberately tolerates uneven row placement among
banks; it does not assume independent asynchronous yaw.

| Maximum visited rows/bank | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|
| Conservative seconds | 15.810 | 22.709 | **29.609** | 36.509 |

For four rows even zero seek needs 33.082 s, so this base two-color protocol
cannot meet 30 s there. An inactive color can be skipped, but no such speedup
is credited. A few scattered walls may occupy many rows; a larger cluster may
occupy few. These are **hypothetical sensitivities**, not representative map
statistics. The gameplay compliance question remains open.

## Full-machine ledger and uncertainties

Allocation `$195+$20B+$.50Bq+$.02(80B)` comes from E-247/E-251 categories:
common controls/power/frame/wiring/drive/feed; $20/head reader/enable/arrest;
$.50/writer and $.02/radius keeper. It grants **zero incremental dollars** for
crank bearings, compensation cam, yokes, loaded radial locks and extra decks.
B3 leaves $120.20 under $500 for those unresolved extras. B16's $1,180.60 can fit
the new illustrative research envelope *only before extras*; it is not a priced,
credible demonstrator yet. It must justify its 1,280 channels and cost reduction.
For comparison E-247 had routing-granted B8/640/27.748 s/$831.80; E-252 had
B10/800/28.627 s/$811 with added parking hardware free. No price floor is inferred.

| Duty | Cell / row | Per head | Board B3 / B27 |
|---|---|---:|---:|
| Columns / lateral guide stations | 1/2; 80/160 | bank resident | 6,400/12,800, either case |
| Fixed lug forms / primary seat | 10/1; 800/80 | bank resident | 64,000/6,400, either case |
| Radial slider / lock / temporary hold / arm / captured follower / yoke | shared | 80 each | 240 / 2,160 each |
| Radius index sites / radial wear pairs | shared | 720 / 80 | 2,160/240 / 19,440/2,160 |
| Yoke wear contacts / output guide stations | shared | 80 / 160 | 240/480 / 2,160/4,320 |
| Retained capture / yaw link / enable / radius readback | shared | 80 each | 240 / 2,160 each |
| Shaft / compensation / release / yaw / feed coordinates | shared | 1 each | 3 / 27 each |

Largest resident bank is 2,160 cells at B3 or 240 at B27. Fixed lug forms are
not moving failure sites. Springs, sockets, inserts, bearings, terminations and
fixtures remain unknown counts, not zero. No new resident hinges or individually
installed local latches are proposed. Shared head replacement requires resident
support; interrupted failure needs props. A head/shaft fault blocks its bank or
exposes its active color. Reader common-mode failure is not independent per cell.

Crude alpha60 stock allocation: one 3×6-mm crank bar and two same-length yoke
rails/output, not a routed or strength-qualified assembly. This adds 1.405 L
at B3 or 12.641 L at B27. With E-252's 2.198-L resident stock: **3.603/14.839 L**,
about **74–222 / 305–916 extrusion hours** at assumed 15–5 mm³/s, 10% scrap,
before followers/frames. Five-second column insertion plus four ten-second head
placements/output gives **8.89+2.67 / 8.89+24 h** before wiring/calibration.
Layer direction and 406.4-mm members need modular joining on the 256-mm bed.
No slicer time or yield claim is made.

Radial pitch11.547 with an assumed 2-mm follower gives 4.423-mm half-clearance
at adverse e=.35. This is broad index geometry, not holding accuracy. Exact
endpoint errors for radius and common-carrier bounds each ±.15/.35/.70 mm plus
±.5° common angle error are **.482/.855/1.509 mm**, assuming the ideal compensation
law otherwise. No height-accuracy limit or X1C prior is inferred. Carrier bias,
shaft twist and reader zero correlate; compensation mismatch, wear and flexure
are additional errors. No board yield follows.

At alpha60, vertical F gives radial lock demand F sin(alpha). Forty outputs at
1 N each imply .866 N/lock, up to 4.335 N m starting shaft torque and 40 N carrier
reaction, before inertia/friction. For .1/10 N torque is .434/43.350 N m. These
are scenarios, not payload requirements. Opposing shaft/carrier work cannot be
deleted without an actual coupled transmission. Bilateral capture avoids
assuming gravity-following, but requires reverse-force retention.

## Decision

No crank detent, guide or narrower-shaft campaign yet. The width and travel
costs survive favorable relaxations, but **dense latency and >$500 alone no
longer justify a product rejection**. The sparse three-row envelope creates a
specific reopening condition: measured gameplay coverage, comparative value
against simpler mechanisms, and a routed support/retention implementation.

Highest-value next work is an evidence-based gameplay map/transition sample,
including row/bank occupancy and scattered edits, before selecting an expensive
head. Compare the simple moving screwdriver row and a concrete mechanical-AND
selector against shared-mask and head-hydraulic controls under that workload.
Sander's manual threaded-pin success is useful informal feasibility input,
not speed/retention/production qualification; reconstruct A-007/E-050/E-131/E-156
before reopening screws. Specialized manufacture may help a few shared parts,
not erase thousands of interfaces. Head hydraulics remain an alternative, with
E-222's independent isolation/flow/compliance obligations; do not start seals
or manifolds merely because this crank screen ended. No print is justified yet.
