# Test 11 — purchased-BOM, sourcing, printability and reliability scaling (S1–S5)

**Question.** For every architecture survivor S1–S5, what does the *bought*
hardware actually cost in three scenarios, what real parts can be sourced today at
what price, what does 5.08 mm pitch cost in printability, and how do per-cell
failure and assembly scale against the product targets?

**Evidence level.** This test produces **cost-model arithmetic and sourced
listing prices**, plus printability/reliability *screens*. It contains **no
physical measurement and no supplier quotation**. Where a line says "sourced", a
link and an observation date exist in [sourcing_notes.md](sourcing_notes.md).
Everything else is an engineering allowance and is labelled as such.

Run:

```text
python 06-experiments/test11_cost_printability_reliability/cost_model.py
python 06-experiments/test11_cost_printability_reliability/print_reliability.py
```

Standard library only. BOM inputs are the `bom_S1..S5.csv` files in this folder.

## Headline results

1. **No survivor has a credible sub-$500 delivered path at working allowances.**
   At working allowances plus 20% contingency the purchases are S1 $621.60,
   S2 $643.20, S3 $3,022.32, S4 $603.84, S5 $518.40. S5 is the only survivor that
   even *rounds* toward the ceiling, and it does so only because its two biggest
   lines ($1.25 motor, $0.60 driver) are **unquoted allowances that real listings
   do not support**.
2. **The cheapest sourced critical part makes it worse, not better.** The one
   traceable 8 mm 18° bipolar PM stepper (MOONS) is **$40/ea** → 80 motors alone =
   $3,200. Sourced DRV8833/TB6612 driver ICs are $0.80–1.33 @100, i.e. **above**
   Test08's $0.60 allowance. Substituting sourced drivers alone moves S5 from
   $432 → ~$490 base ($518.40 → $588.84 with contingency).
3. **Any bought part required on all 6,400 cells kills the budget.** $0.10/cell
   adds $640; even $0.05/cell leaves only $180 for all motors, power, structure
   and electronics. This arithmetic is the strongest result in the test and is
   independent of which mechanism wins.
4. **At 5.08 mm pitch the printed geometry is a fine-nozzle/resin problem, not a
   0.4 mm-nozzle problem.** A 4.68 mm body leaves a 200 µm web, below a 0.4 mm
   line width. The Test08 0.20 mm guide wall is below the fine-nozzle single-wall
   floor once any XY compensation is applied.
5. **A 99% perfect-map goal is far beyond any small prototype.** It needs
   q ≤ 1.57×10⁻⁶ per cell-update and ~1.91 M zero-failure independent trials.
   Per-cell bought hardware with even 0.1% rejects exhausts the whole allowance.

## Method

For each survivor the model sums `quantity × unit price` over **optimistic /
working / high** unit columns, then adds 20% contingency. Categories follow
Test09's `uncategorized` split: actuator, transmission, electronics, power,
wiring, sensor, fasteners, media, module_coupler, programmer, spares, logistics.

Two derived views are reported because they answer different questions:

- **Print-intent floor** — the purchased total if every part the design *intends
  to print* (media, module couplers, decoders, off-board programmer) really is
  printed and works. This isolates "can the bought core fit?". S1 $239, S2 $299,
  S3 $2,519, S4 $311, S5 $432 (working). This is **not** a qualification; it
  assumes away the exact printability/reliability risk this test is measuring.
- **Per-cell sensitivity** — the cost of any bought part needed once per cell.

Sourcing and printability/reliability are in the companion files.

## Per-candidate summary

| Candidate | Optimistic | Working | High | Working +20% | Credible <$500? | Dominant bought line |
|---|---:|---:|---:|---:|---|---|
| S1 threshold/ratchet | $132.19 | $518.00 | $1,122.00 | $621.60 | **No** at working | 64 tile couplers $224 (fallback) |
| S2 planar tiles | $192.19 | $536.00 | $1,206.00 | $643.20 | **No** at working | tile media $96 + 2 axes $96 |
| S3 multi-row DMA | $995.60 | $2,518.60 | $4,876.80 | $3,022.32 | **No, decisively** | 320 selectors $1,600 |
| S4 shared-bus tiles | $206.39 | $503.20 | $1,008.00 | $603.84 | **No** at working | 64 couplers $192 + 64 select drivers |
| S5 rotary reference | $276.00 | $432.00 | $783.00 | $518.40 | **No** with contingency; **only** with unquoted $1.25 motor + $0.60 driver | 80 motors $100 + 80 drivers $48 |

S5 reproduces the Test08 published BOM exactly ($276 / $432 / $783 and
$331.20 / $518.40 / $939.60), so the model is anchored to prior work.

### Why S3 dies on cost

S3 needs 320–400 simultaneously writable selectors. Even at a **speculative**
$2 each the selectors alone are $1,600; sourced commercial solenoids ($3.96 @100+)
put it at $2,800+ for 320. This reproduces `04-architecture-candidates`'
conclusion: the architecture must be **printable/passive fan-out with a handful
of shared drives**, not 320 bought actuators. If it is not, it is
`no credible <$500 path` — not "expensive", but arithmetically out.

