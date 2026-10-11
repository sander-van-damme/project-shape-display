---
status: complete
builds-on: [E-169, E-167, E-099, E-051]
---

# Complementary gates lose pickup to the retaining pocket and shared-plate crossing

**Reject the tested rigid complementary-gate embodiment; retain periodic pickup
as a changed sharing axis.** Rotating the column to exchange a fixed gate for
an orthogonal moving gate could remove a separate pickup slider and acquire
columns at different heights simultaneously. But every nominal coplanar pickup
pose hits the existing angular-retention pocket. Omitting the pocket loses
retention, gives tiny initial bearing, and permits a bounded size/tilt case
where the cap collides before pickup. A nearby moving gate also cannot traverse
the fixed plate. These are distinct geometric failures, not a rejection of all
shared power or column rotation. No machine selection or printing follows.

Input main `6f6b8ee`; LAB-278. Reproduce:
`python3 tools/curated-experiment-checks/E-170/transfer.py`.
Standard-library finite polygon clipping, independent separating-axis checks,
analytical set inclusion and optimistic schedule arithmetic. Self-review only;
no contact dynamics, calibrated manufacturing prior, material allowable,
fabrication CAD, sourced component price or physical measurement. JSON is
reproducible output and is not retained. Dimensions/rates are explicit scenarios
inherited from E-169/E-099 or stated below, not qualified X1C capabilities.

## Changed causal combinations and controls

| Combination | Selection, motion, retention and load path | Disposition / unresolved burden |
|---|---|---|
| Complementary gates | Fixed x-slot bears a y-oriented lug; moving y-slot bypasses it. Independent column rotation transfers the load to the moving gate; shared axial motion transports selected columns. Return rotation deposits on the fixed gate. | Column angle doubles as pickup selection. Tested fixed pocket prevents initial rotation into pickup. |
| Pocketless microturn | Turn only a few degrees while caps are coplanar, acquire on moving plate, lift into the interlevel gap, finish turn and translate. | Small nominal pickup exists, but removes angular retention and fails an allowed clearance scenario. Torque selector must remain engaged/retained; no free detent. |
| Local rotary-to-axial transfer | A helical/ramped gate or captured rotary writer first lifts the selected column, then exchanges supports. | Materially changed escape, not generated here. Must produce actual loaded lift/reseat before cap collision, without turning into an independent axial head by assertion. |
| Nonrotating pawl/deck | E-098 pad carries column while separately written ground dog releases/reseats. | Avoids cap turns but retains two moving support selectors/cell and repeated scans; E-099 already screens grouping. |
| Independent head | E-167 captured rotary-linear head, or E-094 pawl head. | More independent motion, fewer sharing constraints; complete cost/support/readback still open. |

This is functional recombination of periodic lugs with orthogonal pickup gates,
not a new quarter-turn principle. E-051's equal-offset heads acquire at each
old height; **repeated lugs put a pickup at the same gate datum for every discrete
height**. That changed interface is why this does not simply repeat E-051 or
E-099. No literature search or global saturation claim is made this session.

## Finite pickup geometry and the pocket contradiction

Use E-169's lug half-length L=2.15, half-width W=1.2, radius 1.48, 4.6-square
2-thick cap, 10-mm level spacing, fixed central half-aperture A=1.68,
slot/pocket half-width S=1.4 and .4-high pocket rails. Base plate thickness 1.2;
pitch 5.08. Set the fixed bearing plane at z=0 and initially the moving plane
at z=−10, bearing on the next lower lug. That requires an added lower station.
Ideal stem guidance and torsional access are granted, not geometry results.

Let δ be rotation away from the fixed seated y orientation toward the x transit
orientation. Moving plate contact starts when
`L sin δ + W cos δ > S`: **δ>5.48462°** nominally. A coplanar selected cap first
hits its unchanged aligned neighbor at **13.72406°**, from
`(d/2)(cos δ+sin δ)+d/2=5.08`. Thus ignoring the pocket suggests an 8.23944° window.

