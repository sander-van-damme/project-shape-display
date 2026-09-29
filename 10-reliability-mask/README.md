# 10 — Reliability-first low-cost shape display + automatic mask system (DND-104)

**Status: new candidate architecture selected — `A1 binary-latch + shared
writer/reader`.** This is the DND-104 program root. It works from the low-cost
family in [`09-low-cost-variant/`](../09-low-cost-variant/README.md), **not** from
the mechanically dense S5-R in [`08-current-design/`](../08-current-design/README.md)
(untouched, provenance). `09-*/` (S6-LC) is also untouched — this is a *new*
subdirectory.

Owner: CTO. Parent: [DND-104](/DND/issues/DND-104). Program umbrella:
[DND-102](/DND/issues/DND-102). Criteria of record:
[`02-design-criteria/README.md`](../02-design-criteria/README.md) (strengthened by
[DND-103](/DND/issues/DND-103), PR #83).

> **Evidence class.** Everything here is **CALCULATION over sourced FDM process
> limits and sourced actuator ratings**, plus **CAD** (real OpenSCAD + trimesh
> mesh validation). **No part has been printed, purchased or measured**
> ([DND-27](/DND/issues/DND-27)). Prices are point-in-time sourced-class figures
> (2026-09). Nothing here is a physical validation.

## 1. What DND-104 asked, and the central design move

[DND-104](/DND/issues/DND-104) asked for a **reliability-first** low-cost machine:
very few bought actuators, mechanically simple repeated cells, tolerant of FDM
variation, maintainable, with **detectable/recoverable/local/repairable** failure
modes, arbitrary D&D terrain, and **masks developed together with the display**.

The DND-103 criteria added the decisive gate:

> **What has to work correctly 6,400 times?** Minimise it. Prefer *thousands of
> simple things + a few sophisticated shared mechanisms* over *thousands of tiny
> sophisticated mechanisms that happen to fit in CAD*.

The S5-R and S6-LC machines both fail this gate in the same structural way: they
have **6,400 independent passive cells, no per-cell feedback, and a silent
wrong-cell failure mode**. At a 0.01 % per-cell error the whole map is correct only
**52.7 %** of the time (`(1−q)^6400`). A missed latch is invisible and
uncorrectable. S6-LC's own adversarial audit ([DND-91](/DND/issues/DND-91), A6)
called this out and left it unresolved.

**The central move of this program is to make the repeated state *verifiable*.**
A1 keeps the dense visible surface passive and cheap, but adds a **shared
external reader** that scans the field after writing. A failed toggle is *detected
and re-driven* instead of being silently wrong. This converts the reliability
problem from "6,400 independent silent mechanisms" to "a few shared, monitored
mechanisms + a bounded retry loop".

## 2. Divergence first — seven materially different architectures

The screen ([`analysis/reliability_mask.py`](analysis/reliability_mask.py)) defines
seven architectures as first-class data and prints every field for each. Nothing
was pre-picked.

| # | Architecture | Family | Bought actuators | States | Mask medium | Silent elements | Full map | Parts |
|---|---|---|---|---:|---:|---|---:|---:|---:|
| **A1** | **binary-latch + shared writer/reader** | **external shared writer/verifier** | **4** | **2** | **none (direct write)** | **0** | **24.15 s** | **$181** |
| A2 | global broadcast binary interlock | broadcast lock-and-lift | 2 | 5 | printed interlock plate | 6,400 | 11.05 s | $224 |
| A3 | punched-film mask + biased columns | physical bit-image film | 2 | 2 | punched film (consumable) | 6,400 | 33.55 s | $187 |
| A4 | rewritable printed comb mask | reusable printed comb | 2 | 2 | printed louvre comb | 6,400 | 17.55 s | $171 |
| A5 | banked binary ratchet + coarse readback | broadcast threshold ratchet | 4 | 2 | per-bank threshold mask | 6,392 | 17.05 s | $213 |
| A6 | embossed-tape mask | continuous relief tape | 2 | 2 | embossed tape | 6,400 | 29.55 s | $179 |
| A7 | shared-camshaft bank + binary latch | rotating camshaft per bank | 1 | 2 | camshaft angle | 6,400 | 13.05 s | $158 |

Each architecture's full record (ten-job allocation, reliability audit, correlated
vs single-cell failure modes, serviceability, timing stages, BOM sketch, prototype
coupon and **decisive falsifier**) is emitted by `screen()` and tabulated in
[`analysis/architecture_table.md`](analysis/architecture_table.md).

