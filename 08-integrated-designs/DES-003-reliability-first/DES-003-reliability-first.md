---
status: candidate
builds-on: [M-003, P-006, Q-006, E-002]
---
Mechanism: binary hard-stop latch columns at 5.08 mm pitch. Parallel gantry writer heads toggle cells; a reader pass verifies state and permits retry. A frame-fixed reflective vane avoids state-dependent optical standoff. A latch-linked matte shutter encodes the state at that fixed target.

Calculation: eight heads minimum at the assumed 1.0 m/s traverse; writer/read rate 71–228 cells/s/head. Nominal full cycle 18.278 s includes reset, traverse ramps, write, verification and settling. Four-head designs do not reliably clear 30 s. Regional updates isolate local tiles geometrically; elastic disturbance remains unmeasured.

Optical design point: target z=43 mm; standoff 1.8 mm; spot 1.405 mm; neighbour clearance 0.353 mm. Assumed reflectances produce 7.72× on/off return. These are model outputs, not measured detection performance.

Cost: historical base estimate $181 purchased / $209.96 with ×1.16 delivery uplift. The CSV and architecture screen retain provisional head/axis allowances; reconcile the eight-head implementation and complete purchased BOM before procurement. Binary height capability must be evaluated against the product's preferred terrain levels.

Source: `analysis/reliability_mask.py` models architecture comparisons; `a1_writer_rate.py` models writer/reader rates and optical geometry; `a1_regional_update.py` models local isolation; `a1_promotion_timing.py`, `a1_promotion_cost.py`, `a1_hardening.py` expose conservative sensitivities. `scad/` contains latch, reader and prototype coupons. `bom_a1.csv` holds the base BOM.

Reproduce: `python3 analysis/reliability_mask.py convergence`; `python3 analysis/reliability_mask_checks.py`. Render via `python3 analysis/render_a1_cad.py` with OpenSCAD and trimesh. Numeric analyses use Python standard library and the reusable FDM process limits.

Evidence: CAD/calculation and explicit assumptions. Readback can expose failures only if reader classification works in practice. Latch toggle force, reflectance/lighting, gantry registration, wear and loaded-neighbour disturbance need coupon measurements. No physical validation or print-ready claim.
