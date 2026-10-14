---
status: complete
builds-on: [E-276, E-261, E-260, E-263]
---

# Coarse columns: guide lean, manufacturing access and assembly

**Constant-section columns remove cap-yaw amplification, not guide lean.** The retained control has12.7-mm pitch,2.4-mm seams,80-mm guide span,136-mm stock/S50 and65.8% coverage. Its rigid separation bound is.459 mm under explicitly assumed errors. Printing and assembled-thread geometry remain unqualified.

**Evidence:** self-reviewed calculations, finite CAD and actual slicer paths; no physical measurements, fit yield, safe speed or hardware qualification. `tools/curated-experiment-checks/E-277/` retains source; generated files stay in scratch.

## Guide envelope and whole-machine control

Resident thread/screw/bed carries load; two2-mm slabs provide guidance and antirotation. From E-261, stock P=S+b+6,top overhang h=S+2,extreme guide-face span B=b+2. For pitch p,seam s,width w=p−s,nominal clearance c,total-width error±e, and aperture-center error±r:

`G=w+c+e; w_min=w−e; W=G+2r+2h(G−w_min+2r)/B; separation≥p−W`.

A rigid square's inscribed-cylinder width bounds slope. Positive separation suffices for unequal-height neighbors; a negative bound is not collision proof. Exact zero-yaw witness solves `B*tan(theta)+w_min/cos(theta)=G+2r`. At half-square/S50/b40,.327° tilt produces **>.42-mm overlap** one millimetre below finite top faces while satisfying guides. Nominal grid web=.16 mm. CAD,not jamming.

Errors are **bounds,not distributions**. Common translation cancels;skew cancels only at equal heights. `(h2−h1)*skew/B` gives.238 mm at.2 skew/42 span/50 height difference. Omitted:bow,twist,elasticity,contact,friction and wear.

At S50/c.5/e.1/r.1,aligned clearance=.3 mm. Minimum zero-separation seam is3.029 at b40,1.941 at b80. Old.4 seams give−.4-mm webs. At c.8/e.2/r.2,b80 needs3.429 seam; c.24/e.2 instead loses aligned fit(−.16). The finite21-case guide grammar has six nonnegative cases.

| Half-square seam /span, mm | Separation, mm | Stock, mm | Coverage | Tube-only L/1024,.8 wall |
|---|---:|---:|---:|---:|
|3.2 /40|.171|96|56.0%|2.737|
|2.4 /60|.090|116|65.8%|3.611|
|**2.4 /80**|**.459**|**136**|**65.8%**|**4.234**|

2/b80 has only.059 margin/70.98% cover. Width cancels from the separation bound; 2.4 seams leave38.7% at6.35 pitch,27.8% at5.08,where2.68-mm columns cannot contain a3.2-mm screw. Bare4.4 stems cover12% at half-square.10.3 walls/2.4 gaps need player testing; E-276 filled-cell support counts do not transfer.

E-276 conditional four-output S40/S50:local26.84/31.07s,scene201.24/222.88, neutral271.15/331.62,dense391.62/452.09;eight local18.46/20.81. Actual N20/N30 downward headroom needs paid preparation. Bought$798–1768 remains an allocation, not a revised BOM or speed/hold/readback pass. Preserve~30s/~$500/5.08mm/~6400/ 40mm and~$1000 finished/$1000–1500 research comparators;no purchase/UX selection.

## Closed-body manufacture and support

Body:10.3-square/.8 walls/136 length; solid nut z0..10,8.7-square cavity z10..134, roof z134..136. E-263's3.5/1.7 cutter,3-mm single-start lead and explicit.15 radial relief mate nominally with3.2/1.4 male. Not the identified historical print; its.2-mm axis-offset collision remains. S50's64-mm male/10-mm engagement/two2-mm end reserves are reach geometry,not physical stops or strength.

Closed load path:roof→walls→nut→thread→screw/collar→bed. Eccentric butt-seat contact loses compression beyond e2.941 mm; atF.2/e5.15,−.00494/+.01810 MPa needs tension/contact redistribution. Roof-strip surrogate atF9.81 gives32.0 MPa/.202-mm deflection. `manufacture.py` preserves section/load assumptions and independent equilibrium checks; no material,creep,buckling,bond,alignment or strength qualification.

