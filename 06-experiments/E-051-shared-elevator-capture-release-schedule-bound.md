---
status: complete
builds-on: [E-050, Q-012, A-013]
---

# Shared-elevator capture/release: exact abstract schedule bound

## Decision

Reject the **80-channel, zero-offset, stop-at-contact shared elevator** under E-050's fast motion bounds: even instantaneous contacts require 33.350 s for a legal arbitrary-map workload. Keep 160 channels only as an unresolved embodiment: fast motion permits less than **32.73 ms total serial dwell per event stop**, before retries or additional discrepancy. Central motion fails with zero dwell. The loaded-surface extension below tightens the 160-head dwell ceiling to <15.97 ms at the ideal gravity acceleration limit for unsecured miniatures; a half-gravity symmetric profile fails even at zero dwell. This narrows Q-012; it does not reject continuous-motion capture, independently offset/sliding grippers, multiple elevators, or independent linear heads. Those mechanisms require new contact and timing models.

Input revision `f43fb78`. Evidence is exact finite state-space optimization of an idealized mechanism, not CAD, sourced actuator capability, manufacturing yield or physical measurements. No print is justified.

## Mechanism and search boundary

One vertical elevator carries 80 or 160 individually selectable rigid grippers at equal vertical offset. A gripper captures a column at its old height; the local grounded pawl releases only after load transfer. The attached column follows elevator height until its target, where its pawl takes the load and the gripper releases. Unchanged columns stay supported. Grippers must retract clear of undocked tails; individual grip and pawl selection, support-proof readback, reset and recovery remain unimplemented hardware, not free resolved components. The model grants perfect isolation and support transfer to produce an optimistic screen before detailed geometry.

Five assumed states: 0/10/20/30/40 mm, inherited from A-013 rather than a product requirement. Each station contains all 20 unequal old/new pairs (four copies per 80-cell row); this is a valid workload, not a claimed worst-case geometry or load. Identical pair multiplicity changes forces but not ideal timing. Every other five-state workload is a subset and can follow this schedule. Each station begins and ends at zero before horizontal indexing. Contacts occur at rest; all operations at the same height run in parallel. Pawl unloading microtravel and finite overtravel are omitted, as are elasticity, jerk, contact collision, bank registration and common-drive force limitations. These omissions favor survival.

`tools/curated-experiment-checks/E-051/elevator_bound.py` uses Python's standard library. Dijkstra states encode current height, previously visited heights and completed ordered pairs. Capture occurs on the first old-height visit and release on the first subsequent target-height visit; with ideal independent zero-offset grippers, early capture does not restrict elevator reach or another cell. Each graph edge is a rest-to-rest move to any other state, allowing jumps rather than prescribing a monotone sweep. Edge cost is triangular/trapezoidal motion time plus event dwell. Return home after already completing all work needs no contact dwell. Initial capture does. No random seed or probabilistic prior; the finite search settles 607–1,999 states per case.

All 15 motion/dwell combinations select `0→10→20→30→40→30→20→10→0`: eight motion segments and nine contact stops. Upward transitions are acquired/released on ascent; downward transitions may be captured during ascent and released on descent. A column can temporarily rise above both its initial and final state; only targeted columns do so in the abstract model. Miniature interaction and collision among changed columns are unmodelled, so no playability claim follows.

## Complete-map bound and sensitivity

Thirty cases: three E-050 speed/acceleration scenarios × five dwell bounds × two lane counts. Fast/central/slow speed = 400/200/80 mm/s; acceleration = 20,000/5,000/1,000 mm/s². Shared per-map overhead = 2/4/8 s. Index minimum = 0.025/0.05/0.10 s, increased when rest-to-rest travel of one/two row pitches (5.08/10.16 mm) requires more. Full time = overhead + station count × (optimal elevator schedule + index). There are 80 or 40 stations. One index per station retains E-050's return-registration allocation; omitting the final fast 80-head index saves only 0.0319 s and does not alter rejection.

| Scenario | Heads | Zero dwell | 10 ms/stop | 20 ms/stop | 40 ms/stop | 80 ms/stop |
|---|---:|---:|---:|---:|---:|---:|
| Fast | 80 | 33.350 | 40.550 | 47.750 | 62.150 | 90.950 |
| Fast | 160 | 18.216 | 21.816 | 25.416 | 32.616 | 47.016 |
| Central | 80 | 66.700 | 73.900 | 81.100 | 95.500 | 124.300 |
| Central | 160 | 36.432 | 40.032 | 43.632 | 50.832 | 65.232 |
| Slow | 80 | 150.604 | 157.804 | 165.004 | 179.404 | 208.204 |
| Slow | 160 | 81.880 | 85.480 | 89.080 | 96.280 | 110.680 |

Seconds; strict requirement <30. Only three of 30 cases survive. Dwell values are explicit epistemic bounds, not measured distributions; they include the serial critical path of acquisition, unloading, selection, relatching, support verification and release at a stop. They are not E-050's once-per-station contact allowance. All retries are omitted here, including central/slow E-050 allowances, strengthening the rejection as an optimistic bound. Fast 160-head time is `18.216 + 360*dwell` seconds. The zero-contact motion-only penalty against independent rack channels is 8 s per full board at 80 heads, before comparing different contact budgets.

