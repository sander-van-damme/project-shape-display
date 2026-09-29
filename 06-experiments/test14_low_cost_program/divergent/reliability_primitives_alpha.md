# DND-106 — reliability-first cell / mask primitives (InventorAlpha, S1/S2 family)

> **Subdirectory of [`06-experiments/test14_low_cost_program/divergent/`](README.md), child of
> [DND-104](/DND/issues/DND-104).** This folder is the InventorAlpha response to
> the CTO's reliability-first program: invent **concrete cell / selection /
> reset primitives** that attack the one reliability gate the S1/S2 mask family
> keeps losing on — **"what has to work correctly 6,400 times?"**
>
> It does **not** touch `08-integrated-designs/s5r-shared-drive-register/`, does **not** promote an
> architecture, and does **not** re-cost the machine. It is an input to the
> DND-104 synthesis.

## The question this folder answers

`02-design-criteria` (DND-103) makes reliability a **gate**, not a tie-breaker.
The program's own arithmetic ([DND-91](/DND/issues/DND-91) A6/G8) is brutal:

```
A map is correct only if all 6,400 cells are correct.
map yield = (1 - q)^6400
99 % map  =>  q_cell <= 1.57e-6
```

S6-LC's cell is a passive printed pawl with **no per-cell feedback**: a missed
latch is a **silent, undetectable, unrecoverable** height error. That is the
weakness this module attacks — not the cost, not the pitch, not the timing.

## The insight: correlation is only acceptable with a read path

If the *same* mechanism's error is **correlated** across a row (one rocker) or a
bank (one comb), the number of **independent** units collapses and the q budget
loosens dramatically:

| Repeated unit | Count | q break-even for a 99 % map | Looseness vs per-cell |
|---|---:|---:|---:|
| individual cell | 6,400 | **1.57e-6** | 1× |
| row (rocker) | 80 | **1.26e-4** | **80×** |
| bank (comb) | 8 | **1.26e-3** | **~800×** |

Correlation is normally *bad* (bigger blast radius). It only becomes a **win**
when it is paired with a **detection + re-run path** (R3): a whole row that
fails together can be *seen and re-driven*; a single cell that fails silently
cannot. A correlated error with no read path is **strictly worse** than an
independent one at the same q — that is exactly why S6-LC's banked mask is
fragile and why R4 below is rejected.

## The three primitives (all CALCULATION + CAD)

| # | Primitive | Family | Bought delta | What must work 6,400× | Blast radius |
|---|---|---|---:|---|---|
| **R1** | Toggle-rocker **row-shared state** (one rocker = one row) | shared mechanical state | **$0** | **80 row-rocker decisions** (6,400 columns passive) | 80 cells, **detectable** |
| **R2** | **Double-acting wedge-gate** cell (positive hard stops, driven reset) | per-cell positive stops | **$0** | 6,400 gate set/reset events, but reset is a **driven positive stop** | 1 cell |
| **R3** | Mechanical **read-rod readback** (detectable / recoverable) | detection + recovery | **$4.00** (2 sensors, no per-cell hardware) | **80 read decisions** / read pass | n/a (it detects) |
| **R4** | Shared return bar | — | — | — | **REJECTED** (correlated stall, no read path) |

R1 and R2 are the two *cell bets* (mutually exclusive); R3 composes with either.
The recommended combo is **R2 + R3** (smallest blast radius, driven reset, plus
detectability); the best "6,400-times" combo is **R1 + R3** (80 moving decisions,
80-cell blast radius, R3 makes it visible).

### R1 — toggle-rocker row-shared state

One two-state printed rocker **per row** (80 total) toggles between two
hard-stopped angles and carries a 4-step staircase (0/10/20/30/40 mm). Every
column is **passive**: its tooth merely rests on the step the rocker exposes.
The per-cell state is a *rest position*, not a latch — no per-cell spring, no
per-cell release-force threshold.

```
   row (80 cells, 5.08 mm pitch)
   [col][col][col] ... [col]      <- passive columns + tooth
      \   \   \       /          <- teeth rest on steps
   === staircase (4 steps) ===    <- one shared rocker/row
            ||
      rocker pivot -> 2 hard stops
            ||  set by mask-gate stack (shared, bank-local)
```

**Honest cost:** the rocker must present each step as a positive stop under the
full row load (80 × 3.27 N = **261.6 N**); a stuck rocker takes out its **whole
row (80 cells)** — *detectable by R3*. Step tooth margin: 0.90 × 2.40 mm
compression land = **105.6 N** per cell vs 3.27 N → **32×**.

### R2 — double-acting wedge-gate cell

