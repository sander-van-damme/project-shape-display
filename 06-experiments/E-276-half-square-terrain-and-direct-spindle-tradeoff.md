---
status: complete
builds-on: [E-257, E-258, E-272, E-275]
---

# Half-square terrain reduces work but cannot inherit small-stem guidance

**Retain 12.7-mm pitch as a conditional, lower-part-count alternative; do not select the enlarged-cap/same-stem embodiment.** A 32×32 board has 1,024 threaded pairs versus 4,096/6,400. The existing independently driven, 25.4-mm-spaced direct head can address it without the parked rack/band/friction couplings. But simply widening tops while retaining 4.4-mm square stems and 4.64-mm guides permits a nominal adjacent-cap collision. A naive coarse wall conversion also closes a known doorway to half a game square. Protecting the opening is possible by changing wall geometry; this is not automatically acceptable gameplay.

Reproduce `python3 tools/curated-experiment-checks/E-276/coarse.py --check`; omit `--check` for tables; `--figure /path/comparison.svg` exports the comparison. Source uses standard Python plus inherited NumPy. Evidence is **semantic rasterization, finite geometry, calculated schedules and explicitly unquoted allocations**. Self-review; no physical qualification, price refresh, preferred pitch, print or purchase.

## Play geometry before timing

All three grids cover 406.4×406.4 mm: 16×16 one-inch game squares. Rerasterize E-254's original semantic polygons; do not downsample the old height arrays. Retain physical river banks and ravine, their E-258 depth presets, and the connected-wall conversion from E-257. These three annotated maps and overlapping four-square windows remain a convenience sample, not observed player workloads. The optional visual/prop workflow and solid bridge's inability to support under-bridge play remain unresolved.

| Geometric quantity | 80² / 5.08 mm | 64² / 6.35 mm | 32² / 12.7 mm |
|---|---:|---:|---:|
| Connected wall cells | 589 | 343 | 145 |
| Raw / connected wall components | 15 / 9 | 24 / 8 | 16 / 6 |
| Inspected thin wall | 5.08 mm | 6.35 mm | 12.70 mm |
| Southern opening, inherited conversion | 25.40 mm | 25.40 mm | **12.70 mm** |
| Southern opening, protected corridor | 30.48 mm | 31.75 mm | **38.10 mm** |
| Wall cells cleared by protection | 1 | 1 | 3 |
| Inspected river ford | 40.64 mm | 38.10 mm | 25.40 mm |
| Inspected bridge | 50.80 mm | 50.80 mm | 50.80 mm |
| Whole game squares at intended ruin ground /234 | 144 | 163 | 170 |
| Whole game squares at intended river ground /164 | 136 | 137 | 145 |
| Whole game squares at intended ravine ground /173 | 155 | 155 | 163 |

The footprint denominators use the same continuous source-square centers. Coarse apparent support gains partly reflect changed boundaries. At half-square pitch, five additional coplanar ruin squares are actually raised rather than at intended ground, so they are excluded; coplanarity alone is insufficient. No continuous footprint calculation proves real base stability.

Probe coordinates are E-257's retained source coordinates. They are cross-sections, not minimum widths along entire routes. Component counts flag changes without proving which joins are correct. A 25.4-mm opening has zero room for a 25.4-mm base's placement error; a 32-mm illustrative base cannot fit. Grid-aligned clear widths accommodating 32 mm are at least 35.56/38.10/38.10 mm, before real tolerances. The 32-mm value is a scenario, not a new miniature requirement.

The protected alternative declares a source-coordinate rectangle **x449..484, y350..415** through the already inspected southern doorway. Its physical width is 25.4 mm and length 47.17 mm. Polygon clipping confirms zero positive-area intersection with any retained source wall or rubble polygon. Clear every raster cell with positive-area overlap with this rectangle, after wall conversion. At 32² this removes wall cells (19,21), (19,22), (21,22), widening the measured opening to 38.1 mm while retaining six components. Source geometry is clear, but coarse cell footprints erase additional wall ends: this is a representation trade, not lossless repair. Other openings and wall mergers remain unchecked. The executable additionally counts whole game squares remaining at their source-intended ground height; it does not mistake any coplanar raised wall for a safe ground square.

## A new mechanical consequence of coarse pitch

Hold core thread, 4.4-mm stem, 4.64-mm guide opening and support topology fixed to avoid claiming unqualified scaled threads. Near-continuous tops of width `pitch−0.4 mm` give 4.68/5.95/12.30-mm square caps. The 0.4-mm gap is an explicit geometry assumption, not a qualified print clearance.

