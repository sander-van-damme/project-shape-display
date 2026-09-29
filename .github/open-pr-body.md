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
