# DND-91 - Adversarial falsification audit of the selected machine S6-LC

- **Issue:** [DND-91](/DND/issues/DND-91) (Falsifier). Parent [DND-84](/DND/issues/DND-84).
  Supersedes the mis-targeted [DND-74](/DND/issues/DND-74) "S5-R variant" audit; DND-74's own
  description is repointed to this same S6-LC target (see section 7).
- **Target of record:** `09-low-cost-variant/s6lc/` on **main** (PR #69 merged; at audit time
  `origin/main` = `77692c6`, later `038360e`). Model `analysis/s6lc.py`, gate
  `analysis/s6lc_checks.py` (29 checks), BOM `bom_s6lc.csv`, CAD `scad/s6lc_machine.scad`.
  The "S5-R variant" trim (`s5r_ultra.py`) is the **retained negative result**, not the deliverable.
- **Headline under attack:** $139.77 parts -> **$162.13 delivered**, 3 bought actuators, 50 mm
  travel, **7.4 s** full map, banked worst-case release **128.2 N vs 296 N ceiling**, all six gates
  pass, `verdict = PROMOTE_TO_09`.
- **Evidence class of this audit:** **CALCULATION / adversarial re-derivation** over the repo's own
  model, CAD source and BOM, plus **sourced-class fact observations about the repository's own
  documents**. Nothing here is printed, purchased or measured ([DND-27](/DND/issues/DND-27)).
  The audit is deliberately hostile; a refutation is a success.
- **Gate:** [`falsifier_dnd91_checks.py`](falsifier_dnd91_checks.py) (CI-wired). It asserts the
  counter-numbers below, so the prose cannot drift from the arithmetic - the same convention as
  [`falsifier_s5_review_checks.py`](falsifier_s5_review_checks.py) and the DND-46 gate.

## Verdict summary

| # | Attack | Claim under attack | Verdict | Number that decides it |
|---|---|---|---|---|
| A1 | **Cell fit / lane budget** | "pawl+bleed 1.30 <= lane 1.48, cell fits" | **BROKEN** | CAD pawl reaches **2.80 mm** from centreline vs half-pitch **2.54 mm** -> overflows **0.260 mm** into the neighbour band. Owned lane is only **0.74 mm**. |
| A2 | **Pawl spring arithmetic** | release 0.160 N from a 0.90 x 1.20 x 8.00 leaf | **BROKEN (factor 8)** | CAD leaf is **0.45 mm** in the bending axis (`PAWL_T/2`), not 0.90. True release ~ **0.020 N**, 8x softer than modelled. |
| A3 | **296 N release "ceiling"** | "128.2 N vs 296 N ceiling, 2.3x margin" | **BROKEN (circular)** | 296 N = **0.37 N/cell x 800**, borrowed from the *old S1 pawl*; not a sourced strength limit on the comb. |
| A4 | **Full-map timing** | "7.4 s, 22.6 s margin" | **BOUNDED / optimistic** | Mask index, reset-carriage **traverse** and mask re-index are unpriced. Model is 4 strokes + dwells only. |
| A5 | **Cost ladder honesty** | "$139.77 parts / $162.13 delivered" | **BOUNDED-NEEDS-SOURCING** | Softest lines repriced to plausible retail: **$196.93 delivered** (margin $53.07), plus **unlisted** mask media, puncher, gate linkage, splice hardware. |
| A6 | **Per-cell reliability** | implicit "all 6,400 correct" | **BROKEN AS STATED** | At 0.01 % per-cell error, **P(all correct) = 52.7 %**. No per-cell feedback -> silent errors are undetectable. |
| A7 | **Tabletop load during write** | "platen assumed unloaded while writing" | **BROKEN vs requirement** | A battle map has minis **on** the map; load fights the lift axis. The assumption contradicts the product. |
| A8 | **Regional update / jam containment** | "per-bank mask => bank-local replay" | **BOUNDED-NEEDS-MEASUREMENT** | A jammed column does not drop on reset; no feedback. One jam silently corrupts its bank. |

**Bottom line.** S6-LC's headline is **not** physically validated and **cannot be** under DND-27.
Two claims are **broken outright** (A1 cell fit; A2 pawl arithmetic - the two numbers the whole
release/timing/cost story rests on), two more are **broken as stated** (A3 ceiling circularity, A6
reliability), and the remainder are **bounded but need physical measurement**. S6-LC survives as a
*definition*, but its cheapest rejection test (a printed unit-cell coupon, section 6) is now
mandatory before any board print of the full machine.

