---
status: complete
builds-on: [E-050, Q-012, A-013, E-052]
---

# Shared-elevator capture/release schedule and load bounds

Reject the 80-head zero-offset stop-at-contact elevator within E-050's fast
motion bounds: even instantaneous contacts require 33.350 s. Retain 160 heads
conditionally: unloaded fast motion allows <32.73 ms/event; asymmetric motion
with an ideal half-weight normal-force margin allows <9.3943272 ms/event.
Including E-052 unload/reseat excludes the two serial half-weight paths below
even with instantaneous pawls; unloaded paths remain conditional.
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

## Direction-dependent loaded-surface motion

Input `1c53219`; run `asymmetric_motion.py` in the same source directory.
Upward acceleration A=20,000 mm/s² and downward magnitude
B=(1−r)9,810 mm/s² preserve ideal normal force N≥rmg. The margin r is an
explicit scenario, not a product requirement. Ascent braking and descent
acceleration use B; opposite phases use A. For distance d and speed v=400,
peak speed is `min(v,sqrt(2d/(1/A+1/B)))`. Time is
`peak/A+peak/B+(d−peak²/(2A)−peak²/(2B))/peak` (zero distance handled separately).
Swapping acceleration/braking preserves time, so the exact graph uses
`a_eff=2/(1/A+1/B)`. Forces still require the directional profile.
Enforce this profile even on empty segments; occupancy-adaptive profiles are
outside scope. Enumerate four margins, all-pairs/uniform-up/uniform-down,
0/10/20/40-ms dwell and 80/160 heads: 96 deterministic cases. All all-pairs
optima retain the eight-segment sweep.

| Minimum N/(mg) | 80-head all-pairs, zero dwell | 160-head all-pairs, zero dwell | 160-head dwell ceiling | 160-head uniform up/down, zero dwell |
|---|---:|---:|---:|---:|
| 0 | 39.830 s | 21.456 s | <23.734 ms | 14.247 s |
| 0.25 | 43.576 s | 23.329 s | <18.531 ms | 14.791 s |
| 0.50 | 50.154 s | 26.618 s | <9.3943272 ms | 15.878 s |
| 0.75 | 65.786 s | 34.434 s | none | 19.140 s |

Use unrounded `(30−T0)/360` for strict acceptance. Half-weight 10-ms dwell
already gives 30.218 s. Asymmetry rescues the symmetric half-gravity
zero-dwell rejection only; r=0.75 still fails. Uniform maps attach all heads.
Upward force peaks remain 3.039 times weight; no tipping, force–speed, power,
jerk, miniature interaction or hardware qualification follows. r=0 has no
contact margin. Common-drive bounds are not independent-cell probabilities.
Self-review integrates signed acceleration phases, displacement, final speed
and normal-force bounds; distances 0/.001/10/40/1000 mm and exact
triangular/trapezoidal crossover recover the symmetric formula in both
directions. Graph replay verifies ordering, not support geometry. Closed
forms need no discretization study. Stop motion-profile refinement without
a complete affordable channel and contact path; serial microtravel below
removes the apparent half-weight survivor for the stated sequences.

## Lateral-only contact bound

Input `58fc835`; `contact_travel.py` retains the earlier rest-to-rest lateral
screen for E-052's 1.22-mm stroke. At 5/20/50/100 m/s² and 400 mm/s, strokes
take 31.241/15.620/9.879/6.986 ms. Charging one per stop gives unloaded maps
of 29.463/23.839/21.773/20.731 s and half-weight maps of
37.865/32.241/30.175/29.133 s. Re-solving the abstract event graph retains the
nine-stop sweep. Half-weight motion needs >55.295 m/s² lateral acceleration
before unload/reseat or any other contact cost; at 20 m/s² its allowable
stroke is <0.4413 mm. These necessary conditions are superseded by the serial
paths below, not feasible drive specifications. Independent phase integration,
capture-order replay and `T0+360*dwell` reconciliation remain executable.

## Serial unload and reseat critical paths

Input `714e9e2` already contains the lateral-only screen above; this extension
uses the same `contact_travel.py` and E-052 witness (`h=0.47 mm`, `s=1.22 mm`).
Evidence is analytical motion accounting, not contact simulation or hardware
performance. Stop this bounded investigation here: added vertical travel
excludes the half-weight-margin profile for the two explicit sequences below,
even with instantaneous lateral actuation. Faster lateral actuation alone
cannot rescue them. Unloaded motion remains conditional on sequence and drive.

