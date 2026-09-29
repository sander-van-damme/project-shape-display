# DND-109: reliability-first cost + printability envelope for DND-104 mechanism classes

Closes [DND-109](/DND/issues/DND-109). Child of [DND-104](/DND/issues/DND-104).

## What changed

Adds an **independent, sourced-class cost and FDM-printability envelope** for the mechanism
classes the reliability-first program (DND-104) is choosing among, so any candidate can be costed
and screened for printability **without a fresh sourcing pass each time**.

- `09-low-cost-variant/reliability_sourcing/cost_envelope_dnd104.md` — how-to-use rules, the
  sourced-class envelope, media/consumable classification, **PROVISIONAL vs sourced** printability
  rules, assembly + reliability scaling, per-class screening verdicts, and the x1.16
  delivered-uplift convention restated.
- `09-low-cost-variant/reliability_sourcing/cost_envelope_dnd104.csv` — **44 bought lines**, one per
  row, with `optimistic / working / high` scenarios, `printable_excluded` + `consumable` flags,
  sourcing reference and a "death note" per line.
- `09-low-cost-variant/reliability_sourcing/cost_envelope_checks.py` — stdlib gate (all PASS).
- `.github/workflows/ci.yml` — wires the gate into `engineering-checks`.
- `09-low-cost-variant/README.md` — index + run block updated.

## Engineering question

For any reliability-first candidate: **what does its bought hardware cost, what must be bought
rather than printed, what is printable on the baseline X1C/PLA process at 5.08 mm pitch, and how do
per-cell failure and assembly scale toward the <$250 / 99 %-perfect-map targets?**

## Evidence produced

- **Sourced-class listing observations + CALCULATION.** No part bought, printed or measured
  ([DND-27](/DND/issues/DND-27)). Prices are point-in-time (2026-09), consistent with the repo's
  existing `sourcing_notes.md` and `bom_s6lc.csv`.
- **Delivered convention:** additive ×1.16 (+10 % ship, +6 % tax) → **$215.52 parts ceiling** for the
  $250 target; <$200 parts = **$232.00 delivered**.
- **Per-cell bought-hardware sensitivity** (the load-bearing result): $0.05/cell = $320 (fails);
  $0.10/cell = $640; one N20/cell = $7,680; one solenoid/cell = $28,480. **Zero per-cell bought
  hardware is mandatory.**
- **Media classification:** punched card / film / tape / cover film are flagged **consumable and
  purchased**; printed combs/gates/strips are legitimately printed-and-excluded.
- **Printability table** with each rule labelled SOURCED (process limits: 0.88 mm robust wall,
  0.44 mm standalone, 0.22 mm fine-nozzle) or **PROVISIONAL** (0.45 mm/side web, 4.18 mm max body,
  tolerance stacks, sliding clearance), plus the "needs 0.2 mm nozzle or resin" flag list.
- **Reliability scaling:** `P(perfect map) = (1-q)^6400`; 99 % needs q ≤ 1.57e-6 and 1.9 M
  zero-failure trials → detection + bounded recovery must be priced, not assumed.
- **Gate:** `cost_envelope_checks.py` — all checks PASS locally.

## Assumptions

- Prices are sourced-class marketplace ranges unless marked `sourced-live` (existing repo URLs).
- Printed-part fabrication time/wear are excluded from purchased cost by project rule but are not
  free (reported in the printability section).

## What passed / failed

- **Passed:** envelope gate; all media/actuator flag integrity; scenario ordering.
- **Failed / killed on cost:** per-cell or per-row bought actuators; per-cell bearings/sensors; a
  non-shared writer/punch; the matched 8 mm stepper path ($40 → $3,200 for 80 channels).

## What remains uncertain

- Exact current retail prices (volatile); no quotation obtained.
- All printability clearances are coupon-validated rules, not measured tolerances.

## Next test

For each converged DND-104 candidate, substitute its actuator/media/per-cell counts into this
envelope and require: (1) working delivered ≤ $250, (2) zero per-cell bought lines, (3) no
`printable_excluded` flag on a motor/valve, and (4) every structural feature ≥ 0.88 mm or an explicit
fine-nozzle declaration.
