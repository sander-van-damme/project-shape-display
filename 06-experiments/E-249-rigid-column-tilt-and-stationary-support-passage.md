---
status: complete
builds-on: [E-167, E-169, E-173, E-248]
---

# Whole-column tilt changes stationary-support passage, but does not supply guidance

**Park the tested rigid-column shunt before guide, pocket or head detail.** Pitch
rotation about the cap can clear stationary positive supports without a resident
hinge or cap swivel. A nominal finite section clears all twenty unequal height
transitions. However, its 142-mm stem leaves only **.05360 mm** of additional
routing margin after an assumed **.30-mm combined gap-error allowance**, and an
ordinary upper guide collides. The changed principle is real; a competitive
complete machine has not been established. No printing is justified.

Input main `2a55395`. Reproduce with standard Python:
`python3 tools/curated-experiment-checks/E-249/screen.py` (imports E-167's convex
polygon intersection). Evidence: **calculation, nominal rigid-section enumeration
and bounded envelopes; self-review**. No contact dynamics, CAD, process priors,
priced BOM, measured load capacity or physical qualification. Five levels
0/10/20/30/40 are a comparison grammar, not a product resolution decision.

## Reconstruction and causal comparison

| Interface | What remains supported / actual burden |
|---|---|
| E-248 withdrawing row comb | U receives two handoffs; fixed rigid partitioning needs singleton releases for arbitrary masks. This is not a universal impossibility proof. |
| E-167/E-169 bayonet | Individual column turns through a fixed gate; U can stay seated. Interlevel cap turning and checkerboard scheduling avoid some collisions, but wider bearings leave .03668-mm envelope margin in the stated .05-mm edge scenario. Retained rotary-linear capture remains unbuilt. |
| E-173 lane-addressed dog | A stationary selected dog admits other teeth in separate lanes; it is still a moving, retained per-column target selector. E-174/E-175 add guide, keeper and access failures. Not a simple fixed support. |
| Whole-column lateral translation | Removes local lock motion, but cap follows the same shunt. At downward crossing of the old seat, an unchanged same-height neighbor is coplanar. With 4.8-mm tops, displacement toward it cannot exceed .28 mm before errors. A .7-mm bearing overlap cannot clear. |
| Whole-column pitch tilt, tested here | Long lever moves the lower teeth farther than the cap. One rigid printed column; pitch selection/capture belongs to a reusable head. U's fixed rail need not withdraw. Long stems, motion-compatible guidance and loaded head capture are charged below. |

For the pure-translation branch, finite tooth thickness makes recentering before
crossing the old support ineffective: it restores the collision. Lift into an
interlevel gap does not remove the later crossing at the old height. Reducing
cap width to 4.6/4.2/4.0 mm permits nominal shunts .48/.88/1.08 mm, at planar
coverage 82.00/68.36/62.00%. This is a scoped necessary condition for whole-body
translation, not a universal ban on nonrectangular tops or separated caps.
Separating the top from the shunt restores 6,400 additional joints/interfaces.

## Finite changed section

Coordinates mm, pitch 5.08. The column cap underside is H0+h, with H0=100 and
h=0…40. A 2×2-mm stem extends 142 mm below the cap. The 4.8-square cap is 2 mm
thick. Five integral teeth, 2 mm thick/deep, extend from x=0 to b=2.2, at local
bottoms −H0−10j. A fixed rail per cell occupies x=1.5…2.54, z=−2…0 and the
same y contact interval. Upright bearing overlap w=.7; stem-to-rail gap g=.5.
Row/frame grounding is granted, not constructed.

A reusable bilateral head captures and lifts 2 mm, rotates the **whole column**
by .615925 degrees about the moving cap underside, translates to target+2,
rotates upright, and lowers onto its original stationary rail. A virtual pivot
is a prescribed trajectory, **not an installed hinge or a free head mechanism**.
With local (x,z), the rigid transform is
`X=x cos(theta)+z sin(theta); Z=H0+h−x sin(theta)+z cos(theta)`.
The head must carry load and moment until actual seating and height are proved.

