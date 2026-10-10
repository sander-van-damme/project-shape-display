---
status: complete
builds-on: [E-102, E-101, E-062, E-076, E-077, A-013]
---

# Stiffer followers do not rescue the solid-floor beam return

**Stop this retained-ball/floating-beam assembly before shaft-phase or valve
refinement.** A narrower guide portal clears the tested ground-neck crossings,
but an actual half-selected beam intersects its shoe floor. Changing square
floors to capsules fixes neighbor packing yet does not remove that interference.
This rejects the generated contact geometry, not hydraulic addressing, all
floating beams or all rotary support. Compare changed addressing before another
local cam/shoe variant; retain the distinct partial routing results of E-102.

Input main `e7be7dd`. Replay:
`python3 tools/curated-experiment-checks/E-103/retained_support.py`.
Source imports E-102's geometric primitives. Evidence: generated finite solids,
exact collision witnesses, inverse geometric bounds and reference elastic
calculations; self-review. No CAD export, contact solver, sourced process prior,
physical measurement, yield, print or purchase. All dimensions and E/G/error
values are design/scenario bounds, not X1C capability.

## Frame synthesis and conditional load path

Change each follower cheek from .6×1.2 to **1.2×1.6 mm**, centered axially
±1.4 mm about the cam; the 1.2-mm pin spans 2.8 mm between cheek centers.
Generate an open guide portal at z=26…28, above the highest lower cam envelope
(z=24.6) and below the lowest row rail (z=29.8). Two finite feet connect the
portal to the bearing housings at x=±5.08 relative to the cam. Housing necks
continue to ground. The portal supplies a possible lateral brace, not a new
axial reaction that removes shaft/pin loading. Guide clearance is .2 mm per
side; wall thickness is .6 mm. No ideal guide fixity is granted.

A wider **1.2×2.4-mm** cheek generates an actual portal/upper-neck intersection
**1.6×.060×2.0 mm**. The 1.6-mm-wide alternative clears 216 portal/ground-neck
pairs with minimum .340-mm sufficient separation (.140 after two .1-mm
expansions). Neck locations follow E-102's actual four-phase rule, not a
fictitious dense lattice. This is selected-component routing only: upper portals,
full frame ties, guide angular contact and finite bank boundaries remain open.
A complete frame is not worth refining after the downstream floor collision.

Generate the offset row riser at x=`sqrt(2)−5.08/2`, y=`−sqrt(2)`, a 1.6-mm
square from row-rail top z=38 to shoe-floor underside z=84. A finite cap joins it
to the offset shoe. It retains E-102's **.040-mm** shaft-corridor reserve under
opposing .1-mm expansions. Upper column risers run z=78…84. These heights are
allocations; manifolds, drives, valves and 40-mm column travel are additional.

Apply 9.512389 N per dense row support and 1.889049 N per sparse column support,
with only one row selected. The changed fork increases area and weak-axis
stiffness; bracing still needs a contact/rotation solution. Sum rail bending
and shear, fork/ground-neck axial loss, shaft bending, pin bending/shear and
formal eccentric-riser compliance. Rail loads are eight discrete preloads plus
eight selected endpoints on the row, or one central selected endpoint on a
column. Row and column endpoint losses average at the beam center.

| E / G, MPa | Center loss envelope, mm | Reserve within inherited .2 mm | Formal minimum lift, mm |
|---|---:|---:|---:|
| 500 / 200 | .425978 | −.225978 | .274022 |
| 1500 / 600 | .141993 | .058007 | .558007 |
| 3000 / 1200 | .070996 | .129004 | .629004 |

These are **reference series-path envelopes, not rigorous lower bounds or
physical deflections**. Each tier retains its own fork/neck lengths; maxima
of the two paths are combined conservatively. Whole-transition riser eccentricity
is combined with selected load as an envelope, not a simultaneous operating
state. Pin contact is a point load,
shafts are simply supported locally, and the eccentric riser uses a fixed-base
linear column formula without stability amplification. Shaft continuity,
contact distribution, lost support and actual joint restraint can change the
answer in either direction. The low-E case exhausts the allocation in this
model; it does not prove that every stiffer-frame design fails.

Frame/housing bending, Hertz/contact indentation, beam/stem compliance, guide
fit and load redistribution remain unresolved. They are explicitly uncharged,
not assigned a fictitious contact stiffness. Only .058 mm remains at the middle
scenario for all omitted losses within the original allowance. Low modulus,
line loads and fit are correlated scenarios; no independent-cell yield follows.
No full bending/contact pass follows from stiffening the cheeks.

## Retention synthesis, packing control and actual collision

Use a .15-mm-radius beam neck, spherical ends of radius .25/.40/.55/.60 mm,
.1-mm radial pocket allowance and .4/.6-mm shoe walls. A roof aperture of half
width q must clear the neck and retain the sphere. Under opposing .1-mm
dimensional/placement bounds, necessary conditions are
`q >= .15+.2` and `q <= r−.2`, hence **r >= .55 mm**. Equality has no running
margin. Tilted necks may require more aperture; this is a necessary screen.

Square solid floors cover the entire inward sliding range. With 4-mm beam
length and a 3.1-mm differential envelope (stroke, errors and .4-mm accumulated
return lag), each endpoint slides .736078 mm. At 00, opposite shoes in diagonal
neighbor cells are coplanar. Their exact floor separation is
`5.08−2 sqrt(2)−2(r+.1+wall)`, independent of the pad-center offset used to
cover the slide. Including the two .1-mm envelope bounds requires:

| Wall, mm | Largest radius that packs, mm | Minimum capture radius, mm |
|---|---:|---:|
| .4 | .525786 | .550000 |
| .6 | .325786 | .550000 |

