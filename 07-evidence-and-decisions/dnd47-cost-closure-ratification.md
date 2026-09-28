# DND-47 — Independent ratification of the DND-44 machine-preserving cost closure

- **Verdict:** **RATIFIED WITH A QUALIFICATION.** The arithmetic reproduces exactly;
  the $424.95 delivered path is real **as a best-case-priced reduction**, and the
  $1.86 motor break-even is confirmed. The qualification is scenario consistency:
  $40.60 of the $75.05 margin comes from repricing four fixed lines from the BOM's
  `unit_expected` to its `unit_best` column (E6), and a further $16.00 from moving
  the motor from expected $1.25 to best-case $1.05 (E2). The path no longer clears
  if those two best-case moves are removed and the motor is bought at the honest
  expected price. The **binding residual remains K7** (no matched sub-$1.86 motor).
- **Owner:** Cost, BOM & Manufacturing Engineer (CostManufacturing).
- **Issue:** [DND-47](/DND/issues/DND-47), for [DND-44](/DND/issues/DND-44).
- **Inputs:** `06-experiments/test11_cost_printability_reliability/delivered_3scenario/bom_S5_delivered.csv`
  (committed on `main`); the DND-44 closure claim in the issue text; the CTO's
  in-flight `test12_winner_convergence/cost_closure.py` (uncommitted on branch
  `dnd44-readiness-closure`, read for cross-check, **not imported**).
- **Evidence class:** CALCULATION over sourced listings and stated assumptions.
  **No part was bought, printed or measured** ([DND-27](/DND/issues/DND-27)).

The independent re-derivation lives in
`06-experiments/test12_winner_convergence/cost_closure_ratify.py`. It reads the
committed CSV line-by-line and does **not** import `cost_closure.py`, so a
discrepancy between the DND-44 claim and the data is visible rather than inherited.
Run `python cost_closure_ratify.py` (report) or `--selftest` (asserts every figure
below).

## 1. What was checked

| # | Question | Method | Result |
|---|---|---|---|
| Q1 | Is the honest **expected** baseline $592.06 / parts $510.40? | Re-sum the `unit_expected` column × qty, ×1.16 additive | **MATCH** — $510.40 / $592.06 |
| Q2 | Does the E1–E6 path reproduce at $424.95 / margin $75.05? | Apply E1–E6 independently to the CSV | **MATCH** — $366.34 / $424.95 / $75.05 |
| Q3 | Is the motor break-even $1.86? | Solve `(500/1.16 − fixed_other)/80` from the CSV | **MATCH** — **$1.8587** |
| Q4 | Are E1–E6 scenario-consistent? | Split the margin by evidence class | **QUALIFIED** — see §3 |
| Q5 | Does any reduction change the machine? | Structural-line presence + topology check | **PASS** — no line removed |
| Q6 | Is the dual-H-bridge count right? | Compare line qty to motors-per-IC | **FINDING** — 40 IC surplus (conservatism) |

## 2. The claim reproduces, line by line

| Reduction | Item | Δ parts | Evidence class |
|---|---|---:|---|
| E1 | Driver → TB6612FNG @100 $0.7955 | −$62.76 | SOURCED-live (LCSC C88224) |
| E2 | Motor → multipack $1.05 | −$16.00 | SOURCED-listing (**K7 risk**) |
| E3 | Registers folded to PCB, chips still bought @$0.0925 | −$10.30 | SOURCED-live (LCSC C5947) |
| E4 | Controller → RP2040 $5.00 | −$5.00 | SOURCED-live (LCSC C2040) |
| E5 | Spares allowance deleted | −$15.00 | purchasing choice, not machine |
| E6 | 4 fixed lines → their `unit_best` | −$35.00 | **mixes best-case into an expected total** |
| | **Total** | **−$144.06** | |

Baseline parts $510.40 − $144.06 = **$366.34**; ×1.16 = **$424.95** delivered,
**$75.05** below the ceiling. At the pessimistic AliExpress motor $2.66 the same
path is **$574.36** ($74.36 over). Break-even **$1.8587**.

## 3. The qualification: E6 + E2 are best-case-priced lines

The BOM carries three explicit scenarios. The "honest expected" baseline uses the
`unit_expected` column. The reduction path, however, takes E6's four lines from
`unit_expected` **down to `unit_best`**, and E2 takes the motor from expected
$1.25 to best-case $1.05. Those two moves alone are **$40.60 + $16.00 = $56.60 of
the $75.05 margin**.