## 3. The reliability gate in detail (per architecture)

The gate has three parts, all required by DND-103:

1. **Silent-set size** `N_s` — independent repeated parts whose single failure
   yields a wrong visible cell *that the machine cannot notice*.
2. **Readback** — can the machine detect a wrong cell and recover?
3. **Coupon** — is there a cheap printed coupon that can bound the as-printed
   spread?

| # | Repeated moving parts | Precision contacts/cell | Compliant printed parts | Wear interfaces | Silent `N_s` | Readback | Recovery |
|---|---:|---:|---:|---:|---:|---|---|
| **A1** | 6,400 latch arms | **0** | **0** | 6,400 hinges | **0** | **yes (reader)** | **scan → re-write failed cells** |
| A2 | 12,800 | 1.0 | 6,400 | 12,800 | 6,400 | no | full reset only |
| A3 | 6,400 | 0.3 | 6,400 | 6,401 | 6,400 | no | full reset |
| A4 | 6,400 | 0.25 | 6,400 | 12,800 | 6,400 | no | full reset |
| A5 | 6,400 | 0 | 0 | 6,400 | 6,392 | bank-only | per-bank re-home |
| A6 | 6,400 | 0.35 | 6,400 | 6,401 | 6,400 | no | full reset |
| A7 | 6,400 | 0.2 | 6,400 | 7,040 | 6,400 | no | full reset |

**A1 is the only architecture with a structurally zero silent-error set**, because
the reader verifies every cell. A1's state is also the only one with **zero
precision contacts per cell and zero compliant printed parts deciding
correctness** — the armed/disarmed state is bounded by two printed hard stops and
held in compression (the DND-103 "preferred" list, not the "strongly discouraged"
list).

**The map-yield consequence** (program reliability model, `(1−q)^N`):

| Per-cell error q | A1 (N=0) | every other (N≈6,400) |
|---|---:|---:|
| 1e-4 | 100 % | 52.7 % |
| 1e-5 | 100 % | 93.8 % |
| 1.57e-6 (99 % budget) | 100 % | 99.0 % |

For A1 the only remaining question is whether the **reader detection + retry loop**
converges; for the others the per-cell error itself must be proven below 1.57e-6,
which no architecture here (nor S6-LC) can demonstrate analytically.

## 4. Selected machine — A1 binary-latch + shared writer/reader

### 4.1 The mechanism in plain English

- **Visible surface:** an 80 × 80 array of square printed columns at **5.08 mm
  pitch**, **406.4 × 406.4 mm**, **6,400 cells**. Each column has exactly **two
  states**: down (0 mm) and up (40 mm). Five visual height levels are formed by
  combining cells; the columns themselves are strictly binary, which is the
  reliability decision (one hard stop pair, no analog pocket depth).
- **State memory:** a printed **over-centre toggle latch** per cell. The arm
  travels between **two printed hard stops**; it is held against one stop in
  **compression** by the load path, not by a printed spring's force. The state is
  a *position*, and it is exact.
- **Selection / writing:** a **2-axis gantry** carries a **writer head** and a
  **reader head** across the field. The writer toggles only the latches that must
  change. No per-cell and no per-row bought actuator exists.
- **Verification and recovery:** after the write pass, the **reader head** scans
  all 6,400 cells. Cells whose state disagrees with the target are re-written
  (bounded retry). A failed toggle is therefore **detected**, not silent.
- **Reset:** a single global **reset stroke** drops all up-columns to the down
  stop before a new map (one shared mechanism).
- **Automatic mask system:** A1 needs **no physical mask medium** — the "mask" is
  streamed digitally to the writer head. This is the strongest possible answer to
  the mask-subsystem requirement: mask-generation latency is ~0, it cannot tear,
  register or wear, and it is regenerated for free every map. The price is that
  the *writer bandwidth* becomes the product-critical number (§4.2).

### 4.2 The decisive number — writer/reader bandwidth

