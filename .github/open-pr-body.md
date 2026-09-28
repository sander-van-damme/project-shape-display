# Test11 — purchased-BOM, sourcing, printability and reliability scaling for S1–S5

Imports the CostManufacturing deliverables [DND-6](/DND/issues/DND-6) (Test11) and
[DND-11](/DND/issues/DND-11) (three-scenario delivered BOM) onto latest `main`.

## What changed

Adds `06-experiments/test11_cost_printability_reliability/` (with a
`delivered_3scenario/` sub-folder) and updates three READMEs.

- **New** `06-experiments/test11_cost_printability_reliability/`
  - `README.md` — question, evidence level, method, per-candidate results
  - `sourcing_notes.md` — dated (2026-09-28) critical-part prices with links/retrieval status
  - `bom_S1.csv` … `bom_S5.csv` — per-survivor purchased-BOM, every line labelled sourced vs allowance
  - `cost_model.py` — 3 scenarios × per-cell sensitivity × print-intent floor × S5 sourcing sensitivity
  - `print_reliability.py` — 5.08 mm printability, tolerance stack, print-farm throughput, reliability/assembly scaling
  - `checks.py` — 16 deterministic arithmetic checks (all pass)
- **New** `06-experiments/test11_cost_printability_reliability/delivered_3scenario/`
  (DND-11)
  - `README.md` — best / expected / worst **delivered** scenarios, headroom vs the $500 ceiling
  - `bom_S1_delivered.csv` … `bom_S5_delivered.csv` — per-line part, qty, unit, total, vendor, evidence label
  - `delivered_cost_model.py` — applies per-scenario shipping/tax uplift to list prices
  - `checks.py` — 18 delivered-BOM arithmetic checks (all pass)
- **Edited** `06-experiments/README.md`, `07-evidence-and-decisions/README.md`,
  `08-current-design/README.md` — register Test11 and the delivered BOM in the
  experiment index and evidence matrix.

## Engineering question addressed

For every architecture survivor S1–S5: what does the **bought** hardware actually
cost — list and **delivered** — in best/expected/worst scenarios; what real parts
can be sourced today at what price; what does 5.08 mm pitch cost in printability;
and how do per-cell failure and assembly scale against the product targets
(<$500 purchased cost, 6,400 cells, ≥99% map, <30 s full-map update)?

## Evidence produced

Cost-model arithmetic + sourced listing prices + printability/reliability
*screens*. **No physical measurement, no supplier quotation, no purchase.**
Every "sourced" line cites a link and observation date in `sourcing_notes.md`;
everything else is an engineering allowance, labelled `assumption`.

Reproduce (standard library only, Python 3.11+):

```
python 06-experiments/test11_cost_printability_reliability/cost_model.py
python 06-experiments/test11_cost_printability_reliability/print_reliability.py
python 06-experiments/test11_cost_printability_reliability/checks.py
python 06-experiments/test11_cost_printability_reliability/delivered_3scenario/delivered_cost_model.py
python 06-experiments/test11_cost_printability_reliability/delivered_3scenario/checks.py
```

## Assumptions

- Unit prices are optimistic / working / high, plus 20% contingency in the parent model.
- Delivered scenarios apply an uplift assumption to the parts subtotal:
  best +5% shipping / +0% tax; expected +10% / +6%; worst +18% / +11%.
- Categories follow Test09's `uncategorized` split.
- "Sourced" means a link and observation date exist; no quotation confirmed.
- The print-intent floor assumes every part intended to be printed is printed and
  works — it is not a qualification.
- Reliability screen assumes independent per-cell Bernoulli trials.

## Calculations run / results

### Parent model (list, working allowances +20%)
No survivor has a credible sub-$500 path: **S1 $621.60 · S2 $643.20 · S3 $3,022.32 ·
S4 $603.84 · S5 $518.40.**

### Delivered model (DND-11, best/expected/worst)
**Every survivor is over the $500 ceiling in the expected scenario, delivered:**
**S1 $571.88 · S2 $586.96 · S3 $2,880.98 · S4 $548.91 · S5 $592.06.**
S4 is closest (−$48.91), S5 next (−$92.06); both fail only because bought
fallback parts their designs intend to print, or because the motor/driver quotes
are unmatched. S3 has no cost path at all.

### Cross-cutting
- **Any bought part on all 6,400 cells kills the budget:** $0.10/cell adds $640;
  $0.05/cell leaves only $180 for everything else. Mechanism-independent.
- **Sourced critical parts make it worse:** the only traceable 8 mm 18° bipolar PM
  stepper (MOONS) is $40/ea → $3,200 for 80 motors. No commodity bare 8 mm PM
  stepper exists in LCSC/DigiKey/Mouser/Adafruit/Pololu/DFRobot. Sourced
  DRV8833/TB6612 drivers are $0.80–1.33 @100, above Test08's $0.60 allowance.
- **5.08 mm pitch is a fine-nozzle/resin problem**, not a 0.4 mm-nozzle problem.
- **A 99% perfect-map goal needs q ≤ 1.57e-6 per cell-update and ~1.91M
  zero-failure trials** — far beyond any six-cell prototype. Per-cell bought
  hardware at 0.1% rejects already exhausts the allowance.
- S5 **reproduces the Test08 BOM exactly** ($276/$432/$783), anchoring both models.

## What passed / failed

- `checks.py` (parent): **16/16 PASS**, including S5 base reproduction of Test08.
- `delivered_3scenario/checks.py`: **18/18 PASS**, including monotonicity
  best ≤ expected ≤ worst for all survivors and the $0.10/cell identity.
- `cost_model.py`, `print_reliability.py`, `delivered_cost_model.py`: run clean, exit 0.
- **Failed by design (the point of the test):** all five survivors fail the
  sub-$500 working-allowance and expected-delivered screens. S3 fails decisively.

## What remains uncertain

- No supplier quotation for any part; the $1.25 motor has **no traceable matched
  quote**.
- Marketplace multipack motor specs (winding, shaft, lot) are unverified.
- No printed-tolerance or measured-reliability data; printability/reliability
  results are screens, not measurements.
- S1/S2/S4 have a plausible sub-$500 path **only if** their printed
  memory/selector layers work — unproven.

## Most informative next test

Obtain a matched quotation for the cheapest credible 8 mm 18° bipolar PM stepper
and driver (the S5 critical path), and print the 5.08 mm-pitch coupon from
Test11's tolerance section to convert the fine-nozzle/web floor from a screen to
measured process capability. Sourcing is now a **first-class program blocker**,
not a footnote.

---

Branch imports CostManufacturing commit `bf6e78d`; applied to `main` @ `101803d`.
Commit chain: `435d09d` (Test11) → `045958f`/`2735bd5` (DND-11 delivered BOM).
