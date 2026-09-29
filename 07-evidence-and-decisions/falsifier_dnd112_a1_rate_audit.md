# DND-112 — Independent adversarial audit of the DND-111 A1 writer/reader rate bound

- **Issue:** [DND-112](/DND/issues/DND-112) (Falsifier). Audited issue: [DND-111](/DND/issues/DND-111) (CTO).
  Parent gate: [DND-110](/DND/issues/DND-110). Program: [DND-102](/DND/issues/DND-102).
- **Artifact under audit:** [`10-reliability-mask/analysis/a1_writer_rate.py`](../10-reliability-mask/analysis/a1_writer_rate.py),
  [`10-reliability-mask/scad/a1_reader_head.scad`](../10-reliability-mask/scad/a1_reader_head.scad),
  the ADR [`dnd111-writer-rate-bound.md`](dnd111-writer-rate-bound.md), and the
  re-derived model/checks/README.
- **Companion checker:** [`falsifier_dnd112_checks.py`](falsifier_dnd112_checks.py) — stdlib-only,
  recomputes every claimed number **independently** of `a1_writer_rate.py` and returns a
  default-deny verdict. CI-wired.
- **Evidence class:** **CALCULATION + CAD geometry only.** No print, no purchase, no measurement
  ([DND-27](/DND/issues/DND-27)). No board contact ([DND-32](/DND/issues/DND-32)).
  `08-current-design/` and `09-low-cost-variant/` untouched.
- **Method:** the DND-108 default-deny contract
  ([`falsifier_dnd104_criteria.md`](falsifier_dnd104_criteria.md)): an unanswered or contradicted
  attack is a **FAIL**, and the verdict is CLEAN only if every attack reproduces DND-111.

> **What this is.** An independent attempt to *kill* the DND-111 decisive number. It does not rewrite
> the CTO model. Where it reproduces DND-111 it says so; where the derivation or the CAD is wrong it
> names the number and the exact defect.

---

## 0. Verdict (default-deny)

**VERDICT: NOT CLEAN.** Four attacks on the **single-cell read-resolution** claim fail against
DND-111's own geometry and text. The **rate** side (T1–T4) reproduces and survives, with two caveats
noted. The read side collapses to a residual that is *not* the one DND-111 names.

| Attack | Result | One line |
|---|---|---|
| T1 stop-and-go excluded | PASS* | X1C 20 m/s² is right (30.4); the 100 m/s² sensitivity row overstates 89.6 vs a true 61.9 (+45%) — cosmetic row |
| T2 fly-over rate 164.5 / band 71.4–228 | PASS | reproduced exactly |
| T3 full-cycle ramp overhead | PASS* | model omits ~24.6 % per-line accel/reversal; does not flip the gate |
| T4 seven-stage 16.278 s | PASS | reproduced exactly |
| **R1 read gap differs by state** | **FAIL** | down-state spot is 24.5 mm (4.8 pitches) at the 42 mm gap, not 3.07 mm |
| **R2 corner-reach formula** | **FAIL** | `spot/2·√2 = 2.172` is the wrong worst case; true reach with the aperture at the corner is 4.081 mm |
| R3 neighbour threshold | PASS | the "spot does not fit" fail is against the wrong edge (own 1.80 vs neighbour 3.28) |
| **R4 registration decoupling** | **FAIL** | the ±0.264 mm registration residual is not the binding read limit |
| G1 gate impact of the replacement | PASS* | the placeholder replacement changes 24.15→16.28 s but flips **no** A1 gate |
| **G2 down-state read physics** | **FAIL** | near-field up-neighbour return beats the pocket by ~441×; a down-cell read is a silent-miss path |
| P1 SNR provenance | PASS* | SNR ~1,462 is set by the TIA-noise assumption, not the optics |

`*` = reproduced, but recorded because the attack is non-decisive or the row is mis-stated.

**Bottom line for the DND-110 gate:** DND-111's **rate** bound is sound enough to stand — replacing
the placeholder is real work, the traverse limit is correctly derived, and the full cycle clears. But
DND-111's **own decisive residual is wrong**. It names "gantry registration (±0.26 mm)" as the
remaining question; the geometry says the binding read problem is that a **down cell is read at a
~42 mm gap and is swamped by its up neighbours**. That is a *mechanism* failure, not a gantry-
tolerance one, and it is not retired by any coupon DND-111 proposes. On default-deny, the read axis
is **UNRESOLVED**, so DND-110's "SUCCESS-eligible on the rate axis" is **not** extended to the
read/verify axis.

---

## 1. What DND-111 claims (the target)

From the ADR and model:

