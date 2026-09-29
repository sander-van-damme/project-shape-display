<!-- © 2024 Sander Van Damme - All Rights Reserved. -->

# SHA-14 A1 analytic hardening — tolerance + printability + BOM-margin audit

> **Evidence class: CALCULATION over placed A1 CAD + sourced FDM rules only**
> (DND-27). This note prints, purchases, and measures nothing. Nothing here
> is physical validation. S5-R and S6-LC are untouched. No new CAD was
> created: geometry deltas D1/D2 are proposed annotations, not modelled edits.

## Context

[SHA-7](sha7-a1-promotion-decision.md) gated A1 (architecture PROMOTED, build
MEASUREMENT-GATED on coupon A); [SHA-9](sha9-a1-gate-residuals-regional.md)
retired R5 (8-head rule) and half-retired R6 (geometry); [SHA-13](sha13-a1-coupon-readiness.md)
delivered CAD-ready coupons A/B/C. R1–R4 + elastic R6 are measurement-only
and unretireable analytically. Scan/verify cost-down is closed
([SHA-10](sha10-scan-costdown-verdict.md), [SHA-12](sha12-t2-k2-verdict.md));
A7-V stays parked. This note does the cheapest remaining analytic
exploitation: tolerance stack, printability audit, BOM-margin reprice.

Gate script (new, 13/13):
`08-integrated-designs/a1-reliability-first/analysis/a1_hardening.py --gate`.
Provisional FDM rules: `tools/fdm-limits/fdm_process_limits.py`
(X1C + PLA + 0.4 mm nozzle: min feature 0.44, robust wall 0.88,
load-bearing 1.32, accuracy ±0.1/face assumption-class, pin floor 5.0 mm
sourced, bed 256 mm).

## 1. Tolerance analysis — per-fit margins

Worst-case = nominal minus per-face print growth (±0.1 mm, assumption [R4]);
MC = 200k draws at σ = 0.05 mm print scatter.

| Fit | Nominal margin | Worst-case | MC | Verdict |
|---|---|---:|---|---|
| F1 latch excursion in owned lane (0.65 vs 0.74) | +0.09 mm | **−0.11 mm** | ~90 % pass | **FAIL worst-case / PASS nominal+MC** |
| F2 spot half-width vs neighbour (0.7025 vs 1.055) | +0.353 mm | +0.253 mm (print-only; DND-119 MC +0.325) | >99.9 % | **PASS** |
| F3 gantry half-pitch (0.264 vs 2.54 kill) | +2.276 mm | +2.08 mm | ~100 % | **PASS (9.6×)** |
| F4a head standoff (0.81 aperture / 0.55 vane) | +0.81 / +0.55 | +0.61 / +0.35 | pass | **PASS** |
| F4b flap covers spot, per side (1.55 vs 1.405) | +0.073 mm | **−0.028 mm** | ~98 % | **MARGINAL** |

Two fits fail worst-case arithmetic. Both get a cheapest-geometry-delta
**proposal only** (no CAD edit, per the criterion):

- **D1 (for F1):** trim column BODY 3.60 → 3.50 mm (+0.05 mm lane/side;
  surface gap 1.48 → 1.58 mm, still tiles cleanly). Nominal F1 margin
  +0.09 → +0.14 mm. Honest caveat: worst-case ±0.1 stacking cannot clear
  any sub-mm lane analytically — coupon B places it; D1 buys MC headroom,
  not a worst-case proof.
- **D2 (for F4b):** widen flap SHUT_W 1.55 → 1.70 mm (sweep 3.00 →
  3.075 mm, still clears the neighbour body at 3.28 by +0.205 mm).
  Per-side coverage +0.073 → +0.148 mm. Contrast degrades gracefully
  (partial shadow), so F4b is marginal, not hard-failing.

## 2. Printability / manufacturability audit

**Min feature / wall (0.4 mm nozzle rules):** four features sit exactly at
the 0.44 mm floor (latch leaf 0.45, vane 0.44, shutter flap 0.44, aperture
0.44) — printable as one line, zero margin; strength/spread is
coupon-placed, not proven. Hard-stop land 0.88 meets the robust wall;
column body 3.6 is comfortable. **Sourced pin rule (Ø ≥ 5.0 mm) FAILS:**
the 1.0 mm hinge barrel prints weak by the book — carried as the R2/coupon-B
measurand, with a $6 steel-dowel fallback priced (not adopted) in §3.

