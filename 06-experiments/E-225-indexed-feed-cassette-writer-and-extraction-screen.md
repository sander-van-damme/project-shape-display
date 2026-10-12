---
status: complete
builds-on: [E-224, E-218]
---

# Indexed feed removes a speed restriction, not the cassette writer's system burden

**Park the specified indexed writer; end branching-rail refinement.** Stopping
followers before switching removes E-224's `speed ≤ free-gap/switch-time` limit.
It does not enlarge the finite parking window. The sampled favorable schedule
still needs 1,024 gates at 28.608 s, with only .09-mm residual parking margin in
the stated error box, unbuilt captured followers and parallel routing. Direct
support on the existing plain bar bottom fails both parking and upper-rail
clearance. No complete machine earns further local development or printing.

Input main `297c990`. Reproduce:
`python3 tools/curated-experiment-checks/E-225/indexed.py`.
Evidence: **mechanism hypotheses, exact finite-interval checks, ideal state
replay and schedule/stock calculations with explicitly assumed bounds**.
Self-review, no physical measurement, assembly CAD, process prior or purchased
BOM. Five 10-mm-spaced levels remain a comparison alphabet, not chosen resolution.

## Changed transaction and extraction hypothesis

Keep E-224's compact vertical bars and common cassette comb. Write only the
unloaded spare; old terrain stays on its dock. Four branching stations have
synchronized phases, separated by integer multiples of 5.08 mm. All bars stop
clear of every tongue, all required gates switch together, then the cassette
advances one pitch and stops again. Commands at station k raise only targets
at or above k; completed lower codes bypass later stages. No spreading joints,
individual conveyors or off-boundary programming are credited.

A 2-mm tongue followed by the fixed remainder of a 10-mm rise occupies 5.05 mm
in the ±.35-mm/slope-4 scenario. Allowing a 2-mm follower and .70-mm relative
error gives 7.75 mm; choose **two pitches /10.16 mm per station**. A stream with
n bars uses n+8 index cycles, including flush onto the five fixed output rails.
This policy deliberately keeps ramps separated; overlapping ramp contacts,
continuous pipeline reuse and writing during return are different policies.

Proposed extraction: close/prove the common comb while every bar still rests on
its output rail, then withdraw the **whole rail bank sideways** before returning
the cassette carriage. A 4-mm withdrawal and return are explicitly charged.
This supplies a causal support order without adding per-bar moving retainers;
it is not a routed cassette. Cantilever rail roots, frame openings, gate drive
connections, guide clearance and the five-level bypass remain unconstructed.
A locked cassette goes to E-218's two-lane rise-target/then-lower-old exchange.
All lift returns, lane transfer and row indexing remain charged.

Power loss before transfer leaves the old row docked. During writing, fixed
rails support parked bars; a stalled or mis-set unloaded spare is invalid and
must be reset. During rail withdrawal the common comb carries all bars. During
loaded exchange E-218's unqualified shared arrest/dock sequence remains necessary.
Read actual heights and prove keeper, rail clearance and docks before release;
these are required interfaces, not working sensors. One entire row retry is
budgeted; broken support, false readback or a stuck column requires a supported
service stop without a 30-s claim. Touched rows still hand off all 80 cells;
untouched rows remain docked. Ideal unchanged height does not remove E-218's
opposing-cassette-error settling of up to 2e.

## Finite parking and the simpler control

For tongue run w, follower footprint f, pitch p, independent per-bar longitudinal
bound ±e and shared feed/rail phase bound ±c, centered parking margin is

`m = (p − w − f)/2 − e − c`.

Strictly positive m is necessary for this stop-and-switch policy. Enumerating
both neighboring follower errors and common phase corners checks the inequality.
For p=5.08, w=f=2 and c=.10 mm, m=.44/.29/.09/−.26 mm at e=0/.15/.35/.70.
Increasing c from .10 to .20 mm makes the e=.35 case fail. These are competing
bounds, **not X1C distributions or yield estimates**. Coherent phase error does
not cancel here: a common stop bias can put every follower on its gate, even
though common bias cancels E-224's moving-follower headway difference.

