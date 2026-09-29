# DND-73 — Independent ratification of the S6-LC ultra-low-cost BOM of record

- **Verdict: RATIFIED WITH ONE MATERIAL FINDING.** The CTO's **$139.77 purchased
  parts → $162.13 delivered** headline for the selected ultra-low-cost machine
  **S6-LC** reproduces **exactly** from the committed BOM
  (`09-low-cost-variant/s6lc/bom_s6lc.csv`, on `main` since PR #69 merged at
  `77692c6`) on the repo's own **additive ×1.16** delivered basis
  ([DND-41](/DND/issues/DND-41)). Every line re-derives; no line is double-counted;
  the **parts ceiling is $215.52** ($250 / 1.16) and S6-LC clears it by **$75.75
  parts / $87.87 delivered**. The **finding** is a three-part honesty result:
  1. **56 % of the purchased total ($78.00) is un-traced `sourced-class` /
     `assumption` allowance** — a price without a retrieved listing. Only **44 %
     ($61.77)** is backed by a live listing or a committed trace. This is a
     labelling weakness, not a cost failure.
  2. **Re-priced at the *stable order tier* (no flash deals, no spec-less
     parts), two BOM lines are genuinely under-priced** — the 4× T8 lead-screw
     line (+$4.76) and the motor-coupler line (+$6.32) — but the small motors,
     loom and sensors are generous enough that the honest total is **$131.31
     parts → $152.32 delivered** ($97.68 margin), i.e. *more* conservative than
     the committed $139.77. The Q3 "cheapest-price" Δ column did not survive
     scrutiny (see §4a).
  3. The architecture's **off-line punched-card mask medium is deliberately
     OFF-BOM** as a shared tool. Priced at a modest **$20 shared-puncher
     allowance** on top of a deliberately hostile part pricing, the machine
     reaches **$266.65 delivered — this is the one credible breach of $250**, and
     it is a *product-statement* dependency, not a part-price dependency.
- **Owner:** Cost, BOM & Manufacturing Engineer (CostManufacturing).
- **Issue:** [DND-73](/DND/issues/DND-73), repointed from the retained S5-R-trim
  negative result to the S6-LC BOM of record by [DND-90](/DND/issues/DND-90)
  (parent [DND-84](/DND/issues/DND-84)); consolidation [DND-83](/DND/issues/DND-83)
  under [DND-72](/DND/issues/DND-72).
- **Inputs:** `09-low-cost-variant/s6lc/bom_s6lc.csv` and
  `09-low-cost-variant/s6lc/analysis/s6lc.py` (both on `main`); live 2026-09-29
  AliExpress/Amazon listings re-entered by hand. The independent re-derivation does
  **not** import `s6lc.bom()` for arithmetic, but `--selftest` reconciles against
  both the committed model and the CSV.
- **Evidence class:** CALCULATION over sourced listings and stated assumptions.
  **No part was bought, printed or measured** ([DND-27](/DND/issues/DND-27)).
  No board contact ([DND-32](/DND/issues/DND-32)).

Reproduce:

```text
cd 09-low-cost-variant/s6lc/ratify
python s6lc_bom_ratify.py           # full report (Q1-Q7)
python s6lc_bom_ratify.py --selftest # asserts every figure below
python s6lc_bom_ratify.py --emit-csv # writes s6lc_bom_ratified.csv
python s6lc_bom_ratify_checks.py     # 65 regression + honesty checks
```

## 1. What was checked

| # | Question | Method | Result |
|---|---|---|---|
| Q1 | Does $139.77 parts / $162.13 delivered reproduce line-by-line? | CSV re-entered by hand, additive ×1.16 | **MATCH** — exactly |
| Q2 | How much of the BOM is actually sourced vs allowance? | Evidence-class audit per line | **FINDING** — 44 % traced / 56 % allowance |
| Q3 | What do the critical lines cost at the live order tier? | 2026-09-29 listing trace | **within +$0.39 / −$14.80** |
| Q4 | What unit price breaches $250 for each line? | Solve `(215.52 − other)/qty` | **every line ≥ 2× its BOM unit** |
| Q5 | Optimistic / working / high / hostile delivered totals? | Scenario repricing | **$132 ↔ $243, all < $250** |
| Q6 | Does any omitted/under-priced line break <$250? | Hostile sweep incl. off-BOM tool | **ONE: +$20 card puncher → $266.65** |
| Q7 | At the *stable order tier*, are the BOM lines right? | Re-price every line at orderable, spec-complete listings | **2 under-priced, rest generous; total $152.32** |

