<!-- © 2024 Sander Van Damme - All Rights Reserved. -->

# SHA-7 A1 promotion evidence — timing, cost, write-path audit

> **Evidence class.** Everything here is **CALCULATION over sourced limits plus
> CAD**, executed by the scripts below. **No print, no purchase, no measurement**
> ([DND-27](/DND/issues/DND-27)). Nothing here is physical validation.

## 1. Timing decomposition (criterion 1) — PASS

`08-integrated-designs/a1-reliability-first/analysis/a1_promotion_timing.py`
(`--gate`: 7/7). Worst-case all-change map at 80×80, 8 heads, 1.0 m/s:

| Stage | s |
|---|---:|
| Digital map processing | 0.05 |
| Physical mask generation | **0.00** (direct write, no mask) |
| Mask transport / indexing | 2.00 |
| Display reset | 3.00 |
| Write sweep (worst-case) | 5.864 |
| Reader verify pass | 5.864 |
| Re-drive retry (1 % miss, 64 cells) + re-verify | 1.347 |
| Settling / locking | 1.50 |
| **Sustained cycle** | **19.63 < 30** (margin 10.37 s) |

Honest-timing rule: **visible transition = sustained = 19.63 s** — no hidden
prep exists (mask generation is 0.00 s, nothing double-buffered). Stress
corners: 5 % miss → 24.7 s; pessimistic full-sweep toggle + nominal retry →
25.96 s; 4-head boundary → 30.0 s (fails — 8 heads is the adopted count).

## 2. Cost placement (criterion 2) — IDEAL

`08-integrated-designs/a1-reliability-first/analysis/a1_promotion_cost.py`
(`--gate`: 7/7). Purchased parts **$181.00 → IDEAL (<$200)**; delivered
(×1.16) **$209.96 → ACCEPTABLE**; hostile reprice (+35 % soft lines)
**$189.40 → still IDEAL**. Zero per-cell bought hardware (4 shared
actuators; 2.8 ¢/cell amortised).

Enforceable ceiling (S5-gate precedent), executed as a real assertion in the
gate: `assert reader_head_unit_usd <= 30.99  # keeps purchased <$200 (ideal)`.
Gantry-motion sub-assembly ($68) has the same form. CSV matches the model
($181.00 exactly).

## 3. Write-path adversarial audit (criterion 3) — CLEAN (22/22)

`falsifier_sha7_a1_writepath_audit.py` (`--gate`: 22/22), stdlib-only,
imports nothing from the model (A13/A14 precedent):

- **W1 missed toggle → detected.** Reader on/off 7.72× ideal, 5.95× with
  crosstalk, both > 2× gate, at a frame-fixed standoff.
- **W2 double-step → no third state.** Binary crank between hard stops is an
  involution; any parity error is read back, never silent.
- **W3 neighbour disturbance → bounded.** Latch excursion 0.65 mm ≤ owned
  half-lane 0.74 mm (0.09 mm margin); cell-granularity regional update, no
  full-board reset; 0.00 mm modelled vs the 0.10 mm Q5 proposal.
- **W4 force window → bounded with a stated kill line.** 10 N usable writer >
  4.20 N worst snap (±40 % spread) and << 211 N damage land. **Sting
  recorded:** the 3.0 N snap nominal is assumption-class; the coupon **kills**
  the program if measured snap mean exceeds 7.14 N.
- **W5 retry converges → in budget.** 19.63 s nominal; 4 bounded attempts drive
  residual to 1e-8/cell; the 500-cell retry cap (10.5 s worst) cannot overflow
  the 11.7 s headroom (mean load 64 cells, 54σ margin). The audit's own gate
  caught and forced both corrections (cap 640→500, 3→4 attempts).
- **W6/W7 honesty → stated.** Wear, registration, optical constants labelled;
  headline numbers reproduce the live model.

## 4. Residual risks → decision note

See [`sha7-a1-promotion-decision.md`](sha7-a1-promotion-decision.md)
(**GATE**: promote the architecture, gate the build on coupon A).
