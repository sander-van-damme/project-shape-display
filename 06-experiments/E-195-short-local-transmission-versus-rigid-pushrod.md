---
status: complete
builds-on: [E-194, E-121, E-122, E-156]
---

# Local guided transmission preserves the dense input field and adds moving terminals

**Stop this local foil embodiment; retain the straight rigid member as the simpler
transmission control, not a selected machine.** A shallow offset has a nominal
full-density routing construction, but moves the entire retained input array only
half a pitch. It saves perimeter inventory versus E-194 without removing input
selection, retention, or recovery. It adds two slotted moving terminals per cell,
57 mm of depth and compression/reversal contacts. Its .10-mm terminal gaps fail
the explicit ±.05-mm adverse feature/registration box. No fabrication proposed.
Reopen local flexibility for an obstacle or service-access advantage demonstrated
by actual geometry, with materially changed terminals; not another foil section.

Input main `41bd3f6`. Reproduce (Python 3 + NumPy; disposable JSON, optional SVG):

```
OPENBLAS_NUM_THREADS=1 python3 tools/curated-experiment-checks/E-195/local_routes.py
```

Evidence: finite curve/solid envelopes, a reduced quasi-static obstacle beam,
analytical bounds and self-review. No physical measurements, calibrated X1C
priors, contact CAD, strength/life qualification, complete writer or priced BOM.
All dimensions, loads and material values below are construction/scenario
assumptions except the stage-02 pitch, travel, board scale and cost/time targets.

## Different local routes and the same retained input

| Route | End motion and full-density result |
|---|---|
| Straight rigid control | A 3-mm stem continues into a translating screw. Output and input both rise h; no exchanging flexible tails. Fixed rotating nuts retain engaged flanks; their arrest is unqualified. |
| Shallow S offset | A guided 2 × .1-mm foil connects two moving tabs. Two straight tails exchange h and 40−h; a fixed cubic bend offsets the input field 2.54 mm over 15 mm depth. No spool, return spring, new height-acquisition dock or accumulating take-up. Static route and slotted end envelopes clear; standalone module extraction fails. |
| U return | A 10-mm-radius half-circle reverses the input direction. Both end-guide sweeps are explicitly present. Its 20-mm lateral reach intersects the next translated cell's vertical leg at 5.08-mm pitch. Reject this one-plane fold, not all folded transmissions. |
| Module-edge comb | Eight E-194 quarter-bend routes terminate outside a 40.64-mm module. Repeating the module makes its full 40-mm input reserve intersect the preceding module's inboard route. Extra screw length worsens the missing aisle. Reject this tiled layout; vertical fanout would be another constructed architecture. |

E-121 loop and E-122 keeper/tooth failures retain their original scopes.
Confinement changes tension-preload closure, not those failed geometries.

Common input: E-156's 3-mm mean-diameter, .15-mm-lead translating screw through a
4-mm-long resident rotating nut, with 5-mm drive collar. Allocate a **5.8-mm
outside × 5-mm-high housing envelope**, not completed bearing geometry. Alternate
checkerboard sites in two depth tiers 6 mm apart. Nearest screw-to-housing radial
margin is .680 mm, same-tier diagonal housing margin 1.384 mm, and adjacent-tier
axial margin 1 mm. Each screw has 54 mm of threaded travel stock; fixed nut
interval is 8…12 mm below its h=0 top. It remains wholly threaded at both h=0/40
and all intermediate positions. Housing strength, bearings, thread fits and the
asynchronous belt/head selector remain unresolved. Both controls incur them.

## End construction matters more than bend radius

Depth is positive below the lowest surface. Caps have assumed 4.68-mm square
footprints, with their underside at −h; stationary parts stay at depth ≥0.
The foil's output tab is at **50−h mm**, on a 50-mm rigid output stem. The stem
still overlaps guide stations spanning depth 0…8 at full extension. Thus the
40-mm output guide is below the surface, not sticking through low terrain.

Relative to the output stem axis x=0, the foil lies at x=−2.25 mm. The curved
segment begins at depth 51 and ends at depth 66, following
`x(u)=−2.25+2.54(3u²−2u³), depth(u)=51+15u`, 0≤u≤1.
Its arc length is 15.2549756 mm (dense quadrature), minimum bend radius 14.764 mm.
The input tab is at depth `107+6p−h`, p=checkerboard parity; its screw axis is
2.25 mm right of the local foil, hence x=2.54 mm. The input nut is at depth
115…119+6p. Its housing roof is below the deepest guide by 1.5 mm.
There is at least .85 mm between each finite .3-mm-thick moving tab and the bend
at the worst endpoint. All variable geometry is affine in h; endpoint envelopes
cover arbitrary neighbors and every intermediate state, with 81-height checks.

