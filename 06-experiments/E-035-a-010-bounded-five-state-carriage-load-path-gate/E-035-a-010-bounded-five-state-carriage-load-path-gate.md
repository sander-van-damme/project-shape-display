---
status: active
builds-on: [E-034, E-033, A-010, A-011]
---

# E-035: bounded A-010 five-state carriage load-path gate

## Bounded architecture decision

A-010 is redefined for this gate as a **five-state translating follower
carriage**. The laminated aperture gate is a selector only. To avoid the
previous impossible overlapping lateral stop openings, the five aperture and
stop identities are vertically indexed at z = 0, 0.80, 1.60, 2.40, 3.20 mm.
A bidirectional writer moves the gate vertically; a coupled carriage then
translates the Ø1.20 follower vertically inside a 4.60 mm guide envelope. A
stepped stop plate provides one positive stop identity per state. The Ø3.00
shoulder lands on the selected stop-plate shelf. The gate and its guides are
below this reaction plane and are not load-bearing.

This explicitly narrows the prior A-010 claim: it no longer claims a fixed
follower passing through five laterally offset apertures. The carriage and its
actuator path are required parts. State changes require unload, gate
translation, carriage translation, selected-stop seating, and release.

## Joint geometry definition

The frozen E-032-G1 envelope is retained: 40.00 mm frame, 30.48 mm cartridge,
5.08 mm cell pitch, and 4.76 mm nominal frame edge margin. Paired guide
pockets are 4.50 x 4.90 mm; the slider envelope is 4.20 x 4.60 mm, giving
0.30 mm running clearance in each guide axis. The carriage is 4.00 mm wide
in the 4.60 mm guide slot. The gate is 0.40 mm thick, with a 3.00 mm square
aperture. The stop plate has five 1.60 mm square openings/shelves at the
vertical state centres. The follower has Ø1.20 mm and the shoulder Ø3.00 mm x
0.35 mm.

The writer tongue envelope is 4.00 mm stroke: 3.20 mm S0-to-S4 travel plus
0.20 mm approach at each end, with 0.60 mm minimum tab engagement. These are
geometry assumptions inherited from E-033, not actuator capability or timing
results.

## Load path and state-by-state check

For each state S0 through S4, the modeled chain is:

`follower -> shoulder -> selected stop-plate land -> stop plate -> frame`.

The follower shank is centred in both the selected gate aperture and selected
stop opening. Calculated radial clearances are 0.90 mm at the gate and 0.20 mm
at the stop opening. The shoulder has 0.70 mm radial land beyond the stop
opening. Therefore the nominal section has a positive bypass around the gate:
the gate can set state but does not provide the vertical reaction. This is
geometry-derived, not a stress, buckling, friction, or physical-performance
proof. Lateral force and tilt could still defeat the bypass and remain open.

The CAD model is `cad/a010_bounded_carriage.scad`. It includes lower and upper
guide envelopes, an S2 gate section, five vertically indexed stop shelves, carriage,
follower/shoulder, and bidirectional actuator tongue envelope. Reference marks
show all five carriage centre positions without representing simultaneous
occupancy.

## Reproducible analytical evidence

Run from the repository root:

```sh
python3 06-experiments/E-035-a-010-bounded-five-state-carriage-load-path-gate/analysis/a010_carriage_gate_check.py
python3 06-experiments/E-035-a-010-bounded-five-state-carriage-load-path-gate/analysis/a010_carriage_independent_recheck.py
openscad --export-format binstl -o /dev/null 06-experiments/E-035-a-010-bounded-five-state-carriage-load-path-gate/cad/a010_bounded_carriage.scad
```

The primary script calculates five state centres, 3.20 mm indexed travel,
3.60 mm writer stroke, guide/carriage envelope, 0.90/0.20 mm radial
clearances, 0.70 mm shoulder land, and 4.76 mm cartridge edge margin. The
independent script repeats those bounds using a separate interval-style
formulation and passes. OpenSCAD export is CAD syntax/solid-generation
evidence. None is physical validation.

## Independent review disposition

The independent recheck passes the claimed nominal geometry and confirms that
the selected stop identity is one of five explicit positions and that the
gate is not the stated load reaction. Review scope is limited to the scripts,
dimensions, and section-level load path; it does not approve fabrication or
integration.

## Remaining separate gates

Fabrication/flatness and assembly yield; slider and carriage friction/writer
force; debris and guide wear; reader classification and event chain; timing
against the 9 ms screen; lateral disturbance of adjacent loaded cells; and
the E-032 physical reseat, isolation, and 1,000-record measurements are all
unresolved. A-010/A-011 boundary integration remains paused until those gates
are separately addressed. No hardware performance, procurement, or
physical-validation claim is made.
