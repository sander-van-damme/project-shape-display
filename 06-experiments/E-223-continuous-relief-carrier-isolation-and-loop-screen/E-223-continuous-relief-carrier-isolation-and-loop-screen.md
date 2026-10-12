---
status: complete
builds-on: [E-130, E-222, E-139, E-218]
---

# Continuous relief transport couples unchanged heights; separate loops restore local machinery

**Stop the tested row relief conveyor and resident five-code loops.** A passive
prewritten support train translated by one pitch necessarily carries an upstream
height into the next site. Unequal unchanged neighbors cannot both retain height.
Separate loops remove that coupling but restore **6,400 independently retained
phases, 12,800 pulleys and 32,000 code pads**, before connecting ramps, guides or
programmers. Neither earns geometry refinement or printing. This is a transport
constraint and a scoped architecture rejection, not rejection of continuous media.

Input main `954f124`. Reproduce:
`python3 tools/curated-experiment-checks/E-223/carrier.py`.
Evidence: **mechanism hypotheses, exact material-coordinate constraints, ideal
kinematic replay and labelled allocation bounds**; self-review, no finite assembly
CAD, calibrated process distributions, dynamic arrest or physical measurements.
Five comparison heights 0/10/20/30/40 mm remain a screening alphabet, not a product
resolution decision.

## Reconstructed controls

Read and reran E-130 `exchange.py`: the 45-degree loaded transfer needs at least
**.145298 N** additional linear restraint or **2.909911 N mm** rotary torque in
its favorable friction scenarios. Tangent spheres preserve contact but not ground
restraint. Upstream unchanged-stack overlaps are **2.92000 / 1.42879 mm**.
E-139 separately shows that a flat dwell does not arrest moving input inertia.

Read and reran E-222 `screen.py`: arrested forks and flat 10-mm tokens replace the
rolling contact. Four inserts plus four removals in a mixed row require eight
four-stroke cycles. Its optimistic schedule needs **eight heads, 640 forks,
640 shuttles, 25,600 tokens and 27.4848 s**, including one row retry. This is a
necessary timing allocation, not constructed routing, feed, support or reader.

## Proposed transactions, before geometry

**Row relief conveyor:** one circulating train per row; 80 parallel row trains.
Each loaded run lies on a grounded rail at a fixed datum. Simple guided columns
ride broad height pads, with connecting ramp pieces between consecutive pads.
A second 80-position run returns below the loaded rail. End turns lie outside the
column field with clearance for full-height pieces; incoming media no longer
passes sideways through a stationary upstream stack as in E-130.

Height pads are reusable solid blocks; an outside writer removes returned pads,
sorts them by code, loads requested blocks and corresponding transition ramps,
and reads their actual heights before entry. Adjacent codes require distinct ramp
connections; these joints and the writer are unconstructed. Grant a continuous
relief surface to test a *more favorable* topology before designing them. Inventory,
physical selection/assembly, empty return and registration remain inside the update.
This changes transport and support topology, not the principle of a cam surface.

Intended old-to-target sequence:

1. Read old top heights and loaded-train identity while each train is stationary.
   Program the incoming run from the newly received map; old support stays loaded.
2. Release the row drive brake and advance the train. Grounded rail takes vertical
   reaction; positive belt/chain drive takes ramp thrust. Columns follow the
   continuous old-to-new relief. Rows outside the changed region remain parked.
3. Brake on target dwell positions, prove actual heights/support and registration,
   and park. Returned old pieces become writer stock; no disposable mask is free.
4. Source loss invokes a normally applied **grounded drive brake**, with the train
   still mechanically coupled. This explicitly supplies E-130's missing reaction;
   brake torque, closure delay, inertia, belt strength and follower sticking remain
   unqualified. Reader disagreement retains the brake; retry requires rereading
   positions and rewriting missing pieces. A jam requires supported service.

**Failure at step 2:** even granting perfect contact, complete writer, unlimited
stock and instantaneous ideal braking, other columns in a changed row must move.
This is a deliberate geometric displacement, not a small vibration allowance.
An unchanged row can stay parked, but an unchanged loaded region within that row
cannot. There is no <30-s valid arbitrary/local-map cycle for this embodiment.
Do not repair it with more detailed ramps or support-pad clearances.

