---
status: complete
builds-on: [E-257, D-011]
---

# Mid-travel relief depth and player-view comparison

**Carry 6.35-mm pitch, a 20-mm neutral plane and 40-mm travel into the next
playable comparison.** Keep meaningful walls, platforms and cliff edges physical;
offer visual water and removable cover objects. This is a research recommendation,
not an owner-approved policy or qualified machine. Reducing the assigned ravine
depth from 30 to 20 mm is a new representation hypothesis, not a mechanical repair.

D-011 separates sourced play conventions, five contextual map examples and unmeasured
preferences. E-254/E-257 retain the original geometry, A/B/C counts and pitch evidence.
Only their original three windows are timed here; the additional dungeon/cave examples
are qualitative checks. Evidence is deterministic geometry/scheduling and labelled
machine-wide uncertainty bounds; no new physical measurement or observed-play trial.

Reproduce `python 3 tools/curated-experiment-checks/E-258/player_view.py`.
`--figures DIR` additionally uses matplotlib to emit a three-page PDF and PNGs:
river and ravine A/B/C at both pitches, then physical depth and walls. All faces are
actual cell tops/risers at equal XYZ scale. A/B deliberately end in the **same shape**:
their difference is the starting surface and paid preparation. Dashed perimeters mark
start height, not support hardware; semantic colors do not establish working projection.
JSON includes all new arrays, signed counts, bank rows, turns, schedules and sequences.
No generated files or historical arrays are overwritten.

**Challenge 30-mm ravine depth, rather than automatically extending the mechanism.**
Common ordinary ground 20 gives river water 10/ground 20/rocks 30, ravine bottom 0/ground 20/
rocks 30, and ruins wall 40/slab 30. This retains a real depression and+20-mm walls in
0..40 travel. Compared with neutral 30/0..50 it deliberately compresses the ravine
drop 30→20; it is not a coordinate trick or proof of equal visual appeal. Other local
relief stays unchanged. Neutral 20 is halfway through travel, with real downward drive.

| Conditional seconds; prepared common ground | 80×80, N30 / N20 | 64×64, N30 / N20 |
|---|---:|---:|
| Minimum→neutral preparation, excluding unknown homing | 25.33 /21.23 | 21.58 /18.28 |
| Neutral→physical ravine | 25.33 /21.23 | 21.58 /18.28 |
| Nine-transition maximum, independent B2, mixed or both physical | 30.13 /26.03 | 25.38 /22.08 |
| Same maximum, mask B2, mixed | 37.92 /32.30 | 31.40 /26.90 |
| Same maximum, mask B2, both physical | 39.21 /33.59 | 32.61 /28.10 |
| Same maximum, mask B3, mixed | 27.96 /24.63 | 22.63 /20.09 |

The 20-mm case leaves ravine counts 1825/4408/167 (down/still/up) at 80 and 1166/2823/107
at 64 unchanged, still visiting 78/63 rows. Shorter row excursions—not fewer pins—save
4.10/3.30 seconds. This changes the shared-mask shortlist: **64×64/B2 can meet the
30-s physical-subsystem comparator with real depressions** under the assumed rates.
It no longer requires fully visual chasms or a third head in this scheduler.
Its $1023.92 allocation versus independent $953.92 still grants every complete channel
at $4. At 64, N20 mixed, four 16 heads take 47.72 s and the turning full-row schedule 38.25 s;
neither gets a free speed pass from coarse pitch.

Coherent machine-wide uncertainty bounds (not process priors) matter: at 64/N20/mixed,
1500 rather than 2000 loaded rpm gives independent 25.28/mask 30.18 s; acceleration 200
rather than 1000 rev/s² gives 26.48/35.08 s. Row proof 100 rather than 20 ms gives 24.72/
29.54 s; mask writing 50 rather than 10 ms gives mask 30.70 s. Each changes one input.
Thus independent B2 has the more forgiving sampled timing envelope; the mask is a
competitive conditional comparator, not a selected or qualified solution.

