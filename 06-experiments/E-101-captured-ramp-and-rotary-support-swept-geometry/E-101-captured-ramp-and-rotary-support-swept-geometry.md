---
status: complete
builds-on: [E-100, E-061, E-062]
---

# Captured supports collide where rail-only envelopes fit

**Reject the generated straight-post crossed-ramp layout and coplanar captured
radial-cam layout.** Both have finite material collision witnesses. This does
not reject distributed support, hydraulic coincidence or vertically staggered
cam axes. Stop force/valve refinement of these two layouts. Reopen through
changed ground-return routing or axis tiers, not another full-width rail sweep.

Input main `ad68a58`. Reproduce:
`python3 tools/curated-experiment-checks/E-101/support_geometry.py`.
Evidence: generated finite contact geometry, solid-box intersections and
analytical bounds; self-review. No CAD export, contact solver, sourced process
prior, physical measurement or hardware acceptance. Dimensions below are
explicit design/scenario bounds, not X1C process capability. Generated JSON is
not retained. No print or purchase follows.

## Captured ramp and crossing witness

Extend E-100's 15-degree, two-segment track into a closed inclined slot: 1.2-mm
follower pin, 0.6-mm web, 2-mm track width, 0.2-mm fork side clearance and
0.6-mm fork arms. The fork is 3.6 mm across the track and 2.4 mm along it.
The inclined slot supplies both raising and forced return; the ground bed
carries the track reaction. Sliding contact still requires friction/drive force
and guides. At 0.2-mm diametral slot clearance, generated block length is
15.330 mm and height 13.559 mm above ground; translation is 9.330 mm. Its
24.660-mm swept length fits the illustrative 40.64-mm support spacing.
A continuous 2×8-mm track base is geometrically possible; elastic/contact
performance is not established by that observation.

Rows run along x at y=−sqrt(2)+j×5.08; columns along y at
x=sqrt(2)+i×5.08. Row rails occupy z=20…28 plus their commanded 0…2.5-mm
lift; column rails occupy z=48…56 plus lift. Upper ground beds begin at z=32.
Straight ground-return posts use the 3.6×2.4-mm fork footprint and stand in
the gaps halfway between row rails. Lower fork stations sit halfway between
column rails. These are repeated support-grid intersections, not per-cell
support counts. A 3×3 local patch tests the critical crossing.

Rail-only checking is misleading: 7,803 box-pair checks over a 17×17 input
sweep find clearance between rails, upper posts and lower rails, and row shoe
risers and upper rails. The post-to-rail edge gap is 0.34 mm, leaving 0.14 mm
under two adverse 0.1-mm envelope expansions. **But the actual lower fork
arm intersects an upper grounded post by 0.46×0.46×10.8 mm already at 00.**
Both solids are explicitly generated; this is not merely overlapping swept
bounding spheres. Source emits their coordinates. The collision persists
through lift; raising the upper tier alone does not remove a post extending
to ground. Bed/frame ties, guide bearings and valve/manifold packaging have
not been granted a pass. There is no accepted 66-mm-high selector assembly.

A changed post footprint, offset load path, separately supported ground tier
or different support topology can escape this particular witness. Such a
change must carry the E-100 reactions and preserve moving-fork clearance;
removing a colliding volume without replacing its load path is not a solution.
The 320 split input drives and repeated support/contact burden remain.

## Reset clearance consumes the coincidence window

For normal diametral slot clearance c, the pin's vertical free interval is
`c/cos(15°)`. Finite capsule-slot geometry checks both flanks, free midpoint,
stroke endpoints and end-cap clearance. There are 387 contact positions per
clearance scenario; affine flank extrema give an independent continuous bound.
The slot can force the pin down only to the upper edge of that interval.

Retain E-061's s=2.5, gap=1.6, endpoint/gap errors ±0.1 and downward elastic
loss 0…0.2 mm. Two alternative **history assumptions**, not probabilities:

- Directed rise: downward preload keeps the high input seated; only the low
  input may lag during forced reset. Half-select clearance is
  `0.15−c/(2 cos(15°))`.
- Uncontrolled flank occupancy: either input can sit anywhere in its slot
  free interval. Half-select clearance is `0.15−c/cos(15°)`.

| Slot clearance mm | Reset lag mm | Directed half-select clearance mm | Either-flank clearance mm |
|---:|---:|---:|---:|
| 0.10 | 0.103528 | 0.098236 | 0.046472 |
| 0.20 | 0.207055 | 0.046472 | −0.057055 |
| 0.30 | 0.310583 | −0.005291 | −0.160583 |

