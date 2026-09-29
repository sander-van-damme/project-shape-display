# SHA-15 divergent mechanism sketches (candidate record)

> Companion to the verdict note
> [`07-evidence-and-decisions/sha15-divergent-screen.md`](../07-evidence-and-decisions/sha15-divergent-screen.md).
> Sketches live here per the routing rule (new ideas go in `04`);
> the binding kill math and verdicts live in `07`; the one executed
> analytic test lives in `06-experiments/test18_divergent_screen/`.
> Evidence class: CALCULATION over sourced-class prices + textbook physics.
> DND-27: no print, purchase, or measurement.

## M1 — shared-pneumatic bladder lift + 64 tile-gated printed ratchets

One sealed bladder chamber under the board (or one per 10-row bank)
provides all lift energy as compressed air from a single 12 V diaphragm
pump. Each 10x10 tile has one purchased 3/2 micro-valve that vents or
pressures its local bladder branch; within a tile, printed ratchet pawls
(threshold-encoded like S1) decide which of the 80x80 columns advance on
each of four 10 mm broadcast pressure strokes. Height memory and
miniature load live in the printed ratchets; air only moves, never holds.
Regional reveal = pressurize one tile branch while the other 63 stay
vented and ratchet-locked. This is NOT row-3 per-cell pneumatics (6400
seals/valves, killed) and NOT row-26 bladder-only (no selection):
selection sits at the tile layer (64 valves), power is fully shared.

## M2 — permanent-magnet bistable columns + tile-parallel writer comb

Each column carries one cheap ferrite disc that snaps between two printed
steel-keeper seats per level station (4 stations = 5 states, S1-style
unary stepping). A travelling Halbach-array writer bar biases the detent
field contactlessly: columns whose printed steel shutter is open follow
the field step, closed ones stay. No friction wear surfaces, no holding
power, no snap-force variation from PLA elasticity. Selection is magnetic
field gating, not mechanical gating — a different physics from every
A-family mechanism. This answers row-19's "pending a parallel rewritable
medium" clause with a tile-parallel electromagnet comb (64 drivers) rather
than 6400 magnetic bits or a serial head.

## M3 — optothermal SMA broadcast via a single projector

Each column has one SMA U-wire that contracts to toggle a printed latch
one level per thermal cycle (4 broadcast flashes = 5 states). Addressing
is optical: a single stationary DLP/projector module flashes the 80x80
bit-image onto the wire plane; black/white pixels select which wires reach
70-90 °C activation. Zero addressing wires, zero per-cell drivers, one
purchased active component. This answers row-4's "pending a radically
shared thermal selector" clause: the selector is light, not wiring.

## Deferred seeds (NOT surveyed this heartbeat — future queue)

- **D1 — compliant staged-snap column with global compression platen.**
  4 stacked printed bistable frustums per column give 40 mm in 4 snaps;
  one rigid platen compresses the whole board while a printed shutter mask
  selects. Different from R05/Q7 (which frames compliance as a thin
  selector layer, not the stroke itself). Killer unknown: PLA creep under
  sustained snap preload + holding force vs 5 N abuse — measurement-only
  under DND-27, so it can only be parked, not killed, analytically.
- **D2 — electrostatic-clutch shared shaft at tile level (64 clutches).**
  R09 inspiration moved from cell to tile: one motor, 64 printed-clutch
  couplings. Killer unknown: clutch torque density at tile scale.
