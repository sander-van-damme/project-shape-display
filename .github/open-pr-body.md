# DND-44 — S5 readiness closure: close cost/time/buckling killers analytically

## What changed

Advances the promoted S5 winner (`08-current-design/`) from an *honest analytic definition*
to the **closest reachable print-ready state** under the no-physical-test policy
([DND-27](/DND/issues/DND-27)). Six killers are closed or bounded analytically; the risk
register is re-labelled and the residual is reduced to a short list of named physical
quantities.

New analytic modules in `06-experiments/test12_winner_convergence/` (CALCULATION only):

- `timing_closure.py` (K6) — closed-form per-row budget; splits the rate-independent floor
  from rate terms; cross-checks `test09/analyze.schedule()` to 3.6e-15 s.
- `buckling_closure.py` (K1) — bounds the distributed tabletop load over a miniature's base;
  reproduces the repo's own variable-section buckling model across core radii.
- `cost_closure.py` (K5/K7) — rebuilds the sourced BOM with machine-preserving changes E1–E6;
  audits every delta; finds the motor break-even price.
- `cross_cutting_closure.py` (K8/K10/K11) — lateral load path, regional-update bound, detent
  cycle-life bound.
- `DND44_READINESS.md` — the consolidated closure record.
- Six `*_checks.py` regression/honesty gates (46 tests), all wired into CI.

`08-current-design/README.md` now carries the **Final readiness verdict (§9)** and an updated
risk register; `06-experiments/test12_winner_convergence/model.py` and `checks.py` are updated
to match.

## Engineering question addressed

Which DND-41 killers can be closed or bounded analytically, and which single physical quantity
does each residual need?

## Evidence produced (all CALCULATION — no print, no measurement)

- **K1** service load ≤ 0.39 N/column (even a 1 kg miniature on the smallest 25.4 mm base;
  12.7× margin vs the 4.96 N core). The localized 5 N abuse screen is bounded: a 1.10 mm core
  gives 5.60 N, at the cost of step height 0.5→0.4 mm.
- **K5** honest expected delivered baseline **$592.06** (the earlier $501.12 used a $0.80
  driver + best-case motor). Machine-preserving source path **$424.95 delivered, $75.05
  margin**, clearing only for a motor ≤ $1.86.
- **K6** the 45.07 s sweep worst corner is **not** a step-rate problem: the rate-independent
  floor is 18.65 s and ~268 pps meets 30 s at the design point; verify the loaded dwell and
  scan accel, not a "measured rate".
- **K8** lateral load is carried by the guide/bending (1 N → 0.01 mm; limit ~9.4 N), not the
  detent.
- **K10** regional updates 3.9–6.3 s for 1–10 rows.
- **K11** detent leaf ~10⁸ cycles (order-of-magnitude bound).

## Assumptions

All timing/engagement dwells are assumed inputs; the distributed-load argument assumes a
miniature's base spreads over its footprint; cost uses the BOM's own `unit_best/expected`
columns and the sourced LCSC/marketplace listings already in the repo. No new prices were
invented.

## What passed / failed

All 46 checks pass; the CI step for the new closure modules is added. `timing_closure.py` and
`buckling_closure.py` call the repo's own models rather than re-implementing them, so they
cannot drift.

## What remains uncertain

The residual is now exactly: **K7** (a matched 8 mm 18° bipolar PM stepper at ≤ $1.86) plus the
print-realisation quantities (K2 μ/scallop, K9 rotor tolerance, K1-abuse core crush, K4
stiction release/drift, K8 guide shear, K11 creep, R1 error rate, R2 miniature height). Each
needs the named physical measurement, which DND-27 forbids.

## Most informative next test

Purchase+sample one candidate motor lot and measure its step angle, winding resistance and
running torque, which retires K7 and, with it, the only remaining cost residual.

## Delegated verification

- [DND-45](/DND/issues/DND-45) — K2 geometry choice at μ=0.35 and K9 Monte-Carlo angular tolerance.
- [DND-46](/DND/issues/DND-46) — Falsifier adversarial audit of the four closure modules.
- [DND-47](/DND/issues/DND-47) — CostManufacturing ratification of the $424.95 BOM path.
