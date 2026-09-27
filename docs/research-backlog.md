# Research backlog

This file records engineering ideas that are worth testing but are **not yet
validated project architectures**. An idea belongs here when it is plausible
enough to deserve a quantitative or physical test, even if a related earlier
architecture performed poorly.

A backlog entry should only move to "rejected" after its specific hypothesis has
been tested against the current design target. Earlier tests are evidence, not a
blanket rejection of every variant in the same family.

## R01 — high-speed travelling multi-row actuator

### Hypothesis

Revisit travelling/shared actuation, but do **not** restrict the concept to one
cell or one row per carriage stop.

A travelling head could service **2, 3, 4 or 5 rows in parallel** before moving
to the next row group. The mechanism may use multiple independent actuators,
mechanical fan-out, a common stroke plus local selection, or another way of
programming several rows during one carriage dwell.

This is deliberately broader than the previously screened "one XYZ writer" and
"row bank of independent full-stroke pushers". Those estimates showed that their
specific serial/full-stroke transactions were too slow; they do not prove that a
much faster multi-row head is impossible.

### Why it may matter

At 80 rows, grouping rows reduces carriage stations to roughly:

| Rows serviced per station | Stations for 80 rows | Raw average station budget inside 30 s |
|---:|---:|---:|
| 1 | 80 | 0.375 s |
| 2 | 40 | 0.750 s |
| 3 | 27 | 1.111 s |
| 4 | 20 | 1.500 s |
| 5 | 16 | 1.875 s |

The last column is only a sanity bound: reset, parking, settling and any global
lift also consume time. The useful question is whether increased parallelism can
reduce transaction time enough without making actuator count, packaging, power
or cost unacceptable.

A particularly interesting variant is a compact head that spans five adjacent
rows and all 80 columns, then advances by five rows. Another variant is a smaller
head that covers only a subset of columns but uses very fast indexed motion.
Neither should be accepted or rejected without a complete end-to-end schedule.

### Test proposal

Create a future numbered test that sweeps at least:

- rows per carriage station: 1, 2, 3, 4, 5;
- columns actuated in parallel;
- actuator stroke and whether the actuator must perform the full 40 mm travel;
- carriage speed and acceleration;
- engagement/disengagement time;
- reset/homing strategy;
- old-map to new-map worst cases, not only sparse edits;
- purchased actuator/driver count and wiring;
- moving-head mass and required carriage force;
- estimated purchased BOM;
- pitch/fan-out feasibility at 5.08 mm;
- failure recovery and whether one jam blocks an entire row group.

The full-map model must include all reset, positioning, actuation, settling and
parking operations and remain strictly below 30 seconds.

### Physical decision gate

If the analytical sweep produces a credible region, build only the smallest
full-pitch coupon/head that tests the bottleneck. Measure loaded actuation time
and repeatability instead of extrapolating from no-load motor speed.

Keep this branch alive unless quantitative timing, packaging, cost or reliability
bounds rule it out.

## Adding future ideas

Add each new idea as R02, R03, ... with:

1. the hypothesis;
2. why existing tests do or do not already address it;
3. the cheapest test that could reject it;
4. the product-level gates it must eventually meet.
