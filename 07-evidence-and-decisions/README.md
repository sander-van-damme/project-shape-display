# 07 — Evidence and decisions

This stage consolidates what the project has actually learned.

It should distinguish:

- external precedent from project-specific evidence;
- calculation, simulation and CAD from physical measurement;
- validated findings from remaining assumptions;
- a rejected **specific hypothesis** from rejection of an entire mechanism family;
- architecture comparisons from product qualification.

The evidence here should update the knowledge sections in stages 03 and 04 and determine what is allowed to enter [`08-integrated-designs/`](../08-integrated-designs/README.md).

The **Evidence matrix** below is the compact status view. The **Architecture investigation** section records fuller system-level reasoning.

> **Path relocation note ([DND-117](/DND/issues/DND-117), 2026-09).** Records written before the
> DND-117 restructure refer to the old top-level stages `08-current-design/`,
> `09-low-cost-variant/` and `10-reliability-mask/`. Those stages were retired; their content now
> lives at [`08-integrated-designs/s5r-shared-drive-register/`](../08-integrated-designs/s5r-shared-drive-register/README.md),
> [`06-experiments/test14_low_cost_program/`](../06-experiments/test14_low_cost_program/README.md)
> (with the selected S6-LC machine at [`08-integrated-designs/s6lc-low-cost/`](../08-integrated-designs/s6lc-low-cost/README.md)),
> and [`08-integrated-designs/a1-reliability-first/`](../08-integrated-designs/a1-reliability-first/README.md)
> respectively. Historical wording in individual ADRs is preserved; where a link still says
> `08-current-design/` the target is repointed to the current location.

## Evidence matrix

| Item | Sourced | Calculated | Simulated | CAD checked | Printed | Measured | Lifetime tested |
|---|---:|---:|---:|---:|---:|---:|---:|
| M-012 / A-001 rotary-stop architecture | ✓ | ✓ | ✓ | ✓ | — | — | — |
| M-001 travelling multi-row screen | — | ✓ | ✓ | — | — | — | — |
| Test11 final-pitch selector fan-out (S3/S4) | — | ✓ | — | ✓ | — | — | — |
| M-013 perforated height plates | conceptual | partial | — | — | — | — | — |
| M-003 bistable latch family | ✓ | — | — | — | — | — | — |
| M-005 compliant snap-through family | ✓ | — | — | — | — | — | — |
| M-008 shared shaft/clutch family | ✓ | — | — | — | — | — | — |
| M-016 mechanical-memory lattice | ✓ | — | — | — | — | — | — |
| P-010 lock-after-reconfigure precedent | ✓ | — | — | — | — | — | — |
| Test10 mechanism-neutral scale bounds | — | ✓ | — | — | — | — | — |
| Test11 S1–S5 purchased-BOM cost model | ✓ | ✓ | — | — | — | — | — |
| Test11 critical-part sourcing (motors, drivers, couplers) | ✓ | — | — | — | — | — | — |
| Test11 5.08 mm printability & reliability screens | — | ✓ | — | — | — | — | — |
| Test11.1 three-scenario delivered BOM (DND-11) | ✓ | ✓ | — | — | — | — | — |
| Test11 S3/S4 shared-drive machines and rejection gates (cad/coupon, unrendered/unprinted) | — | ✓ | — | ✓ | — | — | — |
| Test11 S5 five-gate status + $1.058 motor ceiling | — | ✓ | — | — | — | — | — |
| Test11 S1/S2 rejection screen | — | ✓ | — | ✓ | — | — | — |
| Test11 printable 5.08 mm coupon | — | ✓ | — | ✓ | ✓ | — | — |
| Test12 winner convergence stack-up (S5) | — | ✓ | ✓ | ✓ | — | — | — |
| Test13 Step-6 load/structure/power, spliced beam (DND-43) | — | ✓ | ✓ | — | — | — | — |
| DND-74 S6-LC falsifier audit (lift sizing, cost headroom, mask write) | ✓ | ✓ | — | — | — | — | — |
| DND-104 reliability-first architecture screen (A1–A7; silent-error gate) | ✓ | ✓ | — | ✓ | — | — | — |
| DND-104 A1 binary-latch + shared writer/reader (selected candidate) | ✓ | ✓ | — | ✓ | — | — | — |
| DND-111 A1 writer/reader rate + single-cell read bound (analytic + CAD) | ✓ | ✓ | — | ✓ | — | — | — |
| DND-112 independent audit of the DND-111 rate/read bound (rate clean; read FAIL) | ✓ | ✓ | — | ✓ | — | — | — |

**Test13 (DND-43) Step-6 structural/drive findings (calculated, not measured).** Adding the
bolted-splice term to the platen/frame beam model changes the winner's structure and drive
spec: at the soft printed modulus the 203.2 mm support spacing assumed in
the integrated design [`08-integrated-designs/s5r-shared-drive-register/`](../08-integrated-designs/s5r-shared-drive-register/README.md) fails the 0.25 mm flatness gate
(**0.514 mm**), so the axis needs **≤ ~150 mm** support spacing (3 cartridges/axis) or a
stiffer rail; and the Test09 **8 mm** lift lead fails the torque-speed gate (**0.51×** margin
against the sourced motor allowance), needing a **≤ 2 mm** lead or a larger motor. A power cut
is **not** self-held at 8 mm lead (`tan λ = 0.318 > μ ≈ 0.15`), so a brake/detent is now a
required item. Full record: [`06-experiments/test13_step6_load_structure_power/`](../06-experiments/test13_step6_load_structure_power/).

External mechanism precedent is not evidence that the shape-display implementation
works. Update this matrix when project evidence changes.

The S1 release-force input remains the **release-force spread across many identical pawls**,
whose break-even is ≈ 9% sd. Under [DND-27](/DND/issues/DND-27) there is no coupon to measure it;
this is a permanently qualitative risk recorded in
[ADR-001 §5.2](convergence-decision-2026-09.md).

### Convergence decision (CTO, 2026-09-28)

**Superseded by [ADR-002](convergence-decision-2026-09-b.md) ([DND-35](/DND/issues/DND-35)): S5 is
promoted to `08-current-design/` (the single-winner stage since retired by [DND-117](/DND/issues/DND-117); now [`08-integrated-designs/s5r-shared-drive-register/`](../08-integrated-designs/s5r-shared-drive-register/README.md)) as the single buildable winner.**
ADR-001 (below) recorded the earlier "no promotion" posture and is preserved as the search record.

**No survivor was promoted under ADR-001.** See
[`convergence-decision-2026-09.md`](convergence-decision-2026-09.md) (ADR-001) and the ranked
elimination order in [`convergence-plan.md`](convergence-plan.md). S1–S5 are one bet in five shapes:
a passive, printable, final-pitch state/selection element written by a small shared programmer and
able to hold load without powered holding. The field is unsupported on regional isolation
(unmeasured), release-force variation (≈9% sd break-even), and matched delivered cost (<$500).

### Falsifier adversarial audit of the convergence logic (2026-09)

[`falsifier-adversarial-audit-2026-09.md`](falsifier-adversarial-audit-2026-09.md) independently
attacks ADR-001's selection logic and the survivors' killer list (per [DND-35](/DND/issues/DND-35)).
Three findings, all **calculation/sourced**, body review, no physical evidence:

1. **"One bet in five shapes" is false for S5.** S1–S4 are *written passive memory* (Bet A); S5 is
   *absolute geometric stops* (Bet B). Their killers do not overlap, so a Bet-A failure does not
   imply a Bet-B failure and should not alone trigger a product re-scope. Run S5's gates in parallel.
2. **The "$500 rejects every survivor" verdict is an artifact for S1/S2/S4.** Their working BOMs
   include $192–$224 of *fallback* purchase for parts the designs explicitly intend to print. Cost
   for S1/S2/S4 is therefore **undetermined pending the print gate**, not failed. (S3's rejection
   and the sourced $40 8 mm-motor finding stand.)
3. **Reliability helper convention was inverted** (`zero_failure_trials` returned the ~58× weaker
    legacy formula). Fixed and pinned to the 1.91 M headline in this branch.

### Falsifier adversarial audit of the S6-LC ultra-low-cost machine (DND-74, 2026-09)

