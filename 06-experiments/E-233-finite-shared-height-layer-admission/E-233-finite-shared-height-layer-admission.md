---
status: complete
builds-on: [E-232, E-231]
---

# Shared layers cannot merge finite feet through an occupied bearing section

**Park the tested common-layer admission mechanisms.** A shared ramp does not
repair E-232's finite shelf obstruction: while lowering an upper foot toward the
pickup, its bearing section enters a lower foot in another cell. Rigid layer
translation preserves the problem or moves unchanged columns. A nonuniform
five-level shutter control escapes it logically, but restores **32,000 resident
moving shutters** and needs **560 shared writer channels / $771.20 assumed bought
allocation / 27.687 s** in the screened schedule. No CAD, latch refinement or print.

Input main `7c812c5`. Reproduce with
`python tools/curated-experiment-checks/E-233/screen.py` (stdlib, stdout only).
Evidence: **architecture hypotheses, finite-envelope calculations, ideal state
replay and allocation scenarios; self-review**. No prices, calibrated
process distributions or physical measurements. Non-product inputs are assumptions.
Five 10-mm heights are a comparison workload, not a resolution decision.

## Finite supported crossing

Use identical vertically guided rectangular feet, thickness f, and a row shelf
of thickness t whose bearing section is identical at every selected column.
The pickup supports a lower foot on lane A; shelf support occupies lane B of
the same foot. Consider old heights `(0,10,20)` and targets `(10,0,20)` mm.
The first two join the pickup; the third must stay at 20.

At shelf level H, the lower foot occupies `[z,z+f]` and the shelf `[H-t,H]`.
First collision is `z=H-f-t`, but upper pickup contact needs `z=H`.
The upper column still lacks pickup support across **f+t** of travel. With f=t=2,
collision starts at z=6 for H=10, leaving a 4-mm unsupported transfer gap.
Early shelf withdrawal drops the upper column; keeping it blocks the lower one.

| Changed crossing | Explicit construction and finite result | Stop / scope |
|---|---|---|
| Retracting ramp | Hold lower feet on the arrested plane. Translate a ramp so upper feet descend continuously onto it. At relative upper height delta the still-bearing shelf section is `[delta-t,delta]`; lower foot is `[0,f]`. These intersect for `0<delta<f+t`. An interior witness is delta=f/2 | A homogeneous transverse ramp cannot finish the merge. Even vanishing ramp thickness leaves its top surface inside the lower foot for `0<delta<f`. Withdrawing its last bearing contact earlier loses support |
| Common moving layer/stack | Translate all occupied shelves by u while the pickup follows | A rigid stack preserves height separations. Moving an occupied unchanged layer moves its column by u. Moving only upper layers still meets the ramp/merge obstruction when their separation closes; early withdrawal needs another support path |
| Pickup approaching from above | Lower a finite flat shoe of thickness d into the bottom-bearing lane | Its underside first hits the foot top when shoe top is H+f+d, before the shoe can get below H. A hook/grip changes the load interface and requires capture/retention; a top pusher supplies no downward support |
| Sideways bypass | Shift feet outside the shelf projection, then return above it | A rigid whole-column shift moves the terrain top and interferes with neighbors. A separately translated foot needs a sliding/articulated interface per column or reusable independently positioned head outputs. No such routing is granted as a free common stroke |
| Nonuniform shelf apertures | Leave shelf material only at the actual old height of each cell, then rewrite to target at the apex | Escapes the shared-section premise. Complete ideal replay below; repeated moving-site and system-allocation stop |

Checks cover 16 f/t combinations (.5/1/2/4 mm), 100/1,000 ramp subdivisions and
an analytic interior witness. A point-foot/zero-thickness control removes the gap;
the analytic intersection establishes failure without discretization dependence.

This is **not a theorem against all layers or all foot shapes**. It applies to
fixed lateral projections with a finite rectangular bearing section shared at
the compared cells. Tapered feet, cell-dependent paths, tensile capture or distinct
support lanes can change the premise; each owes positive bearing area, load
capacity, finite manufacturing margins and a complete transfer. A sharp edge
with vanishing contact area is not a qualified escape. Additional old-height
axes, duplicate grips and local trips do not earn refinement here.

## A complete logical control, with expensive spatial state

Give every cell five independently retained shelf shutters, one at each height;
only the shelf at its present height is inserted. These are separate physical
outputs, not five free software masks. Column→foot→shutter→fixed row bed→frame
is the resident positive load path. Ground-height support is included; replacing
that layer with a base leaves 25,600 moving upper shutters and does not rescue
an otherwise unchanged allocation.

A head has 80 fixed changed-mask outputs and an arrested common pickup. Grant
separate pickup/shutter bearing lanes and collision-free head routing:

