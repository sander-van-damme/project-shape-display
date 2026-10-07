---
status: superseded
builds-on: [A-005, M-008, M-012, P-010, E-001, E-002]
---

Research disposition: retained executable comparison reference under ADR-009. Its former baseline priority is superseded; no automatic coupon or integration task follows.

Mechanism: 80×80 columns at 5.08 mm pitch; five passive rotary height stops, 40 mm travel. Common platen unloads columns. A four-row bank uses 40 writer solenoids and two motors to set dropout keepers on a shared rack. Hard stops carry terrain load without holding power.

Design point: 406.4 mm square active area; 20 bank groups; Ø6 mm steel drive rod; rack pitch 1.00 mm, tooth 0.50 mm. Keeper leaf 0.90 mm; hard shoulder carries hold load.

Calculation: full-map cycle 24.615 s. Purchased base $348.79; illustrative delivered uplift ×1.16 gives $404.60. Prices are historical estimates. No cell-level readback; reliability is unmeasured.

Source: `analysis/s5r_register.py` evaluates geometry, forces, timing, cost and residual sensitivities. `analysis/timing_basis.py` holds assumed motion inputs. `cad/` defines register and bank geometry. `fabrication/scad/` defines the complete printable part set and tiled assembly; `fabrication/tools/part_set.py` holds quantities and orientations. `bom.csv` holds purchased line items.

Reproduce locally: `python3 analysis/s5r_register.py`. Render parts with `python3 fabrication/tools/render_fab_parts.py`; then `python3 fabrication/tools/gen_manifests.py` regenerates print/assembly manifests. Run from this package directory. OpenSCAD and trimesh are required for rendering; numpy and Pillow for optional images. Generated meshes, images and manifests are disposable.

Evidence: CAD and calculation over assumptions and historical sourced listings. Geometry and analytic margins do not establish printability or service reliability.

Risks: keeper friction/creep/fatigue, loaded motor speed, writer repeatability and full-map failure probability require measurement. This package is retained as a reproducible design alternative, not a physically validated machine.