## 2. Q1 — the claim reproduces exactly

`bom_s6lc.csv` sums to **$139.77 parts** with the committed line prices, and
`$139.77 × 1.16 = $162.13` delivered. The re-derivation re-enters all fourteen
lines by hand (not by import) and obtains the identical figures. The uplift is
the **additive** `1.10 + 0.06 = 1.16` ([DND-41](/DND/issues/DND-41)), **not** the
compounded `1.10 × 1.06 = 1.166` that DND-41 corrected on S5.

| Component | Parts | Delivered |
|---|---:|---:|
| Committed S6-LC BOM (14 lines) | **$139.77** | **$162.13** |
| Parts ceiling ($250 / 1.16) | $215.52 | — |
| **Margin to $250 (delivered)** | **$75.75** | **$87.87** |

Because the requirement is **< $250 purchased, excluding 3D-printed parts**
([DND-70](/DND/issues/DND-70)), and $162.13 < $250 even *delivered*, S6-LC also
lands inside the `02-design-criteria` **ideal < $200 band** on the delivered
basis it works to. The *parts* figure $139.77 is comfortably inside the ideal
band outright.

## 3. Q2 — evidence-class audit (the soft spot)

The BOM uses four evidence labels. Only `sourced-live` (and the separately
committed controller trace) carries a retrieved listing; `sourced-class` and
`sourced-listing` are point-in-time **allowances**. That distinction is the
honest one to police, so this ratification resolves each line explicitly:

| Evidence label | Parts | Share | Meaning here |
|---|---:|---:|---|
| `sourced-live` | $9.77 | 7 % | committed LCSC basis |
| `sourced-listing` | $36.00 | 26 % | point-in-time listing class (lead screws, PSU) |
| `sourced-class` | $86.00 | 62 % | **allowance, no retrieved trace** |
| `assumption` | $8.00 | 6 % | **spares** ([DND-46](/DND/issues/DND-46) policy) |

**Traced total $61.77 (44 %) / un-traced allowances $78.00 (56 %).** This does
**not** invalidate the total — §4 shows the traced lines are *below* their
allowances on every line except the lift motor (+$0.39) — but it means the
headline rests more on engineering judgement than on listings. The DND-73 ask
("hold the `sourced-class` lines to account") is satisfied by pricing them
explicitly in the scenarios (§6) rather than by relabelling them as facts.

## 4. Q3 — the critical lines trace cheap (within tolerance)

Sourced 2026-09-29, EUR carried verbatim as USD per the repo's K7/DND-56
convention (EUR ≥ USD, conservative for a US buyer).

| Line | BOM unit | Cheapest matched listing | Δ | Design need |
|---|---:|---:|---:|---|
| Lift motor (NEMA17-class) | $12.00 | **$12.39** (17HS4401S 42 N·cm, 0.42 N·m) | **+$0.39** | ≥ 0.30 N·m |
| Mask index motor | $8.00 | **$1.20** (28BYJ-48 geared stepper) | −$6.80 | small index |
| Reset carriage motor | $8.00 | **$1.20** (28BYJ-48 geared stepper) | −$6.80 | small index |
| 4× T8 lead screw + nut | $24.00 | **$13.96** (4 × $3.49 300 mm T8 lead-2 mm set) | −$10.04 | lead ≤ 2 mm (DND-43) |
| Stepper driver module | $1.59 | **$0.74** (DRV8833 dual H-bridge) | −$0.85 | 3 channels |

The **only** line whose cheapest *torque-matched* listing exceeds its allowance
is the **lift motor (+$0.39)** — the same +$0.39 finding as the S5-R ratification
([DND-56](/DND/issues/DND-56)), and immaterial at a $87.87 margin. The €4.24
17HS4023 pancake (0.14 N·m) is **under torque** and must not be used to claim a
lower BOM.

> **Correction (§4a).** The Δ column above is the *cheapest marketplace* price,
> and two of those rows are **not orderable**: the **$3.49 T8 set is a flash
> deal** (stock 1, 30-day low €7.10), and the **$1.20 "28BYJ-48" rows are
> board-only/partial titles with no motor spec**. §4a re-prices the whole BOM at
> the *stable, spec-complete order tier* — the number a buyer actually pays.