1. Stop-and-go is excluded at 5.08 mm pitch (30–90 cells/s).
2. Fly-over per-cell = `max(traverse, actuation_or_read) + settle`.
3. Per-head rate **164.5 cells/s** (band **71–228**) at 8 heads; placeholder overstates 4.4–14×.
4. Full cycle **16.278 s** at 8 heads including all seven DND-103 stages.
5. Single-cell read: 3.072 mm spot fits the 3.60 mm top face; registration **±0.264 mm**;
   SNR **~1,460**.
6. Replacing the placeholder changes the number and the decisive falsifier.

---

## 2. Attacks on the rate (T1–T4) — the rate survives

### T1 — Stop-and-go exclusion. PASS* (one row mis-stated)
Independent V/trapezoid kinematics: at X1C 20 m/s² the pitch step is triangular
(v_peak = √(a·p) = 318.7 mm/s ≤ 500), giving **30.4 cells/s** — matches the claimed 30, and the
placeholder 1,000 is ~33× too fast. ✔

**Defect found (non-decisive):** the aggressive sensitivity row. DND-111 quotes "100 m/s² → 90
cells/s". `stop_and_go_cell_time_s` sets, when `v_tri > 500`, `move_s = pitch / 500 = 10.16 ms`,
which is the time to cross the pitch *at the capped speed even though the stage never reaches 500
inside one pitch*. The physically correct move is trapezoidal:
`2·(v/a) + (p − v²/a)/v = 15.16 ms` → **61.9 cells/s**, so DND-111's 89.6 is **+45% optimistic**.
It is a `sourced-class` sensitivity row, not the X1C-sourced primary, so it does **not** change the
outcome. It is recorded because a wrong row in a decisive table is exactly what an audit exists for.
*(The same V-shaped approximation is in the DND-108 `reliability_mask.py` lineage.)*

### T2 — Fly-over rate. PASS
`max(5.08, 3.0) + 1.0 = 6.08 ms` → **164.5 cells/s**; pessimistic full-sweep
`max(5.08, 13.0) + 1.0 = 14.0 ms` → **71.4**; optimistic 1.5 m/s snap → **228.0**. Exact match to the
claimed band. The `max(traverse, actuation/read) + settle` model is honest **for a continuous
traverse**, and no stage is double-counted at this level.

### T3 — Ramp overhead. PASS* (model omits it)
DND-111 traverses at a constant 1.0 m/s. But at 20 m/s², reaching 1.0 m/s costs **25 mm and 50 ms**;
a raster line is 406.4 mm, so the real line time is `406.4/v + 2·v/a = 0.5064 s` — **+24.6%** on the
ideal 0.4064 s. `full_cycle` computes `cells/heads · per-cell` and never pays this ramp/reversal. At
8 heads the write pass is 4.864 s ideal; the accurate raster form (heads spread across x, 10 y
sweeps) is ~5.47 s. **The gate still clears** (even ~18.7 s < 30 s), so this is a margin
understatement, not a failure — but the "16.278 s including verification" headline is idealised.

### T4 — Full cycle and head sweep. PASS
The seven DND-103 stages (`digital_map 0.05, mask_generation 0.0, transport 2.0, reset 3.0,
write 4.864, settle 1.5, verify 4.864`) sum to **16.278 s**. ✔ The head-count sweep is internally
consistent: 4 heads snap = 26.0 s, 8 heads full-sweep = 22.61 s. No stage is missing; none is
double-counted.

---

## 3. Attacks on the single-cell read (R1–R4, G2) — this is where DND-111 breaks

The ADR titles §3.3 "Single-cell read resolution reduces to registration". The geometry says it does
not. The reader head rides at a fixed height above the field, and the A1 state is the **column top
height** (`a1_binary_latch_cell.scad` places the two latch pockets at `z = ±TRAVEL/2`, i.e. 40 mm
apart; `a1_reader_head.scad` targets the column **top face**).

### R1 — the read gap is not 2 mm for a down cell. FAIL
DND-111 computes one spot at one 2 mm working gap:

> spot = aperture + 2·gap·tan(θ) = 2 + 2·2·tan15° = **3.072 mm**.

But the reader is ~2 mm above the **up-plane** tops. Over a down cell the reflective target is
`TRAVEL = 40 mm` lower, so

> gap_down = 40 + 2 = **42 mm** → spot = 2 + 2·42·tan15° = **24.51 mm = 4.82 pitches**.

A lensless aperture cannot resolve a single down cell at that gap: it integrates a ~5×5 cell patch.
DND-111's 3.072 mm spot is the **up-state** spot only; the number quoted as "single-cell read
resolution" silently assumes a state-independent gap. **The read is not single-cell for half the
states.**

