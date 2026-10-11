---
status: complete
builds-on: [E-165, E-056, E-115]
---

# Shared comb hooks trade easy release against load-induced peeling

**Retain shared stationary combs as an assembly option; do not admit the thin
unbacked hook as a friction-independent 10-N route, or its fixed rear-stop
repair.** A hanging spring finger with a positive hook avoids E-165's moving-foil compression, but its offset rack contact
peels it outward. A finite frictionless-contact model loses overlap near **1.758 N**
for the nominal metal-like .2-mm finger, versus a 10-N comparison load. A .4-mm
metal-like finger retains a conditional ~14-N geometric limit at the price of
~2.59-N unloaded release. Neither is a qualified spring, support or machine.
The tested rear stop obstructs commanded release. Positive seats remain useful;
this failure does not reject flexure latches or shared-sheet assembly.

Input main `85d7ede`; LAB-270. Reproduce with
`python3 tools/curated-experiment-checks/E-166/probe.py` (Python + NumPy).
Evidence: finite-section generation, quasistatic discrete-elastica/contact
simulation, analytical holdout and self-review. No physical measurements,
calibrated process priors, fabrication CAD or independent review. JSON output is
disposable. No printing or purchase is proposed.

## Mechanism and comparison

The independent search axis is **sharing the fixed return/support sheet**, rather
than moving laminate leaves. Each comb has a common grounded spine and separate
downward fingers. Each finger ends in a formed horizontal hook under a rack tooth;
its own bending provides unloaded return. A transported bidirectional head takes
the column load, lifts clear, pulls the hook sideways, moves the rack to another
tooth, releases the hook, seats/proves support and withdraws. Unchanged hooks stay
engaged. Five teeth at 10-mm spacing give 0/10/20/30/40-mm terrain states in this
embodiment; this is a design choice, not a new product height requirement.

| Combination | Benefit / unresolved or failed condition |
|---|---|
| Hanging integral comb hook | One fixed sheet can combine 40 returns/supports; tension rather than moving-foil feed; load contact migrates toward the toe and can run off |
| Same hook + fixed rear abutment | Can oppose outward displacement, but the tested solid also blocks the required release path; bypass or independently movable stop is owed |
| Side-wing-supported crossbolt | E-054/E-056 can route service load into grounded shelves; a spring comb could supply return, but does not remove their repeated guide/contact obligations |
| Broad jaw / laminate | Continuous height controls; E-148/E-165 retain local clamp reactions, release and proof; no winner follows from comparing hook force with clamp normal force |

