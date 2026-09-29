# DND-72: ultra-low-cost S5-R variant (<$250 purchased) — infeasibility proof + break-even + CAD

**Negative result delivered as required.** The promoted S5-R machine **cannot** be brought under a
**$250 purchased** cost while every other mission requirement is unchanged. This PR proves it,
produces the **sourced cost ladder**, the **requirement-preservation table**, and the **break-even
number**, and adds the new subdirectory `09-low-cost-variant/`. `08-current-design/` is untouched.

**Evidence class:** CALCULATION over the promoted S5-R model + sourced listings, plus CAD (real
OpenSCAD). **No print, no purchase, no measurement** ([DND-27](/DND/issues/DND-27)). **No board
contact** ([DND-32](/DND/issues/DND-32)).

## Engineering question

Can S5-R ($404.60 delivered / 24.615 s) be re-engineered below **$250 purchased** while keeping
406.4 × 406.4 mm, 5.08 mm pitch, 6,400 cells, ≥ 40 mm travel, full-map < 30 s, regional updates and
X1C-buildability?

## Answer

**No — the sub-$250 space is empty, not merely thin.** The binding term is not the actuators; it is
the **fixed no-channel purchased base** (frame, lift/drive, supply, loom, fasteners, controller,
PCB/passives allowance, spares), which is **$218.70 parts → $253.69 delivered** and **by itself
exceeds the $250 target by $3.69**. Headroom for any actuator is **negative (−$3.18 parts)**. Since
the base is a floor, **no actuator count can reach $250**.

An exhaustive sweep of the lever space (R = rows-in-bank 2…16, writers 8…80 step 4, bank motors
1…2; **570 points**) finds **zero** sub-$250 configurations. The cheapest configuration that still
**preserves every requirement** is **R6-W20-M2 (R=6, 20 writers, 2 bank motors)** at
**$345.90 delivered / 29.987 s** — the architecture's break-even, **$95.90 above** the target.

## What changed

- **`09-low-cost-variant/s5r_ultra.py`** — analytic model. Imports the promoted S5-R model
  (`s5r_register`, `nx52_head_actuator`, `timing_closure`, `cost_closure`) so it cannot drift.
  Provides `fixed_base()`, `topologies()`, `budget_scan()`, `cheapest_requirement_preserving()`,
  `relaxation_ladder()`, `decide()`.
- **`09-low-cost-variant/s5r_ultra_checks.py`** — **19 CI-style assertions** pinning: base
  $218.70/$253.69, no sub-$250 point, floor $345.90/R6-W20-M2 (<30 s, <$500), verdict
  `INFEASIBLE_UNDER_UNCHANGED_REQUIREMENTS`, and the S5-R control ($404.60 / 24.615 s) unchanged.
- **`09-low-cost-variant/scad/s5r_ultra_cell.scad`** — real OpenSCAD: the unchanged DND-59 unit cell
  plus the R=6 bank cross-section of the chosen design point.
- **`09-low-cost-variant/stl/{cell,pawl,keeper}.stl`** — watertight renders;
  `tools/render_lowcost_cad.py` renders + mesh-validates and fails hard without OpenSCAD.
- **`09-low-cost-variant/README.md`** — headline, ladder, requirement table.
- **`07-evidence-and-decisions/dnd72-low-cost-variant.md`** — ADR: cost ladder, topology table,
  requirement-preservation proof, break-even, failed ideas, falsifier.
- **CI:** new `lowcost-variant` gate step (model + checks) and a `lowcost-cad-render` job (render +
  printability).
- **`tools/validate/analytic_printability.py`** — routes `s5r_ultra_cell` to the existing
  register-cell checker (geometry is identical).

## Evidence produced

| Check | Result |
|---|---|
| `09-low-cost-variant/s5r_ultra_checks.py` | **19 passed, 0 failed** |
| `09-low-cost-variant/tools/render_lowcost_cad.py` | **ALL PARTS OK** — cell 5.08×5.08×14, pawl 0.9×0.7×8, keeper 0.9×1.1×4.5, all watertight |
| `tools/validate/analytic_printability.py … s5r_ultra_cell.scad` | **VERDICT PASS** (no FAIL, no RISK) |
| `tools/validate/readme_s5r_coherence.py` | **GATE PASS** (R1–R6) — S5-R headline untouched |

Pinned constants: base **$218.70 → $253.69**; S5-R **$404.60 / 24.615 s**; floor **$345.90 /
29.987 s**; gap **$95.90**.

## Requirement-preservation table (chosen point R6-W20-M2)

| Requirement | Status | Class |
|---|---|---|
| 406.4 × 406.4 mm / 5.08 mm / 6,400 cells | preserved | CAD |
| ≥ 40 mm travel | 41 mm platen stroke | CAD + calc |
| full-map < 30 s | 29.987 s | CALCULATION |
| regional updates | common platen ⇒ one stroke | CALCULATION |
| X1C-buildable | watertight + printability PASS | CAD + sourced limits |
| **purchased < $250** | **$345.90 — FAILS by $95.90** | CALCULATION + sourced |

## Assumptions / limits

- The fixed base is inherited as a sourced-plus-allowance bundle; the sweep holds it fixed and
  varies only the actuator lever space. A **sourced, non-requirement-touching base reduction below
  $215.52 parts** is the one named falsifier that would overturn the verdict — recorded for
  [DND-74](/DND/issues/DND-74) to attack.
- Timing is conditional on the promoted crank/settle assumptions, exactly as S5-R's is.
- Measurement-only residue unchanged and un-retirable under [DND-27](/DND/issues/DND-27).

## Most informative next test

A **sourced search for a cheaper fixed base at equal capability** (frame / lift / supply lines),
which is the only avenue to <$250. Otherwise the honest disposition for the parent
[DND-70](/DND/issues/DND-70) is that the <$250 target requires relaxing a requirement or a
different architecture. On close, gated children [DND-73](/DND/issues/DND-73) /
[DND-74](/DND/issues/DND-74) auto-wake.
