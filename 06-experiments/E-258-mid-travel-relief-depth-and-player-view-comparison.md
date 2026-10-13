---
status: complete
builds-on: [E-257, D-011]
---

# Mid-travel relief depth and player-view comparison

**Compare software-selectable 20/30-mm ravine depth on a 6.35-mm grid with
fixed 30-mm ordinary ground and 50-mm mechanical travel.** Sander's authenticated
2026-10-13 answer on LAB-386 (interaction `4e8f39d8-833d-497c-8ec2-c6a3deafcbce`)
requests flexibility between fast updates and larger drops, configurable in software;
he finds both depths potentially enjoyable and a larger drop potentially more immersive.
His separate LAB-384 answer selects physical river banks and a physical ravine (E-254).
These are owner preferences, not measured gameplay superiority or approval of exact
dimensions. The former N20/40 recommendation remains the simpler limited-travel
control; it cannot provide a 30-mm drop and +20-mm walls about the same ground plane.
No actuator architecture or purchase is selected.

D-011 separates sourced play conventions, five contextual map examples and unmeasured
preferences. E-254/E-257 retain the original geometry, A/B/C counts and pitch evidence.
Only their original three windows are timed here; the additional dungeon/cave examples
are qualitative checks. Evidence is deterministic geometry/scheduling and labelled
machine-wide uncertainty bounds; no new physical measurement or observed-play trial.

Reproduce `python3 tools/curated-experiment-checks/E-258/player_view.py`.
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

**Configurable-depth continuation, 2026-10-13 (calculation).** Keep ground at
30 mm in both presets: water 20, rocks 40, walls 50; change only ravine bottom
10→0 mm for a 20→30-mm drop. Shallow-mode targets are exactly the N20/40 targets
plus 10 mm, so their prepared-start and map-to-map deltas are identical. Software
selects geometry within real travel; it cannot create missing headroom. The existing
player-view PDF's relative shapes remain applicable; it does not depict this shared
absolute datum. `configurable_depth` now checks all 30 directed transitions among
three scenes × two presets, including same-scene switches, at each pitch.

| Both physical depressions; assumed seconds | 80×80 / 5.08 mm | 64×64 / 6.35 mm |
|---|---:|---:|
| Independent B2 maximum, shallow / deep | 26.03 / 30.13 | 22.08 / 25.38 |
| Mask B2 maximum, shallow / deep | 33.59 / 39.21 | 28.10 / 32.61 |
| Same ravine, 20↔30-mm switch, independent / mask | 17.13 / 19.59 | 14.98 / 16.96 |
| Cold preparation to fixed ground30, independent | 25.33 | 21.58 |

Cross-preset map transitions do not exceed the deep-suite maxima in this sample.
At64 the switch lowers1166, leaves2930 stationary and raises0 pins; reverse swaps
rise/lower. It visits56 rows,32 columns and24/32 rows in the two head regions.
At80 it lowers1825, leaves4575 stationary, visits70 rows/40 columns and30/40 bank
rows. Road/ruins preset switches are no-ops. Ground, bridge and rocks stay fixed.
Changing the entire neutral plane instead would move2930/4575 pins and visit all
64/80 rows, but takes the **same** modeled seconds: the busiest head already visits
all32/40 rows. Fixed ground improves regional isolation here, not this latency.
Changed-region miniatures/props still need clearance; these are ideal commands,
not demonstrated disturbance-free motion.

At64, ground30 preparation costs3.30 s more than ground20. With the existing
walls-only first scene,21.58+17.16=38.74 s precedes unknown homing and manual/visual
work. Fifty-mm travel with a10-mm engagement requires at least60 mm threaded length
**plus end margins**, versus50 mm plus margins for40 travel. Guide overlap, frame
clearance, transport height, wear, batch fit and incremental manufacture cost are
unqualified. The inherited $953.92 independent/$1023.92 mask allocations are unchanged
accounting placeholders, **not evidence that longer hardware costs nothing**; E-259
supersedes the $4 channel assumption with partial sourced component costs. Neither
allocation establishes a $1000 finished product; keep the ~$500 reference visible.

Recomputed both-relief sensitivity at64:1500 rpm gives25.28/29.68 s independent
shallow/deep and31.23/36.67 s mask;200 rev/s² gives26.48/29.78 and38.50/45.46 s.
These vary one input at a time, not a joint confidence interval. Rates, stop/proof,
mask rewriting and return/retry remain E-255 assumptions; the four-second allowance
has no measured end-to-end validation. The ~30-s reference therefore favors testing
the independent head's operating envelope first; it does not forbid a slower deep
setting. A depth preference is not permission to increase motor speed beyond a
qualified loaded rate.

**Technical recommendation:** retain legible grids, usable base/door footprints,
real support, recovery and repair. Keep80×80/5.08,40-mm travel,~30 s and~$500 as
comparators. Carry64×64/6.35 and fixed-ground software depth presets into architecture
comparison, with N20/40 as the simpler hardware control. Coarser pitch removes36%
of resident duties but remains conditional on passage/topology and miniature checks.
Meaningful physical walls, banks and cliffs supply tactile boundaries; props/visuals
handle decoration, with their real setup costs. Neither greater travel nor a solid
pin bridge supplies playable underpasses.

Proposed controller behavior: preserve semantic terrain and fictional depths separately
from rendered millimetres; expose depth and a predicted wait before movement, compute
from actual retained heights, and keep ordinary ground fixed across presets. A request
outside calibrated stroke/guide/load limits must be rejected or offered an explicit
reduced-depth alternative, never silently clipped. Recompute partial-state recovery
rather than replaying a stale delta. This is a research control contract, **not a
shipping software feature**, automatic geometry simplification or a qualified safety
system. Twenty/thirty millimetres are concrete comparison presets, not the only
permitted future settings.

The owner preference is resolved; no repeated depth question is needed. Next mechanical
discriminator remains E-256's successful-pair hold/drive/travel characterization,
including the added stroke/guide obligation, before detailed head design. Protect
playable openings and compare batch manufacturing/service effort; do not return to
isolated thread optimization. No printing or purchase follows from this reassessment.


Verification: historical arrays preserved exactly; common-offset invariance versus
changed-depth distinction;40-mm range and passage-width checks; independent fixed-bus
arithmetic/no-op/reversal; row/column/quadrant changed-count reconciliation; all
new schedules replayed; fixed-ground preset switches, cross-preset transitions and
uniform-offset delta invariance checked at both pitches. Three-page PDF visually inspected. Self-review only; no
independent physical validation or representative-play claim.