One global rotary bus is a distinct comparator. `bus_oracle` grants implemented
resident AND paths and zero travel/row-selection time, but charges dwell, proof,
signed-mask rewriting, retry and 4 s. Serial intersections and arbitrary subsets in
one selected row are emitted separately: mixed N20 maxima 802.37/50.28 s at 80 and
509.63/41.24 s at 64. These favorable schedules are scoped implementations, not lower
bounds for every possible bus program. Multirow arbitrary subsets still cannot be
inferred from a Cartesian row×column address. A parallel row bus trades shared-head
transport for 4096 resident output paths/8192 serial interruption contacts at 64; compare
their manufacture and service against 128 accessible head output duties. Fewer motors
alone does not select this architecture. Screw retention stays resident in either case;
no head load takeover is inherent. Jacquard selection without a motion/retention path
remains incomplete; E-253/E-255 preserve the distinct stopped-mask and crank results.

**End-to-end timing remains conditional.** For the 64/N20 mixed sequence
walls→visual river→physical ravine, direct cold setup plus changes is 60.92 s;
explicit neutral preparation plus that sequence is 72.08 s. Homing is additional in
both. The maximum ordinary update 22.08 s leaves 7.92 s against the 30-s reference for
everything not already inside E-255's 4-s common allowance. An **illustrative**,
unmeasured 15-s manual marking/prop step makes it 37.08 s, or 41.90 s for mask B2.
Initial ready time is `homing + neutral preparation + first-map service + manual/visual
work`: the 64/N20 walls-only first scene takes 18.28+17.16=35.44 s before homing and
unimplemented workflow. Do not report 18.28 s as full initialization. Homing/occluded
verification and manual conversion have no measured upper bound yet. Proposed stop-position recovery retains
the supported surface then verifies/re-homes affected sites; missing state or damage
requires a paused, cleared repair area. Power-loss retention while already stopped is
owner-observed on one unquantified pair; dynamic arrest and array retention remain open.

**A nominal one-square opening is not a miniature-clearance pass.** The executable
four-square-long passage control puts walls outside its reserved 25.4-mm interior.
It has zero diametral margin for a 25.4-mm base at both pitches. Reserving one extra
clear cell gives 30.48/31.75 mm; even those fail an illustrative 32-mm base. Any positive
assembly/placement allowance defeats the exact 25.4-mm case. These are chosen base
sizes and deterministic bounds, not a measured base population or FDM prior.
Represent the intended traversable area first, then put wall cells outside it;
accept a coarser boundary only where it preserves declared openings and separations.
The existing ruins trace lacks a complete semantic door/topology annotation, so its
9/8-component result remains a warning, not a fixed map or proof that either pitch wins.

**Technical recommendation:** retain grid legibility, miniature access, support and
repair as functional obligations. Keep 80×80/5.08,40-mm stroke,~30 s and~$500 as explicit
comparators; challenge minimum rest and mechanical rendering of decoration. Prioritize
64×64/6.35,N20/40 with a 20-mm physical chasm as the simpler *research comparator*, keeping
N30/50 for a player-valued deeper drop and both river representations open. This reduces
resident duties 36%, but neither array reliability nor a finished $1000 price follows
from the $954 allocation. Do not adopt larger stroke, extra heads or a projector merely
to protect a guessed terrain encoding. A one-head slower design remains worth comparing
if the owner prefers encounter setup over live in-combat reshaping;~30 s is not a veto.

Before selecting hardware, compare the true-scale views with the owner and protect
actual base/door footprints in a small playable scene. Then reuse the successful
screw/seat for E-256's load/torque/travel and moving-loss measurements. Batch variation,
guide overlap and safe reverse—not another isolated thread optimization—can change
whether either head survives. Molding/casting or machined shared parts remain options
only with their tooling, batch yield and maker-hour ledgers in E-257. No printing or
purchasing is needed for this representation decision.


Verification: historical arrays preserved exactly; common-offset invariance versus
changed-depth distinction;40-mm range and passage-width checks; independent fixed-bus
arithmetic/no-op/reversal; row/column/quadrant changed-count reconciliation; all
new schedules replayed. Three-page PDF visually inspected. Self-review only; no
independent physical validation or representative-play claim.
