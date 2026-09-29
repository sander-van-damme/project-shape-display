# DND-98: independently re-ratify the corrected S6-LC purchased BOM

Closes [DND-98](/DND/issues/DND-98).

## What changed

Adds the **independent re-ratification of the corrected (post-DND-93) S6-LC purchased BOM**, which
supersedes the DND-73 ratification of the uncorrected BOM.

- `09-low-cost-variant/s6lc/ratify/s6lc_bom_reratify.py` — re-derives the 20 BOM lines **by hand**
  (not imported from `bom()`), with evidence-class audit, DND-73→DND-93 delta, break-evens,
  optimistic/working/high/hostile/lean scenarios, per-cell sensitivity and reliability scaling.
  `--selftest` and `--emit-csv` included.
- `09-low-cost-variant/s6lc/ratify/s6lc_bom_reratify_checks.py` — CI gate, **68 checks**.
- `09-low-cost-variant/s6lc/ratify/s6lc_bom_ratified.csv` — ratified purchased BOM.
- `07-evidence-and-decisions/dnd98-s6lc-bom-reratification.md` — the ADR.
- `.github/workflows/ci.yml` — wires the new gate; `07-evidence-and-decisions/README.md` and
  `09-low-cost-variant/s6lc/README.md` — index/table updates.

## Engineering question

Does the corrected S6-LC purchased BOM still hold the board ceiling, and if not, which ceiling and
which requirement must move? The issue requires an explicit statement of the **`<$250 purchased,
excluding 3D-printed parts`** gate (DND-70/DND-72) under working and hostile pricing.

## Evidence produced (sourced listings + CALCULATION; no print/purchase/measurement, DND-27)

- Corrected headline **reproduces**: **$226.77 parts / $263.05 delivered (×1.16)**, reconciling with
  `s6lc.bom()` and `bom_s6lc.csv`.
- **`<$250 purchased` mission gate HOLDS: +$23.23.**
- **`$250 delivered` repo convention FAILS: −$13.05** (both stated, neither hidden).
- Growth since DND-73: **+$18.00** (NEMA17→NEMA23 lift re-price) + **+$69.00** six DND-91/A5
  capability allowances = **+$87.00**.
- Evidence class: 35 % traced / **65 % allowance** ($69.00 A5).
- Break-even at $250 purchased: tightest line is the **lift motor** ($30 → cap $53.23, **1.77×**).
- Scenarios (purchased): opt $199.79 / work $226.77 / high $245.61 / lean $187.26 all clear;
  **hostile $300.58 breaches by $50.58**.
- **No per-cell bought hardware** (3 motors; 3.543 cents/cell, 0.363 cents/cell headroom).
- 99 %-map reliability needs **q ≤ 1.57e−6**; G7 remains measurement-gated (coupon C1).

## Assumptions

- EUR listing prices carried verbatim as USD (repo K7/DND-56 convention; conservative for a US buyer).
- The lead-screw line ($24) is under-priced ~$4.76 vs its stable order tier; carried at the committed
  figure and flagged rather than silently re-priced.
- Lift-load model and G3 branch choice are the CTO's (DND-93); this PR ratifies the resulting BOM,
  it does not re-open the mechanism.

## Passed / failed / uncertain

- **Passed:** `s6lc_checks` 40/40, `falsifier_dnd91_checks` 40/40, `falsifier_dnd74_checks` 28/28,
  `s6lc_bom_reratify_checks` 68/68.
- **Failed (recorded):** delivered cost convention ($263.05), hostile-pricing purchased ceiling.
- **Uncertain:** A5 allowance realism; G7 reliability (measurement-only).

## Next test

Printed coupon **C1** (4×4 unit-cell at true pitch + push-pull gauge) to resolve A1/A2/A6 and G7 —
the cheapest experiment that can reject the remaining mechanism assumptions.

Evidence class: **CALCULATION + sourced listings only.** No print, no purchase, no measurement
(DND-27). No board contact (DND-32). `08-current-design/` untouched.
