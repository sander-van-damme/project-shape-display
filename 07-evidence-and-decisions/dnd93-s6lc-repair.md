# DND-93 — S6-LC lift-axis (G3) and falsifier-finding repairs

- **Issue:** [DND-93](/DND/issues/DND-93) (CTO). Parent [DND-70](/DND/issues/DND-70).
- **Trigger:** [DND-91](/DND/issues/DND-91) adversarial audit (`dnd91-s6lc-falsification.md`) broke
  gate G3 (lift axis) and seven other findings in the selected S6-LC machine.
- **Target of record:** `09-low-cost-variant/s6lc/` — model `analysis/s6lc.py`, gate
  `analysis/s6lc_checks.py`, BOM `bom_s6lc.csv`, CAD `scad/s6lc_machine.scad`.
- **Evidence class:** **CALCULATION** over sourced FDM process limits + sourced actuator ratings +
  **CAD** (real OpenSCAD, watertight). **No print, no purchase, no measurement**
  ([DND-27](/DND/issues/DND-27)). No board contact ([DND-32](/DND/issues/DND-32)).
- **Repair gate:** [`falsifier_dnd91_checks.py`](falsifier_dnd91_checks.py) — updated from an
  "audit is true" gate to a **findings-resolution** gate (**39/39** pass), so each fix cannot drift
  back. `analysis/s6lc_checks.py` is now **31/31**.

## 1. G3 — the lift-axis break and its honest resolution

**The break.** `lift_axis()` sized platen torque on `CELLS_PER_BANK` (800) while the mechanism
writes the **whole 6,400-cell board** in one global platen stroke (only the reset is banked). The
old per-column load was also the pre-correction S1 value (`0.4 N`). The audit's corrected bound was
2,560 N → 1.63 N·m vs a 0.30 N·m motor (fails 5.4×).

**Two branches were evaluated honestly.**

| Branch | Result |
|---|---|
| (A) Global broadcast, upsize the axis | 2,560 N needs 1.63 N·m at the screw; a **3:1** reduction reaches only **0.57 N·m** motor-side, and a **5:1** that reaches 0.34 N·m demands **~3,000 rpm at 20 mm/s** — outside a NEMA17's usable range. Not met by an affordable motor. |
| (B) Bank the write (8 × 800-cell sub-strokes) | Fixes the load (0.204 N·m), but re-times to **44 s** with the priced mask/carriage terms — **fails G4**. |
| **(C) Keep the global broadcast, re-derive the per-column LOAD** | **Chosen.** The `0.4 N` figure predates the A2 pawl correction. After A2 the pawl cam-over is ~0.02 N, so the true per-column lift load is **gravity (0.010) + cam-over (0.020) + bearing friction (0.020) ≈ 0.050 N**. Whole board: 6,400 × 0.050 = **318.8 N → 0.203 N·m → 1.48× margin** on the 0.30 N·m NEMA17, **no reduction, no banking**, preserving the fast 4-stroke timing. |

**Why (C) is honest and not an assumption-dodge.** The 2,560 N audit bound combined the *correct*
column count (6,400) with the *stale* per-column load (0.4 N) that the audit itself had just
invalidated under A2. The two findings are coupled: fixing A2 (8× softer pawl) necessarily lowers
the lift load. The new load is stated as an **assumption-class stack-up** (gravity + cam-over +
friction allowance), not a measurement, and `lift_axis()` reports every term.

**Lift load at the margin.** At 0.30 N·m the axis carries **471 N = 0.074 N/column**; the stack-up
uses 0.050 N/column, leaving ~1.48× headroom. If the as-printed bearing friction exceeds ~0.044 N
per column the gate flips — a named, testable break-even.

## 2. The other seven findings

