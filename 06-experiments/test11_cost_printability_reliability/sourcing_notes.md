# Sourcing notes — critical purchased items (S1–S5)

Observed **2026-09-28**. USD unless a source displayed another currency (some
marketplace pages rendered in EUR because the retrieval egress was geolocated to
the Netherlands; those are marked). These are **listing observations, not
delivered quotations**. Nothing was ordered. Treat every figure as a point-in-time
price to be re-verified before purchase.

This file is the sourced-price companion to
`cost_model.py`. It exists because Test08's working BOM allowed the critical
80-channel motor at **$1.25 each with no matched quote**, and the design's
survival depends entirely on whether that number is real.

## 1. The critical item: 8 mm-class 18°/step bipolar PM stepper (80 required)

| Source | Part / spec | Observed price | Provenance |
|---|---|---|---|
| MOONS online shop | 8PM020S1-02001, 8 mm, 18°, 5 V, 0.25 A, 0.4 mN·m **holding**, 8.5 mm long | **$40.00 ea** | retrieved live product page |
| Amazon | Abovehill "10 pairs 8 mm micro stepper 2-phase 4-wire 5–6 V", 39.2 Ω | **≈EUR 0.97 ea** (10-pair pack) | retrieved live product page |
| Amazon | Acxico 4.3 mm 2-phase 4-wire, ~14 Ω, 0.3 A | ≈EUR 0.70 ea (10-pack) | retrieved live product page |
| AliExpress | "8 mm stepper motor" wholesale search, min prices | USD 2.66 / 2.89 / 3.52 / 3.59 / 3.76 / 4.89 ea | cached search-render snippet, individual items unverified |
| LCSC / DigiKey / Mouser / Adafruit / Pololu / DFRobot | bare 8 mm 18° bipolar PM stepper | **not stocked as a discrete part** | live catalog searches |

**Structural finding.** There is **no commodity bare 8 mm 18° bipolar PM stepper**
in the mainstream distributor catalogs. It is either a branded part at ~$40
(MOONS), or a marketplace multipack near $0.70–1.05, or an unverified AliExpress
listing near $2.66+. The $1.25 assumption sits inside the marketplace-multipack
range but has **no traceable matched quotation**.

**Why it matters:** the sourced MOONS holding torque is only 0.4 mN·m and is a
*holding* figure, not running torque. Test08 needs ≥0.15 mN·m running torque at
400 pps. Buying the $40 part is not a cost path; buying the $1 multipack motor is
not yet a qualified part. This is the single largest sourcing risk in the project.

### URLs

- MOONS 8PM020S1-02001: https://www.moonsindustries.com/p/8mm-permanent-magnet-stepper-motors/8pm020s1-02001-000004611120002314
- MOONS series: https://www.moonsindustries.com/series/8mm-permanent-magnet-stepper-motors-a020806
- Abovehill multipack: https://www.amazon.com/Abovehill-Stepper-2-Phase-4-Wire-Connection/dp/B08346RFVZ
- Acxico 4.3 mm: https://www.amazon.com/Acxico-2-Phase-Ultra-Tiny-Precision-Stepper/dp/B09CTT8Z2G
- AliExpress 8 mm search: https://www.aliexpress.com/w/wholesale-8mm-stepper-motor.html

## 2. Motor drivers (80 channels required for S5; 320–400 for S3)

| Part | Source / code | 1-unit | 100-unit | Stock | Provenance |
|---|---|---|---|---|---|
| DRV8833PWR (TSSOP-16) | LCSC **C544801** | $2.3873 | $1.5828 | 421 | retrieved live (LCSC JSON API) |
| DRV8833PWPR (TSSOP-16-EP) | LCSC **C50506** | $2.1016 | $1.3338 | 7,616 | retrieved live (LCSC JSON API) |
| TB6612FNG | LCSC **C88224** | $1.2968 | $0.7955 | 5,436 | retrieved live (LCSC JSON API) |
| DRV8825PWPR | LCSC **C81582** | $2.4007 | $1.6915 | 18,817 | retrieved live (LCSC JSON API) |
| ULN2003ADR | LCSC **C7512** | $0.1547 | $0.1012 | 273,225 | retrieved live; **unipolar only, not suitable for bipolar PM windings** |
| DRV8833 breakout module | Amazon 20-pack | — | ≈EUR 0.66 ea | — | retrieved live product page |
| DRV8833 module | AliExpress | — | ≈EUR 0.72–0.74 ea | — | retrieved live listing |
| A4988 carrier | Pololu | $8.95 | — | live | retrieved live |
| DRV8825 carrier | Pololu | $15.95 | — | live | retrieved live |