At **±3° yaw**, a centered 4.4-mm stem spans only **4.62425 mm** and fits the nominal guide. Two adjacent coplanar caps with opposite yaw have exact separating-axis gaps **+0.1613/+0.0966/−0.2266 mm** at fine/quarter/half-square pitch. The negative half-square gap is a finite polygon-overlap witness, not a probability of actual jamming. All cap separating axes overlap; the result is independently checked against the analytic projection. The screw can accommodate small pin yaw with an associated thread-height change; differing resident phases can place the two caps at equal height. No added antirotation restraint has been constructed.

Half-square caps require opposite yaw below **1.895°** even with centered perfect parts. The core guide permits the 3° witness; manufacturing/translation/warp would add uncertainty. Do not tighten 1,024 fits to rescue it or declare the earlier smaller caps qualified. Wider guide/stem geometry, a different top shape/gap, or a changed common guide is a substantive new construction with stock, friction and support costs. No such remedy is granted here.

Bare 4.4-mm tops cover only **12.0%** of half-square cell area, versus 48.0/75.0% at quarter/fine pitch: deleting wide tops is not a continuous tabletop. Cap overhang beyond the stem becomes **3.95 mm** versus .775/.140. An illustrative .1-N edge load creates .615/.298/.234 Nmm about the stem center, not a measured miniature load or a rated bending calculation. Total projected cap area is **1549/1450/1402 cm²** at half/quarter/fine pitch; a hypothetical 1-mm solid cap layer alone occupies 154.9/145.0/140.2 cm³. Fewer cores do not proportionally reduce surface material; cap stiffness, mass and neighbor motion require new evidence. The footprint-support calculations grant continuous cell coverage and do not qualify cap gaps, rocking or load sharing.

## Conditional architecture, waits and economics

Keep E-272's independently selected direct spindles on one XY carriage at 25.4-mm spacing: 1, 4 (2×2), or 8 (4×2). Finite head envelopes and 3-mm docking stroke are unchanged; no new tiny belts or sliding shared torque couplings are granted. Wide tops live above the guides and require the separate collision check above. The positive underside socket does not require E-275's torque-proportional friction squeeze, but insertion phase, engagement force, screw lift within keeper float, and safe moving disconnect remain unqualified.

Resident support is pin → thread → screw collar → opaque bed → frame throughout selection and motion. Unchanged screws are not commanded; actual accidental contact, frame motion and loaded-neighbor disturbance still require qualification. Unknown engagement inhibits rotation/XY motion. After stop/retract/settle, fresh identified actual-height readback is required; retry uses the actual stable height. Covered, stale, wrong-cell or persistent-fault readings stop completion. A motor encoder cannot certify true terrain height, and a spring return cannot establish safe arrest after power loss.

Timing preserves 850 rpm, lead3, 1000 rev/s², XY200 mm/s and5000 mm/s², 50-ms minimum station seek, **.38-s station transaction** (.08 dock, .10 retract, .10 settle, .10 read), 5-s common handling/reader deployment and one full-stroke retry. These are conditional allocations, not measured wait times or a revived optical-decoder pass. S40 has ground20/depth20, wall+20; S50 has ground30/depth20 or30, wall+20. Paid neutral means physically moving all columns from minimum, not changing a software zero. No homing, prop/miniature handling or art preparation time is newly qualified.

Seconds below are **S40 / S50**, using the inherited wall conversion. Protected-passage local maxima are identical because the worst reveal is a ravine; protected full-scene maxima fall by only .47 s.

| Grid / direct outputs | Four-square reveal max | Scene max | Paid neutral | Minimum-rest first map | Dense full-stroke stress |
|---|---:|---:|---:|---:|---:|
| 32² / 1 | 71.33 / 86.62 | 475.07 / 543.54 | 999.78 / 1240.96 | 1079.08 / 1320.25 | 1481.67 / 1722.84 |
| 32² / 4 | **26.84 / 31.07** | 201.24 / 222.88 | 271.15 / 331.62 | 321.50 / 381.97 | 391.62 / 452.09 |
| 32² / 8 | **18.46 / 20.81** | 142.47 / 157.53 | 140.10 / 170.45 | 180.57 / 210.92 | 200.34 / 230.69 |
| 64² / 4 | 76.41 / 93.12 | 636.89 / 724.18 | 996.17 / 1237.34 | 1132.64 / 1373.82 | 1478.05 / 1719.23 |
| 64² / 8 | 46.25 / 55.66 | 433.18 / 492.24 | 502.64 / 623.35 | 623.58 / 744.29 | 743.58 / 864.29 |
| 80² / 4 | 113.26 / 139.37 | 954.22 / 1090.22 | 1530.77 / 1907.48 | 1752.65 / 2129.36 | 2283.71 / 2660.42 |
| 80² / 8 | 66.42 / 81.01 | 655.02 / 748.90 | 769.95 / 958.42 | 966.66 / 1155.13 | 1146.42 / 1334.89 |

