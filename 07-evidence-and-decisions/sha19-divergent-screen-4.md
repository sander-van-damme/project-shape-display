# SHA-19 divergent screen round 4 verdict — F1/F2/F3 all REJECTED, queue status

> Status: screen COMPLETE. 3 mechanisms surveyed from entirely fresh
> physics (acoustic field transport, buckling-sheet snap arrays,
> chemical-swelling actuation — none is A1-A7 as drawn or T1-T5, and
> none re-litigates M1/M2/M3, D1/D2/D3, or E1/E2/E3 as drawn). F2
> advanced to its cheapest analytic test
> (`06-experiments/test21_divergent_screen4/buckling_gate.py --gate`,
> 5/5); F1/F3 die on one-line ratio math (cheaper than any script).
> No CAD/BOM/procurement beyond the F2 gate per the task brief.
> No substitution was needed: all three named seeds proved coherent
> enough at 5.08 mm pitch to state a fresh one-line gate each.
> Evidence class: CALCULATION over sourced-class prices (2026-09 class
> sweep, ranges not quotations) + textbook physics + design-criteria
> geometry + SHA-7 assumption-class snap forces. DND-27: no print,
> purchase, or measurement. Ranges with stated confidence; residual
> uncertainty explicit.
> Reproduce: `python 06-experiments/test21_divergent_screen4/buckling_gate.py --gate`
> Sketches: [`04-architecture-candidates/sha19-divergent-survey-4.md`](../04-architecture-candidates/sha19-divergent-survey-4.md).
> S5-R, A1, S6-LC packages untouched.

## Kill criteria (up front, same KC1-KC5 frame as SHA-15/16/17)

| ID | Gate | Kill line |
|---|---|---|
| KC1 cost | purchased total must beat A1 ($181); meaningful beat <= ~$171 (>= $10 clear) | nominal >= $181 kills; low-corner-only beat with no robustness kills |
| KC2 timing | sustained full-map cycle < 30 s incl. reset/switching/settle/verify | nominal budget >= 20 s kills (nothing left); best-case total >= 30 s kills at every corner |
| KC3 silent | structurally zero silent cells, or cell-resolving verify with retry | bank-coarse-only readback (A5 pattern, thousands silent) kills |
| KC4 complexity/print | X1C + PLA baseline, 0.4 mm nozzle, modular 256 mm; no sub-mm precision repeated 6400x; <= ~64 purchased selection channels | new physics incompatible with the PLA baseline, or per-cell purchased count, kills |
| KC5 regional | local reveal without full-board reset; proposal bound <= 0.10 mm neighbour motion (Q5) | full-reset-only kills as product weakness (moot once KC1/KC2 kill) |

Cheapest-rejecting analysis first throughout: pressure x area and
diffusion-time one-line ratios before any script (F1, F3); dome-stroke
plus force x count arithmetic before BOM detail (F2); timing kills
before costing where applicable.

## Survey (80x80 = 6400 cells, 40 mm travel, 5 states)

**F1 — acoustic levitation / sorting field + printed ratchets: REJECT (one-line).**
Geometry: shared 40 kHz phased array sustains a standing-wave field;
64 tile shutter channels select which columns couple per pass; printed
ratchets store height and carry miniature load. Force kill: radiation
pressure at the maximum sustained air level (~2-5 kPa class) on a 5x5 mm
reflector gives ~0.05-0.125 N optimistic vs 0.02 N weight PLUS 0.2-1 N
PLA guide stiction — **~2-20x shortfall before dust, humidity, or top
loads**, and two orders below the 5 N abuse-hold the ratchet must keep
(KC4: the D1 floor-ceiling collision in the field domain — softening
guides to help the field surrenders hold). Power-off collapses every
unlatched column (no passive hold during the pass). Selectivity second
kill: λ ~= 8.6 mm with ~4.3 mm node spacing cannot hold per-cell
selective foci on a 5.08 mm grid from one shared array without per-cell
hardware that re-invents the writer (KC4). Array cost corroborates:
100+ transducers x $1-3 + drivers cost back the gantry savings (KC1).
Silent: a dropped or node-hopped column is invisibly wrong with no
per-cell readback (KC3). Why it could have obsoleted A1: one
contactless field replacing all lift wiring and the moving writer. Why
it fails: sound pressure is two orders too weak to throw grams uphill
against sticky PLA guides. Dead — no reopen trigger (no acoustic corner
lifts 0.5 N stiction per cell while leaving miniatures undisturbed).

**F2 — buckling-sheet snap array + edge compression: REJECT (tested).**
Geometry: stacked printed dome sheets (80x80 domes each) snapped by
shared in-plane edge compression; shutter mask per sheet selects domes
per stroke. Stroke kill (binding, topology-independent): a stable dome
on a <= 4.6 mm footprint rises ~0.3-0.5 diameters, i.e. **~1.4-2.3 mm
optimistic vs 40 mm travel — an order short**, so >= 18 stacked sheets
with 18 mask layers are needed at the optimistic corner (gate checks
1-2, 5/5). Force closes the triangle from the other side: 6400 domes x
1.8 N optimistic = **11.5 kN single-pass edge load** (gate check 3) —
industrial hydraulics with a sourced-class floor ~$300 before
sheets/masks/frame, over A1 $181 (KC1, gate check 5). Banking to a
generous 1 kN stage needs 48 strokes even under the unphysical 4-sheet
fiction x 1.00 s = **48 s > 30 s**; the true 18-sheet stack needs
200+ strokes (KC2, gate check 4, 5/5 gate). Silent structure: shutter
miss / unsnapped dome is per-cell silent with no per-cell readback
(KC3). Printability corroboration: PLA creep under sustained bistable
preload was the known measurement-only unknown — moot, analysis kills
first; no park needed. Regional: mask passes are bank-coarse at best
(KC5, moot). Why it could have obsoleted A1: zero per-cell purchased
parts with one edge actuator. Why it fails: domes are too shallow for
the stroke and too strong in aggregate for the stage — the D1 triangle
in the buckling domain. Dead — no reopen trigger (the stroke and force
quantities are the same snap physics; softening domes surrenders hold
as in D1).

