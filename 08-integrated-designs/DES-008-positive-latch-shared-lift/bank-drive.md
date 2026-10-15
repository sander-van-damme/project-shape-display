# D — Global bank drive and resident-cell manufacturing review

**Reference-model boundary:** the tables below preserve the earlier lighter-column drive study. The final resident geometry has 14.93 kg of solid columns and about 8.25 kg of stationary steel channels. Use [the revised independent system audit](review/revised-system.md) for current mass, force, cost and timing; the original tables are sensitivities, not a motor qualification for that CAD.

2026-10-14. Independent manufacturing workstream. Reproduce with `python 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/bank_drive.py`; JSON prints to stdout. This is a sensitivity calculation and procurement screen, **not a qualified motor selection or completed full-machine BOM**.

## Decision

A bank containing 2048 terrain sites does not inherently need an industrial servo. At mean sliding drag at or below 0.1 N per simultaneously moving site, a sensibly geared NEMA23 or efficient ball-screw transmission has a credible torque/speed envelope. At 0.5 N/site the same drive fails its selected margin, even though individual pins would still feel easy to move by hand. Measure summed drag before selecting the bank motor.

A conventional four-ball-screw bank adds approximately **$452–712 per bank**, including explicitly unquoted provisions. Two banks add $903–1424 before terrain, selection, main frame or controller. This is a costly construction reference, not an irreducible architecture cost. Two screws with independently guided stiff crossbeams could reduce it by approximately $139–182 per bank, but need a deflection/load-distribution design. A rated belt lift could reduce cost further; no belt SKU is qualified here. The resident mask's repeated parts remain the larger uncertainty. A $1500 complete machine is **unresolved and not supported by this conservative drive implementation**.

## Load definition

A 64×32-site bank occupies 406.4×203.2 mm at 6.35-mm pitch. The calculation assumes all 2048 sites move together; partial masks reduce column and drag forces but not the moving platen's mass.

| Mass case | Columns kg | Moving platen/frame kg | Miniatures/terrain kg | Total kg |
|---|---:|---:|---:|---:|
| Light | 3.532 | 1.5 | 1 | 6.032 |
| Root's 2-kg platen scenario | 3.532 | 2 | 5 | 10.532 |
| Nominal engineering envelope | 3.532 | 3 | 5 | 11.532 |
| Heavy, solid 100-mm columns | 5.258 | 5 | 5 | 15.258 |

Columns use the earlier 5.4×3.8-mm stem, 6×6×1.2-mm cap and 80-mm length, with 3.8×0.9-mm internal cavity preserving material behind both rack faces. The mass is a conservative envelope without subtracting open rack pockets, density 1.24 g/cm³. It is **not the mass of A's later 3×2.4-mm integration stem** or B's 95-mm solid prototype; those variants require their own CAD mass. The later broad upper bodies make the complete integrated columns heavier than this earlier envelope; the revised audit replaces this mass for that geometry. The 5-kg concentrated terrain allowance is a declared stress scenario, not measured normal miniature mass.

For upward acceleration, `F = m(g+a) + n f_drag`, with `a=0.8 m/s²`, `v=0.08 m/s`, `n=2048`. A separate 1.5 design factor is applied to force before drive torque calculation. Guide drag includes stem bearings and engaged moving interfaces; actual stiction, dust and installation errors are unknown. It does not include force needed to actuate every local pawl at once: A/B sequencing must be sized separately. A 1-N local retention test does not mean every terrain site experiences 1 N in normal operation.

| Mean drag N/moving site | Nominal peak upward N | Steady mechanical W at 80 mm/s | Four-corner design load N/corner |
|---|---:|---:|---:|
| .01 | 142.8 | 10.7 | 53.6 |
| .03 | 183.8 | 14.0 | 68.9 |
| .10 | 327.2 | 25.4 | 122.7 |
| .50 | 1146.4 | 91.0 | 429.9 |

Corner loads above assume equal distribution. Off-center miniatures, platen bending, assembly error and diagonal rack must be checked separately. Four screws divide axial load, **not total motor torque**.

## Transmission comparison

For effective lead `L` per motor revolution and assumed efficiency `eta`, `T=1.5 F L/(2 pi eta)` and `rpm=60 v/L`. Efficiencies are design assumptions, not source-validated for an actual purchase.

| Transmission | Motor rpm | Assumed efficiency | Torque at .01/.03/.10/.50 N/site, Nm |
|---|---:|---:|---|
| TR8×8 direct | 600 | .30 | .909 / 1.170 / 2.083 / 7.298 |
| 1605 ball screw direct | 960 | .90 | .189 / .244 / .434 / 1.520 |
| 1610 ball screw direct | 480 | .90 | .379 / .488 / .868 / 3.041 |
| 20-tooth 3-mm belt pulley, 4.8:1 reduction | 384 | .90 total | .474 / .609 / 1.085 / 3.801 |

