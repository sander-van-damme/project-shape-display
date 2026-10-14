---
status: complete
builds-on: [E-286, E-277, E-280, E-269]
---

# Screw support: modular cage versus continuous sheets

**Park both the fabricated modular cage and the whole-guide service embodiment.**
Coupled plate action supports the coarse bed stiffness hypothesis; staged service
still requires a whole-board body teardown. Whole sheets remove interior seams
and joins but enlarge the service scope. Neither construction qualifies support, speed, repair or manufacture.
Evidence: analytical statics, coupled linear plate FEA, rigid envelopes and
allocated interfaces, self-reviewed; not contact qualification or physical measurements. No purchase/new print; E-281 is optional.
Reproduce cage: `python3 tools/curated-experiment-checks/E-287.py`.
Sheet source and controls are below. Outputs are disposable; source preserves detail.

## Modular cage: preserved failure

Source `E-287.py` retains geometry, load paths, checks and the interface ledger.
Sixteen8×8 modules at12.7-mm pitch contain10.3-mm columns,0–50-mm travel,
16 perforated guide strips,16 keeper halves,eight hollow thrust spines,three
2.2×8-mm metal rings and four.8-mm shear panels each. Ring-supported guides
are at Z54…56/134…136; spines Z−34…−10. Gravity passes through thread/driver,
spines,lower ring,mounts; lateral loads through guides,rings,shell and mounts.

E-277's12.2415-mm body projection plus.2mm/side reserve gives101.5415-mm opening,
103.7415-mm reaction span,107.5415-mm module exterior. With.4-mm module gaps,
footprint425.424mm,enclosure431.366mm and8.7415-mm top seams replace the intended
406.4-mm field/2.4-mm seams. Neither reserve nor miniature usability is qualified.

At assumed E2/70GPa polymer/metal and.05N/site at each guide, lateral deflection
is guide.03406+ring.04806+ideal shell.00137=.08350mm; post-only control6.4601mm.
Only.01650mm remains against illustrative.1mm allocation; correlated.02-mm joint
movement defeats it. At.338N/site diagnostic, axial spine.00479+ring.02457+
panel.000164mm excludes own weight,local contact and settlement. No narrow-joint
refinement. Checks include quadrature,section brackets,central-load identity and
force/support-state balance; these are analytical, not hardware qualification.

Socket access requires36-mm reach,2-mm-AF tip in2.8-mm bore (.2453-mm nominal
radial clearance). Nearest socket axis6.3207mm from ring edge. Four spaced spindles
cover64 sites in two parity groups/row but cannot inherit uniform-grid routing
across widened seams. Lift cradle meets lower-ring lips before mount release;
1mm shelf+1mm pad leave only.2mm separation. Minimum24.50N/module pad load,
.766MPa average excludes some parts/acceleration. Constrained232-mm lift and
.3206° sufficient yaw allowance do not establish a tolerant transfer or broken-part
restraint. Keeper opening still needs separate row restraint.

Board allocation:2048 bodies/screws,2048 guide apertures,1024 thrust contacts,
256 keeper halves,128 spines,64 panels,48 rings,64 mounts,512 guide seats.
1088 frame interfaces imply6.04–18.13h at assumed20–60s each before exclusions;
4096/6400 count-only scaling24.18–72.53/37.78–113.33h. Shell/rings3.56kg and
polymer spines1.12kg exclude guides/keeper. Gross room above E-276's$798 is
$12.63/$43.88 per module toward$1000/$1500, not a quote or net frame budget.
Park this cage: new broad sheets below change the topology; another ring/post/
joint sweep does not. Source preserves further disposable numerical detail.

## Continuous-sheet control: fewer joins, larger shared service scope

**Initial screen:** retain coarse sheets for coupled plate/access work; park the
3-mm unsupported bed under its stated load scenario. The extension below resolves
the global stiffness question and parks whole-guide service. Two full guide sheets,one thrust bed and
four .8-mm perimeter panels remove interior shells/rings/mounts/seams,not resident
threads,capture,radial seats,verification or broken-pair restraint. Source:
`python3 tools/curated-experiment-checks/E-287-sheet.py --check`; omit `--check`
for the six cases. Analytical strip/solid-plate controls, not sheet FEA or CAD.

