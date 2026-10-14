---
status: complete
builds-on: [E-277, E-263]
---

# Long-screw batch deposition and release

**The 90° profile removes upright screw support paths, but does not establish a
whole-pair production route.** `tools/curated-experiment-checks/E-279/screw_batch.py` uses E-277's pinned dependencies
and `--bosl2/--slicer/--output/--analyze-only` arguments. Nine actual slices on
2026-10-14 compare three identical 64×3.2-mm threaded shanks at 10-mm spacing,
.2-mm layers/.45 extrusion width, no brim, the existing comparison profile.
**Bare shanks only:** excludes journals, collar, socket and fixture. No owner print.
E-277's 12.7-mm/1024-cell, S40/S50 and paid N20/N30 controls remain unchanged;
the original comparator is 5.08 mm/~6400 cells, ~40-mm travel and ~30-s updates.

|Profile/orientation|Support|Filament cm³/three|Time/three|Overhang /support-interface segments|
|---|---|---:|---:|---:|
|30° horizontal|off|.87|12m54s|126 /0|
|30° horizontal|on|1.25|16m32s|126 /3617|
|30° upright|off|.92|14m18s|2040 /0|
|30° upright|on|5.09|55m42s|2040 /29755|
|90° horizontal|off|.83|11m35s|126 /0|
|90° horizontal|on|1.21|16m17s|126 /4783|
|90° upright|off/on, identical|.76|10m47s|0 /0|
|90° horizontal|on, three-layer common raft|3.41|30m53s|126 /7005|

No bridge roles in these slices. Upright 90° has no support roles, including when
support is enabled. In both supported horizontal profiles, interface-path
midpoints beneath the projected thread occupy every 1-mm axial bin over 64 mm.
**Segments/bins are deposition evidence, not counts of physical adhesion contacts
or measured scars.** The nut sweeps screw-local 2..62 mm over S50, so supports are
not confined to unused ends. No fit, strength, straightness, creep or yield measurements.
CAD volumes 302.617/290.713 mm³ per 30°/90° shank differ from deposited volumes;
100% infill is not exact geometry or a basis for dimensional compensation.

The 3-layer/4-mm-expansion raft has two first-layer support segments crossing
the 6.8-mm inter-shank gap; plain supports have none. A shared deposited carrier
is not clean group release. Individual thread separation/inspection remain.
It adds 2.20 cm³/14m36s per three; 16-piece production batches remain untested.
[Prusa support guidance](https://help.prusa3d.com/article/support-material_1698)
defines interface gaps and removal/stability tradeoffs;
[orientation guidance](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135)
warns that supported surfaces and strength depend on orientation. Neither source
qualifies this process. The comparison's .2-mm contact gap is not a rigid brace.

**Upright construction sequence matters:** end-only ties join after the full
64-mm slender span exists. They cannot brace earlier layers. Same-height ties
between equally flexible screws do not create a bed-anchored lateral constraint.
A mid-height anchored tie touches the functional thread unless the design changes.
For scale only, an isotropic fixed cantilever bounded by solid 1.4-core/3.2-outer
cylinders gives compliance 16.98–463.38 mm/N at assumed E=1000 MPa, 5.66–154.46 at 3000.
Assumed isotropic stiffness, not nozzle force, hot-polymer data, dynamics or a
predicted failure rate. Support-free paths do not establish growing-span stability.

**Whole-pair accounting:** adding the 90° shank to the existing three-channel/nut
slices gives repeated 1024-pair estimates: upright 594.96h/4.543 L; plain supported
horizontal 626.25h/4.697 L; raft 709.31h/5.448 L. Excludes screw ends, frame, fixtures, scrap, joints; three-copy repetition, not an
optimized-plate/X1C forecast. 1024 channels/nuts/screws and 1024 joints
remain. At 4096/6400 the supported-horizontal repetition is 2505.01/3914.07h;
this is replication burden, not dimensional compatibility of coarse columns.

At 1024, assumed 10/30/60-s screw cleanup adds 2.84/8.53/17.07 maker-hours to the
existing 23.39–53.21h baseline, which excluded cleanup. One minute adds 68.27/106.67h
at 4096/6400. Assumed 30s per 16-piece group adds.533/2.133/3.333h respectively,
**before individual cleanup**; common raft deposition does not earn that rate.
No purchased-cost, RPM, retention, readback or~30s gameplay improvement follows.
Keep the earlier~$500/~$1000/$1000–1500 and40-mm/finer-grid comparators unchanged.

**Decision:** retain upright 90° as least-support control; horizontal support/raft
as removal comparators. None earns owner printing. Stop tie/angle/fit sweeps:
the raft adds time without removing 1024 release duties. Next evidence must change
whole-pair manufacture, including finished ends, or physically discriminate upright
stability from horizontal thread damage;another support-label audit cannot.

## Verification and scope

Three-component manifold/dimension/volume checks; nine actual slices; positive
extrusion totals cross-checked against slicer footers; support-role and raft-gap
witnesses; generated toolpaths visually inspected. Self-review only. Slicer 2.7.2,
OpenSCAD 2023.09.11, BOSL2 `136e6367e65d52196a3ea51d03156f8b622c60fc`,
E-277's explicit-slop matched profiles. Python needs numpy, trimesh, manifold3d,
matplotlib. Source imports E-277's reusable parser/CAD/profile;generated outputs
remain scratch. No physical printing, process yield, loaded speed or qualification.
