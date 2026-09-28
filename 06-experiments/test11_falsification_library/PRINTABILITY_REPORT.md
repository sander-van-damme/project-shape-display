# J2 isolation-rig printability report (slicer-level)

**Issue:** [DND-16](/DND/issues/DND-16) · **Inputs:** J2 STL bundle from [DND-14](/DND/issues/DND-14)
(attachment `j2_stl_bundle.zip`, sha256 `9444cd44044ddb85c9674d41e419bb32262329d9468d896cba542c6582f4cde1`),
`j2_isolation_rig.scad` @ `b34d6b1`.

**Evidence class:** CALCULATION + CAD ANALYSIS over the exported STL. This is a
rasterised slice simulation (0.20 mm layers, 0.05 mm in-plane sampling), **not**
a slicer binary and **not** a physical print.

**Baseline under test (from the SCAD header / `02-design-criteria`):** Bambu X1C,
PLA, 0.4 mm nozzle, 0.20 mm layers, 3 perimeters, 5 top/bottom, 15% gyroid.

**Verdict: PRINT-READY PENDING HARDWARE**, with two non-blocking corrections
listed at the end (a dead `chamfer_mm` parameter and an over-broad "no overhang"
claim). No print-blocking feature found.

## Method

`printability_slice_check.py` (added alongside this report) loads each STL,
checks mesh health, computes overhang faces from triangle normals, then
rasterises each 0.20 mm cross-section and measures wall/feature thickness from
the Euclidean distance transform of the layer material (a wall of width *w* has
an EDT ridge at ≈*w*/2; thickness = 2·EDT on the medial axis). Feature floor for
3 perimeters at 0.4 mm is **1.2 mm**. Sourced from STL *geometry*, so it is
independent of the SCAD comments.

## Per-part results

| Part | BBox (mm) | Watertight | Shells | Overhang faces (real >0.5 mm²) | Min wall (mm) | First-layer area (mm²) | Bed fit (256×256) |
|---|---|---|---|---|---|---|---|
| `holder_5x5` | 37.4 × 37.4 × 8.0 | yes | 1 | 248 (0) | 2.4 | 1360 | ✅ |
| `holder_10x10` | 62.8 × 62.8 × 8.0 | yes | 1 | 248 (0) | 2.4 | 3903 | ✅ |
| `base_rail` | 146.0 × 70.8 × 12.0 | yes | 1 | 0 (0) | 2.2 | 10259 | ✅ |
| `indicator_bracket` | 24 × 24 × 18 | yes | 1 | 32 (32) | 0.8* | 570 | ✅ |
| `miniature_tray` | 29.4 × 29.4 × 3.0 | yes | 1 | 0 (0) | 2.0 | 861 | ✅ |
| `plate` (layout) | 131.6 × 128.2 × 18.0 | yes | 6 | 560 (32) | 0.8* | 10666 | ✅ |

\* The 0.8 mm is a **single-scanline rasterisation artifact** at the bracket's
M3 clearance hole tangent (z = 1.6 mm, one layer, 5th-percentile thickness
9.6 mm). All other 88 layers of that part are ≥ 1.2 mm. The base plate is a
solid 24 × 24 mm slab there — the metric is aliasing two near-equal EDT ridges,
not detecting a real feature. **No real feature in any part is below 1.2 mm.**

## Step-by-step findings (issue's 5 checks)

### 1. Minimum wall thickness vs 0.4 mm nozzle / 3 perimeters — PASS
Minimum real wall across the set is **2.0 mm** (`miniature_tray` sides),
**2.2 mm** (`base_rail` M3-slot walls), **2.4 mm** (holders), all ≥ 1.2 mm and
all comfortably ≥ 3 × 0.4 mm. The declared 6.0 mm holder border, 3.0 mm tray and
12 mm rail are far from the limit. No sub-1.2 mm feature exists.

### 2. Overhangs vs the "no supports" claim — PASS for the rig, with a claim correction
- `holder_5x5`, `holder_10x10`: **248 downward faces each, but every one is a
  zero-thickness sliver from the socket boolean cut** (max single face
  0.283 mm², total 36 mm²). The socket is cut from the open side, so there is
  **no real bridge**; the "all overhangs ≤ 45° by construction" claim holds for
  the holders.