Generated fixed base, pocket rails and 90°-rotated moving base are clipped against
the actual rotated lug polygon. Throughout that cap-safe interval, lug x extent
is less than A. Moving support therefore requires **|x|>S and |y|>A**, exactly
the fixed raised-pocket footprint. Any positive moving bearing area means
positive-volume penetration of the .4-high fixed rail by the seated 1.2-thick
lug. The rails are not unloaded clearance: they physically block the rotation.
32/128/512 angular intervals find 20/77/308 positive pickup poses and **zero
unblocked pickup poses**. Set inclusion establishes the continuous result;
those sample counts are checks, not the proof or reliability statistics.

At δ=0 the moving gate bypasses the column, so it cannot supply the preliminary
release lift. Raising every column first violates local isolation. A selected
local lift/cam, retractable pocket or separate pickup member changes the tested
mechanism and must be counted. A .4-mm release alone also does not clear a
2-mm-thick neighboring cap for an unrestricted turn; E-167's interlevel path
used 2.3 mm. A powered torque channel is not automatically an axial load path.

## Pocketless alternative: bearing and manufacturing counterexamples

With pocket removed, nominal δ=10° provides **.066028 mm²** pickup area; at the
cap-touching limit it is .083188 mm². Mean pressure at that limiting pose is
1.202/12.021/120.209 MPa for .1/1/10-N moving-load scenarios. These are geometry
calculations, not allowables, a load requirement, or a claimed maximum area.
The cap-touching pose has no positive clearance. Eccentricity, contact peaks,
root deformation and guide moments can worsen the mean-pressure diagnostic.

Let e bound each lug/gate edge and relative cap registration; grant an aligned
active column. Use E-169's neighbor guide half-play c=0 or .025 over 25 mm.
Conservative whole-cap drift is `c(1+2*44/25)`. These coherent scenarios can apply
to a bank; no independent-cell averaging or probability distribution is used.
One admissible counterexample shrinks lug dimensions by e and enlarges the gate
slot/aperture by e, with zero lug-to-gate offset. Caps grow by e per half-edge.

| e / c mm | Cap envelope limit | Centered adverse pickup onset | Adverse area at cap limit, mm² |
|---|---:|---:|---:|
| 0 / 0 | 13.724° | 5.485° | .083188 |
| .025 / 0 | 11.128° | 6.994° | .041438 |
| .050 / 0 | 8.746° | 8.567° | .000235 |
| .025 / .025 | 7.742° | 6.994° | .004887 |
| .050 / .025 | 5.570° | 8.567° | 0 |

The last rejection also uses an **actual horizontal section** of the neighbor's
tilted cap at z=43, where its full width is present. Exact section collision
begins at **5.62421°**, still before 8.56709° pickup. Thus this is not merely
failure of a conservative sufficient clearance inequality. ±.00001-radian
holdouts verify the section collision with separating axes.

The source also enumerates 64 edge/offset corners per scenario. Their minimum
is **not** a bound over the interior: the centered adverse case can have less
area than all offset corners. Keep this counterexample to corner-only sampling.
At e=.075 the centered pickup already loses to cap clearance without tilt;
that bound also exceeds E-169's original .2-clearance slot budget. No claim
about actual process prevalence follows. Bias, layer/first-layer shape, warp,
roughness, anisotropy, creep, wear and assembly may change bearing/retention;
none is fitted here. Extending stems/guides invalidates inherited structural
bounds rather than qualifying the new machine.

## Shared-plate crossing and full-display accounting

Two full-pitch orthogonal base plates have **4.8848 mm²** common solid footprint
per cell, independently `4[(5.08/2−S)²−(A−S)²]`. With moving home at −10, a
10-mm upward stroke places the plates together, giving **5.86176 mm³** rigid
intersection. A 40-mm lift cannot pass through that state. Interdigitated forks
or laterally routed supports would be new geometry; holes alone do not fix it.

Keeping the entire moving plate below the fixed 1.2-thick base needs home
separation >41.2 mm. With these congruent 10-mm lug stations, the minimum is
**50 mm**. Fixed contact uses stations 0…40; moving contact uses −50…−10:
**ten stations/cell, 64,000 lugs/board**, versus five and 32,000 in E-169.
The bare column extends at least 94 mm from the lowest lug bottom to cap top,
before material below that lug/guide engagement; its full 40-mm swept extent is
at least 134 mm. The original lower guide at −25 lies in the moving plate's
−50…−10 sweep; it must be relocated or redesigned. No extended-stem stability,
frame stiffness, plate routing or repair-access pass follows.

