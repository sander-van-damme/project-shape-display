# DND-72 — Ultra-low-cost S5-R variant (<$250 purchased): architecture, cost ladder, and the infeasibility proof

- **Issue:** [DND-72](/DND/issues/DND-72) (CTO). Parent [DND-70](/DND/issues/DND-70);
  gated children [DND-73](/DND/issues/DND-73) (CostManufacturing ratification) and
  [DND-74](/DND/issues/DND-74) (Falsifier audit).
- **Status:** **NEGATIVE RESULT — the <$250 target is infeasible under the unchanged mission
  requirements.** Delivered as a proof + break-even, exactly as the issue allows.
- **Evidence class:** **CALCULATION** over the promoted S5-R model and sourced listings +
  **CAD** (real OpenSCAD render, watertight). **No print, no purchase, no measurement**
  ([DND-27](/DND/issues/DND-27)).
- **Artifacts:** `09-low-cost-variant/s5r_ultra.py`, `s5r_ultra_checks.py` (19 checks),
  `scad/s5r_ultra_cell.scad` + `stl/{cell,pawl,keeper}.stl`,
  `tools/render_lowcost_cad.py`. CI: `lowcost-variant` job.

## 1. The question

Can the promoted S5-R machine ([DND-54](/DND/issues/DND-54) … [DND-65](/DND/issues/DND-65),
**$404.60 delivered / 24.615 s**) be re-engineered so its **purchased-component cost is under
$250** while **every other mission requirement is unchanged** — 406.4 × 406.4 mm, 5.08 mm pitch,
6,400 cells, ≥ 40 mm travel, full-map < 30 s, regional updates, X1C-buildable?

## 2. Answer

**No.** The target is not merely hard; the sub-$250 space is **empty for this architecture**.

The binding fact is the **fixed no-channel purchased base** — every bought line that is *not* a
per-cell actuator or a per-channel driver. On the promoted S5-R model that base is **$218.70 parts
→ $253.69 delivered**, and it **by itself exceeds the $250 delivered target by $3.69**. There is
**negative headroom ($-3.18 parts) for even one actuator**, let alone the 2 bank motors + 40
writers the mechanism needs.

Because the base is a *floor* (it only grows with actuators), **no actuator count can bring S5-R
under $250**. An exhaustive sweep of the lever space (R = rows-in-bank 2…16, writers 8…80 step 4,
bank motors 1…2; **570 points**) finds **zero** configurations under $250 — including the ones that
would break the 30 s gate.

## 3. The sourced cost ladder

All figures are **purchased parts × the repo's additive uplift 1.16** (DND-41), from the promoted
model's own `bom()` / `nx52.FIXED_PARTS_NO_CHANNEL`. Evidence class: **calculation over sourced
listings + stated allowances**.

| Line | Parts | Delivered | Class |
|---|---:|---:|---|
| **Fixed no-channel base** (controller, PCB/passives allowance, lift/drive, guide rods, supply, loom, fasteners, spares, sensors) | **$218.70** | **$253.69** | CALCULATION (inherited, sourced + allowances) |
| + 2 bank NEMA17-class motors | $24.00 | $27.84 | sourced-class allowance |
| + 40 writer solenoids | $100.00 | $116.00 | sourced-class allowance |
| + 2 bank H-bridge ICs ($0.7955 ea) | $1.59 | $1.85 | SOURCED (LCSC C88224) |
| + 5 writer darlington chips ($0.30 ea) | $1.50 | $1.74 | sourced-class |
| + 1 sourced steel drive rod | $3.00 | $3.48 | sourced-class |
| **= promoted S5-R** | **$348.79** | **$404.60** | ratified [DND-56](/DND/issues/DND-56) |

The **base alone ($253.69)** is 101.5 % of the $250 target. To reach $250 delivered the *parts*
line must be **< $215.52**, i.e. the base must fall **$3.18 (1.5 %)** **before any actuator is
counted** — and every actuator then pushes it back over.

## 4. Candidate topologies (the lever space that was tried)

The only purchased-cost levers that do not change the mechanism are: **fewer bank motors**, **fewer
writers**, and the **bank depth R** (which trades rows-per-pass against writer stations). They
**fight each other**: deeper R cuts the group count (time) but multiplies the cells written per
group, so it multiplies writer stations (time). Every point is costed + timed + force-checked in
`s5r_ultra.topologies()`.

