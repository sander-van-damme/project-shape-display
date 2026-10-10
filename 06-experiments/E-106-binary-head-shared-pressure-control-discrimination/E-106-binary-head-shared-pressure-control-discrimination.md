---
status: complete
builds-on: [E-104, E-105]
---

# Shared fine pressure is constrained by load spread

**Stop treating shared coarse/fine pressure as a general replacement for
independent metering.** Under the specified eight-level .1-N load spread,
binary full-open heads need eight fine-pressure groups at nominal coefficients.
The modeled checkerboard takes **48.099 s**, or **37.731 s** with much faster
pressure transitions. Ideal independently throttled heads retain a conditional
28.808-s window at illustrative .5-mm accuracy and 2-ms extra transitions.
That comparator assumes regulation which E-105 has not implemented or priced.
This is a controller discrimination, not family rejection or hardware acceptance.

Input main `20179f9`. Replay:
`python3 tools/curated-experiment-checks/E-106/pressure_control.py`.
Evidence: deterministic reduced hydraulic/event simulation, necessary pressure
bounds and self-review. No new sourced component data, calibrated distributions,
physical measurements or independent review. Uses E-105's serial-port inertial
loss plus its competing radial viscous seat loss at full .35-mm opening.
The experiments compare controls within spatial addressing, not new architectures.

## Controller and uncertainty model

Retain 2-mm bore, 8 L/min in both directions, 40-mm travel, 80 heads, E-104's
indexing/acquisition/read/settle allocations and one conservative full-stroke
row recovery in both directions. Only changed cells open. Recovery assumes
fault arrest; persistent stuck valves and reader false acceptance remain
unbounded. The 20-ms read/settle allocation is not a demonstrated reader.

Scenarios assume .3-N downward bias, .05-N drag and payload levels spanning
0/.01/.1 N. Eight evenly spaced payload levels repeat across adjacent up/down
pairs and all rows; this is deliberately correlated, **not a load distribution
or product payload requirement**. Loads and drag are constant over travel and
known to the controller. Spring variation, stiction and unknown miniature
loads can invalidate that knowledge. Common additional .22-N drag is an adverse
case. Pressure bounds .01… .5 MPa, Cd=.4/.6/.8 and viscosity .001/.1 Pa·s are
assumptions, not process priors. Full-lift loss is `L(v)=k v²+r v`, with SI
conversion inside the source. Density is assumed 1000 kg/m³.

For upward motion, signed pressure `u=p_supply` and threshold
`b=(bias+payload+drag)/A`; for lowering, `u=−p_return` and
`b=−(bias+payload−drag)/A`. Forward speed solves `L(v)=u−b`.
The event solver recomputes pressure as heads close. If demand exceeds the pump
cap it reduces u by bisection; it rejects a state when the cap cannot keep all
opened channels moving forward. It does not multiply unequal-load flows by an
invented common factor. Reverse flow would require another model/valving policy.

Binary coarse pressure targets 400 mm/s at the highest threshold, subject to
source limits; other channels can move **faster**. There is no independent
400-mm/s cap without an added restriction. Each head closes before its terminal
band; completed coarse channels wait isolated. For bounded response τ=.002 s
and read error .05 mm, reserve `band=min(stroke,v_max τ+.05)`. The whole band
is subsequently budgeted at fine speed, conservatively ignoring progress during
coarse closure. Using maximum pressure before pump saturation bounds late coarse
speed increases; pressure transients outside the bound are not covered.

For diagnostic accuracy e=.2/.3/.5 mm, `v_s=(e−.05)/τ`. Fine cohorts use a
shared pressure allowing every open channel speed between `v_s/2` and `v_s`.
Each closes independently at its target. With common pressure-error bound ε,
its allowable setpoint interval is
`[b+L(v_s/2)+ε, b+L(v_s)−ε]`, intersected with source limits. The fastest endpoint
of the earliest-ending interval groups all compatible channels. This greedy
interval cover minimizes group count, **not total time**. The half-speed floor
is a controller choice, not a feasibility law. Allowing arbitrarily slow motion
widens the necessary interval to `(b,b+L(v_s)]`, but does not bridge the .1-N
scenario's eight load levels at nominal coefficients.

Each direction charges E-104's initial 10-ms pressure/open/close allowance;
each additional stopped pressure group charges 2 or 10 ms, including reopen,
pressure settling and closure. These are unqualified allocations, separate
from residual closure error. No overlap is credited. Independent throttling
uses parallel per-channel 400-mm/s coarse caps and fine caps v_s, limited by
available load/pressure and pump flow; its ideal regulator absorbs load spread.
It also stops between coarse and fine, with the same charged transition.
Instantaneous pressure redistribution at completion events is optimistic;
actual regulator transients must fit the pressure/response bounds or add time.
E-105's stem-displacement transient is not resolved; closure-volume exchange and
compressibility need dynamic evaluation before any accuracy claim.

## Discriminating results

