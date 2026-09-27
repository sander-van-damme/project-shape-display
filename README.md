<!-- © 2024 Sander Van Damme - All Rights Reserved. -->

# Shape-display test platform

This repository is a repeatable research platform for a pin-based shape display.
Every experiment lives below `tests/`, with its design sources, settings and
instructions kept together. The original prototypes were retained and renamed
systematically; see [`docs/trial-inventory.md`](docs/trial-inventory.md) for the
migration map and known gaps in older experiments.

## Start a new test

Requirements are Python 3.11+, PyYAML, and (depending on the task) CadQuery and
a simulation engine. Create tests from the maintained template rather than from
an older prototype:

```bash
python scripts/new_test.py test08_my_experiment
python -m pip install -r requirements-dev.txt
$EDITOR tests/test08_my_experiment/params.yaml
python tests/test08_my_experiment/model.py
python tests/test08_my_experiment/simulation.py
```

Names must match `testNN_short_description`; never reuse a number. Commit source
and parameters, but not generated `results/` files. A test directory should
contain `params.yaml`, `model.py`, `simulation.py`, and a `README.md`. Legacy
tests are documented exceptions until they are converted as they are revisited.

## Commands

```bash
# Fast deterministic checks (also run in CI)
python -m pytest

# Baseline simulation without a native physics package
python tests/template/simulation.py --engine kinematic

# Optional rigid-body backends
python -m pip install mujoco pybullet
python tests/template/simulation.py --engine mujoco
python tests/template/simulation.py --engine pybullet

# Export the parametric CAD assembly (STEP and STL)
python -m pip install cadquery
python tests/template/model.py
```

MuJoCo and PyBullet are the supported rigid-body candidates. Use PyChrono only
for tests needing flexible bodies, cables, buckling, or FEA; its recommended
installation is `conda install -c conda-forge pychrono`. Backend selection is
explicit in `params.yaml`, so the input remains reproducible.

## Outputs and CI

The simulation validates its height map and writes `results/metrics.json` plus
an SVG final-state preview. Metrics include elapsed motion time, travel, energy
estimate, error and pass/fail status. `.github/workflows/ci.yml` checks the
template, runs unit tests, and uploads results as a pull-request artifact.
Native MuJoCo and PyBullet smoke jobs exercise the optional adapters.

Generated artifacts are intentionally not versioned. A future Pages deployment
can publish the uploaded `results/` directory without mixing generated files
with test definitions.

## Test patterns

Useful deterministic scenarios include:

1. **Flat:** every target is zero; validates reset and release behavior.
2. **Staircase:** columns use successive discrete levels; validates travel and
   timing (the template demonstrates this case).
3. **Structured relief:** a checked or concentric map with an explicit seed if
   any generator is used; validates frequent neighboring height changes.

See [`tests/README.md`](tests/README.md) for the schema, workflow, expected
files, acceptance rules, and guidance for agents.

## Copyright

© 2024 Sander Van Damme - All Rights Reserved. See the repository history for
the original notice.
