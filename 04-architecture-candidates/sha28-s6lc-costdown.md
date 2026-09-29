# SHA-28 S6-LC-GR cost-down: global-reset elimination within the viable S6-LC lane

> Companion verdict: `07-evidence-and-decisions/sha28-s6lc-costdown-verdict.md`.
> Scope: SHA-28 S6-LC exploitation only. NOT A1 hardening, NOT broad divergent screen.
> Baseline: corrected S6-LC $226.77 purchased / $263.05 delivered (DND-98), mission PASS on G5.
> Evidence class: CALCULATION over `08-integrated-designs/s6lc-low-cost/analysis/s6lc.py` + CAD constants. No print/purchase/measurement (DND-27).

## Mechanism description (delta vs S6-LC)

S6-LC-GR = S6-LC with ONE change: replace the **travelling reset carriage** (motor + rail + cable chain + 8 staggered bank combs tripped serially) with a **single global release comb plate** actuated by platen overtravel (one extra 0.5 s lift-to-release dwell at the bottom datum).

- Delete purchased: reset carriage stepper ($8), carriage rail + frame ($20), cable chain ($8), 1 driver channel ($1.59).
- Delete printed/moving: travelling carriage frame, rail mounts, cable routing, 8 independent comb actuators.
- Add purchased: $0 (global comb is printed, excluded per DND-70; stiffening ribs are printed).
- 8 bank combs merge into one global plate printed as 8 sub-tiles on the existing splice scheme (same M3 assortment line).

This is enabled by NEW evidence since banking was introduced: the DND-97 A2 correction (leaf 0.45 mm, 0.020 N/cell, not 0.160). Banking existed to bound the OLD 1025 N unbanked force. Corrected unbanked force is **128 N**, which fits the existing load path with margin (see verdict note).

## Operating principle

Reset = platen drives 2 mm below datum; a printed lost-motion fork lifts ALL pawl toes at once; columns fall by gravity to datum; platen returns. Write path unchanged (4 global broadcast strokes + punched-card mask). Regional update = global reset + masked rewrite of all banks (untouched banks replay their stored masks; no tile disturbance beyond the existing platen stroke).

## Expected component count

- Bought actuators: 3 → **2** (lift NEMA23 + mask small stepper).
- Bought driver channels: 3 → **2**.
- Moving axes: lift + mask + travelling carriage → **lift + mask**.
- Printed parts: −1 carriage + rail mounts + chain guides; combs 8 separate → 1 plate in 8 spliced sub-tiles (net fewer distinct parts).

## Purchased parts (BOM delta, working BOM basis)

| Change | Delta purchased |
|---|---:|
| − Reset carriage motor | −$8.00 |
| − Reset carriage rail + frame | −$20.00 |
| − Cable chain / strain relief | −$8.00 |
| − 1× driver channel (3×$1.59 → 2×$1.59) | −$1.59 |
| + Global comb stiffener (printed, excluded) | +$0.00 |
| **Total** | **−$37.59** |
| **New purchased** | **$189.18** (was $226.77) |
| **New delivered (×1.16)** | **$219.45** (was $263.05) |

Headroom to $250 purchased: $23.23 → **$60.82**. Gap to A1 $181: $45.77 → **$8.18**. Delivered convention ($250) now PASSES by $30.55.

## Printed material / print complexity

- PLA/X1C baseline unchanged. Global plate reuses the bank-comb tooth section (1.6×0.88 mm, CAD) — no new thin features.
- Assembly SIMPLER: no 406 mm rail alignment, no moving-cable service loop, no per-bank comb timing. One fork + one plate vs carriage + 8 trips.
- Risk added: global plate flatness over 406 mm (same splice scheme as frame; recorded unknown, coupon-measurable).

## Estimated cost — see table above. No other lines repriced.

## Expected update speed

- Old: 4 strokes (3.4 s) + mask index (1.0 s) + traverse 7×0.508 (3.556 s) + 8 resets (4.0 s) = **11.96 s**.
- New: 3.4 + 1.0 + 0 traverse + 1×0.5 global reset = **4.9 s**. Margin to 30 s: **25.1 s**.
- Regional (one bank changed): global reset + full masked rewrite ≈ 4.9 s (slower than bank-local 1.35 s, still < 30 s). Recorded trade, not a gate failure.

## Local-update behavior

Bank-local replay (no full reset) is REPLACED by global-reset + selective rewrite. Untouched cells see one extra drop+rewrite cycle (wear + time cost) but end at the same heights; no new disturbance mode beyond the existing platen stroke.

## Reliability / durability / compactness / assembly / scalability

- Zero-silent: UNCHANGED (S6-LC has no per-cell feedback before or after; G8 remains measurement-only via coupon C1). Proposal adds no new silent mode; correlated mode IMPROVES (one fewer motor/driver/cable to fail).
- Lift margin with added reset load: (2560+128)=2688 N → 1.71 Nm vs 2.2 Nm → margin **1.29** (was 1.35). Passes.
- Comb teeth: 0.020 N vs 5.16 N/tooth limit → 258× per-tooth margin; global plate limit scales with teeth (see verdict).
- Durability: global fork cycles 1×/map instead of carriage 8 trips/map — fewer sliding cycles. Plate splice fatigue is the new watch item (coupon).
- Compactness: strictly smaller (no carriage overtravel, no chain bend radius).
- Scalability: reset cost O(1) per map regardless of bank count — scales BETTER than banked traverse.

## Requirement coverage

| Requirement | S6-LC-GR |
|---|---|
| 80×80, 5.08 mm, 40 mm, 5 heights | unchanged (same cell/pawl/mask) |
| Full map < 30 s | 4.9 s PASS |
| Regional update | global-reset+rewrite 4.9 s PASS (slower, recorded) |
| <$250 purchased | $189.18 PASS (+$60.82) |
| $250 delivered convention | $219.45 PASS (was FAIL) |
| Zero-silent frame | unchanged G8-open (coupon C1 path, same as baseline) |
| Power-off hold | unchanged (P1 latch) |
| X1C+PLA | unchanged, simpler |

## Key unknowns

1. Global plate stiffness/flatness over 406 mm as-printed (splice scheme reuse — coupon).
2. Overtravel fork force repeatability (printed cam — coupon).
3. Regional rewrite wear (extra cycles on untouched cells — bounded by 4.9 s/map budget, measurement-only).

## Proposed experiments (cheapest first, none executed — analysis kills cost first)

- E-A (calc, DONE here): force/torque/timing/BOM re-derivation from `s6lc.py` constants.
- E-B (coupon, handoff): 80 mm comb section + fork: measure release force spread + flatness (same C1 rig, no new hardware).
- E-C (coupon): full-width splice flatness over 406 mm (caliper/straightedge).

## Kill criteria vs A1 ($181 to beat)

- KC-cost: must reach ≤ $181 purchased to obsolete A1 on cost. GR reaches $189.18 — closes 82% of the gap, does NOT yet beat A1. Residual $8.18 needs a second cut (e.g. mask-mechanism simplification) — named follow-up, not claimed here.
- KC-rate: full map must stay < 30 s → 4.9 s passes.
- KC-silent: must not add silent cells vs baseline → unchanged (G8-open both).
- Verdict on THIS proposal: PASS as cost-down (mission + delivered gates green, simpler print), FAIL as A1-beater (still $8.18 above). Recorded honestly.
