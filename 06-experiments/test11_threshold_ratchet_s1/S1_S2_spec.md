# S1 / S2 complete-machine specification and component counts

This document answers the "complete the machine" requirement for the two
planar / external-memory architectures. It counts real parts and states the
evidence level of every number. **No physical measurement exists here.** Values
marked *[calculated]* come from the scripts in this folder; *[assumption]* are
engineering hypotheses that a coupon must test.

---

## S1 — broadcast threshold ratchet + global incremental lift

### Concept

Every cell is a square column with a **5-pocket vertical rack** (10 mm spacing,
0/10/20/30/40 mm) and a **printable cantilever pawl** that holds the column
against gravity. Four **broadcast 10 mm lift strokes** advance columns that have
been *armed* by a planar threshold mask. The pawl and the mask gate are passive;
the only powered motions are the common platen and mask registration.

### Function allocation (the ten required jobs)

| Job | S1 answer | Real parts |
|---|---|---|
| Visible moving element | Square 4.72 mm column, 44 mm tall | 6,400 printed columns |
| State storage | 5-pocket rack + pawl detent | 6,400 printed pawls |
| Selection | Four unary threshold planes; each cell's gate bar is blocked/opened per stroke | 25,600 gate decisions, 0 bought selectors |
| Power delivery | One common platen, 4 × 10 mm strokes; banks of cells | 1 platen drive + 1–4 screws/motors *[assumption]* |
| 40 mm motion | Four 10 mm increments accumulated by one-way pawl | printed geometry |
| Retention | Pawl in pocket; no powered hold | printed geometry |
| Load path | Column base → pawl/rack → grid shelf | printed geometry |
| Lowering / reset | Global release comb lifts all pawl toes; columns fall to datum | 1–2 release actuators, 8 bank combs *[assumption]* |
| Full-map update | 4 broadcast strokes (timing model: **5.3 s**, excluding media write) | — |
| Regional update | Bank/tile release + replay of 4 strokes (~4.2 s/tile) | bank clutches *[assumption]* |
| Jam handling | Missed step is local; post-map height scan (not per-cell sensors) | 1 camera/scan *[assumption]* |
| Power loss | Pawls hold; power loss mid-stroke is unresolved (platen fall) | brake *[assumption]* |
| Assembly | 6,400 columns + 6,400 pawls + mask planes, modular 10×10 cartridges | — |
| Active count | 1 platen drive, 1–4 lift motors, 2 release actuators, 1 controller | ~4–8 bought actuators |
| Passive count | 6,400 columns, 6,400 pawls, 25,600 gate bars, 4 mask planes | printed |
| Purchased BOM | platen drive + screws + release + controller + scan ≈ **$150–250** *[assumption, unquoted]* | — |

### The four masks: how selection actually works

Target height encodes unary over 4 thresholds:

```
T1 = {cells with target >= 10 mm}
T2 = {cells with target >= 20 mm}
T3 = {cells with target >= 30 mm}
T4 = {cells with target >= 40 mm}
```

Stroke k arms exactly the cells in Tk and advances them 10 mm. This is why 4
binary planes = 5 heights. It also means **25,600 gate decisions** per full map,
each of which must be physically present in the medium.

### Where S1 fails (this study)

- **C — mask writing.** 12,800 hole/set operations (half the board armed on
  average × 4 planes). Serial punching is 2,560 s. An 80-channel writer is 56 s,
  outside the 30 s visible budget. Fixing this means pre-written media, which is
  S2.
- **B2 — worst-case release force.** If one stroke arms most cells (an all-high
  map arms all 6,400 in stroke 1), total release force is ~2.4 kN at 0.37 N/cell.
  Break-even is 0.234 N/cell, or the board must be banked and stroked in
  sequence.
- **D — print-force variation.** 6,400 printed pawls must share a release-force
  window. Break-even sd is ~9% of mean; typical FDM part-to-part force spread on
  thin cantilevers is reported at 10–20% [assumption]. No per-cell sorting is
  affordable.

### The design change that would revive S1

**Banked broadcast:** split 80×80 into 8 banks of 10 rows (800 cells). Each bank
gets its own release comb and its four sub-strokes. Worst-case simultaneous
release force drops to ~296 N per bank (0.37 N × 800), and each bank can be
verified independently. This trades 8× the stroke time (4 strokes × 8 banks ×
0.55 s ≈ 17.6 s, still under 30 s) for force feasibility. **This is a concrete
new variant: S1-B, banked broadcast ratchet** — worth a coupon, but it still
inherits the mask-writing failure unless media are pre-written.

---

## S2 — independently swappable planar-memory tiles (double-buffered)

### Concept

The display has **64 tiles of 10×10 cells**. Each tile contains a **stack of
four perforated first-stop planes plus a bottom floor**. A column's height is the
first plane lacking a hole beneath its follower — pure mechanical unary decoding
(no per-cell electronics). One shared platen lifts all columns clear; they settle
onto the first stop. Tiles are serviced individually by a **shared lift with a
selective tile clutch**; the medium for the *next* map is written off-line.

### Function allocation

| Job | S2 answer | Real parts |
|---|---|---|
| Visible moving element | Square column per cell | 6,400 printed columns |
| State storage | First-stop height plane (external!) | 4 plates/tile × 64 = 256 plates |
| Selection | Hole/open geometry in the planar medium | passive; 25,600 holes per full map |
| Power delivery | One shared platen + tile clutch | 1–2 lift motors + 64 tile couplers |
| 40 mm motion | Global 41 mm clear + gravity settle onto stop | — |
| Retention | Hard stop + floor; passive | printed |
| Load path | Follower → stop plane → tile frame | printed |
| Lowering / reset | Global or tile-local clear stroke | shared with lift |
| Full-map update | **~2.0 s** read (lift+settle+verify), media pre-written | — |
| Regional update | **~1.8 s/tile** visible; writer time hidden | — |
| Jam handling | A bad hole corrupts one tile; tile is replaceable | — |
| Power loss | Stops hold | — |
| Assembly | 64 tile cartridges, 256 plates, 6,400 followers | — |
| Active count | 1–2 lift motors, 64 tile couplers, 1 controller, 1 writer | ~70 bought items |
| Passive count | 6,400 columns, 6,400 followers, 256 planes | printed/media |
| Purchased BOM | motors + couplers + controller + writer + scan ≈ **$250–400** *[assumption, unquoted]* | — |

### The central unresolved product question

S2's arithmetic passes (G, H, C2). Its fate is decided by two things arithmetic
cannot settle:

1. **Surprise maps.** The 30 s visible budget only holds if the next map is known
   roughly a minute ahead. A genuinely unannounced map makes the off-line writer
   the bottleneck. This must be stated as a product limitation, not hidden.
2. **Exchange disturbance.** Swapping or lifting one tile while a miniature stands
   on a loaded neighbor is exactly Q5. The arithmetic (F) passes only because the
   frame stiffness is an assumed 100 N/mm. That input must be measured.

### The cheapest rejection coupon

Two adjacent true-pitch 5×5 tiles, four planes + floor each. Hold one in a
non-flat state under a representative load; repeatedly clear, change and settle
the other. Measure neighbor peak motion, residual height error, insertion force,
seam step and misreads. If an adjacent miniature moves more than the agreed
allowance, S2's regional claim dies.
