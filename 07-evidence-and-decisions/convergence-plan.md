# DND-2 Convergence Plan (CTO)

Companion decision record: [`convergence-decision-2026-09.md`](convergence-decision-2026-09.md) (ADR-001).


**Owner:** CTO. **Status:** active. **Supersedes:** the open-ended candidate list in
[`04-architecture-candidates/`](../04-architecture-candidates/README.md), which is preserved as the
search record rather than a commitment. **Policy:** all gates are analytic/simulation/CAD — no
physical print tests ([DND-27](/DND/issues/DND-27)); agents merge their own reviewed PRs
([DND-19](/DND/issues/DND-19)).

This document ranks the *quickest tests that can kill a survivor* and states which candidate each
test would kill. The goal is convergence on one or a small number of serious architectures; it is
deliberately not another survey.

## 1. The binding programme constraint

The product target is a strict conjunction: **80×80 cells, 5.08 mm pitch, ≥40 mm travel,
<30 s full-map ready, regional updates, <$500 purchased parts, repeated reuse.** Every survivor is
currently rejected or unsupported on at least one conjunct:

| Gate | Current state of the whole field |
|---|---|
| Timing | Conditional analytical passes exist (S5 26.25 s; S3/S4 shared rows 21–27 s). All are unrealized estimates, not measured, and now cannot be measured (DND-27). |
| Cost | The best-defended BOMs are **$432 / $518.40 with contingency** (S5) and **$447–$1,086** (S3/S4). No architecture has a *matched delivered* BOM under $500. |
| Pitch / printability | No full-pitch cell mechanism has been printed. Fit is judged against *sourced* FDM process limits plus CAD/mesh stack-ups; 0.20 mm walls, 5.08 mm gates and 0.05 mm effective gaps remain nominal assumptions. |
| Load support | Best analytical cam screen is 4.96 N ideal against a 5 N abuse gate; no measured 1 N service hold is possible. |
| Regional isolation | Architecturally plausible in S2/S4; bounded analytically (beam/stiction) but no measured disturbance limit exists (Q5). |
| Reliability | At 0.01 % per-cell error, P(all 6400 correct) ≈ 52.7 %. No per-cell feedback in any cost model; no counted coupon possible. |

**Therefore no survivor can be promoted to [`08-current-design/`](../08-current-design/README.md)
on present evidence.** Promotion requires a survivor to pass its named **analytic/simulation/CAD**
gate below, at final pitch where the gate is about density. Under board directive
[DND-27](/DND/issues/DND-27) no physical gate is available, so promotion also requires the residual
qualitative risks in §3.2 to be explicitly accepted by the board.

## 2. What actually changed in this cycle

The field narrowed for *calculated* reasons, not for interest:

1. **Per-cell bought actuation is dead.** 6400 selectors at even $0.50 is $3,200 (Test10). This kills
   the direct-drive families at this count.
2. **Cell-serial visible writing is dead.** A serial writer needs >213 completed cells/s before
   overhead; the modelled single writer takes ~76 min. This kills the one-XYZ-writer family.
3. **What survives is shared power + passive printed memory + tile/row isolation.** S1–S4 all have
   this shape; S5 is a travelling programmer over passive printed rotors.

The survivors are therefore **not** five unrelated ideas. They are variations on one bet:

> **Bet:** *a passive, printable, final-pitch state or selection element can be written by a small,
> shared, moderately-parallel programmer and can hold terrain load without powered holding.*

If that bet fails, the entire surviving field fails, and the correct response is to reduce the
product requirement (tile resolution, level count, or the <30 s/`<`$500 conjunction) rather than to
search for a sixth variation of the same bet. This is the most important single sentence in this
plan: **test the bet before adding candidates.**

## 3. Elimination order (cheapest informative *analytic* test first)

Each step is a gate: a fail kills the named candidates and stops dependent spend. A pass only
authorises the next step. Steps 0–3 together are the critical path; steps 4–6 run in parallel behind
them. **Every gate below is executable without printing or measuring** — as a calculation,
simulation, or CAD/mesh check — per [DND-27](/DND/issues/DND-27).

