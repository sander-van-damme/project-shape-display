---
status: complete
builds-on: [E-217, E-216, E-084]
---

# Positive two-cassette exchange works ideally; translating stair media does not pack

**Retain the ideal two-stage positive-support principle; reject this translating
staircase before local refinement.** It removes old-code rewriting and 160
friction grips/head, but its resident load-bearing media cannot fit adjacent
5.08-mm rows. No complete machine is selected.

Input main `693829e`. Reproduce with
`python3 tools/curated-experiment-checks/E-218/exchange.py` (standard library,
stdout only). Evidence: **mechanism hypothesis, exact ideal contact-event replay,
necessary geometric inequalities and calculations with labelled assumptions**.
Self-review only; no CAD, measurements, quotes, prints or purchases. Five levels
0/10/20/30/40 mm are a comparison workload, not a product resolution decision.

## Finite supported exchange, before a writer

Each column has a flat 4-mm-wide foot, with two separate 1.6-mm-wide bearing
lanes and a .8-mm central gap. It slides through two lateral guides. An old
cassette supports one lane; an incoming cassette supports the other. Each
cassette carries a grounded positive height profile, minimum 4-mm solid base.
Connecting beams outside the isolated-row finger sweep are assumed; board
carrier/frame clearance remains unproved.

Let old and target profiles be o and n, and their elevator displacements a,b.
Under ideal gravity-following rigid contact, `h_i=max(o_i+a,n_i+b)`.
Simultaneous takeover would require incompatible offsets +40,−40,0 mm.
Instead use this sequential exchange:

| State | Old a / incoming b (mm) | Column heights (mm) | Grounded load path |
|---|---|---|---|
| Write/read incoming outside load path | 0 / absent | 40,0,20 | Old cassette → fixed row dock → frame |
| Insert incoming beneath old base | 0 / −45 | 40,0,20 | Old dock; new top ≤−5, old base bottom −4 |
| Raise incoming | 0 / −20 | 40,20,20 | First/third on old; second on incoming lift |
| Finish raising; close/prove new dock | 0 / 0 | 40,40,20 | Old supports descending cell; new supports rising cell; unchanged has both |
| Take old on lift, release old dock, lower | −20 / 0 | 20,40,20 | Descending cell follows old lift; others on new fixed dock |
| Clear and remove old | −45 / 0 | 0,40,20 | All on new dock; old becomes next unloaded spare |

Incoming rise precedes outgoing descent. Thus all changed cells move monotonically
and unchanged cells stay at their original height **in this ideal contact model**.
There is no reset to zero, friction pickup or copied old-height program. The old
physical profile already encodes old heights. Omitting the old descent would drop the first cell 40 mm.

For all 15,625 three-column old/new combinations, the executable checks exact
contact events and interval midpoints. Affine intervals cover the intervening path. A dense scalar holdout checks all
25 height pairs. This assumes disjoint lanes, adequate structure and following.

**Source loss / recovery construction:** fixed row docks have positive crossbars;
media settings have a common keeper. Two shared lift carriages/head take the
old/new cassettes. A proposed common rack escapement on each carriage uses a
holding dog and a normally engaged trailing catch; withdrawal of a dog requires
its companion catch armed. Catch spacing is assumed 1 mm. During a commanded
step, a lost drive can descend at most one pitch before a frame-backed tooth
catches it. No claim of zero fault motion or qualified catch impact follows.
An unproved catch blocks dock release. Fixed docks carry completed terrain;
no cell brake is required. Dog sequencing, tooth strength, springs, independent
engagement sensing and jam release remain unconstructed interfaces.

In the ideal max model a 1-mm carriage drop changes any affected height by at
most 1 mm. Keep both media present after a transfer fault; prove actual heights,
restore/prove the stalled carriage, and resume the rise or descent. Before
exchange, a bad target read keeps the old dock closed and allows an unloaded
rewrite. After both docks hold the intermediate maximum map, recovery can pause
there. Do not remove the old cassette until all targets and the new dock are
proved. Four injected missing read/keeper/arrest/dock proofs stop the logical
sequence. Readback and flags are specifications, not constructed sensing.
Only one detected pre-transfer rewrite/retry is included in timing; structural
failure, hung columns and lost readback require a safe stop, without a 30-s claim.

## Constructed medium and its decisive packing failure

Give each column one 1.6-mm-wide staircase slider: five horizontal terraces,
8 mm long, at heights 0/10/20/30/40 mm above a 4-mm base. An unloaded setter moves
it through four 8-mm increments, total 32 mm. The fixed column foot sees the
selected terrace. Flat bearing faces take vertical load into the cassette floor;
a common row bar enters one of five broad notches on every slider to prevent
translation. This still repeats 80 guide/keeper engagements per row. A proposed
4-mm notch and 2-mm bar leave 1-mm centered half-clearance; neither common
actuation nor monolithic printing makes those engagements disappear.

