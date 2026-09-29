# SHA-19 divergent mechanism sketches, round 4 (candidate record)

> Companion to the verdict note
> [`07-evidence-and-decisions/sha19-divergent-screen-4.md`](../07-evidence-and-decisions/sha19-divergent-screen-4.md).
> Sketches live here per the routing rule (new ideas go in `04`);
> the binding kill math and verdicts live in `07`; the one executed
> analytic test lives in `06-experiments/test21_divergent_screen4/`.
> Evidence class: CALCULATION over sourced-class prices + textbook physics.
> DND-27: no print, purchase, or measurement.
> S5-R, A1, S6-LC packages untouched.

All three mechanisms use physics never scoped in SHA-15/16/17 and are not
A1-A7 as drawn or T1-T5, nor any killed family (platen, fluid-bus,
magnetic, thermal-broadcast, electrostatic, gravity, vibratory-conveyor,
phase-change-latch, serial-robot-writer). No substitution was needed:
each of acoustic, buckling-sheet, and chemical-swelling is coherent
enough at 5.08 mm pitch to state a one-line gate (acoustic wavelength
~8.6 mm vs 5.08 mm pitch is tight but scopable as a shared field;
domes and swell capsules both fit the cell footprint), so all three are
surveyed as named in the SHA-18 close-out.

## F1 — acoustic levitation / acoustic sorting field + printed ratchet memory

Each of the 6400 columns sits in a smooth printed guide with a light
reflector disc under it. One shared ultrasonic phased array (40 kHz
class, ~100+ transducers under or over the board) sustains a standing-wave
field; per-cell printed shutters or phase-mask channels (64 tile channels)
select which columns couple to the field on each pass, stepping them up a
printed ratchet ladder (4 steps = 5 states, S1-style unary). Memory and
miniature load live in the ratchet; sound only moves, never holds.
Regional reveal = enable one tile's coupling mask while the rest stay
detuned. Why it could have obsoleted A1: the entire lift-energy subsystem
is one contactless field with no per-cell wiring, no wear faces, and no
moving writer — the gantry becomes a speaker board.

Force structure (the binding dimension): acoustic radiation force on a
5x5 mm reflector at the maximum sustained air pressure before
nonlinearity (~2-5 kPa class) is F = p*A ~= 0.05-0.125 N optimistic —
against 0.02 N weight PLUS 0.2-1 N PLA-on-PLA guide stiction, i.e.
**~2-20x shortfall before dust, humidity, or any miniature top load**,
and two orders below the 5 N abuse-hold the ratchet must still provide
(D1-pattern floor-ceiling collision, field domain). A populated board
cannot be sonicated harder without rattling the very miniatures it
carries, and power-off collapses every unlatched column (no passive hold
during the pass). Selectivity is the second independent kill: at 40 kHz
λ ~= 8.6 mm with ~4.3 mm node spacing, per-cell selective foci on a
5.08 mm grid need sub-wavelength control over 6400 sites from one array
— uncredible without per-cell hardware that re-invents the writer.
One-line pressure x area vs stiction ratio kills before any script.

## F2 — buckling-sheet snap array + edge compression + shutter selection

The board is a stack of thin printed sheets, each patterned with an
80x80 array of bistable domes (spherical caps / frustums) on the 5.08 mm
grid. One or two shared edge actuators compress the sheet stack in-plane;
past the buckling threshold, domes snap through out-of-plane, each dome
contributing one height increment. A printed shutter mask per sheet
decides which domes are free to snap on each stroke and which are
blocked. Lift energy is fully shared (edge compression); memory is dome
bistability; selection is the mask. Different from D1 (no rigid platen,
no out-of-plane compression of tall frustums: the stroke element IS an
in-plane-driven sheet dome) and from R05/Q7 (buckling as the full
board-scale stroke array, not a thin selector layer). Why it could have
obsoleted A1: zero per-cell purchased parts, one edge actuator replacing
the gantry, and sheet stacking as a printable-only scaling path.

Stroke-plus-force structure (the binding dimension, executed as the
gate): a stable snap dome on a <= 4.6 mm footprint rises only a fraction
of its diameter (~0.3-0.5x, i.e. ~1.4-2.3 mm optimistic), so one sheet
cannot deliver 40 mm — **>= 18 stacked sheets are needed at the
optimistic corner**, an unbuildable laminate with 18 mask layers and
compounded registration. Force closes the triangle from the other side:
every dome snapping on a stroke loads the edge actuator simultaneously
(6400 x F_snap, SHA-7 assumption-class 1.8-4.2 N), i.e. >= 11.5 kN even
at the -40% corner — industrial hydraulics, cost kill — and banking to
affordable force multiplies strokes past the 30 s budget at every corner
(D1-pattern triangle, buckling domain). The executed gate
(`06-experiments/test21_divergent_screen4/buckling_gate.py --gate`)
checks all five faces 5/5.

## F3 — chemical-swelling actuation (hydrogel / solvent-swollen elastomer)

Each column carries a printed capsule with a dry hydrogel or
solvent-swollen elastomer slug (~5 mm disc, few mm tall). Cycle: (1) a
shared microfluidic bus (64 tile valves) doses solvent to selected cells;
(2) dosed slugs swell (20-100% linear strain class) and jack their
columns up the printed ratchet over one or more dose passes; (3) venting /
drying (global heat or dry-air purge) shrinks unselected slugs for the
down pass. Memory is the ratchet; load rides on the ratchet; chemistry
only moves. Distinctness from E2 (recorded so nobody claims
re-litigation): E2 was solid-liquid paraffin volumetric latching with
conductive/global heating, killed on Tg collision + latent heat; F3 is
room-temperature diffusive solvent uptake with microfluidic addressing,
killed below on independent diffusion-time + strain-limit physics. Why it
could have obsoleted A1: room-temperature soft actuation with trivial
electrics (one pump + tile valves), zero wear faces, zero holding power.

Diffusion-time structure (the binding dimension): swelling is
diffusion-limited, τ ~ L^2/D with D ~ 1e-9-1e-10 m^2/s for water in gel.
At L ~= 2.5 mm (half-pitch slug) τ ~= **1.7-17 hours per swell or
deswell**; even an optimistic 0.5 mm thin-film slug needs minutes per
pass, against 4 passes inside 30 s — **shortfall ~10-1000x at the most
favorable corner**. Strain corroborates: 20-100% linear swell needs a
>= 40 mm dry stack for 40 mm stroke (doubling the package) or
unphysical 10x gels. Addressing is the second independent kill:
per-cell dosing = 6400 fluidic channels (KC4); 64 tile valves re-invent
the M1 valve bill ($128-320) with added seals FDM PLA cannot provide
(porous, KC4); global flooding = full-reset-only (KC5). A half-swollen
slug creeps under load invisibly (KC3). One-line τ math kills before any
script.
