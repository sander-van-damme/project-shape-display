# SHA-17 divergent screen round 3 verdict — E1/E2/E3 all REJECTED, queue status

> Status: screen COMPLETE. 3 mechanisms surveyed from entirely fresh
> physics (inertial stick-slip transport, solid-liquid phase-change
> latching, off-board robotic setting — none is A1-A7 as drawn or
> T1-T5, and none re-litigates M1/M2/M3 or D1/D2/D3 as drawn). E3
> advanced to its cheapest analytic test
> (`06-experiments/test20_divergent_screen3/writer_rate_gate.py --gate`,
> 5/5); E1/E2 die on one-line ratio math (cheaper than any script).
> No CAD/BOM/procurement beyond the E3 gate per the task brief.
> Evidence class: CALCULATION over sourced-class prices (2026-09 class
> sweep, ranges not quotations) + textbook physics + design-criteria
> geometry. DND-27: no print, purchase, or measurement. Ranges with
> stated confidence; residual uncertainty explicit.
> Reproduce: `python 06-experiments/test20_divergent_screen3/writer_rate_gate.py --gate`
> Sketches: [`04-architecture-candidates/sha17-divergent-survey-3.md`](../04-architecture-candidates/sha17-divergent-survey-3.md).
> S5-R, A1, S6-LC packages untouched.

## Kill criteria (up front, same KC1-KC5 frame as SHA-15/16)

| ID | Gate | Kill line |
|---|---|---|
| KC1 cost | purchased total must beat A1 ($181); meaningful beat <= ~$171 (>= $10 clear) | nominal >= $181 kills; low-corner-only beat with no robustness kills |
| KC2 timing | sustained full-map cycle < 30 s incl. reset/switching/settle/verify | nominal budget >= 20 s kills (nothing left); best-case total >= 30 s kills at every corner |
| KC3 silent | structurally zero silent cells, or cell-resolving verify with retry | bank-coarse-only readback (A5 pattern, thousands silent) kills |
| KC4 complexity/print | X1C + PLA baseline, 0.4 mm nozzle, modular 256 mm; no sub-mm precision repeated 6400x; <= ~64 purchased selection channels | new physics incompatible with the PLA baseline, or per-cell purchased count, kills |
| KC5 regional | local reveal without full-board reset; proposal bound <= 0.10 mm neighbour motion (Q5) | full-reset-only kills as product weakness (moot once KC1/KC2 kill) |

Cheapest-rejecting analysis first throughout: force/energy one-line
ratios before any script (E1, E2); serial-rate arithmetic before BOM
detail (E3); timing kills before costing where applicable.

## Survey (80x80 = 6400 cells, 40 mm travel, 5 states)

**E1 — global vibratory stick-slip ratchet conveyor: REJECT (one-line).**
Geometry: sawtooth-ribbed PLA guides (easy-up, hard-down); 1-4
board-wide shakers drive a vertical travelling wave; per-cell wedge
gates (64 tile channels) clamp columns that should ignore the wave.
Force kill: 2 g column vs 0.2-1 N PLA stiction needs peak inertial
acceleration a = F/m = 100-500 m/s^2, i.e. **~10-50 g of board shake
before dust, humidity, or top loads** (KC4: incompatible with the
populated-board product — miniatures slide/topple at ~0.5-1 g lateral,
and 6400 PLA teeth hammered at duty is a wear/fatigue regime, not a
mechanism). Softening the guides surrenders the ~5 N abuse-hold, so
floor and ceiling are the same quantity (D1-pattern collision, friction
domain). Selectivity second kill: the wave is global, so all addressing
lives in 6400 micro-gates each holding back the full stick-slip impulse
without chatter — per-cell precision hardware at 5.08 mm pitch (KC4).
Silent: a chattered gate over/under-steps invisibly with no per-cell
readback (KC3). Timing moot (KC2). Why it could have obsoleted A1: 1-4
purchased shakers replacing the whole gantry/writer with trivial
electrics. Why it fails: grams cannot be thrown uphill against sticky
PLA guides 6400 times without throwing the miniatures off first. Dead —
no reopen trigger (the ratio has no rescuing corner: lighter columns
need MORE g, heavier columns need lift force back).