### Construction and model boundary

Use a406.4-mm active square:32² at12.7 pitch/10.8-mm guide openings, alongside
64² at6.35/4.64 and80² at5.08/4.64. Fine cases use their smaller historical bodies,
not the10.3-mm coarse column. Compare3/6-mm sheet thickness. Broad exterior
ledges receive all four sheet edges; lower/upper guides keep their upper faces
at56/136mm, with80mm separation. The thicker contact zones need fresh actual
body/guide checks; E-277's envelope is not automatically transferred. A surrounding
176-mm-high closed shear shell receives both lateral and gravity reactions.
Exterior ledges/rims grow the enclosure, but no seam is introduced inside the
playfield. Their width, attachment and service access are unconstructed.

Gravity runs thread→screw collar→bed→external ledges→sidewalls→table frame.
Use E-269's3.6-mm bed openings as a support-screen allocation; its3.2-mm journal
and4.4-mm collar are a compatibility requirement, not an inherited fit pass for
E-280's different finished driver. A keeper must still react upward docking.
The writer reaches upward from below without an interior ring or spine; exact
socket/neck/collar datum, capture and torque friction remain owed. There is no
extra far-tip bearing and **no earned RPM**: lateral screw support still depends
on clearance/contact, not merely stiff sheets.

Assume E70GPa,ν.33,ρ2700kg/m³ and perfect continuous edge reactions. Independent
perforated row strips receive .05N/cell lateral guide force; no transverse
sheet action is credited. Integrate bending with the actual hole intervals:
`I=t(p³−a³)/12` inside square guide holes, solid `tp³/12` between holes.
Out-of-plane strips instead use `(p−a)t³/12`. Bed round holes are replaced by
square cuts of equal width for this strip screen. This is a compliant comparison,
**not a rigorous bound on every displacement of a coupled perforated plate**.
In-plane membrane redistribution may materially improve the real guide response.
The shell term retains the earlier perfect two-wall shear/bending approximation.
There is no narrow perimeter ring in series: sheet edges must actually transfer
loads continuously into the walls for this model to apply.

A separate Navier-series solution gives the **unperforated**, simply supported
square plate under uniformly distributed equivalent load:
`D=Et³/[12(1−ν²)]`, `w_center≈.004062 qL⁴/D`.
It is a favorable stiffness control, not perforated-sheet qualification or a
bound on local collar indentation. Strip and solid-plate results are alternatives,
not a certified interval. Clamping, contact, local stress, creep, joints, sheet
warp and loaded plate modes are absent.

### Results and load honesty

The .06N/cell baseline is an **assumed** roughly6g resident-pair allocation near
the coarse printed-body estimate, not measured weight and not a fine-pin mass
forecast. The .338N/cell case reproduces the earlier stock-body-plus-payload
stress allocation. At1024 it already means346N before bed weight, **not ordinary
miniature loading**. Both add the perforated bed's calculated own weight,
distributed equivalently. Guide loads and shell weight ultimately reach the
external frame; its deformation is excluded.

|Cells / sheet mm|Lateral strip+shell mm|Bed, .06N/site: solid / strip mm|Bed, .338N/site: solid / strip mm|Field sheets+shell kg|
|---|---:|---:|---:|---:|
|1024 /3|.0933|.2799 /1.1200|1.3605 /5.4442|2.612|
|1024 /6|.0473|.0408 /.1634|.1759 /.7039|4.606|
|4096 /6|.4634|.1259 /.7889|.6662 /4.1737|5.112|
|6400 /6|2.9980|.1898 /1.8597|1.0340 /10.1338|3.125|

Large linear deflections are warnings outside precision use, not physical failure
predictions. Uniform .02N axial guide drag/site gives1.631/.204mm at1024 for3/6mm
strips; this is a simultaneous binding diagnostic, **not four active writers**.
Do not infer that all pins drag while stationary. Finer-grid equal-per-site force
controls increase total load; they are not equally weighted playable maps.

