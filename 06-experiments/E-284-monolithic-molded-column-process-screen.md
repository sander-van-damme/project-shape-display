---
status: complete
builds-on: [E-277, E-280, E-283, E-276]
---

# Monolithic molded column process screen

**Retain one-piece open-channel molding as a conditional whole-body process escape;
park manual casting before mold-detail optimization.** Unlike E-280 screw-only
casting, this removes dominant body deposition and the nut/body joint. Shared
core tooling or supplied finished bodies must also remove handling. Calculated
scenarios, not mold CAD, a quote, material selection or physical qualification.
Run `python3 tools/curated-experiment-checks/E-284/process.py`.

## Construction and complete mechanism

Unite E-277's 10.3-mm-square,136-mm-long U-channel,integral terrain cap and10-mm
intact nut as **one molded component**, retaining the90-degree included,lead-3
thread and separate resident screw. No bonded seam,insert or extra latch.
Compression flows through cap/channel/nut/thread/screw/thrust seat/frame. The
joint disappears;open-section torsion,guide loading,creep and thread strength
remain unqualified. Descent against guide drag still loads the body. Casting
resin does not inherit PLA stiffness/friction.

Proposed reusable tooling sequence:hold the square body in its outer cavity;
rotate/translate a threaded core downward through the nut's open bottom;
withdraw the long smooth cavity core laterally through the open channel;open
the outer cavity and remove the body. Reset both cores before pouring again.
The nut core owes at least10/3=3.33 turns and10-mm retreat,plus unmodeled runout,
shutoff and clearance;reset owes another3.33 turns. A16-cavity gang tool needs16
synchronized rotary cores,16 core/cavity shutoffs and16 lateral core sites,
potentially on one slide. Shared motion does not eliminate these sites.

E-277's thread-free lateral-core check does **not** prove the combined mold
releases. Thread/cavity core sealing,outer split,draft,gates,vents,core deflection
and shrink-on-core torque remain unconstructed. E-280's residual interference in
exact helical extraction is unresolved. No axial stripping or rigid straight-pull
thread release is assumed. Short nut extraction replaces the long screw's68-mm
extraction duty,but supplies no clearance pass.

Resident ledger:2 pieces/cell(body+screw),one threaded pair,two guides,two screw
journals,thrust/keeper and socket;zero body joins. A32-cell row has64 pieces;
8×8 region128;1024-board2048,versus3072/1024 joins for joined channel+nut+screw or
4096/2048 joins for stock tube+ends+screw. Four shared direct spindles remain.
Individual service needs openable guides/bed and full-length access;damaged
integral nuts scrap their body,not a sealed bank. No new service-access proof.

## Whole-board process accounting

E-277 channel+90-degree nut CAD gives4.123 cm³/body,4.222 L/1024. Its actual
three-copy slicing comparison gives533.62 h of channel+nut deposition. Retained
E-279 bare screws add60.68 h;finished journals/collar/socket,frame,scrap and
qualification remain extra. Removing533.62 h is resource accounting,not an
X1C production forecast or demonstrated molding speed.

Assumptions:16 cavities,30-minute cure,full batches,usable fraction1/.8;8–16 h
general setup;2–5 min shared mixing/pouring/outer-tool/lateral-slide work/batch;
five individual10–30-s duties(thread-core removal,core reset,body removal,
gate/seam finishing,gauge);E-276 installation10.94–23.69 h/1024. Manual core
duties include rotation:3.33 turns at assumed60 rpm is3.33 s of each10–30-s duty.
Shared-core case replaces two core duties with gang out/return at60 rpm,
6.67 s/batch,retaining three manual duties. Extra automation development and
hardware are excluded below so their permissible allowance can be calculated.
No measured production rates.

|1024 bodies|Maker h|Single-tool occupied h|Mixed resin L|
|---|---:|---:|---:|
|Manual cores,100% usable|35.30–87.69|42.67–62.93|6.33|
|Manual cores,80% usable|39.38–99.69|53.33–78.67|7.92|
|Shared cores,100% usable|29.61–70.62|37.10–45.99|6.33|
|Shared cores,80% usable|32.27–78.36|46.37–57.48|7.92|

Occupancy charges cure,shared handling and in-tool core/body operations;
finishing/gauging occur outside but stay in maker hours. Printing can overlap
casting;these are resource totals,not a multi-station calendar promise. Exclusions:
master/tool fabrication,replacement molds,extra automation setup,release-agent
preparation,post-cure/cleanup,failed-gauge diagnosis,loaded proof,commissioning.
64/80 shots are needed;assumed25-shot life needs3/4 tool sets,100-shot life1/1.
No tool life distribution or price is established.

