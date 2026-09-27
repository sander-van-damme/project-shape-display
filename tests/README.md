# Test authoring guide

## Contract

Each new test is a self-contained, deterministic experiment named
`testNN_short_description`. It owns these four files:

| File | Responsibility |
| --- | --- |
| `params.yaml` | Human- and machine-readable inputs and acceptance limits |
| `model.py` | Parametric CadQuery geometry and CAD exports |
| `simulation.py` | Motion plan, backend selection, metrics and validation |
| `README.md` | Goal, procedure, assumptions and expected results |

Do not silently encode dimensions in Python. Add a named YAML field, state its
unit, validate it, and consume the same value from CAD and simulation. Generated
files go in `results/` and are ignored by Git.

## Procedure for people and agents

1. Find the next unused number in `docs/trial-inventory.md`.
2. Run `python scripts/new_test.py testNN_short_description`.
3. Update the copied README first: hypothesis, mechanism and pass criteria.
4. Edit `params.yaml`; keep all lengths in millimetres and times in seconds.
5. Run `model.py`, then `simulation.py --engine kinematic`.
6. If physics matters, repeat with `--engine mujoco` and/or `--engine pybullet`.
7. Inspect `results/final_state.svg` and `results/metrics.json`, then run pytest.

The `target_heights_mm` matrix is row-major and must exactly match the declared
grid. Every value must occur in `pin.height_steps_mm`. The baseline planner
resets all rows, then visits pins row-by-row with one plunger. Tests pass when
the final maximum height error is at most `validation.height_tolerance_mm` and
the predicted reconfiguration time does not exceed the configured limit.

## Engine choice

- **Kinematic:** dependency-light, deterministic planning oracle used by CI.
- **MuJoCo:** preferred contact/dynamics engine and straightforward pip install.
- **PyBullet:** lightweight alternative with useful interactive visualization.
- **PyChrono:** opt-in for flexible components and advanced multi-physics.

Backend adapters currently share the deterministic actuator trajectory so their
results are directly comparable. A test that relies on contact must extend its
adapter and document solver settings in its README.

## Reproducibility checklist

- Pin package versions in a dedicated requirements file when adding dependencies.
- Fix random seeds and record the seed in YAML.
- Never use wall-clock duration as the simulated motion time.
- Record units in key names and emitted metrics.
- Validate dimensions, collisions/clearance assumptions, locking state and final
  height error.
- Keep screenshots, video, CAD and metrics as CI artifacts rather than sources.
