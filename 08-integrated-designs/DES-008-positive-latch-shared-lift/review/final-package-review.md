> Historical package review from 14 October. Its revision-2 memory overlap acceptance is **superseded**: fresh review found independent flag rotation invalidated that bound. The released revision-3 handoff uses captive shoulders, 83 nominal checks and an explicitly restricted planar screen; general tilt/tolerance qualification remains physical. See the current memory handoff and final disposition.

# F final independent package review

2026-10-14. Reviewed the DES-008 main report, research/source limits, manufacturing/cost report, stationary-pulse scheduler, saved timing results, and the small mechanical-memory coupon. This is an engineering review; no physical mechanism was tested.

## Decision first

**Accept the package as an honest, useful engineering handoff at a physical and manufacturing boundary. Do not accept it as a digitally completed Shape Display architecture.** The main report says this clearly and prominently. It identifies a stronger surviving hypothesis, preserves failed alternatives, supplies small decision-changing fabrication articles, and does not quietly mark timing, manufacturing, affordability, or D&D walls as passed.

The strongest remaining objection is the absence of an integrated resident mask-to-dog/ground-pawl mechanism at the intended pitch. Two working coupons would support further development; they would not establish that those interfaces coexist, scale to 4,096 cells, fit the budget, or operate at the modeled rates. That obligation is correctly stated near the recommendation.

The mechanical-memory article's nominal 0.3 mm restraint overlap requires a clearer tolerance/handling qualification. The current loose short guides and uncaptured code bars do not guarantee that overlap. This is not a reason to discard the 5–6 g experiment, but it must be explicit in its handoff and observations.

## Central claims checked

- The report preserves the independently reproduced DES-007 68.93 s finite-strip result and distinguishes the favorable eight-head 29.38 s endless-loop comparator from constructed hardware. The selector count and cost are not hidden.
- The stationary two-bank result is labeled conditional. The saved principal results agree with the main table: 64²/40 mm is 20.817 s and 64²/50 mm is 22.907 s at the assumed 80 ms dirty-row cycle. Those numbers do not qualify physical row speed.
- The full-row sequential-decoder comparison is more defensible for the proposed mechanical writer: 24.497/24.747 s at 64² and 28.337/28.587 s at 80². The report prominently records that all four fail at 120 ms/row.
- For the 64²/40-mm full-scan worst case, the ledger independently checks as `4 + 160×0.08 + 4×0.4 + 2.359839 + (32×0.08 + 1.177460) = 24.497298 s`. The total row-cycle coefficient including the retry is 192; therefore the fixed-plan break-even is `(30 − 4 − 1.6 − 2.359839 − 1.177460)/192 = 108.66 ms`. This checks arithmetic, not the hardware rates or mask validity.
- The finer-height dense stress failure and neutral-plus-first-scene penalty are stated beside the timing claim. Initial known-zero state is distinguished from unqualified commissioning of unknown physical heights.
- I ran `analysis/check_timing_independent.py`; its independent replay matched the three published stopped-retirement extrema and preserved the slower corrected two-key cases. That script does not independently prove the global-platen hardware.
- The catalog anchor recomputes to `128×3.96 + 16×13.46 + 8×(14+6.95) = $889.84`. After the listed minimal common allocations, `$208.89` remains under $1,500, or `$0.0510/site`. The report correctly calls these allowances and necessary bounds, not a delivered manufacturing quote.
- The 704 W / 140.8 A peak coil reference, uncertain board current path, inadequate price-anchor motor rating, and missing site fabrication costs are disclosed. A slow low-hold-current change could alter both power and timing and is not silently credited.
- The wall equation is correct: equal centered walls leave `25.4 − t` mm. In particular, 0.8 mm walls cannot admit a 25 mm base, and no positive-thickness centered walls admit a 25.4 mm base at the nominal 25.4 mm center spacing. This is appropriately a distinct product constraint, not “fixed” by pin resolution.
- The physical short-thread observations remain correctly scoped; they are not repurposed as evidence for rack handoff or compact-array yield.

