# DND-37 — Ratify S5 winner purchased BOM + printability

Stacked on **`dnd-35-convergence-winner`** (DND-35, PR pending). Base: `dnd-35-convergence-winner`.

## What changed
- **New** `06-experiments/test12_winner_convergence/ratify_bom.py` — independent
  re-derivation of the S5 purchased BOM straight from `bom_S5_delivered.csv`, plus a
  `--selftest` that pins the DND-37 findings in CI.
- **New** `07-evidence-and-decisions/dnd37-bom-ratification.md` — the ratification note.
- **Correction** across ADR-002, `test12/README.md`, `08-current-design/README.md`,
  `sourcing_notes.md`: reduced delivered cost **$481.56 → $493.57**.
- **CI**: `ratify_bom.py --selftest` added to the Test12 step.

## Engineering question
Does the S5 winner's purchased BOM arithmetic hold, can any sourced reduction reach
<$400, is there a sourced matched sub-$1 8 mm stepper, and is the X1C/PLA 0.4 mm
printability route sound?

## Evidence produced (CALCULATION over sourced listings — no purchase, no print)
- **BOM arithmetic:** fixed expected subtotal $284.00 reproduces the CSV; sourced-pair
  delivered **$503.71** confirmed.
- **Defect found:** the reduced path subtracts the shift-register line at its **$14
  expected allowance** against a base re-priced to sourced prices; the sourced value is
  only **$3.70** (40 × $0.094). Overstatement **$10.30** → honest reduced **$493.57**
  (still under $500, but **$6.43** margin, not $18.44).
- **Motor supply:** Octopart (DigiKey/Mouser/Farnell/Newark/Arrow) stocks **no** true
  8 mm 18° bipolar PM stepper; only traceable matched part is MOONS 8PM020S1 **$40/ea**
  (→ ~$4,156 delivered). Live AliExpress micro listings €0.79–3.59 ea are unqualified.
  Expected cost is a **range $493.57–$646**.
- **<$400 band:** **not reachable** on any sourced path.
- **Printability:** X1C/PLA 0.4 mm ratified; all features ≥ the sourced 0.44 mm minimum
  feature width. Thin contact features (detent 0.45, body wall 0.60, stem 0.70 mm) are
  under the 0.88 mm robust wall → 0.2 mm nozzle recommended for the *contact* features,
  not required by geometry; resin/SLA not required.

## What passed / failed
- Passed: `checks.py` (9/9), `model.py`, new `ratify_bom.py --selftest`, Test08/10/11
  checks, delivered-BOM checks.
- Failed (kept as findings): the $481.56 reduced figure; the "optional 0.2 mm upper
  guides" characterisation; the <$400 claim.

## Assumptions / uncertainty
Motor and driver unit prices remain **sourced listings, not quotations**; the sub-$1.05
basis is an unqualified marketplace multipack that DND-27 forbids retiring by purchase.
Print tolerance/strength of the thin contact features is a qualitative residual (K2 class).

## Next test
Sample a matched 8 mm motor lot (step angle, running torque ≥0.15 mN·m @400 pps, winding,
shaft) — blocked by DND-27; otherwise carry the range and proceed to the analytic detent
contact sweep.

Co-Authored-By: Paperclip <noreply@paperclip.ing>
