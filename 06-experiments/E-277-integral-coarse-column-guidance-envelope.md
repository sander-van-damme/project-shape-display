---
status: complete
builds-on: [E-276, E-261, E-260, E-263]
---

# Integral coarse columns trade cap yaw for guide lean, seams and stock

**Integral columns remove cap-yaw amplification, not guide lean.** Retain only a geometry control:12.7-mm pitch,2.4-mm seams,80-mm guide separation gives.459-mm bounded rigid separation,136-mm stock/S50 and65.8% coverage. Horizontal monolithic printing is a conditional manufacturing route, not a selected surface or qualified screw assembly.

Reproduce `python3 tools/curated-experiment-checks/E-277/guidance.py --check`; omit the flag for tables. Evidence: self-reviewed **analytical bounds/rigid geometry**, not physical qualification. Wide caps on4.4-mm stems stay parked; no added latch or fit tightening.

## Guidance construction and full-travel bound

Compare a straight square hollow column with **equal top/exterior width**, replacing E-276's wide cap on a narrow stem. The bottom thread, resident screw and thrust bed retain height/support; the writer supplies torque. Two square guide slabs react lateral load and antirotation. Integral roof/bottom material and manufacture cannot inherit the thin-tube allowance.

Use E-261's two2-mm guide slabs, center separation b and travel S. Stock P=S+b+6; maximum top-center height above upper guide h=S+2; extreme guide-face separation B=b+2. This rigid/straight model excludes bow, twist, actual screw restraint, contact/friction, roof stiffness and wear.

For pitch p, seam s, column width w=p−s, nominal guide clearance c, separate total-width errors±e and aperture-center errors±r:

- Broad guide G=w+c+e; slender column w_min=w−e; minimum aligned clearance c−2e.
- A square prism contains an inscribed cylinder, so its horizontal width in either guide coordinate is≥w_min, including yaw/tilt.
- Guide confinement bounds centerline slope by(G−w_min+2r)/B. Extrapolation gives combined neighbor occupied width **W=G+2r+2h(G−w_min+2r)/B**, separation≥p−W.

Positive separation suffices in this rigid model at all smaller/unequal heights; negative bound alone is not collision proof. Solve the exact yaw-zero strip equation `B tan(theta)+w_min/cos(theta)=G+2r`, realize opposite guide contacts and check finite ends to obtain a collision witness. A screw may restrain lean only if its lateral reaction/stiffness is established. Positive guide clearance does not prove guide/thread alignment.

Bounds are **not process distributions**. Common translation cancels between neighbors. Common inter-plane skew cancels at equal heights but contributes `(h2−h1)*skew/B` at unequal heights: .2-mm skew across42 mm over50-mm height difference gives .238 mm. Opposing local/module errors can realize the adverse bound. No independent yield is inferred. Enlarged openings must leave an actual separating web.

## Discriminating geometry results

At.4-mm seams and inherited.24-mm nominal total clearance, with zero manufacturing error:

| Travel / guide span, mm | Stock | Separation bound |
|---|---:|---:|
|40 /40|86 mm|−.320 mm|
|50 /40|96 mm|−.434 mm|
|40 /80|126 mm|−.086 mm|
|50 /80|136 mm|−.144 mm|

At12.7-mm pitch/S50/b40, exact strip tilt is only.327°. One millimetre below finite top faces, opposite neighbors overlap **>.42 mm** while satisfying both guides. This is a geometric witness, not measured jamming. Nominal grid web is.16 mm, without a stiffness/printability claim.

Width cancels from the conservative bound: widening the whole column does not improve absolute separation at fixed seam/clearance/errors. Coarser pitch merely loses less coverage to that seam. For S50,c=.5,e=.1,r=.1 mm, aligned clearance is.3 mm; zero-separation seam is3.029 mm at b40 or1.941 at b80. The old.4-mm seam gives **negative web−.4 mm**. With c=.8/e=.2/r=.2, b80 needs3.429-mm seam. Keeping c=.24 with e=.2 instead fails fit(−.16 mm); tighter nominal fit is not free rescue.

A finite grammar over b40/60/80 and seams.4/.8/1.2/1.6/2/2.4/3.2 has six of21 nonnegative cases under c=.5/e=.1/r=.1:

| Half-square seam / b | Separation | Stock | Plane coverage | Tube-only volume,.8 wall |
|---|---:|---:|---:|---:|
|3.2 /40 mm|.171 mm|96 mm|56.0%|2.737 L|
|2.4 /60 mm|.090 mm|116 mm|65.8%|3.611 L|
|2.4 /80 mm|.459 mm|136 mm|65.8%|4.234 L|