**Separate five-code loops:** give each cell its own short loop containing the five
fixed height pads and connecting ramps. A reusable row writer couples to 80 loops,
proves coupled braking before releasing their phase keepers, advances only changed
loops to the target pad, proves height and keeper engagement, then undocks. Old
height is actual loop phase; unchanged loops never move. Programming is physical
phase selection; no block sorting or external stock is needed. Return/storage are
inside each loop. A mid-move power loss must keep coupling to the writer brake;
a parked loop needs a ground phase keeper because a dwell alone does not arrest
coasting. Reader disagreement retains capture. This grants a supported transaction,
not a constructed keeper/coupling or contact path.

That inversion escapes the shared-material conflict, but **independent phases are
not supplied by a single shaft**. A stopped travelling writer reduces motors while
retaining resident phase keepers, docks and local circulation. A bank common drive
instead needs independent coupling/parking functions. Stop this embodiment at its
replication/routing screen; do not launch another keeper or clutch campaign.

## Exact unchanged-neighbor obstruction

Let `r(s)` be an unmodified, prewritten relief height on the loaded rail. At column
coordinate x and train advance q, ideal point contact gives `h(x,q)=r(x-q)`.
Two unchanged point followers at 0 and pitch p require different constants over
material intervals `[-L,0]` and `[p-L,p]` during stroke L. For **L >= p** those
closed intervals overlap: the same material point would need two heights.
Endpoint equality already fails at L=p. Longer dwell/guard runs cannot fix it.

Concrete witness: an old row alternating 0/40 mm, with one distant cell requested
to change. Two adjacent unchanged sites see **40-mm excursions** within the first
5.08 mm of train motion. Linear interpolation makes the excursion continuous;
changing the interpolation cannot remove the endpoint contradiction. For five
levels, **20/25 unequal unchanged two-site states fail**. Even without isolation,
a one-pitch update can realize only **125/625** two-site old/target pairs: the
second target is forced to equal the first old height. A full new row requires
flushing the old support run, crossing this witness first.

A finite flat foot can bridge a low valley, but cannot avoid collision when an
old high support point enters an unchanged lower foot one pitch downstream.
Thus widening feet does not rescue arbitrary maps. Online rewriting *between or
under loaded sites*, lifting columns off the train, lateral bypass and relative
motion between carriers are changed topologies; this proof does not cover them.
Each must supply its own supported transfer and count its independent state.

Manufacturing robustness of the rejection: labelled independent height errors
bounded by e=.15/.35/.70 mm leave a 40-mm difference of at least
**39.7/39.3/38.6 mm**. Common additive height bias cancels. With coordinate errors
±e, the greatest neighbor separation is **5.38/5.78/6.48 mm**; a 406.4-mm flush
still exceeds it. Shared pitch scale, sag, wear and frame distortion cannot be
averaged away; no distribution, yield or hardware margin follows. A manufactured
escape requires a changed load/transport path, not finer printing.

## Whole-machine ledger and timing limits

Counts below are functional lower counts or explicit provisions, not a complete
BOM. All routes also retain 6,400 columns, at least two guide stations/column,
frame modules, readback, wiring and safe access. Row has 80 cells; a bank contains
b rows. Motors are not equated with controlled mechanical functions.

| Function | Row conveyor: cell / row / b-row bank / board | Separate loops: cell / row / b-row bank / board |
|---|---|---|
| Carrier/code positions | 2 / 160 / 160b / 12,800 including incoming run | 5 / 400 / 400b / 32,000 |
| Connecting ramp positions and mounts | one per carrier position; joints unbuilt | one per code position; joints unbuilt |
| Circulating trains | shared / 1 / b / 80 | 1 / 80 / 80b / 6,400 |
| End pulleys and axle placements | shared / 2 / 2b / 160 | 2 / 160 / 160b / 12,800 |
| Independent parked-phase retention | shared / 1 / b / 80 | 1 / 80 / 80b / 6,400 |
| Grounded loaded bearing sites | 1 / 80 / 80b / 6,400 | 1 / 80 / 80b / 6,400 |
| Accessible shared writer | stock picker, ramp assembler, sorter and reader; count/routing unresolved | H phase drives/brakes/couplings; visits 6,400 docks |

Each pulley adds journal/wear surfaces; each joint needs controlled step, seating
and retention; every phase keeper is a failure site even if printed monolithically.
Springs, inserts, fixtures, fasteners, belt tensioners and drive transmission remain
unknown, not zero. Full-pad stock for the row conveyor includes installed old and
incoming codes plus sorted reserve. A deliberately ample **2N blocks/code = 64,000
blocks** supports double buffering for any map; it is a sufficient provision, not
an inventory minimum. Optimizing it cannot repair the earlier isolation failure.

