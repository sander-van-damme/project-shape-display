# SHA-23 — Comparative cost/BOM audit: A1 vs A7-V vs S6-LC

- **Issue:** SHA-23 (Cost Analyst). Portfolio lane, first side-by-side comparison.
- **Evidence class:** CALCULATION over committed repo BOMs + CAD records. **No print,
  no purchase, no measurement** (DND-27). Figures marked **[S]** are sourced from a
  committed repo artifact; **[E]** are estimates with stated method and uncertainty.
- **Cost convention:** purchased-parts gate per DND-70 (printed parts excluded);
  delivered = purchased × 1.16 additive uplift (DND-41). Bands of record (purchased):
  <$200 ideal / $200–400 acceptable / $400–500 last resort / >$500 unacceptable.
  S6-LC's mission gate is <$250 purchased (DND-70/DND-72 track), distinct from the
  repo's internal delivered convention — see §4.
- **Joint mandate:** per the Board mandate (SHA-11), cost is not optimised in
  isolation. The verdict row (§5) weighs performance, reliability, durability,
  manufacturability and feature coverage against total cost.

## 1. Comparable table (same columns, all three directions)

| # | Column | A1 (reliability-first, SHA-7 GATE) | A7-V (verified camshaft, SHA-8 REJECT) | S6-LC (low-cost, corrected per DND-93/DND-97) |
|---|---|---|---|---|
| 1 | Purchased parts **[S]** | **$181.00** → IDEAL (<$200). `bom_a1.csv` = model ($181.00 exactly, gate 7/7) | **$208–219** (reuse-credit floor ~$190) → ACCEPTABLE but **+$27–38 over A1**. Sketch-level, not a line BOM | **$226.77** → ACCEPTABLE (mission gate <$250 purchased: PASS, +$23.23). `bom_s6lc.csv` |
| 2 | Delivered ×1.16 **[S]** | **$209.96** → ACCEPTABLE | ~$241–254 (×1.16 on the sketch range) | **$263.05** → fails the internal $250 *delivered* convention (−$13.05); mission (purchased) gate unaffected |
| 3 | Hostile reprice **[S]** | **$189.40** (+35 % soft lines) → still IDEAL | Gap **+$19** wider under +35 % soft lines (DND-104 convention) → kills robustly | **$300.58** under premium-traces/allowance×2 → breaches $250 purchased (−$50.58). Working margin is thin |
| 4 | Printed material **[E]** | ~**6 kg PLA / board** (method §2, ±50 %) | ~**6–7 kg PLA / board** (adds 8 camshafts ≥406 mm; method §2, ±60 %) | ~**5–6 kg PLA / board** (method §2, ±50 %) |
| 5 | Print time **[E]** | ~**100 h @12 mm³/s** single-printer equiv. (method §2, ±50 %); parallelises over tiles/modules | ~**110 h** (+ camshaft segments, joint rework excluded; ±60 %) | ~**90 h** (+ mask cards as consumables; ±50 %) |
| 6 | Bought part count **[S]** | **17 BOM lines, ~30 units**, 4 shared actuators, **0 per-cell bought hardware** (2.8 ¢/cell amortised) | A7 base 1 actuator + reader head + scan motion ≈ **+2 sub-assemblies vs A1**; no line BOM exists — count unclosable | **20 BOM lines, 3 bought actuators** (lift/mask/reset), **0 per-cell bought hardware** (3.5 ¢/cell amortised) |
| 7 | Printed part count **[S/E]** | 6,400 columns + 6,400 latch arms + cradles + frame sub-tiles ≈ **13k+ printed parts** [S-count from CAD record; E on tiles] | 6,400 latches + columns + **8 camshafts (≥2 segments each = 16+ segments)** + reader bar ≈ **13k+ printed parts, most complex** | 6,400 columns + 6,400 pawls + 8 combs + mask cards ≈ **13k+ printed parts** [S-count basis: CAD + BOM] |
| 8 | Assembly effort **[E]** | **Medium.** Gantry² + writer + reader alignment, 8-head datum; then tile-local repair (cell-granular re-drive, no reset) | **Highest.** All of A1's reader/gantry work **plus** 8 shaft-segment joints, lobe timing, bank-global retry rigging | **Medium-low.** 3 fixed actuators, belt-synced screws; but full-board mask handling per update + bank sub-tile swap procedure |
| 9 | Fabrication burden **[S/E]** | X1C/PLA/0.4 mm route; latch 0.65 mm vs 0.74 mm owned lane → PASS [S, CAD record]; min-feature + stop-land gates pass [S] | **Unproven.** 80 lobes/shaft over ≥406 mm, ≤0.1 mm repeatability vs joint backlash + PLA torsion — second kill risk [S, SHA-8] | Pawl leaf 0.45 mm vs 0.44 mm floor → **RISK** (at process floor) [S, printability record]; bank 406.4 mm > 256 mm bed → sub-tiles [S] |
| 10 | Verification / silent errors **[S]** | **0 silent**; cell-resolving readback + bounded retry (22/22 audit CLEAN) | 0 silent **only** with full scan (= the cost that kills K1); bank-coarse → 6,392 silent (A5 pattern) | **No per-cell feedback**; at q=1e-4, P(all 6,400 correct)=52.7 %; G8 reliability **UNRESOLVED, measurement-only** (coupon C1) |
| 11 | Full-map time **[S]** | **19.63 s** sustained incl. verify + retry (< 30 s, margin 10.4 s); regional single-cell **0.31 s** | ~**18.9 s** (8-head verify) — EQUAL; 52 s single-row — FAIL. Timing passes only in the costly config | **11.96 s** (< 30 s) + off-line mask prep (serial punch 2,560 s worst case → double-buffer product constraint) |
| 12 | Evidence grade | **Line BOM + CAD + 3 gates (7/7, 22/22, 13/13)** — highest | **Sketch + screen script** — lowest (no line BOM, no CAD gate) | **Line BOM + CAD + 48/48 checks**, mechanism defects repaired (DND-97); reliability measurement-gated |