[`dnd74-s6lc-falsification.md`](dnd74-s6lc-falsification.md) is the **complement to the
DND-91 audit below**: it adds the one break DND-91 did not find — the lift-axis gate is
sized on 1/8 the load — and converges with DND-91 on cost, ceiling, timing, reliability
and regional behaviour. Reproducible checks:
[`falsifier_dnd74_checks.py`](falsifier_dnd74_checks.py) (24 checks, CI-gated). Target:
[`08-integrated-designs/s6lc-low-cost/`](../08-integrated-designs/s6lc-low-cost/README.md)
([DND-72](/DND/issues/DND-72)/[DND-83](/DND/issues/DND-83)).

**Unique break — lift-axis gate G3.** `lift_axis()` computes the platen load on
`CELLS_PER_BANK` (800) while the mechanism writes the **whole 6,400-cell board** in one
global stroke. Corrected, the load is 2,560 N → **≥1.63 N·m** needed vs a 0.30 N·m NEMA17
(0.41 N·m per screw on four screws) → **fails 5.4×**, even gravity+pawl only fails 2.2×.
DND-91 audits the lift axis only under the unloaded-product assumption (its A7); this
factor-8 input error is new.

**Convergent with DND-91:** cost headroom collapses $87.87 → **$7.83** with +$69 honest
allowances; the "296 N ceiling" is circular (DND-91 A3); the regional update is not
bank-local (A8); the mask write is load-bearing (2,560 s serial punch; 30 s needs 427 ops/s);
no per-cell feedback gives P(all 6,400 correct) = **52.7 %** at 0.01 % (A6); timing survives
even with mask-index overhead (A4). This report **defers to DND-91 A1/A2 on pawl geometry
and cell fit** (the SCAD leaf is 0.45 mm and overflows the pitch band).

The correct next step is a CTO fix to `lift_axis()` (or a genuinely banked write), combined
with the DND-91 pawl/CAD fixes, then a re-run of the S6-LC gate.

**Fixed by [DND-93](/DND/issues/DND-93) (2026-09).** The lift axis is now sized on the whole
6,400-cell board (G3 passes, NEMA23-class, 1.35×); the six allowances are in the BOM and the
release ceiling is an independent comb-tooth limit. **G6 delivered cost now fails at $263.05**
(verdict REJECT). The A1/A2 pawl/CAD defects remain open. See
[`dnd93-s6lc-g3-fix.md`](dnd93-s6lc-g3-fix.md); `falsifier_dnd74_checks.py` is re-baselined
(28 checks) to reproduce the attack arithmetic and assert the fix.

### Falsifier review of the S5 promotion (DND-36)

The CTO's [DND-35](/DND/issues/DND-35) convergence (ADR-002, branch
`dnd-35-convergence-winner`, **not yet on `main`**) promotes **S5 — programmed stepped rotary
stops + common lift** to the single buildable winner. The Falsifier adversarial review is
[`falsifier-s5-promotion-review-2026-09.md`](falsifier-s5-promotion-review-2026-09.md), with
reproducible checks in [`falsifier_s5_review_checks.py`](falsifier_s5_review_checks.py).

**Verdict: the direction survives; the promotion fails as stated.** S5 is the best-evidenced
candidate, but three of six `closed-analytically` killers are not closed as written — **K1**
(5 N handling screen; Test08 itself says the gate is not established), **K4** (the cited J2 gate
returns `INCONCLUSIVE`; stiction/wear are measurement-only), **K6** (26.251 s is a best-corner of
a 540-case sweep where 84 % of 400 pps cases fail) — and the **cost stack-up has arithmetic and
double-counting defects** (sourced-pair delivered is **$501.12**, over the ceiling, on the repo's
own additive basis; the model's $503.71 uses an inconsistent multiplicative uplift plus a $2.20
subtotal error). The unsourced **$1.05 motor** is the largest existential cost risk (the only
traceable matched part is $40/ea → $3,200 for 80). See the review for the ranked, print-free
falsification experiments.

### Falsifier adversarial audit of S6-LC (DND-91 / DND-74, 2026-09)

The DND-72 consolidation selected **S6-LC** (`08-integrated-designs/s6lc-low-cost/`, $139.77 parts →
$162.13 delivered, 7.4 s full map, `PROMOTE_TO_09`) as the ultra-low-cost machine of record. The
repointed Falsifier audit is
[`dnd91-s6lc-falsification.md`](dnd91-s6lc-falsification.md), with a CI gate in
[`falsifier_dnd91_checks.py`](falsifier_dnd91_checks.py) (35 checks).

**Verdict: S6-LC survives as a *definition*, but its "all gates pass" headline is not valid as
derived.** Eight attacks; the two load-bearing ones are **broken**:

- **A1 cell fit BROKEN** — `column_fit()` compares pawl+bleed against the *whole* inter-body gap
  (1.48 mm), but a cell owns only 0.74 mm to its half-pitch, and the CAD places the 0.90 mm pawl at
  `BODY/2 + 0.10` so it reaches 2.80 mm > 2.54 mm half-pitch: **0.260 mm overflow into the
  neighbour**. The pitch claim is not established.
- **A2 pawl spring BROKEN (8×)** — the model uses the 0.90 mm root block as the bending section, but
  the CAD leaf is `PAWL_T/2 = 0.45 mm`; true `k` is 0.0801 N/mm, release ≈ 0.020 N (8× softer), and
  there is **no hold-force gate** at all.
- A3 the 296 N "ceiling" is `0.37 N/cell × 800` (the old S1 pawl), not a sourced limit → G2 is
  circular. A4 timing prices 4 strokes + dwells only (mask index, carriage traverse unpriced).
  A5 soft BOM lines repriced to plausible retail give **$196.93 delivered** (margin $53), plus
  unlisted mask media / puncher / splice hardware. A6 the program's per-cell reliability gate is
  **absent from S6-LC**: at q=1e-4, P(all 6,400 correct) = **52.7 %**, with no per-cell feedback.
  A7 the "platen unloaded while writing" assumption contradicts a tabletop map with minis on it.
  A8 regional/jam behaviour is asserted, not modelled.

**Mandatory next step:** coupon **C1** (a 4×4 unit-cell print at true pitch + a push-pull gauge)
before any full-machine print — the cheapest experiment that can reject A1/A2/A6/S1-D.

### S6-LC G3 fix and re-run (DND-93, 2026-09)

[DND-93](/DND/issues/DND-93) fixed the decisive G3 defect and the audit's bounded findings, then
re-ran the gate. **G3 now passes** (`lift_axis` sized on all 6,400 cells = 2,560 N → 1.6297 N·m,
NEMA23-class 2.2 N·m, 1.35×). A real comb-tooth structural limit (**413 N**) replaces the circular
296 N; a **reset-carriage torque gate (G7)** was added (0.082 N·m vs 0.16 N·m, 1.96×); the
mask-index and carriage-traverse timing terms are now priced (full map **11.96 s**); and the six
honest BOM allowances (+$69) plus the NEMA23 motor bring delivered cost to **$263.05**. **G6
(delivered < $250) now FAILS by $13.05**: corrected verdict **REJECT**. A1/A2/A6/A7/A8 remain open
mechanism defects. Details:
[`dnd93-s6lc-g3-fix.md`](dnd93-s6lc-g3-fix.md). The DND-91 gate
[`falsifier_dnd91_checks.py`](falsifier_dnd91_checks.py) is re-baselined (40 checks) to assert the
corrected state and keep the open attacks locked.

### Corrected S6-LC purchased BOM, independently re-ratified (DND-98, 2026-09)

