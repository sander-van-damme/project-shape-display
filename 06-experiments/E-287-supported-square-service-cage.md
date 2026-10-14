---
status: complete
builds-on: [E-286, E-277, E-280, E-269]
---

# Screw support: modular cage versus continuous sheets

**Park the modular cage and whole-guide repair embodiment. Retain coarse coupled
bed action as a structural control.** Broad sheets remove interior seams and joins,
but a trapped-body repair still requires extensive teardown. Evidence: analytical
statics, linear plate FEA, rigid envelopes and allocated interfaces; self-reviewed,
not physical qualification. No purchase/new print; E-281 remains optional.

Reproduce with `python3 tools/curated-experiment-checks/E-287.py`,
`E-287-sheet.py --check` and `E-287-plate.py --check` in the same directory.
The latter needs NumPy2.5.4/SciPy1.18.1/scikit-fem12.0.2 (tested versions).
Source preserves further numerical detail; generated outputs are disposable.

## Modular cage: preserved failure

Sixteen8×8 modules at12.7-mm pitch contain10.3-mm columns,0–50-mm travel,
16 perforated guide strips,16 keeper halves,eight hollow thrust spines,three
2.2×8-mm metal rings and four.8-mm shear panels each. Guides at Z54…56/134…136;
spines Z−34…−10. Gravity passes through thread/driver,spines,lower ring,mounts;
lateral loads through guides,rings,shell,mounts. Upward loads require keepers.

E-277's12.2415-mm body projection plus.2mm/side reserve gives101.5415-mm opening,
103.7415-mm reaction span,107.5415-mm exterior. With.4-mm module gaps, footprint
425.424mm,enclosure431.366mm and8.7415-mm top seams replace406.4mm/2.4-mm seams.
Neither reserve nor miniature usability is qualified.

Assumed E2/70GPa polymer/metal,.05N/site at each guide: lateral deflection
.03406 guide+.04806 ring+.00137 ideal shell=.08350mm; post-only control6.4601mm.
Only.01650mm remains against illustrative.1mm allocation; .02mm common joint
movement defeats it. At.338N/site axial diagnostic, spine.00479+ring.02457+
panel.000164mm excludes own weight,local contact and settlement. No joint tuning.
Checks: quadrature,section brackets,central-load identity,force/support-state balance.

Socket reach36mm;2-mm-AF tool in2.8-mm bore leaves.2453-mm radial nominal gap.
Edge socket is6.3207mm from ring edge. Nonuniform seams invalidate inherited routing.
Cradle-before-mount-release replay retains support,not contact qualification:
1mm shelf+1mm pad leave.2mm separation;24.50N/module/.766MPa excludes parts and
acceleration.232-mm lift/.3206° yaw and broken-part restraint remain unearned.
At1024:2048 bodies/screws,2048 guide apertures,1024 thrust contacts,256 keeper
halves,128 spines,64 panels,48 rings,64 mounts,512 guide seats.1088 frame interfaces
owe6.04–18.13h at20–60s each;4096/6400 count-only24.18–72.53/37.78–113.33h.
Shell/rings3.56kg+spines1.12kg exclude guides/keeper. Gross room above$798 is
$12.63/$43.88 per module toward$1000/$1500,not quotes/net frame budget. Park cage.

## Continuous-sheet construction and independent controls

Two whole guide sheets,one thrust bed,four.8-mm perimeter panels replace interior
rings,seams,guide strips and spines. Exterior ledges receive all four sheet edges;
176-mm closed shell carries reactions to the table. Ledge width,fasteners,registration
and keeper attachment remain unconstructed. No interior seam, but exterior growth.

Compare406.4-mm fields:32² at12.7 pitch/10.8-mm guide openings,64² at6.35/4.64,
80² at5.08/4.64. Fine cases use smaller historical bodies, not coarse10.3-mm bodies.
Guide upper faces remain Z56/136;3/6-mm thickness needs fresh body/contact checks.
Gravity: thread→collar→bed→ledges→shell→frame. Allocated3.6-mm bed bores,3.2-mm
journals,4.4-mm collars are compatibility requirements, not E-280 fit passes.
Writer enters from below; capture,finished driver datum,friction and RPM are unearned.

`E-287-sheet.py` uses E70GPa,ν.33,ρ2700kg/m³ and ideal continuous reactions.
Perforated independent strips integrate actual hole intervals: lateral
`I=t(p³−a³)/12`, vertical `I=(p−a)t³/12` inside cuts; full sections outside.
Bed circles become equal-width square cuts for stiffness only. Independent Navier
solid plate: `D=Et³/[12(1−ν²)]`, `w≈.004062qL⁴/D`. Neither control is a certified
bound on every coupled/local displacement. Shell uses perfect two-wall shear/bending.

Resident baseline .06N/site is an assumed~6g pair allocation, not measured weight
or fine-pin prediction. Diagnostic .338N/site means346N/1024 before bed weight,
not ordinary miniature loading. Both controls include actual circular-hole bed mass.