At1024/6mm the old illustrative .1-mm lateral budget leaves .0527mm before
unmodeled connections, versus .0165mm for the module cage. This is no measured
margin, but a meaningful reason to prefer a broad shared path over tuning the
old narrow rings. A .05mm common connection displacement nearly consumes it.
At3mm even the favorable solid bed bows .280mm under the assumed baseline plus
its weight; the unsupported thin bed does not earn a .1-mm height allocation.
At6mm the coarse .041/.163mm controls straddle that allocation, so the next
useful discriminator is actual perforated-plate action and distributed support,
not a smaller joint-clearance sweep. The .1mm allocation is neither a universal
product gate nor a substitute for combined guidance/neighbor geometry.

### Manufacture, service and complete-machine consequences

Three sheets/four panels replace48 rings/64 panels/128 spines/64 module mounts
and separate guide strips. There are16 **continuous connection paths**, totaling
at least5.581m, versus1088 allocated cage interfaces; these are different units,
not a claimed98.5% assembly saving. Flanges, ledges, actual fasteners, registration,
keeper attachments and joints are not counted as free. Field-only mass excludes
all exterior rims, fasteners and keepers; the cage's3.56kg shell/rings plus1.12kg
spines also excluded its guides. Do not subtract these as complete assembly masses.

At1024 retain3072 guide/bed apertures and100.05m nominal aperture cutting, versus
12288/198.37m and19200/309.95m at4096/6400. Ideal square corners need a real process:
router radius, reliefs, laser/waterjet taper and burrs change functional openings.
All sheets exceed the256-mm printer bed. Outsourced sheet cutting/machining is a
process candidate, not a quoted source. Five–20s manual cleanup/aperture alone
costs4.27–17.07h at1024,17.07–68.27h at4096 and26.67–106.67h at6400. Automated
cut/deburr/gauge capability could change this; no individual hand-fit route is
selected. These hours exclude the existing pair assembly and whole-frame work.

**Service is the trade:** intact straight pairs may still exit through aligned
openings if capture permits it. Removing an entire guide to retrieve a bent body
or trapped fragment removes guidance from up to1024/4096/6400 columns at once,
versus64 in an8×8 module. A closed keeper does not replace lateral guidance.
Clear miniatures, park/isolate the writer and secure every affected pair before
opening; a shared bench fixture or safe staged disassembly is unconstructed.
No assumption of preserved map state, free recovery or convenient in-session
repair follows. This construction removes narrow module lifting gaps but broadens
the restraint/repair obligation. Do not add thousands of private closures to hide it.

Gross room above$798 is$202/$702 toward$1000/$1500;~$500 is already missed.
Net replaced frame allocations before sheet quotes; no cost saving is earned.
The earlier timing references,paid neutral/downward-travel intent and separate
dense stress still apply conditionally. Sheets earn no speed,readback or travel.

Checks: solid/minimum-section strip brackets,32k→64k quadrature agreement<.2%,
central-point-load identity, force and thickness scaling,61→121-term plate series
agreement<1e−7, and mass/aperture accounting. Self-review only. The following extension supplies the coupled bed calculation and service decision;
these initial strip controls remain reproducible comparators.


## Coupled plate and restrained teardown: decision

**Global bed stiffness is plausible; whole-guide service is not selected for further
local development.** The new result resolves the .0408/.1634-mm ambiguity in favor
of substantial two-direction plate action under ideal continuous supports. It does
not earn a bed/collar contact, guide, joint, RPM or physical support pass. The
safe-order service alternative below avoids 1024 simultaneous temporary locks,
but trades them for extensive removal/rethreading. Apply the assembly stop rule;
do not optimize thin service sleeves, individual locks or guide fits.

### Reproducible coupled model

Source: `tools/curated-experiment-checks/E-287-plate.py`, dependencies NumPy2.5.4,
SciPy1.18.1, scikit-fem12.0.2. Run `python3 …/E-287-plate.py --check`, then
`--circle --refine 1` and `--circle --refine 2`; omit `--circle` for circumscribed
3.6-mm square holes, use `--hole 2.545584412` for inscribed squares, or
`--edges clamped` for the favorable edge control. No generated output is retained.

