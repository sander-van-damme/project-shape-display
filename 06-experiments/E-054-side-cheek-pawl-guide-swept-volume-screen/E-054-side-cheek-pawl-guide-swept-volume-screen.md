---
status: complete
builds-on: [E-052, E-053, A-013]
---

# Side-cheek pawl guides: clearance escape, thin-shelf rejection

## Decision

Side-cheek rails escape E-053's rear-guide obstruction, but **reject this simple
cantilever-shelf embodiment at the middle placement bound, 10 N and the inherited
8 MPa screening limit**. Its only enumerated clearance survivor uses 0.4-mm walls;
even an optimistic static lower bound is 23.44 MPa. Retain the tight-bound,
0.8-mm-wall geometry only as an unqualified comparator. Do not print or promote
A-013. Reopen with a materially different shelf load path, smaller substantiated
error/load, or supported material/creep limits; do not refine the same grid.

Input main `908fde3`. Evidence is generated axis-aligned solid/swept-volume
geometry and analytical necessary conditions, not assembled CAD, contact FEA,
physical measurements or calibrated process capability. This is changed 3D
support packaging within the rack family, not a new complete architecture.

## Construction and reproducibility

Run `python3 tools/curated-experiment-checks/E-054/side_cheeks.py`.
Standard library; deterministic enumeration, no random seed. It imports E-052's
twenty unequal five-state transition check. Pawl wings extend sideways in y;
pairs of upper/lower shelves flank the rack's full vertical travel envelope.
Outer vertical walls ground the shelves. Rails extend over the entire pawl
withdrawal sweep in x, preserving 0.8-mm longitudinal bearing coverage. Unlike
the rear guide, the rails may overlap the teeth in x because they clear them in y.
Upper shelves provide the possible opposite reaction needed for overturning;
return, axial stops, attachment to the base and head/release linkage are absent.

Enumerate rack breadth b=1.6/2.0/2.4, minimum lateral bearing q=0.4/0.6/0.8 and
wall/shelf thickness s=0.4/0.6/0.8 mm: 27 geometries per error bound. All dimensions
are search assumptions, not qualified printable minima. Reuse web 1.6, pawl
length 0.8, pawl/tooth thickness 2 and clearance c=0.1 mm. Overlap and reach have
0.02-mm margins beyond E-052's bounds; unload is e+c+0.02. No strength result
from E-050's different tooth breadth is inherited.

Rack and pawl y placement are each ±e/2 relative to an ideally registered guide,
plus common bank displacement ±e/2. Slot z placement is ±e/2, with clearance c
above/below. Bounds e=0.15/0.35/0.60 retain E-050's competing process scenarios;
no distribution or independence is assumed. Shape errors are represented only
by these rigid envelopes, not warped/rough surfaces. Guide errors beyond the
ideal registration require an enlarged bound. Common bias affects whole banks.

Each survivor checks six guide boxes against the rack's conservative full
vertical swept volume and the pawl's exact x translation union at all 16
placement corners (96 box pairs per object type). Pitch confinement includes
common displacement; identical neighboring modules can therefore occupy their
own pitch cells without intersecting. Bearing coverage is checked at both
stroke extrema, which bounds all intermediate translations. This is **prescribed
translation**: free pawl rotation, load-induced contact poses and guided support
transfer are not established by these collision checks.

## Results and independent bounds

| Error e | Clearance survivors / 27 | x/y envelope of narrowest (mm) | Survivors also below 8 MPa lower-bound screen at 1/10/100 N |
|---|---:|---|---|
| 0.15 | 10 | 3.89 / 4.20 | 10 / 1 / 0 |
| 0.35 | 1 | 4.89 / 5.00 | 1 / 0 / 0 |
| 0.60 | 0 | x-pitch rejection | 0 / 0 / 0 |

The middle witness has b=1.6, q=s=0.4, 1.22-mm withdrawal, 0.47-mm unload and
2.37-mm guide-track length. Increasing either bearing or wall to 0.6 mm gives
5.40-mm y width. The exact lateral enclosure is
`Y = b + 4e + 4c + 2q + 2s`.
For these minima, e≤0.37 is necessary; off-grid e=0.369/0.371 holdouts pass/fail.
Width changes four millimetres per millimetre of error bound. At e=0.35 even
continuous optimization permits s≤0.44 with b≥1.6 and q≥0.4.

For a deliberately favorable shelf bound, split F equally across two lower
shelves, spread force over the full pawl length L=0.8, and place all contact at
the outermost admissible edge. Clearance keeps that edge at least c=0.1 from
the cantilever root. Rectangular beam bending then requires
`stress ≥ 3 F c / (L s²)` MPa (N/mm²). Real distributed contact has a larger
lever arm; upper-shelf reaction, shorter pads and stress concentrations worsen
it. At F=10 N, s=0.4 gives 23.44 MPa; even s=0.44 gives 19.37 MPa. Meeting the
assumed 8 MPa limit requires s≥0.685 mm, giving Y≥5.569 mm. Thus the middle
failure is continuous within the declared minima, not just a sparse grid miss.
At tight error, s=0.8 gives Y=5.00 and lower-bound stress 5.86 MPa; this only
avoids rejection. Loads 1/10/100 N and 8 MPa are E-050 sensitivity assumptions,
not product requirements or sourced PLA allowables. Beam stress is a reduced
necessary-condition model; a different support topology invalidates this bound.

The unpreloaded slot has 0.35/0.55-mm total vertical play in tight/middle cases.
Its actual seated and tilted poses could invalidate the inherited tooth/pawl
clearances. No loaded support continuity is claimed. A positive preload or
anti-rotation feature must be modeled and counted, not assumed away. The weak
return element cannot be assigned tabletop load.

## Consequences and checks

A-013 still needs 6,400 pawls, now with two lower and two upper rail surfaces per
cell: 25,600 shelf faces before return/retention, guides, grippers and sensors.
Printed part integration can reduce assembly count but not contact/wear burden.
No channel-cost, <30-s timing, reliability or regional-disturbance improvement
is established; E-050/E-051 remain applicable. Full-board error is not an
independent-cell yield calculation. No probabilistic yield is reported.

Self-review checks independent enclosure algebra, both sides of its continuous
threshold, bearing extrema, box-contact limiting cases and inherited E-052
transitions. Exact affine boxes require no mesh/time-step convergence. The
stress inequality uses force balance and a minimum moment arm, not a calibrated
surrogate; it omits creep and anisotropy and cannot qualify a surviving shelf.
The next useful discriminator is a complete channel with a different grounded
support/load path and credible cost, or another memory principle. The present
thin-wall geometry offers no reason for fabrication or further timing work.
