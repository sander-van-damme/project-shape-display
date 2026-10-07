---
status: active
builds-on: [E-033]
---
# E-034: E-033 SCAD load-path falsification report

## Verdict

**REPAIRED nominal package passes the requested CAD/prose gate.** The gate
cut is through the 0.40 mm slider, the Ø1.20 follower passes a 1.60 mm stop
bore, and the Ø3.00 shoulder bears on the stop-plate top land at z=2.00 mm.
This is CAD/calculation evidence only, not physical-performance validation.

## Reproduction

From the repository root:

```text
python3 06-experiments/E-033-e-032-a-010-insert-geometry-and-load-path-gate/analysis/a010_insert_gate_check.py
PASS nominal A-010 E-033 geometry checks
cells=25 pitch_mm=5.08 state_travel_mm=3.20
stack_height_mm=2.00 placement_bound_mm=0.30
residual_margin_mm=0.60 edge_clearance_mm=4.76

openscad --export-format binstl -o /dev/null .../cad/a010_insert_gate.scad
exit 0; valid 3D object

./repo check
OK: 103 objects; structure and builds-on references valid
```

No physical testing or measurement was performed. The first result is
calculated, the second is CAD/export evidence, and the repository result is a
structure check.

## Independent calculations

- Guide running clearance: `4.50 - 4.20 = 0.30 mm` in one axis and
  `4.90 - 4.60 = 0.30 mm` in the other. This agrees with the E-033 prose;
  the Python check only reports the latter 0.30 mm value.
- Gate aperture/follower clearance: `3.00 - 1.20 = 1.80 mm` diametral, or
  `0.90 mm` radial nominal clearance; the gate cut spans the full 0.40 mm
  slider thickness.
- Stop bore/follower clearance: `1.60 - 1.20 = 0.40 mm` diametral, or
  `0.20 mm` radial nominal clearance. The shoulder/bore diameter difference
  is `3.00 - 1.60 = 1.40 mm`, providing a positive bearing land.
- Declared placement exercise: `0.10 + 0.10 + 0.10 = 0.30 mm`; residual
  radial margin is `0.90 - 0.30 = 0.60 mm`, exceeding the declared 0.20 mm
  screen. This is a tolerance exercise, not process capability.
- Five-state travel: `(5 - 1) * 0.80 = 3.20 mm`; writer stroke is
  `3.20 + 0.20 + 0.20 = 3.60 mm`, matching the E-033/Python definition.
- Cartridge/frame envelope: `(40.00 - 30.48) / 2 = 4.76 mm` per edge and
  `9.52 mm` total margin. The nominal cartridge is inside the frame; datum,
  writer parking, and fixture access are not modeled by the SCAD.
- Declared layer stack reaches z=2.00 mm. The repaired SCAD stop plate ends at
  z=2.00 mm, matching the shoulder reaction plane.

## Decisive contradictions

1. **Through aperture: PASS after repair.** `cell_aperture()` subtracts a
   `3.00 x 3.00 x 0.44 mm` cube from the `0.40 mm` slider, leaving a
   full-depth gate aperture.

2. **Follower clearance and shoulder bypass: PASS after repair.** Each
   stop-plate cell has a `1.60 x 1.60 mm` through bore. The Ø1.20 follower
   clears it, while the Ø3.00 shoulder begins at the plate top z=2.00 mm and
   overlaps the surrounding top land. The gate slider is below the upper guide
   and is not in this vertical reaction chain.

3. **Five-state reach/return envelope: PASS analytically; CAD representation
   is nominal.** The checker enumerates `-1.60, -0.80, 0, +0.80, +1.60 mm`,
   verifies 0.80 mm indexing and 3.20 mm return span, and the SCAD repeats the
   repaired bore at every cell. This does not establish friction, stop wear,
   or actuator capability.

4. **Writer and datum claims are not falsifiable from this SCAD.** No W0
   channel, tongue, 0.60 mm tab engagement, parking location, 0.20 mm parked
   clearance, D+ rail, south clamp, or removal/lift envelope is modeled. The
   Python script checks their declared scalar inputs only.

## Disposition and remaining gates

The repaired package is accepted for nominal CAD/calculation falsification:
through aperture PASS; follower clearance PASS; shoulder/stop load bypass PASS;
five-state reach/return envelope PASS analytically. Remaining physical gates
are unresolved: fabrication/flatness, slider friction and writer force,
shoulder contact stress and compliance, lateral disturbance, debris/wear,
reader event chain, timing, and the E-032 measured reseat/isolation/1,000-record
tests. No physical validation or procurement claim is made.
