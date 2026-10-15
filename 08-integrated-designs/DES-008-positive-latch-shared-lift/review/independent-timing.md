# Independent timing verification and matrix interface boundary

2026-10-14. Purpose: check the consequential timing conclusions without merely rerunning the original schedule, identify mismatches between the simulated selector and the explicit two-key mechanism, and bound the remaining resident-matrix interface.

Reproduce: `python3 08-integrated-designs/DES-008-positive-latch-shared-lift/analysis/check_timing_independent.py`. This separately implements the acceleration-limited travel law, bank scheduling, mask persistence, changed-address enumeration and pin-state replay. It imports the shared workload module only to obtain the existing workload arrays and pulse candidates, **not its scheduler or motion function**. Results are in [timing-audit-results.json](../analysis/timing-audit-results.json). No physical rates were measured.

## Verdict

The original arithmetic is reproduced. The eight-bank reusable serial selector is decisively too slow for the30s objective under its declared rates. Its published26.33s sixteen-bank result is an optimistic selector abstraction requiring512 electrical writers, not a qualified complete machine. Explicit mechanical operation scenarios increase that result to29.19–38.71s and leave no useful qualification margin. No typo or missing40mm pulse rescues the architecture.

The final package should classify these as **conditional simulations**, with the actual A/B reader interfaces unresolved. They are sufficient to reject the studied embodiment as the leading inexpensive architecture; they are not universal lower bounds on all mechanical multiplexing.

## Independent arithmetic reconstruction

For distance d, speed limit v and acceleration a, a triangular move takes `2 sqrt(d/a)` when the implied peak speed does not exceed v. Otherwise acceleration/deceleration consumes `2v/a` and cruise distance is `d−v²/a`. This derives the same duration as C's alternate expression.

I rebuilt every row and bank for all nine40mm scene transitions. The source's critical case is64×64 pins, eight banks/eight writers per bank, and `road → ruins`:

| Ledger item | Independently reconstructed seconds |
|---|---:|
| Common preparation/check allowance |4.000000|
| Row seeking |0.910897|
| Mask programming |25.790998|
| Abstract support events |9.200000|
| Loaded terrain motion |6.650000|
|0.3mm take-up/seating microtravel |2.788548|
| Empty returns |5.150000|
| Row/writer homing |0.607458|
| One longest-row retry |7.223538|
| Total |**62.321440**|

The critical bank has8visited rows,14direction admissions,29retirements,43masks and218changed-address visits. Thus the support ledger is exactly `(14×2 +29×3)×0.08 =9.20s`. The independent program also reproduces48.384330s for continuous full-mask writing and26.326176s for16banks/32writers.

## Physical-model mismatch: retirement masks

C-retirement explicitly says it models a three-state passive lane. Its threshold mask selects **the outputs retiring at that threshold**. The two-key reader/keeper mechanism developed in A instead requires the **outputs remaining active**: its reader holds those keys ON while a common keeper opens and retiring keys spring-return OFF.

These masks have different changed-address histories. Replacing mask semantics while retaining the original compressed support allowances gives66.752263s at B8W8 and25.914298s at B16W32. This is not a correction to the hypothetical three-state algorithm; it is the appropriate model for the actual binary two-key interface. It also changes the worst transition.

## Unpacked reader/keeper operations

An A or B key exchange requires the following ordered motions:

1. Reader advances through ONholes and takes the relevant key load.
2. Common keeper withdraws.
3. Keys reach their intended endpoint under reader/return force.
4. Keeper seats and is checked.
5. Reader withdraws clear of the flag.

There are four commanded strokes, plus key settling/checking, per key exchange. A and B exchanges cannot be merged into a single unsequenced event: capture/take-up must precede ground release; ground reseating/loading must precede dog withdrawal.

The source's2×80ms admission and3×80ms retirement are aggregate allowances. They are not demonstrated to contain this sequence. As an explicit **fast scenario**, use6mm reader stroke (2mm gate thickness +3mm key travel +1mm approach/gap),0.6mm keeper stroke, reader200mm/s, keeper100mm/s, both8000mm/s², and10ms key-settle/check per exchange. One exchange costs0.154641s. Admission uses two exchanges; retirement uses two plus20ms terrain seating check (the separate0.3mm terrain motion remains in its existing ledger).

| Explicit2key schedule | B8W8 | B16W32 |
|---|---:|---:|
| Original compressed support allowances |66.75s|25.91s|
| Fast dimensioned reader/keeper scenario |**71.94s**|**29.19s**|
| Four80ms strokes per key, eight per A/B operation |86.59s|38.71s|

None of these scenarios qualifies a real spring, keeper, cam or motor. The fast scenario is particularly favorable: very short checked pauses, no retry beyond one row, no long reader-compliance oscillation, no proof that the common keeper seats across64mixed keys, no force-dependent loss of speed, and no jam recovery. Simultaneous movements may reduce some time only with a constructed cam sequence preserving support overlap.

## Global reset versus per-flag bidirectional writing

C's changed-address mode assumes a writer can set either0or1 locally. A's simplest coupon writer setsON after a common reset; these are different transactions. A local reset cam followed by conditional setting could eventually provide bidirectional logical writing with one electrical selector, but its stroke/dwell is not implemented.

