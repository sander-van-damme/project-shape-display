---
status: candidate
builds-on: [E-255, E-256, E-258, E-260, E-262, E-269, E-273, E-274, E-275, E-281]
---

# DES-007 — radial pinch strip, four-output demonstrator

**Recommendation: the small manual multiplexing test below, using existing supplies where available. Do not build a full display from this package.** Radial friction avoids socket phase acquisition and E-275's axial squeeze. Four outputs at 6.35 mm pitch share a strip; four adjacent pins witness unintended motion. The drive is an **open strip**; a circulating belt is only a comparator.

**Digital product engineering is incomplete.** No candidate meets both the 30-second complete-play benchmark and $1,500 full-display budget. Performance, common-base wall clearance, production tape and affordable selectors remain failed or unresolved gates. The bench tests selection, bidirectional drive, isolation and retention. No purchases, hardware operation or new physical measurements occurred.

## Baseline and architecture decision

E-255/256 contain firsthand reports of manual screw translation/holding, roughly 2 mm lead and 1 mm play, and breakage near disengagement. These do not qualify powered operation or this new geometry. Historical Trial 5 at `41484f96999847c139b9010e73009d73e9459c89` used 4.4 mm tubes, 3.2 mm screws and nominal 3 mm lead; library/slop reconstruction is not a demonstrated fit. Here E-281's explicit external-generator subtraction gives a 90° profile, 3 mm lead, .9 mm depth and .15 mm radial relief. Existing short-thread tests remain unchanged and physically unknown.

E-254/257/258 provide workloads, not measured gameplay frequencies. E-259–275 retain their speed, routing, phase and friction limits. Independent motion, retained load, neighbor isolation and playable one-inch geometry remain essential; 406.4 mm, 40/50 mm travel, 30 seconds and budgets are comparison targets.

| Construction | Mechanism | Screening result |
|---|---|---|
| E-273 moving rack/socket head | Rack → pinions → selected sockets → resident screws | Paid return and arbitrary screw phase still defeat this embodiment. |
| Permanent row strips and resident pressure latches | Signed strip drive; scanning writer sets retained pressure states | Requires 4,096 catches/releases in addition to threads. Addressing cannot retain states. No cost/manufacturing advantage established. |
| Travelling linear gripper + row brake | Gripper takes load, brake releases, gripper moves, brake closes | Releasing an entire row leaves unchanged neighbors unsupported unless individual catches/takeover are added. |
| E-275 underside friction pad | Common rotor → sliding shaft → friction face | Thrust friction and axial lift remain; a stronger selector does not remove them. |
| **Radial pinch strip** | Shared strip → selected circular rim → screw → square pin | Phase-free contact model; concrete rig. Traction, retention, tape life and isolation need physical evidence. |

Three geometry iterations were implemented. A straight strip could bridge selected–unchanged–selected rims: five fixed separators now constrain OFF spans. A straight upright shoe hit the rear wheel: an offset steel link and cross-arm replace it. A .6 mm strip/large-retraction shoe collided during withdrawal: the current .2 mm strip, .4 mm stroke and concave cross-arm clear the sampled envelope, introducing a serious thin-tape qualification gate. Closed journal plates also prevented insertion over integral rims: both planes are now three split pieces assembled around shafts.

## Mechanical construction

Coordinates are mm; `cad/rig.scad` is authoritative. X=0,6.35,12.70,19.05; Y=0,6.35. The fixed bench services only the front row. [The print handoff](../../owner-print-tests/radial-pinch-four-pin/test.md) supplies assembly, parts and the acceptance sequence.

