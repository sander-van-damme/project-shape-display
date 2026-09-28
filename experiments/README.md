# Experiment authoring guide

## What a test is for

A test is an engineering experiment that helps decide how to build the D&D
battle-map shape display described in [`../project-scope/design-target.md`](../project-scope/design-target.md).
Tests are the **evidence layer** for the [mechanical knowledge base](../engineering-knowledge/README.md);
a completed experiment should feed durable conclusions back into the relevant
mechanism, principle or architecture card.

The repository currently contains a Python/CadQuery/simulation framework, but
**that framework is a suggestion, not a contract**. Future tests are explicitly
allowed to break its APIs, replace it, or ignore it when another approach gives
better evidence.

A useful test should make the following clear regardless of implementation:

- the engineering question or hypothesis;
- the mechanism or idea being evaluated;
- relevant dimensions, assumptions, and constraints;
- how to run, build, measure, or inspect it;
- the evidence/output it produces;
- the conclusion or pass/fail criteria, when appropriate;
- how the result relates to the full D&D battle-map target.

Use the sortable `testNN_<domain>_<mechanism-or-question>` directory naming
convention for new experiments. The number preserves chronology; the remaining
name should explain what engineering family is being tested.

Examples:
- `test10_planar_memory_punched_height_plates`
- `test11_planar_memory_reprogrammable_apertures`
- `test12_shared_power_clutch_bus`

Avoid names such as `testNN_validation` or `testNN_testXX_validation` when a
mechanism/domain name can say what the experiment actually contains. Historical
directory paths stay unchanged so old evidence and links remain reproducible.

## Suggested reference framework

For many software-driven experiments, the existing template is a convenient
starting point:

| Suggested file | Purpose |
| --- | --- |
| `params.yaml` | Human- and machine-readable dimensions, inputs, and limits |
| `model.py` | Parametric CadQuery geometry and CAD exports |
| `simulation.py` | Motion plan, backend selection, metrics, and validation |
| `README.md` | Goal, procedure, assumptions, evidence, and expected results |

Create a copy with:

```bash
python tools/new_experiment.py test08_my_experiment
```

The helper script and four-file layout are conveniences. They are not mandatory.
A new experiment may instead use OpenSCAD, another CAD tool, another language, a
different simulator, physical test data, or a completely different directory
structure.

### Current reference engines

- **Kinematic:** dependency-light deterministic planning oracle used by CI.
- **MuJoCo:** optional rigid-body/contact backend.
- **PyBullet:** optional lightweight rigid-body alternative.
- **PyChrono:** optional candidate for flexible components, cables, buckling, or
  multi-physics studies.

These are proposed tools, not the approved list of tools. If another engine or
method answers the engineering question more credibly, use it and document why.

## API compatibility is not a goal

There is no promise of a stable test API.

A future test may rename fields, replace YAML, change units with clear
documentation, restructure outputs, use another language, or introduce a new
simulation/control architecture. Breaking changes are acceptable when they make
the experiment clearer, more accurate, easier to reproduce, or more useful.

Do not keep a poor abstraction because an older template expects it.

The current CI only verifies the maintained reference framework. An alternative
test does not automatically need to plug into that CI; add appropriate checks
when they provide value.

## Project-level constraints to carry into tests

When relevant, evaluate against the full product target:

- approximately **400 mm × 400 mm** active tabletop area;
- about **5.08 mm or finer pitch** to resolve a ~1/5-square wall on a 1-inch
  D&D grid;
- square/rectangular moving columns rather than circular pins;
- usable vertical travel of at least one representative D&D miniature height;
- a complete full-scale map change that becomes playable in **less than 30
  seconds**, including per-map reset, positioning, actuation, and settling;
- purchased component cost ideally **< $200**, acceptable at **$200–$400**,
  last-resort at **$400–$500**, and unacceptable **> $500**;
- no design cost ceiling for 3D-printed parts.

Small experiments do not have to meet these values directly, but should explain
how their mechanism is expected to scale toward them when scale is relevant.

## Reproducibility guidance

Use the parts that make sense for the experiment:

- keep important dimensions and assumptions explicit rather than hidden in code;
- record units;
- fix random seeds for stochastic simulations;
- pin dependency versions when dependency drift would affect results;
- distinguish simulated time from wall-clock runtime;
- save machine-readable metrics when useful;
- keep generated screenshots, videos, CAD, and metrics as reproducible artifacts
  rather than source files where practical;
- document physical measurements and test setup when the experiment is hardware
  based.

## Test catalog and human-readable names

| Test | Domain / working name | Main question |
|---|---|---|
| `test00_pneumatic_multiplexer` | Pneumatics — matrix multiplexer | Can shared air routing replace per-cell actuation? |
| `test01_threaded_rods` | Screw memory — threaded rods | Can passive screw position store height? |
| `test02_python_cubes` | Geometry — cube clearance | What basic spacing/tiling geometry is viable? |
| `test03_threaded_rod_actuator` | Screw drive — compact actuator | Can the threaded actuator fit the pitch? |
| `test04_plain_cubes` | Sliding columns — plain guide grid | Can square columns tile and slide cleanly? |
| `test05_grid_cubes_rod` | Screw/grid — guided rod variant | Can the screw concept approach target density? |
| `test06_sandwich_detent` | Passive memory — sandwich detent | Can discrete detents hold useful heights? |
| `test07_5x5_grid` | Shared actuation — 5×5 row-comb grid | Does the shared row concept scale beyond one cell? |
| `test08_architecture_search` | Architecture search — rotary stepped stop | Which architecture survives full-scale timing/cost screening? |
| `test09_test08_validation` | Rotary-stop validation — X1C/coupling/structure | Which Test08 assumptions survive falsifiable checks? |

Future tests should keep this same pattern: **domain first, specific mechanism or
question second**.

## Legacy tests

The [Test09 validation workflow](test09_test08_validation/README.md) follows
Test08 without altering its evidence. Run `python experiments/test09_test08_validation/run.py`
for deterministic analytical checks, or add `--render` for OpenSCAD coupon
exports and scoped CAD checks. Physical records remain blank until measured.

The [test08 architecture search](test08_architecture_search/README.md) is a
full-scale analytical/CAD investigation with its own reproduction commands,
cost model and physical-test gates. It intentionally does not use the template's
ideal kinematic lock assumptions.

`test00_...` through `test07_...` are preserved legacy experiments. They do
**not** need to be migrated to the suggested reference framework. Each legacy
directory contains its own README notice so this status is visible where the
historical files are being inspected.
