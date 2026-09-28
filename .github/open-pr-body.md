# DND-47 — Independently ratify the DND-44 machine-preserving cost closure

## What changed

- **New** `06-experiments/test12_winner_convergence/cost_closure_ratify.py` — an
  independent re-derivation of the DND-44 K5/K7 cost claim. It reads the committed
  `bom_S5_delivered.csv` line-by-line and does **not** import `cost_closure.py` for
  its own arithmetic, so a discrepancy between the claim and the data is visible
  rather than inherited. `--selftest` pins every figure **and reconciles against the
  now-committed DND-44 `cost_closure.py`** (merged as PR #42).
- **New** `07-evidence-and-decisions/dnd47-cost-closure-ratification.md` — the
  decision record.
- **Updated** `sourcing_notes.md` §8 — DND-47 ratification addendum.
- **Updated** `.github/workflows/ci.yml` — wire the ratifier into the Test12 CI gate,
  **and fix a main-red regression**: the DND-44 merge (PR #42, `e10e57a`) added
  `buckling_closure.py` (numpy via `cam_strength.py`) to the stdlib-only
  `engineering-checks` job with no numpy install. `84e5385` was green; `e10e57a` and
  every descendant are red. Reproduced in a clean venv (`FAILED (errors=4)`, all
  `ModuleNotFoundError: numpy`). Fix: `pip install numpy>=1.26` in that job. This PR
  also **un-reds `main`**.

## Engineering question

Does the DND-44 claim hold: honest expected baseline **$592.06**, a
machine-preserving E1–E6 path at **$424.95 delivered / $75.05 margin**, clearing
only for a motor **≤ $1.86**, with a **$574.36** downside at the sourced $2.66
motor?

## Evidence produced

All in **CALCULATION** class over sourced listings (`--selftest` asserts each):

| Figure | DND-44 claim | Independent re-derivation |
|---|---:|---:|
| Honest expected baseline (parts / delivered) | $510.40 / $592.06 | **$510.40 / $592.06** |
| E1–E6 path (parts / delivered / margin) | $366.34 / $424.95 / $75.05 | **$366.34 / $424.95 / $75.05** |
| Motor break-even | $1.86 | **$1.8587** |
| Downside @ $2.66 motor | $574.36 | **$574.36** |

**Verdict: RATIFIED WITH QUALIFICATION.**

- **Qualification (scenario consistency):** $40.60 of the $75.05 margin is **E6**
  repricing four fixed lines from `unit_expected` → `unit_best`; a further $16.00
  is **E2** moving the motor from expected $1.25 → best-case $1.05. These mix
  best-case prices into an "expected" total. The path still clears without E6
  ($465.55 delivered, $34.45 margin), so the claim stands; the honest range is
  **$424.95–$465.55**.
- **E1 TB6612FNG is legitimate:** dual H-bridge, VM 2.5–13.5 V, 1.2 A/ch — well
  inside the 5–6 V, ~0.25 A 8 mm 18° PM stepper. E3/E4 reproduce DND-41's
  net-saving method. E5 (spares) is a purchasing choice, not the machine.
- **Machine preserved:** no structural line removed; motor/driver counts, pitch
  (5.08 mm), cells (6,400), travel (40 mm) and topology unchanged.
- **Independent finding:** the `Dual H-bridge` line is priced per **dual** IC at
  qty 80 (= motor count). 80 motors need **40 ICs** → **$36.91 delivered** of
  conservatism *against* the design (adds margin; does not threaten the ceiling).
- **K7 remains the binding residual:** no matched sub-$1.86 motor supply exists.

## Assumptions

E6's `unit_best` values are that column's sourced/allowance prices, treated by
DND-44 as expected; its own basis strings call them "bundled allowance". Uplift is
the repo's additive ×1.16 (DND-41). No purchase, print or measurement.

## Calculations / tests run

`python cost_closure_ratify.py` and `--selftest`; the merged
`cost_closure.py` / `cost_closure_checks.py`; existing `checks.py`,
`ratify_bom.py --selftest`, `detent_checks.py`; plus the full `engineering-checks`
job replicated locally in a clean venv. CI now runs the ratifier and installs numpy.

## What passed / failed

- **Passed:** all four headline figures reproduce exactly; structural-preservation
  check; break-even in band; the merged DND-44 module and this independent
  re-derivation agree on every headline; all CI checks green.
- **Failed / qualified:** the single $424.95 headline omits that it is a
  best-case-priced path; reported as a range. Separately, `main` was red from the
  DND-44 merge until this PR (numpy missing in CI) — fixed here.

## Remaining uncertainty

K7 (unqualified motor supply) is unchanged and unclosable without buying a part
([DND-27](/DND/issues/DND-27)). E6 fixed lines have no volume quote.

## Next test

Single traceable motor sample + 80+spare delivered quote (same winding, step
angle, shaft, lot) — the Test09 Stage C procurement gate. Until then, S5 purchased
cost is **$424.95–$574.36 delivered**.