| # | Test | Evidence level | Kills on failure | Cost | Where |
| ---:|---|---|---|---|---|
| 0 | **Isolation disturbance bound** (Q5): analytic beam/FEA coupling model (clamped/simply-supported rail) + Coulomb-stiction bound between adjacent loaded full-pitch tiles; existing `check_fixture.py` mesh gate. | SIMULATION / CALCULATION | It does not kill a candidate directly; it supplies the shared **disturbance baseline** every other test is judged against. Without it, S2/S4 isolation claims cannot be compared. | Modelling | Falsifier / [DND-5](/DND/issues/DND-5) |
| 1 | **Passive pitch/backlash capability, final pitch.** CAD/mesh validation of the final-pitch geometry against *sourced* FDM process limits (min wall, min slot, overhang, clearance) + worst-case and Monte Carlo tolerance/interference stack-up. | CAD + CALCULATION | Any survivor whose mechanism needs a fit, web, gate or detent outside the sourced process envelope. This is the *cheapest* global kill. | Modelling | CostMfg / [DND-6](/DND/issues/DND-6) |
| 2 | **Passive memory-cell capability.** Force/kinematics model of one final-pitch element: hold force, toggle force, vibration-release threshold, cycle-life bound, with a tolerance stack-up on the detent/ratchet interface. | CALCULATION / SIMULATION | **S5** (if the detent cannot correct a slipped step), **S1** (if the ratchet/gate cannot hold or repeat), **S4** (if the local memory does not exist) — and the whole shared-power/passive-memory bet above. | Modelling | Inventors + Falsifier |
| 3 | **Isolation of a 2×2 tile arrangement**, simulation with representative load: regional reset of one tile while its neighbour carries a modelled miniature mass; report coupling and jam propagation. | SIMULATION | **S2** (registration seizes the follower) and **S4** (coupling/jam propagates) — the two architectures that depend on tile isolation. | Modelling | InventorAlpha/Beta |
| 4 | **Selector / register fan-out** (Q3/Q4), analytic gate (DND-28): one common stroke selectively engages 2×4 outputs at final pitch without neighbour release; use the `t11a_fit_check.py` engine on the analytic run record. | CALCULATION | **S1** (threshold gates), **S3** (fan-out register), **S4** (tile clutch). | Modelling | InventorBeta + Falsifier |
| 5 | **Writer path** (Q2), modelled timing: complete receive→write→install→register→settle for one tile in a kinematic/timing model. | CALCULATION / SIMULATION | **S2** for surprise reveals; bounds S1's mask install. | Script | InventorAlpha |
| 6 | **Load, structure and power:** spliced full-span beam model + dummy platen at modelled column mass; lift torque-speed margin, flatness, power-cut behaviour. | CALCULATION / SIMULATION | Any survivor whose lift/structure cannot maintain the unload gap or hold position on power loss. | Modelling | InventorBeta / CostMfg |

### 3.1 Closed analytically (was a physical coupon)

The former physical steps are now sharpened such that each was taken as far as analysis allows in
the DND-28 re-scope. The strongest analytic result so far is the J2 rail-coupled neighbour bound:
**0.017 mm max (20×20) vs the 0.10 mm gate**, with stiction (0.18–2.84 N) dominating rail shear —
so the isolation *concept* is analytically sound. The S3 selector fan-out likewise yields a min-web
worst-case margin of **+0.11 mm** (thin but positive) and an **unresolved** M3 pivot free-play term
(no designed radial clearance, so the engine returns `INCONCLUSIVE` rather than a false pass).

### 3.2 Permanently qualitative risks (cannot be retired under DND-27)

These were previously the job of a printed or measured coupon. They remain on the risk register as
**qualitative** and must be accepted explicitly by the board before any promotion:

- print realisation (fusion, stringing, layer adhesion, elephant-foot, warp) — Step 1;
- measured release-force spread across many identical elements (≈9 % sd break-even) — Step 2, central bet;
- detent/ratchet hold and repeat after a slipped step — Step 2;
- rig noise floor, cumulative regional creep, and stiction release force under real surface finish — Steps 0, 3;
- miniature-height compliance under real miniature loads and operator handling — Steps 3, 6.

