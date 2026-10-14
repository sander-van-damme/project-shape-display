---
status: complete
builds-on: [E-276, E-261, E-260, E-263]
---

# Coarse columns: guide lean, manufacturing access and assembly

**Constant-section columns remove cap-yaw amplification, not guide lean.** The retained control has12.7-mm pitch,2.4-mm seams,80-mm guide span,136-mm stock/S50 and65.8% coverage. Its rigid separation bound is.459 mm under explicitly assumed errors. Printing and assembled-thread geometry remain unqualified.

**Evidence:** self-reviewed calculations, finite CAD and actual slicer paths; no physical measurements, fit yield, safe speed or hardware qualification. `tools/curated-experiment-checks/E-277/` retains source; generated files stay in scratch.

## Guidance and whole-machine control

Resident screw/thread/bed carries vertical load; two slabs provide lateral guidance/antirotation. E-261 geometry: slabs2 mm, span b, stroke S; column stock P=S+b+6, maximum top height above upper guide h=S+2, extreme guide-face span B=b+2. Omitted: bow, twist, screw restraint, contact/friction, roof stiffness and wear.

For pitch p, seam s, width w=p−s, nominal guide clearance c, separate total-width error bounds±e and aperture-center bounds±r:

- Largest guide G=w+c+e; smallest column w_min=w−e; minimum aligned clearance c−2e.
- An inscribed cylinder bounds square-prism horizontal width below by w_min, including yaw/tilt. Guide confinement bounds centerline slope by(G−w_min+2r)/B.
- Maximum combined neighbor occupied width **W=G+2r+2h(G−w_min+2r)/B**; separation≥p−W. Positive separation suffices for unequal/lower neighbors; a negative bound alone does not prove collision.
- Exact zero-yaw strip contact solves `B*tan(theta)+w_min/cos(theta)=G+2r` and supplies a finite failure witness.

**Bounds,not distributions.** Common translation cancels;inter-plane skew cancels only at equal heights. `(h2−h1)*skew/B` gives.238 mm at .2-mm skew/42-mm span/50-mm height difference. No yield inference.

At half-square/S50/b40, exact.327° strip tilt gives **>.42-mm overlap** one millimetre below finite neighboring top faces while both guides are satisfied. Nominal grid web is only.16 mm. CAD,not measured jamming.

At S50/c.5/e.1/r.1, aligned clearance=.3 mm; zero-separation seam is3.029 mm at b40 or1.941 at b80. Old.4-mm seams give web−.4 mm. At c.8/e.2/r.2,b80 needs3.429-mm seam; retaining c.24/e.2 instead fails aligned fit(−.16). Grammar b40/60/80 ×seams.4/.8/1.2/1.6/2/2.4/3.2 has six nonnegative cases of21:

| Illustrative half-square seam /span | Separation | Stock | Coverage | Tube-only volume at1024,.8 wall |
|---|---:|---:|---:|---:|
|3.2 /40 mm|.171 mm|96 mm|56.0%|2.737 L|
|2.4 /60 mm|.090 mm|116 mm|65.8%|3.611 L|
|**2.4 /80 mm**|**.459 mm**|**136 mm**|**65.8%**|**4.234 L**|

2/b80 has only.059-mm margin/70.98% coverage. Width cancels from this separation bound: the same seam costs more coverage at fine pitch.2.4-mm seams leave38.7% at6.35 pitch and27.8% at5.08; the latter's2.68-mm exterior cannot contain the3.2-mm screw. Bare4.4-mm stems cover12% at half-square.10.3-mm walls/2.4-mm gaps need player/miniature evaluation; E-276 filled-cell support counts do not transfer.

## Section, load and tooling

Body:10.3-square/.8 walls/136 length; solid threaded block z0..10,square8.7 cavity z10..134,roof z134..136. E-263's3.5/1.7-mm cutter,3-mm single-start lead and explicit.15 radial relief mate nominally with3.2/1.4 male. Not the identified historical print;its.2-mm axis-offset collision remains. S50's64-mm threaded male/10-mm engagement/two2-mm end reserves are reach geometry, not physical stops or strength.

