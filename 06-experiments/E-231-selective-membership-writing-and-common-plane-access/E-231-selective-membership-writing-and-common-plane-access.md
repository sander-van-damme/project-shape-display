---
status: complete
builds-on: [E-230, E-229, E-220]
---

# Selective writing preserves support but does not rescue the common-plane machine

**Park the tested live-membership implementations.** A stopped selective writer
can preserve continuing members, but its cheapest sampled <30-s case degenerates
to 80 gates/head: eight heads, 640 gates, 26.439 s, **$687.80 assumed bought
allocation**. A physical write matrix reduces wires, not retained output actuators;
its optimistic $563.50 case still needs 400 actuators. Do not refine fingers,
keepers, cam lands or coils. No printing is justified.

Input main `57e6d4a`. Run `python3 tools/curated-experiment-checks/E-231/screen.py`.
Evidence: **architecture hypotheses, ideal finite-state replay, routing inequalities
and scenario calculations; self-review**. No CAD, sourced prices, calibrated
process distributions, measurements or physical qualification. All non-product
numbers below are explicitly unqualified assumptions. Five 10-mm heights remain
a comparison workload, not a product resolution decision.

## Physical overwrite and output coupling

The required retained output has three configurations: G = column bar engaged /
pickup retracted; O = both engaged; M = bar withdrawn / pickup engaged. Admission
must follow G→O→M; retirement M→O→G. A stopped common lift supplies the frame
reference. Only the addressed channel moves; continuing members stay in M.
Positive endpoint backing must carry withdrawal reaction without electrical power.
A digital bit is neither that backing nor a support contact.

| Construction | Actual writing and output hypothesis | Consequence |
|---|---|---|
| Direct control | 80 retained command actuators/head; common phase motions insert/prove incoming output, then withdraw outgoing output through two links/channel | E-230 comparator; physical links, stable overlap and arrest remain owed |
| Stopped selective mechanical scanner | q retractable gates engage q three-position output yokes at a stopped group. Common ram drives selected yokes to O, proves incoming contact, then reaches the opposite endpoint. Gate retracts before group indexing. Untargeted yokes remain positively backed. Reverse sequence retires members; there is **no erase shoe** | Three retained configurations/yoke, two load-output links, a writer engagement face and guide per channel; q select gates plus scanner translation. A 40-mm sliding-key connection to fixed column bars is required if the writer rides the lift |
| Electrically addressed physical matrix | q column lines × 80/q group lines select three-position polarized electromagnetic output actuators. Two controlled strokes with overlap proof drive G↔M; mechanical stops retain O and endpoints | Still 80 actuators/head, with coils, armatures, three retention positions and two output links. Bidirectional isolation is required: an unisolated 2×2 network has a three-coil sneak path at V/3 per coil. Half-selection immunity is granted for timing, not established |
| Erase-all spare load register | Second full set of load fingers takes over every continuing member before first set is erased. Then rewrite first set and transfer back. An unpowered mask copy alone cannot carry this load | At least 160 fingers/head, duplicated load routing and ≥two extra transfer stages/level. At B6 this adds ≥480 fingers and ≥480 links, plus .692456 s/row even granting free copying. Reject before detailed scheduling: private support duplication restores the burden we set out to remove |

Local scanner engagement and matrix isolation must preserve unaddressed yokes.
Endpoint backing, overlap retention and 40-mm sliding keys remain unconstructed;
no friction, fatigue, creep or source-loss performance is established.

Replay covers **15,625 three-cell old/new maps**, checks each individual support
transition and unchanged height, and exposes erase-all loss of the last support.
An additional **6,250 partial two-cell retries** seats members at their actual
intermediate plane, releases pickups, and regenerates the next transaction from
observed heights. All planes are ideal discrete stops. Broken contacts, jams,
off-grid stops, missed observations and moving impacts are outside this replay.

## Common-plane access is a physical routing obligation

