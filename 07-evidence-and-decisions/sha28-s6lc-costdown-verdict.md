# SHA-28 verdict — S6-LC-GR global-reset cost-down: ADOPT as cost-down, NOT as A1-beater

> Status: screen COMPLETE. ONE cost-down proposal within the viable S6-LC lane, carried from
> concept to quantified BOM delta + print impact + gate re-derivation. Falsification-first:
> cheapest analysis (calculation over `s6lc.py` constants) before any CAD/BOM/procurement.
> Evidence class: CALCULATION. DND-27: no print, purchase, or measurement.
> Sketch: `04-architecture-candidates/sha28-s6lc-costdown.md`.
> S5-R, A1, S6-LC packages untouched (no model edits; this note + sketch only).
> Reproduce: `python3 -c` block in §2 (constants from
> `08-integrated-designs/s6lc-low-cost/analysis/s6lc.py`).

## Kill criteria (up front)

| ID | Gate | Kill line |
|---|---|---|
| KC1 cost-down | purchased must fall vs $226.77 with G5 green | no fall or G5 red kills |
| KC2 rate | full map < 30 s incl. reset/traverse | ≥ 30 s kills |
| KC3 silent | must not add silent cells vs baseline | new silent mode kills |
| KC4 lift | lift margin must stay > 1.0 with added reset load | ≤ 1.0 kills |
| KC5 A1-beat | purchased ≤ $181 to obsolete A1 on cost | > $181 = cost-down only, not A1-beater |

## 1. Why banking existed, and why the A2 correction reopens it

Banking (8×800) was sized when per-cell release was modelled as 0.160 N → unbanked 1025 N,
which exceeded the comb structural limit and forced staggered resets + travelling carriage.
DND-97 corrected the leaf to 0.45 mm → 0.020 N/cell → banked 16 N, unbanked **128 N**.
The carriage ($36 + driver) now hauls a 16 N load with a 15.7×-oversized motor — the
elimination target. This is new evidence addressing the old kill criterion (not re-litigation).

## 2. Binding re-derivation (numbers that decide it)

```
k = 3*1500*(1.2*0.45^3/12)/8^3 = 0.0801 N/mm; f = k*0.25 = 0.0200 N
banked = 16.0 N; unbanked = 128.1 N
lift base: T(2560 N) = 1.6297 Nm, margin 2.2/1.63 = 1.35 (matches s6lc.py)
lift+global: T(2688 N) = 1.7113 Nm, margin = 1.29 > 1.0 → KC4 PASS
per-tooth: 0.020 vs 5.163 N limit → 258× → KC3/G2 PASS (no new physics)
timing: 3.4 (strokes) + 1.0 (mask) + 0 (traverse deleted) + 0.5 (1× global) = 4.9 s → KC2 PASS
BOM: 226.77 − (8.00 + 20.00 + 8.00 + 1.59) = 189.18 purchased; ×1.16 = 219.45 delivered
```

| Gate | Result |
|---|---|
| KC1 cost-down | −$37.59 (−16.6%), G5 green (+$60.82 headroom) → PASS |
| KC2 rate | 4.9 s < 30 s → PASS |
| KC3 silent | no new silent mode; G8-open unchanged → PASS (unchanged, not fixed) |
| KC4 lift | 1.29 > 1.0 → PASS |
| KC5 A1-beat | $189.18 > $181 → FAIL as beater; ADOPT as cost-down |

## 3. Comparison vs baselines

| Dimension | A1 (record $181) | S6-LC ($226.77) | S6-LC-GR ($189.18, this proposal) |
|---|---|---|---|
| Purchased | $181 | $226.77 | **$189.18** (+$60.82 headroom; delivered $219.45 green) |
| Full-map | 19.63 s | 11.96 s | **4.9 s** |
| Silent | 0 + re-drive | G8-open, no feedback | G8-open, no feedback (unchanged) |
| Regional | cell-granular | bank-local 1.35 s | global-reset+rewrite 4.9 s (slower, in-gate) |
| Bought actuators | gantry class | 3 motors | **2 motors** |
| Print/assembly | coupons ready | carriage + 8 combs | **no carriage/chain; 1 spliced plate (simpler)** |

## 4. Killed variants (recorded so nobody re-pays them)

- **V1 — delete thrust bearings ($18):** KILLED analytically. Axial load 2688 N must go through
  bearings; printed PLA washer limit is an order below. No new evidence. Dead.
- **V2 — 4 screws → 2 screws (save ~$12):** KILLED analytically. 406 mm platen racking on 2
  screws under 2688 N breaks the non-racking assumption the lift gate rests on. Needs a
  stiffness coupon nobody has; carriage deletion already pays more with no gate risk. Dead.
- **V3 — manual mask advance (save $8+$15):** KILLED on rate/product. Mask index 1.0 s becomes
  operator time inside the 30 s budget; unannounced-map path already off-budget and flagged.
  Dead without a board product amendment.

## 5. Disposition

- **ADOPT S6-LC-GR as the S6-LC cost-down definition** (proposal + delta recorded; no model
  edits in this heartbeat — `s6lc.py`/BOM/CSV untouched by design).
- **NOT an A1-beater:** residual $8.18 gap ($189.18 vs $181). Named second cut (mask-mechanism
  direct-card-drive, ~$10) is a follow-up hypothesis, not claimed.
- **Next action:** CTO/Cost owner to confirm the −$37.59 delta against sourced traces and decide
  whether to fold GR into `s6lc.py`+BOM+CAD; coupon C1 rig gains one 80 mm comb-fork section
  (no new hardware class).
- **Parked triggers / killed families respected:** no A1 edits, no divergent-screen seeds;
  screw-matrix (SHA-24) and all SHA-15/16/17/19/25 families untouched.