Exact convex-polygon intersection, extruded through common y, checks the stem,
cap and all teeth against three rails and left/right neighbors at every one of
five heights. At 4/16/64 subdivisions per phase: **500/1,700/6,500 moving poses,
zero nominal intersections**. A no-tilt control has 36 intersections at coarse
resolution, including a lower tooth hitting the rail during ascent. The y extent
fits the pitch; no free orthogonal lane or missing tooth is used.

This is a section trajectory, not an assembled supported machine. U stays on its
own rail under the ideal head grant; neither rail deflection nor actual U motion
has been solved. Intermediate head support, angular capture and power-loss arrest
are **unconstructed**. Sample convergence checks bookkeeping, not all unmodelled
collisions. Conservative X envelopes bound translated teeth and neighbor routing;
turning at the 2-mm lift separates tooth bottoms from the rail. The top envelope
leaves .15864 mm after a **separate .10-mm total cap-gap error allowance**. Other
rows, head bodies, fixtures and guide solids are not covered by this cap result.

## Manufacturing envelope and explicit guide counterexample

Let E be the **total adverse error in a gap**, combining face dimensions,
relative registration and deformation. It is not a per-part standard deviation,
X1C capability or probability. Different interfaces need separate budgets; E
below applies only to support/body routing. Common bank bias can consume it at
every site. Perfect commanded angle is granted; additional angular error is unpaid.
For L=H0+42, a=1.5, b=2.2 and stem width s=2, sufficient margins are:

- Upright body/rail: g−E; bearing overlap: w−E.
- All teeth bypass the rail: `a−[b cos(theta)−(H0−2)sin(theta)]−E`.
- Whole stem stays right of the left neighbor's furthest tooth:
  `5.08−b−(s/2)cos(theta)−L sin(theta)−E`.

The latter is conservative across all z, not a necessary collision condition.
A one-dimensional bisection maximizes the minimum of these margins over 0…5°;
a separate .001° grid cross-checks the result. A negative envelope does **not**
prove every routed trajectory fails.

| H0 / stem length mm | Best angle | Minimum margin E=.10 | E=.30 | E=.70 |
|---:|---:|---:|---:|---:|
| 50 / 92 | 1.05586° | .08488 | −.11512 | −.51512 |
| 75 / 117 | .77801° | .19142 | −.00858 | −.40858 |
| 100 / 142 | .61592° | .25360 | .05360 | −.34640 |
| 150 / 192 | .43477° | .32311 | .12311 | −.27689 |
| 250 / 292 | .27375° | .38491 | .18491 | −.21509 |

Thus increasing standoff buys margin with length, material and structural demand;
it does not constitute tolerance qualification. A small declared sweep of H0,
s=1…3, g=.3…1.1 and w=.4…1.3 with teeth inside the pitch admits **160 cases**;
none has positive envelope margins at E=.70. This is a grammar/scenario result,
not a universal tilt impossibility or a manufactured yield estimate.

The key finite counterexample adds an ordinary 2-mm-thick straight sleeve at
z=95, with .2-mm clearance on each side of the 2-mm stem. At the highest released
state h=42, the stem center shifts **.50527 mm** there and its polygon intersects
the left guide. Required nominal left clearance is **.51607 mm**, before errors;
adding the .30-mm allowance would require .81607. A wide straight slot no longer
provides the same upright constraint. Shaped guides, a seated angular restraint
or active head alignment change the mechanism; none is silently supplied here.

A bare 2×2-mm cantilever diagnostic at assumed E_material=1/2/3 GPa gives ideal
Euler loads .168/.336/.504 N at 140 mm, versus 2.056/4.112/6.169 N at 40 mm.
These are **straight-stem comparison calculations**, not bounds on the lugged,
guided column or PLA allowables. They show why simply deleting the obstructing
guide is not a demonstrated escape. Loads remain parametric; this experiment does
not impose 10 N on every cell. Tilt, creep, eccentric loading, anisotropy, wear,
angle error and common frame motion remain unqualified.

## Whole-machine obligations and ledger

