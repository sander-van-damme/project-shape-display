# DND-54 — S5-R shared-drive register: analytic + CAD dropout-latch model

- **Verdict: PROMOTE S5-R (the R=4 shared-drive programmable register) to a
  machine-definition candidate in `08-current-design/`**, on **CAD + CALCULATION**
  evidence. It is the first architecture in the program to clear **every**
  analytic gate it presents — cost, time, pitch, neighbour cross-talk, latch
  release force, bank drive force, and inherited service load — at the 5.08 mm
  pitch. It removes the entire 80-bought-motor cliff that refuted the S5
  incumbent ([DND-49](/DND/issues/DND-49), [DND-52](/DND/issues/DND-52)).
- **This is NOT a print and NOT physical validation** ([DND-27](/DND/issues/DND-27)).
  Every figure is labelled CAD / CALCULATION / sourced / assumption. The decisive
  residual — as-printed friction, gate/tip sharpness, leaf creep and the
  multi-row bar assembly — remains measurement-gated and is stated in §9.
- **Owner:** CTO. **Issue:** [DND-54](/DND/issues/DND-54), for
  [DND-52](/DND/issues/DND-52) and the mission goal.
- **Inputs (imported, so nothing drifts):** `timing_closure.py`, `cost_closure.py`,
  `nx52_head_actuator.py`; the model is
  `06-experiments/test12_winner_convergence/{s5r_register.py, s5r_register_checks.py}`,
  CAD is `s5r_register.scad`, printability is
  `tools/validate/analytic_printability.py` (register-cell branch).
- **Evidence class:** CAD (SCAD + real-OpenSCAD render + mesh validation) and
  CALCULATION (force / timing / endurance over sourced FDM process limits and
  sourced actuator ratings). No purchase, no print, no measurement.
- **DND-58 amendment (rack pitch + drive rod):** the [DND-55](/DND/issues/DND-55)
  bank close-out refuted two register-level geometry values and this ADR now
  carries the corrected ones: rack **pitch 0.60 → 1.00 mm / tooth 0.45 → 0.50 mm**
  (the old 0.15 mm inter-tooth gap fuses at a 0.4 mm nozzle) and the per-stroke
  advance becomes **1.00 mm**; the printed 3 × 2 drive-bar placeholder is replaced
  by a **sourced steel rod d = 6 mm** (bar-torsion skew 4.96 mm → ≤0.005 mm vs the
  0.35 mm keeper gate). Honest delivered BOM is now **$404.60** (adds the 1 steel
  rod; the $401.12 channel-priced total is retained as `delivered_no_rod_usd`).
  See §11.

Run:

```text
cd 06-experiments/test12_winner_convergence
python s5r_register.py            # full model, JSON
python s5r_register_checks.py     # regression + honesty gates
# CAD (real OpenSCAD) + sourced printability:
openscad -o /tmp/s5r.stl s5r_register.scad
python ../../tools/validate/analytic_printability.py s5r_register.scad
```

## 1. The question, restated

[DND-52](/DND/issues/DND-52) found S5-R *cost+time feasible* ($304.73, 24.65 s)
but parked its decisive quantity — **selective dropout / re-engage of an 80-rotor
bank at 5.08 mm pitch** — as "coupon-only". A coupon is forbidden ([DND-27](/DND/issues/DND-27)).
This ADR replaces the coupon with the two evidence classes DND-27 *does* allow —
an analytic kinematic/static model and CAD/mesh validation — and asks whether the
register dropout latch is **kinematically real** at 5.08 mm pitch with bounded
force, no neighbour cross-talk, and a full map under 30 s.

## 2. The concrete mechanism (DND-54 definition)

Rows run along Y; the in-row column pitch is 5.08 mm. The S5 five-level stepped
rotor is **unchanged** (radius 1.5 mm, core 1.0 mm, 72°/level, from
`test08/results/parameters.scad`). S5-R removes the 80 bought head motors:

1. **Shared oscillating drive bar.** One motor (here: two, both ends) strokes a
   toothed bar that runs under a whole group of rotor hubs. Each hub carries a
   printed **drive pawl** — a vertical cantilever leaf, spring-biased into the
   bar's rack. One forward stroke of one rack tooth = a 72° advance of every
   engaged pawl (and therefore every coupled rotor).