---

## A1 - Cell fit: the lane gate ignores placement; the CAD overflows the pitch band (BROKEN)

**Claim under attack** (`s6lc.py:161-183`, locked by `s6lc_checks.py:51-56`):

> `lane_free = PITCH - BODY = 1.48 mm`; `pawl+bleed = PAWL_T + 2*0.20 = 1.30 mm <= 1.48` ->
> "pawl + bleed fits the lane" -> "cell fits overall" PASS.

**Attack.** `lane_free` is `PITCH - COLUMN_BODY = 5.08 - 3.60 = 1.48 mm`, i.e. the gap from *this*
column's body edge to the *next* column's body edge. But a cell owns only **half** of that gap in
the +X direction: from the body edge to its own half-pitch is `5.08/2 - 3.60/2 =` **0.74 mm**. The
model never checks placement - and the CAD does not place the pawl inside the body-adjacent
0.74 mm. The SCAD is explicit (`s6lc_machine.scad:99`):

```scad
translate([BODY/2 + 0.10, 0, 4]) pawl();   // pawl origin at 1.90 mm from centreline
```

The pawl is `PAWL_T = 0.90 mm` thick in X, so its outer face reaches `1.90 + 0.90 =` **2.80 mm**
from the centreline. The cell's half-pitch is **2.54 mm**.

> **The S6-LC pawl overflows its own pitch band by 0.260 mm and intrudes into the neighbouring
> cell's lane**, in the very direction the gate claims to have checked. The pawl thickness alone
> (0.90 mm) already exceeds the owned lane (0.74 mm) by 0.16 mm.

**Why the gate missed it.** `column_fit()` compares the *pawl thickness plus symmetric bleed*
against the *whole* inter-body gap, implicitly assuming the pawl is centred in that gap and that
the neighbour contributes nothing. The real constraint is
`PAWL_T <= (PITCH/2 - BODY/2) = 0.74 mm`, which the 0.90 mm leaf fails by itself. The
`gate_plus_bleed` check has the same structural flaw (the gate is claimed "stacked in Z", so it
does not consume the pitch band - plausible, but asserted, not shown).

**Consequence.** The pitch claim for S6-LC is **not established**. It is inherited from the S1
coupon's "body 3.60 + lane 1.48 = 5.08" budget, but S6-LC's pawl is thicker (0.90) than the S1
budget's pawl leaf and is placed outward instead of in the owned lane.

**Minimal fix (analogue of the DND-46/DND-55 pitch fix).** Either
(a) reduce `PAWL_T` to <= 0.44-0.45 mm **and** place the pawl within the owned 0.74 mm lane, which
changes A2's spring constant (softer), or (b) reduce `COLUMN_BODY` so the owned lane >= pawl
thickness, or (c) redesign the pawl to be stacked in Z over the column (like the gate), removing it
from the X budget. Any of (a)-(c) must be re-gated. **Cheapest test:** print a 4x4 unit-cell coupon
and measure the as-printed column-to-pawl clearance and neighbour interference (section 6).

## A2 - Pawl spring uses the root block's cross-section, not the leaf (BROKEN, factor 8)

**Claim under attack** (`s6lc.py:135-158`):

> `I = w*t^3/12` with `w = PAWL_W = 1.20`, `t = PAWL_T = 0.90`, `L = 8.00` -> `k = 0.6407 N/mm`
> -> release at 0.25 mm deflection = **0.1602 N** -> "per-pawl force 0.160 <= 0.234 design ceiling".

**Attack.** The CAD leaf is **not** 0.90 mm in the bending axis. `pawl()` is
(`s6lc_machine.scad:52-57`):

```scad
translate([0, 0, 0])    cube([PAWL_T,     PAWL_W, 1.5]);    // root block: 0.90 x 1.20 x 1.5
translate([0, 0, 1.5])  cube([PAWL_T/2,   PAWL_W, PAWL_L]); // leaf:       0.45 x 1.20 x 8.0
```

The load-bearing cantilever - the 8.0 mm leaf - has bending thickness `PAWL_T/2 = 0.45 mm`, not
0.90. Recomputing with `t = 0.45`:

