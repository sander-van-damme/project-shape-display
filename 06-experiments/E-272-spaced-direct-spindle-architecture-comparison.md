---
status: complete
builds-on: [E-271, E-267, E-270]
---

# Spaced direct spindles: simpler hardware, smaller useful updates

**One-square spindle spacing removes E-271's inter-channel transmission conflict without changing the resident screw pairs. It does not preserve the sixteen-output head's local-reveal speed.** Retain a direct spindle as a mechanism/door-change control; do not select a multi-spindle machine or refine its docking hardware from this screen.

Reproduce `python3 tools/curated-experiment-checks/E-272/direct.py --check`; omit the flag for full ledgers/workloads. Evidence: finite envelopes, constructive schedules and catalog-plus-assumption economics; self-reviewed, not physical qualification. No print, purchase, safe RPM or cap decoder is established.

## Changed construction and full-scale obligations

Compare 1, 2, 4 and 8 direct encoder spindles arranged 1×1, 2×1, 2×2 and 4×2. Compact centers are **25.4 mm apart**, four coarse cells or five reference cells. A common XY carriage traverses the board; every spindle has its own 3-mm docking slide and reversible motor. The motor, short coupler and tip move together. This removes sixteen belts, 32 pulleys, long bearing risers and staggered motor lanes; it does **not** remove selective docking. Raising the whole head would touch unchanged screws and is excluded.

Each channel reserves a **22×24×89-mm swept carrier/harness box**, plus a 3-mm-diameter direct tip/shaft. The conservative catalog motor box remains 16×16×33 mm with a 3×9-mm output shaft. Independent ±0.2-mm box-face errors leave **1.0 mm** between adjacent Y carriers; ±0.4 leaves 0.6 mm. These correlated/adverse bounds are not printer distributions. At pin pitch the carriers collide; wider spindle spacing provides the escape.

Non-tip hardware ends below z=−7; resident socket plane is z=0. Parked tip ends at −1 and selected tip at +2 mm. At ±0.2 error: 0.6-mm parked gap, 1.6-mm insertion; adjacent 4.4-mm socket envelopes leave 2.25/0.98 mm at coarse/fine pitch. Internal fit, socket phase, runout, loaded bending and resonance remain unqualified.

Four/eight-spindle head reservations are 59.4×59.4×116 and 110.2×59.4×116 mm, excluding the resident stack above. Swept machine reservations are approximately 434–435×494–495 mm including a 60-mm electronics/harness side tray, before enclosure/limits. The tray accommodates up to four dual-driver boards; brackets, heat clearance and cable chain remain unconstructed. A 6×4-mm per-channel cable-drop reservation behind the motor replaces E-271's marginal 3×4-mm drop: twelve assumed 0.8-mm-OD conductors at 50% packing need 12.06 mm² versus 24 allocated. Bends, moving slack, connector access and fatigue still require actual routing.

Sequence: verify every tip parked → seek → insert only selected tips → prove engagement → rotate signed distances independently → stop → retract → settle → obtain fresh, correctly identified actual-cap observations. Unknown docking inhibits rotation and travel. One recoverable wrong result may retry from its observed stable height; persistent faults, lost support or obscured caps stop the operation. Spring return is not a proven safe moving-disconnect response.

Resident support remains **pin→thread→screw collar→opaque bed→frame**, with keeper/frame reacting upward docking force. There is no writer load takeover, per-cell brake or extra pin marking. Each board still has **4,096/6,400 pin–screw pairs and socket/thrust sites**, 8,192/12,800 guide apertures, and the inherited 126/158 two-layer ribs. E-269's fine-grid frame and loaded keeper limitations remain.

Shared count at k outputs: k motors, selectors/returns, carriers, short couplers/tips and cable drops; 2k bushings, guide duties, stops and docking-switch duties; ceil(k/2) bridges. Up to 12k conductors/24k terminations before buses. Selector arithmetic is 5.5k W; catalog motor stall extrapolation is 1.5k A, not a supply rating. The bridge's default 1-A current limit and the selector's unqualified force/duty still constrain startup and docking.

Power off, park and secure the board before bench removal of the shared head. Use split plates and separable harnesses; resident pair repair retains E-269's unloaded/openable-bed procedure. Precision-machined/reamed shared plates and cut coupler stock are plausible alternatives to FDM carriers. Casting or molding these few parts requires tooling/release/shrinkage qualification; neither route removes repeated thread manufacture or hand cleanup.

## Conditional waits, including neutral preparation

Reuse the three sourced map windows and both physical depressions from E-267. They are a convenience sample, not a measured session distribution. S40 uses neutral20/depth20; S50 uses neutral30 with shallow20/deep30 presets. Both retain 20-mm walls. Compare 64² at 6.35-mm and 80² at 5.08-mm over 406.4 mm. A software origin never supplies negative travel.

