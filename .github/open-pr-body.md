# DND-97: S6-LC mechanism-defect repair (A1/A2/A6/A7/A8) + mission-gate clarification

Repairs the remaining mechanism/geometry defects of the selected **S6-LC** machine
(`09-low-cost-variant/s6lc/`) flagged by the [DND-91](/DND/issues/DND-91) audit after
[DND-93](/DND/issues/DND-93) fixed the lift-axis gate G3 and the DND-74/91 bounded findings.
Mines the unmerged `cto/dnd93-fix-s6lc-g3` (#80) A1/A2 geometry work onto `main`, keeping DND-93's
conservative G3 choice (global broadcast + NEMA23-class lift) so the fixes do not conflict.

**Evidence class:** CALCULATION over sourced FDM limits + sourced actuator ratings + CAD (real
OpenSCAD, watertight). **No print, no purchase, no measurement** ([DND-27](/DND/issues/DND-27)).
**No board contact** ([DND-32](/DND/issues/DND-32)). `08-current-design/` untouched.

## Engineering question

Can S6-LC's mechanism defects (A1 cell fit, A2 pawl spring/hold, A6 reliability, A7 unloaded write,
A8 regional/jam) be repaired without re-opening the DND-93 G3 decision — and what is the honest
verdict against the **mission's** cost gate?

## Answer

**Defects repaired; mission gate passes; one measurement-gated item remains.**

- **A1 cell fit.** The cell owns only **half** the inter-body gap (0.74 mm); the old check compared
  the pawl against the whole 1.48 mm gap and the CAD placed it at `BODY/2 + 0.10`, overflowing the
  2.54 mm half-pitch by **0.260 mm**. Fixed: owned-lane gate, root block outboard, 0.45 mm leaf
  in-lane (`0.45 + 0.20 ≤ 0.74`), SCAD re-placed and re-rendered watertight.
- **A2 pawl spring + hold.** `k` now uses the **0.45 mm CAD leaf** (8× correction; release
  **0.020 N**). The softer leaf cannot hold by friction, so a **hold gate** is added, held by the
  **DND-76 P1 bistable over-centre latch** — a hard-stop compression, not a bending preload.
- **A6 reliability.** **G8** added, reported **explicitly UNRESOLVED** (no per-cell feedback; coupon
  C1 is the evidence path).
- **A7/A8.** The unloaded-write and regional/jam cases are restated as **explicit product
  limitations** needing a test, not bare assumptions.
- **Mission gate clarified.** DND-70's gate is the **purchased** figure ("under 250$ excluding
  3d printed parts"). `decide()` now separates the **mission gates (G1–G5, G7)** from the repo's
  internal 1.16 delivered convention (G6) and reports both: **G5 = $226.77 < $250 PASS**;
  G6 = $263.05 (over).

**Verdict: `PROMOTE_TO_09_WITH_MEASUREMENT_GATE`.**

## What changed

- `09-low-cost-variant/s6lc/analysis/s6lc.py` — owned-lane `column_fit`, leaf-section `pawl_spring`
  + hold gate, `reliability()` G8, `decide()` mission/delivered split and restated limitations.
- `analysis/s6lc_checks.py` (48/48), `printability_s6lc.py` (owned-lane keys), `scad/s6lc_machine.scad`
  (pawl re-placed) + re-rendered STLs, `03`-independent gates.
- `07-evidence-and-decisions/falsifier_dnd91_checks.py` (37/37) and `falsifier_dnd74_checks.py`
  (31/31) rewritten as **findings-resolution** gates.
- New ADR `07-evidence-and-decisions/dnd97-s6lc-mechanism-repair.md`; README updated; CI steps updated.

## Evidence produced

| Check | Result |
|---|---|
| `s6lc/analysis/s6lc_checks.py` | **48/48** |
| `falsifier_dnd91_checks.py` (resolution) | **37/37** |
| `falsifier_dnd74_checks.py` (resolution) | **31/31** |
| `s5r_ultra_checks.py` (DND-72 control) | 19/19 |
| `primitives_checks.py` / divergent runner | pass / exit 0 |
| `readme_s5r_coherence.py` | GATE PASS |
| CAD render `render_s6lc_cad.py` | 5 parts watertight |

## Gate table (corrected)

| Gate | Result |
|---|---|
| G1 cell fit (owned half-lane) | PASS |
| G2 release (banked) | PASS (128 N vs 413 N) |
| G3 lift axis (global board, NEMA23) | PASS (1.35×) |
| G4 full map < 30 s | PASS (11.96 s) |
| **G5 purchased parts < $250 (mission gate)** | **PASS ($226.77)** |
| G6 delivered < $250 (internal convention) | $263.05 — over |
| G7 reset-carriage torque | PASS |
| **G8 per-cell reliability** | **UNRESOLVED (measurement, coupon C1)** |

## Assumptions / limits

- G8 reliability is measurement-only (un-retirable under DND-27); coupon C1 is the path.
- Per-column lift load is the conservative S1 allowance (assumption-class), not measured.
- P1 latch snap-force spread across 6,400 parts (~±20 %) is assumption-class.

## Most informative next test

**Coupon C1** (unit-cell pitch/latch/hold/engage coupon) to bound A1/A2/G8, then sourced re-ratification
of the DND-93 BOM (tracked by [DND-98](/DND/issues/DND-98)). Physical build is gated by DND-27.
