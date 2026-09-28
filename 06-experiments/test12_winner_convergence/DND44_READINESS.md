# DND-44 — S5 readiness closure (K1 / K5 / K6 / K8 / K10 / K11)

> **⚠ Superseded in part by [DND-46](/DND/issues/DND-46) / [DND-48](/DND/issues/DND-48).**
> The adversarial audit (`FALSIFIER_AUDIT.md`, `falsifier_checks.py`) broke three of the six
> headlines below. **Use the robust register in
> [`08-current-design/README.md` §7/§9](../../08-current-design/README.md), not the "After" column
> here.** Summary of the corrections: **K1-service is 0.39–3.27 N/column** (not ≤0.39);
> **K5 planning basis is $482.95** (not $424.95); **K8 is open** (at the repo's 40 mm free
> length, 1 N → 0.356 mm, gate load 0.28 N — not 0.01 mm / ~9.4 N); **K6 is conditional on a
> loaded dwell AND a ≥268 pps loaded rate with `inspection_s = 0`**; **K11 is ">=1e6, order
> unknown"** (not ~10⁸). The §"Residuals that survive" table below is superseded by
> `FALSIFIER_AUDIT.md` §8 and the §9 register.

**Question.** [DND-41](/DND/issues/DND-41) left the promoted S5 winner as an honest
*analytic definition*, not a print-ready claim: cost at/over $500, time only in the
best sweep corner, K1 open, and K7–K12/R1–R4 open. [DND-44](/DND/issues/DND-44) asks
which of those can be closed or bounded analytically, and which single physical
quantity (unavailable under [DND-27](/DND/issues/DND-27)) each residual needs.

**Answer (CALCULATION only; no print, no measurement).**

| Killer | Before (DND-41) | After (DND-44) |
|---|---|---|
| K1 cam buckling | open; 4.96 N < 5 N screen; 1 N service load unsourced | **service load closed** (≤0.39 N/column via base distribution, 12.7× margin); localized 5 N abuse screen **bounded** — needs a 1.10 mm core (5.60 N) |
| K5 cost | $501.12 sourced / $483.37 reduced (used a $0.80 driver + best-case motor) | **honest expected baseline $592.06** (over); **machine-preserving source path $424.95** ($75 margin) |
| K6 time | 26.251 s best corner; 17/108 sweep pass; needs "measured ≥400 pps" | **not a rate problem**: rate-independent floor 18.65 s; ~268 pps meets 30 s; the 45.07 s corner is not rate-recoverable |
| K8 lateral | open, no analytic pass | **guide carries lateral**, not the detent; 1 N → 0.01 mm (<0.10 mm gate); limit ~9.4 N |
| K10 regional time | open, "perfect-scaling" | **bounded**: 1 row ~3.9 s, 10 rows ~6.3 s, 80 rows ~24.7 s |
| K11 cycle life | open, single-cycle static | **bounded ~10⁸ cycles** (order-of-magnitude, stated as such) |
| K7 motor supply | open | **refuted at ≤$1.86 on sourced evidence ([DND-49](/DND/issues/DND-49))** — cheapest matched part $8.20–$11.20 → $1,088–$1,367 delivered; reduced-head lever fails the 30 s budget. `k7_motor_trace.py` |
| K9 angular margin | open | open, **delegated** ([DND-45](/DND/issues/DND-45)) |
| K12 usability | open (product) | open (product decision) |

## Modules

| File | Killer | What it does |
|---|---|---|
| `timing_closure.py` | K6 | Closed-form per-row budget; splits rate-independent floor from rate terms; cross-checks `test09/analyze.schedule()` to 3.6e-15 s. |
| `buckling_closure.py` | K1 | Bounds the distributed tabletop load over a miniature's base; reproduces the repo's variable-section buckling model across core radii. |
| `cost_closure.py` | K5/K7 | Rebuilds the sourced BOM with machine-preserving changes E1–E6; audits every delta; finds the motor break-even price. |
| `cross_cutting_closure.py` | K8/K10/K11 | Lateral load path, regional-update bound, detent cycle-life bound. |
| `*_checks.py` | all | Regression + honesty gates (46 tests total across six modules). |

Run: `python <module>.py` and `python <module>_checks.py` (also in CI).