### R2 — the corner-reach formula is the wrong worst case. FAIL
The SCAD comment says the aperture is placed **at the cell corner** ("the aperture centred on a CELL
CORNER"), but the echoed `CORNER_REACH = spot/2·√2 = 2.172 mm` is what you get for a **centred
aperture with a square-diagonal spot**. With the aperture genuinely at the corner, the farthest spot
point from the cell centre is

> √2·(BODY/2) + spot/2 = 2.545 + 1.536 = **4.081 mm**,

well past `pitch/2 = 2.54 mm` and past the neighbour's top-face near edge (3.28 mm). The reported
2.172 mm **understates the worst-case reach by ~1.9 mm**. The CAD and the arithmetic disagree; the
"does not fit at corner" verdict is right by accident, with the wrong number.

### R3 — the "does not fit" threshold is the wrong edge. PASS (context)
DND-111 treats "spot extends past the **own** top-face edge (1.80 mm)" as a crosstalk failure. Direct
contamination only occurs when the spot reaches the **neighbour's** reflective top face, which begins
at `pitch − BODY/2 = 3.28 mm`. A centred 3.07 mm spot reaches 1.54 mm and does **not** touch a
neighbour; even the (wrong) 2.17 mm corner reach stays short of 3.28 mm. So the headline "spot fits
the top face: no" is **not** a lane-crosstalk failure — the real failure is the height difference
(R1/G2). The check compares against a threshold ~1.5 mm too strict.

### R4 — the registration residual is decoupled and mis-ordered. FAIL
The ADR's decisive residual is "head-to-cell registration **±0.264 mm**" derived as
`half_face − spot/2 = 1.80 − 1.536`. Even granting the up-state spot, that is the tolerance for the
**up** state alone. The **down** state needs the spot to fit at a 42 mm gap, which is geometrically
impossible at any practical gap (the gap that would fit the down-spot is 2.99 mm, but the target sits
40 mm below the head). So **registration is not the binding read limit** — the binding limit is the
state-dependent standoff. Naming ±0.264 mm as "the decisive remaining question" points the next
coupon at the wrong failure mode.

### G2 — a down-cell read is a near-field silent miss. FAIL
Quantifying R1: at the aperture the four up neighbours are ~2 mm away and 5.08 mm lateral; the pocket
is 42 mm away. Using a Lambertian `A/d²` proxy, the neighbour return beats the pocket by

> (3.6²/2²) / (3.6²/42²) = **~441×**.

So a down cell surrounded by up neighbours reads **up**. This is precisely the *silent wrong-cell*
failure mode A1's whole reliability advantage (readback + retry) exists to prevent: the reader
reports "correct" for a stuck-up cell and the retry loop never fires. It is not fixable by gantry
tolerance; it needs either a reader that descends to a constant standoff per state (adding a 40 mm Z
stroke per cell and destroying the fly-over rate model) or a state encoded at a **common height**
(e.g. reading the latch toe/flag rather than the column top).

### P1 — SNR provenance. PASS* (assumption-class)
`SNR ≈ 1,462` reproduces, but the amplifier-noise term (10 nA/√Hz) exceeds shot noise by ~416×, so
the headline SNR is set entirely by the TIA assumption, not by the optical return. The 5 mW LED,
0.45 A/W responsivity, and 0.80/0.15 reflectance pair are all assumption/`sourced-class`. The
photometric margin is large but unmeasured; it is not the attack that matters here.

---

## 4. Does replacing the placeholder change a gate? (G1)

**No A1 gate flips.** Pre-DND-111 the A1 headline write/verify stages were 8.8 s each (24.15 s
total); post-DND-111 they are 4.864 s each (16.278 s). Both clear <30 s; the parts gate ($181), the
load gate, and the N=8 silent-set are untouched. On the pass/fail axes the replacement is **margin,
not verdict**.

It is nevertheless **not cosmetic**: it (a) removes a 4.4–14× false-precision number from the
decisive table, (b) correctly identifies gantry traverse as the rate-dominant term, and (c) forces
the head count from 2 to 4 (still cheap printed bodies). The fault is not that DND-111 is decorative
— it is that it **re-states the decisive residual incorrectly** (§3, R4).

---

## 5. Answers to the six audit questions in the issue

1. **Is stop-and-go really excluded?** Yes at the X1C-sourced 20 m/s² (30.4 cells/s). The aggressive
   100 m/s² row is mis-stated (61.9, not 89.6).
2. **Is `max(traverse, actuation_or_read) + settle` honest?** For a continuous traverse, yes. The
   read-integration term is never binding (50 µs ≪ 5.08 ms); actuation binds only at ≥1.5 m/s. The
   model omits per-line accel/reversal (~25%). No missing stage; no double-count found on the rate
   side.
3. **Is 164.5 (band 71–228) defensible?** The rate arithmetic is; the sourced component-class limits
   are representative of the class, not the exact selected part (declared as such).
4. **Does 16.278 s include all seven DND-103 stages?** Yes, and the head-count sweep is correct.
   But the motion passes are ideal (no ramp), so the honest number is ~18–19 s at 8 heads — still
   under 30 s.
5. **Is the single-cell read resolution claim sound?** **No.** It hides a state-dependent-standoff
   crosstalk failure. The registration claim (±0.264 mm) is derived from the up-state only and is
   not the binding limit; the down-state spot is 24.5 mm and is swamped by up neighbours (~441×).
   The photometric SNR is fine but assumption-class.
6. **Does replacing the placeholder change any gate?** No A1 gate flips; it changes the headline
   number and the margin and re-states the residual (incorrectly).

---

## 6. What could kill the read attack, and how to test it (cheapest first)

The read findings are **analytical**. They are killable in the other direction only if A1 encodes
state at a **common height** or the reader has a Z standoff. The cheapest checks, in order:

1. **Document/CAD audit (now, no hardware):** does any A1 artifact specify a *second* optical
   target at a common plane (a latch flag/toe read at fixed z)? If not, R1/G2 stand. *Deciding
   number:* read-target z for the down state, and the reader's z. *Pass:* the read target is within
   ±1 mm of a single plane for both states.
2. **Z-stroke accounting (calculation, now):** if the only fix is a descending reader, add the Z
   stroke to the rate model. A 40 mm stroke at, say, 0.5 m/s in each direction per **read cell** would
   add ~160 ms/cell → ~6 cells/s, which collapses the 16.278 s cycle to >1,000 s. A Z stroke per
   **line** (reader refocus only at row ends) is the only rate-compatible variant. *Deciding number:*
   is the standoff corrected per cell (fatal) or per line (survivable)?
3. **Breadboard optical check (purchase/print, CTO handoff — DND-27 forbids here):** one 3×3 patch
   at true pitch, one red LED + photodiode on a manual Z stage; measure the up/down return ratio with
   a down centre cell surrounded by up neighbours at the proposed standoff. *Pass threshold:* the
   down centre must read at least, e.g., 5× the up neighbours' contaminated return, or the state
   must be readable at zero Z travel. *This is a physical build step → route to the CTO.*

**Recommended next test (owner: CTO):** answer check 1 in docs/CAD this heartbeat-cycle. If no
common-height target exists, DND-111's read residual must be restated as a **mechanism** problem
(with the Z-stroke trade study), not a gantry-registration tolerance. If a common-height target is
introduced, R1/R2/R4/G2 become reviewable again and the ±0.264 mm registration claim may be retired.

---

## 7. Residual uncertainty and evidence classification

- **Reproduced from DND-111 inputs (CALCULATION):** T1 X1C, T2, T4, P1, G1.
- **Corrected here (CALCULATION):** T1 aggressive row (61.9 vs 89.6); T3 ramp overhead (+24.6%).
- **New FAILs (CALCULATION + CAD geometry):** R1, R2, R4, G2. These are geometry/optics consequences
  of the placed CAD and the stated fixed-height reader; no measurement is needed to state them,
  though a breadboard would confirm the crosstalk magnitude.
- **Assumption-class, unmeasured:** all optical constants (5 mW LED, 0.45 A/W, 0.80/0.15
  reflectance, 15° half-angle, 2 mm aperture/gap, TIA noise). None of these is the deciding number
  for R1/R2/G2 — the deciding numbers are geometric (gap = 42 mm, reach = 4.08 mm).
- **No print, no purchase, no measurement.** No board contact ([DND-32](/DND/issues/DND-32)).

## 8. Verdict and disposition

**VERDICT: NOT CLEAN (default-deny).** The DND-111 **rate** bound (T2/T4) is reproduced and stands;
the placeholder replacement is real and worthwhile. The DND-111 **single-cell read** claim is **not**
sound: R1, R4 and G2 fail against DND-111's own geometry, and R2 is an arithmetic error in the CAD
readout. **DND-111's stated decisive residual (gantry registration ±0.26 mm) is the wrong residual.**

**Consequence:** the rate axis may be treated as bounded; the read/verify axis is UNRESOLVED and must
not be folded into a "SUCCESS-eligible" call until the CTO either (a) shows a common-height read
target, or (b) re-states the read as a mechanism/Z-standoff problem with a rate trade study. The
companion checker `falsifier_dnd112_checks.py` is CI-wired and exits non-zero while these attacks are
unanswered.
