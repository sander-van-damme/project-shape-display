---
status: complete
builds-on: [E-286, E-277, E-280]
---

# Supported square service cage

**Park this fabricated cage before joint/latch CAD.** A closed shear shell provides
a plausible reaction path absent from E-286's square-module screen, but the sampled
construction buys it with wide surface seams, substantial assembly and a fragile
unqualified joint-motion budget. Shorter guides alone do not establish a cheaper,
repairable machine. Retain the closed-shell principle; reopening this embodiment
requires a materially simpler fabrication/support construction or process evidence.

Evidence: analytical beam/shear models, rigid envelopes and allocated interfaces,
self-reviewed with executable checks in `tools/curated-experiment-checks/E-287.py`.
Not CAD, contact/plate FEA, sourced material qualification or physical measurements.
No print, purchase, supplier contact or owner decision requested; E-281 stays optional.

## Construction and complete load paths

Sixteen 8×8 modules retain E-277's 12.7-mm pitch, 10.3-mm columns and 0–50-mm travel;
column bases Z2…52, tops Z138…188. Each carries sixteen 12×2-mm perforated guide
strips at Z54…56/134…136, sixteen closed keeper halves, eight 12×24-mm hollow
thrust spines at Z−34…−10, and all 64 intact screws. Screw torque/selection,
thread holding, upward capture and readback remain inherited unqualified functions.
The module frame does not replace them or authorize moving loaded neighbors.

New frame: three square machined rings, 2.2-mm radial width ×8-mm height, at
Z46…54,126…134,−42…−34; four .8-mm sheet side panels join the rings to form a closed
shear shell. Guides and spines seat **on** rings, rather than intersecting their
stock. Continuous panel/ring connections and four joined vertical corners are
required. Fabricated sheet and machined rings are a proposed manufacturing route,
not available quotes, weldability evidence or a drawing ready for manufacture.
Assembling rings from bars instead adds twelve corner joints/module.

Gravity: thread→screw driver→perforated spine top→spine ends→lower ring→four fixed
module mounts→board frame. Guidance: body→guide strips→upper/middle rings→corner
and panel shear paths→lower ring/mounts. Upward loads travel through the closed
keeper and its attachments into this same frame; attachments, preload, buckling,
local plate bending, torsion and joint compliance are not constructed or qualified.
A frame of narrow corner posts without shear panels is a separate weak comparator.

The E-277 conservative body projection is12.2415mm. Add .2mm rigid clearance per
outer body face before the ring, then2.2mm ring+.8mm panel per side. Ring opening
101.5415mm, reaction-center span103.7415mm, outer module107.5415mm. With .4mm between
module shells, each internal boundary adds6.3415mm to the uniform grid. The32²
nominal-pitch footprint is425.424mm, but **external shells make the enclosure
431.366mm** before housing/handles, versus406.4mm reference. Nominal top seams at
module boundaries become8.7415mm rather than2.4mm. These are consequential gaps
for miniature feet, walls and image registration; no player acceptance is inferred.
The .2mm reserve is not a complete loaded-collision allowance: guide displacement,
lean amplification, fabrication and joint movement still need a combined bound.

## Stiffness discrimination, not acceptance

Assume E=2GPa for guide/spine polymer; E=70GPa, ν=.33 for shell/rings. At .05N per
cell **at each of both guides**, there are6.4N total lateral load/module. All inputs
are explicit competing scenarios, not rated alloys, measured miniature forces or
calibrated process variation. Each strip's half reaction is .2N at each ring side.

|Modeled contribution|Displacement mm|
|---|---:|
|Perforated guide, extended to actual ring seats|.03406|
|Ring side, eight point reactions|.04806|
|Perfect closed shell, bending plus shear|.00137|
|Conservative series sum|.08350|
|Four3×3×.8-mm corner posts without shear panels|6.4601|

Guide virtual-work integration at32k/64k intervals differs <.2%; independent
strongest/weakest constant-section point-load expressions bracket it. Ring result
is below a same-total-load central point force; a single midpoint-load limiting
case reproduces FL³/(48EI). Shell formula uses two in-plane walls,
I=2tL³/12 and shear area2tL. These checks validate arithmetic/model consistency,
not real welded/fastened shell boundary conditions. The large post deflection is
a warning outside a precision small-deflection interpretation, not a rated failure.

Against E-286's **allocated**, not product-required, .1mm displacement budget,
only .01650mm remains for all connection movement. A correlated .02mm additive
joint allowance gives .10350mm; .05mm gives .13350mm. Without joint movement the
linear load threshold is .05988N/site. Do not accept micrometre-scale residual
budget as fabricated-joint capability or tune a connector to rescue it.

