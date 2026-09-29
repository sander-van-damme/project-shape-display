# DND-72 — Ultra-low-cost (<$250) synthesis: trim S5-R = NO; re-architect to S6-LC = YES

- **Issue:** [DND-72](/DND/issues/DND-72) (CTO). Parent [DND-70](/DND/issues/DND-70).
- **Status:** **SYNTHESIS — one architecture selected.** Two prior tracks (the DND-72 negative
  result and the DND-71 S6-LC candidate) are reconciled here. The answer to DND-70 is **S6-LC**;
  the negative result is retained as the proof that trimming the S5-R architecture cannot get there.
- **Evidence class:** **CALCULATION** over the promoted S5-R model, the S1/S2 screen, sourced-class
  listings and sourced FDM process limits + **CAD** (real OpenSCAD). **No print, no purchase, no
  measurement** ([DND-27](/DND/issues/DND-27)). No board contact ([DND-32](/DND/issues/DND-32)).
- **Artifacts:** `09-low-cost-variant/` — `s5r_ultra.py` + `s5r_ultra_checks.py` (19 checks,
  the negative result) and `s6lc/` (`analysis/s6lc.py` + `s6lc_checks.py` 29 checks, CAD, BOM,
  evidence). This ADR.

## 1. Why a synthesis was needed

Two parallel ultra-low-cost workstreams were opened under DND-70 within ~60 s of each other:
the **DND-72** track ([DND-72](/DND/issues/DND-72)) and the **DND-71** track
([DND-71](/DND/issues/DND-71)). They asked the same question and produced two headlines that read
as contradictory:

| Track | Subdir | Headline |
|---|---|---|
| DND-72 | `09-low-cost-variant/` | **INFEASIBLE** under unchanged requirements; break-even **$345.90 delivered** |
| DND-71 | `09-lowcost-alternative/` (now folded to `09-low-cost-variant/s6lc/`) | **S6-LC** machine, **$162.13 delivered / 7.4 s** |

They are **not contradictory** — they answer two different questions. This ADR fixes that.

## 2. The reconciliation

**Q1 — "Can the S5-R architecture be trimmed under $250?"** **No** (DND-72).
The binding term is the *fixed no-channel base inherited from S5 lift/scan/frame stock*:
**$218.70 parts → $253.69 delivered with zero actuators**, which alone exceeds the $215.52
parts budget ($250 / 1.16). Actuator headroom is **negative (−$3.18 parts)**. A 570-point sweep
over (rows-in-bank, writers, bank motors) finds **zero** requirement-preserving sub-$250 points;
the cheapest requirement-preserving point is **R6-W20-M2 at $345.90 delivered / 29.987 s**. This is
correct and is pinned by 19 checks.

**Q2 — "Is there a *different* architecture under $250 that keeps every mission requirement?"**
**Yes — S6-LC** (from the DND-71 track). The fixed base is not a law of physics; it is a
consequence of **the 40-solenoid per-row writer bank and the 2-motor bank drive** that the S5-R
family requires. Change the family and the base disappears:

- **Family:** the already-screened **S1 broadcast threshold ratchet** (Test11 S1/S2 screen,
  `04-architecture-candidates/`). Height is held by a **passive printed cantilever pawl**, so
  there is **no per-cell and no per-row bought actuator**.
- **Selection:** a **per-bank threshold mask gate** read from an off-line **punched card** replaces
  the 40 writer solenoids.
- **Lift:** **one** lead-screw stepper over a printed frame replaces the S5 lift/scan/frame stock.
- **S1's two open failures are addressed, not ignored:** the mask-write time goes **off the visible
  budget** (double-buffered punched card, an explicit product statement), and the worst-case
  simultaneous release force is bounded by **banking** (8 banks × 10 rows: unbanked 1,025 N →
  banked 128 N, ceiling 296 N).