## The three headline numbers

1. **K6 is mischaracterised as a "step-rate" problem.** The per-row cycle is
   dominated by *assumed dwell times* (engage 25 ms, disengage 25 ms, three 15 ms
   settles, 2 ms command = 97 ms of a 262 ms row) plus scan acceleration, not by
   motor speed. At the design point the **rate-independent floor is 18.65 s** and
   only **~268 pps** is needed to meet 30 s (400 pps is used). The 45.07 s sweep
   worst corner has a floor of **34.47 s** — no step rate fixes it because it is
   built from slow engagement (50 ms) and slow scan (1000 mm/s²) assumptions.
   **The single quantity to verify is the loaded engagement/settle dwell and the
   scanner's 4000 mm/s², not a "measured ≥400 pps rate".**

2. **K5 is worse than documented, and the fix is the driver, not the motor.**
   Re-derived from the BOM's own `unit_expected` column, the honest baseline is
   **$592.06** (not $501.12 — the old figure used a $0.80 TB6612 and a $1.05
   best-case motor). A machine-preserving source path (sourced TB6612FNG
   $0.7955 @100 as the dual-H-bridge, sourced multipack motor $1.05, register
   and controller consolidation, spares allowance removal, sourced fixed-line
   repricing) lands at **$424.95 delivered, $75.05 under the ceiling**. The path
   clears only for a motor ≤ **$1.86**; at the sourced $2.66 AliExpress part it
   is **$574.36**. **K7 is the single binding residual.**

3. **K1's 1 N service load was conservative by ~10×.** A miniature stands on its
   base, not one 5.08 mm column. A 1 kg miniature on the smallest (25.4 mm) base
   spreads over 25 columns → **0.39 N/column** (7.9 % of the 4.96 N core, 12.7×
   margin). The 4.96 N core still does not meet the *localized* 5 N abuse screen;
   a core re-size to 1.10 mm gives 5.60 N and clears it, at the cost of step
   height 0.5 → 0.4 mm (a real geometry trade, stated, not hidden).

## Residuals that survive (each needs the named physical measurement)

| id | Residual | Exact quantity the residual needs |
|---|---|---|
| K7 | matched 8 mm 18° bipolar PM stepper at ≤$1.86 delivered | **refuted on sourced evidence ([DND-49](/DND/issues/DND-49))**: no matched orderable part ≤$1.86; cheapest matched $8.20–$11.20 → $1,088–$1,367 delivered; reduced head fails 30 s. Unretired only by purchase+sample of the untraced multipack (forbidden under DND-27) or an actuator-class change |
| K2 | detent corrects a slipped step at the sourced μ midpoint | printed PLA–PLA μ and as-printed scallop depth |
| K9 | angular margin under ±0.05 mm print tolerance | as-printed rotor radius/core offset |
| K1-abuse | localized 5 N point load on a 1.0 mm core | printed core crush/shear at the toe |
| K4 | regional stiction release / wear drift | release force + drift on a loaded neighbour |
| K8-residual | printed guide-wall shear strength | printed guide shear at the 0.10 mm gate |
| K10 | realised dwell times at load | loaded engage/settle dwell (same as K6) |
| K11 | printed-leaf creep/fatigue | cyclic creep of the 0.45 mm leaf |
| R1 | per-cell error rate q | counted coupon failures (Q ≤ 1.57e-6 for 99 %) |
| R2 | 40 mm travel vs a real miniature | one measured representative miniature height |

## Integrity notes

- Nothing here is a print or a measurement. Every number is CALCULATION over the
  repo's own sourced listings, geometry and stated assumptions.
- The `cost_closure.py` spine uses the BOM's own `unit_best_usd` for the E6
  repricings; a reviewer can re-derive each from `bom_S5_delivered.csv`.
- `timing_closure.py` and `buckling_closure.py` call the repo's own
  `test09/analyze.py` and `test08/cam_strength.py` rather than re-implementing
  them, so the closures cannot silently drift from the source models.
- Falsifier adversarial audit: [DND-46](/DND/issues/DND-46). CostManufacturing
  BOM ratification: [DND-47](/DND/issues/DND-47). K2/K9 geometry:
  [DND-45](/DND/issues/DND-45).
