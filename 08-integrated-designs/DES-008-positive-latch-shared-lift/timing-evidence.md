# Timing evidence and workload limits

## Final support-transfer correction

Use the corrected values in this section for the dimensioned resident study. The older tables below are retained comparisons using 0.3-mm take-up/seating; they do not represent its final forced-seating sequence. The new independent model uses 0.4-mm take-up, the signed main stroke, ground restoration, then 0.7-mm downward seating and 0.3-mm upward centring **for both signs**. It includes acceleration for each motion. Each pulse, including the time-reserve pulse, adds 0.0659915 s over the earlier ledger. Restoring ground before completing seating is essential for mixed freely following and sticky outputs.

| Corrected category, seconds | 64² / 40 mm | 64² / 50 mm | 80² / 40 mm | 80² / 50 mm |
|---|---:|---:|---:|---:|
| Worst sampled scene | 24.83 | 25.08 | 28.67 | 28.92 |
| Known-zero first scene | 21.27 | 21.52 | 24.47 | 24.72 |
| Neutral preparation + first scene | 31.89 | 38.99 | 36.37 | 44.75 |
| Sustained cycle mean | 23.56 | 23.73 | 27.19 | 27.35 |
| Local reveal maximum | 17.47 | 17.72 | 20.03 | 20.28 |
| Dense full level alphabet | 38.76 | 39.52 | 45.16 | 45.92 |

Complete-row limits for the 30-second scene benchmark are **106.94 / 105.64 ms** at 64² and **85.55 / 84.51 ms** at 80². All four fail at 120 ms. This remains conditional arithmetic: the paired writer, micro slides, complete row decoder, force-limited seating and checks have not met these rates physically. The [independent audit](review/revised-system.md) records exact ledgers, interval reasoning, failed earlier sequences and source hashes; reproduce [revised-system-results.json](analysis/revised-system-results.json). The dimensioned guide embodiment also has a separately reported admitted-play collision, so timing feasibility is not integrated mechanical feasibility.

## Earlier timing comparisons — retained as baseline

The reproducible models retain the E-254/E-258 semantic workload lineage. The inherited 50-mm suite includes three shallow/deep map families, 36 directed scene/neutral cases, 384 two-by-two-square reveals, cold starts, neutral preparation and dense controls. This is a hand-annotated workload sample, **not measured gameplay frequency or a validated percentile**. Its full-pitch wall encodings also do not pass the separate corridor requirement.

The separate 40-mm suite uses neutral 20 mm, a 20-mm ravine and +20-mm walls. It sacrifices 10 mm of depth relative to the deepest inherited interpretation. That is an explicit comparison, not a software offset that creates extra stroke. The finer 5-mm state capability is stressed separately; the sampled scenes mostly use 10-mm increments.

The stationary two-bank calculation includes dirty-row rewrites and final mask clearing, five 80-ms support/check events per pulse, 0.3-mm unload and seating motions, 80 mm/s and 800 mm/s² lift motion, empty returns, one complete mask/pulse retry and four seconds of common preparation/checking. These are assumptions. A mask write accounts for all writer and row-decoder motions; no free carriage translation or buffered preparation is credited.

| Grid / physical travel / 5-mm levels | Worst sampled scene, 80 ms/row | At 120 ms/row | Maximum row-write allowance for every sampled scene to stay within 30 s |
|---|---:|---:|---:|
| 64² / 40 mm | 20.82 s | 26.66 s | 142.9 ms |
| 64² / 50 mm | 22.91 s | 29.67 s | 122.0 ms |
| 80² / 40 mm | 23.86 s | 31.22 s | 113.4 ms |
| 80² / 50 mm | 26.35 s | 34.83 s | 97.2 ms |

These numbers establish a timing budget worth testing. They **do not establish a 30-second playable machine**. Physical mask timing, lift drag, support seating and any required checks may exceed the allowances. Wall/miniature handling and any manual preparation are additional. The retry allowance is a one-mask-plus-pulse **time reserve**, not a qualified recovery sequence; uncertain OLD memory still needs a supported reset with unestablished time. The generated timing results report initial scenes, neutral preparation, local reveals, sustained transitions and dense multi-level stress separately; dense patterns are not hidden in the favorable scene maximum.

**The more defensible row-decoder comparison scans all rows every mask**, rather than assuming skipped rows cost no address travel. At 80 ms per complete row, the scene maxima become **24.50 / 24.75 s** at 64², and **28.34 / 28.59 s** at 80², for 40 / 50 mm. All four fail at 120 ms. The allowed complete cycle tightens to approximately **109 / 107 ms** at 64² and **87 / 86 ms** at 80². Use these limits for a sequential mechanical decoder. The faster table above requires a decoder whose skip behavior is actually included in its row-cycle allowance.

For the dirty-row 64²/80-ms comparator, the category ledger is:

| Category | 40-mm encoding | 50-mm encoding |
|---|---:|---:|
| Known-zero directly to first scene, maximum | 19.73 s | 21.26 s |
| Prepare neutral, then first scene, maximum | 29.87 s | **31.57 s** |
| Sustained scene cycle, mean | 19.56 s | 21.12 s |
| Local reveal, maximum | 11.11 s | 11.12 s |
| Dense complete level-alphabet stress | **38.16 s** | **38.93 s** |

These are separate results, not exceptions concealed by the scene table. Unknown physical initial heights still require a commissioning procedure; its duration is not established by the known-zero case.

For contrast, eight stop-indexed writer positions span 44.45 mm. At 4,000 mm/s², seven 6.35-mm indexed moves already take 0.558 s before writing. Calling that a 0.1–0.2 s mask would require a physically different continuous writer. Independent rescheduling also found that retiring-subset masks do not directly describe the two-key remaining-active mechanism. Both corrected variants still fail the benchmark; see the independent audit.


## Primary sequential-decoder category results

These scan every row for every mask, including unchanged rows. Assumed complete row cycle is 80 ms. Timing reserves are not qualified recovery after unknown OLD memory. Reproduce `full_scan_category_ledgers` in [timing-results.json](analysis/timing-results.json).

| Category, seconds | 64² / 40 mm | 64² / 50 mm | 80² / 40 mm | 80² / 50 mm |
|---|---:|---:|---:|---:|
| Worst sampled scene transition | 24.50 | 24.75 | 28.34 | 28.59 |
| Known-zero first scene | 21.01 | 21.26 | 24.21 | 24.46 |
| Neutral preparation plus first scene | **31.56** | **38.53** | **36.04** | **44.29** |
| Sustained cycle mean, deep where applicable | 23.25 | 23.42 | 26.88 | 27.04 |
| Local reveal maximum | 17.27 | 17.52 | 19.83 | 20.08 |
| Dense uniform lift | 17.77 | 21.26 | 20.33 | 24.46 |
| Dense opposite signed movement | 25.25 | **32.22** | 29.09 | **37.34** |
| Dense full level alphabet | **38.16** | **38.93** | **44.56** | **45.33** |

A resident writer scans large masks even for a small reveal; this explains why its local update is not nearly instantaneous. An address-skipping decoder can improve that result only if its complete actual traversal is included. Commissioning from unknown physical heights and manual wall handling remain outside these known-state calculations.