**Cost cliff is actuator count, not part quality.** Bought actuators fall from 42 (S5-R) to **3**
(S6-LC), and the fixed base from **$218.70** to a **$139.77 total purchased BOM**.

## 3. Selected machine — S6-LC

| Quantity | Value | Class |
|---|---:|---|
| Active area / pitch / cells | 406.4 × 406.4 mm / 5.08 mm / 6,400 | CAD + CALC |
| Travel | 5 levels × 10 mm = **50 mm** (≥ 40 mm) | CAD + CALC |
| Full-map reconfiguration | **7.4 s** (4 broadcast strokes + banked reset) | CALCULATION |
| Regional update | one bank: one mask + one stroke + reset | CALCULATION |
| Purchased parts (excl. printed) | **$139.77** | CALCULATION + sourced |
| Delivered (×1.16) | **$162.13** (margin **$87.87**) | CALCULATION |
| Bought actuators | **3 steppers** (lift, mask index, reset carriage) | CAD + sourced |
| Worst-case release force | 128.2 N banked vs 296 N ceiling | CALCULATION |
| Gates (G1–G6) | **all pass** (`verdict = PROMOTE_TO_09`) | CALCULATION |

Reproduce: `python 09-low-cost-variant/s6lc/analysis/s6lc_checks.py` → **29/29 pass**;
`python 09-low-cost-variant/s5r_ultra_checks.py` → **19/19 pass**.

## 4. Requirement preservation (S6-LC, all against DND-70's unchanged list)

| Requirement | Status | Class |
|---|---|---|
| ~400 × 400 mm active area | 406.4 × 406.4 mm | CAD |
| 5.08 mm pitch / 6,400 cells | body 3.60 + lane 1.48 = 5.08 mm; 80 × 80 | CAD + CALC |
| ≥ 40 mm travel | 50 mm (5 × 10 mm) | CAD + CALC |
| full-map < 30 s | **7.4 s** (22.6 s margin) | CALCULATION |
| regional updates | per-bank mask + stroke + reset | CALCULATION |
| X1C-buildable | 5 watertight parts, sourced FDM-limit table | CAD + sourced |
| **purchased < $250** | **$139.77 parts / $162.13 delivered** | CALCULATION + sourced |

## 5. Residual uncertainty (carried honestly, not retired)

- **Mask preparation is off the visible budget.** A genuinely unannounced arbitrary map needs
  punched-card prep first; a card can be pre-written/reused. This is the deliberate price of
  removing the writer bank and is the single largest product-facing caveat.
- **Pawl release-force spread across 6,400 printed parts** is the S1-D risk; banking bounds the
  total force but not the per-part spread. Break-even sd ≈ 9 % of mean vs typical FDM 10–20 %
  (assumption) — a genuine falsifier.
- **Platen assumed unloaded while writing** (miniatures off the written region), else hold and lift
  compete.
- **No per-cell feedback** — a missed pawl is a silent local height error (same class as S5/S5-R).
- **As-printed friction µ, pocket sharpness, pawl creep** are measurement-only and un-retirable
  under DND-27.

## 6. Decision and next steps

1. **Selected architecture for DND-70 = S6-LC**, in `09-low-cost-variant/s6lc/`. `08-current-design/`
   (S5-R, $404.60) is untouched.
2. The DND-72 negative-result model (`s5r_ultra.py`) is **retained** as the proof that trimming the
   S5-R family cannot reach $250 — it is the reason S6-LC is a new family, not a trim.
3. **Cost ratification** ([DND-73](/DND/issues/DND-73)) and **adversarial audit**
   ([DND-74](/DND/issues/DND-74)) should run against the **S6-LC BOM** (`s6lc/bom_s6lc.csv`),
   not the S5-R trim — this is the single BOM of record.
4. The most informative next test is **sourced**: ratify each S6-LC BOM line against live listings,
   then adversarially attack the punched-card mask-write product statement and the S1-D pawl-spread
   falsifier, since those are the two terms that can still kill S6-LC.