Keep2.4/b80 as the clearer **comparison geometry**, not a product winner;2/b80 has only.059-mm margin despite70.98% coverage. Same2.4-mm seam at quarter/fine pitch leaves38.7/27.8% coverage; fine2.68-mm exterior cannot enclose the3.2-mm screw. Keeping4.4-mm stems without caps covers only12% at half-square pitch.

Even equal-height2.4-mm seams affect bases/props/dice/fingers/appearance. A25.4-mm base spanning several columns is not automatically stable. E-276's filled-cell support counts do not transfer; wall width becomes10.3 instead of12.3 mm, and coarse opening/connectivity remains unresolved.

## Manufacture and load: closed core, seated cap and horizontal bridging

Removing the top enables rigid-core extraction but adds1,024 joins; cavity draft increases material. Park the assumed easy closed mold.

Run `python3 tools/curated-experiment-checks/E-277/manufacture.py --check`; omit the flag for the ledger. Evidence: section construction, rigid-core access, structural surrogates and process/labor scenarios. No new CAD mesh, slicing, FEA, material measurement or qualification is claimed. The optional S40 owner print stays retired.

### Explicit section and force path

Retain10.3-mm square exterior, .8-mm walls,136-mm stock: solid threaded block z0..10, square8.7-mm cavity z10..134, roof z134..136. Use E-263's explicit3.5/1.7-mm major/minor cutting envelope,3-mm single-start lead and.15-mm radial relief against the3.2/1.4 male. This identifies a helical-thread source and section, **not new mating proof or the successful historical print**. E-263's .2-mm offset collision remains; guide freedom does not establish thread alignment. S50's64-mm threaded male/10-mm engagement/2-mm end reserves remain nominal travel geometry.

Load flows roof → tube walls → integral nut block → thread flanks → resident screw/collar → bed/frame. Guides react lateral load and antirotation; writer supplies torque without load takeover. Screw buckling, thread contact/stripping, nut-block bending, frame compliance, hold, creep and moving-loss behavior remain unqualified.

Calculated shell area30.4 mm² and second moment460.51 mm⁴ give .0181 MPa extreme normal stress under an illustrative total .2-N upper load at5.15-mm eccentricity, conservatively lumping column weight there. Nut net-section average is .00207 MPa, **not thread stress or capacity**. A simply supported1-mm roof strip across8.7 mm, carrying.2 N centrally, gives.653 MPa/.00412-mm deflection at2-mm thickness/assumed E1000 MPa. E250 gives.0165 mm;1-mm thickness gives2.61 MPa/.0329 mm. At9.81 N:32.0 MPa/.202 mm. This surrogate is not a bound for anisotropic prints or safe-load evidence; buckling/layer/creep/contact failures are absent. No destructive repeat is requested.

An optional separate2-mm cap seats on the tube end annulus: nominal30.4 mm² transmits downward load in compression (.00658 MPa average at.2 N). Attachment still carries handling/lateral/eccentric duties. A bonded butt joint plus alignment fixture is a **process hypothesis**, one joint/inspection per cell, not an added tiny snap. Joined stock adds a bottom joint and thread registration. Cap offset, size and squeeze-out must remain inside the previous exterior-error allowance or the separation bound is lost. Actual contact area and joint strength are unknown.

### Core access and material

A rigid square core forming the8.7-mm cavity cannot withdraw axially through the closed roof or≤3.5-mm thread opening. An external split mold does not remove this obstruction. Collapsible/sacrificial/dissolvable cores require different tooling/removal ledgers; this is not a universal molding prohibition.

With the cap absent, a square core widening toward the top withdraws upward; an independent thread former unscrews downward. Every overlapping core section narrows after upward translation:1,140 executable section checks supplement this monotonicity relation. This proves **rigid access only**, not release against shrinkage, surface finish, tooling or straightness. Constant exterior walls require lateral external mold opening, leaving parting lines on guide surfaces. Exterior axial draft would invalidate the constant-section guidance model.

For a124-mm cavity with8.7-mm top opening:

| Internal draft | Bottom opening | Bottom wall | Column material at1,024 sites |
|---|---:|---:|---:|
|0°|8.700 mm|.800 mm|5.065–5.140 L|
|.5°|6.536 mm|1.882 mm|7.258–7.333 L|
|1°|4.371 mm|2.964 mm|9.054–9.129 L|

Major/minor cylinders bound thread-cut volume; E-263's explicit cutter replaces the earlier3.2..1.4 bore-only5.081–5.148-L allowance. Neither is exact mesh volume. At illustrative±.2-mm screw offset and.1-mm total cavity-width loss,1° leaves .336-mm radial room;1.5° fails, with zero-clearance angle1.155°. Bounds are not molding priors. Batch shrink/warp is unqualified. Thin.44-mm walls use2.417 L tube-only but owe stiffness.

