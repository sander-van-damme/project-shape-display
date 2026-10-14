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

Body:10.3-square/.8 walls/136 length; solid nut z0..10,8.7-square cavity z10..134, roof z134..136. E-263's3.5/1.7 cutter,3-mm single-start lead and explicit.15 radial relief mate nominally with3.2/1.4 male. Not the identified historical print; its.2-mm axis-offset collision remains. S50's64-mm male/10-mm engagement/two2-mm end reserves are reach geometry,not physical stops or strength.

Closed load path:roof→walls→nut→thread→screw/collar→bed. Eccentric butt-seat contact requires tension beyond e2.941 mm; atF9.81 the roof-strip surrogate gives32.0 MPa/.202-mm deflection. `manufacture.py` preserves equilibrium,material and load assumptions; no strength/creep/bond qualification.

**Closed-core obstruction:**8.7-mm rigid core cannot exit roof or≤3.5 threaded mouth. Open-top+cap permits≥124-mm pull and≥10-mm/3⅓-turn unscrewing. 1,140 section checks establish access only. Cavity draft0/.5/1° increases material5.065–5.140/7.258–7.333/9.054–9.129 L/1024; offset/error scenario loses screw clearance at1.155°. [Protolabs draft](https://www.protolabs.com/resources/design-tips/improving-part-moldability-with-draft/) and [internal thread service](https://www.protolabs.com/resources/design-tips/molded-threads-and-how-to-design-them/) do not qualify our process; the latter cites≥7.6-mm diameters,not3.5 (checked2026-10-14).

256-mm bed/10-mm margins/3-mm gaps packs24 bodies,43 plates before screws/brims/braces; packing only. Closed bodies alone ~6.3kg/$126–191 at1.24kg/L,$20–30/kg. The former94–281h deposition-only estimate is superseded by actual slice accounting below.

Integral FDM has1024 bodies/no joins; tube+nut+cap3072 pieces/2048 joins; open-top molding+cap2048 pieces/1024 joins. `manufacture.py` retains cut/core/fixture operations.

Including E-276 base, integral assembly17.37–35.81h and stock19.47–49.29h exclude tooling,procurement,cleanup,cure,scrap and commissioning. Board:1024 screws/threads/roofs/blocks,2048 apertures,62 ribs. Pair extraction/openable layers/re-registration remain unconstructed.

## Actual closed-body slicing

2026-10-14:OpenSCAD2023.09.11,PrusaSlicer2.7.2,numpy/trimesh/manifold3d/matplotlib; BOSL2`136e6367e65d52196a3ea51d03156f8b622c60fc`,$slop0,64facets. Comparison profile:.4 nozzle/.2 layer/.45 width,100% infill;not X1C or printer-ready.

Run `python3 tools/curated-experiment-checks/E-277/slicing.py --bosl2 /path/to/BOSL2 --slicer /path/to/prusa-slicer --output "$PAPERCLIP_RUN_SCRATCH_DIR/e277-slicing"`; `--analyze-only` rechecks scratch.

Actual witnesses (`slicing.py` retains segment/coordinate details):

- Auto ceiling bridges126.489 mm across124-mm cavity;reject.90° override spans8.25 mm; anchoring/sag unqualified.
- Upper horizontal thread has overhangs and4.216/4.303-mm bridges.
- Internal support adds9.476cm³/three, trapped behind≤3.5 mouth/1.7 bore. Bed-only adds none. Open-top still bridges124.489 mm; separate tube bridges8.585 mm. Short upright nut still overhangs.
- Bed-contact guide face risks flare/removal scars; nominal10.3-mm height slices10.2/10.4 mm. Toolpath rounding,not process measurement.


Three-copy transverse14.70cm³/18.23g/1h49m46s scales **624.5h/5.018L/6.222kg at1024**; internally supported901.1h/8.271L/10.255kg. Not optimized24-up or X1C forecasts. Extra10/30/60-s cleanup adds2.84/8.53/17.07h;stop on inaccessible cleanup or individual fitting.

## Longitudinal split-shell discriminator

Cut the unchanged body along its screw axis; print two complementary open-faced halves horizontally and join. Each contains half the roof/nut; no added locating features or screw changes. `split.py` uses the same arguments/profile as slicing; `--analyze-only` rechecks scratch. Reunited volume differs from integral by<.01mm³.

**Actual six-half paths have no bridge,overhang or support,including with support enabled.** Three pairs15.27cm³/18.94g/1h56m50s; at1024,664.65h/5.212L/6.465kg, not optimized-plate/X1C or physical-print proof. Nominal5.15-mm halves end at commandedZ5.2:assembled10.4 before bondline is toolpath arithmetic,not measurement.

For relative axial half offsets0/.05/.08/.10/.20/.40 mm,sampled minimum male/shell overlap is0/0/.0128/.1705/1.0357/2.7647 mm³.654 cases:109 axial-equivalent phases per offset over one3-mm lead (.05-mm grid,.01 near alignment). One screw phase must fit both halves; common shift of both halves and screw clears. Finite CAD, not continuous optimization,printer tolerance or contact proof. Radial relief.15 only gives.0402-mm axial relief in a30° planar-flank surrogate; faceted helical clearance,warp,shrink,bond cure and deformation remain unqualified.

**Rigid straight-pull half-thread mold fails:** actual9-mm interior former shifted .02/.1/.5 mm toward the open plane intersects by.0265/.1179/.3275 mm³; initial and2-mm-extracted states clear. Smooth semicircular bore control clears all draws. Flexible stripping/unscrewing/changed thread needs new tooling evidence.

Split burden:2048 halves+1024 screws,1024 paired-thread joins,2048 seams. At24-halves/plate:86/342/534 plates for1024/4096/6400. Assumed handling/joining plus E-276 base26.64–56.46h before exclusions;extra minute/thread adds17.07h. **Park before seam/fit refinement** unless batching removes registration or leaves the thread intact.

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

**Changed pair:** included angle30°→90°;same3-mm single-start lead,.9 depth,
3.2 male/3.5 cutter diameters,10-mm nut,parts and joins. Nuts upright,channels
horizontal;not historical-print reconstruction. `thread_profile.py`/`.scad` use the same pinned dependencies,
profile and `--bosl2/--slicer/--output/--analyze-only` arguments above. Outputs are
scratch, not owner-print payloads.

[Pinned BOSL2](https://github.com/BelfrySCAD/BOSL2/blob/136e6367e65d52196a3ea51d03156f8b622c60fc/threading.scad)
gives half-angles15°/45°, axial crest/root flats1.259/.600 mm and radial flank
advance.746/.200 mm per.2-mm layer. Male core1.4/nut minor bore1.7 mm remain.
[Prusa orientation guidance](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135)
informs45°, not this pair's actual fit/strength.

**Actual three-identical-nut slices,2026-10-14**, unchanged.45-mm extrusion width:

| Angle/layer | Support off: overhang segments /time | Support on: support+interface segments /time |
|---|---|---|
|30°/.2 mm|333 /26m28s|1197 /27m40s|
|30°/.1 mm|0 /49m55s|3864 /52m17s|
|90°/.2 mm|0 /26m11s|0 /26m11s|
|90°/.1 mm|0 /50m01s|0 /50m01s|

No bridge paths;90° also has no overhang paths with support enabled. Re-exported
control gives1194 interface segments versus1177 earlier; compare within-run.
**Missing overhang labels do not qualify unsupported printing:**30°/.1 still
generates3864 support/interface segments.90° removes these paths too; sag,crest
rounding,seam blobs and fit remain unmeasured. Both.2-mm unsupported cases use
3.14 cm³/3.89 g.

**Finite mating:** control1002.089-mm³ nut matches prior volume;90° is1003.949.
Each pair clears53 sampled axial states over one turn and S50 endpoints2..52 mm.
At.2-mm axis offset,every state collides: minimum1.0642/.7464 mm³. Wrong rotation
sign also collides. Finite rigid reach,not continuous contact or yield;no further
clearance sweep warranted.

**Force calculation:** half-angle a;lambda=atan(3/(pi*2.3))=22.548°;
k=sqrt(1+(cos(lambda)*tan(a))²). [DANotes](https://www-mdp.eng.cam.ac.uk/web/library/enginfo/textbooks_dvd_only/DAN/threads/mechanics/mechanics.html)
uses effective friction mu*k. Assumed mean diameter2.3/no collar/preload gives
self-lock threshold mu>tan(lambda)/k: **.4030→.3050**. Small-lead approximation
.4010→.2936 would change the decision at assumed mu=.3;retain helix correction.
AtF.2 N/mu.3,raising torque.1911→.2281 Nmm;axial-section radial/axial normal-force
ratio.268→1.0. Rigid surrogates omit real contact,roughness,preload,collar,guide
drag,compliance and creep. No measured PLA coefficient;owner holding and moving
arrest do not transfer.

**Scale:**1024 nuts/screws/channels/joins remain; finer-grid replication is not dimensional compatibility. Nut CAD adds.00190 L/1024. With prior channel slice,90°/.2 repetition gives **533.62h/4.284L/5.311kg**,excluding screws/frame/scrap/joining;not optimized plates/X1C. Avoiding assumed10/30/60-s cleanup saves2.84/8.53/17.07h at1024; source calculates4096/6400. Conditional savings cannot be deducted from the23.39–53.21-h assembly baseline,which already excluded cleanup.

Same lead preserves turns,not qualified850rpm. Earlier whole-machine timing,cost,neutral and~30s/~$500 comparisons remain conditional. Thread still undercuts a mold;unscrewing tooling is uncosted/unqualified.

**Long-screw route:** [E-279](E-279-long-screw-batch-deposition-and-release.md) retains source,nine64-mm slices,per-screw support checks and1024/4096/6400 whole-pair ledger. Retain upright90° as least-support control;park horizontal raft:83.06h extra/1024 without earned group release. No print/fit tuning;stability,thread damage and joins remain unqualified. Next evidence must change finished-pair manufacture or qualify actual stability,release and joint/guides.

## Verification and boundary

Source checks geometry,force balance,extrusion accounting and reported scenario sets;self-review only. Thread extension:212 finite offset/reach cases,two wrong-sign controls,eight slices and independent torque identities. No physical validation.
