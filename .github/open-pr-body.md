# DND-74 — Falsifier adversarial audit of the S6-LC ultra-low-cost machine

## What changed

- **New report:** `07-evidence-and-decisions/dnd74-s6lc-falsification.md` — seven
  adversarial attacks on the CTO-selected machine S6-LC (`09-low-cost-variant/s6lc/`,
  [DND-72]/[DND-83]) with a per-attack **survived / broken / bounded** verdict and the
  deciding number.
- **New CI gate:** `07-evidence-and-decisions/falsifier_dnd74_checks.py` — 24 checks that
  assert every finding, so a silent re-quote cannot return. Wired into `.github/workflows/ci.yml`.
- **07 README:** new audit section + evidence-matrix row.

## Engineering question

Can the S6-LC ultra-low-cost machine (<$250, 6,400 cells, ≤40 mm travel, <30 s full map,
regional updates) be falsified on its **cost ladder, requirement preservation, or mechanism
feasibility**, on repository inputs alone (calculation/CAD; no print, no measurement — [DND-27])?

## Evidence produced (calculation only)

| # | Attack | Verdict | Deciding number |
|---|---|---|---|
| 1 | Cost ladder honesty | survived (bounded) | +$69 honest allowances → $242.17 delivered, $7.83 headroom |
| 2 | **Lift-axis sizing (G3)** | **BROKEN** | 6,400 cells × 0.4 N = 2,560 N → ≥1.63 N·m vs 0.30 N·m NEMA17 |
| 3 | Mask-write product statement | bounded-needs-measurement | 2,560 s serial punch; 30 s needs 427 ops/s |
| 3b | Regional updates | BROKEN (claim) | one global platen ⇒ 7 banks masked "no-change" |
| 4 | No per-cell feedback | bounded-needs-measurement | p=1e-4 → P(all 6,400 correct)=52.7 % |
| 5 | Release-force ceiling | BROKEN (provenance) | "296 N ceiling" is S1's own banked output |
| 6 | Timing completeness | survived (bounded) | +4 mask-index moves → 8.4–11.4 s, still <30 s |
| 7 | Pawl load holding | bounded-needs-measurement | 0.5 N lateral cams toe out of a 0.8 mm pocket |

## The decisive break (Attack 2)

`lift_axis()` computes the platen load on `CELLS_PER_BANK` (800) while the mechanism writes
the **whole 6,400-cell board** in one global platen stroke (`timing()` banks only the reset).
Corrected to 6,400 cells at the model's own 0.4 N/cell, the required torque is **≥1.63 N·m**
(0.65 N·m even gravity+pawl only; 0.41 N·m per screw on four screws) against a 0.30 N·m
NEMA17 — **G3 fails ~5.4×**. The S6-LC analogue of S5's K7 motor cliff ([DND-49]).

## Assumptions

- Load/cam/spread figures use the model's own constants (`s6lc.py`).
- S1 comparison numbers read from `06-experiments/test11_threshold_ratchet_s1/`.
- No physical evidence exists for this programme ([DND-27]); nothing here is measured.

## What passed / failed

- **Passed:** geometry (G1), timing (G4, with margin), the raw delivered cost ceiling (G5/G6).
- **Failed:** lift-axis gate G3 (wrong input); release-force ceiling provenance; the
  "bank-local" regional claim.
- **Bounded:** cost headroom ($7.83), mask-write product constraint, per-cell reliability.

## What remains uncertain

Pawl release-force spread, as-printed friction µ, pocket-roof holding and creep are
measurement-only and cannot be retired under [DND-27]. The mask puncher throughput
(~427 ops/s) is unverified.

## Next test / action

- **CTO (actionable now):** fix `lift_axis()` (size for 6,400 cells, or genuinely bank the
  write), re-run `s6lc_checks.py`, and update the BOM, README gate table and DND-72/83 record.
- Add the +$69 allowance lines and either relax the ≥$50 margin check or shed cost.
- Add a reset-carriage torque gate and an independent release-force limit.

Refutation is a success: this report records S6-LC's failed/soft claims as evidence.