These exclude rotating inertia. Four 16-mm-diameter, 200-mm-long steel cylinders plus an assumed `2.8e-5 kg m²` motor rotor add 0.069 Nm at 800 mm/s² with 5-mm lead, or 0.103 Nm including the same 1.5 factor. The cylinder envelope overstates thread-root inertia; pulleys, couplings and bearing/seal drag add real terms. The rotor value comes from the older vendor datasheet and is a labelled sensitivity input, not a verified current revision specification.

The selected *comparison motor* is StepperOnline 23HS30-2804S, current page $18.26, 57×57×76.5 mm, 2.8 A/phase, advertised 2.00 Nm holding torque. **Holding torque alone is not the drive justification.** Its older primary torque curve, measured with DM542T, 36/48 V and 2.69 A RMS, gives visually approximately 1.6 Nm at 300 rpm, 1.3 Nm at 600 rpm, and about 0.8 Nm at 960 rpm on the 36-V curve; the 48-V curve is higher near 960 rpm. The current page notes parameter adjustments and links an updated curve. The older directly retrievable curve is used as a conservative family comparison, not a guaranteed acceptance curve for a delivered motor.

For the nominal .1-N/site case, the 1605 calculation gives about **.537 Nm including estimated rotational acceleration**, below the older ~.8-Nm characteristic at 960 rpm. At .5 N/site it gives ~1.62 Nm and fails this comparison. TR8×8 at .1 N/site also fails this motor comparison. Thermal duty, resonance, actual friction, supply wiring, and minimum delivered torque remain unqualified.

Motor speed is plausible, but the lift cannot traverse every small increment at constant 80 mm/s. With the stated acceleration, a 5-mm pulse is triangular and takes **.1581 s**, reaching only63.25 mm/s; 40-mm and50-mm standalone strokes take .600 and .725 s. Engagement, mask writing, checks and settling are additional. These are drive kinematics only, not scene times.

## Construction provision and stopped support

A conservative realizable bank uses four external 1605 screws, one at each corner, with ballnuts mounted to a stiff ladder/platen carrying the moving dogs; each screw has a fixed thrust-bearing block and floating radial support. A shared toothed belt synchronizes their phase. Use separate vertical guides and adjustable nut mounts; do not force screw straightness to serve as terrain-platen guidance. Provide accessible coplanarity adjustment and accommodate small parallelism error so four screws do not bind. The short stroke does not make alignment free.

Four ordinary ballnuts and bearing blocks need perimeter room outside the dense active cells. The vendor starts at 200-mm overall screw length, so a catalog build has at least that vertical envelope before caps, top guides and supporting structure. A custom shorter screw is possible but adds machining/quotation, not a free compactness assumption. The 76.5-mm motor can mount horizontally through belt transmission; allow its 57-mm cross-section and shaft clearance outside the pin field.

An efficient ball screw or belt is backdrivable. **No self-locking claim is permitted.** A normally engaged axis brake or positive catch must carry the moving platen and any pins whose ground locks are currently released upon loss of power. Holding current is insufficient. The supported shutdown sequence is: maintain moving-dog capture, return every released terrain site to its grounded pawl, verify the commanded mechanical grounding state, then withdraw drive dogs. The independent axis catch remains necessary during the transfer interval or interrupted sequence. Counterbalance can reduce drive load but does not replace positive support because the selected terrain load changes.

Descending a loaded bank can regenerate energy into the drive bus. The nominal 40-mm descent releases about4.53 J of gravitational energy before friction. Provide braking/clamping or an adequately qualified drive/bus; a generic switching supply is not an energy sink. End stops and pin retention must withstand an interrupted step without allowing neighboring terrain to drop.

For the alternative belt lift, a 3-mm pitch20T pulley has60-mm pitch circumference and19.1-mm pitch diameter;4.8:1 reduction can be two stages20:40 and20:48. This is a **geometric example**, not a rated belt selection. At .1 N/site each of four vertical legs needs at least123 N design differential tension before preload and unequal loading; the .5 case needs430 N. A6-mm printer belt is not presumed adequate. Select rated belt width, teeth in mesh, minimum pulley and shaft bearings from a manufacturer's power/tension tables. Initial installation tension is not maximum working load.

## Price and stock provenance

USD catalog pages inspected2026-10-14, excluding shipping/tax; purchase is neither requested nor made. Low/high totals combine anchors and clearly separate allowances. The $42.95 screw price is the displayed family price; selected200-mm length/options have not been checked in a cart. BF/BK supports were out of stock, and the supply was preorder, so these are replaceable procurement anchors rather than a ready order.