Uncertainty in common drive acceleration affects every station together; treating channel errors independently cannot average it away. E-050's dimensional/error bounds still apply, but are not evaluated by this contact-free schedule. No calibrated friction, fatigue, wear, reader false-acceptance or yield model exists. The 160-channel budget remains at most $1.5625 per complete selector/gripper channel with $250 shared reserve and zero bought cell parts; the shared elevator motor, force transmission and sensing must fit that reserve or reduce the allowance. Sharing one motor does not establish this cost. Simultaneous lifting and stiffness must be sized by active loads, not one-cell force.

## Verification and next discriminator

Run `python3 tools/curated-experiment-checks/E-051/elevator_bound.py`. Checks cover zero motion, independent single-pair 0→40→0 motion, and replay of each cell's acquisition-before-release order (support continuity is assumed, not tested). A hand-computed eight-segment trajectory matches the fast zero-dwell optimum; global optimality is supplied by exhaustive Dijkstra search, not by that hand calculation. Exact finite enumeration needs no time-step convergence study. This is self-review; there is no independent hardware/contact validation.

Stop detailing the rejected 80-head stop-at-contact embodiment under these bounds. For 160 heads, require a complete affordable gripper/release implementation with actual contact geometry and a credible <32.73-ms event critical path before further schedule tuning. Continuous-motion capture or changed gripper offsets can reopen this result only with an explicit mechanism that escapes the at-rest event graph. Independent heads remain separately conditional under E-050. Retain broader mechanism discovery; this result does not select a product architecture.

## Capture load and loaded-surface acceleration extension

Input `3e4b033`; exact enumeration and Newtonian calculations, not physical evidence.
`python3 tools/curated-experiment-checks/E-051/capture_load.py` enumerates all
64 capture assignments on the fixed optimal sweep. Release at the first subsequent
target visit weakly minimizes attached mass; later release only adds occupied
segments. Delaying downward-bound cells until the descending visit gives per-segment
attached counts `[4,6,6,4,4,6,6,4]` per 20 distinct transitions, versus early
capture's `[4,7,9,10,10,9,7,4]`. Enumeration verifies componentwise minimum,
not just a weighted objective. Independent checks count pairs crossing each height
boundary, verify every old/target contact and conserve signed displacement.

For 160 heads (eight copies of each pair), peak attachment falls 80→48 and
summed absolute column travel falls 4.8→3.2 m per station; across 40 stations,
192→128 m. Delayed capture eliminates excursions outside each cell's old/target
interval and keeps the same nine event stops. It does not validate isolation,
contact transfer or miniature collisions spanning multiple columns. No changed
architecture or faster schedule is claimed.

Illustrative moving mass per column including carried payload is bounded at
5/20/50 g, **uncalibrated scenarios**, not PLA process priors or product load
specifications. At the original 20 m/s² acceleration, ideal peak column-only
force magnitude `n*m*(g+a)` decreases from 11.92/47.70/119.24 N to
7.15/28.62/71.54 N. Add elevator, grippers and link mass, friction, seating force,
deflection, drive efficiency and fault loads before sizing anything. Arbitrary
maps are not bounded by the diverse workload's 48-column peak: a uniform
0→40-mm change attaches all 160 columns, requiring 23.85/95.39/238.48 N under
the same original acceleration assumptions. That case is checked explicitly.
Capture timing saves load for mixed maps; it cannot shrink full-map drive sizing
to the all-pairs peak. No motor, power, thermal or stiffness adequacy follows.

For an unsecured miniature resting on a column, vertical normal force is
`N=m*(g+a_z)`. The original symmetric ±20-m/s² acceleration demands negative
normal force during downward acceleration (also during upward braking), so
contact cannot be maintained without retention. This is a necessary mechanics
condition, not a newly imposed requirement to retain miniatures on changed cells;
stage 02 explicitly protects *unchanged* regions. If changed cells must carry
unsecured miniatures, the original fast scenario is inapplicable.

Re-solving the exact graph with vertical acceleration limited to g=9.81 m/s²
keeps the same sweep. Keeping fast horizontal indexing, 400-mm/s speed and
2-s overhead gives **24.250 s** before contacts: total event dwell must be
**<15.97 ms**, not 32.73 ms. At g the normal force is zero for part of the
motion, so this is an optimistic limiting case without contact margin. A
0.5g symmetric bound (explicit assumed margin, not a qualification rule) gives
**32.714 s**, rejecting this embodiment even with instantaneous contacts.
Asymmetric acceleration/braking could change these results and is outside this
symmetric-profile model; it requires a new executable schedule. No friction,
tipping, jerk, manufacturing distribution or failure probability is inferred.

Decision: use delayed capture for any further realization of this sweep, and
size drive loads against uniform as well as mixed maps. Keep 160 heads
conditional for unloaded changed cells; do not advertise its fast timing for
unsecured carried miniatures. For a symmetric loaded-surface implementation,
require the tighter contact budget and an explicit acceleration/contact margin.
Stop load-policy enumeration here; geometry, support-proof timing and complete
channel cost remain the next discriminators. No fabrication is justified.
