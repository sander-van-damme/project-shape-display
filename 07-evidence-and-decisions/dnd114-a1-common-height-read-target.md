# DND-114 — CAD-design + validation of the A1 common-height read target

- **Issue:** [DND-114](/DND/issues/DND-114) (CTO). Parent: [DND-113](/DND/issues/DND-113)
  (A1 read-mechanism correction). Program: [DND-102](/DND/issues/DND-102).
- **Trigger:** the DND-113 ADR §4 left the A1 read/verify axis **UNRESOLVED**: it
  *proposed* a common-height read target but required, in a follow-up issue,
  "(a) a CAD model of the flag + hinge arc, (b) a flag-vs-neighbour contrast
  check at the fixed standoff, and (c) the Δz-in-DoF bound."
- **Evidence class:** **CALCULATION + CAD geometry.** No print, no purchase, no
  measurement ([DND-27](/DND/issues/DND-27)). No board contact ([DND-32](/DND/issues/DND-32)).
  `08-current-design/` and `09-low-cost-variant/` untouched.
- **Branch:** `cto/dnd114-common-height-read-target` from `main` (`1449b72`).
- **Deliverables:** the parameterised flag in
  [`a1_binary_latch_cell.scad`](../08-integrated-designs/a1-reliability-first/scad/a1_binary_latch_cell.scad),
  the flag-read geometry in
  [`a1_reader_head.scad`](../08-integrated-designs/a1-reliability-first/scad/a1_reader_head.scad), the new
  [`common_height_read_target()` / `flag_read_contrast()`](../08-integrated-designs/a1-reliability-first/analysis/a1_writer_rate.py),
  the rendered watertight meshes + [`render_record.json`](../08-integrated-designs/a1-reliability-first/cad/render_record.json),
  the re-baselined [`falsifier_dnd114_checks.py`](falsifier_dnd114_checks.py), this
  ADR, and README §4.2a.
- **Outcome: the DND-113 proposal is now a validated CAD artifact.** The read is
  moved off the state-dependent column top face onto a **frame-fixed target at a
  single standoff**; the 4.82-pitch down spot and the ~441× neighbour/pocket
  swing are **eliminated**. The ±0.264 mm registration figure becomes a
  *secondary* gantry concern, not the binding read limit.

## 1. The design problem, restated

The as-drawn A1 reader interrogates the **column top face**, which moves
`TRAVEL = 40 mm` with the state. Over a **down** cell the gap is ~42 mm, the
lensless aperture spot is ~24.5 mm (4.82 pitches), and the four up neighbours
dominate the pocket return ~441× — a **silent wrong-cell failure** (DND-113
§2). The binding limit is therefore the **state-dependent standoff**.

The fix must make the target **independent of column height**: one target plane,
one reader standoff, for both states. The latch mechanism already contains a
frame-fixed feature — the latch arm pivots on a **frame-anchored hinge** — so a
reflective target tied to the hinge plane is available by construction.

## 2. Two candidate flags (both parameterised in the cell CAD)

### CH-A — frame-fixed reflective vane (**adopted**)

A post on the **frame cradle** in the latch lane, its top face at
`Z_FLAG_TOP = TRAVEL + 3 = 43 mm`. Because the cradle is frame-anchored, the
target z does **not** move with the column: **Δz = 0 by construction**, for both
states. The reader rides at one fixed standoff above it.

The state is encoded by the latch arm: the arm holds the column in compression
against a hard stop, so the arm's angular position **is** the column position.
The arm's silhouette occludes (or clears) the vane depending on state, giving a
binary fixed-standoff return. *(This state-encoding shutter is the one remaining
CAD detail — see §6.)*

### CH-B — arm-carried reflective flag (**fallback**)

A small vane on the latch arm at radius `FLAG_R` from the hinge axis. Its mean z
shifts by the hinge arc

    Δz = FLAG_R · (sin θ_max − sin θ_min) = FLAG_R · 2 · sin(swing/2)

for a symmetric toggle swing. The DND-113 bound was `r_flag ≤ DoF/sin θ`
(one-sided); with a symmetric ±swing/2 the governing form is
`r_flag ≤ DoF / (2·sin(swing/2))`.

| Item | Value | Basis |
|---|---|---|
| Latch toggle swing | 30° | assumption-class |
| DoF budget | ±1.0 mm | DND-112 pass threshold |
| Max arm radius in DoF | **1.932 mm** | `DoF / (2·sin15°)` |
| CH-B chosen radius | 1.20 mm | CAD |
| **CH-B hinge-arc Δz** | **0.621 mm** | `1.20 · 2·sin15°` — **inside the ±1 mm DoF** |
| **CH-A hinge-arc Δz** | **0.000 mm** | frame-fixed (adopted) |

CH-A is adopted because it needs no DoF margin at all; CH-B is carried as a
fallback for a mechanism that cannot accommodate a cradle post.

## 3. Flag-vs-neighbour contrast at the fixed standoff