| Section | k (N/mm) | Release @ 0.25 mm |
|---|---:|---:|
| Model (`t = 0.90`) | 0.6407 | **0.160 N** |
| **CAD leaf (`t = 0.45`)** | 0.0801 | **0.020 N** |

The model overstates the second moment of area by `2^3 =` **8x**. The root block (0.90 mm) is only
1.5 mm tall, so it governs a negligible fraction of the cantilever; using 0.90 for the whole leaf is
wrong.

**Consequence.** Because `k` scales as `t^3`, *every* force number downstream moves:
- true per-cell release ~ **0.020 N**, 8x below the "0.160 N" reported;
- true banked all-armed ~ **16 N**, not 128.2 N;
- true unbanked all-armed ~ **128 N**, not 1,025 N.

A softer pawl sounds *better* for release force - **but it is worse for A3/A8**: an 0.020 N pawl may
not reliably hold a column against gravity + terrain load at all, and the whole "passive pawl holds
height" premise depends on this number. The model's error is not conservative in either direction:
the pawl must be **soft enough to release** and **stiff enough to hold**, and S6-LC has never
checked the hold side (there is no hold-force gate in `s6lc.py`).

**Minimal fix.** Make `pawl_spring()` read the actual CAD leaf section (t = PAWL_T/2) and add a
**hold-force gate**: `k * deflection_at_pocket <=` load per column (column mass + terrain load).
The present model has no hold gate at all.

## A3 - The 296 N "ceiling" is borrowed from a different pawl (BROKEN, circular)

**Claim under attack** (`s6lc.py:186-196`, `s6lc_checks.py:61-64`, README section 5):

> "Worst-case release force: 128.2 N banked vs **296 N ceiling**, 2.3x margin" -> G2 PASS.

**Attack.** 296 N is not an independent structural limit. It is defined in the S1 study as
**0.37 N/pawl x 800 cells** (`S1_S2_spec.md:74-78`) - the per-cell design value of the *S1* pawl.
S6-LC then computes its *own* per-cell force (0.160 N, or 0.020 N after A2) and compares its
product to a ceiling derived from a **different** pawl's per-cell force. There is no sourced
strength limit anywhere for the release-comb tooth bending, the comb bar, the travelling carriage,
the comb actuator torque, or the platen. So the "296 N ceiling" is a consistency check between two
studies, not a physical ceiling, and "2.3x margin" is not a structural claim.

`sensitivity()` also reports `release_force_headroom_n = 296 - 128.2 = 167.8 N` and
`banked_ceiling_n = 296.0` as if sourced. Neither is.

**Consequence.** Banking still *reduces* force proportionally; that part of the argument is sound.
But pass/fail is decided against a self-referential number, so G2 is a **tautology**, not a gate.
With a real ceiling (a 0.88 mm PLA comb tooth, or the reset motor stall torque), the margin would be
recomputed against it - and after A2 the per-cell force changes 8x, so the actual banked force could
be 16 N or 1,025 N depending on which pawl is real. The gate cannot tell which.

**Minimal fix.** Replace `banked_ceiling_n = 296.0` with a sourced/computed limit for the actual
load path (comb tooth bending + carriage actuator torque), and label it `assumption` until measured.

## A4 - Full-map timing is a four-stroke dwell model; the mask machinery is not priced in time (BOUNDED / optimistic)

**Claim under attack** (`s6lc.py:219-238`): `full_map_s = 4*(0.5 + 0.15 + 0.20) + 8*0.50 = 7.4 s`,
22.6 s margin, G4 PASS.

**Attack.** The model prices exactly: 4 platen up-strokes (0.5 s each), 4 settles, 4 returns, and
8 bank resets (0.50 s dwell each). It prices **nothing** for:
- the **mask-index motor** moving between the 4 broadcast strokes (the pattern must change per
  stroke: "four binary masks encode five heights", `s6lc.py:55-57`), and
- the **reset carriage traverse** across the 406.4 mm board between the 8 banks - only the 0.50 s
  *dwell* is paid, not the travel, and
- **mask re-index after reset** to load the next map's medium.

