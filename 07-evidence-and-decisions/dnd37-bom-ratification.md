# DND-37 — S5 winner purchased BOM + printability ratification

> ## ⚠ DND-41 correction (authoritative — supersedes §1–§2, §8–§9 figures below)
>
> A later reconciliation ([DND-41](/DND/issues/DND-41), merged to `main` as the
> DND-41 branch) found **two** defects in the cost arithmetic, both now fixed in
> `model.py` / `checks.py` / `ratify_bom.py`. Use these figures:
>
> | Figure | Corrected value (DND-41) | This doc's earlier value |
> |---|---:|---:|
> | Sourced-pair delivered | **$501.12** ($432.00 parts × **1.16**) | $503.71 (×1.166, double-counted) |
> | Reduced path delivered | **$483.37** ($416.70 parts × 1.16) | $493.57 (wrong register method) |
> | Net register saving | **$10.30** ($14.00 allowance − $3.70 chips still bought) | stated as $3.70 |
>
> 1. **Uplift basis.** The repo's own `delivered_3scenario/delivered_cost_model.py`
>    applies the expected uplift **additively** (`sub + sub·0.10 + sub·0.06 = ×1.16`).
>    The earlier `(1.10)(1.06)=1.166` compounded and inflated every headline.
>    On the additive basis the sourced pair is **$501.12 — over the ceiling by $1.12**.
> 2. **Register method.** The $14 expected allowance leaves the BOM but the 40 chips
>    are still **bought** at $0.0925 → net saving **$10.30**, so honest reduced parts
>    are $284.00 − $10.30 − $5.00 + $148.00 = **$416.70** → **$483.37** delivered,
>    clearing the ceiling by **$16.63**, not $6.43.
>
> The residual risks below (matched-motor supply, thin contact features = K2 class)
> are **unchanged and still open**. `checks.py::test_ratify_bom_agrees_with_model_on_the_headline_costs`
> now pins `model.py` and `ratify_bom.py` together so they cannot diverge again.

- **Verdict:** **RATIFIED with one arithmetic correction and one unretired cost risk.**
- **Owner:** Cost, BOM & Manufacturing Engineer (CostManufacturing).
- **Issue:** [DND-37](/DND/issues/DND-37), for [DND-35](/DND/issues/DND-35).
- **Inputs:** `06-experiments/test11_cost_printability_reliability/delivered_3scenario/bom_S5_delivered.csv`,
  `06-experiments/test12_winner_convergence/model.py`, `sourcing_notes.md`,
  `tools/validate/analytic_printability.py`, `tools/fdm-limits/fdm_process_limits.py`.
- **Evidence class:** CALCULATION over sourced listings and stated assumptions.
  **No part was bought, printed or measured** ([DND-27](/DND/issues/DND-27)).

## 1. What was checked and what the numbers are

An independent re-derivation lives in
`06-experiments/test12_winner_convergence/ratify_bom.py` (does not import the
convenience constants from `model.py`). Run it:

```text
python 06-experiments/test12_winner_convergence/ratify_bom.py
```

| Check | Claim in ADR-002 / `08-current-design` | Independently re-derived | Verdict |
|---|---|---|---|
| Fixed (non motor/driver) expected subtotal | $284.00 | $284.00 from the CSV expected column | **matches** |
| Sourced-pair delivered ($1.05 motor + $0.80 TB6612, unchanged fixed) | $503.71 | $503.71 | **matches** |
| Reduced path delivered (registers on-PCB + sourced RP2040) | **$481.56** | $481.56 *as coded*, but see §2 | **arithmetic correct, method overstates saving** |
| Fully expected (BOM as written, no sourcing) | not stated | $595.13 | reference |
| Required per-cell q for 99 % correct map | ≤1.57×10⁻⁶ | 1.570×10⁻⁶; P(all) at q=1e-4 = 52.7 % | **matches** |

## 2. The one arithmetic defect: the register consolidation double-counts

`model.py` builds the reduced path as
`fixed − $14 (registers) − $5 (controller) + 80·$1.05 + 80·$0.80`, then applies
the ×1.16 delivered uplift. The $14 register saving is the line's **expected
allowance** (40 × $0.35). But the surrounding base has been re-priced to
**sourced** values, and the sourced LCSC price for the 74HC595D is **$0.0925 @50
→ $3.70** for 40. Folding the registers onto the driver PCB removes the part you
would actually have bought, so the honest saving on that line is **$3.70, not
$14** — an overstatement of **$10.30**. (The controller consolidation is sound:
$10 expected allowance → $5 sourced = a real $5 saving.)

