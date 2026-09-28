# DND-2 — Converge the survivor field: explicit CTO decision + updated evidence matrix + ranked elimination order

Synthesizes the first invention + falsification generation into a single, evidence-backed
convergence decision for [DND-2](/DND/issues/DND-2).

**Evidence level: sourced fact + stated assumption + calculation only. No printed or measured
shape-display evidence exists.** This PR records a decision made on analytical evidence and names
the cheap physical tests that can overturn it.

## What changed

- **`07-evidence-and-decisions/convergence-decision-2026-09.md`** (new, ADR-001): the explicit
  decision — **no architecture is promoted to `08-current-design/`** — with factors, consequences,
  integration status, and the conditions that would change the decision.
- **`07-evidence-and-decisions/convergence-plan.md`** (brought onto `main` from the stale local
  `docs/cto-convergence-plan` branch): the ranked elimination order (steps 0–6), candidate
  resolution rules, and evidence-status snapshot.
- **`07-evidence-and-decisions/README.md`**: evidence matrix gains the convergence decision, the
  Falsifier's adversarial survivor-status table, the Test11 survivor-specific calculated results,
  and an explicit physical-evidence-status row (printed: none, measured: none).

## Engineering question answered

Do the surviving architectures (S1–S5) justify promotion on present evidence, and if not, what is
the cheapest test that can discriminate them? **They do not, and the discriminator is regional
isolation plus release-force variation — not timing.**

## Key findings (all calculated, no measurement)

- S1–S5 are **one bet in five shapes**: a passive, printable, final-pitch state/selection element
  written by a small shared programmer and able to hold load without powered holding.
- **S1** is downgraded: fails worst-case stroke force (≈2.37 kN all-armed; break-even 0.234 N/cell)
  and media writing (12,800 ops); survives only as **S1-B banked broadcast** (~296 N/stroke, ~17.6 s)
  and only with pre-written media — i.e. collapses into S2.
- **S2** survives as a *system* (double-buffered, off-line writer), conditional on surprise-map
  handling and exchange disturbance (frame stiffness assumed 100 N/mm — unmeasured).
- **S5** is most specified but the 5 N cam-buckling abuse gate is **not passed** even in the ideal
  model (≈4.96 N).
- **Reliability** is cross-cutting: at 0.01% per-cell error P(all 6,400 correct) ≈ 52.7%; a 6-cell
  coupon is not evidence.
- **Cost**: best-defended BOMs $432–$518 with contingency; no *matched delivered* BOM <$500.

## Ranked next tests (cheapest can-kill first)

1. **Step 0 — J2 isolation rig (Q5):** adjacent loaded full-pitch tiles; measure untouched-neighbour
   peak motion. Protocol written (Falsifier); fixture PRINT-READY PENDING HARDWARE; physical run
   owned by CTO (DND-14).
2. **Step 1 — passive pitch/backlash capability coupon** at final pitch — cheapest global kill.
3. **Step 2 — printed one-bit passive memory cell** (≥1 N hold, small toggle force, thousands of
   cycles) — kills the central bet if it fails.
4. Isolation 2×2 stack → selector/register → writer path → load/power.

## Assumptions

- Per-cell error independence; per-cell pawl release force 0.37 N; frame stiffness 100 N/mm; 5 min
  map re-plan interval; X1C / PLA 0.4 mm baseline.

## What passed / failed

- **Passed (analysis):** S1/S2 pitch budget closes; S1/S2 read timing <30 s under stated assumptions.
- **Failed (analysis):** S1 worst-case force and mask writing; the entire field on physical evidence
  (none exists) and on matched delivered cost.

## Repo-hygiene note

This branch, like the other feature branches, carries a **bootstrap copy** of
`.github/workflows/open-pr.yml` so it can open its own PR (the reusable version is not yet on
`main` — see PR #14). When the reusable workflow lands, the copies should be stripped from feature
branches to avoid duplicate/open-on-every-push behavior.

## Most informative next test

The **J2 isolation rig** run (two adjacent loaded tiles, one resident miniature) — it simultaneously
tests S2, S4, and the Q5 regional claim that S1/S2/S4 all assume.

Co-Authored-By: Paperclip <noreply@paperclip.ing>
