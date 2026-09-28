# Test 12 — Winner convergence stack-up (DND-35)

> **Readiness status (DND-46 / DND-48):** the DND-44 closure headlines for K1/K5/K8 were
> **broken** by the adversarial audit (`FALSIFIER_AUDIT.md`) and the robust figures are folded
> into [`08-current-design/README.md` §7/§9](../../08-current-design/README.md). Robust planning
> numbers: **cost $482.95** (not $424.95), **service buckling 0.39–3.27 N/column**, **lateral
> gate exceeded at the 40 mm extension** (0.356 mm at 1 N), **time conditional on a loaded dwell
> AND a ≥268 pps loaded rate**, **cycle life ">=1e6, order unknown"**. Treat the DND-44/41
> paragraphs below as history.

**Question.** After five parallel hypotheses (S1–S5), converge on **one** buildable
machine and produce its end-to-end stack-up: full-map time, purchased cost, per-cell
reliability, regional-update isolation and travel — with the killing evidence for every
dropped candidate.

**Answer.** The winner is **S5 — programmed stepped rotary stops + common lift**. It is the
only candidate that simultaneously has (a) real solid CAD of the mechanism, (b) an
independently reproduced timing model under the 30 s cap, and (c) a purchased BOM that is
82 % sourced. Its one true blocker, purchased cost, is **$482.95 on the defensible planning
basis** (DND-48; **$17.05 under** the $500 ceiling, conditional on a motor ≤$1.86 — see the
banner above), and the §7 register below is the authoritative status.

**Evidence class.** CALCULATION / SIMULATION over sourced listings and stated
assumptions. **Nothing here is a print and nothing here is a physical measurement**
([DND-27](/DND/issues/DND-27)).

Run:

```text
python 06-experiments/test12_winner_convergence/model.py     # prints the full stack-up
python 06-experiments/test12_winner_convergence/checks.py    # regression + honesty gates
```

DND-45 analytic addenda (K2 named geometry, K9 tolerance stack-up):

```text
cd 06-experiments/test12_winner_convergence
python detent_contact.py && python detent_checks.py   # K2 scallop sweep
python k9_angular_margin.py && python k9_checks.py    # K9 Monte-Carlo
```

DND-49 K7 matched-motor sourcing trace:

```text
cd 06-experiments/test12_winner_convergence
python k7_motor_trace.py && python k7_motor_trace_checks.py   # K7 sourcing
```

