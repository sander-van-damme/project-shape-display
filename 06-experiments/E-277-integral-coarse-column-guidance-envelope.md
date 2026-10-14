---
status: complete
builds-on: [E-276, E-261, E-260, E-263]
---

# Integral coarse columns trade cap yaw for guide lean, seams and stock

**Integral columns remove cap-yaw amplification, not guide lean.** Control:12.7-mm pitch,2.4-mm seams,80-mm guide span,.459-mm rigid separation,136-mm stock/S50,65.8% coverage. Horizontal FDM is conditional, not qualified.

Run `python3 tools/curated-experiment-checks/E-277/guidance.py --check` (without flag: tables). Self-reviewed **analytical/rigid geometry**; wide caps on4.4-mm stems stay parked.

## Guidance construction and full-travel bound

Replace E-276's wide cap/narrow stem with a square hollow column of **equal top/exterior width**. Resident screw/thread/bed retain load; two guide slabs react lateral load and antirotation. Roof/bottom material cannot inherit the thin-tube allowance.

Use E-261's two2-mm guide slabs, center separation b and travel S. Stock P=S+b+6; maximum top-center height above upper guide h=S+2; extreme guide-face separation B=b+2. This rigid/straight model excludes bow, twist, actual screw restraint, contact/friction, roof stiffness and wear.

For pitch p, seam s, column width w=p−s, nominal guide clearance c, separate total-width errors±e and aperture-center errors±r:

- Broad guide G=w+c+e; slender column w_min=w−e; minimum aligned clearance c−2e.
- A square prism contains an inscribed cylinder, so its horizontal width in either guide coordinate is≥w_min, including yaw/tilt.
- Guide confinement bounds centerline slope by(G−w_min+2r)/B. Extrapolation gives combined neighbor occupied width **W=G+2r+2h(G−w_min+2r)/B**, separation≥p−W.

Positive separation suffices for smaller/unequal heights; a negative bound is not collision proof. Solve `B tan(theta)+w_min/cos(theta)=G+2r` at zero yaw with opposite guide contacts and finite ends for a witness. Screw restraint and guide/thread alignment are not established.

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

Width cancels from the separation bound; coarse pitch loses less coverage to the same seam. At S50/c.5/e.1/r.1 mm, aligned clearance=.3 mm; zero-separation seam=3.029 mm at b40 or1.941 at b80. The old.4-mm seam gives **web−.4 mm**. At c.8/e.2/r.2, b80 needs3.429-mm seam. Keeping c.24/e.2 fails fit(−.16 mm).

A finite grammar over b40/60/80 and seams.4/.8/1.2/1.6/2/2.4/3.2 has six of21 nonnegative cases under c=.5/e=.1/r=.1:

| Half-square seam / b | Separation | Stock | Plane coverage | Tube-only volume,.8 wall |
|---|---:|---:|---:|---:|
|3.2 /40 mm|.171 mm|96 mm|56.0%|2.737 L|
|2.4 /60 mm|.090 mm|116 mm|65.8%|3.611 L|
|2.4 /80 mm|.459 mm|136 mm|65.8%|4.234 L|

Keep2.4/b80 as the clearer **comparison geometry**, not a product winner;2/b80 has only.059-mm margin despite70.98% coverage. Same2.4-mm seam at quarter/fine pitch leaves38.7/27.8% coverage; fine2.68-mm exterior cannot enclose the3.2-mm screw. Keeping4.4-mm stems without caps covers only12% at half-square pitch.

The2.4-mm seams need miniature/appearance evaluation; E-276's filled-cell support counts do not transfer. Walls narrow12.3→10.3 mm; connectivity remains unresolved.

## Manufacture and load: closed core, seated cap and horizontal bridging

Run `python3 tools/curated-experiment-checks/E-277/manufacture.py --check` (without flag: ledger). Evidence: sections, rigid tooling access, structural/process scenarios; no mesh, slicing, FEA or physical qualification. S40 print stays retired.

### Explicit section and force path

Retain10.3-mm square exterior, .8-mm walls,136-mm stock: solid threaded block z0..10, square8.7-mm cavity z10..134, roof z134..136. Use E-263's explicit3.5/1.7-mm major/minor cutting envelope,3-mm single-start lead and.15-mm radial relief against the3.2/1.4 male. This identifies a helical-thread source and section, **not new mating proof or the successful historical print**. E-263's .2-mm offset collision remains; guide freedom does not establish thread alignment. S50's64-mm threaded male/10-mm engagement/2-mm end reserves remain nominal travel geometry.

