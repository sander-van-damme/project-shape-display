---
status: complete
builds-on: [E-050, Q-012, A-013, E-052]
---

# Shared-elevator capture/release schedule and load bounds

Reject the 80-head zero-offset stop-at-contact elevator within E-050's fast
motion bounds: even instantaneous contacts require 33.350 s. Retain 160 heads
conditionally: unloaded fast motion allows <32.73 ms/event; asymmetric motion
with an ideal half-weight normal-force margin allows <9.395 ms/event.
Complete channel cost, geometry and support-proof timing remain gates. No
product selection or fabrication follows. Continuous capture, offset grippers,
multiple elevators and independent heads need separate models.

## Mechanism and exact search

Input `f43fb78`; run `python3 tools/curated-experiment-checks/E-051/elevator_bound.py`.
One elevator carries 80/160 independently selectable rigid grippers at equal
vertical offset. Capture at old height precedes local pawl release; the column
follows the elevator until its target, where support transfers to its pawl.
Unchanged columns remain latched. Grip/pawl selection, retraction clearance,
support-proof readback and fault recovery are assumed, not implemented.

Five assumed heights are 0/10/20/30/40 mm. Each station contains every unequal
ordered pair, four copies per 80-cell row. Every other workload is a subset.
Stations start/end at zero; contacts occur at rest, with same-height operations
parallel. Dijkstra states encode height, visited heights and completed pairs;
capture at first old-height visit and release at first subsequent target visit
establish an optimistic reachability model. Jumps are allowed. Initial capture
incurs event dwell; terminal return after all work is complete incurs none.
All 15 motion/dwell combinations choose the eight-segment sweep
`0→10→20→30→40→30→20→10→0`, with nine event stops. Search settles 607–1,999
states/case. Early capture may cause targeted-column excursions; delayed
capture below avoids them. Isolation and continuous support are assumptions.

Fast/central/slow speed = 400/200/80 mm/s, symmetric acceleration =
20,000/5,000/1,000 mm/s², map overhead = 2/4/8 s. Index time is the maximum
of 0.025/0.05/0.10 s and rest-to-rest travel of 5.08/10.16 mm for 80/160 heads.
Full time = overhead + station count × (schedule + index), with 80/40 stations.
One index per station retains return-registration allocation; dropping the last
fast 80-head index saves only 0.0319 s. Dwell is the total serial critical path
of acquisition, unloading, selection, relatching, proof and release at each
stop, not E-050's once-per-station allowance.

| Scenario | Heads | Zero dwell | 10 ms/stop | 20 ms/stop | 40 ms/stop | 80 ms/stop |
|---|---:|---:|---:|---:|---:|---:|
| Fast | 80 | 33.350 | 40.550 | 47.750 | 62.150 | 90.950 |
| Fast | 160 | 18.216 | 21.816 | 25.416 | 32.616 | 47.016 |
| Central | 80 | 66.700 | 73.900 | 81.100 | 95.500 | 124.300 |
| Central | 160 | 36.432 | 40.032 | 43.632 | 50.832 | 65.232 |
| Slow | 80 | 150.604 | 157.804 | 165.004 | 179.404 | 208.204 |
| Slow | 160 | 81.880 | 85.480 | 89.080 | 96.280 | 110.680 |

Seconds, strict <30 requirement; three of 30 cases survive. Fast 160-head
T=18.216+360*dwell seconds. Fast 80-head zero-contact timing costs 8 s more
than independent rack channels, before differing contact budgets. All bounds
omit retries, unloading microtravel, overtravel, jerk, elasticity, collision,
registration and shared-drive limitations. These omissions favor survival.
Dwell and motion are epistemic scenarios, not supplier data or distributions.
Common-drive error affects every station. E-050 fit bounds remain unresolved.
At $250 shared reserve and zero bought cell parts, the $500 cap permits
$1.5625 per complete 160-head selector/gripper channel. Shared motor,
transmission and sensing must fit the reserve or reduce that allowance.

Self-review checks zero motion, independent 0→40→0 single-pair timing,
individual capture-before-release replay and the hand-computed eight-segment
fast sweep. Exhaustive Dijkstra supplies global optimality only within this
abstract graph. No geometry, yield or hardware validation is claimed.

## Capture policy and symmetric loaded-surface limits