2. **Per-column keeper latch.** A bistable over-centre leaf with a 5-position
   gate (run + four stop positions). The writer sets the gate for the column's
   target level.
3. **SELECT.** The writer carriage (40 solenoids, off the dense field) sets every
   keeper in the group. The bar then makes **one continuous forward pass** through
   4 rack steps (4 × 72° = 288°). Each pawl is cammed out of the rack the first
   time it reaches its keeper gate, then latches dropped-out and skips the rest.
4. **RESET.** One reverse pass with a **reset comber** trips every dropped-out
   pawl back over centre to "run". Re-engage is one shared kinematic motion, not a
   per-column actuator.

## 3. The DND-54 correction to DND-52: the bank is R rows deep (R = 4)

[DND-52](/DND/issues/DND-52)'s option-1 timing replaced the whole 80-column step
time with a token "20 stations × 0.3 s" and did **not** model a per-row cycle. An
honest per-row count changes the conclusion: a **single-row** (R=1) bank needs 80
groups, and even with 80 writers and an aggressive 3 rev/s crank it is **≥36 s** —
over budget. The register's real lever is that **the bank bar can span R rows in
depth at no pitch penalty**, because the *row* pitch (5.08 mm) is independent of
the in-row column pitch. A single bank pass then writes **R rows at once**, so the
map needs `ceil(80/R)` groups instead of 80. Sweeping R:

| R (rows in bank) | groups | writer stations/group @W=40 | per group | full map | clears 30 s? |
|---:|---:|---:|---:|---:|:--:|
| 1 | 80 | 2 | 0.9 s | 54.9 s | no |
| 2 | 40 | 4 | 0.9 s | 36.0 s | no |
| **4** | **20** | **8** | **0.9 s** | **24.6 s** | **yes** |
| 5 | 16 | 10 | 0.9 s | 22.3 s | yes (but bank force fails) |

**Chosen design point: R = 4, W = 40 writers, 2 bank motors.** R=5 clears time
but the bank force needs a bigger motor; R=4 is the largest bank the single
0.30 N·m motor class can drive at 2.15× margin (see §4). The added cost of 40
vs 8 writers is $80 and it is well inside the ceiling (§5).

## 4. The static / kinematic gates (all pass)

| Gate | Quantity | Value | Limit | Margin | Class |
|---|---|---|---:|---:|---|
| G1 | cell fit, worst case (pawl+keeper in the 2.08 mm free band) | stack 1.55 mm | ≤ 2.08 mm | 0.53 mm gap | CAD + calc |
| G2 | neighbour cross-talk (dropped pawl carries **zero** rack force) | 0.0 N | — | gap 0.53 mm, lash 0.20 → 0.33 mm | calc |
| G3 | writer release force (keeper over-centre + friction) | 0.066 N | 1.20 N | **18.1×** | calc |
| G4 | bank drive force (320 pawls × 0.0874 N / 0.60 bus) | 46.6 N | 100 N (2 motors) | **2.15×** | calc |
| G5 | latch vs service load (latch dormant in service) | 0 N added | inherits K1 | unchanged | calc |
| G6 | full-map time | **24.62 s** | < 30 s | **+5.39 s** | calc |
| G7 | delivered cost | **$401.12** (working; $387.18 opt / $421.51 high) | ≤ $500 | **−$98.88** | sourced |
| G8 | cycle life (printed pawl/keeper leaf) | ≥1e6, order unknown | reported | — | calc |

**G2 is the pivotal one.** A *dropped-out* pawl is held clear of the rack by its
keeper and therefore carries **no** drive force; the shared bar transmits no
per-cell load to it. Neighbour cross-talk is thus a *geometry gap* (0.53 mm worst
case, minus 0.20 mm detent lash = 0.33 mm clear), not a force. This is the
mechanism that refutes the "silent row error via neighbour drag" failure mode.

**G4** is the binding mechanical gate. With the pawl at 2 extrusion lines
(0.90 mm) and 8 mm long, its seated force is 0.0374 N; plus a 0.05 N unloaded
write load, 320 pawls give 28.0 N at the rack, 46.6 N at the pinion with a 0.60
bus efficiency. Two 0.30 N·m motors (100 N available) give 2.15× margin. **One
motor alone would be only 1.07×** — the sensitivity number that says *use two*.

