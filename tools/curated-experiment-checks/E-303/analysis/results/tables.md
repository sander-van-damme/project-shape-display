# E-303 generated analytical tables

Regenerate with `python analysis/generate.py` from the E-303 directory.
Inputs are **assumptions**, except explicit repository geometry and the separately
labeled published 20 mm reference. CSVs retain additional scenarios and precision.
All table torques are N mm; 1 N mm = 1 mN m = 0.001 N m.

## Screw scenarios

Guide resistance, friction and parasitic torque are illustrative; no owner torque
measurement exists. Lowering negative values mean braking is needed in this model.

| Scenario | Weight N | Guide N | Raise/run N mm | Raise/start N mm | Lower applied N mm |
| --- | --- | --- | --- | --- | --- |
| light terrain | 0.05 | 0.01 | 0.053 | 0.05967 | -0.002095 |
| moderate terrain | 0.2 | 0.05 | 0.2774 | 0.3429 | 0.01757 |
| loaded / imperfect guide | 1 | 0.2 | 1.63 | 2.196 | 0.1831 |
| 5 N obstruction scenario | 5 | 0.5 | 7.205 | 9.8 | 0.6799 |
| 20 N obstruction scenario | 20 | 1 | 27.23 | 37.14 | 2.549 |

## Friction size comparison

Inner radius 1.1 mm; uniform pressure, μk=0.3, μs=0.4. No thrust-brake deduction.

| OD mm | r effective mm | N for 0.1 N mm | N for 0.5 N mm | Kinetic at 0.1 N, N mm |
| --- | --- | --- | --- | --- |
| 4 | 1.594 | 0.2092 | 1.046 | 0.04781 |
| 4.7 | 1.8 | 0.1851 | 0.9257 | 0.05401 |
| 5 | 1.891 | 0.1763 | 0.8815 | 0.05672 |
| 6 | 2.197 | 0.1517 | 0.7587 | 0.0659 |
| 7 | 2.509 | 0.1329 | 0.6644 | 0.07526 |
| 10 | 3.466 | 0.09618 | 0.4809 | 0.104 |
| 20 | 6.739 | 0.04946 | 0.2473 | 0.2022 |

Magnetic field demand for the same 0.1 N mm using **two hypothetical 1 mm² poles**, with 0.1 mm gap each, zero steel reluctance and no leakage. These are field-demand bounds, not a fitting coil layout:

| OD mm | Required gap B T | Gap-only NI A turns |
| --- | --- | --- |
| 4 | 0.5127 | 81.6 |
| 4.7 | 0.4823 | 76.77 |
| 5 | 0.4707 | 74.91 |
| 6 | 0.4367 | 69.5 |
| 7 | 0.4086 | 65.03 |
| 10 | 0.3477 | 55.33 |
| 20 | 0.2493 | 39.68 |

## Magnetic A reference

Two M2 poles, effective root area 1.7 mm² each; gap 0.10 mm each, extra fixed contact equivalent gap 0.05 mm, steel path 25 mm, μr=300. Two 80-turn series coils, calculated 3.42 Ω. Friction annulus 4.0–4.5 mm radius, μk=0.3. Values exclude leakage, bearing torque and temperature rise.

| NI A turns | I A | P W | B T | Force N | Torque ceiling N mm |
| --- | --- | --- | --- | --- | --- |
| 8 | 0.05 | 0.008551 | 0.03016 | 0.00123 | 0.001571 |
| 16 | 0.1 | 0.0342 | 0.06032 | 0.004922 | 0.006283 |
| 32 | 0.2 | 0.1368 | 0.1206 | 0.01969 | 0.02513 |
| 48 | 0.3 | 0.3078 | 0.181 | 0.0443 | 0.05655 |
| 64 | 0.4 | 0.5473 | 0.2413 | 0.07875 | 0.1005 |

## Electrostatic B2 size and air-gap sensitivity

300 V terminal, equal floating halves, 12 µm total PET, εr3.25, μ0.3, 80% active annulus. Gap-closing model; not demonstrated real contact force.

