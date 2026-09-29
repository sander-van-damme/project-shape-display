# SHA-24 competing-architecture verdict — G1 scanning screw-matrix: REJECTED on rate

> Status: screen COMPLETE. ONE genuinely different mechanism developed to
> full comparable evidence (shared spindle-bar actuation + positional
> selection + self-locking-thread brake retention — not A1's toggle latch,
> not A7-V's camshaft, not S1/S4 teeth): advanced to its cheapest analytic
> test (`06-experiments/test22_sms_screen/sms_gate.py --gate`, 5/5) and
> REJECTED on the binding rate gate with cost/silent corroboration.
> No CAD/BOM/procurement beyond the gate per the falsification-first brief.
> Evidence class: CALCULATION over design-criteria geometry + textbook
> thread mechanics + sourced-class actuator ratings. DND-27: no print,
> purchase, or measurement. Ranges with stated confidence; residual
> uncertainty explicit.
> Reproduce: `python 06-experiments/test22_sms_screen/sms_gate.py --gate`
> Sketch: [`04-architecture-candidates/sha24-sms-screen.md`](../04-architecture-candidates/sha24-sms-screen.md).
> S5-R, A1, S6-LC packages untouched.

## Kill criteria (up front, same KC1-KC5 frame as SHA-15/16/17/19)

| ID | Gate | Kill line |
|---|---|---|
| KC1 cost | purchased total must beat A1 ($181); meaningful beat <= ~$171 (>= $10 clear) | nominal >= $181 kills |
| KC2 timing | sustained full-map cycle < 30 s incl. reset/switching/settle/verify | spindles-needed > 16-bar ceiling at the optimistic corner kills |
| KC3 silent | structurally zero silent cells, or cell-resolving verify with retry | open-loop 6,400-silent as drawn kills; reader-fitted variant collapses into KC1 |
| KC4 complexity/print | X1C + PLA baseline, 0.4 mm nozzle; no sub-mm precision repeated 6400x | 0.5 mm thread flanks 6,400x recorded; rotation time kills first, no coupon spent |
| KC5 regional | local reveal without full-board reset | cell-granular in principle, serial-slow in practice (moot once KC2 kills) |

Cheapest-rejecting analysis first: turn-count x spindle-parallelism
arithmetic before any BOM/CAD (this note); E3's serial touch-rate kill does
not bind here — the rotation-time bound does and is computed fresh.

## Screen (80x80 = 6400 cells, 40 mm travel, 5 states)

**G1 — scanning multi-spindle screw columns + self-locking thread brake:
REJECT (tested, 5/5).** Geometry: static printed screw per cell, printed
captive nut carries the column, XY gantry spindle bar drives addressed nuts
by counted turns (5 turns/full-stroke at the coarsest credible 8 mm
multi-start lead), thread self-lock holds power-off load. Rate (binding,
topology-independent): 5 turns at a generous 1,200 rpm + 0.05 s overhead =
**0.30 s/cell optimistic** (~100x A1's 3 ms toggle) → 1,920 spindle-seconds
per full map → **64 spindles for < 30 s at the most favorable corner vs a
16-spindle buildable bar ceiling; 245 nominal** (KC2, gate checks 1–4).
Cost corroborates: 64 channels × $8 floor = **$512 bar alone > A1 $181
before gantry/reader** (KC1, gate check 5). Silent corroborates: open-loop
turns are a full 6,400 silent set as drawn; fitting the A1-class reader
repeats the A7-V cost trap (KC3). Printability recorded, not spent: 0.5 mm
flanks 6,400× are marginal on a 0.4 mm nozzle and one fused nut is a dead
cell (KC4). Why it could have obsoleted A1: the thread is memory + brake +
load path in one passive element — power-off hold with zero per-cell bought
parts and no latch/ratchet teeth anywhere. Why it fails: counted rotation
is two orders slower per cell than a snap toggle, and parallelism buys back
only at dozens of bought spindles. Dead — park-class reopen trigger only
(see sketch).

## Comparison (corners; confidence in parentheses)

| Dimension | A1 (record) | G1 screw-matrix (tested) |
|---|---|---|
| Purchased | **$181** IDEAL (medium) | $512 bar floor optimistic before gantry/reader (medium — moot, rate kills first) |
| Full-map time | 19.63 s sustained (calc) | 64 spindles optimistic / 245 nominal for <30 s (high, this test) |
| Silent cells | 0, cell-local re-drive (calc) | 6,400 open-loop as drawn; reader-fitted repeats A7-V trap |
| Regional | cell-granular | cell-granular in principle, serial-slow (moot) |
| Baseline fit | X1C+PLA coupons ready | 0.5 mm flanks 6,400x marginal (recorded, untested) |
| Power-off hold | latch compression | thread self-lock (the one genuine win, moot) |

## Advance accounting

Advanced exactly ONE mechanism (G1) to its cheapest analytic test; no
CAD/BOM/procurement beyond the gate. Lane brief complied: one serious
competing architecture carried from concept to comparable evidence, killed
fast with recorded rationale. At most one advanced — exactly one was.

## Residual uncertainty

Lead/speed corners are generous-class (8 mm multi-start printable lead,
1,200 rpm under load, 0.05 s overhead); finer pitch, slower spindles, or
realistic engagement only worsen the 64-spindle floor, none rescue it (the
kill holds at the most favorable corner by 4× on spindle count). Thread
printability, back-drive margin, and wear are recorded unknowns, not tested
— analysis kills first. Nothing here is physical validation. Exploration
queue: G1 carries the speculative twist-lock trigger in the sketch; M2's
(SHA-15), D2's (SHA-16), and E3's (SHA-17) triggers stand. Killed at
tile/board scale and NOT to be re-litigated: A1-A7 as drawn, T1-T5,
M1/M2/M3, D1/D2/D3, E1/E2/E3, F1/F2/F3, G1, and the platen, fluid-bus,
magnetic, thermal-broadcast, electrostatic, gravity, vibratory-conveyor,
phase-change-latch, serial-robot-writer, acoustic-field,
buckling-sheet-snap, chemical-swelling, and screw-matrix families.
Next round needs genuinely new seeds outside ALL of these, or a principled
pause case.
