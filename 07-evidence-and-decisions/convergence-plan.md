# DND-2 Convergence Plan (CTO)

Companion decision record: [`convergence-decision-2026-09.md`](convergence-decision-2026-09.md) (ADR-001).


**Owner:** CTO. **Status:** active. **Supersedes:** the open-ended candidate list in
[`04-architecture-candidates/`](../04-architecture-candidates/README.md), which is preserved as the
search record rather than a commitment.

This document ranks the *quickest tests that can kill a survivor* and states which candidate each
test would kill. The goal is convergence on one or a small number of serious architectures; it is
deliberately not another survey.

## 1. The binding programme constraint

The product target is a strict conjunction: **80×80 cells, 5.08 mm pitch, ≥40 mm travel,
<30 s full-map ready, regional updates, <$500 purchased parts, repeated reuse.** Every survivor is
currently rejected or unsupported on at least one conjunct:

| Gate | Current state of the whole field |
|---|---|
| Timing | Conditional analytical passes exist (S5 26.25 s; S3/S4 shared rows 21–27 s). All are unrealized estimates, not measured. |
| Cost | The best-defended BOMs are **$432 / $518.40 with contingency** (S5) and **$447–$1,086** (S3/S4). No architecture has a *matched delivered* BOM under $500. |
| Pitch / printability | No full-pitch cell mechanism has been printed and measured. 0.20 mm walls, 5.08 mm gates, 0.05 mm effective gaps are all nominal. |
| Load support | Best analytical cam screen is 4.96 N ideal against a 5 N abuse gate; no measured 1 N service hold. |
| Regional isolation | Architecturally plausible in S2/S4, untested; no numerical disturbance limit exists (Q5). |
| Reliability | At 0.01 % per-cell error, P(all 6400 correct) ≈ 52.7 %. No per-cell feedback in any cost model. |

**Therefore no survivor can be promoted to [`08-current-design/`](../08-current-design/README.md)
on present evidence.** Promotion requires a survivor to pass its named physical gate below, at final
pitch where the gate is about density.

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

## 3. Elimination order (cheapest informative test first)

Each step is a gate: a fail kills the named candidates and stops dependent spend. A pass only
authorises the next step. Steps 0–3 together are the critical path; steps 4–6 run in parallel behind
them.

| # | Test | Kills on failure | Cost | Where |
|---:|---|---|---|---|
| 0 | **Common isolation rig** (Q5): two adjacent loaded full-pitch tiles + interchangeable drive fixtures; measure untouched-neighbour peak vertical/lateral motion and miniature movement during adjacent reset. | It does not kill a candidate directly; it supplies the shared **disturbance baseline** every other test is judged against. Without it, S2/S4 isolation claims cannot be compared. | Printed + lab fixture | Falsifier / [`DND-5`](/DND/issues/DND-5) |
| 1 | **Passive pitch/backlash coupon, final pitch.** Adjustable-gap and backlash test surfaces → find the input-process capability (minimum reliable fit, web, and slop) at 5.08 mm on the X1C/PLA. | Any survivor whose mechanism needs a fit, web, gate or detent outside the measured capability. This is the *cheapest* global kill. | One plate | CostMfg / [`DND-6`](/DND/issues/DND-6) |
| 2 | **Printed one-bit passive memory cell.** One final-pitch element that stores one binary state, holds ≥1 N service load, toggles with a small force and does not release under vibration, across thousands of cycles. | **S5** (if the detent cannot correct a slipped step), **S1** (if the ratchet/gate cannot hold or repeat), **S4** (if the local memory does not exist) — and the whole shared-power/passive-memory bet above. | Small coupon batch | Inventors + Falsifier |
| 3 | **Isolation, 2×2 tile load stack** with the step-0 rig. Regional reset of one tile while its neighbour carries a representative miniature. | **S2** (registration seizes the follower) and **S4** (coupling/jam propagates) — the two architectures that depend on tile isolation. | Printed | InventorAlpha/Beta |
| 4 | **Selector / register** (Q3/Q4): one common stroke selectively engages 2×4 outputs at final pitch without neighbour release. | **S1** (threshold gates), **S3** (fan-out register), **S4** (tile clutch). | Coupon | InventorBeta + Falsifier |
| 5 | **Writer path** (Q2): complete receive→write→install→register→settle for one tile, timed. | **S2** for surprise reveals; bounds S1's mask install. | Script + coupon | InventorAlpha |
| 6 | **Load, structure and power:** spliced full-span beam + dummy platen at weighed column mass; lift torque-speed margin, flatness, power-cut behaviour. | Any survivor whose lift/structure cannot maintain the unload gap or hold position on power loss. | Lab | InventorBeta / CostMfg |

## 4. Candidate resolution rules (how convergence actually closes)

Apply in order; the first matching rule is the candidate's disposition.

1. **Promote** a survivor to [`08-current-design/`](../08-current-design/README.md) only when it has
   a complete integrated machine description + three-scenario BOM + risk register **and** a physical
   pass at final pitch on its named gate in §3 with measured values, not allowances.
2. **Reject** a survivor when its named gate fails with a measured value that cannot be recovered by
   a geometry change inside the pitch and cost envelope. Record the killing evidence in the
   evidence matrix; do not keep it "open pending a variant".
3. **Park** a survivor when its gate is *inconclusive* (measured value between the pass and fail
   thresholds). Parking requires a stated next test, not a hope.
4. **Merge** survivors that resolve to the same mechanism after specification (e.g. S1 threshold
   memory and S4 tile memory may collapse into one tile-level architecture). Record the merge.

**Time-box:** steps 0–3 complete, or fail decisively, within the current experiment generation. A
survivor that cannot produce a final-pitch physical coupon in that window is parked and cannot be
promoted.

## 5. What would change the plan

- If step 2 **passes** broadly, the field is real and the race is on timing/cost (S3 low-channel
  travelling programmer becomes the most promising because it needs no pre-written media for
  surprise reveals).
- If step 2 **fails**, escalate a requirements re-scope decision to the CEO before any further
  candidate invention. Options: larger pitch, fewer levels, pre-planned (not surprise) maps, or a
  higher cost ceiling. This is a product decision, not an engineering one.
- If step 1 shows the X1C/PLA process cannot hold the needed geometry, switch the baseline process
  question (resin/SLA for the memory layer) to the CEO as a fabrication-baseline change, and record
  it as such — do not silently relax the criteria.

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

**Nothing in the surviving field has printed or measured evidence.** That is the top programme risk
and the reason the plan front-loads steps 0–2.

## 7. Governance

- Branch + PR per coherent result; **no** push to `main`; merges only on board authorisation.
- Candidate promotion into `08-current-design/` is a PR against a branch and is subject to board
  review, not a unilateral CTO edit.
- All evidence rows must state sourced / calculated / simulated / CAD / printed / measured honestly.
- Specialist needs are reported to the CEO; the CTO does not hire.