A **closed** foil guide cannot accept a 3-mm screw/stem in its .5-mm-thick lumen.
Even a side web crosses a closed wall: the generated .3 × .4 × .3-mm intersection
is .036 mm³. The constructed escape uses a .5-mm-wide longitudinal slot through
one wall, a .3-mm-wide connecting web, and remaining side lands supporting the
foil. Nominal web-to-slot and stem-to-shared-wall clearance are each .10 mm.
Terminal joining/strength remains unqualified; charge 12,800 joints and their
inspection. Slotted lands constrain the foil less than a closed channel.

The bent outer envelope is 1.3 mm in-plane × 3.2 mm across rows, including .4-mm
walls and .4-mm nominal total core clearance. At 128 chords, conservative adjacent
route gap is 3.624075 mm; row gap 1.88 mm. Cubic chord error is bounded analytically
by max|x''|·Δz²/8 and subtracted for both routes. Farther neighbors cannot approach
more closely: the x excursion is bounded by 2.54 mm, and rows are disjoint slabs.
The core length is bend+42+6p mm, invariant throughout each 40-mm move. The guide
reserves total bend+82+6p mm; guide envelope and occupied foil are not conflated.

Use 10×10-cell, 50.8-mm module footprints (64 modules, within the X1C envelope).
Input and guide arrays shift bodily; they do not need module-edge fanout. A module
requires split guide plates and independent support of its 100 columns.
Direct downward extraction **fails**: each shallow border housing
passes through the neighboring deeper housing, with .72-mm radial overlap.
The 10×10 checkerboard has 20 outside neighbors that must be cleared before
that path can work, in addition to its own 100 housings. This affects both
controls, and neither earns independent module repair. A staged cartridge
removal/support scheme or changed housing placement is required; it is not
constructed here. Removing a core/nut without a support fixture releases the
sole load path. Frame seams, fasteners and writer approach also remain open.

## Manufacturing and contact discriminator

Common translation cancels; opposed feature growth, location and registration
bounds do not. The declared adverse envelope subtracts 3e from each nominal
clearance. At e=.025/.05/.1/.2 mm the terminal margin becomes
**.025/−.05/−.20/−.50 mm**. At e=.2 the core lumen's .4-mm running clearance also
becomes −.2 mm. These are coherent board/batch scenarios, not independent random
cell errors or X1C yield estimates. Widening conduit spacing cannot cure them.
Hole shrinkage, first layer, warp, roughness, wall/layer errors, orientation,
creep and wear may change those gaps and forces; no calibration suppresses them.

For a nominally clear route the executable solves a **reduced obstacle beam**.
Material coordinate spans the actual fixed-length foil, with tails 1+h and
41−h (p=0), not both full swept reserves. Small normal offset w is bounded by
±c/2; endpoint position/tangent are fixed. With tension positive N:

```
ΔL = ∫[−κw + (w')²/2] ds
Π = (EI/2)∫(κ+w'')² ds + N ΔL
```

Finite differences give a box-constrained quadratic. Coordinate minimization plus
positive-definite free-set solves use zero and both lowest-eigenmode starts.
Negative-curvature directions move to a feasible wall; a free-subspace curvature
check rejects the straight compressed saddle that stationarity alone admits.
Compression makes some Hessians indefinite: reported branches satisfy KKT,
**not a certified global equilibrium or dynamic stability**. Wall reactions are
constraint residuals. The solver includes elastic curvature-entry reactions;
capstan load-only drag would omit them. N=±1 N, E=100/200 GPa, c=.1/.4/.8 mm are
bounded material/contact scenarios, not selected foil properties. h=0/20/40 and
mesh refinement test state/representation sensitivity. Solver results below do
not repair the failed terminal error box.

All 24 reported cases × three starts meet the stationarity and free-curvature
checks (selected residuals <2e−14 N); this does not prove branch uniqueness.
The straight flexible control at −1 N buckles into wall contact (ΣR=.01056 N),
whereas tension and unloaded straight controls have no contact. This catches a
false zero-deflection compression pass. At h=20, E=200 GPa, c=.4 mm:

| Elements | ΣR, compression −1 N | ΣR, tension +1 N | ΔL compression / tension, mm |
|---:|---:|---:|---:|
| 32 | .33544 N | .86113 N | −.050916 / −.071410 |
| 64 | .25914 N | .73100 N | −.042334 / −.060053 |
| 96 | .22803 N | .68799 N | −.039227 / −.057117 |

The final force change is still 12.0%/5.9% of the 64-element values:
**mesh convergence is not established**. Do not use these as force specifications.
At 64 elements the twelve E/c/N scenarios span ΣR=.12388…1.69791 N;
μ=.3 therefore gives .03716….50937 N wall-drag scenarios. At h=0/40 the
nominal branches agree by reflection, ΣR=.27658/.43727 N for compression/tension.
Maximum sampled offset slope is .117: the small-offset approximation remains a
model assumption, not a high-fidelity holdout. No further refinement can remove
the demonstrated geometric/burden disadvantage.