This is a manufacturing/mechanism recombination, not a new positive-lock
principle. A-010's five-position aperture slider is not reopened: this hook is a
binary lock at a fixed datum, with height encoded in the translating rack.
[Covestro's manufacturer design guide, pp. 3–8](https://solutions.covestro.com/-/media/covestro/solution-center/brands/downloads/imported/1557220896.pdf)
provides the snap-hook analogy and emphasizes flexural loading, root geometry
and strain-dependent material response. It does not establish endurance or
properties for X1C PLA or our formed sheet. Accessed 2026-10-11. This source search
and the assembly-function inversion do not establish broad search saturation.

## Finite contact model

Coordinates are x across columns, y toward the rack, z downward; mm and N.
Nominal finger: length L=12, width in x=2, thickness in y=t=.2; grounded at
(y,z)=(0,0). A rigid toe of length e=1 continues perpendicular to the finger at
its bottom. The rack's inner corner is at y=r=.4, giving .6 initial overlap.
The rack tooth extends to y=1.6, thickness 2; a web can occupy y=1.6…3.2.
Finger and toe are finite-thickness polygons; the ideal right-angle joint and
rigid toe omit bend-radius compliance, stress concentration and forming details.
The spine can cross x at y=[−.2,.2], z=[−2,0], clear of the rack's vertical sweep
in this nominal section. Frame attachment/stiffness are not solved.

The beam is inextensible, planar, linearly elastic in curvature, with finite
rotation θ(s), fixed θ(0)=0, and EI=Ewt³/12. Downward service load F is carried
by a rack corner sliding frictionlessly along the hook's upper surface. Rack
lateral guides hold y=r and react the horizontal contact force. With endpoint
coordinates y,z and terminal angle θL:

`a=(r−y)/cos(θL)` is the material contact coordinate along the toe;
`zcontact=z−(r−y)tan(θL)`; contact exists only for `0≤a≤e`.

The minimized potential is
`U=(EI/2)∫θ'² ds + F[L−z+(r−y)tan(θL)]`.
Thus `H=F tan(θL)` is the horizontal force on the finger, **not silently zero**.
For negative θL it increases outward peel. Constant load at a fixed material
point, or counting positive teeth without solving the contact, misses migration.
The rack guides carry −H; their clearance/friction/compliance remain obligations.

The source uses trapezoidal centerline integration, segment curvature energy,
Newton steps with energy line search and a positive-definite Hessian check.
Continuation starts unloaded and stops when contact exceeds the finite toe or
a stable branch cannot be found. All reported cases end in **toe runoff**, not
solver failure. No claim is made about other equilibria after contact is lost,
dynamic arrest, impact, torsion or postyield behavior. Axial extension/shear,
root compliance, friction, local indentation and hook bending are model discrepancy.

For unloaded release a horizontal end force H replaces the rack load; minimize
`(EI/2)∫θ'² ds − H y`. Solve H so the entire toe clears the rack by .1 mm.
The nominal result is H=−.323460 N, tip y=−.696210, z=11.975734, θ=−.087091 rad.
Maximum body y=.300000. With the rack lifted 1 mm, 65 release phases have no
positive-area finger/tooth intersections; reversing those poses gives closing.
Once withdrawn, the y separation excludes every intermediate 40-mm rack
translation and all 20 unequal five-state moves. The release-phase checks are
sampled, not a continuous swept-volume certificate. They assume a load-bearing
head and do not construct head acquisition, actuation or dynamic support transfer.

Loaded finite sections at F=.02/1/1.75 N also have no tooth penetration and actual
contact lies on the toe. This is a unilateral corner/face construction, not an
ideal no-slip pin. Tooth height follows zcontact, so elastic seating sag is real.
Adjacent x-width-2 fingers at 5.08-mm pitch have 3.08-mm nominal lateral separation;
rigid-frame independence is geometric only, not a regional-disturbance result.

## Results, sensitivity and independent checks

| E scenario (MPa), t (mm) | Last supported / next runoff load (N), 64 segments | Unloaded release (N) | Maximum release bending strain |
|---|---:|---:|---:|
| 200,000, .1 | .21875 / .21991 | .04043 | .0721% |
| 200,000, .2 | 1.7500 / 1.7593 | .32346 | .1441% |
| 200,000, .4 | 14.000 / 14.074 | 2.58768 | .2883% |
| 2,000, .4 | .14000 / .14074 | .02588 | .2883% |
| 2,000, .8 | 1.1200 / 1.1259 | .20701 | .5765% |

These modulus values are explicitly metal-like/polymer-like scenarios, **not
material assignments, sourced allowables or measured fatigue/creep limits**.
Even the high-force branch may yield or fail at the formed root before runoff.
The unbacked .2-mm metal-like branch geometrically holds 1 N nominally, not 10 N;
the .4-mm branch escapes that particular 10-N failure. A thick .8-mm polymer-like
finger has L/t=15, so neglected shear/short-beam effects deserve greater caution.

For the nominal section, refinement (segments; dimensionless load increment
Δ[FL²/EI]) gives runoff brackets in N:
32;.01 → [1.74074,1.75926], 64;.005 → [1.75000,1.75926],
128;.0025 → [1.75463,1.75926], 256;.00125 → [1.75694,1.75926].
These are numerical continuation brackets, not rigorous continuum error bounds.

An independent small-angle beam-column solution includes both axial tension and
the sloping contact normal. At runoff,
`r/e=cosh(λ)−λ sinh(λ)`, `λ=L sqrt(F/EI)`.
It gives λ=.978792 and F=1.77414 N, within 1% of the finite-rotation result.
A vertical-only fixed-material-load approximation instead gives
`r/e=sech(λ)`, a much less restrictive ~4.55 N; it omits the sliding normal force.
The source checks energy gradient/Hessian by finite differences, positive
stability pivots, zero-load behavior, infinitesimal `y=−FrL²/(2EI)` and
unloaded `y=HL³/(3EI)`, plus finite polygon touching/penetration controls.
No solver success is treated as material or hardware validation.

Thirty-two coherent manufactured-bank corners vary E=160,000/220,000 MPa,
t=.18/.22, L=11.5/12.5, r=.3/.5 and e=.9/1.1 mm. Last-supported load spans
**.73654…3.24741 N**; every case reaches toe runoff. These are alternative
bounded scenarios, not random cells, a calibrated uncertainty interval or yield.
They combine stock thickness/modulus and relative forming/registration bias;
a common translation cancels, while relative rack/spine offsets do not.
The nominal 1-N disposition therefore changes with the assumed bank corner.
Corners assess the contact model, not every manufactured swept-clearance state.

Cutting burrs, residual curvature, bend radius, local plasticity, toe wear and
roughness/friction are not covered by those five parameters. Printed spine/rack
hole shrinkage, layer/first-layer bias, warp, orientation-dependent stiffness,
interlayer weakness, creep, fatigue and assembly alignment remain uncalibrated.
Contact friction could delay runoff or prevent return; the zero-friction result
does not reject friction-assisted retention. No X1C resolution is substituted
for accuracy and no zero-failure reliability claim follows. A real spring stock or PLA build needs its own constitutive data.

## Backing, board accounting and decision

The explicit rear stop fills y=[−1,−.2], z=[11.8,12.8], over the finger width.
It intersects the generated unloaded release path in **55/65 phases**, first at
15.625% of commanded force. At full withdrawal the endpoint has risen only
.02427 mm. A stop covering this tip-height band cannot both block outward peel
and permit the same sideways motion merely because the rack was unloaded.
This is a finite obstruction of the specified block, not rejection of shaped
cam/bypass, retractable stops, side wings or an additional degree of freedom.
Those need new geometry, grounding and control; E-054/E-056 already expose the
side-wing alternative's guide/contact burden. A backed solution earns no free
return path by being called a positive stop.

Forty fingers fit a 203.2-mm-wide nominal blank. Two combs/row ×80 rows means
**160 sheet placements**, versus 6,400 separately installed spring hooks. With
assumed 15-mm blank height including toe/spine allowance, allocated stock is
.48768 m² before fixtures, kerf, forming, rejected pieces or spares. This is a
40× placement-count reduction, **not measured assembly time or a production
blank layout**. It retains 6,400 elastic fingers, formed toes, rack engagements
and their load cycles. A defective finger can require replacement of its 40-cell
comb while a fixture supports those columns. Common spine deflection/bias can
couple a module; distributed grounding remains necessary, as E-165 illustrates.

Purchased budget remains `Cshared+H*chead+6400*ccell<500`. With a hypothetical
$250 elsewhere, each complete resident purchased bundle must average <$0.0391;
no quote or BOM pass. The sheet does not replace heads, reversible drives,
positive capture, local opening tools, guides, readback, wiring or power.
At the inherited optimistic `T=6+ceil(6400/H)*service`, service=.45/.50/.55 s
requires H=121/137/149 for strict <30 s. Hook unload/retract/return/proof has not
earned those allowances. Registration, transport, settling and a bounded retry
remain included obligations, not discounted preparation. No time pass follows.

Proof must distinguish actual rack/support seating from a closed-looking finger.
Failed proof keeps the head engaged, retries once under support, then stops the
module. Power-loss return may meet a moving tooth or stick; passive finger return
is not proven arrest. A falsely accepted proof can drop a column: assumed
per-cell false acceptance p gives 6,400p expected misses without requiring
independence, but no p is qualified. Regional isolation, life and recovery are
still open. No final machine is selected.

**Stop** the thin unbacked hook as a friction-independent 10-N route and the
specified fixed rear block; retain the thicker spring branch only as a conditional support/assembly control.
Next discriminate a load-backed tongue with release orthogonal to its service
moment, or a shared return attached to the existing side-wing crossbolt. First
construct the finite contact and release route and demonstrate an inventory
advantage; if it merely recreates E-054, switch to a different functional axis.
This question has more value than calibrating a stock modulus for a blocked path.
