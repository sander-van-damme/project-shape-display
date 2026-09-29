# DND-54: price the S5-R block's own channels in the model ($401.12 honest total)

Advances [DND-54](/DND/issues/DND-54), folding in the material finding of the
[DND-56](/DND/issues/DND-56) BOM ratification. The promoting model
(`s5r_register.bom()`) priced the S5-R actuator block's **own** bought driver
channels at zero, so its headline `$397.53` delivered total was not
convention-correct: the fixed no-channel base removes **both** the 80-motor line
**and** the 80-channel TB6612 driver block, and the `nx52_head_actuator.py`
contract requires every option to *"declare its own channel cost exactly once
(no double-count)."* This PR makes the model declare them.

**Evidence class: CALCULATION over sourced listings and stated assumptions. No
purchase, print or physical measurement** ([DND-27](/DND/issues/DND-27)).

## What changed

- `06-experiments/test12_winner_convergence/s5r_register.py` — `bom()` now prices
  the block's own channels: **2 bank H-bridge ICs** (1 dual TB6612 per bank motor,
  `$0.7955` each = `$1.59`) **+ 5 ULN2803-class writer darlington chips** (8
  ON/OFF writers each, `$0.30` each = `$1.50`) = **`$3.09` parts**. The honest
  working total is `delivered_usd = $401.12`; the channels-unpriced DND-54 claim
  is preserved as `delivered_claim_usd = $397.53` (and `parts_claim_usd`). G7
  still passes: `$98.88` under the `$500` ceiling.
- `s5r_register_checks.py` — new gate `test_block_channels_priced_once_and_claim_reproduces`
  asserts the channel line is priced once, the claim reproduces exactly, and the
  honest total equals the ratification's working scenario (16 gates, was 15).
- `s5r_bom_ratify.py` — `reconcile_with_s5r_module()` now reconciles the model's
  **honest** total and channel line against the ratification's working scenario,
  in addition to the claim.
- `07-evidence-and-decisions/dnd54-s5r-register-latch.md` — §5 states the model
  now carries the channels; `$397.53` is the claim, `$401.12` the working total.
- `08-current-design/README.md` — notes the model carries the channels explicitly.

## Engineering question

Does the promoting S5-R model price its own bought channels exactly once, so its
BOM is auditable and the delivered total is the honest one — while still clearing
the `$500` ceiling and the `$30 s` time gate?

## Evidence produced

- Model now returns: fixed no-channel `$218.70`, actuators `$124.00`, channels
  `$3.09`, parts `$345.79`, **delivered `$401.12`** (working), margin `$98.88`,
  claim `$397.53`. `s5r_register.py`, `s5r_register_checks.py` (16 gates),
  `s5r_bom_ratify.py --selftest` + `s5r_bom_ratify_checks.py` (11 gates) all pass;
  all 12 test12 check suites green; the exact CI commands pass locally.

## Assumptions

- Working channel count: conservative 1 dual TB6612 per bank motor (2 ICs); the
  optimistic shared-IC case (1 IC, `$2.30` total) is carried alongside.
- Writer solenoids are ON/OFF loads, so a `$0.30` ULN2803-class darlington
  suffices (not an H-bridge) — the DND-56 insight.
- Unit prices are sourced point-in-time (LCSC C88224 `$0.7955`; ULN2803 allowance).

## Passed / failed

- **Passed:** channel pricing, claim reproduction, cross-module reconciliation,
  G7 cost gate (`$401.12 < $500`), all test12 suites.
- **Failed:** nothing. The DND-54 `< $400 ideal` phrasing was already corrected by
  the CTO amendment to "optimistic scenario; ~$1.12 over working."

## Remains uncertain / next test

- Writer-solenoid **force (N) is not published** by any listing (R-DND54-6), and
  no 2-piece contract quote exists — both purchase-gated ([DND-27](/DND/issues/DND-27)).
- The **multi-row (R=4) bar assembly CAD** (bar torsion, reset comber, writer
  carriage envelope) remains the next discriminating agent-reachable test
  (DND-54 §10 item 3); it is CTO-owned, not a cost item.
