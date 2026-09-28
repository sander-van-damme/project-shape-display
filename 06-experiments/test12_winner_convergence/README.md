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

| # | Candidate | Disposition | Binding evidence |
|---|---|---|---|
| S1 | threshold ratchet + broadcast lift | **kill** | worst-case all-armed stroke **2368 N > 1500 N** cap; mask write needs ≥500 channels |
| S2 | planar-memory tiles | **park** | survives only double-buffered with an off-line writer; no surprise-map path; cost **conditional on the print gate** |
| S3 | multi-row mechanical DMA | **kill** | sourced selectors drive delivered **$2880.98** (5.8× ceiling); fan-out fit gate is a separate [DND-4](/DND/issues/DND-4) question |
| S4 | shared-bus tiles | **park** | printed dog clutch must carry tile torque; bus backlash fails 0.25 mm at 3°/joint; cost **conditional on the print gate** |
| **S5** | **programmed rotary stops + common lift** | **WIN (direction)** | only CAD + simulation + sourced-BOM candidate; 26.251 s best-corner (**conditional**); sourced cost **$501.12** (at/over ceiling), reduced **$483.37**; K1 open, K4 partially-closed |

Two bets, not one (Falsifier): S1–S4 are **Bet A** (written passive memory); S5 is **Bet B**
(absolute geometric stops — a homed rotor + gravity-following toe, no written bit). A Bet-A
failure does not imply a Bet-B failure. S1/S2/S4 cost is **conditional on the print gate**,
not a kill. The readiness labels below were corrected by [DND-41](/DND/issues/DND-41) to match
the Falsifier review.

## 2. End-to-end stack-up (winner)

### Time — CONDITIONAL (best corner)

| Item | Value | Gate |
|---|---:|---|
| Full adversarial map, 400 pps | **26.251 s** | < 30.0 s |
| Sweep cases passing 30 s at 400 pps | **17 / 108** | — |
| Worst sweep case at 400 pps | **45.07 s** | fails |
| 40-channel head @ 800 pps | 39.72 s | fails (why the head is 80-channel) |

26.251 s is the **best corner** of the repo's 540-case `timing_sweep.csv`
(`inspection_s=0`, 25 ms couple, 15 ms settle). This is **calculated**, not measured; no
measured ≥400 pps loaded rate exists. The prior "3.749 s margin" is **withdrawn**.

### Cost — CONDITIONAL range (at/just over the ceiling)

The motor + driver channel is the only cost cliff. Sourced pairing (2026-09-28), repo
**additive** delivered basis (×1.16):

| Path | Parts subtotal | Delivered (×1.16) | vs $500 |
|---|---:|---:|---|
| Sourced motor $1.05 + TB6612 $0.80, unchanged fixed | $432.00 | **$501.12** | **over by $1.12** |
| − net register saving $10.30 (chips still bought at $0.0925) | $421.70 | **$489.17** | −$10.83 |
| − sourced RP2040 controller $5 | $416.70 | **$483.37** | **−$16.63** |

**Correction ([DND-41](/DND/issues/DND-41)):** the prior table printed $434.20 / $503.71 using
a multiplicative `1.10 × 1.06 = 1.166` uplift and a subtotal that does not reproduce; the
repo's own `delivered_3scenario` grid prints this exact cell as **$501.12** ($432.00 × 1.16).
The honest headline is a **range at/just over the ceiling**, clearing only on the reduced path
by a small margin. Reaching the <$400 ideal band is **not** demonstrated.

### Reliability — OPEN (assumption, not measurement)

- At q = 1×10⁻⁴ per cell, **P(all 6,400 correct) = 52.7 %**.
- To reach 99 % whole-map correctness requires q ≤ **1.57×10⁻⁶**.
- No per-cell feedback exists; q is an assumption and no counted coupon can be built
  under DND-27. This is a **permanent residual risk**, stated, not hidden.

### Regional isolation — PARTIALLY-CLOSED (structural sub-bound only)