[`dnd98-s6lc-bom-reratification.md`](dnd98-s6lc-bom-reratification.md) is the **independent
re-ratification** of the corrected (post-DND-93) S6-LC purchased BOM — supersedes the DND-73
ratification of the uncorrected BOM — CI-gated by
`08-integrated-designs/s6lc-low-cost/ratify/s6lc_bom_reratify_checks.py` (68 checks) with the ratified artifact
`s6lc_bom_ratified.csv`. **Verdict: the `<$250 purchased, excluding 3D-printed parts` mission gate
HOLDS** ($226.77, margin **+$23.23**); the repo's stricter **$250 *delivered* convention FAILS**
($263.05, −$13.05) — both stated, neither hidden. Findings: the +$87.00 growth is the NEMA17→NEMA23
lift-motor re-price (+$18) and the six DND-91/A5 capability allowances (+$69); 65 % of the BOM is now
allowance; the **hostile** pricing scenario breaches the purchased ceiling ($300.58, −$50.58); the
cost cliff is the lift motor (break-even $53.23 = 1.77×); the lead-screw line is under-priced ~$4.76
against its stable order tier; there is **no per-cell bought hardware** (3 motors total, 3.543
cents/cell amortised); and the **99 %-map reliability goal needs per-cell error q ≤ 1.57e−6**, which
remains measurement-gated (G7 unresolved, coupon C1).

### Pre-registered adversarial audit criteria for DND-104 (DND-108, 2026-09)

[`falsifier_dnd104_criteria.md`](falsifier_dnd104_criteria.md) is the **frozen, pre-registered**
attack list for the reliability-first program [DND-104](/DND/issues/DND-104), written **before** the
CTO's [`08-integrated-designs/a1-reliability-first/`](../08-integrated-designs/a1-reliability-first/README.md) model exists so convergence cannot cherry-pick gates. CI gate:
[`falsifier_dnd104_checks.py`](falsifier_dnd104_checks.py) (26 self-test checks; `audit(model)` /
`--model <path>` applies the same checklist to the CTO model when it lands). It re-bases the
DND-91/DND-74 method onto the [DND-103](/DND/issues/DND-103) reliability-first criteria and pins:
map-yield `(1-q)^N` (**52.7 %** at q=1e-4, N=6,400; the 99 %-map budget q ≤ **1.570e-6**), the
coupon zero-failure trial counts (**29,956 / 299,572 / 1,908,109** at 95 %), the decisive
**"a coupon can kill, but cannot crown"** bound (400 clean cycles bound q only at **~7.5e-3**, ~4,800×
looser than the board budget), correlated-group detection, per-cell precision counters, the DND-103
seven-stage timing decomposition, the DND-46 hostile-reprice cost ladder, load-during-write, jam
containment, and pitch **placement** (not budget). **Default-deny:** an unanswered attack is a FAIL.
The decisive falsifier is A11 (coupon C1, a 4×4 true-pitch reliability coupon) — a CTO/board print
handoff; no board contact here.

### A1 writer/reader rate + single-cell read, analytically bounded (DND-111, 2026-09)

[DND-110](/DND/issues/DND-110) left A1's whole timing argument resting on the bare placeholder
`HEAD_RATE_CELLS_S = 1000.0` (1 ms/cell) in [`a1-reliability-first/analysis/reliability_mask.py`](../08-integrated-designs/a1-reliability-first/analysis/reliability_mask.py).
[DND-111](/DND/issues/DND-111) replaces it with a sourced/CAD derivation
([`a1-reliability-first/analysis/a1_writer_rate.py`](../08-integrated-designs/a1-reliability-first/analysis/a1_writer_rate.py) +
[`scad/a1_reader_head.scad`](../08-integrated-designs/a1-reliability-first/scad/a1_reader_head.scad); ADR
[`dnd111-writer-rate-bound.md`](dnd111-writer-rate-bound.md)):

- **Stop-and-go is excluded** at 5.08 mm pitch: 30 cells/s at the sourced X1C acceleration
  (20 m/s²), 90 cells/s even at an aggressive 100 m/s². A 1,000 cells/s step rate needs ~5.08 m/s.
- **The rate is traverse/actuation-bounded**: max(traverse, actuation_or_read) + settle. At a
  credible 1.0 m/s gantry the head does **164.5 cells/s** (band **71–228** across 0.5–1.5 m/s and
  snap-trigger vs full-sweep). The placeholder overstated it by **4.4–14×**.
- **The full cycle still clears < 30 s**: 16.278 s at 8 heads (write 4.864 + verify 4.864 + reset
  3.0 + transport 2.0 + digital 0.05 + settle 1.5); 26.0 s even at 4 heads; and 22.61 s at 8 heads
  with the conservative full-sweep toggle.
- **Single-cell read resolution** is photometrically trivial (SNR ~1,460 at 50 µs, gate 5) but
  geometrically reduces to a **±0.264 mm head-to-cell registration tolerance** (2 mm aperture at a
  2 mm gap → 3.072 mm spot on a 3.60 mm top face; worst-case corner reach 2.172 mm).
- **Outcome (a) BOUNDED.** The decisive residual is now as-built gantry registration (±0.26 mm),
  not the rate. The next terminal call for the reader/retry architecture is SUCCESS-eligible on the
  rate axis. No print/measurement (DND-27).

### Falsifier audit of the DND-111 rate/read bound (DND-112, 2026-09)

[`falsifier_dnd112_a1_rate_audit.md`](falsifier_dnd112_a1_rate_audit.md) is the independent
default-deny audit of the DND-111 decisive number ([DND-112](/DND/issues/DND-112), the DND-108
method). CI gate: [`falsifier_dnd112_checks.py`](falsifier_dnd112_checks.py) — stdlib-only,
recomputes every claimed number **independently** of `a1_writer_rate.py` and exits non-zero while
any attack is unanswered.

**VERDICT: NOT CLEAN.** The **rate** side reproduces and stands; the **single-cell read** claim
does not.

- **Rate (reproduced):** fly-over 164.5 cells/s and the 71–228 band (T2), and the seven-stage
  16.278 s full cycle (T4) recompute exactly. Stop-and-go is genuinely excluded at the X1C 20 m/s²
  (30.4 cells/s); the aggressive 100 m/s² row is a V-shaped approximation that overstates 89.6 vs a
  true 61.9 (+45%) — a non-decisive sensitivity row. The full-cycle model omits ~24.6 % per-line
  accel/reversal (T3), so the honest 8-head cycle is ~18–19 s; still < 30 s.
- **Read (FAIL):** the reader rides at a fixed height over the **up**-plane, so a **down** cell is
  interrogated at a ~42 mm gap, not 2 mm. The DND-111 3.072 mm spot is the up-state spot; the
  down-state spot is **24.51 mm = 4.82 pitches** (R1). At that standoff the four up neighbours'
  near-field return beats the pocket by **~441×**, so a down cell reads up — a **silent** miss that
  defeats A1's readback/retry reliability feature (G2). The SCAD `CORNER_REACH = spot/2·√2 = 2.172`
  is the wrong worst case (the aperture is placed at the cell corner; the true reach is 4.081 mm,
  R2), and the ±0.264 mm "registration" residual is derived from the up state alone and is **not**
  the binding read limit (R4).
- **Gate impact:** replacing the placeholder flips **no** A1 gate (both 24.15 s pre and 16.28 s post
  clear < 30 s), but it does remove a 4.4–14× false-precision number and correctly names traverse as
  the rate limit.
- **Consequence:** the rate axis may be treated as bounded; the **read/verify axis is UNRESOLVED**
  and must not be folded into a "SUCCESS-eligible" call. Next test (CTO): state whether any A1
  artifact reads a **common-height** target (latch flag/toe); if not, restate the read as a
  mechanism/Z-standoff problem with a rate trade study (a per-cell Z stroke is fatal; a per-line
  refocus may be survivable). A breadboard optical check is a CTO physical handoff (DND-27).

### DND-113 — read mechanism correction (resolves DND-112)

[DND-113](/DND/issues/DND-113) responds to the DND-112 findings and **accepts the audit**
(ADR [`dnd113-a1-read-mechanism.md`](dnd113-a1-read-mechanism.md)):

- **Question (a) — common-height target:** **No** existing A1 artifact reads a single plane for
  both states; the reader targets the column top face (moves 40 mm). A common-height target is
  **proposed** (a reflective flag at the frame-anchored latch hinge, read at one standoff), pending
  CAD.
- **Question (b) — re-stated residual:** the binding read limit is the **state-dependent standoff**,
  not ±0.264 mm registration (now up-state provenance only). `read_resolution_bound()` reports the
  down-state spot **24.508 mm (4.824 pitches)** and the **~441×** neighbour/pocket ratio, and sets
  `resolves_single_cell = False` for the as-drawn reader.
