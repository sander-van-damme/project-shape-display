# SHA-25 divergent mechanism sketches, round 5 (candidate record)

> Companion to the verdict note
> [`07-evidence-and-decisions/sha25-divergent-screen-5.md`](../07-evidence-and-decisions/sha25-divergent-screen-5.md).
> Sketches live here per the routing rule (new ideas go in `04`);
> the binding verdicts and pause case live in `07`; no analytic test was
> executed because no seed survived scoping (task allows at most one
> advance; zero were advanced).
> Evidence class: CALCULATION over sourced-class prices + textbook physics.
> DND-27: no print, purchase, or measurement.
> S5-R, A1, S6-LC packages untouched.

Round 5 attempted seven G-series seeds against two filters applied BEFORE any
math: (1) freshness vs ALL killed families (A1-A7 as drawn, T1-T5, M1/M2/M3,
D1/D2/D3, E1/E2/E3, F1/F2/F3, platen, fluid-bus, magnetic, thermal-broadcast,
electrostatic, gravity, vibratory-conveyor, phase-change-latch,
serial-robot-writer at tile/board scale, plus rows 1-7/11/16-22/25/27 of the
`04` topology table), and (2) non-overlap vs the Architecture Challenger's
owned lane ([SHA-24](/SHA/issues/SHA-24): shared actuation with passive
selection or state retention — as embodied by its in-progress G1 scanning
multi-spindle screw-column matrix in `sha24-sms-screen.md`, which stores state
in self-locking threads and selects positionally from a shared scanning bar).
Every seed records its non-overlap rationale per the task brief. None cleared
both filters with a coherent, scopable one-line gate — the scoping failures
below ARE the round's engineering output (failures recorded as knowledge, not
filler).

## G1 — photochemical (UV-cure resin) latch + shared lift

Each column carries a printed cup with liquid photopolymer; a shared lift
raises the board while a stationary projector (M3-style addressing, but UV,
not thermal) cures selected cups' resin collars at successive height planes,
freezing columns at 5 planes. Memory is cured resin (zero holding power);
lift energy fully shared; selection is light. Transducer (photopolymerization)
differs from M3 (thermal SMA), E2 (thermal paraffin), F3 (diffusive swelling).
**Non-overlap vs SHA-24:** none available — shared lift + passive cured
retention IS shared actuation with passive state retention, the challenger's
owned lane. **Excluded at scoping** on lane collision alone; corroborating
independent exclusions: per-cell resin supply is fluidic addressing (row 27 /
M1 family), cured resin is irreversible so down-reset needs mechanical break
plus re-coat (full-reset-only, KC5 class), and uncured-resin creep under load
is silent (KC3 class). No gate stated; lane-owned.

## G2 — per-cell piezo / micro-solenoid array (no shared drive)

6400 bought micro-actuators, one per cell, each delivering 40 mm (piezo stack
with lever amplification, or 5 mm solenoid + ratchet). No shared actuation,
so outside the SHA-24 lane (non-overlap: per-cell bought drive vs shared
drive — clean). **Excluded at scoping** as killed-family re-litigation:
rows 1-2 of the topology table already drop motor-per-cell ($3,200 floor at
$0.50/axis) and solenoid-per-cell (6400 coils/switches/wires); solenoids fall
inside the killed magnetic family (M2/D2); piezo stacks delivering 40 mm at
5 mm scale do not exist in the sourced class (stacks give um-mm; lever
amplification trades away the 5 N hold). Count x unit + stroke-fit kills are
one line each. No gate stated; already dropped.

## G3 — manual-direct hand setting + passive ratchet memory

No machine actuation at all: the user presses columns by hand into printed
ratchets (S1-style ladders); the product is a passive board. Outside the
SHA-24 lane (non-overlap: no actuation, shared or otherwise — clean).
**Excluded at scoping** as E3-family re-litigation at a worse corner: E3's
rate kill (hobby press ~0.4-1.5 s/cell, need >= 213 cells/s, shortfall
~85-200x) applies a fortiori to a human hand (~1 s/cell sustained = ~6400 s
per full map, ~200x over budget), and row 22 already drops manually swapped
terrain as primary product. The rate physics is identical; only the writer is
slower. No gate stated; E3 covers it.

## G4 — hygroscopic (moisture-swelling wood/paper) actuation

Each column carries a hygroscopic bilayer or compressed-wood capsule dosed by
a shared humidity bus; swelling jacks the ratchet, drying resets.
Non-overlap vs SHA-24 is arguable (shared humidity bus + ratchet retention
reads as shared actuation + passive retention — likely lane-adjacent).
**Excluded at scoping** as F3 re-litigation regardless: moisture uptake in a
mm-scale capsule is diffusion-limited with the same tau ~ L^2/D structure and
D class as F3 (hours per pass vs 4 passes in 30 s), and per-cell moisture
dosing is the same microfluidic addressing kill (KC4). Different solvent,
same kill quantities. No gate stated; F3 covers it.

## G5 — centrifugal / spin-selection drive

The board spins; columns fling outward/up ramps past gated escapements, with
per-cell gates selecting radius (height). **Excluded at scoping** as
unscopable: no coherent selection/memory story fits 5.08 mm pitch (gates must
resolve grams of centrifugal force against the same 0.2-1 N PLA stiction that
killed D3/E1, while spinning the miniatures off the board at the ~10 g class
accelerations E1 already showed are incompatible with tabletop play). A seed
that cannot state a one-line gate without contradicting E1/D3 quantities is
not a fresh seed; it is a wish. No gate stated; fails the scopability bar.

## G6 — continuous vacuum-suspension hold (field holds, no latch)

Columns float on a shared vacuum/pressure plenum at commanded heights with no
mechanical memory; selection by per-cell bleed orifices. Arguably outside the
SHA-24 lane (non-overlap: no passive retention of any kind — the field IS the
hold — clean on the letter of the lane). **Excluded at scoping** as
killed-family re-litigation: row 20 drops vacuum/granular-jamming height
fields on product geometry (no deterministic square 5.08 mm columns or
40 mm levels); the plenum is fluid-bus (M1 family); power-off collapses every
column (KC3: no passive hold); 6400 bleed orifices are per-cell fluidic
channels (KC4). Three independent prior kills. No gate stated; row 20 + M1
cover it.

## G7 — consumable gas-generation per cell (effervescent / catalytic charge)

Each column carries a single-use chemical charge; a shared electrical bus
fires selected charges, evolved gas drives the column up the ratchet one
pass per charge set. Non-overlap vs SHA-24 is moot (see below).
**Excluded at scoping**: per-cell charge addressing is 6400 electrical/fluidic
channels (KC4, rows 2/27 class); evolved-gas dosing is irreversible and
consumable, so down-reset needs charge replacement by hand (worse than
full-reset-only, KC5); gas pressure in an FDM PLA cup leaks through porosity
(M1's KC4 porosity kill). A display needing 6400 replacement charges per map
is a consumable, not a product. No gate stated; unproductizable at scoping.

(End of file - total 7 seeds attempted, 0 advanced)
