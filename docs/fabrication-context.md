# Fabrication context — Bambu Lab X1 Carbon

Research checked **27 September 2026**.

This project is expected to be prototyped primarily on a **Bambu Lab X1 Carbon
(X1C)**.

## Printer capabilities relevant to the project

Bambu Lab's current X1C specifications list:

- FDM/CoreXY printer;
- build volume: **256 × 256 × 256 mm**;
- included **0.4 mm hardened-steel nozzle**;
- optional **0.2, 0.6 and 0.8 mm** nozzles;
- all-metal hotend, up to **300 °C**;
- maximum toolhead speed **500 mm/s**;
- maximum toolhead acceleration **20 m/s²**;
- supported materials including PLA, PETG, TPU, ABS, ASA, PVA and PET;
- PA, PC and carbon/glass-fibre-reinforced polymers are explicitly within the
  X1C's intended advanced-material capability.

Bambu's X1-series hotend documentation describes the **0.2 mm nozzle** as the
high-fineness option for small/intricate models. Reinforced/particle-filled
filaments are restricted or discouraged with the 0.2 mm nozzle because of clog
and abrasion risk.

Sources:

- https://eu.store.bambulab.com/products/x1-carbon-3d-printer
- https://eu.store.bambulab.com/en/collections/consumables-x1-series/products/complete-hotend-assembly-x1-series

## Dimensional accuracy: do not confuse sensor resolution with part tolerance

Bambu advertises **7 µm lidar resolution**, but that is a sensor specification,
not a guarantee that an arbitrary FDM part will be dimensionally accurate to
7 µm.

The published X1C technical specifications cited above do **not** state a general
guaranteed dimensional tolerance for finished printed parts. Actual fit depends
on nozzle, filament, flow calibration, feature orientation, cooling, shrinkage,
wall count and the specific geometry.

Therefore:

- do not use a blanket ±0.05 mm or similar assumption merely because the printer
  is capable of fine motion/sensing;
- every sliding, rotating, snap or press-fit mechanism at the 5.08 mm pitch must
  have a calibration coupon before its clearance is treated as qualified;
- critical fits should be tested as a small clearance matrix rather than as one
  nominal CAD dimension;
- record nozzle, layer height, filament type/lot, orientation and any XY/hole
  compensation used for every mechanical test.

For the test08 geometry, a **0.20 mm wall is an experimental feature**, even when
using the 0.2 mm nozzle. Being nominally printable as one extrusion-width feature
does not establish yield, stiffness, straightness or repeatability across
thousands of parts.

## Project material baseline

The normal project material is **PLA**. Treat PLA as the baseline for geometry,
timing, mass and assembly experiments unless a test documents a reason to change.

Color is not a mechanical design requirement. Do not assume one PLA color is
stronger than another without material/batch data or a coupon test. Prefer
consistent material and lot for comparative measurements.

Other X1C-compatible materials may be introduced when they solve a measured
problem, for example wear, impact resistance, temperature, creep or compliant
features. A material change is an engineering variable and must be requalified
for friction, shrinkage, fit and printability.

For very fine 0.2 mm-nozzle geometry, avoid assuming carbon/glass-filled
filaments are available as a drop-in strength upgrade; Bambu's nozzle guidance
limits those combinations.

## Consequences for the full display

The ~400 mm active map cannot be printed as one monolithic X1C part because it is
larger than the 256 mm build volume. Full-scale structure should therefore be
modular.

This is compatible with the current test08 direction: small guide cartridges,
row modules or other replaceable tiles are preferred to one large printed frame.
Modularity also makes failed cells and wear parts serviceable.

Before scaling a mechanism to thousands of cells, require repeatable full-pitch
coupon batches printed on the actual X1C and PLA process intended for production.
