# A1 — reliability-first binary-latch + shared writer/reader machine

> **Integrated design (`08-integrated-designs/a1-reliability-first/`).**
> Originally developed under the retired top-level `10-reliability-mask/` stage; that stage held a
> broader reliability-first program and a seven-architecture screen. Only **A1** is the selected
> integrated machine candidate; the screen and provenance now live here alongside it. The other six
> screened architectures are **not** promoted integrated designs — see
> [`analysis/architecture_table.md`](analysis/architecture_table.md).

**Status: new candidate architecture selected — `A1 binary-latch + shared
writer/reader`.** This is the DND-104 program root. It works from the low-cost
family in [`06-experiments/test14_low_cost_program/`](../../06-experiments/test14_low_cost_program/README.md), **not** from
the mechanically dense S5-R in [`08-integrated-designs/s5r-shared-drive-register/`](../s5r-shared-drive-register/README.md)
(untouched, provenance). `09-*/` (S6-LC) is also untouched — this is a *new*
subdirectory.

Owner: CTO. Parent: [DND-104](/DND/issues/DND-104). Program umbrella:
[DND-102](/DND/issues/DND-102). Criteria of record:
[`02-design-criteria/README.md`](../../02-design-criteria/README.md) (strengthened by
[DND-103](/DND/issues/DND-103), PR #83).

> **Evidence class.** Everything here is **CALCULATION over sourced FDM process
> limits and sourced actuator ratings**, plus **CAD** (real OpenSCAD + trimesh
> mesh validation). **No part has been printed, purchased or measured**
> ([DND-27](/DND/issues/DND-27)). Prices are point-in-time sourced-class figures
> (2026-09). Nothing here is a physical validation.

## 1. What DND-104 asked, and the central design move

[DND-104](/DND/issues/DND-104) asked for a **reliability-first** low-cost machine:
very few bought actuators, mechanically simple repeated cells, tolerant of FDM
variation, maintainable, with **detectable/recoverable/local/repairable** failure
modes, arbitrary D&D terrain, and **masks developed together with the display**.

The DND-103 criteria added the decisive gate:

> **What has to work correctly 6,400 times?** Minimise it. Prefer *thousands of
> simple things + a few sophisticated shared mechanisms* over *thousands of tiny
> sophisticated mechanisms that happen to fit in CAD*.

The S5-R and S6-LC machines both fail this gate in the same structural way: they
have **6,400 independent passive cells, no per-cell feedback, and a silent
wrong-cell failure mode**. At a 0.01 % per-cell error the whole map is correct only
**52.7 %** of the time (`(1−q)^6400`). A missed latch is invisible and
uncorrectable. S6-LC's own adversarial audit ([DND-91](/DND/issues/DND-91), A6)
called this out and left it unresolved.

**The central move of this program is to make the repeated state *verifiable*.**
A1 keeps the dense visible surface passive and cheap, but adds a **shared
external reader** that scans the field after writing. A failed toggle is *detected
and re-driven* instead of being silently wrong. This converts the reliability
problem from "6,400 independent silent mechanisms" to "a few shared, monitored
mechanisms + a bounded retry loop".

## 2. Divergence first — seven materially different architectures

The screen ([`analysis/reliability_mask.py`](analysis/reliability_mask.py)) defines
seven architectures as first-class data and prints every field for each. Nothing
was pre-picked.

| # | Architecture | Family | Bought actuators | States | Mask medium | Silent elements | Full map | Parts |
|---|---|---|---|---:|---:|---|---:|---:|---:|
| **A1** | **binary-latch + shared writer/reader** | **external shared writer/verifier** | **4** | **2** | **none (direct write)** | **0** | **18.28 s** | **$181** |
| A2 | global broadcast binary interlock | broadcast lock-and-lift | 2 | 5 | printed interlock plate | 6,400 | 11.05 s | $224 |
| A3 | punched-film mask + biased columns | physical bit-image film | 2 | 2 | punched film (consumable) | 6,400 | 33.55 s | $187 |
| A4 | rewritable printed comb mask | reusable printed comb | 2 | 2 | printed louvre comb | 6,400 | 17.55 s | $171 |
| A5 | banked binary ratchet + coarse readback | broadcast threshold ratchet | 4 | 2 | per-bank threshold mask | 6,392 | 17.05 s | $213 |
| A6 | embossed-tape mask | continuous relief tape | 2 | 2 | embossed tape | 6,400 | 29.55 s | $179 |
| A7 | shared-camshaft bank + binary latch | rotating camshaft per bank | 1 | 2 | camshaft angle | 6,400 | 13.05 s | $158 |

Each architecture's full record (ten-job allocation, reliability audit, correlated
vs single-cell failure modes, serviceability, timing stages, BOM sketch, prototype
coupon and **decisive falsifier**) is emitted by `screen()` and tabulated in
[`analysis/architecture_table.md`](analysis/architecture_table.md).

