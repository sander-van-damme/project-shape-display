# 08 — Current design: S5-R — shared-drive programmable rotary register (R = 4)

**Status:** **PROMOTED — this is the machine.** S5-R is the engineering source of truth
and the slicer-ready build this repository hands over. It supersedes the incumbent S5
(programmed stepped rotary stops + a full-width **80-motor** programming head), which the
outcome of the actuator-class screen ([DND-52](/DND/issues/DND-52)) and the sourced
**K7** motor-cliff finding ([DND-49](/DND/issues/DND-49)) left not analytically retirable
as a cost path. S5-R replaces the 80 bought steppers with a **shared-drive programmable
rotary register**: a 4-row-deep bank (**R = 4**) driven by **2 bank motors** that writes
the per-cell state with **40 writer solenoids**, and a printed **keeper latch** that drops
the selected pawls into the shared rack. See the
[ADR](../07-evidence-and-decisions/dnd54-s5r-register-latch.md) and its amendments
([DND-55](../07-evidence-and-decisions/dnd55-s5r-bank-assembly.md),
[DND-58](../07-evidence-and-decisions/dnd58-s5r-register-reconcile.md),
[DND-59](../07-evidence-and-decisions/dnd59-s5r-residual-retirement.md)); the terminal
verdict is [DND-57](../07-evidence-and-decisions/dnd57-terminal-s5r-verdict.md).

**Headline (promoted model `06-experiments/test12_winner_convergence/s5r_register.py`):**

| Quantity | S5-R value | Source |
|---|---:|---|
| Active area / pitch / cells | 406.4 × 406.4 mm / 5.08 mm / 80 × 80 = 6,400 | model constants |
| Actuators | **2 bank motors + 40 writer solenoids** (42 total) | `BANK_MOTORS`, `WRITERS` |
| Bank depth | **R = 4 rows** (20 groups, no pitch penalty) | `ROWS_IN_BANK` |
| Full-map reconfiguration | **24.615 s** (< 30 s; `margin_to_30s_s` 5.385) | `timing.full_map_s5r_s` |
| Delivered cost | **$404.60** (working; margin $95.40; band $387.18–$421.51) | `bom.delivered_usd` |
| Gates | **G1–G7 all pass** | `decision.all_mechanical_gates_pass` |