Load:roof→walls→nut block→thread→resident screw/collar→bed/frame; writer supplies torque. Illustrative shellA30.4 mm²/I460.51 mm⁴,F.2 N/e5.15 gives.0181 MPa extreme stress; net-nut average.00207 MPa. Roof-strip span8.7/thickness2/E1000 gives.653 MPa/.00412-mm deflection;F9.81 gives32.0 MPa/.202 mm. These surrogates omit anisotropy, contact, creep, buckling and stripping; no safe-load claim.

A separate2-mm cap sits on30.4-mm² annulus(.00658 MPa average at.2 N). Tube+whole nut+cap uses124-mm open tube and flush butt seats: screw pushes nut into lower annulus, cap loads upper annulus. External fixture/bonds owe alignment and eccentric load. `F/A±Fe(w/2)/I` remains compressive only at e≤2.941 mm;F.2/e5.15 gives−.00494/+.01810 MPa, requiring bond tension or redistributed contact. Source numerically recovers force/moment. Joint offset/squeeze-out consumes guide allowance; no bond/peel rating.

**Closed-core obstruction:** rigid8.7-mm square former cannot exit the roof or≤3.5-mm threaded mouth. Splitting the external mold does not remove this obstruction. Cap-only construction permits upward core withdrawal plus separate downward thread-former unscrewing.1,140 section checks prove access only, not shrink/release. Parting lines affect guides;exterior draft changes guidance.

| Cavity draft across124 mm | Bottom opening /wall | Material at1024 |
|---|---:|---:|
|0°|8.700/.800 mm|5.065–5.140 L|
|.5°|6.536/1.882 mm|7.258–7.333 L|
|1°|4.371/2.964 mm|9.054–9.129 L|

