# SHA-15 divergent screen verdict — M1/M2/M3 all REJECTED, queue reseeded

> Status: screen COMPLETE. 3 fundamentally different mechanisms surveyed
> (fluid power bus, field selection, optothermal broadcast — none is A1-A7
> as drawn or T1-T5). M1 advanced to its cheapest analytic test
> (`06-experiments/test18_divergent_screen/pneumatic_gate.py --gate`, 5/5);
> M2/M3 die on one-line count x unit math (cheaper than any script).
> No CAD/BOM/procurement beyond the M1 gate per the task brief.
> Evidence class: CALCULATION over sourced-class prices (2026-09 web sweep,
> ranges not quotations) + textbook physics. DND-27: no print, purchase, or
> measurement. Ranges with stated confidence; residual uncertainty explicit.
> Reproduce: `python 06-experiments/test18_divergent_screen/pneumatic_gate.py --gate`
> Sketches: [`04-architecture-candidates/sha15-divergent-survey.md`](../04-architecture-candidates/sha15-divergent-survey.md).
> S5-R, A1, S6-LC packages untouched.

## Kill criteria (up front)

| ID | Gate | Kill line |
|---|---|---|
| KC1 cost | purchased total must beat A1 ($181); meaningful beat <= ~$171 (>= $10 clear) | nominal >= $181 kills; low-corner-only beat with no robustness kills |
| KC2 timing | sustained full-map cycle < 30 s incl. reset/switching/settle/verify | nominal air/thermal budget >= 20 s kills (nothing left); best-case total >= 30 s kills at every corner |
| KC3 silent | structurally zero silent cells, or cell-resolving verify with retry | bank-coarse-only readback (A5 pattern, thousands silent) kills |
| KC4 complexity/print | X1C + PLA baseline, 0.4 mm nozzle, modular 256 mm; no sub-mm precision repeated 6400x; <= ~64 purchased selection channels | new physics incompatible with the PLA baseline, or per-cell purchased count, kills |
| KC5 regional | local reveal without full-board reset; proposal bound <= 0.10 mm neighbour motion (Q5) | full-reset-only kills as product weakness (moot once KC1/KC2 kill) |

Cheapest-rejecting analysis first throughout: count x unit-cost
multiplication before any script (M2, M3); volume/flow arithmetic before
BOM detail (M1); timing kills before costing where applicable.

## Survey (80x80 = 6400 cells, 40 mm travel, 5 states)

**M1 — shared-pneumatic bladder + 64 tile valves: REJECT (tested).**
Geometry: one bladder (or 8 bank bladders) lifts; 64 tile 3/2 valves gate
air per 10x10 tile; printed threshold ratchets store height and carry
miniature load. Cost (sourced-class): pump $21-25 + 64 valves x $2-5
($128-320) + fittings/tubing/regulator $20-40 = **$169 / $245 / $385**
(low/nominal/high; valve-price confidence medium-low). Nominal-over A1 by
$64 (KC1). Timing (the binding kill, topology-independent): 4 x 10 mm
strokes displace 6.4 L total; banking does NOT reduce total air (gate
asserts 6.40 L == 6.40 L — it bounds peak force only). At 12-15 L/min
free flow derated 60-90% under load: fill band **25.6 / 37.9 / 53.3 s for
air-fill ALONE**; best-case fill + vent + 2 s allowance = **40.4 s > 30 s
at every corner** (KC2, 5/5 gate). Force is explicitly NOT the killer
(4800 N at 30 kPa >> 2.4 kN worst case — recorded so nobody re-litigates
the S1 force angle). Silent structure: ratchet miss still per-cell silent,
plus a NEW correlated mode (slow leak sags a whole bank silently) — worse
than A1 (KC3). Printability second kill: airtight chamber needs a flexible
membrane + seals outside the X1C+PLA baseline (FDM PLA is porous) (KC4).
Regional (the one passing dimension): tile-branch pressurization isolates
well — moot. Why it could have obsoleted A1: single $23 pump replacing
gantry/stepper lift energy with trivial electrics. Why it fails: air is
too slow per litre at this scale and tile valves cost back the savings.

