# SHA-25 divergent screen round 5 verdict — no scopable fresh seeds, principled pause case

> Status: screen COMPLETE. 7 G-series seeds attempted against the freshness
> filter (ALL killed families) and the SHA-24 lane filter (shared actuation
> with passive selection/state retention). 0 survived scoping; 0 advanced to
> any gate (task allows at most one — complied). No CAD/BOM/procurement.
> This note files the principled pause case the task brief sanctions instead
> of filler, with resume triggers and the updated killed-family record.
> Evidence class: CALCULATION-CLASS scoping over killed-family kill
> quantities + topology-table dispositions + lane definition. DND-27: no
> print, purchase, or measurement. Ranges with stated confidence; residual
> uncertainty explicit.
> Sketches: [`04-architecture-candidates/sha25-divergent-survey-5.md`](../04-architecture-candidates/sha25-divergent-survey-5.md).
> S5-R, A1, S6-LC packages untouched.

## Kill criteria (up front, same KC1-KC5 frame as SHA-15/16/17/19)

| ID | Gate | Kill line |
|---|---|---|
| KC1 cost | purchased total must beat A1 ($181); meaningful beat <= ~$171 (>= $10 clear) | nominal >= $181 kills; low-corner-only beat with no robustness kills |
| KC2 timing | sustained full-map cycle < 30 s incl. reset/switching/settle/verify | nominal budget >= 20 s kills (nothing left); best-case total >= 30 s kills at every corner |
| KC3 silent | structurally zero silent cells, or cell-resolving verify with retry | bank-coarse-only readback (A5 pattern, thousands silent) kills |
| KC4 complexity/print | X1C + PLA baseline, 0.4 mm nozzle, modular 256 mm; no sub-mm precision repeated 6400x; <= ~64 purchased selection channels | new physics incompatible with the PLA baseline, or per-cell purchased count, kills |
| KC5 regional | local reveal without full-board reset; proposal bound <= 0.10 mm neighbour motion (Q5) | full-reset-only kills as product weakness (moot once KC1/KC2 kill) |

Cheapest-rejecting analysis first: this round the cheapest test was the
two-filter scoping check itself (freshness + lane), applied before any ratio
math. Five seeds died on documented prior quantities without new arithmetic
needed; one (G1) died on lane ownership; one (G5) died on unscopability.

## Survey (80x80 = 6400 cells, 40 mm travel, 5 states)

**G1 photochemical latch: EXCLUDED at scoping (SHA-24 lane collision).**
Shared lift + passive cured retention is the challenger's owned lane by
definition; corroborating fluidic-addressing (M1/row-27), irreversibility
(KC5), and silent-creep (KC3) exclusions recorded in the `04` note.

**G2 per-cell piezo/solenoid: EXCLUDED at scoping (rows 1-2 + magnetic family).**
Count x unit floor ($3,200+ class) and pitch-fit kills pre-date this round.

**G3 manual-direct hand setting: EXCLUDED at scoping (E3 family, worse corner).**
Human ~1 s/cell = ~6400 s/map, ~200x over budget; E3's gated rate kill binds
a fortiori; row 22 concurs.

**G4 hygroscopic swelling: EXCLUDED at scoping (F3 re-litigation).**
Same diffusion-time quantities, same addressing kill, different solvent.

**G5 centrifugal selection: EXCLUDED at scoping (unscopable).**
Cannot state a one-line gate without contradicting E1/D3 quantities; spin
accelerations incompatible with miniatures on board.

**G6 vacuum-suspension hold: EXCLUDED at scoping (row 20 + M1 + KC3).**
Three independent prior kills (geometry, fluid-bus, power-off collapse).

**G7 consumable gas generation: EXCLUDED at scoping (unproductizable).**
6400 consumable charges per map + PLA porosity + no reset path.

## Comparison (ranges; confidence in parentheses)

| Dimension | A1 (record) | G1-G7 (this round) |
|---|---|---|
| Purchased | **$181** IDEAL (medium) | none credibly below at scoping (high — prior quantities bind) |
| Full-map time | 19.63 s sustained (calc) | G3 ~6400 s by hand; rest uncomputed, moot |
| Silent cells | 0, cell-local re-drive (calc) | G1/G6 silent modes pre-killed (medium) |
| Regional | cell-granular | none offered anything above A1's bar |
| Baseline fit | X1C+PLA coupons ready | G1/G7 resin/gas vs PLA porosity (fail, prior) |

