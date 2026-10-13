---
status: complete
builds-on: [E-255, E-256, E-261, E-262]
---

# Supported S40 screw calibration article

**One optional manual calibration article, not powered or physically qualified.**
The exported mating pair, captured thrust path, two openable guides, removable
second radial land and travel stops pass nominal geometry checks. The owner
handoff is [one eight-part print job](../owner-print-tests/supported-s40/test.md).
Actual-process alignment, stiffness, holding and easy service remain questions
for this article; there is no fitted-process or array acceptance.

Evidence: historical/library source inspection, CAD, mesh booleans and interval
calculations, self-reviewed. No measurements, purchases or owner print obligation.
E-256's positive manual holding report **and near-extension break** remain intact;
this new pair is not the identified successful historical variant.

## Source-controlled mate before fixture CAD

Reinspected trial3 actuator and trial5 actuator/calibrate_screw/calibrate_rect_tube/
frame at41484f96999847c139b9010e73009d73e9459c89. The actual
[BOSL2 source at136e636](https://github.com/BelfrySCAD/BOSL2/blob/136e6367e65d52196a3ea51d03156f8b622c60fc/threading.scad)
confirms E-255: internal mode adds twice `$slop` radially and transforms helical
phase. Trial5's minimum cutter radius1.65 exceeds the male crest1.60. Its
calibration screw uses different dimensions; blindly exporting trial5 is wrong.
The pinned comparison library is still not the known historical print dependency.

This specimen uses **the same external trapezoidal generator for male and female
subtractive tool**, avoiding hidden internal slop: pitch3, depth.9, included angle30°,
one right-handed start, no bevel or blunt start. Male OD3.2, cutter OD3.5; explicit
radial expansion.15 mm. Root radius.7, cutter minimum.85, maximum1.75, nominal
radial engagement.75 mm. A4.4-mm square nut leaves.45-mm minimum wall; the tube
wall remains.44. These are allocations, not measured X1C capability or retention.
Changing the nut from trial5 changes friction; Sander's hold does not transfer.

Male thread occupies0..54. The periodic cutter extends−3..57 (two extra whole
pitches), through the10-mm nut and slightly into the square cavity. Extending
its numerical boundaries removes a coplanar CGAL non-manifold export seam;
no alternate physical fit was tuned. Signed mesh mating independently confirms
rotation `theta = −360*(q−screw_axial_shift)/3` degrees with the pin nonrotating.

## Complete load path and finite dimensions

The following graph was fixed before fixture CAD; the mesh pass refined collar
endfloat from the sketch's.40 to **.38 mm** because of its.02-mm union overlap.
All z coordinates below are relative to nominal thread start, in millimetres.

```
miniature -> fixture tray/cap -> pin -> engaged nut -> resident screw
          -> lower handwheel/thrust face -> frame foot -> table
reverse axial force -> upper handwheel face -> fixed thrust shelf -> side rails
pin torque/side force -> guides z44..46 and84..86 -> common side rails
screw side force -> primary radial land z-4..-2 -> side rails
optional second radial land z-18..-16 -> same rails (no axial duty)
lower travel limit: cap underside -> upper guide top z86
upper travel limit: bottom shoulder top -> lower guide underside z44
```

| Feature | CAD allocation / consequence |
|---|---|
| Pin / nut / useful signed travel |86-mm stock; nut local0..10; q2..42, travel40; neutral20 gives±20 |
| Guide bearing section |Pin local2..84, two2-mm slabs with40-mm center span; full slab coverage throughout travel |
| Thread / cap |54-mm thread,2-mm nominal end margins; cavity ends atq+84,32-mm nominal tip clearance when retracted |
| Thrust capture |Handwheel OD24, z−26..−21.98; fixed faces−26.2/−21.8; axial shift−.20..+.18 |
| Actual margin with axial float |At least1.80-mm thread end margin,31.82-mm cap clearance (31.8 conservatively reported) |
| Radial / square guide |OD3.2 journals in3.6-mm bores;4.4 pin in4.8 square apertures; neither is a qualified print fit |
| Laboratory stops / tray |Bottom shoulder8×8×2; top tray28×28×2, both integral; no removable axial pin brake |
| Assembly envelope |70×50-mm foot;118.2–158.2-mm tray top above foot underside; no array or head envelope implied |

The screw handwheel stays resident and may rotate freely during hold tests.
Thrust capture is not moment fixity or proof of passive retention. Both pin
end stops act before reduced thread overlap, but are **manual contact limits**,
not qualified crash stops: continued turning can damage the thread/fixture.

Two frame halves contain the shared-style guides and bearing seats. Two loose
3.2×4×3.2-mm keys enter3.6×4.4×3.6-mm split pockets; external tape closes the
common rails. No adjustable bearing tower or unexplained fine alignment step.
The second root land has two halves sliding out of rail slots after unloading;
main radial/thrust support stays in place. Pair replacement opens the common
frame, without destructive separation. Tape seam opening and fitting time are
explicit failure observations, not automatically adequate fixture stiffness.

**Sensitivity:** the matched coaxial pair clears, while a rigid.2-mm lateral
pin/screw offset atq22 gives1.243 mm³ interference. This is a failure witness,
not a process prior or probability. Opposing XY bias, print bow, loose key/guide
contacts and two-half registration can consume the nominal clearance. Stop if
assembly needs pushing, bending or fine adjustment; do not add hardware or start
an iterative fit campaign. One functioning sample cannot establish4096/6400 yield.

## Export, manufacture and checks

Source: `tools/curated-experiment-checks/E-263/article.scad`, `export.py`, `check.py`.
For CTO reproduction, obtain a **clean** BOSL2 checkout at136e6367e65d52196a3ea51d03156f8b622c60fc
in a directory namedBOSL2; export.py checks commit and clean status. With OpenSCAD
on PATH and Python dependencies NumPy/trimesh/manifold3d:

```
python3 tools/curated-experiment-checks/E-263/export.py --bosl2 /path/BOSL2 --output /scratch/exports
python3 tools/curated-experiment-checks/E-263/check.py /scratch/exports --pack /scratch/s40-calibration.stl
```

Used OpenSCAD2023.09.11. The dated CGAL ASCII screw export has last-decimal vertex
seams; conversion through manifold float32 topology yields a watertight solid.
The checker requires unchanged bounds within.00002 mm, volume difference<.001 mm³,
positive consistent winding and one material component for each part. **No hole
filling, smoothing or slicer auto-repair.** Only the verified binary combined
plate STL is handed off; it is reloaded and checked again, eight separate solids.

- 252 phase/axial-float states: zero computed thread intersection; pin/frame and
screw/seat clear. Endfloat endpoints are sampled.00001 mm inside contact to
avoid finite-precision face-contact ambiguity; physical intervals are analytic.
- Wrong-direction control atq22.25 intersects8.834 mm³. Overtravel.1 mm beyond
lower/upper stops intersects31.296/4.096 mm³; excess screw float also collides.
- The two keyed frame halves, journals, optional land, key insertion volumes and
plate part separations clear nominally. No clearance-probability or contact-force
model is inferred from mesh booleans.
- Plate occupied bounds x5..229,y5..121.2,z0..86; eight parts,45.367 cm³ CAD solid
volume before infill/support. Each frame half70×116.2×25; pin28×28×86; screw24×24×80;
land halves44×10×2; two keys3.2×4×3.2. All bed minima z0.
- Visually inspected complete assembly and **imported final STL plate**. Frame
split faces are bed-down; handwheel is bed-down; pin tray is bed-down with the
pin inverted. Small frame recesses bridge up to4.8 mm. The inverted pin's final
8-mm shoulder needs externally removable tree supports for its1.8-mm overhang,
starting outside the tray and reaching inward. Never support the internal thread.

This is ready **to slice**, not already sliced or printed. Suggested PLA/.4 nozzle/
.12-mm layers and3–5-hour/40–65-g estimates are uncalibrated; record actual slicer
values. Thin walls, thread overhangs, tall support removal and slender screw are
real first-print risks. Stop rather than force cleanup or adjust fits. Existing
tape/ruler/phone/scale only; no purchase. The two frame halves, two keys, two land
halves and pair total eight parts. Time assembly and intact pair replacement.

## Test decision and machine boundary

The short Dutch protocol/results form covers signed manual travel, loaded passive
hold at low/mid/high positions, reversal and free play, relative lateral/seat
compliance with/without the second root land, visible runout/alignment and handling.
Known force/displacement may support stiffness estimates; finger-feel comparisons
remain qualitative. Weighed miniatures and separate stress objects are distinct.
Conservative external test cap10 g is **not a rated load**; total moving mass also
includes the pin. Skip unknown/unstable loads. No pressing-to-failure, damaged
specimen reuse or motorized test. Any later powered test needs supported drive
and measured compliance/runout, not this mesh pass.

S40/N20 is the simpler control. S50/64-thread/96-pin/N30 stays deferred. The wide
tray, shoulders, tape and oversized handwheel are accessible laboratory features,
**not a pitch-compatible repeated cartridge or production end-stop solution**.
Resident baseline remains4096/6400 pins, screws, thread pairs and thrust/radial
duties plus8192/12800 shared-guide apertures. A second root land adds4096/6400
radial/alignment duties; this test decides whether it helps, not whether to install
thousands. Shared molded/machined beds remain alternatives to printed alignment,
but no tooling, assembly route or price is qualified here.

No new speed/BOM pass: E-262's64-grid/lead3/850-rpm scenarios give35.54/43.29-s
shallow/deep maxima versus~30 s; even850 rpm is not physically earned. E-259's
$984.64/$1166.40 motor/driver subset plus unquoted reserve still excludes support
corrections, versus$500 and$1000/$1500 comparators. This job does not choose pitch,
finish price, owner preference or a head. It is optional and never blocks other
research; no reminders or ongoing owner-wait task are created.

Repository check: the task checkout and unchanged main both report only
`Oversized instructions: AGENTS.md` and
`Oversized instructions: owner-print-tests/AGENTS.md`. These pre-existing guidance
size failures are preserved; no instructions/tooling change is made for this job.