One possible causal envelope uses an 80-mm column with its unique bottom at
z=h−80 mm. Row and column combs act at z=0 and −10, with stationary guide
stations at 0 and −20. At h=40 the bottom is −40: it still spans both guides.
The pickup plane moves −80→−40→−80 and admits only the selected bottom foot at
its actual height. This avoids confusing periodic shelves with the unique foot;
it also avoids vertical intersection with the resident comb planes.

A solid plate would hit unchanged low columns. Retractable fingers must emerge
from clear passages alongside their stems, with a support spine below the feet
and a 40-mm route to the fixed column-bar outputs. During row feed all fingers
must be withdrawn and the head lowered another 2 mm to −82; raise it again
before the next row. The schedule now charges both strokes. 

**Finite envelope screen:** a 4-mm stem at 5.08-mm pitch leaves a 1.08-mm interrow
passage. A centered 1-mm side blade leaves only `.04−e` mm one-sided margin;
all combined e=.15/.35/.70-mm scenarios fail. Even a .5-mm blade leaves
`.29−e` = .14/−.06/−.41 mm. These are opposing part/alignment error bounds,
not X1C distributions. No universal impossibility follows: a narrower lower
stem, separated lower pitch or a different pickup path changes the geometry,
but each owes column stability, top clearance, guides and fabrication at 6,400
copies. Do not refine thin fingers to rescue this screened machine.

A stopped 4-mm writer window/2-mm nose instead has `1−e`=.85/.65/.30-mm
nominal margin. Thus writer registration is not the only or smallest margin.
The 2-mm underpass allowance has `2−2e`=1.70/1.30/.60 mm before sag/debris;
opposing resident/pickup height errors can cause 2e=.30/.70/1.40-mm settling.
Common warp, frame phase, shaft twist and batch bias can affect a whole head;
no independent-cell yield or probability is assigned. A 256-mm printer requires
joined/tiled 406.4-mm rows, adding shared alignment uncertainty.

## Complete update, reading and recovery

Use E-230's v=200 mm/s, a=8,000 mm/s², and
`J=t(2 mm)+.003 s=.034622777 s` for a physical contact stroke and proof.
Let n=80/q. Per-level writing **including output transitions** is:

- direct: 3J (command, incoming output, outgoing output);
- scanner: `4nJ+(n−1)t(5.08)+t((n−1)5.08)` (select, two outputs,
  deselect; group travel and full return);
- matrix: `n(2J+.003)` (two output strokes plus group commutation).

These are sequential constructions, not universal lower bounds. Ten level
visits are charged, including both actions at 40; eight loaded 10-mm moves,
row-comb withdrawal/reseat, two underpass strokes, row feed and two .010-s
height reads give `C=8t(10)+10W+2J+2t(2)+t(5.08)+.020`.
The scanner uses a fixed raster; a second calculation grants **free traversal
and skips all empty groups**. A valid adversarial row assigns successive old
levels and target=(old+1) mod 5 within every group. It needs
`min(160,800/q)` selected group transitions/row. Even this free-travel screen
chooses B8/q80/$687.80, so empty raster visits do not explain the cost ranking.

At a recoverable fault, keep the current bank arrested; read actual heights,
seat all active columns on resident bars at the discrete plane, prove, withdraw
pickups, reset empty from up to 40 mm, then recompute and physically write a new
transaction. Charge `R=.010+W+t(40)` (the same physical writer must retire all
remaining members), **then** a full retry cycle. Direct R=.338868 s.
`T=2+(ceil(80/B)+1)C+R`. This is one causal retry, never a prefetched pattern.
Two seconds cover ingestion, registration and final settling.
If a contact cannot be proved or a column is off-grid, stop for service; this
formula makes no <30-s repair claim. A single bank retry may hold the whole
shared drive cohort stopped while other rows remain supported.