For half-square/four/S50, worst reveal lowers63 cells, leaves961 unchanged, visits8 rows and17 stations: 4.236 seek +1.564 return +12.241 spin +6.46 transaction +1.571 retry +5 common = **31.071 s**. Paid neutral plus first map is465.74 s; the direct minimum-rest first map is381.97 s. The difference is actual preparation, not free hidden work. Its ideal-packing transaction lower bound is24.79 s, so31.07 is not a universal impossibility theorem. At400 rpm the protected S50 local maximum becomes45.85 s; lead2 at850 rpm gives37.66 s. No safe RPM or measured lead is selected. Thirty seconds remains a comparison, and dense stress is separate.

Use E-272's **2026-10-13 dated catalog entries unchanged**, plus its explicitly unquoted allocations; these are not current quotes or guaranteed bounds. Shared hardware dominates, so cutting 75% of quarter-square pairs saves only about$68 in the favorable same-head purchased allocation. Enlarged caps/guide remedies are not included as implemented hardware.

| Grid / outputs | Bought USD low–high | Maker hours low–high |
|---|---:|---:|
| 32² / 1 | 572–1381 | 10.44–22.19 |
| 32² / 4 | **798–1768** | **10.94–23.69** |
| 32² / 8 | **1078–2264** | **11.61–25.69** |
| 64² / 4 | 865–2051 | 17.77–40.76 |
| 64² / 8 | 1146–2546 | 18.44–42.76 |
| 80² / 4 | 916–2263 | 22.89–53.56 |
| 80² / 8 | 1196–2758 | 23.56–55.56 |

Half-square/four remains$298 above the$500 bought reference; its favorable residuals under$1000/$1500 are$202/$702. Eight outputs exceed$1000 favorably and leave$422 under$1500. The high allocations exceed both tiers; none authorizes spending or proves consumer value. Printing material retains the inherited$60–160 scenario; printing time, scrap and cap cleanup are not measured. Labor assumes8–20 s/pair,8–16 h common assembly/calibration and10–30 min/channel, excluding unresolved cleanup. Another minute of individual fitting still adds17.1 h at1024 pairs, versus68.3/106.7 h at4096/6400. Fewer cells help but do not license hand fitting.

Board repetition falls to1024 each of pins, screws, threads, sockets, collar/thrust/keeper sites;2048 guide apertures;62 two-layer row ribs (versus8192/12800 apertures and126/158 ribs). Each32-cell row has32 pairs; an illustrative8×8 region has64. Count antirotation, friction, wear and service duties even when molded into one part. Head duties at k outputs remain k motors/encoders/selectors/returns/carriers/couplers,2k bushings/guide/stop/docking-switch duties,ceil(k/2) bridges,12k conductors/24k terminations before buses and two XY drives. No private resident cartridge/brake is added.

FDM batch fixtures, split/unscrewing molds, machined or formed screw stock and precision shared head plates remain possible routes, not qualified yields or quotes. Wider caps must be integrated with the earlier support-removal/orientation constraints; E-263's retired print is not revived. Use openable shared beds for intact pair replacement after unloading/parking; broken/bent pairs can still require module access. Retain individual service rather than scrapping a sealed region. Fewer ribs/sites do not prove frame stiffness or repair access.

## Decision boundary

The topology change reduces threads, assembly touches and work per reveal; it does not cure docking, passive holding variability, E-270's rejected optical decoder or covered-pin uncertainty. Retain the half-square direct-spindle comparison as a lower-count control, with explicit passage and cap costs. Stop before new shaft/guide/selector detail. A useful subsequent discriminator is a coarse terrain-column construction whose tops cannot collide under its admitted guidance motion, with a batch-manufacture route and unchanged-neighbor support; compare it with retaining narrower cells. This is not a recommendation to print or a reason to reopen E-273–275.
