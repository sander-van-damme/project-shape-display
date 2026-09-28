# DND-41: reconcile the winner cost basis — one consistent reduced figure ($483.37)

## What changed
The concurrent DND-35/DND-37/DND-41 merges left the winner's **reduced delivered cost**
stated two different ways in the repository:

- ADR-002, `08-current-design`, Test12 and `model.py`: **$483.37** (parts $416.70 × 1.16)
- `dnd37-bom-ratification.md` and `ratify_bom.py --selftest`: **$493.57**, labelled
  "parts $423.30 × 1.16".

These cannot both be right, and the difference is the register consolidation method.

## The defect and the correct treatment
`ratify_bom.py`/the ratification note removed only the **sourced chip cost ($3.70)** from a
fixed base that still contained the **$14 register allowance**, i.e. it double-kept
$10.30 of the removed line, then applied the **multiplicative** `1.10 × 1.06 = 1.166` uplift
(the factor the Falsifier flagged as a double-count).

The correct, project-consistent treatment:
- folding the 40 × 74HC595 onto the driver PCB removes the whole **$14** expected allowance
  and adds the sourced chip cost **$3.70** → **net $10.30** saving;
- controller: **$10** expected allowance → **$5** sourced → **$5** saving;
- delivered uplift is the repository's **additive** ×1.16
  (`delivered_cost_model.py`: `sub + sub*0.10 + sub*0.06`).

Result: parts `284 − 10.30 − 5 + 84 + 64 =` **$416.70** → delivered
**$416.70 × 1.16 = $483.37** (margin **$16.63**). The sourced pair is
**$432.00 × 1.16 = $501.12** — over the ceiling by $1.12.

## Files
- `06-experiments/test12_winner_convergence/ratify_bom.py`: additive `UPLIFT`; correct
  `honest_parts` (remove $14 allowance, add $3.70 chips); selftest pins `501.12` / `483.37`
  / net `$10.30`.
- `07-evidence-and-decisions/dnd37-bom-ratification.md`: correction note; §1 table and §8
  verdict updated to $501.12 / **$483.37** / $16.63 margin.
- `06-experiments/test12_winner_convergence/checks.py`: new guard
  `test_cost_basis_is_additive_and_register_saving_is_net` that fails if the multiplicative
  uplift or a non-net register saving returns.

## Evidence class
Calculation over sourced listings. **No print, no measurement** ([DND-27](/DND/issues/DND-27)).
No board contact ([DND-32](/DND/issues/DND-32)).

## What passed / failed
- Passed: all Test08–Test12 + detent checks; `ratify_bom.py --selftest`;
  `falsifier_s5_review_checks.py`.
- Corrected (was contradictory): the ratification figure $493.57 → **$483.37**, matching
  ADR-002/`08-current-design`. The two artifacts now agree.

## What remains uncertain
The cost is a **range**: the reduced path clears $500 at $483.37, but the only traceable
matched 8 mm PM stepper is $40/ea → ~$3,200 (K7). No distributor stocks a matched part and
the sub-$1.05 basis is an unqualified marketplace multipack (unretirable by purchase under
DND-27). Treat expected delivered cost as **$483.37–$646**.

## Most informative next test
Source a matched sub-$1.05 8 mm 18° PM stepper lot (or accept the range) — this is K7, the
decisive remaining cost residual.

## Coordination
- [DND-35](/DND/issues/DND-35) convergence; [DND-37](/DND/issues/DND-37) BOM ratification
  (corrected here); [DND-41](/DND/issues/DND-41) Falsifier-review reconciliation.
