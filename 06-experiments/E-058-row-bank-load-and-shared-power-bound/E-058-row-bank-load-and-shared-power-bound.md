---
status: complete
builds-on: [E-050, E-051, A-013]
---

# Shared lift power can invalidate nominal row-bank timing

Retain A-013 only conditionally; require a complete channel's force–speed,
efficiency and shared-power allocation alongside price before further pawl
refinement. Increasing head count cannot remove full-map lift work. Do not
interpret the existing 10-N stationary support scenario as a requirement to
move every cell against 10 N: doing so changes the product workload.

Input main `0ca5c32`. Analytical necessary-condition screen, not motor selection,
contact simulation, measured friction or hardware qualification. Reproduce with
`python3 tools/curated-experiment-checks/E-058/power_bound.py`.
This extends one architecture's system model, not topology search. No printing.

## Model and bounded uncertainty

Enumerate 80/160/240 heads; E-050 fast/central motion; moving mass per lane
5/20/50 g; sustained downward resistance 0/1/10 N; electrical lift allocation
25/50/100 W; efficiency 0.25/0.50/0.75. These are explicitly chosen sensitivity
scenarios, not distributions, supplier ratings or X1C priors. Mass includes the
moving lane mechanism, column and any secured payload represented by that
lane. Resistance is an additional force opposing upward motion, separate from
mass gravity. It may represent sustained friction or an external load; a short
release-force peak is not a sustained resistance. Shared variation is maximally
correlated: every selected lane has the same adverse parameters. No yield
or probability follows from counts. Actual friction, batch effects and packing
remain uncalibrated; partial lanes with larger mass are not bounded here.

The discriminating reachable workload is uniform 0→40 mm, starting with the
heads at zero. Each station lifts, seats/reads, returns empty, and indexes under
the inherited nonoverlapping schedule. For N active lanes, minimum lift work is
`W=N(mg+R)0.04` joules, g=9.81 m/s². Minimum lift duration is
`max(E-050 rest-to-rest 40-mm time, W/(eta P))`.
Sum this with empty return, contact/read, index and overhead; the last partial
bank uses its actual lane count. Take the maximum of that uniform-map bound
and E-050's arbitrary-map, zero-retry bound. A value ≥30 s rejects this schedule
under the scenario. A smaller value establishes no feasible trajectory.

P is power available continuously to the lift channels after auxiliaries, with
no storage delivering extra transient energy. A buffered supply must instead
be evaluated at its drive-side output and include charging in the sustained
cycle. Efficiency is a constant scenario conversion from input to positive
lift work. The calculation omits acceleration losses, motor heating, empty-head
energy, return braking, jerk and overload recovery. These omissions make it
optimistic. It also omits retries deliberately: failure without retries is
already decisive; surviving bounds do not inherit E-050's one-retry result.
Concurrent independent-lane returns or asynchronous station pipelining would
change the schedule and require a new accounting model.

For the inherited synchronized profile, channel peak upward force is
`mg+R+ma`; full-bank input power just before acceleration ends is
`N(mg+R+ma)v/eta` (SI units). The 40-mm move reaches the specified speed for
both profiles. This is a profile requirement, not an unavoidable peak for
all alternative schedules. Staggering acceleration may reduce peaks but does
not remove lift work; it must be charged against timing. Constant downward
force acting on a supported miniature also needs an explicit payload model;
this screen makes no claim of miniature contact retention at fast acceleration.

## Results and decision

486 deterministic scenarios: 320 reject, including 158 that passed E-050's
zero-retry timing screen. The grid is sensitivity coverage, not a population
or likelihood estimate. At 240 heads, central motion, m=20 g, P=50 W,
eta=0.5:

| Sustained resistance/lane | Full-map lift work | Arbitrary-map lower bound | Synchronized peak input |
|---|---:|---:|---:|
| 0 N | 50.23 J | 23.8774 s | 28.44 W |
| 1 N | 306.23 J | 28.5665 s | 124.44 W |
| 10 N | 2610.23 J | 120.7265 s | 988.44 W |

The 1-N case cannot use the synchronized nominal profile on a 50-W allocation,
although this lower bound alone does not reject a reshaped schedule. The 10-N
case rejects even the optimistic energy-limited schedule. Neither is evidence
that real printed guides exert those forces. With free cell purchases and a
$250 reserve, the independent 240-head channel still has E-050's $25/24 budget:
power electronics, release, sensing and gripper costs cannot be omitted.
Reserve must actually cover supply and bank transport; it is not a sourced BOM.

Self-review: direct conservation identity for 6,400 cells, exact final-bank
lane count, zero-load recovery of the nominal bound, monotonicity with power,
and an energy-only lower-bound check pass in executable assertions. Units are
kg/N/m/W/s; inherited motion uses mm converted for force/power. No numerical
integration, random seed, mesh or convergence study is needed for these
closed-form bounds. No independent physical validation is claimed.

Next discriminator remains a complete affordable drive channel with force–speed
and power evidence, tested against unloaded and loaded workloads separately.
Reject a proposed channel/supply pair whose bounded force or energy violates
these necessary conditions; do not optimize pawl contacts to compensate.
Reopen failed scenarios with lower demonstrated load, greater budgeted power,
changed motion scheduling or an explicit energy-storage architecture. A-013
remains unselected; this result does not reject independent actuation in general.