These are all *assumption*-class terms, unmeasured. They probably do not breach 30 s - the margin is
large - but the honest claim is "**7.4 s of mechanism dwell, plus unpriced mask/traverse
overheads**", not "7.4 s full map". `sensitivity()` even reports
`max_banks_for_30s_at_reset_s = 53`, i.e. the timing gate would tolerate 6x more banks - a sign the
model's margins are dominated by assumed constants, not a measured cycle.

**Consequence.** G4 is **BOUNDED**: it holds if the unmeasured overheads total < 22.6 s. That is
almost certainly true, so this attack does **not** kill S6-LC. It does mean "7.4 s" must be labelled
a calculation over assumed dwells, and the **regional-update timing (one bank) is entirely
unmodelled** despite regional updates being a mission requirement.

## A5 - Cost ladder: no outright lie, but soft lines and unlisted capabilities (BOUNDED-NEEDS-SOURCING)

**Claim under attack** (`bom_s6lc.csv`): $139.77 parts -> **$162.13 delivered**, margin $87.87.

**Attack (DND-46 method: reprice the softest lines, restore unlisted capabilities).**

*Repricing the softest `sourced-class` lines to plausible defensible retail* (the DND-46 E6 failure
mode - bundled lines priced at best case):

| Line | BOM | Plausible | Delta |
|---|---:|---:|---:|
| 4x T8 lead screw + anti-backlash nut | $24.00 | $40.00 | +$16.00 |
| Guide rods + bushings (platen) | $14.00 | $22.00 | +$8.00 |
| Timing belt + 2 pulleys | $12.00 | $14.00 | +$2.00 |
| Lift motor (NEMA17-class) | $12.00 | $14.00 | +$2.00 |
| Motor couplers + thrust washers | $6.00 | $8.00 | +$2.00 |
| **Subtotal** | **$68.00** | **$98.00** | **+$30.00** |

Repriced: parts **$169.77** -> delivered **$196.93**, margin **$53.07**. Still < $250, so the
*headline does not break* - but the margin shrinks by 40 % and these are the exact soft lines the
DND-46 audit broke on S5.

*Capabilities absent from the BOM entirely* (all real, all required for the machine to function):

| Missing capability | Why it is real | Status in BOM |
|---|---|---|
| Mask medium / punched cards | one medium per map level; a consumable | called "printed", no line |
| Card puncher | the model itself calls it a "shared tool, not machine BOM" | excluded by declaration |
| Mask-gate actuation linkage | 8 bank gates vs 1 mask-index motor | unpriced |
| Reset-carriage traverse rails | carriage travels 406.4 mm; only a comb is priced | folded into "guide rods" |
| Printed-sub-tile splice hardware | 406 mm frame printed as 4 sub-tiles | only "M3 assortment $8" |
| Per-cell height verification | admitted absent ("no per-cell feedback") | \$0 - by design |

The "printed parts are excluded" rule is legitimate per DND-70, but **the mask medium and frame
splice hardware are not obviously printable-and-excluded**: the punched card is a purchased
*consumable* if it is a card, and any non-printed splice/metrology is a purchased capability. At a
minimum these must be labelled `assumption` and bounded, as DND-46 demanded for S5.

**Consequence.** A5 is **BOUNDED-NEEDS-SOURCING**, not broken. The defensible worst case is
**~$197 delivered** (margin $53), still under ceiling; the honest statement is "the < $250 margin is
$53-88 depending on sourcing, and is conditional on the mask medium and splice hardware being
printable". The one explicit `assumption` line (spares $8) is *not* the softest line; the softest
are the four bundled `sourced-class` hardware lines.

## A6 - Per-cell reliability: no per-cell feedback, and 6,400 cells compound (BROKEN AS STATED)

**Claim under attack.** S6-LC reports all six gates pass and `PROMOTE_TO_09`; the program's own
reliability model (`06-experiments/test11_falsification_library/reliability.py`) says a map is
correct only if **all 6,400** cells are correct. S6-LC's README (section 9) admits "no per-cell
feedback ... a missed pawl is a silent local height error" but never propagates that to a map yield.

**Attack.** Re-derive the map yield from the program's own numbers:

| Per-cell error q | P(all 6,400 correct) | Expected bad cells/map |
|---|---:|---:|
| 0.01 % (1e-4) | **52.7 %** | 0.64 |
| 0.001 % (1e-5) | 93.8 % | 0.064 |
| 99 %-map budget (1.57e-6) | 99.0 % | 0.01 |