Input `3e4b033`; run `python3 tools/curated-experiment-checks/E-051/capture_load.py`.
All 64 capture assignments on the sweep were enumerated. Release at first
subsequent target weakly minimizes mass; later release only adds occupied
segments. Delaying downward cells until descent gives attached counts
`[4,6,6,4,4,6,6,4]` per 20 pairs versus early capture's
`[4,7,9,10,10,9,7,4]`. Enumeration establishes componentwise minimum;
independent boundary-crossing counts, contact-order and signed-displacement
checks agree. At 160 heads peak attachment falls 80→48; absolute column
travel falls 4.8→3.2 m/station, or 192→128 m/board. Delayed capture avoids
excursions outside each old/target interval without changing stops. Use it
for further realization; stop capture-policy enumeration.

Moving-column mass including payload is an uncalibrated 5/20/50-g scenario.
At 20 m/s², mixed-map column-only peak force n*m*(g+a) falls from
11.92/47.70/119.24 N to 7.15/28.62/71.54 N. Uniform 0→40 maps attach all
160 heads and demand 23.85/95.39/238.48 N instead. Add elevator/gripper/link
mass, friction, seating, drive losses, deflection and faults before sizing.
No power, thermal or stiffness adequacy follows.

Unsecured miniature normal force is N=m*(g+a_z). Symmetric ±20 m/s² loses
contact during downward acceleration/upward braking. This concerns changed
cells; stage 02 protects unchanged regions and does not require retaining
miniatures on changed cells. Limiting symmetric vertical acceleration to g,
while keeping fast index/speed/overhead, gives 24.250 s at 160 heads and
<15.97 ms/event, but zero normal force during part of motion. A symmetric
0.5g scenario gives 32.714 s and rejects. The asymmetric extension narrows
that rejection; neither model establishes tipping or miniature interaction.

## Direction-dependent acceleration changes the loaded-surface screen

Input `1c53219`; reproduce with
`python3 tools/curated-experiment-checks/E-051/asymmetric_motion.py`.
This is parameter/schedule refinement of the same mechanism, not architecture
discovery. Modify the loaded-surface rejection: a downward acceleration limit
alone does not require limiting upward acceleration to the same magnitude.
Keep the 80-head rejection and the complete-channel cost/contact gates.

Let upward acceleration magnitude be A=20,000 mm/s² and downward magnitude
B=(1−r)9,810 mm/s². The explicit scenario r is the minimum normal force as a
fraction of miniature weight; it is not a product requirement or a calibrated
contact margin. Both ascent braking and descent acceleration use B. Ascent
acceleration and descent braking use A. Speed is bounded by 400 mm/s.
For distance d, peak speed is
`min(v, sqrt(2d/(1/A+1/B)))`. Time is
`peak/A + peak/B + (d−peak²/(2A)−peak²/(2B))/peak`, with zero distance handled
separately. Swapping acceleration and braking leaves rest-to-rest time
unchanged. Therefore the existing exact graph can use the algebraically
equivalent symmetric acceleration `2/(1/A+1/B)` without changing its states.
This equivalence is only for time: force uses the actual directional profile.

Enforce this profile on all elevator motion, including empty segments; do not
claim a global optimum over occupancy-adaptive profiles. The inherited fast
horizontal index and 2-s overhead remain unchanged. Enumerate four margins,
three workloads (all ordered pairs, uniform up and uniform down), four dwell
bounds (0/10/20/40 ms), and two head counts: 96 deterministic cases. Every
all-pairs optimum remains the eight-segment sweep with nine event stops.

| Minimum N/(mg) | 80-head all-pairs, zero dwell | 160-head all-pairs, zero dwell | 160-head event dwell ceiling | 160-head uniform up/down, zero dwell |
|---|---:|---:|---:|---:|
| 0 | 39.830 s | 21.456 s | <23.734 ms | 14.247 s |
| 0.25 | 43.576 s | 23.329 s | <18.531 ms | 14.791 s |
| 0.50 | 50.154 s | 26.618 s | <9.395 ms | 15.878 s |
| 0.75 | 65.786 s | 34.434 s | none | 19.140 s |

Ceilings are rounded displays of `(30−T0)/360`; use unrounded executable
values for strict acceptance. At r=0.5, 10 ms/event gives 30.218 s and rejects.
Uniform maps are faster but attach all heads, so do not size force from mixed
maps. Upward acceleration still reaches 20 m/s², giving maximum ideal normal
force 3.039 times weight; the force, supply and stiffness constraints have not
been relaxed. Empty elevator mass, friction, motor force–speed, power, jerk,
contact microtravel, readback errors, retries, tipping and cross-cell miniature
support remain unresolved. Instant acceleration changes imply an idealized
profile, not a qualified miniature-retention result. r=0 has no contact margin.