At Cd=.6, μ=.001, the fine-pressure interval widths and corresponding admissible
force spreads are:

| Diagnostic e | Half-speed…full-speed width | Force spread | Positive-speed-only force spread |
|---|---:|---:|---:|
| .2 mm | 309 Pa | .000972 N | .001301 N |
| .3 mm | 857 Pa | .002692 N | .003598 N |
| .5 mm | 2771 Pa | .008705 N | .011622 N |

The .1-N scenario separates neighboring levels by .014286 N: even the necessary
positive-speed-only intervals do not overlap at e=.5. Eight pressure settings
are needed for that fine-phase policy. Unknown load threshold or common
pressure error consumes the interval; it cannot be averaged across cells.
At ε=1 kPa, even equal loads cannot satisfy the half-speed controller at e=.2
or .3. The .5 case has a remaining interval but slows and narrows further.
This is an inverse control requirement, not a pressure-sensor specification.

Full-stroke checkerboard, nominal coefficients and zero pressure error:

| e | Binary, uniform load | Binary, .01-N spread | Binary, .1-N spread | Ideal throttled, any tested spread |
|---|---:|---:|---:|---:|
| .2 mm | 31.328 s | 56.422 s | 62.572 s | 31.328 s |
| .3 mm | 30.594 s | 40.332 s | 53.888 s | 30.594 s |
| .5 mm | 30.104 s | 32.942 s | 48.099 s | 30.104 s |

This table uses **10-ms extra transitions**. With 2-ms extra transitions,
independent throttling recovers E-105's 30.032/29.298/28.808 s. The .5-mm/.1-N
binary case still takes 37.731 s. For that load case, Cd=.4 reduces the number
of fine groups to four: 33.323…33.571 s at 2-ms transitions across the viscosity
bounds. Cd=.8/low viscosity fails the conservative all-channel recovery's pump
forward-flow condition; high viscosity completes in 38.762 s. These are scoped
controller failures, not a proof that all batching or pressure policies fail.

The adverse common-drag case leaves unloaded lowering force .03 N, less than
`.01 MPa × π mm² = .031416 N` return force. Both controllers fail without any
coefficient/timing refinement. Suction, changed bias or double acting cells
would alter the mechanism. A loaded column does not qualify unloaded lowering.

Source evaluates 216 primary cases, 72 fast-transition cases, 32 coefficient/
viscosity/drag/transition cases and two local cases. Workloads include 40/40,
79/1, unequal strokes 1…40 mm, sparse two-cell mixed rows and one 10×10 patch.
At .5 mm/.1 N/2 ms, binary 79/1 and graded maps take 34.369 and
36.333 s; the sparse equal-load pair takes 28.808 s. The origin 10×10 patch
takes 4.867 s binary versus 4.234 s throttled, including recovery. This is one
patch placement, not a local worst-case bound. These finite heterogeneous
workloads are not an arbitrary-map proof. Error
budgets remain sensitivity inputs, not new requirements. No yield probabilities
or statistical confidence are inferred from this bounded enumeration.

## Decision, economics and next discriminator

Park this **single-bank, shared-pressure grouped controller** for general
heterogeneous maps. Reopen with materially different scheduling/flow control,
a justified narrow load envelope or changed product/time constraints; do not
spend another iteration tuning the same nominal fine pressure. A conditional
near-uniform-load timing window does not cover ordinary unknown loads.

Retain independent metering as an optimistic comparator, not a completed
actuator. Next test a **discrete coarse/fine valve with a fixed fine restriction**:
closed seated state, restricted open state and large-area open state. A long
fine passage could avoid a precision analog seat gap; it adds repeated flow
geometry, clogging/viscosity sensitivity and another transition. Determine
whether any finite restriction bounds both loaded raising and unloaded lowering
under dimensional/fluid uncertainty before designing its return/frame. Compare
against the ideal throttled bound and the parked binary controller. If it has
no credible window, perform portfolio comparison rather than further fine-gap
optimization. This is a bounded metering investigation within LAB-206.

E-104's joint budget still applies: `Cshared+80 Chead+6400 Ccell <= $500`.
For assumed $250 shared and $.01 purchased/cell, **complete** head allowance is
$2.325, including driver/return/control; neither binary nor analog parts have
been sourced at that price. At $.02/cell it is $1.525. Extra pressure regulation,
load estimation and additional fine-path hardware must use that same budget.
No economic survivor, fabricated seal, print request or purchase is authorized.

Self-review checks volume conservation, loss inversion, pump saturation against
an independent volume/time bound, empty limits, opposite-sign threshold
mapping and greedy cover against brute-force interval endpoints. A separately
coded fixed-step holdout solves speeds by bisection at 100/50/25 μs and agrees
with event time within three steps. These verify implementation of the reduced
law, not its physical validity. Source is retained; JSON output is reproducible
and omitted. Control observability, leakage, closure dynamics, cost and complete
mechanical return remain unresolved.
