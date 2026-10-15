> Preserved independent screening ledger. Earlier mass and traveling-head allocations are superseded for the resident geometry by the revised system audit. See ../cost-and-manufacture.md for the final integrated cost disposition.

> Updated drive comparison: the [bank-drive study](../bank-drive.md) adds a conventional supported four-screw transmission at $903–1,424 for two banks. It substitutes for the two unqualified lift motor/driver accounting pairs; it is not an extra pair of motors. This embodiment exceeds $1,500 with the selector electronics before the remaining terrain mechanism. A cheaper transmission is a new engineering obligation, not a credited saving.

**Final-geometry update:** the legacy ledger below uses the earlier 7.06-kg column estimate. The resident CAD instead gives 14.93 kg. The revised independent audit in [revised-system.md](revised-system.md) updates raw polymer, lift demand and the remaining budget; no complete resident fabrication quote exists. The $100 common power allowance concerns selector/control power, while the conventional-drive provision separately counts its 36-V supplies. Neither establishes adequate capacity or duty for the 704-W coil reference.

# Manufacturing and cost: surviving bank lift and rejected traveling heads

**Read the stationary global-platen addendum below for the surviving architecture.** The earlier traveling-head allocations are preserved comparison evidence, not the selected architecture’s BOM. Complete resident-module fabrication remains unquoted.

2026-10-14, independent manufacturing/economics review. Reproduce `python3 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/cost.py`. Full itemized counts and low/high allocation rows are in [the itemized CSV](../analysis/bom-comparisons.csv); full numerical output in [cost-results.json](../analysis/cost-results.json).

## Decision

**The retained-mask head saves money relative to 64 direct catalog selectors per head, but the emerging complete machine is not demonstrated inside $1,000–$1,500.** Eight retained heads are an approximate **$2.58k–$6.33k allocation**, versus **$4.94k–$7.91k** for eight direct-solenoid heads. Those are explicit component/material allowances including *unquoted custom-fabrication reserves*, not quotations or proven sale prices. Even deleting every custom-fabrication reserve leaves the eight-head retained machine at **$2.07k–$4.00k**. Do not promote it as an affordable complete machine using only its 64 writer-solenoid count.

Four retained heads are closest: approximately **$1.55k–$3.86k** under this ledger. Whether four suffice for representative timing is the decisive next comparison. If only eight heads satisfy timing, the cost/time conflict is real. Fewer independent motion axes and mechanically synchronized heads deserve an explicit timing comparison; hypothetical production pricing does not resolve the conflict.

Direct control has lower selection complexity and can be the better *small mechanism demonstrator*, but it does not win the complete-machine catalog cost comparison. It retains the shared-load handoff mechanics. It also has a serious hold-power and packing burden unless a new latching or low-hold-current selector is qualified.

## Count the proposed architecture completely

Fixed display: 4096 terrain stems, 4096 grounded pawl/lock interfaces, two guide apertures per stem, fixed pawl supports, guide carriers, frame and service access.

Each retained head has 64 moving dogs, 64 A dog-control keys, 64 vertical C-guide interfaces, 64 B grounded-pawl release keys, 128 compliant reader rods, 64 mask flags, two common keepers, two reader platens, eight expensive writers, writer traverse, Z lift, row transport and a coupled phase sequencer. Counts are interfaces/parts as specified by the lead, before detailed CAD establishes which features can share a manufactured piece. An integral comb lowers individual piece count, not the number of required working contacts.

| Whole-machine count | B4 retained | B6 retained | B8 retained |
|---|---:|---:|---:|
| Grounded pawls | 4096 | 4096 | 4096 |
| Moving dogs | 256 | 384 | 512 |
| A keys | 256 | 384 | 512 |
| Vertical C-guide interfaces | 256 | 384 | 512 |
| B keys | 256 | 384 | 512 |
| Compliant reader rods | 512 | 768 | 1024 |
| Retained flags | 256 | 384 | 512 |
| Common keeper bars | 8 | 12 | 16 |
| Reader platens | 8 | 12 | 16 |
| Writer actuators | 32 | 48 | 64 |
| Independent motion axes/drivers | 16 | 24 | 32 |
| Eight-channel coil driver boards | 4 | 6 | 8 |
| Coil conductors, excluding electronics interconnect | 64 | 96 | 128 |
| Motor phase conductors | 64 | 96 | 128 |