The staircase occupies 40 mm in the row direction. Over all independent codes,
its swept depth is **40+32=72 mm**, before an assumed 4-mm guide/frame allowance:
**76 mm versus 5.08-mm row pitch**. Even zero frame allowance, perfect manufacture
and terraces only as long as the assumed 2-mm foot require `9×2=18 mm`.
For coplanar, noninterleaving, full-base sliders, fitting all arbitrary adjacent
codes would require terrace length ≤5.08/9=.564 mm; it cannot support the
2-mm foot. This is a necessary geometry failure of this construction, not an
FDM accuracy prediction. The executable finds base collisions for **all 25 adjacent code pairs** at
8-mm terraces; 72-mm separation clears them in the zero-frame control.
Two foot lanes enable handoff; they do not provide fifteen free row lanes.

A deliberately simple deck escape places overlapping row envelopes in separate
vertical bands. With 8-mm terraces it needs 15 phases. Allocating 44-mm profile,
45-mm exchange stroke and 1-mm separation per band gives **1,350 mm depth**.
At 4/2-mm terraces this construction gives 8/5 phases and 720/450 mm depth;
with .70-mm error the 2-mm terrace has negative capture margin. These are
**specific sufficient rectangular deck allocations, not universal minimum
machine depths**. Crossed routing, overlapping transfer volumes or different
media topology might do better and must be constructed. Decks also require
variable-length columns/relay rods, new guide spans and docking access. Retaining
identical columns is no longer free. Simply spreading rows instead needs about
80×76=6,080 mm of support footprint plus load-path fanout. Neither is a compact,
priced escape. Resident row overlap is enough to stop; do not refine the notch.

## Full 6,400-cell ledger and optimistic schedule

Counts below describe the attempted medium even though its packing fails.
At B=16 heads, each bank serves five rows; each head has one spare cassette.

| Functional item | Cell / row | Bank (400 cells + spare) | Board |
|---|---|---|---|
| Columns / lateral guide stations | 1 / 80 columns, 160 stations | 400 / 800 | 6,400 / 12,800 |
| Resident state sliders, slide guides, keeper engagements | 1 each / 80 each | 400 each | 6,400 each |
| Resident terrace faces / keeper notch positions | 5 / 400 each | 2,000 each | 32,000 each; faces, not extra pieces |
| Spare sliders / guides / keeper sites | 80 per head | 80 each | 1,280 each |
| Cassettes / common keeper bars | 1 resident per row | 5 resident +1 spare | 80 resident +16 spare |
| Alternating row dock sites | 2 per row | 10 | 160; empty docking lane retained |
| Loaded lift carriages / positive arrest sets | 2 per head | 2 | 32; two dogs/set means ≥64 dog functions |
| Head carriage / lane transfer / writer lanes | 1 / 1 / q per head | same | 16 / 16 / 16q |

Total media: **7,680 independently retained slides**, 38,400 terrace faces and
38,400 keeper notch positions. Keeper fixtures, docks, readers, lift bearings,
arrest springs and wiring have no complete BOM; no local spring/insert/grip
is prescribed. Media guide/contact wear and
notch registration occur 7,680 times. There are 6,400 column insertions, 7,680
media placements, 96 keeper setups, 160 dock alignments and 16 head alignments;
406.4-mm carriers require at least two printed sections at the recorded build
volume. Buried media failure requires positive support before removal; it is
not accessible merely because a writer is shared. One dock fault affects 80
columns, head outage 400 cells, shared reader bias potentially all commands.

For a favorable timing relaxation the full-width head carries its spare below
the rows and writes it there, eliminating a 406-mm edge-feed stroke. This assumes
an unobstructed underfloor route, alternate-lane docking and unloaded writer
access; packing above already defeats the proposed route. No prewritten spare
or stored old code is credited. At every visited row:

- Write all 80 target values, including unchanged values, from arbitrary prior
  spare contents. Each q-way group uses a worst 32-mm set, 2-mm engagement and
  withdrawal, and 5-ms read. Group indexing is 5.08 mm. Open/close keeper is in
  the stated auxiliary allowance; no separate erase is needed for absolute setting.
- Raise new and lower old by 45 mm each; charge two more empty 45-mm carriage
  resets, two 2.4-mm lane-transfer strokes and one 5.08-mm row move.
- Charge .5 s/row for docking, keeper, computation/registration and load/height
  proof, then 2 s/map global overhead and one complete worst-row retry. No overlap.

All axes assume v≤200 mm/s and a=2,000/8,000 mm/s². Continuous motion is a
**relaxation with unbuilt continuous arrest**, not the positive dog sequence.
The explicit indexed alternative stops each loaded 1-mm step and charges 1 ms
for dog proof; empty returns are continuous. Loaded-carriage inertia is unpriced.

