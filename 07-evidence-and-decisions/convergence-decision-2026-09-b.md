# ADR-002 — Convergence to one buildable machine: S5 promoted to `08-current-design`

- **Status:** Accepted (CTO), delegated merge authority ([DND-19](/DND/issues/DND-19)).
- **Date:** 2026-09-28.
- **Owner:** CTO.
- **Issue:** [DND-35](/DND/issues/DND-35).
- **Supersedes:** the "no architecture promoted" posture of
  [`convergence-decision-2026-09.md`](convergence-decision-2026-09.md) (ADR-001) and the
  "five co-equal survivors" posture of
  [`04-architecture-candidates/`](../04-architecture-candidates/README.md).
- **Amends:** [`convergence-plan.md`](convergence-plan.md) §4.1, which required explicit
  board acceptance of the §3.2 qualitative risks before promotion. Under
  [DND-32](/DND/issues/DND-32) the board has directed near-total silence and delegated the
  convergence decision to the CTO; the qualitative risks are therefore **accepted
  internally, recorded, and carried on the risk register** rather than held pending a board
  confirmation.

## 1. Decision

**Promote S5 — programmed stepped rotary stops + common lift — to
[`08-current-design/`](../08-current-design/README.md) as the single buildable winner.**

Every other candidate is recorded as killed or parked with binding evidence (§2). The
decision rests on the fact that S5 is the **only** candidate that simultaneously has:

1. **real solid CAD** of the mechanism (rotor, follower, guides, lift plate; interference
   checked at five levels and twenty raised angles — `06-experiments/test08_architecture_search/`),
2. an **independently reproduced timing model** under the 30 s cap (**26.251 s**,
   `06-experiments/test09_test08_validation/results/summary.json`),
3. a purchased BOM that is **82 % sourced** (vs 24–37 % for S1–S4), i.e. the only cost
   number in the field that is more sourced than assumed.

This is a decision on **evidence quality**, not preference. S1 and S4 show nominally lower
working BOMs, but those BOMs are dominated by unquoted coupling/selection allowances and are
therefore less trustworthy than S5's; a nominal cost win on a 30 %-sourced BOM is not a real
win.

## 2. Killing evidence for the dropped candidates

| # | Candidate | Disposition | Binding evidence | Source |
|---|---|---|---|---|
| S1 | threshold ratchet + broadcast incremental lift | **kill** | worst-case all-armed stroke **2,368 N vs 1,500 N** cap; mask write requires ≥500 parallel channels; no CAD | `test11_threshold_ratchet_s1/rejection.py` |
| S1-B | banked broadcast ratchet | **park** | force fixed by banking (≈296 N/stroke, 17.6 s), but mask writing still needs pre-written media — collapses into S2 | `convergence-decision-2026-09.md` §3 |
| S2 | planar-memory tiles | **park** | survives only double-buffered with an off-line writer; cannot serve surprise maps; no CAD | `test11_threshold_ratchet_s1/` |
| S3 | multi-row mechanical DMA head | **kill** | sourced analytic printability **FAIL**: pivot 0.80 < 5.0, declared min web 0.24 < 0.88; expected delivered **$2,880.98** (5.8× ceiling); **CI-visible** | `tools/validate/analytic_printability.py` on `selector_fanout_coupon.scad` |
| S4 | distributed passive tiles on a shared bus | **park** | printed dog clutch must transmit tile torque and fail open; correlated bus backlash exceeds 0.25 mm at 3°/joint; expected delivered $548.91 | `test11_shared_drive_gate_analysis/` |
| S5 | programmed rotary stops + common lift | **WIN** | only CAD+simulation+sourced-BOM candidate; 26.251 s; sourced cost $503.71, reduced $481.56 | this ADR, `test12_winner_convergence/` |

**Failed ideas are kept as assets**, not deleted: the rejection log in
`test08/README.md:114-150` (unsupported follower, nine-level angular failure, 40-channel
timing failure, thin-core cam buckling) and the S3/S4 selector-coupon findings
(`test11_selector_coupon/`) remain in the search record.

## 3. Why the winner's two headline blockers do not block

### 3.1 The 5 N cam-buckling "gate" is mis-scoped

The revised 1.0 mm cam core gives **4.96 N** ideal critical buckling load, below a
self-imposed **5 N** screen. But the product requirement is a **1 N service load for 24 h**;
the 5 N is a *sacrificial handling screen*, explicitly described as
"**not a whole-hand safety certification**" (`test08/README.md:263`). Against the actual
1 N service load the design has a **≈5× margin**. The 5 N screen is retained as a coupon
handling test for the printed part, not as a design gate. This is a **reclassification on
evidence**, not a relaxation of a product requirement.

### 3.2 Cost clears $500 with margin on a matched sourced path

The motor/driver channel is the only cliff. On the sourced pairing (Amazon multipack 8 mm
PM motor $1.05 + TB6612FNG $0.80, expected delivered uplift ×1.16), the winner lands at
**$503.71** — essentially on the ceiling. Two concrete BOM consolidations bring it to
**$481.56**:

- fold the 40 discrete 74HC595 shift registers onto the custom driver PCB (−$14, a line
  already present in the BOM as "custom driver PCBs and passives");
- use the sourced RP2040 controller instead of the $10 allowance (−$5).

Reaching the project's <$400 ideal band is **not** demonstrated. The winner lands in the
"acceptable" ($200–$400) to "last-resort" ($400–$500) band — with margin under the ceiling.

## 4. Consequences

- `08-current-design/` now names one machine with a full buildable definition, sourced BOM,
  assembly route and print-ready CAD.
- The source-of-truth programme risk register is now:
  1. **K2** — printed rotary detent hold/repeat (qualitative; DND-27).
  2. **Reliability** — q ≤ 1.57×10⁻⁶ needed for 99 % map correctness; no per-cell feedback
     (assumption).
  3. **40 mm travel** — provisional design envelope; no representative miniature measured.
  4. **Realised step rate** — timing depends on ≥400 pps loaded, assumed.
  5. **Matched motor supply** — the only traceable matched 8 mm PM stepper is $40/ea; the
     sub-$1.05 price is an untraced marketplace multipack.
- S1/S2/S4 remain **parked** (stated next analytic step, not a hope). S3 is **killed**.
- No sixth variation of the shared-power/passive-memory bet will be invented; if a residual
  risk above proves fatal under analysis, the correct response is a product-requirement
  re-scope escalated to the CEO — not more candidates.

## 5. Honesty statement

Every figure in this ADR is **sourced fact, stated assumption, calculation, simulation, or
CAD** — never physical validation. **No printed or measured shape-display evidence exists,
and under [DND-27](/DND/issues/DND-27) none will be produced.** The 40 mm travel, the
sub-$1.05 motor price, the 400 pps loaded rate, the per-cell error rate and the printed
detent behaviour are **assumptions**, named as such, that analysis cannot retire.