Keep the nine-stop delayed-capture sweep, 160 heads, 40 stations, 400-mm/s
speed cap, fast index and 2-s overhead. Eight stops capture columns, eight
stops deposit them, and seven do both. Every moving microleg starts/ends at
rest. Let `U=move(h,400,a_eff)` and `L=move(s,400,a_lateral)`; upward/downward
vertical limits give `a_eff=2/(1/A+1/B)`. U is 9.695 ms for A=B=20 m/s² and
15.448 ms for A=20, B=4.905 m/s². Distinct pawls can insert/withdraw in parallel;
operations on the shared elevator cannot use contradictory vertical phases.
Assume instantaneous gripper acquisition/release and ideal independent pawl
commands. Neither is an implemented selector.

Two explicit serial paths expose the previously omitted operations:

- **Seat cycle:** arrive at seated height z with incoming columns held and
  their pawls withdrawn; grip outgoing columns; lift h; insert incoming pawls
  while withdrawing outgoing pawls; lower h; release incoming grippers.
  Start/end each event at z. Charge `2U+L` at all nine stops, including the
  initial/final return microlegs. Inter-stop distances remain 10 mm.
- **Clearance cycle:** arrive at z+h; insert incoming pawls; lower h; release
  incoming grippers and grip outgoing columns; lift h; withdraw outgoing
  pawls. Depart at z+h. Initial capture and final deposition each cost U+L;
  the seven mixed stops each cost 2(U+L). All eight inter-stop moves remain
  10 mm; the initial lift and final lowering close the board-height path.

Thus full-map times are `T0+40*(18U+9L)` and `T0+40*16*(U+L)` respectively.
The generous one-branch relaxation `T0+360*(U+L)` bounds both from below:
it lets capture and deposition branches overlap and discards their other
vertical legs. It is **not a realizable complete sequence** or a global optimum
across altered trajectories. Do not add microtravel to a macro profile that
already includes it; these paths define exactly where the extra legs occur.
The earlier event-graph optimum is not a proof that either detailed sequence
is globally optimal. No new graph search is claimed.

| Lateral acceleration | Unloaded seat cycle | Unloaded clearance cycle | Half-weight seat cycle | Half-weight clearance cycle |
|---|---:|---:|---:|---:|
| 5 m/s² | 36.443 s | 44.415 s | 48.987 s | 56.499 s |
| 20 m/s² | 30.820 s | 34.418 s | 43.364 s | 46.502 s |
| 50 m/s² | 28.753 s | 30.744 s | 41.297 s | 42.828 s |
| 100 m/s² | 27.712 s | 28.892 s | 40.255 s | 40.976 s |

The half-weight relaxation reaches **32.179 s even as L→0**: U alone exceeds
its 9.394327-ms event allowance. Under that relaxation, extra vertical travel
would have to fall below approximately 0.174 mm even with instantaneous pawls,
versus this embodiment's 0.47 mm (and E-052's 0.45-mm middle-bound minimum).
For unloaded motion, strict <30 s requires lateral acceleration >27.412 m/s²
for the seat cycle or >64.220 m/s² for the clearance cycle before all omitted
costs. At 50 m/s² the seat cycle leaves only 3.463 ms per event on average
for grip, proof, settling, control and retries; at 100 m/s² the clearance cycle
leaves 3.078 ms. A residual average is an aggregate budget, not permission for
every contact to exceed a common-drive deadline. Neither case is accepted.

Sensitivity is explicit: triangular microtravel scales as sqrt(distance /
acceleration). Adding 1 ms to U/L costs 0.720/0.360 s per board for the
seat cycle, or 0.640/0.640 s for the clearance cycle.
These are shared-drive epistemic bounds, not independent cell distributions.
The h/s witness retains E-052's geometric error-envelope limitations; it does
not account for backlash, friction, deformation, roughness, wear or settling.
Increasing distances or reducing acceleration worsens these bounds; credible
shorter strokes or different sequencing requires changed evidence. No yield,
reliability, dynamics qualification or new manufacturing prior is inferred.

Retain the overlap escape conditions: merge unloading/approach into inter-level
motion, use offset/local grippers with independent support, prewithdraw while
independently held, or use a fly-through cam/multiple elevators. Such changes
must replay actual approach/departure coordinates, contact order, all held
columns, support continuity, unchanged-cell isolation and full-board time.
A shared elevator's microexcursion also moves every attached column; the
seat cycle no longer inherits the earlier no-excursion capture-policy result.
Geometry and a complete affordable selector remain prerequisites to promoting
these paths. No print or procurement. Stop nominal dwell refinement; reopen
only with a concrete changed support-transfer mechanism or evidenced drive.

Self-review: replay verifies event counts, all eight inter-stop distances,
initial/final height closure and agreement with the two closed-form totals;
independent constant-acceleration integration verifies both signs of each
vertical microleg. Sixteen explicit path cases and eight relaxed cases run
deterministically alongside the retained lateral-only checks. Closed forms
need no mesh/time-step study. This checks arithmetic and stipulated ordering,
not actual gripper/guide contact geometry or independent engineering review.