| Per bank item | Count | Low total $ | High total $ | Basis |
|---|---:|---:|---:|---|
| NEMA23 motor +DM542T | 1+1 |37.91|37.91|Primary catalog|
| 36-V approximately200-W supply |1|19.96|35.00|Catalog low/preorder, high allowance|
|1605 screw+ballnut|4|171.80|220.00|Family catalog low, high allowance|
|BF12/BK12 support pairs|4|67.20|88.00|Catalog low/out of stock|
|Ballnut mounting blocks|4|39.80|56.00|Catalog low; integrated plate could substitute|
|Synchronization belt/pulleys/idlers|1 set|35|70|Unquoted provision|
|Independent vertical guides|1 set|30|70|Unquoted provision|
|Brake/positive catch and release|1|20|60|Unquoted, unconstructed|
|Mounts/leveling/fastener stock|1 set|20|50|Unquoted provision|
|Axis wiring/limit/fusing|1 set|10|25|Unquoted provision|
|**Total**||**451.67**|**711.91**|Not a supplier quote|

Sources:

- [Motor and current downloadable files](https://www.omc-stepperonline.com/nema-23-bipolar-1-8deg-1-9nm-269oz-in-2-8a-3-2v-57x57x76mm-4-wires-23hs30-2804s).
- [Directly retrieved primary torque/speed curve](https://www.omc-stepperonline.com/download/23HS30-2804S_Torque_Curve.pdf), [older full datasheet](https://www.omc-stepperonline.com/download/23HS30-2804S.pdf). The graph itself was visually inspected, not inferred from holding torque.
- [DM542T driver](https://www.omc-stepperonline.com/digital-stepper-driver-1-0-4-2a-20-50vdc-for-nema-17-23-24-stepper-motor-dm542t), current page $19.65.
- [Mornsun36-V supply](https://www.omc-stepperonline.com/200w-36v-5-9a-90-132vac-180-264vac-switching-power-supply-lm200-20b36r2), $19.96 preorder. The apparently cheaper [S-150-36](https://www.omc-stepperonline.com/150w-36v-4-17a-115-230v-switching-power-supply-stepper-motor-cnc-router-kits-s-150-36) has minimum quantity10 and preorder status, so its $14.40 headline is not a two-bank purchase basis.
- [Zyltech1605 screw](https://www.zyltech.com/zyltech-16mm-1605-antibacklash-ball-screw-w-ballnut-pre-cut-lengths-200mm-1300mm/):5-mm pitch,16-mm diameter, maximum stated axial clearance.1mm; precision assertion is vendor-provided, not measured here.
- [ZyltechBF/BK support pair](https://www.zyltech.com/zyltech-bf12-bk12-end-support-bearing-block/), $16.80 and related DSG16H block $9.95.
- [Gates light power and precision design manual](https://www.gates.com/content/dam/gates/home/knowledge-center/resource-library/catalogs/light-power-and-precision-manual.pdf), selection reference only; no belt part or rating claimed.

## Resident mask: independent dimensional challenge

A supplied an integration concept with a3×2.4-mm terrain stem and an84-mm-tall memory gate,0.8-mm thick inX and4.2-mm wide inY. GateX occupies3.4..4.2mm between adjacent stems, it moves1.6mm inY to write and2mm inZ to unlatch, and a continuous1.2-mm reader slot spans the50-mm movement range. The A reader travels with the lift; the B release reader is fixed atZ3.5mm. This avoids a long compression rod but introduces a thin load-bearing gate and a moving-reader-to-fixed-gate interface.

With only end supports, `I=4.2*.8^3/12=.1792 mm^4`, assumed PLA `E=3000 N/mm²` and simply supported span84mm, transverse deflection is **22.97 mm per newton** at midspan. Even.3 N blocked-reader force produces~6.9mm. Slots make the actual gate less stiff. This estimate disproves an unsupported-panel implementation; it is not a material failure qualification.

Rigid backing must restrict the local unsupported span, while allowing both write motions and the reader to pass. Solid-section10/15/20-mm spans give.039/.131/.310mm per N respectively. An actual slotted panel is less stiff and needs contact/FEA or coupon verification. The backstop must carry an OFF reader force directly into a grounded or moving frame; a nearby decorative wall is insufficient if its own contact/clearance is not specified.

Count the new parts/interfaces explicitly:4096 tall gate slides;4096 retention pockets/detents;4096 A passage/blocked-face contacts;4096 local cam-block guides and dog couplings;4096 B bridge guides plus ground-pawl contacts;backing channels with clearance for both mask motions;row unlock tabs;column programming followers;and sliding A read-frame interfaces throughout the stroke. Combining parts into combs reduces assembly count, not the number of friction-sensitive interfaces. With4096 gates, one minute of individual fitting still adds68.3h. Do not substitute the data-actuator count for the repeated-site count: two banks of 64 data actuators mean 128 expensive data actuators, while passive memory remains 4096 sites.

The above is a review of explicit dimensions communicated by A. Actual final CAD intersections, support continuity and manufactured clearances must be reviewed once the files exist; do not label this paragraph a completed collision check. The next decision-changing test should measure cumulative blocked-reader deflection and gate write friction in at least neighboring ON/OFF cells, not merely demonstrate that one free flag slides.
