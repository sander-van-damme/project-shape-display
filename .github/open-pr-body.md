# DND-41 — finish the S5 reconciliation: S1/S2/S4 cost caveat + K5 label

## What changed
Completes the DND-41 reconciliation of the S5 winner with the DND-36 Falsifier review. The
bulk (additive cost basis, K1/K4/K6 re-labels, K7–K12) already landed on `main`; this PR adds
the two remaining acceptance items and aligns one label. **No CAD, BOM or winner change.**

- **S1/S2/S4 cost qualifier (item 6):** ADR-002 §2 now states that the parked S1/S2/S4 rows
  carry **$192–$224 of fallback purchase** for parts their designs intend to print, so their
  cost is **undetermined pending the Bet-A print gate** — stated for symmetry with S5. The
  test12 README carries the same figures.
- **K5 label:** `closed-analytically (range)` → **`conditional`**, matching the docs and the
  Falsifier finding that the sourced pairing is **at/over the ceiling** and only the reduced
  path clears it by a small margin.

## Engineering question
Are all six DND-41 acceptance items now satisfied on the S5 winner deliverable?

## Evidence
- `06-experiments/test12_winner_convergence/checks.py` — all tests pass; asserts K5 `conditional`
  alongside K1 `open`, K4 `partially-closed`, K6 `conditional`, K7–K12 `open`.
- `model.py` + `ratify_bom.py --selftest` reproduce the additive figures ($501.12 sourced /
  $483.37 reduced) unchanged.

## Policy
CALCULATION on repository inputs only. No print, no measurement ([DND-27](/DND/issues/DND-27)).
No board contact ([DND-32](/DND/issues/DND-32)). Branch + PR, self-merge ([DND-19](/DND/issues/DND-19)).
