# S5 winner BOM + printability — ratification (DND-37)

**Verdict: RATIFIED (conditional).** The S5 purchased BOM and the X1C/PLA 0.4 mm modular
printability route are ratified as the program winner, with one named residual cost risk
(the motor supply) and one named residual process risk (K2 detent friction). Neither is a
reason to reject; both are stated so they cannot be mistaken for closed.

**Evidence class.** CALCULATION over sourced listings + stated allowances. **No purchase,
no print, no measurement** ([DND-27](/DND/issues/DND-27)). Every figure below is arithmetic
on `bom_S5_delivered.csv` and the LCSC/marketplace listings recorded in
`../test11_cost_printability_reliability/sourcing_notes.md` (observed 2026-09-28).

Run all checks:

```text
python 06-experiments/test12_winner_convergence/model.py
python 06-experiments/test12_winner_convergence/checks.py
```

---

## 1. Arithmetic verified — no drift, no double-count

`checks.py::test_fixed_subtotal_is_reproduced_from_the_sourced_bom` recomputes the fixed
subtotal directly from the sourced CSV. Independently re-derived for this note:

| Component | Derivation | Value |
|---|---|---:|
| Fixed (non motor/driver) expected subtotal | Σ qty×unit_expected over 16 CSV rows, excl. `PM motor`, `Dual H-bridge` | **$284.00** |
| Sourced pair parts | 284.00 + 80×$1.05 (motor) + 80×$0.80 (TB6612) | $432.00 |
| Sourced pair **delivered** (×1.10 ship ×1.06 tax = ×1.166) | 432.00 × 1.166 | **$503.71** |
| Two consolidations | − $14.00 (registers onto PCB) − $5.00 (RP2040 $10→$5) | −$19.00 |
| Reduced parts | 265.00 + 64.00 + 64.00 | $413.00 |
| Reduced **delivered** | 413.00 × 1.166 | **$481.56** |

Both totals reproduce the model exactly. **The two consolidations are real and not
double-counted:**

- **Registers (−$14):** the CSV carries a discrete line `8-bit shift registers (74HC595)`,
  40 × $0.35 expected = $14.00, *and* a separate `Custom driver PCBs and passives` line
  ($25). Folding 40 discrete registers onto that already-budgeted PCB is a genuine net
  removal of the discrete line — it is not charging the PCB twice.
- **Controller (−$5):** the CSV `Controller` expected is the $10 Pico-module allowance;
  the sourced RP2040 bare chip is $0.7645 @100 (LCSC C2040). The model conservatively
  credits only $5, keeping support passives/regulator in the line. Defensible.

**The driver substitution is also real:** the CSV's `Dual H-bridge channel` line prices
DRV8833PWPR at **$1.58** expected; the model uses **TB6612FNG @ $0.7955 @100** (LCSC
C88224), a dual H-bridge that drives one bipolar PM stepper per package (same channel
count). This is a **cheaper sourced matched part**, not a discount assumption.

## 2. Is there a *sourced* path to the <$400 ideal band? — **No.**

The fixed structure is already lean and mostly essential; the motor/driver pair is the
only large swing. Solving for the pair price that delivers at $400:

| Fixed subtotal | Parts budget for $400 delivered (400/1.166 = $343.05) | Required motor+driver pair /ea |
|---|---:|---:|
| $284.00 (unreduced) | $59.05 | **$0.7382** |
| $265.00 (reduced) | $78.05 | **$0.9757** |

So even with both consolidations, the whole 80-channel motor+driver pair must average
**≤ ~$0.98** to reach $400 — and to reach $500 it must be ≤ ~$2.23. There is **no sourced
part at $0.74–0.98 for a motor+driver pair.** The cheapest sourced bipolar driver alone is
$0.7955 (TB6612 @100); the cheapest credible motor is $1.05 (untraced multipack). The pair
floor is ~$1.85, not $0.98.

Additional candidate cuts considered and **rejected** (not double-countable / not sourced):