Group changed cells by their coordinate residues modulo the spindle spacing, then greedily cover the resulting lattice with the spindle rectangle. Overlapping footprints do not select a cell twice; unchanged neighbors stay unselected. Choose the shorter of row- and column-serpentine station orders. This constructive schedule is not a route optimum. Simultaneous mixed signs require independent motors. Whole-carriage seek uses the inherited 200-mm/s, 5,000-mm/s² assumptions with at least 50 ms per station. A **0.38-s station transaction** allocates 0.08 docking/engagement, 0.10 retract, 0.10 settle and 0.10 simultaneous read; add inherited 4-s common handling and 1-s reader deployment. Rotation assumes 850 rpm, lead3 mm and 1,000 rev/s². None is rated hardware performance.

Charge one immediate full-stroke retry after known stable readback. Covered/broken/unknown results have no finite completion bound. E-270 rejected its tested image decoder; the read slot and cost below are conditional obligations, not a rescued optical system. Encoder turns cannot prove true cap height. Unchanged loaded neighbors still need mechanical isolation evidence; a successful changed-cap read does not inspect the whole board.

All entries below are seconds; paired entries are **S40 / S50**. All include the conditional read and one recoverable full-stroke retry.

|Grid / outputs|Four-square reveal max|Scene-transition max|Cold neutral preparation|Dense full-stroke stress|
|---|---:|---:|---:|---:|
|64² / 1|249.02 / 309.49|1782.29 / 2056.88|3842.33 / 4806.33|5769.86 / 6733.86|
|64² / 2|130.64 / 160.99|1046.93 / 1203.40|1926.11 / 2408.22|2889.87 / 3371.99|
|64² / 4|76.41 / 93.12|636.89 / 724.18|996.17 / 1237.34|1478.05 / 1719.23|
|64² / 8|46.25 / 55.66|433.18 / 492.24|502.64 / 623.35|743.58 / 864.29|
|80² / 1|380.80 / 475.15|2744.15 / 3173.80|5950.80 / 7456.91|8962.56 / 10468.68|
|80² / 2|197.07 / 244.37|1596.72 / 1840.48|2980.36 / 3733.53|4486.24 / 5239.41|
|80² / 4|113.26 / 139.37|954.22 / 1090.22|1530.77 / 1907.48|2283.71 / 2660.42|
|80² / 8|66.42 / 81.01|655.02 / 748.90|769.95 / 958.42|1146.42 / 1334.89|

The source separately charges neutral preparation, minimum-rest first-map writes and prep-plus-first-map totals. Ground must physically rise before downward relief is available. Known pre-positioning only removes initial seek. Dense stress is a separate diagnostic, not a30-s gate.

To avoid blaming an inefficient greedy cover, the source reports a favorable relaxation:

`T ≥ 5 + retry + sum(spin(abs(delta)/lead))/k + (.38+.05)*ceil(changed/k)`.

This grants perfect packing, no extra travel and parallel readback: a necessary bound **within the stopped transaction/rate model**, not a universal limit. Four-square windows are spatial tests, not a required reveal size.

Spread shared spindles span equal board regions. Independent carriages assign one spindle/XY to each1×1,2×1,2×2 (quadrants), or4×2 region. Both replay the same relief/local/preparation/minimum-rest/dense workloads. Independent heads start/return at regional upper-left corners; maximum regional time includes common deployment and one full-stroke retry once. Docking/readback remain per cell, granting k concurrent readers.

**Independent timings grant collision-free routing.** At a Y region boundary, adjacent targets leave carrier clearance `pitch−24−2e` = **−18.05/−19.32 mm** coarse/fine at e=.2; X gives−16.05/−17.32. Uncoordinated same-height carriages fail; coordination or changed routing remains unpaid. Even free resolution cannot beat the regional work bounds below. The synthetic16×16/30-mm quadrant patch alone needs184.33 s rotation. Cooperative mobile heads remain a different, unconstructed topology.

At eight compact outputs the worst coarse reveal is **46.25/55.66 s** for S40/S50; the best-case transaction bounds across the same windows are **35.61/43.37 s**. Fine-grid values are 66.42/81.01 s versus bounds52.07/64.07 s. Worst schedules/bounds can occur in different windows. Coarse S50 has79 of133 nonempty windows within30 s, versus45 of133 fine. These fractions describe this spatial sample, not the chance a player waits less than30 s.

Synthetic S50 single-cell20-mm changes take≤11.07 s. Thin one-square walls/two-square doors change4/8 coarse or5/10 fine cells: compact4/8 maxima13.97/15.50 s coarse/fine; serial fine ten-cell19.66 s. These are small command examples, not sampled play or relief restrictions. Coarse8 S50 local maxima850→400 rpm:55.66→87.65 s; lead2/400:118.15 s.

Spread eight-output S50 has307.45/473.12-s local maxima and653.84/1024.24-s scene maxima coarse/fine. Its distant outputs do not help a compact change. Compact eight's known pre-positioning only reduces the coarse S50 worst reveal to54.09 s. Its minimum-rest first-map maximum is744.29 s, versus929.47 s including paid neutral30 preparation followed by the first map. Preparation is not free merely because the later terrain moves downward.

E-270's sixteen-output coarse control has conditional S50 local28.84 s and scene253.98 s, with its decoder still rejected. The direct eight roughly doubles these constructed waits; in exchange it removes belt routing and halves channel count. Favorable bought allocation$1145.52 is only$101 below E-271's bare16 comparison, although$556 below encoder16. Bare16 still owes custom feedback and its own unqualified routing/force duties; neither is a product winner.