**The one thing that changed for the board:** the machine is now a **complete printable
package**, not just a definition — [`fabrication/`](fabrication/) carries 14 real-OpenSCAD
parts (**25,661 pieces**), 14 watertight bed-fitting STLs, print + assembly manifests, a
full-set sourced-FDM-limit **PASS**, and a CI coherence gate pinning it to the promoted
model ([DND-60](/DND/issues/DND-60), [DND-61](/DND/issues/DND-61)). **Start at
[§6a](#6a-how-to-print-and-build-the-s5-r-machine-the-fabrication-package-dnd-60dnd-61) →
[`fabrication/README.md`](fabrication/README.md)** for "what to print".

**Evidence class:** CAD (real OpenSCAD) / CALCULATION / SIMULATION over sourced listings
and stated assumptions. **No printed or measured evidence exists and none will be
produced** ([DND-27](/DND/issues/DND-27)). Every quantitative claim below states its
class. What remains is a **short, named, measurement-only residue** (as-printed μ, keeper
creep/fatigue, per-set reliability q, loaded motor curve) listed in the live
[§7 S5-R residual register](#7-s5-r-residual-register-live).

**S5-R promotion ([DND-54](/DND/issues/DND-54)):** the analytic + CAD dropout-latch model
closed the S5-R mechanism the way [DND-27](/DND/issues/DND-27) allows and promoted it to a
machine-definition candidate — as a **4-row-deep shared bank** (the DND-52 option-1 was
single-row and, counted honestly per row, could not meet 30 s). At R = 4 with 40 writer
solenoids and 2 bank motors: **$404.60 delivered working, 24.615 s**, all seven analytic
gates passing (cell fit, zero neighbour cross-talk, writer force, bank force, latch
inherits K1, time, cost). The delivered figure was independently ratified
([DND-56](/DND/issues/DND-56)) and carries the R = 4 block's own marginal channels
($3.09) **and its sourced steel drive rod** (`delivered_usd` $404.60 vs the rod-unpriced
`delivered_no_rod_usd` $401.12 and the channels-unpriced `delivered_claim_usd` $397.53).
This is **CAD + CALCULATION only**.

**S5-R bank ([DND-55](/DND/issues/DND-55)):** the R = 4 **multi-row bank assembly** is
CAD-modelled and closed analytically. The reset-comber and writer-carriage **envelopes
fit** (five empty OpenSCAD interference queries; carriage/column clearance 0.40 mm worst
case) and **R = 4 adds no pitch penalty**. Two DND-54 geometry claims did not survive and
were fixed: the printed **3 × 2 placeholder bar was ~28× over** the bar-torsion gate (peak
tip skew 4.96 mm vs gate/2 = 0.175 mm) → a **sourced steel drive rod d = 5–6 mm** (or an
Ø8 printed round bar); and the DND-54 **rack fused** (0.15 mm inter-tooth gap < one
0.44 mm line) → **rack re-dimensioned to pitch 1.00 / tooth 0.50 mm**. See
[§8 item 10](#8-next-actions).

**S5-R register reconciliation ([DND-58](/DND/issues/DND-58)):** the DND-55 corrections
are folded into the register definition itself. `s5r_register.scad` / `s5r_register.py`
carry the corrected rack (**pitch 1.00 / tooth 0.50 mm**, `RACK_STROKE_MM = 1.00`) and a
**sourced steel drive rod d = 6 mm** (`BAR_D_MM`), rendered as a round rod in CAD. The
full-map time is **unchanged at 24.615 s** because the bank pass is *angular* (72°/level;
the linear per-stroke advance does not enter the timing). One steel rod adds **$3.00 parts
→ $3.48 delivered**, so the honest working BOM is **$404.60 delivered** (`margin $95.40`).
R-DND55-4 is **closed**.

**S5-R residual retirement ([DND-59](/DND/issues/DND-59)):** the remaining
**agent-reachable** S5-R residuals are now retired or bounded on the DND-27
evidence classes. **R-DND54-KEEPER** is **closed**: the keeper leaf is re-profiled
**0.45 → 0.90 mm (1 → 2 extrusion lines, printability RISK → PASS)** and its
*hold* is moved from a tolerance-fragile bending-spring offset to a **hard printed
shoulder in compression** (144–324× the pawl push-out). The re-profile moves the
keeper into the **row (Y) axis** so it does not consume the pitch band (X gap
0.98 mm, Y gap 0.28 mm worst case). **R-DND54-6** is **closed agent-side**: the
writer force is re-derived bottom-up (**0.2425 N**) and the sourced 5 V push
solenoid class (**1.20 N**, 4.95×) clears it. **R-DND54-5** is **bounded
agent-side**: a 99 % full map needs per-keeper **q ≤ 1.57e-6**, and a per-group
verify+retry relaxes it **2–10×** (writer redundancy **~798×**); the as-printed q
is the measurement-only residue. **R-DND54-3** is **bounded agent-side**:
break-evens re-derived (min crank **468 deg/s**, 1.54×; max settle **0.084 s**,
1.67×) and the sourced NEMA17 class clears at 2.15× torque. **R-DND55-1** is
**closed for the steel rod**: skew 0.0052 mm even at an extreme eccentricity
e = 6 mm (33× inside the gate; break-even e ≈ 201 mm). See
[`dnd59-s5r-residual-retirement.md`](../07-evidence-and-decisions/dnd59-s5r-residual-retirement.md)
and the live [§7 S5-R residual register](#7-s5-r-residual-register-live).
The only residue left is **measurement-only**.

**S5-R fabrication package ([DND-60](/DND/issues/DND-60), completed by
[DND-61](/DND/issues/DND-61)):** the machine is now a **slicer-ready printable
package**, not just a definition. `08-current-design/fabrication/` carries a
**complete real-OpenSCAD printed-part set** (14 distinct parts, 25,661 pieces),
**14 watertight, bed-fitting STLs**, a **print manifest** and an **assembly
manifest**, a **full-set printability PASS** against the sourced FDM limits, and
a **CI coherence gate** that pins the package to the promoted model
(`s5r_register.py`). [DND-61](/DND/issues/DND-61) removed the last gap: the two
structural tiles used to ship as **reduced witness blocks**; both now render at
their **true full 27 × 27 / 137.16 × 137.16 mm** size as single manifold solids
(the gate's new **C7** fails a reduced witness that lacks a real envelope or a
documented sub-tile route). See §6a. The only remaining residue is
**measurement-only** (the board's own build/measure) — no agent-reachable
fabrication work remains.

---

## 1. Machine in one paragraph

An 80 × 80 array of **square printed columns** at 5.08 mm pitch (406.4 × 406.4 mm) is
divided into independently printable **cartridges/modules** because the 406 mm span
exceeds the 256 mm X1C bed. Each column carries **five passive stepped rotary cams** (a
5-level height memory) and rides on a **common lifting platen**. State is written by a
**shared-drive programmable rotary register**, not a bought motor per column: a
**4-row-deep bank (R = 4)** of 320 pawls is traversed by **40 writer solenoids** and
**2 bank motors** — each writer releases a printed **keeper latch** so the selected pawls
drop and engage a **shared rack** driven by the bank motors, rotating each rotor to its
selected hard-stop level. A single platen stroke of 41 mm (40 mm travel + 1 mm unload
clearance) raises all columns so the newly-selected rotor steps seat as the platen lowers.
The rotor's hard stop, not any powered element, **holds terrain load**, so the machine
draws no holding power per cell. This removes the **80-bought-motor cliff** of the
incumbent S5 at **$404.60 delivered, 24.615 s** full-map (all seven analytic gates pass).

## 2. Why this machine (and not the others)

| Criterion | **S5-R result** | Nearest rival |
|---|---|---|
| Real CAD of mechanism | **yes** — register + R=4 bank + unit cell + full printable part set, interference-checked | S1/S2/S4: none |
| Timing under 30 s | **24.615 s** (promoted model) | S3 25.20 s (budget only) |
| Per-cell bought parts | **0** (passive printed rotors) | all survivors: 0 intended |
| Bought actuators | **42** (2 bank motors + 40 writers), no per-column motor | S5: 80 motors; all rivals: higher or unproven |
| Expected-delivered cost | **$404.60 delivered** (margin $95.40; band $387.18–$421.51) | S5 $482.95 robust / $501.51 expected-motor; S4 $548.91 |
| Decisive failure | none quantitative; measurement-only residue only | S1 force, S2 surprise maps, S3 printability+cost, S4 clutch+backlash |

### 2a. Superseded incumbent S5 (kept for the record)

S5 — programmed stepped rotary stops with a **full-width 80-channel programming head of 80
bought PM steppers** — was the earlier promoted winner ([ADR-002](../07-evidence-and-decisions/convergence-decision-2026-09-b.md),
[DND-35](/DND/issues/DND-35)). It is **no longer the machine**: its cost path is **not
closed** because the only traceable matched 8 mm 18° PM stepper lists at **$40/ea**
(→ $1,088–$4,040 delivered), so the sub-$1.86 clearing path needs an untraced multipack —
**K7 refuted on sourced evidence** ([DND-49](/DND/issues/DND-49)) — and no actuator-class
lever retires it ([DND-52](/DND/issues/DND-52)). Its own robust figures were **$482.95
delivered / 26.251 s**, with K1-service, K5, K6, K8 and K11 not cleanly closed (the robust
register is preserved in the [legacy appendix](#appendix-a-legacy-incumbent-s5-register-and-verdict)).
S5-R is the promoted machine that replaces it.

ADR for the promotion and its rival screen: [ADR-002](../07-evidence-and-decisions/convergence-decision-2026-09-b.md),
[DND-52 pivot ADR](../07-evidence-and-decisions/dnd52-head-actuator-pivot.md),
[DND-54 register ADR](../07-evidence-and-decisions/dnd54-s5r-register-latch.md),
[Test12 stack-up](../06-experiments/test12_winner_convergence/),
[Test08 CAD + machine](../06-experiments/test08_architecture_search/),
[Test09 validation](../06-experiments/test09_test08_validation/).

## 3. Functional allocation (all ten jobs named)

| Job | Mechanism | Evidence |
|---|---|---|
| Map representation | per-rotor angle (5 levels × 80×80), firmware map | CAD |
| Selection | shared register: 40 writer solenoids + printed keeper latch over the R=4 bank | CAD + calculation |
| Power delivery | shared platen + 2 bank motors driving one shared rack | calculation |
| Vertical positioning | common platen lift, 41 mm stroke | CAD + calculation |
| State retention | passive stepped cam + hard stop + detent leaf | CAD + analytic bound **K2 (DND-38)** |
| Tabletop load support | rotor hard stop / follower toe (latch dormant in service) | calculation |
| Lowering / reset | platen lower, gravity return, reset-comber | calculation |
| Regional isolation | per-column rotor memory (only the touched group's rotors move) | analytic bound |
| Programming | bank-serial register writes; regional = rewrite only affected rows | calculation |
| Detection / recovery | axis reference sensors (no per-cell feedback) | assumption |

## 4. Key dimensions

| Parameter | Value | Basis |
|---|---:|---|
| Grid | 80 × 80 = 6,400 cells | design criteria |
| Pitch | 5.08 mm | design criteria (1 in / 5) |
| Column body | 4.68 mm square, 80.2 mm long | CAD (leaves 0.40 mm top gap) |
| Travel | 40 mm (provisional envelope) | design criteria — **not** miniature-verified |
| Levels / increment | 5 / 10.0 mm | calculation |
| Rotor / core | Ø3.0 mm rotor, 1.5 mm cam / **1.0 mm** core | CAD (register unit cell) |
| Platen stroke | 41 mm (40 + 1 unload) | calculation |
| Bank depth | R = 4 rows (20 groups of 320 cells), no pitch penalty | `ROWS_IN_BANK` |
| Actuators | **2 bank motors + 40 writer solenoids** (42 total) | `BANK_MOTORS`, `WRITERS` |
| Register clearances | X gap 0.98 mm, Y gap 0.28 mm worst case (pawl 0.90 mm; keeper 0.90 mm in Y) | `cell_fit` |
| Drive rod | sourced steel Ø6 mm (`BAR_D_MM`) | `s5r_register.py` (DND-58) |
| Rack | pitch 1.00 / tooth 0.50 mm (`RACK_STROKE_MM = 1.00`) | `s5r_register.py` (DND-58) |
| Active area | 406.4 × 406.4 mm, modular for X1C | design criteria |

## 5. Bill of materials (purchased, S5-R)

Base = the promoted register model's `bom()` in
`06-experiments/test12_winner_convergence/s5r_register.py`; ratified by
[DND-56](/DND/issues/DND-56) and amended by [DND-58](/DND/issues/DND-58) (steel rod).

| Line | Qty | Sourced part | Unit | Notes |
|---|---:|---|---:|---|
| Bank motors (NEMA17 class) | 2 | sourced class | 2.15× force margin | shared rack drive |
| Writer solenoids (5 V push) | 40 | sourced class | 1.20 N vs 0.2425 N (4.95×) | keeper release |
| Bank H-bridge IC | 2 | @ $0.7955 | $0.80 | bank drive blocks |
| Writer darlington chips | 5 | @ $0.30 | $0.30 | 40 writers / 8 per chip |
| Steel drive rod | 1 | Ø6 mm sourced | $3.00 | replaces printed bar (DND-55/58) |
| Fixed no-channel parts | 1 lot | controller, PCBs, passives, lift/drive, frame, supply, loom, fasteners, spares | $218.70 | `fixed_no_channel_parts_usd` |

**Totals (promoted model `s5r_register.bom()`):**

| Quantity | Value |
|---|---:|
| Purchased parts (`parts_usd`) | $348.79 |
| **Delivered working (`delivered_usd`)** | **$404.60** |
| Margin to $500 (`margin_usd`) | $95.40 |
| Sourced band | $387.18–$421.51 |
| Rod-unpriced (`delivered_no_rod_usd`) | $401.12 |
| Channels-unpriced claim (`delivered_claim_usd`) | $397.53 |

The delivered total prices the R = 4 block's **own** marginal channels ($3.09) and its
**sourced steel drive rod** ($3.00 parts → $3.48 delivered). The model's own `bom()`
returns all of the above; `s5r_bom_ratify_checks.py` asserts the ratified numbers.

### 5a. Superseded incumbent S5 BOM (kept for the record)

The following was the incumbent-S5 cost path (80 bought PM steppers + 80 drivers). It is
**not** the machine; it is preserved because its K7 finding (the motor cliff) is exactly
what motivated S5-R.

Base = the S5 delivered BOM (`06-experiments/test11_cost_printability_reliability/delivered_3scenario/bom_S5_delivered.csv`).
Fixed expected subtotal **$284.00**; motor + driver channel was the cost driver.

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

**Superseded S5 totals (expected delivered, additive ×1.16):**

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

Restoring both gives the **defensible S5 planning basis: $482.95 delivered, $17.05 under the
ceiling**. The still-legitimate driver swap (TB6612FNG, a dual H-bridge for dual H-bridge at the
@100 LCSC price of $0.7955) is best-in-price: at the repo's *other* sourced driver (DRV8833PWPR
C50506, $1.3338) the total is $474.91. Every change preserves the mechanism, pitch, travel, cell
count and drive topology; all the variants are audited line-by-line in `test12/cost_closure.py`
and attacked in `test12/falsifier_checks.py`. **The path clears only for a motor ≤ $1.86
delivered**; at the expected $1.25 motor, with E5+E6 restored, it is **over the ceiling at
$501.51**.

**The one cost risk that killed S5 (K7):** the only *traceable matched* 8 mm 18° bipolar PM stepper found
(MOONS 8PM020S1) lists at **$40/ea**; the cheapest *matched, orderable* part is a Chinese OEM
(CCHT) at **$11.20 @100** (→ **$1,366.87 delivered**) and **$8.20 @3,001+** (→ $1,088.47). The
sub-$1.86 price is an untraced marketplace multipack with **no published step angle** and must be
sample-verified by the purchaser before a build; [DND-49](/DND/issues/DND-49) therefore records K7
**refuted on sourced evidence** — no matched, traced part exists at ≤$1.86, and the reduced-head
design lever breaks the 30 s budget. **S5-R is the pivot that removes this cliff**; the S5-line
register is preserved in [Appendix A](#appendix-a-legacy-incumbent-s5-register-and-verdict).

## 6. Fabrication, assembly and print readiness

**Entry point — print this:** the promoted machine's complete slicer-ready part set, print
manifest and assembly manifest are in **[`fabrication/`](fabrication/)** (see
[§6a](#6a-how-to-print-and-build-the-s5-r-machine-the-fabrication-package-dnd-60dnd-61)
and [`fabrication/README.md`](fabrication/README.md)). That package is the board's "what to
print" for S5-R. Everything in §6b below is the **earlier S5-line coupon/harness route**,
kept for provenance and for the shared rotor/platen/frame geometry, not as the S5-R print
route.

### 6a. How to print and build the S5-R machine (the fabrication package, DND-60/DND-61)

The **complete slicer-ready S5-R part set + print & assembly manifests** live
in [`fabrication/`](fabrication/) — this is the board's *"print this"* package:

- **Part set:** [`fabrication/scad/s5r_parts.scad`](fabrication/scad/s5r_parts.scad)
  (every distinct printed part, driven by
  [`s5r_parts_common.scad`](fabrication/scad/s5r_parts_common.scad)) → 14
  rendered, watertight STLs in [`fabrication/stl/`](fabrication/stl/). The two
  structural tiles are the **real full 27 × 27 / 137.16 × 137.16 mm** parts
  ([DND-61](/DND/issues/DND-61)); no reduced witness blocks remain.
- **Print manifest:** [`fabrication/manifests/print_manifest.md`](fabrication/manifests/print_manifest.md)
  — quantity, PLA, nozzle/layer, orientation, supports, sourced FDM limit per
  part, estimated mass/time. **Every critical feature PASSES** the sourced
  printability gate (no FAIL, no RISK).
- **Sub-tile fallback:** a documented 3 × 3 `cell_cartridge_tile` route
  (45.72 mm tiles) in the assembly manifest, only if the board's useful bed is
  under 137.16 mm; not required on a 256 mm X1C.
- **Assembly manifest:** [`fabrication/manifests/assembly_manifest.md`](fabrication/manifests/assembly_manifest.md)
  — exploded ordering, fasteners, and the ratified purchased BOM
  (**$404.60 delivered working**, [DND-56](/DND/issues/DND-56)).
- **Renders:** [`fabrication/images/`](fabrication/images/) — board-viewable PNGs
  of every part (iso/front/top), an assembled and exploded view of the per-cell
  register, and (DND-88) the **whole machine assembled** plus a documented
  installed-register 9 × 9 sub-block, generated by
  [`fabrication/tools/render_images.py`](fabrication/tools/render_images.py) and
  [`fabrication/tools/render_machine.py`](fabrication/tools/render_machine.py)
  ([DND-69](/DND/issues/DND-69), [DND-88](/DND/issues/DND-88)). See the
  [image gallery](fabrication/images/README.md). **CAD render, not a print.**
- **Coherence gate:** [`fabrication/tools/fab_package_checks.py`](fabrication/tools/fab_package_checks.py)
  — asserts the fabrication constants match the promoted register model, every
  part renders watertight and fits the 256 mm X1C bed, quantities match the
  80 × 80 / 3 × 3 layout, every part clears its sourced limit, and (C7) no part
  is a reduced witness without a real envelope or a documented sub-tile route.
  Runs in CI (`fab-package` job).
- **README coherence gate:** [`tools/validate/readme_s5r_coherence.py`](../tools/validate/readme_s5r_coherence.py)
  — asserts this README's promoted-machine headline (actuator count, full-map time, delivered
  cost, machine name) matches the promoted model `s5r_register.py`, so the source-of-truth
  headline cannot drift back to a superseded machine. Runs in CI (`readme-coherence` job).

**Evidence class: CAD + sourced FDM limits + calculation. No part has been
printed or measured** ([DND-27](/DND/issues/DND-27)); the board performs the
first physical print. The package carries an explicit
[**measurement-only residue**](fabrication/README.md#5-honesty--residual-uncertainty-measurement-only-residue)
(as-printed μ, leaf creep, per-set reliability, loaded torque-speed) that only a
physical build can retire.

### 6b. Legacy S5-line fabrication route (coupon/harness — provenance)

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

## 7. S5-R residual register (live)

Live register for the **promoted S5-R machine**. Every agent-reachable residual is
**closed or bounded** on DND-27 evidence classes; what remains is **measurement-only**
(un-retirable under [DND-27](/DND/issues/DND-27)) and is labelled as such. The legacy
incumbent-S5 K-register (K1–K12, R1–R8) is relocated to
[Appendix A](#appendix-a-legacy-incumbent-s5-register-and-verdict).

| Residual | Risk | Status | Evidence class |
|---|---|---|---|
| R-DND54-KEEPER | keeper leaf 1 extrusion line (RISK) | **closed** — re-profiled 0.45 → 0.90 mm (2 lines); hold is a printed shoulder in compression; keeper moved to the Y (row) axis (X gap 0.98 mm, Y gap 0.28 mm) | CAD + CALCULATION |
| R-DND54-6 | writer force unconfirmed | **closed agent-side** — bottom-up 0.2425 N; sourced 5 V push solenoid class 1.20 N (4.95×) | CALCULATION + sourced |
| R-DND54-5 | missed keeper set = silent row error | **bounded agent-side** — 99 % map needs q ≤ 1.57e-6 per keeper; verify+retry relaxes it 2–10×, writer redundancy ~798× | CALCULATION |
| R-DND54-3 | crank speed / writer settle | **bounded agent-side** — break-evens re-derived (min crank 468 deg/s, 1.54×; max settle 0.084 s, 1.67×); sourced NEMA17 class clears at 2.15× torque | CALCULATION + sourced |
| R-DND55-1 | bar reaction eccentricity e | **closed for the steel rod** — skew 0.0052 mm even at extreme e = 6 mm (33× inside gate; break-even e ≈ 201 mm) | CALCULATION |
| R-DND54-4 | multi-row bar / comber / carriage envelopes | **closed for envelopes/pitch** — five empty interference queries; R=4 adds no pitch penalty; sourced-rod requirement | CAD + CALCULATION |
| R-DND55-4 | rack reconcile (DND-55 correction) | **closed** — rack pitch 1.00 / tooth 0.50 mm; `RACK_STROKE_MM = 1.00`; time unchanged 24.615 s | CAD + CALCULATION |
| R-DND54-1 | as-printed friction μ, gate/tip sharpness | **measurement-only** (un-retirable) | — |
| R-DND54-2 | printed-leaf creep / fatigue | **measurement-only** (un-retirable) | — |
| R-DND54-5-q | as-printed per-set reliability q | **measurement-only** (requirement bounded by DND-59) | — |
| R-DND54-3-curve | loaded NEMA17 torque-speed curve | **measurement-only** | — |

**Residual retirement ([DND-59](/DND/issues/DND-59)):** the four agent-reachable residuals plus
one inherited residual are retired/bounded above; see
[`dnd59-s5r-residual-retirement.md`](../07-evidence-and-decisions/dnd59-s5r-residual-retirement.md)
for the derivations, the keeper tolerance Monte-Carlo, and the bottom-up writer-force model.

**Conditional-gate note (honesty):** exactly as S5's K6 was conditional on a dwell, the
**24.615 s** time gate is conditional on the **bank crank speed (720 deg/s)** and the
**writer settle (0.05 s)** assumptions. Its break-evens are in the model (`sensitivity`:
`timing_min_crank_deg_s_for_30s` = 468, `timing_max_settle_s_for_30s` = 0.084). Cycle life is
**reported, not gated** (`>=1e6, order unknown`), and the missed-set failure class (no
per-cell feedback) is unchanged.

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
5. **DND-48 fold the robust figures into this register** — **done** (§5a, [Appendix A](#appendix-a-legacy-incumbent-s5-register-and-verdict) here; the
   `plan` document). Robust planning numbers replace the DND-44 headlines.
6. **CostManufacturing** ratifies the machine-preserving cost path — [DND-47](/DND/issues/DND-47).
7. **Fabricator** confirms the CAD is print-ready against the harness and X1C envelope.
8. **Actuator-class / drive-topology pivot** — **done** ([DND-52](/DND/issues/DND-52),
   `test12_winner_convergence/nx52_head_actuator.py` + `_checks.py`, ADR
   [`dnd52-head-actuator-pivot.md`](../07-evidence-and-decisions/dnd52-head-actuator-pivot.md)).
   K7 has **no analytically retirable fix on the incumbent S5 head**: every
   bought-actuator lever fails cost on the real price tier or pitch. **One pivot
   survives — S5-R, a shared-drive one-time programmable rotary register** — the
   DND-52 screen's *single-row* option was later shown (DND-54) not to meet 30 s
   when counted honestly per row; the **promoted S5-R is the R=4 bank** below
   (2 bank motors + 40 writer solenoids, **$404.60 delivered**, **24.615 s**). It removes
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
    (inherits K1), **24.615 s full map**, **$404.60 delivered working** (ratified
    [DND-56](/DND/issues/DND-56); $387.18–$421.51 sourced band; DND-58 adds the
    steel rod). Real CAD of the unit
   cell renders and passes the sourced printability gate (one accepted RISK: the
   0.45 mm keeper leaf is 1 extrusion line). **Verdict: promote S5-R to a
   machine-definition candidate**; the remaining residuals (as-printed μ, gate/tip
   sharpness, leaf creep, the multi-row bar assembly) are measurement/CAD-gated and
   unmeasurable under [DND-27](/DND/issues/DND-27). Next discriminating (no-coupon)
   test: a **multi-row (R=4) bar-assembly CAD** for torsion / reset-comber / writer
   envelope.
10. **S5-R R=4 multi-row bank assembly** — **done** ([DND-55](/DND/issues/DND-55),
    `test12_winner_convergence/s5r_bank.py` + `_checks.py` + `s5r_bank.scad`,
    ADR [`dnd55-s5r-bank-assembly.md`](../07-evidence-and-decisions/dnd55-s5r-bank-assembly.md)).
    **CAD:** the R=4 bank (racked bar + 8 modelled columns + reset comber + writer-carriage
    sweep envelope) renders in real OpenSCAD; **all five interference queries empty**
    (run / selected / comber-park / comber-trip / carriage-sweep), so the **comber and
    carriage envelopes fit** and **R=4 adds no pitch penalty**. **CALCULATION:** the
    printed **3 × 2 bar is ~28× over** the keeper gate (skew 4.96 mm vs 0.175 mm) —
    **fix: sourced steel rod d = 5–6 mm** (skew ≤ 0.005 mm) or an Ø8 printed round bar;
    and the DND-54 **rack (0.60/0.45) fuses** (0.15 mm gap) — **fix: rack pitch 1.00 /
    tooth 0.50 mm**. **Verdict:** R-DND54-4 closed for the envelopes and pitch, and
    sharpened for the bar (a sourced-rod requirement, not a printed part). No print,
    no measurement.
11. **S5-R register reconciliation of the DND-55 corrections** — **done**
    ([DND-58](/DND/issues/DND-58), `s5r_register.scad` / `s5r_register.py` /
    `s5r_register_checks.py`, ADR amendment §11 in
    [`dnd54-s5r-register-latch.md`](../07-evidence-and-decisions/dnd54-s5r-register-latch.md)).
    The register now carries the corrected rack (**pitch 1.00 / tooth 0.50 mm**,
    `RACK_STROKE_MM = 1.00`) and a **sourced steel drive rod d = 6 mm** (`BAR_D_MM`,
    rendered as a round rod). **Timing unchanged at 24.615 s** (the bank pass is angular:
    72°/level; the linear per-stroke advance does not enter the timing). **BOM: +$3.48
    delivered** for the rod → honest working total **$404.60 delivered** (`margin
    $95.40`); the earlier $401.12 / $397.53 figures are retained as
    `delivered_no_rod_usd` / `delivered_claim_usd`.     **Verdict:** R-DND55-4 closed;
    R-DND54-4 closed for envelopes/pitch. No print, no measurement.
12. **S5-R residual retirement — the last agent-reachable residuals** — **done**
    ([DND-59](/DND/issues/DND-59), `s5r_residuals.py` + `s5r_residuals_checks.py`,
    ADR [`dnd59-s5r-residual-retirement.md`](../07-evidence-and-decisions/dnd59-s5r-residual-retirement.md)).
    Retires the four agent-reachable residuals + one inherited residual:
    keeper leaf RISK (re-profile to 2 lines + compression shoulder), writer force
    (bottom-up 0.2425 N vs sourced 1.20 N, 4.95×), missed-set reliability (q ≤
    1.57e-6; verify/redundancy levers 2–10×/798×), crank break-evens (468 deg/s,
    0.084 s; sourced class clears), and bar eccentricity (closed for the steel
    rod). **Registry now: every S5-R residual is closed/bounded agent-side except
    the measurement-only residue.**
13. **S5-R complete fabrication package** — **done**
    ([DND-60](/DND/issues/DND-60) + [DND-61](/DND/issues/DND-61),
    `08-current-design/fabrication/`): a slicer-ready printed-part set (14 distinct
    parts, 25,661 pieces), 14 watertight STLs, print + assembly manifests, a
    full-set sourced-FDM-limit PASS, and the `fab_package_checks.py` C1–C7 CI gate.
    DND-61 renders the two structural tiles at their true full size (no reduced
    witnesses). See [§6a](#6a-how-to-print-and-build-the-s5-r-machine-the-fabrication-package-dnd-60dnd-61).
14. **README reconcile to the promoted S5-R machine** — **done**
    ([DND-64](/DND/issues/DND-64), this document): header/§1/§2/§5/§6/§7/§9 now describe
    S5-R; the incumbent S5 is a clearly-labelled superseded subsection
    ([§2a](#2a-superseded-incumbent-s5-kept-for-the-record), [§5a](#5a-superseded-incumbent-s5-bom-kept-for-the-record)) and
    the K-register is relocated to [Appendix A](#appendix-a-legacy-incumbent-s5-register-and-verdict). A
    new CI gate (`tools/validate/readme_s5r_coherence.py`) fails if this README's
    headline contradicts the promoted model, so it cannot drift again.

### 8a. Consolidated S5-R residual registry (DND-59) — LEGACY DUPLICATE

> The live register is [§7](#7-s5-r-residual-register-live). This table is the original
> DND-59 registry, kept for provenance.

| Residual | Status | Evidence class |
|---|---|---|
| R-DND54-KEEPER (keeper leaf 1 line RISK) | **closed** — 2 lines + compression shoulder; printability PASS | CAD + CALCULATION |
| R-DND54-6 (writer force unconfirmed) | **closed agent-side** — bottom-up 0.2425 N; sourced class 1.20 N (4.95×) | CALCULATION + sourced |
| R-DND54-5 (missed set = silent error) | **bounded agent-side** — q ≤ 1.57e-6; verify/redundancy levers quantified | CALCULATION |
| R-DND54-3 (crank 720 deg/s, settle 0.05 s) | **bounded agent-side** — break-evens 468 deg/s / 0.084 s; sourced class clears | CALCULATION + sourced |
| R-DND55-1 (bar eccentricity e) | **closed for the steel rod** — 33× inside gate at extreme e | CALCULATION |
| R-DND54-4 (multi-row bar/envelopes) | closed for envelopes/pitch; sharpened to sourced rod ([DND-55](/DND/issues/DND-55)/[DND-58](/DND/issues/DND-58)) | CAD + CALCULATION |
| R-DND55-4 (rack reconcile) | closed ([DND-58](/DND/issues/DND-58)) | CAD + CALCULATION |
| R-DND54-1 (as-printed friction mu, gate/tip sharpness) | **measurement-only** (un-retirable, [DND-27](/DND/issues/DND-27)) | — |
| R-DND54-2 (printed-leaf creep/fatigue) | **measurement-only** (un-retirable, [DND-27](/DND/issues/DND-27)) | — |
| R-DND54-5-q (as-printed per-set q) | **measurement-only** (requirement bounded by DND-59) | — |
| R-DND54-3-curve (loaded NEMA17 curve) | **measurement-only** | — |

---

## 9. Final readiness verdict (S5-R)

**Verdict: PRINTABLE / buildable package ready for the board's first physical print, with a
small, named, measurement-only residue.** S5-R is the promoted machine: it clears every
mission requirement on its labelled evidence class —
- **Area / pitch / cells:** 406.4 × 406.4 mm, 5.08 mm, 6,400 — design criteria;
- **Travel:** ≥ 40 mm — design criteria (miniature-verified = measurement-only, R2);
- **Full-map reconfiguration:** **24.615 s < 30 s** — CALCULATION (conditional on the bank
  crank/settle assumptions; break-evens in the model);
- **Cost:** **$404.60 delivered < $500** — CALCULATION + sourced listings (band
  $387.18–$421.51);
- **Regional update:** bounded (common platen ⇒ one stroke per update) — CALCULATION;
- **Bought actuators:** 42 (2 bank motors + 40 writers), no per-column motor — the S5
  K7 motor cliff is **removed**;
- **Printable:** 14 real-OpenSCAD parts, 14 watertight bed-fitting STLs, print + assembly
  manifests, full-set sourced-FDM-limit **PASS** — CAD ([DND-60](/DND/issues/DND-60)/[DND-61](/DND/issues/DND-61)).

**What remains is measurement-only** (un-retirable under [DND-27](/DND/issues/DND-27)): the
as-printed friction μ / gate-tip sharpness (R-DND54-1), printed-leaf creep/fatigue
(R-DND54-2), the as-printed per-set reliability q (R-DND54-5-q), and the loaded motor
torque-speed curve (R-DND54-3-curve). These are named and bounded; the board retires them by
building the machine. No agent-reachable residual remains.

The superseded incumbent S5 did **not** reach this state (its K7 motor cliff, K5 pricing
basis, K1 base-contact model and K8 free-length questions were unretired); that legacy
verdict is preserved in [Appendix A](#appendix-a-legacy-incumbent-s5-register-and-verdict).

The mission-level disposition is recorded in the company `plan` document.


---

## Appendix A: legacy incumbent-S5 register and verdict

> **LEGACY — the superseded incumbent S5 machine.** This appendix is retained for
> provenance only (it documents why S5's cost path failed). **The live register is
> [§7](#7-s5-r-residual-register-live) and the live verdict is [§9](#9-final-readiness-verdict-s5-r).**

### A1. Robust risk register (DND-41 / DND-48)

| id | Risk | Class | Status |
|---|---|---|---|
| K1 | Cam buckling under handling load | calculation | **service load NOT closed (DND-46)** — the DND-44 "≤0.39 N/column, 12.7× margin" assumed the base conforms to *every* column top beneath it. A shape display's defining property is that column tops are at **different heights**, so a rigid base stands on the **highest three** columns (a three-point contact): 1 kg → **3.27 N/column**, only **1.5× margin** vs the 4.96 N core. Service load is therefore **0.39–3.27 N/column depending on base contact**; the three-point case is the bounding model, so **size the core against ~3.3 N**. The localized 5 N abuse screen is **bounded**: a core re-size to 1.10 mm gives **5.60 N** and clears it, at the cost of step height 0.5→0.4 mm (a real geometry trade, not a free fix). Residual: the real base contact model. `test12/buckling_closure.py`, `falsifier_checks.py` |
| K2 | Printed detent holds/repeats after a slipped step | calculation | **closed-analytically (named geometry, DND-45)** — nominal 0.20 mm scallop fails at the sourced PLA–PLA midpoint μ = 0.35 (torque/friction 0.92). The chosen **0.40 mm scallop** gives **1.84 at μ = 0.35** and **1.29 at μ = 0.50**, inside the 0.50 mm cam envelope (exact min depth 0.271 mm at μ = 0.35). As-printed μ/creep/tip sharpness remain measurement-only. `test12/DETENT_CONTACT.md` |
| K3 | Gravity return vs guide friction | calculation | **closed** — 4.06× weight/drag margin (solid column) |
| K4 | Regional update disturbs neighbour | calculation | **partially-closed** — 0.017 mm rail-bending *structural* sub-bound vs a 0.10 mm gate; J2 engine returns **INCONCLUSIVE** — stiction release and wear drift are measurement-only. ([DND-41](/DND/issues/DND-41)) |
| K5 | Cost > $500 delivered | calculation | **not closed at $424.95 (DND-46)** — that headline needed four simultaneous best-case choices (E5 spares deleted + E6 bundled lines repriced). Defensible planning basis: **$482.95 delivered, $17.05 margin** (spares + E6 restored). Sourced-DRV8833 variant **$474.91**. At the expected $1.25 motor it is **$501.51, over the ceiling**. E6 is best-case repricing, not sourcing, and is labelled as such. Conditional on a motor ≤ **$1.86**. `test12/cost_closure.py`, `falsifier_checks.py` |
| K6 | Time > 30 s at the realised step rate | calculation | **conditional (DND-46)** — 26.251 s at the design point; the **rate-independent floor is 18.65 s**. The closure is **conditional on a loaded engage/settle dwell AND a ≥268 pps (~804 rpm) loaded rate**; ~268 pps only *just* meets 30 s, and the pass assumes **`inspection_s = 0`** (at 3 s inspection the design point is 29.25 s — meets the hard cap, misses the 27 s target). The 45.07 s sweep corner is *not* rate-recoverable (its floor is 34.47 s). Verify the loaded dwell and scan accel, not a "measured rate". `test12/timing_closure.py`, `falsifier_checks.py` |
| K7 | Purchased-actuator cost cliff (80 motors) | assumption | **open — the binding residual of K5; REFUTED at ≤$1.86 on sourced evidence ([DND-49](/DND/issues/DND-49)); no actuator-class/pivot retires it ([DND-52](/DND/issues/DND-52))** — the sub-$1.86 clearing path needs an untraced multipack with **no published step angle**; every *matched, orderable* part found is $8.20–$40 → **$1,088–$4,040 delivered**. The only traced matched part (MOONS 8PM020S1) is $40 → $4,040. The reduced-head lever (fewer motors) **fails the 30 s budget** (40 channels → ~104 s) **and fails cost on the order tier** (R=4 → $531.99; boundary $9.82/station vs the $11.20 tier). Unretired only by a purchase sample (forbidden under [DND-27](/DND/issues/DND-27)) **or the S5-R shared-register pivot**. **[DND-54](/DND/issues/DND-54) closes the S5-R dropout mechanism analytically** (R=4 bank, $401.12 delivered working, 24.62 s, all gates pass) and promotes it. `test12/k7_motor_trace.py`, `nx52_head_actuator.py`, `s5r_register.py` |
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


### A2. Legacy incumbent-S5 readiness verdict (DND-46 / DND-48)

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
