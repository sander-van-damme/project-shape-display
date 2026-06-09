# Trial 6 — sliding release grid (1×5 test strip)

Implements the three-layer sandwich: a guide grid for the pins, a sliding
3D-printed "wire comb" that locks/releases them, and a cover grid on top.
Pins carry a sawtooth rack recessed in a groove on one face; blade tongues
on the sliding strip reach into the groove. Push a pin up and the ramps cam
the strip aside against a rubber band (click); load a pin down and the flat
tooth face presses on the blade top (locked); pull the strip 1 mm and every
pin drops to the floor plate.

Everything is in `test-strip.scad` (vanilla OpenSCAD, no libraries).
Pick the part with the `part` variable or `-D 'part="..."'`, or use the
pre-exported STLs in `stl/`. `section.scad` renders a cut-open assembly
for inspection.

## Key dimensions (defaults)

| parameter        | value | meaning                                   |
|------------------|-------|-------------------------------------------|
| pitch            | 8.5   | 3 pins per 1-inch D&D square              |
| pin_w            | 6.0   | square pin width                          |
| travel / levels  | 30/6  | 5 mm per elevation level                  |
| release_travel   | 1.0   | strip slide to release                    |
| engagement       | 0.7   | blade overlap over the tooth tips         |
| pin_clear        | 0.3   | pin–channel clearance per side (loose!)   |

The loose channel fit is intentional: holding comes from the detent, not
friction, so print variance in the channels does not matter.

## Printing

| part           | qty | orientation              | notes                          |
|----------------|-----|--------------------------|--------------------------------|
| pins_print     | 1   | as exported (lying down) | groove faces up — clean teeth  |
| grid_bottom    | 1   | as exported              | 3+ perimeters                  |
| release_strip  | 1   | flat                     | PETG preferred (cam wear)      |
| grid_top       | 1   | as exported              |                                |
| floor_plate    | 1   | flat                     |                                |
| push_rod       | 1   | vertical, or use 3.5 mm rod stock |                       |

PETG recommended throughout; PLA works for the grids. 0.2 mm layers.

## Assembly

1. Bolt `floor_plate` under `grid_bottom` (4× M3).
2. Drop `release_strip` into the pocket, stem out through the east slot.
3. Bolt `grid_top` on (same M3 bolts).
4. Loop a rubber band from the stem paddle hole around the peg on the east
   wall. The band pulls the strip west = engaged. Band tension sets the
   click force — start light.
5. Pull the stem (released) and drop the pins in from the top, groove
   facing east toward the blades — they only seat in that orientation,
   which is the point of the groove key. Let go of the stem.

## Test protocol

1. Click: push a pin up from below through a floor hole with the rod. It
   should click in clean 5 mm steps. Too stiff → lighter band or reduce
   `engagement`. Doesn't hold → tighter band or increase `engagement`.
2. Lock: press a raised pin down hard. It must not move. Stand weights on
   it (a mini is ~0.3–0.5 N; test to 5 N+).
3. Level accuracy: raise to each of the 6 levels, measure heights.
4. Release: pull the stem — all raised pins must drop freely to the floor
   plate. If any hang, increase `pin_clear` or check for stringing in the
   channels.
5. Re-engage: let the stem go with all pins down; raise a pin one click to
   confirm the blades re-entered the grooves.

## Tuning knobs

- `seat_gap` (0.1): vertical slack at each detent; raise if blades rub.
- `strip_clear` (0.25): strip sliding fit; raise if the strip binds.
- `tip_recess` (0.4): how far tooth tips hide below the pin face.
- `tooth_land` (2.0): vertical land = tolerance to height error.

## Scaling notes (beyond this test strip)

- Multi-row boards: slice the release layer into one strip per row sharing
  a common release bar, so pushing pins in one row cannot momentarily
  unlock other rows. The strip module already is exactly one such row.
- The inter-pin budget rules: `pitch − pin_w ≥ bridge_t + release_travel
  + 2×strip_clear`. Grow pitch or shrink pins before growing travel.
- Surface coverage upgrade ("stepped pins"): make the visible pin body
  nearly full pitch width and move the groove + rack to a narrower tail
  running in a lower tier. Same sandwich, hidden mechanism, ~90% coverage.