| Lowest allocation meeting timing in sampled grid | B/q | Physical actuators | Retained outputs / links | Map seconds | Bought allocation |
|---|---:|---:|---:|---:|---:|
| Direct control | 6/80 | 480 | 480 / 960 | 29.962 | $564.60 |
| Selective writer, including q80 limit | 8/80 | 640 | 640 / 1,280 | 26.439 | $687.80 |
| Actual multiplexed scanner, q<80 | 20/40 | 800 | 1,600 / 3,200 | 25.516 | $1,027.00 |
| Physical matrix, including one-group limit | 5/80 | 400 | 400 / 800 | 28.238 | $563.50 |
| Actual multiplexed matrix, q<80 | 8/40 | 640 | 640 / 1,280 | 27.105 | $753.40 |

Grid B=1…80, q=1/2/4/5/8/10/16/20/40/80. E-230 itself reproduces
B6/28.674933 s; underpass and causal grounding/reset raise it to 29.962484 s:
only **37.5 ms** remain for any additional map overhead. At loaded acceleration
2,000 mm/s² the best direct/scanner/matrix allocations become
$687.80/$749.40/$710.90. No option meets the bought target under these assumptions.
Both optima abandon multiplexing.

Bank enables must retain idle row combs, column supports and disabled pickup
states while common shafts move; loaded phases require local lift arrest.
Bank feed couplings engage only after row-seat proof, then advance one pitch.
An idle bank cannot silently seek arbitrary rows independently. Sparse requests
may require no-op feed traversal; the full-map bound remains applicable. A
five-row patch within one bank calculates direct/scanner/matrix
13.388/15.500/11.459 s, including retry. These are contiguous-patch examples.
All changed columns still visit 40 mm: a 0↔10 change detours 30 mm above both
endpoints. Nonmembers remain supported ideally; touching miniatures, bridged
loads and settling at redundant supports prevent a physical isolation claim.

Reader coverage must include every selected yoke's incoming **and outgoing**
output, 80 actual column heights before and after the row, bank enable/feed
position, common plane, and row-comb seating across all 80 contacts. Proposed
per-bank camera/folded-light paths are unconstructed; endpoint flags cannot
prove load-bearing contact. Ten ×80×80 =64,000 membership observations/map
alone give a union bound .064 at an **assumed** per-observation undetected rate
10⁻⁶, before retries/output reads. Correlated occlusion or calibration error
invalidates an independence interpretation. The .003/.010-s proofs are grants.

## Replication, force, fabrication and bought hardware

Resident hardware is unchanged from E-230: per cell one moving column, two
guide/wear stations, seven shelf levels and two resident support sites; per row
80 columns, 160 guides/support sites, 560 shelves and one comb/keeper axis.
Board totals: 6,400 columns, 12,800 guides and support sites, 44,800 shelf levels,
80 row axes/keepers. The unique foot adds 6,400 pickup bearing regions.

At B8, each bank has ten rows/800 cells. Each head adds 80 column bars/keepers,
80 pickup slides, 80 retained three-state yokes, 160 links including 80 moving-z
interfaces, 80 writer gates in the fastest scanner, one lift/arrest/carriage and
one feed enable. Board: 640 each bars/pickups/yokes/gates, 1,280 links and
1,920 yoke retention positions. Each slide/link needs at least two locating
bearing regions; exact bearings, springs, sockets, inserts and mounting fasteners
are **unselected**, not zero. Matrix swaps gates for coils/armatures/isolation;
spare-load-register copying adds at least another 80 pickups/head. Every
additional overlap stop must retain power-loss state, not merely indicate it.