Sourcing detail: [`../test11_cost_printability_reliability/sourcing_notes.md`](../test11_cost_printability_reliability/sourcing_notes.md) §8.


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
not a kill: their working BOMs carry **$192–$224 of fallback purchase** for parts the designs
intend to print (S1: 64 tile couplers $192 + release combs $32; S4: 64 printed clutches $192),
so their cost is **undetermined pending the Bet-A print gate** — stated for symmetry with S5's
own cost range. The readiness labels below were corrected by [DND-41](/DND/issues/DND-41) to
match the Falsifier review.

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
| K1 | cam buckling under handling load | **open (service load, DND-46)** | 4.96 N core **< 5 N** abuse screen. Service load is **0.39–3.27 N/column** depending on base contact; the rigid tripod case (3.27 N) is bounding and leaves only **~1.5×** margin — size the core against **~3.3 N**. Localized 5 N abuse bounded only by a 1.10 mm core re-size. |
| K2 | printed rotary detent holds/repeats after a slipped step | **closed-analytically (named geometry)** | Analytic contact sweep ([DETENT_CONTACT.md](DETENT_CONTACT.md), [DND-38](/DND/issues/DND-38), [DND-45](/DND/issues/DND-45)): the nominal 0.20 mm scallop fails at the sourced PLA–PLA midpoint (0.92). A **0.40 mm scallop** gives torque/friction **1.84 at μ = 0.35** and **1.29 at μ = 0.50**, inside the **0.50 mm** cam envelope; exact min depth for a 1.25 margin at μ = 0.35 is 0.271 mm. As-printed μ/creep/tip sharpness remain measurement-only. Does not kill S5. |
| K3 | gravity return vs guide friction | **closed-analytically** | 20.29 mN weight vs 5 mN assumed drag = 4.06×; 15.29 mN headroom (solid column). |
| K4 | regional update disturbs a loaded neighbour | **partially-closed** | 0.017 mm is a rail-bending *structural* sub-bound vs a 0.10 mm gate; the J2 engine returns **INCONCLUSIVE** — release/drift are measurement-only. |
| K5 | purchased cost > $500 delivered | **conditional (robust $482.95)** | [DND-48](/DND/issues/DND-48): defensible planning basis **$482.95 delivered ($17.05 margin)** (spares + E6 restored); sourced-DRV8833 variant **$474.91**; expected-motor case **$501.51 (over)**. The old $424.95 needed four simultaneous best-case choices. Conditional on a motor ≤**$1.86** (see K7). |
| K6 | full-map time > 30 s at realised step rate | **conditional (DND-46)** | 26.251 s at the design point; floor **18.65 s**; conditional on a loaded engage/settle **dwell** AND a **≥268 pps (~804 rpm)** loaded rate, with `inspection_s = 0` assumed. The 45.07 s corner is not rate-recoverable. |
| K7 | purchased-actuator cost cliff (80 motors + 80 drivers) | **refuted at ≤$1.86 (sourced), residual (DND-49)** | [DND-49](/DND/issues/DND-49) `k7_motor_trace.py`: cheapest *matched, orderable* 8 mm 18° bipolar PM stepper is CCHT **$11.20 @100 / $8.20 @3,001+** → **$1,088–$1,367 delivered**; MOONS 8PM020S1 $40 → $4,040. The $1.05 multipack clears but has **no published step angle**. Reduced-head lever **fails the 30 s budget** (40 ch → ~104 s). |
| K8 | lateral holding (knocked miniature) | **open (DND-46)** | at the repo's own 40 mm free length, 1 N → **0.356 mm** (3.5× the 0.10 mm gate) and the 0.10 mm-gate load is **0.28 N**. Gate is a free-length/guide-capture question (12 vs 40 mm). |
| K9 | angular margin vs print tolerance | **closed-analytically** | Monte-Carlo propagation of the sourced ±0.05 mm FDM positional tolerance through the toe/sector geometry ([K9_ANGULAR_MARGIN.md](K9_ANGULAR_MARGIN.md), [DND-45](/DND/issues/DND-45)): 5 levels keep margin positive (0% fail, worst draw **1.72°**, mean 5.52°) under the bounded tolerance reading, but a Gaussian tail gives 1.31% fail; **6 levels fail 65.6%**; **4 levels is robust (0% everywhere)**. The K12 level-count tradeoff now carries a hard margin bound. |
| K10 | regional-update time untested end to end | **open** | homing + full 41 mm platen stroke not bounded. |
| K11 | cycle life of printed detent/ratchet | **open** | single-cycle static model; creep/fatigue unmodelled. |
| K12 | coarse-slope / multi-level usability | **open** | 10 mm steps may be too coarse; product decision. |

**Cheapest falsification for K2 (now run):** the analytic contact/sensitivity sweep of the
detent interface over a sourced PLA contact-friction range is complete —
[DETENT_CONTACT.md](DETENT_CONTACT.md), `detent_contact.py`, `detent_checks.py`, CI-gated.
It reproduces the Test09 restoring-torque anchor (0.00298 mN·m) and shows the nominal leaf
corrects a one-step slip only if the printed contact friction is **μ ≤ 0.323** (sourced
range 0.2–0.5, midpoint 0.35 does not). **[DND-45](/DND/issues/DND-45)** extends the sweep
over scallop depth: the exact minimum depth for a 1.25 margin at μ = 0.35 is **0.271 mm**,
and the **chosen 0.40 mm scallop** (inside the 0.50 mm cam envelope) gives **1.84 at
μ = 0.35** and **1.29 at μ = 0.50** — so K2 is closed by a named geometry at the sourced
friction, with the as-printed μ/creep/tip sharpness the only unretired terms.

## 4. What this does and does not claim

- **Does:** converge the field to one machine on recorded evidence; show its time and cost
  stack-ups close with margin; state exactly which risks remain.
- **Does not:** claim measured performance, a printed unit, a qualified motor supply, or a
  verified 40 mm miniature requirement. The residual risks in §3 (K2) and §2 (reliability)
  are stated, not retired.