The whole A1 claim rests on the head being able to write and read at the required
rate. This is **computed**, not asserted (`writer_bandwidth()` in the model):

| Term | Value | Basis |
|---|---:|---|
| Parallel writer heads | 8 | 8 heads on one gantry bar |
| Per-head rate | 1,000 cells/s | 1 ms/cell toggle-or-read (assumption-class) |
| Effective rate | 8,000 cells/s | 8 × 1,000 |
| Worst-case write-all (6,400) + 80-lane overhead | **8.8 s** | `writer_bandwidth()` |
| Verify pass (6,400) + 80-lane overhead | **8.8 s** | `writer_bandwidth()` |
| Reset + settle + transport + map processing | **6.55 s** | model |

Total worst-case full-map cycle = **24.15 s < 30 s** (5.85 s margin), *including*
verification. Typical maps (≈half the cells change) are faster.

> **The one assumption that can kill A1:** 1 ms/cell for a mechanical/optical
> toggle-and-read at a ~2 mm working gap. Prototype B (5×5) is the cheapest test
> that bounds it. If the head cannot reach ~1 ms/cell, A1's timing dies — and the
> falsifier says so explicitly.

### 4.3 Honest timing decomposition (DND-103 requirement)

| Stage | Seconds | Notes |
|---|---:|---|
| Digital map processing | 0.05 | rasterise target to head stream |
| Physical mask generation | **0.00** | **no physical mask** (direct write) |
| Mask transport / indexing | 2.00 | gantry lane repositioning |
| Display reset | 3.00 | global reset stroke |
| Broadcast lift / write | 8.80 | worst-case all-change write |
| Settling / locking | 1.50 | two-state hard stop settles fast |
| **Verification** | **8.80** | **reader pass (this is the reliability feature)** |
| **Full cycle** | **24.15** | **visible transition = full (no hidden prep)** |

Because there is no physical mask, there is **no hidden preparation**: the
*sustained arbitrary-map cycle time* **equals** the *visible transition time*. This
is the one architecture in the program with no off-line mask caveat.

### 4.4 Reliability audit (DND-103 per-architecture audit)

| Field | A1 value | Class |
|---|---|---|
| Repeated moving parts | 6,400 latch arms (1/cell) | CAD |
| Precision contacts per cell | **0** (hard stops) | CAD |
| Compliant printed elements | **0** | CAD |
| Wear interfaces | 6,400 hinge pivots (compression-loaded) | CAD |
| Tolerance-sensitive interactions | latch-to-stop land (generous 0.88 mm land) | CAD |
| Correlated failure modes | gantry/reader fault → region wrong, **but detected** | calc |
| Single-cell failure modes | failed toggle → read back, re-driven | calc |
| Serviceability | gantry replaceable; frame is modular tiles | CAD |
| Detectable / recoverable / local / repairable | **all four** | design |

**What has to work correctly 6,400 times?** — the *reader must correctly classify
each cell*, and the *writer must toggle most cells first try*. But unlike every
other architecture, a miss is **observed and repaired**. The repeated mechanism
that must be *perfect* is reduced from 6,400 latches to **8 shared heads**.

### 4.5 Purchased BOM

| Line | Qty | Ext USD | Evidence |
|---|---:|---:|---|
| X gantry stepper (NEMA17-class) | 1 | 14.00 | sourced-class |
| Y/head-traverse stepper (NEMA17-class) | 1 | 14.00 | sourced-class |
| Writer toggle actuator | 1 | 9.00 | sourced-class |
| X guide rail pair + bushings | 1 | 22.00 | sourced-class |
| Y guide rail + bushings | 1 | 16.00 | sourced-class |
| Timing belts + pulleys (X, Y) | 2 | 16.00 | sourced-class |
| Writer head body + toggle prong | 1 | 6.00 | allowance |
| Reader head (reflectance/photodiode row) | 1 | 12.00 | sourced-class |
| Controller (RP2040) | 1 | 5.00 | sourced-live |
| Stepper drivers (DRV8833-class) | 3 | 6.00 | sourced-live |
| Power supply + protection (24 V) | 1 | 12.00 | sourced-listing |
| Wire / connectors / flex loom | 1 | 18.00 | sourced-class |
| Limit / home switches | 5 | 5.00 | sourced-class |
| Frame splice hardware | 1 | 10.00 | allowance |
| Fasteners (M3 assortment) | 1 | 8.00 | sourced-class |
| Spares and miscellaneous | 1 | 8.00 | assumption |
| **Purchased parts** | | **$181.00** | **mission gate < $250 PASS** |
| **Delivered (×1.16)** | | **$209.96** | internal convention PASS |