| Path | Parts | Delivered | Margin | Clears? |
|---|---:|---:|---:|---|
| DND-44 E1–E6 (as claimed) | $366.34 | $424.95 | $75.05 | yes |
| E1–E5 only (fixed lines stay expected) | $401.34 | $465.55 | $34.45 | **yes, still** |
| E1–E5 + expected motor $1.25 | $417.34 | $484.11 | $15.89 | yes, thin |

Interpretation: **E6 is not a sourcing change — it is a re-labelling of existing
"bundled allowance" lines to their optimistic column.** It is defensible only if
those `unit_best` values are treated as the *expected* delivered price, which the
BOM does not assert (their `basis` strings say "bundled allowance"). The path does
**not** die without E6 (it still clears by $34.45), and it survives even with the
expected-priced motor. So E6 is a **magnitude risk, not a validity risk**. The
honest headline for the machine-preserving path is therefore a **range
$424.95–$465.55**, not a single $424.95.

## 4. What is legitimate (independent conclusions)

- **E1 (TB6612FNG) is a legitimate matched driver.** TB6612FNG is a dual H-bridge,
  VM 2.5–13.5 V, 1.2 A continuous per channel. The 8 mm 18° PM stepper is a 5–6 V,
  ~0.25 A bipolar part — well inside both ratings. It is a **dual** bridge, so one
  IC drives **two** motors. Sourced `$0.7955 @100` (LCSC C88224) is consistent with
  `sourcing_notes.md §2`.
- **E3/E4 reproduce the DND-41 net-saving method** ($10.30 register, $5.00
  controller). No double-count: the register chips remain in the BOM at $0.0925.
- **E5 (spares) is honest.** Spares are replacement stock, not part of the buildable
  machine. Removing the allowance does not change the machine and is not a
  hidden cost deletion.
- **Q5 — machine preservation holds.** No structural line is removed: motor count
  (80), driver count, lift/scanner motors, rails, screws, belts, power, loom, head
  shafts and fasteners all remain. Pitch (5.08 mm), cell count (6,400), travel
  (40 mm) and drive topology are untouched by every reduction.

## 5. Independent finding — the dual-H-bridge line over-buys by ~$36.91

The BOM line `Dual H-bridge channel (DRV8833PWPR bare IC or module)` has
**quantity 80** — the motor count — but the priced part (DRV8833 / TB6612FNG) is a
**dual** bridge, so 80 motors need **40 ICs**. Pricing 80 ICs at the per-IC price
carries a **surplus of 40 ICs = $36.91 delivered** (40 × $0.7955 × 1.16). This
conservatism works **against** the design (it inflates cost), so it does not
threaten the <$500 claim; if the count is corrected the path gains ~$37 of extra
margin. Recorded so the number is not accidentally "fixed" in the wrong direction
(pricing 40 ICs at a *per-channel* rate would be a different, incorrect case).

## 6. Residual untraced lines

| Line | Status | Why it matters |
|---|---|---|
| PM motor @ ≤$1.86 | **untraced multicast** | No distributor stocks a true 8 mm 18° bipolar PM stepper. MOONS 8PM020S1 = $40/ea; the $1.05 multipack is an unqualified marketplace listing. **Binding residual (K7).** |
| E6 fixed lines (rods, belts, head shafts, fasteners) | allowance → best-case | `unit_best` is a listing/allowance, not a volume quote; no 80-unit contract price exists. |
| Lift/scanner motors, coupling, axis drivers | ASSUMPTION | No matched quote; small relative cost (≤$46 total). |
| Driver PCBs, wiring, power | partly sourced / allowance | Bundled; not individually quoted. |

## 7. Verdict and next test

**RATIFIED WITH QUALIFICATION.**

- The DND-44 arithmetic is **correct and independently reproduced** — $592.06
  baseline, $424.95 path, $75.05 margin, $1.8587 break-even, $574.36 downside.
- The path is a **best-case-priced** path; its honest range is **$424.95–$465.55**.
  It clears the $500 ceiling on every variant tested, so the **claim stands**; the
  margin is simply smaller and more conditional than the single headline number.
- **K7 is unchanged and binding:** the path is only as real as the motor price, and
  no matched sub-$1.86 motor supply exists. This is a purchasing/sample-verification
  risk that cannot be closed without buying a part ([DND-27](/DND/issues/DND-27)).
- **Next test:** a single traceable motor sample + 80+spare delivered quote with the
  same winding, step angle, shaft and lot (the Test09 Stage C procurement gate).
  Until then, treat the S5 purchased cost as **$424.95–$574.36 delivered** (best-case
  path to realistic-motor downside).
