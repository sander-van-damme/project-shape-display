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
|30° upright|off|.92|14m18–25s|2040 /0|
|30° upright|on|5.09|55m42s|2040 /29755|
|90° horizontal|off|.83|11m35s|126 /0|
|90° horizontal|on|1.21|16m17s|126 /4783|
|90° upright|off/on|.76|10m40–50s|0 /0|
|90° horizontal|on, three-layer common raft|3.41|30m53s|126 /7005|

Fresh replay reproduced segment counts and material;upright time estimates varied
by seconds across exports/runs. Ranges include both runs,not calibrated timing
uncertainty. Exact support-off/on time equality was an invalid regression check;
checks now require absence of support roles and equal reported material.
No bridge roles in these slices. Upright 90° has no support roles, including when
support is enabled. In both supported horizontal profiles, interface-path
midpoints beneath each of the three projected threads occupy every 1-mm axial
bin over64 mm (checked per screw,not just their union).
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

**Whole-pair accounting:** channel4057s/9.41cm³ +90° nut1571s/3.14cm³ +
screw slice,each for three copies. Excludes journals,collar,socket,frame,fixtures,
scrap and joining;not optimized plates or an X1C forecast.4096/6400 are replication
controls,not fine-grid compatibility.

|Cells|Upright whole pair h/L|Supported horizontal h/L|Common raft h/L|
|---:|---:|---:|---:|
|1024|594.30–595.25 /4.543|626.25 /4.697|709.31 /5.448|
|4096|2377.20–2380.99 /18.173|2505.01 /18.787|2837.24 /21.791|
|6400|3714.37–3720.30 /28.395|3914.07 /29.355|4433.19 /34.048|

AtN cells,retainN channels+nuts+screws,N joins,2N guide apertures andN individual
screw release/inspection duties. Supported horizontal/raft exposesN working
threads to support. Exact adhesion-contact count,release force and scars remain
unknown;segment replication is a deposition proxy,not a physical contact count.
Hypothetical16-screw grouping gives64/256/400 groups:assumed30s/group adds
.533/2.133/3.333h **before** individual duties.16-up slicing,release and its setup
rate are unqualified;do not substitute them for three-copy machine estimates.

Channel/nut handling and joining at three10–30s operations per cell,plus5min per
assumed24-channel/289-nut plate,are12.45–29.52,49.63–117.90,77.50–184.17h.
These exclude E-276 installation base (10.94–23.69h at1024),screw cleanup,tooling,
cure,scrap and commissioning. Additional10/30/60s screw cleanup gives
2.84/8.53/17.07h at1024,11.38/34.13/68.27h at4096,and17.78/53.33/106.67h at6400.
Labor scenarios,not observations;correlated batch failure can add whole-plate
rework. The source reuses E-277's component/handling ledger rather than dropping
it when adding screws. No purchased-cost,RPM,retention,readback or~30s gameplay
improvement follows. Earlier~$500/~$1000/$1000–1500 and40-mm/finer-grid comparators
remain unchanged.

**Decision:** retain upright 90° as least-support control; horizontal support/raft
as removal comparators. None earns owner printing. Stop tie/angle/fit sweeps:
the raft adds time without removing 1024 release duties. Next evidence must change
whole-pair manufacture, including finished ends, or physically discriminate upright
stability from horizontal thread damage;another support-label audit cannot.

## Verification and scope

Three-component manifold/dimension/volume checks; nine actual slices; positive
extrusion totals cross-checked against slicer footers; support-role,per-screw64-bin exposure and raft-gap
witnesses; generated toolpaths visually inspected. Self-review only. Slicer 2.7.2,
OpenSCAD 2023.09.11, BOSL2 `136e6367e65d52196a3ea51d03156f8b622c60fc`,
E-277's explicit-slop matched profiles. Python needs numpy, trimesh, manifold3d,
matplotlib. Source imports E-277's reusable parser/CAD/profile;generated outputs
remain scratch. No physical printing, process yield, loaded speed or qualification.


## Complete-screw deposition extension