### Why S1/S2/S4 are cheaper but still fail

Their working totals are dominated by *fallback* allowances for parts the designs
intend to print (64 tile couplers at $3 across S1/S4). Their **print-intent
floors** ($239 / $299 / $311) are healthier, but that floor is only reachable if
64 printed couplers/media cartridges/decoders are dimensionally reliable across
thousands of cells — exactly what is unproven. The honest statement is:
**S1/S2/S4 have a plausible sub-$500 path only if the printed memory/selector
layer works; if any bought per-cell or per-tile part is needed, they fail.**

## The critical sourcing result

Test08's $1.25 motor assumption is *inside* the marketplace-multipack range
(~$0.70–1.05 on Amazon, ~$2.66+ AliExpress) but has **no traceable matched
quotation**. The only traceable 8 mm 18° bipolar PM part is $40/ea. There is **no
commodity bare 8 mm PM stepper** in LCSC/DigiKey/Mouser/Adafruit/Pololu/DFRobot.

| motor $/ea \ driver $/ea | 0.60 (Test08) | 1.33 (DRV8833PWPR @100) | 2.39 (DRV8833PWR @1) | 0.66 (Amazon board) |
|---|---:|---:|---:|---:|
| 1.25 (Test08 target) | $432.00 | $490.70 | $574.98 | $436.80 |
| 1.00 (Amazon multipack) | $412.00 | $470.70 | $554.98 | $416.80 |
| 0.70 (Amazon multipack) | $388.00 | $446.70 | $530.98 | $392.80 |
| 2.66 (AliExpress) | $544.80 | $603.50 | $687.78 | $549.60 |
| 40.00 (MOONS, traceable) | $3,532.00 | $3,590.70 | $3,674.98 | $3,536.80 |

Only the two cheapest **untraced** marketplace rows and the unverified $0.60
driver stay near the ceiling. Sourcing is now a **first-class blocker**, not a
footnote. Full evidence: [sourcing_notes.md](sourcing_notes.md).

## Printability at 5.08 mm pitch

Screens in `print_reliability.py`:

- **Web width.** body 4.68 mm → 200 µm web (fine-nozzle/resin only); 4.48 mm →
  300 µm; 4.40 mm → 340 µm (both marginal on 0.4 mm, and 4.40 mm drops surface
  fill to 75%).
- **Top-gap stack.** A 0.40 mm nominal gap loses 150 µm (worst case) to
  ±0.10 mm width, ±0.05 mm index and ±0.10 mm deflection. At this pitch the gap
  can close before any dust/creep; it is a coupon problem, not a CAD constant.
- **Guide wall.** Test08's revised 0.20 mm wall is below the fine-nozzle
  single-wall floor with any XY compensation → **0.2 mm nozzle or resin**.
- **Print time.** 12,800–19,200 parts at 45–300 s/part is 160–1,600 printer-hours
  (~1–9 weeks continuous on one X1C). 100% infill for solid mass tests is slower
  still. Print yield across thousands of identical fine parts is unproven.
- **PLA creep/fatigue/wear.** PLA creeps under sustained load; the cam toe
  carries ~3.1 MPa at 1 N and the follower sits preloaded in a guide. Lifetime
  testing is required, not assumed. Dry-cleanable cartridges and replaceable
  followers are mandatory.

## Assembly and reliability scaling

- **P(perfect map) = (1−q)^6400.** At q = 1×10⁻⁴ (a 0.01% per-cell defect rate)
  only **52.7%** of maps are perfect; q = 1×10⁻³ gives 0.17%.
- **99% perfect map** needs q ≤ **1.57×10⁻⁶** per cell-update and
  **1,907,667** zero-failure independent trials for a one-sided 95% bound. No
  small coupon can establish this; **detection with bounded recovery must be
  priced and timed**, or the goal relaxed.
- **Assembly.** 4 parts/cell × 6,400 cells = 25,600 parts; at 10–30 s each that
  is **71–213 hands-on hours**. Detachable 10×10 cartridges and a replaceable
  head/tile strategy are the only practical route; monolithic gluing is excluded.
- **Correlated faults** (one warped tile, one misaligned head, one shared-bus
  fault) invalidate simple per-cell pooling and must be modelled as module/row
  events.

## Decision implications

- **Cost alone currently rejects every survivor at working allowances**, and the
  sourced critical parts make it worse rather than better.
- The decisive next procurement action is **one traceable 8 mm motor sample plus
  an 80+spares delivered quote** (Test09 Stage C). Until that exists, S5's $518.40
  and S1–S4's floors are *not* product-relevant.
- The decisive next fabrication action is the **Stage A process/clearance coupon
  matrix**; the 200–340 µm webs and 0.20 mm guide wall decide whether 5.08 mm
  pitch is ordinary-FDM-fabricable at all.

## Limits

No part was bought, printed or measured. Prices are point-in-time listings
(2026-09-28) and volatile; DigiKey and Mouser blocked retrieval. The model's
"high" column is an engineering envelope, not a retail scenario. Printed-part
fabrication time and machine wear are excluded from purchased cost by project
rule but are not free.
