# DND-38: analytic detent contact sweep for S5 — bounds K2

Resolves [DND-38](/DND/issues/DND-38). Turns the S5 winner's one residual risk
(**K2**, printed rotary detent hold/repeat after a slipped step) from
"qualitative, no closed form" into a bounded, parameterised condition, and gives
the concrete closing levers. Calculation only — no print, no measurement
([DND-27](/DND/issues/DND-27)).

> **Note on base.** This branch is based on `dnd-35-convergence-winner` (the
> accepted ADR-002 convergence, `afa4ba8`), which is not yet on `main`. Opening
> this PR against `main` therefore also integrates the DND-35 winner promotion.

## Engineering question

Does the nominal printed detent (0.45 mm leaf, 10 mm long, 1 mm wide, 0.2 mm
scallop; `test09/params.json`) correct a one-step (18°) rotor slip and hold
height, across a **sourced** PLA–PLA static-friction range and a ±0.05 mm
print-tolerance stack-up?

## Evidence produced

New, CI-gated analytic model `06-experiments/test12_winner_convergence/detent_contact.py`
+ honesty/regression gates `detent_checks.py` + write-up `DETENT_CONTACT.md`.

- Reproduces **all three existing detent anchors**: peak restoring torque
  **0.00298 mN·m** (Test09), peak leaf force **6.58 mN** and strain **0.13 %**
  (Test08).
- Governing law: **`T_r/T_f = A·k/(μ·r)`**, exactly independent of E and
  preload (both torques carry the leaf force) — asserted in tests.
- **Nominal leaf fails at the sourced friction midpoint μ = 0.35**: restoring
  0.00256 mN·m vs friction 0.00278 mN·m → ratio **0.92 < 1**. A slipped rotor
  stays one 10 mm level wrong.
- **μ cliff = 0.323**. Closes only at the low end of the sourced PLA range
  (μ ≤ 0.32) **or** by deepening the scallop from 0.20 mm to **≥ 0.31 mm**
  (1.55×; recommended 0.34 mm with 10 % margin).
- Independent finding: the seated-valley friction dead-band is **0.00093 mN·m**,
  ~**25× below** the 0.02356 mN·m toe-flat plateau disturbance — the detent alone
  cannot hold terrain load; the **hard stop** remains the retention element.

**Verdict: `conditional`.** The leaf as dimensioned is not sufficient across the
sourced friction range; a geometry/friction change is required. It **does not
kill S5**.

## Assumptions / named un-modelled terms

- Leaf modelled as a linear cantilever, `K = E·b·t³/(4·L³)`; friction as a Coulomb
  moment `μ·F·r` opposing the slide at the mid rim radius (1.55 mm).
- Modulus envelope 700–2500 MPa and μ 0.2/0.35/0.5 are taken from Test09 params
  and the J2 analytic gate's sourced PLA–PLA range.
- **Un-modelled and un-measurable under DND-27:** the as-printed μ, creep, wear,
  and the FDM-achieved scallop depth. K2 therefore stays on the risk register as
  a **conditional** item with a quantitative pass rule.

## What changed

- `detent_contact.py`, `detent_checks.py`, `DETENT_CONTACT.md` — new model, gates
  and write-up.
- `test12_winner_convergence/checks.py` — K2 asserted as
  `conditional-analytically` carrying the 0.323 rule.
- `model.py`, `README.md` — K2 result updated; cheapest-falsification marked run.
- `07-evidence-and-decisions/convergence-decision-2026-09-b.md` and
  `08-current-design/README.md` — K2 status and next action updated.
- `.github/workflows/ci.yml` — runs the detent sweep + checks on every push/PR.

## Tests run

```text
python 06-experiments/test12_winner_convergence/detent_contact.py   # JSON result
python 06-experiments/test12_winner_convergence/detent_checks.py    # 9 checks, OK
python 06-experiments/test12_winner_convergence/checks.py           # 9 checks, OK
python 06-experiments/test12_winner_convergence/model.py            # stack-up
```

## Passed / failed

- **Passed:** anchor reproduction; E-independence; K2 bounded and CI-gated.
- **Failed (design finding, not tool error):** the nominal printed detent does not
  correct a step at the sourced midpoint friction.

## Remaining uncertainty / next test

Only a printed μ + scallop-depth coupon can close K2 fully; DND-27 forbids it.
Until then the design must either specify a controlled low-friction rim contact
or adopt the ≥ 0.31 mm scallop.
