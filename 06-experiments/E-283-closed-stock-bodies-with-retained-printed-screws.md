---
status: complete
builds-on: [E-282, E-278, E-276]
---

# Closed-stock bodies with retained printed screws


**Retain hollow aluminium stock with the printed lead-3 pair as a conditional comparator.** This separates E-278's expensive sampled ASA body from its slow purchased M4 thread. It removes the maker-made longitudinal seam and channel deposition,not the two end joints. Run `python3 tools/curated-experiment-checks/E-283/closed_stock.py`. Sourced listings and calculations,self-review;no CAD assembly or physical qualification.

Sources checked2026-10-14:

- [OBRAMAT ref10357312](https://www.obramat.es/productos/tubo-cuadrado-aluminio-bruto-10x10x1mm-2-6m-10357312.html): hollow10×10×1-mm aluminium,2.6 m,€4.93/bar including displayed IGIC;comparison table lists1 m at€2.75 including IVA. Store selection governs availability/prices and regional tax labels differ. These are observed listing values,not delivered Dutch prices or stock commitments. No dimensional/straightness specification retrieved. Closed stock means no maker-made seam,not certified metallurgically seamless extrusion.
- [Sinclair & Rush](https://www.sinclair-rush.co.uk/categories/tubes-bars-rods/plastic-box-section-square-tubes/?id=80986) offers RPVC extrusion and bulk cut lengths,but its smallest displayed **exterior** is13 mm;10 mm is internal. It cannot fit12.7-mm pitch. The cutting service does not establish a suitable product.
- [KIPP K0493](https://www.kippcom.nl/en/products/OPERATING-PARTS/Tube-connectors-profile-connectors/Round-tubes-and-square-tubes/Round-and-square-tubes-/p/agid.2022) explicitly identifies10×10-mm aluminium as **solid bar**,despite the “square tubes” family title. It cannot supply the screw cavity;do not transfer family tolerances to a nonexistent hollow10-mm item.

The old€727.65 ASA/£1568.49 aluminium examples are not general stock price floors. No supplier contact or purchase.

### Changed construction and load

Use10/8-mm tube cut124 mm,retaining136-mm assembled height,10-mm nut/2-mm cap envelopes,80-mm guide span,S50 and physicalN30 neutral. E-277's10.3-mm end parts are **not drop-in fits**;new10-mm cap/nut envelopes and positive seats remain unconstructed. Intended compression path:cap→tube annulus→nut shoulder→printed thread→resident screw thrust bed. Joints still owe reverse/eccentric load,torque and capture. No adhesive/press-fit rating is granted. Openable guides/bed must preserve individual pair replacement.

Per cell:tube,cap,nut,screw;two joins,one threaded pair,two guide interfaces,two screw journals,thrust/keeper contacts and socket. A32-cell row has128 parts/64 joins;8×8 region256/128;board4096/2048. Four shared spindles remain. Compared with E-278 there is no separate metal nut insertion or.7-mm lead;compared with the open printed channel,the cap adds one join. No new resident latch.

Calculated area36 mm² and **assumed** density2.7 g/cm³ give12.05 g/body,12.34 kg/1024 and.118 N self-weight/column before ends,miniature or screw. Self-weight uses59% of an illustrative.2-N total axial case;if.2 N instead denotes payload,the sum is at least.318 N. Recompute drive/holding against total mass before reusing old torque cases. Transport mass is secondary,but self-weight is mechanically relevant. Packaged shipping weight is not a measured bare-tube density.

E-278 already provides the10-mm guide control:62.0% top coverage,.759-mm sufficient neighbor gap at assumed.5-mm clearance/±.1-mm width/±.1-mm guide-center bounds;±.3-mm width loses fit. None is a measured stock tolerance. Lot-correlated size,bow,twist and cut burrs remain unknown;do not start another guide-margin sweep.

### Batch ledger and decision

|Coarse bodies replicated|2.6-m bars /listed EUR|Finished tube kg|8-bar-group saw strokes|End joins|Maker hours scenario|
|---:|---:|---:|---:|---:|---:|
|1024|52 /256.36|12.34|140|2048|26.63–70.76|
|4096|205 /1010.65|49.37|520|8192|68.44–192.76|
|6400|320 /1577.60|77.14|800|12800|99.78–284.22|

4096/6400 are replication diagnostics:10-mm bodies cannot fit6.35/5.08-mm grids. Assumed1-mm kerf/2-mm trim gives20 parts/bar;seven groups of at most8 bars give140 strokes/1040 blanks. Suitable clamping without crushing/slip is unproven. The1-m control needs147 bars/€404.25. At80% completed usable fraction:64 long bars/€315.52 and29.52–79.42 maker hours;reject end pieces/printing remain additional. No independent defect probability assumed.

Labor assumptions:60–180 s/group loading/clamping,5–15 s/stroke,four10–30-s operations/body (deburr both ends,join cap,join nut,gauge),4–12 h setup plus E-276 installation. Pair run-on is already in that base. Fixture fabrication,cure occupancy,consumable preparation,failed checks,transport and commissioning remain unpaid. A cut-to-length quote must specify squareness,burrs,bow and size;“cut” is not “finished.” Saw automation does not automate2048 joints.

Removing channels eliminates384.66 comparison print-hours;retained nut/bare-shank allowance209.64 h is **accounting only**,since changed ends need new slices. Caps,finished screw ends,frame,scrap remain additional. At assumed1.0–1.3 USD/EUR,stock adds$256.36–333.27. E-276 four-output hardware plus a separate$100–500 cutting/fixture allocation gives partial bought$1154.04–2601.50 before freight,tax reconciliation,end materials,joining and inspection. No quote,exchange-rate forecast,$1500 demonstrator pass or~$1000 finished-price claim;the~$500 reference remains unmet by this allocation.

Lead3 preserves only the *kinematic* S40/S50 comparison:local26.84/31.07 s,scene~201/223 s,paid neutral271/332 s,dense392/452 s at assumed850 rpm. Manufacture earns no loaded speed,holding,power-loss arrest,readback or~30-s gameplay qualification. Coarse pitch/62% coverage remain unapproved play choices;unchanged neighbors retain their resident pairs but isolation is unqualified.

**Decision:** reopen body-cost comparison,not E-278's fine-lead pair or individual plug/fit CAD. Next useful independent construction:shared end joining with explicit seating/load path,cycle,fixture occupancy and repair route that reduces repeated handling. Cheap stock and fewer saw strokes alone are insufficient. E-281 stays optional/unprinted. Finite cut replay,gang coverage,material conservation,replication,yield sensitivity and invariant end-join checks passed;not hardware proof.

### Shared end-assembly screen

`python3 tools/curated-experiment-checks/E-283/end_assembly.py` adds a finite
single-operator/carrier schedule. **Calculated scenarios, not measured production
rates or CAD/contact proof.** Two constructions keep the resident screw/height
memory and replace neither the thread nor the drive:

- **Seated adhesive ends:** top cap bears on the upper tube annulus; bottom nut
  has a lower flange bearing under the tube annulus. Both flanges stay within the
  10-mm outer envelope, with square spigots entering the nominal 8-mm bore.
  Compression passes through seats rather than adhesive alone. Adhesive still
  owes capture during commanded descent against guide drag, eccentric lifting,
  and rotational clearance take-up. A shared carrier locates 16 tubes; a platen
  seats ends before the carrier leaves for cure. No adhesive, bond thickness,
  substrate preparation or cure strength is qualified. Opposed rigid platens do
  not accommodate unequal cut lengths automatically; shared seating compliance
  or individually floating tooling would need construction and accounting.
- **Shared inward staking:** retain those seats, replace bonding by indenting
  tube walls into recesses in each end spigot. Four indent sites per end mean
  eight plastic-deformation sites/body,8192/1024,not two magically shared joints.
  Process bodies outside the display at wider fixture spacing, then install them.
  Two end operations each use opposed tooling; square spigots react torque.
  Inward displacement must preserve the screw cavity; outward bulging must clear
  guides. Unspecified stock alloy/temper, springback, wall splitting, polymer
  crushing/creep and correlated die-height errors prevent a capture/force pass.
  Shared press force sums simultaneous sites and cannot be inferred from the
  small miniature load. No press selection or purchase is justified.

Both preserve four resident parts, two joins and independent resident support.
A bonded or staked tube/nut unit is replaceable **as one cell**, not promised
reusable: accessing the failed unit requires the still-unconstructed openable
bed/guides and removal of its screw. Neighbor support cannot depend on removing
an entire loaded row. Destructive release can scrap tube and ends; thread failure
is not fixed by resetting software. E-281's short loose pairs cannot qualify
these joints.

Explicit manual work: deburr twice; load tube,cap,nut; seat; unload; gauge = eight
per-body touches. Adhesive adds two doses. Staking adds two shared press/reorient
operations,20–60 seconds **total per 16-body batch**. Each touch takes an assumed
5–15 seconds; assume three-hour carrier dwell for adhesive and zero for staking.
These are competing bounds,not calibrated distributions; cleaning, glue mixing,
full proof testing, rework and automation are excluded. E-283 cutting/setup and
E-276 installation stay charged; joining fixture setup adds2–4 hours.

|Bodies|Adhesive maker h|Stake maker h|Adhesive touches|Stake touches|
|---:|---:|---:|---:|---:|
|1024|31.48–83.29|28.99–75.82|10240|8192|
|4096|81.81–230.89|71.86–201.02|40960|32768|
|6400|119.56–341.56|104.00–294.89|64000|51200|

Only1024 at12.7-mm pitch is geometrically contemplated; the larger counts remain
replication diagnostics,not fits at6.35/5.08mm. At1024,one16-seat adhesive carrier
occupies206.22–234.67 hours for this joining sequence. Sixteen carriers/256 seats
reduce that to17.22–45.67 hours,including the final three-hour dwell,**without
changing14.22–42.67 hands-on joining hours**. That is extra carrier inventory and
space,not free automation. Charging unload time before dwell conservatively
withholds carrier reuse. These are uninterrupted station schedules,not a calendar
promise; retained printing and other production stages are not overlapped here.

The optimistic adhesive total leaves only0.52 hour against an illustrative32-hour
maker weekend; the stake case leaves3.01 hours before exclusions. The upper bounds
exceed it substantially. The earlier26.63–70.76-hour coarse estimate used four
aggregate10–30-second body operations; this explicit sequence is a changed
process assumption,not evidence that workers actually got slower. Tooling money
is not newly quoted: the previous$1154–2602 partial bought allocation excludes
these extra cure carriers/press/dies/consumables. No~$500 or$1000 finished-price
pass; a$1000–1500 research allowance does not authorize purchasing.

**Decision:** shared seating/cure management alone does not establish low-touch
assembly; park individual bonded/staked plug refinement. Staking trades2.49–7.47
maker hours at1024 for thousands of unqualified deformation sites. Reopen through
actual multi-part feeding/seating/gauging evidence, a supplied assembled body/end
route, or a construction that eliminates an end joint. Do not presume a faster
adhesive cures the handling problem. Retained lead3/S40–50/N30 and assumed850-rpm
local26.84–31.07s,scene201–223s,neutral271–332s,dense392–452s remain unchanged;
no~30-second gameplay,loaded speed,retention or isolation qualification follows.
No new owner print. Checks cover partial batches,serial closed-form limits,
unlimited-carrier limit,monotonic carrier benefit,and invariant manual work.
