# DND-76 — divergent low-cost cell / mechanism primitives (<$250 purchased)

**Question.** [DND-71](/DND/issues/DND-71) is developing the ultra-low-cost
(<$250 purchased, printed parts free) shape display. Its leading candidate
**S6-LC** — a banked broadcast ratchet descending from
[Test11 S1](../../06-experiments/test11_threshold_ratchet_s1/) — uses passive
printed **pawl-in-rack** column memory (5 pockets, 10 mm steps), one **broadcast
10 mm platen stroke**, a **per-bank threshold mask gate**, and a **banked
release comb**, with ~3 bought motors and ~$139.77 parts.

This directory invents **four concrete cell-level / selection primitives** that
attack S6-LC's four named weak points, counts every component honestly, and
names the cheapest analytic falsifier for each.

**One-line answer.** All four primitives are **100 % printed** — they add
**zero bought selectors, zero bought clutches, and zero motors** — and they
clear every analytic gate: 13.0 s full map (< 30 s), $170.17 purchased even at
worst-case optional extras (< $250), and a friction-independent cell state.
The decisive trade is honest and local: each primitive replaces a
*tolerance-fragile force* with a *hard-stop position*, at the cost of a
**correlated, silent error** if a whole comb or clutch fails (bounded by 4 home
sensors per bank, not per-cell feedback).

**Evidence class: CALCULATION over sourced FDM limits + CAD (real OpenSCAD).
No print, no purchase, no measurement** ([DND-27](/DND/issues/DND-27)). This
folder does **not** qualify an architecture and does **not** touch
`08-current-design/`.

## Reproduce

```bash
python 09-lowcost-alternative/primitives/primitives.py        # full screen (JSON)
python 09-lowcost-alternative/primitives/primitives_checks.py # 35 pinned assertions
python 09-lowcost-alternative/primitives/tools/render_primitives_cad.py  # real CAD
```

The checks run in CI (`engineering-checks` job); the CAD render runs in the
`lowcost-primitives-cad-render` job, which **hard-fails if OpenSCAD is missing**
so a skipped render can never be mistaken for validated CAD.

## The four primitives at a glance

| # | Primitive | Attacks S6-LC weakness | Bought delta | Decisive failure mode |
|---|---|---|---:|---|
| **P1** | Friction-independent **bistable over-centre latch** | #1 release-force spread (S1-D, break-even sd ~9 %) | **$0** | snap can stall mid-throw if the comb force is under-sized against print-stiffness spread |
| **P2** | **Printed 4-plane louvre comb stack** + one camshaft/bank | #2 mask medium | **$0** (32 printed bars, 0 motors) | a stuck comb arms/disarms a whole **80-cell band** (silent, correlated); 4 home sensors/bank detect whole-comb only |
| **P3** | **Relieved pocket throat + V-guide** at 3.60 mm body / 1.48 mm lane | #3 guidance / pocket sharpness | **$0** | as-printed V-guide wear and throat fusing are measurement-only |
| **P4** | **Single-actuator banked reset** (reset bar rides the platen) | #4 reset with one actuator | **$0** (8 printed one-way clutches, 0 motors) | a clutch that sticks engaged re-trips the combs on the up-stroke, corrupting the mask |

## P1 — friction-independent bistable over-centre latch

**Why S6-LC hurts here.** A plain pawl release force is
`F = k·defl + μ·N`. On a loaded column the μ·N term is sized by the DND-48
bounding service load (3.27 N/column). Across the *sourced* PLA–PLA μ band
[0.20, 0.50] the release force **more than doubles** (0.79 → 1.78 N, ratio
**2.24×**), which is an implied spread of **19.1 % of the mean** — over the
**9 %** break-even the S1-D screen already found (typical FDM spread 10–20 %).
That is the whole reason S1 needed a banked release at all.

**The primitive.** Store the armed/disarmed state as a **position bounded by two
hard printed walls**, not as a preload. A 0.90 mm (2-line) printed over-centre
link is thrown past dead point by the mask comb; the link's toe then either
blocks or clears the pawl's release path.

- Link rate `k = 3EI/L³` = **1.53 N/mm**; over-centre throw 0.40 mm →
  **snap force 0.61 N** (sub-Newton, easily comb-set).
- A ±20 % stiffness spread moves the *snap* force ±20 %, which the comb is
  oversized against; the **state after flipping is exact** because both states
  are hard stops. Friction still resists the snap but **cannot hold a state**
  that a wall bounds.
- **Cost: $0** (one printed part per cell, 6,400 prints).

**Decisive failure / cheapest rejection.** Solve the snap at μ_high = 0.50 *and*
−20 % stiffness; if the comb force cannot still throw the link past dead point,
P1 dies. A 3×1 printed coupon would settle it if board policy allowed a print
([DND-27](/DND/issues/DND-27) forbids it). **Kill threshold:** worst-case snap
force > comb force.