## 5. Cost and time

**Cost (delivered = parts × 1.16, the repo's additive basis, imported from
`cost_closure.py`):** no-channel base **$218.70** + 2 bank motors × $12 +
40 writers × $2.50 = **$342.70 parts → $397.53 delivered** as the *channels-unpriced
claim* ($102.47 under the $500 ceiling; $969 under the S5 incumbent's refuted
$1,366.87). The 80-channel driver block ($63.64) leaves with the motors. The
**honest working total is `$401.12`** once the S5-R block's own marginal channels
are priced (§ below); `s5r_register.bom(4)` now returns both (`delivered_claim_usd`
= `$397.53`, `delivered_usd` = `$401.12`). *Sourced point-in-time prices; the DND-52
$304.73 figure was the smaller W=8 variant and did not include the second bank
motor or the wider writer bank.*

**The model prices the block's own channels (the DND-56 fix, now in `bom()`).**
The fixed no-channel base has **both** the 80-motor line **and** the 80-channel
TB6612 driver block removed, so — by the `nx52_head_actuator.py` contract,
*"every option declares its own channel cost exactly once"* — the S5-R block must
declare its channels. `bom()` now charges **2 bank H-bridge ICs** (1 dual TB6612
per bank motor, `$0.7955` each = `$1.59`) **+ 5 ULN2803-class writer darlington
chips** (8 ON/OFF writers each, `$0.30` each = `$1.50`) = **`$3.09` parts**,
bringing the honest working total to **`$401.12`** — the same figure the DND-56
ratification derived independently. `s5r_register_checks.py` gates this so a
future edit cannot silently re-zero the channel line.

**Independent ratification ([DND-56](/DND/issues/DND-56)).** The $397.53 figure was
re-derived from first principles against sourced listings and **reproduces exactly**
(the no-channel base and the `218.70 + 63.64 = 282.34` driver-block identity both
hold — no double-count); the two actuator allowances trace to **$12.39 (motor) /
$2.20 (writer)**, within ±$0.40. **One material correction:** `bom()` prices the
S5-R block's *own* channels at **zero**. The 80-channel TB6612 block leaves *with*
the motors, but the 2 bank steppers and 40 writer solenoids still need channels —
2 bank H-bridge ICs + 5 ULN2803-class writer switches = **$3.09 parts** (the
writers are on/off, so a ~$0.30 darlington channel suffices, not a TB6612). Pricing
them explicitly (they were only *implicitly* covered by the fixed
`Custom driver PCBs and passives` line, which was sized for the 80-motor head):

| Scenario | Delivered | vs $500 | vs <$400 |
|---|---:|---:|---:|
| Optimistic (sourced units, 1 bank IC) | **$387.18** | −$112.82 | −$12.82 |
| **Working (allowances + marginal channels)** | **$401.12** | **−$98.88** | **+$1.12** |
| High (premium NEMA17 + premium writer) | **$421.51** | −$78.49 | +$21.51 |
| Claim above (channels unpriced) | $397.53 | −$102.47 | −$2.47 |

The credible delivered figure is therefore **$401.12** (working), i.e.
**$387.18–$421.51** across the sourced band — **solidly under the $500 ceiling, but
~$1.12 *over* the program's ideal <$400 band** in the working scenario. The
ceiling-level verdict is unchanged; the "<$400 ideal" phrasing only held because
the block channels were unpriced. Break-even for the $500 ceiling: bank motor
**$54.62/ea**, writer **$4.63/ea** — 4.5× and 1.85× the allowances, so no line
dies on cost. Residual: the writer solenoid's **force (N) is not published by any
listing** (R-DND54-6), and no 2–4-piece contract quote exists — both
purchase-gated under [DND-27](/DND/issues/DND-27). The ratifying note is
`07-evidence-and-decisions/dnd54-s5r-bom-ratification.md`
(`06-experiments/test12_winner_convergence/s5r_bom_ratify.py`, 11 CI gates).