## 4. Candidate resolution rules (how convergence actually closes)

Apply in order; the first matching rule is the candidate's disposition.

1. **Promote** a survivor to [`08-current-design/`](../08-current-design/README.md) only when it has
   a complete integrated machine description + three-scenario BOM + risk register **and** an
   analytic/simulation/CAD pass at final pitch on its named gate in §3 (§3.1), **and** the board
   has explicitly accepted the §3.2 qualitative risks. No physical pass is available under DND-27.
2. **Reject** a survivor when its named gate fails against a *sourced* process limit or an analytic
   bound that cannot be recovered by a geometry change inside the pitch and cost envelope. Record
   the killing evidence in the evidence matrix; do not keep it "open pending a variant".
3. **Park** a survivor when its gate is *inconclusive* (analytic result between the pass and fail
   thresholds, e.g. the M3 pivot term). Parking requires a stated next analytic step, not a hope.
4. **Merge** survivors that resolve to the same mechanism after specification (e.g. S1 threshold
   memory and S4 tile memory may collapse into one tile-level architecture). Record the merge.

**Time-box:** steps 0–3 complete, or fail decisively, within the current experiment generation. A
survivor that cannot produce a final-pitch analytic/CAD disposition in that window is parked and
cannot be promoted.

## 5. What would change the plan

- If step 2 **passes** analytically with positive margin, the field is real **on paper** (subject to
  §3.2 residual risks) and the race is on modelled timing/cost (S3 low-channel travelling programmer
  becomes the most promising because it needs no pre-written media for surprise reveals).
- If step 2 **fails** analytically, escalate a requirements re-scope decision to the CEO before any
  further candidate invention. Options: larger pitch, fewer levels, pre-planned (not surprise) maps,
  or a higher cost ceiling. This is a product decision, not an engineering one.
- If step 1 shows the final-pitch geometry cannot fit the *sourced* FDM process envelope, switch the
  baseline process question (resin/SLA for the memory layer) to the CEO as a fabrication-baseline
  change, and record it as such — do not silently relax the criteria. This can only be assessed
  against sourced process limits, never by printing.

## 6. Evidence status snapshot

The honest current standing, to be kept in step with
[`07-evidence-and-decisions/README.md`](README.md):

| Candidate | Sourced | Calculated | Simulated | CAD | Printed | Measured |
|---|---:|---:|---:|---:|---:|---:|
| S1 threshold/ratchet | partial | ✓ | — | — | — | — |
| S2 planar tiles | partial | ✓ | — | — | — | — |
| S3 multi-row DMA | partial | ✓ | partial | — | — | — |
| S4 shared-bus tiles | partial | ✓ | — | — | — | — |
| S5 rotary stops | ✓ | ✓ | ✓ | ✓ | — | — |

**Nothing in the surviving field has printed or measured evidence, and under
[DND-27](/DND/issues/DND-27) none will be produced.** The *Printed* / *Measured* columns are
therefore permanently empty for this programme, not merely pending. The top programme risk is now
the set of permanently qualitative assumptions in §3.2, which analysis cannot retire; the plan
front-loads steps 0–2 to retire everything that *can* be retired.

## 7. Governance

- Branch + PR per coherent result; **no** push to `main`. **Merge authority is delegated to agents**
  per board directive [DND-19](/DND/issues/DND-19): merge your own PR once reviewed and the
  checks/evidence support it. No board approval is needed to merge.
- Candidate promotion into `08-current-design/` remains a PR and requires the §3 analytic gates plus
  explicit board acceptance of the §3.2 qualitative risks.
- All evidence rows must state sourced / calculated / simulated / CAD / printed / measured honestly;
  printed and measured will read `—` by policy.
- **No physical print test may be introduced as a gate** while
  [DND-27](/DND/issues/DND-27) is in force.
- Specialist needs are reported to the CEO; the CTO does not hire.