**Corrected, defensible delivered total: $493.57** (parts $423.30 × 1.16) — still
under the $500 ceiling, but with **$6.43 margin, not $18.44**. The winner remains
inside the "last-resort" ($400–500) band.

This is a *conservatism* defect, not a fatal one: the design still clears $500 on
the sourced pairing. It must be recorded so no downstream reader treats $18.44 as
real headroom.

## 3. Can any sourced reduction reach the <$400 ideal band? **No.**

- The only remaining large block is the fixed non-motor/non-driver $284, and
  **82 % of the S5 BOM is already sourced at its cheapest observed price**. The
  18 % assumed remainder (driver PCBs, scanner/lift motors, belts, sensors,
  spares) are engineering allowances with no lower sourced alternative on record.
- The motor + driver channel is $148 of the $434 sourced subtotal and is already
  at the cheapest sourced unit prices ($1.05 + $0.80). Halving both would save
  only ~$74 delivered — not enough to reach $400, and no such part exists.
- **Reaching <$400 is not demonstrated on any sourced path without a new,
  unproven part.** This is the honest statement the ADR already makes; the
  ratification confirms it.

## 4. Matched-motor risk: unchanged and now better evidenced

The critical open question was whether a **sourced, matched** 8 mm 18° bipolar PM
stepper near $1.00 delivered-inclusive exists. Live checks on 2026-09-28:

| Source | Finding | Evidence |
|---|---|---|
| Octopart (aggregates DigiKey, Mouser, Farnell, Newark, Arrow) | Query "8mm stepper motor" returns **only** large NEMA/hybrid frames (e.g. QSH6018 €114+) and €268–503 integrated PANdrives. **No true 8 mm-diameter PM bipolar stepper is stocked** by any mainstream distributor. | SOURCED (live page) |
| MOONS online shop | `8PM020S1-02001`, 8 mm, 18°, bipolar, 0.4 mN·m holding / 0.15 mN·m detent → **$40.00 EA**. The only *traceable matched* part. | SOURCED (live product page) |
| AliExpress "8mm stepper motor" | Genuine micro listings exist: "Micro Mini 8 mm 2-phase 4-wire" **€2.66 ea** (1k+ sold); "8 mm/10 mm 2-phase 4-wire screw-slide micro stepper" **€3.59 ea**; "10 pcs 3–5 V 2-phase 4-wire dia 8 mm, 8×9.5 mm" **€7.89/10 → €0.79 ea** (143 sold). | SOURCED (live listing page) |
| Amazon "Abovehill" multipack | ≈EUR 0.97 ea (the $1.05 line's basis) | SOURCED (prior run) |

**Residual risk, stated precisely:** the sub-$1.05 price is a **marketplace
multipack with no datasheet-matched step angle, winding, shaft or lot**, and no
distributor stocks a matched part. The *only* traceable matched part is $40/ea,
which alone puts the machine at ~**$4,156 delivered** (~$3,200 for the motors).
The cheapest *credible* sub-$500 path therefore depends on **one unqualified
supply line**: a marketplace 8 mm PM stepper that must be sample-verified
(step angle, holding/running torque ≥0.15 mN·m at 400 pps, shaft, lot) before any
build. This cannot be closed analytically and is **not closed by this
ratification**.

> Note: no single untraced listing reaches a *qualified* $1.00 delivered-inclusive
> matched part. The listing band (€0.79–3.59) brackets $1.05 but is not a
> guarantee. Treat the motor price as a **range $1.05–$3.00** until a lot is
> sampled; at $2.66 the honest delivered total is ~**$646**.

## 5. Printability route — ratified with caveats

**Route:** Bambu X1C, PLA, **0.4 mm nozzle**, 0.20 mm layers, modular cartridges.
Assessed against `tools/fdm-limits/fdm_process_limits.py`
(min feature 0.44 mm = one 1.1×nozzle line; robust wall 0.88 mm; load-bearing wall
1.32 mm; FDM dimensional accuracy ±0.1 mm).

The winner's declared printed features (`test08_architecture_search/params.json`):

| Feature | Value | vs 0.4 mm floor | Note |
|---|---:|---|---|
| detent thickness | 0.45 mm | **just above** 0.44 mm min | at the floor; the guiding 0.2 mm-nozzle candidate |
| body wall | 0.60 mm | above min, **below** 0.88 robust | hollow-body variant only |
| stem thickness | 0.70 mm | above min, below robust | follower stem |
| guide slot width | 2 × 0.65 = 1.30 mm | fine | not a limit |
| guide wall | 1.25 mm | fine | not a limit |
| cam core radius | 1.0 mm | fine | buckling-governed, not print-governed |

**Verdict on printability:** the **0.4 mm nozzle route is geometrically viable** —
every feature is at or above the sourced minimum standalone feature width, and the
load-bearing guide walls are comfortable. But **three features (detent 0.45, body
wall 0.60, stem 0.70 mm) sit below the 0.88 mm robust wall**, i.e. they are
single/double-line features whose realised strength and dimensional spread are
exactly the kind of property DND-27 forbids us to measure. The `08-current-design`
phrase "optional 0.2 mm nozzle for the thin upper guides" is **not** what the
geometry shows: the thin features are the **detent leaf, body wall and follower
stem**, and they are the *load/contact* features, not incidental trim. The honest
statement is:

- the part is printable at 0.4 mm, but the thin contact features are **at the
  process floor** and their tolerance/strength is a **qualitative residual**
  (same class as K2);
- a **0.2 mm nozzle** would give real margin on the detent leaf (0.45 mm → 2+
  lines) and is the recommended process for the contact features, but it is a
  **process choice, not a proven fix**;
- resin/SLA is **not required by the geometry** and would change the material
  properties (creep, fatigue) the whole passive-memory bet relies on — flag for
  the CEO, do not silently adopt (per ADR-001/ADR-002 escalation rule).

**Print-yield / cost note:** print time and material are excluded from the
purchased ceiling by project rule, but they are not free. 6,400 columns ×
(follower + rotor + guides) is a large print run; the modular cartridge strategy
(4 × 8 modules of 20 × 10 cells) is the correct call for scrap replacement and
regional rebuild, and is ratified.

## 6. Reliability and assembly scaling — carried, not closed

- At q = 1×10⁻⁴ per cell, **P(all 6,400 correct) = 52.7 %**; reaching 99 %
  whole-map correctness needs **q ≤ 1.57×10⁻⁶**. No per-cell feedback exists and
  no coupon can be built under DND-27, so this is a **permanent assumption**.
- Assembly: **zero bought parts per cell** (passive printed rotors) is the single
  most valuable property of S5 — it is the only survivor for which the per-cell
  bought-hardware sensitivity (see §7) does not immediately kill the budget.
- Replaceability/module strategy is ratified as the correct mitigation for
  scrap and regional rebuild.

## 7. The portable result (unchanged by any correction)

Because the board is **6,400 cells**, **any bought part required once per cell
kills the budget**: $0.10/cell = $640, already $140 over $500 before motors,
power or structure. Survivors must keep the per-cell layer **printed or passive**.
S5 does. This is the strongest, mechanism-independent finding and it is what the
selection actually rests on.

## 8. Verdict and residual risk (one paragraph)

**RATIFIED.** The S5 purchased BOM is the best-evidenced in the field and clears
the $500 ceiling on its sourced pairing. One arithmetic correction is recorded:
the reduced figure is **$493.57**, not $481.56, because the register
consolidation was priced at its expected allowance ($14) against a sourced base
(true saving $3.70) — a $10.30 conservatism defect that still leaves the design
under ceiling. The <$400 ideal band is **not reachable on any sourced path**. The
**exact residual cost risk** is the **matched-motor supply**: no distributor
stocks a true 8 mm 18° bipolar PM stepper; the only traceable matched part is
MOONS at $40/ea (~$4,156 delivered), and the sub-$1.05 basis is an unqualified
marketplace multipack that can only be retired by purchasing and sampling a lot
(forbidden under DND-27). Treat the winner's expected delivered cost as a
**range $493.57–$646** until that lot exists. Printability on the 0.4 mm X1C/PLA
route is **ratified**, with the thin contact features (detent 0.45, body wall
0.60, stem 0.70 mm) flagged as **at the 0.44 mm process floor** — a qualitative
residual in the same class as K2, not a clean pass.

## 9. What would change the verdict

- A traceable matched 8 mm motor lot quote (sample + 80 + spares, same winding,
  shaft, step angle) near $1.00 delivered → the cost cliff closes and the $503.71
  figure becomes a point, not a range.
- A sourced sub-$0.60 matched bipolar driver → ~$16 delivered saving.
- Evidence that the thin contact features can be printed at 0.4 mm with adequate
  strength → removes the 0.2 mm-nozzle recommendation.