**Time (24.62 s, calc):** fixed platen/reference 5.26 s + 19 group-index moves
(19 × 0.071 s) + 20 groups × 0.90 s. Per group: 8 writer stations × 0.05 s +
4 select steps × 0.1 s + 1 reset step × 0.1 s = 0.40 + 0.40 + 0.10 s.

## 6. Sensitivity — where the verdict flips (the discriminating numbers)

| Assumption | Chosen | Break-even | Margin |
|---|---:|---:|---:|
| bank crank speed | 720 °/s | **468 °/s** | 1.54× |
| writer station settle | 0.05 s | **0.084 s** | 1.67× |
| bank motor torque (2 motors) | 0.30 N·m | **0.14 N·m** | 2.15× |
| per-face print accuracy (fit) | ±0.10 mm | **±0.365 mm** | 3.65× |
| actuators | $124 parts | ceiling at ~$460 parts | $98.88 headroom |

**The time gate is conditional on the crank speed and the writer settle, exactly
as S5's K6 is conditional on its loaded dwell.** The geometry gate is robust
(3.65× the assumed print error). The cost gate has $98.88 of headroom at the
working tier (see §5).

## 7. CAD evidence

`s5r_register.scad` is a **single-column unit cell** (housing, rotor, pawl,
keeper, toothed drive bar). It renders with a real OpenSCAD (2023.09.11) into four
watertight STLs (`assembly`, `cell`, `pawl`, `keeper`); `analytic_printability.py`
reads the SCAD constants and returns:

| Feature | Value | Limit | Verdict |
|---|---:|---:|---|
| pawl leaf thickness | 0.90 mm | 0.88 mm | PASS |
| keeper leaf thickness | 0.45 mm | 0.88 mm | RISK (1 line; light latch) |
| housing wall | 0.90 mm | 0.88 mm | PASS |
| lateral gap to neighbour (worst case) | 0.47 mm | 0.20 mm | PASS |
| rotor bore free play (worst case) | 0.20 mm | 0.20 mm | PASS |
| rack tooth height | 0.45 mm | 0.44 mm | PASS |

The single RISK is the keeper leaf at one extrusion line — an **accepted** risk
for a lightly-loaded bistable latch, stated rather than hidden. The load-bearing
pawl is two lines and PASSes.

## 8. What this does and does not claim

- **Does:** define S5-R concretely; show that all its analytic gate quantities
  close with stated margins; provide real CAD of the unit cell plus sourced
  printability; add multi-row depth (R) as the design lever DND-52 omitted; and
  give the break-even numbers for the next test.
- **Does not:** claim a printed or measured part, a qualified motor/solenoid, a
  full multi-row bar assembly, or a retired friction/creep quantity. The
  measurement-gated residuals are: as-printed pawl/keeper friction μ, gate and
  tip sharpness, leaf creep (K2/K11 class), and the multi-row bar drive's
  torsional/timing behaviour. **No coupon will be printed** ([DND-27](/DND/issues/DND-27));
  these remain named residuals, not retired ones.

## 9. Residual uncertainty / risk register

| id | Residual | Class | Status |
|---|---|---|---|
| R-DND54-1 | As-printed pawl/keeper friction μ and gate/tip sharpness | measurement-only | open — inherits K2 class; no coupon ([DND-27](/DND/issues/DND-27)) |
| R-DND54-2 | Printed-leaf creep/fatigue (G8 cycle life) | measurement-only | open — '≥1e6, order unknown' on DND-46 FDM constants |
| R-DND54-3 | Crank speed (720 °/s) and writer settle (0.05 s) | assumption | conditional — break-even 468 °/s / 0.084 s; analogue of S5's K6 |
| R-DND54-4 | Multi-row (R=4) bar drive: torsion, per-row timing skew, full assembly interference | CAD/calc | **closed for envelopes/pitch** ([DND-55](/DND/issues/DND-55)); **sharpened** to a sourced-steel-rod requirement ([DND-58](/DND/issues/DND-58)) |
| R-DND54-5 | Missed keeper set = silent row error | assumption | open — same class as S5's missed step; no per-cell feedback (R1 unchanged) |
| R-DND54-6 | Sourced motor/solenoid at the assumed price and force | sourced | point-in-time; unretired by purchase ([DND-27](/DND/issues/DND-27)) |