The **fair direct variant** deletes masks, compliant reader rods, keepers, reader platens, writer actuators and writer traverse. It retains 64 moving dogs, A keys, B keys, guidance and ordered common sequencing per head. A direct selector cannot simply pull the stationary lock open before the moving dog has accepted load. Agent B independently agreed with this accounting. The direct variant therefore needs **256/384/512 selectors** and **12/18/24 motion motors/drivers**, with 512/768/1024 coil conductors plus motor phases. It is not a bare solenoid attached to every ground pawl.

A compound one-coil linkage might consolidate A/B parts, but its capture-before-release and reseat-before-uncouple mechanism has not been designed. Its cost is not credited here. Both variants need the same pin support, neighboring-row isolation, stopped-axis load retention and service provisions.

## Catalog evidence and what it does not prove

Prices accessed 14 October 2026, USD before shipping/tax:

* [Adafruit 2776 solenoid](https://www.adafruit.com/product/2776): $4.46 at 10–99, $3.96 at 100+; 5 V, 1.1 A, 3-mm throw/80-g quoted force, 12.6-g mass. Use $4.46 for retained 32–64 writers; $3.96 for direct 256–512 selectors. No force-speed curve or continuous-duty qualification was supplied by the page.
* [Adafruit 6318 eight-channel coil driver](https://www.adafruit.com/product/6318): $14.95 at 1–9, $13.46 at 10–99. The [guide](https://learn.adafruit.com/adafruit-i2c-to-8-channel-solenoid-driver/overview) identifies individual MOSFETs rated 3.6 A peak and 70 mΩ. This is not a demonstration that the board's shared input/terminals/thermal layout tolerates eight simultaneous 1.1-A coils continuously. Boards also have only eight I²C addresses; the direct architecture needs bus segmentation or local controllers, included as an allowance but not designed.
* [Adafruit 324 NEMA17](https://www.adafruit.com/product/324): $12.60 at 10–99; 350-mA 12-V rating and 0.20-Nm holding torque. [Adafruit 6109 A4988](https://www.adafruit.com/product/6109): $6.26 at 10–99. **These establish a transparent motion-electronics price anchor, not selected motors.** In particular, a quoted holding torque does not qualify the required high-speed load; the motor page's demonstrated 50 rpm does not establish a fast Z axis. Actual motion-motor procurement can exceed the low-price allowance. High allocations use $25 motor/$12 driver as scenarios, not sourced quotes.

Motion motors are assigned per head: writer traverse, Z, row and sequencer for retained; Z, row and sequencer for direct. A common sequencer already drives both A/B reader actions, so no extra reader motor is charged. Mechanically sharing axes between heads could reduce count but invalidates independent-head scheduling until recomputed.

### Priced electronics subtotal

| Configuration | Coil actuators + coil drivers | Motion motors + drivers, low price anchor | Subtotal before all mechanics, power and controls |
|---|---:|---:|---:|
| B4 retained | $202.52 | $301.76 | **$504.28** |
| B6 retained | $303.78 | $452.64 | **$756.42** |
| B8 retained | $405.04 | $603.52 | **$1008.56** |
| B4 direct | $1444.48 | $226.32 | **$1670.80** |
| B6 direct | $2166.72 | $339.48 | **$2506.20** |
| B8 direct | $2888.96 | $452.64 | **$3341.60** |

This table explains why counting only expensive writers is misleading. B8's 64 solenoids are $285.44, but its complete *priced electronics anchor* is over $1,000 before all terrain and mechanisms.

## Whole-machine allocation

The script includes every major stated category: coils; coil boards; all motion motors/drivers; Z guides/transmission; row guides/transmission; sequencer shaft/cam/link stock; writer traverse; head polymer; common precision/load-path fabrication; memory-specific fabrication; terrain polymer; fixed guide polymer; all grounded pawl fabrication; structure/feet/covers; controller/communications/limits; power conversion/distribution; wiring/connectors/fusing; fasteners/shims/spares.

Low allocations assume simple stock guides, owner-produced printed carriers, modest frame, qualified cheap motor choices and no custom hand fitting. High allocations reflect more expensive stock assemblies and larger fabrication reserves; they are **not upper bounds**. No external supplier has accepted the geometry or quoted the custom parts. All scenarios exclude paid labor, printing-machine depreciation, electricity, new tools, shipping, VAT, physical qualification and redesign.

| Configuration | Subtotal **excluding all custom-fabrication reserves** | Allocation **including reserves** |
|---|---:|---:|
| B4 retained | $1217–$2370 | **$1547–$3860** |
| B6 retained | $1645–$3187 | **$2065–$5097** |
| B8 retained | $2074–$4004 | **$2584–$6334** |
| B4 direct | $2516–$3756 | **$2726–$4646** |
| B6 direct | $3593–$5266 | **$3833–$6276** |
| B8 direct | $4671–$6776 | **$4941–$7906** |

Three explicit unknown fabricated-cost terms are essential:

* `Q_ground`: all 4096 grounded pawls/comb fabrication, low/high allowance $150/$650 per display. This is not a quotation. Depending on selected metal/print process and seat construction it could be higher.
* `Q_head`: common dogs/keys/load-path finishing/cam fabrication beyond raw head polymer and transmission stock, allowance $15/$60 per head. This is extremely sensitive to whether many features integrate into a small number of printable/etched pieces. Outsourcing hundreds of individually machined keys would greatly exceed it.
* `Q_memory`: flags, compliant rods, keepers and reader-specific fabrication, allowance $30/$150 per head. It assumes bulk array production, not bespoke machining per flag. Thin spring comb capability is documented in D's first report; actual price and fatigue qualification are unknown.

The low total includes the rack-wall-preserving hollow stem material at assumed $20/kg; high includes 100-mm solid stems. Neither is a slicer-derived material bill. Actual CAD volumes and chosen suppliers should replace these allowances before procurement. These numbers are suitable for rejecting hidden-cost claims, not claiming budget compliance.

### Memory break-even threshold

At the sourced electronic prices, one direct head's 64 coils and eight coil boards cost $361.12. One retained head's eight writers, one coil board and *extra* writer motor/driver cost $69.49. The retained mechanism therefore has **$291.63 per head** available to pay for writer guide/drive hardware, memory-specific manufacturing and extra assembly before direct hardware becomes cheaper, ignoring the direct variant's larger power burden.

After the assumed $12–$30 writer hardware, the remaining threshold is **$261.63–$279.63/head**, or about **$4.09–$4.37 per retained bit** including two compliant reader rods, shared hardware and labor. That is a plausible target for bulk printed/etched mechanisms; it is not free. At an illustrative $20/h labor value, three extra assembly hours per head consume $60 of that margin. A design requiring eight hours of fitting plus $150/head fabrication already exceeds it. The real break-even decision is whether a repeatable memory mechanism can stay below this total and meet scan time, not whether it contains fewer motors.

### Electrical burden

| Configuration | All-coils-on current at 5 V | All-coils-on electrical power | Coil mass |
|---|---:|---:|---:|
| B4 retained | 35.2 A | 176 W | 0.403 kg |
| B6 retained | 52.8 A | 264 W | 0.605 kg |
| B8 retained | 70.4 A | 352 W | 0.806 kg |
| B4 direct | 281.6 A | **1408 W** | 3.226 kg |
| B6 direct | 422.4 A | **2112 W** | 4.838 kg |
| B8 direct | 563.2 A | **2816 W** | 6.451 kg |

The retained writers need short pulses if flags retain state. The direct design must keep selected state throughout the handoff/move unless it adds mechanical memory or a truly bistable actuator. Thus table values are peak limits, not sustained wall-power predictions; direct dense moves can nevertheless sustain a large fraction. Dense scenes must not be excluded from PSU, wiring or thermal analysis. Reducing PWM holding current is a useful experiment but needs force-versus-stroke/temperature measurements; it cannot be assumed from rated current. Simple flyback diodes can slow release and therefore affect timing.

[Adafruit SG92R micro servos](https://www.adafruit.com/product/169) are an alternative direct-selector reference: $4.76 at 100+, 23×11×29 mm, 9 g and quoted 0.1 s/60°. Four heads require $1218.56 of servos before PWM electronics, brackets or transmissions. They may reduce continuous coil heating but do not restore the original cost target; actual response, holding current and settling remain unqualified. At 6.35-mm pitch the 11-mm bodies need at least two staggered rows and transmission to each lane. Do not count a hypothetical zero-hold-current servo as a positive mechanical lock.

A retail product called a “latching solenoid” may simply operate a door latch. [SparkFun ROB-15324](https://www.sparkfun.com/solenoid-12v-latch-lock.html) is explicitly powered-to-retract and spring-return, $15.95 single, not a bistable state memory. Genuine pulse-held solenoids exist (for example [Takigen's keep-type explanation](https://www.takigen.co.jp/tech/solenoid)), but a small affordable force-qualified part has not been selected. Such a change needs pricing, packaging and a reversing driver, not just a different noun.

## Stem mass and tolerance implications

Proposed geometry is 5.4-mm X by 3.8-mm Y stem, 6×6-mm cap, 6.35-mm pitch and 40-mm stroke. Length was not frozen when this screen was made, so both 80/100 mm are shown. PLA density assumption 1.24 g/cm³; cap thickness 1.2 mm. Rack recesses are not subtracted in the conservative envelope calculation.

| 4096 columns | 80-mm stem | 100-mm stem | Caveat |
|---|---:|---:|---|
| Solid envelope | 8.43 kg | 10.52 kg | Can be reduced with grooves/infill only after stiffness and layer paths checked |
| Symmetric 0.8-mm hollow walls | 5.09 kg | 6.32 kg | **An 0.8-mm blind rack recess penetrates this wall**; not credited as drop-in design |
| 1.6-mm rack-side wall, other walls 0.8 mm | 6.30 kg | 7.85 kg | Leaves 0.8 mm behind 0.8-mm recess; cavity3.8×1.4 mm; local tooth strength remains unqualified |

This corrects a tempting optimistic hollow-rod estimate. Symmetric walls save 40.7% of cross-section but delete the blind-recess back wall. The supported-rack hollow alternative saves only 25.9% of section. Deliberate through-window rack teeth may be feasible, but require new load-path and wear analysis. The hollow variant should have a printable closed roof across only the small cavity width, not inaccessible supports along an 80-mm bore. A closed cap also changes bridge/roof paths; inspect actual slices.

A second issue is guide-web packaging. The 5.4-mm X stem leaves only `6.35−5.4=0.95 mm` to divide between diametral clearance and a shared guide web. If the guide has 0.60-mm clearance, its web is 0.35 mm: below the ordinary 0.45-mm extrusion used by previous experiments. If the web is 0.60 mm, diametral clearance is 0.35 mm. Under explicit sensitivity bounds ±0.15 mm on stem/hole width and 0.10-mm local registration, remaining radial clearance is `(0.35−0.15−0.15)/2−0.10=−0.075 mm`, a jam witness. These are uncertainty tests, not measured X1C tolerances.

A 4.8–4.9-mm X stem underneath the same6-mm cap offers a straightforward escape: 0.60-mm clearance then leaves0.95–0.85-mm guide webs. Alternatively, etched/machined guide plates and calibrated printing may achieve smaller clearances, but that is a process-dependent cost and qualification choice. Do not label the present5.4-mm stem “generous-tolerance FDM.” Cap gaps are only0.35 mm; guide tilt and stem bending must not let raised caps touch neighbors.

## Assembly and maker time

No measured assembly times exist. The script deliberately keeps every operation visible:

* Common display:10–20s to load/check each terrain stem,64 whole-row strips at1min each or512 eight-finger strips at2min each, and8–16h for frame/electronics/general assembly.
* Common per head:64 dogs at5–15s,128 A/B keys at10–30s,0.5–1.5h alignment, and three motion assemblies at0.33–0.75h each.
* Retained selection per head:64 flags at8–30s,128 compliant reader rods at12–45s,0.5–1.5h keepers/platens,0.5–1.5h writer traverse, eight writer mount/wire checks at60–180s,0.2–0.6h control verification.
* Direct selection per head:64 selector mount/wire checks at45–180s,0.5–1.5h interface setting.

| Configuration | Calculated hand-work sensitivity |
|---|---:|
| B4 retained | **35.8–100.7 h** |
| B6 retained | **43.5–123.1 h** |
| B8 retained | **51.1–145.6 h** |
| B4 direct | 33.4–95.0 h |
| B6 direct | 39.9–114.5 h |
| B8 direct | 46.3–134.1 h |

These are neither forecasts nor qualified rates. They expose the consequence of replicated assembly and small-module segmentation. The low scenario already narrowly exceeds four8-hour days for B4, before printer upkeep, repair or extensive testing; B8 cannot honestly be sold as an established weekend build. The high scenario illustrates why many loose small parts are unacceptable. Batch fixtures and integral arrays must remove actual touch operations, not merely move them to an uncounted “preassembly” stage. One minute of per-terrain-site fitting adds68.3h to every scenario. A failed production process should be corrected rather than hand-tuned into service.

A buildable memory design must specify how128 rods/head remain captured during insertion, how spring preload is set collectively, how64 flags/head reset without individual trimming, and how whole-head wear components can be replaced. A mask with512 physical bits and1024reader rods at B8 is a substantial small-parts machine despite only64expensive writers.

## Concrete simplifications that could change the decision

1. **Four heads if measured timing permits.** The savings are much larger than shaving a few cents from each flag. A four-head direct demonstrator can still use a small subset of lanes; that does not promise a cheap full board.
2. **Share writer traverse across heads.** All use eight writer addresses. One mechanically common traverse could replaceB motors/rails with one, but independently ready heads then wait for the common scan; worst added latency can approach one scan. Scheduling must count that. A continuously scanning writer may serve ready masks, but a fresh mask is not valid until all its addresses have been visited. Double buffering requires more passive hardware.
3. **Share phase sequencer and/or5-mm Z shuttle.** Long racks let a common stroke act on selected pins at arbitrary current heights. Shared same-sign pulses are physically natural, but opposite signs and independently completing rows require phased scheduling. Connecting all heads mechanically can reduce32 axes to roughly11 for B8 (eight row axes + common writer/phase/Z) before further row coupling. Catalog motor/driver saving is roughly$396, plus associated stock hardware, but combined load/stiffness and synchronization need new calculations. The current independent-head timing must not be reused unchanged.
4. **Integrate guides and spring arrays into a few serviceable cassettes.** This is the meaningful route to lower assembly time. A cassette still needs individually replaceable stems and must retain all neighbors when opened. Full-width combs avoid thousands of pieces but demand support and registration across406 mm.
5. **Keep direct selectors as a benchmark until passive memory is physically real.** Its extra cost buys simpler state acquisition and removes the serial rewrite bottleneck. If a complete retained head costs over approximately$292 more in fabrication/assembly per head than the direct mechanical interface, retention has lost its claimed monetary advantage even before its timing penalty.

These investigations are decision-changing because they alter head count, whole axes or repeated assembly. Minor CAD polishing and friction tweaks do not address the system gap.

## CAD review boundary

When this report was generated, the announced first prototype sources were not yet present. The dimensional objections above therefore review the communicated geometry and operation counts, **not a rendered assembly**. A final CAD packing review remains to be appended after those files exist. In particular, verify A-key fullZ travel, B-key independent return, all reader rod capture, unselected-key isolation, springseat load path, guide webs, caps at maximum tilt and the writer's64-address mapping. Cost confidence cannot exceed geometry confidence.

## Later iteration: two stationary banks with global platen and resident mask

The lead subsequently supplied a new timing candidate: two stationary2048-site banks, a global lift platen for each bank, row-addressed resident selection memory,128 reused data actuators, two row-enable/index axes, two globalZ axes and two support sequencers. The supplied timing result is20.82s for40-mm range /22.91s for50-mm range at80ms **complete row write**, with timing break-even row writes around143/122ms respectively. These timing results belong to the separate throughput workstream; D has not independently reproduced that simulation. An80ms row write must include row positioning, gating, actual bit movement, retention and release. This cost screen does not turn that timing assumption into physical evidence.

**This is a stronger active-component count than eight traveling heads but a substantially larger resident passive machine.** Necessary counts now include4096grounded pawls,4096positive transport dogs,4096resident mask bits and approximately4096–8192additional keys if separate dog and stationary-pawl control is needed. Any two-reader-per-site implementation would also have8192reader contacts/rods. A resident bit must control a dog moving with the platen and a stationary pawl in a safe sequence; that interface has not been constructed or costed. Do not take the favorable global timing while retaining only the small traveling-head memory count.

### Necessary affordability threshold, not a whole-machine quotation

The exact current catalog tiers give:

| Item | Count × sourced unit | Subtotal |
|---|---:|---:|
| Adafruit2776 data solenoids |128×$3.96|$506.88|
| Adafruit6318 eight-channel boards |16×$13.46|$215.36|
| Motion motor/driver price anchors |8×($14.00+$6.95)|$167.60|
| **Electronics price anchor** ||**$889.84**|

Only six axes are explicitly assigned by the architecture description; eight are retained here as an explicit two-axis auxiliary reserve. At eight units the motor/driver quantities use1–9catalog prices, not the10+tiers used by the traveling-head comparison. Pricing only the six assigned axes lowers the anchor to$847.94. Neither count has qualified the force/speed of the actual global-lift motors. Driverboard all-channel current and bus segmentation remain to be engineered. A custom PCB may lower the$215driver bill, but still needs128switches/flyback networks/connectors, layout/manufacture/assembly and validation; subtracting the whole bill is unjustified.

At a$1500total, the eight-axis anchor leaves **$610.16**, only **$0.149/site before all terrain material, frame, power, guides or mechanical transmission**. Deduct merely the following explicit low allocations: two-sided rack-backed hollow80-mm terrain material$141.27, frame$80, controller$30, power$100, wiring/fuses/connectors$50. The remaining amount is **$208.89, or$0.0510/site**, for **all** groundpawls, resident bits, positive transport dogs, extra keys, guides, platen, shafts/bearings/belts, precision fabrication, fasteners and spares. This is a stringent necessary cost target, **not demonstrated manufacturability at five cents per site**. The named mechanical categories have not been built, so a credible complete BOM cannot yet be supplied.

At$1000, electronics leave$110.16; the illustrative terrain-column material alone exceeds that remainder. At$500, this particular sourced electrical configuration already fails the bought-parts benchmark. These are scoped conclusions for the specified component choices, not a theorem that every possible custom-coil or PCB implementation must cost as much.

The global architecture should therefore be recorded as **timing-promising under stated row-write assumptions, cost unresolved**, with a necessary low-cost resident mechanism still missing. A multi-site bench prototype can demonstrate that interface before any4096-site manufacturing commitment. If the per-site mechanism needs even$0.25 of extra purchased/fabricated hardware, that adds$1024; at$0.50 it adds$2048. A five-part/site mechanism assembled at10seconds per part consumes56.9hours before the frame or tests. Integrating each resident bit and lock into etched/molded arrays may materially reduce touch time, but requires actual geometry and process quotations.

### Global force is a different problem from a row head

A bank can have2048simultaneously moving columns. The80-mm two-sided rack-backed hollow stem assumption contributes approximately34.6N of column weight per bank. An explicitly chosen **5kg terrain/miniature load concentrated in one bank** contributes49.1N, about83.7Ncombined before platen, dogs and other moving-machine mass. This is a design load scenario, not a measurement of typical gameplay or an owner-approved payload specification. The local1N/pin prototype load is a stress-test value; multiplying it by2048does not describe actual ordinary distributed miniature loading. Guide drag, however, can occur at every moving pin and must be measured.

| Assumed drag per simultaneously moving site | Added friction,2048sites | Bank lift force including columns+5kg terrain, excluding moving-machine mass | Torque at8-mm screw lead,30% efficiency |
|---:|---:|---:|---:|
|0.01N|20.5N|104.2N|0.44Nm|
|0.03N|61.4N|145.1N|0.62Nm|
|0.10N|204.8N|288.5N|1.22Nm|
|0.25N|512N|595.7N|2.53Nm|
|0.50N|1024N|1107.7N|4.70Nm|

All drag values are **sensitivity inputs**, not empirical PLA values. Formula is `T=F*lead/(2π*efficiency)`. Acceleration, friction transients, platen mass, support-point imbalance and design margin are additional. The$14price-anchor motor's0.20Nmholding torque therefore does **not** qualify even thelow-drag8-mmlead case. A reduction drive or suitable larger motor and multi-point supported platen is required. Lower screw lead reduces torque but increases rpm;80mm/s requires600rpm at8-mmlead or2400rpm at2-mmlead. A cheap holding-torque specification cannot validate either operating point.

A global lift can be physically plausible—100N at80mm/s is only8W useful linear power—but stiffness, synchronized support, high-drag tails and load-transfer failures matter more than ideal energy. The decisive next measurement is aggregate free-moving guide drag and lock-release/capture force on a small full-pitch module, followed by a bank-scale load path with known mass. Any quoted global motor should then be selected at operating speed with measured friction margin. Do not reuse the former64-site head force budget for a2048-site bank.


### Subsequent source-level review of B's minimum handoff CAD

the first `rack_handoff.scad` prototype source became available after the preceding first draft. This is a manual four-active/four-witness15-mm-stroke test, not the resident global-mask mechanism. Source inspection establishes the following; there was no physical test and no mesh-based clearance simulation in D's review:

* **A definite print-plate overlap was reported to B for repair:** the second square guide post's long body spansX12.8–15.2,Y72–133,Z0–2.4 after its plate transform; the long-peg flange centeredat(16,105) spansX13.5–18.5,Y102.5–107.5,Z0–1.5. They intersect. B subsequently reported moving long pegs toX42–63,Y125 and small pegs toX76/81,Y125; source inspection confirms that change. This removes the identified post/peg overlap. B is performing independent mesh/component checks; D has not repeated those. This was a layout defect, not a mechanism rejection.
* The pawl head bears on a nominal0.6-mm-wide rigid ground-seat ledge. The terrain-contact overhang from that ledge is about0.75 mm, so the long0.6-mm printed leaf is used to bias the pawl while the seat takes load. This is the correct intended load-path principle. The actual narrow seat's print paths and wear remain unqualified.
* The retracted dog body reachesY4.35 while the neighboring witness stem beginsY4.45: **only0.10-mm nominal isolation gap**. The dog sidearm's stated0.15/0.20-mm gaps to neighboring stems and guide-slot0.15-mm side clearances are likewise sensitive. They can be useful test dimensions, but CAD separation cannot establish untouched-neighbor movement under FDM variation.
* Both upper/lower guides use5.8-mm X holes with5.4-mm stems: nominal0.20-mm side clearance and0.55-mm webs. This is somewhat printable geometry, but the previously described width/registration bound still gives a jam witness. The guide/rod manufacturing process must be tested together.
* The actual pin has **0.65-mm grooves on both front and rear faces**. Thus a symmetric0.8-mm hollow wall would leave only0.15mmbehind each groove. Preserving0.8mmbacking needs1.45-mm front/rear walls and a3.8×0.9-mm cavity, saving only16.7% of gross cross-section. The new global-platen cost/force arithmetic uses this two-sided backing case:7.06kg/8.80kg for4096columns at80/100-mm envelope lengths, before groove-volume subtraction. The earlier traveling-head table deliberately retains its original one-sided optimistic envelope so its provenance remains visible; it should not be promoted to a final material bill for the two-sided CAD.

The prototype is an appropriate inexpensive test of positive loaded handoff if the plate overlap is fixed and the owner understands those fit uncertainties. It does not validate full-stroke rod stability, fast selection, resident memory, global-plate stiffness or full-array manufacturing yield.


The preliminary 15-mm-stroke, 5.4 × 3.8-mm stem CAD comments above preserve the review that triggered revisions. They are not the final print dimensions; use the released coupon handoff and final review for those.
