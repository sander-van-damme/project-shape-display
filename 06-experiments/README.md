# 06 — Experiments

Experiments are the evidence layer of the Shape Display project. They answer specific engineering questions with calculation, simulation, CAD, fabrication or physical measurement.

Every experiment should make clear:

- the hypothesis or engineering question;
- the relevant design criteria from [`02-design-criteria/`](../02-design-criteria/);
- what was built, calculated, simulated or measured;
- the assumptions and limits of the evidence;
- the result and what it changes in stages 03–05;
- the cheapest next experiment if an important uncertainty remains.

## Current experiment line

| Test | Purpose | Status |
|---|---|---|
| [`test08_architecture_search/`](test08_architecture_search/) | Full-scale architecture screening, especially rotary stepped stops and shared programming | Analytical/CAD evidence; no product-qualified architecture |
| [`test09_test08_validation/`](test09_test08_validation/) | Falsifiable validation of Test08 assumptions, sourcing, structure, coupling and physical gates | Active validation; physical gates remain unverified |
| [`test10_broad_architecture_screen/`](test10_broad_architecture_screen/) | Mechanism-neutral full-scale count, information, timing and selector-cost bounds | Reproducible calculation; no physical validation |
| [`test11_shared_drive_gate_analysis/`](test11_shared_drive_gate_analysis/) | Concrete S3/S4 shared-drive machines, ordered rejection tests, S5 gate status | Calculated system models + unrendered CAD coupon; no printing or measurement |

Test08 and Test09 contain the current quantitative engineering line. Their code, parameters, BOMs, CAD and measurement files remain separate because they are reproducible evidence rather than narrative documentation. Test11 adds the shared-drive family (S3/S4) and the S5 gate list as calculated evidence.

## Legacy experiments

[`legacy/`](legacy/) preserves Test00–Test07 exactly as historical engineering evidence. These experiments remain useful for understanding ideas already tried, but they predate the current workflow and should not be treated as the active architecture.

| Test | Main question |
|---|---|
| `test00_pneumatic_multiplexer` | Can shared air routing replace per-cell actuation? |
| `test01_threaded_rods` | Can passive screw position store height? |
| `test02_python_cubes` | What basic spacing and tiling geometry is viable? |
| `test03_threaded_rod_actuator` | Can a compact threaded actuator fit the pitch? |
| `test04_plain_cubes` | Can square columns tile and slide cleanly? |
| `test05_grid_cubes_rod` | Can the screw/grid concept approach target density? |
| `test06_sandwich_detent` | Can discrete detents passively hold useful heights? |
| `test07_5x5_grid` | Does shared row actuation scale beyond one cell? |

## Reproducing the current analytical checks

From the repository root with Python 3.11+:

```bash
python 06-experiments/test08_architecture_search/checks.py
python 06-experiments/test09_test08_validation/run.py
python 06-experiments/test10_broad_architecture_screen/checks.py
python 06-experiments/test11_shared_drive_gate_analysis/checks.py
python 06-experiments/test11_shared_drive_gate_analysis/coupon_geometry.py
```

All four baseline workflows use the Python standard library. Optional CAD/rendering steps documented inside the experiment READMEs may require additional tools such as OpenSCAD.

## Project-level gates

When relevant, experiments should evaluate against the full product target: roughly 400 × 400 mm active area, ~5.08 mm pitch, ~6,400 cells, at least 40 mm usable travel, a playable full-map update in under 30 seconds, regional updates without disturbing unrelated terrain, low purchased-component cost, and reliable tabletop load support.

A small prototype does not need to satisfy every full-scale target, but it must state what it tests and what remains extrapolated.