**Closed-core obstruction:**8.7-mm rigid former cannot exit roof or≤3.5 threaded mouth. Split external mold does not help. Open-top+cap permits≥124-mm axial core pull and separate thread-former unscrewing(≥10 mm/3⅓ turns);1,140 section checks prove only access. Cavity draft0/.5/1° changes bottom opening8.700/6.536/4.371, wall.800/1.882/2.964 and total column material5.065–5.140/7.258–7.333/9.054–9.129 L/1024. At±.2 screw offset/.1 cavity-width loss,1° leaves.336 radial room; 1.5° fails,zero at1.155°. Geometry bounds,not mold priors. [Protolabs draft guidance](https://www.protolabs.com/resources/design-tips/improving-part-moldability-with-draft/) does not qualify this core; its [thread service](https://www.protolabs.com/resources/design-tips/molded-threads-and-how-to-design-them/) uses manual unscrewing/internal diameters≥7.6 mm,not3.5 (checked2026-10-14). Thin.44 walls reduce tube-only stock to2.417L without stiffness qualification.

256-mm bed/10-mm margins/3-mm gaps packs24 bodies (17+7 rotated),43 plates; **packing only**,excluding screws/brims/braces. Deposition5/10/15 mm³/s implies 281/141/94h before travel/support/scrap. At1.24kg/L,$20–30/kg,closed columns alone ~6.3kg/$126–191; old whole-print$60–160 allowance does not transfer.

| Route at1024 | Pieces /joins | Process burden |
|---|---:|---|
|Integral FDM|1024 /0|43 packed plates;1024 removals/inspections|
|Tube+nut+cap|3072 /2048|1024 cuts/2048 cut faces;128m feed at1-mm kerf,.031L kerf waste|
|Open-top mold+cap,.5°|2048 /1024|1024 core/former removals;16-cavity example64 cycles/16 toolsets|

`manufacture.py` retains volume/packing/draft/seat/energy/labor details. At10–30s/operation and5min/plate,integral handling6.43–12.12h,stock8.53–25.60, mold11.38–34.13. E-276 base makes integral17.37–35.81h,stock19.47–49.29 before tooling,procurement,cleanup,cure,scrap,assembly/commissioning exclusions. 4096/6400 replication diagnostics are not fine-pitch-compatible bodies. Board still has1024 screws/threads/roofs/blocks,2048 guide apertures,62 row ribs; row32 pairs/64 apertures,8² region64/128. Pair replacement,136-mm extraction, openable layers and re-registration remain unconstructed.

## Actual closed-body slicing

2026-10-14:OpenSCAD2023.09.11,PrusaSlicer2.7.2,numpy/trimesh/manifold3d/matplotlib; BOSL2`136e6367e65d52196a3ea51d03156f8b622c60fc`,E-263 cutter,$slop0,64facets. Integral4983.871mm³/5.104L at1024; five solids,three copies/3-mm gaps,no brim/ties. `slicing.ini` uses.4 nozzle/.2 layer/.45 width,100% infill; **not an X1C preset or printer program**.

Run `python3 tools/curated-experiment-checks/E-277/slicing.py --bosl2 /path/to/BOSL2 --slicer /path/to/prusa-slicer --output "$PAPERCLIP_RUN_SCRATCH_DIR/e277-slicing"` (on one line); `--analyze-only` rechecks scratch. [Prusa support](https://help.prusa3d.com/article/support-material_1698/) and [bridge guidance](https://help.prusa3d.com/article/poor-bridging_1802/) do not qualify our geometry.

Actual witnesses:

- CeilingZ9.8:auto19×126.489-mm longitudinal traverses/body across124-mm cavity; reject.90° override gives8.25-mm transverse spans,anchoring/sag unqualified.
- Upper horizontal thread:overhangZ6.2,bridgeZ7.0,max4.216mm auto/4.303 transverse.
- Internal support:11,644 segmentsZ1.4..9.2,9.476cm³/three,trapped behind≤3.5 mouth/ 1.7 bore. Bed-only adds none. Open-top auto still bridges124.489 mm;8.7 opening does not qualify124-mm-reach cleanup. Separate tube bridges8.585 mm;upright nut has overhangs without bridge infill. Accessible mouths do not prove fit/bonding.
- BedZ.2 is a guide face:flare,texture/removal scars unqualified. Nominal10.3 body ends at commandedZ10.2,tube10.4:mesh/layer rounding,not measured guide allowance.

Three-copy transverse14.70cm³/18.23g/1h49m46s scales **624.5h/5.018L/6.222kg at1024**; internally supported901.1h/8.271L/10.255kg. Separate slices,not optimized24-up or X1C forecasts; earlier94–281h was deposition-only. Other control role/time/mass results remain executable. Extra10/30/60-s cleanup adds2.84/8.53/17.07h,unmeasured. Stop on inaccessible cleanup or individual fitting.

## Longitudinal split-shell discriminator

Cut the unchanged body along its screw axis; print two complementary open-faced halves horizontally and join. Each contains half the roof/nut; no added locating features or screw changes. `split.py` uses the same arguments/profile as slicing; `--analyze-only` rechecks scratch. Reunited volume differs from integral by<.01mm³.

**Actual six-half paths have no bridge,overhang or support,including with support enabled.** Three pairs15.27cm³/18.94g/1h56m50s; at1024,664.65h/5.212L/6.465kg, not optimized-plate/X1C or physical-print proof. Nominal5.15-mm halves end at commandedZ5.2:assembled10.4 before bondline is toolpath arithmetic,not measurement.

For relative axial half offsets0/.05/.08/.10/.20/.40 mm,sampled minimum male/shell overlap is0/0/.0128/.1705/1.0357/2.7647 mm³.654 cases:109 axial-equivalent phases per offset over one3-mm lead (.05-mm grid,.01 near alignment). One screw phase must fit both halves; common shift of both halves and screw clears. Finite CAD, not continuous optimization,printer tolerance or contact proof. Radial relief.15 only gives.0402-mm axial relief in a30° planar-flank surrogate; faceted helical clearance,warp,shrink,bond cure and deformation remain unqualified.

**Rigid straight-pull half-thread mold fails:** actual9-mm interior former shifted .02/.1/.5 mm toward the open plane intersects by.0265/.1179/.3275 mm³; initial and2-mm-extracted states clear. Smooth semicircular bore control clears all draws. Flexible stripping/unscrewing/changed thread needs new tooling evidence.

1024-site burden:2048 halves+1024 screws,1024 paired-thread joins,2048 seam lines; 32-cell row64 halves/32 joins,8² region128/64.4096/6400 diagnostics need8192/12800 halves; coarse bodies do not fit those pitches.24-halves/plate gives86/342/534 plates before screws/support/brims. At10–30s per half handling and pair joining, plus5min/plate,15.70–32.77h at1024; E-276 base makes26.64–56.46h before tooling, cleanup,cure,scrap,commissioning. One extra minute registering each thread adds 17.07h. Two124×.8-mm seam lands take10.16mL adhesive at.05-mm bondline across1024; placement,squeeze-out,guide size,bond strength and service remain unqualified. **Park before seam/fit refinement** unless a batch process avoids individual registration or the thread remains intact; no tiny locating-feature rescue.

## Open channel with one intact nut

**Conditional manufacturing improvement, not a qualified column.** Remove one 8.7×.8-mm cavity wall along124 mm. Print the126-mm U-channel with integral2-mm terrain end open-side up; butt-join the unchanged10-mm intact nut, printed upright. Assembled exterior/length remain10.3-square/136 mm. No thread seam, separate cap, locating teeth or fit change. `open_channel.py`/`.scad` use the same arguments/profile as `slicing.py`; `--analyze-only` checks scratch outputs.

**Actual CAD/slicing,2026-10-14:** watertight channel/nut volumes3118.742/1002.089 mm³; total4.220 L/1024,17.32% below integral before screws. Three identical channels have **no bridge,overhang or support paths**, even with support enabled. Three intact nuts still have333 overhang segments atZ.4..10.0. Support enabled adds1177 bore-interface segments atZ.2..9.6 and three tiny bed-support paths; it does not eliminate thread overhangs. Short open mouths improve access but neither removal through the1.7-mm minor bore nor unsupported fit is established.

| Three-component slices | Filament cm³ /g | Estimated time |
|---|---:|---:|
|Channels, support off/on|9.41 /11.67|1h07m37s|
|Nuts, support off|3.14 /3.89|26m21s|
|Nuts, support on|3.20 /3.96|27m33s|

Unsupported repetition: **534.57h/4.284L/5.311kg at1024**, versus integral624.5h and split664.65h; supported nuts541.39h. Separate three-copy slices,not optimized plates,X1C forecasts or physical prints. At assumed$20–30/kg,$106–159 filament excludes screws,frame,scrap,bonds. Existing bought/time allocations still apply.

Load:terrain end→three walls→nut joint→thread→resident screw/bed. The rigid U retains the square convex hull (361 yaw extrema); guide support directions match, but **stiffness/deformation allowances do not transfer**. Open edges,wall splay, warp,joint-axis error and correlated printing remain unknown. Exposed screws/dark cavities at unequal heights also change player appearance despite65.8% top cover.

U-seatA23.44 mm²,centroid1.4104 mm toward web,Ix416.609/Iy256.475 mm⁴. At assumed centralF.2 N,affine pressure+.00442..+.01575 MPa; open-side edge loading gives −.01060..+.04209 MPa and requires tension for full contact. Independent Gauss integration recovers force/moments to1e−10. No bond/peel/creep/torque/withdrawal rating; downward gravity alone does not establish joint retention.

[Jönköping University thin-wall approximations](https://mechanics.ju.se/SolidMechanics/Torsion.html) give J_open≈Σbt³/3=5.001 versus closed J≈t(w−t)³=685.9 mm⁴,about137× softer at equal material. **Free-warping surrogate**,not FDM/contact simulation.12 scenarios use assumedG200/1000 MPa,torque.1/1/5 Nmm,effective spans4/54 mm. At1 Nmm/54 mm, open twist3.094/.619° versus closed.0226/.00451°; largest open15.47° warns against small-deformation interpretation. Actual torque,guide contact,warping restraint and laminate properties are unknown; neither universal failure nor isolation pass.

Thread-free cavity permits lateral9.5-mm core exit: six sampled withdrawals 0..10 mm have≤.00060 mm³ numerical overlap at nominal touching surfaces. Translation moves the core away from the web while staying between walls/end; no thread undercut or124-mm axial pull. No draft,shrink,release-force,tool-life or mold-cost pass. A molded channel still needs an intact nut and one joint.

At1024:1024 channels+1024 nuts+1024 screws,1024 joins,2048 guide apertures; 32-cell row32 joins,8² region64. Split-half piece/join count is unchanged but paired-thread registration disappears. Tube+nut+cap loses1024 pieces/1024 joins. 4096/6400 replication diagnostics retain4096/6400 joins;these coarse bodies do not fit6.35/5.08 pitches. Conservative24-channel/289-nut packing needs43+4 plates, excluding screws/brims/fixtures. Assumed10–30s per channel handling,nut handling and join,plus5min/plate gives12.45–29.52h; with E-276 base **23.39–53.21h** before tooling,cleanup,cure,scrap,commissioning. Individual minute/join adds17.07h. Bonded replacement still owes136-mm extraction and openable guide layers.

**Retain the manufacturing comparator; stop before joining-detail CAD or an owner print.** Intact-nut manufacture,loaded torsion/guide interaction and batch joining now discriminate viability. No improved speed,hold,readback,miniature appearance or finished-price claim; preserve the whole-machine references above.

## Verification and boundary

Source retains guide,core,volume,packing,phase and extrusion-accounting checks. New source adds361 hull extrema,four joint loads,12 torsion scenarios,six core withdrawals and four slices. Self-review,not physical validation.

**Park bonded split threads,internally supported closed bodies and automatic long bridges.** Transverse unsupported and intact-nut/open-channel routes remain conditional on actual thread manufacture,loaded behavior and batch assembly. No owner print,head selection or strength/speed/readback/repair/gameplay pass.
