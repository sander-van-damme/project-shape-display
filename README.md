<!-- © 2024 Sander Van Damme - All Rights Reserved. -->

# D&D battle-map shape display

This repository explores a tabletop shape display whose primary goal is to become
a physical **Dungeons & Dragons battle map**. The intended surface is a dense grid
of independently height-adjustable **square or rectangular columns** that can
turn terrain, walls, platforms, stairs, pits, and other map features into physical
relief while leaving a usable surface for miniatures.

The repository is deliberately experimental. Historical trials are preserved
below `tests/`, and future experiments are free to use different mechanisms,
languages, CAD systems, simulators, APIs, or folder layouts when that produces a
better engineering result.

## Product target

The engineering target is defined in more detail in
[`docs/design-target.md`](docs/design-target.md). The most important constraints
are:

- **Use case:** a real tabletop D&D battle map, not a generic demo display.
- **Active footprint:** approximately **400 mm × 400 mm**, so it fits naturally
  on a table while still providing a useful encounter area.
- **Map-scale resolution:** use the common **1-inch (25.4 mm) battle-map square**
  as the reference grid. A feature such as a wall should be representable at
  roughly **one-fifth of a square**, so the full-scale target pitch is about
  **5.08 mm or finer**.
- **Scale implication:** a 400 mm side at about 5.08 mm pitch implies roughly
  **79–80 columns per axis**, or about **6,200–6,400 independently height-adjustable
  elements** at full target resolution.
- **Element shape:** the target display elements are **square/rectangular
  columns**, not round pins. Legacy files may still use the word `pin`.
- **Vertical travel:** the display should cover at least the full height of a
  typical D&D miniature so meaningful terrain and elevation differences can be
  represented. Tests that validate this should state the reference miniature
  and measured height they use.
- **Cost:** 3D-printed parts are not subject to a design cost ceiling. The cost
  limits below apply to purchased/non-3D-printed components such as electronics,
  motors, bearings, rods, sensors, PCBs, power supplies, and similar hardware:
  - **under $200:** ideal;
  - **$200–$400:** acceptable;
  - **$400–$500:** last-resort / absolute-limit territory;
  - **over $500:** unacceptable.

Smaller prototypes are useful, but they should be evaluated by whether their
mechanism can plausibly scale toward these battle-map requirements.

## Testing philosophy

The current Python/CadQuery/simulation setup is a **recommended reference
workflow, not a project constraint**. It exists because it is useful for quick,
repeatable experiments and CI, not because future work must preserve it.

A future test may:

- break the current Python API;
- use a completely different programming language;
- use OpenSCAD, FreeCAD, custom scripts, spreadsheets, physical measurements, or
  another CAD/simulation approach;
- replace the current simulation stack;
- use a different file layout;
- add its own CI or no CI when that is not useful.

What matters is that the experiment clearly states the question it is answering,
documents important assumptions and dimensions, produces inspectable evidence,
and records enough information for someone else to understand or reproduce the
result. Do not keep a weaker approach merely to stay compatible with the current
framework.

See [`tests/README.md`](tests/README.md) for the suggested workflow and the
expectations that apply regardless of implementation.

## Suggested reference workflow

For experiments where the existing stack is useful, the repository includes a
Python 3.11 + PyYAML + CadQuery reference template with a deterministic simulator
and optional MuJoCo/PyBullet backends:

```bash
python scripts/new_test.py test08_my_experiment
python -m pip install -r requirements-dev.txt
$EDITOR tests/test08_my_experiment/params.yaml
python tests/test08_my_experiment/model.py
python tests/test08_my_experiment/simulation.py
```

Useful commands for the reference template:

```bash
# Fast deterministic checks used by the current CI
python -m pytest

# Dependency-light baseline simulation
python tests/template/simulation.py --engine kinematic

# Optional rigid-body backends
python -m pip install mujoco pybullet
python tests/template/simulation.py --engine mujoco
python tests/template/simulation.py --engine pybullet

# Optional parametric CAD export
python -m pip install cadquery
python tests/template/model.py
```

PyChrono can still be useful for flexible bodies, cables, buckling, or FEA. It is
not a required project dependency.

Generated outputs such as simulation metrics, screenshots, and CAD exports can
live in `results/` and remain unversioned when they are reproducible.

## Copyright

© 2024-2026 Sander Van Damme - All Rights Reserved.
