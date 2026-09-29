# DND-75 — Divergent ultra-low-cost shape-display architectures (<$250 purchased)

- **Issue:** [DND-75](/DND/issues/DND-75) (InventorAlpha), child of
  [DND-71](/DND/issues/DND-71); sibling of the CTO's [DND-72](/DND/issues/DND-72).
- **Status:** **THREE CANDIDATES CLEAR BOTH GATES.** All three divergent
  machines reach <$250 purchased **and** <30 s full-map, unlike every S6-LC trim.
- **Evidence class:** **CALCULATION** over the promoted S5-R model and
  sourced-class allowances + **CAD** (analytic printability, sourced FDM limits).
  **No print, no purchase, no measurement** ([DND-27](/DND/issues/DND-27)).
- **Artifacts:** `09-lowcost-alternative/divergent/analysis/divergent_lowcost.py`,
  `divergent_lowcost_checks.py` (18 checks), `scad/a1_cam_cell.scad`,
  `scad/a2a3_media_cell.scad`, `tools/run_divergent_checks.py`. CI job
  `dnd75-divergent-lowcost`.

## 1. The question

DND-72 falsified the <$250 target **for the S5-R/S6-LC architecture**: its fixed
no-channel purchased base is $218.70 parts → $253.69 delivered with zero
actuators, so no actuator count can win. The DND-72 falsifier named the only way
out: a **sourced base reduction below $215.52 parts without touching a mission
requirement**.

DND-75 asks a different question: *design a materially different machine whose
base does not contain those expensive lines at all.* Not a trim — a divergence.

## 2. The lever: attack the base, not the actuators

S6-LC trimmed bank motors and writers. That lever is dead. The expensive base
lines exist *only* because S5-R has a travelling head, a zoned multi-screw lift
and a separate scanner axis:

| Line | Parts |
|---|---:|
| Guide rods/rails and bearings | $25.00 |
| Four lift screws and nuts | $20.00 |
| Lift motor + coupling | $26.00 |
| Scanner motor | $12.00 |
| Belts pulleys idlers | $12.00 |
| Head shafts and friction-pad material | $12.00 |
| Axis drivers (3) | $9.00 |
| Axis reference sensors | $4.00 |
| Wire connectors flexible loom | $22.00 |
| Power supplies and protection | $35.00 |
| **Total** | **$177.00** |

Deleting this block leaves a **retained base of $41.70**. A machine that needs
none of it starts ~6× below the $253.69 floor.

**Hostile audit.** A deleted line with no substitute is an accounting trick. The
`ATTACK_AUDIT` table lists, for every attacked line, what removes it and what
replaces it, and every candidate **pays for its own power supply, cables and any
retained axis** (`SUBSTITUTE_LINES`). A1 = +$11, A2 = +$11, A3 = +$12. Even
after that, all three stay under $250.

## 3. The three machines

### A1 — single-shaft cam machine
One stepper → printed camshaft (4 phased lift cams + bank cam + Geneva writer
drum). No scanner motor, no lift motor/coupling, no lead screws, no belts, no
guide rods, no head actuator, no writer solenoids.
- **Cost:** $58.30 parts → **$67.63 delivered** ($80.39 with substitutes).
- **Time:** 17.76 s.
- **Honest failure:** the lift cam alone needs **0.3302 Nm** vs the 0.30 Nm
  class allowance — the single-motor gate **fails by 0.0302 Nm**; the summed
  bank+lift case is **0.6099 Nm** and stalls. A second $12 motor (→ **$80.39**)
  or a ~$16 stronger stepper (→ **$72.27**) clears it. The cost claim survives;
  the *single-motor* claim does not.
- **Killing test (no print):** `a1_force_gate` — already run; the negative
  result is the evidence.

### A2 — hand-crank energy-reservoir + punched-tape reader
Zero bought motion actuators. A torsion spring is charged by hand; an
80-channel mechanical tape reader selects; a printed escapement meters four
10 mm strokes.
- **Cost:** $42.90 parts → **$49.76 delivered** ($62.52 with substitutes).
- **Time:** 26.86 s (break-even: ≤3.09 s/bank at 8 banks).
- **Decisive failure:** the tape **writer** is the product. 25,600 holes at one
  needle ≈ 85 min off-line (≈11 min at 8 needles); works only for known-ahead
  maps.
- **Killing test (no print):** holes/channels × step vs the acceptable interval.

### A3 — S1-B banked broadcast ratchet + punched-film media
S1 revived per test11's own prescription (banked, shared sub-strokes) with the
mask-writing failure retired by an off-line punch carriage.
- **Cost:** $98.29 parts → **$114.02 delivered** ($127.94 with substitutes).
- **Time:** 22.06 s at **4 banks of 20 rows**.
- **Correction to test11:** its prescribed 8 banks is **38.9 s and FAILS 30 s**;
  the bank sweep shows 4 banks clears both gates (592 N release < 1500 N).
- **Decisive failure:** punched-film registration with no per-cell feedback.
- **Killing test:** 5×3 true-pitch single-film-plane coupon.

## 4. Requirement preservation

| Requirement | A1 | A2 | A3 | Class |
|---|---|---|---|---|
| 6,400 cells at 5.08 mm | unchanged register cell | unchanged column | unchanged column | CAD |
| ≥ 40 mm travel | 4 × 10 mm cam | 4 × 10 mm spring | 4 × 10 mm stroke | calc |
| full-map < 30 s | 17.76 s | 26.86 s | 22.06 s | calc |
| regional updates | index cam | pause tape | one bank | calc |
| X1C-buildable | printability PASS | printed PASS, media RISK | printed PASS, media RISK | CAD |
| **purchased < $250** | **$67.63** | **$49.76** | **$114.02** | calc |

## 5. What this changes

- S6-LC's negative result was **not** the end of the <$250 question; it was a
  proof about *that architecture's base*. A base-only attack (delete the head,
  the multi-screw lift and the scanner axis) reaches **$50–$128 delivered**.
- The cheapest credible machine is **A2** ($49.76); the most buildable today is
  **A1** ($67.63, one motor, printed cams); the most conservative (keeps the
  proven S5 register and adds only punched film) is **A3** ($114.02).

## 6. Residual uncertainty / next test

- **A1:** real cam torque at the actual profile (friction, not full-rise arm).
- **A2/A3:** the punched-media cell is the one coupon worth printing first — it
  retires the family's central unknown.
- No candidate has a full multi-row assembly interference check; only unit cells
  are modelled.