**F3 — chemical-swelling actuation + microfluidic bus: REJECT (one-line).**
Geometry: hydrogel/solvent-swollen slug per column jacks the ratchet
over dose passes; 64 tile microfluidic valves address; ratchet holds
load. Distinctness from E2 (recorded so nobody claims re-litigation):
E2 was paraffin solid-liquid latching with global heating, killed on Tg
collision + latent heat; F3 is room-temperature diffusive uptake with
fluidic addressing, killed below on independent diffusion + strain
physics. Time kill: τ ~ L^2/D with D ~ 1e-9-1e-10 m^2/s; at L ~= 2.5 mm
τ ~= **1.7-17 hours per swell/deswell, minutes even for an optimistic
0.5 mm film** — against 4 passes inside 30 s, **shortfall ~10-1000x at
the most favorable corner** (KC2 by orders). Strain corroborates:
20-100% linear swell needs a >= 40 mm dry stack for 40 mm stroke
(KC4 packaging). Addressing second kill: per-cell dosing = 6400 fluidic
channels (KC4); 64 tile valves re-invent the M1 valve bill ($128-320)
plus seals FDM PLA cannot provide (porous, KC4); global flooding =
full-reset-only (KC5). Silent: half-swollen creep under load invisible
(KC3). Why it could have obsoleted A1: room-temperature soft lift with
trivial electrics. Why it fails: diffusion is hours, not seconds, at
millimetre scale. Dead — no reopen trigger (no gel corner swells 40 mm
in seconds at pitch while shrinking back on command).

## Comparison (ranges; confidence in parentheses)

| Dimension | A1 (record) | F1 acoustic (one-line) | F2 buckling (tested) | F3 swelling (one-line) |
|---|---|---|---|---|
| Purchased | **$181** IDEAL (medium) | 100+ transducers + drivers kill savings (medium) | $300+ floor, actuator alone (low-medium) | valves + pump re-invent M1 bill (medium) |
| Full-map time | 19.63 s sustained (calc) | uncomputed, moot | 48 s optimistic fiction / 200+ true-stack (high, this test) | hours per swell; minutes optimistic film (high, this test) |
| Silent cells | 0, cell-local re-drive (calc) | dropped/node-hop, no readback | shutter miss/unsnapped dome, no readback | half-swollen creep, no readback |
| Regional | cell-granular | tile-mask (only pass) | bank-coarse passes (weak) | tile-dosed / flood-reset (fail) |
| Baseline fit | X1C+PLA coupons ready | field vs stiction/miniatures (fail) | 18-sheet laminate + creep moot (fail) | diffusion + PLA porosity (fail) |

## Advance accounting

Advanced exactly ONE mechanism (F2) to its cheapest analytic test; F1/F3
advanced zero steps beyond one-line ratio math; no CAD/BOM/procurement
beyond the F2 gate. Task brief complied. At most one advanced — exactly
one was.

## Residual uncertainty

Sourced-class prices are point-in-time equivalents, not quotations; the
$300 big-actuator floor is wide ($300-800) but the margin over $181 at
the floor needs no precision. Snap forces are SHA-7 assumption-class
(3.0 N nominal); the F2 kill holds at the -40% corner (1.8 N) with 18 s
of timing margin on the 4-sheet fiction, so coupon-measured snap would
have to fall ~4x below nominal to reopen — and that corner contradicts
the 5 N hold demand. Dome-rise ratios (0.3-0.5x diameter) are textbook
bistability class, not coupon measurements; acoustic-pressure (2-5 kPa),
stiction (0.2-1 N), PLA Tg, and gel diffusivity (1e-9-1e-10 m^2/s) are
order estimates, not coupled simulation — all F1/F3 kills hold at the
most favorable corner by >= 10x, so measurement could not rescue them.
Nothing here is physical validation. Exploration queue: NO new parked
triggers from this round (F1/F2/F3 all dead); M2's (SHA-15), D2's
(SHA-16), and E3's (SHA-18) speculative triggers stand. Killed at
tile/board scale and NOT to be re-litigated: A1-A7 as drawn, T1-T5,
M1/M2/M3, D1/D2/D3, E1/E2/E3, F1/F2/F3, and the platen, fluid-bus,
magnetic, thermal-broadcast, electrostatic, gravity, vibratory-conveyor,
phase-change-latch, serial-robot-writer, acoustic-field,
buckling-sheet-snap, and chemical-swelling families. Next divergent
round must seed physics outside ALL of these — the named unscoped space
from SHA-18 is now exhausted, so round 5 needs genuinely new seeds (or
a principled pause case) with a fresh one-line gate before any script.