**E2 — paraffin phase-change latch + global lift: REJECT (one-line).**
Geometry: ~0.1-0.3 g paraffin capsule + spring pawl per column; global
lead screw unloads, global heater melts all slugs, per-tile mask
selects sink order over passes, heater off freezes the pattern.
Distinctness from M3 (recorded so nobody claims re-litigation): M3 was
solid-state Nitinol wire + projector addressing, killed on $/cell wire
cost; E2 is liquid-solid volumetric change + conductive/global heating,
killed below on independent temperature-collision + latent-heat physics.
Temperature kill: paraffin melt ~55-65 C vs PLA Tg ~55-60 C — **the
latch melts at exactly the temperature that softens its own capsule and
guides** (KC4), and minutes-long freezing in low-conductivity plastic
at 5.08 mm pitch equalises neighbours (crosstalk kills selectivity).
Energy/timing corroboration: ~200 kJ/kg x 6400 x ~0.2 g ~= **~250 kJ
per latch-melt before losses — ~40+ min at 100 W heating alone**, plus
minutes of natural cooling (KC2 by two orders). Addressing second kill:
per-cell heaters/valves = 6400 purchased channels (KC4); global oven =
full-reset-only with no regional path (KC5). Silent: a half-frozen slug
creeps under load invisibly (KC3). Why it could have obsoleted A1: zero
wear faces, zero holding power, fully shared lift + heat. Why it fails:
the latch temperature collides with the baseline plastic and the
freeze is minutes, not seconds. Dead — no reopen trigger (no paraffin
corner melts far below PLA Tg while freezing in seconds at pitch).

**E3 — external-robot writer + passive memory: REJECT (tested).**
Geometry: board is pure passive PLA ratchets (zero purchased/cell);
a commodity desktop arm/plotter presses each column to height serially.
Rate kill (binding, topology-independent): 6400 touches in < 30 s needs
>= 213 cells/s sustained; hobby pick-press cycle class is 0.4-1.5
s/cell (~1-2.5 cells/s), so the **optimistic serial total is 2560 s
(85x rate shortfall) and nominal is 6400 s** (KC2, 5/5 gate). Parallel
fingers close the rate only by rebuilding the gantry: 86 fingers at the
optimistic corner x ~$8 floor = **~$688 >> A1 $181** (KC1, gate).
Repeatability corroborates the silent kill: 3-sigma +/-1.5 mm nominal
vs ~1.0 mm usable margin at 5.08 mm pitch seats wrong teeth with no
on-board readback (KC3, gate). Regional is the one passing dimension
(drive only to changed cells) — moot. Why it could have obsoleted A1:
it deletes the writer subsystem from the product entirely (board as
paper, robot as pen). Why it fails: serial touch kinematics are two
orders too slow, and parallelising re-invents the gantry at higher
cost. Park-class speculative reopen trigger only: sourced serial
press cycle demonstrating >= 100 cells/s sustained at <= 5.08 mm pitch
with <= 0.3 mm 3-sigma AND arm cost <= $100 — i.e. a two-order robot
capability break, not an incremental deal. No follow-up issue — parked,
not queued.

## Comparison (ranges; confidence in parentheses)

| Dimension | A1 (record) | E1 vibratory (one-line) | E2 wax-latch (one-line) | E3 robot writer (tested) |
|---|---|---|---|---|
| Purchased | **$181** IDEAL (medium) | shakers cheap, gates kill (medium) | heaters/mask kill savings (medium-low) | arm $150-300 + board; 86-finger parallel ~$688 floor (medium) |
| Full-map time | 19.63 s sustained (calc) | uncomputed, moot | ~40+ min heat alone (high, this test) | 2560 s optimistic / 6400 s nominal (high, this test) |
| Silent cells | 0, cell-local re-drive (calc) | gate chatter, no readback | half-frozen creep, no readback | wrong-tooth press, no readback |
| Regional | cell-granular | tile-gated (only pass) | full-reset oven (fail) | drive-to-change (only pass) |
| Baseline fit | X1C+PLA coupons ready | 10-50 g shake vs PLA/miniatures (fail) | melt collides with PLA Tg (fail) | pitch vs repeatability (fail) |

## Advance accounting

Advanced exactly ONE mechanism (E3) to its cheapest analytic test; E1/E2
advanced zero steps beyond ratio math; no CAD/BOM/procurement beyond the
E3 gate. Task brief complied. At most one advanced — exactly one was.

## Residual uncertainty

Sourced-class prices/cycles are point-in-time equivalents, not
quotations; arm-cycle and finger-floor spreads are wide but the E3
margins (85x rate, ~$500 cost gap at the floor) need no precision.
Stiction (0.2-1 N), PLA Tg (55-60 C), paraffin melt/latent-heat
textbook values are order estimates, not coupled simulation — all E1/E2
kills hold at the most favorable corner by > 10x, so measurement could
not rescue them. Nothing here is physical validation. Exploration
queue: E3 carries the speculative trigger above; E1/E2 are dead with no
triggers; M2's (SHA-15) and D2's (SHA-16) triggers stand. Killed at
tile/board scale and NOT to be re-litigated: A1-A7 as drawn, T1-T5,
M1/M2/M3, D1/D2/D3, E1/E2/E3, and the platen, fluid-bus, magnetic,
thermal-broadcast, electrostatic, gravity, vibratory-conveyor,
phase-change-latch, and serial-robot-writer families. Next divergent
round must seed physics outside ALL of these — the remaining unscoped
space is thin (acoustic levitation/sorting, buckling-sheet snap
arrays, and chemical-swelling actuation were never scoped; each needs a
fresh one-line gate before any script).