|Cells/thickness mm|Lateral strip+shell mm|Bed baseline solid/strip mm|Bed diagnostic solid/strip mm|Field sheets+shell kg|
|---|---:|---:|---:|---:|
|1024/3|.0933|.2799/1.1200|1.3605/5.4442|2.612|
|1024/6|.0473|.0408/.1634|.1759/.7039|4.606|
|4096/6|.4634|.1259/.7889|.6662/4.1737|5.112|
|6400/6|2.9980|.1898/1.8597|1.0340/10.1338|3.125|

Park unsupported3-mm bed under this load. Large linear deflections are warnings,
not physical failure predictions. Uniform.02N/site guide drag gives1.631/.204mm
for1024 at3/6mm: simultaneous-binding diagnostic, not four writers or stationary drag.
At1024/6 the lateral.1mm allocation leaves.0527mm before joints; .05mm common
connection movement nearly consumes it. Fine equal-per-site cases are not equal-mass maps.

Sixteen continuous connections total5.581m, not16 easy touches. At1024,3072 apertures/
100.05m cutting owe4.27–17.07h at assumed5–20s cleanup each;4096/6400 owe
17.07–68.27/26.67–106.67h. Outsourced cutting,deburring,gauging could change this;
router radii,taper,burrs and square-corner relief are unqualified. All sheets exceed
256-mm print width. Mass excludes rims,fasteners,keepers. Net replaced frame
allocations before quoting; gross$202/$702 above$798 is not available free hardware.

## Coupled bed calculation resolves the stiffness ambiguity