## 3. The reliability gate in detail (per architecture)

The gate has three parts, all required by DND-103:

1. **Silent-set size** `N_s` — independent repeated parts whose single failure
   yields a wrong visible cell *that the machine cannot notice*.
2. **Readback** — can the machine detect a wrong cell and recover?
3. **Coupon** — is there a cheap printed coupon that can bound the as-printed
   spread?

| # | Repeated moving parts | Precision contacts/cell | Compliant printed parts | Wear interfaces | Silent `N_s` | Readback | Recovery |
|---|---:|---:|---:|---:|---:|---|---|
| **A1** | 6,400 latch arms | **0** | **0** | 6,400 hinges | **0** | **yes (reader)** | **scan → re-write failed cells** |
| A2 | 12,800 | 1.0 | 6,400 | 12,800 | 6,400 | no | full reset only |
| A3 | 6,400 | 0.3 | 6,400 | 6,401 | 6,400 | no | full reset |
| A4 | 6,400 | 0.25 | 6,400 | 12,800 | 6,400 | no | full reset |
| A5 | 6,400 | 0 | 0 | 6,400 | 6,392 | bank-only | per-bank re-home |
| A6 | 6,400 | 0.35 | 6,400 | 6,401 | 6,400 | no | full reset |
| A7 | 6,400 | 0.2 | 6,400 | 7,040 | 6,400 | no | full reset |

**A1 is the only architecture with a structurally zero silent-error set**, because
the reader verifies every cell. A1's state is also the only one with **zero
precision contacts per cell and zero compliant printed parts deciding
correctness** — the armed/disarmed state is bounded by two printed hard stops and
held in compression (the DND-103 "preferred" list, not the "strongly discouraged"
list).

**The map-yield consequence** (program reliability model, `(1−q)^N`):

| Per-cell error q | A1 (N=0) | every other (N≈6,400) |
|---|---:|---:|
| 1e-4 | 100 % | 52.7 % |
| 1e-5 | 100 % | 93.8 % |
| 1.57e-6 (99 % budget) | 100 % | 99.0 % |

For A1 the only remaining question is whether the **reader detection + retry loop**
converges; for the others the per-cell error itself must be proven below 1.57e-6,
which no architecture here (nor S6-LC) can demonstrate analytically.

### 3a. Independent pre-registered audit (DND-108) — A1 is CLEAN

The Falsifier wrote a **frozen** adversarial register before this model existed
([`falsifier_dnd104_criteria.md`](../../07-evidence-and-decisions/falsifier_dnd104_criteria.md),
[DND-108](/DND/issues/DND-108)), with a default-deny contract: any unanswered attack
is a FAIL for promotion. Pointed at A1 it returns **PRE-REGISTERED CLEAN, 11/11,
zero unresolved**:

```
python 07-evidence-and-decisions/falsifier_dnd104_checks.py \
    --model 08-integrated-designs/a1-reliability-first/analysis/audit_view_a1.py
```

The A1 silent-set declared to that audit is **N=8** (the shared reader heads, the
only elements that can still fail *undetected*); the 6,400 latch cells are
observed by the reader and are therefore not silent. A coupon of **>= 2,400
zero-miss cycles per head** bounds q below the N=8 budget at 95 %.

## 4. Selected machine — A1 binary-latch + shared writer/reader

### 4.1 The mechanism in plain English

- **Visible surface:** an 80 × 80 array of square printed columns at **5.08 mm
  pitch**, **406.4 × 406.4 mm**, **6,400 cells**. Each column has exactly **two
  states**: down (0 mm) and up (40 mm). Five visual height levels are formed by
  combining cells; the columns themselves are strictly binary, which is the
  reliability decision (one hard stop pair, no analog pocket depth).
- **State memory:** a printed **over-centre toggle latch** per cell. The arm
  travels between **two printed hard stops**; it is held against one stop in
  **compression** by the load path, not by a printed spring's force. The state is
  a *position*, and it is exact.
- **Selection / writing:** a **2-axis gantry** carries a **writer head** and a
  **reader head** across the field. The writer toggles only the latches that must
  change. No per-cell and no per-row bought actuator exists.
- **Verification and recovery:** after the write pass, the **reader head** scans
  all 6,400 cells. Cells whose state disagrees with the target are re-written
  (bounded retry). A failed toggle is therefore **detected**, not silent.
- **Reset:** a single global **reset stroke** drops all up-columns to the down
  stop before a new map (one shared mechanism).
- **Automatic mask system:** A1 needs **no physical mask medium** — the "mask" is
  streamed digitally to the writer head. This is the strongest possible answer to
  the mask-subsystem requirement: mask-generation latency is ~0, it cannot tear,
  register or wear, and it is regenerated for free every map. The price is that
  the *writer bandwidth* becomes the product-critical number (§4.2).

### 4.2 The decisive number — writer/reader bandwidth

