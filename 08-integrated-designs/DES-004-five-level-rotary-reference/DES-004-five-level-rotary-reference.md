---
status: superseded
builds-on: [DES-003, A-005, M-012]
---
# DES-004: five-level rotary reference

Historical hypothesis: one passive stepped rotor/follower per visible column, a shared writer and fixed-height coded reader, local state changes and bounded retry. The intended terrain levels are 0/10/20/30/40 mm at 5.08 mm pitch.

**The executable CAD does not implement the five-height support mechanism.** It contains rotor body, pocket, axle hole, coded vane and sample writer/reader geometry. E-042 rejects its stop/return/load-path handoff and transition schedule. “Verified successor” was an unsupported identity and has been removed. This is a retained comparison package under ADR-009, not a selected product design or fabrication handoff.

Historical timing uses eight heads, four detent increments at 2 ms plus 1 ms settling, giving an 8.2 s write pass and 19.9612 s total. At 5 ms/detent the total is 29.5612 s; combining that dwell with 5% assumed misses gives about 34.95 s. These are sensitivity calculations with assumed motion/retry, not measurements or a supported actuator schedule.

`bom_des004.csv` records the $370 inherited baseline plus 6,400 metal axle pins: $498 nominal or $729 conservative. These allowances exclude printed burden and do not prove component availability. E-013 retains the axle sourcing/fit screen. The old claim that no purchased item scales with cell count is false for this BOM.

The 5×5 coupon's pocket radius was increased from 1.70 to 2.20 mm to clear the coded vane (outer-corner radius about 2.016 mm). E-012 retains the nominal and assumed tolerance screen, including about 0.0546 mm worst-case vane margin and 0.30 mm worst-case axle/bore diametral clearance. Actual process distributions remain unresolved. The former separate coupon wrapper duplicated this source and E-012.

Retained source: `cad/des004_rotor_coupon_5x5.scad`, `analysis/des004_rotor_coupon_fit_gate.py`, `analysis/five_level_successor_bound.py`, `analysis/independent_falsification_bound.py`, and the BOM. Run the analysis scripts from the repository root. A successful scalar checker or logical smoke does not supply missing geometry or physical evidence.

Reopen only with a materially useful mechanism and a full-system comparison under the mission. Model actual height stops, transitions, support and load path before interpreting force, timing, tolerance or readback claims. Physical validation remains absent.