Full table: [`bom_a1.csv`](bom_a1.csv). The **bought-actuator count is 4** (three
motors + one writer actuator class). There is **no per-cell and no per-row bought
actuator**. Printed frame, columns, latch arms and cradle lands are excluded per
[DND-70](/DND/issues/DND-70).

### 4.6 Prototype ladder (DND-103 requirement)

| Stage | Scope | Validates | Kills the program if… |
|---|---|---|---|
| **A — single cell** | 1 cell at true pitch | latch holds 3.27 N in compression; writer toggles it; reader distinguishes states | latch won't toggle at writer force, or reader can't tell states |
| **B — 5×5 array** | 25 cells, short gantry | neighbouring tolerances, writer repeatability, scan-verify + retry catches a deliberately stuck cell | placement error > half pitch, or reader can't resolve 1 wrong cell in 25 |
| **C — one bank** | 10 × 80 = 800 cells | bank reset, gantry traverse, tabletop load under a placed mini, correlated faults | a bank write exceeds the linear timing extrapolation |
| **D — multiple banks** | 4 banks = 3,200 cells | cross-bank timing, sustained throughput, head duty drift, regional update | sustained cycle > 30 s or accuracy drifts |
| **full machine** | 6,400 cells | full < 30 s arbitrary map + regional update | only reached after A–D survive |

### 4.7 Decisive falsifier

> **The writer head cannot both toggle AND read a latch within a ~2 mm working
> gap at ~1 ms/cell across 406 mm.** If that fails, A1's timing (and its sole
> reliability advantage) dies. Cheapest test: **coupon A** (one cell, flip+read).

Secondary falsifiers: gantry XY registration over 406 mm (belt stretch, thermal)
must hold half-pitch placement; the latch hinge must survive 6,400-cycle wear
(measurement-only under DND-27).

## 5. Why not the runners-up

| Architecture | Why it loses the reliability gate |
|---|---|
| A5 banked binary ratchet | Best of the rest (reliability score 6.4), but readback is **per-bank only**; a single stuck cell inside a bank stays silent — **6,392 silent elements**. |
| A7 shared-camshaft | Only **1** bought actuator, but **6,400 silent elements** and a printed 80-lobe camshaft repeatability risk (≤0.1 mm angular) is unproven. |
| A4 rewritable comb | **6,400 silent elements**; the comb writer is itself a repeated precision mechanism; a stuck slat corrupts an 80-cell band. |
| A3 punched film | **6,400 silent elements**; a consumable that must register 80 holes to <0.1 mm and can tear. Also fails <30 s as modelled (33.55 s). |
| A6 embossed tape | **6,400 silent elements**; tape creep under follower load blurs the relief; near the timing edge (29.55 s). |
| A2 global interlock | **6,400 silent elements**; a stuck interlock is invisible; needs a per-level plate that is itself precision. |

The gap is not marginal: A1's silent set is **0**, every other is **≈6,400**. On
the program's own reliability model that is the difference between a map that is
always correct and a map that is ~53 % correct at a plausible 0.01 % per-cell
defect rate.

## 6. Decision: selection vs promotion (S5-R is untouched)

**This is a new candidate, not a silent replacement.** `08-current-design/`
(S5-R, promoted machine, $404.60 delivered, 24.615 s) and `09-low-cost-variant/`
(S6-LC) are **unchanged**. A1 lives in a new directory and is proposed as the
**reliability-first low-cost candidate** for the program.

| Machine | Bought actuators | Silent cells | Full map | Parts | Delivered | Reliability gate |
|---|---:|---:|---:|---:|---:|---|
| S5-R (`08-`) | 42 | 6,400 | 24.615 s | $348.79 | $404.60 | fails (silent, no readback) |
| S6-LC (`09-`) | 3 | 6,400 | 11.96 s | $226.77 | $263.05 | unresolved (G8 measurement-only) |
| **A1 (`10-`, new)** | **4** | **0** | **24.15 s** | **$181.00** | **$209.96** | **passes (0 silent; reader + retry)** |

