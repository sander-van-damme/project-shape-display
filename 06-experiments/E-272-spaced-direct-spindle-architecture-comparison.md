---
status: complete
builds-on: [E-271, E-267, E-270]
---

# Spaced direct spindles: simpler hardware, smaller useful updates

**One-square spindle spacing removes E-271's inter-channel transmission conflict without changing the resident screw pairs. It does not preserve the sixteen-output head's local-reveal speed.** Retain a direct spindle as a mechanism/door-change control; do not select a multi-spindle machine or refine its docking hardware from this screen. The remaining advantage is fewer shared mechanisms, not a qualified product.

Reproduce `python3 tools/curated-experiment-checks/E-272/direct.py --check`; omit the flag for the complete ledgers and workloads. Evidence is conservative finite envelopes, constructive scheduling and catalog-plus-assumption economics. Self-review is not independent validation or physical qualification. No print, purchase, safe RPM or actual-cap decoder is established.

## Changed construction and full-scale obligations

Compare 1, 2, 4 and 8 direct encoder spindles arranged 1×1, 2×1, 2×2 and 4×2. Compact centers are **25.4 mm apart**, four coarse cells or five reference cells. A common XY carriage traverses the board; every spindle has its own 3-mm docking slide and reversible motor. The motor, short coupler and tip move together. This removes sixteen belts, 32 pulleys, long bearing risers and staggered motor lanes; it does **not** remove selective docking. Raising the whole head would touch unchanged screws and is excluded.

Each channel reserves a **22×24×89-mm swept carrier/harness box**, plus a 3-mm-diameter direct tip/shaft. The conservative catalog motor box remains 16×16×33 mm with a 3×9-mm output shaft. Independent ±0.2-mm box-face errors leave **1.0 mm** between adjacent Y carriers; ±0.4 leaves 0.6 mm. These correlated/adverse bounds are not printer distributions. At the original pin spacing the same carriers collide at both pitches. Thus the escape is *spindle spacing*, not thinner motor housings.

Non-tip hardware ends below z=−7; resident socket plane is z=0. Parked tip ends at −1 and selected tip at +2 mm. At ±0.2 error: 0.6-mm parked gap, 1.6-mm insertion; adjacent 4.4-mm socket envelopes leave 2.25/0.98 mm at coarse/fine pitch. Internal coupler, bearing and torque-contact geometry is reserved, not constructed. No self-centering or socket-phase tolerance is inferred. Radial runout, loaded bending and structural resonance are unmodeled.

Four/eight-spindle head reservations are 59.4×59.4×116 and 110.2×59.4×116 mm, excluding the resident stack above. Swept machine reservations are approximately 434–435×494–495 mm including a 60-mm electronics/harness side tray, before enclosure/limits. The tray accommodates up to four dual-driver boards; brackets, heat clearance and cable chain remain unconstructed. A 6×4-mm per-channel cable-drop reservation behind the motor replaces E-271's marginal 3×4-mm drop: twelve assumed 0.8-mm-OD conductors at 50% packing need 12.06 mm² versus 24 allocated. Bends, moving slack, connector access and fatigue still require actual routing.

Sequence: verify every tip parked → seek → insert only selected tips → prove engagement → rotate signed distances independently → stop → retract → settle → obtain fresh, correctly identified actual-cap observations. Unknown docking inhibits rotation and travel. One recoverable wrong result may retry from its observed stable height; persistent faults, lost support or obscured caps stop the operation. Spring return is not a proven safe moving-disconnect response.

Resident support remains **pin→thread→screw collar→opaque bed→frame**, with keeper/frame reacting upward docking force. There is no writer load takeover, per-cell brake or extra pin marking. Each board still has **4,096/6,400 pin–screw pairs and socket/thrust sites**, 8,192/12,800 guide apertures, and the inherited 126/158 two-layer ribs. E-269's fine-grid frame and loaded keeper limitations remain. Clear head envelopes do not qualify that resident structure.

Shared count at k outputs: k motors, selectors/returns, carriers, short couplers/tips and cable drops; 2k bushings, guide duties, stops and docking-switch duties; ceil(k/2) bridges. Up to 12k conductors/24k terminations before buses. Selector arithmetic is 5.5k W; catalog motor stall extrapolation is 1.5k A, not a supply rating. The bridge's default 1-A current limit and the selector's unqualified force/duty still constrain startup and docking. A lighter direct carrier helps only if its measured mass/friction fits the force budget.

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

Cold-neutral preparation is paid separately. The source also reports minimum-rest first-map writes and neutral-preparation-plus-first-map totals. Minimum rest reaches the same final absolute surface directly but cannot support later downward terrain without actually raising the ordinary ground. Known pre-positioning only subtracts the initial seek; it cannot erase rotation or stopped transactions. Dense stress remains a separate diagnostic, not a 30-s product gate.

To avoid blaming an inefficient greedy cover, the source reports a favorable relaxation:

`T ≥ 5 + retry + sum(spin(abs(delta)/lead))/k + (.38+.05)*ceil(changed/k)`.

