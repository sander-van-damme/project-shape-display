# Sourcing ledger — checked 2026-09-27

No orders placed, supplier contacted, delivered quotation obtained, or physical
motor measured. USD list prices are **sourced**; they are not delivered prices.
The BOM separates sourced entries from **engineering allowances** and
**speculative bulk targets** in each row. Shipping, import/currency exposure and
20% contingency are additional, separate allowances. Requote before purchase.

| ID | Primary source and observed fact | Qualification limit |
|---|---|---|
| M1 | [MOONS PM catalogue](https://www.moonsindustries.com/c/permanent-magnet-stepper-motors-a0208): 8PM020S1-02001, 8 mm class, 8.5 mm length, 18°, bipolar, 0.25 A, 0.4 mN m **holding** torque, $40 list | Listed product, delivery/stock unconfirmed. No usable loaded speed curve or shaft drawing retrieved. Rated voltage, shaft diameter/length and winding resistance must be confirmed. 80 cost $3200 before anything else. |
| M2 | [DFRobot FIT0708](https://www.dfrobot.com/product-2199.html): $12.90 single, $11.90 at ten; 10 mm linear motor, 18°, 20 ohm ±10%, 3.3–5 V, 1500 pps auto-start specification | Different assembly, no loaded rotary torque guarantee; requires removal/adaptation of screw slider and dimensional inspection. Cannot be substituted for an 8 mm PM08 motor. 80 cost $952 before delivery. Use dual bridges; do not infer GPIO drive suitability from sales wording. |
| M3 | [Archived PM08-2](../test00_pneumatic_multiplexer/docs/micro-stepper-datasheet.pdf) | Historical 3.3 V, 40 ohm, 18°, 8 mm, 5 gf cm pull-in torque; >800 pps is no-load. Historical €0.52/pair is not a current price. Test09 has no matched current low-cost offer. |
| D1 | [LCSC DRV8833PWR C544801](https://www.lcsc.com/product-detail/C544801.html): retrieved search snapshot displayed 566 stock; $2.3734 single, $1.8005 at 30, $1.5752 at 100 | Dynamic price table was not exposed on subsequent direct-page retrieval; these are sourced cached listing values, not a confirmed checkout. For 80 use 30 tier; 100 costs $157.52 versus 80×$1.8005=$144.04. PCB/passives additional. |
| D2 | [TI DRV8833](https://www.ti.com/product/DRV8833): two bridges drive one bipolar stepper, 2.7–10.8 V supply; PW package 500 mA RMS per bridge | Electrical architecture reference only. Choose current limit from the actual motor, check rail drop and fault output; chip fault cannot detect every missed step. |
| D3 | [Pololu 2130 carrier](https://www.pololu.com/product/2130): $10.95 single, $9.27 at 25; backorders allowed in retrieved listing | Practical one-motor bench driver if obtainable; 80 carriers $741.60. This carrier cost is **not** the bare-IC BOM. |
| S1 | [Adafruit 2776](https://www.adafruit.com/product/2776): $4.95 single, $4.46 at 10–99, $3.96 at 100+; displayed in stock; 5 V, 1.1 A, 3 mm throw, 12.6 g | Multi-row conservative $4.46 means sourced 100+ price plus $0.50 driver allowance for 320/400 channels. Smaller banks retain $4.46 as a rough allowance; shipping and loaded response unqualified. The lightweight 3 g selector mass is a custom-selector hypothesis, not this solenoid. |
| F1 | [Project X1C context](../../02-design-criteria/README.md), with [manufacturer specifications](https://eu.store.bambulab.com/products/x1-carbon-3d-printer) | 256 mm build volume, PLA baseline, 0.4/0.2 mm nozzles. Direct manufacturer retrieval failed during Test09; no new dimensional tolerance claimed. |

Search also covered 8 mm/18° surplus and linear motors. Aggregator prices and
unidentified marketplace motors were not promoted to qualified quotes. This is
not proof that cheap motors do not exist. It is a procurement gate: obtain one
traceable sample and an 80+spares delivered quote with the same winding, shaft,
step angle and production lot; measure that sample, then several lot samples.

At historical PM08 electrical assumptions, each phase draws 82.5 mA and an
80-channel two-phase head dissipates 43.56 W (13.2 A at 3.3 V). FIT0708 at 3.3 V
would instead nominally dissipate 87.12 W for 80; MOONS current cannot be combined
with the PM08 resistance. Driver wiring, thermal test and supply BOM must follow
the selected winding. No-load frequency, holding torque and pull-in torque are
three different specifications; none establishes 400 pps loaded running torque.

Blank `measurements/procurement.csv` records source/date, matched part, quantities,
unit currency, conversion, shipping, taxes and delivered USD. Update the BOM and
rerun before authorizing scale. Bench instruments and the existing printer are
test equipment, excluded from the product BOM; brake, sensors and permanent
structural hardware are included. No purchased part is hidden under printing.