Load flows roof → tube walls → integral nut block → thread flanks → resident screw/collar → bed/frame. Guides react lateral load and antirotation; writer supplies torque without load takeover. Screw buckling, thread contact/stripping, nut-block bending, frame compliance, hold, creep and moving-loss behavior remain unqualified.

Calculated shell area30.4 mm² and second moment460.51 mm⁴ give .0181 MPa extreme normal stress under an illustrative total .2-N upper load at5.15-mm eccentricity, conservatively lumping column weight there. Nut net-section average is .00207 MPa, **not thread stress or capacity**. A simply supported1-mm roof strip across8.7 mm, carrying.2 N centrally, gives.653 MPa/.00412-mm deflection at2-mm thickness/assumed E1000 MPa. E250 gives.0165 mm;1-mm thickness gives2.61 MPa/.0329 mm. At9.81 N:32.0 MPa/.202 mm. This surrogate is not a bound for anisotropic prints or safe-load evidence; buckling/layer/creep/contact failures are absent. No destructive repeat is requested.

An optional2-mm cap seats on the30.4-mm² tube annulus (.00658 MPa average at.2 N). Its butt bond carries handling/lateral/eccentric duties; one joint/inspection per cell.

**Joined stock:**10.3/8.7-mm square tube z10..134, full-width nut z0..10 and cap z134..136. The screw pushes the nut against the lower tube annulus; the cap presses on the upper annulus. Both flush butt seats have30.4-mm² area, with no hidden plug/fastener. An external alignment fixture holds both bonds. This is finite section geometry, not a sourced stock size or qualified adhesive. The separate10-mm nut has through tooling/cleaning access; clean the124-mm open tube before joining. A monolithic closed body lacks machining access to its wide cavity through the3.5-mm mouth.

For either seat, full-contact elastic traction `p=F/A ± F e (w/2)/I` stays compressive only for `e≤I/(A w/2)=2.941 mm`. At.2 N/e5.15 mm, extrema **−.00494/+.01810 MPa** require bond tension or contact redistribution/opening. This is not bond failure: roof/guide reactions may redistribute moment. Four-rectangle traction integration independently recovers force/moment. Neither small average stress nor this conditional model qualifies thread/peel/creep strength. Joint offset/squeeze-out must stay within the guidance exterior-error allowance.

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

