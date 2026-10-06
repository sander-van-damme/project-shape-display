---
status: candidate
builds-on: [DES-004, Q-009, E-012]
---

# DES-005: DES-004 5x5 rotor coupon geometry

The executable coupon definition is retained with DES-004 because it is a
falsification article for that design:
`../DES-004-five-level-rotary-verified-successor/cad/des004_rotor_coupon_5x5.scad`.
The associated fit-gate report and script are in that design's `analysis/`
directory.

This design freezes the actual rotor, axle, vane, writer, reader, and frame
interfaces at the dimensions in E-012. The nominal and worst-case geometry
checks are reproducible, but the candidate axle/bore worst-case diametral
clearance is only 0.02 mm. That is a release risk under FDM process
variation, not a measured fit result. No production geometry or
hardware-performance claim follows until Q-009 physical measurements exist.
