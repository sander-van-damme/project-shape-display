# DND-37 — Ratify the S5 winner purchased BOM and printability

Implements [DND-37](/DND/issues/DND-37) (child of [DND-35](/DND/issues/DND-35), winner
convergence). Ratifies the S5 purchased BOM and the X1C/PLA 0.4 mm modular printability
route as the program winner, with the residual motor-supply risk stated precisely.

## What changed

- **New** `06-experiments/test12_winner_convergence/RATIFICATION.md` — the ratification
  note (verdict, arithmetic re-derivation, <$400 reachability proof, motor-source
  assessment, printability route, open risks, next test).
- **Edited** `06-experiments/test12_winner_convergence/checks.py` — 3 new DND-37 gates
  (9 → 12 tests): no sourced sub-$400 path; the driver substitution is a real sourced
  reduction; the matched-motor fallback is an arithmetically dead cost path.
- **Edited** `06-experiments/test12_winner_convergence/README.md` — link the ratification
  and its verdict.

## Engineering question

Can the S5 winner purchased BOM and printability route be ratified, and is there any
**sourced** path to the project's <$400 ideal band without new unproven parts?

## Evidence produced

CALCULATION over sourced listings (LCSC/marketplace, observed 2026-09-28) plus stated
allowances. **No purchase, no print, no measurement** ([DND-27](/DND/issues/DND-27)).

Independent re-derivation (all reproduce the model exactly):

| Component | Value |
|---|---:|
| Fixed (non motor/driver) expected subtotal, from `bom_S5_delivered.csv` | **$284.00** |
| Sourced pair (motor $1.05 + TB6612 $0.80) delivered ×1.166 | **$503.71** |
| + 2 consolidations (−$14 registers onto PCB, −$5 RP2040) → reduced delivered | **$481.56** |

## Assumptions

- Delivered uplift ×1.10 ship ×1.06 tax (expected scenario), applied to all parts.
- The TB6612FNG ($0.7955 @100) drives one bipolar PM stepper per package, so it is a
  like-for-like, cheaper substitute for the CSV's DRV8833PWPR ($1.58 expected).
- `q = 1×10⁻⁴` per-cell error is an assumption; there is no per-cell feedback.

## Calculations run / results

- **No sourced <$400 path exists.** At the reduced fixed stack ($265), delivering at $400
  needs the 80 motor+driver pairs to average **≤ $0.9757/ea**; the cheapest sourced pair
  is **$1.85** ($1.05 motor + $0.80 driver). Hard floor with a *free* motor+driver is still
  **$308.99 delivered**. This is asserted as a gate, not just claimed.
- **Cheapest credible pair clears $500 with margin:** $481.56 reduced, −$18.44.
- **Matched-motor fallback is dead:** the only traceable matched 8 mm 18° bipolar PM
  stepper is **MOONS 8PM020S1 at $40/ea → ~$4,000 for 80** (>5× ceiling, asserted).

## What passed / failed

- `checks.py`: **12/12 PASS** (including the 3 new DND-37 gates).
- `model.py`, `detent_checks.py`: run clean, exit 0.
- **Failed by design:** the <$400 ideal-band target is not reachable on current sourced
  parts — stated explicitly per DND-37 §2.

## What remains uncertain

- **Motor supply qualification (the #1 cost risk).** The $1.05 motor is an untraced
  marketplace multipack (winding/shaft/lot/holding-torque unverified). The only matched
  replacement is ~$40/ea (~$4,000). The $1.05→$40 gap is a qualification risk, not an
  averageable number.
- **K2 detent friction:** corrects a one-step slip only for printed PLA μ ≤ 0.323 or a
  scallop ≥ 0.31 mm; the sourced midpoint μ≈0.35 does not correct at nominal.
- **Reliability q** (assumed) and the **40 mm travel** envelope (provisional) remain open.

## Next test

Obtain **one traceable, matched 8 mm 18° bipolar PM stepper datasheet + price at the
required lot (80 + spares), delivered-inclusive.** One document either confirms the
$481.56 path or collapses S5 to ~$4,000. No hardware required under DND-27.

---

Branch `cost/dnd37-s5-ratification`. Verdict: **BOM + printability route RATIFIED,
conditional on motor qualification.** No board contact (DND-32).
