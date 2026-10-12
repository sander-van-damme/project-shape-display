---
status: complete
builds-on: [E-219, E-216, A-022]
---

# Crossed redundant supports remove individual releases but duplicate bank selectors

**Retain orthogonal redundant support as a principle; park the constructed
row-at-a-time, delta-group programmer.** It replaces cassette inventory and
friction pickups with two grounded common combs per column. Its conditional
<30-s cases still require 1,280 or more independently selectable support bars,
plus reusable pickup fingers. Sharing fewer lines imposes a real scheduling
cost. No complete machine earns contact refinement or printing.

Input main `61835b6`. Reproduce with
`python3 tools/curated-experiment-checks/E-220/support.py` (stdlib, stdout only).
Evidence: **mechanism hypothesis, exact ideal support/state replay, combinatorial
bounds and assumed schedule/manufacturing scenarios**. Self-review; no finite
assembly CAD, physical measurements, purchased quotations or process priors.
Five levels 0/10/20/30/40 mm remain a comparison workload, not a resolution decision.

## In-place mechanisms and the missing state distinction

| Construction | State and grounded load path | Result |
|---|---|---|
| Additive row/column backing | Shared row offset plus column offset; no individual stored height | Only 85 of 625 two-by-two five-level maps satisfy the necessary cycle identity |
| Two crossing supports, highest wins | Column rests on the higher row/column backing; no individual stored height | 165 of 625 maps; high diagonal with low off-diagonal is unreachable |
| Redundant fixed combs plus individual column position | Each simple column stores height in its position; either grounded comb can support a periodic shelf | All discrete target maps reachable in the ideal writer replay; selection/time and physical pickup remain costly |
| E-219 cassette control | Separate height-coded media stores target; old/new cassettes support transfer | 38,320 solid pieces or 7,680 indexed wheels at 16 heads, with failed/unclosed packing and writing obligations |

For additive backing `h00+h11=h01+h10`; for maximum backing a row or column
raising either diagonal also raises an off-diagonal. The witness is
`[[40,0],[0,40]]`. Enumeration is cross-checked by reconstructing max supports
from row/column minima. This rejects **these separable load laws**, not every
shared layer, compliant surface or time-multiplexed architecture. Temporal
selection can create arbitrary maps only if something retains individual state.
A-022 does so with three serial local stages; the new construction instead
retains the single column position through parallel common supports.

## Crossed support and one actual programming sequence

Hypothesis: row combs enter column shelves from one side at frame z=0; column
combs enter from a perpendicular side at z=−10 mm. Each comb has a positive
frame-backed seat and a keeper against withdrawal. A column remains supported
when **row OR column comb is seated**; opening row set R and column set C frees
exactly R×C. Either path must carry the entire cell load. Selection is in-place:
no copied old-height mask, spare cassette or sorted stock.

One travelling row head per bank carries 80 retractable positive pickup fingers
on one elevator. At z=−20 mm, selected fingers enter a third side of the periodic
column shelf. A proposed long cam/key couples each finger's engagement to its
column selector bar, across the elevator travel. This is **80 real reusable
finger slides/head**, not a free selective platen. Groove, head bridge, cam,
keeper, support-plane bypass and travelling dock geometry remain unconstructed.

Process all cells of a visited row by signed height difference Δ, at most eight
nonzero groups (±10/20/30/40 mm):

1. Keep the row comb seated. Withdraw only column bars for the current Δ group;
   engage/prove their head fingers and the arrested lift at the common datum.
2. Withdraw the row comb. Unselected columns retain their column-comb path;
   selected columns now sit on the positive fingers, with shelf height
   `h_i(u)=old_i+u`, u from 0 to Δ. Other rows keep their row supports throughout.
3. At the discrete target, insert/prove the row comb before withdrawing fingers.
   Restore column supports; return the empty lift to its datum. Then write the
   next subset. Unchanged columns are never deliberately raised or reset.

The common datum works arithmetically because shelves repeat every 10 mm. With
row/column/pickup planes 0/−10/−20 and 40-mm travel, **seven shelf levels** per
column cover all parked acquisition states (local z=−60…0). This does not prove
that finite forks and combs can pass each other or carry load at pitch.

