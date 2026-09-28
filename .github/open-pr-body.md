# DND-49: close K7 — trace a matched 8 mm 18° bipolar PM stepper to ≤ $1.86 delivered (or refute the cost path)

Closes K7, the **last agent-reachable cost killer** and the binding residual of the S5
cost path. Requested work: sourcing/analysis only — **no purchase, no print**
([DND-27](/DND/issues/DND-27)).

## What changed

- **New** `06-experiments/test12_winner_convergence/k7_motor_trace.py` — the K7
  sourcing trace: actuator envelope, sourced candidate table, break-even math, and
  the reduced-head design-lever timing check.
- **New** `06-experiments/test12_winner_convergence/k7_motor_trace_checks.py` —
  9 CI-gated regression/honesty checks.
- `06-experiments/test11_cost_printability_reliability/sourcing_notes.md` — **§8**
  candidate table with URLs, qty-100 unit prices and datasheet specs.
- `08-current-design/README.md` — §5 note, §7 K7 row, §9 verdict row updated.
- `06-experiments/test12_winner_convergence/{README.md,DND44_READINESS.md}` — K7 rows.
- `.github/workflows/ci.yml` — new "Test12 K7 matched-motor sourcing trace" step.

## The engineering question

Does a **matched, traced** 8 mm 18° 2-phase **bipolar** PM stepper exist at
**≤ $1.86 delivered-inclusive**? If not, what is the cheapest matched price, the
resulting delivered total, and the minimum-cost design lever to get back under $500?

The $1.86 is the break-even of the [DND-44]/[DND-47] machine-preserving path: each
$1.00 of motor price adds $92.80 delivered over 80 channels (`k7_motor_trace`:
break-even = **$1.8587**).

## Evidence produced (sourced listings, retrieved 2026-09-28)

| Vendor | Part | Unit | Qty basis | Matched? | Delivered (80) |
|---|---|---:|---|---|---:|
| CCHT (Made-in-China) | 8 mm 3.3 V, model 07-005-032 | **$8.20** | 3,001+ (**$11.20 @100**) | yes | **$1,088 / $1,367** |
| CCHT | 8 mm 5 V, model 07-005-036 | $11.20 | 100–1,000 | yes (torque fails) | $1,367 |
| MOONS | 8PM020S1-02001 | $40.00 | 1 (list) | yes | $4,040 |
| DFRobot | FIT0708 | $11.90 | 10+ | no (10 mm) | $1,432 |
| Amazon "Abovehill" | 10-pair 8 mm multipack | $1.05 | pack | **no (no step angle)** | $424.95 |
| AliExpress | 10-pc 8×9.5 mm pack | $0.86 | pack | **no (no step angle)** | $407.32 |
| AliExpress | Micro Mini 8 mm | $2.66 | 1 pc | no (no 18° spec) | $574.36 |

Not stocked as a bare 8 mm 18° bipolar PM stepper: LCSC, DigiKey (403), Mouser
(denied), Octopart, Adafruit, Pololu, SparkFun; Alibaba/Made-in-China family bottoms
at ~$8.20 at 3,000+ units.

## Result — **K7 REFUTED on sourced evidence**

- **No matched, orderable 8 mm 18° bipolar PM stepper exists at ≤ $1.86 delivered.**
  The cheapest matched part is **$8.20–$11.20** → **$1,088–$1,367 delivered**; the only
  matched + fully-specified retail part (MOONS) is **$40** → **$4,040**.
- The sub-$1.86 path exists **only** for an untraced marketplace multipack whose
  **step angle is not published** and whose product pages are JS-only. That is the
  residual K7 describes.
- **Caution flag:** the MOONS matched part's *detent* torque (0.15 mN·m) **equals the
  target running torque** — detent drag subtracts from running torque, so holding is
  not a proxy.
- **The reduced-head design lever is not viable.** Fewer motors would let a pricier
  matched motor fit (20 @ $8.20 ≈ $536; 10 ≈ $432), but the head programs all 80
  columns per row, so fewer channels means `80/N` re-index passes per row. Re-derived
  on the Test12 timing model: **W=40 → ~104 s, W=20 → ~162 s, W=10 → ~229 s** — all
  fail the 30 s budget. W=80 → 26.3 s passes.

Honest design-level options, both outside agent reach: (a) qualify the marketplace
multipack by buying/sampling a lot (forbidden under DND-27), or (b) change the head
actuator class / drive topology.

## What passed / failed

- All Test12 checks pass, including the 9 new K7 checks (`python k7_motor_trace_checks.py`).
- Full stdlib check suite (test08–test13, falsification, fixtures) re-run green locally.

## Assumptions & limits

- Prices are point-in-time listings (2026-09-28), not quotations. Delivered uplift is
  the repo's additive ×1.16 ([DND-41](/DND/issues/DND-41)).
- No running torque-vs-speed curve is published for any 8 mm-class PM stepper by any
  accessible source; the envelope is stated from the winner definition (`params.json`).
- No purchase, print or measurement — evidence class is SOURCED-LISTING / calculation.

## Remains uncertain / next test

K7 cannot be retired by agents under DND-27. The next decision is **product-level**:
accept the untraced-multipack risk with a named purchaser qualification gate, or open a
head-actuator-class change. Keep the issue's `06`/`07` records current if either is chosen.
