# DND-35 — Converge to one buildable architecture + printable winner

## What changed
- **ADR-002** (`07-evidence-and-decisions/convergence-decision-2026-09-b.md`): S5 —
  *programmed stepped rotary stops + common lift* — is **promoted to `08-current-design`**
  as the single buildable winner.
- **`08-current-design/README.md`**: full buildable definition — system description,
  functional allocation, key dimensions, sourced BOM, assembly route, print-ready CAD
  pointer and risk register.
- **`06-experiments/test12_winner_convergence/`**: executable end-to-end stack-up
  (`model.py`, `checks.py`) + `render_winner_cad.py` (real OpenSCAD render + mesh
  validation of all five S5 coupon parts) and its CAD record.
- CI: new Test12 stack-up checks and a winner-CAD render job.
- `04-…`/`07-…` READMEs and the evidence matrix point at the promotion.

## Engineering question
Which of S1–S5 can be defined, priced and printed now — and what is the end-to-end
stack-up?

## Evidence produced
- **Time:** 26.251 s full adversarial map (reproduced, Test09) < 30 s.
- **Cost:** sourced pair $503.71 delivered; with two BOM consolidations **$481.56**
  (clears $500 with $18.44 margin). Fixed subtotal $284.00 is reproduced from the
  sourced delivered CSV by `checks.py`.
- **Isolation:** 0.017 mm neighbour bound vs 0.10 mm gate.
- **Travel:** 40 mm / 5 levels = 10 mm increment.
- **CAD:** 5 parts render, mesh-validate and fit the 256 mm bed (`winner_cad_record.json`).
- **Kills:** S1 2368 N > 1500 N stroke + mask write; S3 analytic printability FAIL +
  $2880.98 delivered; S2/S4 parked.

## Evidence class
Sourced / assumption / calculation / simulation / CAD only. **No print, no measurement**
(DND-27). The residual risks (printed detent K2, whole-map reliability, 40 mm travel
provenance, realised step rate, matched motor supply) are named in the risk register,
not hidden.

## What passed / failed
- Passed: all stdlib checks incl. new Test12; winner CAD render (5/5 parts); existing
  Test08/09/10/11 checks unchanged.
- Failed (design findings, kept as evidence): S3 selector-fanout printability FAIL
  (pre-existing, unchanged).

## What remains uncertain
- K2 printed-detent hold/repeat (qualitative under DND-27) — cheapest falsification:
  analytic detent contact sweep ([DND-38](/DND/issues/DND-38)).
- Whole-map reliability: q ≤ 1.57e-6 needed for 99%; no per-cell feedback.
- 40 mm travel is a provisional envelope — no miniature measured.
- Matched 8 mm PM stepper supply below ~$1.05 is untraced.

## Most informative next test
The analytic detent contact sweep (K2), because it is the only residual that can flip the
winner's central passive-memory assumption.

## Coordination
- [DND-36](/DND/issues/DND-36) Falsifier adversarial review of the winner.
- [DND-37](/DND/issues/DND-37) CostManufacturing BOM + printability ratification.
- [DND-38](/DND/issues/DND-38) Analytic detent sweep (K2).
