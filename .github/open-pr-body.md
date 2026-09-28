# DND-37b — port the three DND-37 regression gates from the stale PR #32 onto `main`

## What changed

PR #32 (DND-37) was authored on a pre-PR-#28 base and was **not merged as-is** (it would
have reverted the reviewed cost correction and deleted `ratify_bom.py` /
`dnd37-bom-ratification.md`). Its one genuinely-new, base-independent asset was its three
executable DND-37 gates. This PR ports exactly those onto `main` and drops the stale parts.

## Engineering question

Can DND-37's §2 claims be pinned as executable regression gates rather than prose?

## Evidence produced (CALCULATION over the sourced BOM; no purchase, no print, DND-27)

Added to `06-experiments/test12_winner_convergence/checks.py` (10 → 13 tests):

1. `test_dnd37_no_sourced_sub_400_path_exists` — solves for the motor+driver pair price
   implied by the <$400 band and asserts it is **below the cheapest sourced pair** and
   below one sourced motor alone. Encodes "no sourced <$400 path exists".
2. `test_dnd37_driver_substitution_is_cheaper_than_csv_drv8833` — TB6612FNG $0.80 < the
   CSV's DRV8833PWPR $1.58 expected, i.e. the substitution is a real sourced reduction,
   not a discount assumption.
3. `test_dnd37_matched_motor_fallback_is_a_dead_cost_path` — a $40 matched motor puts the
   machine at >5× the ceiling; the program's #1 cost risk is asserted, not hidden.

## Verification

```
python 06-experiments/test12_winner_convergence/checks.py   # 13/13 pass
```

## Disposition of PR #32

Superseded. Its correct content is in `main` via the DND-41 reconciliation (PR #33) and
this gate port; the rest of the branch regressed reviewed work. No API token exists to
close the GitHub PR object (deploy key is git-only) — harmless fallout, noted on
DND-35/DND-6.
