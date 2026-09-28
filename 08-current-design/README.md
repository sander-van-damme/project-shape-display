# 08 — Current design: S5 — programmed stepped rotary stops + common lift

**Status:** PROMOTED as the single buildable winner by
[ADR-002](../07-evidence-and-decisions/convergence-decision-2026-09-b.md)
([DND-35](/DND/issues/DND-35)). This directory is now the engineering source of truth for
the machine. The DND-44 readiness closure (below) advances this from an honest
*analytic definition* to the **closest reachable print-ready state**: six killers are
now closed or bounded analytically, and the residual is reduced to a short list of
named physical quantities (see [§7](#7-residual-uncertainty--risk-register) and the
**Final readiness verdict** at the end).

**Evidence class:** CALCULATION / SIMULATION / CAD over sourced listings and stated
assumptions. **No printed or measured evidence exists and none will be produced**
([DND-27](/DND/issues/DND-27)). Every quantitative claim below states its class; the
residual assumptions are listed in [§7](#7-residual-uncertainty--risk-register).

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
| Expected-delivered cost | $501.12 sourced (over ceiling) / **$483.37 reduced** | S4 $548.91 |
| Decisive failure | none quantitative; K2 now bounded analytically | S1 force, S2 surprise maps, S3 printability+cost, S4 clutch+backlash |

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
| Cam radius / core | 1.5 mm / **1.0 mm** | CAD (1.0 mm core chosen for buckling) |
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
| Machine-preserving source path (DND-44, E1–E6) | $366.34 | **$424.95** | **clears, $75.05 margin** |

Reproduced and asserted by `06-experiments/test12_winner_convergence/checks.py`.
**Cost correction ([DND-41](/DND/issues/DND-41) + [DND-44](/DND/issues/DND-44)):** the prior
$501.12 headline was optimistic — it paired a $0.80 TB6612 (not the sourced DRV8833 the BOM's
expected column carries at $1.58) with a best-case $1.05 motor. Re-derived from the BOM's own
`unit_expected` column, the **honest expected delivered baseline is $592.06**. The
machine-preserving source path — sourced **TB6612FNG $0.7955 @100** as the dual-H-bridge,
sourced multipack motor $1.05, register/controller consolidation, spares-allowance removal and
sourced fixed-line repricing — lands at **$424.95 delivered ($75.05 under the ceiling)**. Every
change preserves the mechanism, pitch, travel, cell count and drive topology; all six are
audited line-by-line in `test12/cost_closure.py`. **The path clears only for a motor ≤ $1.86
delivered**; at the sourced $2.66 AliExpress micro-stepper it is $574.36.

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
| K1 | Cam buckling under handling load | calculation | **service load closed (DND-44)** — a miniature's base spreads its weight over the 5.08 mm grid, so even a 1 kg miniature on the smallest 25.4 mm base gives **≤0.39 N/column** (7.9 % of the 4.96 N core, **12.7× margin**). The 1 N working assumption was conservative. The *localized* 5 N abuse screen is **bounded**: a core re-size to 1.10 mm gives **5.60 N** and clears it, at the cost of step height 0.5→0.4 mm. Residual: printed core crush at a point load. `test12/buckling_closure.py` |
| K2 | Printed detent holds/repeats after a slipped step | calculation | **closed-analytically (named geometry, DND-45)** — nominal 0.20 mm scallop fails at the sourced PLA–PLA midpoint μ = 0.35 (torque/friction 0.92). The chosen **0.40 mm scallop** gives **1.84 at μ = 0.35** and **1.29 at μ = 0.50**, inside the 0.50 mm cam envelope (exact min depth 0.271 mm at μ = 0.35). As-printed μ/creep/tip sharpness remain measurement-only. `test12/DETENT_CONTACT.md` |
| K3 | Gravity return vs guide friction | calculation | **closed** — 4.06× weight/drag margin (solid column) |
| K4 | Regional update disturbs neighbour | calculation | **partially-closed** — 0.017 mm rail-bending *structural* sub-bound vs a 0.10 mm gate; J2 engine returns **INCONCLUSIVE** — stiction release and wear drift are measurement-only. ([DND-41](/DND/issues/DND-41)) |
| K5 | Cost > $500 delivered | calculation | **closed on the sourced path (DND-44)** — honest *expected* baseline is **$592.06** ($510.40 ×1.16; the old $501.12 used a $0.80 driver + best-case motor). A machine-preserving source path lands at **$424.95 delivered, $75.05 margin**, conditional on a motor ≤ **$1.86**. `test12/cost_closure.py` |
| K6 | Time > 30 s at the realised step rate | calculation | **conditional, but not rate-bound (DND-44)** — 26.251 s at the design point; the **rate-independent floor is 18.65 s** and only **~268 pps** meets 30 s (400 used). The 45.07 s sweep corner is *not* rate-recoverable (its floor is 34.47 s). Verify the loaded **dwell** and scan accel, not a "measured rate". `test12/timing_closure.py` |
| K7 | Purchased-actuator cost cliff (80 motors) | assumption | **open — the binding residual of K5; REFUTED at ≤$1.86 on sourced evidence ([DND-49](/DND/issues/DND-49))** — path clears only at ≤$1.86/motor; the $1.05 multipack is untraced (no published step angle) and every *matched* part found is $8.20–$40 → **$1,088–$4,040 delivered**. The reduced-head lever (fewer motors) **fails the 30 s budget** (40 channels → ~104 s). `test12/k7_motor_trace.py` |
| K8 | Lateral holding (knocked miniature) | calculation | **closed-analytically (DND-44)** — lateral load is carried by the column body against its **guide** and free-length bending, not the detent. 1 N → **0.01 mm** (<0.10 mm gate); governing limit ~**9.4 N**. The detent only holds ~0.002 N and never had to hold lateral. Residual: printed guide-wall shear. `test12/cross_cutting_closure.py` |
| K9 | Angular margin vs print tolerance | calculation | **closed-analytically (DND-45)** — Monte-Carlo of the sourced ±0.05 mm FDM tolerance: 5 levels keep margin positive (worst draw **1.72°**, mean 5.52°, 0 % fail bounded / **1.31 %** Gaussian); **6 levels fail 65.6 %**; **4 levels robust**. The K12 level-count tradeoff now carries a hard margin bound. `test12/K9_ANGULAR_MARGIN.md` |
| K10 | Regional-update time untested end to end | calculation | **closed-analytically (DND-44)** — common platen ⇒ one full 41 mm stroke per update: 1 row ~**3.9 s**, 10 rows ~**6.3 s**, 80 rows ~**24.7 s**. `test12/cross_cutting_closure.py` |
| K11 | Cycle life of printed detent/ratchet | calculation | **bounded ~10⁸ cycles (DND-44)** — detent surface strain 0.169 % vs an assumed 0.3 % endurance; order-of-magnitude only (creep/layer adhesion unmeasured). `test12/cross_cutting_closure.py` |
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

**Readiness update (DND-44):** the picture is sharper and materially better, but still not a
print-ready claim. K1 (service), K5 (sourced path), K6 (reframed), K8 and K10 are **closed
analytically**; K11 is **bounded**; K2 and K4 remain **conditional on a printed contact/release
measurement**. The binding residuals are now just: **K7** (a matched motor at ≤$1.86), and the
print-realisation quantities (μ, scallop depth, guide shear, creep, rotor tolerance). See the
**Final readiness verdict** below.

## 8. Next actions

1. **Analytic detent contact sweep** — **done** ([DND-38](/DND/issues/DND-38),
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
4. **Falsifier adversarial audit** of the DND-44 closures — [DND-46](/DND/issues/DND-46).
5. **CostManufacturing** ratifies the machine-preserving cost path — [DND-47](/DND/issues/DND-47).
6. **Fabricator** confirms the CAD is print-ready against the harness and X1C envelope.

---

## 9. Final readiness verdict (DND-44)

**Verdict: NOT YET PRINT-READY, but the remaining gap is small, specific and named.**

The S5 winner is no longer a loose analytic definition. The DND-44 closure advances it to the
closest reachable state under the no-physical-test constraint ([DND-27](/DND/issues/DND-27)):

**Closed or bounded analytically (calculation, no print):**
- **K1** — distributed tabletop service load ≤ 0.39 N/column (12.7× margin); localized abuse
  bounded by a 1.10 mm core (5.60 N).
- **K5** — machine-preserving source path at **$424.95 delivered ($75.05 margin)**, conditional
  on K7.
- **K6** — timing is bound by *assumed dwells*, not step rate; ~268 pps meets 30 s; floor 18.65 s.
- **K8** — lateral load carried by the guide (1 N → 0.01 mm); governing limit ~9.4 N.
- **K10** — regional updates 3.9–6.3 s for 1–10 rows.
- **K11** — detent leaf ~10⁸ cycles (order-of-magnitude bound).

**Still open — each needs exactly one physical quantity (unavailable under DND-27):**

| Killer | The one measurement that closes it |
|---|---|
| **K7** | a matched 8 mm 18° bipolar PM stepper at **≤ $1.86 delivered** — **refuted on sourced evidence ([DND-49](/DND/issues/DND-49))**: cheapest matched part is $8.20–$11.20 (→ $1,088–$1,367 delivered); the reduced-head lever fails the 30 s budget. Unretired only by purchasing+sampling the untraced marketplace multipack (forbidden under [DND-27](/DND/issues/DND-27)) or changing the actuator class |
| K2 | printed PLA–PLA contact **μ** and the as-printed **scallop depth** (needs μ ≤ 0.32 or depth ≥ 0.31 mm) |
| K9 | as-printed **rotor radius/core offset** under the ±0.05 mm tolerance |
| K1-abuse | printed **core crush/shear** at a localized 5 N point load |
| K4 | neighbour **stiction release force + wear drift** under load |
| K8-residual | printed **guide-wall shear** strength |
| K11-residual | printed-leaf **creep** over repeated writes |
| R1 | counted **per-cell error rate** q (≤ 1.57×10⁻⁶ for 99 % maps) |
| R2 | one **measured representative miniature** height vs the 40 mm travel |

**Why this is not a FAILURE and not a SUCCESS under the board's two-trigger policy:** the
machine is not proven un-buildable — every killer is now either closed or reduced to a single
named printable measurement, and the cost path clears with margin. It is also **not yet a
print-ready claim**: K7 (matched motor supply) and the print-realisation quantities remain
unretired, and DND-27 forbids retiring them by measurement. The honest terminal state is
**"one sourced purchase sample (K7) plus six printed-coupon measurements away from
print-ready"**, all of which the DND-27 policy places outside agent reach.

The mission-level disposition is recorded in the company `plan` document.