| OD mm | Gap µm | Torque N mm | C terminal pF | Stored µJ |
| --- | --- | --- | --- | --- |
| 4.7 | 0 | 0.04277 | 6.498 | 0.2924 |
| 4.7 | 5 | 0.007718 | 2.76 | 0.1242 |
| 4.7 | 20 | 0.001039 | 1.013 | 0.04557 |
| 7 | 0 | 0.1526 | 16.63 | 0.7485 |
| 7 | 5 | 0.02753 | 7.066 | 0.318 |
| 7 | 20 | 0.003706 | 2.592 | 0.1167 |
| 10 | 0 | 0.4542 | 35.84 | 1.613 |
| 10 | 5 | 0.08195 | 15.23 | 0.6852 |
| 10 | 20 | 0.01103 | 5.586 | 0.2514 |

## B concept annulus, separately dimensioned

Ro4.5/Ri1.8 mm on Ø10 mm carrier; 100% of this annulus before insulating seam allowance, otherwise as B2 above.

| Gap µm | Gap-closing N mm | Bulk-stress N mm | C pF |
| --- | --- | --- | --- |
| 0 | 0.3916 | 0.1205 | 32.04 |
| 5 | 0.07065 | 0.02174 | 13.61 |
| 20 | 0.00951 | 0.002926 | 4.993 |

## Stagger clearance

Same-height circular envelopes only; negative clearance means collision. Last column checks a 3.2 mm shaft crossing the neighboring tier. A design allowance of 0.30 mm total envelope-to-envelope clearance is an assumption, not proven FDM tolerance.

| D mm | 1 height gap mm | 2 heights gap mm | 4 heights gap mm | Neighbor shaft gap mm |
| --- | --- | --- | --- | --- |
| 4 | 1.08 | 3.184 | 6.16 | 1.48 |
| 4.7 | 0.38 | 2.484 | 5.46 | 1.13 |
| 5 | 0.08 | 2.184 | 5.16 | 0.98 |
| 6 | -0.92 | 1.184 | 4.16 | 0.48 |
| 7 | -1.92 | 0.1842 | 3.16 | -0.02 |
| 10 | -4.92 | -2.816 | 0.16 | -1.52 |

## Continuous coil power

| Active | 0.01 W/cell → W | 0.05 W/cell → W | 0.1 W/cell → W | 0.25 W/cell → W | 0.5 W/cell → W | 1 W/cell → W |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.01 | 0.05 | 0.1 | 0.25 | 0.5 | 1 |
| 100 | 1 | 5 | 10 | 25 | 50 | 100 |
| 1000 | 10 | 50 | 100 | 250 | 500 | 1000 |
| 6400 | 64 | 320 | 640 | 1600 | 3200 | 6400 |

## Electrostatic electrical power

4.7 mm envelope at ideal zero air gap. Full resistive charge/discharge cycles; fixed bleeders and leakage are examples, not verified parts. Converter quiescent power and switch leakage are excluded.

| Cells | 10 Hz switching W | 100 MΩ bleeders W | 10 GΩ leakage W |
| --- | --- | --- | --- |
| 1 | 5.848e-06 | 0.0009 | 9e-06 |
| 100 | 0.0005848 | 0.09 | 0.0009 |
| 1000 | 0.005848 | 0.9 | 0.009 |
| 6400 | 0.03743 | 5.76 | 0.0576 |

## Useful plots and full data

- [Screw friction](screw-friction-sensitivity.svg)
- [A magnetic gap versus power](magnetic-gap-power.svg)
- [B floating electrostatic gap versus size](electrostatic-gap-size.svg)
- [Coil power at array scale](array-coil-power.svg)
- [All 16 two-rail matrix states](matrix-two-rail-states.csv)
- [Counterfactual scaling of published specialized 20 mm clutch](published-cubic-counterfactual.csv)
- [Slip heat](slip-heat.csv)
- [Film/voltage sweep](electrostatic-film-voltage.csv)
- [Thread-diameter/friction sensitivity](screw-thread-sensitivity.csv)
- [OFF preload sweep](off-drag.csv)
- [Winding envelopes, not complete clutches](winding-envelope.csv)
