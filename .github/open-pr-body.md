# DND-71 — S6-LC: ultra-low-cost shape-display alternative (<$250 purchased)

Closes/advances [DND-71](/DND/issues/DND-71) (board direction [DND-70](/DND/issues/DND-70)).

## What changed

- **New subdir `09-lowcost-alternative/`** holding a complete candidate machine
  definition: architecture rationale, real-OpenSCAD CAD, a sourced BOM with a
  delivered total under the ceiling, and the analytic timing/force/cost model.
- **`08-current-design/` (S5-R) is not touched** — the board required a new
  subdir, and this PR opens/modifies none of it.
- New CI: an `engineering-checks` step (model + 29 regression checks +
  printability) and a real-OpenSCAD render job `s6lc-cad-render`.

## Engineering question addressed

Can the product (80×80 cells, 5.08 mm pitch, ≥40 mm travel, <30 s full map,
regional updates) be built for **< $250 purchased parts, excluding printed**
when S5-R's parts are $348.79 and its legacy fixed base alone is $218.70?

## Result (all six analytic gates PASS)

| Metric | S5-R | **S6-LC** |
|---|---:|---:|
| Purchased parts | $348.79 | **$139.77** |
| Delivered (×1.16) | $404.60 | **$162.13** (margin $87.87) |
| Full map | 24.615 s | **7.4 s** |
| Bought actuators | 42 | **3** |

The decisive move is removing the **40-solenoid writer bank** (replaced by a
passive per-bank broadcast threshold mask) and the legacy lift/scan stock.
S1's two known failures are addressed: banked reset bounds worst-case release
force to 128 N (296 N ceiling), and the mask is set off-line (a stated product
limitation, priced and documented, not hidden).

## Evidence produced

- `analysis/s6lc.py` — geometry, force, timing, BOM, gate screen.
- `analysis/s6lc_checks.py` — **29/29 checks pass**.
- `analysis/printability_s6lc.py` — sourced-FDM-limit table, **all PASS**.
- `analysis/render_s6lc_cad.py` — **5 parts render watertight** (real OpenSCAD + trimesh).
- `cad/*.json` — CAD + printability records; `bom_s6lc.csv` — BOM line table.
- `evidence/architecture-rationale.md`, `evidence/printable-path.md`.

## Assumptions / evidence class

**CAD + CALCULATION over sourced FDM limits and sourced actuator ratings. No
part has been printed, purchased or measured** ([DND-27](/DND/issues/DND-27)).
The platen speed (20 mm/s), settle/return/reset overheads, and the lead-screw
efficiency are stated assumptions; break-evens are in `sensitivity()`.

## What passed / what failed

- Passed: all six gates (cell fit, banked release force, lift torque, timing,
  cost parts, cost delivered); sourced-FDM printability; watertight CAD.
- Honest limitation: mask preparation is **off the visible budget** (double
  buffering or pre-written media required for a known next map).

## Remaining uncertainty

Measurement-only under DND-27: as-printed pawl release-force spread (S1-D),
friction μ, pocket sharpness, pawl creep, platen flatness.

## Most informative next test (no print)

A CAD + mechanism-dynamics study of the **release-comb trip under a loaded
neighbour**, plus a release-force-spread sensitivity that finds the sd at which
the broadcast decode fails — owned by [DND-78](/DND/issues/DND-78) (Falsifier).

## Follow-ups created

- [DND-75](/DND/issues/DND-75) — InventorAlpha: divergent alternatives.
- [DND-76](/DND/issues/DND-76) — InventorBeta: divergent cell/mechanism primitives.
- [DND-77](/DND/issues/DND-77) — CostManufacturing: independent BOM ratification (blocked by DND-71).
- [DND-78](/DND/issues/DND-78) — Falsifier: adversarial audit (blocked by DND-71).

---

# DND-75 — InventorAlpha divergent ultra-low-cost machines

Added as a self-contained subdir `09-lowcost-alternative/divergent/` beside the
CTO's S6-LC. `08-current-design/` untouched.

## Engineering question

DND-72 proved S6-LC's fixed no-channel base ($218.70 parts → $253.69 delivered)
exceeds <$250 with zero actuators, and that trimming actuators cannot win. Can a
**materially different** machine delete the base's expensive lines instead?

## Result — three complete machines, all <$250 **and** <30 s

| | A1 single-shaft cam | A2 hand-crank + punched tape | A3 S1-B banked broadcast |
|---|---|---|---|
| Parts | $58.30 | $42.90 | $98.29 |
| **Delivered (×1.16)** | **$67.63** | **$49.76** | **$114.02** |
| + honest substitutes | $80.39 | $62.52 | $127.94 |
| Full map | 17.76 s | 26.86 s | 22.06 s |
| Bought motion actuators | 1 | 0 | 2 |

The lever is the **base**, not the actuators: the lines that exist only because
S5-R has a head, a multi-screw lift and a scanner axis total **$177.00**, leaving
a retained base of **$41.70**.

## Evidence produced

- `divergent/analysis/divergent_lowcost.py` — baseline decomposition, attack
  audit, three full machine allocations (ten jobs, BOM, timing, failure mode,
  cheapest killing test), summaries.
- `divergent/analysis/divergent_lowcost_checks.py` — **18/18 checks pass**.
- `divergent/scad/a1_cam_cell.scad` — printability **PASS**.
- `divergent/scad/a2a3_media_cell.scad` — printed features PASS, film thickness
  reported as an honest **MEDIA RISK**.
- New CI job `dnd75-divergent-lowcost`.

## What passed / what failed (honest)

- Passed: all three cost + timing gates, after paying for substitute lines.
- **Failed:** A1's single motor cannot carry bank + lift (needs 0.3302 Nm vs the
  0.30 Nm allowance); a 2nd/stronger motor keeps it under $250.
- **Corrected:** test11 prescribed 8 banks for S1-B; that is 38.9 s (fails 30 s).
  A3 uses **4 banks of 20 rows** (22.06 s, 592 N release < 1500 N).
- **Product limitation:** A2's tape write is off the visible budget (~85 min
  off-line at one needle); works only for known-ahead maps.

## Residual uncertainty / next test

- A1: real cam torque at the actual profile (friction, not full-rise arm).
- A2/A3: the punched-media cell is the first coupon worth printing — it retires
  the family's central unknown.
- Only unit cells are modelled; no full multi-row interference check.

See `07-evidence-and-decisions/dnd75-divergent-low-cost.md`.