A1 does **not** beat S6-LC on raw speed or actuator count. It beats it — and S5-R —
on the **reliability gate that DND-103 made first-class**, and it is cheaper than
both. Under the program's stated priority ("reliability/buildability outrank the
last few dollars"), that is the decisive advantage.

**Promotion proposal:** promote **A1** as the reliability-first low-cost candidate
at the next convergence gate, *conditional on* prototype A/B bounding the
writer/reader rate and the latch toggle. This is an explicit proposal, not an
automatic replacement (per DND-104 §5).

## 7. Failure modes, recorded honestly

- **If 1 ms/cell is unreachable**, A1's 24.15 s becomes >30 s and the design must
  either add heads (cost) or reduce verification frequency (reliability cost). The
  falsifier is recorded; the program should not hide this.
- **If the reader cannot resolve a single wrong cell** among 6,400 (contrast,
  reflections, adjacent-cell crosstalk), the "0 silent" claim collapses to
  "6,400 silent with an expensive decoration". Prototype B is the kill test.
- **Gantry registration** over 406 mm is the classic 2-axis failure; belt stretch
  and thermal drift are unmeasured. A position-repeatability coupon is required.
- **Hinge wear** across 6,400 pivots is measurement-only under DND-27; the
  compression hold removes the *spring-force* risk but not wear.
- **Column top load path** is a compression hard stop (good), but the exact land
  dimensions are CAD-provisional until a calibration coupon exists.

## 8. Reproduce

```bash
# architecture screen (7 machines, full JSON)
python 10-reliability-mask/analysis/reliability_mask.py

# convergence: selection, why, bandwidth, prototype ladder, falsifier
python 10-reliability-mask/analysis/reliability_mask.py convergence

# 35 pinned regression checks
python 10-reliability-mask/analysis/reliability_mask_checks.py

# CAD: render + mesh-validate the binary-latch cell (real OpenSCAD, hard-fails if absent)
export PATH="$HOME/.local/bin:$PATH"
python 10-reliability-mask/analysis/render_a1_cad.py

# generate the full comparison table
python 10-reliability-mask/analysis/make_table.py
```

## 9. Files

| Path | What |
|---|---|
| [`analysis/reliability_mask.py`](analysis/reliability_mask.py) | the architecture screen, reliability gate, timing, BOM, convergence |
| [`analysis/reliability_mask_checks.py`](analysis/reliability_mask_checks.py) | 38 regression checks |
| [`analysis/render_a1_cad.py`](analysis/render_a1_cad.py) | OpenSCAD render + mesh validation |
| [`analysis/make_table.py`](analysis/make_table.py) | emits the full per-architecture comparison table |
| [`analysis/architecture_table.md`](analysis/architecture_table.md) | the generated comparison table |
| [`scad/a1_binary_latch_cell.scad`](scad/a1_binary_latch_cell.scad) | the A1 unit cell (real OpenSCAD) |
| [`cad/stl/`](cad/stl/) | watertight rendered parts (column, latch, cradle) |
| [`cad/render_record.json`](cad/render_record.json) | mesh-validation record |
| [`bom_a1.csv`](bom_a1.csv) | A1 purchased BOM |
| [`../../07-evidence-and-decisions/dnd104-reliability-mask.md`](../../07-evidence-and-decisions/dnd104-reliability-mask.md) | the ADR / decision record |

## 10. Residual uncertainty (all measurement-only or product)

- Writer/reader rate (1 ms/cell) and single-cell read resolution — assumption-class.
- Gantry XY registration over 406 mm — unmeasured.
- Hinge wear across 6,400 pivots — measurement-only (DND-27).
- As-printed latch hard-stop dimensions and toggle snap force spread — measurement-only.
- Column top land dimensions — CAD-provisional until a calibration coupon exists.

A1 is **not** claimed print-ready or physically validated. It is a *definition*
whose every **mission gate passes on DND-27 evidence classes** and whose
reliability structure is the only one in the program that converts 6,400 silent
failures into a monitored, recoverable, local failure.
