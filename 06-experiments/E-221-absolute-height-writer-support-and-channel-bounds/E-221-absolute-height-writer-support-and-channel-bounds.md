---
status: complete
builds-on: [E-084, E-220, E-219]
---

# Absolute-height writing exchanges delta groups for independently supported axes

**Park the narrow-window continuous writer; retain a stopped row head only as
an architecture-level cost/arrest comparator.** One supported visit can remove
E-220's eight delta groups and crossed selectors, but it does not remove
independent load-bearing state. In the favorable timing scenario a stopped
head needs 240 driven/arrested axes across three banks; continuous passage
needs 640 across eight. A shared sweep instead restores 6,400 resident catches.
None earns local contact development or printing.

Input main `48b75b5`. Reproduce:
`python3 tools/curated-experiment-checks/E-221/writer.py` (stdlib, stdout only).
Evidence: **mechanism hypotheses, exact ideal state replay and necessary-condition
calculations using explicitly assumed bounds**. Self-review; no constructed
assembly, process distributions, vendor quotations or physical measurements.
Five 0/10/20/30/40-mm heights are a comparator, not a resolution decision.

## Three spatial programmers and where memory lives

| Construction | Load path and independent memory | First decision |
|---|---|---|
| Travelling shaped backing, no resident retention | Column → passing profile → frame only during contact | Reject: after departure all freely sliding columns return to bottom. A circulating pre-shaped carrier must stay resident or transfer to another memory; its preparation is not free |
| Common rising/descending platen, timed resident catches | Parked column shelf → individual catch → frame; during movement foot → common arrested platen → frame | Ideal one-visit absolute write works, but restores 6,400 moving catches, 32,000 shelf positions and 80 real release/hold gates per head. Stop before catch design: no demonstrated system advantage pays for repeated locks |
| Independently positioned bottom shoes with one row keeper | Parked shelf → common row comb → frame; during visit foot → independently arrested shoe axis → head/frame | Removes resident moving catches, crossed column bars and delta groups. Conditional timing improves; real per-shoe drives, arrests, sensing and routing remain the deciding burden |

The sweep first rises from below all feet to 40 mm. Release each **changed**
column's catch only when the platen contacts its old bottom height. At the top,
all changed columns are at 40; on descent, close each catch at its target before
platen departure. Unchanged catches never open. The executable checks all
15,625 three-column old/new combinations. These are ideal point engagements,
not a finite time/contact proof. Removing selective catches and lifting a whole
row `(0,40,20)→(40,0,20)` displaces its unchanged 20-mm column by 20 mm.
Thus this construction needs independent release and deposit support, not just
one universal ramp. Changed columns may temporarily overshoot their target.

A sweep gate must perform old-height release, retained-open traversal,
target-height seating proof and reset/bypass. Loss of drive requires both
common-lift arrest and stable gate state; spring closure into moving shelves is
not established safe. Eighty reusable holds/arrests or 6,400 local bistable
functions must be paid for. This fails the repeated-complexity priority before
fine geometry or a timing optimization is warranted. It does not prohibit all
common-sweep topologies.

## One supported row visit without individual resident locks

Proposed stopped head: 80 independently vertical shoes beneath column bottoms,
45-mm shoe stroke from −5 to 40 mm. A fixed grounded row comb seats in one of
five periodic column shelves. The comb is positively kept when the head is
absent; the head docks to operate it. No crossed column selector is needed.

1. With the row comb seated, command all shoes from −5 to the **old absolute
   heights**, acquire/prove contact and each axis's independent arrested path.
2. Withdraw the common row comb only after every shoe is supported. Move each
   shoe directly from old to target; unchanged shoes stay at their acquired
   height. Load path is through the arrested axes and head rail/frame.
3. Insert/prove the common row comb at target heights, read actual column
   heights, then lower every empty shoe to −5. Feed/index the head one row and
   repeat; skipped rows remain on their combs. No prepared physical map.

Resident memory is column position held on the comb. During the visit it is
80 independent shoe positions. A single motor/common shaft cannot hold these
arbitrary values without 80 actual transmissions and independent disengagement/
retention functions. Calling those clutches a shared drive does not remove them.
All 80 shoes are used when any cell in the row changes; row handoff is a real
within-row disturbance exposure. Other rows keep their load paths.

Replay enumerates 15,625 three-cell transitions. Between old and target,
`h_i(u)=old_i+(target_i-old_i)u`; the grounded shoe stays in contact in the ideal
following model. Constant unchanged heights follow algebraically, not just from
sampling. Missing acquisition or arrest proof inhibits comb release; missing
comb-seat proof retains the shoes. No independent reviewer or physical reader
is implied by these logical flags. A hung column is a detected safe stop, not
successful downward placement.