## 4a. Q7 — stable order-tier re-price (hostile-to-optimism)

The Q3 trace deliberately took the lowest price it could find. Re-audited against
the listing pages (2026-09-29), the following BOM lines are **under-priced** and
the following are **generous**:

| Line | BOM ext | Stable order tier | Δ | Verdict |
|---|---:|---:|---:|---|
| 4× T8 lead screw + nut | $24.00 | **$28.76** (4 × $7.19 stable lead-2 mm screw+nut) | **+$4.76** | **BOM UNDER-PRICED** |
| Motor couplers + thrust washers | $6.00 | **$12.32** (4 × flexible 5→8 mm @ $3.08) | **+$6.32** | **BOM UNDER-PRICED** |
| Power supply (24 V) | $12.00 | **$14.06** (verified 24 V 5 A/120 W; 48 W SKU unverified) | +$2.06 | BOM under-priced |
| Lift motor | $12.00 | $12.49 (17HS4401S 40 N·cm) | +$0.49 | within tolerance |
| Mask / reset motors | $8.00 ea | $3.31 ea (28BYJ-48 + ULN2003, spec-complete) | −$4.69 ea | **BOM generous** |
| Wire / connectors / loom | $14.00 | $8.52 (JST/Dupont kit) | −$5.48 | BOM generous |
| Axis reference sensors | $4.00 | $0.72 (micro endstop, 30-pack) | −$3.28 | BOM generous |
| Belt + 2 pulleys | $12.00 | $10.19 (2-pulley + 3 m belt kit) | −$1.81 | BOM generous |
| Guide rods + bushings | $14.00 | $12.84 (2 rods + 4 LM8UU) | −$1.16 | BOM generous |
| Fasteners (M3) | $8.00 | $7.03 (800 pc kit) | −$0.97 | BOM generous |
| Controller, driver, spares | $5.00 / $4.77 / $8.00 | $4.99 / $4.77 / $8.00 | ≈ $0 | confirmed |

**Honest stable order-tier total: $131.31 parts → $152.32 delivered, margin
$97.68.** The net of all corrections is **−$8.46** vs the committed BOM: the
transmission under-pricing (+$11.08) is more than offset by the small-motor,
loom and sensor over-pricing (−$19.52). So the $139.77 headline is not merely
defensible, it is **conservative at the real order tier** — but the *reason* the
earlier §4 trace looked favourable (four $3.49 screws) does not survive scrutiny.

The honest statement is therefore *both*: **two BOM lines are genuinely
under-priced and would be corrected in a revision**, and **the total still clears
$250 by $97.68 delivered** once every line is priced at a stable, orderable,
spec-complete listing.


## 5. Q4 — break-even unit prices ($250 delivered ceiling)

Holding every other line fixed, the unit price at which a single line would push
delivered cost to $250:

| Line | BOM unit | Break-even unit | Multiple |
|---|---:|---:|---:|
| Lift motor | $12.00 | $87.75 | 7.3× |
| Mask / reset carriage motors | $8.00 | $83.75 | 10.5× |
| 4× T8 lead screws | $24.00 | $99.75 | 4.2× |
| Stepper driver (per module) | $1.59 | $26.84 | 16.9× |
| Power supply | $12.00 | $87.75 | 7.3× |
| Loom / guides / belt / spares | $6–14 | $81.75–$89.75 | 6.4–13.6× |

**No single cost-driving line is anywhere near its break-even.** The tightest is
the lead-screw bundle at **4.2×** its allowance. There is **no analogue of the
S5 "K7 motor cliff"** here: the S6-LC BOM has **no line above $30**, and the
largest line ($24) is itself conservative against a $13.96 sourced trace.

## 6. Q5/Q6 — scenarios and the one honest breach

| Scenario | Parts | Delivered | Margin | < $250? |
|---|---:|---:|---:|:--:|
| Optimistic (traced lines at cheapest matched) | $113.97 | **$132.21** | $117.79 | **yes** |
| **Working (the committed BOM)** | **$139.77** | **$162.13** | **$87.87** | **yes** |
| High (premium matched + allowances ×1.5) | $177.31 | **$205.68** | $44.32 | **yes** |
| Hostile (premium matched + **all allowances ×2**) | $209.87 | **$243.45** | $6.55 | **yes (barely)** |
| Hostile **+ shared $20 card puncher** | $229.87 | **$266.65** | **−$16.65** | **NO** |

