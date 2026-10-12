---
status: complete
builds-on: [E-170, E-236, E-238, E-250]
---

# Staggered shared carriers clear turning caps but multiply supported transactions

**Retain vertical staggering as a geometric building block; park this shared
carrier machine before capture, guide or angular-seat design.** Two alternating
carriers replace independent Z motion with common strokes and preserve fixed
unchanged-column support ideally. Their complete five-stroke schedule nevertheless
needs **16 banks/1,280 reusable capture selectors, 26.073 s**, with **$1,180.60**
in a favorable inherited allocation that charges nothing extra for the second
carrier or yaw. This is worse than E-236's 400 selectors, despite solving a
separate unchanged-support problem. No selected machine or justified print.

Fetched input main `f23d6d3` (engineering unchanged from `8b35644`). Reproduce:
`python3 tools/curated-experiment-checks/E-251/screen.py` (stdlib; imports E-236
and E-167). Evidence: **finite synthesis, analytical geometry, ideal support
replay and assumed timing/cost/error scenarios; self-review only**. No fabricated
article, contact dynamics, calibrated FDM prior, priced BOM or independent validation.
Generated JSON is disposable.

## Changed architecture and complete operation

One integral column has a square cap, stem and seven periodic fixed lug forms.
A stationary rail supports each column; its height stores state. A reusable
row head has two Z carriers serving global checkerboard colors `(row+column)%2`.
Each carrier contains 40 selectively closing bilateral captures. A common yaw
motion acts through captures only on selected columns. The commands must remain
mechanically retained under load; they are not 80 independent Z motors.

Before each common signed stroke: write/read the 80-bit mask while all columns
are seated; capture/prove selected lugs below the fixed rail; lift colors to
different axial offsets; turn both 90 degrees; execute common Z displacement;
turn back; lower onto fixed supports; prove support and detach. The empty
carriers retain the new integer datum before the next write. Unchanged columns
never join a carrier or lose their fixed primary support in this ideal protocol.

This differs from E-170's blocked pocket pickup: **radially closing captures
are granted**, so they can engage before release lift. It does not repair that
old gate geometry. It differs from E-247's nine differential rails: only two
color carriers move together, with selection rewritten between signed strokes.
It differs from E-250's independently held Z outputs: arbitrary deltas come
from time-coded membership, not independent simultaneous travel.

The grants are consequential: no finite selective bilateral jaw, torque coupling,
retainer, resident yaw restraint, compatible guide, carrier bridge, reader or
failure-safe arrest is constructed. A common motor brake covers neither a lost
capture nor a broken branch transmission. Local brackets, cams and springs must
not be developed merely because this logical protocol has support flags.

## A broad axial phase window, not a manufactured mechanism

Use pitch 5.08 mm, 4.8-square ×2-mm caps, 10-mm discrete height spacing, 1.2-mm
lugs and 1.2-mm fixed rail thickness. Five output heights over 40 mm are a
comparison workload, not a product resolution requirement. During turning,
let color offsets be `s1 < s2`. Sufficient axial separations are

```
s1 > 2 + E                    active cap versus unchanged cap
s2 - s1 > 2 + E               neighboring active colors
s2 < D - 1.2 - 1.2 - E        next lower lug below fixed rail
```

The unused active/U upper-cap bound `s2 < D-2-E` is weaker. E is a labelled
**total adverse loss of each axial gap**, including relative placement and
thickness effects; it is not a per-feature standard deviation or an X1C prior.
Maximizing the least slack gives `s1=(D-.4)/3`, `s2=2*s1`, and
`margin=(D-6.4)/3-E`. At D10 the offsets are **3.2 and 6.4 mm**; margins are
**1.20/.85/.50/0 mm** at E=0/.35/.70/1.20. Two phases need `D>6.4+3E` under
these sufficient conditions. D5 fails even nominally; D7.5 leaves only .0167 mm
at E=.35. Do not shrink lugs/caps to reopen those cases. E-167's one-color window
has a different, less demanding spacing condition.

Checks enumerate all height pairs, selected/unchanged combinations, adjacent
and diagonal positions: **6,800/26,000 finite cap poses** at 16/64 angular
subdivisions, with no collision. The continuous argument is axial separation
for opposite colors/U and the diagonal circumcircle bound
`sqrt(2)*5.08 > sqrt(2)*4.8` for same-color neighbors. Aligned caps have disjoint
XY footprints during lift, 90-degree transit and seating, regardless of heights.
The same-phase adjacent midturn deliberately collides. Only the axial rail
interval is checked; this is not a finite support/jaw/guide assembly pass.

