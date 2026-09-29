# SHA-17 divergent mechanism sketches, round 3 (candidate record)

> Companion to the verdict note
> [`07-evidence-and-decisions/sha17-divergent-screen-3.md`](../07-evidence-and-decisions/sha17-divergent-screen-3.md).
> Sketches live here per the routing rule (new ideas go in `04`);
> the binding kill math and verdicts live in `07`; the one executed
> analytic test lives in `06-experiments/test20_divergent_screen3/`.
> Evidence class: CALCULATION over sourced-class prices + textbook physics.
> DND-27: no print, purchase, or measurement.
> S5-R, A1, S6-LC packages untouched.

All three mechanisms use physics not screened in SHA-15/16 and are not
A1-A7 as drawn or T1-T5: (E1) inertial stick-slip transport, (E2)
solid-liquid volumetric phase-change latching, (E3) off-board robotic
setting with on-board passive memory. None is a platen, fluid bus,
magnet-detent, SMA/optothermal-broadcast, electrostatic-clutch, or
gravity-drop design as drawn — see the E2 distinctness note below.

## E1 — global travelling-wave vibratory ratchet conveyor

Each column sits in a sawtooth-ribbed PLA guide (asymmetric friction:
easy-up, hard-down). One or four board-wide vibration actuators (coin
ERM or piezo shakers under the baseplate) drive a vertical travelling
wave; stick-slip rectifies the oscillation into net upward stepping of
all columns simultaneously. Selection is per-cell wedge gates (64 tile
gate channels, printed): an engaged gate clamps its column to the frame
so it ignores the wave; a released column climbs one micro-step per
wave cycle. Height memory is the sawtooth ratchet; miniature load rides
on the ratchet, never on vibration. Down-reset is a second wave mode
(or a tilt + symmetric buzz) with gates inverted. Regional reveal =
gate one tile's columns while the other 63 stay clamped.

Inertial-authority structure (the binding dimension): stepping needs
peak inertial force m*a to break stiction uphill on every cycle. A
printed PLA column (~1.5-2 cm^3, ~2 g) against PLA-on-PLA guide
stiction of order 0.2-1 N needs a = F/m = 100-500 m/s^2, i.e. ~10-50 g
of board acceleration — before dust, humidity swell, or miniature top
loads. A 400x400 mm populated board shaken at 10 g+ throws the very
miniatures the display exists to carry (they slide/topple at ~0.5-1 g
lateral) and hammers 6400 PLA ratchet teeth at kilohertz duty. Softening
the guides to cut stiction surrenders the 5 N abuse-hold the product
needs — the same floor-ceiling collision as D1, in the friction domain.
Selectivity is the second independent kill: the wave is global, so
addressing lives entirely in 6400 micro-gates that must each hold back
the full stick-slip impulse without chattering — per-cell precision
hardware at 5.08 mm pitch (KC4). One-line force ratio kills before any
script.

## E2 — paraffin phase-change latch + single global lift

Each column carries a printed capsule with ~0.1-0.3 g of paraffin wax
plus a spring pawl. Cycle: (1) a global low-force lift (one cheap lead
screw, columns unloaded during latching) raises all columns to top;
(2) a global heater plane softens ALL wax slugs at once; (3) per-column
printed displacement valves (or per-tile heater mask, 64 channels) let
selected columns sink to their target ledge while the wax is liquid;
(4) heater off — wax freezes and locks every column at its ledge by
solid encapsulation. Memory is the frozen wax (zero holding power, zero
wear faces); lift energy is fully shared; selection is freeze-timing.
This is NOT M3 as drawn: no Nitinol, no per-cell SMA wire cost
structure, no projector/optical addressing, no solid-state shape-memory
transduction. The transducer here is liquid-solid volumetric change with
conductive/global heating and mechanical encapsulation — the unscoped
"chemical/phase-change latching" seed named in the SHA-16 close-out.
It is killed below by independent physics (latent heat + Tg collision +
freeze time), not by M3's $/cell wire math.

Phase-thermal structure (the binding dimension): paraffin melt sits at
~55-65 C; the fabrication baseline is PLA with Tg ~55-60 C — the latch
melts at exactly the temperature that softens its own capsule, guides,
and ratchets. Selective freezing at 5.08 mm pitch in a
low-conductivity plastic array is uncredible: thermal diffusion over a
minutes-long freeze equalises neighbours (crosstalk), so the mask
cannot hold a per-cell pattern. Energy corroborates: ~200 kJ/kg latent
heat x 6400 x ~0.2 g ~= ~250 kJ per full-board latch cycle (before
sensible heat and losses) — a ~100 W heater needs ~40+ min of heating
alone, and natural cooling of 6400 encapsulated slugs back through PLA
is minutes more (KC2 by two orders). Addressing is the second
independent kill: per-cell heaters/valves = 6400 purchased channels
(KC4); global-oven heating = no selectivity, full-reset-only (KC5).
Frozen-wax creep under sustained miniature load is the known
measurement-only unknown — moot, analysis kills first. One-line
temperature-collision + energy math kills before any script.

## E3 — external-robot writer + passive on-board memory (fresh)

The board carries only passive printed ratchet columns (S1-style
threshold ladders, zero purchased parts per cell, zero holding power).
ALL actuation lives off-board in a commodity desktop robot — a 4-DOF
arm or an XY plotter + Z press finger (~$150-300 sourced class) — that
drives over the board and presses each column to its target height one
touch at a time. Selection is the robot's own kinematics (no on-board
gating at all); memory is the printed ratchet; regional updates are
free (drive only to the changed cells). Why it could have obsoleted A1:
it deletes the entire gantry/writer/head subsystem from the product —
the "printer" becomes a dumb passive board plus a shared external tool,
with trivial electrics on-board and the cheapest possible per-cell
hardware (pure PLA). Product analogy: the board is paper, the robot is
the pen.

Rate structure (the binding dimension, executed as the gate): a
full-map change must set up to 6400 cells in < 30 s, i.e. >= 213
cells/s sustained including travel, press, settle, and verify. A hobby
pick-press cycle is class 0.4-1.5 s/cell (move + press + retract),
i.e. ~1-2.5 cells/s — shortfall ~85-200x even at the optimistic corner
before travel across 400 mm, ratchet-settle, or any retry. Parallel
fingers close the rate only by multiplying purchased writers (64+
fingers = a gantry again, at a cost floor far above A1 $181). Pitch vs
repeatability corroborates the silent kill: hobby-arm repeatability is
class +/-0.2-0.5 mm against 5.08 mm pitch with 0.4 mm features — a
mis-registered press seats the wrong ratchet tooth with no on-board
readback (KC3). The executed gate
(`06-experiments/test20_divergent_screen3/writer_rate_gate.py --gate`)
checks all five faces 5/5.