## Advance accounting

Advanced ZERO mechanisms to any gate (no script, no CAD, no BOM). Task brief
complied: at most one advanced, and none survived scoping to deserve it.
Advancing any G-seed past its documented prior kill would have been filler,
which the brief explicitly forbids.

## Principled pause case (not abandonment)

**Claim:** broad fresh-seed search at tile/board scale under the current
requirements + baseline has exhausted its scopable space. Rounds SHA-15
through SHA-19 killed 12/12 mechanisms across every transducer family with
kill margins >= 10x at the most favorable corner; the `04` topology table
independently drops per-cell actuation, serial writers, manual media,
vacuum fields, fluidic decoders, wedge strips, and tendon-per-cell; and the
SHA-24 lane now owns the one remaining structurally distinct allocation
(shared drive + passive retention). The 7 attempts above show the residue:
lane collisions, prior-family re-litigations at equal-or-worse corners, or
unscopable wishes. Continuing to spin fresh-seed rounds on this quarter's
evidence cannot beat A1 $181 / 30 s / zero-silent; capacity is better spent
on exploitation (A1/S5-R), the SHA-24 verdict, and trigger monitoring.

**Resume triggers (any one re-opens divergent search):**

1. Parked triggers fire on new evidence — M2 (SHA-15: printable-magnet medium
   < $0.01/cell with measured neighbour decoupling), D2 (SHA-16: >= 50 mNm
   from <= 40 mm printed clutch at <= 400 V with >= 0.2 mm dust-tolerant gap),
   E3 (SHA-18: writer-rate breakthrough), SHA-24 G1 (bayonet medium >= 40 mm
   lead with <= 50 ms dwell). Re-test ONLY the triggered family, on the
   stated evidence.
2. A new sourced transducer medium with a published quantity that moves a
   kill ratio (force, time constant, cost/cell, torque density) by >= 10x vs
   the corner assumed in its verdict.
3. Requirement relaxation (slower full-map budget, fewer cells, higher cost
   ceiling) or fabrication-baseline change (sealed fluidics, sub-0.4 mm
   precision, non-PLA structural process) that invalidates a KC-line premise.
4. SHA-24 verdict lands: if the challenger lane itself is killed, its
   embodiment lessons (not its lane) become reusable constraints for the next
   seed attempt; if it survives, exploration targets the delta it leaves.

**Parked-trigger standing re-affirmed:** M2, D2, E3 triggers stand unchanged;
no new evidence was presented this round, so none was re-tested per the brief.

## Residual uncertainty

Scoping judgments reuse prior rounds' assumption-class quantities (stiction,
diffusivity, rate corners) rather than re-deriving them; if any single prior
kill quantity is wrong by >= 10x, its family re-opens — but no evidence this
round suggests such an error, and DND-27 forbids the measurement that could
show it. Lane-boundary judgments (G1/G4) interpret SHA-24's lane grant
broadly by design (shared-energy + passive-hold in any transducer); a
narrower Board reading could free G1-class photochemistry, but its
corroborating fluidic/irreversibility exclusions would still bind. Nothing
here is physical validation.

## Killed-family record (cumulative, binding on future rounds)

Killed at tile/board scale, NOT to be re-litigated without trigger evidence:
A1-A7 as drawn, T1-T5, M1/M2(player parked trigger)/M3, D1/D2(parked)/D3,
E1/E2/E3(parked, gated 5/5), F1/F2(gated 5/5)/F3, G1(lane-owned by SHA-24)/
G2(rows 1-2, magnetic)/G3(E3-rate)/G4(F3-diffusion)/G5(unscopable)/
G6(row-20, fluid-bus)/G7(unproductizable), and the platen, fluid-bus,
magnetic, thermal-broadcast, electrostatic, gravity, vibratory-conveyor,
phase-change-latch, serial-robot-writer, acoustic-field, buckling-sheet-snap,
chemical-swelling, per-cell-bought-actuator, manual-media, vacuum-field,
photochemical-latch (lane-owned), hygroscopic-swelling, centrifugal, and
consumable-gas families.
