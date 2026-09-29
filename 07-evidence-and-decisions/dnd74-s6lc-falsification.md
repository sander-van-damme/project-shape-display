# Falsifier adversarial audit — DND-74: the S6-LC ultra-low-cost machine (complement to DND-91)

- **Status:** Independent review (Falsifier). Adversarial, not consensus. A refutation
  is a success; failed ideas are recorded as evidence.
- **Date:** 2026-09-29.
- **Owner:** Falsifier (agent `49e3be36`).
- **Target of record:** `09-low-cost-variant/s6lc/` — model `analysis/s6lc.py`, gate
  `analysis/s6lc_checks.py` (29 checks), BOM `bom_s6lc.csv`, CAD
  `scad/s6lc_machine.scad`, rendered under `cad/`. Produced by the CTO on
  [DND-72](/DND/issues/DND-72), consolidated by [DND-83](/DND/issues/DND-83).
- **Issue:** [DND-74](/DND/issues/DND-74). Prior Falsifier audits:
  [DND-5](/DND/issues/DND-5), [DND-36](/DND/issues/DND-36), [DND-46](/DND/issues/DND-46).
- **Relationship to the sibling audit [DND-91](/DND/issues/DND-91).** The sibling
  [`dnd91-s6lc-falsification.md`](dnd91-s6lc-falsification.md) (PR #75, on `main`) audits the
  *same* target and **supersedes** this report on the pawl geometry and cell fit: its **A1**
  shows the SCAD pawl overflows the pitch band (`PAWL_T` 0.90 > owned 0.74 mm lane), and its
  **A2** shows the SCAD leaf is `PAWL_T/2 = 0.45 mm`, so the true release is ~0.020 N, 8x
  softer than the model's 0.160 N. This report therefore **defers to DND-91 on A1/A2** and does
  **not** re-assert the 0.160 N figure as physics; where it uses the model's constants it is to
  test the *model's internal consistency*, which is the point of the one new break below.
- **Unique contribution of this report.** DND-91 audits the lift axis only under the
  "platen-unloaded" product assumption (its A7). It does **not** find that `lift_axis()` is
  sized on **one bank (800 cells)** while the write is **global over 6,400**. That factor-8
  load error is **Attack 2 below** and is the decisive new finding. Attacks 1/3/4/6/7 are
  stated as **convergent confirmations** of DND-91 A5/A3/A6/A4/A7, flagged as such.
- **Evidence discipline:** every finding below is a **calculation on the repository's own
  declared constants**, or a **sourced-fact reading of repository files**. Nothing here
  is measured; nothing here is a physical test. No board contact is made or requested.

This document is hostile to S6-LC. Its job is to find where the machine's own numbers
are wrong, circular, or silently reach outside the stated evidence class — before the
board spends a print on it.

**Reproduce:** `python3 07-evidence-and-decisions/falsifier_dnd74_checks.py`
(pure standard library, asserts every finding below).

---

## Headline

**Seven attacks. One is a new, decisive break; the rest are bounded or convergent with
DND-91.** The decisive new break is **Attack 2**: the lift-axis gate (`G3`) was computed on
**one bank's worth of cells (800)** while the mechanism writes the **whole 6,400-cell board**
in one platen stroke. Correcting that input fails G3 by ~5.4x (needs >=1.63 N·m vs a 0.30 N·m
NEMA17). DND-91 does not find this (it audits the lift axis only under the unloaded-product
assumption, its A7). The remaining attacks here **converge with** DND-91 (marked *conv.*) or
are bounded. Timing and geometry survive; the release-force ceiling is circular (Attack 5,
*conv.* A3); the mask-write and regional-update claims reach outside the visible budget in
ways that must be stated as product limitations, not hidden (Attacks 3 and 3b, the latter
*conv.* A8).

**Read this report with DND-91.** Where the two disagree, **DND-91 wins on pawl geometry and
cell fit** (its A1/A2); this report wins on the lift-axis load input (its absence).

| # | Attack | Claim under attack | Verdict | Deciding number |
|---|---|---|---|---|
| 1 | Cost ladder honesty *(conv. DND-91 A5)* | $139.77 parts / $162.13 delivered | **survived (bounded)** | +$69 honest allowances -> $242.17 delivered, $7.83 headroom |
| 2 | **Lift-axis sizing (G3)** — *new* | 0.30 N·m motor, 1.47x margin | **BROKEN (new)** | 6,400 cells x 0.4 N = 2,560 N -> >=1.63 N·m; 4 screws -> 0.41 N·m each > 0.30 |
| 3 | Mask-write product statement — *new angle* | "off-line, 7.4 s visible" | **bounded-needs-measurement** | serial punch 2,560 s; 30 s prep needs 427 ops/s |
| 3b | Regional updates *(conv. DND-91 A8)* | "bank-local replay" | **BROKEN (claim), mechanism bounded** | one global platen => 7 other banks must be masked "no-change" |
| 4 | No per-cell feedback / reliability *(conv. DND-91 A6)* | implicit "all cells correct" | **bounded-needs-measurement** | p=1e-4 -> P(all 6,400 correct)=52.7% |
| 5 | Release-force ceiling *(conv. DND-91 A3)* | "128 N vs 296 N ceiling" | **BROKEN (provenance)** | 296 N is S1's own banked *output*, not an independent limit |
| 6 | Timing completeness *(conv. DND-91 A4)* | 7.4 s full map | **survived (bounded)** | +4 mask-index moves -> 8.4-11.4 s, still <30 s |
| 7 | Pawl load holding | "pawl holds column against gravity / terrain load" | **bounded-needs-measurement** | see DND-91 A1/A2; geometry itself is broken |

---

## Attack 1 — Cost ladder honesty: **survived, but headroom is thin**

**Claim.** `$139.77` purchased parts, `$162.13` delivered, against a `$250` ceiling.

**Attack.** Re-added every `assumption` / `sourced-class` line from `bom_s6lc.csv` and
priced the capabilities the mechanism *actually needs* that are not on the list:

| Omitted / understated capability | Allowance |
|---|---:|
| Mask index mechanism (rack/pinion/cam + 8 gate linkages) | $15.00 |
| Reset carriage rail + carriage frame hardware | $20.00 |
| 4x screw thrust bearings (axial load ~2,560 N, not priced) | $18.00 |
| Homing/limit switches (only 4 sensors priced for >=6 axes) | $3.00 |
| Cable chain / strain relief for the moving reset carriage | $8.00 |
| Power connector / switch / fuse | $5.00 |
| **Subtotal** | **$69.00** |

**Result.** `$139.77 -> $208.77` parts -> **`$242.17` delivered** at the repo's 1.16
uplift. Still under $250, so the gate holds — but **headroom falls from $87.87 to
$7.83 (3.1 %)**. A single wrong marketplace multipack now busts the ceiling. This is
exactly the DND-46 failure mode (soft "allowance" lines dressed as fact), just not yet
fatal.

**Minimal fix.** Add these lines to `bom_s6lc.csv` as explicit `allowance`-class entries
so the ladder shows the true $7.83 margin, and re-run the `delivered margin >= $50`
check — which will then **fail**. Either the margin check is relaxed with justification,
or the design must shed ~$45 of allowances.

**Note on the silent-free capabilities.** The controller, 3 drivers, PSU, loom,
fasteners and sensors *are* priced. The frame/columns/pawls/masks are printed and
legitimately excluded by [DND-70](/DND/issues/DND-70). The **card puncher** is declared
a "shared tool, not machine BOM" — see Attack 3, where that exclusion is doing most of
the work.

---

## Attack 2 — Lift-axis sizing: **BROKEN** (the decisive finding)

**Claim** (`s6lc.py:lift_axis`, G3 PASS, margin 1.47x). Load = `LIFT_LOAD_N (0.4 N) x
CELLS_PER_BANK (800)` = 320 N, torque 0.204 N·m vs a 0.30 N·m motor.

**Attack.** The mechanism description is explicit that the **write is global**: "one
platen, 4 broadcast 10 mm strokes" (`README.md` §2), `timing()` uses `STROKES = 4` with
`reset_total = BANKS x RESET_S` — i.e. *only the reset is banked*. If the platen strokes
the whole board, it lifts **all 6,400 cells**, not 800. The function silently uses
`CELLS_PER_BANK` — the reset-bank size — as the write load.

Correcting the input to the mechanism as described:

| Load model | Force | Torque at screw (lead 2 mm, eta 0.5) | vs 0.30 N·m motor |
|---|---:|---:|---|
| `lift_axis()` as coded (800 cells) | 320 N | 0.204 N·m | PASS |
| Global write (6,400 x 0.4 N) | 2,560 N | **1.63 N·m** | **FAIL (5.4x)** |
| Global + pawl cam on advancing cells | 3,584 N | **2.28 N·m** | **FAIL (7.6x)** |
| Global, gravity+pawl only (no 0.4 allowance) | 1,024 N | **0.65 N·m** | **FAIL (2.2x)** |

Even shared across the four belt-synced screws, **each screw needs 0.41 N·m > 0.30
N·m**. The `lift_axis()` gate is wrong by a factor of **8** (6,400 / 800).

**Consequence.** G3 does not pass as written. A corrected model needs a >=1.6 N·m-class
motor (NEMA23-class, ~$25-40) or a genuinely banked write (which then changes the timing
model and the whole "broadcast" premise). This is the S6-LC analogue of S5's K7 motor
cliff from [DND-49](/DND/issues/DND-49): a cost/feasibility path that only closes on an
unpublished parameter.

**Minimal fix (the way DND-46/DND-55 fixed the rack pitch and printed bar).** Pick one
honest branch and re-run the gate:

1. **Keep the global broadcast** -> set `lift_axis` cells to `CELLS` (6,400), size the
   motor to >=1.63 N·m (with >=1.3x margin ~= 2.1 N·m), re-price it (~$25-40), and
   re-check cost. Timing is unchanged.
2. **Bank the write** (8 x 800-cell sub-strokes) -> `lift_axis` at 800 is then correct,
   but the timing model becomes ~8x the armed term and the "4 global strokes" claim and
   7.4 s headline both change; re-run G4.

Either way the current `lift_axis()` + G3 pairing is internally inconsistent and must
not be quoted as a pass.

---

## Attack 3 — The mask-write product statement: **bounded-needs-measurement (and a real dodge risk)**

**Claim.** "Mask preparation is off-line ... the visible transition is 7.4 s." An
unannounced map is "mask-set-time first".

**Attack.** The requirement from [DND-70](/DND/issues/DND-70) is unchanged: "full-map
reconfiguration **strictly < 30 s**". The S1 screen's own test C (adopted here) says an
80-channel writer needs **56 s**, i.e. >30 s. The cheapest shared writer is a card
puncher:

| Prep method | Time | vs 30 s |
|---|---:|---|
| Serial punch, 0.20 s/op, 12,800 ops | 2,560 s (42.7 min) | FAIL 85x |
| Modest puncher, 10 ops/s | 1,280 s | FAIL 43x |
| To fit a 30 s prep | needs **427 ops/s** | — |

So the "off-line" claim is **load-bearing**: without it, setting the map blows the 30 s
budget by two to three orders of magnitude. The README states the limitation honestly
(§6), which is why this is *bounded* rather than *hidden*. But two things must be made
explicit before this is a product:

1. The **double-buffer mode** ("set mask *n+1* while showing *n*") is the only honest
   way the "strictly <30 s" target holds, and it requires the next map to be known
   ~10 s ahead. That is a **product limitation on the operator**, not a machine
   property — it must sit in the criteria, not only in a design caveat.
2. The **card puncher is excluded from the BOM** as a "shared tool". For a 6,400-cell
   map that puncher must output up to 12,800 set-ops; if no 427 ops/s puncher exists at
   hobby cost, the exclusion is a **dodge**, not a shared tool. This is unverified.

**Minimal fix.** State the double-buffer requirement as a first-class product constraint
(input timing), and either (a) quote a real puncher with its throughput and cost, or
(b) demote the <30 s claim to "<30 s for a pre-known next map". Do not let "off-line"
carry the 30 s gate without the product constraint attached.

---

## Attack 3b — Regional updates: **claim BROKEN, mechanism bounded**

**Claim** (`README.md` §4): "Regional isolation | mask gates are per-bank => bank-local
replay".

**Attack.** The write element is **one global platen**. To update only one bank you must
(i) reset that bank, (ii) arm only that bank's mask, and (iii) stroke the **global**
platen four times. On those strokes, every *other* bank's armed cells advance too —
unless all seven other banks' gates are explicitly set to **BLOCK** for every stroke.
That is a **full-board mask operation for the seven "unchanged" banks**, plus a global
platen stroke. It is not "bank-local" in mechanism; it is bank-local only in *which mask
you edit*. Time for a bank update is ~3.9 s (4 strokes + 1 reset), but the mask prep is
still full-board (Attack 3).

**Consequence.** The regional-update requirement can be met, but the stated mechanism is
misleading. Re-state as: "regional update = full-board mask with seven banks held at
'no-change' + global replay", and carry it as a variant of the Attack-3 product
constraint.

**Minimal fix.** Same as Attack 3: make mask content, not just timing, the explicit
regional primitive.

---

## Attack 4 — No per-cell feedback and the 6,400-cell reliability roll: **bounded-needs-measurement**

**Claim** (`README.md` §4, `decide()`): detection is "axis reference sensors only; no
per-cell feedback". A missed pawl is a "silent local height error".

**Attack.** With no per-cell sensing, a board is correct only if **all 6,400 cells are
correct**: `P = (1-p)^6400`.

| Per-cell error p | P(all 6,400 correct) |
|---:|---:|
| 1e-4 (0.01 %) | **0.527** |
| 1e-5 | 0.938 |
| 1.57e-6 (project 99 % goal) | 0.990 |

At a plausible 0.01 % per-cell error, **~47 % of builds have at least one silent error**
that the machine cannot see. The project's own reliability target (`q <= 1.57e-6`) is the
only one that keeps the board correct >=99 % of the time.

**Consequence.** This is inherited by the whole passive-memory family (S5 shares it), so
it is not an S6-LC-unique killer — but S6-LC is *worse* than S5 here because it has **no
writer to verify against** and no scan. A post-map height scan is mentioned
parenthetically in the S1 spec but is **absent from the S6-LC BOM**. Either add a scan
(cost + time not modelled) or state the reliability floor.

**Minimal fix.** Add the height-scan (camera/ToF) as a priced BOM line and a timing term,
or explicitly adopt the project reliability gate `q <= 1.57e-6` as the per-cell
requirement for the pawl decode.

---

## Attack 5 — Release-force ceiling: **provenance BROKEN** (conclusion likely survives)

**Claim** (`release_force()`): "banked all-armed force <= 296 N", G2 PASS.

**Attack.** The number 296 N is **S1's own banked output** (`0.37 N/cell x 800`), used
here as an independent "ceiling". S6-LC then compares its *own* recomputed banked force
(128 N) against it. That is **circular**: the bound is not an independent structural
limit — it is the older variant's result. Note the internal evidence that 296 N was
never a ceiling: S1's *un-banked* all-armed force was 2,368 N, which **exceeds** S1's
own 1,500 N structural cap, yet 296 N (S1's banked reduction) is quoted as if it were a
hard physical limit. S6-LC is softer (all-armed 1,025 N, below the cap), so its banked
result is probably fine — but the gate's *evidence* is not independent.

**Consequence.** G2's *conclusion* (banking bounds reset force) is probably fine because
S6-LC's pawl is softer (0.160 N < S1's 0.37 N), but the **gate's evidence is not valid
as written**. Also: no independent structural limit is stated for the comb / carriage /
pawl-toe at 128 N, and the **reset motor torque is never gated** at all (0.082 N·m
needed through a 2 mm screw — tight for an $8 small stepper, but unmodelled).

**Minimal fix.** Replace the "296 N ceiling" with a stated structural limit derived from
the pawl-toe/comb geometry or a sourced actuator/pawl break rating; add an explicit
reset-carriage torque gate mirroring `lift_axis()`.

---

## Attack 6 — Timing completeness: **survived, but understated**

**Claim.** 7.4 s = 4x(0.5 + 0.15 + 0.20) armed + 8x0.50 reset.

**Attack.** `timing()` contains **no mask-index term**, yet the README says a "mask gate
index motor sets the 8 bank mask gates". Between the four global strokes the gate must
advance to the next threshold; that is at minimum 4 index moves (or 32 if per-bank).
Adding 4 x 0.25-1.0 s gives **8.4-11.4 s** — still comfortably under 30 s, so G4 holds,
but the headline "7.4 s" understates the real cycle.

**Minimal fix.** Add an explicit `MASK_INDEX_S` term to `timing()` and re-quote the
headline; the margin is large enough that this is an honesty fix, not a gate failure.

---

## Attack 7 — Pawl load holding: **bounded-needs-measurement**

**Claim** (`README.md` §2): "a passive printed cantilever pawl that holds the column
against gravity ... Height is stored mechanically — the pawl, not any powered element,
holds terrain load."

**Attack.** The pawl is deliberately **soft** (low release force = low k) to keep the
banked release force down. But a single cantilever's stiffness sets both the release
force *and* the resistance to lateral cam-out. **This test uses the model's declared
constants only for internal consistency; DND-91 A2 shows the real leaf is 0.45 mm (8x
softer), which makes cam-out even easier.** From the model's own constants
(k = 0.641 N/mm, pocket depth 0.8 mm):

- A **0.51 N lateral** load fully cams the toe out of the pocket. With the DND-91 A2
  correction (k ~= 0.08 N/mm) the cam-out threshold is ~0.06 N.
- A 50 g miniature tilted 5 deg gives ~0.04 N lateral — with the corrected k that is a
  large fraction of cam-out. There is also **no stated pocket-roof angle**; S1's own spec
  uses an **8 deg undercut** for one-way holding which *creates* a cam-out component
  proportional to the axial load. S6-LC never states the roof angle, so holding under
  load is undefined.
- Vertical load is carried by the pocket floor in compression, but the model gives no
  bearing stress or creep analysis for a 0.9 x 1.2 mm PLA toe under a sustained
  miniature load over hours.

**Consequence.** Not an immediate kill — a near-flat pocket roof carries most axial load
in compression — but the claim "pawl holds terrain load" is **unquantified**, and DND-91
A2's softer leaf makes it worse. It hinges on a pocket-roof angle and a bearing/creep
budget that are not in the model.

**Minimal fix.** State the pocket-roof angle and add (a) a bearing-stress check on the
toe/pocket shelf at the 5 N abuse load and (b) a creep note; a 10-copy coupon with spring
gauge + 1 N x 1 h hold measurement is the cheapest test (no print allowed in this env —
see DND-91 §6).

---

## What survived, and what it means

- **Not even the "survivors" are safe.** This report alone would say geometry (G1) and
  timing (G4) survive; **DND-91 A1/A2 shows G1 is broken** (pawl overflows the pitch band;
  leaf section wrong by 8x). After both audits, S6-LC's *only* surviving headline is the
  raw cost ceiling — and that is bounded with $7.83 headroom.
- **The machine is not decision-ready.** Two program gates are falsified (G1 by DND-91 A1,
  G3 by Attack 2 here) and G2 rests on circular evidence. The "3 bought actuators / 7.4 s /
  $162.13 / all gates pass" headline must not be quoted.
- **One print would settle the physics, but DND-27 forbids it.** The cheapest test (pawl
  release-force spread, friction, pocket-roof holding, creep) is the S1-style unit-cell
  coupon; DND-91 §6 scopes it. Until a print is permitted, those residuals stay qualitative.

## Evidence-class compliance

| Claim in `s6lc/` | Evidence class claimed | Actual | Compliant? |
|---|---|---|---|
| Geometry / pitch / cell fit | CAD + calculation | DND-91 A1: **CAD overflows the band** | **no (DND-91)** |
| Pawl release 0.160 N | calculation | DND-91 A2: **8x too stiff (leaf 0.45 mm)** | **no (DND-91)** |
| Lift torque 1.47x margin | calculation | calculation, **on 1/8 the load** | **no (Attack 2)** |
| Banked release 128 N vs 296 N | calculation | calculation, circular ceiling | **no (Attack 5)** |
| Full-map 7.4 s | calculation | calculation, missing mask-index | partial (Attack 6) |
| Mask prep off-line | product statement | acknowledged limitation | yes (honest) |
| Pawl holds load | calculation | unquantified (roof angle absent) | **no (Attack 7)** |
| CAD mesh watertight | CAD | real OpenSCAD + trimesh | yes |
| Bought-actuator count 3 | sourced-class | sourced-class, soft lines | partial (Attack 1) |

## Next actions (owner)

1. **CTO** — fix `lift_axis()` (Attack 2, the new break): size for 6,400 cells, or genuinely
   bank the write, and re-run `s6lc_checks.py`. Combine with the DND-91 A1/A2 pawl/CAD fixes.
2. **CTO** — add the honest allowance lines (Attack 1) and either relax the $50 margin check
   or shed cost.
3. **CTO** — add the reset-carriage torque gate and an independent structural limit
   (Attack 5); add a mask-index timing term (Attack 6).
4. **Falsifier (this issue)** — the CI gate `falsifier_dnd74_checks.py` locks the unique
   lift-axis finding so a silent re-quote cannot return.
5. **Print authority** — a unit-cell coupon (DND-91 §6) is the mandatory cheapest test; no
   print is permitted in this environment ([DND-27](/DND/issues/DND-27)).

## Residual uncertainties (cannot be closed analytically; DND-27)

- Pawl release-force spread across 6,400 parts (S1-D): only a coupon measures it.
- As-printed pocket-roof angle, friction mu, creep: measurement-only.
- Whether any hobby card puncher reaches ~427 ops/s (Attack 3): unverified.
- Whether the corrected (DND-91 A2) soft pawl can hold load at all: measurement-only.
