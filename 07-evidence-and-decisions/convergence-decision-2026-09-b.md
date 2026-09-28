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

### 1.1 Two bets, not one (adopting the Falsifier audit, [DND-36](/DND/issues/DND-36))

- **Bet A — written passive memory** (S1–S4): a threshold/selection element is *set* by a
  shared writer and must *memorise* a bit. Killers: print/force spread, gate hold, register
  fan-out, tile-clutch independence.
- **Bet B — absolute geometric stops** (S5): a homed rotor + gravity-following toe; no
  written bit, no threshold, no hold force that can decay. Killers: cam/toe strength, loaded
  motor torque-speed, detent capture of a lost step, motor sourcing cost.

A Bet-A failure does **not** imply a Bet-B failure. S5 is therefore selected on its own
evidence. This ADR is not evidence that Bet A is viable.

### 1.2 Adopting the Falsifier promotion review ([DND-36](/DND/issues/DND-36))

The Falsifier's winner-specific review
(`falsifier-s5-promotion-review-2026-09.md`, merged PR #27) concludes: **"S5 promotion
SURVIVES AS A DIRECTION but FAILS AS STATED."** Its arithmetic has been re-derived and
confirmed here before being adopted:

- **Cost (§3.2 corrects below):** the published $503.71 / $481.56 use a *multiplicative*
  uplift (`1.10 × 1.06`) against a fixed subtotal taken from the *additive* model. On the
  repository's own additive basis the sourced-pair delivered figure is **$501.12 — over the
  $500 ceiling** — and the reduced path is **$483.37**.
- **K1/K4/K6 labels:** three of the six "closed-analytically" killers are contestable or
  measurement-only. Re-labelled below.
- **Unstated killers:** five failure modes were absent from the killer list (motor-cost
  cliff, lateral holding, print-tolerance angular margin, regional-update time, printed-detent
  cycle life). Added as K7–K11.

**Disposition:** S5 remains the single winner, but `08-current-design` is **not** presented as
print-ready until the re-labelled killers and corrected cost range are stated. No product
requirement is relaxed ([DND-39](/DND/issues/DND-39)).

## 2. Killing evidence for the dropped candidates

| # | Candidate | Disposition | Binding evidence | Source |
|---|---|---|---|---|
| S1 | threshold ratchet + broadcast incremental lift | **kill** (Bet A) | worst-case all-armed stroke **2,368 N vs 1,500 N** cap; mask write requires ≥500 parallel channels; no CAD | `test11_threshold_ratchet_s1/rejection.py` |
| S1-B | banked broadcast ratchet | **park** | force fixed by banking (≈296 N/stroke, 17.6 s), but mask writing still needs pre-written media — collapses into S2 | `convergence-decision-2026-09.md` §3 |
| S2 | planar-memory tiles | **park** (Bet A) | survives only double-buffered with an off-line writer; cannot serve surprise maps; no CAD. Cost **conditional on the print gate** | `test11_threshold_ratchet_s1/` |
| S3 | multi-row mechanical DMA head | **kill** (Bet A) | sourced analytic printability **FAIL**: pivot 0.80 < 5.0, declared min web 0.24 < 0.88; expected delivered **$2,880.98** driven by **sourced selectors**; **CI-visible** | `tools/validate/analytic_printability.py` on `selector_fanout_coupon.scad` |
| S4 | distributed passive tiles on a shared bus | **park** (Bet A) | printed dog clutch must transmit tile torque and fail open; correlated bus backlash exceeds 0.25 mm at 3°/joint. Cost is **conditional on the print gate**, not a kill | `test11_shared_drive_gate_analysis/` |
| S5 | programmed rotary stops + common lift | **WIN** (Bet B) | only CAD+simulation+sourced-BOM candidate; 26.251 s best corner (400 pps sweep passes 17/108); sourced pair $501.12, reduced $483.37 | this ADR, `test12_winner_convergence/` |

**Cost-disposition correction (Falsifier Finding 2).** S1, S2 and S4 are **not** cost-killed
here. Their working BOMs are inflated by *fallback* lines for parts their designs intend to
print (S1: 64 tile couplers $192 + release combs $32; S4: 64 printed clutches $192), so their
true cost is **undetermined pending the Bet-A print gate**, not failed. This ADR cites no
fallback-inflated BOM as killing evidence.

**Failed ideas are kept as assets**, not deleted: the rejection log in
`test08/README.md:114-150` (unsupported follower, nine-level angular failure, 40-channel
timing failure, thin-core cam buckling) and the S3/S4 selector-coupon findings
(`test11_selector_coupon/`) remain in the search record.

## 3. The winner's contested points, corrected

### 3.1 K1 cam buckling — CONTESTED (re-labelled from "closed")

The revised 1.0 mm cam core gives **4.96 N** ideal critical buckling load, below the **5 N**
abuse screen. The original ADR re-classified the 5 N as a non-gate because the design product
load is **1 N service for 24 h** — which would give a **≈5× margin**. The Falsifier review is
correct that this is only valid if **1 N is a true upper bound** on tabletop vertical load,
and the repository does **not** establish that: no miniature has been measured
(`miniature_measured: false`) and Test08's own text says the 5 N screen expects "a support or
material redesign may be necessary". The 1 N figure is a **stated assumption**.

**Corrected label: K1 = `open` (contestable).** It closes only on a **sourced ≤4.5 N
tabletop-vertical-load bound**. If the true worst case is 5 N, the 4.96 N cam **fails by
0.8 %** and the core must be re-sized. This is the single decisive re-label.

### 3.2 Cost — CORRECTED: the sourced pair is at/over the ceiling

The repository's own additive delivered model is
`parts × (1 + 0.10 ship + 0.06 tax) = parts × 1.16`
(`delivered_3scenario/delivered_cost_model.py`). The Test12 model instead used
`1.10 × 1.06 = 1.166` applied to a fixed subtotal carried from the *expected* scenario.

| Path (additive ×1.16) | Parts | Delivered | vs $500 |
|---|---:|---:|---|
| Sourced BOM expected scenario (CSV) | $510.40 | **$592.06** | over |
| Sourced pair (motor $1.05 best, driver $0.80) | $432.00 | **$501.12** | **over by $1.12** |
| + real net register saving $10.30 + RP2040 $5 | $413.00 | **$483.37** | under |
| *As first published (multiplicative ×1.166)* | *$432.00* | *$503.71* | *defect* |

**Corrected statement:** on the cheapest sourced pairing the winner is **≈$501 (at/over the
$500 ceiling)**; the reduction path lands **≈$483** — a real but *small* margin, **not** the
advertised $18.44. Part of the advertised reduction is **double-counted**: folding 40 ×
74HC595 onto the driver PCB removes a $0.35 expected *allowance* line ($14) but the chips are
still purchased (sourced $0.0925 → $3.70), so the real net saving is **$10.30**. Reaching the
< $400 ideal band is **not** demonstrated. **K5 = `conditional`**, not "closed".

## 4. Consequences

- `08-current-design/` names one machine with a full buildable definition, sourced BOM,
  assembly route and print-ready CAD — but is now explicitly **not print-ready as stated**
  until the corrected killers and cost range are carried.
- The source-of-truth programme risk register is now (corrected):
  1. **K1 — cam buckling:** `open/contestable`; 4.96 N < 5 N abuse screen; closes only on a
     sourced ≤4.5 N tabletop-load bound.
  2. **K2** — printed rotary detent hold/repeat. **Bounded analytically** by
     [DND-38](/DND/issues/DND-38) (`test12_winner_convergence/DETENT_CONTACT.md`): the
     nominal leaf corrects a one-step 18° slip only for a contact friction μ ≤ 0.323, so at
     the sourced PLA–PLA midpoint μ = 0.35 it does not (torque/friction 0.92). It closes
     with a cleaner contact (μ ≤ 0.32) or a scallop deepened to ≥ 0.31 mm. K2 stays on the
     register as a **conditional** item with a quantitative pass rule — it does not kill S5.
  3. **K4 — regional isolation:** `partially closed (structural bound 0.017 mm only)`;
     stiction release + wear drift are measurement-class and the cited rig returns
     `INCONCLUSIVE`.
  4. **K5 — cost:** `conditional`; sourced pair ≈$501 (at/over ceiling); reduced ≈$483.
  5. **K6 — time:** `conditional`; 26.251 s is the best corner of a 540-case sweep; at
     400 pps only 17/108 cases pass, worst 45.07 s.
  6. **K7 — motor-cost cliff:** the only traceable matched 8 mm PM stepper is $40/ea
     (80 × $40 = $3,200, 8× the ceiling); the $1.05 price is an untraced multipack.
  7. **K8 — lateral holding:** the hard stop resists downward load; lateral load is resisted
     only by the detent (~0.0014 mN·m) and the printed bushing.
  8. **K9 — print-tolerance angular margin:** 12.50° nominal falls to 6.50° after a 6°
     seating error; ±0.05 mm tolerance on a 1.5 mm rotor is not propagated.
  9. **K10 — regional-update time:** full 41 mm platen stroke + head home/reference per
     activation; not bounded end to end.
  10. **K11 — printed detent/ratchet cycle life:** creep/fatigue over thousands of writes
      unmodelled (cross-cuts K2).
  11. **Reliability R1** — q ≤ 1.57×10⁻⁶ needed for 99 % map correctness; no per-cell
      feedback; unclosable under [DND-27](/DND/issues/DND-27).
  12. **R2 40 mm travel** — provisional design envelope; no representative miniature measured.
  13. **R3 realised step rate** — timing depends on ≥400 pps loaded, assumed.
  14. **R4 matched motor supply** — the only traceable matched part is $40/ea (see K7).
- **Print-readiness gate:** a printable-board test is justified once **K1, K5 and K7** close
  (all three are analytically/sourcingly attackable under DND-27).
- S1/S2/S4 remain **parked** (their cost is conditional on the Bet-A print gate, not failed).
  S3 is **killed**.
- No sixth variation of the shared-power/passive-memory bet will be invented; if a residual
  risk above proves fatal under analysis, the correct response is a product-requirement
  re-scope escalated to the CEO — not more candidates.

## 5. Honesty statement

Every figure in this ADR is **sourced fact, stated assumption, calculation, simulation, or
CAD** — never physical validation. **No printed or measured shape-display evidence exists,
and under [DND-27](/DND/issues/DND-27) none will be produced.** The 40 mm travel, the
sub-$1.05 motor price, the 400 pps loaded rate, the per-cell error rate, the 1 N service
load and the printed detent behaviour are **assumptions**, named as such, that analysis
cannot retire. Following the Falsifier promotion review ([DND-36](/DND/issues/DND-36)), the
killer list no longer presents any contestable or measurement-only item as
"closed-analytically".
