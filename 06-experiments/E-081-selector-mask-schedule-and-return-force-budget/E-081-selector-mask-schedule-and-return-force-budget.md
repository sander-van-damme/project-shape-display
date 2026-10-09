---
status: complete
builds-on: [E-077, E-079, E-080, A-016]
---

# Destination masks dominate the retained-selector scan budget

**One or two scans do not complete an arbitrary-height map.** For the explicit
reset-to-zero/rise-and-deposit controller, a full 80×80 map with H destination
heights in every row needs **80(1+H) row writes**, even granting simultaneous
two-array programming or a temporally reused command array. Five heights need
480 writes; 21 need 1,760. Under E-079's chosen 8.746-mm writer stroke, five
heights exceed 30 s at 20 m/s² before any other work. At 100 m/s², 21 heights
still need 65.836 s. These reject the specified schedules/drive scenarios,
not all mechanical coincidence or finer-height architectures.

Input main `37b7e62`. Reproduce with
`python3 tools/curated-experiment-checks/E-081/mask_schedule.py`.
Deterministic standard-library state replay and closed-form timing; no seed,
measurements, sourced process priors, geometry simulation or hardware claims.
This is complete command-operation accounting around an **idealized** output
machine, not a completed machine design. Reset/lock/grip geometry remains open.

## Controller and command-memory alternatives

Retain A-016's long-tail grippers, shared elevator, ground pawls, and reset
changed columns to zero before rising to requested heights. Each changed cell
is first gripped and verified, then its pawl opens. At each occupied target
height: insert the relevant pawls, prove support, then release those grippers.
Unchanged cells keep their ground pawls and never acquire elevator grip.
The model checks support after each logical transition and exact final heights;
it does not solve unloaded pawl insertion, grip strength, motion microtravel,
elastic disturbance or finite contact continuity. Height indices represent any
chosen levels spanning 0–40 mm. Five/9/21 evenly spaced levels correspond to
10/5/2-mm increments; these are workloads, **not new quantization requirements**.

Generate target height `column mod H` and old height `(target+1) mod H` in every
row. Every cell changes and every row contains H targets for H≤80. The first
mask selects all changed cells; each subsequent mask selects cells depositing
at one destination. Every cell occurs exactly twice, so there are 12,800
selected-site commands. Row writes are counted only for nonempty rows; a row
can write arbitrary columns together. Hence full population occupancy costs
80(1+min(H,80)), although this saturation says nothing about added elevator
stops when different rows use different height sets. This count is exact for
this encoding, not an information-theoretic bound on all encodings.

Compare three implementations without equating their hardware:

- **Two independent persistent command arrays:** separately command grip and
  pawl actuation. Serial writers cost twice the row count. Ideal dual writers
  can program matching masks concurrently, but the cams still sequence grip
  acquisition before pawl withdrawal, and pawl proof before grip release.
- **One transient mask reused through phased cams:** write each event mask,
  operate grip/pawl phases in the required order, and clear the command before
  its next use. Grip and pawl **physical states must persist independently**
  of clearing/rewriting the command. A reset comb and parked cams alone do not
  demonstrate that output storage. Additional downstream retention may replace,
  rather than simply eliminate, the second command array.
- **Direct one-bit output without persistent actuators:** rejected as a complete
  controller. The support path needs (pawl closed, grip open), (closed, closed)
  and (open, closed); a passive two-state mapping of one bit cannot represent all
  three. A shared cam phase or other state can supply the third condition, but
  its physical hold/transfer mechanism must then be counted. This does not
  reject all one-array or phased-cam architectures.

A transient array's event clear/reset is additional work, not a free row write.
Persistent dual flags can instead set initially and selectively reset at each
destination. No scan overlap with moving columns is credited: programming cams
are parked. Overlap, look-ahead buffering or extra writer banks changes this
schedule and needs its own storage/isolation accounting.

## Whole and local time boundaries

