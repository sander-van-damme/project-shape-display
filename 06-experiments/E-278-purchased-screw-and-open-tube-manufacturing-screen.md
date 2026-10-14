---
status: complete
builds-on: [E-277, E-276, E-260]
---

# Purchased threads remove printing duties but stock cost and fine lead dominate

**Park the sampled M4/open-tube full-board combination before joint CAD.** It removes printed mating threads and inaccessible cavity support, but adds purchased stock, two end joins and a nut insertion per column. At half-square pitch, the four-output S50 control rises from31.07 to75.98 s for the worst local reveal at the same assumed850 rpm. Favorable assembled purchasing scenario is$1714, not a delivered quote. Faster qualified drives and cheaper controlled stock could change the decision; metal threads as a principle are not rejected.

Run `python3 tools/curated-experiment-checks/E-278/stock.py --check`; omit flag for all tables. **Evidence:** supplier listings checked2026-10-14, conditional schedule replay, rigid bounds and labor allocations; self-review, no CAD/contact simulation or physical measurements. E-276/E-277 printed controls remain conditional too.

## Changed construction and sourced boundaries

Proposed coarse construction:32² sites/12.7-mm pitch,10×10/8×8-mm open square tube, small top cap and bottom nut carrier, purchased M4×.7 screw and flat square nut. Retain80-mm guide span,126/136-mm column envelope for40/50-mm stroke, and nominal10-mm bottom/2-mm top allocations. Cut tube lengths114/124 mm. These ends are functional envelopes, not manufactured joints.

