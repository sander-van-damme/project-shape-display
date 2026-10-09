---
status: complete
builds-on: [E-077, E-079, E-080, A-016, E-051]
---

# Rigid-elevator reset, displacement masks and selector return budget

**Mixed starting heights cannot be reset simultaneously by a rigid shared
elevator.** Explicit release at zero and reacquisition increases the tested
five/21-height workloads to **800/3,360 row writes**. A reset-free displacement
controller reduces the cyclic examples to 320 writes, but an adversarial map
with every signed displacement restores 800/3,360. Retain that controller as a
useful workload-dependent alternative; neither controller rescues the tested
E-079 writer for arbitrary 21-height maps.

Input `beaefef`; reproduce with
`python3 tools/curated-experiment-checks/E-081/mask_schedule.py`.
Deterministic standard-library kinematic replay and analytical bounds; no random
seed, process distributions, measurements, CAD or qualified mechanism. This
canonical revision replaces the original ideal reset assignment with one
shared elevator coordinate and a fixed offset for each engaged collet. Its
original 480/1,760-write counts remain only the synchronous-reset comparator,
which requires an additional differential/slipping mechanism. Earlier writer
rejections remain conservative, but the old controller was not executable
with rigid collets.

## Kinematic obstruction and two explicit controllers

A gripped column has height `z_i=e+d_i`: elevator coordinate e plus the offset
d_i fixed at acquisition. Therefore two gripped columns preserve their height
difference. Starting at 10 and 40 mm, a common −40-mm move predicts −30 and
0 mm, not two zero heights. A hard stop blocks motion or forces slip; adding
longer tails does not remove this constraint.

Both controllers use independently retained grip and ground-pawl states.
Acquire grip and prove support before opening the pawl; close and prove the
pawl before releasing grip. Every unchanged cell remains grounded and ungripped.
A command bit may be reused through phased cams only if these output states
persist independently. One passive two-state output cannot represent the
required (pawl closed, grip open), (closed, closed), (open, closed) states.
Clearing a command must not release support. Ideal state observation here is
not a reader model. Unload/reseat microtravel and finite contact geometry remain
unimplemented; E-051 shows why those can consume a deadline.

**Release-at-zero reset:** acquire only changed cells with positive old height.
Descend, stopping at `e=−old_height`; seat that group at zero and release its
grips. Cells initially at zero remain grounded. Once all reset cells are
supported at zero, regrip only cells with positive target height, withdraw
those pawls, and rise to their destination groups. Zero-target cells stay
finished. Return the empty elevator to its initial coordinate. Each move
preserves collet offsets and every logical transfer has support. Macro travel
is `2 max(max_changed_old,max_changed_target)`, at most 80 mm for 40-mm travel.
This does not include required unloading clearance or finite tail engagement.

**Direct displacement:** compute `delta=target−old`. At e=0 acquire only the
negative-delta group. Descend through its distinct deltas, seating/releasing
cells at their targets, then return empty to zero. Acquire the positive group,
rise through its deltas, deposit and return empty. Unchanged cells never join.
Each changed column stays between its old and requested height in this ideal
model. Macro travel is `2(max(0,max_delta)−min(0,min_delta))`, at most 160 mm.
This trades elevator travel for fewer resets, transfers and often masks. It
is a scheduling change within A-016's long-tail shared-elevator family, not a
new physical selector and not E-051's equal-offset capture-at-old-height model.
No global scheduling optimality is claimed.

Long-tail reach must now cover the actual relative elevator/column envelope,
including ungripped columns during empty returns. A provisional 80-mm track
alone is not a sweep/packing proof. A slipping or differential gripper is a
third physical alternative, discussed below, not silently included in either
rigid-collet replay.

## Workloads and exact command counts

The cyclic full map sets `target=c mod H`, `old=(target+1) mod H` in each of
80 rows; H evenly spaced states span 0–40 mm. Five/9/21 states mean 10/5/2-mm
steps, explicit workloads rather than new product quantization requirements.
All cells change. Each row contains every state for H≤80.

The counts below are **selected-row visits**, not complete transient-mask writes
(E-083 accounts for old/new differences and final clear). Count each nonempty
row in each acquisition/deposition mask once, granting
ideal parallel programming of two arrays or one reusable mask with persistent
outputs. Serial independent array writers double W. Reset requires a descending
acquisition, H−1 old-height deposit masks, an ascending acquisition and H−1
target deposit masks: **W=160H**. The direct cyclic controller has only two
signed displacement values (−one step and +40 mm): four masks, **W=320**.

