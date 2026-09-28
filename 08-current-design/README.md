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
| Expected-delivered cost | $503.71 sourced / **$481.56 reduced** | S4 $548.91 |
| Decisive failure | none quantitative; K2 qualitative | S1 force, S2 surprise maps, S3 printability+cost, S4 clutch+backlash |

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
| State retention | passive stepped cam + hard stop + detent leaf | CAD + **qualitative (K2)** |
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

**Totals (expected delivered, ×1.16):**

| Scenario | Purchased parts | Delivered | Verdict |
|---|---:|---:|---|
| As-listed (sourced pair) | $434.20 | **$503.71** | on ceiling (+$3.71) |
| − shift registers onto PCB | $420.20 | **$487.46** | clears |
| − RP2040 controller | $415.20 | **$481.56** | clears with $18.44 margin |

Reproduced and asserted by `06-experiments/test12_winner_convergence/checks.py`. The
**best-case** delivered was $389.55 (all-cheapest untraced prices) — that path is not used
in this definition.

**The one cost risk:** the only *traceable matched* 8 mm 18° bipolar PM stepper found
(MOONS 8PM020S1) lists at **$40/ea**, which alone would put the machine at ~$4,000. The
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
| K1 | Cam buckling under handling load | calculation | **closed** — 4.96 N critical vs 1 N service (≈5×); 5 N is a handling screen, not a gate |
| K2 | Printed detent holds/repeats after a slipped step | **qualitative** | open — analysis cannot retire under DND-27; cheapest falsification = analytic detent contact sweep |
| K3 | Gravity return vs guide friction | calculation | **closed** — 4.06× weight/drag margin (solid column) |
| K4 | Regional update disturbs neighbour | calculation | **closed** — 0.017 mm vs 0.10 mm gate |
| K5 | Cost > $500 delivered | calculation | **closed** — $481.56 reduced |
| K6 | Time > 30 s | calculation | **closed** — 26.251 s at 400 pps |
| R1 | Whole-map reliability | assumption | open — q ≤ 1.57×10⁻⁶ needed for 99 %; no per-cell feedback |
| R2 | 40 mm travel vs real miniature | assumption | open — no miniature measured; requirement may change |
| R3 | Realised step rate ≥ 400 pps loaded | assumption | open |
| R4 | Matched motor supply at < $1.05 | assumption | open — only traceable matched part is $40/ea |

## 8. Next actions

1. **Analytic detent contact sweep** (closes or names K2) — cheapest falsification.
2. **CostManufacturing** ratifies the BOM and printability.
3. **Falsifier** adversarially reviews the killer list for a missed failure mode.
4. **Fabricator** confirms the CAD is print-ready against the harness and X1C envelope.
