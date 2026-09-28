# Template — single-plunger staircase

## Goal

Reconfigure a 3×3 display to a staircase with one XY-Z plunger and verify final
height accuracy, locking, collision count, travel and total simulated time.

This directory is a **reference example**, not a required architecture. It is
also the source copied when `90-tools/new_experiment.py` is used. Future tests may use
different code, APIs, languages, CAD tools, simulation methods, or file layouts.

## Inputs and model

Edit `params.yaml`. It defines grid dimensions, **square column** geometry,
allowed detent levels, actuator speeds, target heights and acceptance limits.
`model.py` reads the same file and builds a guide plate with a square moving
column in every cell. It writes STEP and STL files, which can be kept as
generated artifacts.

The square-column geometry reflects the target battle-map surface. Legacy tests
may still call these elements pins.

## Run

From the repository root:

```bash
python -m pip install -r requirements-dev.txt
python 06-experiments/template/simulation.py --engine kinematic

# Optional CAD and physics tools
python -m pip install cadquery mujoco pybullet
python 06-experiments/template/model.py
python 06-experiments/template/simulation.py --engine mujoco
python 06-experiments/template/simulation.py --engine pybullet
```

For flexible rods or buckling studies, PyChrono is another possible tool. It is
not a required project dependency, and neither are the other engines listed
above.

## Expected results

`results/metrics.json` is the machine-readable record and
`results/final_state.svg` is a headless-safe preview of the target/final state.
The command exits non-zero when height or time limits fail. The template should
report nine locked columns, no collisions, exact discrete heights, and a
reconfiguration time below eight seconds.

The eight-second limit is specific to this tiny 3×3 reference scenario; it is
not the product-level timing target. Experiments that evaluate an actuation or
map-update architecture should separately measure or estimate full-scale
end-to-end map reconfiguration against the project target of **less than 30
seconds** documented in `02-design-criteria/design-target.md`.

When copying this template, replace this goal and record the hypothesis,
physical assumptions, engine-specific behavior and expected numeric bounds.
