# Test 12 — Winner convergence stack-up (DND-35)

**Question.** After five parallel hypotheses (S1–S5), converge on **one** buildable
machine and produce its end-to-end stack-up: full-map time, purchased cost, per-cell
reliability, regional-update isolation and travel — with the killing evidence for every
dropped candidate.

**Answer.** The winner is **S5 — programmed stepped rotary stops + common lift**. It is the
only candidate that simultaneously has (a) real solid CAD of the mechanism, (b) an
independently reproduced timing model under the 30 s cap, and (c) a purchased BOM that is
82 % sourced. Its one true blocker, purchased cost, clears the **$500** ceiling with margin
under the sourced-pair-plus-consolidation path below.

**Evidence class.** CALCULATION / SIMULATION over sourced listings and stated
assumptions. **Nothing here is a print and nothing here is a physical measurement**
([DND-27](/DND/issues/DND-27)).

Run:

```text
python 06-experiments/test12_winner_convergence/model.py     # prints the full stack-up
python 06-experiments/test12_winner_convergence/checks.py    # regression + honesty gates
```

## 1. The decision

Two bets, not one (adopting the Falsifier audit, [DND-36](/DND/issues/DND-36)): **Bet A** is a
*written* passive memory set by a shared writer (S1–S4); **Bet B** is S5's *absolute geometric
stops* (a homed rotor + gravity-following toe, no written bit). A Bet-A failure does not imply a
Bet-B failure, so S5 is chosen on its own evidence.

| # | Candidate | Disposition | Binding evidence |
|---|---|---|---|
| S1 | threshold ratchet + broadcast lift | **kill** (Bet A) | worst-case all-armed stroke **2368 N > 1500 N** cap; mask write needs ≥500 channels |
| S2 | planar-memory tiles | **park** (Bet A) | survives only double-buffered with an off-line writer; no surprise-map path. Cost **conditional on the print gate** |
| S3 | multi-row mechanical DMA | **kill** (Bet A) | sourced analytic printability **FAIL** (pivot 0.80 < 5.0; declared min web 0.24 < 0.88); delivered **$2880.98** (sourced selectors); CI-visible |
| S4 | shared-bus tiles | **park** (Bet A) | printed dog clutch must carry tile torque; bus backlash fails 0.25 mm at 3°/joint. Cost **conditional on the print gate** |
| **S5** | **programmed rotary stops + common lift** | **WIN** (Bet B) | only CAD + simulation + sourced-BOM candidate; 26.251 s; sourced cost path **$503.71**, reduced **$481.56** |

S1/S2/S4 cost is **not** cited as killing evidence: their BOMs are inflated by fallback lines
for parts their designs intend to print (Falsifier Finding 2). S3's cost is driven by *sourced*
selectors and remains a genuine kill.

## 2. End-to-end stack-up (winner)

### Time — PASS

| Item | Value | Gate |
|---|---:|---|
| Full adversarial map, 400 pps | **26.251 s** | < 30.0 s |
| Margin to hard cap | 3.749 s | — |
| Margin to 27 s internal target | 0.749 s | — |
| 40-channel head @ 800 pps | 39.72 s | fails (why the head is 80-channel) |

Time is the Test09-reproduced value (`test09.../results/summary.json:16`) and is
**calculated**, not measured. At 200 pps the schedule fails 30 s; the design depends on a
realised ≥400 pps loaded step rate.

### Cost — PASS on the reduction path

The motor + driver channel is the only cost cliff. Sourced pairing (2026-09-28):

| Path | Parts subtotal | Delivered (×1.16) | vs $500 |
|---|---:|---:|---|
| Sourced motor $1.05 + TB6612 $0.80, unchanged fixed | $434.20 | **$503.71** | +$3.71 (on the ceiling) |
| + fold 40 discrete shift registers onto the driver PCB (−$14) | $420.20 | **$487.46** | **−$12.54** |
| + sourced RP2040 controller (−$5) | $415.20 | **$481.56** | **−$18.44** |

Fixed subtotal **$284.00** is reproduced directly from
`bom_S5_delivered.csv` (expected scenario) by `checks.py`, so the model cannot drift from
the sourced BOM. Reaching the <$400 ideal band is **not** demonstrated; the winner lands
in the project's "acceptable" band with margin.

### Reliability — OPEN (assumption, not measurement)

- At q = 1×10⁻⁴ per cell, **P(all 6,400 correct) = 52.7 %**.
- To reach 99 % whole-map correctness requires q ≤ **1.57×10⁻⁶**.
- No per-cell feedback exists; q is an assumption and no counted coupon can be built
  under DND-27. This is a **permanent residual risk**, stated, not hidden.

### Regional isolation — PASS (analytic bound)

The J2 rail-coupled neighbour bound is **0.017 mm** against a **0.10 mm** gate. Stiction
(0.18–2.84 N) dominates rail shear, so the isolation concept is analytically sound. The
0.10 mm gate itself is a design assumption, not a measured disturbance limit.

### Travel — PASS (design envelope)

40 mm travel, 5 levels → **10.0 mm** increment. The 40 mm figure is a **provisional
envelope**: no representative miniature has been measured (`miniature_measured: false`).

## 3. Killer list + cheapest falsification

| id | Risk | Status | Result vs gate |
|---|---|---|---|
| K1 | cam buckling under handling/abuse load | **closed-analytically** | 4.96 N critical vs **1 N service** (≈5× margin). The 5 N figure is a *sacrificial handling screen*, explicitly "not a whole-hand safety certification" (`test08/README.md:263`), and is retained as a coupon handling test, not a design gate. |
| K2 | printed rotary detent holds/repeats after a slipped step | **qualitative** | No closed form; printed contact/creep. Permanently qualitative under DND-27. |
| K3 | gravity return vs guide friction | **closed-analytically** | 20.29 mN weight vs 5 mN assumed drag = 4.06×; 15.29 mN headroom (solid column). |
| K4 | regional update disturbs a loaded neighbour | **closed-analytically** | 0.017 mm vs 0.10 mm gate. |
| K5 | purchased cost > $500 delivered | **closed-analytically** | $503.71 sourced; **$481.56** reduced. |
| K6 | full-map time > 30 s at realised step rate | **closed-analytically** | 26.25 s vs 30 s at 400 pps. |

**Cheapest falsification for the one quantitative residual (K2):** an analytic
contact/sensitivity sweep of the detent interface over a sourced PLA contact-friction
range, reporting the toggle/release force window and its sensitivity to ±0.05 mm print
tolerance. If the window closes, the winner needs a spring detent (costs, but does not
kill the architecture). This can be done entirely in the existing harness.

## 4. What this does and does not claim

- **Does:** converge the field to one machine on recorded evidence; show its time and cost
  stack-ups close with margin; state exactly which risks remain.
- **Does not:** claim measured performance, a printed unit, a qualified motor supply, or a
  verified 40 mm miniature requirement. The residual risks in §3 (K2) and §2 (reliability)
  are stated, not retired.
