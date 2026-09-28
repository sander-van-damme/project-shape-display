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

Two bets, not one (Falsifier audit, [DND-36](/DND/issues/DND-36)): **Bet A** is a *written*
passive memory set by a shared writer (S1–S4); **Bet B** is S5's *absolute geometric stops*
(a homed rotor + gravity-following toe, no written bit). A Bet-A failure does not imply a
Bet-B failure, so S5 is chosen on its own evidence.

| # | Candidate | Disposition | Binding evidence |
|---|---|---|---|
| S1 | threshold ratchet + broadcast lift | **kill** (Bet A) | worst-case all-armed stroke **2368 N > 1500 N** cap; mask write needs ≥500 channels |
| S2 | planar-memory tiles | **park** (Bet A) | survives only double-buffered with an off-line writer; no surprise-map path. Cost **conditional on the print gate** |
| S3 | multi-row mechanical DMA | **kill** (Bet A) | sourced analytic printability **FAIL** (pivot 0.80 < 5.0; declared min web 0.24 < 0.88); delivered **$2880.98** (sourced selectors); CI-visible |
| S4 | shared-bus tiles | **park** (Bet A) | printed dog clutch must carry tile torque; bus backlash fails 0.25 mm at 3°/joint. Cost **conditional on the print gate** |
| **S5** | **programmed rotary stops + common lift** | **WIN** (Bet B) | only CAD + simulation + sourced-BOM candidate; 26.251 s best corner (400 pps sweep passes 17/108); sourced pair **$501.12** (at/over ceiling), reduced **$483.37** |

S1/S2/S4 cost is **not** cited as killing evidence: their BOMs are inflated by fallback lines
for parts their designs intend to print (Falsifier Finding 2). S3's cost is driven by *sourced*
selectors and remains a genuine kill.

## 2. End-to-end stack-up (winner)

> **Correction (Falsifier promotion review, [DND-36](/DND/issues/DND-36)).** The first pass of
> this stack-up presented three contestable killers as `closed-analytically` and a cost figure
> built on a *multiplicative* uplift. Both are corrected below. **S5 survives as the direction;
> the promotion as originally stated is retracted.** S5 is **not** print-ready as stated.

### Time — CONDITIONAL

| Item | Value | Gate |
|---|---:|---|
| Full adversarial map, best corner, 400 pps | **26.251 s** | < 30.0 s |
| Best-corner margin to hard cap | 3.749 s | — |
| 400 pps sweep (`timing_sweep.csv`) | **17/108 cases < 30 s** | worst 45.07 s |

Time is the Test09-reproduced value (`test09.../results/summary.json:16`) and is
**calculated**, not measured. **K6 is conditional:** 26.251 s is the best corner of a
540-case sweep; at the design rate of 400 pps only **17/108** cases pass and the worst case
is **45.07 s**. A realised **≥400 pps loaded** step rate is required and is unmeasured.

### Cost — CONDITIONAL: the sourced pair is at/over the ceiling

Corrected to the repository's own **additive** delivered model
(`delivered_cost_model.py`: `parts × (1 + 0.10 ship + 0.06 tax) = parts × 1.16`):

| Path (additive ×1.16) | Parts | Delivered | vs $500 |
|---|---:|---:|---|
| Sourced BOM expected scenario (CSV) | $510.40 | **$592.06** | over |
| Sourced pair (motor $1.05 best, driver $0.80) | $432.00 | **$501.12** | **over by $1.12** |
| + real net register saving $10.30 + RP2040 $5 | $413.00 | **$483.37** | under |
| *As first published (multiplicative ×1.166)* | *$432.00* | *$503.71* | *defect* |

The original `DELIVERED_UPLIFT = 1.10 × 1.06` was inconsistent with the repo's additive
model, and the advertised −$14 register saving was **double-counted** (the 74HC595s are still
purchased; sourced $0.0925 → $3.70 for 40, so the real net saving is **$10.30**). Fixed
subtotal **$284.00** is still reproduced from `bom_S5_delivered.csv` by `checks.py`.
**K5 is conditional:** the cheapest sourced pair is **at/over $500**; only the reduced path
clears, with a **small** real margin. Reaching the <$400 ideal band is **not** demonstrated.

