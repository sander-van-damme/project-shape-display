# DES-003 critical-fit calibration coupon

Executable work product for [Q-009](../../../05-research-questions/Q-009-fdm-critical-fit-calibration.md).
The source [`a1_coupon_calibration.scad`](../scad/a1_coupon_calibration.scad) models actual DES-003 interfaces: three binary-latch stations at 5.08 mm pitch, five true-pitch registration stations with half-pitch marks, a two-rail repeated-fit pair, and the frame-fixed reflective flag at the adopted 1.8 mm reader gap.

Generate the nominal measurement sheet and render deterministically:

```sh
python3 analysis/a1_coupon_calibration.py
openscad -o /tmp/a1_coupon_calibration.stl scad/a1_coupon_calibration.scad
```

`a1_coupon_calibration.csv` intentionally leaves `measured_mm`, `pass_fail`, and `notes` blank. Fill them only after a recorded X1C/PLA print process. Geometry and bands are CAD-derived/calculated; fit yield, force, friction, wear, creep, optical classification, and print-to-print spread are unresolved. No physical validation is claimed.
