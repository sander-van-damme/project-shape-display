# DND-113 — CTO response to the DND-112 read finding: A1 read mechanism correction

- **Issue:** [DND-113](/DND/issues/DND-113) (CTO). Parent gate: [DND-111](/DND/issues/DND-111).
  Auditor: [DND-112](/DND/issues/DND-112) (Falsifier). Program: [DND-102](/DND/issues/DND-102).
- **Trigger:** the DND-112 audit ([`falsifier_dnd112_a1_rate_audit.md`](falsifier_dnd112_a1_rate_audit.md),
  PR #88) returned **NOT CLEAN (default-deny)**: the DND-111 *rate* bound
  reproduces, but the **single-cell read** claim fails against DND-111's own
  geometry (R1, R2, R4, G2).
- **Evidence class:** **CALCULATION + CAD geometry.** No print, no purchase, no
  measurement ([DND-27](/DND/issues/DND-27)). No board contact ([DND-32](/DND/issues/DND-32)).
  `08-current-design/` and `09-low-cost-variant/` untouched.
- **Branch:** `cto/dnd113-read-mechanism` from the DND-112 audit tip (`447c8bc`).
- **Deliverables:** the corrected
  [`a1_writer_rate.py`](../10-reliability-mask/analysis/a1_writer_rate.py),
  [`a1_reader_head.scad`](../10-reliability-mask/scad/a1_reader_head.scad), the
  updated model/checks/README, this ADR, and the re-baselined
  [`falsifier_dnd112_checks.py`](falsifier_dnd112_checks.py).
- **Outcome: the audit is accepted.** The rate axis stays **BOUNDED**; the
  read/verify axis is re-stated as a **state-dependent-standoff mechanism
  problem** (option **b**) with a concrete **common-height read target
  proposed** (option **a** design), and a rate trade study for the descending
  reader.

## 1. The two required questions, answered

DND-113 asked for a or b. The honest answer is **b, with a proposed a**:

**a. Common-height read target — does ANY A1 artifact read a single plane for
both states?** **No.** The only reader artifact,
[`scad/a1_reader_head.scad`](../10-reliability-mask/scad/a1_reader_head.scad),
targets the **column top face**, which moves `TRAVEL = 40 mm` with the state.
No latch toe/flag read at fixed z is specified anywhere in A1. The audit is
therefore **correct on the artifacts as they stand**. A common-height target is
*mechanically available* (see §4) and is **proposed**, but it is **not yet a
validated artifact** and must not be treated as one.

**b. Re-state the read as a state-dependent-standoff problem.** **Yes — done.**
The binding read limit is the **state-dependent standoff**, not the ±0.264 mm
gantry registration. The model, ADR and README now carry that, with the rate
trade study (§5). The ±0.264 mm number is retained **only as up-state
provenance**; it is explicitly no longer the decisive residual.

## 2. The finding, reproduced (CALCULATION + CAD)

All four FAILs reproduce exactly against the placed geometry
(`10-reliability-mask/analysis/a1_writer_rate.py`, `read_resolution_bound()`):

| Item | Value | Source |
|---|---:|---|
| Up-state interrogated gap | 2.0 mm | assumption-class |
| Up-state spot (DND-111's 3.072 mm) | 3.072 mm | aperture + 2·g·tan15° |
| **Down-state gap** | **42.0 mm** | 40 (travel) + 2 |
| **Down-state spot** | **24.508 mm = 4.824 pitches** | same formula, g = 42 |
| Neighbour return / pocket return | **~441×** | Lambertian A/d² proxy |
| Corrected corner reach (aperture at cell corner) | **4.081 mm** | √2·(BODY/2) + spot/2 |
| DND-111's wrong `CORNER_REACH` | 2.172 mm | `spot/2·√2` (centred aperture) |
| Neighbour top-face near edge (true crosstalk threshold) | 3.280 mm | PITCH − BODY/2 |
| Registration number (up-state only) | ±0.264 mm | half_face − spot/2 |

**The consequence is a silent wrong-cell failure.** A down cell surrounded by up
neighbours returns mostly neighbour light; the reader classifies it **up**. That
is exactly the failure A1's readback/retry loop exists to prevent — so the audit
is right that A1's *sole reliability advantage* is unproven until the read is
fixed. The photometric contrast (SNR ~1,460) is large but **irrelevant** here:
the problem is geometric, not contrast.

## 3. What changed (all calculation + CAD; no print)

### 3.1 Read model — corrected and residual carried

`read_resolution_bound()` now computes and reports:
- `spot_up_state_mm` = 3.072 and `spot_down_state_mm` = 24.508 (4.82 pitches);
- `corner_reach_mm` = **4.081** (the correct worst case);
- `neighbour_near_edge_mm` = 3.28 and `spot_contaminates_neighbour` (R3);
- `standoff_ratio_neighbour_over_pocket` = **441.0** (G2);
- `registration_tolerance_mm` = 0.264 retained **as provenance only**;
- `binding_read_limit = "state_dependent_standoff"`;
- `resolves_single_cell = False` for the **as-drawn** fixed-height top-face
  reader.

### 3.2 Two new model functions

- **`common_height_read_target()`** — answers question (a): *no existing A1
  artifact reads a common-height target*; and specifies the **proposed** fix:
  a reflective flag on the **frame-anchored latch hinge** (fixed z), read at one
  standoff for both states, with the latch tilt encoding the state. Its hinge-arc
  Δz bound must stay inside the reader depth of field (`r_flag ≤ DoF/sin θ`;
  ≤1.93 mm for a 30° swing and a ±1 mm DoF budget).
- **`z_stroke_trade_study()`** — prices the alternative (a reader that descends
  to the down pocket), see §5.

### 3.3 CAD — corrected geometry and the defect made visible

`scad/a1_reader_head.scad` now:
- computes `SPOT_UP` and `SPOT_DOWN` and echoes both (24.51 mm = 4.82 pitches);
- replaces `CORNER_REACH = spot/2·√2` with the correct
  `CORNER_HYP + SPOT_UP/2 = 4.081 mm`;
- uses the **neighbour near edge** (3.28 mm) as the crosstalk threshold (R3);
- renders the down-state cone (red) over the 3×3 patch, so the ~5-cell
  overreach is visible in the render, and a schematic common-height flag.

The render record (`cad/render_record.json`) now carries
`SPOT_DOWN_diameter=24.5077`, `CORNER_REACH_corrected=4.08148`,
`down-state single-cell read resolvable: false`.

### 3.4 Two bundled small fixes (DND-112 non-decisive defects)

- **T1 stop-and-go trapezoid.** `stop_and_go_cell_time_s()` now uses the correct
  speed-limited **trapezoid** `2·(v/a) + (p − v²/a)/v` when `√(a·p) > 500 mm/s`.
  The aggressive 100 m/s² row is **61.9 cells/s**, not DND-111's 89.6 (+45 %
  optimistic). (Still excluded; the sourced X1C 20 m/s² row is unchanged at
  30.4.)
- **T3 per-line ramp.** `full_cycle()` now **adds** the per-line accel/reversal
  (`raster_pass_time_s()`): at 8 heads, 10 lines × 2·(v/a) = **1.0 s per pass**.
  The honest 8-head cycle is **18.278 s** (was the idealised 16.278 s), **still
  < 30 s**. The head sweep: 4 heads = 30.006 s (just misses), 8 = 18.28 s, 16 =
  12.41 s.

## 4. Option (a) — the concrete common-height read target (PROPOSED)

The mechanism already contains a frame-fixed feature: the latch arm pivots on a
**frame-anchored hinge** whose z does not move with column height. The proposal:

1. Put a small **reflective flag** on the latch arm at/near the hinge, so its
   centroid z stays within the reader depth of field for both latch positions.
2. The reader interrogates that flag at **one standoff** for both states; the
   latch **tilt** (state) changes the returned intensity (bright face vs dark /
   tilted face), giving a binary read.
3. Because the latch holds the column in **compression against a hard stop**, the
   latch position **is** the column position — so reading the latch remains a
   valid verification of the column state.

Why this is the right direction: it removes the 40 mm state-dependent standoff
entirely, so R1/G2 vanish and the ±0.264 mm registration claim can be reinstated
*with the correct geometry* (and the corner-reach number of §3.3).

**Status: PROPOSED, not validated.** It needs, in a follow-up issue (a) a CAD
model of the flag + hinge arc, (b) a flag-vs-neighbour contrast check at the
fixed standoff, and (c) the Δz-in-DoF bound. Until then A1's read axis is
**unresolved** and DND-110's "SUCCESS-eligible on the rate axis" must **not**
extend to the read/verify axis.

## 5. Option (b) rate trade study — descending the reader

If no common-height target is adopted, the reader must move in Z to hold the
standoff. `z_stroke_trade_study()` bounds it (trapezoidal 40 mm each way at
0.5 m/s, X1C 20 m/s²):

| Variant | Per-cell rate | Full-cycle cost |
|---|---:|---:|
| Z stroke **per cell** | **5.4 cells/s** | **> 2,380 s (both passes)** — **rate-fatal** |
| Z refocus **per line** (row ends) | — | **~29.8 s** (80 rows × 2 passes) — must be **priced** into the cycle |

A per-cell Z stroke collapses the cycle by ~130× — the fly-over rate model dies.
A per-line refocus is the only rate-compatible variant, but it costs ~29.8 s on
its own, which **exceeds the 30 s gate** unless the write/verify time shrinks
(fewer, larger strokes; a faster Z axis; or fewer refocus points). **Conclusion:
correct the standoff with a common-height target (§4), not by descending the
reader.**

## 6. Consequence for the DND-110 gate

- **Rate axis: BOUNDED (outcome a).** Unchanged; the audit reproduced T2/T4 and
  the bundled fixes make the decisive table exact.
- **Read/verify axis: UNRESOLVED.** The old "SUCCESS-eligible on the rate axis"
  must **not** extend to the read/verify axis. A1's reliability advantage
  (readback + retry) is unproven until the read target is settled.
- **Decisive next step:** the common-height read target (§4) is the highest-value
  follow-up: it converts the read from a mechanism failure back into a bounded
  geometric/contrast question. Recommend a child issue to CAD-design and validate
  the latch flag; only then can the ±0.264 mm registration claim be reinstated
  with the corrected corner-reach geometry.

## 7. Residual uncertainty / evidence classification

- **Reproduced (CALCULATION):** T2 fly-over 164.5; T4 seven-stage 16.278.
- **Corrected (CALCULATION):** T1 aggressive row 61.9 (was 89.6); T3 ramp
  overhead now priced → 18.278 s.
- **Accepted and CARRIED (CALCULATION + CAD):** R1 (down spot 24.51 mm/4.82
  pitches), R4 (standoff is binding, registration is provenance), G2 (441×).
- **Fixed (CAD):** R2 corner reach 4.081 mm; R3 neighbour-edge threshold.
- **Assumption-class, unmeasured:** all optical constants (5 mW LED, 0.45 A/W,
  0.80/0.15 reflectance, 15° half-angle, 2 mm aperture/gap, TIA noise). None is
  the deciding number for R1/G2 — those are geometric.
- **NEW residual (design intent, not CAD):** the proposed common-height flag.
- **No print, no purchase, no measurement** ([DND-27](/DND/issues/DND-27)); no
  board contact ([DND-32](/DND/issues/DND-32)).

Nothing here is a physical validation.

## 8. Verdict

**The DND-112 audit is ACCEPTED.** R2 is fixed, T1/T3 are fixed, and R1/R4/G2
are carried as the corrected read residual. The DND-112 companion checker
`falsifier_dnd112_checks.py --gate` now exits 0, asserting the resolution. The
rate bound stands; the read/verify axis is explicitly **not** SUCCESS-eligible
until a common-height read target is CAD-designed and validated.
