# DND-56 — Independent ratification of the DND-54 S5-R delivered BOM

- **Verdict: RATIFIED WITH ONE MATERIAL FINDING.** The DND-54 **$397.53 delivered**
  claim reproduces **exactly** from the committed CSV against the repo's own
  delivered-BOM convention (E1–E6 reduced basis, additive ×1.16). The no-channel
  base **$218.70** and the driver-block identity **$218.70 + $63.64 = $282.34** both
  hold, so the S5-R BOM does **not** double-count the 80-channel driver block.
  The **finding** is that the S5-R `bom()` prices the *actuator block's own*
  channels at **zero**: the 80-channel TB6612 block leaves *with* the 80 motors,
  but the 2 bank motors and 40 writer solenoids still need channels. Pricing them
  explicitly puts the honest end-to-end working total at **$401.12 delivered —
  still $98.88 under the $500 ceiling, but $1.12 over the program's ideal <$400
  band**. The two actuator-class unit prices are **allowances, not traced
  listings**, and the sourced order-tier trace confirms them to within ±$0.40.
- **Owner:** Cost, BOM & Manufacturing Engineer (CostManufacturing).
- **Issue:** [DND-56](/DND/issues/DND-56), for [DND-54](/DND/issues/DND-54).
- **Inputs:** `06-experiments/test11_cost_printability_reliability/delivered_3scenario/bom_S5_delivered.csv`
  (committed on `main`); the DND-54 S5-R `bom()` claim; the DND-48/DND-52 E1–E6
  basis in `test12_winner_convergence/cost_closure.py` and `nx52_head_actuator.py`.
  The independent re-derivation is `test12_winner_convergence/s5r_bom_ratify.py`;
  it does **not** import `s5r_register.bom()` for its own arithmetic, and
  `--selftest` reconciles against both committed modules.
- **Evidence class:** CALCULATION over sourced listings and stated assumptions.
  **No part was bought, printed or measured** ([DND-27](/DND/issues/DND-27)).

Run:

```text
cd 06-experiments/test12_winner_convergence
python s5r_bom_ratify.py            # full report
python s5r_bom_ratify.py --selftest # asserts every figure below
python s5r_bom_ratify_checks.py     # regression + honesty gates
```

## 1. What was checked

| # | Question | Method | Result |
|---|---|---|---|
| Q1 | Is the no-channel base $218.70 with the driver block removed? | Re-derive E1–E6 from the CSV by hand | **MATCH** — $218.70; identity $282.34 |
| Q2 | Does the S5-R claim reproduce at $342.70 / $397.53 / $102.47? | Independent additive BOM | **MATCH** — exactly |
| Q3 | Is the uplift the additive ×1.16 (not the DND-37 ×1.166)? | Constant + check | **MATCH** — ×1.1600 |
| Q4 | Are the $12 motor / $2.50 writer traced, or allowances? | Sourced listing trace | **ALLOWANCES, confirmed to ±$0.40** |
| Q5 | Does the S5-R block need its own bought channels? | Channel count + price | **FINDING** — yes, +$3.09 parts |
| Q6 | Delivered total at the real order tier; break-evens for $500/$400? | Scenarios + solve | **$387–$422; motor cap $54.62 / writer cap $4.63 (ceiling)** |
| Q7 | If a traced part costs more, how much margin is consumed? | High scenario | **−$0.39 (motor) / +$0.30 (writer); high still −$78.49** |

## 2. The claim reproduces exactly

`bom()` in `s5r_register.py` is `nx.FIXED_PARTS_NO_CHANNEL + 2×$12 + 40×$2.50`,
then `× 1.16`. Re-derived from the CSV with the sourced prices re-entered by hand:

| Component | Value | Source |
|---|---:|---|
| no-channel fixed base (E1–E6, motor **and** driver removed) | $218.70 | `bom_S5_delivered.csv` |
| 2 × bank motor @ $12.00 **allowance** | $24.00 | DND-52 allowance |
| 40 × writer solenoid @ $2.50 **allowance** | $100.00 | DND-52 allowance |
| **parts** | **$342.70** | |
| **delivered (×1.16)** | **$397.53** | margin **$102.47** |