### Reliability — OPEN (assumption, not measurement)

- At q = 1×10⁻⁴ per cell, **P(all 6,400 correct) = 52.7 %**.
- To reach 99 % whole-map correctness requires q ≤ **1.57×10⁻⁶**.
- No per-cell feedback exists; q is an assumption and no counted coupon can be built
  under DND-27. This is a **permanent residual risk**, stated, not hidden.

### Regional isolation — PARTIALLY CLOSED (structural bound only)

The J2 rail-coupled neighbour bound is **0.017 mm** against a **0.10 mm** gate, but that is a
**structural sub-bound**. The cited rig (`isolation_rig_runner.py`) returns **INCONCLUSIVE**:
stiction release and cumulative wear drift are **measurement-class** terms, not analytically
derivable. K4 is **not** closed.

### Travel — PASS (design envelope)

40 mm travel, 5 levels → **10.0 mm** increment. The 40 mm figure is a **provisional
envelope**: no representative miniature has been measured (`miniature_measured: false`).

## 3. Killer list + cheapest falsification (corrected)

| id | Risk | Status | Result vs gate |
|---|---|---|---|
| K1 | cam buckling under handling/abuse load | **open/contestable** | 4.96 N critical **< 5 N abuse screen (fails by 0.8 %)**. The 1 N service load is an **unsourced assumption** (`miniature_measured:false`); closes only on a sourced ≤4.5 N tabletop-load bound. |
| K2 | printed rotary detent holds/repeats after a slipped step | **conditional** | Analytic contact sweep ([DETENT_CONTACT.md](DETENT_CONTACT.md), [DND-38](/DND/issues/DND-38)): nominal leaf does not correct an 18° slip at the sourced PLA–PLA friction midpoint (torque/friction = 0.92); closes only for μ ≤ 0.323 or a deepened scallop (≥ 0.31 mm). Does not kill S5. |
| K3 | gravity return vs guide friction | **closed-analytically** | 20.29 mN weight vs 5 mN assumed drag = 4.06×; 15.29 mN headroom (solid column). |
| K4 | regional update disturbs a loaded neighbour | **partially-closed (structural only)** | 0.017 mm rail sub-bound vs 0.10 mm gate; cited rig returns `INCONCLUSIVE`; stiction release + drift are measurement-class. |
| K5 | purchased cost > $500 delivered | **conditional** | Additive: sourced pair **$501.12** (at/over ceiling); reduced **$483.37**. |
| K6 | full-map time > 30 s at realised step rate | **conditional** | Best corner 26.25 s; at 400 pps only **17/108** sweep cases pass, worst 45.07 s. |
| K7 | motor-cost cliff (80 motors + 80 drivers) | **open** | Only traceable matched 8 mm PM stepper is **$40/ea → $3,200** (8× ceiling); $1.05 is an untraced multipack. |
| K8 | lateral holding of a knocked miniature | **open** | Hard stop resists downward load; lateral load resisted only by the detent (~0.0014 mN·m) + printed bushing. |
| K9 | angular margin vs print tolerance | **open** | 12.50° nominal margin → 6.50° after a 6° seating error; ±0.05 mm tolerance on a 1.5 mm rotor not propagated. |
| K10 | regional-update time not bounded end to end | **open** | Any write needs a full 41 mm platen stroke + head home/reference; regional time unbounded. |
| K11 | printed detent/ratchet cycle life | **open** | Single-cycle static model; creep/fatigue of the 0.45 mm leaf over thousands of writes unmodelled. |

**Cheapest falsifications (all analytic, no print):** (1) source the max tabletop vertical +
lateral load → closes K1/K8; (2) re-run the additive cost model → confirms K5; (3) count
`under_30` at 400 pps in `timing_sweep.csv` → confirms K6; (4) run
`isolation_rig_runner.py` → confirms K4 as `INCONCLUSIVE`; (5) Monte-Carlo angular error from
±0.05 mm print tolerance → bounds K9; (6) buckling check at 5 N → confirms K1.

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
