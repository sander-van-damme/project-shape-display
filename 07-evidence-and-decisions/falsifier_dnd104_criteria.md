# DND-104 — Pre-registered adversarial audit criteria for the reliability-first candidates

- **Issue:** [DND-108](/DND/issues/DND-108) (Falsifier). Parent [DND-104](/DND/issues/DND-104),
  grandparent [DND-102](/DND/issues/DND-102).
- **Pre-registration register:** a fixed, frozen list of attacks written **before** the CTO's
  `10-reliability-mask/` model exists, so convergence cannot cherry-pick gates. Every attack names
  the **exact deciding number** and the **cheapest test** that would reject it.
- **Companion gate:** [`falsifier_dnd104_checks.py`](falsifier_dnd104_checks.py). It runs green
  **now** against the repository's own reliability arithmetic (independent of the CTO model), and
  it exposes `audit(model)` / `--model <path>` so the same checklist can be pointed at
  `10-reliability-mask/` the moment it lands.
- **Method provenance:** follows the method that broke S6-LC
  ([`dnd91-s6lc-falsification.md`](dnd91-s6lc-falsification.md)) and the DND-74 audit
  ([`dnd74-s6lc-falsification.md`](dnd74-s6lc-falsification.md)), re-based on the reliability-first
  criteria [DND-103](/DND/issues/DND-103) in [`02-design-criteria/README.md`](../02-design-criteria/README.md).
- **Evidence class of this document:** **CALCULATION / document audit only.** No print, no
  purchase, no measurement. No board contact ([DND-32](/DND/issues/DND-32), [DND-27](/DND/issues/DND-27)).
  `08-current-design/` untouched.

> **What this is not.** It is not a scorecard a candidate "passes". It is a list of ways a candidate
> can be **killed**. A candidate that cannot answer an attack with a number and a test is not
> "passed" — it is **unfalsified**. The default verdict for an unanswered attack is **FAIL**.

---

## 0. How to read the register

Every attack below has the same fields, so a CTO model can be held to it mechanically:

| Field | Meaning |
|---|---|
| **ID** | Attack id (A1…A13, plus gates G-*). |
| **Claim under attack** | The sentence the candidate must defend. |
| **Attacker's math** | The pre-registered counter-number, computed in the companion script. |
| **Deciding number** | The single number that flips the verdict. |
| **Cheapest test** | The smallest coupon/measurement/derivation that can reject it. |
| **Pass / Fail threshold** | Exact numeric bar. |
| **Consequence of pass / fail** | What the verdict licenses / forbids. |
| **Class** | CALCULATION (now) or MEASURED (coupon required). |

The companion script pins the `Deciding number`s as assertions so prose cannot drift from arithmetic.

The CTO's convergence must report, per architecture, the **audit vector** `(A1…A13, G1…G8)` with
each field answered by a number or an explicit `UNRESOLVED`. An `UNRESOLVED` attack is a **FAIL for
promotion**, and promotion requires **zero** FAILs (G8 reliability may be `UNRESOLVED-BUT-GATED` only
if the candidate ships a coupon C1 that the program commits to running — see §6).

---

## 1. The central gate: reliability arithmetic (A1–A4)

This is where the reliability-first program lives or dies. All four attacks are pure arithmetic and
runnable now.

### A1 — Map yield compounds; "all 6,400 correct" is ~52.7 % at q = 0.01 %

- **Claim under attack:** "the machine builds a correct map."
- **Attacker's math.** A map is correct only if **every** repeated element is correct:
  `P(perfect map) = (1 - q)^N`, with `N` = the number of independent repeated elements the
  architecture **claims**. At the program's own stated fear-point `q = 0.01 % = 1e-4`:

  | N | P(all correct) |
  |---:|---:|
  | **6,400** | **0.5273** |
  | 800 | 0.9231 |
  | 100 | 0.9900 |
  | 25 | 0.9975 |
  | 1 | 0.9999 |

  So at 0.01 %/cell, **all 6,400 correct is only 52.7 %** — a coin flip. The repeat count `N` is
  the lever.
