# 08 — Current design: S5 — programmed stepped rotary stops + common lift

**Status:** PROMOTED as the single buildable winner by
[ADR-002](../07-evidence-and-decisions/convergence-decision-2026-09-b.md)
([DND-35](/DND/issues/DND-35)). This directory is now the engineering source of truth for
the machine. The DND-44 readiness closure advanced this from an honest *analytic
definition* to the closest reachable print-ready state; the **DND-46 adversarial audit**
then broke three of the six DND-44 headlines, and **DND-48** folds those robust figures
back in (below). Only K10 is a clean analytic bound; K1-service, K5 and K8 are **not
closed** as published, K6 is **conditional** on a dwell *and* a loaded rate, and K11 is a
**pseudo-quantitative** point estimate. The residual is a short list of named physical
quantities (see [§7](#7-residual-uncertainty--risk-register) and the **Final readiness
verdict** at the end).

**Evidence class:** CALCULATION / SIMULATION / CAD over sourced listings and stated
assumptions. **No printed or measured evidence exists and none will be produced**
([DND-27](/DND/issues/DND-27)). Every quantitative claim below states its class; the
residual assumptions are listed in [§7](#7-residual-uncertainty--risk-register).

**K7 update ([DND-52](/DND/issues/DND-52)):** the head-actuator / drive-topology pivot
screen found **no analytically retirable fix on the incumbent 80-motor head**, but
**one cost+time-viable pivot — S5-R, a shared-drive programmable rotary register**
($304.73 delivered, 24.65 s) — which trades the bought-motor cliff for an unproven
selective-dropout mechanism. See §8 item 8 and the
[ADR](../07-evidence-and-decisions/dnd52-head-actuator-pivot.md).

**S5-R update ([DND-54](/DND/issues/DND-54)):** the analytic + CAD dropout-latch model
**closes the S5-R mechanism the way [DND-27](/DND/issues/DND-27) allows and promotes
S5-R to a machine-definition candidate** — as a **4-row-deep shared bank** (the
DND-52 option-1 was single-row and, counted honestly per row, could not meet 30 s).
At R=4 with 40 writer solenoids and 2 bank motors: **$397.53 delivered, 24.62 s**,
with all seven analytic gates passing (cell fit, zero neighbour cross-talk, writer
force 18×, bank force 2.15×, latch inherits K1, time +5.4 s, cost −$102). See
[§8 item 9](#8-next-actions) and the
[ADR](../07-evidence-and-decisions/dnd54-s5r-register-latch.md). This is **CAD +
CALCULATION only** — no print, no measurement; the as-printed μ/creep and the
multi-row bar assembly remain named residuals.

---

## 1. Machine in one paragraph

An 80 × 80 array of **square printed columns** at 5.08 mm pitch (406.4 × 406.4 mm) is
divided into independently printable **cartridges/modules** because the 406 mm span
exceeds the 256 mm X1C bed. Each column carries **five passive stepped rotary cams** (a
5-level height memory) and rides on a **common lifting platen**. A **full-width 80-channel
programming head** travels row-to-row: it indexes over a row, couples 80 small permanent-
magnet steppers to the 80 column rotors, rotates each rotor to the selected hard-stop
level, releases, and moves on. A single platen stroke of 41 mm (40 mm travel + 1 mm unload
clearance) raises all columns so the newly-selected rotor steps seat as the platen lowers.
The rotor's hard stop, not any powered element, **holds terrain load**, so the machine
draws no holding power per cell.

## 2. Why this machine (and not the others)

| Criterion | S5 result | Nearest rival |
|---|---|---|
| Real CAD of mechanism | **yes** — rotor/follower/guides/lift plate, interference-checked | S1/S2/S4: none |
| Timing under 30 s | **26.251 s** (reproduced) | S3 25.20 s (budget only) |
| Purchased BOM sourced share | **82 %** | S4 37 %, S1 30 % |
| Per-cell bought parts | **0** (passive printed rotors) | all survivors: 0 intended |
| Expected-delivered cost | **$482.95 robust** (DND-48) / $501.51 over-ceiling expected-motor case | S4 $548.91 |
| Decisive failure | none quantitative; K1-service now the bounding structural residual | S1 force, S2 surprise maps, S3 printability+cost, S4 clutch+backlash |

ADRs and evidence: [ADR-002](../07-evidence-and-decisions/convergence-decision-2026-09-b.md),
[Test12 stack-up](../06-experiments/test12_winner_convergence/),
[Test08 CAD + machine](../06-experiments/test08_architecture_search/),
[Test09 validation](../06-experiments/test09_test08_validation/).

## 3. Functional allocation (all ten jobs named)

| Job | Mechanism | Evidence |
|---|---|---|
| Map representation | per-rotor angle (5 levels × 80×80), firmware map | CAD |
| Selection | 80-channel rotary head, firmware bitmap | CAD + calculation |
| Power delivery | shared platen + one head drive train | calculation |
| Vertical positioning | common platen lift, 41 mm stroke | CAD + calculation |
| State retention | passive stepped cam + hard stop + detent leaf | CAD + analytic bound **K2 (DND-38)** |
| Tabletop load support | hard stop / toe contact (3.11 MPa @ 1 N) | calculation |
| Lowering / reset | platen lower, gravity return | calculation |
| Regional isolation | per-column rotor memory (only the touched row's rotors move) | analytic bound |
| Programming | row-serial head writes; regional = rewrite only affected rows | calculation |
| Detection / recovery | axis reference sensors (no per-cell feedback) | assumption |

## 4. Key dimensions

| Parameter | Value | Basis |
|---|---:|---|
| Grid | 80 × 80 = 6,400 cells | design criteria |
| Pitch | 5.08 mm | design criteria (1 in / 5) |
| Column body | 4.68 mm square, 80.2 mm long | CAD (leaves 0.40 mm top gap) |
| Travel | 40 mm (provisional envelope) | design criteria — **not** miniature-verified |
| Levels / increment | 5 / 10.0 mm | calculation |
| Cam radius / core | 1.5 mm / **1.0 mm** (re-evaluate against ~3.3 N tripod service load) | CAD (1.0 mm core; buckling **not** closed — DND-48) |
| Platen stroke | 41 mm (40 + 1 unload) | calculation |
| Head | 80 channels, 18° PM steppers, 400 pps | calculation |
| Active area | 406.4 × 406.4 mm, modular for X1C | design criteria |

## 5. Bill of materials (purchased)

Base = the S5 delivered BOM (`06-experiments/test11_cost_printability_reliability/delivered_3scenario/bom_S5_delivered.csv`).
Fixed expected subtotal **$284.00**; motor + driver channel is the cost driver.

| Line | Qty | Sourced part | Unit | Delivered basis |
|---|---:|---|---:|---|
| 8 mm 18° bipolar PM stepper | 80 | Amazon multipack 8 mm (sourced listing) | $1.05 | 2026-09-28 |
| Dual H-bridge driver | 80 | TB6612FNG @100 (LCSC) | $0.80 | 2026-09-28 |
| Controller | 1 | RP2040 (LCSC C2040) | $5.00 | sourced |
| Shift registers | 40 → 0 | 74HC595 → folded onto driver PCB | — | consolidation |
| Driver PCBs + passives | 1 | JLCPCB/LCSC | $25.00 | allowance |
| Scanner motor | 1 | — | $12.00 | allowance |
| Lift motor (planetary NEMA17) | 1 | AliExpress | $18.00 | sourced listing |
| Coupling/lift engagement | 1 | spring-compliant beam | $8.00 | allowance |
| Axis drivers | 3 | TB6612 boards | $3.00 | allowance |
| Guide rods/rails/bearings | 1 | AliExpress | $40.00 | sourced |
| Four lift screws + nuts (T8, 8 mm lead) | 1 | AliExpress | $20.00 | sourced — **lead to be re-sized ≤2 mm per Step 6 (DND-43); 8 mm fails the torque-speed gate at 0.51×** |
| Belts/pulleys/idlers | 1 | AliExpress | $20.00 | allowance |
| Power supply + protection (24 V) | 1 | AliExpress SMPS | $35.00 | sourced |
| Axis reference sensors | 4 | AliExpress | $1.00 | allowance |
| Wire/connectors/loom | 1 | AliExpress JST/Dupont | $22.00 | sourced |
| Head shafts + friction pads | 1 | AliExpress brass/felt | $20.00 | sourced |
| Fasteners | 1 | AliExpress M2/M3 | $12.00 | sourced |
| Spares / misc | 1 | — | $15.00 | allowance |

**Totals (expected delivered, additive ×1.16):**

| Scenario | Purchased parts | Delivered | Verdict |
|---|---|---:|---|
| **Honest expected baseline (DND-44, BOM `unit_expected`)** | $510.40 | **$592.06** | **over the ceiling** |
| As-listed (sourced pair: $1.05 motor + $0.80 TB6612) | $432.00 | $501.12 | over the ceiling by $1.12 |
| DND-44 four-best-case path (E1–E6, spares deleted) | $366.34 | $424.95 | clears, $75.05 margin — **not defensible as stated** |
| **Robust planning basis (DND-48): E5 spares + E6 bundled lines restored** | **$416.34** | **$482.95** | **clears, $17.05 margin** |
| Same, with the *sourced* DRV8833PWPR driver ($1.3338) | $409.40 | $474.91 | clears, $25.09 margin |
| E5 + E6 + expected motor ($1.25) | $432.34 | **$501.51** | **over the ceiling** |

Reproduced and asserted by `06-experiments/test12_winner_convergence/checks.py` and
`falsifier_checks.py`.
**Cost correction ([DND-41](/DND/issues/DND-41) + [DND-44](/DND/issues/DND-44) + [DND-46](/DND/issues/DND-46) + [DND-48](/DND/issues/DND-48)):** the prior
$501.12 headline was optimistic — it paired a $0.80 TB6612 (not the sourced DRV8833 the BOM's
expected column carries at $1.58) with a best-case $1.05 motor. Re-derived from the BOM's own
`unit_expected` column, the **honest expected delivered baseline is $592.06**. The DND-44
machine-preserving source path landed at **$424.95 delivered ($75.05 margin)** — but the
[DND-46](/DND/issues/DND-46) audit showed that margin requires **four simultaneous best-case
choices**, two of which are not defensible:
- **E5 deletes the spares allowance ($15)** — a build needs replacement stock.
- **E6 reprices four bundled structural lines** (guide rods, belts, head shafts, fasteners)
  from `unit_expected` ($40/$20/$20/$12) to their `unit_best_usd` ($25/$12/$12/$8), consuming
  the entire best-to-expected gap on lines with **no machine change** — $35 of the $144 reduction.

Restoring both gives the **defensible planning basis: $482.95 delivered, $17.05 under the
ceiling**. The still-legitimate driver swap (TB6612FNG, a dual H-bridge for dual H-bridge at the
@100 LCSC price of $0.7955) is best-in-price: at the repo's *other* sourced driver (DRV8833PWPR
C50506, $1.3338) the total is $474.91. Every change preserves the mechanism, pitch, travel, cell
count and drive topology; all the variants are audited line-by-line in `test12/cost_closure.py`
and attacked in `test12/falsifier_checks.py`. **The path clears only for a motor ≤ $1.86
delivered**; at the expected $1.25 motor, with E5+E6 restored, it is **over the ceiling at
$501.51**.

**The one cost risk (K7):** the only *traceable matched* 8 mm 18° bipolar PM stepper found
(MOONS 8PM020S1) lists at **$40/ea**; the cheapest *matched, orderable* part is a Chinese OEM
(CCHT) at **$11.20 @100** (→ **$1,366.87 delivered**) and **$8.20 @3,001+** (→ $1,088.47). The
sub-$1.86 price is an untraced marketplace multipack with **no published step angle** and must be
sample-verified by the purchaser before a build; [DND-49](/DND/issues/DND-49) therefore records K7
**refuted on sourced evidence** — no matched, traced part exists at ≤$1.86, and the reduced-head
design lever breaks the 30 s budget. This is the **binding residual** of the cost path (see §7).

## 6. Fabrication, assembly and print readiness

**Process baseline:** Bambu X1C, PLA, 0.4 mm nozzle, 0.20 mm layers; optional 0.2 mm nozzle
for the thin upper guides.

**Modularity:** the 406.4 mm field is split into printable cartridges (e.g. 4 × 8 modules
of 20×10 cells ≈ 101.6 × 50.8 mm) that bolt to a spliced frame. **Support spacing is set by
Step 6 (DND-43), not by the earlier monolithic estimate:** with the bolted splice modelled
at the soft printed modulus the frame needs support **every ≤ ~150 mm** to hold the 0.25 mm
flatness budget (203.2 mm gives 0.514 mm and **fails**). Either split each axis into **3
cartridges** (≈135 mm), or raise the as-printed rail modulus toward bulk PLA, for which
203.2 mm passes at 0.144 mm. See
[`test13_step6_load_structure_power/`](../06-experiments/test13_step6_load_structure_power/).

**Print-ready geometry (CAD, not a print):**
- `06-experiments/test08_architecture_search/coupon.scad` — rotor, follower, follower
  guide, body guide, lift plate, assembly, section; driven by `results/parameters.scad`
  generated from `params.json` (run `analysis.py` first).
- Interference is checked at five levels and twenty raised angles by `cad_check.py`.
- The software-only harness (`tools/validate/validate_geometry.py`) renders with real
  OpenSCAD and applies sourced FDM process limits.

**Assembly route (first article = the 3×2 coupon, 15.24 × 10.16 mm):**
1. Print the coupon set with a 0.2 mm nozzle: 6 followers, 6 rotors, 6 slotted follower
   guides, 2 upper guide tiers, 1 lift plate.
2. Ream printed rotor bushings; support rotor axes and guide tiers square in an external
   fixture (tiers at z = 110.2–114.2 / 118.2–122.2 on assembly).
3. Rotate rotors by hand without lifting their shafts; verify five-level seating.
4. Raise the common plate with a micrometer/screw stage; record seating at each level.
5. Fail criteria (from `test08/README.md`): a level change on unloading, a jam, or a
   minimum wall below the sourced process floor is a **geometry failure**, not a reason to
   enlarge the pitch silently.

**What the coupon is not:** it is a contact/guide/fit coupon, not an automated printer. The
thrust retainer, brake, detent leaf and motor head are **not** in the STLs; their omission
is not proof they fit.

## 7. Residual uncertainty / risk register

| id | Risk | Class | Status |
|---|---|---|---|
| K1 | Cam buckling under handling load | calculation | **service load NOT closed (DND-46)** — the DND-44 "≤0.39 N/column, 12.7× margin" assumed the base conforms to *every* column top beneath it. A shape display's defining property is that column tops are at **different heights**, so a rigid base stands on the **highest three** columns (a three-point contact): 1 kg → **3.27 N/column**, only **1.5× margin** vs the 4.96 N core. Service load is therefore **0.39–3.27 N/column depending on base contact**; the three-point case is the bounding model, so **size the core against ~3.3 N**. The localized 5 N abuse screen is **bounded**: a core re-size to 1.10 mm gives **5.60 N** and clears it, at the cost of step height 0.5→0.4 mm (a real geometry trade, not a free fix). Residual: the real base contact model. `test12/buckling_closure.py`, `falsifier_checks.py` |
| K2 | Printed detent holds/repeats after a slipped step | calculation | **closed-analytically (named geometry, DND-45)** — nominal 0.20 mm scallop fails at the sourced PLA–PLA midpoint μ = 0.35 (torque/friction 0.92). The chosen **0.40 mm scallop** gives **1.84 at μ = 0.35** and **1.29 at μ = 0.50**, inside the 0.50 mm cam envelope (exact min depth 0.271 mm at μ = 0.35). As-printed μ/creep/tip sharpness remain measurement-only. `test12/DETENT_CONTACT.md` |
| K3 | Gravity return vs guide friction | calculation | **closed** — 4.06× weight/drag margin (solid column) |
| K4 | Regional update disturbs neighbour | calculation | **partially-closed** — 0.017 mm rail-bending *structural* sub-bound vs a 0.10 mm gate; J2 engine returns **INCONCLUSIVE** — stiction release and wear drift are measurement-only. ([DND-41](/DND/issues/DND-41)) |
| K5 | Cost > $500 delivered | calculation | **not closed at $424.95 (DND-46)** — that headline needed four simultaneous best-case choices (E5 spares deleted + E6 bundled lines repriced). Defensible planning basis: **$482.95 delivered, $17.05 margin** (spares + E6 restored). Sourced-DRV8833 variant **$474.91**. At the expected $1.25 motor it is **$501.51, over the ceiling**. E6 is best-case repricing, not sourcing, and is labelled as such. Conditional on a motor ≤ **$1.86**. `test12/cost_closure.py`, `falsifier_checks.py` |
| K6 | Time > 30 s at the realised step rate | calculation | **conditional (DND-46)** — 26.251 s at the design point; the **rate-independent floor is 18.65 s**. The closure is **conditional on a loaded engage/settle dwell AND a ≥268 pps (~804 rpm) loaded rate**; ~268 pps only *just* meets 30 s, and the pass assumes **`inspection_s = 0`** (at 3 s inspection the design point is 29.25 s — meets the hard cap, misses the 27 s target). The 45.07 s sweep corner is *not* rate-recoverable (its floor is 34.47 s). Verify the loaded dwell and scan accel, not a "measured rate". `test12/timing_closure.py`, `falsifier_checks.py` |
| K7 | Purchased-actuator cost cliff (80 motors) | assumption | **open — the binding residual of K5; REFUTED at ≤$1.86 on sourced evidence ([DND-49](/DND/issues/DND-49)); no actuator-class/pivot retires it ([DND-52](/DND/issues/DND-52))** — the sub-$1.86 clearing path needs an untraced multipack with **no published step angle**; every *matched, orderable* part found is $8.20–$40 → **$1,088–$4,040 delivered**. The only traced matched part (MOONS 8PM020S1) is $40 → $4,040. The reduced-head lever (fewer motors) **fails the 30 s budget** (40 channels → ~104 s) **and fails cost on the order tier** (R=4 → $531.99; boundary $9.82/station vs the $11.20 tier). Unretired only by a purchase sample (forbidden under [DND-27](/DND/issues/DND-27)) **or the S5-R shared-register pivot**. **[DND-54](/DND/issues/DND-54) closes the S5-R dropout mechanism analytically** (R=4 bank, $397.53, 24.62 s, all gates pass) and promotes it. `test12/k7_motor_trace.py`, `nx52_head_actuator.py`, `s5r_register.py` |
| K8 | Lateral holding (knocked miniature) | calculation | **open — worse than stated (DND-46)** — the DND-44 "1 N → 0.01 mm, limit ~9.4 N" hard-coded a **12 mm free length** with no geometry basis. The repo's own `unrelieved_upper_body_length_mm` is **40 mm** (80.2 − 40.2), where `L³` scaling gives **0.356 mm at 1 N** (3.5× the 0.10 mm neighbour gate) and a 0.10 mm-gate load of only **0.28 N**. The governing limit is set by the chosen free length and an unsourced guide-shear constant, not the mechanism. Gate: the **free-length / guide-capture geometry** (extension vs tier capture) plus printed guide-wall shear. `test12/cross_cutting_closure.py`, `falsifier_checks.py` |
| K9 | Angular margin vs print tolerance | calculation | **closed-analytically (DND-45)** — Monte-Carlo of the sourced ±0.05 mm FDM tolerance: 5 levels keep margin positive (worst draw **1.72°**, mean 5.52°, 0 % fail bounded / **1.31 %** Gaussian); **6 levels fail 65.6 %**; **4 levels robust**. The K12 level-count tradeoff now carries a hard margin bound. `test12/K9_ANGULAR_MARGIN.md` |
| K10 | Regional-update time untested end to end | calculation | **closed-analytically (DND-44)** — common platen ⇒ one full 41 mm stroke per update: 1 row ~**3.9 s**, 10 rows ~**6.3 s**, 80 rows ~**24.7 s**. `test12/cross_cutting_closure.py` |
| K11 | Cycle life of printed detent/ratchet | calculation | **pseudo-quantitative (DND-46)** — the DND-44 "~10⁸ cycles" point estimate (9.98e7) rests on two asserted, unsourced FDM constants (ε_endurance = 0.3 %, Basquin m = 8). A conservative FDM endurance (0.2 %) drops it 25× to ~3.9e6; defensible constants span **4e5–1e9**. Report as **">=1e6, order unknown"**. For context, a full map cycles each detent once per row (~80×), so 1e6 detent cycles is ~12.5k full maps — the real risk is creep/layer adhesion, not high-cycle fatigue. `test12/cross_cutting_closure.py`, `falsifier_checks.py` |
| K12 | Coarse-slope / multi-level usability | assumption | **open — product decision** — 10 mm steps may be too coarse; a product/usability choice, not an engineering gap |
| R1 | Whole-map reliability | assumption | open — q ≤ 1.57×10⁻⁶ needed for 99 %; no per-cell feedback |
| R2 | 40 mm travel vs real miniature | assumption | open — no miniature measured; requirement may change |
| R3 | Realised step rate ≥ 400 pps loaded | assumption | **reframed by DND-44** — the binding quantity is the loaded engagement/settle dwell (K6), not the step rate per se |
| R4 | Matched motor supply at < $1.05 | assumption | open — only traceable matched part is $40/ea (same as K7) |
| R5 | Frame/platen splice stiffness ratio (k = 0.25 assumed) | assumption | open — sets the ≤150 mm support spacing; higher k relaxes to 203.2 mm. Step 6 (DND-43) |
| R6 | As-printed rail modulus (700 vs 2500 MPa spans the flatness pass/fail line) | assumption | open — Step 6 (DND-43) |
| R7 | Sourced lift-motor torque at speed (0.30 N·m assumed) | assumption | open — Step 6 drive sizing depends on it until sample-verified |
| R8 | Lift lead must be ≤ 2 mm (8 mm fails 0.51×); power cut back-drives the screw (not self-locking) | calculation | open — **new required item**: a friction brake or platen detent, not yet in the BOM or the 26.25 s timing budget. Step 6 (DND-43) |

**Readiness summary (DND-41):** the S5 direction survives, but the winner is **not** "closed"
on cost, time or isolation as previously stated. It is **on/just over the $500 ceiling**;
time is **conditional** on an unmeasured step rate; isolation is a **structural sub-bound only**;
and K1 plus K7–K12 remain **open**. This is an honest readiness statement, not a print-ready
claim.

**Readiness update (DND-44):** the picture was sharper and materially better, but still not a
print-ready claim. K1 (service), K5 (sourced path), K6 (reframed), K8 and K10 were reported as
**closed analytically**; K11 as **bounded**; K2 and K4 remained **conditional on a printed
contact/release measurement**.

**Readiness update (DND-46 / DND-48 — the robust register):** the DND-46 adversarial audit broke
**three of those six closures as published** and reframed two more. Only **K10 is a clean analytic
bound**. What survives is:
- **K1-service** is **0.39–3.27 N/column** (base-contact dependent); the tripod case is bounding
  and leaves only ~1.5× margin — size the core against **~3.3 N**.
- **K5** is **$482.95** on the defensible basis (not $424.95), **$474.91** with the sourced
  DRV8833, and **$501.51 (over)** at the expected motor.
- **K8** is **open and worse**: at the repo's own 40 mm free length, 1 N deflects **0.356 mm** and
  the 0.10 mm-gate load is **0.28 N** — the gate is a **free-length/guide-capture** question.
- **K6** is **conditional on a loaded dwell AND a ≥268 pps (~804 rpm) loaded rate**, with
  `inspection_s = 0` assumed.
- **K11** is **">=1e6, order unknown"** (4e5–1e9 across defensible FDM constants).
The binding residuals are **K7 + the E5/E6 best-case-pricing basis of K5**, the **K1 base-contact
model**, the **K8 free-length/guide-capture**, and the print-realisation quantities (μ, scallop
depth, guide shear, creep, rotor tolerance). See the **Final readiness verdict** below.

## 8. Next actions

1. **Analytic detent contact sweep** — **done** ([DND-38](/DND/issues/DND-38),
   `test12_winner_convergence/DETENT_CONTACT.md`): K2 bounded, conditional. **DND-44**
   took it further: geometry selection at the sourced μ midpoint is delegated
   ([DND-45](/DND/issues/DND-45)). Next physical step is a printed μ + scallop coupon,
   which DND-27 forbids.
2. **DND-44 readiness closure** — **done** (`test12_winner_convergence/DND44_READINESS.md`,
   four analytic modules + 46 CI checks). K1(service)/K5/K6/K8/K10 closed; K11 bounded.
3. **Step-6 load/structure/power** — **done** ([DND-43](/DND/issues/DND-43),
   `test13_step6_load_structure_power/`): corrected support spacing (≤ ~150 mm or stiffer
   rail), lift lead (≤ 2 mm or larger motor), and a now-required power-cut brake/detent.
   **Open follow-up for CostMfg/Fabricator:** fold the brake/detent and the re-sized lead
   into the BOM and the timing budget, and update the CAD support layout.
4. **Falsifier adversarial audit** of the DND-44 closures — **done**
   ([DND-46](/DND/issues/DND-46), `test12_winner_convergence/FALSIFIER_AUDIT.md`,
   `falsifier_checks.py`, 19 CI checks). Broke K1/K5/K8; reframed K6 and K11.
5. **DND-48 fold the robust figures into this register** — **done** (§5, §7, §9 here; the
   `plan` document). Robust planning numbers replace the DND-44 headlines.
6. **CostManufacturing** ratifies the machine-preserving cost path — [DND-47](/DND/issues/DND-47).
7. **Fabricator** confirms the CAD is print-ready against the harness and X1C envelope.
8. **Actuator-class / drive-topology pivot** — **done** ([DND-52](/DND/issues/DND-52),
   `test12_winner_convergence/nx52_head_actuator.py` + `_checks.py`, ADR
   [`dnd52-head-actuator-pivot.md`](../07-evidence-and-decisions/dnd52-head-actuator-pivot.md)).
   K7 has **no analytically retirable fix on the incumbent S5 head**: every
   bought-actuator lever fails cost on the real price tier or pitch. **One pivot
   survives — S5-R, a shared-drive one-time programmable rotary register** (2 index
   motors + 8 writer solenoids, **$304.73 delivered**, **24.65 s**), which removes
   the 80-bought-motor cliff entirely but rests on the unproven selective
   dropout/re-engage of an 80-rotor bank at 5.08 mm pitch (a coupon, forbidden
   under [DND-27](/DND/issues/DND-27)). Next agent-reachable step: an **analytic / CAD
   kinematic model** of the register dropout latch (not a print) to decide whether
   S5-R can be machine-defined.
9. **S5-R analytic + CAD dropout-latch model** — **done** ([DND-54](/DND/issues/DND-54),
   `test12_winner_convergence/s5r_register.py` + `_checks.py` + `s5r_register.scad`,
   ADR [`dnd54-s5r-register-latch.md`](../07-evidence-and-decisions/dnd54-s5r-register-latch.md)).
   The **R=4 shared-drive bank register** (40 writers, 2 bank motors) **clears every
   analytic gate**: cell fit, zero neighbour cross-talk (a dropped pawl carries no
   rack force), writer force 18×, bank force 2.15×, latch dormant in service
   (inherits K1), **24.62 s full map**, **$397.53 delivered**. Real CAD of the unit
   cell renders and passes the sourced printability gate (one accepted RISK: the
   0.45 mm keeper leaf is 1 extrusion line). **Verdict: promote S5-R to a
   machine-definition candidate**; the remaining residuals (as-printed μ, gate/tip
   sharpness, leaf creep, the multi-row bar assembly) are measurement/CAD-gated and
   unmeasurable under [DND-27](/DND/issues/DND-27). Next discriminating (no-coupon)
   test: a **multi-row (R=4) bar-assembly CAD** for torsion / reset-comber / writer
   envelope.

---

## 9. Final readiness verdict (DND-46 / DND-48 — robust register)

**Verdict: NOT YET PRINT-READY, and the remaining gap is larger than DND-44 stated, but still
specific and named.**

The [DND-46](/DND/issues/DND-46) adversarial audit broke three of the six DND-44 closure
headlines. The S5 winner still survives — no killer is proven to kill the architecture — but the
readiness statement must **not** carry the DND-44 headlines as written. This is the robust
register, matching `FALSIFIER_AUDIT.md` §8.

**Clean analytic bound (calculation, no print):**
- **K10** — regional updates bounded: 1 row ~3.9 s, 10 rows ~6.3 s, 80 rows ~24.7 s. The floor is
  the mandatory full platen stroke (~3.6 s fixed), not region size.

**Conditional / broken-as-published (robust figures):**
- **K1-service** — **0.39–3.27 N/column depending on base contact**; the rigid tripod case
  (3.27 N) is bounding and leaves ~1.5× margin vs the 4.96 N core. **Size the core against ~3.3 N.**
  Localized 5 N abuse bounded only by a 1.10 mm core re-size (step height 0.5→0.4 mm).
- **K5** — defensible planning basis **$482.95 delivered ($17.05 margin)**; sourced-DRV8833 variant
  **$474.91**; expected-motor case **$501.51 (over)**. E6 is best-case repricing, not sourcing.
  Conditional on a motor ≤ $1.86.
- **K6** — **conditional on a loaded dwell AND a ≥268 pps (~804 rpm) loaded rate**;
  `inspection_s = 0` assumed; floor 18.65 s; the 45.07 s corner is not rate-recoverable.
- **K8** — **open**: at the repo's own 40 mm free length, 1 N → **0.356 mm** and the 0.10 mm-gate
  load is **0.28 N**. The gate is a free-length/guide-capture question.
- **K11** — **">=1e6, order unknown"** (4e5–1e9 across defensible FDM constants).

**Still open — each needs exactly one physical quantity (unavailable under DND-27):**

| id | Residual | The one measurement / action that closes it |
|---|---|---|
| **K7** | matched motor + best-case-pricing basis | a matched 8 mm 18° bipolar PM stepper at **≤ $1.86 delivered** — **refuted on sourced evidence ([DND-49](/DND/issues/DND-49))**: cheapest *matched* part is $8.20–$11.20 (→ $1,088–$1,367 delivered); the reduced-head lever fails the 30 s budget **and the order-tier cost** ([DND-52](/DND/issues/DND-52)). Unretired only by purchasing+sampling the untraced multipack (forbidden under [DND-27](/DND/issues/DND-27)) **or by adopting the S5-R shared-register pivot**, whose own residual is the register dropout/re-engage |
| **K5-basis** | bundled-line + spares pricing | a sourcing quote for the four E6 lines and a spares policy |
| **K1-service** | base contact model | the real miniature base contact (conforming vs tripod), or a core sized for 3.3 N |
| **K1-abuse** | localized 5 N point load | printed **core crush/shear** at the toe |
| **K8-free** | free length at extension | guide-capture length / tier geometry (12 vs 40 mm) |
| **K8-shear** | printed guide-wall shear | printed **guide-wall shear** strength at the 0.10 mm gate |
| **K6-rate** | loaded torque-speed | a pull-out / torque-speed curve for the 8 mm 18° PM stepper at ≥268 pps |
| **K6-dwell** | realised loaded dwell | one loaded engage/settle dwell (25/15 ms assumed) |
| K2 | printed PLA–PLA contact **μ** + as-printed **scallop depth** (needs μ ≤ 0.32 or depth ≥ 0.31 mm) |
| K9 | as-printed **rotor radius/core offset** under the ±0.05 mm tolerance |
| K4 | neighbour **stiction release force + wear drift** under load |
| K11-span | printed-leaf **creep/fatigue** (bound 4e5–1e9) |
| R1 | counted **per-cell error rate** q (≤ 1.57×10⁻⁶ for 99 % maps) |
| R2 | one **measured representative miniature** height vs the 40 mm travel |

**Why this is not a FAILURE and not a SUCCESS under the board's two-trigger policy:** the
machine is not proven un-buildable — no killer is quantitatively decisive, and every residual is
reduced to a single named physical quantity. It is also **not yet a print-ready claim**: K7, the
K5 pricing basis, the K1 base-contact model, K8 free-length/guide-capture and the
print-realisation quantities remain unretired, and DND-27 forbids retiring them by measurement.
The honest terminal state is **"one sourced purchase sample (K7) plus a small set of printed-coupon
measurements away from print-ready"** — a gap named precisely by this register, not a dead end.

The mission-level disposition is recorded in the company `plan` document.