The no-channel base is the **E1–E6 reduced** basis, not the raw `unit_expected`
column: E1 driver $0.7955, E3 registers $0.0925, E4 controller $5.00, E5 spares
deleted, E6 four fixed lines at their sourced listing prices. Using the raw
`unit_expected` column gives $284.00 and would *not* reproduce the claim; the
DND-54 model correctly inherited the reduced basis. The identity checked by
DND-52's `checks.py` (`218.70 + 63.64 = 282.34`) is asserted here too.

## 3. Q5 — the S5-R block's own channels are priced at zero (finding)

The DND-52 note says: *"The 80-channel driver block ($63.64) leaves with the
motors."* True — but the **S5-R block is a different actuator set** and needs its
own channels; the model's `bom()` charges none:

| New load | Count | Unit | Parts |
|---|---:|---:|---:|
| Bank steppers → H-bridge channel | 2 | TB6612FNG dual IC (working: 1 IC/motor) | $1.59 |
| Writer solenoids → low-side switch | 40 → 5 | ULN2803-class 8-ch darlington @ $0.30 | $1.50 |
| **marginal channel parts** | | | **$3.09** |

The writer solenoids are **ON/OFF**, not bipolar, so they take a ~$0.30 darlington
channel, not a TB6612 H-bridge — this is why the S5-R channel cost is tiny. The
channels are almost certainly **already covered in spirit** by the fixed line
`Custom driver PCBs and passives`, but that line was sized for the 80-motor
H-bridge head, so pricing the marginal channels explicitly makes the S5-R BOM
auditable rather than silently reliant on an over-specified line.

**Honest end-to-end working total: $401.12 delivered** (parts $345.79), margin
**$98.88** under the ceiling. This is **$1.12 over the <$400 ideal band** — the
DND-54 ADR's "inside the ideal <$400 band" statement held only because the block
channels were unpriced. Both figures are reported; the ceiling verdict is
unchanged.

## 4. Q4 — the two actuator-class prices are allowances, confirmed by sourcing

Sourced 2026-09-29 (AliExpress, EUR carried verbatim as USD per the repo's K7
convention; EUR ≥ USD, so conservative for a US buyer).

**Bank stepper** — design need: NEMA17-class, ≥ 0.30 N·m holding, 4-wire bipolar.

| Listing | Price | Torque | Class |
|---|---:|---:|---|
| 17HS4401S 42 N·cm | €12.39 | 0.42 N·m | SOURCED-LIVE, matched |
| HANPOSE 52 N·cm | €13.99 | 0.52 N·m | SOURCED-LIVE, matched |
| 17HS4401S 40 N·cm non-captive | €17.59 | 0.40 N·m | SOURCED-LIVE, matched |
| 17HS4023 pancake | €4.24 | 0.14 N·m | SOURCED-LIVE, **under torque** |

Cheapest **torque-matched** orderable part is **$12.39**, so the **$12.00
allowance is credible** (undershoot $0.39, 3.3 %). The torque class the design
assumes (0.30 N·m) is comfortably covered by a 0.42 N·m part. The cheap €4.24
pancake does **not** meet the 0.30 N·m requirement and must not be used to claim a
lower BOM.

**Writer solenoid** — design need: small 5 V push solenoid, ≥ 1.2 N release.

| Listing | Price | Class |
|---|---:|---|
| 8×10 mm open-frame, 4 mm stroke | €2.20 | SOURCED-LIVE, matched |
| 8×10 mm through-type | €2.59 | SOURCED-LIVE, matched |
| 10 mm cylindrical, 5.5 mm stroke | €2.63 | SOURCED-LIVE, matched |
| 8×10 mm square door-type | €2.84 | SOURCED-LIVE, matched |

Cheapest matched **$2.20**, so the **$2.50 allowance is credible** (overshoot
$0.30). **Caveat:** none of these listings publishes a force (N) figure; the ≥1.2 N
release requirement is the *design's* assumption and is **not** confirmed by the
listings — that remains R-DND54-6.

## 5. Q6/Q7 — scenarios, order tier, break-evens

