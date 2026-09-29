# DND-73 — Independently ratify the S6-LC ultra-low-cost BOM of record ($139.77 / $162.13)

**Issue:** [DND-73](/DND/issues/DND-73) (repointed by [DND-90](/DND/issues/DND-90); parent [DND-84](/DND/issues/DND-84)).
**Verdict: RATIFIED WITH ONE MATERIAL FINDING.**
**Evidence class:** SOURCED listings + CALCULATION only. No purchase, no print, no measurement ([DND-27](/DND/issues/DND-27)). No board contact ([DND-32](/DND/issues/DND-32)).

## What changed

- `09-low-cost-variant/s6lc/ratify/s6lc_bom_ratify.py` — independent re-derivation of the committed
  BOM (lines re-entered by hand; does **not** import `s6lc.bom()`), live 2026-09-29 listing trace,
  break-evens, scenarios, hostile findings, and a **stable order-tier re-price (Q7)**.
- `09-low-cost-variant/s6lc/ratify/s6lc_bom_ratify_checks.py` — **65-check CI gate**.
- `09-low-cost-variant/s6lc/ratify/s6lc_bom_ratified.csv` — ratified working BOM artifact.
- `07-evidence-and-decisions/dnd73-s6lc-bom-ratification.md` — the ratification note.
- `.github/workflows/ci.yml` — new `DND-73 S6-LC BOM ratification gate`.
- `09-low-cost-variant/s6lc/README.md` — ratification status.

## Engineering question

Does a **defensible** purchased BOM for the selected **S6-LC** machine clear the board's
**< $250** ceiling (excluding 3D-printed parts), and where can the claim be broken?

## Result

| Check | Result |
|---|---|
| Claim reproduces | **$139.77 parts → $162.13 delivered** (additive ×1.16), margin **$87.87** — exact |
| Parts ceiling | $215.52; parts headroom **$75.75** |
| Critical lines traced | lift motor **+$0.39**; all others **−$0.85 … −$14.80** vs BOM |
| Break-even per line | every line has **≥ 2×** headroom (no cost cliff; largest line $24) |
| Scenarios | optimistic **$132.21** / working **$162.13** / high **$205.68** / hostile **$243.45** — all < $250 |
| Stable order tier (Q7) | **$131.31 parts → $152.32 delivered**, margin **$97.68** — clears |
| **Finding:** off-BOM card puncher | hostile **+ $20 puncher = $266.65 > $250** |

## Evidence produced

- **Finding 1 (labelling):** **44 %** of parts is listing-traced / committed; **56 % ($78.00)** is
  disclosed `sourced-class` / `assumption` allowance. Contained by the scenario analysis (2×
  allowance repricing still clears at $243.45).
- **Finding 2 (line prices, Q7):** re-pricing every line at the **stable order tier** (no flash
  deals, no spec-less parts) shows **two lines genuinely under-priced** — the 4× T8 lead-screw line
  **+$4.76** (the $3.49 "set" is a stock-1 flash deal; the stable lead-2 mm screw+nut is ~$7.19) and
  the motor-coupler line **+$6.32**. Small motors / loom / sensors are generous enough that the
  honest total is **$131.31 parts → $152.32 delivered** ($97.68 margin) — *more* conservative than
  the committed $139.77. The naive "cheapest listing" Δ column did not survive scrutiny.
- **Finding 3 (scope):** the architecture's off-line **punched-card mask medium** is excluded from
  the BOM as a **shared tool** (correct). A $20 puncher allowance on hostile pricing gives
  **$266.65 > $250** — the one credible breach, and it is a product/scope dependency, not a part price.
- No analogue of the S5 "K7 motor cliff": the S6-LC BOM has **no line above $30**.

## Assumptions

- Repo additive delivered uplift ×1.16 ([DND-41](/DND/issues/DND-41)).
- EUR carried verbatim as USD (K7/DND-56 convention; EUR ≥ USD, conservative for a US buyer).
- Printed parts (frame, columns, pawls, masks, combs) excluded by the requirement.

## What ran

```
python 09-low-cost-variant/s6lc/ratify/s6lc_bom_ratify.py           # report (Q1–Q7)
python 09-low-cost-variant/s6lc/ratify/s6lc_bom_ratify.py --selftest
python 09-low-cost-variant/s6lc/ratify/s6lc_bom_ratify.py --emit-csv
python 09-low-cost-variant/s6lc/ratify/s6lc_bom_ratify_checks.py    # 65/65 pass
python 09-low-cost-variant/s6lc/analysis/s6lc.py                    # committed model unchanged
python 09-low-cost-variant/s6lc/analysis/s6lc_checks.py             # 29/29 pass
```

## What passed / failed

- **Passed:** claim reproduction, uplift basis, trace delta, per-line ≥2× break-even headroom,
  scenario ordering + all-clear, stable order-tier clearance, reconciliation with `s6lc.bom()` and
  `bom_s6lc.csv`, ADR contents.
- **Recorded failure (deliberate):** hostile + shared card puncher **$266.65 > $250** — pinned by
  the gate so it cannot be silently reversed.

## Remaining uncertainty / next test

- ±$0.39 means, not contract quotes; no 2-piece quote for the lift motor.
- The stable order-tier trace is point-in-time; a revision should correct the T8 and coupler lines.
- Next: trace PSU/loom/guide/belt allowances to lift the traced share above 70 %, and state the
  card-puncher scope in the BOM header. Hand the puncher-scope question to
  [DND-74](/DND/issues/DND-74) as part of its mask-write attack.
