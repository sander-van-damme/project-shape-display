# DND-48 — fold the DND-46 falsifier residuals into the robust S5 readiness register

## What changed

Replaces the DND-44 closure **headlines** with the robust figures demanded by the
[DND-46](/DND/issues/DND-46) adversarial audit, across the two documents the acceptance names
(`08-current-design/README.md` and the company `plan`) plus the stack-up model that publishes
them. Also lands the audit content itself (PR #44) so `falsifier_checks.py` is in CI.

- `08-current-design/README.md` — §2 cost row, §4 core note, §5 BOM variants, §7 risk register
  (K1/K5/K6/K8/K11), §8 workstreams and §9 the **robust final readiness verdict**.
- `06-experiments/test12_winner_convergence/model.py` — K1/K5/K6/K8/K11 KILLERS status/result and
  the time/cost notes now carry the robust figures; new `robust_planning_delivered()` anchor.
- `06-experiments/test12_winner_convergence/checks.py` — labels/anchors updated to match.
- `06-experiments/test12_winner_convergence/register_checks.py` — **new:** 14 CI gates that fail
  if a robust figure is mis-computed *or* if the register regresses to a DND-44 headline.
- `06-experiments/test12_winner_convergence/FALSIFIER_AUDIT.md` + `falsifier_checks.py` +
  `.github/workflows/ci.yml` — the DND-46 audit and its 19 checks (PR #44 content), merged here.
- `06-experiments/test12_winner_convergence/README.md`, `DND44_READINESS.md`,
  `07-evidence-and-decisions/README.md` — supersession banners / robust-register pointer.
- `.github/workflows/ci.yml` — runs `register_checks.py`.

Rebased onto `main` including [DND-45](/DND/issues/DND-45) (PR #45, K2 named scallop + K9
Monte-Carlo); DND-45's K2/K9 closures are preserved alongside these K1/K5/K6/K8/K11 robust edits.

## Engineering question

Do the DND-44 closure headlines survive adversarial attack, and if not, what is the defensible
readiness statement the repo should carry?

## Robust figures (all CALCULATION, no print — [DND-27](/DND/issues/DND-27))

| Killer | DND-44 headline | Robust figure (DND-48) |
|---|---|---|
| K5 cost | $424.95, $75.05 margin | **$482.95, $17.05 margin** (E5 spares + E6 bundled lines restored); sourced-DRV8833 variant **$474.91**; expected-motor case **$501.51 (over)**. E6 is best-case repricing, not sourcing. |
| K1 service | ≤0.39 N/column, 12.7× margin | **0.39–3.27 N/column**; the rigid three-point-contact case (3.27 N) is bounding (1.5× margin). Size the core for **~3.3 N**. |
| K8 lateral | 1 N → 0.01 mm; limit ~9.4 N | At the repo's own **40 mm** free length, 1 N → **0.356 mm** and the 0.10 mm-gate load is **0.28 N**. Gate = free-length/guide-capture. |
| K6 timing | "not a rate problem" | Conditional on a loaded dwell **AND** a **≥268 pps (~804 rpm)** loaded rate; `inspection_s = 0` assumed. |
| K11 cycle life | ~1e8 cycles | **">=1e6, order unknown"** (4e5–1e9 across defensible FDM constants). |
| K10 regional | bounded | **CONFIRMED** — clean analytic bound. |

Every cost figure is re-derived arithmetically from `cost_closure.py`'s own spine
(`sourced_parts_usd = 366.34`, ×1.16 delivered) and asserted in `register_checks.py`.

## What passed / failed

- `register_checks.py` 14/14, `falsifier_checks.py` 19/19, and all six existing closure/stack-up
  check modules pass locally.
- No closure module was changed — the audit and the register are the only substantive edits.

## Assumptions

- Cost basis is the repo's own additive ×1.16 delivered uplift and `unit_expected`/`unit_best`
  columns; no new sourcing.
- The three-point-contact model is the bounding base-contact case; the true service load depends
  on the real miniature base (conformity vs rigidity) — a named residual.

## What remains uncertain / next most informative test

Residuals match `FALSIFIER_AUDIT.md` §8: **K7** (matched motor ≤$1.86), **K5-basis** (bundled-line
+ spares quote), **K1-service** (base-contact model), **K8-free** (guide-capture length),
**K6-rate/dwell** (loaded torque-speed + dwell), **K2/K9/K4/K11** and **R1/R2** (print/measurement
quantities, forbidden under DND-27). The most informative cheap test remains a single loaded
engage/settle dwell timing at the design rate.

## Acceptance mapping

- [x] `08-current-design/README.md` and the `plan` document carry the robust figures, not the
  DND-44 headlines.
- [x] Final readiness statement residual list matches `FALSIFIER_AUDIT.md` §8 (gated by
  `register_checks.py`).
- [x] PR #44 content merged so `falsifier_checks.py` is in CI.
