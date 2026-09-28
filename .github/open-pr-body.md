# DND-30: reconcile ADR-001 with delegated merge authority + no-print directive

Resolves [DND-30](/DND/issues/DND-30). Makes the repository's decision record
self-consistent with board directives [DND-19](/DND/issues/DND-19) (agents merge
their own reviewed PRs) and [DND-27](/DND/issues/DND-27) (no physical print
tests).

## What changed

`07-evidence-and-decisions/convergence-decision-2026-09.md` (ADR-001):

- **§4 — merge authority.** Replaced "Merge remains board-authorized. Agents do
  not merge." with the DND-19 delegated-merge rule, and recorded the merge status
  of PRs #12–#17 against `origin/main` (`1a9926e`): all merged via the
  `integrate/test11-all` branch; no open PRs remain. Verification anchors:
  `8ea9c5f` and `452206f` are ancestors of `origin/main`.
- **§5 — binding tests re-ranked as analytic/simulation/CAD.** The three former
  physical steps (isolation rig, printed pitch coupon, printed one-bit memory
  cell) are replaced by executable non-physical gates, preserving the same
  elimination order and kill logic:
  1. beam/FEA coupling + stiction isolation bound (SIMULATION/CALCULATION);
  2. CAD/mesh vs *sourced* FDM process limits + worst-case/Monte-Carlo stack-up
     (CAD + CALCULATION);
  3. force/kinematics memory-cell model + tolerance stack-up
     (CALCULATION/SIMULATION);
  4–7. isolation 2×2 model, analytic selector fan-out, modelled writer path,
     analytic/FEA load & power.
- **§5.2 — permanently qualitative risks.** A new explicit table names what a
  printed/measured coupon would have retired and can no longer be closed
  (print realisation, release-force spread, detent hold/repeat, rig noise floor
  & creep, stiction release, miniature-height compliance). This is the
  "flagged assumptions" deliverable.
- **§1/§2/§3/§6/§7** updated so the critical path reads analytic/simulation/CAD
  plus accepted qualitative risk, not physical experimentation; the honesty
  statement now states no printed/measured evidence exists **and none will be
  produced**.

`07-evidence-and-decisions/convergence-plan.md`:

- **§3** elimination table re-expressed with an explicit **Evidence level**
  column (CALCULATION / SIMULATION / CAD); physical-test cost/where columns
  removed; added **§3.1** (what DND-28 already closed analytically: J2
  neighbour bound 0.017 mm vs 0.10 mm gate; S3 min-web +0.11 mm; unresolved M3
  pivot) and **§3.2** (permanently qualitative risks).
- **§4** promotion rule no longer requires a "physical pass at final pitch";
  requires the analytic/CAD gate **and** explicit board acceptance of §3.2.
  "Measured value" language in reject/park rules replaced with analytic bounds.
- **§6** evidence snapshot annotated: Printed/Measured columns are permanently
  empty by policy.
- **§7** governance corrected: merges are delegated (DND-19); no physical gate
  may be introduced (DND-27).

`07-evidence-and-decisions/README.md` (consistency fix in the canonical evidence
matrix the ADR points at):

- Removed the stale "physical J2-0…J2-4 run … owned by the CTO (DND-14)" status
  and the orphaned coupon-measurement fragment; the adversarial table now shows
  gate evidence levels and explicitly says no physical run remains to schedule.

## Engineering question addressed

Can ADR-001 and the convergence plan carry the programme's elimination logic
without any gate that requires printing or measurement — and if not, exactly
which assumptions become permanently qualitative?

## Evidence produced

- Documentation revision only; no new analytical run.
- Reused existing DND-28 analytic results (J2 0.017 mm neighbour bound vs
  0.10 mm gate; S3 min-web +0.11 mm; M3 pivot `INCONCLUSIVE`) as the concrete
  examples of a closed analytic gate and an unresolved one.
- Local CI parity: `test11_cost_printability_reliability/checks.py`,
  `test11_falsification_library/checks.py`, and `check_fixture.py` all exit 0
  on this branch. The edits touch only `07-evidence-and-decisions/` and
  `.github/open-pr-body.md`, which CI does not execute.

## Assumptions made explicit

- The §5.2 list is the complete set of previously-physical binding assumptions;
  any future gate that cannot be expressed analytically is parked there by the
  §6 rule.
- "Sourced FDM process limits" are cited as rules/values, not measured on this
  machine, per DND-27.

## What passed / failed

- All edited documents are internally consistent with DND-19 and DND-27: PASS.
- No new physical-test requirement introduced anywhere: PASS.
- No claim of printed/measured validation is made anywhere: PASS.

## What remains uncertain

The §5.2 risks remain genuinely unretired — that is the honest state, not a
papering-over. A survivor can now only be **promoted** if the board explicitly
accepts them alongside the analytic gate.

## Most informative next test

Close the one analytically-decidable loose end from DND-28: add an explicit
**designed radial clearance** to the S3 pivot in `selector_fanout_coupon.scad`
and re-run the T11-A stack-up, converting M3 from `INCONCLUSIVE` to a real
analytic disposition — all without printing.
