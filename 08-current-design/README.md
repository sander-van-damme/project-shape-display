# 08 — Current design: S5 — programmed stepped rotary stops + common lift

**Status:** PROMOTED as the single buildable winner by
[ADR-002](../07-evidence-and-decisions/convergence-decision-2026-09-b.md)
([DND-35](/DND/issues/DND-35)). This directory is now the engineering source of truth for
the machine.

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
|---|---:|---:|---|
| As-listed (sourced pair) | $432.00 | **$501.12** | **over the ceiling by $1.12** |
| − shift registers onto PCB (net $10.30; chips still bought at $0.0925) | $421.70 | **$489.17** | clears |
| − RP2040 controller | $416.70 | **$483.37** | clears with $16.63 margin |

Reproduced and asserted by `06-experiments/test12_winner_convergence/checks.py`. **Cost
correction ([DND-41](/DND/issues/DND-41)):** the prior table used a multiplicative
`1.10 × 1.06 = 1.166` uplift and a $434.20 subtotal that does not reproduce; the repo's own
`delivered_3scenario` grid prints the sourced-pair cell as **$501.12** ($432.00 × 1.16). The
honest headline is a **range at/just over the ceiling**, clearing only on the reduced path by
a small margin. The **best-case** delivered was $389.55 (all-cheapest untraced prices) — not
used in this definition.

**The one cost risk (K7):** the only *traceable matched* 8 mm 18° bipolar PM stepper found
(MOONS 8PM020S1) lists at **$40/ea**, which alone would put the machine at ~$3,200 (8× the
ceiling). The sub-$1.05 price is an untraced marketplace multipack and must be sample-verified
by the purchaser before a build. This is stated, not hidden (see §7).

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
| K1 | Cam buckling under handling load | calculation | **open** — 4.96 N critical **< 5 N** Test08 measurement-protocol screen; the 1 N service load is **unsourced**. Close with a sourced ≤4.5 N tabletop-load bound, else re-size the core. ([DND-41](/DND/issues/DND-41)) |
| K2 | Printed detent holds/repeats after a slipped step | **conditional (analytic)** | open — bounded by [DND-38](/DND/issues/DND-38): nominal leaf corrects an 18° slip only for μ ≤ 0.323; fails at the sourced PLA–PLA midpoint μ = 0.35 (torque/friction 0.92). Closing levers: μ ≤ 0.32 or scallop depth ≥ 0.31 mm. `test12_winner_convergence/DETENT_CONTACT.md` |
| K3 | Gravity return vs guide friction | calculation | **closed** — 4.06× weight/drag margin (solid column) |
| K4 | Regional update disturbs neighbour | calculation | **partially-closed** — 0.017 mm is a rail-bending *structural* sub-bound vs a 0.10 mm gate; the J2 engine returns **INCONCLUSIVE** — stiction release and wear drift are measurement-only. ([DND-41](/DND/issues/DND-41)) |
| K5 | Cost > $500 delivered | calculation | **conditional (range)** — $501.12 sourced (over ceiling) → **$483.37** reduced; real but small margin. ([DND-41](/DND/issues/DND-41)) |
| K6 | Time > 30 s | calculation | **conditional** — 26.251 s best corner; only **17/108** sweep cases pass at 400 pps, worst **45.07 s**; needs a measured ≥400 pps loaded rate. ([DND-41](/DND/issues/DND-41)) |
| K7 | Purchased-actuator cost cliff (80 motors) | assumption | **open** — only traceable matched 8 mm PM stepper is $40/ea (→ $3,200); sub-$1.05 part untraced |
| K8 | Lateral holding (knocked miniature) | calculation | **open** — hard stop resists downward load only; detent restoring torque ≈ 0.00139 mN·m; no analytic pass |
| K9 | Angular margin vs print tolerance | calculation | **open** — 5 levels: 12.50° nominal → 6.50° after a 6° seating error; ±0.05 mm print tolerance not propagated |
| K10 | Regional-update time untested end to end | uncertainty | **open** — homing + full 41 mm platen stroke not bounded |
| K11 | Cycle life of printed detent/ratchet | uncertainty | **open** — single-cycle static model; creep/fatigue unmodelled |
| K12 | Coarse-slope / multi-level usability | assumption | **open** — 10 mm steps may be too coarse; product decision |
| R1 | Whole-map reliability | assumption | open — q ≤ 1.57×10⁻⁶ needed for 99 %; no per-cell feedback |
| R2 | 40 mm travel vs real miniature | assumption | open — no miniature measured; requirement may change |
| R3 | Realised step rate ≥ 400 pps loaded | assumption | open |
| R4 | Matched motor supply at < $1.05 | assumption | open — only traceable matched part is $40/ea |
| R5 | Frame/platen splice stiffness ratio (k = 0.25 assumed) | assumption | open — sets the ≤150 mm support spacing; higher k relaxes to 203.2 mm. Step 6 (DND-43) |
| R6 | As-printed rail modulus (700 vs 2500 MPa spans the flatness pass/fail line) | assumption | open — Step 6 (DND-43) |
| R7 | Sourced lift-motor torque at speed (0.30 N·m assumed) | assumption | open — Step 6 drive sizing depends on it until sample-verified |
| R8 | Lift lead must be ≤ 2 mm (8 mm fails 0.51×); power cut back-drives the screw (not self-locking) | calculation | open — **new required item**: a friction brake or platen detent, not yet in the BOM or the 26.25 s timing budget. Step 6 (DND-43) |

**Readiness summary (DND-41):** the S5 direction survives, but the winner is **not** "closed"
on cost, time or isolation as previously stated. It is **on/just over the $500 ceiling**;
time is **conditional** on an unmeasured step rate; isolation is a **structural sub-bound only**;
and K1 plus K7–K12 remain **open**. This is an honest readiness statement, not a print-ready
claim.

## 8. Next actions

1. **Analytic detent contact sweep** — **done** ([DND-38](/DND/issues/DND-38),
   `test12_winner_convergence/DETENT_CONTACT.md`): K2 bounded, conditional. Next physical
   step is a printed μ + scallop coupon, which DND-27 forbids.
2. **Step-6 load/structure/power** — **done** ([DND-43](/DND/issues/DND-43),
   `test13_step6_load_structure_power/`): corrected support spacing (≤ ~150 mm or stiffer
   rail), lift lead (≤ 2 mm or larger motor), and a now-required power-cut brake/detent.
   **Open follow-up for CostMfg/Fabricator:** fold the brake/detent and the re-sized lead
   into the BOM and the timing budget, and update the CAD support layout.
3. **CostManufacturing** ratifies the BOM and printability.
4. **Falsifier** adversarially reviews the killer list for a missed failure mode.
5. **Fabricator** confirms the CAD is print-ready against the harness and X1C envelope.