S6-LC has **no per-cell or per-bank feedback** (its own residual list), so an error is invisible and
uncorrectable: the operator cannot know a pawl failed to engage or release. For a machine whose
entire state is 6,400 **independent passive pawls**, the program's own reliability discipline
requires q <= 1.57e-6. S6-LC presents **no evidence** that the as-printed pawl spread meets this -
and A2 shows the modelled spring constant is uncertain by 8x, i.e. the engagement threshold is not
even pinned analytically.

**Consequence.** The reliability gate that the rest of the program applies (`convergence-decision`,
`dnd37`) is **absent from S6-LC's six gates (G1-G6)**. Adding it converts "all gates pass" into
"gates pass **except** the reliability gate, which is unaddressed". This is exactly the class of
omission the Falsifier role exists to catch.

**Minimal fix.** Add G7 (per-cell reliability) to `decide()`, require a stated per-cell error budget,
and state the coupon test that measures pawl engage/release spread (section 6) as the gate's
evidence path.

## A7 - Tabletop load vs "platen unloaded while writing" (BROKEN vs requirement)

**Claim under attack** (`s6lc.py:374-378`, README section 9): "The platen is assumed unloaded while
writing (miniatures off the region being written), otherwise hold and lift compete."

**Attack.** The product is a **tabletop D&D battle map**. D&D is played with miniatures *on* the
map, and the mission explicitly includes **regional updates** - reshaping terrain *under or beside*
placed minis. The S6-LC assumption requires the operator to **remove miniatures from the region
being written** before every update and replace them after. That is:
1. a direct contradiction of the "tabletop battle map in play" use case, and
2. an unquantified operational cost moved outside the machine (like the mask prep dodge).

Quantitatively, the lift axis is sized for `LIFT_LOAD_N = 0.4 N` **per column during a write**
(`s6lc.py:202`) over a bank of 800 cells = 320 N; its computed torque margin is only **1.47x** over
a 0.30 Nm motor (`s6lc.py:208-216`). A miniature is 5-30 g = 0.05-0.3 N; if a mini sits on a column
being lifted, that load is additive. The 1.47x margin has no headroom for a *loaded* map, which the
README already concedes. So the machine is only in-spec **with the miniatures off the moving
region** - a product-level restriction never surfaced as a gate.

**Consequence.** G3 (lift torque) passes **only under the unloaded assumption**, which conflicts
with the use case. The honest disposition is "G3 conditional on minis-off-region; tabletop-in-play
updates are out of spec until the assumption is either dropped (bigger motor / bearing) or the
product requirement is explicitly amended".

## A8 - Regional update and jam containment (BOUNDED-NEEDS-MEASUREMENT)

**Claim under attack** (README section 4, `dnd72-low-cost-synthesis.md:64`): "regional update = one
bank: one mask + one stroke + reset", and "mask gates are per-bank => bank-local replay".

**Attack.**
1. **Jam propagation.** Reset works by lifting every pawl of a bank with the release comb and
   letting gravity drop the columns. A column that is **jammed** (friction, a nicked pocket, a
   speck of debris, static) does **not** drop, and there is no feedback (A6). One stuck column keeps
   its stale height while the rest of the bank resets - a silent error.
2. **Regional update still needs the medium.** A regional update resets one bank and replays its
   mask. But the *new* pattern for that bank comes from the same off-line medium. So "regional
   update" inherits the **off-line mask-prep caveat in full**; the visible bank replay time is only
   part of the operation.
3. **Mask-index motif.** The model has **8 bank mask gates** but **one** mask-index motor
   (`bom_s6lc.csv` line 3, `s6lc.py:280`) - the actuation of 8 separate gates by one motor is never
   specified (cables? a single shared shaft across 406 mm? one card moved bank to bank?). This is the
   mechanism-level analogue of the S1 "mask write" failure, not yet resolved.

**Consequence.** A8 is **BOUNDED-NEEDS-MEASUREMENT**: no number here is proven wrong, but the
regional/jam behaviour is asserted rather than modelled. It requires the coupon (section 6) plus a
one-bank jam-injection test.

---

## 6. Cheapest experiment that can reject S6-LC (the one physical test that matters)

DND-27 forbids purchase/print in the agent environment, but the machine cannot be promoted without
**one** printed coupon. This is the minimal, cheapest test that can kill or bound every broken
claim above. **Hand to the CTO / board for a real X1C print** (PLA, 0.4 mm nozzle, 0.2 mm layers):