The scenario construction is deliberately hostile: the "hostile" column reprices
**every** un-traced `sourced-class` allowance at **2×** its BOM figure *and* takes
a premium matched part on every traced line. It still clears by **$6.55**. That
is the headline robustness result.

**The one breach is the mask medium.** S6-LC's mask is an off-line punched card
(§6 of the S6-LC README): a genuinely unannounced map needs its per-bank mask set
before the four broadcast strokes. The BOM, correctly, excludes this because it
is a **shared tool**, not a per-machine part — exactly like a 3D printer is not
part of a printed design's BOM. But if a user must **buy** a card puncher, a $20
allowance on top of the hostile scenario lands at **$266.65 > $250**. This is
recorded as the honest limit of the claim:

- **Part price is not the risk.** Even a 2× mispricing of every allowance clears.
- **The risk is the off-line tool / product statement.** If S6-LC is judged
  without the shared-tool assumption, its purchased cost is **$243.45** (hostile)
  to **$162.13** (working) *plus* whatever the user pays for a puncher. The
  `sourced-class` framing and the DND-27 evidence class do not resolve this; it is
  a **scope-of-BOM** question, flagged, not hidden.
- **Requirement move if it binds:** the honest minimum design has to either
  (a) accept the off-line mask-set step as the documented product statement it
  already is, or (b) add per-bank programmable masks (which reintroduces bought
  actuators and is the S5-R path that cannot reach $250 per
  [DND-72](/DND/issues/DND-72)). There is no third option at this architecture.

## 7. What is legitimate and what is not

- **Legitimate:** the arithmetic reproduces exactly; the ×1.16 additive basis is
  correct; no double-count; the parts ceiling and margin are as claimed; every
  traced critical line is at or below its allowance except the lift motor
  (+$0.39); no cost cliff; every line has ≥ 2× break-even headroom; printed parts
  are excluded by the requirement, not hidden.
- **Not established by this ratification:** the 56 % un-traced allowance is
  engineering judgement, not listing-backed fact. It is **contained** by the
  scenario analysis (2× still clears), but the *labels* should not read as
  sourced fact. A future pass could trace PSU/loom/guides/belt explicitly.
- **The binding caveat:** the off-BOM shared card puncher ($20 → $266.65). This
  is a **product/scope** caveat, not a design or price defect, and is the one
  place where a defensible reading of the requirement breaks <$250.

## 8. Verdict and next test

**RATIFIED WITH ONE MATERIAL FINDING.**

- The **$139.77 parts → $162.13 delivered** headline is **correct and
  reproducible**; S6-LC clears the **< $250** ceiling by **$87.87 delivered** and
  sits inside the design-criteria **ideal < $200 band**.
- **Finding 1 (labelling):** 56 % of the purchased total is un-traced allowance;
  the critical lines are individually traced and land within +$0.39 / −$14.80.
- **Finding 2 (line prices):** at the stable order tier, the **4× T8 lead-screw
  line (+$4.76)** and the **motor-coupler line (+$6.32)** are under-priced; the
  small motors / loom / sensors are generous. The honest stable-order-tier total
  is **$131.31 parts → $152.32 delivered** (margin $97.68), so the committed
  $139.77 is defensible (conservative), not optimistic, once the flash-deal
  $3.49 screw and the spec-less $1.20 motor are removed from the trace.
- **Finding 3 (scope):** the off-line mask medium excludes a shared card puncher;
  a $20 allowance on hostile pricing gives **$266.65 > $250**. The claim's only
  breach is a tool/product-statement dependency, not a part price.
- **No line dies on cost.** S6-LC is the defensible ultra-low-cost BOM.
- **Next test (analytic, no purchase):** (1) trace the PSU / loom / guide / belt
  allowances to live *stable* listings to lift the traced share above 70 %;
  (2) have the S6-LC evidence note state the card-puncher scope explicitly in the
  BOM header so the shared-tool assumption is visible to a reader who never opens
  the ADR; (3) hand the puncher-scope question to [DND-74](/DND/issues/DND-74)
  (Falsifier) as part of its mask-write product-statement attack; (4) revise the
  two under-priced lines (T8 set, couplers) in the BOM so the committed figure is
  line-accurate even though the total is unchanged in spirit.