## P2 — printed 4-plane louvre comb stack (the mask medium)

**Why S6-LC hurts here.** S6-LC's mask must encode, per bank,
`T_k = {cells with target ≥ k·10 mm}` for `k = 1..4`. That is **320 bits/bank**,
**2,560 decisions** across 8 banks. Where do those bits physically live?

**Candidates screened (`mask_scheme_screen`):**

| Medium | Bought | Verdict | Why |
|---|---:|---|---|
| Punched paper card | $0 | **REJECT** | 80 holes at 5.08 mm need ≥0.10 mm registration; paper tears/jams |
| Printed **single** comb, relative shift | $0 | **REJECT** | a single comb only reproduces shift-identical patterns; an arbitrary threshold set arms the wrong cells (silent map error) — *recorded as a failed idea* |
| **Printed 4-plane louvre comb stack + camshaft** | **$0** | **SELECT** | fully printed; 0 extra motors |
| Bought 80-channel line-punch head | $38 | REJECT | S5-R writer-cost territory; eats the whole budget |
| Magnetic printed comb + hall latch | $0 | REJECT | printed magnets creep; needs bought magnets |

**The selected medium.** Four 1.20 mm (3-line, load-bearing) printed comb bars
per bank, each with an open slot over every armed cell and a 1.32 mm (3-line)
land over every disarmed cell, guided in a 1.60 mm channel (**0.20 mm free after
worst-case tolerance**). The four bars are stroked as a stack by **one camshaft
per bank**, driven off the bank's **own platen stroke** through the same one-way
pawl clutch as P4 — so the primitive adds **no motor**. The bitmap is written by
a **shared travelling writer** (8 passes, ~4.0 s) that parks off the dense
field, so **pitch is unchanged**.

**Decisive failure mode (the honest weakness).** A comb that fails to move
mis-arms an entire **80-cell column band** — a silent, *correlated* error. Only
**4 comb home sensors per bank (32 total)** can see it, and only as a
whole-comb failure; a single mis-set slot needs per-cell readback the architecture
cannot afford. This is the trade P2 makes: it buys zero bought selectors and
zero motors, and pays in correlated failure granularity.

**Cheapest rejection:** `comb_printability()` (slot web ≥ 0.88 mm, guide gap
≥ 0.10 mm worst case) + an OpenSCAD render at pitch. **Kill:** web < 0.88 mm or
guide gap ≤ 0.10 mm.

## P3 — column guidance and rack-pocket geometry at 3.60 mm body / 1.48 mm lane

**Why S6-LC hurts here.** The S1 coupon's side-by-side pitch budget famously did
**not** close:
`body + pawl + bleed + gate + bleed = 3.60+0.80+0.20+0.80+0.20 = 5.60 > 5.08`.
At a 3.60 mm body the lane is **1.48 mm**. The pawl is 0.80 mm; two 0.10 mm
print bleeds leave **0.48 mm of throw**.

**The primitive.**
- The gate is **stacked above the pawl in Z** (the S1 correction), so it does not
  consume lane — the 1.48 mm lane holds only the pawl (`throw 0.48 mm`).
- A **30° relieved pocket throat** (under the sourced 45° overhang limit) stops
  the toe wedging on a fused sharp edge and lets the pocket self-clear.
- A **60° V-guide** (0.88 mm, 2-line rail) centres the 3.60 mm body to ≈0.10 mm;
  the pocket is 2.40 mm wide against a 0.60 mm toe, giving **0.90 mm side
  clearance — 9× the centring error**.
- The pocket **floor is a 2-line land in compression** (0.88 × 2.40 mm,
  ≈63 N allowable vs the 3.27 N bounding service load → **19×**). The terrain
  load path is column → tooth → printed land, **never a bending leaf**.

**Decisive failure / cheapest rejection.** `lane_budget()` + the 30° throat
overhang check. **Kill:** `pawl_stack_worst > 1.48 mm` or relief > 45°.
As-printed V-guide wear and throat fusing remain **measurement-only**.

## P4 — single-actuator banked reset

**Why S6-LC hurts here.** Resetting 8 banks normally wants a second carriage or
8 actuators. **The primitive** avoids both:

- A printed **reset bar rides the underside of the common platen** — an already
  moving part, so there is **no second carriage and no extra motor**.
- A **Z-offset engagement dog** contacts only the currently-indexed bank's four
  comb tails at the down limit; the platen/index motor walks it bank to bank
  (this is the **one actuator**).
- A **printed one-way pawl clutch** on each comb trips on the down-stroke and
  **free-wheels on the up-stroke**, so the reset cannot fight the write.

Reset time = 8 banks × (0.55 s platen stroke + 0.30 s index) = **6.8 s**
(calculation, assumption-class).