[Protolabs draft guidance](https://www.protolabs.com/resources/design-tips/improving-part-moldability-with-draft/) makes draft dependent on depth/material/ejection; its small-angle advice does not qualify this124-mm core. Its [molded-thread guidance](https://www.protolabs.com/resources/design-tips/molded-threads-and-how-to-design-them/) uses manually unscrewed formers and specifies internal threads≥7.6 mm. That published service is **not an established source for this3.5-mm cutter form**; other suppliers/processes are not excluded. Casting likewise owes core release, shrink, material/friction and handling evidence. No quote or automated unscrewer is assumed. Sources checked2026-10-14.

### Batch effort and whole-machine ledger

Horizontal one-piece FDM lies on a10.3×136-mm face at10.3-mm build height. The long cavity ceiling needs8.7-mm **transverse** bridges, not124-mm longitudinal bridges; thread overhangs/transition require separate inspection. [Prusa's guidance](https://help.prusa3d.com/article/poor-bridging_1802) confirms short unsupported bridging depends on cooling/settings, not that this body/thread works on an X1C. Internal removable support is neither automatically needed nor safe to assume unnecessary. Sag/debris in the thread, bed bias and exterior scars affect function.

A256-mm-plate footprint with10-mm margins/3-mm gaps fits17+7 rotated bodies: **24/plate,43 plates**. This excludes screws/brims/braces and is neither optimal nesting nor slicing. At hypothetical5/10/15 mm³/s sustained deposition,5.065 L alone needs281/141/94 machine hours before travel/support/scrap. Five minutes handling/plate adds3.58 maker hours, excluding removal/inspection. Upright packing revives the owner's stability concern and is not selected. At assumed1.24 kg/L, columns alone weigh6.28–6.37 kg; hypothetical$20–30/kg gives$126–191, already challenging the inherited$60–160 **total** printing allowance. These are scenarios, not quotes/material measurements. Half-degree internal draft adds about43% material.

| Cells | Cap only:1 join/cell,10–30 s | Stock+ends:2 joins/cell,10–30 s |
|---|---:|---:|
|1,024|2.84–8.53 h|5.69–17.07 h|
|4,096 reference|11.38–34.13 h|22.76–68.27 h|
|6,400 reference|17.78–53.33 h|35.56–106.67 h|

Fine rows scale joins only:10.3-mm bodies cannot fit them. Cap work raises inherited four-spindle maker10.94–23.69 h to13.78–32.22 h before process/cleanup/cure/scrap/commissioning. Another minute fitting each pair adds17.1 h. Stock cutting/deburring/joining and automated fixtures remain unpaid.

Board repetition:1,024 columns/screws/threads/roofs/bottom blocks,2,048 guide apertures;32-cell row32/64 and8×8 region64/128 pairs/apertures. Two layers retain62 row ribs/frame joints. Quarter/fine references4096/6400 pairs and8192/12800 apertures remain. No private moving guide, latch or anti-backlash nut is added. Individual service through openable shared layers must accommodate136-mm stock; extraction, bed access and re-registration are unconstructed.

E-276's granted four-output S40/S50 waits remain local26.84/31.07 s, scenes201.24/222.88, neutral271.15/331.62, dense391.62/452.09; eight-output local18.46/20.81. S40/N20 and S50/N30 provide actual downward headroom with paid preparation. The old bought allocation$798–1768 is **not a revised BOM** or drive/readback qualification for heavier columns. Retain~30 s/~$500, possible~$1000 finished value/$1000–1500 research and5.08-mm/6400-cell/40-mm comparators; no purchase/preference is inferred.

## Decision and limits

Stop near-continuous column detail: yaw improvement does not fix the nominal lean/web failures. The2.4-mm-seam/b80/136-mm-stock control owes thread alignment, elasticity, miniature support and process evidence. Horizontal one-piece FDM minimizes joins; open-top molding removes trapped-core geometry but adds material/joints and lacks a sourced small-thread process. Stress averages do not justify reinforcement or establish strength. No new speed/support/readback/repair/play qualification; no tooling, head detail or replacement print.

Next discriminator: actual horizontal body/thread slicing and support-access comparison, including three identical bodies, bridge direction, exterior errors and cleanup. Stop on inaccessible support removal or individual fitting; retain coupled guide/thread alignment as unresolved. This is computational work before any owner handoff.

Checks:432 exact-strip/guide-contact cases, finite collision witness, zero-clearance/fit/monotonicity/pitch/correlation limits, volume arithmetic and21-case geometry grammar;1,140 core-section checks, independent volume decomposition/Simpson integral, failed draft, beam compliance from strain energy, load/thickness scaling, all24 footprint rectangles/gaps and labor scaling. These verify models, not hardware.