The bare IC is the cost-effective choice: **DRV8833PWPR at $1.33/unit (100 tier)
is the cheapest matched bipolar dual-H-bridge**; TB6612FNG at $0.80/unit is
cheaper still if its 1.2 A rating fits. Test08 allowed $0.60/channel, which is
**below the cheapest sourced bipolar IC**; the honest working line is ~$0.80–1.33
even at volume, unless a bare-module multipack at ~$0.66 is accepted.

## 3. Couplers, shafts and bearings

| Item | Source | Observed price | Provenance |
|---|---|---|---|
| Aluminium rigid coupler 6-pc set (1/2/3.17/4/5/6 mm bores) | AliExpress | ≈EUR 1.90 ea | retrieved live listing |
| 1 mm mini universal/cross coupler (brass) | AliExpress | EUR 6.59 ea | retrieved live listing |
| 3–3 mm micro brass cross coupler | AliExpress | ≈EUR 0.72–1.20 ea (packs) | retrieved live listing |
| RC shaft sleeve coupler 2–6 mm | AliExpress | EUR 1.71 ea | retrieved live listing |
| 681X / 682ZZ / 683ZZ mini shielded bearings | AliExpress | ≈EUR 0.30 ea (10-pk) | retrieved live listing |
| MR52/63/74ZZ mini bearings | AliExpress | ≈EUR 0.34 ea (10-pk) | retrieved live listing |
| Assorted MR52…MR148ZZ bearings | AliExpress | ≈EUR 0.26 ea (10-pk) | retrieved live listing |
| Brass rod 2–15 mm × 300 mm | AliExpress | EUR 4.39 ea | retrieved live listing |