## Memory-coupon overlap: nominal does not mean guaranteed

The source geometry has a 0.5 mm idle gap between the top lug and the code channel, a 0.8 mm foot engagement, and therefore 0.3 mm nominal overlap. Code-bar old-state alignment is necessary before row acquisition. The coupon deliberately has manual code-bar hold-down and loose vertical row guides.

The guide-post diameter is 2.4 mm and cassette-hole diameter 2.9 mm, over approximately 2.2 mm guide length. Their 0.5 mm diametral clearance is not itself a vertical error; it permits angular motion. A simple local upper estimate is

`theta_guide = atan(0.5 / 2.2) = 12.80°`.

For roll across the flag's 2.4 mm depth, a conservative condition that retains full-face acquisition before full-face foot release is

`overlap(theta) = 5.2 cos(theta) − 2.4 sin(theta) − 4.9 mm`.

Here 5.2 mm is flag bottom-to-top height, 2.4 mm is its depth, and 4.9 mm is code-channel underside minus fixed floor height. This produces:

| Roll | Conservative overlap |
|---:|---:|
| 0° | 0.300 mm |
| 3° | 0.167 mm |
| 5° | 0.071 mm |
| 6° | 0.021 mm |
| 6.40° | approximately zero |
| 7° | −0.031 mm |
| 12.80° | −0.361 mm |

This is a conservative contact-envelope sensitivity, not a complete contact simulation. Partial corner engagement can remain after this full-face criterion fails, but that is not robust retained acquisition and may bind. The short guides do not forbid the problematic roll. A code bar lifting upward by 0.3 mm independently consumes the entire nominal overlap. Print-height error and lug/foot variation consume more.

Therefore the coupon handoff should require the operator to keep the row level and code bars seated, observe acquisition from the side, stop on bar lift or forced fit, and record any temporary free state or binding. The test is meant to learn whether that contact transition survives actual parts; CAD does not guarantee it. It should not be called a fully captive mechanism.

A straightforward follow-up, if measured roll is the problem, is approximately 10 mm guide sleeves at the cassette ends with corresponding taller posts, outside the code-bar lanes. The same angular estimate falls to 2.86°, leaving about 0.17 mm nominal full-face overlap before print variation or bar lift. This adds less than 1 g in a plausible section, but needs revised meshes and slicing; I did not alter the reviewed files. Positive vertical code-bar guides would still be required for a powered version.

The root engineer reports PrusaSlicer 2.7.4 with 0.16 mm layers, three walls, 100% PLA infill and 1 mm brim: **5.71 g and 1 h 2 min 13 s**, without the low-adhesion warning present without brim. Record that as a slicer estimate and retain the exact profile. It supersedes my earlier unsliced 25–50 minute allowance. A READY file handoff does not constitute physical success, and no powered row rate or terrain coupling should be attached to it.

## Small clarity changes recommended

1. Use the **full-row-scan 109/107 ms limits** as the primary sequential-decoder performance gate. The faster dirty-row figures are valid computational comparators only if the address travel needed to skip a row is demonstrated inside their allowance. The main report already makes this distinction; retain it in the final user summary.
2. Describe the scheduler's retry as **one-mask-plus-pulse time reserve**, not a qualified recovery sequence. The code comment says it does not assume stale knowledge, but this mechanical RAM requires known OLD bits. If old state is uncertain, a safe reset mechanism and its time remain missing. The main report mostly says this already; changing that comment avoids overstating what the reserve proves.
3. `cost-and-manufacture.md` begins with the superseded traveling-head comparison and reaches the selected global architecture later. Add a short initial pointer or reorder for navigation, so a reader cannot mistake the $1.55–6.33k head allocations for a quoted complete global-lift BOM. Preserve the historical accounting rather than silently replacing it.
4. Keep “computationally demonstrated” attached to **ideal selection logic / arithmetic**. Neither nominal CSG checks nor the pulse replay establishes elastic neighbor isolation or positive engagement after printing.

## Next obligations in priority order