| id | R | writers | bank motors | delivered | full-map s | <$250? | <30 s? | bank force | all reqs? |
|---|---:|---:|---:|---:|---:|---|---|---|---|
| R4-W40-M2 (promoted control) | 4 | 40 | 2 | $404.60 | 24.615 | no | yes | ok | yes |
| R8-W8-M1 | 8 | 8 | 1 | $295.57 | 50.902 | no | **no** | **fail** | no |
| R6-W16-M1 | 6 | 16 | 1 | $319.12 | 34.187 | no | **no** | **fail** | no |
| R8-W16-M1 | 8 | 16 | 1 | $319.12 | 30.902 | no | **no** | **fail** | no |
| R6-W24-M1 | 6 | 24 | 1 | $342.66 | 27.187 | no | yes | **fail** | no |
| R4-W24-M1 | 4 | 24 | 1 | $342.66 | 30.615 | no | **no** | ok | no |

Cheaper configurations always miss < 30 s; configurations that clear < 30 s always cost ≥ $319.
A **single** bank motor additionally **fails the bank-drive force gate** for R ≥ 6 (one motor
supplies 50.0 N; R=6 needs 69.9 N, R=8 needs 93.2 N), so depth is capped at R=4 for a one-motor
bank. **None is under $250.**

## 5. Requirement-preservation proof / break-even

The cheapest configuration that **preserves every mission requirement** is found exhaustively
(`cheapest_requirement_preserving()`):

| Quantity | Value |
|---|---:|
| Cheapest requirement-preserving id | **R6-W20-M2** (R=6, 20 writers, 2 bank motors) |
| Purchased parts | $298.19 |
| **Delivered** | **$345.90** |
| Full-map time | **29.987 s** (< 30 s, margin 0.013 s) |
| Margin to the mission's own $500 ceiling | $154.10 |

So the honest floor of this architecture under unchanged requirements is **~$346**, and the $250
target is **~$96 too low**. This is the **break-even number** the issue asks for.

| Requirement | Status at R6-W20-M2 | Class |
|---|---|---|
| ~400 × 400 mm / 5.08 mm / 6,400 cells | unchanged geometry | CAD |
| ≥ 40 mm travel | 41 mm platen stroke retained | CAD + calc |
| full-map < 30 s | **29.987 s** | CALCULATION (crank/settle-conditional) |
| regional updates | common platen ⇒ one stroke | CALCULATION |
| X1C-buildable | unit cell renders watertight + printability **PASS** | CAD + sourced limits |
| **purchased < $250** | **$345.90 — FAILS by $95.90** | CALCULATION + sourced |

## 6. What is needed for <$250 (the only remaining avenue)

Because the base is the binding term, the *only* way to reach <$250 is a **sourced reduction of the
fixed base itself** (cheaper frame / lift / supply lines at the *same capability*), or a
**relaxation of a mission requirement**:

- relaxing **time** alone does not help (the base already busts the target with zero actuators);
- relaxing **cost target** to a realistic figure ⇒ **$346** is the architecture's floor;
- a **different architecture** with a genuinely lower fixed base floor would be required, which is
  out of scope for "an S5-R variant" and would re-open the whole machine definition.

**The one falsifier that overturns this verdict:** a sourced, non-requirement-touching
fixed-base reduction below **$215.52 parts** ($250 delivered). Until such listings exist, <$250 is
unreachable at any actuator count. This is recorded for [DND-74](/DND/issues/DND-74) to attack.

## 7. Evidence classes (explicit)

| Claim | Class |
|---|---|
| Base $218.70 → $253.69; S5-R $404.60 / 24.615 s | CALCULATION (over sourced listings + allowances, ratified DND-56) |
| No sub-$250 point in 570-point sweep | CALCULATION |
| Floor $345.90 / 29.987 s | CALCULATION |
| Unit cell watertight, printability PASS | **CAD** (real OpenSCAD) + sourced FDM limits |
| Anything about printed fit/function | **not claimed** — measurement-only, un-retirable under DND-27 |

## 8. Failed ideas recorded as evidence

- **"Just use fewer writers."** Cost falls, time rises past 30 s (R8-W8-M1 = $295.56 / 50.90 s).
- **"Just use one bank motor."** Saves ~$14 but the bank force gate (46.6 N required at R=4) is
  met by one motor (50 N) only marginally and the writer-station cost still dominates; the true
  binding term is the **base**, not the actuators.
- **"Cheaper drive topology."** Any topology that preserves the requirements sits ≥ $319 delivered;
  <$250 is unreachable because the non-actuator base already exceeds it.

## 9. Disposition

- **Artifacts** in `09-low-cost-variant/` on branch `cto/dnd72-ultra-low-cost`.
- **No board contact** ([DND-32](/DND/issues/DND-32)); this is an internal negative result.
- Gated children [DND-73](/DND/issues/DND-73) / [DND-74](/DND/issues/DND-74) auto-wake on close.
- **Residual uncertainty:** the base line is inherited as a sourced-plus-allowance bundle; the
  sweep is over the actuator lever space only (the base is held fixed). A future sourced base
  reduction is the named falsifier.
