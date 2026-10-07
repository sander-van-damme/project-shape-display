---
status: active
builds-on: [E-016, Q-009, DES-004, DES-005]
---

# ADR-007: E-016 FDM calibration gate disposition

## Decision

Close E-016 as an analytical definition and retain DES-004/DES-005 as
candidate designs. Do not promote either design to a reproducible-print or
production pass: the gate is blocked on future physical measurements.

## Reproducible matrix

The controlled coupon is the existing 5x5, 5.08 mm-pitch frame with centre
and boundary locations. The independent sweeps are:

| Interface | Levels | Planned evidence |
|---|---|---|
| Rotor pocket radius | 2.10, 2.20, 2.30 mm | 36 rotor rows: 3 pocket × 3 bore × 2 locations × 2 orientations |
| Rotor bore for 1.00 mm pin | 1.20, 1.40, 1.60 mm | F functional and A adverse orientation |
| Writer pocket-minus-tongue clearance | 0.20, 0.40, 0.60 mm/axis | 3 witness rows, 30 engagements each |
| Reader target offset | 0.00, -0.20, +0.20 mm | 3 witness rows, 150 reads each |

The plan therefore contains 42 rows. The executable plan and result contract
are in `06-experiments/E-016-des-004-des-005-fdm-critical-fit-calibration-matrix/`.
Every physical result must identify printer/nozzle/layer/filament lot,
slicer profile hash, XY and elephant-foot compensation, orientation and part
ID. Dimensions are measured at three clock positions after 30 minutes at room
temperature; loaded rotor work uses the 3.27 N service load.

## Acceptance gate

A row passes only when all five stops reach and return without binding or
neighbour contact, measured post-fit diametral clearance is at least 0.10 mm,
writer clearance is at least 0.20 mm in both axes, writer engagement is 30/30,
reader result is 150/150 with at least 0.20 mm reader margin, and the loaded
3.27 N result passes. The checker requires the full 42 planned identities,
declared attempt counts, process metadata, three clock positions, stop/load
evidence, and measured min/mean/max/range summaries. Missing or unresolved
physical evidence is a rejection of the result record, not a pass.

## Evidence classification

Calculated/CAD: the 42-row enumeration, 2.20 mm pocket repair, nominal
0.1046 mm vane/frame clearance, assumed worst-case 0.0546 mm vane/frame
clearance, and nominal 0.40 mm axle/bore clearance are reproducible arithmetic
and geometry checks. Contract tests and synthetic fixtures test the checker;
they are not printed parts or measurements.

Unresolved: FDM dimensional spread, actual pin tolerance, fit yield, friction,
loaded rotation/return, reader registration, writer engagement, anisotropy,
creep, wear, and production yield. No physical coupon, measurements, or
cycling evidence exist in E-016.

## Recommendation and handoff

**Proceed conditionally to fabrication calibration; revise neither baseline
CAD nor architecture yet.** The next owner is the Design Engineer assigned
to LAB-84 or a fabrication operator nominated by the project lead. That owner
must print and inspect the labelled 42-row matrix, retain failed parts,
populate the result CSV, and update Q-009. Until then, DES-004/DES-005 remain
candidate designs and no production or procurement commitment follows.
