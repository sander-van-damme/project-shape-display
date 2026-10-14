---
status: complete
builds-on: [E-276, E-261, E-260, E-263, E-256]
---

# Coarse columns: guide lean, manufacturing access and assembly

**Constant-section columns remove cap-yaw amplification, not guide lean.** The retained control has12.7-mm pitch,2.4-mm seams,80-mm guide span,136-mm stock/S50 and65.8% coverage. Its rigid separation bound is.459 mm under explicitly assumed errors. Printing and assembled-thread geometry remain unqualified.

**Evidence:** self-reviewed calculations, finite CAD and actual slicer paths; no physical measurements, fit yield, safe speed or hardware qualification. `tools/curated-experiment-checks/E-277/` retains source; generated files stay in scratch.

## Guide envelope and whole-machine control

Resident thread/screw/bed carries load; two2-mm slabs provide guidance and antirotation. From E-261, stock P=S+b+6,top overhang h=S+2,extreme guide-face span B=b+2. For pitch p,seam s,width w=p−s,nominal clearance c,total-width error±e, and aperture-center error±r:

`G=w+c+e; w_min=w−e; W=G+2r+2h(G−w_min+2r)/B; separation≥p−W`.

A rigid square's inscribed-cylinder width bounds slope. Positive separation suffices for unequal-height neighbors; a negative bound is not collision proof. Exact zero-yaw witness solves `B*tan(theta)+w_min/cos(theta)=G+2r`. At half-square/S50/b40,.327° tilt produces **>.42-mm overlap** one millimetre below finite top faces while satisfying guides. Nominal grid web=.16 mm. CAD,not jamming.

Errors are **bounds,not distributions**. Common translation cancels;skew cancels only at equal height. Differential-height skew gives.238 mm at.2/42 span/50 height difference. Bow,twist,elasticity,friction and wear omitted.

At S50/c.5/e.1/r.1, aligned clearance=.3 mm; zero-separation seam minima are3.029/b40 and1.941/b80. Larger assumed errors can erase clearance or separation; the21-case grammar has six nonnegative cases.

| Half-square seam /span, mm | Separation, mm | Stock, mm | Coverage | Tube-only L/1024,.8 wall |
|---|---:|---:|---:|---:|
|3.2 /40|.171|96|56.0%|2.737|
|2.4 /60|.090|116|65.8%|3.611|
|**2.4 /80**|**.459**|**136**|**65.8%**|**4.234**|

2/b80 leaves.059 margin/70.98% coverage. At6.35/5.08 pitch,2.4 seams leave38.7/27.8% coverage;2.68-mm columns cannot contain3.2-mm screws. Coarse walls/gaps need player evaluation;E-276 filled-cell support does not transfer.

E-276 conditional four-output S40/S50:local26.84/31.07s,scene201.24/222.88, neutral271.15/331.62,dense391.62/452.09;eight local18.46/20.81. Actual N20/N30 downward headroom needs paid preparation. Bought$798–1768 remains an allocation, not a revised BOM or speed/hold/readback pass. Preserve~30s/~$500/5.08mm/~6400/ 40mm and~$1000 finished/$1000–1500 research comparators;no purchase/UX selection.

## Closed-body manufacture and support

10.3-square/.8-wall/136-long body:nut z0..10,cavity8.7-square z10..134,
roof z134..136. E-263 cutter3.5/1.7,lead3,radial relief.15 mates3.2/1.4 male;
not identified historical print.64-mm male/10-mm nut/two2-mm reserves permit
S50 geometrically,not safe stops or strength.

Roof→walls→nut→thread→screw/collar→bed. Eccentric butt-seat tension begins
beyond e2.941mm;F9.81 roof-strip surrogate32MPa/.202-mm deflection.
`manufacture.py` retains assumptions/equilibrium,not strength qualification.