All active banks must share the stage and integer stroke datum. An independent
bank in transit can place its aligned cap at the same actual elevation as a
neighbor turning at 45 degrees: the executable includes this collision witness.
Thus a common phase clock, row-parity routing and bank inhibits are obligations.
A fault leaving one bank off-grid defeats the phase guarantee; stop the coupled
motion rather than credit a free local retry. Uniform rigid Z translation cancels
relative gaps; bank phase error, thickness bias and rail warp do not. Actual
lateral cap gap remains only .28 mm and is **not** qualified by the axial margin.

Selected caps can transiently reach **46.4 mm above the initial zero datum**.
No stage-02 maximum overshoot is specified, but this excursion must remain in
mechanical clearance and D&D use accounting. The lower capture datum is
`z=-20+10q`; its highest lifted contact is -13.6 mm, below the fixed rail.
This separates ideal planes, not routed carriers or guide bodies.

## Synthesized supported schedule

Search closed carrier walks in q={-4,-3,-2,-1,0}; independently select or bypass
each nonzero stroke; require all 25 old/target pairs and 0…40-mm intermediate
**seated** heights. Unchanged cells receive only zero masks. Capture shelf index
is `k=2+h-q`; require 0…6. The 4/12/52 walks of length 2/3/4 supply no complete
bounded code. Of 204 five-stroke walks, 28 cover all pairs and 18 use seven lugs.
Tie-breaking by row time, empty recovery depth and sequence chooses
**[-20,+10,+10,-20,+20] mm**, also appearing in E-238's earlier code synthesis.
The new result is its coupled turn transaction, not a new five-stroke discovery.

Each color has 40 columns, enough to contain all 25 transition pairs in a row;
this is an explicit arbitrary-map workload requiring the universal code.
Selected cells may detour within 0…40 between seated states. Replay checks
**15,625 three-cell maps /546,875 ideal support states**: capture precedes fixed
support loss, ground precedes detachment, unchanged cells stay seated. These
flags grant bilateral load capture; they are not contact or reader evidence.

At assumed linear v200/a8000 mm/s units, translation is .525 s over five strokes.
At angular v720/a7200 degrees/s units each quarter-turn is .225 s. Each pulse
charges three 2-mm transactions (write, capture, detach), two 6.4-mm lift/seat
moves, two quarter-turns and eight 3-ms stage proofs: **.682868 s overhead**,
in addition to its signed Z stroke. Stages are sequential; no prepared mask,
free physical overwrite or unconstructed concurrent capture is credited.

```
row = .525 + 5*.6828683298 + move(5.08) = 3.989741649 s
T = 2 + move(20) + .010 + (ceil(80/B)+1)*row
```

The 2-s allocation covers online map ingestion, registration and final settling.
One entire extra row plus empty datum reset/read covers a **detected stable,
reseated** retry; regenerate masks from actual heights. This does not cover lost
support, a jammed off-grid bank or physical repair. Proof and settling allocations
are unqualified. Regional one/five-row cases are 10.114/26.073 s with the same
conservative retry/reset allowances; arbitrary seek adds actual travel. U support
is invariant ideally; frame displacement/vibration and individual proof remain
unmeasured.

Automatic reset can restore a recoverable command/index state while the fixed
supports remain loaded; every mask overwrite already starts in that supported
state. It does not replace capture integrity, seating proof or fault detection.
Even deleting all reset/write/capture/seat overhead in the table below fails the
assumed allocation, so better reset alone cannot rescue this embodiment. Whole-pin
homing would deliberately disturb unchanged terrain and cannot be treated as a
free regional-update recovery. Selective internal reset remains an architectural
option, not a reason to reopen intricate resident hardware without a new ledger.

Six or more pulses cannot beat the selected row time **in this transaction
grammar**: both ±40-mm reach require total motion ≥80 mm, each ≥10-mm stroke
is trapezoidal, and each incurs the same overhead. This does not bound machines
that retain captures across pulses, combine yaw/lift, change paths or decode
absolute destinations. Geometry and timing do not establish optimality over
those architectures.

| Protocol / relaxation | Banks | Reusable selectors or output pairs | Calculated time | Favorable bought allocation |
|---|---:|---:|---:|---:|
| Two staggered shared carriers | 16 | 1,280 selectors | 26.073 s | $1,180.60 |
| Two serial color phases, 3.2-mm release | 40 | 3,200 selectors | 24.902 s | $2,659.00 |
| Single 3.2-mm carrier, cap collisions ignored | 14 | 1,120 selectors | 28.873 s | $1,057.40 |
| Staggered, all non-yaw transaction overhead deleted | 10 | 800 selectors | 27.564 s | $811.00 |
| Staggered, angular speed **and acceleration** doubled | 12 | 960 selectors | 28.702 s | $934.20 |