These continuous intervals are empty; the eight sampled cases merely illustrate
the inverse result. The r=.55, wall=.6 floors actually overlap by
.248427×.248427×.6 mm at 00. The .4-wall exclusion is sensitive to the chosen
error bound: below .095157 mm per opposing error the intervals can reopen.
This is not a claim that those errors are achievable or unavoidable.

**Challenge the square-footprint restriction:** replace each floor by a capsule
around its complete diagonal slide segment. With r=.60, wall=.40, a 3×3-cell
patch gives **153 exact floor-pair checks**, minimum gap **.327845 mm**, or
.127845 after the opposing bounds. Thus square-corner packing is escapable.
Do not reject all captured shoes from bounding-box overlap.

The capsule control nevertheless has a **material collision in nominal
half-select**, before errors or reset lag. At endpoint differential 2.5 mm,
`sin(theta)=2.5/4=.625`. The beam neck center one millimetre inward from its
high sphere lies at local `z=r−.625`, measured from that shoe's floor top.
For r=.60 this is **−.025 mm**, inside the solid floor z=−.6…0. Its in-plane
point is inside the capsule by .616702 mm. It lies beyond the sphere and before
the beam center, so this is actual beam material, not an intentional ball/pad
contact. All eight radius/wall cases have an interior witness. Source emits
solid dimensions and witness coordinates; one interior point suffices to
reject an all-states clearance claim without a mesh or sweep step size.

The contact failure persists after the corners are removed and is distinct
from E-102's shaft collision. The floor must be relieved, its contact moved,
or the joint changed. A hole cannot simply be deleted without restoring sphere
support through tilt and sliding. A clevis/trunnion, rocking saddle or centrally
retained beam could escape; none is ruled out or qualified here. E-101's pad
coverage and rigid-length checks remain correct but are insufficient evidence
for an assembled ball-ended beam.

## Reset remains a separate obstruction

At a cam dwell, radial groove clearance and shoe vertical pocket clearance add
in series. For cam/shoe gaps .2/.2 mm, an endpoint can lag .4 mm. E-061's
.15-mm half-select reserve becomes **−.05 mm** even if the raised endpoint is
known to stay seated downward; with uncontrolled flank occupancy it becomes
**−.25 mm**. High/high upper stem travel grows to **1.5 mm**.
With gaps .1/.1, directed reserve is .05 mm but uncontrolled reserve is −.05.
These are nine deterministic clearance/history cases, not reliability data.
A preload must establish the favorable history against friction and dynamics;
positive capture alone does not. The floor collision already rejects this
embodiment, so no shaft-phase or hydraulic refinement follows.

## Portfolio decision and reopening

| Complete-system direction | Retained evidence | Decision consequence |
|---|---|---|
| Four-phase rotary support + retained floating beam | E-102 routing; this frame subset; failed beam contact and reset | Park this assembly; do not optimize shaft phase or print it. Roughly 1,600 cams and 3,200 bearings already precede 6,400 valves/beams and 12,800 shoes. |
| Ground-backed segmented ramps + same beam | E-100's shallow track reduces axial error, but E-101 ground return and this beam contact remain unresolved | No automatic fallback: about 320 input drives and 1,920 supports do not remove the repeated beam gate. |
| A-013 direct long-stroke rack heads | Positive local support; sampled servo procurement exceeds the whole bought budget (E-059) | Keep as control, not a selected affordable machine. |
| Spatially addressed short-stroke chamber-valve heads | New combination: a moving row bank directly opens fixed-base chamber valves; fluid positions columns | Bound this next, before more local cam variants. It removes floating beams and long coincidence rails, while retaining A-014's unqualified seals/volume memory. |

The last direction is an **architecture hypothesis**, not a survivor: 80 reusable
short-stroke open/close channels on one indexing row bank would act on 6,400
normally closed chamber valves. Row position supplies one address dimension;
individual head states supply the other. A common reversible hydraulic supply
moves pistons while selected chamber valves are open. Close and read back each
finished column before withdrawing/indexing; closed non-target valves retain
volume. No retained command dog or global height reset is required. It replaces
individual 40-mm positioning work with short valve motion, rather than claiming
that existing direct-head procurement became cheaper.

At an assumed $250 shared reserve and the absolute $500 bought ceiling,
80 complete head channels could consume at most **$3.125/channel only if no
cell hardware is bought**; conversely zero head cost leaves at most
$.0390625/cell. Both maxima cannot be spent together. One scan permits less
than 375 ms/row before other-map overhead. Neither a price nor a timing pass
is established. Fixed-base valve access, 5.08-mm pitch head packing, independent
close/readback, 40-mm bidirectional flow, acquisition, reset, index and recovery
must all be charged. The row writer may lose on travel, sensing or seals.

E-076/E-077 positive shutters remain a useful control but are not new here:
blocked rigid rams and compliant pullback already have explicit failures.
Do not merely relabel a shutter/dog selector as hydraulic coincidence.
Reopen the parked floating beam only with changed contact/return and load-path
evidence escaping these witnesses. Continue the same hydraulic-addressing
question through the spatial head comparison; valve qualification remains
conditional on a complete addressing survivor. No general hydraulic or rotary
principle is rejected, and no demonstrated hardware is replaced.

Self-review: actual portal/floor intersections, analytical sphere-aperture and
continuous-radius packing bounds, an escaping capsule control, nominal-state
rod-in-floor witnesses, zero-error feasible control, central-force bending/shear
identities, zero support-load response and inverse-modulus scaling pass. No
independent review or physical validation is claimed. Exact rejection witnesses
need no time-step convergence; the elastic model is not contact simulation.