With the input favorably fixed, the force-reversal coordinate change in this
reduced closure is |Δ(ΔL−N L/EA)|: **.02058 mm** nominal at 64 elements,
.02075 mm at 96, and **.00410….21948 mm** across the six E/clearance pairs.
This is a pair of static endpoints, not a solved frictional reversal trajectory,
backlash specification or post-outage excursion bound.

Signed motion is separate from signed load. On a fixed computed branch, the
wall-drag scenario is `Fdrag=μ ΣR sign(v)`, μ=0/.05/.3, and dissipated power is
`Fdrag·v≥0`. Velocity reversal flips drag; it does **not** necessarily reverse
axial load under gravity. Force reversal compares N=−1 and +1 branches and their
ΔL plus axial extension N L/EA. Neither a single capstan factor nor encoder angle
captures this path dependence. End-clamp friction, slotted-land torsion, evolving
normal force along a frictional strip, stick/slip, folds and transient settling
remain outside this constant-N planar model. Its friction allowance is diagnostic,
not a self-consistent transmission-capacity bound. No force/time tail or reliability
probability is inferred. The omitted curvature²w term and small-offset expansion
also create model discrepancy; richer contact work is unjustified without an
access/burden advantage.

Independent control: assumed 3-mm rigid PLA rod, E=1…3.5 GPa, pinned unsupported
length 56 mm gives first Euler load 12.51…43.80 N. The .1-mm foil with E=200 GPa
over a 41-mm free straight span first buckles at .196 N. These are onset bounds,
not strength/fatigue or confined-collapse predictions. Rigid guide reactions and
stiffness remain unqualified; the rod does not inherit foil wall friction.

## Whole board, loss and conditional decision

| Charged inventory/envelope | Rigid control | Local offset foil |
|---|---:|---:|
| Retained screw/nut inputs; private coordinates | 6,400 | 6,400 |
| Common 54-mm threaded stock | 345.6 m | 345.6 m |
| Additional rigid stem stock | 339.2 m, tier average | 320.0 m |
| Foil core / guide envelopes | none | 385.632 / 641.632 m |
| Unslotted conduit-wall reference volume | none | 1.899 L, before supports/seams; slots remove some material |
| Thin moving tabs / permanent core end joints | none | 12,800 / 12,800 |
| Depth below lowest cap / full travel envelope | 110 / 150 mm | 167 / 207 mm |

The wall-volume reference is not a slicer estimate. Foil/guide inventory falls
from E-194's 1.23/1.49 km, without beating the rigid control on access, input
count, contacts or depth. Rod printing, strength and repair are still charged.
One additional 10-s operation at all 12,800 ends is **35.56 assembly hours**;
actual joining/inspection time is unknown. Bought cost still obeys
`H*c_head+6400*c_input+c_shared+c_foil_and_joints<500`.
With $250 elsewhere all site purchases share <$0.039063/site even with free heads;
this is an allowance, not a market floor. No affordable BOM is established.

A generous 100-mm/s, 1,000-mm/s² rest-to-rest 40-mm stroke takes .5 s. With
.1 s for each visit and 6 s/map for preparation, transport, registration,
verification, settling and one bounded retry, `6+ceil(6400/H)*.6<30` requires
**H≥165** independently bidirectional heads. This is a necessary schedule bound;
all those overhead allocations and contact recovery remain unearned. The common
.15-mm lead implies 40,000 rpm at that speed. Do not import it as an operating
point: E-156 already shows severe light-load coast and source-contact coupling.

With a favorably clamped input, output load goes through stem→tab→foil→input tab
→screw→nut flanks→thrust housing→frame. Removing drive torque is not clamping the
input; stationary self-lock and moving arrest remain different claims. Compression
buckling/wall switching can move a top even when its input is fixed. Broken foil,
failed terminal or released nut can remove sole support. No bend energy, friction
or reader is credited as an independent catch. Arbitrary retained maps are only
kinematic states: 625 two-cell old/new maps check private-coordinate reach, not
hardware isolation. Correlated frame/guide or drive faults can affect a whole bank.

Verify actual tops and support after source separation; encoder angle alone is
insufficient. Failed proof requires supported correction before release, with a
bounded retry/abort path. No false-accept rate is measured: assumed p=1e−4 would
mean .64 expected misses per board without needing independence. Slotted-guide
pinch or a bad common reader can affect all cells; no yield or reliability claimed.

**Portfolio action:** close this finite local-route comparison. Stop foil-section
optimization, local foil input-lock detail and fabrication for this embodiment.
Keep the rigid control and E-194 routing primitives; no machine selected. Next
explore actual retained-input hardware reduction or verified access. Reopen local
foil on an obstacle/service benefit plus robust ends. Self-review only.