The cost relaxation reuses E-236: $195 common +$20/bank +$.52/selector; extra
carrier/yaw hardware is free. At B16, common/bank allowances alone are $515.
This is an unfavorable **scenario**, not a market price lower bound. Varying
contact throws 1/2/4 mm and proof 0/3/10 ms gives B14–16 and $1,057–1,181.
Shrinking local contacts is neither needed nor justified to make this decision.

As a separate matched E-250 control, giving independent Z/yaw pairs the same
staggered cap route removes serial color visits: five banks/400 pairs suffice
at **26.708 s** in its direct service model. The $295 shared
reserve leaves **<$.5125/complete pair** under $500. It remains an unbuilt control,
not a priced winner. E-236 has 400 selectors at 26.681 s/$503 lean shared or $675
independent allocation, but transfers unchanged support. Those scopes differ.

## Replication, manufacture, force and service

For B16 each bank serves five rows/400 resident columns. Seven lug **forms** are
fixed parts of each column, not seven independent moving latches.

| Duty / part | Cell / row | Bank / head | Board |
|---|---|---|---:|
| Moving column / fixed lug forms | 1/7; 80/560 | 400/2,800 | 6,400 /44,800 |
| Fixed vertical seat / yaw-restraint duties | 1/1; 80/80 | 400 each | 6,400 each; yaw restraint unbuilt |
| Assumed two column guide stations | 2; 160 | 800 | 12,800 |
| Bilateral capture / retained command / torque coupling | reusable | 80 each | 1,280 each |
| Command endpoints | reusable | 160 | 2,560 |
| Common Z carriers / carrier grounding-arrest duties | reusable | 2 each | 32 each |
| Row carriage, reader and bank inhibit assemblies | reusable | 1 each | 16 each |

Separate resident springs/inserts are not constructed. Capture contact surfaces,
pivots, wear interfaces, sockets, fixtures and head returns are unknown counts,
not zero-cost omissions. One insertion at 5 s/cell is 8.89 h; one capture
assembly operation at 10 s is 3.56 h, before wiring, proof or calibration.

An illustrative union of a 102-mm radius-.8 stem, 4.8×4.8×2 cap and seven E-250
lug forms is **1.661 L/board**, or **30.75–92.25 extrusion hours**, for scale only; slender
stem strength, small bearing area and angular retention are **not** accepted.
Extrusion-only time at assumed 5–15 mm³/s excludes travel/setup/supports;
10% scrap multiplies it by 1/.9. Horizontal printing changes lug/cap surface and
layer load paths; upright printing exposes slender-part and anisotropy risks.
No sliced print time, actual assembly route or qualified whole-head envelope
exists. 406.4-mm rows require segmented fabrication on the 256-mm bed. Common
warp or registration can invalidate a bank; no IID yield is inferred.

For 1,280 simultaneously selected cells, assumed 3-g moving columns, two
.25-kg carriers/bank and 8-m/s² acceleration, payload scenarios .1/1/10 N/cell
require **301/1,453/12,973 N** before guide drag. At 10-mm drive radius these
are 3.01/14.53/129.73 N m; at .2 m/s and .7 efficiency they imply
86/415/3,707 W. Rate/cost assumptions do not qualify that drive. Light unloaded
cells cannot inherit heavy-load gravity following; bilateral captures remain
required. All-up 1-N terrain adds 256 J potential energy before losses.

Head service should occur with columns seated on fixed rails. A broken rail or
column still needs a temporary prop and extraction route; these are unbuilt.
A carrier fault can affect 40 live cells/head; common-drive and reader failures
are correlated. Actual height, angular return and supported seating need proof
before detachment. Neither an encoder nor a total row-force sum proves every seat.

**Decision:** no jaw, thinner lug, guide, spring, motor-speed or print continuation.
Staggering escapes serial cap-turning but does not pay for five complete release
transactions. Reopen shared capture only through a changed transaction that keeps
selected columns safely captured between strokes or otherwise removes repeated
turn/reseat work, and count each independently arrested output immediately.
Compare that proposed change with E-222's shared-drive retention obligations
before modelling any engagement detail. The axial phase inequality and explicit
asynchronous-neighbor failure remain reusable regardless of that choice.