**M2 — permanent-magnet bistable columns + tile-parallel writer: REJECT
(one-line).** Geometry: 1+ ferrite discs per column snapping between
keeper seats; Halbach bar writes contactlessly through printed shutters.
Cost: cheapest sourced ferrite 5 mm disc $0.03-0.18 ea (bulk vs retail;
medium confidence) x 6400 = **$192 floor at the absolute cheapest corner
— already > $181 before the 64-driver writer comb ($192-512), keeper
steel, or anything else** (KC1, no script needed). 5-state encoding needs
up to 4 magnetic elements per cell, which quadruples the floor. Timing:
travelling-bar schedule could pass — moot. Silent: stuck magnet invisible
without readback; stray fields + steel hardware/dice/debris near the
surface (KC3). Crosstalk second kill: 5 mm magnets on 5.08 mm pitch couple
to neighbours unavoidably; selective write needs field gradients over
< 5 mm from a travelling bar — marginal analytically (KC4). Why it could
have obsoleted A1: zero wear, zero hold power, zero snap-force variation.
Why it fails: magnet count x unit cost kills before physics matters.
Reopen trigger (park-class, speculative): bonded-ferrite printable medium
with sourced effective cost < $0.01/cell AND measured neighbour-coupling
below a 2x selective-write threshold. No follow-up issue — parked, not queued.

**M3 — optothermal SMA broadcast via projector: REJECT (two independent
kills).** Geometry: 1 SMA U-wire per column toggles a printed latch per
thermal flash; 4 flashes = 5 states; a single projector addresses all
6400 wires optically. Cost kill 1: bulk Nitinol $1-2/m (low) to Flexinol
$2.50/ft retail; 0.1 m/cell -> **$0.10-0.83/cell -> $640-5300 floor, over
the $500 ABSOLUTE ceiling before drivers/crimps/projector** (KC1).
Material kill 2 (independent of price): SMA activation needs 70-90 °C
(Flexinol LT/HT datasheet) while the fabrication baseline is PLA
(Tg ~55-60 °C) — the actuator cooks its own mechanism; thermal crosstalk
at 5.08 mm pitch in a low-conductivity plastic array makes selective
70 °C+ addressing of one cell without softening neighbours uncredible
(KC4). Timing corroborates: Flexinol-class cooling 0.5-13 s/cycle (datasheet
off-times) x 4 cycles + settle leaves no robust margin, and forced-air
cooling of 6400 cells is a new subsystem (KC2). Silent: fatigued wire
fails to contract invisibly; resistance drift (KC3). Why it could have
obsoleted A1: exactly one purchased active component, zero wiring.
Why it fails: per-cell SMA count cost plus activation-vs-PLA physics.

## Comparison (ranges; confidence in parentheses)

| Dimension | A1 (record) | M1 pneumatic (tested) | M2 magnetic | M3 SMA |
|---|---|---|---|---|
| Purchased | **$181** IDEAL (medium) | $245 nominal, $169 low-only (medium-low) | $192 floor before writer (medium) | $640+ floor (medium) |
| Full-map time | 19.63 s sustained (calc) | 40.4 s best-case (high, this test) | uncomputed, moot | uncomputed, moot |
| Silent cells | 0, cell-local re-drive (calc) | per-cell + correlated bank-sag (worse) | thousands w/o readback | thousands w/o readback |
| Regional | cell-granular | tile-isolated (only pass) | tile/writer-dependent | flash-global (full reset) |
| Baseline fit | X1C+PLA coupons ready | needs membrane/seals (fail) | pitch crosstalk (fail) | cooks PLA (fail) |

## Advance accounting

Advanced exactly ONE mechanism (M1) to its cheapest analytic test; M2/M3
advanced zero steps beyond count x unit math; no CAD/BOM/procurement
beyond the M1 gate. Task brief complied.

## Residual uncertainty

Sourced-class prices are point-in-time equivalents, not quotations; valve
$2-end quality, pump derate under pulsatile load, and line/leak losses are
unmodeled — all worsen M1, none rescue it (best corner already fails by
10 s). SMA/PLA thermal bounds use datasheet activation vs textbook Tg, not
coupled simulation. Nothing here is physical validation. Exploration queue:
D1/D2 seeds named in the `04` survey note are unworked hypotheses, not
claims; M2 carries a speculative reopen trigger above.
