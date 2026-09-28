# 08 — Current design: S5 — programmed stepped rotary stops + common lift

**Status:** PROMOTED as the single buildable winner by
[ADR-002](../07-evidence-and-decisions/convergence-decision-2026-09-b.md)
([DND-35](/DND/issues/DND-35)). This directory is the engineering source of truth for the
machine — **but it is NOT print-ready as stated.** The Falsifier's winner-specific review
([DND-36](/DND/issues/DND-36)) found three of six "closed" killers contestable or
measurement-only and the cost stack-up inconsistent; ADR-002 §1.2/§3 and §5–§7 below carry
the corrected labels and range. A printable-board test is justified once K1, K5 and K7 close.

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
| Timing under 30 s | **conditional** — best corner 26.251 s; 400 pps sweep passes 17/108 | S3 25.20 s (budget only) |
| Purchased BOM sourced share | **82 %** | S4 37 %, S1 30 % |
| Per-cell bought parts | **0** (passive printed rotors) | all survivors: 0 intended |
| Expected-delivered cost | **conditional** — sourced pair $501.12 (at/over ceiling); reduced $483.37 | S4 $548.91 |
| Decisive failure | none proven; but K1/K4/K5/K6 contestable and K7–K11 open | S1 force, S2 surprise maps, S3 printability+cost, S4 clutch+backlash |

**Two bets, not one** (Falsifier audit, [DND-36](/DND/issues/DND-36)): S1–S4 are *Bet A*
(written passive memory); S5 is *Bet B* (absolute geometric stops — a homed rotor + gravity-
following toe, no written bit). A Bet-A failure does not imply a Bet-B failure. S1/S2/S4 cost
is **conditional on the print gate**, not a kill (their BOMs are fallback-inflated).

**Promotion review correction** (Falsifier, [DND-36](/DND/issues/DND-36)): *"S5 promotion
survives as a direction but fails as stated."* The corrected honest status: S5 remains the
single best-evidenced winner, but K1/K4/K6 must not be presented as closed, K5 must be stated
on the additive basis (sourced pair at/over $500), and K7–K11 must be carried.

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
| Four lift screws + nuts (T8, 8 mm lead) | 1 | AliExpress | $20.00 | sourced |
| Belts/pulleys/idlers | 1 | AliExpress | $20.00 | allowance |
| Power supply + protection (24 V) | 1 | AliExpress SMPS | $35.00 | sourced |
| Axis reference sensors | 4 | AliExpress | $1.00 | allowance |
| Wire/connectors/loom | 1 | AliExpress JST/Dupont | $22.00 | sourced |
| Head shafts + friction pads | 1 | AliExpress brass/felt | $20.00 | sourced |
| Fasteners | 1 | AliExpress M2/M3 | $12.00 | sourced |
| Spares / misc | 1 | — | $15.00 | allowance |