A global reset is not necessarily slower. It clears many bits in parallel, so only addresses containing new ONbits need visits. An independently modeled variant uses the binary remain-active masks, two1.8mm common reset strokes at100mm/s and4000mm/s² when previous flags containONbits, and the fast explicit A/B operations above. Its worst B8W8 case is **60.799841s**, with183address visits. This is faster than the71.94s bidirectional local-writing variant but still decisively misses30s. Both alternatives should be distinguished rather than claiming one universally dominates.

## Workload and pulse coverage checks

The40mm scene suite contains three inherited maps:

* Ruins heights20/30/40mm.
* Road heights10/20/30mm.
* Ravine heights0/20/30mm.

There are six directed map-to-map transitions and three neutral-to-map transitions. These are actual generator workloads, but they do not exercise all5mm heights. The source's5mm/9level results must not be described as dense9level scene testing merely because the algorithm's quantum is5mm.

C-combs allows repeated pulse denominations. Therefore the apparent `(5,10,20)` list does **not** exclude40mm:20+20 achieves it. Independent subset enumeration confirms all5mm increments through40mm are covered by the four-pulse set5,5,10,20. Through50mm,5,10,20,20 covers all increments. All2mm increments through40mm are covered by2,4,8,10,16. The source searches the smallest pulse count first and then motion cost; it is a constrained scheduling heuristic, not a proof of global time optimality over all pulse codes.

A separate64×64stress field containing all positive and negative5mm differences gives176.635887s under the original B8W8 retirement abstraction and180.708026s under the explicit fast binary-key variant. This is a dense stress case, not a prediction of ordinary scene interruption. It demonstrates why a nine-level arbitrary-height claim must include distinct-level retirement cost.

Other accounting limits:

* The retirement microtravel assumes0.3mm take-up/seating; actual clearance may differ.
* The programmed40mm upper endpoint can temporarily require40.3mm mechanical travel during take-up/overtravel. Useful range is not the same as total hard-stop range.
* Empty reset is charged as the nominal largest displacement, not the final signed0.3mm offset. For upward phases this can omit~3.75ms at80mm/s; downward phases can overcharge the same amount. This is immaterial to the conclusion but should be specified before detailed trajectory control.
* Mask programming is serialized with motion. Pipelining may help only when both keys are mechanically retained and reader rods are withdrawn. It cannot be granted to an arbitrary selector abstraction.
* All nine scene pairs and all dense replayed outputs finish at their targets in the independent ideal state replay; unchanged ideal columns never change. This is logical support scheduling, not elastic contact validation.

## Resident matrix: finite programming transaction

A mechanically enabled row cassette may carry flags in hard OFF/ONpockets. The selected row rises into column U-channels while other rows remain below them. That does not make old-state acquisition free. Before a row rises, each column setter must align to that row's existing flag position. Only then can the row engage the forks without forcing bits. The transaction is:

`set column channels to old row bits → raise row cassette → move columns to new row bits → lower row cassette`.

This requires two data moves plus rowup/down. If an alternative fork captures both bit positions without prepositioning, it needs the actual wide-entry/closing/capture geometry and resulting stroke. No50ms row-programming claim should silently omit old-state acquisition.

## Main remaining boundary: memory is not terrain capture

A2×2row/column memory coupon can prove arbitrary bit programming and disabled-row isolation. It cannot prove the global terrain platen. Each selected terrain column still needs:

1. Positive bidirectional dog capture.
2. An independent take-up movement unloading its ground pawl.
3. Selective withdrawal of that ground pawl at fixed frame height.
4. Retained dog engagement throughout terrain Ztravel.
5. Ground-pawl reseating and transfer before dog withdrawal.

A binary flag directly equated with `ground released = NOT dog engaged` has a gap at switching and is unacceptable. The two functions need sequenced overlap. The resident version must count capture and release followers, guides, flags and long engagement tracks across every site, not just4096memorybits.

### Bounded two-common-frame escape

For a **fixed mask during each whole pulse**, separate common A and B frames could read the same resident flag at different stages. A engages selected dogs and remains mechanically held; a0.3mm platen take-up unloads ground pawls; B selectively releases those pawls at fixedZ and remains held while the platen moves. At the endpoint B restores the original pawls, terrain seats, and A withdraws unloaded dogs. Flags are rewritten only after all terrain is grounded. This avoids private key keepers because common frames remain physically held, unlike the overlapping writer/retirement architecture.

A positive vertical slot/C-channel can keep a dog laterally captured while it slides inZ. It needs approximately useful40mmstroke plus capture/overtravel margin (at least43mmprovisionally), actual opposed walls and fixed-frame reactions. A spring merely pressing a beveled dog is not equivalent. B's fixed-height release follower must remain engaged independently of platenZ. One selected flag must admit both common read paths while OFFbypasses both; finite clearance and backing are mandatory.

The topology is not logically impossible, but its tileable section is **unconstructed**. At6.35mmpitch a5.6mmfull-width column leaves only0.75mm total lateral gap. A robust dog, release follower and command flag cannot all be casually drawn beside it in one plane. A narrower stem, staggeredZplanes or enlarged internal spacing needs explicit packaging. A4096site design implies at least4096capture interfaces and4096release interfaces in addition to memory and resident supports, even when common actuators replace their private keepers.

For scale, even an assumed0.05N guide/release drag per selected site sums to205N if all4096sites move. A1N/site dynamic design load would imply4096N at the platen before losses. These are load scenarios, not measured demands; they show why a few successful low-load memory cells cannot qualify a full force path. The selected common-frame interface and its minimum multi-pin loaded test are the genuine next physical/geometry boundary.
