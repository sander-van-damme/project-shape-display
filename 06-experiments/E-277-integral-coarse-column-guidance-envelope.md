---
status: complete
builds-on: [E-276, E-261, E-260, E-263]
---

# Integral coarse columns trade cap yaw for guide lean, seams and stock

**Integral columns remove cap-yaw amplification, not guide lean.** Control:12.7-mm pitch,2.4-mm seams,80-mm guide span,.459-mm rigid separation,136-mm stock/S50,65.8% coverage. Actual slicing rejects automatic longitudinal bridging and trapped internal supports. Explicit transverse, support-free FDM remains unqualified.

Run `python3 tools/curated-experiment-checks/E-277/guidance.py --check`. Self-reviewed rigid geometry;wide caps/4.4-mm stems stay parked.

## Guidance construction and full-travel bound

Equal top/exterior square column replaces wide cap/narrow stem. Resident screw/thread/bed retain load;two slabs react lateral load/antirotation. Roof/bottom material exceeds tube-only allowance.

E-261:two2-mm slabs,span b,travel S. Stock P=S+b+6;top above upper guide h=S+2;extreme face span B=b+2. Rigid model omits bow,twist,screw restraint,contact/friction,roof stiffness,wear.

For pitch p, seam s, column width w=p−s, nominal guide clearance c, separate total-width errors±e and aperture-center errors±r:

- Broad guide G=w+c+e; slender column w_min=w−e; minimum aligned clearance c−2e.
- A square prism contains an inscribed cylinder, so its horizontal width in either guide coordinate is≥w_min, including yaw/tilt.
- Guide confinement bounds centerline slope by(G−w_min+2r)/B. Extrapolation gives combined neighbor occupied width **W=G+2r+2h(G−w_min+2r)/B**, separation≥p−W.

Positive separation suffices for smaller/unequal heights;negative bound is not collision proof. Solve `B tan(theta)+w_min/cos(theta)=G+2r` at zero yaw/opposite contacts for a finite witness. Screw restraint/alignment unestablished.

**Bounds,not distributions.** Common translation cancels;inter-plane skew cancels only at equal heights. Unequal heights add `(h2−h1)*skew/B`:.2-mm skew/42-mm span/50-mm height difference gives.238 mm. Opposing local errors can realize adverse bound;no yield inference. Apertures need separating webs.

## Discriminating geometry results

At.4-mm seams and inherited.24-mm nominal total clearance, with zero manufacturing error:

| Travel / guide span, mm | Stock | Separation bound |
|---|---:|---:|
|40 /40|86 mm|−.320 mm|
|50 /40|96 mm|−.434 mm|
|40 /80|126 mm|−.086 mm|
|50 /80|136 mm|−.144 mm|

At12.7-mm pitch/S50/b40, exact strip tilt is only.327°. One millimetre below finite top faces, opposite neighbors overlap **>.42 mm** while satisfying both guides. This is a geometric witness, not measured jamming. Nominal grid web is.16 mm, without a stiffness/printability claim.

Width cancels from the separation bound; coarse pitch loses less coverage to the same seam. At S50/c.5/e.1/r.1 mm, aligned clearance=.3 mm; zero-separation seam=3.029 mm at b40 or1.941 at b80. The old.4-mm seam gives **web−.4 mm**. At c.8/e.2/r.2, b80 needs3.429-mm seam. Keeping c.24/e.2 fails fit(−.16 mm).

Grammar:b40/60/80,seams.4/.8/1.2/1.6/2/2.4/3.2; six of21 nonnegative at c=.5/e=.1/r=.1:

| Half-square seam / b | Separation | Stock | Plane coverage | Tube-only volume,.8 wall |
|---|---:|---:|---:|---:|
|3.2 /40 mm|.171 mm|96 mm|56.0%|2.737 L|
|2.4 /60 mm|.090 mm|116 mm|65.8%|3.611 L|
|2.4 /80 mm|.459 mm|136 mm|65.8%|4.234 L|

**Control:**2.4/b80;2/b80 has only.059-mm margin/70.98% coverage. Same seam at quarter/fine leaves38.7/27.8% coverage;fine2.68-mm exterior cannot enclose3.2-mm screw. Bare4.4-mm stems cover12% at half-square.