The all-displacements challenge fills each row by repeating `(old,target)` pairs
`(h,0)` and `(0,h)` for h=1…H−1. It fits 80 columns for the tested H≤21 and
forces every signed displacement. Both controllers then require **W=160H**;
this is a realizable unfavorable workload, not a claim that all possible maps
have this count. The direct route still halves transfers for cells that would
otherwise need an intermediate reset. Exact sparse row counting is executable.

| Workload | Reset W | Direct W | All-inclusive row budget, reset / direct, with B=6 s |
|---|---:|---:|---:|
| Two-height cyclic | 320 | 320 | <75 / <75 ms |
| Five-height cyclic | 800 | 320 | <30 / <75 ms |
| Nine-height cyclic | 1,440 | 320 | <16.667 / <75 ms |
| 21-height cyclic | 3,360 | 320 | <7.143 / <75 ms |
| Five-height all-displacements | 800 | 800 | <30 / <30 ms |
| 21-height all-displacements | 3,360 | 3,360 | <7.143 / <7.143 ms |
| Uniform zero→one positive height | 160 | 160 | <150 / <150 ms |

`T=B+(W+R)t <30 s`: t includes address changes, pin/pulse actuation, withdrawal,
registration and row readback; R counts extra retried rows. B includes elevator
travel, all global cam/clear/support-proof phases, settling and non-row recovery.
B=6 s is only an allocation scenario, not demonstrated performance. Do not add
elevator time twice. No overlap with elevator movement is credited. A transient
array's clear/reset takes additional time; two persistent arrays can selectively
set/reset but still sequence support acquisition and deposition.

A 5×5 initially flat changed patch costs 10/25/30/30 row writes for the generated
2/5/9/21-state examples under either controller; only up to five target values
are present. No changed cells means zero writes/motion. Counts do not prove
physical regional isolation: shared reactions/deflections still matter.

## Fixed writer and common-return constraints

E-079's middle-error witness has d=1.89 mm, a=0.4 mm, k=0.8 N/mm,
c=0.10 mm and guide friction=0.1. It retains only 0.0225-mm geometric reserve
and 0.00296-N slow-seating margin. Its **chosen sufficient** writer stroke is
8.74554 mm, before free approach through shutters; it is not a universal
minimum. Two rest-to-rest legs with symmetric acceleration a, infinite speed
and no dwell require `4 sqrt(D/a)`, D in metres.

| Acceleration | 800-write writer time alone | 3,360-write writer time alone |
|---|---:|---:|
| 5 m/s² | 133.831 s | 562.092 s |
| 20 m/s² | 66.916 s | 281.046 s |
| 100 m/s² | 29.926 s | 125.688 s |

With B=6 s, five/21-height reset (or all-displacement) deadlines require
**a>155.476 / >2,742.601 m/s²** even with no other row work. These are mathematical
necessary conditions, not proposed motor ratings. At 100 m/s² the cyclic
direct controller uses 11.970 s writer time, leaving conditional room for other
operations; the adversarial maps remove that benefit. The executable output
also adds actual replayed macro elevator moves at assumed 400 mm/s and 20 m/s²,
with zero contact dwell, separately from B. Five-height reset and direct all-displacement maps then cost
30.286 and 30.526 s respectively, rejecting both even before other overhead.
These are unqualified drive bounds;
20 m/s² can lose contact with unsecured miniatures on changed cells (E-051).

E-077's supported return member, 0.7-mm-square neck and assumed 10-MPa allowable
cap the ideal pull limiter at 4.9 N, versus assumed 4-N normal 80-pin drag.
E-079's push reaction reaches 70.764 N. Combining these separate hypothetical
witnesses requires distinct push/pull limits or paths; one 4.9-N limiter cannot
drive that push. Their assembly and dynamic jam protection have not been proved.

For equivalent moving mass m, grant return acceleration `A=(4.9−4)/m` and
active reverse braking `B=(4.9+4)/m`. The ideal return time is
`sqrt(2D(1/A+1/B))`; downward gravity adds 9.81 to A and subtracts it from B.
No speed cap, transmission inertia beyond m, limiter tolerance or impact is
included. Return-only times discard the entire push and every other operation:

| Mass | 800 writes, balanced / gravity-assisted | 3,360 writes, balanced / gravity-assisted |
|---|---:|---:|
| 5 g | 8.275 / 8.081 s | 34.756 / 33.940 s |
| 20 g | 16.550 / 15.164 s | 69.512 / 63.691 s |
| 50 g | 26.169 / 21.658 s | 109.908 / 90.965 s |
| 100 g | 37.008 / 27.138 s | 155.433 / 113.981 s |

