# DND-36: Falsifier adversarial review of the S5 winner promotion (DND-35)

Resolves [DND-36](/DND/issues/DND-36). Independent adversarial review of the CTO's
[DND-35](/DND/issues/DND-35) convergence: ADR-002 promotes **S5 — programmed stepped
rotary stops + common lift** to the single buildable winner. This PR tries to kill that
promotion on evidence, not to ratify it.

## Engineering question

Is the S5 promotion — its killer list and its end-to-end time/cost/isolation stack-up —
supported as stated, or does it present contestable / measurement-only / arithmetic-broken
claims as closed?

## Verdict

**The direction survives; the promotion fails as stated.**

- S5 is genuinely the best-evidenced candidate (real CAD + a reproduced timing model + an
  82 %-sourced BOM). Promoting it over S1–S4 is defensible.
- But **three of six `closed-analytically` killers are not closed as written**, and the
  **cost margin is an arithmetic artifact**.

| Killer | ADR-002 says | This review finds |
|---|---|---|
| K1 cam buckling | closed, 4.96 N vs 1 N | **contested** — `test08/README.md:263` says the 5 N screen is *not* met and "expect a redesign"; the 1 N service load is unsourced (`miniature_measured:false`) |
| K4 regional isolation | closed, 0.017 vs 0.10 mm | **not closed** — the cited J2 gate returns `INCONCLUSIVE`; stiction release + wear drift are measurement-only |
| K6 time < 30 s | closed, 26.251 s | **conditional** — 26.251 s is one corner of the repo's own 540-case sweep; at 400 pps **17/108 pass**, worst **45.07 s** |
| K5 cost < $500 | closed, $503.71→$481.56 | **fails on the repo's own basis** — sourced-pair delivered = **$501.12** (over ceiling); $503.71 needs an inconsistent multiplicative uplift (`1.10*1.06`) plus a $2.20 subtotal error; the reduction is partly double-counted |

## Evidence produced

- New note `07-evidence-and-decisions/falsifier-s5-promotion-review-2026-09.md` — full
  adversarial review with per-finding cheapest falsification and a ranked, **print-free**
  experiment list.
- New executable `07-evidence-and-decisions/falsifier_s5_review_checks.py` — reproduces all
  four findings from repository inputs (`bom_S5_delivered.csv`, `timing_sweep.csv`, the J2
  analytic README) and asserts them, so the review can be verified rather than trusted.
- `07-evidence-and-decisions/README.md` — index points to the review.
- Plus six **unstated killers** the winner's list omitted (purchased-actuator cost cliff at
  $40/ea MOONS; no lateral-holding killer; print-tolerance erosion of the 6.5° angular
  margin; regional-update time; detent cycle life).

## Evidence class / limits

All claims are **CALCULATION** on repository inputs or **sourced-fact** readings of the
repository's own documents. **Nothing is printed or measured** ([DND-27](/DND/issues/DND-27)).
No board contact ([DND-32](/DND/issues/DND-32)).

## What remains uncertain / next test

Each finding names its cheapest print-free falsification. Priority order: (1) source the max
tabletop vertical + lateral load → closes K1/K8; (2) adopt the additive uplift and net the
register saving → K5; (3) count `under_30` at 400 pps → K6; (4) run the J2 runner → K4. This
PR changes no CAD, no BOM, and no winner selection.

## Recommendation

Keep S5 as the single winner, but **re-label K1/K4/K6 and re-state cost as a corrected
range** before `08-current-design` is called print-ready. Recorded for the CTO on DND-36.