To expose rather than hide throughput, grant a repaired transfer, independent
retained angular selection, sufficient lugs and collision-free guidance.
An optimistic protocol separates raising/lowering. Periodic pickup lets all
old heights acquire together; release groups depend on displacement 10/20/30/40.
One arm plus four deposit scans per sign gives **ten row scans**, not E-099's
twenty. It grants one complete local service slot per logical write; an actual
two-stage pickup may need more scans. For B equal row banks, n=80/B, row pitch
5.08, v=200 mm/s, a=5000 mm/s²:

`T = 6 + 10 n slot + 10(n−1)move(5.08) + 8move(10) + 2move(40)`.

The 6-s allocation must cover preparation/registration, uncounted microtravel,
proof, bounded retry and final settling; it is not an earned overhead bound.
Logical all-pairs reach is checked; physical transfer is explicitly failed.
No overlap is credited. Under a .1-s slot:

| Banks | Rotary setting channels | Optimistic T, s | $/complete channel ceiling, $250 elsewhere/free cells |
|---:|---:|---:|---:|
| 1 | 80 | 137.562 | 3.125 |
| 2 | 160 | 72.062 | 1.5625 |
| 4 | 320 | 39.312 | .78125 |
| 8 | 640 | 22.937 | .390625 |
| 16 | 1280 | 14.750 | .1953125 |

At slots .02/.05/.1/.2 s the first passing tested B is 4/4/8/16. These are
conditional allocations, not hardware timing or a comparison at identical
proof assumptions to E-099. At B=8, $.02 bought/cell reduces the complete
channel ceiling to **$.190625** under $500; under $400 with free cells it is
$.234375. Drives, moving plates, angular capture/retention, accessible readers,
wiring, power, guides and registration must actually fit those allocations.
No priced affordability pass follows. Shared lift removes independent axial
motors only by adding moving gate sites, long periodic columns and retained
rotary access. At 10 s/site, one repeated assembly operation alone is 17.8 h.

Unchanged θ=90° columns nominally bypass the moving gate and remain grounded.
But a wrongly armed 10° neighbor in the pocketless alternative has .066028 mm²
pickup contact: the plate can lift it by its own 2.3-mm release movement. This
is a geometric half-selection witness, not a force-qualified lift prediction.
Pocket retention prevents that fault and also prevents intended pickup.
Actual local displacement, common plate deflection/vibration, arbitrary-map
verification and transient input-loss arrest remain unproved. Read actual
height, angular state and support before detaching; failed proof must retain
support and stop/retry the bank. Such sensing/recovery is an obligation, not a
perfect readback grant. False acceptance p still means 6,400p expected misses
without independence; p and common-mode bias remain unknown.

## Decision and next discriminator

Stop the unchanged-pocket paired-plate design and the close-spaced full-stroke
plate. Do not add detailed actuator CAD or print this geometry. Preserve the
periodic-lug acquisition idea because it genuinely removes old-height scans,
but no complete service advantage is established over pawl/direct controls.

Reopen with **finite selected rotary-to-axial transfer at a fixed datum**, or a
materially different nonrotating periodic pickup. The next useful test is whether
a grounded cam can provide the required short release lift, positive bearing
and reseat within the neighbor-angle envelope at bounded torque/friction,
without a second independent axial channel; include unchanged cells and both
motion signs. Reject a geometry before system optimization if it cannot support
that transfer. This is a new contact/energy discriminator; another plate-spacing
or angular sampling sweep cannot repair the established failures. No additional
budget, staffing, purchase or physical experiment is needed.

Self-review: analytical pocket-footprint inclusion; exact plate overlap formula;
clipping/SAT threshold agreement; cap prism section; zero-angle/90° bearing
limits; 64/256/1024-point-per-axis independent area integration (final area error
.0000242 mm²); three angular grids; all 25 logical old/new height pairs. These
checks validate the reduced calculations, not hardware or independent review.
