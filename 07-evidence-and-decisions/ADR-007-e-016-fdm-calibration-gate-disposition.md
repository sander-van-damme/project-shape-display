---
status: superseded
builds-on: [E-016, Q-009, DES-004]
---
# ADR-007: retained FDM calibration contract

Historical decision: E-016 defines a 42-row rotor/writer/reader matrix and synthetic result checker, not completed physical calibration. The earlier instruction to proceed directly to fabrication is superseded by ADR-009.

The matrix spans pocket radii 2.10/2.20/2.30 mm, bores 1.20/1.40/1.60 mm for a 1.00 mm pin, two locations and two orientations (36 rows), three writer-clearance witnesses and three reader-offset witnesses. `tools/fdm-critical-fit-calibration/` retains the executable source. Process metadata and actual observations are required for physical interpretation; synthetic fixtures establish only checker behavior.

The assumed 3.27 N load, writer/reader margins and proposed observation counts need an applicable mechanism and explicit definitions before use. E-042 identifies the missing rotor stop/return/load path and the separate E-028 contract defects. Passing this calibration checker cannot close those gates or establish board reliability.

Under the mission, first identify the manufacturing/model uncertainty that changes a design decision, then adapt a targeted calibration if needed. FDM spread, friction, fit yield, anisotropy, creep, wear and reader behavior remain unmeasured here. Preserve raw failures and provenance when measurements eventually exist.