Major/minor cutter cylinders bound thread volume. At±.2 screw offset/.1 cavity-width loss,1° leaves.336 radial room;1.5° fails,zero at1.155°. These are geometry bounds, not molding priors. [Protolabs draft guidance](https://www.protolabs.com/resources/design-tips/improving-part-moldability-with-draft/) does not qualify this long core; its [thread service](https://www.protolabs.com/resources/design-tips/molded-threads-and-how-to-design-them/) uses manual unscrewing/internal diameters≥7.6 mm, not this3.5-mm form (checked2026-10-14). Other processes owe tooling, material, shrinkage, release and quotes. Thin.44 walls reduce tube-only volume to2.417 L but have no stiffness pass.

## Board manufacturing ledger

256-mm bed,10-mm margins/3-mm gaps packs17+7 rotated10.3×136 bodies:24/plate,43 plates,**packing only**,excluding screws/brims/braces. Hypothetical deposition5/10/15 mm³/s gives281/141/94h before travel/support/scrap. At assumed1.24kg/L and$20–30/kg,columns alone~6.3kg/$126–191; old whole-print$60–160 allowance cannot transfer.

| Route,1024 sites | Pieces /joins | Additional process |
|---|---:|---|
|Integral FDM|1024 /0|43 packed plates;1024 removal/inspection duties|
|Tube+nut+cap|3072 /2048|3.860L tube+1.205–1.280L ends;1024 cuts/2048 cut faces;128m feed at1-mm kerf,.031L waste excluding stock ends|
|Open-top mold+cap,.5°|2048 /1024|7.258–7.333L;1024 core/former removals;16-cavity example64 cycles/16 toolsets|

Cap-only mold needs≥124-mm core pull,≥10-mm former withdrawal/3⅓ turns, then lateral opening/ejection. Fill,cure/cool,trim,inspection,reset and gang tooling remain unpaid. **Labor scenarios:**10–30s/operation,5min/plate; stock counts cut/deburr/join,mold counts core/former/eject/trim/join. Exclude tooling,procurement,cure,machine time,scrap,assembly and commissioning.

4096/6400 source diagnostics replicate coarse bodies,not6.35/5.08-mm-compatible parts. At1024,integral handling6.43–12.12h,mold11.38–34.13h,stock8.53–25.60h. Coarse cap joins alone2.84–8.53h;stock joins5.69–17.07h. Adding E-276's base gives integral17.37–35.81h/stock19.47–49.29h, before exclusions. Service replaces column/pair rather than repairing an inaccessible bond. Board retains1024 screws/threads/roofs/blocks,2048 guide apertures,62 row ribs/frame interfaces.32-cell row:32 pairs/64 apertures;8² region:64/128.136-mm extraction,openable layers and re-registration remain unconstructed.

E-276 **conditional** four-output S40/S50:local26.84/31.07s,scene201.24/222.88,neutral271.15/331.62,dense391.62/452.09;eight local18.46/20.81. Actual N20/N30 downward headroom needs paid preparation. Bought$798–1768 remains an allocation,not a revised BOM or speed/hold/readback pass. Keep~30s/~$500/5.08mm/~6400/40mm references and~$1000 finished/$1000–1500 research comparators;no purchase/UX selection.

## Actual three-body slicing

2026-10-14:OpenSCAD2023.09.11,PrusaSlicer2.7.2,numpy/trimesh/manifold3d/matplotlib. BOSL2`136e6367e65d52196a3ea51d03156f8b622c60fc`;unchanged E-263 cutter,$slop0,64facets. Five watertight solids;integral4983.871mm³/5.104L at1024,decomposition error<.01mm³. Three copies/3-mm gaps,no raft/brim/ties.

Profile:`slicing.ini`,.4 nozzle/.2 layer/.45 width,100% infill. **Not an X1C preset or printer program.** Run `python3 tools/curated-experiment-checks/E-277/slicing.py --bosl2 /path/to/BOSL2 --slicer /path/to/prusa-slicer --output "$PAPERCLIP_RUN_SCRATCH_DIR/e277-slicing"`.

`--analyze-only` rechecks scratch outputs. [Prusa support](https://help.prusa3d.com/article/support-material_1698)/[bridge guidance](https://help.prusa3d.com/article/poor-bridging_1802) is not physical qualification.

Actual witnesses:

- Integral ceiling atZ9.8:automatic19×126.489-mm longitudinal traverses/body across124-mm cavity;reject.90° override gives8.25-mm transverse spans,anchors/sag unqualified.
- Upper horizontal thread:overhang perimetersZ6.2,bridgeZ7.0,max4.216mm auto/4.303 transverse;fit unknown.
- Internal support:11,644 sampled segmentsZ1.4..9.2,9.476cm³ per three,trapped behind≤3.5-mm mouth/1.7-mm bore envelope. Bed-only adds none.
- Open-top body:auto124.489-mm bridges;8.7-mm opening helps access,not124-mm-reach cleanup. Separate tube has8.585-mm transverse paths;upright nut has overhang perimeters without bridge infill. Two-end access does not qualify threads/bonds.
- First layerZ.2 is a sliding guide face;bed texture/flare/removal scars lack a measured allowance. Lower cavity skins/walls rest on earlier layers.

Nominal10.3-mm integral/open ends at commandedZ10.2,tube at10.4:half-layer mesh rounding,not measured dimensions or extra guide clearance. No layer/fit sweep.

Three-copy estimates:integral transverse14.70cm³/18.23g/1h49m46s;automatic14.75/18.29/1h49m33s. Internally supported integral24.23/30.04/2h38m24s. Open-cap unsupported/supported totals14.78/25.06cm³ and1h43m35s/2h37m35s;joined totals15.61/26.34cm³ and1h55m20s/2h45m19s. Detailed role/mass accounting remains executable.

Separate slices,not optimized plates. Transverse three-body repetition: **624.5h/5.018L/6.222kg at1024**, not X1C or24-up prediction. Earlier94–281h was deposition-only. Supported integral scales901.1h/8.271L/10.255kg. Extra10/30/60-s cleanup adds2.84/8.53/17.07h;access does not establish those times. Stop on individual fitting/inaccessible cleanup.

## Longitudinal split-shell discriminator

**Changed construction:** cut the same integral body along its screw axis. Print two complementary open-faced halves horizontally, then join them; each includes half the roof and half the nut. No added locating pins, clips, fit changes or screw changes. The nominal reunited solid recovers the integral volume within.01 mm³. Complementary halves retain different phases;three pairs are identical.

Run `split.py` with the same arguments/profile as `slicing.py`,using a separate scratch output; `--analyze-only` rechecks saved meshes/toolpaths. **Actual six-half paths contain no bridges,overhang perimeters or support,including with support enabled.** Three pairs cost15.27cm³/18.94g/1h56m50s versus integral14.70/18.23/1h49m46s. Linear repetition gives664.65h/5.212L/6.465kg at1024,not an optimized plate or X1C forecast. Each nominal5.15-mm half ends at commandedZ5.2:assembled10.4 before bondline is toolpath arithmetic,not measured size. Open access helps;toolpaths do not prove as-deposited threads or bonding.

Open manufacture adds thread registration at every assembly. For relative axial half offsets0/.05/.08/.10/.20/.40 mm, finite male/shell intersections have sampled minimum overlap0/0/.0128/.1705/1.0357/2.7647 mm³ respectively. Search covers109 axial-equivalent screw phases over one3-mm lead (.05-mm grid plus.01 near alignment),654 cases total;not a continuous optimum. One screw phase must fit both halves. These are rigid CAD witnesses,not calibrated printer errors or a universal acceptance tolerance. Common axial displacement of both halves and screw clears. Radial relief.15 mm gives only.0402-mm axial relief in a planar30°-included-flank surrogate; it is not a clearance guarantee for the faceted helix. Bond cure,relative shrinkage,warp,guide-axis error,thread wear and deformation remain unmodeled.

**Straight-pull molding still fails for the unchanged thread.** Isolate a9-mm interior section of the actual positive-half thread former and withdraw toward the open split plane. At.02/.1/.5-mm withdrawal, finite overlap is.0265/.1179/.3275 mm³;initial and2-mm-extracted states clear. The intervening collision matters. A smooth semicircular-bore control clears every sampled withdrawal. Flexible stripping,unscrewing or a changed thread form owe new tooling/process evidence;open cavity alone is not a release solution.

Repetition at1024:2048 half-shells+1024 screws,1024 joining/paired-thread-registration operations and2048 longitudinal seam lines,besides original guides,beds and head. Row:64 halves/32 joins;8² region:128/64.4096/6400 diagnostics need8192/12800 halves and4096/6400 joins;coarse bodies do not fit those pitches.24-halves/plate packing gives86/342/534 plates before screws/support/brims.

Assuming10–30s per half handling and per joined pair plus5min/plate gives15.70–32.77h at1024;with E-276 base,26.64–56.46h before tooling,cleanup,cure,scrap and commissioning. An extra minute of individual thread registration adds17.07h. These are allocations,not demonstrated cycle times. The two124×.8-mm wall seam lands alone take10.16mL adhesive at.05-mm nominal bondline across1024;amount is small,placement is not free. Gap/squeeze-out changes exterior guides and nut geometry. Bond separation/torque/eccentric-load strength and screw release remain unqualified;no revised BOM or hold/RPM pass.

## Verification and boundary

`guidance.py --check`:432 exact-strip cases,finite collision,21-case grammar,fit/correlation/stock anchors. `manufacture.py --check`:1140 core sections,independent volume/energy/packing/seat-equilibrium/convergence/labor checks. `slicing.py`:five solids,three-copy plates,11slice cases,filament conservation and bridge/support witnesses. `split.py`:nominal solid conservation,654 phase cases,common-offset control,rigid former withdrawal versus smooth-bore control,six-half/three-body plates,three slice cases and independent filament accounting. Self-review is not physical validation.

**Park the bonded split-half thread embodiment before seam/fit refinement:** reopen only with a credible batch registration/bond process that avoids individual adjustment,or an unsplit thread interface. Do not add tiny locating features to rescue it. Open access is a useful manufacturing result,not qualification.

**Park internally supported integral FDM and the tested automatic long-bridge setting.** Transverse support-free remains conditional on as-deposited thread,anchoring and sag evidence without individual fitting. Joined/molded controls retain access advantages and real joining/process costs. No owner print,head detail or strength/speed/readback/repair/gameplay pass.