The executable checks all **15,625 three-column old/new combinations**, plus an
80-cell row containing all eight signed differences. Ground-support flags and
the affine supported path preserve unchanged heights and monotonic changed
heights. Endpoint/midpoint checks accompany the affine argument; this is not
contact dynamics. Three injected missing capture/arrest/row-seat proofs inhibit
release of the last assumed load path. Logical proof flags are specifications,
not constructed sensing.

Power loss requires the common elevator's arrested load path and selectors
remaining in their commanded state. Spring-closing a comb during transit could
collide with a moving column; it is not automatically safe. Apply E-218's
proposed two-dog/1-mm-step shared arrest as a slower schedule comparator, with
unqualified catch impact and ≤1-mm geometrical descent. Before row-seat proof,
retain head support; after proof, stop on grounded combs. A bad group read may
be retried while the row remains supported. A jammed column, false proof,
broken tooth or unsupported pickup requires a safe stop, not a claimed <30-s repair.

## Addressing lower bound and complete-map schedule

Even grant a whole-board head able to move any freed rectangle without new
local mechanisms. Starting all at zero, raise only the 80 diagonal cells to
40 mm. A safe release rectangle containing two diagonal cells also contains
unchanged off-diagonal cells with neither resident support. Without another
independently retained backing, each transaction covers at most one diagonal
cell. Enumeration checks n=2…5; the two-cell argument proves all n.

For the **fixed-datum, lift-then-empty-return implementation**, at assumed
v=200 mm/s and a=8,000 mm/s², t(40)=.225 s: **80×2t(40)=36 s**, before any
switching, registration, proof or preparation. This is a scoped bound; moving
acquisition datums, multiple lifts or additional independent support change it.
The permission to move unchanged cells is not used as an escape.

The explicit row head supports arbitrary subsets within one row, avoiding the
rectangle restriction by visiting rows sequentially. Worst-useful rows contain
all eight Δ groups: 200 mm loaded motion plus 200 mm empty return per row.
Banks B independently serve contiguous rows and require 80 independent column
selectors each. The favorable motion-only time is 2.4 s/row at a=8,000.

Model:
`T=2+(ceil(80/B)+1)[sumΔ(t_loaded(|Δ|)+t_empty(|Δ|))+8τ+t(5.08)]`.
The extra row charges one worst-row retry on the critical bank. Two seconds
cover digital preparation, common homing/readback/settling. τ=.1/.25/.5/1 s
is an **unverified total group allowance** for physical subset writing, column
bar/finger motions, row withdrawal/reseat, engagement readback and proof. No
offline pattern preparation or overlapping motions are credited. Indexed arrest
charges t(1)+1 ms on every loaded millimetre; empty returns remain continuous.

| Arrest / acceleration | B | Group allowance | Column selectors | Calculated map time |
|---|---:|---:|---:|---:|
| Continuous relaxation /2,000 | 16 | .10 s | 1,280 | 28.799 s |
| Continuous relaxation /8,000 | 16 | .10 s | 1,280 | 21.502 s |
| Continuous relaxation /8,000 | 16 | .25 s | 1,280 | 28.702 s |
| Indexed /8,000 | 16 | .25 s | 1,280 | 49.535 s |
| Indexed /8,000 | 40 | .25 s | 3,200 | 25.768 s |

Grid B=1/2/4/5/8/10/16/20/40/80, a=2,000/8,000, τ=.1/.25/.5. Minimum B is
16 even for the fastest sampled case; this is not a universal optimizer result.
At B=16/fast, τ=.1/.25/.5/1 gives 21.502/28.702/40.702/64.702 s. The .25 case
has only .0270 s/group additional slack. Continuous arrest remains unbuilt.
A five-row patch in one bank can consume the full critical path if it contains
all deltas; one changed cell needs only its one group. Other banks remain parked.

## Replication, manufacturing, cost and service

Counts for B=16, five rows/bank. Common parts still repeat functional contacts.

