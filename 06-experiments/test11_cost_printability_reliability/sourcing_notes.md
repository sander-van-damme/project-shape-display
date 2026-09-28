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
