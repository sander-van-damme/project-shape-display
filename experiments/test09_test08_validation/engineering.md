# What Test09 reduces, and what it cannot

Evidence words have their literal meanings: **calculated** is an equation;
**simulated** is an event schedule; **sourced** is a documented supplier claim;
**assumed** is an input awaiting evidence; **measured** requires a physical record.
All physical gates are currently **unverified**. `uncertainties.csv` is the
31-item canonical register, including thresholds and architecture consequences.
Values between an acceptance and a hard failure threshold are inconclusive and
do not permit scaling. Stage procedures below govern the required sample counts.

## Historical audit

Read the root target, architecture report, test guide, fabrication/miniature
context, backlog, and all Test08 documentation, parameters, BOM, sources,
analysis/checks/CAD/strength/plot scripts and blank measurement template.
Inspected historical **mechanism source**, not only Test08's historical table:

| Source | Finding relevant to Test09 |
|---|---|
| test01 `bolt-v3.scad` | 4 mm screw, 2 mm pitch, 50 mm length. Twenty rotations for 40 mm still require a qualified rapid coupling; printable screw memory does not make actuation free. |
| test02 `models/pixel.py`, `models/grid.py` | Explicit slider widths and guide cavities are useful for process coupons; no actuation or retention evidence. |
| test03 `actuator.scad` | 6 mm body exceeds target pitch. Screw/coupling dimensions are designs, not friction measurements. |
| test04 `frame.scad` | 4.64 + 0.44 = 5.08 mm spacing; long thin guide walls already present. |
| test05 `actuator.scad`, `calibrate_rect_tube.scad` | 4.4 mm hollow body, 3.2 mm screw and 3 mm lead; clearance sweep precedents. No empirical fit tolerances. |
| test06 `test-strip.scad` | Comments and geometry explicitly cam an entire release strip when one column rises. Cannot reuse this as independently holding latches. |
| test07 `grid.scad`, `caddy.scad` | One comb per row still couples cells in that row. Feeders are schematic; 12.6 mm motors in two ranks cannot pack at 5.08 mm pitch; 5.1 mm tube OD also exceeds it. Multi-row speed therefore deserves a fresh screen with different local retention. |

Test08's six checks were rerun and passed. Its optional NumPy 1.26.3 cam-strength
screen was also rerun: 4.96488 N converged ideal critical load, with the uniform
beam check within 3.3e-9 relative error. These check model behavior, not parts.
Its nominal schedule was independently reconstructed rather than copied. CAD
reuses the historical source by generating a local snapshot, records its hash,
and rechecks its specified contacts. No historical source is edited.

## Return and fabrication

The historical relieved-body volume predicts solid **2.069 g** and hollow
**0.997 g** at assumed density 1.24 g/cm³. Their measured values remain blank.
The 2× return margin requires drag below **10.15 mN** / **4.89 mN** respectively.
Test09 does not assign a friction coefficient. Normal forces from bow, guide
misalignment, layer ridges, lateral load and contamination dominate; a guessed
PLA-on-PLA coefficient would not establish breakaway force.

The fit sweep subtracts combined width/bore error and `12*tan(tilt)` from total
body clearance: a dimensional sensitivity screen, not a printer tolerance.
Fixture tilt relative to gravity and misalignment between guide tiers are
different experiments. Tilting the board changes weight components and contact;
offsetting a guide changes preload and can jam even a vertical board.

Increasing clearance at fixed 4.68 mm width consumes already thin webs:
0.05/0.10/0.15 mm per side leaves 0.30/0.20/0.10 mm webs. A 4.48 mm body with
0.10 mm clearance leaves 0.40 mm webs at unchanged **5.08 mm pitch**, but lowers
surface fill from 84.87% to 77.77% and reduces weight. It is an experimental
fallback, not a silent Test08 improvement; full follower relief/toe dimensions
and mass must be revised if selected. Do not insert the wider follower in it.

First compare PLA solid followers printed upright and on their side, 0.4 mm
nozzle at 0.12 mm layers, then 0.2 mm at 0.08 mm layers for the fine guides.
These are starting slicer settings, not qualified recipes. Record actual wall
paths in the slicer; a missing or single fragile web fails even if STL is valid.
Set 100% infill for the solid comparison; weigh it because actual infill/voids
change mass. No CF-filled material is assumed usable with the 0.2 mm nozzle.

