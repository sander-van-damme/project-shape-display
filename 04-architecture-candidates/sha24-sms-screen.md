# SHA-24 competing-architecture concept: scanning multi-spindle screw-column matrix (G1)

> Companion to the verdict note
> [`07-evidence-and-decisions/sha24-sms-screen.md`](../07-evidence-and-decisions/sha24-sms-screen.md).
> Sketches live here per the routing rule (new ideas go in `04`);
> the binding kill math and verdict live in `07`; the executed analytic
> test lives in `06-experiments/test22_sms_screen/`.
> Evidence class: CALCULATION over design-criteria geometry + sourced-class
> actuator ratings + textbook thread mechanics. DND-27: no print, purchase,
> or measurement. S5-R, A1, S6-LC packages untouched.

## Why this direction (and not the others)

The lane demands shared actuation with passive selection/state retention,
substantially different from A1 (gantry toggle-latch + reader) and from the
A7-V camshaft challenger (bank shaft angle + reader). The screw column is
the one retention physics that is neither a latch/ratchet/detent (A1, S1,
S4, S5 all store state in teeth) nor a cam program (A7-V): **the thread
itself is the memory, the brake, and the load path** — self-locking
friction holds any of 5 quantized heights with power off, in compression
on the thread flanks. Selection is purely positional (the spindle engages
only the addressed nut), so there are zero per-cell bought parts and zero
latch/ratchet precision contacts. Relation to prior drops, stated so nobody
claims re-litigation without evidence: #18 (shared screw-driving matrix)
was dropped on 20 turns/cell at 2 mm lead with row-parallel Test08 timing
and couplings; #6 (single XYZ pick/push writer) was dropped on ~76 min
serial time. G1 is a different embodiment — high-lead multi-start printable
thread (5 turns for 40 mm, not 20) driven by a parallel multi-spindle
scanning bar (not one serial head, not a row-parallel coupling matrix) —
and it is screened below with fresh turn-count x spindle-parallelism
arithmetic that directly addresses those two kill criteria. E3's serial
touch-rate kill is related but not binding here: the binding bound is
**rotation time per cell**, not touch rate.

## Mechanism description

Each of the 6,400 cells is a printed column captive in a smooth printed
guide, carried on a printed internal nut riding a **static vertical
printed lead screw** fixed to the frame (screw does not rotate; the nut
travels). Five heights are 5 quantized nut positions over 40 mm. A shared
XY gantry carries a **spindle bar** (N rotary spindles, one per addressed
column, each a printed driver bit on a small bought rotary source via a
shared belt). The bar descends, the bits engage the exposed nut crowns of
one row-segment, the spindles rotate the addressed nuts by a counted number
of turns while unaddressed nuts in the segment are held by a passive
spring detent against rotation (selection = which spindles are clutched in;
the rest freewheel), then the bar lifts and indexes. Down-reset is the same
operation in reverse (screw back down to the datum hard stop — no separate
global reset mechanism). A datum hard stop at the bottom gives turn-count
reference.

## Operating principle

- **Power delivery (shared):** 2 gantry steppers + 1–2 spindle-drive motors
  + belt to N spindle bits. All bought rotation is on the moving bar.
- **Selection (passive/positional):** only nuts under an engaged spindle
  turn; nut-rotation detents keep unaddressed nuts parked. No per-cell
  electrics, no mask medium, no threshold gates.
- **Positioning:** counted turns × lead = height (open-loop step count per
  cell, e.g. 0/1.25/2.5/3.75/5 turns at 8 mm lead).
- **State retention (passive brake):** thread self-locking (lead angle <
  friction angle) holds height with power off; play load bears in
  compression on the flanks. No spring force decides correctness.
- **Load support:** the static screw core in compression (same column that
  positions also carries the miniature).
- **Regional update:** drive the bar only to changed cells; untouched nuts
  never unlock. No full-board reset, no tile disturbance.

## Expected component count

- Per cell, printed: 1 column + 1 nut + 1 guide bore + 1 rotation detent
  = 4 printed parts × 6,400 = 25,600 printed parts (no bought parts/cell).
- Shared, bought: 2 gantry steppers, 1–2 spindle motors, ~N spindle bits
  + belt + couplings, rails, controller, drivers, PSU, loom, switches
  (≈ A1 gantry class + spindle bar).
- Shared, printed: frame tiles, guide plates, spindle bar body, nut crowns.

## Purchased parts (sketch, not a line BOM)

Gantry class ≈ A1 ($181 package) **plus** the spindle bar: N driver bits,
N miniature clutch/dog elements, belt + tensioners, 1–2 extra motors +
drivers. The gate below shows N ≥ 64 at the optimistic corner, so the
spindle bar alone reintroduces dozens of bought channels — the cost shape
A1 avoids. No costing beyond this ceiling is justified once KC2 kills.

## Printed material

PLA on the X1C baseline. ~25,600 cell parts + frame + bar. Nut + screw are
the precision pair (see print complexity).

## Print complexity

HIGHE — the load-bearing thread is the risk: an 8 mm-lead 4-start thread
(2 mm pitch) on a ~4–5 mm screw diameter needs ~0.5 mm flank features
repeated 6,400× on a 0.4 mm nozzle, plus matching internal nuts with
working clearance. Thread wear, print-stringing in nuts, and pitch
variation across the bed directly become height errors. One fused nut =
one dead cell.