The mechanically simpler control bears directly on the **3.4-mm bar bottom**,
without a separate projected follower. With the same 2-mm tongue,
`(5.08−2−3.4)/2=−.16 mm` even at zero error. Also, five superposed rails directly
under the shaft cannot supply the claimed low-code bypass: a 64-mm vertical bar
on level 0 intersects rails at 10/20/30/40 mm. Exact interval intersections give
**10 collisions among 25 bar-level/rail-level pairs**. This is a scoped geometric
failure of bottom-bearing stacked rails, not a ban on side followers. A lateral
follower can put the rails beside the shaft, but it owes finite follower/rail
routing and clearance from both resident bearing lanes. Narrowing a bottom nose
alone does not remove shaft/upper-rail interference. Stop before designing a
finer tongue, special toe or spring to rescue this comparator.

## Complete schedule and dynamic limits

Assume feed limit 200 mm/s, acceleration 8,000 mm/s²; rest-to-rest quintic motion
per pitch. Its unit-duration peak speed and acceleration are `1.875p` and
`10√3 p/3`. For each cycloidal cam segment, conservatively bound
`|z̈| ≤ max|cam″|·max(ẋ²) + max|cam′|·max|ẍ|`.
The second term matters in indexed motion. Choose duration to satisfy these
bounds plus a 20% time allowance. This is a **sufficient conservative profile**,
not a time-optimal trajectory or proof all possible feeds are too slow.

The favorable assumed vertical acceleration bound is 100 m/s². At e=.35 the
calculated index is .10255 s and gate switch/proof .04516 s. This is not a
gravity-following allowance: high downward acceleration needs a captured follower
or preload. A gravity-only, zero-drag sufficient profile instead bounds vertical
acceleration by 9.81 m/s²; friction makes that smaller. Captured channels add
opposing contact surfaces, alignment, force and service burden; no such complete
follower has been constructed. Positive rail driving is not free following.

Each row charges common 40-mm reset and return; n+8 write/switch cycles; sideways
rail withdrawal/reinsertion; full empty feed return; two loaded exchange moves
and two empty resets; two 2.4-mm lane strokes; one row hop; .5 s auxiliary read,
keeper, docking and registration allowance. Add 2 s/map plus one worst-row retry.
B banks operate independently; full time is `2+(ceil(80/B)+1)·row_time`.
No free offline work or cycle overlap. Grid B=1/2/4/8/16, streams/head
s=1/2/4/8/16/40/80; gates=4Bs. Spatial splitting is still a **grant**, not CAD.

| Assumed case | B × s | Gates | Calculated seconds |
|---|---:|---:|---:|
| Zero local error, 45-mm exchange, continuous arrest | 16 × 16 | 1,024 | 27.667 |
| ±.35 mm, 45-mm exchange, continuous arrest | 16 × 16 | 1,024 | 28.608 |
| ±.35 mm, 65-mm exchange, continuous arrest | 16 × 40 | 2,560 | 27.892 |
| ±.35 mm, 65-mm exchange, one full-row stream/head | 16 × 1 | 64 | 108.908 |
| Gravity-only sufficient profile, 65-mm exchange, largest grid | 16 × 80 | 5,120 | 38.996 |

No sampled indexed 1-mm loaded-arrest case passes. The 45-mm stroke is E-218's
optimistic borrowed allowance; 65 mm is sensitivity, not proved bar clearance.
At B=16/s=16/45 mm, auxiliary time .25/.5/1 s gives 27.108/28.608/31.608 s.
A five-row patch within one bank consumes the same critical path as the full map;
a single-row patch costs two row services including retry. Faster other banks
cannot help a concentrated regional request.