**Source loss is not supplied by a powered servo.** The fast case grants an
unbuilt zero-motion brake per shoe. The slower comparator gives each shoe two
positive arrest functions, 1-mm loaded increments and 1-ms proof per increment,
as in E-219/E-220. At least one arrest must remain grounded during transfer;
≤1-mm geometrical catch descent is not a qualified impact limit. Comb and dock
state must also remain mechanically retained. A failed reader, broken support
or jam does not receive an invented <30-s recovery. One detected full-row retry
is budgeted; failed deposit holds the row on its arrested head for service.

## Full-map time, continuous dwell and physical transactions

Assume v=200 mm/s, a=2,000 or 8,000 mm/s². Rest-to-rest motion is
`t(d)=2√(d/a)` below v²/a, otherwise d/v+v/a. A mixed row containing both
0→40 and 40→0 attains all three sequential maxima: acquire 45 mm, rewrite
40 mm, clear 45 mm. No sum of incompatible worst cases is used.

Per-row service `S=2t(45)+L(40)+u`; L=t for ideal continuous arrest, or
`40[t(1)+.001]` for indexed loaded motion. Assumed u=.10/.25/.50 s covers
command distribution, contact/height read, comb withdraw/reseat and proof.
Two global seconds cover map processing, initial registration and final settle/
verification; these are **unqualified allocations**, not measured overheads.
All per-map homing/reset must fit them. Shoes get **12,800 old/target commands**,
6,400 acquisition proofs and 6,400 target checks; 80 comb withdrawals and
reseatings; 6,400 empty returns; feed per visited row plus one full retry.
Sensors may multiplex, but coverage, occlusion and their time are not solved.
Buffers cannot reduce sustained physical production, as E-084 established.

For B disjoint banks the stopped schedule is
`T=2+(ceil(80/B)+1)[S+t(5.08)]`, including one retried row in the critical bank.
For continuous passage grant a non-overlapping **effective contact window**
w=2 mm: all acquisition, writing and clearing must fit `w/v_feed≥S`.
Thus pitch time τ≥5.08S/w. Charge
`T≥2+(ceil(80/B)+2)τ+v_feed/a`: an entry/exit pitch, one retry interval and
acceleration ramps. This deliberately grants retry without reversal and omits
unconstructed docking details; a pass is optimistic. A long contact footprint cannot be credited without routing contacts past
neighboring rows or adding independently retained pipelined head state.

| Arrest / a / u | Stopped B × 80 axes / s | Continuous 2-mm B × 80 axes / s |
|---|---:|---:|
| Ideal / 8,000 / .10 | 3 × 80 = 240 / 26.511 | 8 × 80 = 640 / 27.146 |
| Ideal / 2,000 / .10 | 4 × 80 = 320 / 26.167 | 10 × 80 = 800 / 28.671 |
| Ideal / 8,000 / .25 | 4 × 80 = 320 / 23.533 | 9 × 80 = 720 / 29.242 |
| Indexed / 8,000 / .10 | 5 × 80 = 400 / 28.942 | 16 × 80 = 1,280 / 29.282 |
| Indexed / 8,000 / .25 | 6 × 80 = 480 / 28.022 | 20 × 80 = 1,600 / 27.671 |

Enumerate B=1…80, both arrests, both accelerations and all three overheads;
strictly <30 s. A three-bank fast stopped head rises to 30.711 s at u=.25 and
37.711 s at u=.50. Fast continuous w=1/2/4 mm needs B=20/8/4 respectively;
4 mm is a changed contact geometry with little pitch separation, not free dwell.
A tall/overlapping moving profile also still needs resident retention after exit.

Regional time follows `2+(max changed rows in any bank+1)×row cycle`, with actual
seek travel added. Worst concentration of 27 changed rows in one three-bank
machine takes full-map time. Even one changed cell invokes all 80 shoe pickups
in that row. Ideal unchanged heights hold, but real row disturbance is unqualified.

## Whole-machine burden, manufacturing and affordable channels

For the favorable **stopped B=3** hypothesis (banks of 27/27/26 rows):

