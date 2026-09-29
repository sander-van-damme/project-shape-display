# DND-72: ultra-low-cost (<$250 purchased) — S6-LC selected + S5-R-trim infeasibility proof + CAD

**Consolidated single track.** Two divergent ultra-low-cost workstreams (this DND-72 track and the
DND-71 track) were reconciled under CEO consolidation direction. Output: **one BOM of record, one
selected architecture**, in the new subdirectory `09-low-cost-variant/`. `08-current-design/`
(S5-R, $404.60 delivered) is **untouched**.

**Evidence class:** CALCULATION over the promoted S5-R model, the S1/S2 screen, sourced-class
listings and sourced FDM process limits, plus CAD (real OpenSCAD). **No print, no purchase, no
measurement** ([DND-27](/DND/issues/DND-27)). **No board contact** ([DND-32](/DND/issues/DND-32)).

## Engineering question

Can the S5-R product be delivered under **$250 purchased** (excl. 3D-printed parts) while keeping
406.4 × 406.4 mm, 5.08 mm pitch, 6,400 cells, ≥ 40 mm travel, full-map < 30 s, regional updates and
X1C-buildability?

## Answer — two parts

**1. Trimming the S5-R architecture: NO.** The sub-$250 space is empty for this family. The binding
term is the **fixed no-channel purchased base** (frame, lift/drive, supply, loom, fasteners,
controller, PCB/passives allowance, spares): **$218.70 parts → $253.69 delivered**, which alone
exceeds the **$215.52 parts budget** ($250 / 1.16). Actuator headroom is **negative (−$3.18
parts)**. A **570-point** sweep over (R = rows-in-bank, writers, bank motors) finds **zero**
sub-$250 requirement-preserving points; the cheapest is **R6-W20-M2 at $345.90 delivered / 29.987 s**
— a **$95.90** gap.

**2. Changing the architecture: YES — S6-LC.** The fixed base is a *consequence* of the 40-solenoid
per-row writer bank and the 2-motor bank drive, not a law. The screened **S1 broadcast threshold
ratchet** family removes them:

| Quantity | S5-R | **S6-LC** | Class |
|---|---:|---:|---|
| Bought actuators | 42 | **3** | CAD + sourced |
| Purchased parts | $348.79 | **$139.77** | CALCULATION + sourced |
| Delivered (×1.16) | $404.60 | **$162.13** | CALCULATION |
| Full-map reconfiguration | 24.615 s | **7.4 s** | CALCULATION |
| Gates G1–G6 | — | **all pass** | CALCULATION |

S6-LC: passive printed pawl memory (no per-cell/per-row bought actuator), per-bank threshold mask
gate read from an **off-line punched card**, one lead-screw lift stepper, 8 banks × 10 rows bounding
the worst-case release force (1,025 N unbanked → 128 N banked vs 296 N ceiling). 50 mm travel
(5 × 10 mm).

## What changed

- **`09-low-cost-variant/s6lc/`** — the **selected machine**: `analysis/s6lc.py` (geometry, force,
  timing, BOM, gates), `analysis/s6lc_checks.py` (**29 checks**, all pass), `bom_s6lc.csv`,
  `scad/s6lc_machine.scad` + rendered `cad/stl/*` (5 parts), `evidence/`.
- **`09-low-cost-variant/s5r_ultra.py` / `s5r_ultra_checks.py`** — retained as the **negative
  result**: fixed-base floor, 570-point sweep, break-even ($345.90), `INFEASIBLE_UNDER_UNCHANGED_
  REQUIREMENTS` (**19 checks**, all pass).
- **`07-evidence-and-decisions/dnd72-low-cost-synthesis.md`** — the reconciliation ADR: why the two
  headlines are complementary, the selected machine, requirement-preservation table, residual
  uncertainty.
- **`09-low-cost-variant/README.md`** — rewritten to lead with S6-LC + the negative result.
- **CI:** adds the **S6-LC gate** step alongside the existing DND-72 trim gate.

## Evidence produced

| Check | Result |
|---|---|
| `09-low-cost-variant/s6lc/analysis/s6lc_checks.py` | **29/29 pass** — all six gates, `PROMOTE_TO_09` |
| `09-low-cost-variant/s5r_ultra_checks.py` | **19/19 pass** — trim infeasibility |
| `tools/validate/readme_s5r_coherence.py` | **GATE PASS** — S5-R headline untouched |

Pinned: S5-R **$404.60 / 24.615 s**; trim base **$218.70 → $253.69**; trim floor **$345.90 /
29.987 s**; S6-LC **$139.77 / $162.13 / 7.4 s**, 128.2 N banked release.

## Requirement-preservation (selected machine S6-LC)

| Requirement | Status | Class |
|---|---|---|
| 406.4 × 406.4 mm / 5.08 mm / 6,400 cells | preserved | CAD |
| ≥ 40 mm travel | 50 mm (5 × 10 mm) | CAD + calc |
| full-map < 30 s | **7.4 s** (margin 22.6 s) | CALCULATION |
| regional updates | per-bank mask + stroke + reset | CALCULATION |
| X1C-buildable | 5 watertight parts + sourced FDM-limit table | CAD + sourced |
| **purchased < $250** | **$139.77 parts / $162.13 delivered — PASS** | CALCULATION + sourced |

## Assumptions / limits

- **Mask preparation is off the visible budget**: a genuinely unannounced arbitrary map needs
  punched-card prep first (a stated product limitation; cards can be pre-written/reused). This is
  the price of removing the writer bank.
- **S1-D pawl release-force spread** across 6,400 printed parts is the live falsifier; banking
  bounds the total force, not the per-part spread.
- Platen assumed unloaded while writing; no per-cell feedback (same class as S5/S5-R).
- As-printed friction µ, pocket sharpness, pawl creep are measurement-only and un-retirable under
  [DND-27](/DND/issues/DND-27).

## Most informative next test

**Sourced ratification of the S6-LC BOM** ([DND-73](/DND/issues/DND-73)) and **adversarial audit**
([DND-74](/DND/issues/DND-74)) against `09-low-cost-variant/s6lc/bom_s6lc.csv` — the single BOM of
record — attacking the punched-card mask-write product statement and the S1-D pawl-spread
falsifier, the two terms that can still kill S6-LC. On close, DND-73/DND-74 auto-wake.