Parallel routing is a real remaining obstacle: s=16 gives only 25.4 mm per
five-bar block, while the proposed writer grants **40.64 mm extra run per stream**.
Adjacent coplanar stream envelopes overlap. Staggered tracks, removable subframes
or a spread/repack carrier must be constructed and counted; the calculation
cannot silently supply them. Single-stream service avoids that split but misses
timing under the stated policy. Thus indexing improves the 45-mm calculation
from E-224's 2,560 gates to 1,024, without establishing a compact affordable machine.

## Replication, economics and manufacturing

Favorable 16-head/s=16 case; each bank serves five rows plus one spare:

| Functional item | Cell / row | Bank including spare / head | Board |
|---|---|---|---:|
| Columns / guide stations | 1 / 80; 2 /160 | 400 /800 | 6,400 /12,800 |
| Media bars / active comb contacts | 1 each /80 each | 480 each | 7,680 each |
| Bar guides / notch positions | 2 /160; 5 /400 | 960 /2,400 | 15,360 /38,400 |
| Common cassette keeper / alternative row docks | 1 /2 per row | 6 /10 | 96 /160 |
| Four writer gates / five rail paths per stream | shared | 64 /80 | 1,024 /1,280 |
| Loaded lift/arrest sets, two dog functions/set | shared | 2 /≥4 | 32 /≥64 |
| Feed, reset, rail withdrawal, lane transfer, carriage, readers | shared | ≥1 each | ≥16 each |

No per-bar spreading joint is added. But finite side followers, capture faces,
rail-root fixtures, springs, inserts, fasteners, wiring and spatial multiplexing
hardware are **unknown, not zero**. Resident bar/comb/guide interfaces remain
repeated wear and tolerance sites. A common stop-phase or rail bias can fault an
entire head; dock failure can expose 80 loaded cells. Jam access still requires
supporting the row before withdrawing buried media. Common printing does not
remove individual functional sites or 406-mm row assembly on a 256-mm bed.

Same solid bar allocation as E-224 at B=16: **2.674 L**, excluding followers,
carriers and writers. At assumed extrusion 5–15 mm³/s and 10% scrap this is
55.0–165.1 h; 7,680 bar placements at 10/30 s add 21.3/64 h. Columns add the
existing 4.608-L control. No sliced print, assembly timing or PLA creep evidence.
Keeper, guides and bearing lanes retain E-224's unqualified functional envelopes;
parking adds .09-mm residual margin, plus unmodeled debris, wear and rail warp.

An assumed $250 nongate reserve leaves **<$.244 per complete gate** at 1,024
under $500, or <$.146 under $400; at 2,560 these fall to $.0977/$.0586. These are
allocations, not prices. All 32 lift/arrest sets and 16 heads' drives/readers,
frames, supplies and fixtures still owe a BOM. At slope ≤4, assumed unloaded
resistance .05/.3/1 N, all 80 bars can occupy rising segments across the four
stations; the quasistatic feed envelope `80·4R` is 16/96/320 N per head, before inertia or capture
friction. Loaded row force remains 80/261.6/800 N at assumed 1/3.27/10 N per cell.

## Decision and verification

Keep the indexed-feed escape from the continuous-speed inequality, its absolute
phase sensitivity, and the bottom-bearing/upper-rail counterexample. Do not treat
the conservative profile as a universal lower bound, or grant permanent compact
routing from nominal throughput. The specified family has neither broad repeated
margins nor a credible whole-system cost/support path; no further gate, nose,
comb or dog refinement is justified. Reopening needs a genuinely changed shared
transaction that removes these obligations, not a faster assumed motor.

Checks: 3,125 five-bar pipeline codes; 729 ideal old/new three-column handoffs;
24 finite-error parking boxes with all corners; exact plain-bar/rail intersections;
quintic acceleration finite-difference errors decreasing 1.86e−4 →1.42e−5 →8.98e−7;
flush, stock and monotonic schedule limits. These verify the stated model, not
physical capture, sensing, gravity following or independent validation.