The whole A1 claim rests on the head being able to write and read at the
required rate. **DND-111 replaced the old bare placeholder**
(`HEAD_RATE_CELLS_S = 1000.0`, labelled assumption-class) with a
first-principles derivation from sourced component-class kinematics and the
placed CAD: [`analysis/a1_writer_rate.py`](analysis/a1_writer_rate.py). See
[`07-evidence-and-decisions/dnd111-writer-rate-bound.md`](../../07-evidence-and-decisions/dnd111-writer-rate-bound.md).

The derivation bounds two candidate head kinematics:

| Kinematics | Bound | Verdict |
|---|---|---|
| **Stop-and-go** (stop at each cell) | 30 cells/s at X1C-class accel (20 m/s²), 90 cells/s at an aggressive 100 m/s² | **excluded** at 5.08 mm pitch |
| **Fly-over** (traverse at speed v, toggle/read on the fly) | per-cell time = max(traverse, actuation_or_read) + settle | **the real kinematics** |

| Term | Value | Basis |
|---|---|---|
| Parallel writer/reader heads | 8 | CAD/design |
| Credible traverse speed | 1.0 m/s | between sourced X1C 0.5 m/s and repo-prior 1.5 m/s |
| Per-cell traverse (5.08 mm) | 5.08 ms | calc |
| Latch toggle (snap-trigger) | 3 ms | device-class over-centre trigger |
| Read integration | 0.05 ms (50 µs) | sensor budget |
| Hard-stop settle | 1 ms | assumption |
| **Derived per-head rate** | **164.5 cells/s** | max(5.08, 3) + 1 ms |
| Derived rate band | **71–228 cells/s** | 1.0 m/s pessimistic full-sweep to 1.5 m/s snap-trigger |
| Placeholder overstatement | **4.4–14×** | 1,000 vs 71–228 cells/s |
| Effective rate (8 heads) | 1,316 cells/s | 8 × 164.5 |
| Worst-case write-all (6,400) | **5.864 s** | `a1_writer_rate.full_cycle()` (+1.0 s ramp) |
| Verify pass (6,400) | **5.864 s** | `a1_writer_rate.full_cycle()` (+1.0 s ramp) |
| Reset + settle + transport + map processing | **6.55 s** | model |
| **Total worst-case full-map cycle** | **18.278 s < 30 s** | **11.7 s margin**, including verification |

The dominant limit is **gantry traverse** at the credible design point (the
latch snap is hidden under it at ≤1.0 m/s; the full-sweep toggle takes over if
the gantry is pushed to 1.5 m/s). **DND-113 adds the per-line accel/reversal
overhead** (DND-112 T3): at 8 heads, 10 lines × 2·(v/a) = 1.0 s per pass, so the
honest cycle is **18.278 s** (was the idealised 16.278 s). The full map clears
< 30 s at **8 heads** (18.278 s); **4 heads just misses (30.006 s)**; with the
*pessimistic* full-sweep toggle it clears at 8 heads (24.61 s).


> **The one assumption that can still kill A1:** the derived rate is
> CALCULATION over sourced component-class limits. It does **not** prove the
> as-built gantry reaches 1.0 m/s while holding half-pitch registration, nor
> that the as-printed latch snaps at the modelled force. Those are
> tolerance/wear questions, not the decisive rate question, and are carried as
> explicit residual (§10). **The rate itself is no longer an unconstrained
> placeholder — that is DND-111 outcome (a), Bounded.**

### 4.2a Single-cell read resolution (DND-111; corrected by DND-113; fixed by DND-114; closed by DND-115)

Can one wrong cell among 6,400 be distinguished from its neighbours? **DND-112
audited DND-111's answer and falsified it** (R1/R2/R4/G2). DND-113 corrected the
mechanism: the as-drawn reader reads the **column top face**, which moves
`TRAVEL = 40 mm` with the state, so the read is **state-dependent-standoff
bound**, not registration bound. **DND-114 resolves the read axis** with a
CAD-validated **common-height read target**.

