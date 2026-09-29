# SHA-16 divergent screen round 2 verdict — D1/D2/D3 all REJECTED, queue status

> Status: screen COMPLETE. 3 mechanisms surveyed (compliant platen drive,
> tile-level electrostatic clutches, gravity-drop release — none is A1-A7
> as drawn or T1-T5, and none re-litigates M1/M2/M3). D1 advanced to its
> cheapest analytic test
> (`06-experiments/test19_divergent_screen2/platen_gate.py --gate`, 5/5);
> D2/D3 die on one-line ratio math (cheaper than any script).
> No CAD/BOM/procurement beyond the D1 gate per the task brief.
> Evidence class: CALCULATION over sourced-class prices (2026-09 web sweep,
> ranges not quotations) + textbook physics + SHA-7 assumption-class snap
> forces. DND-27: no print, purchase, or measurement. Ranges with stated
> confidence; residual uncertainty explicit.
> Reproduce: `python 06-experiments/test19_divergent_screen2/platen_gate.py --gate`
> Sketches: [`04-architecture-candidates/sha16-divergent-survey-2.md`](../04-architecture-candidates/sha16-divergent-survey-2.md).
> S5-R, A1, S6-LC packages untouched.

## Kill criteria (up front, same KC1-KC5 frame as SHA-15)

| ID | Gate | Kill line |
|---|---|---|
| KC1 cost | purchased total must beat A1 ($181); meaningful beat <= ~$171 (>= $10 clear) | nominal >= $181 kills; low-corner-only beat with no robustness kills |
| KC2 timing | sustained full-map cycle < 30 s incl. reset/switching/settle/verify | nominal budget >= 20 s kills (nothing left); best-case total >= 30 s kills at every corner |
| KC3 silent | structurally zero silent cells, or cell-resolving verify with retry | bank-coarse-only readback (A5 pattern, thousands silent) kills |
| KC4 complexity/print | X1C + PLA baseline, 0.4 mm nozzle, modular 256 mm; no sub-mm precision repeated 6400x; <= ~64 purchased selection channels | new physics incompatible with the PLA baseline, or per-cell purchased count, kills |
| KC5 regional | local reveal without full-board reset; proposal bound <= 0.10 mm neighbour motion (Q5) | full-reset-only kills as product weakness (moot once KC1/KC2 kill) |

Cheapest-rejecting analysis first throughout: ratio/one-line math before
any script (D2, D3); force x count arithmetic before BOM detail (D1);
timing kills before costing where applicable.

## Survey (80x80 = 6400 cells, 40 mm travel, 5 states)

**D1 — compliant staged-snap column + global platen: REJECT (tested).**
Geometry: 4 stacked printed bistable frustums per column (10 mm each);
one rigid platen compresses the board; a printed shutter mask selects
which columns snap per stroke. Cost: single-pass needs a >= 11.5 kN stage
(optimistic corner) — industrial electric cylinder or hydraulic power
pack, sourced-class floor ~$300 before plumbing (low confidence, wide
range — moot, the margin over A1 $181 is absolute) (KC1). Timing (the
binding kill, topology-independent): mask banking divides force by P but
multiplies strokes to 4 x P; at the optimistic 1.8 N corner with a
generous 1 kN / 20 mm/s actuator, 48 strokes x 1.00 s = **48.0 s > 30 s**;
nominal corner 104 strokes x 1.75 s = **182 s** (KC2, 5/5 gate). The
triangle is closed from below too: the seed's own ~5 N abuse-hold demand
implies >= 32 kN single-pass (bistable hold and snap-through scale
together), so softening the frustums is no exit. Force is the mechanism of
the kill, not a second kill — recorded so nobody re-litigates the S1 force
angle as if D1 were "just" an S1 variant. Silent structure: shutter miss
is per-cell silent with no per-cell readback path (KC3). Printability
corroboration: PLA creep under sustained snap preload was the seed's known
measurement-only unknown — moot now, since analysis kills first; no park
needed and none taken. Regional: mask-strip passes are bank-coarse at best
(KC5, moot). Why it could have obsoleted A1: one actuator replacing the
gantry writer with trivial electrics. Why it fails: 6400 simultaneous snap
forces never fit an affordable stage, and banking converts force into
strokes past the 30 s budget at every corner.