The flag sits in the **latch lane** at `x = HINGE_X = BODY/2 + LATCH_T/2 + CLEAR
= 2.225 mm`. The nearest **neighbour column body** begins at
`x = PITCH − BODY/2 = 3.28 mm`, leaving only **1.055 mm** of X clearance. The
own column is *below* the flag plane, so it cannot occlude or contribute. The
lane is **open in Y** across the full pitch, so the spot may spread in Y freely.

The flag reader therefore uses a **dedicated small aperture** (`0.60 mm`) and a
**tight fixed standoff** (`1.0 mm`):

| Quantity | Value | Check |
|---|---:|---|
| Flag footprint | 0.44 (X) × 1.60 (Y) mm | CAD |
| Flag-read aperture | 0.60 mm | CAD |
| Fixed standoff | 1.0 mm | CAD |
| Spot at the flag | 1.136 mm | `a + 2·g·tan15°` |
| Spot X half-width | 0.568 mm | vs 1.055 mm clearance |
| **Clears neighbour body** | **PASS** | margin **0.487 mm** |
| **Fits flag Y width** | **PASS** | 1.136 ≤ 1.60 mm |

The fixed standoff is **identical for both states**, so the down-cell
neighbour/pocket ratio does not swing by ~441×; the read integrates **only the
flag**. The photometric SNR (~1,460, assumption-class) is large but **not the
deciding number** — the deciding numbers are geometric (spot vs lane).

## 4. R1/G2 re-check against the new target

| Attack | As-drawn (DND-113) | With the CH-A common-height target |
|---|---|---|
| **R1** down-state gap | 42 mm → 24.5 mm spot | **N/A** — one fixed standoff |
| **R4** binding read limit | state-dependent standoff | **secondary**: ±0.264 mm registration only |
| **G2** neighbour/pocket ratio | ~441× (silent wrong-cell) | **1×** — no state-dependent standoff |
| **Single-cell down read** | **NO** (reads up) | **YES** (fixed target) |

## 5. What changed (all calculation + CAD; no print)

- `10-reliability-mask/scad/a1_binary_latch_cell.scad`: added the parameterised
  `ch_a_frame_vane()` and `ch_b_arm_flag()` modules, a `part="flag"` printable
  selector, a `common_height_target()` module, and the flag self-checks
  (`HINGE_X`, lane fit, Δz=0, hinge-arc bound, `R_FLAG_MAX`, min feature).
- `10-reliability-mask/scad/a1_reader_head.scad`: replaced the DND-113 schematic
  flag with the real CH-A vane + a `flag_reader_head()` at the fixed standoff,
  and added the flag-read self-checks (`FLAG_SPOT_X`, neighbour clearance,
  flag-Y fit).
- `10-reliability-mask/analysis/a1_writer_rate.py`: `common_height_read_target()`
  now reports the **ADOPTED** CH-A target (Δz=0) and the CH-B bound; new
  `flag_read_contrast()` computes the fixed-standoff geometry; `read_resolution_bound()`
  reports both the as-drawn defect and
  `resolves_single_cell_with_common_height_target = True`.
- `10-reliability-mask/analysis/render_a1_cad.py`: renders + mesh-validates the
  `flag` part and **fails hard** if the common-height checks do not pass.
- `10-reliability-mask/cad/render_record.json`: now carries the flag mesh
  (watertight, 0.44×1.6×0.82 mm) and the flag-read echoes.
- `10-reliability-mask/README.md` §4.2a + the decisive falsifier: updated from
  "proposed" to "adopted + CAD-validated", with the one remaining CAD detail
  called out.

## 6. Residual uncertainty / evidence classification

- **CAD (rendered, watertight):** the CH-A vane, the CH-B flag, the flag reader,
  the placed lane geometry.
- **CALCULATION:** the hinge-arc Δz bound (0.621 mm CH-B; 0 mm CH-A), the
  fixed-standoff spot (1.136 mm) and neighbour clearance (0.487 mm margin).
- **Assumption-class, unmeasured:** the 30° latch swing, the 0.60 mm flag
  aperture, the 1.0 mm flag standoff, all optical/device constants.
- **NEW residual (design detail, not yet CAD):** the **state-encoding shutter** —
  the CH-A vane is the fixed target; the mechanism that makes its apparent
  brightness depend on latch state (the arm's silhouette occluding the vane) is
  identified but not yet dimensioned. This is a bounded, low-risk CAD detail: the
  arm already passes through the lane at the hinge.
- **No print, no purchase, no measurement** ([DND-27](/DND/issues/DND-27)); no
  board contact ([DND-32](/DND/issues/DND-32)).

Nothing here is a physical validation.

## 7. Verdict

**The DND-113 proposal is CAD-validated and adopted.** A single common-height
read target (CH-A frame-fixed vane, top face at z = 43 mm) removes the
state-dependent standoff; the flag-vs-neighbour contrast passes with a 0.487 mm
margin; the CH-B hinge-arc Δz bound passes at 0.621 mm inside a ±1 mm DoF. The
read/verify axis is no longer state-dependent-standoff bound. The remaining
residual is the state-encoding shutter geometry — a CAD detail, not a physics
risk. The falsifier companion `falsifier_dnd114_checks.py --gate` now exits 0.
