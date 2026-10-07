---
status: complete
builds-on: [E-034, E-033, A-010, A-011]
---

# E-035: rejected A-010 carriage repair source

## Disposition

Rejected by E-039. The calculations below describe the attempted repair; their scalar PASS values do not establish actual five-state geometry or load continuity. E-039 retains the decisive CAD defects and the 6.20 mm required envelope versus the 4.90 mm pocket. Source is preserved as an auditable failed model, not an active repair task.

## Attempted datum and geometry

The repaired model uses `(x,y)` as the cartridge datum and `z` only as the
load axis. State positions are `y = -1.60, -0.80, 0.00, 0.80, 1.60 mm`.
The gate's single 3.00 mm square aperture, the 4.00 x 0.42 mm carriage, the
Ø1.20 follower, the 1.60 mm selected stop bore, and the Ø3.00 x 0.35 mm
shoulder all share the same `(x=0,y=selected_state)` centre. The gate is
z=0.40–0.80; the stop plane is z=1.20–1.50. The follower runs between these
planes and the shoulder lands on the stop plane, giving the intended path:
`follower -> shoulder -> selected stop land -> stop plate -> frame`.

The fixed guide datum is 4.50 x 4.90 mm with a 4.20 x 4.60 mm slider
envelope; the carriage is 4.00 mm wide in the x direction. The writer tongue
covers 3.20 mm S0–S4 travel plus 0.20 mm approach at each end (3.60 mm
stroke) and is drawn with 0.60 mm tab engagement. These are geometry
assumptions, not actuator, friction, timing, stress, or fabrication claims.

## CAD and reproducible checks

`cad/a010_carriage_params.scad` is the shared parameter source. The SCAD and
both Python checks consume those values; no check duplicates the nominal
state or clearance constants. The repaired CAD has one opaque S2 section and
four transparent reference states, plus all five stop bores and the writer
path. Reference states are alternatives, not simultaneous occupancy.

From the repository root:

```sh
python3 tools/curated-experiment-checks/E-035/a010_carriage_gate_check.py
PYTHONPATH=tools/curated-experiment-checks/E-035 python3 tools/curated-experiment-checks/E-035/a010_carriage_independent_recheck.py
openscad --export-format binstl -o /dev/null tools/curated-experiment-checks/E-035/a010_bounded_carriage.scad
```

The checks produce reproducible **PASS** results for aperture radial
clearance (0.90 mm), stop radial clearance (0.20 mm), shoulder land (0.70
mm), guide/carriage envelope, five indexed stop identities, follower load
reaction datum, 3.60 mm writer path, and frame/cartridge clearance (4.76 mm).
They are calculated/shared-CAD evidence only. OpenSCAD export is CAD
syntax/solid-generation evidence only.

## Remaining gates

Fabrication/flatness, assembly yield, slider and writer force, debris and wear,
reader classification, event timing, lateral disturbance, and the E-032
physical reseat/isolation/1,000-record measurements remain unresolved.
A-010/A-011 integration remains paused. No physical validation or fabrication
authorization follows from this analytical repair.