Common brake failure or transmission fracture downstream requires bank-local
arrest. At 640 loaded cells, E-230's assumed f=3.27 N/cell, .003-kg column,
.5-kg head and 20% guide drag give 5.92-kg moving hardware mass, **2.598 kN**
peak force, **25.98 N·m** at 10-mm output radius, **742 W** input at .7 efficiency.
These omit any added writer mass: each extra kg adds 17.81 N at 8 m/s².
A 400-mm end-loaded 12-mm shaft with assumed G=80 GPa twists .638-mm
height-equivalent; d20 gives .083 mm. This coherently shifts all pickups on a
bank and consumes contact timing/clearance margin. Neither shaft nor brake is
qualified. Arrest capture distance and energy, backlash and impact are unknown.

For the all-0→10 workload, pooling at 40 requires **837.12 J** gross upward
payload work versus 209.28 J for direct positioning; descent must dissipate or
recover the difference. Empty 3-g columns following downward acceleration 8 m/s²
allow only **.00543 N** guide drag before losing contact; at 2 m/s², .02343 N.
Hanging columns defeat pickup contact; captive pull-down changes the interfaces. Scanner yoke
resistance R=.3/1/3 N with q80/B8 gives 192/640/1,920 N common write force
before link friction or load-induced binding. Physical coils must supply this
work too; selecting a cheap electronic line does not supply mechanical energy.

Complete category **allocations, not quotations or established cost floors**:
controller/power/frame/wiring/spares-freight $15/20/25/15/10; shared
lift-driver/brake/phase/feed/writer/shafts-bearings $30/10/10/10/20/30.
Base $195. Per bank reader/enable/local arrest/mounts-guides $10/3/3/4;
retention hardware $.02 per output. Direct/scanner complete channels $.50 each.
Matrix three-state actuator $.50 each, bidirectional line drivers $.10 per
(q+n) line/head, isolation $.05 per output. No actuation, power, thermal,
reader or arrest rating substantiates these optimistic allocations. Printed
backing/links are assumed; any needed metal fasteners/springs must fit the
allocated categories or increase them.

At direct B6, nonchannel $324.60 leaves <$0.36542/channel under $500.
Scanner B8's $367.80 leaves <$0.20657/channel. Matrix B5's nonactuator $363.50
leaves <$0.34125 per physical actuator. Merely assuming cheaper channels is
not an escape; the force, three retained states and optical proof are still owed.

Column blanks remain 8.192 L (~228 h at assumed 10 mm³/s). Illustrative
20×4×3-mm yoke blanks add .154 L at B8; 40×4×3-mm link blanks add .614 L,
~21.3 h combined before gates, bar stock, guides, shelves, frame and supports.
Stock envelopes, not CAD/slicing. Ten-percent scrap multiplies by 1/.9;
module-registration faults correlate reprints. Print orientation is unqualified.
At ten seconds each, 3,840 bar/pickup/yoke/link/gate placements add 10.67 h;
6,400 column insertions at five seconds add 8.89 h. Wiring, 1,920 retention
positions, fixtures and calibration are extra. A bar fault affects up to ten
cells, a head outage 800. Replace only after proving row support; inaccessible
buried bars require supported module removal. No tool-free service claim.

## Redirect the transaction

Safe selective overwrite is logically possible, but these implementations pay
for sequential live writing with more banks or hundreds of physical actuators.
A generous stopped-writer registration margin does not fix pickup access,
gravity following, loaded arrest or cost. This rejects the tested constructions only.

Next test a changed transaction: program **unloaded target stops before pickup**,
keep one changed-cell mask fixed throughout the stroke, let a rising plane
acquire bottoms passively, and let prepositioned target stops retire columns
geometrically during descent. Then reseat the row comb before removing the
stops. This replaces ten live membership writes with one unloaded target program
and one fixed mask, but owes real stop memory, separate pickup/stop access,
bar preparation/reset and retained support during row feed. Compare directly
against E-221's loaded shoes and E-226's unloaded-bar handling: do not silently
restore their independent axes, turnover/transport or fine locks. The next
screen must first decide whether these complete-machine obligations can be
cheaper; no new local mechanism campaign is authorized by this hypothesis.