- **Fixed:** the SCAD/ADR corner-reach formula (R2 → **4.081 mm**); the stop-and-go trapezoid
  (T1 → **61.9** cells/s at 100 m/s²); the per-line ramp in `full_cycle` (T3 → **18.278 s** at 8
  heads).
- **Trade study (`z_stroke_trade_study()`):** a Z stroke per **cell** = **5.4 cells/s**, cycle
  **> 2,380 s** (rate-fatal); per **line** (refocus) = **~29.8 s** (must be priced).
- **Gate:** the DND-112 companion checker `falsifier_dnd112_checks.py --gate` now exits 0, asserting
  the resolution. The read/verify axis remains **not** SUCCESS-eligible until the common-height
  target is CAD-designed and validated. No print/measurement (DND-27).


### DND-114 — common-height read target (CAD-validated; resolves DND-113 §4)

[DND-114](/DND/issues/DND-114) converts the DND-113 **proposal** into a CAD-validated artifact
(ADR [`dnd114-a1-common-height-read-target.md`](dnd114-a1-common-height-read-target.md)):

- **Adopted target (CH-A):** a **frame-fixed reflective vane** on the frame cradle in the latch lane,
  top face at `z = TRAVEL + 3 = 43 mm`. Its z does **not** move with the column, so **Δz = 0 by
  construction** for both states. The reader interrogates it at **one fixed standoff** (1.0 mm,
  dedicated 0.60 mm aperture).
- **Δz-in-DoF bound (CH-B fallback):** an arm-carried flag at radius `r` shifts by
  `Δz = r·2·sin(swing/2)`. Max radius in the ±1 mm DoF is **1.932 mm**; at the chosen `r = 1.20 mm`
  (30° swing) **Δz = 0.621 mm** — inside the budget.
- **Flag-vs-neighbour contrast:** the flag sits at `x = 2.225 mm`; the neighbour body begins at
  `x = 3.28 mm` (1.055 mm clearance). The flag-read spot is **1.136 mm**, half-width **0.568 mm**,
  clearing the neighbour body by **0.487 mm** and fitting the 1.60 mm flag width. The lane is open in
  Y.
- **R1/G2 re-check:** the as-drawn 42 mm gap / 24.5 mm spot / ~441× neighbour/pocket swing are
  **eliminated** by the fixed standoff (ratio → 1×). The as-drawn top-face defect is still recorded as
  the historical defect, not erased.
- **Gate:** the companion checker `falsifier_dnd114_checks.py --gate` exits 0 (7 attacks). Render +
  mesh validation of the flag part is CI-wired. No print/measurement (DND-27).
- **Superseded in part by [DND-115](/DND/issues/DND-115):** the 1.0 mm standoff / 0.60 mm aperture
  proved infeasible for the state-encoding shutter under a tolerance stack-up, so DND-115 adopts a
  **1.8 mm standoff / 0.44 mm aperture** (spot 1.405 mm). The CH-A target, Δz = 0, and the R1/G2
  result are unchanged; `falsifier_dnd114_checks.py` is re-baselined to the DND-115 values.


### DND-115 — state-encoding shutter (closes the read/verify axis)

[DND-115](/DND/issues/DND-115) closes the one artifact DND-114 left open (ADR
[`dnd115-a1-state-encoding-shutter.md`](dnd115-a1-state-encoding-shutter.md)):

- **The gap:** DND-114's CH-A vane is common-height but **state-invariant** — a plain post returns
  the same light in both latch states, so it cannot distinguish up from down.
- **The mechanism:** a **matte-dark flap** on a **shutter crank** sharing the frame-fixed latch hinge
  axis. Hidden (flap flat over the vane, normal +Z) blocks the beam; visible (flap edge-on) clears it.
  The pivot is directly over the vane, so a 90° crank swing moves the flap only ~2.87 mm laterally.
- **State encoding:** hidden covers **100%** of the 1.405 mm read spot, visible **0%** → **7.72×**
  on/off return ratio (gate 2×). The reflective **target stays frame-fixed** (`Δz = 0`); the flap is an
  absorber (ρ ≈ 0.05), so no state-dependent target z is reintroduced.
- **Standoff revision:** the adopted fixed standoff is **1.8 mm** with a **0.44 mm** aperture (the
  DND-114 1.0 mm window is infeasible for a 0.44 mm flap under printed tolerances). Swept flap clears
  the neighbour body by **0.255 mm**, the own column by **3.41 mm**.
- **Tolerance stack-up:** worst-case + a **200k-draw Monte Carlo** (`shutter_tolerance_mc()`): zero
  failures on every margin at realistic (±0.10 mm) frame pitch tolerance; the binding term is
  inter-cell pitch, retired by a single monolithic print. **Audit caveat (DND-118):** the MC pins
  the aperture plane to the nominal vane top, so its aperture check is tautological; a corrected MC
  with an explicit aperture tolerance still passes.
- **R1/G2/R4 re-check:** unchanged by the shutter; `resolves_single_cell_with_common_height_target`
  still holds with the shutter present. **Audit caveat (DND-118):** the neighbour up-cell top is
  weakly in-cone, not "off-beam" as stated; the on/off ratio is **6.37×** with that term included
  (still > 2× gate). See [`falsifier_dnd115_a1_shutter_audit.md`](falsifier_dnd115_a1_shutter_audit.md).
- **Gate:** `falsifier_dnd115_checks.py --gate` exits 0 (9 attacks, default-deny). Render + mesh
  validation of the shutter part is CI-wired. No print/measurement (DND-27). **Independently
  audited by the Falsifier in [DND-118](/DND/issues/DND-118)** — mechanism reproduces, closure
  framing corrected (see the DND-118 entry below).


### DND-118 — falsifier independent audit of the DND-115 shutter (read axis, corrected framing)

[DND-118](/DND/issues/DND-118) is the **independent** adversarial audit of the DND-115 decisive
number (ADR + register
[`falsifier_dnd115_a1_shutter_audit.md`](falsifier_dnd115_a1_shutter_audit.md); checker
[`falsifier_dnd115_a1_shutter_audit.py`](falsifier_dnd115_a1_shutter_audit.py) — stdlib-only,
imports nothing from `a1_writer_rate.py`):

- **Reproduced (geometry):** hidden occlusion 100%, visible clearance 0%, on/off **7.72×**,
  frame-fixed target (Δz = 0), sweep clearances 0.280 / 3.420 / 0.810 mm, min feature 0.44 mm,
  and claim-5 (1.0 mm standoff infeasible at gap 0.55 → −0.190 mm; 1.8 mm feasible → +0.610 mm).
- **Reproduced (robustness):** hidden coverage stays 1.000 for flap tilts 0–20°; the visible state
  stays clear for crank 90–75° — the states are insensitive to linkage angular error.
- **FAIL A5/A6 (crosstalk):** the ADR's "neighbour top is off-beam" is **false** — at the
  neighbour-top plane the coaxial 15° cone radius is 1.286 mm vs the 1.055 mm near-edge offset, so
  a bright neighbour is weakly in-cone (≈4.4% of the cone; ≈4.6% of the vane return,
  state-invariant). Correcting for it the on/off ratio falls **7.72× → 6.37×** — **still above the
  2× gate**, but the number was **reported and never gated** (`contrast_passes` ignores it).
- **FAIL A7 (framing):** "absorber Δz 0.55 mm inside ±1 mm DoF" is **vacuous** — the DoF budget
  applies to a reflective *target*; the target is frame-fixed (Δz = 0) and the absorber term is
  7.7× smaller than the vane term.
- **FAIL A9 (method):** `shutter_tolerance_mc()` pins the aperture plane to the *nominal* vane top,
  so `aperture_clearance` can never fail — tautological. Re-running with an explicit aperture
  placement tolerance (±0.10 / ±0.20 mm) still passes (worst +0.442 / +0.347 mm): the **design**
  survives; the **as-written MC** does not demonstrate it.
- **Verdict:** the mechanism **survives** independent recomputation; the **closure statement is
  over-claimed**. Correct the ADR/model wording (A5/A6/A7/A9) before citing this as the read-axis
  closure basis. Residuals remain assumption-class optical constants and measurement-only
  linkage force/friction/wear (DND-27). No physical coupon justified by this audit alone.