**Finished ends change the support obligation and accounting, but do not rescue
screw-only casting as a whole-pair production solution.** `finished_batch.py`
uses the same CLI/profile/dependencies, with E-280's unchanged 90° screw,
128 facets, three copies at10-mm spacing. These are assumed finished journals,
collar and socket, not qualified support hardware. Finite mesh checks reproduce
405.703mm³/part and4.4×4.4×78mm envelope; three disjoint manifold solids per plate.
Four actual Prusa2.7.2 slices,2026-10-14, plus analysis replay:

|Orientation|Support|Time/three|cm³/three|Bridge / overhang / support-interface segments|
|---|---|---:|---:|---:|
|Upright|off|14m39s|1.11|60 /0 /0|
|Upright|on|17m14s|1.44|60 /0 /386|
|Horizontal|off|15m45s|1.24|42 /660 /0|
|Horizontal|on|26m41s|2.28|42 /660 /9117|

Upright socket faces the bed:60 bridge segments occur atZ2.2mm over its nominal
2-mm-deep blind cavity. Enabled support has69 interface segments within the
socket's axial region and317 in the lower-journal region; no support or bridge
paths occur in the64-mm threaded region. This is not the bare shank's
support-free result. Generated supports extend outside the driver/journal and
into the socket; removal and socket/seat fit remain unmeasured. Unsupported
bridging is also unqualified. A wider bed contact does not qualify the now78-mm
tall print's evolving slender span, adhesion or straightness.

Horizontal head radius2.2mm leaves the3.2-mm thread envelope0.6mm above the bed;
only the driver/collar has first-layer part paths (X10.225..15.775mm).
The unsupported slice is an intentionally adverse comparison, not a printable
alternative. Enabled interface midpoints beneath **each** screw occupy all64
axial1-mm bins of the thread, plus journal/socket regions. Both orientations
therefore retain N individual release and functional inspection duties; segment
counts describe deposition, not adhesion contacts or measured scars. No extra
clips, profile changes, supports or owner-print job were designed.

Reusing channel+nut5628s/12.55cm³ per three, the completed-screw comparisons are:

|Cells|Upright support off h/L|Upright support on h/L|Horizontal support on h/L|
|---:|---:|---:|---:|
|1024|616.96 /4.663|631.66 /4.775|685.42 /5.062|
|4096|2467.84 /18.650|2526.63 /19.101|2741.67 /20.248|
|6400|3856.00 /29.141|3947.85 /29.845|4283.85 /31.637|

These replace bare-shank accounting only when using E-280's exact assumed ends;
they remain three-copy repetition, not optimized-plate or X1C forecasts.
Screw-only print time at1024 is83.34/98.04/151.80h respectively. The unsupported
upright screw now represents13.51% of joined-pair print hours, versus the former
bare-shank10.21%; neither is a universal bound. Compare E-280's assumed39.82–54.40h
casting occupancy to these finished-screw values, **not** bare-shank60.68h.
With unchanged channel/nut printing, its573.44–588.02h serial resource sum is
only4.69–7.05% below unsupported-upright616.96h, before tool fabrication and
casting exclusions. Independent equipment can overlap; this is not calendar
lead time or a measured casting advantage. E-280's40.90–104.67 maker-hours still
apply. Upright integral U/closed columns from E-277 would instead total676.31/
794.07h with the unsupported complete screw, before frame/scrap: eliminating
column joins does not make screw deposition the dominant remaining process.

**Decision:** close the finished-end accounting gap; retain upright as the lower
support-burden comparison, not a print-ready or selected process. Do not reopen
screw-only molds or socket/support micro-tuning from these times. Useful next
research must remove substantial whole-pair manufacture/assembly or establish
actual process/support evidence. E-281 remains the single optional owner test.
No changed~30s gameplay claim, price pass, retention, readback or repair proof;
12.7-mm/1024,S40/S50,N20/N30 and the5.08-mm/6400,~40-mm,~$500 references remain
as above. Fine-grid replication here is burden only, not geometric compatibility.

Verification: finite dimensions/volume/component count; all positive extrusion
cross-checked against slicer material footer; four support-on/off comparisons;
per-screw support coverage, socket bridge-height and head-only first-layer
witnesses; plotted paths inspected. Analysis replay passes. Self-review only;
no physical print, measured labor, speed or yield. Generated meshes/G-code/plots
are scratch, with executable source retained.
