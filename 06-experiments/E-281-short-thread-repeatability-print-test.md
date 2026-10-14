---
status: complete
builds-on: [E-277, E-279]
---

# Short-thread repeatability print test

One optional small physical discriminator follows E-277's support-free 90°
profile. It asks whether unmodified nominal threads actually mate consistently;
CAD and slicer paths cannot measure this. It does **not** restart local fit
optimization or qualify the parked long-screw manufacturing routes. No physical
results exist. Owner handoff: `owner-print-tests/short-thread-fit/test.md`.

## Changed specimen and decision

Five pairs on one plate: three identical functional nominal pairs with .15-mm
radial relief, one .10-mm and one .20-mm relief control. All males retain
3.2-mm major diameter, .9-mm depth, 3-mm single-start lead, 90° included angle;
female cutters are 3.5/3.4/3.6 mm with explicit zero BOSL2 slop. These are chosen
bounds, not a process distribution or reproduction of the owner's historical
working print. Ten-mm nuts retain the E-277 body and plain open thread ends.
Sixteen-mm exposed male threads replace 64 mm; permanent 14×14×3 mm grips anchor the
print and permit finger rotation. The final .6 mm tapers to the 1.4 mm core; no
sacrificial support contacts a thread. Raised dot counts 1–5 identify parts outside
the working contact. No guide or joined channel is included.

Why upright despite the owner's long-rod concern: E-279's horizontal paths contact
the entire working thread, so shortening an upright support-free specimen isolates
roughness/fit without that cleanup confound. A 16 mm cantilever has 1/64 the static
compliance of 64 mm at equal EI; this is a length-scaling identity, **not** hot-layer
stiffness, nozzle-force or print-stability qualification. Broad grips anchor the
base but do not brace the upper thread. Actual success remains to be observed.

A nominal pair must start by hand, move approximately one turn bidirectionally
with full engagement, and survive five gentle cycles without custom sanding or
visible damage. Compare all three nominal repeats before interpreting the two
controls. Cross-fitting nominal nut 1 onto screws 2/3 can localize inconsistency.
No load-to-failure or holding claim: no axial fixture/antirotation guide exists.

All three nominal repeats passing justifies a later supported motion/retention
article; inconsistent nominal fits prioritize actual-process variation; success
only at loose clearance does not select a production fit. All failing parks this
unchanged print route. Five parts cannot establish a probability distribution,
independent yield or thousands-of-cells qualification. Correlated lot/bed effects
are deliberately left observable, not modeled as independent draws.

## Verification

OpenSCAD 2023.09.11, BOSL2 `136e6367e65d52196a3ea51d03156f8b622c60fc`,
PrusaSlicer 2.7.2; same E-277 .4-mm nozzle/.2-mm layers/.45-mm lines/100% infill
comparison profile. Ten individual exports and the reloaded plate are watertight,
consistently wound, positive-volume, separated bodies. Plate 94×32.15×19 mm;
20 zero-area facets from float32 placement are removed, without hole-filling;
plate volume agrees with the individual exports within .01 mm³.

425 sampled coaxial assembly positions (five pairs, nut bottom 3.5..19.25 mm)
have zero finite-solid intersection. The wrong rotation-sign control intersects
by 1.9211 mm³. This covers entry and one fully engaged turn, not continuous
contact, misaligned assembly or compliant printed motion.

Both actual support-off/on slices have **zero support, bridge and overhang
paths**. Each uses 8.53 cm³ / 10.57 g; estimated normal times 1h07m14s/15s.
This is a comparison-profile estimate, not X1C timing; normal material cooling
and short-layer slowdown can increase it. Positive extrusion independently agrees
with the slicer material footer. Mesh layout and deposited sections were visually
inspected; all 30 identification dots have extrusion paths at their final layer
in both slices. Labels are outside the load interface. No G-code is delivered.

An abandoned .6-mm circular entry chamfer ended above the thread's minor diameter,
creating a ledge: the actual slice showed 143 bridge and 138 overhang segments at
Z=.8 mm. Removing that chamfer restores the existing plain E-277 nut opening;
no extra fit feature or support-cleanup duty was introduced. This scoped failure
is preserved here; old generated meshes remain disposable scratch.

Reproduce with `python3 tools/curated-experiment-checks/E-281/check.py --bosl2
/path/to/BOSL2 --slicer /path/to/prusa-slicer --output <scratch> --deliverables
<scratch-pack>` (one shell line). Python dependencies: numpy, trimesh,
manifold3d, matplotlib and networkx. `--reuse-cad` only reuses unchanged SCAD
exports already in the scratch directory. The default regenerates everything.
The single READY P1 pack is an unperformed physical experiment, not a fit pass.

## Whole-machine consequence

This test adds no production component and selects no architecture. E-277/E-279
retain 1024 threaded pairs and 1024 channel/nut joins at 12.7 mm/32²; 4096/6400 remain
replication comparators, not compatibility of 10.3 mm bodies with fine grids.
E-279's upright bare-pair repetition 594–595 h/1024 excludes finished screw ends,
frame, scrap and joining. This coupon cannot reduce that ledger or qualify 850 rpm.
The 5.08 mm/~6400-cell, 40 mm, ~30 s/~$500 reference and coarser S40/S50 raised-neutral,
~$1000 finished /$1000–1500 demonstrator comparisons remain unchanged. Neither
optional printing nor a favorable fit supplies a purchase or product decision.

Source: `tools/curated-experiment-checks/E-281/check.py` and `coupon.scad` reuse
E-277's pinned BOSL2/profile/parser. Generated CAD, G-code, plots and numerical
outputs remain scratch; only the owner-ready STL is retained. Self-review only.