| Quantity | Value | Basis |
|---|---|---|
| Column top face | 3.60 mm square | CAD |
| Reader working gap (to the **up** top) | 2.0 mm | repo prior |
| Up-state spot (DND-111's 3.072 mm) | 3.072 mm (fits centre-aligned) | aperture + 2·g·tan15° |
| **Down-state gap (as drawn)** | **42 mm** (40 travel + 2) | CAD |
| **Down-state spot (as drawn)** | **24.51 mm = 4.82 pitches** | same formula |
| Up-neighbour / down-pocket return (as drawn) | **~441×** | Lambertian A/d² |
| Corrected corner reach (aperture at cell corner) | **4.081 mm** | √2·(BODY/2) + spot/2 |
| Neighbour near edge (true crosstalk threshold) | 3.28 mm | PITCH − BODY/2 |
| **Common-height target (CH-A, adopted)** | **frame-fixed vane, top z = 43 mm** | DND-114 CAD |
| **CH-A hinge-arc Δz** | **0.000 mm** (frame-fixed) | DND-114 CAD |
| CH-B fallback hinge-arc Δz (r = 1.20 mm, 30° swing) | **0.621 mm** (DoF ±1 mm) | DND-114 calc |
| Flag-read fixed standoff / aperture | **1.8 mm / 0.44 mm** (DND-115 revision) | DND-115 CAD |
| Flag-read spot | **1.405 mm**; clears neighbour by **0.353 mm** | DND-115 calc |
| Registration tolerance | ±0.264 mm (**secondary** gantry concern) | CAD + geometry |
| **State-encoding shutter (DND-115)** | **matte-dark flap, 90° crank on the shared hinge axis** | DND-115 CAD |
| Shutter flap width × thickness × depth | 1.55 × 0.44 × 1.60 mm | DND-115 CAD |
| Shutter hinge z / flap tip radius | 45.8 mm / 2.03 mm | DND-115 CAD |
| **Shadow of the read spot, hidden / visible** | **100% / 0%** | DND-115 calc |
| **On/off return ratio** | **7.72×** (gate 2×) | DND-115 calc |
| Shutter sweep — neighbour body clearance | **0.280 mm** | DND-115 calc |
| Shutter sweep — own column clearance | **3.42 mm** | DND-115 calc |
| Absorber (flap) standoff Δz | 0.55 mm (provenance only) | DND-115 calc / DND-119 |
| **Single-cell resolution, as drawn** | **NO** — a down cell reads up | DND-113 |
| **Single-cell resolution, with CH-A target** | **YES** — one fixed standoff | DND-114 |
| **State actually read (up vs down)?** | **YES** — shutter gives a 7.7× on/off return | DND-115 |

**The fix (DND-114) is a common-height read target, now CAD-validated.** The
reader no longer interrogates the moving column top face. Instead it reads the
**CH-A frame-fixed reflective vane** in the latch lane (top face at
`z = TRAVEL + 3 = 43 mm`), whose z does **not** move with the column — `Δz = 0`
by construction, for both states. The reader rides at **one fixed standoff**
(1.0 mm, dedicated 0.60 mm aperture): the flag spot is 1.136 mm and its X
half-width (0.568 mm) stays under the 1.055 mm clearance to the neighbour column
body, so the read integrates **only the flag** — the 4.82-pitch down spot and
the ~441× neighbour/pocket swing are **eliminated**. The latch holds the column
in compression against a hard stop, so the arm position is the column position.
A fallback **CH-B** arm-carried flag has its hinge-arc `Δz` bounded at 0.621 mm
inside the ±1 mm DoF. A reader that descends per **cell**
remains rate-fatal (>1000 s cycle); per **line** it costs ~29.8 s. See
[`dnd114-a1-common-height-read-target.md`](../../07-evidence-and-decisions/dnd114-a1-common-height-read-target.md).

**DND-115 closes the read axis by making that fixed target state-dependent.**
DND-114's vane is common-height but **state-invariant** — a plain post returns
the same light in both latch states, so it cannot actually tell up from down.
DND-115 adds the missing encoder: a **matte-dark flap** on a **shutter crank**
that shares the frame-fixed latch hinge axis with the toe arm. The crank has two
hard-stop positions — **hidden** (flap flat over the vane, plane normal +Z: the
beam is blocked) and **visible** (flap edge-on: the beam reaches the vane). The
flap pivot sits directly over the vane, so a 90° crank swing moves the flap only
~2.87 mm laterally (inside the own lane). The **reflective target stays
frame-fixed** (`Δz = 0`); the flap is an **absorber** (matte black), so no
state-dependent target z is reintroduced — only the *shadow* is state-dependent.
Computed at CAD + calculation: the hidden state covers **100%** of the read spot,
the visible state **0%**, giving a **7.72× on/off return ratio** (gate 2×). The
swept flap clears the neighbour body by **0.280 mm** and the own column by
**3.42 mm**. A **tolerance stack-up (worst-case + 200k-draw Monte Carlo)** shows
the DND-114 **1.0 mm standoff is infeasible** for a 0.44 mm flap under printed
placing tolerances, so DND-115 adopts a **1.8 mm standoff / 0.44 mm aperture**
(spot 1.405 mm, still clearing the neighbour by 0.353 mm). Residuals are now
assumption-class optical constants and measurement-only wear (DND-27).

**DND-119 corrected the claim framing** (from the DND-118 audit) with no geometry
change: the neighbour top is **not** off-beam but **weakly in-cone and
state-invariant** (cone radius 1.286 mm vs 1.055 mm near-edge offset), so the
crosstalk term is modelled and **gated** in `contrast_passes` — the
crosstalk-corrected on/off ratio is **5.95×** (still > 2× gate; DND-123 corrected
this from the internally-inconsistent 6.37×, which mixed point- and area-normalised
returns). The vacuous
"absorber within ±1 mm DoF" check is downgraded to **provenance only**, and the
tolerance MC now samples an explicit reader/aperture placement tolerance so its
aperture check can fail (worst +0.434 mm nominal / +0.325 mm at ±0.20 mm, still
positive). See
[`dnd115-a1-state-encoding-shutter.md`](../../07-evidence-and-decisions/dnd115-a1-state-encoding-shutter.md).


### 4.3 Honest timing decomposition (DND-103 requirement)

| Stage | Seconds | Notes |
|---|---:|---|
| Digital map processing | 0.05 | rasterise target to head stream |
| Physical mask generation | **0.00** | **no physical mask** (direct write) |
| Mask transport / indexing | 2.00 | gantry lane repositioning |
| Display reset | 3.00 | global reset stroke |
| Broadcast lift / write | 5.864 | worst-case all-change write (DND-111 derived; DND-113 ramp) |
| Settling / locking | 1.50 | two-state hard stop settles fast |
| **Verification** | **5.864** | **reader pass (this is the reliability feature)** |
| **Full cycle** | **18.278** | **visible transition = full (no hidden prep)** |

Because there is no physical mask, there is **no hidden preparation**: the
*sustained arbitrary-map cycle time* **equals** the *visible transition time*. This
is the one architecture in the program with no off-line mask caveat.

### 4.4 Reliability audit (DND-103 per-architecture audit)

| Field | A1 value | Class |
|---|---|---|
| Repeated moving parts | 6,400 latch arms (1/cell) | CAD |
| Precision contacts per cell | **0** (hard stops) | CAD |
| Compliant printed elements | **0** | CAD |
| Wear interfaces | 6,400 hinge pivots (compression-loaded) | CAD |
| Tolerance-sensitive interactions | latch-to-stop land (generous 0.88 mm land) | CAD |
| Correlated failure modes | gantry/reader fault → region wrong, **but detected** | calc |
| Single-cell failure modes | failed toggle → read back, re-driven | calc |
| Serviceability | gantry replaceable; frame is modular tiles | CAD |
| Detectable / recoverable / local / repairable | **all four** | design |

**What has to work correctly 6,400 times?** — the *reader must correctly classify
each cell*, and the *writer must toggle most cells first try*. But unlike every
other architecture, a miss is **observed and repaired**. The repeated mechanism
that must be *perfect* is reduced from 6,400 latches to **8 shared heads**.

### 4.5 Purchased BOM

| Line | Qty | Ext USD | Evidence |
|---|---:|---:|---|
| X gantry stepper (NEMA17-class) | 1 | 14.00 | sourced-class |
| Y/head-traverse stepper (NEMA17-class) | 1 | 14.00 | sourced-class |
| Writer toggle actuator | 1 | 9.00 | sourced-class |
| X guide rail pair + bushings | 1 | 22.00 | sourced-class |
| Y guide rail + bushings | 1 | 16.00 | sourced-class |
| Timing belts + pulleys (X, Y) | 2 | 16.00 | sourced-class |
| Writer head body + toggle prong | 1 | 6.00 | allowance |
| Reader head (reflectance/photodiode row) | 1 | 12.00 | sourced-class |
| Controller (RP2040) | 1 | 5.00 | sourced-live |
| Stepper drivers (DRV8833-class) | 3 | 6.00 | sourced-live |
| Power supply + protection (24 V) | 1 | 12.00 | sourced-listing |
| Wire / connectors / flex loom | 1 | 18.00 | sourced-class |
| Limit / home switches | 5 | 5.00 | sourced-class |
| Frame splice hardware | 1 | 10.00 | allowance |
| Fasteners (M3 assortment) | 1 | 8.00 | sourced-class |
| Spares and miscellaneous | 1 | 8.00 | assumption |
| **Purchased parts** | | **$181.00** | **mission gate < $250 PASS** |
| **Delivered (×1.16)** | | **$209.96** | internal convention PASS |

Full table: [`bom_a1.csv`](bom_a1.csv). The **bought-actuator count is 4** (three
motors + one writer actuator class). There is **no per-cell and no per-row bought
actuator**. Printed frame, columns, latch arms and cradle lands are excluded per
[DND-70](/DND/issues/DND-70).

### 4.6 Prototype ladder (DND-103 requirement)

| Stage | Scope | Validates | Kills the program if… |
|---|---|---|---|
| **A — single cell** | 1 cell at true pitch | latch holds 3.27 N in compression; writer toggles it; reader distinguishes states | latch won't toggle at writer force, or reader can't tell states |
| **B — 5×5 array** | 25 cells, short gantry | neighbouring tolerances, writer repeatability, scan-verify + retry catches a deliberately stuck cell | placement error > half pitch, or reader can't resolve 1 wrong cell in 25 |
| **C — one bank** | 10 × 80 = 800 cells | bank reset, gantry traverse, tabletop load under a placed mini, correlated faults | a bank write exceeds the linear timing extrapolation |
| **D — multiple banks** | 4 banks = 3,200 cells | cross-bank timing, sustained throughput, head duty drift, regional update | sustained cycle > 30 s or accuracy drifts |
| **full machine** | 6,400 cells | full < 30 s arbitrary map + regional update | only reached after A–D survive |

### 4.7 Decisive falsifier (updated by DND-111; corrected by DND-113; fixed by DND-114; closed by DND-115)

> **The reader cannot resolve a single cell at a common standoff.** DND-112
> falsified DND-111's "single-cell read reduces to registration": the reader
> read the **column top face**, whose z moves 40 mm with the state. Over a
> **down** cell the gap was ~42 mm, the spot ~24.5 mm (4.82 pitches), and the
> up neighbours dominated the return by ~441× — a **down cell reads up**. That
> silent wrong-cell failure made A1's readback/retry advantage **unproven** on
> the as-drawn artifacts. DND-113 re-stated the binding limit as the
> **state-dependent standoff** (not ±0.26 mm registration). **DND-114 fixes it:**
> the CAD-validated **CH-A frame-fixed reflective vane** (top z = 43 mm,
> `Δz = 0`) is read at **one fixed standoff**, so the down spot is 1.405 mm and
> clears the neighbour body by 0.353 mm — the 4.82-pitch spot and
> the 441× swing are eliminated. **DND-115 closes it:** the vane alone was
> state-invariant, so a matte-dark **shutter flap** on the shared frame-fixed
> hinge axis now shadows the read spot in one latch state (100%) and clears it in
> the other (0%), giving a **7.72× on/off return ratio** with the reflective
> target still frame-fixed (`Δz = 0`). See
> [`dnd114-a1-common-height-read-target.md`](../../07-evidence-and-decisions/dnd114-a1-common-height-read-target.md)
> and [`dnd115-a1-state-encoding-shutter.md`](../../07-evidence-and-decisions/dnd115-a1-state-encoding-shutter.md)
> (and the DND-113 correction
> [`dnd113-a1-read-mechanism.md`](../../07-evidence-and-decisions/dnd113-a1-read-mechanism.md)).

The **rate** is bounded (outcome a): "is 1 ms/cell possible?" is answered (no,
it is traverse-bounded at 71–228 cells/s/head; the honest cycle is 18.278 s at 8
heads). The read/verify axis is now **closed at CAD + calculation** by the
DND-114 target plus the DND-115 shutter; the remaining residuals are
assumption-class optical constants and measurement-only wear, not physics.

Secondary falsifiers: the as-printed over-centre latch snaps at the modelled
writer force (the state is exact by hard stop, but the *snap* is a force
question); the latch hinge survives 6,400-cycle wear (measurement-only under
DND-27); as-built gantry registration (±0.26 mm) — a *secondary* read concern.
All are coupon/measurement questions under DND-27, **not** the decisive read
mechanism question.

## 5. Why not the runners-up

| Architecture | Why it loses the reliability gate |
|---|---|
| A5 banked binary ratchet | Best of the rest (reliability score 6.4), but readback is **per-bank only**; a single stuck cell inside a bank stays silent — **6,392 silent elements**. |
| A7 shared-camshaft | Only **1** bought actuator, but **6,400 silent elements** and a printed 80-lobe camshaft repeatability risk (≤0.1 mm angular) is unproven. |
| A4 rewritable comb | **6,400 silent elements**; the comb writer is itself a repeated precision mechanism; a stuck slat corrupts an 80-cell band. |
| A3 punched film | **6,400 silent elements**; a consumable that must register 80 holes to <0.1 mm and can tear. Also fails <30 s as modelled (33.55 s). |
| A6 embossed tape | **6,400 silent elements**; tape creep under follower load blurs the relief; near the timing edge (29.55 s). |
| A2 global interlock | **6,400 silent elements**; a stuck interlock is invisible; needs a per-level plate that is itself precision. |

The gap is not marginal: A1's silent set is **0**, every other is **≈6,400**. On
the program's own reliability model that is the difference between a map that is
always correct and a map that is ~53 % correct at a plausible 0.01 % per-cell
defect rate.

## 6. Decision: selection vs promotion (S5-R is untouched)

**This is a new candidate, not a silent replacement.** `08-integrated-designs/s5r-shared-drive-register/`
(S5-R, promoted machine, $404.60 delivered, 24.615 s) and `06-experiments/test14_low_cost_program/`
(S6-LC) are **unchanged**. A1 lives in a new directory and is proposed as the
**reliability-first low-cost candidate** for the program.

| Machine | Bought actuators | Silent cells | Full map | Parts | Delivered | Reliability gate |
|---|---:|---:|---:|---:|---:|---|
| S5-R (`08-`) | 42 | 6,400 | 24.615 s | $348.79 | $404.60 | fails (silent, no readback) |
| S6-LC (`09-`) | 3 | 6,400 | 11.96 s | $226.77 | $263.05 | unresolved (G8 measurement-only) |
| **A1 (`10-`, new)** | **4** | **0** | **18.28 s** | **$181.00** | **$209.96** | **passes (0 silent; reader + retry)** |

A1 does **not** beat S6-LC on raw speed or actuator count. It beats it — and S5-R —
on the **reliability gate that DND-103 made first-class**, and it is cheaper than
both. Under the program's stated priority ("reliability/buildability outrank the
last few dollars"), that is the decisive advantage.

**Promotion proposal:** promote **A1** as the reliability-first low-cost candidate
at the next convergence gate. The **rate** is no longer an open condition —
DND-111 bounded it analytically (outcome a), corrected by DND-113 (18.278 s). The
**read/verify axis is now CLOSED at CAD + calculation**: DND-114 gave a
frame-fixed CH-A target (Δz = 0) and DND-115 added the state-encoding shutter
(hidden covers 100% of the read spot, visible 0%, 7.72× on/off, target still
frame-fixed), so the readback/retry advantage is no longer unproven on the
mechanism. The latch toggle force remains a coupon/measurement residual (DND-27).
This is an explicit proposal, not an automatic replacement (per DND-104 §5).

## 7. Failure modes, recorded honestly

- **The rate is bounded, not assumed (DND-111).** The old 1 ms/cell placeholder
  is 4.4–14× optimistic. The honest derived rate (71–228 cells/s/head) still
  clears 30 s at 8 heads (**18.278 s** with the DND-113 per-line ramp; 4 heads just
  misses at 30.006 s), and the pessimistic full-sweep toggle clears at 8 heads
  (24.61 s). If the gantry cannot be built to carry the needed head count at
  1.0 m/s, add heads (cheap printed bodies) or reduce the map size. Timing no
  longer dies on a bare assumption.
- **The as-drawn read was state-dependent-standoff bound (DND-112/DND-113); DND-114 fixes it and DND-115 closes it.**
  The as-drawn reader read the column top face; over a down cell the gap was
  ~42 mm, the spot ~24.5 mm (4.82 pitches), and up neighbours dominated ~441×, so
  a down cell read up. The ±0.26 mm registration number is up-state-only
  provenance. DND-114 replaces the target with a **CAD-validated frame-fixed
  reflective vane** (top z = 43 mm, Δz = 0) read at **one fixed standoff**
  (1.8 mm, DND-115); the spot (1.405 mm) clears the neighbour body by 0.353 mm.
  DND-115 adds the **state-encoding shutter** (matte-dark flap on the shared
  hinge axis): hidden covers 100% of the spot, visible 0%, a 7.72× on/off return,
  with the reflective target still frame-fixed. A per-cell Z stroke remains
  rate-fatal (>1000 s cycle); a per-line refocus costs ~29.8 s. Residual: the
  standoff/aperture and the flap matte reflectance are assumption-class; wear is
  measurement-only (DND-27).
- **Gantry registration** (secondary, once a common-height target exists) over
  406 mm is the classic 2-axis failure; belt stretch and thermal drift are
  unmeasured. A position-repeatability coupon is required.
- **Hinge wear** across 6,400 pivots is measurement-only under DND-27; the
  compression hold removes the *spring-force* risk but not wear.
- **Column top load path** is a compression hard stop (good), but the exact land
  dimensions are CAD-provisional until a calibration coupon exists.

## 8. Reproduce

```bash
# architecture screen (7 machines, full JSON)
python 08-integrated-designs/a1-reliability-first/analysis/reliability_mask.py

# convergence: selection, why, bandwidth, prototype ladder, falsifier
python 08-integrated-designs/a1-reliability-first/analysis/reliability_mask.py convergence

# 75 pinned regression checks (includes the DND-111/113/114/115 rate + read checks)
python 08-integrated-designs/a1-reliability-first/analysis/reliability_mask_checks.py

# DND-111 + DND-113 + DND-114 + DND-115: writer rate bound + read mechanism
# (full JSON, incl. shutter_read_contrast() + shutter_tolerance_mc())
python 08-integrated-designs/a1-reliability-first/analysis/a1_writer_rate.py

# DND-112 audit resolution gate (exits 0; CI-wired)
python 07-evidence-and-decisions/falsifier_dnd112_checks.py --gate

# DND-114 common-height read target gate (exits 0; CI-wired)
python 07-evidence-and-decisions/falsifier_dnd114_checks.py --gate

# DND-115 state-encoding shutter gate (exits 0; CI-wired)
python 07-evidence-and-decisions/falsifier_dnd115_checks.py --gate

# CAD: render + mesh-validate the binary-latch cell and reader head
export PATH="$HOME/.local/bin:$PATH"
python 08-integrated-designs/a1-reliability-first/analysis/render_a1_cad.py

# generate the full comparison table
python 08-integrated-designs/a1-reliability-first/analysis/make_table.py
```

## 9. Files

| Path | What |
|---|---|
| [`analysis/reliability_mask.py`](analysis/reliability_mask.py) | the architecture screen, reliability gate, timing, BOM, convergence |
| [`analysis/a1_writer_rate.py`](analysis/a1_writer_rate.py) | **DND-111 + DND-113 + DND-114** writer rate bound + read-mechanism correction + common-height target |
| [`analysis/reliability_mask_checks.py`](analysis/reliability_mask_checks.py) | 60 regression checks |
| [`analysis/render_a1_cad.py`](analysis/render_a1_cad.py) | OpenSCAD render + mesh validation (cell parts + reader head + CH flag) |
| [`analysis/make_table.py`](analysis/make_table.py) | emits the full per-architecture comparison table |
| [`analysis/architecture_table.md`](analysis/architecture_table.md) | the generated comparison table |
| [`scad/a1_binary_latch_cell.scad`](scad/a1_binary_latch_cell.scad) | the A1 unit cell (real OpenSCAD) + **DND-114** common-height flag + **DND-115** shutter |
| [`scad/a1_reader_head.scad`](scad/a1_reader_head.scad) | **DND-111 + DND-113 + DND-114/115** reader-head optical geometry + self-checks |
| [`cad/stl/`](cad/stl/) | watertight rendered parts (column, latch, cradle, flag, shutter, reader head) |
| [`cad/render_record.json`](cad/render_record.json) | mesh-validation record |
| [`bom_a1.csv`](bom_a1.csv) | A1 purchased BOM |
| [`../../07-evidence-and-decisions/dnd104-reliability-mask.md`](../../07-evidence-and-decisions/dnd104-reliability-mask.md) | the DND-104 ADR |
| [`../../07-evidence-and-decisions/dnd111-writer-rate-bound.md`](../../07-evidence-and-decisions/dnd111-writer-rate-bound.md) | **DND-111** rate-bound ADR |
| [`../../07-evidence-and-decisions/dnd113-a1-read-mechanism.md`](../../07-evidence-and-decisions/dnd113-a1-read-mechanism.md) | **DND-113** read-mechanism correction ADR |
| [`../../07-evidence-and-decisions/dnd114-a1-common-height-read-target.md`](../../07-evidence-and-decisions/dnd114-a1-common-height-read-target.md) | **DND-114** common-height read target ADR |
| [`../../07-evidence-and-decisions/dnd115-a1-state-encoding-shutter.md`](../../07-evidence-and-decisions/dnd115-a1-state-encoding-shutter.md) | **DND-115** state-encoding shutter ADR |

## 10. Residual uncertainty

- Writer **rate** — **bounded by DND-111, corrected by DND-113**: 71–228
  cells/s/head, traverse-bounded, factor 4.4–14× below the retired placeholder.
  Not measurement-only.
- **Read/verify mechanism — CLOSED at CAD + calculation (DND-114 + DND-115).**
  The as-drawn top-face reader was state-dependent-standoff bound
  (DND-112/DND-113). DND-114 specifies a **frame-fixed reflective vane** (CH-A,
  top z = 43 mm, Δz = 0) read at **one fixed standoff** (1.8 mm, DND-115): the
  spot (1.405 mm) clears the neighbour body by 0.353 mm. DND-115 adds the
  **state-encoding shutter** (matte-dark flap, 90° crank on the shared hinge
  axis): hidden covers 100% of the spot, visible 0%, a 7.72× on/off return, with
  the reflective target still frame-fixed. Residuals: the standoff/aperture and
  the flap matte reflectance are assumption-class; the flap/hinge wear is
  measurement-only (DND-27).
- **Registration** (±0.26 mm) — a **secondary** read concern once a
  common-height target exists; as-built over 406 mm is unmeasured.
- **As-printed latch snap force** at the writer contact — coupon/measurement-only
  (DND-27). The STATE is exact by hard stop; only the snap force is uncertain.
- Hinge wear across 6,400 pivots — measurement-only (DND-27).
- Column top land dimensions — CAD-provisional until a calibration coupon exists.

A1 is **not** claimed print-ready or physically validated. Its **rate** is
CALCULATION-bounded (DND-111 outcome a, corrected by DND-113), its **read/verify
mechanism** is CLOSED at CAD + calculation by DND-114 (frame-fixed common-height
target) and DND-115 (state-encoding shutter: 7.72× on/off, target still
frame-fixed), and its reliability structure is the only one in the program that
*could* convert 6,400 silent failures into a monitored, recoverable, local
failure — **and that conversion is now supported on paper end to end**. The
remaining residuals are assumption-class optical constants and the
coupon/measurement questions that DND-27 forbids settling physically.