All scenarios include the block's own channels (§3). Optimistic uses the cheapest
torque-matched motor €12.39 / cheapest writer €2.20 / 1 bank IC; working uses the
DND-54 allowances / 2 bank ICs; high uses €13.99 / €2.84 / 2 bank ICs.

| Scenario | Parts | Delivered | Margin | <$500? | <$400? |
|---|---:|---:|---:|:--:|:--:|
| Optimistic | $333.78 | **$387.18** | $112.82 | yes | **yes** |
| Working (allowances) | $345.79 | **$401.12** | $98.88 | yes | no ($1.12 over) |
| High (premium parts) | $363.37 | **$421.51** | $78.49 | yes | no |
| DND-54 claim (channels unpriced) | $342.70 | $397.53 | $102.47 | yes | yes |

**Break-even unit prices** (working channel cost; the *other* actuator held at its
DND-54 allowance):

| Line | For $500 ceiling | For <$400 ideal |
|---|---:|---:|
| Bank motor (per unit, ×2) | **$54.62** | $11.52 |
| Writer solenoid (per unit, ×40) | **$4.63** | $2.48 |

The ceiling has **large** headroom: the motor could cost **4.5×** its allowance and
the writer **1.85×** before the ceiling is hit. The **ideal <$400 band** is the
tight one: a writer at $2.48/ea or a motor at $11.52/ea (below the cheapest
matched $12.39) is what the band needs. **The honest S5-R verdict is: solidly
under $500, marginally over the <$400 ideal band.**

## 6. What is legitimate (independent conclusions)

- **The claim's arithmetic is correct** and independently reproduced; the
  no-channel basis and the ×1.16 additive uplift are the repo's own convention.
- **No double-count.** The 80-motor line and the 80-channel TB6612 block are both
  removed and never re-added. The S5-R actuators are counted once.
- **The $12 / $2.50 allowances are credible** against sourced order-tier listings
  (±$0.40), unlike the S5 incumbent's refuted K7 motor.
- **The S5-R block's channel cost is negligible ($3.09 parts)** because the
  writers are ON/OFF loads, not bipolar motors — the same insight that removed the
  motor cliff.

## 7. Residual untraced lines

| Line | Status | Why it matters |
|---|---|---|
| Bank motor @ $12.00 | **allowance → traced $12.39** | Torque-matched and orderable; +$0.39 is immaterial at the ceiling. No 2-pc contract quote, only 1-pc listings. |
| Writer solenoid @ $2.50 | **allowance → traced $2.20** | Price supported; **force (N) NOT published** — the 1.2 N requirement is unconfirmed (R-DND54-6). |
| Writer-switch (ULN2803) @ $0.30 | **allowance** | LCSC-class part; not individually quoted. −$1.50 scale, immaterial. |
| Bank H-bridge (TB6612) | **sourced** | Same LCSC C88224 basis as E1; 1 vs 2 ICs changes the total by only $0.80. |
| No-channel fixed base | **inherited** | Carries the DND-47 qualification: E6 mixes best-case into the total. |

## 8. Verdict and next test

**RATIFIED WITH ONE MATERIAL FINDING.**

- The **$397.53** claim is correct and reproducible. The S5-R BOM is **not**
  double-counting the driver block.
- The block's own channels were unpriced; the honest working total is
  **$401.12 delivered**, still **$98.88 under the $500 ceiling** but **outside the
  <$400 ideal band by $1.12**. The DND-54 "inside the ideal band" phrasing should
  read **"in the optimistic scenario; ~$1 over in the working scenario."**
- The two actuator unit prices are **allowances**, now backed by sourced listings
  to within ±$0.40. **No line dies on cost.** The cost gate is robust: the motor
  could cost 4.5× its allowance before the ceiling binds.
- **Remaining cost residual:** the writer solenoid's **force** is unconfirmed by
  any listing, and no 2-piece contract quote exists for either actuator. Both are
  measurement/procurement-only under [DND-27](/DND/issues/DND-27).
- **Next test (analytic, no coupon):** reconcile the S5-R block-channel line into
  the S5-R `bom()` (or explicitly cite `Custom driver PCBs and passives`), and have
  the DND-54 multi-row bar CAD own the channel placement; and update the ADR's
  cost sentence to the **$397.53–$401.12 working range**.