### Robust S5 readiness register (DND-46 / DND-48, 2026-09)

The [DND-44](/DND/issues/DND-44) closure headlines ("K1 ≤0.39 N, K5 $424.95, K8 1 N→0.01 mm")
were adversarially audited by the Falsifier ([DND-46](/DND/issues/DND-46),
[`FALSIFIER_AUDIT.md`](../06-experiments/test12_winner_convergence/FALSIFIER_AUDIT.md), 19 CI
checks). **Three of the six closures do not survive as published** — K1-service, K5 and K8 — and
K6/K11 are reframed. [DND-48](/DND/issues/DND-48) folds the robust figures into the register
([`s5r-shared-drive-register/README.md` §7/§9](../08-integrated-designs/s5r-shared-drive-register/README.md)) and the company `plan`:
**cost $482.95** (not $424.95), **service buckling 0.39–3.27 N/column**, **lateral gate exceeded
at the 40 mm extension** (0.356 mm at 1 N), **time conditional on a loaded dwell AND a ≥268 pps
loaded rate**, **cycle life ">=1e6, order unknown"**. Only **K10** remains a clean analytic
bound. Residuals that survive attack are listed in `FALSIFIER_AUDIT.md` §8. Regression gates:
`06-experiments/test12_winner_convergence/register_checks.py`.

### Adversarial status of the survivors (Test11)

The matrix above records *what evidence exists*. It does not record *what would
kill each candidate*. [Test11](../06-experiments/test11_falsification_library/)
adds that layer. No survivor has any **printed or measured** evidence and, under
[DND-27](/DND/issues/DND-27), none will be produced; every gate below is an
**analytic/simulation/CAD** gate, proposed and not yet passed.

| Survivor | Biggest unproven assumption | Cheapest rejection gate | Gate evidence level |
|---|---|---|---|
| S1 threshold/ratchet | four gates + ratchet + 40 mm travel fit at 5.08 mm | 2×5 analytic fit/stack-up, two masks, one shared stroke | CALCULATION |
| S2 planar tiles | four planar layers register for a 0.7 mm follower | 5×5 kinematic stack-up, five heights, checkerboards | CALCULATION / SIMULATION |
| S3 multi-row DMA | 2×4 printed register completes a loaded dwell | 2×4 analytic fan-out gate (`t11a_fit_check.py`) | CALCULATION / CAD |
| S4 shared-bus tiles | cheap clutch is independent under load; jams stay contained | two 2×4 tile models + modelled jam | SIMULATION |
| S5 rotary stops | printed cam/detent/return work at pitch and load | Test09 Stage A→B then C (analytic) | CALCULATION / SIMULATION |

Reliability is a **cross-cutting gate**: at a 0.01% per-cell error rate a
6400-cell map is correct only 52.7% of the time, and a six-cell coupon would be
99.94% perfect even at that failing rate. No clean small demo can be built to
promote any architecture. See
[Test11 reliability.py](../06-experiments/test11_falsification_library/reliability.py).

Test11 now also ships the **runnable** pieces of that gate so a survivor's fate
is mechanical, not a judgement call:

- [`isolation_rig_runner.py`](../06-experiments/test11_falsification_library/isolation_rig_runner.py)
  scores the J2 analytic run record into GO / KILL / INCONCLUSIVE per survivor
  (with repeat-count guards); a non-measured row is never reported as `MEASURED`.
  Its `--selftest` exercises every gate on SYNTHETIC rows and is CI-wired; it is
  not evidence for any survivor.
- [`analytic/`](../06-experiments/test11_falsification_library/analytic/) holds
  the DND-28 analytic proxies: rail-beam coupling + stiction bounds and the
  fixture fit stack-up.
- [`check_fixture.py`](../06-experiments/test11_falsification_library/check_fixture.py)
  gates the fixture geometry (5.08 mm pitch, X1C bed fit, one-plate layout) as a
  mesh/render check. OpenSCAD is absent in the agent environment, so the SCAD
  parse step is reported SKIPPED, never passed.

There is **no remaining physical J2 run to schedule**: the former J2-0…J2-4
protocol was re-scoped to its analytic proxy by [DND-28](/DND/issues/DND-28). The
residual measurement-only claims are permanently qualitative
([ADR-001 §5.2](convergence-decision-2026-09.md)).

### Test11 survivor-specific calculated results

[Test11 threshold-ratchet screen](../06-experiments/test11_threshold_ratchet_s1/README.md)
(InventorAlpha) adds, for S1/S2:

- S1 gate/pawl **fit** at pitch (2.28 mm budget closes); density is *not* the killer.
- S1 worst-case stroke force ≈2.37 kN if 6,400 pawls arm in one stroke → **fails** unless banked
  (**S1-B**: ≈296 N/stroke, ≈17.6 s).
- S1/S2 mask writing needs ≥500 channels or off-line pre-write; serial is 2,560 s.
- S1 full map ≈5.3 s, S2 full ≈2.0 s → timing passes; force and media-writing discriminate.
- S2 survives only double-buffered with an off-line writer.

### Physical evidence status

**Printed: none. Measured: none — and none will be produced** under board directive
[DND-27](/DND/issues/DND-27) (no physical print tests). The J2 isolation rig is now scored only
through its analytic proxy
([`analytic/`](../06-experiments/test11_falsification_library/analytic/)); the former physical
J2-0…J2-4 run was re-scoped by [DND-28](/DND/issues/DND-28) and its source issue is
`cancelled`. Physical measurement is not an available evidence class for this programme; the
residual qualitative risks are listed in
[ADR-001 §5.2](convergence-decision-2026-09.md).

## Mechanism coverage audit — September 2026

A function-driven Deep Research pass deliberately searched outside the vocabulary
already used in the repository. Most candidate findings mapped back to known
space and were **not** added again:

- punched cards / patterned media → M-002, M-013 and M-014;
- cable, chain and tendon distribution → M-009;
- magnetic or spring latches → M-003 / P-002;
- travelling writers → M-001;
- pneumatic shared force → M-015 and legacy Test00;
- generic scissor/pantograph mechanisms provide stroke transformation but do not
  introduce a new addressing, memory or regional-update topology by themselves.

Two findings survived the novelty gate:

