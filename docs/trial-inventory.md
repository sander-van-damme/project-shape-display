# Legacy trial inventory

The September 2026 repository migration retained every tracked source and asset
and assigned stable, sortable test names. Older trials predate the four-file
test contract and are preserved as historical design evidence rather than made
to look reproducible retroactively.

| Former path | Current path | Contents / purpose | Contract status |
| --- | --- | --- | --- |
| `trial-0-pneumatic-multiplexer` | `tests/test00_pneumatic_multiplexer` | SolidPython pneumatic multiplexer and renders | Legacy |
| `trial-1-threaded-rods` | `tests/test01_threaded_rods` | OpenSCAD threaded rod/cube revisions | Legacy |
| `trial-2-overcomplicating-cubes-in-python` | `tests/test02_python_cubes` | Python/SolidPython cube experiment | Legacy |
| `trial-3-new-threaded-rods` | `tests/test03_threaded_rod_actuator` | OpenSCAD actuator, frame and calibration parts | Legacy |
| `trial-4-plain-old-cubes` | `tests/test04_plain_cubes` | Simple cube/frame and design documents | Legacy |
| `trial-5-grid-and-cubes-and-rod` | `tests/test05_grid_cubes_rod` | OpenSCAD grid, cube and actuator iteration | Legacy |
| `trial-6-claude-sandwich` | `tests/test06_sandwich_detent` | Sandwich detent sources, STLs and images | Legacy |
| `trial-7-5x5-grid` | `tests/test07_5x5_grid` | Parametric 5x5 detent grid and caddy | Legacy |
| n/a | `tests/template` | Maintained CadQuery/simulation reference | Current |

When revisiting a legacy test, add parameters and validation rather than
altering its original design intent. New work starts at `test08_…`.