**Supports / bed fit:** cell parts need no supports (vertical walls, no
>45° overhang, no bridge >5 mm). All 6 CAD parts watertight and bed-fit
(`render_record.json`); the 406.4 mm field is modular (≥2×2 frame tiles +
210 mm rail segments, coupon-C precedent) — **PASS**.

**Material / time / assembly class (analytic):** ~2.4 g printed/cell →
**~15 kg PLA** for the field (DND-70 excluded from the ceiling, but a
batch/queue plan is required); **~111 single-X1C days** time-class →
multi-machine tile batches, not a cost risk; **~25.6k simple placements**
(4 ops/cell) + 4 shared subassemblies, zero per-cell bought hardware.

**Top-3 simplification levers (elimination-first):**

1. **L1 — co-print the CH-A vane into the cradle tile:** eliminates 1 part
   type + 6,400 placements; read geometry unchanged. Assembly −25 %.
2. **L2 — co-print shutter crank + latch toe arm as one arm:** eliminates
   1 assembly interface/cell (−6,400 ops); shadow kinematics unchanged.
3. **L3 — interlocking printed dovetails for frame tiles:** eliminates the
   $10 splice line (+ part of the $8 fastener line), ~$10–14 purchased.

## 3. BOM-margin reprice (hostile + fallback-purchase)

| Convention | Purchased | Band | Delivered (×1.16) |
|---|---:|---|---:|
| Base (`bom_a1.csv`) | $181.00 | **IDEAL** | $209.96 |
| Hostile (+35 % soft lines, DND-46) | $189.40 | IDEAL | $219.70 |
| Hostile + fallback purchases (prong insert $8, pin contingency $6, frame fallback $15) | **$218.40** | **ACCEPTABLE** | $253.34 |

Fallbacks are assumption-class contingencies executed only if coupons kill
the printed variant — they are priced, not adopted. Even fully executed,
A1 sits **$281.60 under the $500 ceiling** and $181.60 under the
ACCEPTABLE ceiling. Band verdict: IDEAL base, ACCEPTABLE under every
hostile convention tried.

**Cheapest cost-down lever keeping zero-silent + 8-head rule intact:** L3
dovetails (−$10–14) + limit switches 5→3 via stall-detect homing (−$2;
re-home recovery kept): ~$12–16 down. The band does not move (already
IDEAL) — the lever buys headroom against fallback execution.

## Verdict

- **Tolerance: 3 PASS, 1 FAIL (F1 worst-case), 1 MARGINAL (F4b).** D1/D2
  proposed as annotations; no CAD touched. F1/F4b worst-cases are coupon-B/A
  measurands, not program killers (nominal + MC pass; graceful degradation).
- **Printability: PASS modular, with 4 features at the 0.44 mm floor and
  the hinge pin honestly failing the sourced pin rule** (carried as R2).
- **BOM margin: IDEAL base ($181), ACCEPTABLE under hostile+fallback
  ($218.40), $281.60 under the $500 ceiling.** No cost pressure on the
  architecture; cheapest lever (−$12–16) needs no band change.
- **Residual uncertainty (unchanged + two analytic):** R1–R4 + elastic R6
  stay measurement-only (DND-27); F1 worst-case and the pin rule join them
  as coupon-placed (B/A respectively). Nothing analytic remains that can
  retire them — the next step is physical coupons, a handoff, not analysis.

## Reproduce / verify

```bash
python 08-integrated-designs/a1-reliability-first/analysis/a1_hardening.py --gate  # 13/13 (new)
python 08-integrated-designs/a1-reliability-first/analysis/a1_promotion_cost.py --gate    # 7/7 (unchanged)
python 08-integrated-designs/a1-reliability-first/analysis/a1_regional_update.py --gate   # 13/13 (unchanged)
python 08-integrated-designs/a1-reliability-first/analysis/a1_coupon_readiness.py --gate  # 32/32 (unchanged)
git status --short  # S5-R (08-integrated-designs/s5r-*) and S6-LC untouched
```