## 2. Estimate method (§1 rows 4–5) and uncertainty

Printed mass/time are **excluded from every cost gate by project rule (DND-70)**,
so no direction carries a repo-tracked print-time figure —rows 4–5 are the first
numbers of their kind and are **explicitly estimates**:

- **Method:** per-cell solid volume = hollow-square-tube column (≈10.4 mm² wall
  section × 46 mm ≈ 480 mm³) + latch/pawl + cradle/comb share ≈ 640–750 mm³ solid
  PLA per cell; × 6,400 cells; PLA 1.24 g/cm³; print rate 12 mm³/s volumetric
  (conservative X1C/0.4 mm PLA rate). Frame/gantry/camshaft extras folded as
  +10 % (A1/S6-LC) / +20 % (A7-V shafts).
- **Result:** A1 ≈ 5.7 kg / ≈95 h; S6-LC ≈ 5.2 kg / ≈90 h; A7-V ≈ 6.3 kg / ≈110 h
  (single-printer equivalent; tile/module parallelism divides wall-clock by printer count).
- **Uncertainty: ±50 % (A1/S6-LC), ±60 % (A7-V)** — wall thickness, infill, support,
  failed-print scrap and travel moves are unmodelled; A7-V additionally unmodelled
  (no CAD). Rounded to one significant figure in the table for that reason.
- **Falsification-first note:** the cheapest useful check is not a finer estimate —
  it is weighing one printed tile/module on the winner's first print and rescaling.
  Recorded as next action (§6).

## 3. Printability and part-count-reduction notes per direction

- **A1.** Printability: latch + clearance 0.65 ≤ 0.74 owned lane PASS; min-feature
  and stop-land gates pass; flag/read-spot geometry gated in CAD record [S].
  Reduction: reader-head ceiling is enforceable (`≤ $30.99` keeps IDEAL) [S];
  gantry-motion sub-assembly ($68→$91 motion lines incl. writer-adjacent steppers —
  see `bom_a1.csv`) is the single largest block and the only credible reduction
  target; **no per-cell bought part exists to eliminate** (already zero) — the
  S5 portable finding (dnd37 §7: $0.10/cell = $640) is satisfied structurally.
- **A7-V.** Printability: no CAD, no printability gate — 80-lobe ≥406 mm PLA shaft
  in ≥2 segments against a ≤0.1 mm repeatability budget is analytically hostile
  (joint backlash + torsion) [S, SHA-8 K4]. Reduction: the SHA-8 lesson is
  structural — broadcast-write families **cannot buy cell-resolving verification
  for less than the gantry they delete**; no component-level reduction re-opens K1
  (even the $20 reuse floor totals ~$190 > $181). Revisit only on a drawn <$10
  scan-motion design, then K1 → K4 coupon (1×5 lobes at true pitch).
- **S6-LC.** Printability: pawl leaf 0.45 mm vs 0.44 mm floor = RISK at the process
  floor [S]; 406.4 mm bank → sub-tiles with seam hardware ($8 M3 line) [S]; comb
  tooth 0.88 mm (2 lines) and mask boss 0.88 mm comfortable [S]. Reduction: BOM is
  already 65 % allowance ($147 of $226.77 [S, dnd98 §4]) — eliminating components
  beats cheapening: the six A5 allowances ($69) and lead-screw/guide lines are the
  named ~$11.25 purchased-reduction targets for the delivered convention; the
  NEMA23 lift ($30, 1.77× break-even) is the tightest line. Per-cell bought
  hardware is already zero — headroom buys at most a **$0.0036/cell** part [S, dnd98 §7].

