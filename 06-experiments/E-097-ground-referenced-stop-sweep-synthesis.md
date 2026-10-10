---
status: complete
builds-on: [E-095, E-096, E-094]
---

# Upright stop sweeps clear the lifted foot but fail dense packing and loose indexing

**Stop the tested same-plane staircase and clearance-key carousel embodiments.**
Both upright support geometries avoid vertical overshoot during unloaded setting;
that alone does not make a useful 6,400-cell machine. A wider carousel retains a
conditional bearing envelope, but its tested positive index admits a concrete
wrong-height contact. Continue the campaign with deck-carried selection and
column-carried height storage/grounded support as a changed combination. Keep
larger, remotely packaged carousels as a conditional comparison, not a product.

Input main `fcb4d17`. Reproduce:
`python3 tools/curated-experiment-checks/E-097/stop_synthesis.py`.
Evidence: generated convex polygon prisms, finite overlap volumes, interval
bounds and deterministic search; self-review only. No measured process prior,
strength/contact-force solution, qualified indexer, assembled writer or hardware.
This explores **two stop topologies**, with 324 carousel parameter variants;
variants are not independent architecture discoveries. A horizontal-axis cam was
not generated: this rotary embodiment turns upright steps about a vertical axis.

## Geometry, transitions and uncertainty

Nine levels are 0…40 mm in 5-mm increments. Carousel sector j is a quadrilateral
between radii `max(.2,R−b)` and `R+b`, angular endpoints ±20° about j×40°, extruded
from z=−2 to 5j. The sectors meet around an annular core; a common lower plate
and index flange can connect them. The square foot is centered at (R,0).
Rotation −j×40° presents height j. Distinct faces at the wraparound remain real
40-mm vertical steps, not an interpolated height function. The 0.6-mm foot is a
changed section, not E-095's accepted 1.2-mm support lane or a strength-qualified
contact. Its nominal 0.36-mm² area requires mean stress `F/0.36` N/mm² for F N;
no allowable load follows from clearance.

The translating comparator has nine adjacent 2×2-mm plan rectangles centered
at x=2j, each extruded z=−2…5j. Translating by −2k places step k under x=0.
It has an 18-mm material length and a 34-mm full setting envelope. The stops
remain upright in both families. For a lifted foot bottom ≥43.8 mm and top-step
height ≤40.2 mm, **3.6 mm vertical clearance holds for every intermediate pose**.
This is the E-095 ideal-guide boundary, not headroom inherited from the failed
E-096 guide. It proves neither clearance to side housings nor bank tiling.

Search R={1.1,1.5,2,3,4,5} mm, b={1,1.5,2} mm, square foot side={.6,1.2} mm,
per-body XY datum bound e={0,.1,.2} mm and residual phase bound={0,2,5}°.
Relative translations range over ±2e on each axis; expand foot faces by .1 mm
and erode pad faces by .1 mm. These are explicit epistemic bounds, not X1C
capability or independent-cell distributions. Coherent bank errors are included.
Require .05-mm full-foot edge reserve as a **sufficient bearing screen**; partial
bearing can work, so failure of this screen alone is not an impossibility proof.
Roughness, warp/tilt, guide play, stiffness, creep, wear and indexing dynamics
remain additional uncertainty, not zero-valued calibrated inputs.

## Discrimination and positive-index failure

No generated case meets both the full-bearing screen and same-plane 5.08-mm
center spacing for a circular base of radius R+b. The latter reserve is
`5.08−2(R+b)−2e−.2`; it assumes independent rotor centers on the surface grid.
Internal selectors are **not required** to use that grid. This excludes only
this colocated arrangement; relocated supports require their real load links
and volume rather than an assertion that pitch can change.

| Carousel section, e=.2, .6-mm foot | Full-bearing reserve | Same-plane gap |
|---|---:|---:|
| R=4, b=1.5, phase ±2° | .12536 mm | −6.52 mm |
| R=5, b=1.5, phase ±5° | .15236 mm | −8.52 mm |

Increasing radial width was included because a fixed narrow annulus can fail
radially even as its angular spacing improves. For R=4,b=1.5, the conservative
phase envelope for the .05-mm screen is **±3.2816°** at e=.2, versus ±7.3475° at
e=.1 and ±11.0751° at e=0; edge errors remain present at e=0. These are geometric
specifications for a retainer, not measured angular tolerances.

A finite grounded index key tests whether simple positive engagement suffices:

