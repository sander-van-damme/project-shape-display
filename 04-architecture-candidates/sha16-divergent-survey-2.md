# SHA-16 divergent mechanism sketches, round 2 (candidate record)

> Companion to the verdict note
> [`07-evidence-and-decisions/sha16-divergent-screen-2.md`](../07-evidence-and-decisions/sha16-divergent-screen-2.md).
> Sketches live here per the routing rule (new ideas go in `04`);
> the binding kill math and verdicts live in `07`; the one executed
> analytic test lives in `06-experiments/test19_divergent_screen2/`.
> Evidence class: CALCULATION over sourced-class prices + textbook physics.
> DND-27: no print, purchase, or measurement.
> S5-R, A1, S6-LC packages untouched.

## D1 — compliant staged-snap column + global compression platen

Each of the 6400 columns is a stack of 4 printed bistable frustums
(conical shells). One 10 mm snap each gives 40 mm in 4 snaps; intermediate
stable states give 5 heights (S1-style unary stepping, but the stroke
element IS the compliant column, not a separate ratchet). One rigid platen
covering the whole 400x400 board compresses downward; a printed shutter
mask per level decides which columns are free to snap through on each
stroke and which are blocked (held at height). Lift energy is fully shared
(one actuator drives the platen); memory is the frustum bistability;
selection is the mask. Different from R05/Q7 (compliance as a thin selector
layer, not the stroke itself) and from M1 (no fluid, no valves: the shared
bus is a rigid plate).

Force structure (the binding dimension): every column that snaps on a given
stroke contributes its snap-through force simultaneously against the platen.
Worst-case full-map change snaps all 6400 frustums on the same stroke, so
platen force = 6400 x F_snap. SHA-7 W4 bounds F_snap as assumption-class
3.0 N nominal, 4.2 N worst (+/-40% spread), with a coupon kill line at
7.14 N; the D1 seed note itself demands holding against ~5 N abuse. Even
the optimistic 1.8 N corner (-40%) puts 11.5 kN on the platen — three
orders above a hobby linear actuator and an order above a NEMA17 lead
screw. Banking (mask enables 1/P of the board per pass, P passes per level)
trades force for strokes: 4 x P platen strokes per map, each 10 mm under
load plus shutter-switch and settle overhead. The executed gate
(`06-experiments/test19_divergent_screen2/platen_gate.py --gate`) shows the
triangle never closes: single-pass needs >= 11.5 kN (industrial hydraulics,
cost kill); banked to affordable force (<= 1 kN) needs >= 48 strokes even
at the optimistic corner (timing kill, >= 84 s vs 30 s). Softening the
frustums to cut F_snap surrenders the 5 N abuse-hold the seed demands —
the floor and the ceiling are the same quantity.

## D2 — electrostatic-clutch shared shaft at tile level (64 clutches)

R09 inspiration moved from cell to tile: one motor spins a single long
drive shaft (or one per 10-row bank); each 10x10 tile taps power through an
electrostatic clutch — two printed electrode discs (one shaft-side, one
tile lead-screw side) separated by a thin dielectric film. Charging the
pair to 200-400 V clamps them by electrostatic pressure
P = e0*er*V^2/(2*d^2); discharging releases. 64 clutch channels replace
6400 actuators; when engaged, a tile's lead screw lifts its 100 columns
(two height latches per column, S1-style, or a tile ratchet ladder).
Selection is field clamping, holding is mechanical — no holding power, no
per-cell wiring, one motor. Different physics from D1 (field, not platen)
and from M2 (Coulomb clamping through a dielectric, not magnet detents;
no permanent magnets, no travelling writer).

Torque-density structure (the binding dimension): optimistic corner —
300 V across 50 um polyimide (er ~ 3.4), 40 mm clutch disc, mu 0.3 —
yields ~540 Pa x 1.26e-3 m^2 x 0.3 x 13 mm effective radius ~= 2-3 mNm
per clutch. One tile lead screw lifting 100 loaded columns (~1-2 N each
with friction) through a 2 mm lead needs ~60-130 mNm: shortfall factor
~25-50x at the optimistic corner, ~100x+ nominal (200 V, dust-thickened
gap, humidity-derated dielectric). Closing 50x needs either ~2 kV
(dielectric breakdown, safety, driver cost) or a ~280 mm clutch disc
(larger than the tile) — both absurd. Corroborating kills: 64 channels of
200-400 V drive electronics cost back any savings (KC1); charged
dielectrics attract dust into the 50 um gap at exactly the 5.08 mm-pitch
dust scale (KC4); a slipping clutch under load is silent without per-cell
readback (KC3). One-line count x unit-physics math kills before any script.

## D3 — gravity-drop selective release + single global lift (fresh)

New family, not a variant of anything screened: gravity is the free
down-actuator, one shared motor is the up-actuator, selection is
release-only. Cycle: (1) the global lift raises ALL 6400 columns to top
dead centre in one slow shared motion; (2) per-tile release gates (64
printed escapements) drop selected columns by gravity to patterned
catch-ledges at the 4 intermediate heights over 4 drop passes
(binary/unary mask per pass); unreleased columns stay latched at top.
Down-selection costs no energy and needs only 64 low-force gate channels
(the gates hold back grams, they never lift); the single lift motor does
all work against gravity plus friction. Why it could have obsoleted A1:
one ~$25 lift actuator + 64 printed gates + zero per-cell purchased parts
and zero holding power (ledges, not friction) — conceptually the cheapest
bill of materials of any round-2 candidate, with a fully shared lift
simpler than A1's 8-head gantry writer.

Weight-vs-stiction structure (the binding dimension): a printed PLA column
(~5x5x60 mm solid-equivalent with frustum/ledge features, ~1.5-2 cm^3)
weighs ~2 g, i.e. ~0.02 N of drop authority. Sliding stiction of PLA on
PLA in a 5.08 mm-pitch guide with print-variation interference is
order 0.2-1 N (two orders above weight even before dust, humidity swell,
or a miniature standing on the column adding 0-100 g+ of uncontrolled top
load). Gravity cannot reliably start, stop, or land the drop: columns jam
mid-guide (silent wrong heights, KC3), drop times scatter by load (timing
unmodellable, KC2), and the global lift-up pass with miniatures on the
board disturbs the very terrain regional updates must preserve (KC5).
Tilting the board to amplify drop authority couples all 6400 columns to
one tilt angle — the opposite of regional addressing. One-line
weight-vs-friction ratio (~100x shortfall) kills before any script; no
cheaper test exists and none is needed.
