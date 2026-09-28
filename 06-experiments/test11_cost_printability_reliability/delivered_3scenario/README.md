# Test 11.1 — Three-scenario DELIVERED purchased BOM (S1–S5)

**Question (DND-11 / DND-6).** For each architecture survivor S1–S5, what does the
*bought* hardware actually cost **delivered** in three scenarios — best, expected,
worst — with per-line part, quantity, unit price, line total, vendor and evidence
label, and how much headroom remains under the **$500** purchased-component
ceiling?

**Evidence level.** Cost-model arithmetic over **sourced listing prices** (live
2026-09-28) plus **explicit engineering allowances**. There is **no supplier
quotation, no purchase and no measurement**. Every line is labelled
`sourced` or `assumption` so nothing analytical is presented as validated.

Run:

```text
python 06-experiments/test11_cost_printability_reliability/delivered_3scenario/delivered_cost_model.py
python 06-experiments/test11_cost_printability_reliability/delivered_3scenario/checks.py
```

Standard library only. Inputs are the five `bom_S*_delivered.csv` files here.
This folder is the DND-11 deliverable; the optimistic/working/high analysis in
the parent `test11_cost_printability_reliability/` remains the source-model.

## Scenario definitions

| Scenario | Sourcing posture | Delivered uplift (assumption) |
|---|---|---|
| **Best** | Highest-volume / most favourable: marketplace multipacks, one consolidated regional shipment, group-buy tiers | +5% shipping, +0% tax/import |
| **Expected** | Realistic single-quantity retail: small-bundle list prices, one or two shipments, nominal import | +10% shipping, +6% tax/import |
| **Worst** | Low-volume / expedited / single-source: branded distributor parts, split shipments, air freight, full duty/handling | +18% shipping, +11% tax/import |

The uplifts are **assumptions**, applied to the parts subtotal, and are labelled
as such. They convert "list price" into "what you pay to get it on the table",
which is the number the $500 ceiling is actually about.

## Headline result

**Every survivor is over the $500 ceiling in the expected scenario, delivered.**
Delivered totals (best / expected / worst):

| Candidate | Best deliv. | Expected deliv. | Worst deliv. | Headroom (expected) | Verdict |
|---|---:|---:|---:|---:|---|
| S1 threshold/ratchet | $128.30 | **$571.88** | $1,369.98 | −$71.88 | OVER |
| S2 planar tiles | $189.20 | **$586.96** | $1,465.44 | −$86.96 | OVER |
| S3 multi-row DMA | $1,029.63 | **$2,880.98** | $6,187.87 | −$2,380.98 | OVER, decisively |
| S4 shared-bus tiles | $204.11 | **$548.91** | $1,210.02 | −$48.91 | OVER |
| S5 rotary reference | $389.55 | **$592.06** | $1,153.52 | −$92.06 | OVER |

- **S4 is closest** (−$48.91) and **S5 next** (−$92.06); both fail only because
  of bought fallback parts their designs intend to *print* (tile couplers) or
  because the critical motor/driver quotes are not matched.
- **S3 has no cost path at all**: 320 selectors at even a speculative $5 each are
  $1,600, so expected delivered is 5.8× the ceiling.
- **Best-case totals are all under $500** — but only by assuming the cheapest
  untraced marketplace prices, the most favourable consolidation, *and* that every
  printable fallback part really prints and works. That assumption is exactly the
  unproven printability/reliability question.

## Evidence mix (expected-case delivered total)

| Candidate | Sourced share | Assumed share |
|---|---:|---:|
| S1 | 30% | 70% |
| S2 | 28% | 72% |
| S3 | 24% | 76% |
| S4 | 37% | 63% |
| S5 | **82%** | 18% |

S5 is by far the best-evidenced BOM (its motors, drivers, controller, registers,
rods, screws, power, connectors and fasteners all carry a live source or listing).
S1–S4 are dominated by unquoted coupling / selection / programmer allowances,
which is itself a finding: **their cost numbers are less trustworthy than S5's**.

## The two critical lines (S5, 80 channels each)

`PM motor` and `Dual H-bridge channel` decide whether S5 has any sub-$500 path.
Expected-delivered totals over the sourced price grid:

| motor $/ea ↓ \ driver $/ea → | TB6612 $0.80 | DRV8833PWPR $1.33 | Test08 $0.60 | DRV8833PWR@1 $2.39 |
|---|---:|---:|---:|---:|
| Amazon multipack $1.05 *(sourced listing)* | **$501.12** | $550.66 | $482.56 | $648.42 |
| Test08 allowance $1.25 | $519.68 | $569.22 | $501.12 | $666.98 |
| AliExpress $2.66 | $650.53 | $700.06 | $631.97 | $797.83 |
| AliExpress $3.00 (worst) | $682.08 | $731.62 | $663.52 | $829.38 |
| MOONS matched $40.00 | $4,115.68 | $4,165.22 | $4,097.12 | $4,262.98 |

**Only the sourced multipack motor plus the cheapest sourced matched bipolar
driver lands under $500 delivered — at $501.12, i.e. essentially on the ceiling
with no margin.** The single *traceable matched* 8 mm PM stepper (MOONS) puts S5
above $4,000 delivered. Test08's `$1.25` motor and `$0.60` driver remain
**unmatched allowances**; `$0.60` is below the cheapest sourced matched bipolar IC
(TB6612FNG $0.80 @100).

## Per-cell bought-hardware sensitivity (mechanism-independent)

| $/cell | Added for 6,400 cells | Room left below $500 |
|---:|---:|---:|
| $0.05 | $320 | $180 |
| $0.10 | $640 | **−$140** |
| $0.25 | $1,600 | −$1,100 |
| $0.50 | $3,200 | −$2,700 |
| $1.00 | $6,400 | −$5,900 |

**Any bought part required once per cell kills the budget.** At $0.10/cell the
board is already $140 over before motors, power or structure. This is the
strongest, most portable result in the test: it does not depend on which
mechanism wins. Survivors must keep the per-cell layer **printed or passive**.

## What would change the answer

- A **traceable matched 8 mm motor quote** (sample + 80+spares, same winding,
  shaft, step angle, lot) near $1.00 delivered-inclusive. Until that exists, S5's
  expected number is a range ($501–$670), not a point.
- A **sub-$0.60 matched bipolar driver** or a validated dual-channel module.
- Proof that the **printed tile coupler / latch / decoder** works across thousands
  of cells, which removes the 64×$3 fallback from S1/S4.
- Real **shipping/tax invoices** to replace the uplift assumptions.

## Limits

No part bought, printed or measured. Prices are point-in-time listings
(2026-09-28) and volatile; DigiKey/Mouser/Octopart were unreachable from this
run (403), so their prices appear only as aggregator estimates in the parent
sourcing notes. The delivered uplifts are assumptions, not invoices. Printed-part
cost is excluded by project rule but print time, machine wear, creep and assembly
labour are not free and are treated in the parent Test11 write-up.
