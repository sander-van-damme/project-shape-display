# DND-107 — reliability-first whole-machine architectures (InventorBeta, mask + non-mask)

**Status: 3 complete machines screened; B2 and B3 clear both mission gates;
B1 is a reported FAILED candidate (a real negative result).**

This file is the short companion to
[`analysis/reliability_machines_beta.py`](analysis/reliability_machines_beta.py)
for [DND-107](/DND/issues/DND-107) (child of [DND-104](/DND/issues/DND-104)).
The S6-LC machine ([`../s6lc/`](../../../08-integrated-designs/s6lc-low-cost/README.md)) was attacked by
[DND-91](/DND/issues/DND-91): its correctness rests on **6,400 printed keepers**
and **6,400 pawls**, with a ~0.45 mm leaf, a stiffness-set latch and no per-cell
feedback. [DND-103](/DND/issues/DND-103) then made reliability and buildability
**first-class gates**. This deliverable is the reliability-first divergence.

> **Evidence class. Everything here is CALCULATION over the imported S5-R/S6-LC
> model + sourced-class allowances + CAD constants. No part has been printed,
> purchased or measured** ([DND-27](/DND/issues/DND-27)).

## The gate question: "what has to work correctly 6,400 times?"

| Machine | Answers the 6,400x question with | Repeat count of the *decision* element |
|---|---|---:|
| S6-LC (reference) | 6,400 keepers + 6,400 pawls | **6,400** |
| **B1** shared-shaft screw memory | 6,400 passive nuts on threads (no spring) | 6,400 threads, 0 compliant decisions |
| **B2** pressure blanket + hold | 6,400 living-hinge toggles (binary flip only) | **6,400** toggles |
| **B3** rotary drum mask | **80** drum tracks + 6,400 passive hard-stop pawls | **80** |

## The three machines

| | **B1** shared-shaft binary screw/nut | **B2** single-source pressure blanket | **B3** rotary drum mask |
|---|---|---|---|
| Mask? | **No** | **No** | Yes |
| Bought actuators | 3 steppers | 1 stepper + 1 valve (+pump) | 3 steppers |
| Parts / delivered | $68.39 / **$79.33** | $62.80 / **$72.85** | $74.39 / **$86.29** |
| Visible transition | **170.9 s (FAIL)** | **14.26 s (PASS)** | **22.46 s (PASS)** |
| Sustained cycle | 170.9 s | 14.26 s (mask-free) | 22.46 s (drum write double-buffered) |
| Per-cell compliant element | **0** | 6,400 toggles (binary, 2-line) | 6,400 pawls (hard-stop; keeper deleted) |
| Verdict | **FAIL_AS_DRAWN** | **PASS** | **PASS** |

### B1 — shared driveshaft binary screw/nut memory (NON-MASK) — **FAILED**
Every column rides a captive nut on a non-rotating threaded post; a shared
horizontal shaft turns a row's posts only when that row's selector rail engages
its tumblers. Height is thread position against **hard stops**; there is **no
per-cell compliant decision element at all**. It is the most reliable of the
three *and it fails 30 s*. The screw lead is a three-way trap:

- serial rows: **1,617 s** (~54× over budget);
- gang selection fixes speed but multiplies shaft torque — the sourced two-end
  NEMA17-class drive caps the gang at ~55 rows, whose best timing is still
  **> 30 s** (`gang_sweep`);
- a larger lead is faster but stops self-locking (needs a brake) **and** raises
  torque linearly (`lead_sweep`).

**No lead/gang setting clears both the 30 s timing and the torque gate.** B1's
value is the negative result: a shared-shaft binary screw memory cannot meet the
mission on a low-cost stepper class. Recorded as a failure.

### B2 — single-source pressure blanket + mechanical hold (NON-MASK) — **PASS**
One pump/valve pressurises a common bladder; all columns rise together to a hard
top stop; one write bar flips a printed 2-state toggle for columns that must
stay. Drop pressure → unlatched columns fall to datum. Blanket force margin is
**+3,520 N** over 6,400 × 0.20 N. The toggle's spring sets only the **binary
flip**, not the height (a hard stop does), so B2 does **not** inherit S6-LC's
continuous-force correctness.
*Limits:* regional reveal is not free (common blanket → zoned bladder or a
full re-lift), and terrain is **binary 0/40 mm only** without a second toggle
stack.

### B3 — rotary drum mask, written once per map, read mechanically (MASK) — **PASS**
A rotary drum carries one bit track per **row** (80 tracks), rewritten between
maps by one travelling carriage and read by a fixed follower during the same
four broadcast strokes S6-LC uses. It **deletes the per-cell keeper** and keeps
only the hard-stop pawl: the repeated decision count drops **80×** (6,400 → 80),
and a bad track fails a whole row **visibly** instead of silently.
*Limits:* drum write is the product (45 s off-line, hidden only by
double-buffering); track registration is a correlated row-level failure.

## Reliability audit (DND-103 required fields)

| Field | S6-LC | B1 | B2 | B3 |
|---|---:|---:|---:|---:|
| Repeated moving parts | 6,400 | 6,400 | 6,400 | 6,400 |
| Precision contacts / cell | 2 | 1 | 1 | 1 |
| Compliant printed elements | 6,400 | **0** | 6,400 | 6,400 |
| Tolerance-sensitive / cell | 6,400 | 1 (per row) | 6,400 | 80 |
| Min repeated feature | **0.45 mm** | 1.20 mm | 0.90 mm | 0.90 mm |
| Detection path | none per cell | row motor stall | visible on binary map | whole-row visible |

Correlated vs single-cell failures and serviceability are enumerated per machine
in the model (`*_AUDIT` dicts / `screen()` output).

## The cheapest test that can reject each idea

- **B1:** already rejected analytically (`gang_sweep` + `lead_sweep` disjoint
  sets). No coupon worth printing unless a stronger drive is proposed.
- **B2:** 5-column strip with one bladder region + one write-bar cam profile,
  cycled ~200×; measure toggle engagement **and** release rate.
- **B3:** one drum-track segment + follower + gate, cycled ~500× at true 10 mm
  stroke pitch; measure track-open reliability and write-carriage edge quality.

## Reproduce

```bash
python 06-experiments/test14_low_cost_program/divergent/tools/run_reliability_machines_checks.py
```

## Files

| Path | What |
|---|---|
| [`analysis/reliability_machines_beta.py`](analysis/reliability_machines_beta.py) | machine model: allocation, BOM, timing decomposition, gates, reliability audit |
| [`analysis/reliability_machines_beta_checks.py`](analysis/reliability_machines_beta_checks.py) | 28 CI-style assertions |
| [`scad/b2b3_reliability_cell.scad`](scad/b2b3_reliability_cell.scad) | B2/B3 repeated-feature CAD witness at true pitch |
| [`tools/run_reliability_machines_checks.py`](tools/run_reliability_machines_checks.py) | runner |

## Residual uncertainty
- All force, torque, pressure and timing figures are **assumption-class** over a
  sourced model; no measurement.
- B2 toggle hinge **fatigue life** and B3 drum-track **registration tolerance**
  are measurement-only and are the two real unknowns.
- No full multi-row assembly interference check; only unit cells/witnesses.