## 10. Decision and next actions

1. **PROMOTE S5-R (R=4) to a machine-definition candidate alongside the incumbent
   S5.** It is the only architecture that clears cost, time, pitch and the
   dropout mechanism analytically. Update `08-current-design/` to carry S5-R as
   the promoted direction and S5 as the bought-motor fallback (nominal only,
   refuted on the order-tier motor price).
2. **Fold the S5-R register into the DND-48 robust risk register** with the
   R-DND54 residuals above; the K-path (K1/K2/K3/K4/K8/K9/K11) is inherited
   unchanged because the rotor, follower, detent and hard stop are unchanged.
3. **Next discriminating test (analytic/CAD, no coupon):** a **multi-row bar
   assembly CAD** (`R=4`) checking bar torsion, the reset comber envelope, and
   the writer carriage envelope — the only unit-cell-external geometry not yet
   modelled. **Done: [DND-55](/DND/issues/DND-55).**
4. **CostManufacturing:** re-verify the 2-motor + 40-writer delivered BOM against
   sourced listings — **done ([DND-56](/DND/issues/DND-56))**: $397.53 reproduces;
   honest working total **$401.12 delivered** after pricing the block's marginal
   channels (§5). Amendment folded into this ADR.
5. **Do NOT contact the board.** S5-R promotion is an internal ADR; the board
   trigger is a buildable print-ready machine, which this is not yet (the
   measured-friction/creep residuals are unresolved and unmeasurable under
   DND-27). State that boundary plainly.

## 11. DND-58 amendment — register reconciliation of the DND-55 corrections

[DND-55](/DND/issues/DND-55) CAD-modelled the R=4 bank and returned two
corrections that land at the **register** level (its residual R-DND55-4):

**(a) Rack re-dimension.** The DND-54 rack (`RACK_TOOTH_PITCH = 0.60`,
`RACK_TOOTH_HEIGHT = 0.45`) leaves a **0.15 mm inter-tooth gap** that fuses at a
0.4 mm nozzle (one line = 0.44 mm). `s5r_register.scad` / `s5r_register.py` now
carry **pitch 1.00 / tooth 0.50 mm** (gap 0.50 mm, printable). The per-stroke
advance `RACK_STROKE_MM` is re-derived from the **pitch** (1.00 mm), not the old
tooth height (0.45 mm); it was previously set to `RACK_TOOTH_HEIGHT_MM`.

**(b) Timing is unchanged.** The pass is **angular**: the crank turns 72°/level
regardless of rack pitch. The 0.60 → 1.00 mm linear advance does *not* move the
select/reset times, so the full-map figure stays **24.62 s** (< 30 s, +5.39 s).
`timing()` now reports `rack_stroke_mm = 1.00` and `crank_deg_per_level = 72` to
make this traceable.

**(c) Drive bar section.** The printed 3 × 2 placeholder (peak bar-torsion skew
4.96 mm, ~28× the keeper gate/2 = 0.175 mm) is replaced by a **sourced steel rod
d = 6 mm** (skew ≤ 0.003 mm, ~67× under the gate); an Ø8 printed round bar is the
fallback. The register model declares `BAR_D_MM = 6.0`,
`BAR_MATERIAL = "sourced steel rod"`, and `s5r_register.scad` renders a round rod.

**(d) BOM delta.** One 6 mm × 406.4 mm steel rod enters the S5-R block at a
**$3.00 sourced-class allowance** → **$3.48 delivered** at the repo's 1.16 uplift.
The honest working total moves **$401.12 → $404.60 delivered** (`margin_usd =
$95.40`). Both earlier figures are retained as fields (`delivered_claim_usd`
$397.53, `delivered_no_rod_usd` $401.12) so the DND-54/DND-56 records still
reproduce. `s5r_register_checks.py` gates all of the above.

**Residuals after this amendment.** R-DND55-4 (register timing reconciliation) is
**closed**; R-DND54-4 is closed for envelopes/pitch and sharpened to a
sourced-rod requirement. R-DND55-1 (reaction eccentricity `e`) remains an
assumption for any *printed* bar, but is made irrelevant by the steel rod. No new
measurement-only residual is introduced. Evidence class: CAD + CALCULATION.
