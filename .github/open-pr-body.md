# DND-35: Falsifier adversarial audit of convergence logic + reliability-helper fix

Adversarial review requested by [DND-35](/DND/issues/DND-35) ("ask Falsifier to
adversarially review the winner's killer list"). No winner exists yet, so this
audits the **selection logic and the survivors' kill list** instead — the layer
that must be sound before a winner can be named. Independent reviewer: Falsifier.

## What changed

New artifact `07-evidence-and-decisions/falsifier-adversarial-audit-2026-09.md`
with three findings (all **calculation/sourced**, no physical evidence, per
[DND-27](/DND/issues/DND-27)):

1. **"One bet in five shapes" is false for S5.** S1–S4 are *written passive
   memory* (Bet A: gate/pawl, planar shutter, printed register, tile clutch).
   S5 is *absolute geometric stops* (Bet B: gravity follower on a home-homed cam
   sector — no threshold, no set/clear state, no hold force). Their killers do
   not overlap, so a Bet-A failure (≈9 % release-force spread, gate hold) does
   **not** imply a Bet-B failure (cam buckling ~4.96 N vs 5 N, detent capture,
   motor sourcing). The plan's single-fate rule should become two bets, and S5's
   gates should run in parallel with the Bet-A gates.
2. **The "$500 rejects every survivor" verdict is an artifact for S1/S2/S4.**
   Their working BOMs charge $192–$224 for *fallback* parts the designs
   explicitly intend to print (e.g. `bom_S1.csv`: "No bought part intended in S1
   baseline; allowance only if tile isolation needs a coupler"). Cost for
   S1/S2/S4 is therefore **undetermined pending the print gate**, not failed.
   The two robust cost results stand: any bought part per cell ($0.10 → $640),
   and the sourced $40 8 mm stepper that threatens S5's 80-motor head.
3. **`reliability.zero_failure_trials()` was inverted.** It documented a
   one-sided 95 % upper bound but computed `ln(conf)/ln(1−q)` (the probability of
   *seeing zero failures*), returning **32,664** at q = 1.57×10⁻⁶ where the
   project's own headline and `test11_cost_printability_reliability/checks.py`
   say **1,907,667** — a **~58× overstatement of demonstrated reliability**. Made
   convention-explicit, defaulted to the upper bound, and pinned the agreement
   in `checks.py` so it cannot regress.

Also corrected `06-experiments/test11_falsification_library/measurement_plan.md`,
which had rationalised the 3.27×10⁴ figure instead of flagging the inversion.

## Engineering question addressed

Does ADR-001's convergence logic correctly identify what can kill each survivor,
and is the reliability arithmetic it rests on self-consistent?

**Answer: not yet.** The Bet-A/Bet-B conflation can trigger an unnecessary
product re-scope, the S1/S2/S4 cost verdict is conditional not final, and the
reusable reliability helper disagreed with the project's own headline by 58×.

## Evidence produced

- New adversarial review (calculation + sourced-fact document review).
- `reliability.py`: convention-explicit `zero_failure_trials(..., convention=)`;
  default `upper_bound` reproduces 1,907,667 at q = 1.57×10⁻⁶.
- `checks.py`: replaced the legacy-pinned `n == 513` test with
  `test_headline_1p91M_trials_are_the_upper_bound`, asserting the upper-bound
  value equals the headline and the legacy formula is >50× smaller.
- `07-evidence-and-decisions/README.md`: audit pointer added to the evidence
  matrix section.

## Assumptions made explicit

- The two-bet framing is a documented reading of the repository's own S5
  mechanism description; rejecting it requires showing S5's write is
  threshold-dependent (Finding 1's stated falsification test).
- Cost for S1/S2/S4 is treated as conditional on the printed selector/media
  layer, consistent with Test11's own print-intent floors.

## What passed / failed

- `test11_falsification_library/checks.py`: **20 tests PASS**.
- `test11_cost_printability_reliability/checks.py`: **PASS**.
- `test09_test08_validation/checks.py`: **PASS**.
- `isolation_rig_runner.py --selftest`: **PASS** (now reports the correct
  upper-bound trial count).
- `check_fixture.py`: **PASS** (OpenSCAD render SKIPPED in this environment,
  correctly, not passed).

## What remains uncertain

- Whether S5's home-stop/detent write is deterministic — only a coupon could
  prove it; qualitative under DND-27.
- Whether the printed selector/media layer works at all — the pivot of
  Finding 2; qualitative under DND-27.
- Release-force spread, print realisation and creep — unchanged from ADR-001 §5.2.

## Most informative next test

Adopt the two-bet framing on [DND-35](/DND/issues/DND-35) and re-rank the gate
list so S5's Step 2/Step 6 killers (cam strength, loaded motor torque-speed,
detent capture) run in parallel with the Bet-A killers — because a Bet-A failure
currently, and wrongly, ends the whole convergence search.

---
Opened by the reusable credential-free `open-pr` workflow on the Falsifier branch.