**Decisive failure mode.** A clutch that **sticks engaged** on the up-stroke
re-trips the combs after the write, corrupting the mask — a **whole-bank
(800-cell)** correlated error. The clutch must be a **positive pawl**, not a
friction clutch: a friction clutch's release torque has the same μ-spread
problem P1 removes, so a detented slip ring is **REJECTED** for the same reason.

**Cheapest rejection:** a kinematic check that the Z-offset bar engages one bank
only, plus a pawl-vs-friction clutch screen. **Kill:** clutch release depends on
μ, or the bar engages > 1 bank at once.

## Full system accounting (the ten jobs)

| Job | S6-LC-with-primitives allocation | Class |
|---|---|---|
| Visible moving element | 6,400 printed square columns | CAD |
| State storage | printed 5-pocket rack + pawl (passive; holds with no power) | CAD |
| Selection | printed 4-plane louvre combs (32 bars), bank-local | CALC |
| Power distribution | one common platen + one bank/index motor (+ writer) | CALC |
| 40 mm motion | 4 broadcast 10 mm platen strokes (common, paid once) | CALC |
| Retention | rack tooth in a 2-line compression land | CALC |
| Lowering / reset | P4 single-actuator banked reset (rides the platen) | CALC |
| Full-map update | mask write 4.0 s + 4 broadcast strokes 2.2 s + reset 6.8 s = **13.0 s** | CALC (assumption-conditional) |
| Regional update | index to the affected bank(s); comb is bank-local, neighbours hold | CALC |
| Jam handling | per-bank friction coupling limits torque; post-write height scan; no per-cell feedback | ASSUMPTION |
| Power loss | pawls hold height; platen needs a printed detent brake (inherited) | ASSUMPTION |
| Assembly | 8 bank modules + 12,800 printed column/pawl prints + 32 combs + 8 clutches + writer | CALC |

### Component counts (real, not "a selector")

| Bought | Count | | Printed | Count |
|---|---:|---|---|---:|
| Motors | **3** (unchanged) | | Columns + pawls | 12,800 |
| Per-cell selectors | **0** | | Bistable links (P1) | 6,400 |
| Clutches | **0** | | Comb bars (P2) | 32 |
| Mask items | **0** | | One-way clutches (P4) | 8 |
| | | | Reset bar (P4) | 1 |

**Bought BOM delta (calculation):** required **$0.00**. Even at worst case —
the writer gets its own motor + index ($24.00) and all 32 comb home sensors are
bought ($6.40) — the machine is **$170.17 purchased**, still **$79.83 under
$250**. The cheap architecture's lever is **prints, not bought selectors**.

### End-to-end timing budget (calculation, assumption-conditional)

| Term | s |
|---|---:|
| Mask write (8 banks × 0.50 s pass) | 4.00 |
| 4 common broadcast strokes @ 0.55 s | 2.20 |
| Banked reset (8 × [0.55 + 0.30]) | 6.80 |
| **Full map** | **13.00** |

The platen is **common**, so the four broadcast strokes are paid **once**, not
per bank — only the mask write is serial. This is the same evidence class as
S1's 25.20 s budget: an assumption-conditional calculation, **not a
measurement**.

## Evidence boundaries

| Claim | Type | Status |
|---|---|---|
| Four primitives add $0 bought parts / 0 motors | CALCULATION | pinned by checks |
| S6-LC friction pawl spread 19.1 % > 9 % gate | CALCULATION | from sourced μ band + DND-48 load |
| Latch snap 0.61 N, 2-line printable | CALCULATION + CAD | |
| Comb web 1.32 mm, guide gap 0.20 mm worst case | CALCULATION + CAD | |
| Lane throw 0.48 mm; floor margin 19× | CALCULATION | |
| Full map 13.0 s | CALCULATION | assumption-conditional |
| Worst-case machine $170.17 < $250 | CALCULATION | optional items priced |
| Bistable link actually flips at worst-case print spread | **assumption** | needs a coupon (forbidden under DND-27) |
| Whole-comb failure severity | CALCULATION | correlated, silent |

## Decision

- **P1** — retain. It removes μ from the stored state and is the direct answer
  to the S1-D release-spread failure. Residual: worst-case snap-vs-comb margin.
- **P2** — retain **as the mask medium**, with the correlated 80-cell failure
  named. It is the only candidate that is both cheap and reliable enough.
- **P3** — retain. It closes the pitch budget and puts the load in compression.
- **P4** — retain. It resets 8 banks with the platen's own actuator.
- **Failed ideas recorded as evidence:** paper punched cards; the single
  relative-shift comb; a bought 80-channel punch head; magnetic printed combs;
  a friction (detented slip-ring) reset clutch.
- **No architecture is promoted** by this folder. The primitives are inputs to
  the [DND-71](/DND/issues/DND-71) synthesis and are recorded there.
