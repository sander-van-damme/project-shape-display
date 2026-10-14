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

Socket access:36-mm reach,2-mm-AF tip in2.8-mm bore (.2453-mm nominal radial gap),
axis6.3207mm from ring edge. Four spaced spindles cannot inherit uniform routing
across widened seams. Cradle pads meet ring lips before mounts release; 1mm shelf+
1mm pad leave only.2mm separation. Minimum24.50N/module/.766MPa pad loading excludes
some parts and acceleration. Constrained232-mm lift/.3206° yaw allowance does not
earn tolerant transfer or broken-part restraint. Opening a keeper needs restraint.

At1024 cells:2048 bodies/screws,2048 guide apertures,1024 thrust contacts,256 keeper
halves,128 spines,64 panels,48 rings,64 mounts,512 guide seats. The1088 frame
interfaces imply6.04–18.13h at assumed20–60s each before exclusions;4096/6400
count-only scaling24.18–72.53/37.78–113.33h. Shell/rings3.56kg+spines1.12kg excludes
guides/keeper. Gross room above E-276's$798 is$12.63/$43.88 per module toward
$1000/$1500, not a quote or net frame budget. Park cage and narrow-joint refinement.

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

## Restrained whole-guide service and assembly stop

Keeper capture does not laterally restrain bodies. Passing a temporary sleeve
through every occupied guide leaves only(10.8−10.3)/2=.25mm wall/side before clearance.
Reject that fragile1024-site fixture. A split temporary guide duplicates registration
and obstructs withdrawal; shared restraint is not free.

The simpler safe-order construction removes **bodies**, retaining screws in the bed
and keeper. It is an offline overhaul, not preserved map state or qualified repair:

1. Clear miniatures,save desired terrain,isolate/park writer. Upright bench stand
   provides underside access and fragment catch. Keep both guides,bed,keeper and
   edge reactions attached; do not invert an unrestrained array.
2. One reusable top gripper holds body weight/rotation before a controlled manual
   underside driver unthreads it. Upper guide/gripper restrain the body as it leaves
   the lower guide. Screw stays in its original radial seat/capture. No powered
   overtravel command proves release. Do not open keeper or lift pairs together.
3. Lift the body through the upper aperture into a numbered closed storage channel.
   Repeat with both guides installed. A10.3-mm jaw opening plus.8-mm external jaws
   gives11.9mm outside versus12.7 pitch; gripper does not pass through a guide.
   This is an envelope, not earned force/access/tolerance performance.
4. A jammed/bent body blocks guide removal. After healthy neighbors are removed,
   shared clamp/catch tooling may permit sacrificing the failed body in sections.
   Cutting and debris/fragment restraint require case-specific construction; do not
   assume automatic release. If safe clearance cannot be established, keep cage
   closed. The state replay refuses removal with even one body remaining.
5. Only after physically verifying zero bodies/fragments may a guide be lifted.
   All1024 screws retain bed radial seats/keeper; guides never supplied a far-tip
   bearing. Refit/register guide before rethreading/checking bodies. Restore and
   verify terrain; saved commands are not measured heights.

Source replays support order and last-body refusal, not grip/contact/damaged-part
qualification. No universal safe extraction of arbitrarily broken pairs is claimed.
Count one gripper,driver,bench stand/catch tray,32 storage trays×32 channels and32
closures, plus damaged-target tools. Assumed406.4×150×16-mm trays occupy31.21L before
rack/handles; storage channels need clearance, not precision working fits. Folded/
machined board or sheet,outsourced or joined trays owe material/labor; no free fixture.

At least2048 transfers plus2048 thread release/start events. Assumed10–30s/transfer
alone costs5.69–17.07h, excluding turns,fixtures,damage,alignment,proof and restoration.
4096/6400 count-only control22.76–68.27/35.56–106.67h. Initial aperture cleanup above
remains additional. One trapped fault reopens1024 rethreading operations: **stop
whole-guide repair development before local sleeve/lock/fit CAD.**

Next decision: retain broad bed action, reopen only with a materially different
bounded service partition/transfer or earned process avoiding array-wide rethreading,
narrow seams and thousands of closures. Whole-pair manufacture and powered support
remain unresolved; no further local frame refinement or owner print selected.
Existing E-276 conditional850rpm S40/S50 local26.84/31.07s,scene201/223s,neutral271/
332s,dense392/452s remain comparisons to~30s, not earned speed. Keep12.7 versus
6.35/5.08-mm pitch,40/50-mm travel,paid elevated neutral/downward travel and
~$500/$1000/$1500 cost distinctions. This stiffness result earns no faster play,
cheaper complete machine or permission to purchase.
