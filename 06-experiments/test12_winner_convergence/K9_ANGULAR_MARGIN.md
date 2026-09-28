# DND-45 — K9 Monte-Carlo angular-margin stack-up (print tolerance)

**Question.** Test09/Test12 (K9) quote a **12.50°** nominal angular margin for the 5-level
stepped rotor, reduced to **6.50°** after a **6.00°** seating error. But the **±0.05 mm
FDM print-positional tolerance** on the **1.5 mm-radius** rotor was never propagated. Does
the tolerance eat the remaining margin, and at how many levels?

**Answer (CALCULATION / MONTE-CARLO, no print/measurement, [DND-27](/DND/issues/DND-27)).**
K9 is now **closed quantitatively and it changes the level-count decision**:

- **5 levels is safe only under the bounded reading** of ±0.05 mm (a capability limit):
  worst-case seat (6.00°) gives mean margin **5.52°**, p05 **3.67°**, **worst draw 1.72°**,
  **failure probability 0.00%**. The guaranteed margin shrinks from 6.50° nominal to
  **~1.7°** — a thin but positive reserve.
- **Under a Gaussian reading** (±0.05 mm as 1σ, heavier tail): 5 levels has a **1.31%**
  probability of a **negative** margin. It is **not** unconditionally robust.
- **6 levels fails outright:** mean **−0.47°**, **65.6%** failure under the bounded /
  worst-case seat model (69.1% Gaussian). The Test09 note "6 levels leave 0.50° nominal"
  is **not survivable** once tolerance is propagated.
- **4 levels is the maximum unconditionally-safe count:** 0% failure under every model
  (bounded or Gaussian, worst-case or random seat), worst draw still positive.
- **8/9/10 levels are dead on arrival** — negative nominal envelope already.

**Verdict: K9 → `closed`.** With the sourced ±0.05 mm tolerance, **5 levels keeps the
angular margin positive but with only ~1.7° worst-case reserve**; **4 levels is the
robust choice**; **6 levels must be rejected**. The residual decision is the K12
level-count vs height-resolution product tradeoff, now carrying a hard margin constraint
instead of a nominal-only claim.

## Model

The margin is set by the **toe half-envelope** and the **sector half-angle**:

```
toe_angle(θ) = atan2(toe_width/2, toe_x − center_x)      (Test08 analysis.geometry)
angular_margin = 180/levels − toe_angle − seating_error
```

The lever arm the ±0.05 mm tolerance perturbs is `toe_x − center_x = 0.85 − (−0.30) =
1.15 mm`; the toe half-width is `0.50 mm`. Nominally `atan2(0.50, 1.15) = 23.499°`,
reproducing Test09's **"23.50° toe envelope"**.

Monte-Carlo terms drawn per trial (200,000 draws, fixed seed 20260928):

| Term | Distribution | Source |
|---|---|---|
| `toe_x` positional | ±0.05 mm | sourced FDM positional tolerance |
| `center_x` positional | ±0.05 mm | sourced FDM positional tolerance |
| `toe_width` feature | ±0.05 mm | sourced FDM dimensional tolerance |
| rotor radius feature | ±0.05 mm → angular shift `|Δr|/r` | sourced FDM dimensional tolerance |
| seating error | worst-case 6.00° **and** \|N(0,2)\| truncated at 6° | Test09 seating gate |
| tolerance shape | **uniform** (bounded, primary) **and** Gaussian σ=0.05 (conservative) | stated |

## Results (per level count)

**Primary model — bounded uniform ±0.05 mm, worst-case 6.00° seat:**

| Levels | nominal margin | mean | std | p05 | min | P(margin<0) |
|---:|---:|---:|---:|---:|---:|---:|
| 4 | 21.50° | 14.53° | 1.11° | 12.66° | 10.76° | **0.00%** |
| **5** | 12.50° | **5.52°** | 1.11° | 3.67° | **1.72°** | **0.00%** |
| 6 | 6.50° | **−0.47°** | 1.11° | −2.32° | −4.28° | **65.6%** |
| 8 | −1.00° | −7.97° | 1.11° | −9.82° | −11.77° | 100% |

**Conservative model — Gaussian σ=0.05 mm, worst-case seat:**

| Levels | mean | min | P(margin<0) |
|---:|---:|---:|---:|
| 4 | 13.93° | 3.31° | **0.00%** |
| 5 | 4.92° | −6.14° | **1.31%** |
| 6 | −1.08° | −12.75° | **69.1%** |

**Max safe level count (0% failure):** bounded/worst-case = **5**; Gaussian/worst-case =
**4**; bounded/random-seat = **5**. The intersection is **4**; 5 is safe only under the
bounded tolerance reading, with ~1.7° worst-case reserve.

## What this does / does not establish

- **Does:** propagate the ±0.05 mm print tolerance through the actual toe/sector geometry;
  give the marginal distribution and failure probability per level count; show **6 levels
  fails** and **4 levels is robust**, so the K12 product tradeoff has a hard margin bound.
- **Does not:** measure the real as-printed tolerance distribution on these parts, nor the
  rotor radius/core deviation. The ±0.05 mm figure is a sourced FDM capability claim, and
  the two distribution shapes bound the honest range. No coupon can retire this under
  DND-27.

## Run

```text
python k9_angular_margin.py    # full MC result, JSON
python k9_checks.py            # regression + honesty gates (fast, 40k draws)
```