At32 maker hours,optimistic installation/setup/shared work leaves38.41 s/attempt
for **all** individual duties. Five10-s manual duties exceed this;three10-s duties
fit at100% usability before exclusions. Shared cores save5.69 h at optimistic
touches,17.07 h at pessimistic touches. Extra gang-tool engineering/setup beyond
those savings removes the maker-time benefit;the pessimistic case still exceeds
32 h. Larger batches reduce shared work,not N releases/gauges.32 h is an owner
build-effort comparison,not a product rejection gate.

4096/6400 coarse-body replication gives manual117.18–302.76 /178.60–464.06 maker h
and shared94.43–234.49 /143.04–357.40 h at100% usable. These are **replication
diagnostics**:10.3-mm bodies do not fit6.35/5.08-mm pitch. No fine-grid tooling,
material or timing compatibility is claimed.

## Cost and process uncertainty

Sources checked2026-10-14:

- [Smooth-On Smooth-Cast300](https://www.smooth-on.com/products/smooth-cast-300/)
  lists density1.05 g/cm³,3-minute pot life,nominal10-minute cure and1% linear
  shrinkage. Thin/low-mass castings take longer;pressure casting is recommended
  for best results. These support cautions,not our30-minute scenario or thread
  yield. Optional maximum-property post-cure takes4–6 h at65°C;equipment and
  handling remain additional.
- [Protolabs threaded-part guidance](https://www.protolabs.com/resources/design-tips/molded-threads-and-how-to-design-them/)
  describes threaded-core removal and restricts its internal-thread service to
  diameters at least7.6 mm. It does **not** qualify our3.5-mm cutter envelope.
  Outsourcing needs a capable process and quote;no supplier was contacted.

Assumed50% mixing/runner waste and$30–80/kg resin give$199–532 resin at100%
usability:allocations,not current prices. E-276's optimistic four-spindle$797.68
hardware allowance leaves negative$297.68 /$202.32 /$702.32 from whole-machine
$500/$1000/$1500 references for **all** body production and other excluded work.
At$1500,only$170–503 remains after resin for molds,cores,pressure/post-cure
equipment,screw finishing and other exclusions. At$1000 the favorable resin
allocation leaves$2.85. Pessimistic inherited hardware$1768.23 already exceeds
these totals. No tooling affordability,finished-price pass or purchase authority.
Supplier-made bodies have at most$0.198/$0.686 each under optimistic$1000/$1500
ceilings **including amortized tooling**,before other exclusions. Do not add the
resin allocation again to an all-in supplier quote.

Uncompensated1% resin contraction changes136 mm by1.36 mm and lead3 by.03 mm;
1% differential lead strain across10-mm engagement accumulates.10 mm. These are
calculations,not tolerances. Printed screws do not automatically share resin
shrinkage. Master/tool bias and cure conditions correlate across cavities/shots;
80% usability is a deterministic scenario,not independent failure probability.
One bad shot can spoil16 bodies;one biased master can spoil every lot. Functional
checks must cover loaded hold,fit,straightness and travel,not cosmetic appearance.
Uniform compensation cannot remove flash,warp or unknown friction.

## Product consequence and decision

12.7-mm/1024-cell S40/S50 retains real N20/N30 neutral and resident support.
Manufacture earns no improvement to conditional850-rpm four-spindle local
26.84/31.07-s,scene~201/223-s,paid-neutral271/332-s or dense392/452-s schedules.
Original~30-s gameplay,~40-mm travel,5.08-mm/6400-cell and~$500 references stay
visible;coarser surface/premium cost are not approved play choices. Powered
speed,arrest,unchanged-neighbor isolation and actual-height sensing remain open.

**Decision:** retain the route because it removes533.62 comparison print-hours
and1024 joins;manual casting is not a demonstrated weekend process. Stop before
parting-line/core-clearance refinements. Reopen detailed tooling through a
concrete low-touch whole-body release/finishing/gauging construction or capable
supplied-process evidence within the economic allowance. No owner input is
needed for this result. E-281 remains the one optional,unperformed fit print.
No new print,purchase or hardware claim.

Verification:independent reconstruction of manual hours and occupancy;partial
batches;yield sensitivity;invariant maker work with changed cure;manual/shared
difference;batch-size monotonicity;inverted32-h budget recovery. Self-review;
no CAD,casting,load or independent validation claimed.