It grants perfect packing of changed cells into k outputs, no extra travel and full parallel readback. This is a necessary bound **within this stopped transaction/rate model**, not a universal screw-machine limit. A faster real transaction or different addressing topology would change it. The four-square windows are spatial tests, not a claim that every reveal must contain that many changed cells.

A spread arrangement spaces shared-carriage spindles across equal board regions; it is also replayed, with finite mutual clearance. It sacrifices concurrency for clustered updates. Separate independent quadrant carriages cannot remedy a reveal entirely inside one quadrant: even granting free routing, a synthetic 16×16 patch lowered30 mm requires **184.33 s of rotation** on its one direct spindle at850 rpm/lead3. Additional rails, boundary-crossing collisions and independent optical paths would cost more. Stop this dedicated-quadrant option before detailed routing; mobile cooperative heads are a different, unconstructed topology.

At eight compact outputs the worst coarse reveal is **46.25/55.66 s** for S40/S50; the best-case transaction bounds across the same windows are **35.61/43.37 s**. Fine-grid values are 66.42/81.01 s versus bounds52.07/64.07 s. The windows giving worst schedules and worst bounds need not be the same. Coarse S50 has79 of133 nonempty windows within30 s, versus45 of133 fine. These fractions describe this spatial sample, not the chance a player waits less than30 s.

A synthetic single-cell20-mm change takes up to11.07 s atS50, while a one-square thin wall or two-square door changes4/8 coarse or5/10 fine cells. With four/eight compact outputs their maxima are13.97 s coarse and15.50 s fine; the single spindle's fine ten-cell case takes19.66 s. These are bounded *small command examples*, not sampled game actions or a proposed restriction on physical relief. At eight coarse outputs, reducing assumed speed850→400 rpm changes the S50 four-square maximum55.66→87.65 s; lead2 at400 gives118.15 s. No faster operating speed is earned here.

Spread eight-output S50 has307.45/473.12-s local maxima and653.84/1024.24-s scene maxima coarse/fine. Its distant outputs do not help a compact change. Compact eight's known pre-positioning only reduces the coarse S50 worst reveal to54.09 s. Its minimum-rest first-map maximum is744.29 s, versus929.47 s including paid neutral30 preparation followed by the first map. Preparation is not free merely because the later terrain moves downward.

E-270's sixteen-output coarse control has conditional S50 local28.84 s and scene253.98 s, with its decoder still rejected. The direct eight roughly doubles these constructed waits; in exchange it removes belt routing and halves channel count. Favorable bought allocation$1145.52 is only$101 below E-271's bare16 comparison, although$556 below encoder16. Bare16 still owes custom feedback and its own unqualified routing/force duties; neither is a product winner.

## Cost and decision

Checked 2026-10-13: [Pololu5180](https://www.pololu.com/product/5180) $32.45 each below five/$29.85 at eight; [4763 cable](https://www.pololu.com/product/4763) $3/$2.76 respectively; [Adafruit3297 dual bridge](https://www.adafruit.com/product/3297) $5.95; [2776 docking solenoid](https://www.adafruit.com/product/2776) $4.95 below ten. No-load RPM and extrapolated stall figures do not rate the threaded assembly.

The executable ledger itemizes every allocation. Per channel: short coupler/tip/two bushings $2.5–7; carrier/guides/stops/return $3–8; selector electronics $1–2; harness $1.5–4; two switches $2–4. Shared plates, distribution, XY, chassis, supply/protection, controller, resident structure, actual-cap reader and its mounting are separately included. Extra simultaneous reader paths receive $5–20 each beyond the first, **unquoted and unqualified**. Landed allowances are 10%+$20 /15%+$60; these scenarios are not guaranteed bounds or market price floors. Spread-carriage extra span and independent-carriage hardware are not included in the compact-head allocation.

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

Printing adds $60–160 of assumed material, with print time, yield and support cleanup unmeasured. Inherited 8–20 s handling/pair, 8–16 h shared build/calibration and 10–30 min/channel expose the maker-time range in the source; two-to-four-day assembly is not established. Quoting or molding threads would need a real manufacturing route, not a discount multiplier. No price tier authorizes spending.

**Disposition:** retain the spaced direct construction as a physically simpler, slower comparator and stop before multi-head detail. Small synthetic door changes are a distinct use case; accepting their latency does not imply accepting minutes for larger reveals or initial setup. The next useful independent discriminator is a changed shared drive/selection topology that groups adjacent cells without E-271's sixteen tiny belt routes, screened at complete-machine scale. Repeated schedule tuning, extra stereo margin sweeps and thinner risers cannot close the present gap. Optional owner printing remains retired; no renewed question is necessary for this bounded comparison.

Checks replay all signed changed cells exactly once and preserve unselected commands; verify full reach, dense closed-form station/rotation counts, no-op and reversal invariance, a far-corner serial timing anchor, lower-bound consistency, envelope collision/failure witnesses and budget identities. These verify the declared model only.
