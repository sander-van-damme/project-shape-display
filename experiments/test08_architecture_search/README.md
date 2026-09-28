# Test 08 — full-scale architecture search and programmed rotary stops

**Outcome: no product-qualified architecture.** Strongest next experiment:
passive five-level stepped cams, an 80-channel PM-stepper programming head and
a common lifting platen. Full-scale timing is conditionally 26.25 s; the working
purchased BOM is $432, or $518.40 with 20% contingency. Return friction, reliable
angular memory, head coupling, structural support and sourcing remain gates.

Start with the [engineering report](../../research/architecture-investigation-2026-09.md).
Other evidence:

- [Architecture families and rejection/iteration log](architectures.md)
- [Historical audit](history.md) and [external source ledger](sources.md)
- [Configuration](params.json) and [purchased BOM allowances](bom.csv)
- [Smallest physical prototype and decision criteria](prototype.md)

## Reproduce

From repository root, Python 3.11+, standard library only for analysis/checks:

```text
python experiments/test08_architecture_search/analysis.py
python experiments/test08_architecture_search/checks.py
```

Optional variable-section cam buckling screen (tested with NumPy 1.26.3):

```text
python -m pip install numpy==1.26.3
python experiments/test08_architecture_search/cam_strength.py
python experiments/test08_architecture_search/cam_strength.py --core-radius 0.45
```

This solver checks itself against the closed-form uniform cantilever result and
records cross-section and element-count convergence. It is a structural screen,
not a material qualification or rated load. Output is `results/cam_strength.json`;
the override preserves a separate file documenting the rejected thin-core case.

Optional report figure: `python experiments/test08_architecture_search/plots.py`
(matplotlib 3.8.2). It writes `results/engineering_summary.png` and `.svg` from
the current metrics and sensitivity sweep, without another simulation.

For actual parametric CSG/STL exports and scoped interference checks, install/use
OpenSCAD (tested with the installed Windows command-line program):

```text
python experiments/test08_architecture_search/cad_check.py --render
```

The CAD command can take several minutes. It fails on compiler warnings, errors,
missing exports or nonempty interference solids. It queries five supported
states and twenty raised rotation angles. Continuous radial clearance is also
bounded analytically. It does not check the omitted head/frame/retention system.

`params.json` is the dimensional source; `analysis.py` emits
`results/parameters.scad` for `coupon.scad`. Run analysis before opening the SCAD
file. `part` selects rotor, follower, follower_guide, body_guide, lift_plate,
assembly or section. The baseline coupon is 3×2, at final horizontal pitch.
Its fixture, detent spring and drive head are not an assembled print-ready kit.
Upper guide heights derive from body length; follower-guide and lift coordinates
implement the 40 mm baseline. A different stroke requires updating and validating
the whole stack, not just `travel_mm`.

## Generated evidence

All generated files stay in ignored `results/` and are reproducible:

- `metrics.json`: configuration hash, timing, force, geometry, mass variants,
  cost and reliability bounds. There is deliberately no blanket mechanical pass.
- `worst_schedule.json`: complete ordered events, including reset and every home.
- `timing_sweep.csv`: 48 combinations of head count, motor rate and coupling time.
- `timing.svg`: six full-map cases with the 30 s boundary.
- `parameters.scad`, `assembly.csg`, five part STLs, `cad_checks.json` and three
  PNG renders after the CAD command.

The independent unit checks validate acceleration formulas, all-cell coverage,
adversarial maps, partial-width head groups, invalid height encoding and known
mechanical/cost failures. Historical files and the template are unchanged.

## Important interpretation

This is an analytical/event model plus real solid geometry, not rigid-body
physics. Height support and successful detent seating are conditional states.
No ideal-lock flags or zero-collision constants are offered as measurements.
The initial unsupported follower failed its load screen; initial full-width
guides had zero wall thickness; the first short follower guide lost contact at
full extension; nine cam levels fail angular clearance; a
40-channel head fails full-map timing. Those failures informed the revised
candidate rather than being hidden by a pleasing render.

The 40 mm stroke has not been checked against a measured named miniature. No
physical measurements, completed procurement, printed prototype or lifetime
validation are claimed.