## Cost and decision

Checked 2026-10-13: [Pololu5180](https://www.pololu.com/product/5180) $32.45 each below five/$29.85 at eight; [4763 cable](https://www.pololu.com/product/4763) $3/$2.76 respectively; [Adafruit3297 dual bridge](https://www.adafruit.com/product/3297) $5.95; [2776 docking solenoid](https://www.adafruit.com/product/2776) $4.95 below ten. No-load RPM and extrapolated stall figures do not rate the threaded assembly.

Executable allocations/channel: coupler/tip/bushings $2.5–7; carrier/guides/stops/return $3–8; selector electronics $1–2; harness $1.5–4; switches $2–4. Shared plates, distribution, XY, chassis, protected supply, controller, resident structure, cap reader/mount and extra read paths($5–20/channel) are included. Landed10%+$20 /15%+$60. These unquoted scenarios are not guaranteed bounds or market floors. Extra carriage/span hardware is added below.

|Grid / outputs|Purchased USD low–high|Residual at $500 / $1000 / $1500, favorable only|Maker hours|
|---|---:|---|---:|
|64² / 1|639.60–1663.13|-139.60 / +360.40 / +860.40|17.27–39.26|
|64² / 2|712.64–1790.09|-212.64 / +287.36 / +787.36|17.44–39.76|
|64² / 4|865.26–2050.86|-365.26 / +134.74 / +634.74|17.77–40.76|
|64² / 8|1145.52–2546.25|-645.52 / -145.52 / +354.48|18.44–42.76|
|80² / 1|690.29–1875.10|-190.29 / +309.71 / +809.71|22.39–52.06|
|80² / 2|763.33–2002.06|-263.33 / +236.67 / +736.67|22.56–52.56|
|80² / 4|915.95–2262.82|-415.95 / +84.05 / +584.05|22.89–53.56|
|80² / 8|1196.21–2758.22|-696.21 / -196.21 / +303.79|23.56–55.56|

Printing material adds assumed$60–160; print time/yield/cleanup are unmeasured. Labor assumes8–20 s/pair,8–16 h common assembly/calibration,10–30 min/channel;2–4-day assembly is not established. Manufacturing discounts need real processes. Price tiers authorize no spending.

## Regional versus spread carriage comparison

Seconds, **S40 / S50**, at the same conditional rates/readback, granting collision-free independent travel.

|Independent spindles / grid|Local max|Scene max|Paid neutral prep|Dense stress|
|---|---:|---:|---:|---:|
|2 /64²|249.02 /309.49|898.45 /1055.86|1924.33 /2406.44|2888.09 /3370.21|
|4 /64²|246.98 /307.45|532.73 /645.67|965.83 /1207.01|1447.71 /1688.89|
|8 /64²|246.98 /307.45|459.17 /565.52|486.08 /606.78|727.02 /847.72|
|2 /80²|380.80 /475.15|1377.77 /1623.42|2978.57 /3731.74|4484.45 /5237.63|
|4 /80²|378.77 /473.12|828.81 /1005.99|1492.96 /1869.67|2245.90 /2622.61|
|8 /80²|378.77 /473.12|722.66 /889.25|749.65 /938.12|1126.12 /1314.59|

Independent1 reproduces serial. Independent2/4/8 local bounds:240.51/300.98 s coarse,372.24/466.59 fine. Extra regions cannot accelerate work confined to one region; distributed scenes can benefit.

Independent carriages add120–240 USD XY/limits plus20–60 USD control/service/harness and1–3 maker hours each. Counts:2k XY drives/limit duties, k rotary drives/docking slides; unchanged resident hardware. Spread heads add30–100 USD bridge,5–20 USD per extra spindle harness,1–3 h assembly. These unquoted allowances do not qualify collision resolution, stiffness or optical coverage.

|Coarse outputs|Independent purchased USD|Spread shared purchased USD|
|---|---:|---:|
|1|640–1663|640–1663|
|2|867–2135|751–1928|
|4|1327–3086|915–2235|
|8|2224–4961|1217–2822|

Fine-grid resident support adds50.69/211.97 USD to the low/high ends of each row. Four independent carriages cost1327 USD favorably but lose compact four's local concurrency; eight exceed2200 USD. Their modest preparation savings do not earn priority over localized play waits and collision resolution. This does not make30 s a universal gameplay gate.

**Disposition:** retain the spaced direct construction as a physically simpler, slower comparator and stop before multi-head detail. Small door commands do not establish acceptable larger-reveal or setup waits. The next useful independent discriminator is a changed shared drive/selection topology that groups adjacent cells without E-271's sixteen tiny belt routes, screened at complete-machine scale. Optional owner printing remains retired; no new question.

Checks replay all signed changed cells exactly once and preserve unselected commands; verify full reach, dense closed-form station/rotation counts, no-op and reversal invariance, a far-corner serial timing anchor, lower-bound consistency, envelope collision/failure witnesses, exact regional partition/critical-path and single-region anchors, and budget identities. These verify the declared model only.