| Arrest assumption | B / q | Data lanes | Calculated full-map s |
|---|---|---|---|
| Continuous, a=2,000 | 16 /16 | 256 | 28.400 |
| Continuous, a=8,000 | 8 /40 | 320 | 25.942 |
| Continuous, a=8,000 | 16 /8 | 128 | 29.634 |
| Continuous, a=8,000 | 16 /16 | 256 | 20.525 |
| Indexed, a=8,000 | 16 /40 | 640 | 24.674 |

Sweep B=1/2/4/8/16, q=1/2/4/8/16/40/80 and both accelerations. No B≤4 survivor;
indexed arrest has no other minimal-q survivor in this grid. These are conditional
schedule calculations, never machine passes. At B=16/q=8/fast, .25/.5/1/2-s row
allowances give 28.134/29.634/32.634/38.634 s. A five-row regional patch in one
bank still consumes six row services including retry: the full-board critical
path time. Each visited row replaces all 80 supports. Rows outside the touched
bank remain docked; real unchanged-cell displacement within a row is unqualified.

E-216's 256-lane comparator takes 21.167 s with 2,560 friction grips. E-217's
384-gate binary case takes 23.929 s with those grips plus 7,680 bits and 2,560
pushers. This construction eliminates the grips/pushers/old-code write, but
repeats resident direct-support media and fails geometry. The favorable 128-lane
case leaves only $1.953/lane from a **$250 assumed reserve** under the $500 ceiling;
640 lanes leave $.391. Under $400 those become $1.172/$.234. These are allocations,
not quotations; 32 lifts/arrests, 16 carriages, lane transfers, writers, readers,
docks, power, guides, wiring and fasteners must also fit. No affordable BOM exists.

## Manufacturing, force and evidence limits

The illustrated solid staircase stock is `1.6×8×(4+14+24+34+44)` mm³/slider.
At B=16, media alone is **11,796.48 cm³**, excluding carriers, guides and feet.
Assumed effective extrusion 5–15 mm³/s gives **655.4–218.5 h**; 10% scrap multiplies
by 1/.9. E-216 column stock adds 4,608 cm³ and 256–85.3 h before changed feet or
long deck load routes. Ten/thirty seconds to place each media slider adds
21.33/64 h; columns at five seconds add 8.89 h. Hollowing needs a load-path study
but cannot remove the geometric sweep. Tall thin terraces need layer-direction,
buckling, creep and warpage evidence; they are not qualified compression posts.

Use E-216's explicitly assumed summed common/local/alignment bounds
.15/.35/.70 mm. In the attempted bearing lanes, nominal 1.6-mm overlap leaves
1.45/1.25/.90 mm; an 8-mm terrace under a 2-mm foot leaves longitudinal margins
2.85/2.65/2.30 mm. The proposed keeper leaves .85/.65/.30 mm. These broad nominal
margins improve on micrometre clearances but do not qualify a slender step or
shared bar. Common print/row errors affect whole cassettes. Opposite signed
old/new vertical errors can change an unchanged cell by up to **.30/.70/1.40 mm**;
shared bias within each cassette does not cancel between cassettes. Compliance,
debris, read error and dock deflection add uncertainty. No disturbance exception
or actual process envelope is established.

Assumed cell service loads F=1/3.27/10 N require row supports of 80/261.6/800 N,
not friction normal forces of E-216's 654–2,616 N at its middle load. At a 10-mm
drive radius ideal torque is .8/2.616/8 N·m, before mass, friction and efficiency.
A row raised 40 mm needs 3.2/10.464/32 J. Eccentric half-foot support adds
guide drag and bending.

The max law also assumes each descending column follows gravity. With assumed
unloaded mass 3 g, an 8 m/s² downward acceleration leaves only
`.003×(9.81−8)=.00543 N` for guide drag. Quasistatic downward force is only
.02943 N; assumed drag .005/.05/.2 N spans following and complete sticking.
There is no qualified guide-friction bound. Top readback must catch a hung column;
adding 6,400 springs or friction pickups would be a changed architecture, not a
free recovery. Impact at cassette contact/catch, lateral vibration, guide wear,
PLA creep and dynamic separation remain outside the rigid max model.

## Decision and reopening condition

Preserve the grip-free handoff law and scoped packing failure. Do not optimize
this slider, keeper, writer or dog and do not print it. Faster writing cannot
cure resident geometry; this does not reject all direct-support media.

Reopening needs a changed encoding/load route that stores height without this
long translating staircase, fits adjacent arbitrary codes and retains the two
positive bearing paths. First compare bounded-volume rotary height blocks with
separable solid-height support pieces: count resident state/retention, unloaded
selection/inventory, service and complete transfer at scale before drawing fine
contacts. A rotating block must supply actual horizontal bearing faces and
retention; a loose-piece scheme must count every feed/sort/return transaction.
Neither is a survivor.