- **Deciding number:** the candidate's **declared `N`** (number of independent elements that must
  each work) and its **declared `q`**, fed through `(1-q)^N`.
- **Pass threshold:** `(1 - q_declared)^N_declared >= 0.99` for a 99 %-map target.
- **Cheapest test:** none required — it is arithmetic. The candidate must **declare N and q**.
  An architecture that cannot state `N` **fails A1 by silence**.
- **Consequence of pass:** the reliability budget is arithmetically closed at the declared numbers.
- **Consequence of fail:** the candidate must change `N` or `q`; q = 1e-4 at N = 6,400 is a 52.7 %
  map and is not a product.
- **Class:** CALCULATION. **Owner of q:** the coupon (A2).

**Pre-registered reading.** The single most important reliability claim a candidate can make is
**"N is small."** The DND-103 principle *"thousands of simple things + a few sophisticated shared
mechanisms"* is exactly a claim that the number of per-cell precision elements is minimized and the
sophisticated count is a small number of shared, testable mechanisms. A candidate must show its
`N` decomposition, not a single `N`.

### A2 — The `q` the reliability gate actually needs, and how a coupon bounds it

- **Claim under attack:** "our repeated element's as-printed error rate is low enough."
- **Attacker's math.** For a 99 %-map target the per-element budget is
  `q <= 1 - 0.99^(1/N)`:

  | N (independent elements) | q required for 99 % map |
  |---:|---:|
  | 6,400 | **1.570e-6** |
  | 800 | 1.256e-5 |
  | 100 | 1.005e-4 |
  | 25 | 4.019e-4 |
  | 1 | 1.000e-2 |

  Correlated elements should be **grouped** (a bank that fails together counts once for the yield
  formula but many for the product), so the candidate must declare both the **independent group
  count** and the **group size**.
- **Deciding number:** the **coupon zero-failure trial count** needed to *demonstrate* `q` at 95 %
  confidence: `n >= ln(0.05)/ln(1-q)`.

  | q to be excluded | trials (95 % upper bound) |
  |---:|---:|
  | 1e-4 | **29,956** |
  | 1e-5 | **299,572** |
  | 1.570e-6 | **1,908,109** |

  The program's own `reliability.py::zero_failure_trials` computes exactly this.
- **Pass threshold (coupon C1):** for the **device's own declared `N`**, the coupon must run
  **enough counted cycles** that the *upper* 95 % bound on per-element error is **below**
  `1 - 0.99^(1/N)`.