1. Read old heights, program/prove the fixed changed mask, insert fingers at
   z=-6 mm. Unchanged columns remain on their resident shutters.
2. Rise to 42 mm. Each changed foot leaves its own shelf; there is no shelf in
   that cell at any higher old level. Old shelves remain until all changed feet
   are supported at the apex. Higher and unchanged columns retain support.
3. Lock the pickup and membership mask. Reuse the 80 writer gates via a separate
   mode/output coupling to overwrite the five resident layers, one layer at a
   time, at changed cells only. Clear old bits and insert target bits while
   unloaded; unchanged outputs remain mechanically backed. Read all five layers.
4. Descend. Changed height follows `max(plane,target)`; a foot contacts its target
   shelf before pickup separation. Prove final support and read actual heights.
5. Lower to -6, withdraw fingers, feed one row and return. Resident shutters retain
   all heights while the head travels. A 6-mm underpass replaces the inherited
   2-mm allowance because the lowest shelf itself occupies space below zero.

The control checks **15,625 three-cell map pairs / 1,703,125 support states**,
including intermediate cleared shutters, invariant unchanged heights and finite
2-mm foot/2-mm shelf intersections. It also checks **6,250 two-cell stable wrong
stop/retry cases**: finish supported descent to actual discrete heights, read,
clear/reset, recompute from that actual state, then physically rewrite and retry.
No original delta is blindly replayed. This is a logical construction with
explicit geometry grants, not a finite three-dimensional machine.

All checks grant retained shutters, mask backing and a grounded pickup arrest.
Removing arrest produces a source-loss counterexample after pickup leaves an
old shelf. Bank-local arrest must cover downstream
drive failure. Arrest distance/energy and shutter strength/proof remain unconstructed. Missing shelves,
hung/off-grid columns, broken contacts and unreadable support require arrested
service, not a promised <30-s repair.

## Whole-machine burden and manufacturing bounds

| Functional item | Per cell / row | Per head or bank at B7 | Board |
|---|---|---|---|
| Moving columns / guide-wear stations | 1/2; 80/160 per row | Up to 960/1,920 per 12-row bank | 6,400/12,800 |
| Moving shutters / load lands / retained binary outputs | 5 each; 400 each per row | Up to 4,800 each | 32,000 each |
| Shutter guide-wear contacts | Assume 2/shutter; 10/cell | Up to 9,600 | 64,000 |
| Fixed row-layer backing strips | 5/row | Up to 60 | 400; at least 800 printed length modules on the 256-mm bed |
| Pickup slides / fixed mask states / writer gates | Shared | 80 each | 560 each |
| Mask-to-output links | Shared, at least 2/channel | At least 160 | At least 1,120; writer mode routing extra |
| Pickup / row-feed / layer-writer mechanisms | Shared | One each, with local enable/arrest | Seven each; common drives shared across banks |

B7 has three 12-row and four 11-row banks. Homogeneous shelves instead need
400 row-layer motions and 32,000 bearing sites before solving admission.

The control removes E-231's 44,800 periodic shelf levels and 80 row comb axes,
but adds 32,000 sliding/retention devices. Individual motors, springs, inserts or
sockets are not logically required; an all-printed retainer is unconstructed.
Stops, bearings, fasteners and reader paths remain unknown. A layer fault can
release 80 cells; a head/arrest fault affects up to 960. Buried five-layer guides
need module access with columns still on proved support.

For labelled dimensional/alignment bounds e=.15/.35/.70 mm (not X1C priors):

- f=t=2 with both thicknesses high by e gives gap 4+2e = 4.30/4.70/5.40 mm.
  A common vertical placement bias cancels from the gap: it cannot rescue crossing.
- Two 2-mm foot bearing lanes with centered 1-mm noses leave `.5-e` =
  .35/.15/-.20 mm lateral margin. Pickup routing remains unconstructed;
  E-231's narrow inter-stem blade is not silently qualified.
- Apex insertion margin `2-2e` = 1.70/1.30/.60 mm. Underpass below a 2-mm shelf
  has `6-2-2e` = 3.70/3.30/2.60 mm. Opposing support-height errors can move a
  column by 2e = .30/.70/1.40 mm during takeover, before bending or debris.

Joined strips, batch bias, guide warp and drive twist correlate errors. These
are bounds, not probabilities. Friction, anisotropy, wear, creep and seating
remain unqualified; nominal margins do not justify nose/retainer refinement.

Illustrative 12×4×2-mm shutter stock totals 3.072 L; 80×4×4-mm column stock is
8.192 L. Their 11.264 L requires **313 h at assumed 10 mm³/s**, 348 h with 10%
scrap, excluding guides, beds and frames. These are stock volumes, not sliced
parts. Flat shutter printing favors layer-plane bearing but guide accuracy and
creep remain unknown. At assumed 10 s/shutter plus 5 s/column, placements alone
consume **97.8 h**, before 800 strip modules, head links, wiring and calibration.

