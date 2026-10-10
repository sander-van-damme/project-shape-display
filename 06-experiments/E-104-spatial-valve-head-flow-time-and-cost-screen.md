---
status: complete
builds-on: [E-103, E-060, A-013]
---

# Minority-direction rows constrain the hydraulic writer

**Retain only a conditional fast, small-bore route for finite head/valve work.**
A 3-mm bore, 8-L/min reversible supply and 400-mm/s free piston speed give
25.127 s all-up and 28.356 s checkerboard, but **33.758 s for 79 up / 1 down
in every row**. A favorable full-map example is not arbitrary-map acceptance.
At 2-mm bore the same flow/speed gives 28.216 s for the complete ideal direction
split envelope; a shared 20% speed loss makes it 32.266 s. No actual actuator,
pump, seal, reader, affordable channel or hardware performance is established.

Input main `de049d3`. Replay:
`python3 tools/curated-experiment-checks/E-104/valve_head_screen.py`.
Evidence: deterministic conservation/timing model, exact ideal flow events,
inverse budgets and self-review. No stochastic priors, sourced component data,
CAD/contact/CFD, calibration or physical measurement. Numerical design and error
bounds below are explicit assumptions, **not** X1C accuracy or fluid properties.
The grid varies one spatial-head topology; it is not 27 new architectures.

## Model, complete schedule and adversarial workload

An 80-head bank registers to one row. Independently commanded heads open only
requested fixed-base chamber valves. A single common supply serves raising and
lowering in **separate pressure phases**, all other valves closed. Each channel
closes at target; verify before withdrawal/index. Closed cells see the shared
pressure history, so bidirectional sealing remains mandatory. No two rows are
open together; no reset of unchanged heights is credited.

For area A, displacement h and channel speed cap v, volume is Ah. For a phase,
`max(sum(Ah)/Q, max(h/v))` is a necessary ideal time bound. Source also integrates
an explicit ideal flow-sharing law: active channel speeds are their free caps
multiplied by `min(1,Q/sum(Av))`. Sort completion events in free-travel time h/v
and integrate the common scale exactly. The event time can exceed the simple
bound for unequal strokes/caps. Neither law proves that real pressure-dependent
valves, seals and loads realize those speeds or the required flow allocation.

For uniform A/v and full strokes H, n up and 80−n down need
`max(nAH/Q,H/v) + max((80−n)AH/Q,H/v)` when both signs occur; omit an absent
phase. This convex function of n is maximal at **1/79**, or ties other splits
when speed-limited. Enumerate all 81 splits. Increasing any stroke can only
lengthen this ideal model, so the full-stroke split envelope covers arbitrary
heights/directions under **uniform** A/v. It does not extend that proof to the
heterogeneous scenarios or a different flow law.

Assumed per-map schedule, without overlap:

- 0.5 s preparation/setup; no uncharged per-map home/reset.
- Rest-to-rest row indexing: 200 mm/s maximum, 5,000 mm/s² acceleration;
  79 adjacent 5.08-mm moves take 5.036211 s. Actual bank mass/registration and
  fluid connections are unqualified. Full scans can reverse next map.
- Per visited row: 40 ms total acquire/withdraw plus 20 ms parallel read/settle.
- Per nonempty direction: 10 ms pressure setup/open/close overhead, plus flow.
- One bounded detected failure per map: allocate full 40-mm motion of every
  changed channel in the affected row in **both** directions, plus acquisition,
  two phase overheads and read/settle. This bounds arbitrary mixed under/overshoot
  correction inside the stroke under the same flow law; it is an overestimate,
  not a command to reset neighbors. Use the most expensive row. It presumes
  fault arrest and cannot recover a persistent stuck-open valve or unreadable
  channel. Additional failed rows stop the update.

The read and phase times are allocations, not measured capabilities. Finite
closure displacement is **not** solved by adding latency to elapsed time; see
the metering gate below. Compressibility transients, acceleration of fluid and
pistons, relief dynamics and actual settling may demand more time.

## Results and sensitivity

All table times include the above one-row retry. Flow limits are magnitudes
available in **both** directions, not a pump's unloaded forward rating.

| Bore / flow / free speed | All up, s | 40/40, s | 79/1, s |
|---|---:|---:|---:|
| 3 mm / 8 L/min / 400 mm/s | 25.127 | 28.356 | **33.758** |
| 2 mm / 8 L/min / 400 mm/s | 19.416 | 28.216 | 28.216 |
| 3 mm / 12 L/min / 400 mm/s | 20.490 | 28.242 | 29.177 |
| 2 mm / 8 L/min / 320 mm/s | 21.466 | **32.266** | **32.266** |

Grid: bores 2/3/4 mm × flows 2/4/8 L/min × speeds 100/250/400 mm/s.
**Only 1 of 27 parameter cases** survives all 81 ideal splits; 26 miss the strict
30-s gate even within these allocations. This is a scoped schedule rejection,
not proof that a different overhead allocation or multi-bank architecture fails.
At 400 mm/s the inverse flow thresholds are **>4.894 / 11.011 / 19.575 L/min**
for 2/3/4-mm bores. Even unlimited flow requires **>360.325 mm/s** for arbitrary
mixed maps with these overheads. The 3-mm/12-L/min row is a continuous-bound
escape control outside the original grid, not a priced pump selection.