Let W be counted row writes, t the **all-inclusive** row service, B the total
remaining time and R additional retried rows. Then `T=B+(W+R)t <30 s`.
Row service includes actual address changes, pin/pulse actuation, withdrawal,
registration and row readback; B includes elevator/reset travel, all global
cam/clear/support-proof phases, settling and any non-row recovery. Use B=6 s
only as an explicit allocation scenario, not a demonstrated motion/reader time.
If those operations exceed six seconds, the row budget shrinks accordingly.
Do not add a row operation again in B.

| Full-map workload | W, ideal parallel/reused | All-inclusive row budget with B=6 s | Serial dual budget |
|---|---:|---:|---:|
| Two heights in every row | 240 | <100.000 ms | <50.000 ms |
| Five heights in every row | 480 | <50.000 ms | <25.000 ms |
| Nine heights in every row | 800 | <30.000 ms | <15.000 ms |
| 21 heights in every row | 1,760 | <13.636 ms | <6.818 ms |
| Uniform change to one height | 160 | <150.000 ms | <75.000 ms |

A 5×5 changed patch costs 10/25/30/30 row writes for the generated
2/5/9/21-height examples; the latter two contain only five distinct targets.
Zero changed cells need zero writes. Full-width shutter movement and shared
cam reaction can still disturb adjacent terrain despite ideal logical isolation.
These local operation counts do not establish a local-time or disturbance pass.

The mechanical timing witness uses E-079's middle-error, a=0.4 mm, k=0.8 N/mm,
c=0.10 mm, guide-friction=0.1 section. It has only 0.0225 mm geometric reserve,
0.00296 N slow-seating margin, and a **chosen sufficient** writer travel of
8.74554 mm before free approach through shutters. It is not the minimum stroke
of all mechanisms. Assume a fixed stroke that travels this distance and returns
to rest every row. At symmetric acceleration a, infinite speed and no dwell,
two legs take `4 sqrt(D/a)` with D in metres. This is an optimistic lower time
for that stroke/acceleration policy, not for every potentially adaptive drive.

| Acceleration (m/s²) | Five-height writer time alone | 21-height writer time alone |
|---|---:|---:|
| 5 | 80.299 s | 294.429 s |
| 20 | 40.149 s | 147.215 s |
| 100 | 17.955 s | 65.836 s |

With B=6 s and no other row work, five heights need a>55.971 m/s²; 21 need
>752.505 m/s². These are mathematical deadlines, **not proposed motor ratings**.
The latter would require about 2.57 m/s peak stroke speed. Finite speed limits,
jerk, free approach, shutter movement, indexing, readback, reset and settling
all worsen the deadline. Serial dual programming doubles these times; true
parallel hardware has to be counted. At 100 m/s², five heights leave only
12.593 ms/row beyond writer motion if B really fits six seconds.

## Return force couples the speed gate to a common jam

E-077's supported return member, 0.7-mm-square neck and assumed 10-MPa
effective allowable cap the ideal limiter force at 4.9 N; assumed normal
80-pin return drag is 4 N. E-079's push reaction at the chosen travel reaches
70.764 N. Combining these **separate hypothetical witnesses** requires distinct
push and force-limited pull paths or mode-dependent force limitation. A single
4.9-N limiter cannot drive that blocked push. The combination has not been
packed or qualified.

For moving equivalent mass m, balanced-axis return acceleration is at most
`A=(4.9−4)/m`; generously allow active reverse braking at `B=(4.9+4)/m`.
The fastest rest-to-rest return has `t=sqrt(2D(1/A+1/B))`. This is more favorable
than incorrectly assuming the same net force for acceleration and braking.
For a vertically downward return, add g=9.81 to A and subtract g from B.
The source evaluates both gravity cases. There is no speed cap, compliance,
limiter tolerance, impact overshoot or transmission inertia beyond m; actual
jam protection under those dynamics is unproved. Effective mass and friction
are scenarios, not part weighings or calibrated distributions.

Return-only times discard the entire push stroke and every other operation:

| Equivalent moving mass | Five heights, balanced / gravity-assisted | 21 heights, balanced / gravity-assisted |
|---|---:|---:|
| 5 g | 4.965 / 4.849 s | 18.206 / 17.778 s |
| 20 g | 9.930 / 9.099 s | 36.411 / 33.362 s |
| 50 g | 15.701 / 12.995 s | 57.571 / 47.648 s |
| 100 g | 22.205 / 16.283 s | 81.417 / 59.704 s |

For the tested masses of 20–100 g, 21 heights fail on return alone even with favorable gravity.
This is a conditional rejection of the combined stroke/force/mass scenario,
not proof of an actual writer's mass, speed or universal mechanical limit.

## Inventory, uncertainty and detection

One command array repeats 6,400 memories; two repeat 12,800. The shutter route
adds 12,800/25,600 aperture sites and, with a moving row writer, 80/160 captive
pins and spring pockets. Row indexing, supported return beams, keys, reset
combs, detents and cam paths remain real interfaces. Fixed writers instead
repeat the pins and springs at every cell. The magnetic route needs
160/320 reversible row/column lines plus local magnets/returns/detents, and
retains E-080's pulse-history gate. The moving row's pins are a hardware-count
advantage, not proof that registration and writer return fit the row deadline.

At an assumed $250 budget for **all other bought hardware**, $500 leaves
$0.0390625 per cell for one purchased item, or $0.01953125 each for two. With
$400 consumed elsewhere these become $0.015625/$0.0078125. Those allowances
include no supplier claim. No route has a complete priced BOM, print/assembly
time, lifetime or qualified repair procedure, so there is no credible cost or
reliability Pareto winner. A reusable mask does not make output latches, guides,
collets, pawls and repair access disappear.

At least acquisition and deposition support observations occur per changed
cell: 12,800 opportunities on a fully changed board, before flag/address reads.
If each has bounded unsafe false-accept probability p, the union bound is
`P(any unsafe acceptance) ≤ min(1,12800p)` without independence. This is not a
failure estimate: p is unknown, and common reader bias can defeat both
observations. A retry is justified only for a detected, recoverable fault;
false acceptance consumes no retry budget and still jeopardizes support.
Every extra 1 ms per row adds 0.480/1.760 s for five/21 heights. One retried
80-row group adds 80t; a complete replay doubles W and still does not cure bias.

All force, dimensional, timing and mass inputs are competing epistemic bounds.
Worst shared friction/limiter/registration shifts apply to the whole row and
are never divided by 80 or 6,400. E-079's correlated-error limitations and
E-080's uncalibrated contact law still apply. No sampled yield or failure-rate
claim follows from this enumeration.

## Decision and verification boundary

Stop using E-077's one/two-scan budget to discuss completion of arbitrary maps.
Reject the E-079 fixed-stroke policy at the listed failing speed/workload bounds;
retain only its explicitly conditional low-height timing cases. Do not further
tune that ramp's widths or claim one reused command array has eliminated output
retention. Magnetic cooldown/pulse/readback schedules must fit the same event
budgets, but E-080's dimensionless times cannot be converted to milliseconds
without a physical inertia/stiffness/field package. Neither route is accepted
for fabrication or machine selection.

The next useful gate is a **changed addressing/storage implementation** that
escapes at least one demonstrated burden: row-local reusable command storage,
a directly driven positive-completion selector, or bounded physical magnetic
storage/scheduling. Require finite state retention/reset and an explicit place
for output support, then compare this same workload; another guessed damping
sweep or nominal width adjustment cannot resolve the campaign.

Self-review: all 81 old/new maps for two cells over three heights preserve
ideal support and unchanged cells; injected omitted pawl seating raises an
unsupported-cell assertion. Generated full-board counts independently match
80(1+min(H,80)) and 12,800 selected commands, including saturation at 80/81
levels; zero-change and local workloads exercise sparse row counting. Motion
checks integrate triangular phases, recover symmetric/asymmetric limiting cases
and the finite-speed formula. Closed forms require no time-step convergence.
This verifies bookkeeping and the abstract controller, not contacts, reader
performance, a physical force limiter or independent external validation.