Rigid8.7-mm cavity core cannot pass roof or≤3.5 mouth. Open top+cap owes≥124-mm
pull and≥10-mm/3⅓-turn unscrewing.1140 section checks establish access only.
Draft0/.5/1° gives5.065–5.140/7.258–7.333/9.054–9.129L at1024;offset scenario
loses screw clearance at1.155°. [Protolabs internal-thread service](https://www.protolabs.com/resources/design-tips/molded-threads-and-how-to-design-them/)
minimum7.6mm does not qualify3.5mm(checked2026-10-14).

24-body geometric packing/256-mm bed gives43 plates before screws/braces.
Integral body:no joins;tube+nut+cap:2048 joins;open-top+cap:1024 joins.
With E-276 base,integral17.37–35.81h/stock19.47–49.29h exclude tooling,
cleanup,cure,scrap,commissioning.1024 screws/threads/roofs,2048 guide apertures,
62 ribs;service extraction/openable layers remain unconstructed.

## Actual closed-body slicing

2026-10-14:OpenSCAD2023.09.11,PrusaSlicer2.7.2,numpy/trimesh/manifold3d/matplotlib; BOSL2`136e6367e65d52196a3ea51d03156f8b622c60fc`,$slop0,64facets. Comparison profile:.4 nozzle/.2 layer/.45 width,100% infill;not X1C or printer-ready.

Run `python3 tools/curated-experiment-checks/E-277/slicing.py --bosl2 /path/to/BOSL2 --slicer /path/to/prusa-slicer --output "$PAPERCLIP_RUN_SCRATCH_DIR/e277-slicing"`; `--analyze-only` rechecks scratch.

Path witnesses:

- Auto ceiling bridges126.489 mm across124-mm cavity;reject.90° override spans8.25 mm; anchoring/sag unqualified.
- Upper horizontal thread has overhangs and4.216/4.303-mm bridges.
- Internal support adds9.476cm³/three, trapped behind≤3.5 mouth/1.7 bore. Bed-only adds none. Open-top still bridges124.489 mm; separate tube bridges8.585 mm. Short upright nut still overhangs.
- Bed-contact guide face risks flare/removal scars; nominal10.3-mm height slices10.2/10.4 mm. Toolpath rounding,not process measurement.


Three-copy transverse14.70cm³/18.23g/1h49m46s scales **624.5h/5.018L/6.222kg at1024**; internally supported901.1h/8.271L/10.255kg. Not optimized24-up or X1C forecasts. Extra10/30/60-s cleanup adds2.84/8.53/17.07h;stop on inaccessible cleanup or individual fitting.

## Longitudinal split-shell discriminator

`split.py`/`.scad` preserve complementary axial halves,printed open-face up;
reunited volume differs<.01mm³. Six-half slices have no bridge/overhang/support,
even enabled. Three pairs15.27cm³/18.94g/1h56m50s;1024 extrapolation664.65h/
5.212L/6.465kg. Nominal5.15 halves slice5.2:10.4 assembled before bondline,
not a measurement.

654 finite phase cases:relative axial offsets0/.05/.08/.10/.20/.40mm give
minimum overlap0/0/.0128/.1705/1.0357/2.7647mm³. One screw phase must fit both
halves;common shift clears. Radial.15 relief gives only.0402 axial planar-flank
relief at30°. Not continuous contact,printer tolerance or yield.

Rigid half-thread former fails:9-mm interior core shifted.02/.1/.5mm intersects
.0265/.1179/.3275mm³;initial/2-mm states clear. Smooth semicircular control
clears. No straight-pull thread mold pass.

1024 paired-thread joins/2048 seams;24-halves/plate gives86/342/534 plates for
1024/4096/6400. Handling+E-276 base26.64–56.46h before exclusions;one extra
minute/join adds17.07h. **Park seam/fit refinement** unless changed batching
removes registration or keeps the thread intact. Source retains phase grids,
force-free geometry controls and slicing provenance.

## Open channel with one intact nut

**Conditional manufacturing improvement, not a qualified column.** Remove one 8.7×.8-mm cavity wall along124 mm. Print the126-mm U-channel with integral2-mm terrain end open-side up; butt-join the unchanged10-mm intact nut, printed upright. Assembled exterior/length remain10.3-square/136 mm. No thread seam, separate cap, locating teeth or fit change. `open_channel.py`/`.scad` use the same arguments/profile as `slicing.py`; `--analyze-only` checks scratch outputs.

**Actual CAD/slicing,2026-10-14:** watertight channel/nut3118.742/1002.089 mm³;4.220 L/1024,17.32% below integral before screws. Three channels have no bridge/overhang/support paths even with support enabled. Three upright nuts have333 overhang segments; support adds1177 bore-interface and3 bed segments. Short mouths do not establish support removal or unsupported fit.

| Three-component slices | Filament cm³ /g | Estimated time |
|---|---:|---:|
|Channels, support off/on|9.41 /11.67|1h07m37s|
|Nuts, support off|3.14 /3.89|26m21s|
|Nuts, support on|3.20 /3.96|27m33s|

Unsupported repetition: **534.57h/4.284L/5.311kg at1024**;supported nuts541.39h. Not optimized plates,X1C or physical-print proof. At$20–30/kg,$106–159 filament excludes screws,frame,scrap,bonds. Bought/time allocations remain conditional.

Load:terrain end→three walls→joint→nut→thread→screw/bed. U retains square convex hull at361 yaw extrema,not stiffness. Wall splay,warp,joint-axis errors and correlations remain unknown; exposed screws/cavities change appearance at unequal heights.

U-seatA23.44 mm², centroid1.4104 toward web,Ix416.609/Iy256.475 mm⁴. CentralF.2 gives compressive affine pressure; open-edge loading needs tension. Gauss integration checks force/moments;no bond/peel/creep/torque rating. `open_channel.py` retains full cases.

[Jönköping thin-wall approximations](https://mechanics.ju.se/SolidMechanics/Torsion.html):J_open≈5.001 versus closed685.9 mm⁴,about137× softer. Free-warping surrogate,not FDM/contact simulation.12 scenarios varyG200/1000 MPa,torque.1/1/5 Nmm,span4/54 mm. At1 Nmm/54 mm,open twist3.094/.619° versus closed.0226/.00451°;maximum15.47° warns against small-deformation interpretation. Contact/warping restraint/material remain unknown.

Thread-free cavity permits9.5-mm lateral core exit:six nominal draws0..10 mm have≤.00060 mm³ numerical overlap. No thread undercut/124-mm axial pull;no draft,shrink,release-force,tool-life or mold-cost pass. Intact nut and joint remain.

At1024:1024 channels+1024 nuts+1024 screws,1024 joins,2048 guide apertures. Split-half count stays unchanged but paired-thread registration disappears; tube+nut+cap loses1024 pieces/joins. Finer-grid replication is not dimensional compatibility. Assumed24-channel/289-nut packing needs43+4 plates. Handling/joining10–30s and5min/plate gives12.45–29.52h;with E-276 base **23.39–53.21h** before tooling,cleanup,cure,scrap,commissioning. Extra minute/join adds17.07h;136-mm extraction/openable guides still owed.

## Print-oriented intact thread discriminator

`thread_profile.py`/`.scad`:included angle30°→90°,same3-mm lead,.9 depth,
3.2 male/3.5 cutter,10-mm nut;no part/join change. Same pinned dependencies,
profile and`--bosl2/--slicer/--output/--analyze-only`. Not historical-print
reconstruction. [BOSL2](https://github.com/BelfrySCAD/BOSL2/blob/136e6367e65d52196a3ea51d03156f8b622c60fc/threading.scad)
gives flats1.259/.600mm,radial flank advance.746/.200mm per.2 layer;
core1.4/bore1.7 remain.

Actual three-nut slices,2026-10-14:

|Angle/layer|Unsupported overhang segments/time|Supported segments/time|
|---|---|---|
|30°/.2|333/26m28s|1197/27m40s|
|30°/.1|0/49m55s|3864/52m17s|
|90°/.2|0/26m11s|0/26m11s|
|90°/.1|0/50m01s|0/50m01s|

No bridges;90° also has no overhangs with support enabled.30°/.1 demonstrates
why absent overhang labels alone are insufficient. Re-exported control1194
interface segments versus earlier1177;compare within-run. Unsupported.2 cases
3.14cm³/3.89g. Sag,rounding,blobs and fit remain unmeasured.

212 finite mating cases:53 axial states/pair over one turn andS50 endpoints
2..52mm clear coaxially;at.2-mm offset all collide,minimum1.0642/.7464mm³.
Wrong-sign controls collide. Not continuous contact or yield.

Helix-corrected [DANotes](https://www-mdp.eng.cam.ac.uk/web/library/enginfo/textbooks_dvd_only/DAN/threads/mechanics/mechanics.html)
model:lambda22.548°,k=sqrt(1+(cos(lambda)*tan(angle/2))²),self-lock requires
mu>tan(lambda)/k=.4030→.3050. Small-lead approximation.4010→.2936 changes the
assumed-mu.3 decision. AtF.2N/mu.3,torque.1911→.2281Nmm;radial/axial normal
ratio.268→1.0. Source verifies force identities;collar,preload,roughness,guide
drag,compliance/creep and actual friction remain unqualified.

1024 joined channels/nuts/screws remain.90° nut adds.00190L;channel+nut slice
repetition533.62h/4.284L/5.311kg excludes screws/frame/scrap/joining. Avoided
10/30/60-s cleanup would save2.84/8.53/17.07h,but baseline23.39–53.21h already
excludes cleanup. No qualified850rpm or mold release follows.

E-279 retains nine64-mm screw slices and pair ledger. Upright90° is least-support
control;horizontal raft adds83.06h/1024 without earned group release. No fit,
angle or support-label sweep absent changed manufacture or physical evidence.

## Upright one-piece bodies (2026-10-14)

**Integral90° nut+136-mm body removes1024 joins without molding.**
`upright.py`/`.scad` reuse pinned dependencies/profile and
`--bosl2/--slicer/--output`;`--analyze-only` rechecks four slices. Closed tube
and open U print nut-down with integral roof. Explicit`-D angle=90` avoids the
imported module's30° default;independent nut+prism volume checks guard this.

Unsupported bodies have no thread overhang/support paths;both roof bridges
span8.585 mm atZ134.2. U adds six8.3-mm roof-edge overhang segments. Automatic
support generates13749/27683 support+interface segments closed/U,including
below10 mm. Closed support is trapped behind the threaded mouth;open-side
access does not prove clean removal.

|Three bodies|Time|Filament cm³|Repetition h/L at1024|
|---|---:|---:|---:|
|Closed,unsupported|2h04m56s|15.30|710.73/5.222|
|U,unsupported|1h44m14s|12.64|592.97/4.314|
|Closed,supported|2h51m43s|23.99|976.88/8.189|
|U,supported|2h49m37s|25.13|964.93/8.578|

Against joined533.62h,unsupported U/closed add59.35/177.11h;with60.68-h bare
screws,total653.65/771.41h before finished ends/frame/scrap. Three-copy
extrapolations,not X1C/batch forecasts. Assumed1.24kg/L,$20–30/kg gives body
filament$107–161 U/$130–194 closed,not an all-in cost.

Body+screw:2 pieces/cell,64/row,128/8×8,2048/board;1024 fewer pieces/joins.
Threads,guides,journals,thrust/keepers/sockets and shared spindles remain.
Roof→walls→nut→thread→screw→bed support remains;closed walls remove U torsion
weakness. Failed nut scraps body;openable guides/136-mm service extraction,
warp,layer strength,holding and actual motion remain unqualified. Earlier whole-machine comparisons remain unchanged.

17×17 packing with3-mm gaps/10-mm margins gives289 bodies/256-mm bed,not a
stable/sliced batch;brims/braces excluded. Assume removal+gauge10–30s each,
5min/plate and E-276 base10.94–23.69h:four plates give16.96–41.09 maker h versus
joined23.39–53.21h under its different operation list. Cleanup,tooling,rejects,
fitting and commissioning remain extra;60s/body adds17.07h. Body-only handling
at4096/6400:24.01–69.52/37.47–108.58h. Replication only:10.3-mm bodies do not
fit6.35/5.08 pitch. Correlated plate failure is unmeasured.

Equal-E ideal cantilever`I/L³` versus64-mm solid3.2 shank is9.32× closed/5.19× U
weak-axis. No adhesion,nozzle-load,anisotropy,resonance or growing-print qualification.

**Retain conditional assembly-saving controls,not manufacturing winners.**
No cap/brace/fit sweep or new owner print. Reopen through actual bridge/tall-body
process evidence or a whole-pair production advantage. E-281 remains optional.
Checks:one-shell meshes,volume sums,three-copy paths,extrusion accounting and
four-slice replay;self-review,no physical qualification.

## Verification and boundary

Source checks geometry,force balance,extrusion accounting and reported scenario sets;self-review only. Thread extension:212 finite offset/reach cases,two wrong-sign controls,eight slices and independent torque identities. No physical validation.