The2.4-mm seams need miniature/appearance evaluation; E-276's filled-cell support counts do not transfer. Walls narrow12.3→10.3 mm; connectivity remains unresolved.

## Manufacture and load: closed core, seated cap and horizontal bridging

Run `python3 tools/curated-experiment-checks/E-277/manufacture.py --check` (without flag: ledger). Sections/tooling/scenarios/CAD/slicing only;no FEA or physical qualification. S40 print retired.

### Section, load and tooling access

Section:10.3-mm square exterior/.8-mm walls/136-mm stock; solid threaded block z0..10,square8.7-mm cavity z10..134,roof z134..136. E-263 supplies the3.5/1.7-mm cutter at3-mm single-start lead/.15-mm radial relief against3.2/1.4 male. It is not the identified successful historical print. Its.2-mm offset collision remains; guide freedom does not prove thread alignment. S50 retains64-mm threaded male/10-mm engagement/2-mm end reserves as nominal travel geometry. Load:roof→walls→nut block→thread→resident screw/collar→bed/frame. Guides react lateral load/antirotation; writer supplies torque,not support. Buckling,thread stripping,frame compliance,hold,creep and moving-loss remain unqualified. **Structural scenarios,not safe loads:** shellA30.4 mm²/I460.51 mm⁴;F.2 N/e5.15 gives.0181 MPa extreme stress,net-nut average.00207 MPa. Roof-strip span8.7/thickness2/E1000 gives.653 MPa/.00412-mm deflection;F9.81 gives32.0 MPa/.202 mm. Source retains thickness/modulus sensitivity. Anisotropic/layer/contact/creep failure omitted.

Separate2-mm cap seats on30.4-mm² annulus(.00658 MPa average at.2 N). Joined stock uses124-mm open tube,nut and cap with two flush butt seats,no hidden plugs. Screw pushes nut into lower annulus;cap loads upper annulus;external fixture aligns bonds. Full-contact elastic traction `F/A ± F e(w/2)/I` is compressive only for e≤2.941 mm. AtF.2/e5.15,−.00494/+.01810 MPa requires bond tension or contact opening/redistribution,not proof of failure. Numerical traction integration recovers force/moment. Joint offset/squeeze-out consumes the guide exterior-error allowance;bond/thread/peel strength unknown. Tube/adhesive unsourced;clean before joining.

**Closed-core obstruction:** rigid8.7-mm square core cannot leave through roof or≤3.5-mm threaded mouth; external split mold alone cannot fix it. Collapsible/sacrificial/dissolvable cores owe new tooling/removal ledgers. Cap-only allows upward withdrawal of a core widening toward the open top; independent thread former unscrews downward.1,140 section checks prove rigid access only,not shrink/release/straightness. Constant exterior requires lateral mold opening;parting lines affect guides. Exterior axial draft would change the guidance model.

| Internal draft /124-mm cavity | Bottom opening /wall | Material at1024 |
|---|---:|---:|
|0°|8.700/.800 mm|5.065–5.140 L|
|.5°|6.536/1.882 mm|7.258–7.333 L|
|1°|4.371/2.964 mm|9.054–9.129 L|