| Candidate | Verdict |
|---|---|
| Lift motor line ($18 expected) | **Cannot cut** — the sourced retail planetary NEMA17 is ≈EUR24.19, i.e. the expected line is already *below market*. |
| Scanner motor ($12 allowance) | Unproven — needs a sourced NEMA-8/11 listing to become a real, traceable reduction. Audit candidate, not a ratified saving. |
| Guides/rails ($40) | Already sourced-bundled; no verified split to reduce. |
| Power/wiring/loom/fasteners | Sourced-bundled essentials; no legitimate sourced reduction identified. |

**Hard floor (informational):** with a *free* motor+driver pair, the reduced fixed stack is
still **$308.99 delivered** ($331.14 unreduced). So <$400 is theoretically *reachable* only
if a ~$0.98 motor+driver pair existed; it does not. **Statement required by DND-37
§2: no sourced <$400 path exists on current evidence.**

## 3. Sourced matched 8 mm bipolar PM stepper near $1.00 — **not identified**

- The **only traceable, matched** 8 mm 18° bipolar PM stepper is **MOONS 8PM020S1-02001
  at $40.00/ea** → $3,200 for 80, ~$4,000 delivered. That is not a cost path.
- The **sub-$1.05 price is an untraced marketplace multipack** (Amazon "Abovehill" 10-pair
  pack, ≈EUR0.97/ea, 2026-09-28). Its **winding, shaft, lot and holding torque are
  unverified**. The sourced matched part has only **0.4 mN·m holding torque**.
- LCSC / DigiKey / Mouser / Adafruit / Pololu / DFRobot **do not stock a bare commodity
  8 mm 18° bipolar PM stepper** as a discrete.

**Residual cost risk, stated precisely:** the winner's $481.56–$503.71 delivered total
rests on a **~$1.05 motor with no matched quotation and no verified datasheet**. If the
multipack cannot deliver the required step angle/torque at the required lot consistency,
the only matched replacement is ~**$40/ea**, which puts S5 at **~$4,000** — arithmetically
dead. The gap between $1.05 and $40 is a **sourcing-qualification risk**, not a number we
can average away. This is the single most important open item for the program.

## 4. Printability route — RATIFIED (X1C / PLA / 0.4 mm, modular cartridges)

- The stack-up is a **0.4 mm-nozzle, ordinary X1C PLA** design at module/cartridge scale;
  no line calls for resin or a 0.2 mm nozzle in the S5 winner routes.
- The pitch-critical features are handled by **modular cartridges** (replaceable tiles)
  rather than a monolithic 6,400-cell print, which is the only practical yield strategy.
- **Residual process risk (K2):** the printed rotary detent corrects a one-step slip only
  for printed contact friction **μ ≤ 0.323** or a scallop deepened to **≥ 0.31 mm**
  ([DETENT_CONTACT.md](DETENT_CONTACT.md), [DND-38](/DND/issues/DND-38)); the sourced
  PLA–PLA midpoint μ≈0.35 does **not** correct at nominal. This bounds the design, it does
  not kill it: the closing levers are known and printable, but the as-printed μ/creep cannot
  be measured under [DND-27](/DND/issues/DND-27).

## 5. What is ratified vs what remains open

**Ratified:** the S5 purchased BOM structure ($284 fixed reproduced from source), the
sourced-pair cost (~$503.71) and the reduction path (~$481.56, clears $500 with margin),
the driver substitution (TB6612 $0.7955 < DRV8833 $1.58), and the X1C/PLA 0.4 mm modular
printability route.

**Open (named, not hidden):**
1. **Motor supply qualification** — no matched quote; multipack specs unverified; matched
   fallback is ~$40/ea (~$4,000). *This is the program's #1 cost risk.*
2. **K2 detent friction** — needs μ ≤ 0.323 or scallop ≥ 0.31 mm as-printed.
3. **Reliability q** — assumed 1×10⁻⁴; no per-cell feedback; 99% map needs q ≤ 1.57×10⁻⁶.
4. **Travel envelope** — 40 mm is provisional (`miniature_measured: false`).

## 6. Cheapest next test (no purchase, no print under DND-27)

**Obtain one traceable, matched 8 mm 18° bipolar PM stepper datasheet + price at the
required lot (80 + spares), delivered-inclusive.** One document either confirms the
$481.56 path or collapses S5 to the ~$4,000 matched scenario. It is the highest-value
per-dollar action in the program and requires no hardware.