The J2 rail-coupled neighbour bound is **0.017 mm** against a **0.10 mm** gate — but that is
only a **rail-bending structural** sub-bound. The J2 engine itself returns **INCONCLUSIVE**
(`test11_falsification_library/analytic`): rig noise, stiction release force and cumulative
wear drift are measurement-only. The 0.10 mm gate is a design assumption.

### Travel — PASS (design envelope)

40 mm travel, 5 levels → **10.0 mm** increment. The 40 mm figure is a **provisional
envelope**: no representative miniature has been measured (`miniature_measured: false`).

## 3. Killer list + cheapest falsification

| id | Risk | Status | Result vs gate |
|---|---|---|---|
| K1 | cam buckling under handling load | **open** | 4.96 N critical **< 5 N** Test08 measurement-protocol screen; the 1 N service load is **unsourced**. Close with a sourced ≤ 4.5 N tabletop-load bound, else re-size the core. ([DND-41](/DND/issues/DND-41)) |
| K2 | printed rotary detent holds/repeats after a slipped step | **conditional** | Analytic contact sweep ([DETENT_CONTACT.md](DETENT_CONTACT.md), [DND-38](/DND/issues/DND-38)): nominal leaf does not correct an 18° slip at the sourced PLA–PLA friction midpoint (torque/friction = 0.92); closes only for μ ≤ 0.323 or a deepened scallop (≥ 0.31 mm). Does not kill S5. |
| K3 | gravity return vs guide friction | **closed-analytically** | 20.29 mN weight vs 5 mN assumed drag = 4.06×; 15.29 mN headroom (solid column). |
| K4 | regional update disturbs a loaded neighbour | **partially-closed** | 0.017 mm is a rail-bending *structural* sub-bound vs a 0.10 mm gate; the J2 engine returns **INCONCLUSIVE** — release/drift are measurement-only. |
| K5 | purchased cost > $500 delivered | **conditional (range)** | $501.12 sourced (over ceiling); **$483.37** reduced; real but small margin. |
| K6 | full-map time > 30 s at realised step rate | **conditional** | 26.25 s best corner; only **17/108** sweep cases pass at 400 pps, worst **45.07 s**; needs a measured ≥400 pps loaded rate. |
| K7 | purchased-actuator cost cliff (80 motors + 80 drivers) | **open** | only traceable matched 8 mm PM stepper is **$40/ea** (→ $3,200); sub-$1.05 part untraced. |
| K8 | lateral holding (knocked miniature) | **open** | hard stop resists downward load only; detent restoring torque ≈ **0.00139 mN·m**; no analytic pass. |
| K9 | angular margin vs print tolerance | **open** | 5 levels: 12.50° nominal → **6.50°** after a 6° seating error; ±0.05 mm print tolerance not propagated. |
| K10 | regional-update time untested end to end | **open** | homing + full 41 mm platen stroke not bounded. |
| K11 | cycle life of printed detent/ratchet | **open** | single-cycle static model; creep/fatigue unmodelled. |
| K12 | coarse-slope / multi-level usability | **open** | 10 mm steps may be too coarse; product decision. |

**Cheapest falsification for K2 (now run):** the analytic contact/sensitivity sweep of the
detent interface over a sourced PLA contact-friction range is complete —
[DETENT_CONTACT.md](DETENT_CONTACT.md), `detent_contact.py`, `detent_checks.py`, CI-gated.
It reproduces the Test09 restoring-torque anchor (0.00298 mN·m) and shows the nominal leaf
corrects a one-step slip only if the printed contact friction is **μ ≤ 0.323** (sourced
range 0.2–0.5, midpoint 0.35 does not). Closing levers: a cleaner contact or a scallop
deepened to **≥ 0.31 mm**. This does not kill the architecture; it bounds K2 with a
quantitative rule and keeps it on the risk register, because the as-printed μ/creep cannot
be measured under [DND-27](/DND/issues/DND-27).

## 4. What this does and does not claim

- **Does:** converge the field to one machine on recorded evidence; show its time and cost
  stack-ups close with margin; state exactly which risks remain.
- **Does not:** claim measured performance, a printed unit, a qualified motor supply, or a
  verified 40 mm miniature requirement. The residual risks in §3 (K2) and §2 (reliability)
  are stated, not retired.