If gravity fails, first reduce guide preload/contact length and test solid
bodies. Individual ballast adds lift mass and assembly. Even 0.02 N return
springs add 128 N to the platen; 0.1 N adds 640 N. Printed springs require life
and creep testing. A common pull-down cannot pull an individually stuck column
after other columns stop unless a releasable individual linkage is added.
Positive return is a new mechanism; latch/shared-motion alternatives also need
an explicit down-reset solution and do not automatically solve friction.

## Rotor, detent and coupling

The calculated toe half-envelope is **23.50°**. Four levels leave **21.50°**
nominal margin and 13.33 mm steps; five leave **12.50°** and 10 mm steps; six
leave **6.50°** and 8 mm steps. Six also needs up to 6° correction from 18° full
steps; there is only 0.50° geometrical reserve at a ±6° seating gate. Eight,
nine and ten levels have negative nominal toe clearance. Four and five align
exactly with this motor's full steps. Five remains a useful hypothesis; four
is the first fallback. Height resolution is a product tradeoff, not free margin.

Original individual cell parts fit conservative ±2.50 mm XY envelopes, leaving
0.08 mm between neighboring envelopes at 5.08 mm pitch for arbitrary heights
and rotations. This is only a rigid nominal bound: shared guide plates are
intentional connections; new detents, retention, frame and elastic deflection
are excluded. Stage B's mixed-height checks and Stage D's integration gate are
still necessary. The scripts reject changing the baseline grid/stroke without
revising the coupled historical geometry/mass and reliability screens.

The Test08 wheel has 0.25 mm radius cutouts centered on a 1.65 mm radius. A point
follower reaches a notch only within `asin(0.25/1.65)` = **±8.72°**. Elsewhere
the circular rim supplies no deterministic angular restoring gradient. A finite
tip alters the boundary but does not demonstrate ±18° correction. The historic
notch is therefore not evidence for the missed-step gate.

New wheel: `r(theta)=1.65-0.10*(1+cos(5 theta))` mm. A replaceable PLA leaf
10×1×0.45 mm with assumed 0.05 mm preload rides its continuous scallop. Ideal
basin half-width is 36°, enough geometrically to investigate one missed step.
`F=E*b*t³*delta/(4*L³)` and `T=-F*dr/dtheta` give only **0.00298 mN m** peak
restoring torque at assumed E=1500 MPa. Maximum strain is about **0.169%**.
Neither is a material allowable or measured holding torque. Friction can stop
it well before center, and nib geometry changes the torque curve; measure both
directions and release from multiple angles. Bench leaf is flat for controlled
layer orientation. A vertical axial leaf is a possible packing change, but its
clamps, home lug, thrust stack and head still need an integrated full-pitch CAD
check before Stage D. The flat bench assembly is explicitly **not tileable**.

A further warning: an assumed 1° circumferential plateau slope under 1 N at
1.35 mm radius would produce `F*r*tan(slope)` = **0.0236 mN m** disturbance,
about eight times the candidate leaf's peak restoring torque. Even 0.1° is
comparable. This is a sensitivity calculation, not a measured printing error
or predicted slip (contact friction may resist it). Test loaded angular drift
and vibration; the unloaded capture test alone cannot qualify passive memory.

Toe contact pressure remains roughly 3.11 MPa at 1 N / 15.54 MPa at 5 N.
The Test08 cam beam screen predicts 4.96 N with an ideal clamped root and no
eccentricity or creep; it gives **no acceptable 5 N margin**. Do not treat
coupon STLs or the proposed detent as repairing this weakness. Toe edge wear,
bridge layer failure and cam bow are Stage B stop conditions.

An 18° motor electrical step is not a rotor encoder. A friction coupling slips
at the hard stop and can leave arbitrary relative phase. Home 22 pulses toward
the stop; record actual rotor angle on reversal, including backlash, first-step
motion and deliberate slips. A motor rotor that turns successfully while the
face slips can silently miswrite. A detent can only rescue errors inside its
**measured** attraction range.

The bench coupling uses a replaceable 2.3 mm face pad against the Test08 drive
disc, an axially guided motor carrier and external compression spring. Test
0.1, 0.2, 0.5 and 1 N preload, 0.5–1 mm disengagement travel; these are trial
values. With effective radius 0.75 mm and required torque 0.15 mN m,
`mu*F >= 0.20 N`; no mu is presumed. Measure slip torque, running torque and
axial force together. Require mechanism torque < half measured motor running
torque, a non-slip write, and controlled stop slip without damage. A narrow or
empty slip window rejects the friction coupling. At 0.5 N per channel the head
must distribute 40 N, not merely align eighty unloaded shafts.