## Charged programming, timing, force and economics

Assume v=200 mm/s, a=8,000 mm/s², rest-to-rest motion t(d), and
`J=t(2)+.003=.0346228 s` per physical throw/proof. The sampled indexed writer
visits all five layers; each write receives three J stages (select, output, clear).
A fixed mask copied into separate retained outputs stays loaded during gate reuse.
Common mode routing and selective overwrite at unchanged sites remain grants.

Row cycle `C=3J+2J+15J+[4t(10)+t(40)]+2t(42)+2J+2t(6)+t(5.08)+.020`
= **1.937101 s**: fixed mask, writer mode, five physical layer writes, writer
traverse/reset, pickup rise/descent, unloaded finger clearing, underpass, feed,
and old/final reads. No prewritten arbitrary pattern is excluded from the clock.

With two seconds for ingestion/registration/final settling, and one causal retry:
`T=2+(ceil(80/B)+1)C+R`, `R=t(42)+J+.010+t(40)`.
R conservatively allows supported completion/read and empty writer reset before
an entirely new row cycle. It is not prefetched recovery. Search B=1…80.

| Conditional control | Banks / writer channels | Seconds | Bought allocation |
|---|---:|---:|---:|
| Five resident shutter layers, a=8,000 | 7 / 560 | 27.687 | $771.20 |
| Same construction at B6 | 6 / 480 | 31.561 | $704.60 |
| Pickup a=2,000; writer unchanged | 7 / 560 | 29.712 | $771.20 |
| E-231 direct selective admission comparator | 6 / 480 | 29.962 | $564.60 |

Five contiguous changed rows in one bank calculate **14.127 s**, with retry;
seek remains unallocated, and sparse maps may require the full feed raster.
Changed 0↔10 cells visit 42, a 32-mm detour. Unchanged support is ideal only;
bridged miniature loads, vibration and physical isolation are not qualified.

Bought category **allocations, not quotes or cost floors**: inherited E-231 base
$195 covers controller/power/frame/wiring/spares and shared lift, brake, phase,
feed, writer, shafts/bearings. Per bank add reader/enable/arrest/mounts $10/3/3/4,
80 retained mask outputs at $.02 and 80 complete writer channels at $.50.
Add common layer-writer axis/brake $20/10, $5/bank local mounting/arrest, and
$.20 per 400 resident strip mounts. This is `305+66.6B`, even granting entirely
printed resident retention. At B7, $.005/$.02 bought hardware per shutter raises
allocation to **$931.20/$1,411.20**. Even free writer channels leave $491.20,
only $8.80 below the hard ceiling for any underallocated hardware. None is rated.

At assumed 1/3.27/10 N static load/cell, 3-g columns, .5-kg moving head/bank and
20% guide-force addition, B7 simultaneously moves 560 cells with peak force
.748/2.273/6.796 kN. Middle case needs **22.73 N·m at 10-mm output radius and
649 W peak input at .7 efficiency**. A 400-mm end-loaded shaft with assumed
G=80 GPa twists .558/.072 mm height-equivalent at diameter 12/20 mm. The $20
power allocation is not qualification of that duty. Shutter backing must hold
up to 261.6 N per fully occupied row layer at 3.27 N/cell, before impact.
All-0→10 upward work via 42 is 878.976 J versus 209.28 J direct. Gravity following
by a bare 3-g column permits only .00543 N guide drag at 8 m/s² downward
acceleration (.02343 N at 2); a captive pull-down adds interfaces not included.

Read coverage includes old/final heights, fixed mask, all five shutter layers,
writer position, bank enable and actual bearing/lock proof. At least 51,200 cell
observations/map precede retry. J's 3-ms proof and .010-s height reads are grants;
flags do not establish load bearing. At an assumed undetected rate 10⁻⁶ the
union bound is .0512; correlated occlusion/calibration prevents an independence
claim. No qualified optical path, dynamic arrest or error-detection coverage exists.

## Decision and reopening condition

Preserve the shared-section obstruction and the cost of its nonuniform escape.
Stop this embodiment before manufacturing details; this does not reject all
shared programming.

Redirect the next architecture screen away from merging loaded feet onto one
plane. Compare a **shared programmer acting on unloaded, captive height supports**
with a direct supported row head, first requiring a whole-machine route that
avoids E-227's travelling cassettes and E-221's independent loaded axes. Begin
with a concrete support-exchange/retention sequence and its repeated-site ledger;
reject a renamed bank of 6,400 precision catches or free media transport before
scheduling. Reopen shared layers only with a specified finite, load-bearing change
to the common-section premise and fewer total moving/critical sites than this
control. No target-memory optimization is justified while admission depends on
an oracle or on the stopped 32,000-shutter implementation.
