---
status: complete
builds-on: [E-028, DES-004, ADR-007, E-016, E-014, E-012]
---

# E-042: independent falsification of the E-028 loaded rotor/readback gate

## Verdict

**REJECTED for physical handoff; analytical geometry is only conditionally
supported.** No coupon was printed, assembled, measured, or cycled. The
repository checks reproduce nominal/tolerance arithmetic and synthetic result
fixtures only. They do not close any physical E-028 gate.

Two E-028 gates fail as currently specified, rather than merely lacking
confidence:

1. The claimed 10,000-transition schedule is not balanced. For a forward pass,
   `cell = k mod 25` and `state = k mod 5` assign each cell one fixed state
   (cell 0→0, …, cell 24→4). The stated next pass assigns each cell one fixed
   complementary state. Repetition therefore exercises at most one pair per
   cell, not all directed five-state transitions. It cannot substantiate the
   phrase “balanced directed schedule” or a 10,000 state-changing record.
2. The frozen coupon CAD contains no five hard stops, detent pockets, follower,
   or return element. `assembly()` contains only the frame and rotors; writer,
   reader, axle, retainer, and load are separate sample solids or prose. Thus
   stop reach/return and the 3.27 N load path are not reproducible from the
   article definition.

The cheapest decisive correction is a document/CAD repair before fabrication:
freeze either a stop/return/load/writer/reader fixture assembly with datums and
tolerances or explicitly add those functions to the coupon CAD; then generate
and machine-check records as `(cell, from_state, to_state)` with all 20
directed pairs represented. The Design Engineer owning E-028/LAB-107 is the
next owner; a fabricator/operator follows only after that repair.

## Gate disposition

| E-028 gate | Disposition | Falsifying evidence / gap |
|---|---|---|
| pre/post clearance | unresolved | CAD/tolerance only; no article or post-fit measurement |
| five-stop motion/return | **fail as defined** | CAD has no stop/detent/return mechanism; no reproducible stop datum |
| writer engagement | blocked | tongue and pocket are sample geometry, not an assembled stroke/force/pose |
| fixed-standoff reader | blocked | aperture/standoff are nominal; target registration, optical margin definition, and calibration are absent |
| 3.27 N loaded motion | **fail as defined** | force value is a design input; force application area, direction, fixture stiffness, and reaction path are not frozen |
| neighbour isolation | blocked | C3 is loaded, while edge/corner witnesses are specified unloaded; no loaded-neighbour datum/uncertainty is defined |
| timing | unresolved | event fields exist, but no performance threshold or synchronized fixture definition supports DES-004 timing |
| 10,000 smoke | **fail** | proposed schedule repeats fixed state assignments/pairs and does not emit a verifiable from-state schedule |
| post-fit condition | unresolved | no physical article or inspection evidence |

The nominal geometry screen remains a **calculated/CAD-derived conditional
pass**: 25.40 mm field span, 7.30 mm frame margin per side, 0.70 mm nominal
pocket-to-body radial allowance, 0.40 mm nominal axle/bore diametral
clearance, and 0.0546 mm assumed worst-case vane/frame margin. The last value
is tolerance-derived, not process capability. No sourced or measured result
supports fit, friction, return force, read discrimination, wear, or coupling.

## Reproducible checks

Run from repository root on 2026-10-07:

- `fit_calibration_matrix.py --plan`: **PASS**, 42 synthetic calibration rows
  listed. Its attempt counts (for example, five for a fit row) are not the
  E-028 counts and do not check E-028's 600 writer attempts, 1,500 reads, or
  10,000 transition records.
- `des004_rotor_coupon_fit_gate.py`: **PASS**, including nominal and assumed
  worst-case assertions and `logical_smoke(...)=10,000` with zero model errors.
  This is geometry/state-assignment calculation; it does not model stops,
  load, contact, optics, or hardware.
- `python3 -m unittest discover -s tools/fdm-critical-fit-calibration -p
  'test_*.py'`: **PASS**, 8 tests. Fixtures are synthetic and concern the
  E-016 calibration contract, not E-028 physical evidence.
- OpenSCAD frame export: **PASS**, but the rendered `assembly()` still has no
  stop/return, writer, reader target, retainer, or load fixture assembly.

Evidence classes are intentionally separated: sourced claims are limited to
repository inputs; calculated/CAD-derived claims are the checks above;
tolerance-derived claims use assumed +/- values; inferred claims are the gate
dispositions from missing/absent definitions; physical measurement and
hardware validation are **unresolved**.

## Research disposition

Retain this adverse result and the audited source as negative engineering knowledge. ADR-009 supersedes the former assignment to repair and fabricate this coupon. Any future mechanism must earn investigation through a distinct computational comparison; the missing geometry and defective schedule remain unresolved.

## Consolidated acceptance-contract corrections

The earlier contract review corrected the writer denominator to 30 attempts ×5 stops ×2 directions ×2 articles = **600**, not 300. A qualifying record would also require 1,500 identified reader observations, exactly 10,000 actual state-changing `(cell, from_state, to_state)` records with declared initial states and balanced directed-pair coverage, and separately counted no-ops. These are proposed test counts, not collected data or statistical life qualification.

The E-016 checker only checks its 42 calibration rows. It cannot validate E-028's loaded transitions, timing, 600 writer attempts or 1,500 reads. A dedicated acceptance contract must bind actual applied force and tolerance to calibrated raw traces; measure writer clearance in both axes at stated poses/datums; mathematically define reader margin and its calibration; identify loaded untouched neighbours, forces, directions, displacement datums and uncertainty; and reject missing/unscorable records. Geometric overlap, optical contrast and confidence are different quantities. Timing field completeness alone does not meet a performance limit.

The 3.27 N load, 0.10 mm neighbour displacement and 0.20 mm writer/reader margins are historical screening assumptions. They are not product requirements or sourced standards. Under ADR-009 this audit is retained negative knowledge; it does not commission another repair or physical coupon.