- **Cheapest test:** a counted-failure coupon: one representative repeated element, cycled `n`
  times, counting every miss. **A 6-cell coupon with a handful of cycles cannot bound q at board
  scale** (DND-104's own reliability discipline). The coupon is honest only if the trial count is
  stated and the resulting bound is stated.
- **Consequence of pass:** the candidate's `q` is bounded (at 95 % confidence) below its budget.
- **Consequence of fail:** q is unbounded; the candidate must either lower `N` (fewer independent
  elements), add detection/recovery, or run more trials.
- **Class:** CALCULATION for the budget; **MEASURED** for the bound.

### A3 — Correlated failure: one shared mechanism takes out a group

- **Claim under attack:** "our repeated elements fail independently."
- **Attacker's math.** The DND-76 primitives / S6-LC design already conceded that detection is at
  **4 home sensors per bank** (32 sensors over 8 banks), **not per cell**. So a stuck comb / clutch
  / mask strip produces a **silent, correlated** error over its whole group (80–800 cells). The
  yield formula in A1 assumes independence; correlated failures make the effective error rate
  **worse** than the independent model, not better.
- **Deciding number:** the **worst-case correlated group size** = the largest set of cells that
  share a single selection/memory/reset element, and whether a **detection path** localizes the
  fault to that group.
- **Pass threshold:** every shared element must be (a) reachable/replaceable, (b) detectable by a
  stated sensor or re-home path, and (c) bounded to a declared group size. A correlated fault with
  **no detection** fails regardless of its probability.
- **Cheapest test:** jam-injection on one coupon group (see A9) plus a README statement of the
  sensor/recovery path.
- **Consequence of pass:** correlated faults are detectable and localized.
- **Consequence of fail:** the reliability arithmetic in A1/A2 is optimistic — correlated failures
  increase the effective error rate.
- **Class:** CALCULATION + document audit now; MEASURED via A9.

### A4 — "What has to work correctly 6,400 (or fewer) times?" — the count attack

- **Claim under attack:** the DND-103 gate question.
- **Attacker's math.** The candidate must publish a decomposition, not one number:

  | Counter | Must be answered per architecture |
  |---|---|
  | Independent moving elements per cell | integer, and their function |
  | Precision contacts **per cell** | integer |
  | Compliant (springy) printed elements | integer, and whether their *force* decides correctness |
  | Wear interfaces | count + expected service life (cycles) |
  | Tolerance-sensitive interactions | count |
  | Repeated elements that must each work | **N** for A1 |
  | Shared mechanisms (sophisticated, few) | count + how each is tested |
  | Correlated-failure groups | count + group size |

- **Deciding number:** the **per-cell count of precision/force-critical elements**. The DND-103
  criteria forbid precision/force-critical interactions at the cell level.
- **Pass threshold:** **zero** force-critical printed springs per cell; **zero** sub-mm precision
  contacts per cell; every retention is a **positive hard stop**, or an explicit, bounded,
  measured exception.
- **Cheapest test:** CAD dimension audit of the coupon cell + the A2 counting coupon.
- **Consequence of pass:** the architecture is genuinely "thousands of simple things."
- **Consequence of fail:** the candidate has re-imported the exact pattern DND-103 was written to
  prevent; **FAIL**, no coupon can rescue a force-critical 0.45 mm spring at 6,400 copies.
- **Class:** CALCULATION / CAD audit.

---

## 2. Honest timing (A5–A6)

### A5 — Unpriced mask-generation / transport / reset / verification terms

- **Claim under attack:** "full-map < 30 s."
- **Attacker's math.** The DND-103 timing decomposition requires **seven** stages reported
  separately, and **both** the visible transition time and the sustained arbitrary-map cycle time.
  The S1/comb mask medium has a **12,800-hole** write per full map (6,400 cells × 4 unary planes),
  and the program's own screen already found the write fails on the visible budget at 80 channels:

  | Mask-write path | Time | Verdict vs 30 s |
  |---|---:|---|
  | serial single needle, 12,800 holes × 0.20 s | **2,560 s** | FAIL |
  | 80 channels in parallel | **56 s** | FAIL on the visible budget |
  | 500 channels in parallel | **8.96 s** | passes only with ~500 channels |

  A candidate must **name and time** mask generation, transport/indexing, reset, broadcast strokes,
  settling/locking, and verification. Off-budget prep is only legitimate as an explicit
  **double-buffer** product statement, and then the **sustained cycle time** must be reported too.
- **Deciding number:** the **sum of all seven stages**, including any stage declared "off the
  visible budget", for the **sustained** (worst-case) cycle.
- **Pass threshold:** visible transition **< 30.0 s** **and** sustained arbitrary-map cycle
  **< 30.0 s**.
- **Cheapest test:** document audit — every stage must have a number and a class; a missing stage
  is a FAIL. Then one timed coupon stroke + one timed mask-index cycle.
- **Consequence of pass:** the timing claim is honest.
- **Consequence of fail:** the headline is optimistic; restate with the real bottleneck.
- **Class:** CALCULATION now; MEASURED coupon later.

### A6 — Regional update really works (or the trade-off is explicit)

- **Claim under attack:** "regional update = one bank / one strip."
- **Attacker's math.** DND-103 now **permits** coarse bank-local / segment / strip updates as an
  acceptable simplification **only if the trade-off is quantified and surfaced**. But a regional
  update that resets one bank must still (a) not disturb its neighbours, (b) not require the whole
  board's mask media to be re-made, and (c) fit its own time budget. The S6-LC/DND-91 finding was
  that a bank-local replay still inherits the **off-line mask-prep caveat in full**.
- **Deciding number:** `(regional update time) / (full map time)` and the **neighbour disturbance**
  in mm.
- **Pass threshold:** neighbour peak displacement **<= 0.10 mm**; unchanged cells require **no**
  deliberate reset/homing; regional time < full-map time and scales with region size.
- **Cheapest test:** the DND-104 coupon with two adjacent groups; cycle one, measure the other.
- **Consequence of pass:** regional updates are a real property.
- **Consequence of fail:** record "full-board reset per reveal" as an explicit product weakness, or
  fix the mechanism.
- **Class:** CALCULATION + CAD now; MEASURED later.

---

## 3. Cost (A7)

### A7 — Soft-line repricing (DND-46 method) + missing capabilities

- **Claim under attack:** "purchased BOM < the ceiling."
- **Attacker's math.** The **DND-46 method** that broke S5: (1) reprice the softest `sourced`-class
  lines to plausible defensible retail (bundled lines priced at best case are the documented failure
  mode), and (2) restore **capabilities absent from the BOM entirely**. On S6-LC this moved
  $162 → ~$197 delivered, and DND-93 later found the corrected figure at **$226.77 parts /
  $263.05 delivered** (mission gate holds on parts, delivered convention fails). The candidate must
  be audited the same way:
  - reprice lead screws, guide rods/bushings, belts/pulleys, motors, couplers;
  - restore **mask medium**, **puncher / mask-generation hardware**, **mask-transport linkage**,
    **frame splice hardware** for the 406 mm frame (X1C bed is 256 mm), and any
    **verification/metrology** capability.
- **Deciding number:** the **hostile repriced purchased total** vs the ceiling. Under the DND-104
  program the tightened ceiling is **<$250 purchased (excluding 3D-printed parts)**; the mission
  ceiling is <$500 purchased.
- **Pass threshold:** **hostile repriced purchased total < $250** (strong target), with every
  missing capability either costed or explicitly excluded-and-justified as printable.
- **Cheapest test:** line-by-line repricing + capability checklist (no purchase needed).
- **Consequence of pass:** the cost claim survives hostile pricing.
- **Consequence of fail:** the cost headline is unqualified; restate the real number.
- **Class:** sourced listings + CALCULATION.

---

## 4. Load / jam / regional / silent failure (A8–A10)

### A8 — Load-during-write (the battle map is *in play*)

- **Claim under attack:** "the platen is unloaded while writing."
- **Attacker's math.** The product is a **tabletop D&D map with miniatures on it**, and regional
  updates explicitly reshape terrain under/beside placed minis. S6-LC's lift axis was sized for
  `LIFT_LOAD_N = 0.4 N/column` while writing, and its README conceded the "minis off the region"
  restriction. A miniature is 5-30 g = **0.05-0.3 N**; if a mini sits on a lifted column the load
  is additive. **Any architecture that assumes the moving region is unloaded while writing is out
  of spec for the stated use case.**
- **Deciding number:** the **write-time load per moving column** vs the mechanism's hold/lift
  capacity: `(column mass + terrain load + a representative miniature load) <= capacity / SF`.
- **Pass threshold:** the mechanism either (a) holds the surface **with minis on it**, or (b) the
  design explicitly states "minis off the moving region" as a **product limitation** (not a hidden
  assumption) and the lift/hold gate is re-derived under the loaded case.
- **Cheapest test:** load a coupon column with a representative mini (0.05-0.3 N) and cycle it.
- **Consequence of pass:** load-during-write is addressed.
- **Consequence of fail:** G3-class lift/hold gates pass only under an assumption that contradicts
  the product; restate.
- **Class:** CALCULATION now; MEASURED later.

### A9 — Jam & silent failure: one jam must not silently corrupt a row, bank, or module

- **Claim under attack:** "a jam is contained and detectable."
- **Attacker's math.** Reset works by releasing every element of a group and letting it return
  (gravity / spring). A **jammed** element (friction, a nicked pocket, debris, static) does **not**
  return, and without per-cell feedback it keeps a **stale height** while the rest of the group
  resets — a silent error. This is the historic S1 "silent miss" failure. The reliability gate
  (A1) is invalid if this path is unaddressed.
- **Deciding number:** the **jam blast radius** = number of cells whose commanded height is wrong
  from one jam, **and** the time/step to detect it. Target blast radius: **1 cell**, detectable.
- **Pass threshold:** a single jam changes **only its own cell's** height, **and** a stated
  detection path (per-group home sensor, re-home, or error check) reports the fault. No silent
  wrong cell.
- **Cheapest test:** deliberately jam one coupon cell, run a full reset cycle, and measure whether
  neighbours stay correct and whether the fault is reported.
- **Consequence of pass:** jam containment is a real, tested property.
- **Consequence of fail:** the reliability arithmetic is optimistic and the architecture needs an
  explicit detection/recovery path or a redesign.
- **Class:** CALCULATION + document audit now; MEASURED later.

### A10 — Tolerance / print variation destroys the pitch or the fit

- **Claim under attack:** "the as-printed cell fits its lane and clears its neighbour."
- **Attacker's math.** The DND-103 rule: the 5.08 mm pitch is a **visible surface** requirement, not
  an internal mechanism budget. The historic S6-LC failure (DND-91 A1) was an **unplaced** pawl
  overflowing its 0.74 mm owned half-lane by 0.260 mm while the gate compared against the whole
  1.48 mm inter-body gap. Any candidate whose repeated feature is placed near the pitch boundary is
  at risk; **the placement, not the budget, must be audited.**
- **Deciding number:** the **maximum radial excursion of any moving feature from the cell
  centreline**, in mm, vs the **owned half-lane** `(PITCH/2 - BODY/2)`.
- **Pass threshold:** every moving feature lies **within its owned half-lane** in CAD, with
  clearance >= the candidate's stated FDM tolerance; **zero** neighbour overlap at the pitch
  lattice; a coupon confirms no as-printed interference.
- **Cheapest test:** CAD placement audit (now, no print) + a 4x4 full-pitch coupon measuring
  neighbour interference.
- **Consequence of pass:** the pitch claim is placed, not merely budgeted.
- **Consequence of fail:** the pitch claim is not established; the mechanism needs re-placement or
  re-budget.
- **Class:** CAD now; MEASURED later.

---

## 5. The decisive falsifier and the placement gate (A11–A12)

### A11 — The single decisive falsifier

- **Claim under attack:** the candidate's **headline** (cost + time + reliability together).
- **Attacker's math.** Every outstanding attack above collapses to **one cheap experiment** per
  candidate family: *can the repeated element, printed at true full pitch on the actual X1C + PLA
  process, place, engage, hold, release, and repeat **without a silent miss**, when cycled enough
  times to bound `q` below `1 - 0.99^(1/N)`?* If the answer is no, the architecture is refuted at
  the coupon level before any board print.
- **Deciding number:** the **counted-failure coupon result**: `failures / trials`, vs the A2 budget.
- **Pass threshold:** zero failures across the A2 trial count for the declared `N`.
- **Cheapest test:** coupon **C1** (section 6).
- **Consequence of pass:** the architecture is eligible for the prototype ladder (B -> C -> D).
- **Consequence of fail:** the architecture is refuted; record as a failed idea.
- **Class:** MEASURED (handoff — no print in the agent environment).

### A12 — Pitch/lane placement (mandatory, not just a budget)

- **Claim under attack:** "the cell fits at 5.08 mm."
- **Attacker's math.** Restated as a hard gate: the candidate must show the **placed** CAD, not a
  free-space budget. Any claim of the form "feature + bleed <= gap" that ignores placement
  (DND-91 A1) is automatically **BROKEN**.
- **Deciding number:** `max_feature_excursion_mm <= own_half_lane_mm`, with
  `own_half_lane = PITCH/2 - BODY/2`.
- **Pass threshold:** strict inequality with a stated clearance; verified in CAD source, not prose.
- **Cheapest test:** read the SCAD placement line and compute; then the C1 coupon.
- **Consequence of pass:** A10 is closed.
- **Consequence of fail:** A10 fails.
- **Class:** CAD + CALCULATION.

---

## 6. The cheapest experiment that can reject each candidate (coupon C1)

DND-27 forbids purchase/print in the agent environment. This coupon is written **now** so it is
ready to hand to the CTO / board for a real X1C print (PLA, 0.4 mm nozzle, 0.2 mm layers). Every
candidate family (S1-broadcast / threshold-ratchet; punched-film/tape; comb-mask; the CTO's
eventual `10-reliability-mask/` design) can be screened with this single coupon.

**Coupon C1 — true-pitch repeated-element reliability coupon.**

- **Cells/modules:** one **4 x 4** block at true 5.08 mm pitch (16 repeated elements), plus one
  isolated element, plus one **two-group** pair (for A6/A9 regional + jam).
- **Important dimensions:** true `PITCH = 5.08 mm`; candidate's declared `COLUMN_BODY`; every
  moving feature measured from the cell centreline; the mask/selection interface at the candidate's
  own thickness. Print a **clearance matrix** (3 values spanning the candidate's tolerance) rather
  than one nominal fit.
- **Parts to print:** the repeated cell x16; the selection/mask element x1 group; the reset/release
  element x1 group; a base plate. Per the candidate's own CAD.
- **Purchased parts:** none required (**pure print** + a digital caliper + a push-pull gauge or a
  0.01 g balance + a phone camera for the counted run).
- **Measurements:**
  1. as-printed body, lane clearance, and **neighbour interference** at the pitch lattice (checks
     A10/A12);
  2. **engage/release rate** over a **counted** number of cycles per element (checks A1/A2);
  3. **hold force** under a representative mini load (checks A8);
  4. **release-force spread** (sd as % of mean) across the 16 elements (checks A4);
  5. **jam injection**: jam one element, reset the group, measure neighbour state and whether the
     fault is reported (checks A9);
  6. **regional disturbance**: cycle one group, measure the other (checks A6).
- **Pass/fail thresholds:**
  - A10/A12: **zero** neighbour contact at the pitch lattice;
  - A1/A2: **zero silent misses** across the A2 trial count for the declared `N`. For a 99 % map at
    `N = 6,400` that needs a bound on `q`, not literally 1.9M cycles on a 16-cell coupon — the
    coupon run and the extrapolation must both be stated, and the **coupon must state what `N` it
    can honestly bound** (see the honest-bound table below);
  - A8: hold force >= per-element design load **with** a representative mini load;
  - A9: jam blast radius = 1 cell **and** detectable;
  - A6: neighbour peak displacement **<= 0.10 mm**.
- **Repetitions/cycles:** at least **100 counted cycles/element on 4 elements (400 total)** per
  coupon, and **3 coupon batches** (bed-centre + bed-corners, after the DND-103 coupon discipline)
  to capture print-to-print variation. **This cannot demonstrate `q = 1.570e-6`**; the coupon's job
  is to reject the *large*-`q` failure modes and to **measure the counted per-cycle failure rate**,
  and to state the resulting upper bound explicitly.
- **Full-scale assumption tested:** that the repeated element, printed at true pitch on the actual
  X1C + PLA process, simultaneously (a) fits, (b) holds under a mini, (c) releases consistently,
  (d) contains a jam to one cell, and (e) repeats without a silent miss.
- **Consequence of passing:** the candidate's A1/A2/A4/A6/A8/A9/A10 risks are bounded; the
  prototype ladder (B -> C -> D) may proceed.
- **Consequence of failing:** the candidate is **refuted** at the repeated-element level before any
  board print; the failure mode is recorded as evidence.

**What a coupon can and cannot bound (pre-registered).** A coupon with `n` counted cycles and zero
observed misses bounds the per-element error rate at `q <= ln(0.05)/ln(1 - 1/n)`-style levels only.
Concretely, a **400-cycle** coupon (16 elements x 25, or 4 x 100) that runs clean bounds `q` no
better than `~7.5e-3` at 95 % confidence — **~4,800x looser than the 1.570e-6 a 6,400-element board
needs**. Therefore the coupon's valid conclusions are:
- it can **reject** any candidate whose failure mode shows up at rates above ~1e-3 per cycle
  (the practical, recurring failures: fit, jam, force spread, neighbour interference);
- it **cannot** promote a candidate on reliability grounds; only a mechanism with an **error
  detection + recovery** path converts the coupon into a real reliability argument (because
  detected-and-recovered errors never enter the map yield).

This is the single most important pre-registered consequence in this document: **a coupon can
kill, but it cannot crown.** An architecture without detection/recovery cannot be promoted to a
full 6,400-cell print on any coupon evidence we can afford.

A second, **non-physical** test runnable now (no print):

- **CAD placement sweep** — re-render the candidate cell at the true placement and assert no
  X-overlap with the neighbouring cell at the pitch lattice; reproduces A10/A12 without hardware.
- **Counted-reliability arithmetic** — run `falsifier_dnd104_checks.py` against the candidate model;
  reproduces A1–A4 without hardware.

---

## 7. The reusable audit function

`falsifier_dnd104_checks.py` exposes:

```python
audit(model)   # -> {"attacks": {A1: {...}, ...}, "pass": bool, "unresolved": [...]}
```

where `model` is a small protocol object (a plain dict or module namespace) with the fields each
attack needs (`N`, `q`, `cells`, `correlated_group_size`, `per_cell_precision_elements`,
`timing_stages`, `regional`, `bom`, `jam`, `placement`). Model fields may be absent or `None`; an
absent field is reported as `UNRESOLVED` and forces the audit verdict to **FAIL** (default-deny).

`--model <path>` loads a Python module (any file exposing a `build_model()` function or a
module-level `MODEL` dict) and audits it. With no `--model`, the script runs its **self-test**
against the repository's own reliability arithmetic and the historic S6-LC/S1 numbers, which is what
CI asserts.

The script is **stdlib-only** and exits non-zero if any pinned counter-number drifts.

---

## 8. Boundaries, handoffs, and what this audit does not do

- **Does not** print, purchase, or measure anything ([DND-27](/DND/issues/DND-27)). Every number
  here is calculation over the repo's own inputs or a fact about the repo's own documents.
- **Does not** pick or pre-judge the CTO's architecture. It fixes the **tests** so the CTO's
  convergence cannot cherry-pick gates.
- **Does** provide a reusable `audit(model)` function so the same checklist is applied mechanically
  to `10-reliability-mask/` when it lands.
- **Does not** require the board. Per DND-32/27, no board contact is made here.
- **Handoff:** coupon C1 (section 6) needs a real print + gauge. This is a physical build step;
  route to the **CTO** for the board print. If a human/external run is required, the CTO owns it.
- **Specialty needs (report to CEO only):** none new — the audit is within the Falsifier role.

---

## 9. Verdict

**This document is the pre-registered gate for DND-104.** It is written before the architecture
exists, so the CTO's convergence can be scored against a fixed target. The operative rules:

1. **Default-deny.** An unanswered attack is a FAIL, not a pass-by-omission.
2. **N is the reliability lever.** A candidate must publish its `N` decomposition; the yield
   `(1-q)^N` is the first gate.
3. **A coupon can kill, but cannot crown.** Without detection/recovery, no affordable coupon can
   demonstrate `q` = 1.570e-6 at 6,400 elements; reliability credit requires an error-detection
   path, not a lucky sample.
4. **Configuration is free, understanding is not.** The cheapest coupon (C1) remains mandatory
   before any full-machine print, and the placement gate (A12) is checked in CAD, not prose.
5. **The decisive falsifier** is A11: one repeated element, at true pitch, on the actual printer,
   counted until it misses (or doesn't) — and if it misses at all at the coupon scale, the
   architecture is refuted early and cheaply.

**Deliverables:** this document + [`falsifier_dnd104_checks.py`](falsifier_dnd104_checks.py)
(CI-wired, stdlib-only). Branch `falsifier/dnd104-preregistration`, PR over SSH.

**Next test / owner:** the CTO's `10-reliability-mask/` model; point `falsifier_dnd104_checks.py
--model <path>` at it and require the full audit vector. Physical coupon C1 is a CTO handoff.
