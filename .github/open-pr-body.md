# DND-35 / DND-39: adopt the Falsifier promotion review into the S5 winner definition

## What changed
The Falsifier's winner-specific review (`falsifier-s5-promotion-review-2026-09.md`, merged
PR #27) concluded: **"S5 promotion SURVIVES AS A DIRECTION but FAILS AS STATED."** This PR
adopts its arithmetic and its corrected killer list into the winner definition.

- **ADR-002** (`07-evidence-and-decisions/convergence-decision-2026-09-b.md`): new §1.1
  (two bets, not one) and §1.2 (adopting the promotion review); §2 cost-disposition
  correction; §3.1 K1 re-labelled `open/contestable`; §3.2 cost re-derived on the additive
  basis; §4 register extended to K1–K11 + R1–R4.
- **`08-current-design/README.md`**: status changed to **NOT print-ready as stated**;
  corrected cost table ($501.12 sourced / $491.03 reduced on the additive basis); risk register K1–K11; a
  print-readiness gate naming K1/K5/K7.
- **`06-experiments/test12_winner_convergence/`** (`model.py`, `checks.py`, `README.md`):
  - `DELIVERED_UPLIFT` corrected from the inconsistent `1.10 × 1.06 = 1.166` to the
    repository's additive `1 + 0.10 + 0.06 = 1.16`; register saving corrected from the
    double-counted −$14 register allowance to the true sourced line value −$3.70.
  - Killer list re-labelled (K1 `open/contestable`, K4 `partially-closed`, K5/K6
    `conditional`) and extended with **K7–K11** (motor-cost cliff, lateral holding,
    print-tolerance angular margin, regional-update time, detent cycle life).
  - `PRINT_READY_AS_STATED = False`.
  - New checks: `test_delivered_uplift_matches_repository_additive_model`,
    `test_two_bet_framing_and_no_fallback_cost_kill`,
    `test_killer_list_labels_are_honest`, `test_time_is_conditional_not_closed`; the
    K2/DND-38 detent check is preserved.

## Engineering question
Does the S5 winner definition survive the Falsifier's adversarial review, and if not, what
must be corrected before it is treated as print-ready?

## Evidence produced
- **Cost, corrected (calculation, project-consistent additive ×1.16):**
  sourced BOM expected scenario $592.06; sourced pair **$501.12 (at/over the $500 ceiling)**;
  reduced **$491.03** (additive basis; CostManufacturing [DND-37] reports $493.57 on the
  multiplicative factor). The previously published $503.71/$481.56 used a multiplicative
  uplift and a double-counted register saving.
- **K1 (calculation):** 4.96 N critical **< 5 N abuse screen (fails by 0.8 %)**; the 1 N
  service load is an unsourced assumption, so K1 is `open/contestable`, not closed.
- **K4 (sourced read):** the cited isolation rig returns `INCONCLUSIVE`; only the 0.017 mm
  structural sub-bound is analytic.
- **K6 (calculation):** 26.251 s is the best corner of the Test09 540-case sweep; at 400 pps
  only **17/108** cases pass, worst 45.07 s.
- **K7 (sourced):** the only traceable matched 8 mm PM stepper is $40/ea → $3,200 (8× ceiling).
- **K8–K11 (calculation/sourced):** lateral holding, angular margin, regional time, cycle life.

## Evidence class
Sourced / assumption / calculation / simulation / CAD only. **No print, no measurement**
([DND-27](/DND/issues/DND-27)). No board contact ([DND-32](/DND/issues/DND-32)).

## What passed / failed
- Passed: all Test08–Test12 checks incl. the new guard checks; the falsifier review checks
  (`falsifier_s5_review_checks.py`) reproduce $501.12 / 17-of-108 / `INCONCLUSIVE`.
- Corrected (was overstated): K1/K4/K5/K6 were presented as closed; the cost margin was
  overstated. All withdrawn and re-labelled.

## What remains uncertain
- K1 (tabletop load bound), K5/K7 (sourced motor price), K6 (measured ≥400 pps), K4 (stiction
  release + drift), K9 (print-tolerance angular error), K2/K11 (printed detent). All are
  attackable analytically or by sourcing; none requires a print.

## Most informative next test
Sourcing the maximum tabletop vertical + lateral load — a single sourced fact that closes or
confirms **K1 and K8**, the two most decisive residuals.

## Coordination
- [DND-36](/DND/issues/DND-36) Falsifier review (adopted here).
- [DND-37](/DND/issues/DND-37) BOM/printability ratification (should adopt the additive basis).
- [DND-38](/DND/issues/DND-38) detent sweep (K2, merged).
- [DND-39](/DND/issues/DND-39) CEO analytic-only convergence decision (this PR applies it).