Major/minor cutter cylinders bound thread removal,replacing earlier3.2..1.4 bore allowance5.081–5.148 L. At±.2-mm screw offset/.1-mm cavity-width loss,1° leaves.336-mm radial room;1.5° fails,zero room at1.155°. These are bounds,not molding priors. Thin.44-mm walls use2.417 L tube-only but owe stiffness. [Protolabs draft guidance](https://www.protolabs.com/resources/design-tips/improving-part-moldability-with-draft/) does not qualify124-mm core release. Its [thread service](https://www.protolabs.com/resources/design-tips/molded-threads-and-how-to-design-them/) uses manual unscrewing/internal threads≥7.6 mm,not this3.5-mm form (checked2026-10-14). Other casting/suppliers owe material,shrink,release,handling and quotes.

### Batch/system ledger

Horizontal face10.3×136 mm,height10.3. The cavity permits an8.7-mm transverse bridge geometrically; actual slicing below challenges automatic direction. A256-mm plate/10-mm margins/3-mm gaps fits17+7 rotated bodies:24/plate,43 plates,excluding screws/brims/braces;packing only. Hypothetical5/10/15 mm³/s deposition gives281/141/94 h before travel/support/scrap. At1.24 kg/L,columns6.28–6.37 kg and assumed$20–30/kg give$126–191,already exceeding parts of the old$60–160 total-print allowance. No measured yield;upright stability owner-disfavored.

| Route,1024 sites | Pieces /joins | Material/operations |
|---|---:|---|
|Integral FDM|1024/0|5.065–5.140 L;43 packed plates;1024 removal/inspection duties|
|Tube+nut+cap|3072/2048|Tube3.860 L+ends1.205–1.280 L;1024 cuts/2048 cut faces;128-m feed at1-mm kerf(.031 L waste),excluding stock ends|
|Open-top mold+cap,.5°|2048/1024|7.258–7.333 L;1024 core/former removals;16-cavity example64 cycles/16 toolsets|

Core pull≥124 mm up;former≥10 mm down/3⅓ turns,plus handling/reset. Retract core before part motion;open mold laterally. Fill,cool/cure,eject,trim,inspect and caps unpaid. Gang tooling owes torque/reset/cost.

**Labor assumptions:**10–30 s/operation,5 min/plate;stock cut/deburr/join;mold core/former/eject/trim/join. Exclude tooling,procurement,machine/cure time,ends/caps,scrap,assembly/commissioning.

| Sites | Integral h /plates | Stock h /joins | Mold h /joins /16-cavity cycles |
|---|---:|---:|---:|
|1024|6.43–12.12/43|8.53–25.60/2048|11.38–34.13/1024/64|
|4096 reference|25.63–48.38/171|34.13–102.40/8192|45.51–136.53/4096/256|
|6400 reference|40.03–75.58/267|53.33–160.00/12800|71.11–213.33/6400/400|

Reference rows replicate the coarse body,not a body fitting6.35/5.08-mm pitch;source retains their material/feed scaling. Coarse joins alone2.84–8.53 h cap-only,5.69–17.07 h stock. E-276 base labor+stock becomes19.47–49.29 h;integral17.37–35.81 h,still excluding above duties. No automation credit.

Service replaces pair/column,not an in-situ bond;cap inspection ends at bonding. Repetition:1024 columns/screws/threads/roofs/blocks,2048 apertures,62 row ribs/frame joints.32-cell row32/64 pairs/apertures;8×8 region64/128. Quarter/fine4096/6400 pairs,8192/12800 apertures. No private latch/guide/anti-backlash addition.136-mm extraction/openable-layer access/re-registration remain unconstructed.

E-276 four-output S40/S50 grants:local26.84/31.07 s,scenes201.24/222.88,neutral271.15/331.62,dense391.62/452.09;eight-output local18.46/20.81. S40/N20,S50/N30 supply actual downward headroom and paid preparation. Bought$798–1768 is **not a revised BOM** or heavier-column drive/readback proof. Retain~30 s/~$500,possible~$1000 finished/$1000–1500 research,5.08-mm/6400-cell/40-mm references;no purchase/preference inferred.

## Three-body slicing

**CAD/toolpaths,2026-10-14,self-reviewed,no print.** `slicing.scad` reuses E-263 cutter unchanged,$slop=0,64 facets,BOSL2 `136e6367e65d52196a3ea51d03156f8b622c60fc`. Five connected/watertight solids:integral/open/tube/nut/cap. Integral4983.871 mm³/5.104 L at1024;decompositions agree within.01 mm³ mesh roundoff,not process tolerance. Three copies,3-mm gaps,no raft/brim/ties;no yield.

Reproduce:OpenSCAD2023.09.11,PrusaSlicer2.7.2 (Ubuntu arm64 2.7.2+dfsg-1build2),Python/numpy/trimesh/manifold3d/matplotlib:

```sh
python3 tools/curated-experiment-checks/E-277/slicing.py \
  --bosl2 /path/to/BOSL2 --slicer /path/to/prusa-slicer \
  --output "$PAPERCLIP_RUN_SCRATCH_DIR/e277-slicing"
```

Profile:.4 nozzle/.2 layers/.45 width,two classic perimeters,100% fill,density1.24;bridge20/external30/perimeter40 mm/s,acceleration1000 mm/s²,no compensation. **Comparison only, not an X1C preset or usable machine program.** Settings,meshes,G-code,logs,summary,plot stay in scratch; `--analyze-only` rechecks them.

| Surface/route | Actual extrusion paths | Consequence |
|---|---|---|
|10.3×136-mm bed face|First layerZ.2,no external support|Bed texture/flare/removal scars affect a sliding guide face; no measured error or sanding allowance.|
|Lower cavity skin/sidewalls|Built from bed/earlier layers|Supported nominally; warp,adhesion,strength unknown.|
|Integral ceiling,automatic|AtZ9.8,19 longitudinal126.489-mm traverses/body across124-mm cavity|**Reject automatic setting:** earlier assumed short bridge is absent.|
|Same,90° override|8.25-mm transverse spans across nominal8.7-mm cavity,short longitudinal connectors|Support-free;anchors/sag unqualified. Override changes thread paths too.|
|Horizontal upper thread|Overhang perimetersZ6.2,bridgesZ7.0;selected max4.216 mm auto/4.303 transverse|Upper thread unsupported;lower bore builds from earlier material. Fit unknown.|
|Integral,support everywhere|11,644 sampled cavity support segments,Z1.4..9.2;9.476 cm³ total support/interface per three|Roof seals support behind≤3.5-mm mouth/1.7-mm minimum bore envelope. **Park: no demonstrated removal/inspection route.**|
|Integral,bed-only support|No internal support;unchanged long bridges|Does not solve ceiling/thread.|
|Open-top body + cap|Automatic124.489-mm bridges;generated internal supports|8.7-mm open end improves access,not124-mm-reach cleanup or horizontal bridging.|
|Separate tube/upright nut/cap|Tube auto transverse8.585-mm segments;nut overhang perimeters,no bridge-infill;cap bed-supported|Two-end access and orientation improve; thread/bond quality remain unknown.|

Actual roles follow [Prusa support semantics](https://help.prusa3d.com/article/support-material_1698),not physical necessity. [Bridge guidance](https://help.prusa3d.com/article/poor-bridging_1802) is no qualification. Dissolving/breaking/retaining support owes removal,debris and travel evidence.

Nominal10.3-mm integral/open bodies end at commandedZ10.2,the tube at10.4: mesh rounding straddles a half-layer boundary. Paths are not measurements or extra guide margin. No layer/fit sweep.

**Slicer estimates per three copies**, including support where enabled. Cap/joined totals sum separately sliced components; no optimized batch schedule:

| Route | cm³ / grams | Machine time |
|---|---:|---:|
|Integral automatic / transverse|14.75/18.29;14.70/18.23|1h49m33s;1h49m46s|
|Integral internally supported,parked|24.23/30.04|2h38m24s|
|Cap-only unsupported / supported + caps|14.78/18.32;25.06/31.07|1h43m35s;2h37m35s|
|Joined unsupported / supported tube + ends|15.61/19.34;26.34/32.66|1h55m20s;2h45m19s|

Proportional repetition of transverse three-body batches gives **624.5 h/5.018 L/6.222 kg at1024**, not X1C performance or a24-up schedule. The earlier94–281 h was deposition-only; travel/short paths matter. Setup,scrap,screws,assembly remain unpaid. At assumed$20–30/kg,column material alone$124–187. Rejected supported integral scales901.1 h/8.271 L/10.255 kg.

Maker time is unmeasured. Retain43-plate **packing-only** and6.43–12.12-h handling scenarios,not a proven slice schedule. Cap-only adds1024 joins/2.84–8.53 h;joined2048/5.69–17.07 h before other work. Extra10/30/60-s cleanup per column adds2.84/8.53/17.07 h; access does not establish those times. Stop on individual fitting/inaccessible cleanup. E-276 waits,speed,retention,BOM and gameplay remain granted comparisons.

## Decision and limits

**Complete: park internally supported integral FDM;reject tested automatic longitudinal bridges.** Transverse support-free remains conditional on as-deposited thread,anchoring and sag evidence without individual fitting. Joined/molded controls retain access advantages and join/process costs. No owner print,head detail or strength/speed/readback/repair/gameplay pass. Reopen supported integral only with credible removal access/process or changed construction.

Checks:432 strip cases/finite collision/21-case grammar;1140 core sections;independent volume,energy,packing,seat-equilibrium/convergence and labor checks;five connected solids/three-copy plates/11 slice cases,filament accounting and bridge/support witnesses. Models,not hardware proof.