**Coupon C1 - unit-cell pitch/spring/engage coupon.**
- **Cells/modules:** one 4 x 4 block (16 cells) at true 5.08 mm pitch, plus an isolated single cell.
- **Parts to print:** 16 columns with 5-pocket racks, 16 pawls, one 80 mm mask-gate strip, one
  80 mm release comb. Dimensions per `s6lc_machine.scad` (BODY 3.60, PAWL_T 0.90/0.45, RACK pocket
  0.8 x 3.0, pitch 5.08).
- **Purchased parts:** none (pure print + a digital caliper + a push-pull gauge / kitchen scale).
- **Measurements:**
  1. as-printed column body, lane clearance, and **neighbour interference** (caliper; checks A1);
  2. **pawl release force** by pushing a column through a pocket with a push-pull gauge (checks A2);
  3. **pawl hold force** - load a column with weights until it slips (checks the missing hold gate);
  4. **engage reliability**: cycle one cell 100x and count engages/releases that seat correctly;
  5. **release-force spread** across the 16 pawls (sd as % of mean) (checks the S1-D 9 % break-even).
- **Pass/fail thresholds:** A1 pitch band must show **zero** neighbour contact; A2 measured release
  within 2x of the model (0.020-0.040 N); hold force >= the per-column design load; engage rate
  **100 %** over 100 cycles to extrapolate toward q <= 1.57e-6; spread sd <= 9 %.
- **Repetitions/cycles:** 100 engage/release cycles per cell on 4 cells (400 total); 3 coupons to
  capture print-to-print variation.
- **Full-scale assumption tested:** that a printed passive pawl can, at 5.08 mm pitch, simultaneously
  fit, release at a consistent force, hold under load, and repeat >100x without a silent miss.
- **Consequence of passing:** S6-LC's A1/A2/A6/S1-D risks are bounded; the full-machine print can be
  green-lit for the board's winner print.
- **Consequence of failing:** S6-LC is **refuted** at the single-cell level before any full build;
  the minimal fix (pawl redesign / pitch re-budget) is needed, or the architecture is abandoned.

A second, cheaper **non-physical** test (runnable now, no print):
- **CAD clearance sweep** - re-render `s6lc_cell.stl` at the true placement and assert no X-overlap
  with the neighbouring cell at the pitch lattice; this alone reproduces A1 without hardware.
- **Hold-force gate** - add the missing `k * deflection <= load` gate to `s6lc.py` and re-run; this
  alone reproduces the A2 hold-side gap.

## 7. Boundaries, handoffs, and what this audit does not do

- **Does not** print, purchase, or measure anything ([DND-27](/DND/issues/DND-27)). Every number is
  calculation over the repo's own inputs or a fact about the repo's own documents.
- **Does not** overturn the *selection* of S6-LC over the folded divergence - A1/A2 are defects of
  S6-LC's current numbers, not proof that the S1-broadcast family cannot work.
- **Does** repoint [DND-74](/DND/issues/DND-74) to S6-LC and record this audit as its result.
- **Handoff:** coupon C1 (section 6) needs a real print + gauge. This is a physical build step;
  route to the **CTO** for the board print. Per DND-32/27, no board contact is made here.
- **Specialty needs (report to CEO only):** none new - the audit is within the Falsifier role. A
  failure-analysis / metrology specialist is **not** required; a caliper and a push-pull gauge suffice.

## 8. Verdict

**S6-LC is NOT ready to print as a full machine on this evidence.** Its own 6-gate screen omits the
reliability gate the rest of the program enforces, and two of its load-bearing numbers (cell fit and
pawl release force) are wrong as written. The correct disposition is:

- **Retain S6-LC as the selected *definition*** (it is the most conventional of the surviving
  cheap architectures and its cost story is defensible at ~$197 delivered).
- **Reject its "all gates pass / PROMOTE_TO_09" headline as an unqualified claim.** Restate as:
  "G1-G6 pass under stated assumptions; **G1 (cell fit) and G2 (release force) are invalid as
  derived**; G7 (reliability) is absent; G4/G3 are conditional on unmeasured/contradictory
  assumptions."
- **Mandatory next step:** coupon C1 (section 6) before any full-machine print.