Separate-loop routing witness: take two pulleys of radius 4 mm with centers
5.08 mm apart along the row direction. Copying at pitch makes one loop's right
pulley coincide with the next loop's left pulley. Pitch limits only tops, so a
multideck escape is permissible. With 2-mm bases and 40-mm maximum pads, a simple
**nonoverlapping bounding-box** allocation has width
`5.08 + 2(4+42) = 97.08 mm`, requiring 20 decks and 1,840 mm summed box depth.
This is a poor *specified* layout, **not a lower bound for all packing**. Upright
nonrotating carriers, different loop orientation or remote offsets are different
routes, with bearings/links still to count. Do not optimize this pulley layout.

At assumed 3.4-mm square pad stock, the five 2/12/22/32/42-mm blocks total
**8.13824 L** for separate loops, versus E-222's **2.95936 L** of tokens. They need
32,000 placements plus 6,400 loops/keepers and 12,800 pulleys; belt/ramp volume is
additional. At assumed effective 5–15 mm³/s and 10% scrap, pad stock alone needs
**167.5–502.4 h**. Column stock adds E-222's 4.608 L before guides/frame. These
are volume allocations, not slicer estimates or actual process times. Functional
joint error, roughness, anisotropy, creep, belt stretch and correlated batch bias
remain unqualified. A loop buried below the board requires supported access;
a row-train jam affects up to 80 cells. No accessible repair route is constructed.

**Timing:** shared row transport at 200 mm/s has a favorable **2.032-s** travel
floor for 406.4 mm, excluding acceleration, start/stop, proof and return readiness.
If physical writing takes tau seconds/code with W writers, arbitrary programming
requires at least `6400*tau/W`. Even granting perfect pipeline overlap and only
E-222's two global seconds, `2+max(2.032,6400*tau/W)<30` needs at least
**3/5/12/23 writers** at tau=.01/.02/.05/.10 s. Sorting, ramp installation,
registration, homing/reference, proof, settling and bounded recovery only add time.
These floors are not a complete schedule or a way to hide preparation in a buffer.
The isolation counterexample already rejects the row cycle independent of speed.

For separate loops, a favorable H-channel writer has `T >= 2+6400*t_cycle/H`;
at H=80 the complete per-cell visit must be **<.35 s**. That interval must include
couple/prove, keeper release, arbitrary phase move, arrest, keeper proof, readback,
uncouple, transport and recovery share. No mechanism establishes it. Unlike
E-222's explicit 27.4848-s scenario, neither new topology has a complete accepted
schedule. We stop before inventing omitted motion times or a favorable BOM.

Purchased economics: even assigning only $250 to *all* shared structure, writers,
sensors, electronics, supply and motion leaves **<$.0391/cell** under $500 for
all resident loop hardware combined. This is an optimistic allocation ceiling,
not a quoted cost or proof of universal impossibility. Printed journals/keepers
remove bought parts but retain their 6,400-fold assembly, wear and service burden.
The row conveyor's fewer drive functions cannot compensate for its failed isolation.

## Decision and next discriminating change

Preserve the material-coordinate conflict as an early filter for prewritten relief
belts, linked pads and transported height masks. Source-loss braking and below-rail
return alone do not make such a conveyor an arbitrary-map machine. Independent
loops escape the proof but are a worse repeated-hardware starting point than the
simple-column controls; park this construction before detailed contacts.

The next useful invention must **decouple media transport from loaded support
without a resident moving loop at each cell**: e.g. unloaded low-profile commands
program an in-place broad support, or an old/target exchange occurs orthogonally
with explicit support overlap. First construct one unequal unchanged-neighbor
witness through the complete swap, including physical rewriting. E-218 remains
an overlap-law comparator, not a revived cassette winner. No next-step print,
clutch, pocket or fine guide optimization is justified.

Checks: rerun both predecessor sources; exact closed-interval/material identity
proof; all 625 two-site endpoint combinations; 16/64/256-point continuous traces;
finite-foot high-point obstruction; coherent/relative error bounds; independent
volume/unit checks and E-222 schedule import. These establish necessary-condition
failures and accounting, not independent review or hardware performance.