| Interface | Nominal construction |
|---|---|
| Screw and radial support | Ø2.4 shaft; Ø5×3 drive rims at Z−4…−1 / −10…−7; two split 3 mm journal planes at Z0/15, Ø2.6 apertures. Lower rim is overhung, not bracketed below. |
| Axial load path | Pin → 10 mm thread engagement → screw → Ø5×2 collar at Z18…20 → upper bed → six tie bolts/spacers → foot. Keeper Z20.2…21.8 reacts upward loads; .2 axial float. |
| Thread/pin | Ø3.2 thread Z20…40, Ø1.4 root; 5×5×25 pin, 10 mm nut, Ø3.8 hollow and 1 mm closed top. Nut bottom Z22+q, top Z47+q. q=0…6 preserves full overlap and 2 mm end reserve. |
| Guidance/stops | 5.3 square holes at Z34…36 / 44…46; .15 side clearance. Roof at Z53.2 catches near q=6.2; collar catches bottom near q=−2. Neither stop is a commanded position. |
| Shared strip | TPU test coupon 180×3×.2; X translation. OFF front Y−2.8 versus rim tangent−2.5: .30 nominal gap. Printed TPU is not a production belt rating. |
| Separators | Five Ø1 steel wires at X=(i−.5)6.35, Y−2.3; length23.8. Their back tangent−2.8 constrains each OFF span. |
| Independent selector | Printed sliding base + printed tip + bonded Ø.8×18.8 steel link, offset X3.175. Base Y−4.4 OFF / −4.0 ON; tip front−3.1/−2.7. Strip thickness completes contact. |
| Selection/release | M3 screw pushes base (.8 turn nominally .4 mm); loosen and pull its manual return tab to release. No automatic return or calibrated force. |
| Retention | Resident thread/collar friction alone holds after release. No hidden brake: observed backdrive fails the build. |

Normal force reacts through journals, without deliberately lifting the screw. Thrust friction still matters. A nominal steel link with .8 mm diameter, 9.6 mm free length, E=200 GPa under .8 N deflects .059 mm (elastic calculation, not paperclip/adhesive qualification). Metal links are not printable PLA substitutes.

Five-mm caps leave 1.35 mm gaps (62.0% area coverage). Coplanar bases bridge caps; cliff-edge support is unqualified. Guide play allows several tenths top displacement. The roof is only a bench catch. A 50 mm stroke needs ≥64 mm threaded length and about 114 mm body for a roughly 60 mm guide separation; this 25 mm tube cannot provide it. E-262's long-column speed/overhang limits remain.

### Actuation cycle

Establish all eight q≈3 physically and record heights/wheel marks. Under gentle strip tension engage only requested shoes. To command `[+3,−3,+1,0]`, select 0/2, pull 5.236 mm (+1 ideal height), stop/release 2, pull 10.472 more for 0 (+2), stop/release 0, select 1 and reverse 15.708 (−3). Stop/release all. Second-row pins remain untouched. Reverse and inspect. Different signs serialize; magnitudes retire at stopped thresholds. Threads/support never disengage. Slip affects accuracy, not socket phase. Preparation is real work, not a software offset. At-speed release is only an unqualified timing control. Stop on binding, unexpected rotation, backdrive or strip damage.

## Contact and drive bounds

For R=2.5, journal radius r=1.2, torque T0 excluding radial-load-induced friction, use conservative `F_rad ≤ N+T/R`:

`T_required=(T0+mu_j*r*N)/(1−mu_j*r/R)`; `T_available=mu_strip*N*R`.

`analysis/system.py` sweeps T0=.1/.35/1 Nmm, N=.4/.8/1.2 N, strip friction .2/.4/.6 and journal friction .1/.25/.4: **assumptions**, containing passes and failures. At T0=.35, mu_j=.25, N=.8, torque≈.670 Nmm; at mu_strip=.4 capacity=.800. This is a narrow hypothetical margin. Sixty-four outputs require 17.2 N strip pull **before** shoe/guide drag: 28.6 MPa in a 3×.2 section. The test strip is unqualified at scale. Segmentation adds drives/tensioners and costs.