Numerical simulation: quarter of the 406.4×406.4×6-mm bed, 256 explicit holes,
mirrored to1024; isotropic E70GPa, ν.33. Morley triangular bending energy is
`D∫[(1−ν) Hess(w):Hess(v)+ν Δw Δv]dA`. Zero normal slope at symmetry planes;
zero deflection and free rotation at exterior supported edges; hole edges free.
Circular boundaries use8/16 polygon segments at refinement1/2. Fine mesh has
65,536 triangles/135,681 DOFs per quarter. This is a coupled sheet, not fitted
strip interpolation. Method follows the primary
[scikit-fem plate example](https://github.com/kinnala/scikit-fem/blob/12.0.2/docs/examples/ex02.py).

Resident allocation stays .06N×1024=61.44N; round-hole bed weight24.591N, total
86.031N. These are separate load vectors. Resident forces are smeared over remaining
material, not applied as singular collar contacts. Solid/square controls keep the
same total force to isolate geometry. Two illustrative miniature layouts put
16×20g on sixteen25.4-mm square footprints, total3.139N: distributed symmetrically
across the board or clustered in its central101.6-mm square. These are plausible
light-load scenarios, **not measured miniature populations or typical occupancy**.
Patch forces are normalized over actual remaining metal. Dense extra load is
(.338−.06)N×1024=284.672N, separately added to resident and bed weight.

|Simply supported result|Peak bed displacement mm|
|---|---:|
|Solid numerical / independent Navier, baseline|.040844 / .040822|
|Independent perforated strips, baseline (earlier source)|.1634|
|Circular holes, resident alone / bed alone, fine mesh|.033990 / .013604|
|Circular holes, baseline, refinement1 /2|.048145 / .047595|
|Circular holes, baseline + spread / clustered miniatures|.049791 / .052102|
|Circular holes, dense diagnostic including weight|.205082|
|Inscribed / circumscribed square cuts, refinement1 baseline|.046646 / .051573|
|Circumscribed squares, refinement2 baseline|.050442|
|Clamped circumscribed squares, refinement1 baseline|.016173|

Solid analytical disagreement .053%; circular refinement change1.14%, square2.19%.
Residual and translational reaction balance checked to1e−5 relative. The independent
strip source retains section, quadrature and point-load controls. Circle/square
ordering is an observed global sensitivity, not a certified local-displacement
bracket. No independent reviewer or physical validation is claimed.

**Edge/model uncertainty matters more than another mesh sweep.** Do not credit
clamping without a moment-carrying attachment. Common downward ledge settlement
of0/.02/.05mm adds directly to absolute bed height: clustered case .0521/.0721/
.1021mm. Equal common movement does not itself create relative terrain relief,
but can shift the writer datum; unequal settling also distorts it. Assumed E50GPa
and thickness5.5mm multiply force-induced bending by1.818: clustered .0947mm plus
.02 settlement is .1147mm (bed-weight term held fixed conservatively). These are
labelled correlated bounds, not process priors. Missing edge contact cannot be
represented by small settlement; strip/two-direction support alternatives remain
relevant until continuous ledges are constructed. The .1mm allocation remains a
comparison, not a player-derived universal limit.

Kirchhoff theory omits transverse shear and local 3D collar/edge behavior; t/d=1.67
at the holes makes local thin-plate stresses particularly unsuitable. No contact
stress, pull-through, screw-seat stiffness, panel/rim deformation, guide axial drag,
warp, joints or vibration rating follows. The guide's much larger10.8-mm apertures
are **not** qualified by this bed calculation. A global low-deflection result alone
cannot close loaded support.

### Whole-guide removal without releasing the array

A keeper retains screws; it cannot laterally restrain the tall bodies. A temporary
sleeve through every occupied10.8-mm aperture leaves only(.5/2)=.25mm wall per side
before any fitting clearance. Reject that fragile1024-site fixture route. A split
external temporary guide duplicates aperture registration and obstructs withdrawal;
it is not free shared restraint.

The simpler service construction is **empty the bodies while retaining the bed,
screw seats and keeper**, then lift an unloaded guide. Treat this as an offline
bench overhaul, not an in-session procedure or preserved map state:

1. Clear miniatures, save desired terrain only, isolate and park the writer, and
   hold the chassis upright on a bench stand with underside tool access and a
   fragment-catching tray. Both guides, all edge reactions, bed and keeper stay
   attached. Do not invert the unrestrained array.
2. Use one reusable top gripper to hold a body's weight and rotation before a
   manually controlled underside driver unthreads it. The existing upper guide
   and gripper restrain the body as it leaves the lower guide. Never use a powered
   overtravel command as proof of release. The screw remains in its original bed
   journal/capture; do not open its keeper or extract all pairs together.
3. Lift that body through the upper aperture and place it horizontally in a
   numbered, closed storage channel. Repeat; remaining bodies retain both guides.
   Tool geometry allocation:10.3-mm jaw opening with .8-mm external jaws gives
   11.9mm outside, .8mm less than pitch. It need not pass through a guide. This is
   an envelope, not qualified gripping force, access at all heights or tolerance.
4. A jammed/bent body is a **stop**, not permission to pull the guide. After healthy
   neighbors are removed, an accessible shared clamp and catch enclosure may allow
   the failed body to be sacrificed in sections while both guides remain installed.
   Cutting, debris containment and fragment capture need a case-specific safe
   construction; none is assumed automatic. If every body/fragment cannot be
   cleared safely, leave the cage closed. The model deliberately refuses guide
   removal with even one resident body remaining.
5. Only with the body count physically zero may the whole guide be unbolted and
   lifted. All1024 screws still retain their existing bed radial seats and keeper;
   the removed guide never supplied them a new far-tip bearing. Refit/register the
   guide before loading bodies. Re-engage and check every body, then restore and
   verify terrain. A saved command map does not prove actual recovered heights.

The source replays that support order and the one-body-left refusal. It is a
logical prerequisite check, **not proof of gripping, damaged-part release or hardware
safety**. No claim of a universal repair for arbitrary fractured pairs is made.

Count the service equipment: one gripper, one controlled driver, one upright
bench stand/catch tray,32 storage trays with32 channels each and32 closures, plus
any damaged-target clamp/catch tooling. A406.4×150×16-mm tray allocation occupies
31.21L stacked before handles/rack; channels are storage clearance, not precision
operating fits. All exceed the256-mm printer width: folded/machined board or
sheet trays, outsourced fabrication or joined trays owe labor/material/space.
These are allocations with no quote, force rating or free-fixture assumption.

At least2048 body transfers and2048 thread release/start events remain. Assumed
10–30s per transfer alone costs5.69–17.07h, **excluding** turning, preparation,
fixture fabrication, damaged-target work, alignment, inspection and restoration.
At4096/6400, the same count-only control is22.76–68.27/35.56–106.67h. Re-threading
1024 sites after a single trapped fault reopens the very manufacturing burden the
continuous sheets were meant to reduce. Existing3072 apertures/100m cuts and
4.27–17.07h assumed manual deburring remain in the initial-build ledger. Automated
cut/deburr/gauge could improve that initial work, but does not remove this teardown.

**Next decision:** park whole-guide repair and its fixture refinement. Preserve
coarse two-direction metal bed action as a useful structural control. Reopen only
for a materially different bounded service partition/transfer or an earned process
that eliminates array-wide rethreading without narrow module seams, thousands of
closures or fragile repeated fits. The task does not select another micro-CAD or
print step. Whole-pair manufacture and powered contact/support remain unqualified;
E-281 stays optional. The prior~$500/$1000/$1500 comparisons,12.7 versus6.35/5.08-mm
pitch, paid neutral,40/50-mm travel,~30-s update reference and separate dense waits
remain unchanged; this analysis earns neither a cheaper machine nor faster play.