There is no shared-stroke program yet. Granting independently captured Z/pitch
outputs gives an optimistic service comparison: axial v=.2 m/s, a=8 m/s²;
angular v=30°/s, a=360°/s²; two 2-mm unload/reseat moves, 40-mm travel and two
turns. Add .10 s for acquisition/proof/release, plus two worst-case 42-mm empty
strokes to approach an old tail and return below all tails before row transport:
**1.02370 s/row**. Include one 5.08-mm row feed per visit, one whole retried row
and 2 s for map ingestion, registration and final settling: **four heads / 320
output pairs / 24.556 s**. At .05/.20-s interface overhead the same four heads
take 23.506/26.656 s. Empty approach/return is .470 s per visit; deleting it
falsely permits two heads/160 pairs. These are
allocations granting parallel independent motion, completed programming and
readback inside each slot, not a scheduler for a built machine. No free prepared
mask is credited. A shared lift must replace those individual motions with an
explicit retained selection sequence; E-236's five-pulse comparator is not
inherited automatically.

| Function | Per cell / row | B4 bank or reusable head | Board |
|---|---|---|---:|
| Integral columns / tooth forms | 1 / 5; 80 / 400 | 1,600 / 8,000 resident | 6,400 / 32,000 |
| Stationary bearing sites | 1; 80 | 1,600 resident | 6,400 |
| Guide stations, at least two assumed | 2; 160 | 3,200 resident | 12,800, geometry unresolved |
| Separate resident hinge, swivel, spring, moving dog | 0 in declared solid column | none constructed | 0 credited; cannot add them free |
| Bilateral captures / retained axial / pitch outputs | reused | 80 each/head | 320 each |
| Load/angle/height proof duties | reused | ≥80 each/head | ≥320 each |
| Feed, grounding, arrest and service | shared | 1 system/head, force rating open | 4 systems, not priced parts |

Each output needs either coupled X/Z/pitch motion or a real virtual-pivot linkage;
counting it as one channel does not make it one cheap actuator. A $295 shared
reserve leaves **$0.640625 per complete output pair** under $500, before unallocated
resident hardware. This is a spending allowance, not a price floor or BOM pass.
No force-rated actuator, grip, arrest, routed reader or assembly has been selected.

Declared integral solids total **4.0837 L** across the board before guides/frame/
heads: 76–227 extrusion hours at assumed 15–5 mm³/s, or 84–252 hours with 10%
scrap. No slicing estimate. Upright skinny printing versus horizontal guide
finish/lug layers needs qualification. 6,400 insertions at an assumed 5 s already
cost 8.89 h; 320 shared captures at 10 s add .89 h before their actual assembly,
wiring and calibration. Row rails need modular joining inside the 256-mm bed.
Integral shapes reduce loose pieces, not the number of bearing and guide duties.

At rest, load flows tooth → fixed rail → frame; five integral teeth are fixed
forms, not 32,000 moving latches. While released, the head carries everything;
loss of head holding while shunted has no proven catch. A wrong-height seat may
be firmly supported, so actual height and bearing proof are both needed. Retry
is permissible only after actual support/position is known; broken grip, stuck
column and off-grid arrest need supported shutdown, not promised 30-s recovery.
Unchanged rails remain installed but frame compliance and vibration still couple
cells. Resident failure requires supported column extraction; head failure can
halt 1,600 scheduled cells. No extraction route is drawn.

## Decision

This changes the earlier support-cut conclusion in one useful way: **stationary
positive support with rigid columns is kinematically possible in a tilted section
without a cap swivel**. It also exposes the next cost immediately: the guide and
loaded motion must permit that tilt. The tested straight guide fails, the long
stem alone has no demonstrated load capacity, and the direct head is only a
functional budget allocation. Do not proceed to pockets, hinges, thinner stems,
individual returns or another local clearance search.

Reopening requires a complete shared motion/guidance topology that materially
reduces the 320 independently retained loaded output pairs while preserving U's
resident support and providing affordable arrest/readback. First compare that
architecture against E-236 and direct heads; no automatic E-249 detailing task.
Otherwise redirect invention to a different support/addressing topology. The
external review's unchanged-neighbor concern is addressed explicitly; fixed tooth
forms are not equated with moving failure sites. No physical pass is claimed.