`E-287-plate.py --circle --refine 1` and `--circle --refine 2` solve a quarter bed
with256 explicit holes mirrored to1024. Morley bending energy:
`D∫[(1−ν) Hess(w):Hess(v)+ν Δw Δv]dA`. Zero normal slope at symmetry planes;
zero exterior deflection/free rotation; free hole edges. Method follows the primary
[scikit-fem plate example](https://github.com/kinnala/scikit-fem/blob/12.0.2/docs/examples/ex02.py).
Circular boundaries use8/16 segments; fine mesh65,536 triangles/135,681 DOFs per
quarter. Omit `--circle` for3.6-mm square cuts; `--hole 2.545584412` gives inscribed
squares; `--edges clamped` gives favorable rotational restraint. No fitted strip blend.

Separate loads: resident61.44N, bed24.591N, total86.031N. Resident forces are smeared
over remaining metal, excluding local collar contacts. Geometry controls keep total
force fixed. Sixteen assumed20g miniatures add3.139N over sixteen25.4-mm square
footprints, spread symmetrically or clustered in the central101.6-mm square. These
are light-load scenarios, not measured populations/typical occupancy. Patch forces
are normalized over remaining metal. Dense diagnostic adds284.672N independently.

|Simply supported case|Peak bed displacement mm|
|---|---:|
|Solid numerical/independent Navier baseline|.040844/.040822|
|Circular resident alone/bed alone, fine|.033990/.013604|
|Circular baseline refinement1/2|.048145/.047595|
|Circular baseline+spread/clustered miniatures|.049791/.052102|
|Circular dense diagnostic including weight|.205082|
|Inscribed/circumscribed squares, refinement1 baseline|.046646/.051573|
|Circumscribed squares, refinement2 baseline|.050442|
|Clamped circumscribed squares, refinement1 baseline|.016173|

Solid analytical disagreement.053%; circular refinement change1.14%,square2.19%.
Residual/reaction balance checked to1e−5 relative. Independent strip checks retain
section/quadrature/point-load controls. Observed geometry ordering is not a certified
local bound. No independent reviewer or physical validation.

**Two-direction action resolves global baseline stiffness favorably; edges remain
conditional.** Common ledge settlement0/.02/.05mm makes clustered absolute deflection
.0521/.0721/.1021mm. Common movement shifts writer datum but not necessarily relative
terrain; unequal settlement also distorts it. Assumed E50GPa/thickness5.5mm multiplies
bending1.818: clustered.0947mm+.02 settlement=.1147mm, holding bed weight fixed
conservatively. These are correlated bounds, not process priors. Missing edge contact
cannot be replaced by small settlement; clamping needs a moment-carrying connection.
The.1mm allocation is not a universal player-derived gate.

Kirchhoff theory omits shear/local3D behavior; thickness/hole diameter1.67 especially
invalidates local thin-plate stress claims. No collar indentation/pull-through,
screw-seat stiffness,guide drag,warp,joints,panel/rim or vibration rating follows.
The guide's10.8-mm apertures are not qualified by this bed calculation.

## Restrained whole-guide service

**Park whole-guide repair: one trapped body expands teardown to the whole array.**
Keeper capture does not laterally restrain bodies. Temporary sleeves through
10.8-mm occupied guides around10.3-mm bodies leave only.25mm wall/side before
clearance; reject this fragile1024-site fixture. Split temporary guides repeat
registration and obstruct withdrawal.

The source replays this safer order, not grip/contact or damaged-part qualification:
clear miniatures/save desired state/isolate writer; support the upright board on
an underside-access stand with catch; keep both guides,bed,keeper and edge reactions
attached. One top gripper carries body weight/rotation while an underside driver
unthreads it. Upper guide/gripper restrain withdrawal; screw remains in its bed
seat/capture. Store each body in a numbered closed channel. A10.3-mm jaw opening
plus.8-mm jaws gives11.9mm outside at12.7 pitch; no earned grip/access/tolerance.
A jammed/bent body blocks guide removal. Sacrificial cutting needs independently
constructed access and fragment restraint; if unavailable, keep cage closed.
The replay refuses guide removal with even one body remaining. Verify zero bodies/
fragments before removing a guide; refit/register before rethreading and proving
terrain. Do not invert an unrestrained array or treat saved commands as actual state.

Count gripper,driver,stand/catch,damaged-target tools and32 closed trays×32 channels.
Assumed406.4×150×16-mm trays occupy31.21L before rack/handles; manufacture is unpaid.
At least2048 transfers plus2048 thread release/start events. Assumed10–30s/transfer
alone costs5.69–17.07h at1024,22.76–68.27/35.56–106.67h at4096/6400, excluding
turns,fixtures,damage,alignment,proof,restoration and initial aperture cleanup.
Stop whole-guide sleeve/lock/fit development; one fault must not inherit free teardown.

## Downward row extraction through fixed guides

**Flat rows have a nominal handoff window; mixed-height rows do not inherit it.**
Park this passive two-plane fixture, not all downward service. Reproduce with
`python3 tools/curated-experiment-checks/E-287-transfer.py`:32,040 interval cases,
endpoint controls and dimensional bounds. Analytical envelopes, not contact/CAD
or hardware qualification.

Replace the bed with32 removable12×24-mm row spines carrying closed keeper/thrust
(E-286); both guide sheets stay fixed. Clear miniatures,isolate/park writer,engage/
prove a guided bench elevator before releasing four row mounts. Lower intact pairs
without screw rotation; insert a shared split body-guide fixture below the lower
sheet, attach it to the cradle, then continue descent. Gravity remains
body→thread→screw→spine→elevator. Body restraint must transfer from fixed guides to
fixture. Broken threads need independent body capture; bent/jammed bodies cannot
be forced through guides. Reverse transfer for reinstall; catch/fragments remain owed.

The6-mm guides occupy Z50…56/130…136. Body interval is[2+h-d,138+h-d] for extension h
and row descent d. Test a24-mm fixture: two2-mm contact planes with20mm clear space,
**not a universal minimum span**. Lateral access/fit/stiffness are not credited.
Expose its whole span below Z50 before any body loses2mm upper-guide overlap:

`d >= max(0,2+max(h)+24-50)`; `d <= 138+min(h)-130-2`.

|Row state|Earliest insertion d, mm|Latest retained-guide d, mm|
|---|---:|---:|
|Mixed0/50|26|6|
|Mixed0/40|16|6|
|Flat N30|6|36|
|Flat S50|26|56|

Mixed S50 exposes at most6mm before upper overlap vanishes,4mm retaining2mm overlap.
At d8 low top=130/high bottom=44. A4-mm fixture has zero timing margin,not a pass.
Assumed body-length±.2/relative-guide-spacing±.4/height-range±.2mm bounds give
3.2…4.8mm; no measured distribution. Common datum translation cancels. A single
lower guide+screw could restrain differently but needs new contact/load evidence.
Homing cannot presume a failed target moves. Moving healthy neighbors to a known
stuck height is a distinct possible procedure,not proved here; unknown/broken targets
remain. Short clamps/sequential restraint owe32 gripping/moment reactions and proof;
do not proceed to narrow fixture/fit tuning.

S50 needs140mm descent to clear guides with2mm reserve; lateral exit beneath
neighboring spines at Z−34 still needs224mm. Writer access/removal,bench height and
constrained motion are unpaid. At1024:32 spines,64 keeper halves,128 mounts,one
32-site fixture/64 contacts,elevator/catch. Replacing the bed forfeits its coupled
plate result: rows carry gravity to perimeter supports. E-286 beam controls do not
qualify local thrust,mounts or frame. Fixed guide edges stay independently supported;
no ideal interior top seam, but coarse bodies still do not fit fine/quarter grids.
One-row teardown potentially transfers64 pairs versus2048; missing support handoff
prevents a repair claim. Count-only4096/6400:64/80 spines,256/320 mounts,128/160
fixture contacts. Fabrication/tooling are unpriced; no labor/cost/speed gain or new
print follows. Existing gameplay,neutral,dense and cost comparisons below remain.

Next decision: retain broad bed action, reopen only with a materially different
bounded service partition/transfer or earned process avoiding array-wide rethreading,
narrow seams and thousands of closures. Whole-pair manufacture and powered support
remain unresolved; no further local frame refinement or owner print selected.
Existing E-276 conditional850rpm S40/S50 local26.84/31.07s,scene201/223s,neutral271/
332s,dense392/452s remain comparisons to~30s, not earned speed. Keep12.7 versus
6.35/5.08-mm pitch,40/50-mm travel,paid elevated neutral/downward travel and
~$500/$1000/$1500 cost distinctions. This stiffness result earns no faster play,
cheaper complete machine or permission to purchase.