[Protolabs draft guidance](https://www.protolabs.com/resources/design-tips/improving-part-moldability-with-draft/) does not qualify this124-mm core. Its [thread service](https://www.protolabs.com/resources/design-tips/molded-threads-and-how-to-design-them/) uses manually unscrewed formers and internal threads≥7.6 mm: **not an established source for this3.5-mm form**. Other suppliers/casting remain possible, owing release, shrink, material/friction, handling and quotes. Checked2026-10-14.

### Batch effort and whole-machine ledger

Horizontal FDM lies on a10.3×136-mm face,10.3-mm high. The cavity ceiling needs8.7-mm **transverse** bridges, not124-mm longitudinal ones. [Prusa's bridging guidance](https://help.prusa3d.com/article/poor-bridging_1802) does not qualify this X1C body/thread. Thread overhangs, sag/debris, bed bias, scars and support removal remain untested.

A256-mm plate,10-mm margins/3-mm gaps fits17+7 rotated bodies: **24/plate,43 plates**, excluding screws/brims/braces. This is not optimal nesting or slicing. Hypothetical5/10/15 mm³/s deposition needs281/141/94 machine hours before travel/support/scrap. At assumed1.24 kg/L, columns weigh6.28–6.37 kg; hypothetical$20–30/kg gives$126–191 versus inherited$60–160 **total** printing allowance. No quote/material measurement; .5° draft adds43% volume. Upright printing remains disfavored by the owner's stability observation.

| Route at1,024 sites | Pieces / joins | Material and paid operations |
|---|---:|---|
| Integral horizontal FDM |1,024 /0|5.065–5.140 L;43 plates;1,024 removal/inspection sites |
| Square tube + nut + cap |3,072 /2,048|3.860 L tube +1.205–1.280 L ends;1,024 cuts/2,048 cut faces;128 m feed at1-mm kerf (.031 L waste), before stock-end loss |
| Open-top mold + cap, .5° draft |2,048 /1,024|7.258–7.333 L;1,024 core pulls/former removals;16-cavity example:64 cycles/16 tool sets |

Mold removal needs≥124-mm upward core pull and≥10-mm downward former retreat (3⅓ turns), plus handling clearance and reverse reset. Retract the core before conflicting part motion, then open exterior halves laterally. Filling, cooling/curing, ejection, gate/flash removal, inspection and separate cap manufacture remain unpaid. Gang unscrewing/shared pull plates need tooling, torque/reset and cost evidence; casting does not erase these operations.

**Manual-time sensitivities, not forecasts/yields:**10–30 s each for integral removal/inspection plus5 min/plate; stock cut/deburr and two joins; mold core pull/reset, former unscrew/reset, eject/trim and cap join. Excluded: tooling/fixtures, procurement, machine/cure/cooling time, separate ends/caps, scrap, pair assembly and commissioning.

| Sites | Integral active hours / plates | Stock active hours / joins | Mold active hours / joins /16-cavity cycles |
|---|---:|---:|---:|
|1,024|6.43–12.12 /43|8.53–25.60 /2,048|11.38–34.13 /1,024 /64|
|4,096 reference|25.63–48.38 /171|34.13–102.40 /8,192|45.51–136.53 /4,096 /256|
|6,400 reference|40.03–75.58 /267|53.33–160.00 /12,800|71.11–213.33 /6,400 /400|

Reference rows replicate the **same coarse body**, which cannot fit6.35/5.08-mm pitch. Their straight material is20.261–20.562 /31.657–32.128 L; .5° mold29.031–29.332 /45.361–45.832 L; stock feed512/800 m. Coarse joins alone cost2.84–8.53 h cap-only or5.69–17.07 h stock. Adding stock work to E-276's10.94–23.69 h gives **19.47–49.29 h**; integral removal/plate handling gives17.37–35.81 h. Exclusions above still apply; these are not complete estimates. Another minute fitting each coarse pair adds17.1 h. No unbuilt automation earns savings.

Service replaces the column/pair rather than repairing a bonded end in situ. Caps grant inspection access before bonding; no reversible attachment is constructed.

Board repetition:1,024 columns/screws/threads/roofs/bottom blocks,2,048 guide apertures;32-cell row32/64 and8×8 region64/128 pairs/apertures. Two layers retain62 row ribs/frame joints. Quarter/fine references4096/6400 pairs and8192/12800 apertures remain. No private moving guide, latch or anti-backlash nut is added. Individual service through openable shared layers must accommodate136-mm stock; extraction, bed access and re-registration are unconstructed.

E-276's granted four-output S40/S50 waits remain local26.84/31.07 s, scenes201.24/222.88, neutral271.15/331.62, dense391.62/452.09; eight-output local18.46/20.81. S40/N20 and S50/N30 provide actual downward headroom with paid preparation. The old bought allocation$798–1768 is **not a revised BOM** or drive/readback qualification for heavier columns. Retain~30 s/~$500, possible~$1000 finished value/$1000–1500 research and5.08-mm/6400-cell/40-mm comparators; no purchase/preference is inferred.

## Decision and limits

**Horizontal one-piece FDM survives only as a candidate for slicing.** Its thread/ceiling must avoid inaccessible cleanup. Joined stock has accessible ends but2,048 bonds without established labor advantage; open-top molding adds material/joins and lacks a sourced small-thread process. Park both as controls. The2.4-mm-seam/b80/136-mm control still owes thread alignment, elasticity, miniature support and manufacture. No strength, speed, readback, repair or gameplay pass; no reinforcement, tooling, head detail or replacement print.

Next discriminator: actual horizontal body/thread slicing and support-access comparison, including three identical bodies, bridge direction, exterior errors and cleanup. Stop on inaccessible support removal or individual fitting; retain coupled guide/thread alignment as unresolved. This is computational work before any owner handoff.

Checks:432 exact-strip cases, finite collision witness, fit/correlation/pitch limits and21-case grammar;1,140 core sections, volume decomposition/Simpson integral, failed draft, strain-energy beam compliance,24 packing rectangles/gaps, joined-piece/material balance, seat force/moment integration with mesh convergence and labor scaling. Model checks, not hardware proof.