## Timing and reliability

`worst_schedule.json` covers reset/reference, 41 mm raise, 79 accelerated index
moves, 80 complete engage/home/write/disengage/seat transactions, park, lower,
settle, inspection and recovery. All-low is still rewritten. High→low,
low→high, inverse checkerboard and one-high-per-row all use global unloading;
old heights cannot reduce this stroke. The transition cross-product is a
schedule test, not a dynamic collision or successful return simulation.

The result matches Test08: **26.251 s**, with **0.749 s** to 27 s. A 1 s final
inspection alone loses the engineering target. Doubling coupling time to
50 ms each way loses the hard 30 s limit. The 540-case sweep covers rates,
coupling, all three settling durations, acceleration
and inspection jointly; favorable points are assumed, never a measured region.
`qualify.py` uses recorded maxima ×1.2 and minima /1.2, not an optimistic average.
At least 1000 rows spanning cold/warm/worn/misaligned conditions are needed even
for its **conditional timing** gate. A real measured operating region is absent.

For independent cells, `P(perfect map)=(1-q)^6400`; for separate row and module
events the screen multiplies by `(1-q_row)^80*(1-q_module)^64`. These independent
event classes are a simplifying assumption; clustered wear and shared supply
faults invalidate simple pooling. A 99% perfect-map goal needs cell q≤1.570e-6
even with no correlated faults, and **1,907,667** zero-failure independent trials
for a one-sided 95% bound. Eight channels ×10,000 gives a 3.745e-5 bound under
independence, far short of this goal. Count row transactions separately.

Detection is therefore required for a credible larger prototype unless far more
reliability evidence appears. A camera/fiducial/lighting allowance is included,
but a top view can miss height errors and occluded columns. Test oblique views
or rotor fiducials with known false states; no coverage or latency is claimed.
Current sensing/driver fault lines catch rail and electrical faults, not all
stuck followers or slipping couplers. Detected failures keep READY false;
aborting a map is **not** successful <30 s readiness. Time a retry including
unload and inspection. Unbounded/manual repairs fail the product timing gate.

## Structure and lift

13.24 kg of calculated solid columns plus 2–6 kg assumed platen gives
**15.24–19.24 kg** moving mass before user payload. Models assume a cleared board.
Use 4 kg platen and 10 mN drag as an illustrative case: **236.57 N** peak lift.
Eight simply supported hollow beams, 20×30 mm with 2 mm walls, each taking 1/8
of distributed load, give **0.799 mm** sag over 406.4 mm at assumed E=1500 MPa.
At 203.2 mm support spacing the same line load gives **0.0499 mm**. The flat
2 mm strip's linear result is outside small-deflection validity by orders of
magnitude: it establishes failure of that idealization, not a literal sag.

These are 1-D beam bounds. They exclude module joint compliance, shear,
torsion, screw mounts, creep and load redistribution. Four corner screws do
not magically give every interior beam end a rigid support. Candidate: 64
10×10 guide tiles on a two-direction box grid, with 9 support nodes on a
203.2 mm grid or 16 closer nodes; compare with deeper beams on four screws.
Printed 203.2 mm half beams and two bolted splice plates allow a worst-position
joint test before a whole grid. Modular assembly needs measured datums and
shimmed tile registration, not assumed rigidity across bolted PLA joints.

`lift_drive.csv` explores 4/9/16 screws, 2/4/8 mm leads and 0.2–0.5 efficiency.
At 35 mm/s those leads need **1050/525/262.5 rpm**: a finer self-locking candidate
trades speed and motor torque. Self-locking is **not** inferred from lead alone.
One synchronous belt needs tensioners, shaft thrust bearings and either reliable
braking or a normally engaged catch. 10° skew with 8 mm lead makes 0.222 mm
height error, nearly the entire flatness budget. A motor's holding torque is
not its available torque at operating rpm. Measure loaded torque with a 2×
reserve. Reprice nine/sixteen screws and any deeper structure; current BOM has
only four and therefore is not a qualified structural purchase list.

The realistic Test09 allowance including brake, inspection, freight/import
reserve and contingency is **$1089.65**, optimistic **$411.60**, conservative
retail scenario **$5993.85**. Even realistic non-motor hardware exceeds $500
after contingency. This does not prove no custom cheap implementation exists;
it rules out qualification of the currently specified/allowed one. Cost and
physics must be met in the same design. Full-scale purchases are not justified.