| Function | Cell | Row | Largest bank / head | Board |
|---|---:|---:|---:|---:|
| Moving columns / two guide stations | 1 / 2 | 80 / 160 | 2,160 / 4,320 | 6,400 / 12,800 |
| Shelf positions / comb bearing contacts | 5 / 1 | 400 / 80 | 10,800 / 2,160 | 32,000 / 6,400 |
| Resident row comb / keeper / frame seat | shared | 1 each | 27 each | 80 each |
| Reusable shoe axes / drive transmissions | shared | 80 during visit | 80 each | 240 each |
| Shoe guide-bearing stations / foot contacts | shared | 160 / 80 active | 160 / 80 | 480 / 240 |
| Ideal brakes OR indexed arrest functions | shared | 80 OR ≥160 active | 80 OR ≥160 | 240 OR ≥480 |

Indexed fast timing actually needs B=5 or more, so ≥800 arrest functions there.
Add one transport/retained docking system, row-comb operator and reader assembly
per head, with per-axis contact and arrest proof coverage. Every drive includes
motor or clutch, linkage, mounts and wiring; none is absorbed into a free head.
No resident springs/inserts/individual sockets are specified; head brake springs,
bearings, fixtures and fasteners are **unknown**, not zero. Column assembly still
requires 6,400 insertions; head assembly ≥240 axis placements and calibrations;
80 retained-comb assemblies. Buried guides and comb failures require support
before access; a head outage affects up to 2,160 cells, while comb failure affects
80. Module joints are needed across 406.4 mm on the 256-mm bed.

A carried-forward simple-column stock allowance of 4.608 L gives 256–85 h at
assumed effective 5–15 mm³/s extrusion, before shelves, guides, frame, heads,
supports and scrap. Ten percent scrap multiplies material/time by 1/.9.
Unconstructed head/comb volume and print orientation prevent a total print-time
claim. Shelves, layer strength, tall-part warp, installation access and alignment
remain manufacturing obligations.

Use **bounded combined errors**, not fabricated X1C statistics: e=.15/.35/.70 mm.
The E-220 4-mm groove/2-mm blade scenario leaves 1−e=.85/.65/.30 mm half-gap.
Assuming a 2-mm foot fully supported on a 3.4-mm shoe, lateral margin .7−e is
.55/.35/0 mm. Neither is finite routed CAD. Opposed comb/head vertical errors
permit 2e=.30/.70/1.40 mm takeover movement; calibrating each shoe adds work and
may still miss load-dependent head deflection. Shared head sag, row warp and
print-batch bias correlate whole rows/banks; no IID cell-yield claim is made.
Sliding contact during continuous passage adds wear and lateral force absent
from the stationary shoe comparator. Roughness, creep, debris and anisotropy
remain outside these boxes.

At assumed 1/3.27/10 N per cell, one loaded head carries 80/261.6/800 N; a 40-mm
full-row rise needs 3.2/10.464/32 J ideal work. Individual axes need .01/.0327/.1
N·m at 10-mm ideal drive radius, before friction/inertia/transmission loss.
Gravity following is still unproved: a 3-g column at 8 m/s² downward acceleration
leaves only .00543 N for guide drag. A captive bidirectional shoe would add
capture/release interfaces and timing; it is not silently included.

An **assumed $250 non-axis reserve** leaves less than $1.042 per 240-axis channel
under $500, or $.625 under $400. At 400 indexed channels the caps are $.625/$.375;
at 640 continuous channels $.391/$.234. They must buy drive, transmission,
arrest, sensing share, wiring and mounts. Reserve owes all row mechanisms,
transports, power and frame hardware. These are allocation bounds, **not quotes
or proof of economic impossibility**. No procurement or cost acceptance follows.

## Architecture decision

E-220's favorable embodiment needed 1,280 selectors and 1,280 pickup fingers;
E-219 needed 640–1,280 handlers plus 38,320 sorted blocks or 7,680 indexed wheels.
The stopped absolute head reduces shared functional counts and removes duplicate
media, crossed selectors and resident individual moving locks. It does so by
making 240–480 shared axes independently load-bearing, depending on unqualified
arrest and overhead assumptions. This is a useful architecture distinction,
not evidence that hundreds of complete channels fit the budget.

**Stop continuous 2-mm development**: it multiplies channels relative to stopping
and adds sliding contact without a demonstrated product benefit. **Stop the
resident-catch sweep** before repeating local lock optimization. **Keep the
stopped head as a quantitative control, not a selected architecture**. Reopening
requires a concrete low-cost shared transmission/positive retention scheme
accounting for every independent axis and supported arbitrary old/target pair;
or a different broad load path that eliminates these functions. The next useful
screen is that channel mechanism and a complete bought/printed allocation,
compared with a genuinely different support topology. Do not optimize shoes,
shelves or brakes in isolation and do not print from this result.
