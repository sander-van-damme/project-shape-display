---
status: superseded
builds-on: [A-001, M-004, M-014, P-006, E-002]
---

Research disposition: retained executable comparison reference under ADR-009. Its former baseline priority is superseded; no automatic coupon or integration task follows.

Mechanism: 80×80 five-level rack columns at 5.08 mm pitch. A passive mask selects engagement during global broadcast lift strokes. Reset is banked into eight groups of ten rows. Three purchased motor axes replace the register's solenoid bank.

Calculation: 11.96 s visible display transition excludes physical mask generation/handling. Arbitrary-map sustained cycle remains unproven. Full-board lift loads 6,400 cells, requiring NEMA23-class lift sizing; banked reset bounds release load to 800 cells.

Cost: historical estimate $226.77 purchased; ×1.16 illustrative delivery allowance gives $263.05. Purchased cost clears $250; delivered cost exceeds $250. Printed parts excluded. Prices and capabilities require rechecking before purchase.

Source: `analysis/s6lc.py` evaluates mechanism, whole-board lift, bank reset, cycle, cost and reliability. `scad/s6lc_machine.scad` defines the machine geometry. `bom_s6lc.csv` holds purchased lines. CAD represents a concept, not a complete production drawing set.

Reproduce: `python3 analysis/s6lc.py`; regression checks `python3 analysis/s6lc_checks.py`. Optional `analysis/render_s6lc_cad.py` requires OpenSCAD and trimesh; image rendering requires numpy and Pillow. Printability calculations use root `tools/fdm-limits/fdm_process_limits.py`.

Evidence: CAD/calculation only. Risks: mask fabrication and alignment, release-force variation, loaded-neighbour motion, pawl wear, silent wrong cells and array-scale assembly yield. No readback mechanism establishes full-map correctness.