- Faceted radius-5.5-mm flange occupies z=−6…−3, with nine radial through
  pockets of radii 3…5.5 and angular half-width 16°. A connecting plate above
  the flange must join the step core. Ground bearing/support remains ungenerated.
- A round radius-.3-mm peg at (4,0), z=−7…−4, enters a pocket axially. The bounded
  radius-.4 pin, slot-face erosion .1, and relative XY datum corners ±.4 retain
  **.10723-mm insertion reserve**. Circumscribed polygons bound the circular pin.
- Prescribed withdrawal 4 mm downward → 40° rotation → reinsertion has 51
  collision-free nominal flange/key states. Axial separation proves the rotation
  leg between samples; the insertion stroke stays in the same through pocket.
  Key retention, actuator, support platen and carrier are **granted**, not solved.
- Even granting perfect axial retention, the inserted nominal key permits a
  continuous **8° rotor drift** with at least .23692-mm peg/pocket reserve.
  At that angle the radius-4,b=1.5 carousel's 40-mm sector intersects a low-state
  foot at (4,−.4), side .8, by **.11393 mm³**. This foot is within the declared
  relative-datum/edge box. The key and follower datums need not share one error.

Thus this key inserts but does not retain the safe state. A nonzero collision,
not merely failure of the conservative bearing screen, rejects it. Axial
retention alone cannot fix angular free play. Preloaded/tapered indexing,
amplified remote indexing or a different storage principle would need a new
finite force/withdrawal/packing demonstration. Do not refine this loose key.

Two additional finite witnesses preserve the scope of the packing exclusions:
R=1.1,b=1 with a .8-mm low-state foot shifted −.4 in y intersects the high sector
by **12.78825 mm³** at zero rotation. A nominal b=2-mm translating staircase at
state 0 intersects a neighboring .6-mm-wide foot at x=5.08, height 0, by
**4.74000 mm³**. The staircase cannot be repeated in this shared lane under
arbitrary unchanged terrain. Separate lanes or relocated support links are
changed architectures, not clearance adjustments to these witnesses.

## Whole-board consequence and next discriminator

The generated R=4,b=1.5 **step cores alone** total **9.774 litre** at 6,400 cells;
the b=2 staircase cores total **5.069 litre**. These are exact prism-volume
calculations for the generated solids, excluding bases, indexers, columns,
voiding/infill and waste; they are not sliced filament or printing-time claims.
Hollowing changes the compression/creep problem. An 11-mm carousel repeated on
5.08-mm centers already needs changed packaging before adding its index key,
bearing, actuator access or service clearance. Simple multi-tier or remote
placement is not a generated escape and has no compactness credit.

Both families still repeat one moving stop and one retention function per cell,
plus selective pickup. Neither earns E-094's shared 80B channel allowance or
<.75943-s B=4 stop-setting allocation. Its 94-mm deck route, support proofs,
return and recovery remain charged; there is no demonstrated timing gain or
price. E-014/E-015's coupon frame/shaft limitations remain relevant: no ideal
local ground face here establishes full-board structure or regional disturbance.
No force/reliability ranking or hardware acceptance follows from these solids.

The next useful comparison changes where state lives: **fixed lips on terrain
columns, selective pads carried by the deck and written at common home height;
height retained by a column rack and ground-level support dog**. Putting selection
on the deck may remove E-096's 40-mm hook-handle reach problem. Grounded dogs
would engage selected target groups during descent, replacing prewritten tall
stops with repeated support-setting visits. This is a hypothesis, overlapping
the known direct-rack comparator, not a newly completed architecture. Generate
actual selection/support transitions and arbitrary old/new schedules before
claiming fewer interfaces or channels; preserve direct heads as the control.
Reopen these upright stops only with changed packaging **and** finite retained
indexing that escapes the recorded collisions. No printing is justified.

## Verification limits

The run checks 24,786 carousel prism poses over all 81 old/new pairs in both
rotation directions and 12,393 staircase prism poses. Continuous vertical
separation makes the unloaded-sweep conclusion independent of sample density.
XY error corners are exact for affine translation of each half-plane. Angular
sampling carries a Lipschitz remainder; six holdouts refine 16/64/256 subdivisions
and preserve disposition, with final refinement changes below .007 mm. The
phase envelope uses 20 bisection iterations; decimal output is computational
resolution, not physical certainty. Independent nominal face-distance, sector
area, clipping, touching-contact and vertical-gap checks exercise the geometry.
No dynamic time-step, FEA convergence or external validation is claimed.