**Totals (corrected, additive delivered ×1.16 — the repository's own basis):**

| Scenario | Purchased parts | Delivered | Verdict |
|---|---:|---:|---|
| Sourced BOM expected scenario (CSV) | $510.40 | **$592.06** | over |
| As-listed sourced pair (motor $1.05, driver $0.80) | $432.00 | **$501.12** | **at/over ceiling (+$1.12)** |
| − real net register saving $10.30 — RP2040 $5 | $413.00 | **$483.37** | clears (~$16.63) |

Reproduced and asserted by `06-experiments/test12_winner_convergence/checks.py`. The earlier
published figures ($503.71 / $481.56, "−$18.44 margin") used a **multiplicative** uplift
(`1.10 × 1.06`) inconsistent with the repo's additive model and **double-counted** the register
saving (the 74HC595s are still bought); both are withdrawn (Falsifier promotion review,
[DND-36](/DND/issues/DND-36)). Reaching the <$400 ideal band is **not** demonstrated.

**The one cost risk (K7):** the only *traceable matched* 8 mm 18° bipolar PM stepper found
(MOONS 8PM020S1) lists at **$40/ea**, which alone would put the machine at ~$3,200. The
sub-$1.05 price is an untraced marketplace multipack and must be sample-verified by the
purchaser before a build. This is stated, not hidden (see §7).

## 6. Fabrication, assembly and print readiness

**Process baseline:** Bambu X1C, PLA, 0.4 mm nozzle, 0.20 mm layers; optional 0.2 mm nozzle
for the thin upper guides.

**Modularity:** the 406.4 mm field is split into printable cartridges (e.g. 4 × 8 modules
of 20×10 cells ≈ 101.6 × 50.8 mm) that bolt to a spliced frame; the frame needs support
every ≤203 mm to hold the 0.25 mm flatness budget (0.0499 mm sag at 203.2 mm support vs
0.799 mm at full 406.4 mm span).

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
| K1 | Cam buckling under handling load | calculation | **open/contestable** — 4.96 N critical < 5 N abuse screen (fails by 0.8 %); 1 N service load is unsourced. Closes only on a sourced ≤4.5 N tabletop-load bound |
| K2 | Printed detent holds/repeats after a slipped step | **conditional (analytic)** | open — bounded by [DND-38](/DND/issues/DND-38): nominal leaf corrects an 18° slip only for μ ≤ 0.323; fails at the sourced PLA–PLA midpoint μ = 0.35 (torque/friction 0.92). Closing levers: μ ≤ 0.32 or scallop depth ≥ 0.31 mm. `test12_winner_convergence/DETENT_CONTACT.md` |
| K3 | Gravity return vs guide friction | calculation | **closed** — 4.06× weight/drag margin (solid column) |
| K4 | Regional update disturbs neighbour | calculation | **partially-closed** — structural bound 0.017 mm vs 0.10 mm gate; stiction release + wear drift are measurement-class; cited rig returns `INCONCLUSIVE` |
| K5 | Cost > $500 delivered | calculation | **conditional** — sourced pair $501.12 (at/over ceiling); reduced $483.37 |
| K6 | Time > 30 s | calculation | **conditional** — best corner 26.251 s; at 400 pps 17/108 sweep cases pass, worst 45.07 s |
| K7 | Motor-cost cliff (80 motors + 80 drivers) | sourced calculation | **open** — only traceable matched stepper is $40/ea → $3,200 (8× ceiling) |
| K8 | Lateral holding of a knocked miniature | calculation | **open** — hard stop holds downward; lateral only via detent (~0.0014 mN·m) + bushing |
| K9 | Angular margin vs print tolerance | calculation | **open** — 12.50° nominal → 6.50° after 6° seating error; ±0.05 mm tolerance unpropagated |
| K10 | Regional-update time unbounded end to end | calculation | **open** — full 41 mm platen stroke + head home/reference per activation |
| K11 | Printed detent/ratchet cycle life | qualitative | **open** — single-cycle static model; creep/fatigue unmodelled |
| R1 | Whole-map reliability | assumption | open — q ≤ 1.57×10⁻⁶ needed for 99 %; no per-cell feedback; unclosable under DND-27 |
| R2 | 40 mm travel vs real miniature | assumption | open — no miniature measured; requirement may change |
| R3 | Realised step rate ≥ 400 pps loaded | assumption | open |
| R4 | Matched motor supply at < $1.05 | assumption | open — only traceable matched part is $40/ea |

**Print-readiness gate:** the machine is **not** print-ready as stated. A printable-board test
is justified once **K1, K5 and K7** close (all three are analytically/sourcingly attackable
under DND-27).

## 8. Next actions

1. **Analytic detent contact sweep** — **done** ([DND-38](/DND/issues/DND-38),
   `test12_winner_convergence/DETENT_CONTACT.md`): K2 bounded, conditional. Next physical
   step is a printed μ + scallop coupon, which DND-27 forbids.
2. **CostManufacturing** ratifies the BOM and printability.
3. **Falsifier** adversarially reviews the killer list for a missed failure mode.
4. **Fabricator** confirms the CAD is print-ready against the harness and X1C envelope.