- `base_rail`, `miniature_tray`: **zero** downward faces. Straight column prints.
- `indicator_bracket`: **32 real overhang faces (103 mm²)** — the crown of the
  horizontal M3-indicator stem hole (Ø8.2 mm, axis along Y, z ≈ 3.9–12.1 mm).
  The hole crown approaches horizontal (nz → −1.0). This is the standard FDM
  "horizontal round hole" overhang: self-supporting layer-by-layer at 0.20 mm
  for an 8.2 mm hole, but it **is** > 45° and the SCAD header's blanket
  "no supports, all overhangs ≤ 45° by construction" is factually wrong for this
  part. Non-blocking; see correction C2.

### 3. Plate layout spacing vs 6 mm, and bed footprint — PASS
Measured shell decomposition of `plate.stl` (6 shells, as the CAD claims):

| Shell | x (mm) | y (mm) | Gap to neighbour |
|---|---|---|---|
| holder A | 0–62.8 | 0–62.8 | — |
| holder B | 68.8–131.6 | 0–62.8 | **6.0 mm** to A |
| tray A | 0–29.4 | 68.8–98.2 | **6.0 mm** below holder row |
| tray B | 35.4–64.8 | 68.8–98.2 | 6.0 mm to tray A |
| bracket A | 0–24 | 104.2–128.2 | **6.0 mm** below tray row |
| bracket B | 30–54 | 104.2–128.2 | 6.0 mm to bracket A |

Overall plate **131.6 × 128.2 mm** ≪ 256 × 256 (≈ 48% × 50% of the bed). The
**base_rail (146.0 × 70.8 mm) is not on the plate** and must print as a second
job; it also fits the bed. Total two-plate print, no part is bed-limited at the
5×5/10×10 sizes.

### 4. Socket pocket depth (1.0 mm) prints without an internal bridge — PASS
Column probe through the holder at the active-field centre (x = y = 30 mm,
tile = 10):

```
solid   0.00 → 2.00 mm   (2.0 mm floor)
void    2.00 → 3.00 mm   (1.0 mm socket pocket)
void    3.00 → 8.00 mm   (open active field)
```

The socket is an **upward-open recess in the floor's top face**, with 2.0 mm of
solid floor beneath it. The only downward face is the 1095 mm² socket floor at
z = 2.0, fully supported by the 2 mm slab below it. **No internal bridge, no
support, prints as a clean one-sided part.** This also independently re-confirms
the [DND-14] buried-socket fix: the pocket is genuinely open.

### 5. Findings / required SCAD edits — no hard blocker
No print-blocking feature. Two corrections are worth folding into the next
`j2_isolation_rig.scad` revision (both cosmetic-to-minor, neither blocks the
first print):

- **C1 (dead parameter):** `chamfer_mm = 0.6` is declared (line 45) and never
  used anywhere in the geometry. Either apply the edge chamfer it promises or
  delete the parameter and its comment. First-layer elephant-foot at the seam
  face is currently unmitigated; with 2.0–2.4 mm minimum walls and 0.03 mm
  typical X1C elephant-foot, this is very unlikely to matter, but the code and
  the comment disagree and should be reconciled.
- **C2 (claim correction):** the header says "no supports (all overhangs
  ≤ 45 deg by construction)". That is true for the holders, rail and tray, but
  the `indicator_bracket` stem hole has > 45° crown overhangs. Either narrow the
  claim to the parts it applies to, or reorient the bracket (print the stem hole
  axis vertical) / make it a teardrop. Recommended: narrow the claim, note the
  round-hole overhang as expected and self-supporting.

## What this does and does not prove

- **Does:** every exported part is manifold and watertight; walls, first layers,
  plate gaps and bed fit are within the X1C/0.4 mm baseline; the socket is a real
  open pocket with no internal bridge; the only > 45° overhangs are the bracket
  stem-hole crown, which FDM handles without support at this diameter.
- **Does not:** replace a slicer binary (no per-feature/perimeter toolpath
  simulation, no actual slice time / layer count / support-generation run was
  executed — no slicer is installed in this environment), and says nothing about
  material strength, warping, dimensional accuracy or the physical part. A
  print-ready claim still ends at the printer.

## Smallest next test

Slice `plate.stl` + `base_rail.stl` in Bambu Studio / Orca with the baseline
profile and confirm (a) zero auto-supports generated, (b) slice time and one-plate
layout, (c) layer count matches ~40 (holder) / ~60 (rail). That is the only step
between this report and the physical print.

---

*Reproduce:* `python3 06-experiments/test11_falsification_library/printability_slice_check.py <stl...>`
(requires numpy + scipy; no slicer binary needed).
