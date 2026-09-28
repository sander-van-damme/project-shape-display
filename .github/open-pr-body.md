# DND-41b — reconcile the two cost models on `main` (ratify_bom.py vs model.py)

## What changed

After the DND-41 reconciliation (`model.py` → $501.12 / $483.37 on the additive
×1.16 basis) landed, `main` was left carrying **two contradictory cost models**:

- `model.py` / `checks.py` — **$501.12 sourced / $483.37 reduced** (additive ×1.16).
- `ratify_bom.py` — **$503.71 sourced / $493.57 reduced** (multiplicative ×1.166 +
  a register method that kept the $14 allowance in the base).

`ci.yml` runs `ratify_bom.py --selftest` as a gate, so the two could not be caught
by the existing tests. This PR removes the contradiction at the source.

## Engineering question

Which cost model is correct on the repo's own delivered basis, and can the two
models be pinned together so they cannot diverge again?

## Evidence produced (CALCULATION over the sourced BOM — no purchase, no print, DND-27)

1. **Uplift basis.** `06-experiments/test11_cost_printability_reliability/delivered_3scenario/delivered_cost_model.py`
   applies the expected uplift **additively** (`sub + sub·0.10 + sub·0.06`). The
   prior `(1.10)(1.06) = 1.166` **compounds** and inflates every headline by ~0.5%.
   On the repo's basis the sourced pair is **$432.00 × 1.16 = $501.12 — over the
   $500 ceiling by $1.12**.
2. **Register consolidation method.** The $14.00 expected allowance leaves the BOM,
   but the 40 chips are still **bought** at $0.0925 → $3.70. The net saving is
   **$10.30**, not the full $14.00 (and not merely $3.70). Honest reduced fixed is
   `$284.00 − $10.30 − $5.00 = $268.70`, parts `$416.70`, delivered
   `$416.70 × 1.16 = $483.37` — clearing the ceiling by **$16.63**.
3. **Root-cause guard added.** `checks.py::test_ratify_bom_agrees_with_model_on_the_headline_costs`
   imports `ratify_bom` and asserts it agrees with `model.py` on both headline
   costs and the uplift constant. The models can no longer silently drift.

## Files

- `06-experiments/test12_winner_convergence/ratify_bom.py` — additive uplift;
  correct net-consolidation method; selftest now asserts $501.12 / $483.37.
- `06-experiments/test12_winner_convergence/checks.py` — new cross-model gate (9 → 10 tests).
- `07-evidence-and-decisions/dnd37-bom-ratification.md` — DND-41 correction banner
  superseding the stale §1–§2 figures.
- `07-evidence-and-decisions/convergence-decision-2026-09-b.md` — §3.2 numbers corrected.

## Verification

```
python 06-experiments/test12_winner_convergence/ratify_bom.py --selftest
python 06-experiments/test12_winner_convergence/checks.py      # 10/10 pass
python 06-experiments/test12_winner_convergence/model.py
```

## Assumptions / uncertainty

- The uplift (10% ship + 6% tax) and the sourced motor price ($1.05, untraced
  marketplace multipack) are unchanged assumptions, not quotes. The winner clears
  the ceiling only on the reduced path and only if the $1.05 motor qualifies;
  the matched alternative is ~$40/ea (~$4,000). **Unchanged, still the #1 risk.**
- No physical test (DND-27). This is arithmetic reconciliation only.