All tested masses now fail the 21-height reset/adversarial deadline on return
alone, even with favorable gravity. This rejects only the combined stroke,
force, mass and schedule scenarios. The mass, friction and allowable are bounds,
not weighed components or calibrated process distributions.

## Slipping-reset alternative and complete-system burden

A slipping collet could let each changed column stop at the zero datum while
the elevator continues downward. For common reset depth D, relative slip at
site i is `D−old_i`. This changes the physical mechanism: static holding must
support upward load, downward slip must not overload the zero stop, and the
collet must re-establish lift without missed engagement. No such clamp is
implemented. Friction, stick-slip, wear and common preload drift cannot be
replaced by a perfect clutch assumption.

For the cyclic five/21-height full maps, aggregate reset slip is **128.00 /
130.72 m per update**. At hypothetical constant sliding force 0.1/0.5/1 N per
site, dissipated work is 12.8/64/128 J for five heights. Near the end, as many
as 6,400 sites transmit stop load or approach breakaway: a conservative
640/3,200/6,400-N shared-load envelope. Exact kinetics and which sites are
still sliding alter this profile; no real-force or thermal estimate follows.
Allowing slip thus removes some address operations by adding a repeated
force-critical wear interface and ground-stop burden. Do not credit the old
synchronous-reset count to rigid grips.

One command array still repeats 6,400 memories; two repeat 12,800. The shutter
route adds 12,800/25,600 aperture sites plus 80/160 travelling captive writer
pins/spring pockets; fixed writers repeat those pins at every cell. Indexing,
return beams, keys, reset combs, detents and cam routes remain. Magnetic arrays
need 160/320 reversible lines plus magnets/returns/detents and retain E-080's
pulse-history gate. Reusing a command array does not delete physical grip/pawl
retention, guides or service access.

With an assumed $250 for all other bought hardware, the $500 cap leaves
$0.0390625 per cell for one bought item or $0.01953125 each for two; at $400
elsewhere, $0.015625/$0.0078125. These are residual allowances, not supplier
prices. Neither route has a complete affordable BOM, print/assembly burden,
lifetime or qualified repair procedure; no cost/reliability winner follows.

Direct displacement has 12,800 support observations for 6,400 changed cells.
The cyclic reset requires 20,480/24,480 at five/21 levels, before flag/address
reads, because reset/regrip adds transfers. Given an actual per-observation
unsafe false-accept bound p, `P(any unsafe acceptance)≤min(1,Np)` without
independence. p is unknown; common reader bias can defeat repeated observations.
Retries help only detected, recoverable faults. One extra ms per row costs
0.800/3.360 s for the reset/adversarial maps, versus 0.320 s for cyclic direct;
one 80-row group retry costs 80t. Whole replay doubles W and does not cure bias.

## Decision and evidence limits

Reject simultaneous rigid reset and stop interpreting the original bookkeeping
as a physically executable controller. Retain explicit zero-deposit/regrip and
direct displacement as kinematic comparators, with sparse and adversarial maps.
Do not optimize the old narrow ramp again: its force/return burden remains even
when a favorable workload compresses masks. Magnetic pulse schedules face the
same operation budgets but still lack a physical timescale and finite package.
No route earns fabrication, hardware selection or reliability acceptance.

Next discriminate a **directly driven, positive-completion command selector**
with finite retention/reset and grip/pawl support transfer against this budget.
Row-local reusable hardware remains possible, but must count repeated bank
travel and is related to A-013/E-051 rather than a new architecture discovery.
Reopen slipping reset only with an explicit clamp/stop force path that bounds
aggregate wear/load and lift re-engagement. These are implementation gates,
not a request for another arbitrary damping/tolerance sweep.

Self-review (not external validation): exhaust all 81 two-cell old/new maps
at three heights for both controllers; check fixed offsets, continuous logical
support, unchanged cells, no below-zero motion and final targets. Direct paths
also preserve each cell's old/target interval. Between stops motion is monotone
and affine, so endpoint height checks bound the whole segment. Injected absent
pawl support fails. Independent path formulas and the two-height-difference
counterexample challenge the former reset. Full-board cyclic/all-displacement,
zero-change, uniform and local counts are checked, plus original saturation
cases at 80/81 levels. Motion checks integrate acceleration phases and recover
symmetric/asymmetric and finite-speed limits. Closed forms need no timestep
study. Model checks do not validate collet geometry, pawl insertion clearance,
reader behavior, force limiters or actual manufactured performance.
