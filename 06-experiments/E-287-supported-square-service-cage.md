---
status: complete
builds-on: [E-286, E-277, E-280, E-269]
---

# Screw support: modular cage versus continuous sheets

**Park the fabricated modular cage; retain the coarse continuous-sheet control
conditionally.** Whole sheets remove interior seams and joins but enlarge the
service scope. Neither construction qualifies support, speed, repair or manufacture.
Evidence: analytical statics, rigid envelopes and allocated interfaces, self-reviewed;
not CAD/contact FEA or physical measurements. No purchase/new print; E-281 is optional.
Reproduce cage: `python3 tools/curated-experiment-checks/E-287.py`.
Sheet source and controls are below. Outputs are disposable; source preserves detail.

## Modular cage: preserved failure and reopening conditions

Sixteen8×8 modules retain E-277's12.7-mm pitch,10.3-mm columns and0–50-mm travel;
bases Z2…52,tops Z138…188. Each module has16 perforated12×2-mm guide strips
at Z54…56/134…136,16 closed keeper halves and eight12×24-mm hollow thrust spines
at Z−34…−10. Three machined square rings (2.2-mm radial width×8-mm height) at
Z46…54,126…134,−42…−34 receive guides/spines **on** their faces. Four .8-mm sheet
sidewalls form a shear shell with joined corners. Assembled-bar rings instead
add12 corner joints/module. No joint/process qualification is implied.

Gravity: thread→driver→perforated spine→lower ring→four mounts→board frame.
Guidance: body→strips→upper/middle rings→panel/corner shear paths→lower mounts.
Keeper attachments carry upward loads. Local contact, buckling, torsion, attachment
compliance and thread holding remain unqualified; frame stiffness cannot replace them.

E-277's sufficient body projection12.2415mm plus .2mm/side rigid reserve gives
101.5415-mm ring opening,103.7415-mm reaction span,107.5415-mm module exterior.
With .4-mm inter-module gaps,32² pitch footprint425.424mm and enclosure431.366mm
exceed406.4mm. Interior top seams widen2.4→8.7415mm. Neither miniature usability
nor the .2-mm collision reserve is qualified; loaded lean/joints consume clearance.

Assume polymer E2GPa,metal E70GPa,ν.33. At .05N/cell at **each** guide, total6.4N
lateral/module: guide bend .03406mm +ring .04806 +ideal shell .00137 =.08350mm.
Four3×3×.8-mm corner posts without shear panels give6.4601mm, outside precision
small-deflection use. Against an allocated .1mm budget, only .01650mm remains;
correlated .02/.05-mm joint movement gives .10350/.13350mm. The linear no-joint
threshold is .05988N/site, not a safe rating. No micrometre joint optimization.
At .338N/site axial diagnostic, spine .00479mm +lower ring .02457 +panel compression
.000164 excludes self-weight, local face bending and settlement. Not typical
miniature loading or a hardware pass; thrust friction still enters motor torque.

Checks:32k→64k guide integration<.2%,strong/weak section brackets,central-load
FL³/(48EI),force balance and positive support-state replay. Joint/model errors
dominate numerical error. The perfect shell uses two in-plane walls with
I=2tL³/12 and shear area2tL; actual connections are not demonstrated.

Nearest socket axis is6.3207mm from inner ring edge. A2-mm-AF tool has2.3094-mm
corner diameter in2.8-mm bores,nominal radial clearance .2453mm. Reach from lower
ring underside into driver is36mm. Four25.4-mm-spaced spindles cover64 sites in
two parity groups/row, but cannot batch across widened boundaries. No inherited
uniform-grid routing or optical calibration is a prediction for this cage.

Service proposal: clear miniatures,park writer,secure broken targets/fragments;
four bench-lift pads meet inner lower-ring lips **before** mounts release. Installed
shelves occupy outer lips. Allocating1mm to each leaves only .2mm separation.
Transfer closed module to bench nest before withdrawing cradle. Separate restraint
is still needed before opening the eight-site keeper row. Four1×8-mm pads see at
least24.50N/.766MPa average from diagnostic cells/shell/rings/spines; omitted guides,
keeper,fasteners and acceleration preclude a rating. At .1mm drift/.4mm gap,
sufficient yaw allowance .3206° requires constrained lifting. Lift232mm to clear
neighbor tops (versus224mm prior module). No tolerant transfer,broken-part restraint,
repair time or actual-height restoration has been constructed.

At1024 cells retain2048 bodies/screws,2048 guide apertures,1024 thrust contacts,
256 keeper halves,128 spines. Add64 panels,48 monolithic rings,64 mounts,512 guide
seats. Per-module minimum interfaces:12 ring/panel+32 guide seats+16 spine seats+
4 corner seams+4 mounts=68,or1088/board. One assumed20–60s operation/interface
alone costs6.04–18.13h,excluding fabrication,extra fasteners,inspection,fixtures and
rework. Metal shell/rings3.56kg plus polymer spines1.12kg excludes guides/keeper/etc.
4096/6400 **count-only** scaling gives4352/6800 interfaces and24.18–72.53/
37.78–113.33h; coarse geometry does not fit fine pitches.

E-276 optimistic$798 leaves gross$12.63/$43.88 per16 modules toward$1000/$1500,
before omitted hardware; replacement frame allowances must be netted. No quote,
finished price or purchase authority. Conditional850rpm S40/S50 local26.84/31.07s,
scene201/223s,neutral271/332s,dense392/452s remain references versus~30s,not new
performance. Ideal64-cell S50 reset+N30 restore1.569min excludes repair/routing/proof.
Reopen only with materially simpler frame/transfer or process evidence; shorter
guides and nominal contact area do not earn a complete machine.

## Continuous-sheet control: fewer joins, larger shared service scope

**Retain coarse sheets for coupled plate/access work; park the3-mm unsupported
bed under its stated load scenario.** Two full guide sheets,one thrust bed and
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
agreement<1e−7, and mass/aperture accounting. Self-review only. **Continue only the
coarse shared-sheet load/access question; do not refine cage joints or optical
patterns.** A coupled perforated-plate model can resolve the present stiffness
ambiguity; a viable service sequence must accompany any subsequent selection.