## Estimated cost

Not credibly below A1: gantry + reader-equivalent verification (KC3
forces a reader — see reliability risks) + ≥54-spindle bar. Nominal
placement: **above $181 at every corner** (KC1 corroborates; the gate
asserts the spindle-count floor and a $/spindle floor, no full BOM needed).

## Expected update speed (binding — see gate)

Per-cell screw time 0.30 s optimistic (5 turns at 1,200 rpm + engage/
settle overhead) vs A1's 3 ms toggle hidden under 5.08 ms traverse.
Full-map spindle-seconds 1,920 optimistic; fitting < 30 s needs
**64 spindles** at the most favorable corner (gate check 4, 5/5).
Nominal corner needs 245. KILLS on KC2.

## Local-update behavior

Cell-granular in principle (drive only changed cells, 0.00 mm modelled
disturbance of neighbours — same rigid-body argument as A1 R6). Moot once
KC2 kills: single-cell edit still costs a full engage/traverse/dwell
(≥ 0.5 s) and any multi-cell region pays serial screw time.

## Reliability risks

- **Silent set without a reader:** a stalled nut (fused thread, debris,
  skipped spindle steps) parks at the wrong height invisibly — the full
  6,400 silent set returns. Earning A1-class zero-silent needs the same
  cell-resolving reader + retry that killed A7-V on cost (K1): the reader
  the concept deletes is the reader the concept needs.
- **Correlated mode:** one worn driver bit mis-drives every cell it
  touches (band/region wrong); belt stretch drifts turn counts globally.
- **Open-loop turns:** no per-cell feedback; detent slip during engagement
  loses the datum.

## Durability risks

- Thread-flank wear across 6,400 printed nuts under 1 N service + handling
  abuse; PLA creep under sustained flank load blurs quantized heights.
- Driver-bit wear (1 bit drives hundreds of nuts).
- Detent fatigue. All measurement-only under DND-27; moot after KC2.

## Compactness

Board 406.4 × 406.4 mm + gantry + spindle bar overtravel. Z-stack grows:
nut crown + driver-bit engagement + screw core below the board. Comparable
footprint to A1, taller Z.

## Assembly complexity

HIGH: 6,400 screw/nut pairs must each turn freely by hand after assembly
(25,600 printed parts with one precision thread pair each), plus spindle
bar with ≥ 54 compliant bits aligned to 5.08 mm pitch. No per-cell wiring
(the one assembly win), paid back in thread fitting.

## Scalability

Anti-scales: cells ÷ spindles × screw-time is linear in map size with a
~0.30 s/cell constant — ~50x worse than A1's ~6 ms/cell/head constant.
Larger maps need proportionally more spindles.

## Requirement coverage

| Requirement | G1 placement |
|---|---|
| 80×80, 5.08 mm pitch | fits geometrically (nut crown + detent in lane — arithmetic only) |
| 5 heights over 40 mm | quantized turns, native |
| < 30 s full update | **FAIL** (64 spindles optimistic; 245 nominal) |
| Regional update | cell-granular in principle, serial-slow in practice |
| <$500 purchased ($181 to beat) | **FAIL** (spindle bar + forced reader) |
| Zero-silent-error frame | **FAIL** as drawn (open-loop turns); reader-fitted variant fails cost |
| Power-off hold | PASS (self-locking thread — the one genuine win) |
| X1C + PLA baseline | MARGINAL (0.5 mm thread flanks 6,400×) |

## Key unknowns (all moot after the KC2 kill; recorded for the trigger)

1. Smallest reliably printable multi-start lead at ~4–5 mm diameter on a
   0.4 mm nozzle with working nut clearance (needs a thread coupon).
2. Self-lock margin of as-printed PLA-on-PLA threads under 1 N + abuse
   (back-drive = lost state).
3. Spindle engagement repeatability at 5.08 mm pitch (bit-to-crown
   registration, wear).
4. As-printed turn-count accuracy vs height quantization bands.

## Proposed experiments (cheapest first; none executed — killed analytically)

- **T22-A (would-be binding coupon):** single screw/nut pair at true pitch:
  measure turns-to-height, back-drive torque, and fused-nut rate over 10
  prints. Kills on printability before any bar is built.
- **T22-B:** 1×5 spindle-bar section, checkerboard turn pattern under load:
  measure complete engage/drive/disengage dwell (the loaded-dwell analogue
  of S3's T11-B).
- **T22-C:** wear cycling of one nut over 1,000 traverses (height drift).
- None is warranted: KC2 kills at the optimistic corner by > 3× even
  before printability is tested.

## Reopen trigger (park-class, speculative)

A sourced screw medium delivering 40 mm in **≤ 1 turn** (lead ≥ 40 mm —
a printed "twist-lock" bayonet, not a thread) with self-locking hold AND
a demonstrated ≤ 50 ms engage/drive/disengage dwell at 5.08 mm pitch would
reopen the rate gate. That medium is not a thread as drawn and would need
its own coupon. No follow-up issue — parked, not queued.