1. **Physical support handoff and isolated writing:** measure the two small articles, including their failures. For memory, preserve the OLD-to-NEW acquisition and unselected-row witness checks. For the rack article, the other reviewer is covering detailed geometry; this review does not duplicate it.
2. **Integrated resident module:** combine one stored bit, both A/B read interfaces, one captured moving dog, one fixed grounded pawl, and the relative-Z guide. Prove that selection remains load-free while both support paths transfer in order. Include an unchanged adjacent site and the actual module depth.
3. **Measured row cycle and writer load:** demonstrate OLD data positioning, row acquisition, NEW data positioning, retained lowering, row indexing and necessary settling inside roughly 109 ms for the 64²/40-mm sequential-decoder comparison. Separately measure data-bar force, current and temperature. Failure here changes the timing/cost decision.
4. **A quoteable repeated module and aggregate force:** count every manufactured part, flexure, sliding contact and assembly touch. Measure guide drag and release/capture force before sizing the global platen, transmission and motors. The current five-cent/site remainder is a warning that present affordability is unsupported.
5. **An accepted playable wall/base interface:** actual base dimensions plus a traversable corridor mockup must resolve the failed centered-wall geometry. A manual or automatic wall subsystem must be counted explicitly if selected.

Do not order or print a full display on the present evidence. Do not claim the mission has reached a complete affordable playable architecture. The justified outcome is the strongest surviving conditional option, explicit reasons alternatives were rejected, and small reproducible tests that can change that option's ranking.

## Revision-2 closure of the memory-fixture objection

The original short-guide/manual-bar-hold critique above is retained as review history and is **superseded by revision 2** of the coupon. The engineer repaired the fixture before release: 10 mm guide sleeves and taller posts, 1.6 mm pocket engagement, 2.2 mm row lift, and two removable keeper bridges retained by four printed transverse keys. Code bars now have positive vertical restraint without an operator holding them down. No purchased hardware was added.

The revised nominal overlap is 1.1 mm. Under explicit measured limits—diametral post/hole gap ≤0.8 mm, effective guide length ≥9.8 mm, flag height ≥5.9 mm, seated floor-to-channel gap ≤5.0 mm, and total code-bar upward play ≤0.5 mm—the conservative full-face overlap is **0.185 mm**. These bounds must be checked on physical parts; there is still no print-process or dynamic qualification. The keyed keepers' nominal combined vertical play is 0.4 mm. Keys are manually removable and must remain fully inserted; vibration retention is outside this unloaded experiment.

All nineteen revised plate bodies are watertight. The solid PLA estimate is 8.77 g on an 82.6 × 84.6 mm plate. Fifty-five nominal CSG cases show zero positive-volume interference, including keeper/key mounting and code-bar travel. Wrong-OLD acquisition remains deliberately blocked. The first revision-2 print orientation produced an unexpected 21.916 mm longitudinal code-channel bridge in PrusaSlicer. The code bars were subsequently inverted onto their closed roofs, removing that channel bridge; keeper/key-hole bridges remain subject to final slice review. The old 5.71 g / 1 h 2 min 13 s slice is not valid for revision 2.

Revision-2 source SHA-256: `80246e82ec166ce477299631ef8a16f19ef190b57f531d691c06d6fa4881f67b`. The source, STLs, 55-case proof, bounded tolerance calculation, dimensioned PNG/PDF, and updated handoff are in `work/mission/F-matrix/`.

**Disposition:** the actionable fixture defects have been addressed in CAD; accept the revised coupon for final slicer/fabrication handoff with explicit measured acceptance limits. The earlier overall package decision remains unchanged: useful conditional architecture and physical boundary, not a completed affordable/playable full-machine design.

The final orientation-only correction preserves the assembly geometry, all 55 nominal collision checks, and the bounded overlap result. Code bars now print with channels upward on their closed roofs. The earlier upright revision-2 slice (9.10 g / 1 h 41 min 44 s) is provisional and superseded; use the new slice. Final source SHA-256: `80246e82ec166ce477299631ef8a16f19ef190b57f531d691c06d6fa4881f67b`.