At .338N/site axial diagnostic, short polymer spine/minimum-section bending is
.00479mm, lower ring .02457mm and panel compression .000164mm. This omits frame
self-weight, local thrust-face bending and joint settlement; gravity response is
not a loaded height pass. E-286's thrust friction must still enter drive torque.

## Socket access and supported extraction

Every socket axis lies inside the ring opening, nearest edge6.3207mm away. A
2-mm-AF tool has2.3094mm corner diameter versus2.8mm spine bores: nominal radial
clearance .2453mm, not a fit pass. From below the lower ring to4mm into the driver
requires36mm tip reach. Tip bending, socket engagement, keeper attachment and motor
housing clearance remain unqualified. Four25.4-mm-spaced spindles cover each module
in two parity groups per row; executable address enumeration covers all64 sites.
They cannot batch across widened boundaries. No prior uniform-grid routing/time
or optical calibration is inherited as a new machine prediction.

Clear miniatures and park the writer. A shared guided bench lift approaches from
below the module opening: four pads contact the lower ring's inner lip before
mounts release; installed shelves support its outer lip. Allocating1mm each leaves
only .2mm nominal separation within the2.2-mm ring. This names a continuous path,
not a constructed tolerant transfer. The cradle carries the **closed** module to
a bench nest; support is proved before removing the cradle. Keeper opening still
requires separate restraint of the affected eight-site subrow. Broken targets and
loose fragments must be secured before lift; intact-pair support proves neither.

Four1×8-mm pad allocations carry at least24.50N including diagnostic cells,
modeled shell/rings and spines, giving .766MPa average contact stress. Guides,
keepers, fasteners and handling acceleration are omitted, so this is not a lift
rating. No clamps, motion interlocks or free gang inspection are credited.
Frame envelope permits only .3206° sufficient yaw at .1mm drift and .4mm inter-shell
gap; the lift must be constrained. Lowest frame Z−42 must rise232mm to clear a
neighbor top188 plus2mm, versus224mm in E-286. Temporary pad/carriage thickness may
increase this. Bench opening, replacement, retention proof and actual-height
restoration remain necessary; motor commands are not recovered height evidence.

## Whole-machine manufacture and value

At1024 cells retain2048 bodies/screws,2048 guide apertures,1024 thrust contacts,
256 keeper halves and128 spines. Add64 panels/48 monolithic rings/64 module mounts;
512 guide seats remain required. Minimum allocated frame interfaces/module:
12 ring/panel +32 guide seats +16 spine seats +4 corner seams +4 mounts =68.
At16 modules this is1088 interfaces. One20–60s operation/interface alone gives
6.04–18.13 maker hours, excluding preparation, multiple fasteners, finishing,
alignment, cure, rejects, inspection, lift and bench tooling. Not a net addition
to E-286's overlapping frame allowances, nor demonstrated assembly savings.

Assumed densities2.7/1.24g/cm³ give3.56kg shell/rings plus1.12kg polymer spines per
1024 cells before guides, keepers, columns, screws and whole-machine hardware.
Panel corners are conservatively double-counted; ring machining scrap is excluded.
4096/6400 count-only controls require64/100 modules,4352/6800 interfaces and
24.18–72.53/37.78–113.33 interface hours. The coarse geometry **does not fit**
6.35/5.08mm pitch. No fine-grid manufacturing or reliability pass follows.

E-276's optimistic$798 four-spindle machine already misses the~$500 bought-parts
reference. Gross room to$1000/$1500 is only$12.63/$43.88 per16 modules, before
inspection, lift and other exclusions. Those are **incremental ceilings**, not
quotes or additive BOMs: replaced frame allocations must be explicitly credited.
No low-touch joining, acceptable scrap or supplied price has been established.
A$1000 finished device/$1000–1500 demonstrator remains worth considering on play
value, without purchasing authority; this screen does not earn either price.

Inherited S40/S50 local26.84/31.07s, scene201/223s, neutral271/332s and dense392/452s
at assumed850rpm stay reference calculations versus~30s, not cage predictions.
Real elevated neutral, downward travel and paid initial preparation remain owed;
full6400-cell/40mm stress is separate. E-286's ideal64-cell S50 reset+N30 restore
is1.569min at850rpm before repair, routing and height proof. New seams and service
hardware have not earned faster or enjoyable play. Prioritize a construction that
removes frame joins or avoids narrow inter-module transfers; do not continue local
ring/post/fit optimization on this weak whole-machine proposition.