Self-review integrates each constant-acceleration phase separately to verify
signed displacement and final zero speed, checks acceleration and normal-force
bounds, and recovers the symmetric formula. Test distances include zero,
0.001/10/40/1000 mm and the exact triangular/trapezoidal crossover, in both
directions. The exact event search validates capture-before-release for every
transition; this assumes support transfer rather than validating geometry.
Closed forms require no numerical mesh/time-step convergence. There is no
independent physical validation, probability distribution or manufacturing-yield
claim. Common acceleration limits affect all stations, not independent cells.

Decision: retain a conditional asymmetric 160-head loaded-surface comparator;
the former half-gravity rejection applies only to symmetric profiles. Do not
continue timing refinement without an affordable complete gripper/release
channel and support-proof event path within this budget, plus a common drive
that can supply the asymmetric force profile. No fabrication is justified.
Reopen the failed 75%-weight-margin scenario only with changed motion/contact
scheduling or justified different bounds. Broader mechanism discovery remains
open; this result selects no product architecture.

## Finite pawl travel narrows the contact-time survivor

Input main `58fc835`; reproduce with
`python3 tools/curated-experiment-checks/E-051/contact_travel.py`.
Use E-052's 1.22-mm middle-bound withdrawal witness as an explicit embodiment,
not a universal lower bound on pawl travel. At each of the nine all-pairs sweep
stops at least one column requires withdrawal or reinsertion. For this screen,
that lateral stroke begins and ends at rest while the elevator is stopped.
Different channels may operate in parallel; count only one stroke per stop,
even when both acquisition and deposition occur. Omit grip, 0.47-mm unload,
seating, support proof, control latency and retries. This is deliberately an
optimistic contact bound, not a complete mechanism or BOM.

Lateral acceleration is independent of vertical acceleration: test explicit
5/20/50/100 m/s² scenarios, with 400 mm/s speed cap. These are uncertainty
bounds, not sourced motor capability or manufacturing priors. All strokes are
triangular, with minimum time `2 sqrt(stroke/acceleration)`. Re-solve the event
graph at each resulting dwell; the nine-stop sweep remains optimal within the
inherited graph. The entire row shares the bound; no independent-cell yield
or probability is inferred.

| Lateral acceleration | One stroke | Fast unloaded map | Half-weight-margin map |
|---|---:|---:|---:|
| 5 m/s² | 31.241 ms | 29.463 s | 37.865 s |
| 20 m/s² | 15.620 ms | 23.839 s | 32.241 s |
| 50 m/s² | 9.879 ms | 21.773 s | 30.175 s |
| 100 m/s² | 6.986 ms | 20.731 s | 29.133 s |

For the half-weight-margin case, strict <30 s requires lateral acceleration
>55.295 m/s² even with every other contact operation instantaneous. At
20 m/s², the allowed stroke is <0.4413 mm rather than 1.22 mm. At 100 m/s²,
only 2.409 ms/event remains for all omitted operations. These are necessary
conditions, not feasible drive specifications. The unloaded 5 m/s² case has
only 1.492 ms/event left; a nominal pass is not acceptance.

Decision: exclude the combination of this stroke, stop-at-contact sequence,
160 heads, half-weight vertical profile and lateral acceleration ≤50 m/s².
Retain unloaded and faster-lateral cases only as conditional comparators.
Changed-cell miniature retention is not a stage-02 requirement. Reopen the
excluded combination only with shorter robust travel, evidenced faster drive,
more parallel elevators, or a different support-transfer sequence that overlaps
stroke with travel. A fly-through cam, prewithdrawal while independently
supported, or offset gripper changes the mechanism and needs geometry and
continuous-support validation; it cannot inherit this timing table. The
result strengthens the reason to investigate an explicit shared-energy
selector rather than further optimize nominal pawl dimensions. No print.

Self-review: independently integrate acceleration phases to recover stroke
and zero terminal speed; check the unlimited-speed triangular bound, replay
capture-before-release, and reconcile graph timing with `T0+360*dwell`.
All eight deterministic cases pass these numerical checks. Closed forms need
no mesh convergence. Contact elasticity, backlash, wear and actual drive
force–speed remain unmodelled; they cannot improve the stated rest-to-rest
bound under its limits. No physical or independent review is claimed.
