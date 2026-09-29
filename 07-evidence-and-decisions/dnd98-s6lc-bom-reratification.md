# DND-98 — independent re-ratification of the corrected S6-LC purchased BOM

- **Issue:** [DND-98](/DND/issues/DND-98) (Cost, BOM & Manufacturing Engineer). Parent the
  ultra-low-cost track [DND-70](/DND/issues/DND-70); corrected by [DND-93](/DND/issues/DND-93).
- **Supersedes:** [DND-73](/DND/issues/DND-73) `dnd73-s6lc-bom-ratification.md`, which ratified the
  *uncorrected* S6-LC BOM ($139.77 parts / $162.13 delivered / $87.87 margin). DND-93 repaired the
  lift axis (DND-74 branch 1: keep the global broadcast, upsize to a NEMA23-class motor) and added
  the six honest DND-91/A5 capability allowances; this document re-ratifies that corrected BOM
  independently and re-states the ceiling verdict.
- **Target of record:** `09-low-cost-variant/s6lc/bom_s6lc.csv` (20 lines) and
  `09-low-cost-variant/s6lc/analysis/s6lc.py:bom()`.
- **Evidence class:** **sourced listings + CALCULATION** only. No purchase, no print, no measurement
  ([DND-27](/DND/issues/DND-27)). No board contact ([DND-32](/DND/issues/DND-32)). `08-current-design/`
  untouched.
- **Gate:** `09-low-cost-variant/s6lc/ratify/s6lc_bom_reratify_checks.py` (CI-wired).
- **Reproduce:**
  ```bash
  python 09-low-cost-variant/s6lc/ratify/s6lc_bom_reratify.py            # full report
  python 09-low-cost-variant/s6lc/ratify/s6lc_bom_reratify.py --selftest
  python 09-low-cost-variant/s6lc/ratify/s6lc_bom_reratify_checks.py
  ```

## 1. Engineering question

Does the **corrected** S6-LC purchased BOM — after DND-93 fixed gate G3 (upsized the lift axis to a
NEMA23-class motor, keeping the global broadcast) and added the six DND-91/A5 capability allowances —
still hold the board ceiling, and if not, which ceiling and which requirement must move? The issue
requires an explicit statement of the **`<$250 purchased, excluding 3D-printed parts`** gate
(DND-70 / DND-72) under working and hostile pricing.

## 2. Headline (re-derived line by line, by hand, not imported)

| Figure | Value | Class |
|---|---:|---|
| Purchased parts | **$226.77** | CALCULATION over sourced + allowance lines |
| Delivered (×1.16 additive, DND-41) | **$263.05** | CALCULATION |
| **Purchased margin to $250** | **+$23.23** | CALCULATION — **mission gate HOLDS** |
| Delivered margin to $250 | **−$13.05** | CALCULATION — repo convention **FAILS** |

The re-derivation reproduces the DND-93 headline exactly and reconciles with `s6lc.bom()` and the
committed CSV. There is **no discrepancy** to report.

### The two ceilings are not the same gate

- **Mission gate (DND-70):** *"purchased-component cost under $500"* at goal level, tightened by the
  DND-72 ultra-low-cost track to **<$250 purchased, excluding 3D-printed parts**. **$226.77 clears it**
  with **+$23.23** margin.
- **Repo delivered convention (DND-41):** the additive ×1.16 delivered number compared to $250.
  **$263.05 does not clear it** (−$13.05).

DND-98 states both and does not fold one into the other. DND-93's model flags G6 (`clears_delivered`)
red, G5 (`clears_parts`) green — this ratification confirms that exactly.

## 3. Where the +$87.00 growth came from (DND-73 → DND-93)

| Source | Amount |
|---|---:|
| Lift motor re-price NEMA17 $12 → NEMA23 $30 (global-board lift needs ≥2.2 N·m) | **+$18.00** |
| Six DND-91/A5 capability lines (mask index mechanism $15, carriage rail $20, thrust bearings $18, homing switches $3, cable chain $8, power protection $5) | **+$69.00** |
| **Total** | **+$87.00** |

