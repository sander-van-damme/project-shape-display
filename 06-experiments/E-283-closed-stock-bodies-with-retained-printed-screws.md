---
status: complete
builds-on: [E-282, E-278, E-276, E-262, E-277]
---

# Closed-stock bodies with retained printed screws


**Retain hollow aluminium stock with the printed lead-3 pair as a conditional comparator.** This separates E-278's expensive sampled ASA body from its slow purchased M4 thread. It removes the maker-made longitudinal seam and channel deposition,not the two end joints. Run `python3 tools/curated-experiment-checks/E-283/closed_stock.py`. Sourced listings and calculations,self-review;no CAD assembly or physical qualification.

Sources checked2026-10-14:

- [OBRAMAT ref10357312](https://www.obramat.es/productos/tubo-cuadrado-aluminio-bruto-10x10x1mm-2-6m-10357312.html): hollow10×10×1-mm aluminium,2.6 m,€4.93/bar including displayed IGIC;comparison table lists1 m at€2.75 including IVA. Store selection governs availability/prices and regional tax labels differ. These are observed listing values,not delivered Dutch prices or stock commitments. No dimensional/straightness specification retrieved. Closed stock means no maker-made seam,not certified metallurgically seamless extrusion.
- [Sinclair & Rush](https://www.sinclair-rush.co.uk/categories/tubes-bars-rods/plastic-box-section-square-tubes/?id=80986) offers RPVC extrusion and bulk cut lengths,but its smallest displayed **exterior** is13 mm;10 mm is internal. It cannot fit12.7-mm pitch. The cutting service does not establish a suitable product.
- [KIPP K0493](https://www.kippcom.nl/en/products/OPERATING-PARTS/Tube-connectors-profile-connectors/Round-tubes-and-square-tubes/Round-and-square-tubes-/p/agid.2022) explicitly identifies10×10-mm aluminium as **solid bar**,despite the “square tubes” family title. It cannot supply the screw cavity;do not transfer family tolerances to a nonexistent hollow10-mm item.

The older sampled stock prices were not general floors. No supplier contact or purchase.

### Changed construction and load

Use10/8-mm tube cut124 mm,retaining136-mm assembled height,10-mm nut/2-mm cap envelopes,80-mm guide span,S50 and physicalN30 neutral. E-277's10.3-mm end parts are **not drop-in fits**;new10-mm cap/nut envelopes and positive seats remain unconstructed. Intended compression path:cap→tube annulus→nut shoulder→printed thread→resident screw thrust bed. Joints still owe reverse/eccentric load,torque and capture. No adhesive/press-fit rating is granted. Openable guides/bed must preserve individual pair replacement.

Per cell:tube,cap,nut,screw;two joins,one threaded pair,two guide interfaces,two screw journals,thrust/keeper contacts and socket. A32-cell row has128 parts/64 joins;8×8 region256/128;board4096/2048. Four shared spindles remain. Compared with E-278 there is no separate metal nut insertion or.7-mm lead;compared with the open printed channel,the cap adds one join. No new resident latch.

Area36 mm² and assumed2.7 g/cm³ give12.05 g/tube,12.34 kg/1024 and.118 N each
before ends/payload. This consumes59% of a.2-N **total** load; if.2 N means payload,
load is at least.318 N. See the mass/support extension below.

Inherited E-278 guide calculation:62% coverage,.759-mm sufficient gap at
assumed.5-mm clearance/±.1-mm width/±.1-mm guide-center bounds;±.3-mm width loses
fit. Size,bow,twist,burrs and lot correlation are unmeasured;no guide-fit sweep.

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

A failed bonded/staked body is replaceable as one cell, not necessarily reusable.
Destructive release may scrap tube and ends. An openable bed/guide must permit
removal without releasing loaded neighbors; that access is unconstructed.

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

Only1024/12.7mm is contemplated; larger counts are replication diagnostics.
At1024,one16-seat adhesive carrier occupies206.22–234.67 h;16 carriers/256 seats
reduce elapsed joining to17.22–45.67 h including final3-h cure, but retain
14.22–42.67 hands-on hours. Inventory/space are additional. Charging unload time
before dwell conservatively delays reuse. These uninterrupted station schedules
do not overlap retained printing or promise calendar delivery.

The explicit-touch ledger supersedes the earlier four-aggregate-operation labor
estimate. Shared cure management does not remove handling. Park individual plug
and stake details: staking saves2.49–7.47 maker hours at1024 but adds8192 unqualified
deformation sites. Extra cure carriers, press/dies and consumables are unpriced.
Reopen through multi-part feeding/seating/gauging, supplied assembly or elimination
of an end joint. Checks cover partial batches, serial and unlimited-carrier limits,
monotonic carrier benefit and invariant manual work.

### Automation investment ceiling

`python3 tools/curated-experiment-checks/E-283/automation_budget.py` inverts that
ledger before investing in a feeder. **Necessary calculated bounds, not a
constructed automated process.** Retain accepted-pair installation, cutting,
4–12 h general setup and 2–4 h joining-fixture setup. Add an illustrative 60 s of
shared operator work per 16 attempted bodies. Every remaining per-body operation
must fit the residual allowance: deburring, loading all three components, dosing,
unloading, gauging and routine cleanup. Calling a platen automatic cannot remove
these operations. Additional automation development/setup is charged separately.

|Case, 32 maker-hour comparison|1024 bodies: residual s/attempt|4096 diagnostic|6400 diagnostic|
|---|---:|---:|---:|
|Optimistic inherited base; no additional automation setup|48.09|2.47|infeasible|
|Same, plus 8 h automation setup|19.97|infeasible|infeasible|
|Same 8 h, 80% usable fraction, 60 s additional handling/reject|3.10|infeasible|infeasible|

Only 1024 at 12.7-mm pitch is a proposed fit; 10-mm bodies still cannot fit the
quarter-square 6.35-mm or reference 5.08-mm grids. The larger columns in the table
are replication diagnostics, not alternative playable layouts. “Infeasible”
means fixed/shared/reject work already exceeds this **chosen maker-hour scenario**
even with zero residual handling; it is not a product rejection or a universal
bound on other production routes. The pessimistic inherited base alone is 40.62 h
at 1024, so joining-only automation cannot make that case fit 32 h. Even the
optimistic 17.25-h base exceeds a 16-h build before residual work.

At1024/full usability,8 h setup costs28.125 s/body. At80% usability,1280 attempts
include256 rejects costing4.27 h in diagnosis/disposal. This is a deterministic
lot scenario, not measured independent yield. Bad lots may also need repeated
setup/qualification. Proof, commissioning, adhesive preparation and unlisted
tooling remain unpaid; cure occupancy and printing remain separate elapsed costs.

**Decision:** a shared press or faster cure is not an established weekend route.
Before feeder CAD, require concrete transfer of deburring/component feed/gauge
work or supplied assembly. The20-s/3.1-s allowances are falsifiable targets, not
proven cycles. Checks independently reconstruct target totals, recover the manual
ledger and verify setup, partial batches and yield sensitivity.

### Stock mass versus screw support

**Retain the stock route conditionally; do not transfer its 850-rpm schedule into
an operating claim.** `OPENBLAS_NUM_THREADS=1 python3
tools/curated-experiment-checks/E-283/load_screen.py` applies E-262's existing
linear beam model to the changed moving body. This is a calculated sensitivity,
not calibrated contact dynamics, measured material properties or a motor rating.
No new bearing, thread, owner print or purchase is selected.

Tube mass12.05 g plus **assumed2-g ends/joining** gives14.05 g. The printed
E-277 control is5.18 g:124×23.44 mm² channel,2-mm integral cap and solid10.3²×10-mm
nut envelope at assumed1.24 g/cm³. Nut bore is not deducted; joining is excluded.
These are calculated comparators, not weighed parts or identical sections.
With **.2-N payload**, total gravity is.251/.338 N and moving mass25.57/34.44 g
(printed/metal). Payload is illustrative, not surveyed miniature loading.
Screw mass remains separate. Both use64-mm thread,S50/N30.

Reuse root1.4/OD3.2 mm,E1000 MPa, screw density1400 kg/m³ and51 nut positions over
S50. Nut load/support acts at its midpoint7–57 mm, leaving the full overhang.
Base translation is fixed; spring cases use10 Nmm/rad base slope stiffness.
The table gives **minimum0.8×linear natural frequency expressed as rpm**:

|Nut support, .2-N payload|Printed body|Aluminium body|
|---|---:|---:|
|Ideal point restraint, simple base|991|991|
|.1 N/mm spring, zero lateral body lump|630|620|
|.1 N/mm spring, full translating mass lump|463|395|
|1 N/mm spring, full translating mass lump|832|815|
|No nut restraint, fixed base|static instability|static instability|

Zero/full lateral mass at the nut are allocation scenarios, not bounds on real
long-column dynamics; distributed rotation, unilateral contacts and frame modes
are omitted. Soft/full-lump minima occur18/20 mm into travel. Ideal support
suppresses lump translation and leaves the screw overhang dominant. Without
payload/nut restraint, minima are686/167 rpm; metal's small static margin is not
qualification. The OD-cylinder screw is.721 g (.0071 N), whose distributed gravity
is omitted from geometric stiffness; defects/creep also remain absent.

E-277's helix-corrected thread-only force triangle gives raising torque at
assumedμ=.3 and .2-N payload of **.240/.323 Nmm** (30° included profile) or
**.286/.385 Nmm** (90°), printed/aluminium respectively:34.7% more for metal.
An added.1-N upward guide-drag scenario is included in the executable output;
collar drag, preload, acceleration and motor torque-speed capability are not.
The friction-only holding thresholds stayμ=.403/.305 for30°/90° because load
cancels in this model. More weight raises torque magnitude, not that threshold;
negative calculated lowering torque atμ=.3 means this ideal thread would need
braking. It neither refutes Sander's observed holding pair nor qualifies this
changed pair. Friction, support and moving power-loss arrest remain unmeasured.

**Decision:** mass alone does not reject stock, but its savings do not close
support or feeding. Before further tooling include total load and guide-to-screw
coupling; do not add resident bearings or tune fits from assumed spring values.
The earlier parts/cost ledger and conditional gameplay schedules remain unchanged;
no replacement rated speed, ~30-s gameplay pass or physical isolation follows.
No new print or purchase; E-281 remains optional/unperformed.

Checks recover E-277's torque anchor and independent force-triangle form, force
scaling and holding sign, stock mass conservation, Euler SI/N-mm equivalence,
nonincreasing frequency with added load/mass, and40→80-element changes below
1.75×10⁻⁶ in three checked loaded soft-support positions. Numerical convergence
is much smaller than the uncalibrated model uncertainty. Self-review only.