## 4. Gate reconciliation (why S6-LC "REJECT" and "PASS" coexist)

- DND-93 verdict **REJECT** is keyed to **G6 (delivered <$250)**: $263.05 fails by
  $13.05 [S]. DND-97 clarifies the mission gate (DND-70: *"under $250 excluding 3D
  printed parts"*) is **G5 (purchased)**: $226.77 **PASSES** (+$23.23) [S].
- Verdict keyed on mission gate: `PROMOTE_TO_09_WITH_MEASUREMENT_GATE` — all
  mission gates pass; G8 reliability is the single measurement-gated item (coupon
  C1) [S, dnd97 §5]. The delivered figure rides alongside, nothing hidden.
- S5 lineage for convention only: DND-37/DND-41 (×1.16 additive uplift, register
  net-saving method), DND-47 (E1–E6 best-case-pricing qualification, K7 motor
  cliff), DND-54 (S5-R $401.12 working total). None of the three directions here
  re-uses S5 hardware; the conventions transfer, the numbers do not.

## 5. Cost/quality verdict (SHA-11 joint mandate — not cost in isolation)

| Direction | Cost rank | Quality rank | Joint verdict |
|---|---|---|---|
| **A1** | 1st ($181, hostile-proof IDEAL) | 1st (0 silent, verify+retry, cell-regional, coupon-gated residuals stated) | **Preferred.** Greatest useful performance × reliability per dollar; measurement-gated, not analysis-complete |
| **S6-LC** | 2nd ($226.77, thin margin, hostile-breachable) | 3rd (no feedback, G8 unresolved, mask double-buffer constraint, minis-off-region limitation) | **Viable low-cost lane.** Keep as the cost-floor definition; next spend is coupon C1, not full-machine print |
| **A7-V** | 3rd ($208–219, loses to A1 it must beat) | 2nd-equal on silent count only in the costly config, worse blast radius (bank-global retry) + shaft risks | **Parked.** REJECT on K1 stands; no CAD/BOM spend until a <$10 scan design exists |

Eliminate-over-cheapen check: all three already eliminate per-cell bought
hardware (the only move that matters at 6,400×). Remaining cost work is
sub-assembly-level (A1 gantry, S6-LC allowances) — no direction has a
component-cheapening path that changes rank.

## 6. Next action

1. **Whoever runs the winner's first print:** weigh one printed tile/module,
   rescale §1 rows 4–5 from estimate to measured, and record here (closes the
   ±50 % band for ~$0 marginal cost).
2. **S6-LC owner:** coupon C1 (DND-91 §6: 4×4 pitch/spring/engage coupon) before
   any full-machine print — cost is not the gate, G8 reliability is.
3. **A7-V:** no action (parked, no follow-up issue — per SHA-8, the family is
   parked, not queued).

## Sources (every number traced)

- A1 BOM/timing/audit: `08-integrated-designs/a1-reliability-first/bom_a1.csv`,
  `analysis/a1_promotion_cost.py` ($181.00 / $209.96 / $189.40 hostile / ceilings),
  `cad/render_record.json` (lane 0.65≤0.74, min-feature, stop-land),
  `07-evidence-and-decisions/sha7-a1-promotion-timing-cost.md` (19.63 s, 22/22 CLEAN),
  `sha7-a1-promotion-decision.md` (GATE + R1–R6), `sha9-a1-gate-residuals-regional.md`
  (8-head rule, 0.31 s single-cell).
- A7-V: `04-architecture-candidates/a7v-verified-camshaft/README.md`,
  `06-experiments/test15_a7v_challenger_screen/screen_a7v.py`,
  `07-evidence-and-decisions/sha8-a7v-challenger-verdict.md` (K1 $208–219, K4 risk).
- S6-LC: `08-integrated-designs/s6lc-low-cost/bom_s6lc.csv` ($226.77/$263.05),
  `cad/s6lc_printability_record.json` (leaf 0.45 RISK, sub-tiles),
  `07-evidence-and-decisions/dnd98-s6lc-bom-reratification.md` (allowances 65 %,
  hostile $300.58, $0.0036/cell), `dnd74/dnd91` (falsification record),
  `dnd93-s6lc-g3-fix.md` (NEMA23 branch, G6 REJECT), `dnd97-s6lc-mechanism-repair.md`
  (mission-gate clarification, G8).
- Conventions: `dnd37-bom-ratification.md` + DND-41 correction (×1.16, per-cell rule),
  `dnd47-cost-closure-ratification.md` (E1–E6 qualification, hostile convention),
  `dnd54-s5r-bom-ratification.md` (channel-pricing honesty precedent).
