# DND-108: pre-register adversarial audit criteria for the DND-104 reliability-first candidates

Parent [DND-104](/DND/issues/DND-104). Refs [DND-103](/DND/issues/DND-103), [DND-27](/DND/issues/DND-27),
[DND-32](/DND/issues/DND-32).

## What changed

- `07-evidence-and-decisions/falsifier_dnd104_criteria.md` — the **frozen, pre-registered** attack
  register (A1–A12 + gates) that any DND-104 reliability-first candidate must survive, written
  **before** the CTO's `10-reliability-mask/` model exists. Each attack names the exact deciding
  number, the cheapest test, the pass/fail threshold, and the consequence of pass/fail.
- `07-evidence-and-decisions/falsifier_dnd104_checks.py` — CI gate (26 self-test checks) that pins
  every counter-number so the prose cannot drift from arithmetic. Exposes
  `audit(model)` / `--model <path>` so the same checklist is applied mechanically to
  `10-reliability-mask/` the moment it lands. **Default-deny:** an unanswered attack is a FAIL.
- `.github/workflows/ci.yml` — wires the new gate into `engineering-checks`.
- `07-evidence-and-decisions/README.md` — evidence-index entry.

## Engineering question

Can the CTO's DND-104 convergence cherry-pick its gates? **No** — the gates are pre-registered here,
so a candidate is scored against a fixed target written by the adversarial critic, not by its own
author.

## Evidence produced (all CALCULATION / document audit — no print, purchase, or measurement)

- **Reliability gate math:** `P(perfect map) = (1-q)^N`. At q = 0.01 % (1e-4), a 6,400-element map is
  only **52.7 %**; a 99 %-map target requires q ≤ **1.570e-6** at N = 6,400.
- **Coupon bounds:** zero-failure trials at 95 % = **29,956** (q=1e-4), **299,572** (q=1e-5),
  **1,908,109** (q=1.570e-6). **A coupon can kill, but cannot crown:** 400 clean cycles bound q only
  at **~7.5e-3**, ~4,800× looser than the board budget — so reliability credit requires an
  error-detection/recovery path, not a lucky sample.
- **Counting attack:** the per-cell precision/force-critical count must be **zero**; DND-103 forbids
  force-critical springs and sub-mm precision contacts repeated per cell.
- **Honest timing:** the seven-stage decomposition; S1/comb mask write is **2,560 s** serial,
  **56 s** at 80 channels (fails 30 s), **8.96 s** at ~500 channels.
- **Cost (DND-46 method):** hostile repricing + restoring unlisted capabilities; S6-LC's corrected
  figure is **$226.77 parts / $263.05 delivered** (mission gate holds, delivered convention fails).
- **Load/jam/regional:** write-time load must include a mini (0.05–0.3 N); jam blast radius must be
  1 cell **and detectable**; regional neighbour displacement ≤ 0.10 mm.
- **Pitch placement:** max feature excursion ≤ owned half-lane (0.74 mm at body 3.60), audited in
  CAD, not budgeted (the DND-91/A1 failure re-stated as a hard gate).
- **Decisive falsifier A11 + coupon C1:** a 4×4 true-pitch repeated-element reliability coupon
  (measurements, thresholds, cycles, full-scale assumption, pass/fail consequences), a CTO/board
  print handoff.

## What passed / failed

- Gate runs green: **26/26** self-test checks pass; `--model` audit correctly returns `FAIL` for an
  incomplete/empty model (default-deny verified).
- No candidate is judged yet — the CTO model does not exist. This PR pre-commits the tests.

## Assumptions / what remains uncertain

- All numbers are calculation over the repo's own model (`test11_falsibility reliability.py`,
  `test11_threshold_ratchet_s1`, S6-LC); none is measured.
- Coupon C1 is a physical print that cannot run in the agent environment; it is routed to the CTO.

## Next test

Point `falsifier_dnd104_checks.py --model <path>` at the CTO's `10-reliability-mask/` model and
require the full audit vector; physical coupon C1 is the CTO handoff.
