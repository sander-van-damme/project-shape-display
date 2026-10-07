---
status: complete
builds-on: [DES-004, E-009, E-010, E-012, E-013, Q-005]
---

# E-014: DES-004 regional-isolation falsification

## Question and acceptance rule

Can the DES-004 5x5 rotary coupon update selected rotors without moving an
untouched, loaded neighbour by more than the provisional Q-005 limit of
0.10 mm peak or residual motion? This is an analytical falsification screen;
analytical acceptance is not physical validation.

The claim is rejected only by a reproducible geometry/force model that predicts
more than 0.10 mm, or by a valid physical run exceeding the limit. It is
supported analytically only if the model bounds writer force/torque, rotor
friction, frame/support stiffness, contact, and actuator trajectory. Otherwise
the disposition is unresolved.

## Reproduction

From the repository root, run:

```text
python3 08-integrated-designs/DES-003-reliability-first/analysis/e009_analytical_bound.py
python3 08-integrated-designs/DES-004-five-level-rotary-reference/analysis/des004_rotor_coupon_fit_gate.py
```

The first command is the existing perimeter-coupling sensitivity model. It
uses the design-calculated 3.27 N service load, 0.10 mm gate, and
`n_boundary = 4(side - 1)`. The second command checks the DES-004 source
geometry and stated tolerance envelope. Both are calculations; neither is FEA
or a hardware test.

## Cheapest decisive checks

### 1. Direct geometry interference

The DES-004 source has 5.08 mm pitch, 2.20 mm pocket radius, 1.50 mm rotor
radius, and a vane envelope checked by E-012. The executable gate reported:

| check | calculated result | disposition |
|---|---:|---|
| nominal pocket-to-rotor radial allowance | 0.70 mm | pass |
| nominal rotor-body gap to neighbour | 2.08 mm | pass |
| nominal vane-to-neighbour-body gap | 1.355 mm | pass |
| worst-case pocket-to-rotor radial allowance | 0.60 mm | pass |
| worst-case vane-to-frame radial margin | 0.0546 mm | pass, fragile |
| worst-case axle/bore diametral clearance | 0.30 mm | pass, assumed |
| worst-case writer side/width clearance | 0.30 mm each | pass, assumed |

No direct rotor, vane, writer, or pocket interference is predicted by these
checks. The 0.0546 mm vane margin is small enough that print-process spread
could create binding, but that would be a local fit failure, not evidence of
regional isolation.

### 2. Shared-path and coupling check

The CAD contains independent rotor/axle bodies and no shared rotor shaft or
coupler. That removes a direct rigid shared-actuation path in the modeled
coupon, but it does not bound disturbance through the common 3 mm frame,
writer contact, support, or actuator reaction. The E-009 sensitivity output is:

| updated region | boundary cells | required stiffness at 5% assumed coupling | maximum coupling at 50 N/mm sensitivity |
|---|---:|---:|---:|
| 5x5 | 16 | 26.16 N/mm | 9.557% |
| 10x10 | 36 | 58.86 N/mm | 4.247% |
| 20x20 | 76 | 124.26 N/mm | 2.012% |

The 5x5 result is not a bound on DES-004: 50 N/mm is explicitly only a
sensitivity label, and no writer force, frame stiffness, support stiffness,
coupling fraction, contact state, or trajectory is sourced or measured. The
rotary architecture also introduces unmodeled writer torque and friction that
the DES-003 perimeter model does not represent.

## Verdict

**UNRESOLVED; regional-isolation claim not supported or rejected analytically.**

The geometry check finds no hard adjacent-cell interference, but its smallest
margin is an assumed 0.0546 mm FDM tolerance result. The coupling calculation
shows that a 5x5 update could meet 0.10 mm under some stiffness/coupling pairs,
but none is justified for DES-004. The ideal 10,000-transition logical smoke
in E-012 is irrelevant to mechanical disturbance: it exercises bookkeeping,
not force, contact, displacement, detent, wear, or support response.

The decisive next evidence is the E-009 loaded-neighbour test using the DES-004
rotary writer and actual support: synchronized coupon/reference displacement,
command trajectory, load/contact record, both update directions, worst
orientation, and repeated peak/residual results. A validated FEA could replace
the physical test only if it includes those same force, contact, material,
clearance, and boundary inputs. No physical validation has occurred here.
