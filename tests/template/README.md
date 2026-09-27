# Template — single-plunger staircase

## Goal

Reconfigure a 3×3 display to a staircase with one XY-Z plunger and verify final
height accuracy, locking, collision count, travel and total simulated time.
This directory is both an executable example and the source copied for new tests.

## Inputs and model

Edit `params.yaml`. It defines grid dimensions, cylindrical pin geometry,
allowed detent levels, actuator speeds, target heights and acceptance limits.
`model.py` reads the same file and builds a bored guide plate with a pin in every
cell. It writes STEP and STL files, which are expected CI artifacts.

## Run

From the repository root:

```bash
python -m pip install -r requirements-dev.txt
python tests/template/simulation.py --engine kinematic

# Optional CAD and physics tools
python -m pip install cadquery mujoco pybullet
python tests/template/model.py
python tests/template/simulation.py --engine mujoco
python tests/template/simulation.py --engine pybullet
```

For flexible rods or buckling studies, install PyChrono separately with
`conda install -c conda-forge pychrono` and create a documented adapter in the
new test. It is intentionally not a default CI dependency.

## Expected results

`results/metrics.json` is the machine-readable record and
`results/final_state.svg` is a headless-safe screenshot of the target/final
state. The command exits non-zero when height or time limits fail. The template
should report nine locked pins, no collisions, exact discrete heights, and a
reconfiguration time below eight seconds.

When copying this template, replace this goal and record the hypothesis,
physical assumptions, engine-specific behavior and expected numeric bounds.
