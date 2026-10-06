# DES-004 5x5 rotor coupon geometry and fit gate

Status: **repaired analytical gate passed; physical fit unresolved**.

The coupon is defined in `cad/des004_rotor_coupon_5x5.scad`. It uses the
DES-004 5.08 mm pitch and a 40 mm square frame, matching the existing DES-003
5x5 coupon envelope. Twenty-five 3.00 mm radius? No: each rotor is a 3.00 mm
diameter, 3.00 mm thick disk with a 1.40 mm bore and a 0.45 x 1.20 mm coded
vane envelope. The explicit correction in that sentence matters: `ROTOR_R`
is 1.50 mm, so rotor diameter is 3.00 mm.

The first geometry screen exposed a blocker: the original 1.70 mm pocket
radius was smaller than the integral vane's 2.016 mm nominal outer corner,
so the vane intersected the solid frame. The repaired candidate uses a 2.20
mm pocket radius. With the stated analytical tolerances, the minimum
vane-to-frame radial margin is approximately 0.055 mm and the nominal
pocket-to-rotor radial allowance is 0.70 mm. This is a CAD/tolerance
calculation, not a print result; the small vane margin remains a fit risk.

## Calculated gate

`python3 analysis/des004_rotor_coupon_fit_gate.py` passes all assertions. Each
rotor is a 3.00 mm diameter, 3.00 mm thick disk with a 1.40 mm bore and a
0.45 x 1.20 mm coded vane envelope:

| Check | Bound | Result |
|---|---:|---|
| 5x5 centre span | 25.40 mm ≤ 40.00 mm | pass |
| frame edge margin | 7.30 mm each side | pass |
| rotor pocket radial allowance | 0.70 mm | pass |
| axle/bore diametral allowance | 0.40 mm | pass |
| nearest rotor edge gap | 2.08 mm | pass |
| coded vane to neighbour body | 1.355 mm | pass |
| 10 mm pin over 8 mm coupon stack | 2.00 mm end margin | pass |

These are nominal and assumed-tolerance geometry calculations only. They do not establish printed
clearance, shaft straightness, detent torque, load retention, reader margin,
writer engagement, wear, or regional isolation.

## Fit disposition

The coupon geometry is bounded enough to print and inspect as the next
falsification article. Procurement remains open: the previously observed
1 mm x 10 mm catalog pin is only a candidate, and its tolerance, finish,
straightness, actual delivered length, and interaction with the printed 1.40
mm bore must be checked against samples. A physical pass requires the actual
coupon to demonstrate free rotor motion through all five stops, no binding at
the nominal 3.27 N service load, and measured clearance retention before and
after cycling. No such measurements exist yet.