$139.77 + $87.00 = **$226.77**. All six A5 lines are `allowance`-class (no retrieved listing) and
total **$69.00**. The remaining 14 lines are unchanged from the DND-73-ratified BOM.

## 4. Evidence-class audit

| Class | $ | Share |
|---|---:|---:|
| Traced (live/committed) | $79.77 | 35 % |
| Allowances (no retrieved trace) | $147.00 | 65 % |
| — of which DND-91/A5 capability | $69.00 | 30 % |

The corrected BOM is **majority allowance**. The traced critical lines re-audited 2026-09-29:

| Line | BOM unit | Cheapest matched trace | Delta |
|---|---:|---:|---:|
| Lift motor (NEMA23, ≥2.2 N·m) | $30.00 | $24.99 (23HS5628, 2.0 N·m) | −$5.01 |
| Mask index small stepper | $8.00 | $3.31 (28BYJ-48 + ULN2003) | −$4.69 |
| Reset carriage small stepper | $8.00 | $3.31 | −$4.69 |
| 4× T8 lead screw + nut | $24.00 | $28.76 (4 × $7.19 stable tier) | **+$4.76** |
| Stepper driver (DRV8833) | $1.59 | $0.74 | −$0.85 |

Note the lead-screw line: the DND-73 Q7 lesson holds — the $3.49 listing is a **flash price, not
orderable**; the stable order tier is $7.19/screw, i.e. 4 × $7.19 = $28.76, so the corrected BOM's
$24.00 line is **under-priced by ~$4.76** against the stable tier. This is the one line where the
committed BOM is *optimistic*, and it is carried forward honestly rather than re-priced (DND-93 kept
the line at $24). If it were marked to the stable tier the parts would be $231.53 (still under $250).

## 5. Break-even unit prices ($250 purchased ceiling)

Holding every other line fixed, the unit price at which each line alone breaches $250 purchased:

- **Tightest line: the lift motor** — BOM $30.00, cap **$53.23** (**1.77×**).
- Next tightest: the lead-screw set $24.00 → cap $47.23 (1.97×); carriage rail $20 → cap $43.23
  (2.16×); thrust bearings $18 → cap $41.23 (2.29×); mask mechanism $15 → cap $38.23 (2.55×).
- Every other line has **>2.6×** headroom.

**The cost cliff is now the lift motor** (1.77× break-even on the purchased ceiling, and only
1.35× torque margin — see DND-93 §1), followed by the lead-screw set. There is no line with <1.7×
headroom, so a single moderate price rise does not break the gate; but the total headroom is only
$23.23, so **two** moderate rises can.

## 6. Scenarios

| Scenario | Parts | Delivered | Clears $250 **purchased**? |
|---|---:|---:|---|
| Optimistic (cheapest matched traces) | $199.79 | $231.76 | **yes** |
| **Working (committed corrected BOM)** | **$226.77** | **$263.05** | **yes** |
| High (premium matched traces; allowances ×1.5) | $245.61 | $284.91 | **yes** (thin) |
| Lean (working, A5 allowances ×0.5, cheapest NEMA23) | $187.26 | $217.22 | **yes** |
| **Hostile (premium traces; allowances ×2.0)** | **$300.58** | $348.67 | **NO (−$50.58)** |

**Finding:** the corrected BOM clears the $250 **purchased** ceiling under working, high, optimistic
and lean pricing, but **hostile pricing breaches it by $50.58**. On the stricter *delivered*
convention it fails even at working pricing ($263.05, −$13.05).

## 7. Per-cell bought-hardware sensitivity

The corrected S6-LC has **zero per-cell purchased hardware**; the only bought actuators are **three
motors** (lift, mask index, reset carriage). The ceiling is therefore a **fixed-base** problem, not a
per-cell one:

- whole purchased BOM = **3.543 cents/cell** amortised over 6,400 cells;
- purchased headroom = **0.363 cents/cell**;
- headroom buys a per-cell bought part of at most **$0.0036** before the purchased ceiling breaks.

This is the key scaling fact: *any* move to per-cell or per-row bought actuation multiplies the base
by ~6,400 and kills the ceiling immediately. S6-LC's whole reason for existing is that it has none.

## 8. Reliability and assembly scaling

A map is correct only if **all 6,400 cells** are correct; with per-cell error `q`, yield `(1−q)^6400`.

| q | Map yield | Expected bad cells |
|---:|---:|---:|
| 1e−3 | 0.17 % | 6.4 |
| 1e−4 | 52.73 % | 0.64 |
| 1e−5 | 93.80 % | 0.064 |
| **1.57e−6** | **99.00 %** | 0.010 |
| 1e−6 | 99.36 % | 0.006 |

The **99 %-map goal needs `q ≤ 1.57e−6`**, which S6-LC cannot demonstrate without measurement
(G7 is explicitly **UNRESOLVED** in DND-93; the evidence path is printed coupon C1). Assembly and
replaceability must therefore be designed around field repair: the replaceable units are the printed
column, the printed pawl/leaf, the **10-row bank sub-tile**, the release comb (per bank) and the mask
card (per map). A failed cell is swapped by pulling its bank sub-tile, **not** by re-printing the
406 mm frame. Bought spares are a single $8 allowance line.

## 9. Verdict

**The `<$250 purchased` mission gate HOLDS for the corrected S6-LC at $226.77 (margin +$23.23).**
The repo's stricter $250 *delivered* convention **FAILS** at $263.05 (−$13.05) — stated, not hidden.
This confirms DND-93's corrected verdict **REJECT on G6 (delivered)**, with G5 (purchased) green.

Honest remaining gaps:

1. **The delivered shortfall is $13.05**; clearing it on the delivered convention needs **$11.25 of
   purchased parts shed** ($226.77 → $215.52). The lead-screw line alone is under-priced by ~$4.76
   against its stable order tier, so the true delivered figure is arguably ~$268.57.
2. **Hostile pricing breaches the purchased ceiling** ($300.58, −$50.58). The purchased margin
   ($23.23) is thin and the lift motor is the tightest line (1.77× break-even).
3. **65 % of the BOM is allowance**, of which $69.00 is the DND-91/A5 capability stack with no
   retrieved listing. If any A5 allowance is materially under-priced, the purchased gate breaks.
4. **G7 per-cell reliability is UNRESOLVED** (measurement-only, DND-27) and is the real risk to the
   product, not cost.

**What must move if the delivered convention must be met:** shed ~$11.25 of purchased parts (the six
A5 allowances and the lead-screw/guide-rod lines are the targets), or accept the ×1.16 delivered
uplift as a shipping/tax convention rather than a design requirement. **No design requirement needs
to move for the purchased mission gate.** For completeness: the unmerged alternative repair on branch
`cto/dnd93-fix-s6lc-g3` (branch C: keep the NEMA17, re-derive the lift load to ~0.05 N/column) would
price at $238.77 purchased / $276.97 delivered — **worse on both bases** than the branch-1 repair
ratified here, so branch 1 is the cost-preferred and adopted definition.

## 10. What this changes for the program

- The DND-73 ratification is **superseded**; the ratified BOM artifact is now
  `09-low-cost-variant/s6lc/ratify/s6lc_bom_ratified.csv` ($226.77 / $263.05).
- The DND-93 verdict **REJECT (G6 delivered)** is confirmed at the cost boundary: the *purchased*
  mission gate is green (+$23.23), the *delivered* convention is red (−$13.05), and reliability
  remains the measurement gate.
- No change to `08-current-design/`. No board contact.
