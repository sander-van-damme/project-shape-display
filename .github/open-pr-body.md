# DND-51: land the honest post-Falsifier / post-K7 readiness record on `main`

Integrates [DND-47](/DND/issues/DND-47), [DND-48](/DND/issues/DND-48) and
[DND-49](/DND/issues/DND-49) onto `main` and folds every finding into one internally
consistent S5 readiness register. Requested work: integration + analysis only — **no
purchase, no print** ([DND-27](/DND/issues/DND-27)).

## What changed

- **CI fix (DND-49/DND-47).** `.github/workflows/ci.yml` now installs
  `numpy>=1.26` in the `engineering-checks` job before the Test12 DND-44 closures
  run. `main` was red from `e10e57a` onward because `buckling_closure.py` imports
  `numpy` via `cam_strength.py` in a stdlib-only job. This **un-reds `main`**.
- **DND-47 (cost ratification).** New
  `06-experiments/test12_winner_convergence/cost_closure_ratify.py` (independent
  re-derivation that reads `bom_S5_delivered.csv` line-by-line and does *not* import
  `cost_closure.py`), new `07-evidence-and-decisions/dnd47-cost-closure-ratification.md`,
  and `sourcing_notes.md` §8.
- **DND-48 (robust register).** New `FALSIFIER_AUDIT.md`, `falsifier_checks.py`
  (19 checks) and `register_checks.py`, plus corrected figures in
  `08-current-design/README.md`, `DND44_READINESS.md` and `07-evidence-and-decisions/`.
- **DND-49 (K7 refutation).** New `k7_motor_trace.py` / `k7_motor_trace_checks.py`,
  `sourcing_notes.md` §9, and K7 rows across the register.
- **DND-51 fold.** The DND-49 K7 refutation, written against the old DND-44 text, is
  re-expressed inside the DND-48 robust register so §7/§9 and
  `DND44_READINESS.md` agree with `register_checks.py`.

## The engineering question

What is the **honest** readiness of the S5 winner once the DND-46 adversarial audit
and the DND-49 K7 sourcing trace are folded in, and does the register on `main`
state it without overstating any killer?

## Evidence produced

| Killer | Robust figure landed | Class |
|---|---|---|
| K1 service | **0.39–3.27 N/column** (base-contact dependent); tripod case bounding at **1.5×** margin | calculation |
| K5 cost | **$482.95** defensible basis ($17.05 margin); **$474.91** sourced DRV8833; **$501.51 over** at expected motor | calculation |
| K6 time | conditional on loaded dwell **and** ≥268 pps; floor 18.65 s | calculation |
| K7 motor | **REFUTED at ≤$1.86 on sourced evidence**; cheapest matched $8.20–$11.20 → $1,088–$1,367 delivered | SOURCED-LISTING |
| K8 lateral | **0.356 mm** at 1 N (40 mm free length), 0.10 mm-gate load **0.28 N** | calculation |
| K10 regional | clean bound: 1 row ~3.9 s, 10 rows ~6.3 s, 80 rows ~24.7 s | calculation |
| K11 life | **">=1e6, order unknown"** (4e5–1e9 span) | calculation |
| K9 angular | 5 levels hold margin; 6 levels fail 65.6 % | simulation (MC) |

## What passed / failed

- All eight Test12 closure scripts pass locally once numpy is present
  (`timing`/`buckling`/`cost`/`cross_cutting` `_closure_checks.py`), plus the new
  `falsifier_checks.py`, `register_checks.py`, `cost_closure_ratify.py` and
  `k7_motor_trace_checks.py`.
- Full stdlib suite (test08–test13) re-run green locally.
- Merge order keeps `main` green at each step: DND-49 (numpy pin) → DND-47 → DND-48
  (last, so the corrected register is final).

## Assumptions & limits

- Prices are point-in-time listings (2026-09-28), not quotations; delivered uplift is
  the repo's additive ×1.16.
- No running torque-speed curve is published for any accessible 8 mm-class PM stepper.
- No purchase, print or measurement — evidence class is SOURCED-LISTING / calculation
  / CAD / simulation.

## Remains uncertain / next test

K7 cannot be retired by agents under DND-27; the honest terminal state is **"one
sourced purchase sample (K7) plus a small set of printed-coupon measurements away from
print-ready"**. The next engineering decision is the head actuator class vs the
untraced-multipack qualification gate.