1. **Tileable reprogrammable mechanical-memory lattices (M-016).** Unit-cell
   mechanical state can act as reusable structural memory with separate write and
   read phases. A demonstrated precedent is Chen, Pauly & Reis,
   [Nature 589, 386–390 (2021)](https://doi.org/10.1038/s41586-020-03123-5).
   The project-relevant hypothesis is a dense **memory/selector layer**, not a
   direct 40 mm metamaterial terrain actuator.
2. **Reconfigure unlocked, carry load locked (P-010).** Reconfigurable fixture
   research demonstrates the useful system split between low-load motion and
   high-stiffness locked service; see Lyu et al.,
   [Journal of Mechanical Design 138(8), 2016](https://doi.org/10.1115/1.4033037).
   For Shape Display this suggests separating writer force from tabletop load
   support.

These are sourced precedents only. They do not validate 5.08 mm pitch, 6,400
channels, <30 s updates, regional isolation or project cost. They therefore add
Q7/Q8 to the research backlog without promoting a new current architecture.

## Broad-search calculated evidence — September 2026

[Test10](../06-experiments/test10_broad_architecture_screen/) adds only arithmetic
evidence; it does not validate a mechanism. At the common 80×80, five-state
reference scale it calculates:

- 6,400 cells across 406.4 mm at 5.08 mm pitch;
- at least `6400 × log2(5) = 14,860` independent state bits, or 19,200 bits in a
  fixed three-bit encoding;
- more than 213.33 completed cell transactions/s for a purely serial writer to
  finish within 30 s before overhead;
- 64 tiles when the board is partitioned into 10×10-cell regions;
- 25,600 passive binary decisions for four unary height thresholds per cell;
- at an explicitly illustrative 0.40 s complete station dwell, 32.0 s for 80
  one-row stations and 8.0 s for 20 four-row stations, both excluding reset;
- 6,400 bought selectors cost $3,200 even at an assumed $0.50 each, while 64
  module selectors at $2 each cost $128 before the rest of the machine.

These bounds justify rejecting bought per-cell selection and ordinary serial
visible writing as baselines. They do **not** establish that threshold gates,
planar tiles, a multi-row head or module clutches work. The broad candidate
record therefore retains four new survivor families alongside the rotary-stop
reference and explicitly leaves the S5-R integrated design unchanged.

## Purchased-cost, sourcing, printability and reliability evidence — September 2026

[Test11](../06-experiments/test11_cost_printability_reliability/) builds a
per-survivor purchased-BOM model and dates the critical parts. It is **cost
arithmetic plus sourced listing prices**, not a quotation or a measurement.

### Purchased cost per survivor (working allowances; +20% contingency in parens)

| Candidate | Optimistic | Working | High | Credible <$500? |
|---|---:|---:|---:|---|
| S1 threshold/ratchet | $132.19 | $518.00 ($621.60) | $1,122.00 | No at working |
| S2 planar tiles | $192.19 | $536.00 ($643.20) | $1,206.00 | No at working |
| S3 multi-row DMA | $995.60 | $2,518.60 ($3,022.32) | $4,876.80 | No, decisively |
| S4 shared-bus tiles | $206.39 | $503.20 ($603.84) | $1,008.00 | No at working |
| S5 rotary reference | $276.00 | $432.00 ($518.40) | $783.00 | No with contingency |

S5 reproduces the Test08 BOM exactly, anchoring the model. **No survivor has a
credible sub-$500 delivered path at working allowances.** S1/S2/S4 working totals
are dominated by *fallback* bought allowances for parts they intend to print;
their print-intent floors are $239 / $299 / $311 and are only reachable if the
printed selector/media layer is dimensionally reliable across thousands of cells.

### The critical sourcing result

There is **no commodity bare 8 mm 18° bipolar PM stepper** in
LCSC/DigiKey/Mouser/Adafruit/Pololu/DFRobot. The only traceable part (MOONS
8PM020S1-02001) is **$40/ea**; marketplace multipacks are ~$0.70–1.05 (Amazon,
untraced) or ~$2.66+ (AliExpress, unverified). Test08's **$1.25 motor has no
matched quote**, and its **$0.60 driver is below the cheapest sourced matched
bipolar IC** (TB6612FNG $0.80 @100, DRV8833PWPR $1.33 @100). Substituting sourced
drivers alone moves S5 from $432 to ~$490 base ($588.84 with contingency).

Any bought part required on all 6,400 cells kills the budget: **$0.10/cell adds
$640**. This arithmetic is mechanism-independent and is the strongest single
result: **selection/programming must be printed/passive or heavily shared**.

Sourcing is now a **first-class blocker**. The next procurement action is the
Test09 Stage C gate — one traceable 8 mm motor sample plus an 80+spares delivered
quote with the same winding, shaft, step angle and lot — before any full-scale
purchase. Date: 2026-09-28.

### Three-scenario delivered BOM (DND-11)

[Test11.1](../06-experiments/test11_cost_printability_reliability/delivered_3scenario/README.md)
restates the model as the board asked: **best / expected / worst *delivered*
purchased totals**, with vendor and evidence labels per line and a shipping /
import uplift per scenario. Delivered (expected-case) totals and headroom:

| Candidate | Best deliv. | Expected deliv. | Worst deliv. | Headroom (expected) |
|---|---:|---:|---:|---:|
| S1 | $128.30 | $571.88 | $1,369.98 | −$71.88 |
| S2 | $189.20 | $586.96 | $1,465.44 | −$86.96 |
| S3 | $1,029.63 | $2,880.98 | $6,187.87 | −$2,380.98 |
| S4 | $204.11 | $548.91 | $1,210.02 | −$48.91 |
| S5 | $389.55 | $592.06 | $1,153.52 | −$92.06 |

**Every survivor exceeds the $500 ceiling in the expected delivered scenario.**
The best-case column is under $500 for all five, but only by assuming the cheapest
untraced marketplace prices plus a successful printed selector/latch layer — the
unproven part. S4 is closest (−$48.91) and S5 next (−$92.06). S3 has no cost path
at all. S5 is the best-evidenced BOM (82% of its expected total carries a live
source/listing); S1–S4 are 63–73% unquoted allowance, so their numbers are less
trustworthy. The decisive procurement action is unchanged.

### Printability at 5.08 mm pitch

At final pitch the printed geometry is a **fine-nozzle/resin problem**:

- a 4.68 mm body leaves a **200 µm web** — below a 0.4 mm line width;
- the Test08 0.20 mm guide wall is below the fine-nozzle single-wall floor with
  any XY compensation;
- a 0.40 mm nominal top gap loses 150 µm to ±0.10 mm width, ±0.05 mm index and
  ±0.10 mm deflection allowances;
- 12,800–19,200 parts is 160–1,600 printer-hours on one X1C, before print yield.

These are the numbers that decide whether 5.08 mm pitch is ordinary-FDM
fabricable at all, and they point at the Stage A coupon matrix as the next
physical action.

### Reliability and assembly scaling

`P(perfect map) = (1−q)^6400`: at 0.01% per-cell defects only **52.7%** of maps
are perfect; a **99% goal needs q ≤ 1.57×10⁻⁶** and ~1.91 M zero-failure
independent trials. Assembly of 4 parts/cell × 6,400 cells is **71–213 hands-on
hours** at 10–30 s/part. Detection with bounded recovery must be priced and timed
for any larger prototype; detachable 10×10 cartridges are mandatory.

## Architecture investigation — September 2026

### Decision

**No investigated architecture is yet convincingly compliant with all product
requirements. Do not build 6400 cells from this investigation.** The strongest
next experiment is **passive stepped rotary stops programmed by an 80-channel
travelling PM-stepper head, with a common lifting platen**. It has a conditional
26.25 s complete-map schedule at 80×80, but no qualified low-cost actuator supply,
no measured return-friction margin and no demonstrated coupling/detent reliability.
The working purchased BOM is **$432 / $518.40 with 20% contingency**, above the
$500 ceiling when contingency is included. This is a research recommendation,
not a product pass.

The useful result is a narrower, falsifiable engineering question: can an
unloaded 3 mm printed stepped cam, guided follower and cheap 8 mm PM motor deliver
reliable passive height memory at 5.08 mm pitch? A small coupon can reject that
idea before thousands of parts are printed.

Reproduction and evidence are in
[test08](../06-experiments/test08_architecture_search/README.md), including the
[architecture comparison](../06-experiments/test08_architecture_search/),
[historical audit](../06-experiments/test08_architecture_search/),
[source ledger](../06-experiments/test08_architecture_search/),
[parameters](../06-experiments/test08_architecture_search/params.json) and
[BOM](../06-experiments/test08_architecture_search/bom.csv).

### Scope and search

The design target and the request's **strictly less than 30 s end-to-end** limit
govern this investigation. Historical experiments are evidence, not constraints.
The comparison covers per-cell motors, single and parallel travelling writers,
shared screw drives, serial and parallel pneumatics, Jacquard-style catches,
mechanical coincidence addressing, binary weighted mechanical memory, thermal
actuators, passive molds and the new rotary-stop approach. The detailed comparison
records actuator counts, purchased components, timing, power, density and
manufacturing implications for each.

The recurring tradeoff is that cheap shared actuation saves motors but spends
time. Full-stroke row pushers still need both extension and retraction on every
row. A single writer would need about 213 completed cells/s before overhead;
at the modeled motion rates it takes roughly 76 minutes. Multiple row writers
can meet timing only by adding too many drives. Pneumatic designs move cost
and reliability into thousands of seals/valves. Scanned binary catches can meet
timing in principle, but the sourced 80-solenoid bank costs $356.80 and draws up
to 440 W before the rest of the machine is added.

After the rotary candidate exposed weaknesses, the search revisited fewer head
channels, different vertical level counts, servo gearing, solid columns, binary
catches and spring return. The quantitative rejection/iteration trail is kept
in the architecture comparison; the latest historical trial was not assumed best.

### What the proposed mechanism actually does

Each square column has an offset lower follower. Its toe rests on one of five
flat-height sectors of a freely selectable rotor. A guide constrains the slender
follower; a separate guide pair constrains the visible square body. The rotor
is not intended to lift a loaded column. Its flat plateau and thrust support
carry play loads after programming, without motor torque.

A common platen lifts every column to 41 mm above its zero height, clearing
even the tallest 40 mm cam sector. Below the stationary rotor shafts, a travelling
head engages 80 rotors at once with axially compliant friction face couplings.
It turns each rotor backwards against an individual home stop, then forwards
by 0, 4, 8, 12 or 16 full motor steps. It disengages so an independent printed
detent can seat the rotor. The head indexes to the next row. After all 80 rows
are programmed and the head is parked, the platen lowers; each column follows
by gravity until its toe reaches the programmed step.

This arrangement separates long-stroke motion, selection, mechanical memory
and load support. It also keeps the moving head below all stationary shafts,
avoiding the unresolved “head travels through the column field” interference
of some scanned-latch concepts. Nothing requires 6400 purchased motors, springs,
magnets, cables or bearings. **It does require 6400 reliable printed sliding and
rotating assemblies.**

The phase-independent friction coupling and detent are proposals, not qualified
hardware. Hard-stop homing can leave motor phase error after slip/stall. One
18° missed step exceeds the 12.50° geometric toe margin. The detent must reliably
correct that phase error while unloaded; assuming perfect step counting does
not solve it. The CAD contains the cam and detent wheel, but not a production
detent, stop, coupling head, bearing retention system or complete structural frame.

### Dimensions, counts and tabletop surface

| Item | Proposed value / status |
|---|---|
| Active area | 406.4 ×406.4 mm; 80×80 at 5.08 mm pitch |
| Moving square body | 4.68 mm wide ×80.2 mm long; lower 40.2 mm relieved for fixed guide; 0.40 mm top gaps |
| Projected top coverage | 84.87%; square cells retain the 1-inch / five-cells grid |
| Usable levels | 0, 10, 20, 30, 40 mm; five independently chosen heights |
| Miniature reference | **Not measured.** 40 mm is provisional; miniature-height compliance remains open |
| Cam | 3.0 mm outside diameter, 2.0 mm central core; five 72° sectors; 42 mm maximum top including 2 mm base |
| Follower | 42 mm tall, 0.7×1.8 mm stem; 1 mm wide, 1.5 mm thick toe; fixed slotted guide extends from z=4 to 84 mm |
| Body guidance | Two 4 mm guide tiers at z=110.2–114.2 and 118.2–122.2 mm in coupon coordinates |
| Vertical envelope | Surface z=124.2–164.2 mm; head, rails and frame below imply roughly 220–270 mm tabletop height, not a thin mat |
| External plan envelope | Allow roughly 460×500 mm for borders, rails and two staggered ranks; packaging not finalized |
| Actuators | 80 PM motors + one scan axis + one platen drive + one common coupling axis =83 |
| Printed memory parts | 6400 rotors, 6400 column/followers, 6400 independent detents, guides and frame modules |
| Motor electronics | 80 dual H bridges, 40 eight-bit control shift registers, ten proposed eight-channel boards, one controller |
| Harness | 320 short motor conductors confined to the head; shared power and serial connection to controller |

Eight-millimeter motors do not fit a single 5.08 mm row. Two staggered ranks
give 10.16 mm motor spacing. Their shafts need short compliant/flexible fan-in
connections to the 5.08 mm rotor grid. That packaging is an allowance, not CAD-
validated. The 80-channel head is expected to weigh order 1–2 kg; 4 m/s² scanning
therefore needs roughly 4–8 N before guide drag, reasonable for a belt axis but
still a test requirement.

Moving columns and the assumed platen alone total 15.24 kg. Rotors, guides,
frame, motors and power add more: plan for roughly 20–25 kg overall until a
complete mass model exists. This is a substantial tabletop appliance, not a
portable battle mat; the product target sets no mass ceiling, but usability
is worse than the original small prototypes suggest.

Five height levels suit walls, pits and terraces, but make coarse slopes and
stairs. Nine levels with the existing toe geometry **interfere**: the toe spans
more than a 40° sector. More vertical resolution requires another contact design,
not just changing a software parameter. Miniature bases need locally level
25.4 mm footprints or deliberately designed platforms. Cells cannot make an
arbitrary stepped surface stable for every base. Avoid isolated high support
cells beneath a miniature.

Global reset moves the whole surface. This is an encounter-map writer with a
cleared board, not a proven way to preserve miniatures on the surface during
transitions. Manual removal/replacement is unbounded and is not included in
26.25 s. If that is required as part of every transition, the complete use case
does not meet the timer. The mechanical timer ends after the new surface settles,
not after an operator repairs faults or repositions figures.

### Complete update timing

The event model uses rest-to-rest trapezoidal/triangular axis moves. It includes
every cell even for an all-zero target, homes every row's rotors, parks the head,
and lowers/settles the surface. It credits no overlap between operations.
The assumed PM rate is 400 full steps/s, below the archived motor's no-load
response specification, **but no loaded torque-speed curve validates it**.
The 25 ms coupling strokes and 15 ms settles also need measurement.

| Operation, complete board | Seconds |
|---|---:|
| Axis reference from defined parked state | 0.500 |
| Raise all columns clear, 41 mm | 1.346 |
| 79 row index moves, acceleration included | 5.631 |
| Commands/control | 0.160 |
| 80 engagements | 2.000 |
| 80 rotor home sweeps, 22 steps and settling | 5.600 |
| Worst-case writing, 16 steps and settling per row | 4.400 |
| 80 disengagements | 2.000 |
| Passive detent seating | 1.200 |
| Return head to park | 1.668 |
| Lower platen | 1.346 |
| Final settle before ready | 0.400 |
| **Total** | **26.251** |

All-high, checkerboard, stairs spanning all heights and seeded random full maps
all reach the worst-case bound because every row contains a maximum-height cell.
All-low still takes 23.051 s; alternating rows take 24.651 s. Arbitrary old maps
are covered by the global clearance stroke. All 25 old/new single-cell height
pairs are checked in the ideal support-state calculation.

Sensitivity matters more than the nominal pass: 200 pulses/s yields **33.851 s**;
800 pulses/s yields 22.451 s. Halving the head to 40 channels yields **39.725 s
even at 800 pulses/s**. At 400 pulses/s, increasing each engagement and
disengagement from 25 to 50 ms adds 4 s and fails. The available margin is only
3.749 s. Cold recovery from an arbitrary head position is not covered by the
0.5 s parked-state reference allowance; re-establishing park adds travel.

An update with a stuck follower or misindexed cam is **not ready for play**.
No bounded repair/detection loop is modeled. Consequently this is a fault-free
conditional timing estimate, not a reliable end-to-end performance guarantee.
Partial updates do not rescue this conclusion: the present mechanism still
globally lifts the surface, and the required full-map bound stands on its own.

### Loads, return, structure and power

The final candidate uses solid printed bodies rather than hollow bodies, since
printing is not the cost bottleneck. Geometry at the assumed material density
gives **2.069 g/cell**, 13.24 kg of moving columns, and 20.29 mN gravity force
per cell. The hollow alternative is 0.997 g and provides just 9.78 mN. At the
assumed 5 mN guide drag the margins are 15.29 and 4.78 mN respectively. Dirt,
warping and lateral loads can erase either margin. Test breakaway friction;
do not infer it from nominal CAD clearance.

With a 2 kg platen, 0.2 m/s² lift acceleration and 5 mN drag per cell, the
calculated peak lift force is **184.5 N**. An 8 mm lead at assumed 30% efficiency
needs **0.783 N·m total screw-drive torque at 262.5 rpm**. Require at least
1.57 N·m at that speed for a twofold qualification margin. The $18 lift motor
allowance is not a matched torque-speed selection; a larger motor or transmission
may increase the BOM. Four synchronized screws and four guides distribute load;
belt phase errors or one stuck corner can rack the platen.

The unsupported follower screens at only **0.108 N** Euler load using 1.5 GPa
effective modulus and a conservative fixed-free length. Reducing effective
unsupported length to 5 mm raises that screen to 7.62 N. This does **not** prove
the printed guide is rigid enough to provide that support. Toe contact area is
about 0.322 mm², giving 3.11 MPa at 1 N and 15.54 MPa at 5 N. Local layer
orientation, cam-edge crushing and creep may dominate. A 1 N per-cell service
test and a short 5 N accidental-load test are proposed, not passed.

An initial short guide ended at z=40 mm; inspection caught that the stem left it
at full extension. The final guide extends to z=84 mm. Clearance slots through
the lower body and lift plate let that stationary guide pass; a narrow bridge
crosses the guide's open slot to transmit load to the stem. The body was lengthened
to leave 40 mm of uninterrupted square upper column, keeping the guide relief
below adjacent terrain even with a 40 mm step. This fixes nominal interference
and support coverage, at the cost of a taller, heavier machine. The relieved
body and bridge need load tests; a short guide must not be reinstated to simplify
the print while keeping the improved Euler figure.

An additional variable-section beam buckling model screens the cam itself,
using a geometric-stiffness eigenproblem and sampled cross-sectional principal
inertias. The original 0.45 mm core radius gives an idealized 2.45 N critical
load; enlarging it to 1.0 mm improves that to **4.96 N**, while retaining 0.15 mm
toe/core clearance. Cross-section sampling and beam-mesh refinement are recorded,
and the solver recovers the uniform-cantilever Euler solution. This is still
not a 5 N rating: actual toe load is eccentric, the root is not a perfect clamp,
and print defects/creep are excluded. The 5 N abuse gate is therefore an explicit
red flag, even after the improvement. A measured stronger support/material or
another cam structure is needed before claiming tolerance of hand pressure.

Guide-wall arithmetic originally gave zero thickness. The revision leaves
0.20 mm walls with 0.10 mm clearance per side. It needs a fine-nozzle or resin
coupon and structural backing; it is not ordinary 0.4 mm-nozzle geometry.
Nominal 0.4 mm top gaps leave only 0.05 mm after the explicitly modeled width,
pitch and ±0.1 mm deflection allowances. Those deflections are limits, not measured
values. A simple solid-body cantilever screen at 42 mm exposure gives about
0.041 mm deflection under 0.1 N lateral load, but about 0.41 mm under 1 N.
Neighbor contact and guide compliance require testing under real handling.

The CAD's 2 mm lift plate is a **coupon**, not a full-width structural platen.
A 406 mm unsupported printed sheet would deflect far too much. The full device
needs a ribbed/box platen and supported modular guide cartridges (provisionally
64 modules of 10×10 cells). Platen flatness should stay within 0.25 mm and the
1 mm unloading clearance must remain positive everywhere under load. No FEA or
validated full-frame CAD establishes that yet.

At 3.3 V and 40 Ω per phase, 80 two-phase motors dissipate **43.56 W** when all
energized, about 13.2 A on the motor rail. Although motion is serialized, the
platen must remain raised during writing. Without a qualified passive brake,
count a60 W lift holding allowance concurrently with the43.56 W head and15 W
auxiliaries: **118.56 W nominal peak**; specify and test roughly a150 W protected
supply arrangement. Assuming the lift consumed nothing while stationary would
understate the power requirement. A qualified passive holding device could
reduce this, but its hardware cost must then be added.
This excludes fault current and unknown lift-motor sizing changes. Holding the
completed terrain requires no powered head torque. Lift screws with an 8 mm
lead must not be assumed self-locking: loss of power during reset needs a brake,
self-locking transmission or controlled descent, none yet fully designed/costed.

### Purchased cost

The detailed 18-line BOM explicitly includes drivers, PCBs, wiring, head shafts,
power, rails, four lift screws, belts, sensors and spares. It uses printed cell
bearings; adding even $0.10 of bought hardware per cell would add $640.

| Scenario | Before contingency | With 20% |
|---|---:|---:|
| All-low allowances | $276 | $331.20 |
| Working allowances | $432 | $518.40 |
| High allowances | $783 | $939.60 |

These are not three supplier quotations. In particular the 80 PM motors are
allowed at $1.25 each, without a current matched delivered quote. The working
non-motor total is $332. To stay below $500 with 20% contingency, motors would
need to average at most **$1.058** with every other allowance unchanged. To reach
$400, merely discounting the motors is insufficient in practical terms: roughly
$99 must be removed from the $432 base estimate. Under $200 has no demonstrated
path. A $276 optimistic combination is not evidence of an available machine.

The historical surplus motor price suggests a procurement experiment is worth
doing. Conversely, sourced FS90 servos cost $632 for 80 alone, and current
industrial micro-steppers are much more expensive. No purchases were made.
Unresolved brake, better lift motor, failed prints, extra feedback or structural
metal can invalidate the current allowance; they must be added when specified.

[Test11](../06-experiments/test11_cost_printability_reliability/) now dates these
critical parts (2026-09-28) and confirms the ceiling fails: the only traceable
8 mm PM stepper is MOONS at $40/ea, the cheapest sourced matched bipolar driver
is ~$0.80–1.33, and no survivor has a credible sub-$500 delivered path at working
allowances. Sourcing is recorded there as a first-class blocker.

### Reliability, assembly and maintenance

At an independent per-cell error rate of 0.01%, the probability that all 6400
cells are correct is only **52.7%**. Even 0.001% yields 93.8%. A 99% perfect-map
goal requires approximately **1.57×10⁻⁶ errors per cell-update**, before correlated
faults such as a warped guide tile or misaligned head. About 1.91 million zero-
failure independent trials would be needed for a one-sided 95% bound at that
rate. A successful six-cell demonstration cannot establish it.

Likely faults and consequences:

- A sticking column remains too high during lowering. The platen cannot pull it
  down; the map is wrong and the timer has not validly ended.
- A missed rotor step or a detent that does not seat can land the toe on an edge,
  select the wrong height or drop later under a miniature. No per-cell sensor
  presently detects this.
- One misaligned coupling can slip while the other 79 succeed. Spring compliance
  distributes engagement height, but creates another tolerance and wear variable.
- Axial coupling force can unseat a rotor unless its thrust retention is designed.
  At just 0.5 N/coupling the beam must distribute 40 N; this is not negligible.
- Dust, stringing and filament swelling can turn an initially free guide into a
  jam. Dry cleanable cartridges and replaceable followers are required.
- One large servo/motor-bank power or communication failure affects a whole row.
  A controller must keep “ready” false on detected faults; undetected cell faults
  remain the central reliability problem.
- Power loss during play leaves the mechanical stops holding. Power loss during
  the common lift is not safely resolved by that fact; reset recovery rehomes
  every rotor and requires preventing uncontrolled platen descent.

Even at 20 seconds per insertion/check, two separate parts per cell cost about
71 hours. Add detents, wiring, guide calibration and debugging: **100–200 hours
of hands-on work is a planning range**, not a measured assembly study. Fine-feature
printing and thousands of inspections make this a demanding one-person hobby
project. Use detachable 10×10 cartridges and a replaceable head driver module;
do not glue thousands of critical cells into a monolithic board.

### Evidence level and limits

| Evidence | What was established | What was not |
|---|---|---|
| Parameterized OpenSCAD | Real cam sectors, follower/toe, slotted guide, two upper guide plates and lift coupon; STL/CSG export | Complete production mechanism or frame |
| CSG intersections | Named cam/follower/guide/plate pairs at five seating heights and 20 raised rotor angles | Manufacturing tolerance, elastic interference, head/frame collisions or positive retention |
| Analytic geometry | Swept rotor radius, 1 mm unloaded clearance, 12.50° angular margin, contact area and thin walls | Contact stability or printed feature quality |
| Event simulation | All 6400 writes, 80 row homes, acceleration, coupling, park, lower and settle; six maps and 48 sensitivity cases | Loaded motor capability, fault detection or repair time |
| Force/structure screens | Weight, friction limits, follower Euler bounds, variable-section cam buckling, contact stress, lift torque and electrical load | Material allowables, fatigue, wear, creep, layer adhesion or full-frame stiffness |
| BOM and reliability scaling | Complete categories and sensitivity to per-cell hardware/error | Qualified quotes or measured reliability |

This work does not use a kinematic animation as proof. Tests ensure the known
weak cases remain failures. The proposed detent, hard stop, rotor retention and
head still need detailed prototype design and physical qualification. The
[prototype protocol](../06-experiments/test08_architecture_search/) gives
measurable continuation/abandonment gates. That is the next decision point;
neither a full-scale purchase nor a 6400-part print batch is justified yet.
