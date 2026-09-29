# DND-115 — CAD-design + validation of the A1 state-encoding shutter

- **Issue:** [DND-115](/DND/issues/DND-115) (CTO). Parent gate: [DND-110](/DND/issues/DND-110)
  (CEO terminal decision). Corrected model: [DND-113](/DND/issues/DND-113). Adopted
  target: [DND-114](/DND/issues/DND-114). Program: [DND-102](/DND/issues/DND-102).
  Audited by [DND-118](/DND/issues/DND-118); claim framing corrected by
  [DND-119](/DND/issues/DND-119) (no geometry change).
- **Trigger:** DND-114 §6 left one read-axis artifact undimensioned: the CH-A
  frame-fixed vane is a common-height target, but it is **state-invariant** — a
  plain post returns the same light in both latch states, so it cannot actually
  distinguish up from down. The mechanism that makes the vane's apparent
  brightness encode the latch state was *identified* (the arm's silhouette) but
  not dimensioned.
- **Evidence class:** **CALCULATION + CAD geometry.** No print, no purchase, no
  measurement ([DND-27](/DND/issues/DND-27)). No board contact
  ([DND-32](/DND/issues/DND-32)). `08-current-design/` and `09-low-cost-variant/`
  untouched.
- **Branch:** `cto/dnd115-state-encoding-shutter` from `main` (`60d33d7`).
- **Deliverables:** the parameterised `shutter_crank()` / `shutter_flap()` in
  [`a1_binary_latch_cell.scad`](../08-integrated-designs/a1-reliability-first/scad/a1_binary_latch_cell.scad)
  with a `part="shutter"` printable selector and self-checks; the new
  [`shutter_read_contrast()` / `shutter_tolerance_mc()`](../08-integrated-designs/a1-reliability-first/analysis/a1_writer_rate.py);
  the hard CAD self-checks in [`render_a1_cad.py`](../08-integrated-designs/a1-reliability-first/analysis/render_a1_cad.py);
  the re-baselined [`falsifier_dnd114_checks.py`](falsifier_dnd114_checks.py)
  (standoff/aperture revision); the new [`falsifier_dnd115_checks.py`](falsifier_dnd115_checks.py)
  (12 attacks after DND-119, default-deny); the rendered watertight shutter mesh +
  [`render_record.json`](../08-integrated-designs/a1-reliability-first/cad/render_record.json); this ADR;
  and README §4.2a/§4.7/§6/§10.
- **Outcome: the read/verify axis is CLOSED at CAD + calculation (outcome a).**
  The shutter shadows the fixed-standoff read spot in one latch state (100%) and
  clears it in the other (0%), a **7.72× on/off return ratio**, while the
  reflective target stays frame-fixed (`Δz = 0`). The remaining residuals are
  assumption-class optical constants and measurement-only wear (DND-27).

## 1. The design problem, restated

DND-114 moved the read off the state-dependent column top face onto a
**frame-fixed reflective vane** (CH-A) read at one fixed standoff. That killed
the 42 mm state-dependent gap and the ~441× neighbour swing — but it left the
read **state-invariant**: nothing in the CH-A artifact made the returned light
differ between the up and down latch states. A vane that returns the same signal
in both states cannot verify the state, so A1's readback/retry advantage was
still unproven.

The fix must make the vane's apparent brightness **state-dependent** without
reintroducing a state-dependent *target z* (the exact defect DND-113/DND-114
removed). The latch already has a frame-fixed feature — the hinge axis — and the
latch holds the column in compression against a hard stop, so the **arm angle is
the column state**. A shutter carried on the same hinge axis therefore encodes
the state.

## 2. The mechanism (CAD)

A **shutter crank** shares the frame-fixed latch hinge axis with the toe arm.
The crank has two hard-stop positions:

| State | Crank angle | Flap plane normal | Beam |
|---|---:|---|---|
| **HIDDEN** | 0° (flat over the vane) | +Z | blocked |
| **VISIBLE** | 90° (toward the own body) | ≈ +X (edge-on) | reaches the vane |

The **flap pivot IS the hinge axis**, placed **directly over the vane** at
`(HINGE_X, 0, Z_SHUT_HINGE)`. Because the flap rotates ~in place, a large crank
swing produces only a small lateral stroke
(`FLAP_R · 2·sin(swing/2) = 2.87 mm`), which fits the own lane. The flap is a
**matte-dark absorber** (`ρ ≈ 0.05`), so the reflective **target stays the
frame-fixed vane top** (`Δz = 0`); only the *shadow* is state-dependent.

| Parameter | Value | Basis |
|---|---:|---|
| Hinge axis x | 2.225 mm (`HINGE_X`) | CAD, latch lane |
| Hinge axis z | 45.8 mm | CAD |
| Flap tip radius `FLAP_R` | 2.03 mm | CAD |
| Flap width × thickness × depth | 1.55 × 0.44 × 1.60 mm | CAD (1-line thickness) |
| Crank swing | 90° | CAD (over-centre stops) |
| Flap underside gap above vane (flat) | 0.55 mm | CAD |
| Flap top clearance to aperture plane | 0.81 mm | CAD |
| Reader standoff / aperture | **1.8 mm / 0.44 mm** | CAD (DND-115 revision) |
| Read spot | 1.405 mm | `a + 2·g·tan15°` |
| Swept flap neighbour clearance | **0.280 mm** | CAD envelope |
| Swept flap own-column clearance | **3.42 mm** | CAD envelope |

## 3. The state-encoding contrast (CALCULATION)

The beam is vertical over the vane axis; the flap casts a shadow on the read
plane. The covered fraction of the spot is computed from the flap's projected
XY footprint at each crank angle:

| Quantity | Value | Check |
|---|---:|---|
| Shadow of the read spot — HIDDEN | **100%** | fully occluded |
| Shadow of the read spot — VISIBLE | **0%** | fully clear |
| On/off return ratio | **7.72×** | gate 2× — **PASS** |
| On/off ratio incl. in-cone neighbour | **6.37×** | gate 2× — **PASS** (DND-119) |
| Reflective target Δz | **0.000 mm** | frame-fixed — **PASS** |
| Absorber standoff Δz | 0.55 mm | **provenance only** (DND-119; term 7.7× below the vane term) |
| Neighbour crosstalk (clear state) | **4.6%** of the vane return; **modelled and GATED** (ratio ≤ 1) | **PASS** (DND-119) |
| Ambient | rejected ~1000× (modulated LED + sync detect) | assumption-class |

The deciding numbers are **geometric** (shadow fraction, lane clearance), not
SNR. The photometric ceiling remains assumption-class.

**DND-119 correction (from the [DND-118](/DND/issues/DND-118) audit).** Four
claim-framing/method defects are corrected here with **no geometry change**:

- **A5 — crosstalk gated.** `shutter_read_contrast()` now carries the neighbour
  term into `contrast_passes` via `neighbour_crosstalk_gated` (physical in-cone
  ratio ≤ 1) and `on_off_return_ratio_with_crosstalk ≥ 2`. The number is a margin,
  not a report.
- **A6 — "off-beam" removed.** The neighbour top is **not** off-beam: at the
  neighbour-top plane the coaxial 15° cone radius is **1.286 mm** vs the
  **1.055 mm** near-edge offset, so the edge is in-cone by **0.231 mm**. The
  in-cone part of the neighbour top is the **0.231 mm²** crescent (4.45% of the
  cone); it contributes a small **state-invariant** return (~4.6% of the vane
  term); the corrected on/off is **6.37×**, still > 2× gate.
- **A7 — absorber DoF downgraded.** The "absorber Δz inside ±1 mm DoF" check is
  **vacuous**: the target is the frame-fixed vane (Δz = 0), and the absorber term
  is 7.7× below the vane term. It is reported for provenance only and **not**
  counted as evidence.
- **A9 — MC de-tautologised.** `shutter_tolerance_mc()` previously pinned the
  aperture plane to the nominal vane top, so `aperture_clearance` could never
  fail. It now samples an explicit reader/aperture-plane placement tolerance
  (±0.10 mm; hostile ±0.20 mm) and the aperture check is fail-able. Worst sampled
  aperture clearance is **+0.434 mm** nominal and **+0.325 mm** at ±0.20 mm —
  still positive, so the design survives; the method now demonstrates it.

**Residual modelling-convention caveat (DND-121).** The crosstalk term
`rho·A_nb/g_nb²` is an **area-scaled** quantity added to the **unit-area** vane
proxy `rho/g_vane²`. The `~4.6%` neighbour/vane ratio (equivalently the quoted
`6.37×`) therefore depends on the choice of area reference: a dimensionally
consistent treatment that scales both sources by the detector's actual read-spot
area gives `2.1%` and `6.78×`. Every defensible convention leaves the on/off
ratio **far above the 2× gate**, so this does not change the gate outcome or any
design decision; it is recorded as a presentational/evidence-class residual. The
audit's A13 attack pins the ADR's quoted figures to the model's actual output, so
the number cannot drift silently.

## 4. The DND-115 revision to the DND-114 standoff (IMPORTANT)

DND-114 assumed a **1.0 mm** fixed standoff with a 0.60 mm aperture. DND-115's
tolerance stack-up shows that window is **infeasible** for a 0.44 mm flap: with
`gap + thickness + aperture_clearance = 1.0 mm`, printed placing tolerances make
the aperture-clearance check fail in **~0.5–1 %** of draws (and up to 32 % for a
0.30 mm gap split). DND-115 therefore **raises the adopted standoff to 1.8 mm**
and sets the aperture to **0.44 mm (1 line)**. The read spot becomes 1.405 mm
(half-width 0.702 mm), still clearing the neighbour body by **0.353 mm** and
fitting the 1.60 mm flag Y-width. This is a deliberate, evidence-driven
correction to a DND-114 *assumption* — the artifact (frame-fixed vane, Δz = 0,
one fixed standoff) is unchanged; only the standoff distance moves.

## 5. Tolerance stack-up (worst-case + Monte Carlo, DND-27 policy)

`shutter_tolerance_mc()` runs **200,000** draws over the printed/assembly
tolerances (assumption-class, sourced FDM): hinge x ±0.05, hinge z ±0.20, flap
radius ±0.15, flap thickness ±0.10, flap width ±0.10, vane top ±0.10, gap ±0.10,
inter-cell pitch ±0.10 mm (and a hostile ±0.20 sensitivity). **DND-119 (A9):** the
reader/aperture-plane placement is now an **independent** tolerance (±0.10 mm,
hostile ±0.20 mm) instead of being pinned to the nominal vane top.

| Check | Nominal worst margin | Fail rate (nominal) | Fail rate (±0.20 pitch) |
|---|---:|---:|---:|
| Neighbour flap clearance | **0.084 mm** | **0.000** | 0.036 % |
| Aperture clearance | **0.434 mm** | 0.000 | 0.000 |
| Vane gap | 0.450 mm | 0.000 | 0.000 |
| Coverage | 0.045 mm | 0.000 | 0.000 |
| Own clearance | 3.351 mm | 0.000 | 0.000 |
| On/off ratio | 4.48× | 0.000 | 0.000 |

The binding term is the **inter-cell pitch tolerance** on the neighbour body; a
single monolithic frame print retires it (nominal-tolerance fail rate is **0**
across 200k draws). The worst-case neighbour clearance can go negative only
under the hostile ±0.20 mm pitch assumption, at 0.036 %. **DND-119 (A9):** the
aperture-clearance check is now fail-able (independent reader placement); worst
sampled clearance is +0.434 mm nominal and +0.325 mm at ±0.20 mm reader
placement, so the design survives and the pre-DND-119 tautology is retired.

## 6. R1/G2/R4 re-checked with the shutter present

| Attack | As-drawn (DND-113) | With CH-A + shutter |
|---|---|---|
| **R1** down-state gap | 42 mm → 24.5 mm spot | **N/A** — one fixed standoff (1.8 mm) |
| **R4** binding read limit | state-dependent standoff | **secondary**: ±0.264 mm registration only |
| **G2** neighbour/pocket ratio | ~441× (silent wrong-cell) | **1×** — no state-dependent standoff |
| **Single-cell down read** | **NO** (reads up) | **YES** (fixed target, state-encoded) |
| **State actually distinguished** | **NO** (state-invariant) | **YES** (7.72× on/off) |

`resolves_single_cell_with_common_height_target = True` still holds **with the
shutter present**: the shutter is an absorber in the beam, not a target, and the
reflective target z is unchanged.

## 7. What changed (all calculation + CAD; no print)

- `scad/a1_binary_latch_cell.scad`: added `shutter_crank()`, `shutter_flap(state)`,
  a `part="shutter"` printable selector, the shutter parameters, and the shutter
  self-checks (vane gap, aperture clearance, neighbour envelope, own-column
  clearance, min feature, spot coverage).
- `scad/a1_reader_head.scad`: revised the flag-read standoff/aperture to the
  DND-115 values (1.8 mm / 0.44 mm).
- `analysis/a1_writer_rate.py`: new `shutter_read_contrast()` and
  `shutter_tolerance_mc()`; `flag_read_contrast()` re-baselined to the DND-115
  standoff/aperture; `common_height_read_target()` and `read_resolution_bound()`
  updated; `OUTCOME_STATEMENT` updated to the closed read axis; `report()` carries
  the new blocks.
- `analysis/render_a1_cad.py`: renders + mesh-validates the `shutter` part and
  **fails hard** if the shutter self-checks do not pass.
- `analysis/reliability_mask_checks.py`: 11 new DND-115 checks (75/75).
- `cad/render_record.json`: now carries the shutter mesh (watertight,
  1.55×1.60×2.75 mm) and the shutter echoes.
- `07-evidence-and-decisions/falsifier_dnd115_checks.py`: **new** default-deny
  auditor (12 attacks after DND-119) that recomputes every shutter number independently.
- `07-evidence-and-decisions/falsifier_dnd114_checks.py`: standoff/aperture
  re-baselined to 1.8 mm / 0.44 mm.
- `.github/workflows/ci.yml`: new **hard gate** running
  `falsifier_dnd115_checks.py --gate`.
- `08-integrated-designs/a1-reliability-first/README.md` §4.2a/§4.7/§6/§10: updated from "residual" to
  "closed".

## 8. Residual uncertainty / evidence classification

- **CAD (rendered, watertight):** the shutter crank + flap, the placed hinge,
  the swept envelope, the flag reader at the revised standoff.
- **CALCULATION:** the shadow fraction (100% / 0%), the 7.72× on/off ratio, the
  absorber Δz (0.55 mm), all clearances, the Monte Carlo stack-up.
- **Assumption-class, unmeasured:** the flap matte reflectance (0.05), the
  standoff (1.8 mm) and aperture (0.44 mm), the printed tolerances, all optical
  constants.
- **Measurement-only (DND-27):** the flap/hinge wear across 6,400 cycles, the
  as-printed snap force, the as-built pitch over 406 mm.
- **No print, no purchase, no measurement** ([DND-27](/DND/issues/DND-27)); no
  board contact ([DND-32](/DND/issues/DND-32)).

Nothing here is a physical validation.

## 9. Verdict

**The read/verify axis is closed at CAD + calculation (outcome a).** DND-114's
frame-fixed vane removed the state-dependent standoff; DND-115's shutter makes
that fixed-standoff return state-dependent: the hidden state covers 100% of the
read spot, the visible state 0%, a **7.72× on/off return ratio** (gate 2×), with
the reflective target still frame-fixed (`Δz = 0`). The recommended,
tolerance-robust configuration uses a **1.8 mm standoff / 0.44 mm aperture** (the
DND-114 1.0 mm standoff is infeasible under the stack-up); the swept flap clears
the neighbour body by 0.280 mm and the own column by 3.42 mm, and the Monte Carlo
stack-up passes at zero failures under realistic tolerances. **DND-119 corrected
the claim framing** from the DND-118 audit with no geometry change: the neighbour
crosstalk is now **modelled and gated** (physical in-cone ratio 0.068, corrected
on/off **6.37×** > 2× gate), the false "off-beam" wording is removed (the
neighbour is weakly in-cone, state-invariant), the vacuous "absorber in DoF"
claim is downgraded to provenance, and the tolerance MC samples an independent
reader/aperture placement so its aperture check can fail (still +0.44/+0.34 mm).
The remaining residuals are assumption-class optical constants and
measurement-only wear. The falsifier companions `falsifier_dnd115_checks.py
--gate` and `falsifier_dnd115_a1_shutter_audit.py --gate` both exit 0.