Reference 3-mm scenarios: shared speed ×.8 makes 79/1 **35.758 s**; uniform bore
bias +.1 mm with alternating ±.05 mm makes **34.687 s**. Combine those with
alternating ±20% speed variation: **36.895 s**. Doubling row and phase overhead
makes **40.238 s**. These deterministic common/local bounds expose correlation;
there are no probabilities, yield or uncertainty confidence intervals. Bore
and speed are varied independently as a sensitivity model; their actual
pressure/conductance/friction coupling remains unknown. Adversarial assignment
of slow channels to each direction still needs evaluation once geometry exists.

Just **two changed cells per row**, one each direction, take 28.216 s at the
reference despite only 45.239 mL moved versus 1,809.557 mL for a full stroke.
Sparse changes spread over all rows need not be fast. A 10×10 full-stroke mixed
patch takes **4.154…5.972 s** over all 71×71 translations and writer starts at
either board edge (10,082 deterministic alignment cases). Untargeted valves
remain commanded closed; this is scheduling isolation, not measured disturbance.

## Pressure, metering, recovery and joint economics

Single-acting lowering needs downward bias/load to exceed seal drag plus return
backpressure: `Fb+Fload−Fdrag−preturn*A > 0`. Source enumerates bias .1/.5/1 N,
drag 0/.2/.5 N and return 0/.01 MPa at unloaded 3-mm bore. Bias .1 N with .2 N
drag fails even at zero gauge return; favorable loaded lowering cannot establish
unloaded lowering. Upward pressure must exceed `(Fb+Fload+Fdrag)/A` before flow
losses. No friction or pressure rating is inferred. Suction, double acting
pistons or added springs change the mechanism and must be accounted for.

At 8 L/min and assumed source differentials .1/.5/1.5 MPa, instantaneous ideal
hydraulic power is **13.33/66.67/200 W**, before electrical losses. At 2-mm bore,
full upward displacement stores **.804 L**; at 3 mm it is 1.810 L, before dead
volume, plumbing and reservoir margin. These volumes, power and port flow must
fit the machine and shared budget; no CFD or containment claim follows.

Illustrative **unapproved** .2-mm height budget with .05-mm read error leaves
.15 mm for closure motion. At 400 mm/s, uncompensated delay (or residual timing
error after feedforward compensation) must be **<.375 ms**, ignoring fluid
transients. A serial reader visiting 80 moving channels needs >213,333 samples/s
even before actuation latency. At 2 ms residual delay, single-speed operation
must slow to ≤75 mm/s: checkerboard becomes **98.416 s**. This excludes that
reactive single-speed/accuracy scenario, not all metering. A fast/slow approach,
local readback or predictive closure may escape but must charge transitions,
valve cycles, calibration and common timing error. Stage 02 sets no numerical
height tolerance; do not convert this diagnostic into a new product constraint.
False acceptance remains unbounded. Readback before withdrawing does not prove
long-term seal retention; E-060 compliance/leakage diagnostics still apply.

Enforce **Cshared + 80 Chead + 6400 Ccell ≤ $500** together. For assumed $250
shared equipment, head prices $1/$2/$3 leave at most **$.0265625 / $.0140625 /
$.0015625 per cell** for all purchases. A $5 head already fails with free cells.
These are procurement targets, not prices. Shared equipment must include the
pump, reservoir/manifolds, reader/control, row motion, wiring, power and repair
provision. Head cost includes its drive, return, link, electronics and bought
interfaces; cell cost includes every bought valve/seal/guide/fastener. PLA
printing has no formal price ceiling but 6,400 valves, piston seals and guides
remain a major assembly, wear, leak and service burden; no print-time estimate
is possible before geometry.

## Decision and verification limits

The spatial writer removes E-103's floating beams/long support shafts and
A-013's individually driven 40-mm head motions. It does **not** remove 6,400
valves/seals, reservoir volume or high-speed metering. Distributed coincidence
remains parked for its actual contact/reset failures; sourced direct rack-head
servos remain over budget. No complete-system Pareto winner is established.

Proceed with one finite staggered head/base-valve acquisition/withdrawal design
using 2-mm bore as a screen input, with the 3-mm/higher-flow case as a control.
Resolve attainable port flow, closure and unloaded lowering together before
claiming the ideal timing window survives. Cheap nominal solenoids, zero-cost
seals and infinitely fast readers are not allowed substitutes. Reject/redirect
if finite geometry or complete-channel costs close this window; no print or
purchase. Bidirectional sealing and full-system reliability remain later gates.

Self-review checks SI conversions, volume conservation, empty-work/large-flow limits,
sign symmetry, monotonicity, exact uniform formulas, adverse splits and joint
cost/force limits. A separately coded forward time-step integrator at
1/.5/.25 ms bounds event-time disagreement by four steps for a heterogeneous
holdout. That checks the numerical method, not the flow law. No independent
review, actual contact, calibrated manufacturing model or physical reliability
claim is made. Generated JSON is reproducible and not retained.