[Habasit's textile guide](https://www.habasit.com/-/media/Project/Habasit/PublicWebSite/Documents/English/Industries/Textile/2006-Yarn-0519-en.pdf) supports the industrial drive analogy, not this selective mechanism. [TS-5](https://tdm.habasit.com/PDS/en-us/Spindle%20Tapes/TS-5-en-us.pdf) specifies .55 mm,1.6 N/mm per1% extension and15 mm minimum pulley diameter including counter-flexion; [W-8](https://tdm.habasit.com/PDS/en-us/Spindle%20Tapes/W-8) also specifies 15 mm. Neither is qualified around Ø5 rims/Ø1 separators. Wear, reverse tracking and splices remain unknown.

[Pololu4841](https://www.pololu.com/product/4841), source checked2026-10-14, is12 V,2200 rpm no-load,1.7 kg·cm extrapolated stall,5 A stall,4 mm shaft,$56.95 single. At10 mm capstan radius,17.2 N needs .172 Nm, approximately stall: **fails** this full-row scenario without reduction/segmentation. Endpoints are not continuous ratings. The first test is hand-driven.

## Gameplay geometry and sourced miniature sizes

Compare 80² at 5.08,64² at 6.35 and32² at 12.7 over 406.4 mm (16² one-inch squares). **6.35 is a test pitch, not an accepted gameplay resolution.** This offset-link envelope does not fit 5.08;12.7 loses relief detail without solving walls.

[WizKids25 mm bases](https://shop.wizkids.com/products/wizkids-deep-cuts-clear-25mm-round-base-15-ct) explicitly serve Deep Cuts/Nolzur's; [Nolzur's](https://wizkids.com/dnd-unpainted/) labels 25 mm bases. [LITKO](https://litko.net/products/1-inch-coherency-trays-3-figure-line-formation-25mm-circle-bases) distinguishes 25 mm/one-inch bases. [Wizards SRD5.2.1](https://media.dndbeyond.com/compendium-images/srd/5.2/SRD_CC_v5.2.1.pdf) assigns Small/Medium a 5-foot square, not a guaranteed plastic diameter. Design for **25–25.4 mm bases**;32 mm is an oversized check. Miniature scale is not base diameter.

An assumed 25.6 mm upper envelope plus .25 placement clearance/side needs **26.1 mm**. These are design allowances, not sourced manufacturing tolerances. Centered 1 mm walls leave **24.4 nominal /24.0 with .2 inward error/side**. Even .4 sheet leaves25.0 nominal. All three pitches fail this one-square corridor.

Dimensioned drawings also check a 4.2 mm bottom recess for an assumed≤3.2 mm-high base: centered placement can fit, but 4 mm corner feet leave only 21.4 mm traversal opening. **Failed passage**, not a solution. Figure overhang is also unknown. Widening passages or displacing supports may work for specific maps but cannot silently preserve adjacent one-square corridors. No zero-thickness wall or owner-approved compromise is claimed.

## Whole-system timing and improvements

`analysis/system.py` imports unchanged E-258 semantic workloads: shallow/deep ruins/river/ravine, every directed map/preset transition plus neutral,384 four-square reveal windows/grid and dense signed stress. The sample is not validated. Heads start/finish at their own bank origins. Model includes 150 mm/s and1500 mm/s² seeking, .20 s approach/withdrawal per row, .15 per stopped mask including clearing,150 rev/s² drive acceleration, .10 settling+.15 verification allowance per row, one full-row retry/head and5 s common preparation. All rates are unmeasured assumptions. The finite strip pays unloaded net return after each row. Unknown initial heights require additional unbounded commissioning; excess faults also have no bounded time.

64²,3 mm lead,850 rpm **loop comparator**, seconds:

| Heads / selectors | Worst scene | Worst local reveal | Known-zero first map | Neutral then first map | Allocated total USD |
|---|---:|---:|---:|---:|---:|
| 2/128 |89.28|22.39|87.95|128.01|2,773–5,668|
| 4/256 |51.09|21.04|47.91|71.92|4,872–9,197|
| 6/384 |38.18|20.61|36.94|54.69|6,972–12,727|
| 8/512 |29.38|20.26|28.90|44.36|9,072–16,257|

The constructed-strip principle's **four-head scale comparator takes 68.93 s** (cold69.51; neutral+first97.25). Output contains both finer pitches, leads2/3,400/850/1500 rpm,2/4/6/8 heads, sustained updates, stresses and critical-bank ledgers. Four-head loop/strip sustained means 46.68/60.64 s; dense opposite-sign stress66.20 s. Manual wall/miniature handling is additional:10/30/60 s makes the optimistic29.38 case 39.38/59.38/89.38 s. No full-play30-second objective is marked met.

`analysis/improvements.py` checks two escapes. Moving retirement reduces four-head850-rpm loop time to 44.00 s; six heads1500 rpm reach 29.07. But .05 s release delay alone means 2.125/3.75 mm error before coast/slip. A 16-writer retained mask in four sectors at .04 s/sector+.08 reset costs .24 s/mask: four/eight heads become 57.48/32.80 s. Four-head selector-only allocation is$1,558 before the rest of the machine; latches remain unqualified. Neither establishes an affordable compliant machine. Tape strength and gameplay acceptance remain gates.

## Cost and manufacture

`system.py::cost` accounts for resident material/scrap, all selectors/links/drivers/wiring, motor/encoder, tape/tension/guards, Y/Z axes, frame/guides/panels, power/fuses, controller, inspection, walls, jigs/fasteners, shipping/contingency. Allocations are **not quotes**, exclude paid labor/VAT and require location-specific pricing. [FS0403](https://www.pololu.com/product/3421/specs) comparator:$9.35 at5,20×8.3×19.3 mm,.08 s/60°,.7 kg·cm stall6 V; not a loaded .15 s clutch rating. Full-row selector packaging is not released CAD.

4,096 thread pairs/rims/collars plus two radial/two square-guide duties remain. $.04–.12 material/site includes assumed scrap, not measured yield.12–30 seconds/pair,4–10 minutes/shared output and8–20 common hours imply **38.7–96.8 maker hours** for four heads, excluding printing and remedial work. Thousands of hand-fitted parts are not accepted as a production plan. `prototype-bom.csv` separately accounts for the small hand rig. Service only unloaded; open the split bed/keeper, replace the pair and recheck all eight heights.

## Evidence and continuation

| Criterion | Classification | Limit |
|---|---|---|
| Playable geometry | **Failed / unresolved** | Centered-wall corridor fails common bases; no player trial or approved alternative. |
| Independent bidirectional motion | **Computationally supported; physically unresolved** |625 ideal signed replays; nominal CAD/isolation only. |
| Complete small-rig mechanics | **Computationally supported; physically unresolved** | Journals/collar/keeper/guides/stops/shoes/links constructed; friction, bonds and tape untested. |
| Full-display scalability | **Unresolved** | Long columns, production tape, transport and full selector packaging not released. |
| Approximately 30-second complete-play update | **Not met** | Constructed-strip scale model misses; favorable controls lack qualified hardware/handling. |
| Cost/manufacture | **Failed at $1,500 full-display allocation; bench fit unresolved** | Complete costs and assembly hours exposed; no production yield. |
| Reproducibility | **Computationally supported** | SCAD, scripts, profiles, STL handoff and verification record supplied. |
| Physical validation path | **Prepared, not performed** | Four active/four witness pins, adversarial commands and acceptance sheet. |

See `verification.txt` for versions, commands, CAD and slicer evidence. **Next decisive step:** optional unloaded 1010/0101 isolation, signed commands, then modest measured loads and stopped release. Leakage, backdrive, inadequate traction or strip damage stops this embodiment. A pass permits measured force/speed windows and one-bank engineering, not a full-array purchase. Product continuation separately needs a common-base wall solution and accepted cost/update trade-off. This package does not declare the mission accomplished.