The respective zero-margin c ceilings are **0.289778 and 0.144889 mm**.
These are functional requirements, not achievable-print claims. Whole-line
clearance/bias is correlated; no independent-cell yield is inferred. Reversing
pressure, guide stiction, inertia and follower preload must decide which
history is defensible. A closed slot alone does not establish the favorable
one. At c=.2, the adverse high/high upper stem travel increases from 1.1 to
**1.307055 mm**; E-061's travel allowance cannot simply be inherited. Minimum
selected lift remains .5 mm only while all downward losses stay inside .2 mm.
E-100 strain, bed/contact loss and shoe/riser compression share that allowance.
Reset drive force and beam retention remain unproved.

## Finite beam and rotary comparison

The generated beam uses 4-mm endpoint-center spacing, 0.25-mm endpoint balls,
a central 0.4-mm ball for the stem, and a conservative capsule envelope.
Horizontal pads retain sphere contact under ±0.1-mm endpoint errors. The
maximum inward slide is .524365 mm per end; 1.070782-mm square pads provide
.1-mm edge reserve. All 4,356 sampled states preserve length, pad coverage and
neighbor-beam clearance. The sphere contacts preserve the center-height mean;
a plain tilted rectangular beam would need a different contact calculation.
Anti-yaw guidance, preload, positive beam retention and central stem clearance
are not generated. Thus beam sliding is a conditional geometric result, not
completed selection/reset. Illustrative 1.6-mm-square, 34-mm row risers have
ideal pinned buckling loads 2.331…13.988 N at E=500…3000 MPa against the
1.189-N endpoint load, and axial loss .031584….005264 mm. Straightness,
end restraint, creep and strength are not qualified.

A materially different support transmission rotates distributed radial cams.
The generated closed-groove centerline has 60-degree high and low dwells,
120-degree half-cosine rise/fall, and 2.5-mm lift. Generate 721 polar points
for each shaft diameter; inspect the exact high-dwell annular web at the
intermediate −90-degree shaft position. A captured 1.2-mm follower with .2-mm
clearance and .6-mm inner/outer webs requires outer radius
`R = d/2 + 2×.6 + 1.2 + .2 + 2.5 = d/2+5.1 mm`.
At d=1 or 2 mm, that web intersects the adjacent 5.08-mm-spaced shaft by
**.58 mm radially**. Axially staggering cam disks cannot avoid continuous
neighboring shafts. Even the zero-diameter limit puts the neighboring shaft
center inside the web. The swept clearance inequality `R+d/2≤5.08` would
require d≤−.02 mm. This rejects these coplanar axes with the stated contact
package; it is not an exclusion of all cams. Rise pressure angle, actual groove
offset, follower load and positive-reset force need not be refined after the
exact dwell-web collision.

For comparison only, an external-profile cam without this capture package
has a more favorable swept bound d≤1.98 mm. A 203.2-mm shaft at that diameter
under the 47.562-N line load, distributed uniformly and rising 2.5 mm over pi
radians, has formal mean-slope twist 2.124…12.742 rad at G=1200…200 MPa.
A 30-degree diagnostic twist ceiling needs 2.810…4.398-mm diameter. These are
explicit elastic scenarios, not PLA allowables. Large twist invalidates a
uniform-phase interpretation; **it does not prove failure to reach the dwell**,
because the cam unloads and the shaft can unwind. Dynamics, friction and
stored-energy recovery would decide that claim. No dwell performance is accepted.

## Decision and remaining gate

These two embodiments fail task 1's geometry gate before valve synthesis.
Continue the same campaign with a changed three-dimensional support routing:
vertically staggered rotary axes and axially staggered support stations are a
bounded next discriminator, with complete ground bearings and beam return.
This changes the contact routing that caused the failures; it is not another
shaft-diameter sweep. Reject it if actual follower/shaft/ground geometry or
load-dependent phase cannot preserve isolation. Valve, flow and full-system
comparison stay dependent on a real selector survivor. No hydraulic family
selection or rejection follows yet.

Self-review includes zero-clearance isolation recovery, a deliberate post-at-
rail collision control, exact fork/post overlap, exact annular-wall/shaft
intersection, rigid-beam length and contact checks, and 32→128 step refinement
of straight-slot sampling against analytical extrema. These verify this reduced
geometric model. No nonlinear contact, manufactured-fit, dynamic reset,
independent review or production-reliability claim is made.