| Supplier observation | What it establishes / does not establish |
|---|---|
|[3FParts 3F-00125-006-1104](https://3fparts.com/shop/m4-70mm-socket-head-cap-screw-din-912-stainless-steel-304-a2-70): M4×70, full thread,.7-mm pitch,7-mm head,4-mm head height,3-mm hex recess,2-mm recess depth;₹8.47 at1000|Specific accessible screw/socket dimensions. Extending that tier to1024 is arithmetic;1000+ requests a quote. No landed price, lead accuracy, straightness, wear or rated motion duty.|
|[Accu SSC-M4-70-12.9](https://www.accu.co.uk/metric-cap-head-screws/16035-SSC-M4-70-12-9):70-mm nominal length,**not full thread**,minimum20-mm threaded length|Same nominal size/DIN912 does not guarantee travel. Do not substitute this item for the full-thread candidate.|
|[Accu HFSN-M4-A4](https://www.accu.co.uk/flat-square-nuts/21334-HFSN-M4-A4):7-mm width and2.2-mm thickness,each+0/−.4 mm,.7-mm pitch|Nut envelope/variation,not a calibrated load/lead/backlash specification. No usable price retrieved;cost below is an allocation.|
|[aero-naut ASA tube344-772809, retailer listing](https://www.architekturbedarf.de/plastic/asa-profile-strips/square-tubes/asa-square-tubes-ext-10-mm---int-8-mm/getpdf/):10/8 mm,1000-mm lengths,€4.95 from3 pieces,includes19% German VAT|Retail stock example,not bulk supply quote. Seller warns actual dimensions can differ by a few percent;extrusion is not automatic precision qualification.|
|[B&Q/CQFD aluminium tube3232637800006](https://www.diy.com/departments/anodised-aluminium-square-tube-l-1m-w-10mm-t-1mm/3232637800006_BQ.prd):10×10×1 mm,1 m,£10.67|Accessible material comparator;not a cheaper demonstrated source or a fit/straightness specification. At147 lengths,£1568.49 for tube alone.|

Keep currencies native; USD scenarios below use explicitly chosen conversion factors, **not observed exchange rates**. Availability,shipping/import/tax differences and volume quotations remain unresolved. No supplier contact or purchase.

### Load, travel and service obligations

The intended downward load path is **cap→tube→bottom carrier→nut→screw→head bearing face→lower bed→frame**. A shoulder *above* the nut transfers its upward reaction into the carrier; the carrier's upper seat meets the lower tube annulus. A nut simply glued inside a tube is not that positive compression path. Carrier bond/capture still owes reverse motion,torque,eccentric loading and service strength;two end joins are counted. Nut antirotation requires a formed pocket or grounded restraint;loose placement in8-mm stock is not a completed interface. No force-fit or1024 manual fit adjustments granted.

The screw head must sit **on a lower thrust surface** with central driver access;an upper keeper limits lift. A head merely hanging below a shaft-hole plate cannot carry downward load. This changes E-269's bed/contact dimensions;the inherited resident-support allowance is not a new bearing design.7-mm heads cannot occupy one level at6.35/5.08-mm pitch.10-mm columns also cannot fit those grids. Fine/quarter comparisons below are workload/repetition diagnostics,not constructible variants.

Full nut engagement plus two illustrative2-mm end reserves requires at leastS+2.2+4=46.2/56.2 mm threaded reach.70-mm full thread clears this axial necessary condition;20-mm partial thread does not. Exact head-to-guide stack,runout,usable end threads,engagement strength and end stops remain unconstructed. The2.2-mm nut is not equivalent to E-277's10-mm printed engagement block. Commanded endpoints do not establish physical limits.

The resident pair carries load while the independent shared spindle supplies torque. Unchanged neighbors retain their pairs;they do not transfer onto the writer. Nut/thread/guide friction,head thrust wear,lubrication,backdrive and moving power-loss arrest remain unknown. Smaller lead may improve static holding, but Sander's positive PLA-pair observation cannot qualify this metal pair. Metal stiffness alone does not establish any safe RPM. No private brake/latch is added as an assumed cure.

Use E-276's stop→retract→settle→fresh actual-height read sequence,known-state retry and refusal on unknown/occluded height. Its optical readback is still unqualified. A motor encoder does not verify a captive nut,engaged socket or true terrain height. Openable shared guides/beds permit intended column/pair replacement after unloading;136-mm extraction,keeper access and broken-pair service require construction. Do not seal a module for disposal.

### Stock variation can consume the guide allowance

E-277's rigid envelope,now10-mm width/2.7-mm seam/b80/S50,with clearance.5,total-width error bound±.1 and guide-center bound±.1 mm gives.3-mm minimum aligned clearance and.759-mm neighbor separation. Surface coverage is only**62.0%**,versus65.8% in E-277. Wall width and miniature support counts from filled-cell maps do not transfer.

A competing±.3-mm width bound (3% of10 mm;scenario,not calibrated supplier distribution) makes minimum clearance−.1 mm. Widening nominal clearance to.8 restores.2-mm aligned fit but loses the sufficient neighbor-separation bound(−.629 mm). Negative bound is not a proved collision. This applies the inherited joint guide/column error envelope,not a claim the supplier measured both errors. Common lot bias,local bow/twist and spatial correlations remain unmeasured. No sanding,sorting,guide tightening or further margin optimization is justified by a nominal catalog size.

## Complete conditional wait comparison

Replay E-276 protected-passage maps and physical river/ravine policies;three annotated scenes/four-square windows are a convenience sample,not observed typical play. S40:ground20/depth20/walls+20. S50:ground30/depth20 or30/walls+20;software cannot add stroke. Spindles stay independently driven at25.4-mm spacing. Keep1000 rev/s²,.38-s dock/retract/settle/read transaction,5-s shared handling,XY travel/return and one full-stroke retry. No homing or handling of obscuring miniatures is newly qualified.

Seconds shown areS40/S50. Printed row uses3-mm lead;others.7-mm metal lead. **Every RPM and transaction is an assumption**,not hardware performance.

| Outputs /rpm /lead | Local reveal max | Scene max | Paid neutral | Direct minimum-rest first map | Dense full stroke |
|---|---:|---:|---:|---:|---:|
|4 /850 /3 printed control|26.84/31.07|200.77/222.41|271.15/331.62|321.03/381.50|391.62/452.09|
|4 /850 /.7|56.82/75.98|482.95/575.72|670.07/929.23|883.86/1143.02|1186.38/1445.54|
|4 /2000 /.7|34.53/42.24|274.32/313.75|375.81/485.95|466.66/576.81|595.24/705.38|
|8 /850 /.7|36.96/47.29|336.05/400.59|341.11/471.19|514.56/644.64|599.26/729.35|
|8 /2000 /.7|23.26/27.21|192.47/219.90|192.83/248.11|266.54/321.83|302.54/357.83|

A.7 lead needs57.14/71.43 turns over40/50 mm,versus13.33/16.67 at3. Same nominal linear speed needs3642.86 versus850 rpm;at unchanged rotational acceleration it still gives four-output27.67/31.91-s local waits. Equal motion profiles require scaling acceleration too,1000→4285.71 rev/s²;that torque/inertia claim is unearned. Four-output30-s local crossings occur at2829.56/4340.85 rpm;eight at1197.69/1680.73. These are scheduler roots,not recommended operating speeds. At unlimited RPM but retained acceleration,local floors23.91/25.21 and17.17/17.40 show speed alone is not categorically excluded.

At64²/80²,four outputs/S50/850/.7 yield local259.34/398.37 s,scene1936.35/2993.38,dense5681.41/8849.16. These preserve the~6400-cell/~5.08-mm reference and coarser comparison without pretending the sampled parts fit. Dense stress remains separate from the~30-s gameplay reference;longer waits alone do not make a functional machine impossible.

## Manufacturing and complete-machine economic screen

S50 tube cut124 mm+1-mm kerf with2-mm end-trim allowance yields**7 parts/metre**,not8:8×125+2=1002 mm. For1024 sites buy147 one-metre lengths;finished tube4.571 L,kerf.0369 L,unused/trim stock.684 L. Long stock or recovered offcuts could improve yield;not credited. S40/114-mm tubes yield8/metre,128 lengths,€633.60. Cap/carrier/nut/screw volume and rejected parts are additional.

| Replicated sites | S50 bars /tube EUR | Cuts /end faces /joins /nut inserts | Added handling h |
|---|---:|---:|---:|
|1024|147 /727.65|1024 /2048 /2048 /1024|14.22–42.67|
|4096|586 /2900.70|4096 /8192 /8192 /4096|56.89–170.67|
|6400|915 /4529.25|6400 /12800 /12800 /6400|88.89–266.67|

Last two rows replicate the coarse body as burden diagnostics. Labor assumes five10–30-s operations per site:cut,deburr both ends,insert nut,two joins. No measured cycle times,batch automation,fixture manufacture,cure time,inspection,scrap or commissioning. Manual10-mm screw run-on alone at1–2 turns/s takes2.03–4.06 h/1024;check against inherited8–20-s pair assembly allowance rather than adding it twice. Trays,gang saws and adhesive jigs could reduce touches,but need demonstrated cycle/quality data. Outsourced extrusion cut-to-length or molded carrier batches need quotes,minimum-order/tooling and tolerance specifications. These are useful reopening paths,not free economies.

Per site:five handled parts(tube,cap,carrier,nut,screw),two joins,one threaded pair/nut antirotation interface,two guides,head thrust and upward keeper contacts.32-cell row:160 parts/64 joins/64 guides;8×8 region:320/128/128;board:5120/2048/2048. Resident support,guides,62 row ribs and head/wiring duties from E-276 remain. No printed thread or closed long cavity remains,but joining and alignment burdens are real.

Keep E-276's dated four/eight-output bought allocations$797.68–1768.23/$1077.94–2263.63,including resident bed allowances,**excluding printed-part material**. Add tubes and screws;nut price allocated$.10–.50 each. Low scenario conversion1 USD/EUR and.010 USD/INR;high1.3 and.015. These brackets are deliberately chosen sensitivities,not rates,quotes,confidence intervals or market floors.

| Outputs | Added tube/screw/nut USD | Bought total USD | Maker hours incl.base |
|---|---:|---:|---:|
|4|916.78–1588.04|**1714.46–3356.28**|25.16–66.36|
|8|916.78–1588.04|1994.72–3851.67|25.83–68.36|

No double subtraction of printed costs:they were outside bought baseline. End-piece printing,adhesive,new bearing details,freight/import,scrap and tooling remain unpaid. Total material/time cannot inherit E-277's integral-print estimate. Even free screws/nuts plus low-conversion tube give four-output$1525.33. Under$1500,the favorable four-output case leaves**$3.49/metre** for stock after listed screws/nuts;under$1000,there is essentially no stock allowance. Eight outputs leave$1.58/metre at$1500. Original~$500 bought target,possible~$1000 finished value and$1000–1500 demonstrator remain comparisons;none is a purchase authorization or automatic rejection gate.

## Decision and verification

This is a material manufacturing escape,not a thread-fit tweak. It eliminates two printed thread forms per site and sealed support removal,but the sampled retail stock combines high spend,substantial joins and slower ordinary-speed updates without a qualified guide/holding/readback system. **Do not develop its nut carrier or tighten its guides now.** Reopen with cheaper dimension-controlled batch stock/joining and a credible loaded drive window;do not claim all extrusions,metal screws or slower premium displays are excluded. An isolated purchased pair can remain a later diagnostic control without selecting1024 copies.

Checks:independent stock packing/material conservation,dense station/spin closed forms,S40/S50 and4/8 outputs,invariant routing under lead change,exact lead/rate/acceleration scaling,guide-bound sensitivity and cached-vs-full threshold replay. Existing E-276/E-277 evidence retains its scope. No owner test,reminder,new preference question,hardware purchase or physical validation.