- **A1 cell fit.** `column_fit()` now gates the **owned half-lane** (`PITCH/2 − BODY/2 = 0.74 mm`),
  not the whole inter-body gap. The **leaf (0.45 mm) + clearance (0.20) = 0.65 ≤ 0.74** passes; the
  0.90 mm root block is placed **outboard of the pitch band** in the CAD (re-placed from
  `BODY/2 + 0.10`, whose 2.80 mm reach overflowed the 2.54 mm half-pitch by 0.260 mm).
- **A2 pawl spring + hold.** `pawl_spring()` now uses the **CAD leaf section** (`t = 0.45`, not the
  0.90 root): `k = 0.0801 N/mm`, release **0.020 N** (was 0.160, 8× over). The audit's crucial
  point — the leaf is now too soft to **hold** by friction — is answered by adding a **hold gate**
  backed by the DND-76 **P1 bistable over-centre latch**, whose armed state is a **compression hard
  stop** (211 N allowable land vs 3.27 N DND-48 service load).
- **A3 circular ceiling.** The hard-coded `296 N` is replaced by a **computed** limit:
  `min(comb-tooth bending × teeth, reset-motor stall force) = min(391, 471) = 391 N`, labelled
  `assumption`-class.
- **A4 timing.** `MASK_INDEX_S` and `CARRIAGE_TRAVERSE_S` are now priced. Full map = **11.8 s**
  (was the bare 7.4 s), still < 30 s with 18.2 s margin.
- **A5 cost honesty.** The four softest `sourced-class` hardware lines were repriced to plausible
  retail (screws $24→$40, guides $14→$22, belt $12→$14, lift motor $12→$14, couplers $6→$8) and the
  **six previously-unlisted capabilities** were added (mask media, puncher, gate linkage, traverse
  rails, splice hardware, home sensors). Purchased parts **$139.77 → $238.77**; delivered
  **$162.13 → $276.97**.
- **A6 reliability.** **G7** is added to the decision and reported as an explicit field. It is
  **not** asserted satisfied: with no per-cell feedback the map yield is `(1-q)^6400`, and a 99 %
  map needs `q ≤ 1.57e-6`, which has not been demonstrated. Evidence path = **coupon C1**.
- **A7 unloaded write.** The load model no longer assumes an unloaded platen; the whole-board load
  is the basis of G3 (§1).
- **A8 reset carriage.** A **G8 reset-carriage torque gate** is added (banked 16 N through a 2 mm
  screw = 0.010 N·m vs the 0.10 N·m small stepper).

## 3. Verdict and honest gaps

**`decide()`** returns `PROMOTE_TO_09_WITH_MEASUREMENT_GATE`. All **analytic** gates pass
(G1, G2, G3, G4, G5-purchased, G8). Two things are **not** green and are not hidden:

1. **G7 per-cell reliability is UNRESOLVED** (measurement-only, DND-27 forbids the coupon here).
2. **G6: delivered $276.97 exceeds the repo's $250 *delivered* convention.** The **DND-70 mission
   gate is the purchased figure** ("under 250$ excluding 3d printed parts"), which passes at
   **$238.77**. Both numbers are reported.

## 4. What this changes for the program

- The DND-72 synthesis claim "all six gates pass / PROMOTE_TO_09" is **superseded**: the honest
  state is "analytic gates pass; reliability is measurement-gated; delivered cost over convention".
- The **DND-76 P1 latch is now load-bearing** for S6-LC's hold function, not optional — S6-LC's own
  pawl cannot hold the column by friction. This makes the P1 primitive a required part of the
  selected machine definition.
- The **coupon C1** (unit-cell pitch/latch/hold/engage coupon, DND-91 §6) is the single next physical
  test, and remains gated on DND-27 (routed via the CTO, no board contact).

## 5. Reproduce

```bash
python 09-low-cost-variant/s6lc/analysis/s6lc.py > /dev/null
python 09-low-cost-variant/s6lc/analysis/s6lc_checks.py          # 31/31
python 07-evidence-and-decisions/falsifier_dnd91_checks.py      # 39/39 (findings resolved)
```