| Function | Cell / row | Bank / shared head | Board |
|---|---|---|---|
| Columns / lateral guide stations | 1/2; 80/160 | 400/800 | 6,400 /12,800 |
| Resident positive bearing sites | 2; 160 | 800 | 12,800 |
| Column shelf levels | 7; 560 | 2,800 | 44,800; three interface regions/level, not extra pieces |
| Row comb axes / keepers | 1 per row | 5 each | 80 each |
| Column comb axes / keepers | shared over five cells | 80 each | 1,280 each |
| Reusable finger slides / command couplings | 80 at active row | 80 each/head | 1,280 each |
| Elevator / arrest / row carriage | shared | 1 each/head | 16 each; ≥32 arrest-dog functions |

No individual column springs, inserts, sockets or separate moving lock are
prescribed. Yet every shelf, tooth, guide and finger must work; three shelf
interface regions imply 134,400 potential bearing regions, before opposite
groove walls. The 1,360 common support axes require guides, retention and access;
80B is a logical independently selectable-axis count, **not necessarily 80B
electric motors**. Mechanical multiplexing must include its own retained states
and write time; it cannot be assumed to meet τ.

At assumed $250 reserved for all other hardware, the $500 ceiling leaves
<$0.195 per 1,280-way selector, or <$0.078 at 3,200 ways; the $400 case leaves
<$0.117/$0.047. Allocations, not prices. No complete affordable BOM is supplied.
The reserve owes lifts, arrests, head carriages, readers, row drives, frame,
fasteners, power and wiring. A cheap common actuator is not 1,280 free clutches.

Illustrative 4×4×80-mm column blanks are **8.192 L**, before groove subtraction,
caps or routing changes. Two full 406.4-mm-square, 2-mm-thick support-plane blanks
add .661 L before apertures, segmentation, ribs and slides. At assumed effective
extrusion 5–15 mm³/s, column blanks alone take **455–152 h**; 10% scrap multiplies
by 1/.9. These are stock/time sensitivities, not sliced CAD. Five seconds to
insert each column adds 8.89 h; ten seconds per 1,360 support-axis placement adds
3.78 h, before 1,280 finger assemblies, keeper setup and proof. 406.4-mm row parts
need joints on the 256-mm bed. Orientations, shelf roots, tall-column straightness,
support removal and actual print/rework time remain unknown.

E-216's **assumed coherent combined errors** e=.15/.35/.70 mm give .85/.65/.30 mm
insertion margin for a 4-mm groove/2-mm blade (1-mm nominal half-gap). A proposed
1-mm bearing land has the same overlap bounds before deflection/debris; its area
and root strength are not constructed. Opposing support-height errors permit up
to 2e=.30/.70/1.40 mm displacement when removing the higher redundant support.
Thus two positive supports do not establish undisturbed takeover. Row/column
warp gives correlated errors across 80/five cells respectively; no IID yield or
printer resolution is credited. Anisotropy, friction, roughness, wear and creep
could worsen both load capacity and seating.

At assumed cell loads 1/3.27/10 N, a fully selected row needs 80/261.6/800 N
on its head, and ideal .8/2.616/8 N·m at 10-mm drive radius. Each support path
must carry full load. Gravity following remains E-218's unresolved issue: a
3-g unloaded column accelerating downward at 8 m/s² leaves only .00543 N against
guide drag. Capturing both groove faces could force descent but introduces
backlash and impact; it is a changed finite pickup, not an assumed cure.
Broken row combs affect 80 cells; column-segment faults affect five; head outages
affect 400. Redundancy allows stopped service only after proving the surviving
path and its load capacity. Replacing a buried comb still needs supported access.

## Decision and next discriminator

This materially changes the resident topology: individual release mechanisms,
old-code media, friction grips and cassette duplication disappear. They are
replaced by two support paths, seven shelf levels, 1,360 retained common axes
and 1,280 shared fingers in the favorable banked case. That is not yet a simpler
complete machine. **Stop this row/delta embodiment before fork, shelf, cam or
return optimization.** Reopen only with a concrete supported writer/addressing
topology that removes the bank-selector multiplication or eight-group motion
without releasing unchanged neighbors.

Next architecture work should test whether a continuous spatial programmer can
set absolute height in one supported visit with a small shared command set,
instead of duplicating a parallel 80-way program across every fast bank. First
construct where independent state resides during the visit and source loss;
then charge write/reset/read/feed at >213 finished cells/s. E-084's buffer-rate
failure remains a control. No print is justified by this conditional replay.