**D2 — electrostatic-clutch shared shaft at tile level: REJECT (one-line).**
Geometry: one motor + shaft; 64 printed electrostatic clutches (200-400 V
across ~50 um dielectric) tap power to tile lead screws. Torque-density
kill: optimistic corner (300 V, polyimide, 40 mm disc, mu 0.3) yields
~2-3 mNm per clutch vs ~60-130 mNm needed to lift 100 loaded columns
through a 2 mm lead — **shortfall ~25-50x optimistic, ~100x+ nominal**
(KC4: physics incompatible with tile-scale power transfer in PLA
packaging). Closing 50x needs ~2 kV (breakdown/safety) or a ~280 mm disc
(larger than the tile) — both absurd, so no corner survives. Corroborating:
64 high-voltage drivers cost back the savings (KC1); charged dielectrics
inhale dust into the 50 um gap (KC4); clutch slip under load is silent
without readback (KC3). Why it could have obsoleted A1: one motor, zero
holding power, 64 printed channels. Why it fails: Coulomb clamping at tile
scale is two orders too weak. Reopen trigger (park-class, speculative):
sourced dielectric/clutch stack demonstrating >= 50 mNm from a <= 40 mm
printed clutch at <= 400 V AND dust-tolerant gap >= 0.2 mm. No follow-up
issue — parked, not queued.

**D3 — gravity-drop selective release + single global lift: REJECT (one-line).**
Geometry: shared motor lifts ALL columns to top; 64 printed release gates
drop selected columns by gravity to catch-ledges over 4 passes. Weight-vs-
stiction kill: a ~2 g printed PLA column has ~0.02 N of drop authority vs
order 0.2-1 N PLA-on-PLA guide stiction — **~10-100x shortfall before dust,
humidity swell, or uncontrolled 0-100 g+ miniature top loads** (KC4:
gravity is not a credible actuator at 5.08 mm PLA scale). Drop-time scatter
makes timing unmodellable (KC2); jammed mid-guide columns are silent wrong
heights (KC3); the lift-all pass with miniatures on the board disturbs
exactly the terrain regional updates must preserve (KC5). Why it could have
obsoleted A1: conceptually the cheapest BOM of the round (one $25 lift +
printed gates, zero holding power). Why it fails: grams cannot drive
sticky PLA guides repeatably 6400 times. No reopen trigger — the ratio has
no rescuing corner (lighter guides jam worse; heavier columns need lift
force back). Dead.

## Comparison (ranges; confidence in parentheses)

| Dimension | A1 (record) | D1 platen (tested) | D2 e-clutch | D3 gravity |
|---|---|---|---|---|
| Purchased | **$181** IDEAL (medium) | $300+ floor, actuator alone (low-medium) | HV drivers kill savings (medium) | ~$25 lift + gates (low-medium, moot) |
| Full-map time | 19.63 s sustained (calc) | 48 s optimistic / 182 s nominal (high, this test) | uncomputed, moot | unmodellable scatter, moot |
| Silent cells | 0, cell-local re-drive (calc) | per-cell shutter miss, no readback | clutch slip, no readback | jammed drops, no readback |
| Regional | cell-granular | bank-coarse passes (weak) | tile-gated (only pass) | lift-all disturbs (fail) |
| Baseline fit | X1C+PLA coupons ready | creep moot; force triangle kills | kV/dust incompatible | stiction incompatible |

## Advance accounting

Advanced exactly ONE mechanism (D1) to its cheapest analytic test; D2/D3
advanced zero steps beyond ratio math; no CAD/BOM/procurement beyond the
D1 gate. Task brief complied. At most one advanced — exactly one was.

## Residual uncertainty

Sourced-class prices are point-in-time equivalents, not quotations; the
$300 big-actuator floor is wide ($300-800) but the margin over $181 at the
floor needs no precision. Snap forces are SHA-7 assumption-class (3.0 N
nominal); the D1 kill holds at the -40% corner (1.8 N) with 18 s of timing
margin, so coupon-measured snap would have to fall ~4x below nominal to
reopen — and that corner contradicts the seed's own 5 N hold demand.
E-clutch/gravity ratios use textbook physics (Coulomb pressure, weight vs
stiction order estimates), not coupled simulation. Nothing here is physical
validation. Exploration queue: D2 carries a speculative reopen trigger
above; D1/D3 are dead with no triggers; M2's trigger (SHA-15) stands.
Next divergent round must seed entirely fresh physics — platen, fluid-bus,
magnetic, thermal, electrostatic, and gravity families are all now killed
at tile/board scale, leaving (unscoped, not claimed): vibration/ratchet
conveyors, chemical/phase-change latching, and external-robot writers.