**No 80-unit contract price was published** for any coupler, shaft or bearing —
all marketplace prices are small-bundle list prices. Test08's `head shafts and
friction-pad material` line ($20 working for 80 compliant shafts) is therefore an
*allowance*, not a quote. A coupler test part is purchasable today; an 80-piece
matched supply is not.

**Tile couplers (S1/S4, 64 required):** the designs intend these to be *printed*.
The cost model treats a bought fallback at $3 ea (S4) / $0.50 ea (S1 release
latches) as an explicit allowance. No commercial miniature magnetic/mechanical
coupler was found at a volume price; the ~$3 ideal / $6 absolute per-channel
allowance in `04-architecture-candidates` has **no sourced part behind it**.

## 4. Other bought hardware (live or allowance)

| Item | Source | Observed price | Provenance |
|---|---|---|---|
| Adafruit mini push-pull solenoid (2776), 5 V, 3 mm throw | Adafruit | $4.95 / $4.46 @10 / **$3.96 @100+** | retrieved live qty table |
| 74HC595D shift register | LCSC C5947 | **$0.0925 @50 / $0.0802 @150** | retrieved live API |
| RP2040 bare chip | LCSC C2040 | $0.7645 @100 | retrieved live API |
| ESP32-WROOM-32E | LCSC C701342 | $3.42 @100 | retrieved live API |
| Raspberry Pi Pico | Adafruit | $5.00 | retrieved live |
| T8 lead screw THSL-300-8D + nut | AliExpress | ≈EUR 2.89 | retrieved live listing |
| T8 anti-backlash nut | AliExpress | ≈EUR 2.47 ea | retrieved live listing |
| NEMA17 planetary gearmotor 5.18:1 | AliExpress | ≈EUR 24.19–26.19 | retrieved live listing |
| Pololu NEMA17 with integrated lead screw | Pololu | $105.52 / $109.06 | retrieved live |
| M2/M3 screw+nut assortment | AliExpress | ≈EUR 5.19–8.09 | retrieved live listing |
| PLA 1 kg 1.75 mm | AliExpress | ≈EUR 9.69 | retrieved live listing |
| 24 V SMPS 200 W class | AliExpress | from EUR 5.39 (select W) | retrieved live listing |
| JST-XH / Dupont connector kits | AliExpress | ≈EUR 2.52–8.49 | retrieved live listing |

**Blocked sources:** DigiKey (HTTP 403) and Mouser (Access Denied) could not be
retrieved directly; their prices here appear only via the Octopart aggregator and
are labelled aggregator estimates. Amazon search pages and AliExpress item pages
need JavaScript; AliExpress began returning empty responses after ~10 queries.

## 5. What this changes

- Test08's **$1.25 motor** sits in the marketplace-multipack range but has **no
  traceable quote**; the one traceable part is $40/ea.
- Test08's **$0.60 bipolar driver** is **below the cheapest sourced matched IC**
  ($0.80 TB6612FNG @100, $1.33 DRV8833PWPR @100). Substituting sourced drivers
  pushes the $432 base to ~$490 (still $518.40 → $588.84 with contingency).
- The cheapest *credible* sub-$500 path therefore needs **both** a marketplace
  motor near $1.00 and a sub-$0.60 driver. Neither is currently a matched supply.
- **Recommendation:** run the Test09 Stage C procurement gate — obtain one
  traceable 8 mm motor sample and an 80+spares delivered quote with the same
  winding, shaft, step angle and lot — before any full-scale purchase. Sourcing is
  now a first-class blocker, not a footnote.

## 6. Delivered addendum (DND-11)

The three-scenario **delivered** BOM that consumes these prices is in
[`delivered_3scenario/`](delivered_3scenario/README.md). It applies a scenario
shipping/import uplift to the parts subtotal and reports best/expected/worst with
per-line vendor and evidence labels. Result: every survivor is over $500 at the
expected delivered scenario, and the cheapest sourced motor+driver pair for S5
lands at $501.12 delivered — on the ceiling with no margin. Prices here are the
2026-09-28 source; re-verify before any purchase.

## 7. DND-37 re-check — the matched-motor question (2026-09-28)

Re-run for the S5 winner ratification ([DND-37](/DND/issues/DND-37)). Conclusion
unchanged and now better evidenced: **no distributor stocks a true 8 mm 18°
bipolar PM stepper.**

| Source | Finding | Evidence |
|---|---|---|
| Octopart (aggregates DigiKey, Mouser, Farnell, Newark, Arrow) | "8mm stepper motor" → only large NEMA/hybrid frames (QSH6018 €114+) and €268–503 integrated PANdrives. No small 8 mm PM bipolar stepper at any price. | SOURCED (live page 2026-09-28) |
| MOONS online shop | `8PM020S1-02001`, 8 mm, 18°, bipolar, 0.4 mN·m holding / 0.15 mN·m detent → **$40.00 EA**. Only traceable matched part. | SOURCED (live product page) |
| AliExpress "8mm stepper motor" | Genuine micro listings: "Micro Mini 8 mm 2-phase 4-wire" **€2.66 ea** (1k+ sold); "8/10 mm 2-phase 4-wire screw-slide micro stepper" **€3.59 ea**; "10 pcs 3–5 V 2-phase 4-wire dia 8 mm, 8×9.5 mm" **€7.89/10 → €0.79 ea** (143 sold). | SOURCED (live listing page) |

**Residual risk:** the sub-$1.05 basis is an **unqualified marketplace multipack**
(no datasheet-matched step angle, winding, shaft or lot). Only a purchased,
sampled lot can retire it, and that is forbidden under
[DND-27](/DND/issues/DND-27). Treat the S5 expected delivered cost as a **range
$483.37–$646** (at a $2.66 marketplace motor) until a matched lot exists. The
$40 MOONS part would put the machine at ~$4,156 delivered. Basis note ([DND-41](/DND/issues/DND-41)):
on the repo's additive ×1.16 delivered basis the sourced pair is **$501.12** (over
the ceiling) and the reduced path is **$483.37**; the earlier $503.71/$493.57
figures used a multiplicative ×1.166 uplift and an over-counted register saving.
See
[`../../07-evidence-and-decisions/dnd37-bom-ratification.md`](../../07-evidence-and-decisions/dnd37-bom-ratification.md).

## 8. DND-47 ratification of the DND-44 cost closure (2026-09-28)

Independent re-derivation (`test12_winner_convergence/cost_closure_ratify.py`, no
import of the DND-44 module) confirms the DND-44 numbers exactly:

| Figure | DND-44 claim | Independent re-derivation |
|---|---:|---:|
| Honest expected baseline delivered | $592.06 | **$592.06** (parts $510.40) |
| E1–E6 machine-preserving path | $424.95 | **$424.95** (parts $366.34) |
| Margin below $500 | $75.05 | **$75.05** |
| Motor break-even | $1.86 | **$1.8587** |
| Downside at $2.66 AliExpress motor | $574.36 | **$574.36** |

**Qualification.** $40.60 of the $75.05 margin is E6 repricing four fixed lines
(rods/bearings, belts/idlers, head shafts, fasteners) from the BOM's
`unit_expected` to its `unit_best` column, and $16.00 is E2 moving the motor from
expected $1.25 to the best-case $1.05 listing. These are best-case prices mixed
into an "expected" total. The path still clears without E6 ($465.55 delivered,
$34.45 margin), so the claim **stands**, but the honest headline is a **range
$424.95–$465.55**, not a single number.

**Independent finding — dual-H-bridge over-count.** The driver line carries qty 80
(= motor count) priced per **dual** H-bridge IC (DRV8833/TB6612). 80 motors need
**40 ICs**; the surplus 40 ICs = **$36.91 delivered** of conservatism *against* the
design. Correcting it adds margin; it does not threaten the ceiling.

**Unchanged residual (K7).** The sub-$1.86 motor basis remains an unqualified
marketplace multipack; the only matched part (MOONS 8PM020S1) is $40/ea. Full
verdict: [`../../07-evidence-and-decisions/dnd47-cost-closure-ratification.md`](../../07-evidence-and-decisions/dnd47-cost-closure-ratification.md).
## 9. DND-49 K7 closure — trace the matched motor to ≤ $1.86 delivered (2026-09-28)

Executable trace: [`../test12_winner_convergence/k7_motor_trace.py`](../test12_winner_convergence/k7_motor_trace.py)
(checks: `k7_motor_trace_checks.py`). The K7 requirement is a **matched** 8 mm
18° 2-phase **bipolar** PM stepper at **≤ $1.86 delivered-inclusive** (the
break-even for the DND-44 / DND-47 machine-preserving path; each $1.00 of motor
price adds $92.80 delivered over 80 channels).

### Candidate table (retrieved 2026-09-28; qty 80 + spares unless noted)

| Vendor | Part | Unit | Qty basis | Matched? | Specs | Evidence |
|---|---|---:|---|---|---|---|
| MOONS' shop | 8PM020S1-02001 | $40.00 | 1 (list) | yes | 8 mm, 18°, bipolar, 20 Ω, 0.25 A, 0.4 mN·m **holding**, 0.15 mN·m **detent** | SOURCED-LIVE |
| CCHT (Made-in-China) | Compact 8mm 3.3V, model 07-005-032 | **$8.20** | 3,001+ (**$11.20 @100**) | yes | 8 mm, 18°, 2-ph 4-wire **bipolar**, 3.3 V, 165 mA, 20 Ω, **1.50 gf·cm (0.147 mN·m)** | SOURCED-LIVE |
| CCHT (Made-in-China) | Compact 8mm 5V, model 07-005-036 | $11.20 | 100–1,000 | yes | 8 mm, 18°, bipolar drive, 5 V, 50 Ω, **0.23 gf·cm (0.023 mN·m)** | SOURCED-LIVE |
| DFRobot | FIT0708 | $11.90 | 10+ | **no (10 mm)** | 10 mm, 18°, bipolar drive, 20 Ω, 3.3–5 V, 1500 pps auto-start, no torque published | SOURCED-LIVE |
| Amazon | Abovehill multipack, 10 pair | $1.05 | 10-pair pack | **no (no step angle)** | 8 mm, 2-ph 4-wire, 5–6 V; step angle & bipolar unconfirmed | UNVERIFIED |
| AliExpress | 10-pc 8×9.5 mm pack | $0.86 | 10-pc pack | **no (no step angle)** | 8 mm, 2-ph 4-wire, 3–5 V | UNVERIFIED |
| AliExpress | Micro Mini 8 mm + gear | $2.66 | 1 pc | no (no 18° spec) | 8 mm, 2-ph 4-wire | UNVERIFIED |
| AliExpress | 8/10 mm screw-slide linear | $3.59 | 1 pc | no (linear, no 18°) | 8/10 mm, 2-ph 4-wire | UNVERIFIED |
| repo archive | PM08-2 datasheet | (€0.52/pair historic) | — | historical | 8 mm, 18°, 3.3 V, 40 Ω, 0.490 mN·m **pull-in**, >800 pps no-load | SOURCED-ARCHIVE (non-actionable) |

URLs: CCHT [07-005-032](https://cn-ccht.en.made-in-china.com/product/TOLAylwxCbYh/China-Compact-8mm-3-3V-DC-Micro-Stepper-Motor-for-Precision-Control.html) /
[07-005-036](https://cn-ccht.en.made-in-china.com/product/GZITWbJrHeRj/China-Compact-8mm-5V-DC-Micro-Stepper-Motor-for-Precision-Control.html) ·
[Moons 8PM020S1](https://www.moonsindustries.com/p/8mm-permanent-magnet-stepper-motors/8pm020s1-02001-000004611120002314) ·
[DFRobot FIT0708](https://www.dfrobot.com/product-2199.html) ·
[Amazon B08346RFVZ](https://www.amazon.com/dp/B08346RFVZ) ·
[AliExpress 32908973633](https://nl.aliexpress.com/item/32908973633.html),
[4000806393169](https://nl.aliexpress.com/item/4000806393169.html),
[1005008916092796](https://nl.aliexpress.com/item/1005008916092796.html).

**Still not stocked** as a bare 8 mm 18° bipolar PM stepper: LCSC (search +
wwwapi endpoints), DigiKey (403), Mouser (denied), Octopart (large/NEMA only),
Adafruit, Pololu, SparkFun, Alibaba/Made-in-China (family bottoms at ~$8.20).

### Verdict — **K7 REFUTED** (no matched traced part ≤ $1.86 delivered)

| Motor basis | Delivered (E1–E6) | vs $500 |
|---|---:|---:|
| Untraced Amazon multipack $1.05 | $424.95 | under by $75.05 (**the basis the whole path rests on**) |
| Untraced AliExpress $0.86 | $407.32 | under by $92.68 |
| AliExpress $2.66 (sourced downside) | $574.36 | over by $74.36 |
| **CCHT matched $11.20 @100** | **$1,366.87** | over by $866.87 |
| CCHT matched $8.20 @3,001+ | $1,088.47 | over by $588.47 |
| MOONS matched $40 | $4,039.51 | over by $3,539.51 |

The sub-$1.86 clearing path **requires an untraced marketplace multipack whose
step angle is not published**; every matched, currently-orderable part is
$8.20–$40, putting the machine **$588–$3,540 over** the ceiling. Note also that
the MOONS matched part's **detent torque (0.15 mN·m) equals the target running
torque** — a caution flag, not a margin, since detent drag subtracts from
running torque.

### Minimum-cost design lever — the reduced head FAILS the time budget

Reducing the 80-channel programming head would let a pricier matched motor fit
(20 motors @ $8.20 ≈ $536 delivered; 10 ≈ $432), but the head must program all
80 columns per row, so fewer channels means `80/N` re-index passes per row.
Re-derived on the Test12 timing model:

| Head width | Full-map time | 30 s budget |
|---:|---:|---|
| 80 | 26.3 s | **PASS** |
| 40 | 104.1 s | FAIL |
| 20 | 162.1 s | FAIL |
| 10 | 229.4 s | FAIL |

**The reduced-head lever is not viable.** The honest design-level lever is
therefore not fewer motors: it is (a) qualify the marketplace multipack (buy a
sample lot — forbidden by [DND-27](/DND/issues/DND-27)), or (b) accept a
different actuator class / drive topology for the head. K7 stays **refuted on
sourced evidence** and remains the binding cost residual of S5.