A 2-position sliding wedge sits in the 1.48 mm lane beside the 3.60 mm column.
High stop = a printed wall (cell stays low); low stop = a printed wall reached by
the **platen pushing the gate down**. This is the direct answer to S6-LC's
[DND-91](/DND/issues/DND-91) A8 failure ("release the pawls and trust gravity; a
jammed column silently keeps its stale height"). Here **reset is a driven,
positive event** — a sticky gate is pushed through; only a hard wedge (debris)
resists, and R3 finds it.

### R3 — mechanical read-rod readback

A comb of 80 compliant fingers sweeps a row; a finger that cannot seat transmits
an edge to one shared read-out rod (one **mechanical read point per row, 80
total**; 2 bought sensors). It does not reduce q — it converts *undetectable*
into *detectable and re-runnable*, which is the specific DND-103 criterion
("detectable, recoverable, local and repairable"). With a re-run recovery of
p ≥ 0.9, silent per-row error drops from **1.26e-4 to 1.26e-5** and the flagged
10 % is visible at the table.

### R4 — rejected (recorded as evidence)

One shared return bar that lifts every cell at once. **Force concentrates**
(sum of 6,400 cell forces ≈ **3,904 N** at a 0.61 N/cell class snap), a single
jam stalls the whole board, and there is no read path. Recorded as a **negative
result**: *shared state is only a win when the shared member tolerates a local
jam* (R1's per-row rockers do; R4's single bar does not).

## Reliability-audit schema (every primitive answers all of it)

Each primitive is passed through `audit()` and must supply: plain-English
mechanism, diagram, bought delta, repeated moving parts, precision contacts /
cell, compliant printed elements, wear interfaces, tolerance-sensitive
interactions, **correlated** failure modes, **single-cell** failure modes,
serviceability, decisive falsifier, 3×1 / 5×5 coupon test, and *what must work
6,400 times* — plus all **ten functional jobs**. A missing field or unanswered
job **fails the conformance gate** (`missing_fields` / `unanswered_jobs`).

## Honest timing (CALCULATION, assumption-class — not a measurement)

| Term | s |
|---|---:|
| 4 broadcast strokes @ (0.50 up + 0.15 settle + 0.20 return) | 3.40 |
| Mask write (8 banks × 0.50) | 4.00 |
| Driven reset (8 banks × 0.55, platen uses its own axis) | 4.40 |
| **Full-map visible transition** | **11.80** |
| R3 full read pass (reported **separately**, not hidden) | 20.00 |
| Regional read (one bank = 8 rows) | 2.00 |

The machine clears the **< 30 s** gate with **18.2 s margin**. The read pass is a
verify/regional step reported separately, per DND-103's "report visible
transition and sustained cycle separately".

## Reproduce

```bash
python 06-experiments/test14_low_cost_program/divergent/reliability_primitives_alpha.py
python 06-experiments/test14_low_cost_program/divergent/reliability_primitives_alpha_checks.py   # 30/30
python 06-experiments/test14_low_cost_program/divergent/tools/run_reliability_checks.py          # screen + checks + CAD
python tools/validate/analytic_printability.py \
  06-experiments/test14_low_cost_program/divergent/scad/reliability_cell.scad
```

CAD: [`scad/reliability_cell.scad`](scad/reliability_cell.scad) — R2 wedge gate
at true 5.08 mm pitch (`reliability_cell_assembly`, `coupon_witness` = 5×3),
R1 off-pitch row rocker, R3 read finger. The analytic printability gate is wired
in `tools/validate/analytic_printability.py::check_reliability_cell`: every
printed wall PASSes; the **only RISK is the deliberately compliant R3 sensing
finger** (0.80 mm) which is intended to flex and carries no load.

## Evidence discipline ([DND-27](/DND/issues/DND-27))

**No print, no purchase, no measurement.** Every force is CALCULATION over
sourced PLA-class values (E = 1500 MPa, yield/compress 50 MPa, μ 0.20–0.50,
[DND-48] 3.27 N/column load); every geometry is CAD. Prices are allowance-class.
Prices, forces, printability and timing are **not physically validated**;
the decisive falsifier for each primitive is the 3×1 / 5×5 coupon below.

## Cheapest test that can reject the family (before CAD/BOM detail)

**3×1 / 5×5 true-pitch coupon** (DND-27 forbids the print here — this is the
hand-off test definition):

- one row of R1 (one rocker + 3 columns): cycle the rocker through all 4 steps
  100× and measure which step each column rests on;
- three R2 cells: set/drive-reset 100× and measure gate seating, residual column
  height error, and worst-case gate running clearance (neighbour contact = fail);
- one R3 read comb: set a known mix of gate states, sweep 100× and measure the
  **detection rate** and **false-positive rate**.

**Kill thresholds:** R1 fails if the rocker cannot hold a hard stop under row
load without passing a step; R2 fails if the platen cannot drive all gates to
the low stop or the gate contacts its neighbour; R3 fails if it cannot separate
a seated gate from an unseated one at the 1.40 mm throw.

## Files

| File | Purpose |
|---|---|
| [`reliability_primitives_alpha.py`](reliability_primitives_alpha.py) | The primitives R1/R2/R3, the rejected R4, the audit harness, timing, BOM delta, decision. |
| [`reliability_primitives_alpha_checks.py`](reliability_primitives_alpha_checks.py) | 30 CI-style assertions pinning the headline (schema completeness, correlation arithmetic, timing, rejected-idea record). |
| [`scad/reliability_cell.scad`](scad/reliability_cell.scad) | CAD witness at true 5.08 mm pitch (R2 gate, R1 rocker, R3 finger). |
| [`tools/run_reliability_checks.py`](tools/run_reliability_checks.py) | Runs the screen + 30 checks + analytic CAD printability. |

## Decision

- **R1 — retain** as the best *"what must work 6,400 times"* primitive (80
  decisions), conditional on the rocker holding a positive stop under row load.
- **R2 — retain** as the smallest-blast-radius cell and the **removal of the A8
  gravity-drop failure class** (driven reset).
- **R3 — retain** as the mandatory pairing for any *correlated* state (R1): it
  is what converts a correlated error from disqualifying to recoverable.
- **R4 — rejected** and recorded as the negative result.
- **No architecture is promoted.** These are inputs to the
  [DND-104](/DND/issues/DND-104) synthesis.

See the operational record on [DND-106](/DND/issues/DND-106).
