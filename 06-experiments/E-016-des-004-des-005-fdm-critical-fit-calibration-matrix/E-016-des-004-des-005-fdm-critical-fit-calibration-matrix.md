---
status: active
builds-on: [Q-009, DES-004, DES-005, E-012]
---

# E-016: FDM critical-fit calibration matrix

## Purpose and evidence boundary

This is a CAD-ready and measurement-ready definition for the X1C/PLA
process. It closes the definition gap in Q-009; it does not report printed
results. All dimensions below are nominal design inputs or acceptance
thresholds. Future printed values must include printer, nozzle, layer height,
filament lot, slicer profile, compensation, orientation, and operator.

The smallest useful falsifier is one 5x5 frame containing centre and boundary
cells, plus witness features, printed in two orientations, followed by a
3-level fit sweep. A failure rejects that clearance/orientation/process
condition; it does not alone falsify the architecture.

## Frozen baseline and variables

Use the existing `des004_rotor_coupon_5x5.scad` defaults: 5.08 mm pitch,
40 mm frame, 3.00 mm rotor diameter and thickness, 2.20 mm pocket radius,
1.00 mm axle/1.40 mm bore, 0.45 x 1.20 mm vane, 0.80 x 1.00 mm writer tongue
in a 1.20 x 1.40 mm pocket, and 0.70 x 1.00 mm reader aperture at 1.80 mm
standoff. Defaults remain unchanged.

Sweep only assembly-critical interfaces:

| Variable | Levels (mm) | Falsifies |
|---|---:|---|
| Pocket radius | 2.10, 2.20, 2.30 | vane/frame interference versus excess web |
| Bore diameter for 1.00 mm pin | 1.20, 1.40, 1.60 | insertion, free rotation, wobble, retention |
| Writer pocket minus tongue, each axis | 0.20, 0.40, 0.60 | engagement/binding and missed actuation |
| Reader target registration offset | 0.00, ±0.20 | five-state read aperture margin |

The 2.10 mm pocket row is deliberately a likely falsifier: the current CAD
vane envelope is about 2.145 mm under the existing tolerance screen. The 1.40
mm bore and 0.40 mm writer clearances are current baseline rows. Do not choose
a replacement dimension from this analytical plan alone.

## Print articles and orientation

Print labelled articles in one controlled batch, without supports in the
functional interfaces:

1. **F (functional):** frame flat on XY; rotors flat on XY with bore axis Z;
   writer and reader samples in their intended orientation.
2. **A (adverse):** one rotor with bore axis parallel to XY and vane thickness
   crossing layers; one writer tongue with its thin dimension in Z. This bounds
   anisotropy and elephant-foot sensitivity, and is not a production proposal.

For each of the 3 pocket levels and 3 bore levels, print one centre and one
boundary rotor position. Apply the 3 writer levels to separate writer samples
and the 3 reader offsets to the fixed reader target. This is 9 rotor/bore
combinations × 2 locations × 2 orientations, with writer and reader witnesses
shared across combinations: 36 rotor rows + 3 writer rows + 3 reader rows = 42
planned rows. The executable `--plan` output labels each row with article,
test type, orientation, location, swept values, and attempt count. No 3^4
Cartesian explosion is needed: interfaces are calibrated independently, then
selected rows are assembled once.

Record nozzle diameter, layer height, line width, wall/top/bottom counts,
temperatures, speed, flow and XY compensation, elephant-foot compensation,
filament lot/dry condition, slicer version/profile hash, orientation, and part
IDs before accepting results.

## Measurement procedure

After 30 minutes at room temperature, measure with calibrated pin gauges or
micrometers to 0.01 mm resolution at three clock positions. Record actual pin
diameter, bore, rotor OD, pocket at every inspected cell, vane envelope,
writer tongue/pocket, aperture, and target offset. Report mean, minimum,
maximum, and range; never replace spread with CAD nominal.

For each rotor, insert the actual pin with hand seating and rotate through all
five stops unloaded and at the 3.27 N centre-cell service load. Record binding,
stop reach, return-to-stop, and neighbour contact. For each writer row, make
30 engagements at each stop. For each reader offset, make 30 reads per stop.
If a 0–5 N load fixture is unavailable, leave loaded results unresolved;
hand judgement is not a substitute. These are physical measurements when
performed; none exist in this experiment yet.

## Acceptance and falsification rules

Hard acceptance for a measured row: all 5 stops reachable/returned without
binding; no rotor/frame or vane/neighbour contact; zero failed writer
engagements in 30 attempts; zero wrong reader states in 150 reads; measured
post-fit diametral clearance ≥0.10 mm at every inspected location; writer
clearance ≥0.20 mm in both axes; and reader aperture/target margin ≥0.20 mm.
The result checker requires `reader_margin_mm` and applies that last gate; a
row with no reader measurement is unresolved, not an analytical pass.
These are provisional engineering gates, not sourced standards.

Reject a row if any hard gate fails, any feature is outside the CAD envelope,
or locations/orientations disagree beyond the reported process spread. A pass
establishes only fit/readability under the recorded process and sample size;
it does not establish wear life, map-level reliability, timing, load strength,
or production yield. The 10,000-transition proposal remains a later physical
smoke/falsification test.

## Reproducible analytical checks

From the repository root:

```sh
python3 06-experiments/E-016-des-004-des-005-fdm-critical-fit-calibration-matrix/fit_calibration_matrix.py --plan
python3 08-integrated-designs/DES-004-five-level-rotary-verified-successor/analysis/des004_rotor_coupon_fit_gate.py
openscad --export-format binstl -o /dev/null -D 'part="frame"' 08-integrated-designs/DES-004-five-level-rotary-verified-successor/cad/des004_rotor_coupon_5x5.scad
```

The first command prints the 42-row sweep and, with `--results measured.csv`,
checks required result columns and hard gates. The latter two are CAD/geometry
checks only. No command can claim a part was printed or physically validated.

## Analytical execution record (LAB-98)

Calculated from the script and CAD gate on 2026-10-07: the plan enumerates 42
rows (36 rotor fit rows, 3 writer rows, 3 reader rows). The independent CAD
screen passes its assertions: nominal vane/frame clearance is 0.1046 mm and
the assumed worst-case screen leaves 0.0546 mm; nominal axle/bore clearance is
0.40 mm and the assumed worst-case screen leaves 0.30 mm. These are
CAD/tolerance calculations, not printed measurements. `./repo check` remains
non-zero because the repository checker reports pre-existing collapsed
experiments E-013, E-019, and E-021; no E-016 structural error was emitted.
Physical validation remains open: no coupons, dimensional measurements,
engagement trials, loaded rotation, or reader trials exist.

## Disposition and next action

Analytical status: **defined; no physical result**. The baseline is unchanged
and not promoted. Next owner: the Design Engineer assigned to LAB-84 or a
fabrication operator nominated by the project lead. Print the labelled matrix,
populate the result CSV, then update Q-009 with measured rows and retain
failed parts as evidence. Rollback is simply to retain the unchanged DES-004/
DES-005 CAD defaults; no production or purchase commitment is made.
