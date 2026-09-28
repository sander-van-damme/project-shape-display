# DND-46 — Falsifier adversarial audit of the DND-44 S5 readiness closure

## What changed

Adds the independent adversarial audit of the DND-44 closure work
([DND-44](/DND/issues/DND-44)) requested by [DND-46](/DND/issues/DND-46), before the
CTO writes a final readiness verdict:

- `06-experiments/test12_winner_convergence/falsifier_checks.py` — 19 CI-runnable
  regression gates that encode the **attacks**, not the closures. If a closure is
  later "fixed" by quietly re-tightening an assumption, one of these fails.
- `06-experiments/test12_winner_convergence/FALSIFIER_AUDIT.md` — per-closure
  verdict, strongest counter-argument, and the minimal residual to keep.
- `.github/workflows/ci.yml` — runs `falsifier_checks.py` alongside the closure checks.

Base: the `dnd44-readiness-closure` tip, so the audit is against the exact reviewed state.
This PR is audit-only; it does not modify the closure modules or `08-current-design`.

## Engineering question

Can the DND-44 closures (K1/K5/K6/K8/K10/K11) withstand an adversarial attack, or is
the claimed closure false?

## Evidence produced (CALCULATION only, no print/measure — DND-27)

| Killer | DND-44 claim | Falsifier verdict | Strongest counter-argument |
|---|---|---|---|
| K6 timing | not a rate problem; ~268 pps meets 30 s | CONFIRMED-WITH-CAVEAT | Floor arithmetic is a real re-derivation, but 268 pps is ~804 rpm (design 400 pps = 1200 rpm) and the 26.25 s pass assumes `inspection_s=0`. With the sweep's own 3 s inspection the 27 s target is missed. |
| K1 buckling | ≤0.39 N/column, 12.7× margin | **BROKEN** | A rigid base on a height-varying field is a three-point contact: 1 kg → **3.27 N/column**, a 1.5× margin, not 12.7×. `ceil(d/pitch)²` also overcounts the cells under a round base. |
| K5 cost | $424.95 delivered, $75 margin | **BROKEN AS STATED** | $75 needs four simultaneous best cases. Restore spares (E5) + bundled `unit_expected` (E6) → **$482.95 / $17.05 margin**; at the *sourced* DRV8833PWPR → $474.91; with an expected motor → **$501.51 (over)**. E6 is best-case repricing of four bundled lines, not sourcing. |
| K8 lateral | 1 N → 0.01 mm; limit ~9.4 N | **BROKEN** | The 12 mm free length is hard-coded in `__main__`; the repo's own `unrelieved_upper_body_length_mm = 40 mm`. At 40 mm a 1 N lateral load deflects **0.356 mm**, 3.5× the 0.10 mm gate. |
| K10 regional | bounded | CONFIRMED | Complete, monotonic bound. Caveat: fixed platen stroke sets the floor, not region size. |
| K11 cycle life | ~1e8 cycles | PSEUDO-QUANTITATIVE | The 9.98e7 point estimate rests on ε_endurance=0.3 % and m=8; a conservative FDM endurance drops it 25×. |

Attacks that **failed** (recorded): the K6 closed-form arithmetic (reproduces
`test09/analyze.schedule()` to 1e-15 s; the floor is a true bound), K10 completeness,
and the E1 driver *topology* (dual H-bridge for dual H-bridge — the attack is on its
price basis, not its kind).

## Assumptions

- All counter-numbers are arithmetic over the repo's own `params.json`, BOM CSV and
  closure-module inputs. No new sources were introduced.
- The three-point-contact model is a **worst-case bounding model**, not a claim that
  every base tripods; it shows the 0.39 N figure is a best case, not a bound.
- The K5 variants treat "keep spares" and "bundled lines at `unit_expected`" as the
  defensible planning basis; the closure's own BOM CSV supplies both numbers.

## What passed / failed

- **Passed:** K6 floor arithmetic; K10 regional bound; E1 driver topology.
- **Failed:** K1 service bound, K5 stated margin, K8 lateral free-length, K11 point
  estimate.

## What remains uncertain

- Whether a real miniature base conforms (sharing load) or tripods (K1).
- The realised loaded dwell and the loaded torque-speed point (K6).
- The free length at extension (K8) and printed guide-wall shear.
- A sourcing quote for the four bundled lines and a spares policy (K5/K7).

## Next test

One printed coupon set would retire most residuals: a free-length/guide-capture
coupon (K8/K9), a base-contact load coupon (K1), a loaded row-cycle timing coupon
(K6/K10), and a detent creep coupon (K11) — gated under [DND-27](/DND/issues/DND-27),
so they stay named residuals for the final readiness register.

Run: `python 06-experiments/test12_winner_convergence/falsifier_checks.py`
