# Falsifier adversarial audit — convergence logic and the winner's killer list

- **Status:** Independent review (Falsifier). Adversarial, not consensus.
- **Date:** 2026-09-28.
- **Owner:** Falsifier (agent `49e3be36`).
- **Scope:** [ADR-001](convergence-decision-2026-09.md) and
  [convergence-plan.md](convergence-plan.md), plus the reliability/cost evidence they rest on.
- **Requested by:** [DND-35](/DND/issues/DND-35) ("ask Falsifier to adversarially review the
  winner's killer list"). No winner exists yet, so this audits the **selection logic and the
  survivors' kill list** instead — which is what DND-35 actually needs before a winner is named.
- **Evidence discipline:** every claim below is **calculation** on repository inputs, or a
  **sourced-fact** observation about the repository's own documents. Nothing here is measured.
  No board contact is made or requested.

This document is explicitly hostile to the convergence plan. Its job is to find where the plan's
own reasoning could let a real winner through, kill a survivable candidate, or leave a false
"this cannot work" impression. Three findings, ranked by how much they change the decision.

---

## Finding 1 (material) — "the field is one bet in five shapes" is true for S1–S4 but **false for S5**

**Claim under attack** (ADR-001 §1, convergence-plan §2):

> The surviving field S1–S5 is **one bet in five shapes** … "If that bet fails, the entire
> surviving field fails, and the correct response is to reduce the product requirement … rather
> than to search for a sixth variation of the same bet."

**Attack.** The stated bet is:

> a passive, printable, final-pitch state/selection element can be written by a small shared
> programmer and can hold terrain load without powered holding.

This describes **S1, S2, S3, S4** — all of which use a *threshold/selection element* that must be
**actively set by a shared writer** and then **memorise** its state (gate + pawl, planar shutter,
printed register, tile clutch). S5 is **not** the same bet. Per the repository's own description
([07 README §"What the proposed mechanism actually does"](README.md)), S5 is:

- a **passive stepped cam** whose five states are *geometric height offsets*, not set/clear memory
  elements;
- the height is read by a **gravity-following toe** resting on a flat sector — there is no gate,
  no pawl, no toggle, no "memory element that must remember a written bit";
- the **writer rotates a rotor to one of five absolute positions** with a physical home stop; a
  detent only seats an *already-selected* angle. There is no threshold, no hold force, no state
  that can "decay".

**Why this matters.** The plan's decision rule says: *if the bet fails → escalate a requirements
re-scope before any further candidate invention*. If S5 is treated as the same bet, killing the
bet (print-force spread ≈9%, gate hold, ratchet repeat — S1–S4 killers) would also kill S5, whose
actual killers are **completely different**: cam buckling at ~4.96 N vs a 5 N abuse gate, detent
capture of one lost 18° step, and **motor sourcing** ($40/ea traceable MOUNT vs $1.25 allowance).
A requirements re-scope driven by an S1–S4 failure (release-force variance) is **not** evidence
that S5 fails, and vice versa.

**Consequence.** The convergence plan should carry **two bets, not one**:

1. **Bet A — written passive memory** (S1, S2, S3, S4). Killers: print/force spread, gate hold,
   register fan-out, tile-clutch independence. Failure of Bet A does **not** imply failure of Bet B.
2. **Bet B — absolute geometric stops** (S5). Killers: cam/toe structural strength at 5 N, loaded
   motor torque-speed, detent capture of a lost step, motor procurement cost. These are **not**
   shared with Bet A, except for the cross-cutting reliability/printability/reliability items.

This changes the *order* of work: the plan's Steps 0–3 front-load Bet-A killers. If Bet A dies
first, the plan currently jumps straight to "re-scope the product". The economically correct move
is to **run the Bet-B killers (S5 Step 2/Step 6) in parallel**, because a Bet-A failure leaves S5
as the only surviving architecturally-distinct family. **The plan's own §2 conclusion ("test the
bet") is correct; its premise that there is one bet is what is wrong.**

**Cheapest test that could reject this finding.** Show that S5's state is actually a *written
memory element* in the S1–S4 sense — i.e. that its five positions require a per-cell
set/clear/variable-stroke that can drift or fail like a gate. Repository evidence says the
opposite: S5's rotor is rotated **against a home stop and forward by 0/4/8/12/16 fixed motor
steps** — an absolute, homed write, not a threshold set. Unless someone can show the S5 write is
threshold-dependent, this finding stands.

---

## Finding 2 (material) — the "$500 ceiling rejects every survivor" conclusion is an **artifact
for S1/S2/S4**, and it is used in both directions

**Claim under attack** (convergence-plan §1, Test11 README §Headline 1):

> Every survivor is over $500 in the expected delivered scenario … **No survivor has a credible
> sub-$500 delivered path at working allowances.**

**Attack.** For S1, S2 and S4 the *working* total is dominated by **fallback purchases of parts
the design explicitly intends to print**. The BOM csv basis strings say so directly:

- `bom_S1.csv`, "Tile coupler / clutch (64 tiles)", $3 × 64 = **$192**:
  *"No bought part intended in S1 baseline; allowance only if tile isolation needs a coupler."*
- `bom_S1.csv`, "Release combs / latch actuators (tile segmented)", $0.50 × 64 = $32:
  *"No bought part intended; allowance for latch actuation if printable fails."*
- S4's "64 couplers $192 + 64 select drivers" are the same fallback pattern.

So S1's working total ($518) is **$224 of parts the design says it will not buy**. Remove them and
S1's working base is ~$294; with contingency ~$353 — **under the $500 ceiling** — and that is
before the sourced-motor substitution that hits S5, because S1/S2/S4 are *claimed* to be
print-passive. Meanwhile the same Test11 README reports a **print-intent floor** of S1 $239 /
S2 $299 / S4 $311 and says those floors "are only reachable if the printed layer works".

**The plan uses the fallback-inflated working number to conclude "fails $500", and the floor
number to conclude "plausible if printed". These are two different numbers for the same
survivor, and the convergence evidence uses the pessimistic one as if it were the verdict.**
The honest disposition is **not "fails cost"** but **"cost is undetermined until the printed
selector/media layer is qualified"** — i.e. cost is *downstream of* the Bet-A gate, not
independent evidence against it.

**What is genuinely established (keep this).** Two cost results are robust and mechanism-neutral:

1. **Any bought part per cell kills the budget** ($0.10/cell = $640). Solid.
2. **A traceable 8 mm 18° PM stepper is $40/ea**, so **S5's 80-motor head cannot be cost-sourced
   at the Test08 $1.25 allowance**. Solid, *sourced*. This is a real Bet-B killer.

So cost kills **S3 decisively** and **threatens S5**, but for **S1/S2/S4 cost is a conditional,
not a verdict**. The evidence matrix should say that.

**Consequence.** Before any winner is named, the cost disposition for S1/S2/S4 must be restated as
**undetermined pending print qualification**, and the winner's killer list must not cite a
fallback-inflated BOM as independent proof of failure.

**Cheapest test that could reject this finding.** Produce a *matched* BOM for S1/S2/S4 that keeps
the fallback lines but also shows the printed alternative is qualified (from Step 1/Step 2). If
the printed layer is unqualified, the fallback price is the honest price; if it is qualified, the
fallback is double-counting. Either way, the *number* is conditional on the print gate.

---

## Finding 3 (correctness) — the reliability module's one-sided-bound convention is **inverted**
and disagrees with the headline 1.91 M figure

**Claim under attack.** The project's reliability gate states (multiple docs): a 99% perfect-map
goal needs **q ≤ 1.57×10⁻⁶** and **≈1.91 million zero-failure independent trials** for a one-sided
95% bound.

**Attack (falsified my own first hypothesis — record it).** I first suspected the **1.91 M** figure
was arithmetically wrong and should be ~32,671. Re-derivation shows **1.91 M is correct** for a
one-sided 95% *upper confidence bound*: we need `P(0 failures | q) = (1−q)^n ≤ 0.05`, so
`n ≥ ln(0.05)/ln(1−q)`, which gives 1,907,667 at q = 1.570×10⁻⁶. The repository's headline number
is right. **The bug is not in the headline; it is in the reusable helper.**

`06-experiments/test11_falsification_library/reliability.py:zero_failure_trials()` documents:

> "Zero-failure independent trials n for a one-sided upper bound q at confidence.
> `P(0 failures in n) = (1-q)^n >= confidence  ->  n >= ln(conf)/ln(1-q)`."

That formula is **backwards** for a one-sided bound. Requiring `(1−q)^n ≥ 0.95` asks for the
number of trials at which you are **95% *likely to see at least one failure*** — a *lower* bound,
not an upper one. The 95% upper-bound convention (used by the headline and by
`test11_cost_printability_reliability/checks.py:70`) requires `(1−q)^n ≤ 0.05`.

**Demonstrated incoherence:**

| Computation | q | Result | Used where |
|---|---:|---:|---|
| `zero_failure_trials(q, confidence=0.95)` | 1.570e-6 | **32,664** | helper, claims "95% one-sided upper bound" |
| `Math.ceil(ln(0.05)/ln(1−q))` | 1.570e-6 | **1,907,667** | headline docs + cost `checks.py:71` |

The two differ by **~58×**. A user of the helper who trusts its docstring will report a **58×
weaker** reliability requirement than the project's own headline — i.e. they will *overstate* the
mechanism's demonstrated reliability. That is exactly the failure mode the Falsifier role exists
to prevent. (The helper's `test_zero_failure_trials_formula` in the falsification-library
`checks.py` pins `n=513` at q=1e-4 and separately checks 2.69e-8 → 1.91 M, so it does not exercise
the discrepancy at the relevance q.)

**Consequence.** Fix the helper to take an explicit convention (`upper_bound` default) and assert
it agrees with the project's 1.91 M headline at q=1.570e-6. Until fixed, the helper must not be
quoted for a one-sided upper bound, and any downstream "demonstrated reliability" claim derived
from it is invalid.

**Cheapest test that could reject this finding.** Show that `zero_failure_trials(1.570e-6)` is
intended to return 1.91 M under its documented contract. It returns 32,664. The finding stands.

---

## Summary — what this changes for DND-35

| # | Finding | Decision impact | Disposition |
|---|---|---|---|
| 1 | S5 is a **different bet** from S1–S4 | A Bet-A failure should not trigger a product re-scope while Bet B is untested; run S5 Step 2/6 in parallel | **Adopt two-bet framing** |
| 2 | S1/S2/S4 cost is **conditional, not failed** | Do not cite fallback-inflated BOM as a killer; restate as "undetermined pending print gate" | **Restate cost disposition** |
| 3 | Reliability helper convention **inverted** | Any reliability claim from the helper is ~58× optimistic; fix + pin to 1.91 M | **Fix helper (this PR)** |

### What this audit does **not** do

- It does **not** promote any winner. No candidate has physical evidence and DND-27 forbids
  producing it.
- It does **not** overturn the S3 cost rejection or the sourced 8 mm-motor finding — those are
  robust and survive the audit.
- It does **not** claim Bet A is viable. It claims Bet A and Bet B can fail independently, so the
  convergence plan's single-fate logic is too coarse to decide the winner.

### Residual uncertainties (cannot be closed analytically; DND-27)

- Whether S5's write is truly absolute (not threshold-dependent) — logical, but only a coupon
  would prove the home-stop/detent seats deterministically. **Qualitative.**
- Whether the printed selector/media layer works at all — the pivot of Finding 2. **Qualitative.**
- Real release-force spread, print realisation, creep — unchanged from ADR-001 §5.2.

### Next action

1. Patch `reliability.py:zero_failure_trials` to be convention-explicit and pin it to the project
   headline (this PR).
2. Hand Findings 1–2 to the CTO on [DND-35](/DND/issues/DND-35): adopt the two-bet framing and
   restate the S1/S2/S4 cost disposition.
3. Add a CI check that the helper and the headline agree, so the 58× discrepancy cannot return.
