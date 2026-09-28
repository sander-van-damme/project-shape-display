# DND-37: port the 3 cost-model regression gates from superseded PR #32

**Owner:** CostManufacturing · **Issue:** [DND-35](/DND/issues/DND-35) · **Evidence class:** CALCULATION (no purchase/print, [DND-27](/DND/issues/DND-27))

## What changed

Adds the **only surviving value of the superseded PR #32** — its three DND-37
cost-model regression gates — to `06-experiments/test12_winner_convergence/checks.py`,
adapted to the corrected additive (`x1.16`) model on `main`:

1. `test_no_sourced_path_claims_the_400_ideal_band` — no sourced or reduced path
   may claim the <$400 ideal band.
2. `test_cost_model_is_a_real_function_of_sourced_prices` — substituting the
   traceable DRV8833 driver ($1.3338) must move the headline by exactly
   `channels x delta x uplift`; a hard-coded total fails.
3. `test_matched_motor_fallback_is_dead` — the only traceable matched part
   (MOONS 8PM020S1, ~$40/ea) puts the winner >2x over the ceiling.

`checks.py` already runs in the `engineering-checks` CI job (`.github/workflows/ci.yml:67`),
so these gates are enforced on every push/PR.

## Engineering question

Can the S5 winner's purchased-cost *claims* be fenced so a future edit cannot
quietly reintroduce a sub-$400 claim, hard-code the headline, or re-brand the
matched motor as a winner path?

## Evidence produced

- `python 06-experiments/test12_winner_convergence/checks.py` → **13/13 pass**
  (was 10/10).
- `python 06-experiments/test12_winner_convergence/ratify_bom.py --selftest` → OK,
  asserts the additive **$501.12 / $483.37** on `main`.

## Assumptions

- The win/ceiling/floor constants in `model.py` are the reviewed DND-41 figures.
- These gates are base-independent of the additive-vs-multiplicative fix already
  merged in PR #37; they guard the *claims*, not the arithmetic basis.

## What failed / remains uncertain

- These are CALCULATION gates over the sourced BOM CSV; they are not purchase or
  measurement evidence. K7 (actuator cost cliff: no matched sub-$1.05 motor) stays
  **open** — this PR only makes that dead end non-regressable.

## Next test

None required on this branch. Reconciled under CTO-owned [DND-41](/DND/issues/DND-41).
