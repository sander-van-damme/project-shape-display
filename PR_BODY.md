# Test11 — S1 threshold-ratchet / S2 planar-tile rejection screen + printable 5.08 mm coupon

Invented and stress-tested the two **planar / external-memory** candidate machines for
[DND-3](/DND/issues/DND-3), and produced the cheapest physical object that can reject the
leading one.

**Evidence level: analytic geometry + calculation + CAD source only. No printed or measured
validation.** Remote CI (Actions `engineering-checks`) reproduces the scripts and builds the
coupon STLs; that is not a physical test.

## What changed

- New `06-experiments/test11_threshold_ratchet_s1/`:
  - `geometry.py`, `timing.py`, `rejection.py`, `sensitivity.py`, `checks.py` — hostile
    arithmetic with every term explicit.
  - `build_coupon.py` (emits `params.json`, `manifest.json`, `coupon.scad`, slicer-ready binary
    STLs) and `coupon_checks.py` — printable 5.08 mm-pitch coupon + structural checks.
  - `README.md` (results/gates) and `S1_S2_spec.md` (complete machine spec + part counts).
- `04-architecture-candidates/README.md` — Test11 refinement; adds survivor variant **S1-B
  (banked broadcast ratchet)**.
- `05-research-questions/README.md` — first answers to Q1/Q2/Q5/Q7/Q8.
- `06-experiments/README.md`, `07-evidence-and-decisions/README.md` — experiment table + evidence
  matrix.
- `.github/workflows/ci.yml` — runs the new `checks.py`.

## Engineering question

Can a passive, printable, final-5.08 mm-pitch state/selection element (a) be **selected** by a
shared programmer and (b) **hold** a miniature's load — i.e. do the surviving planar/external-
memory families (S1 broadcast threshold ratchet, S2 swappable planar-memory tiles) survive hostile
arithmetic before any CAD/BOM?

## What passed / failed (arithmetic only)

- **Density is not the killer.** Pawl + gate fit in **2.28 mm** beside a 2.0 mm shaft at 5.08 mm
  pitch once the gate is stacked **above** the pawl in Z; a 2.40 mm rack pocket leaves printable
  rails. The "gate cannot fit at 5.08 mm" fear is unsupported by the pitch budget.
- **S1 fails on force.** An all-high map arms all 6,400 pawls in one stroke → **~2.37 kN** at
  0.37 N/cell (break-even 0.234 N/cell). Revive only via **S1-B banked broadcast** (8 banks ×
  10 rows → ~296 N/stroke, ~17.6 s total, still < 30 s).
- **Mask writing kills both as-is.** 12,800 unary hole/set ops: serial 2,560 s; an 80-channel
  writer is 56 s; needs **≥500 parallel channels** (~9 s) or an **off-line writer** hidden by
  double buffering. This converts S1 into S2 unless disposable media are acceptable.
- **Print variation needs margin, not sorting.** The safe release window survives only to
  ~**9% force sd** across 6,400 printed pawls; no per-cell calibration is affordable.
- **Timing is not the discriminator.** S1 full map ~5.3 s, S2 full ~2.0 s — both pass the 30 s cap
  under stated assumptions. Force and media-writing are the discriminators.
- **S2 survives as a system, not a mechanism** — conditional on an off-line writer and on two
  unproven product properties: **surprise maps** (writer becomes the bottleneck if the next map is
  not known ~1 min ahead) and **exchange disturbance** (Q5 regional isolation; frame stiffness is
  an assumed 100 N/mm input that must be measured).

## Assumptions

- Per-cell pawl release force 0.37 N (assumed); break-even computed in `sensitivity.py`.
- Frame stiffness 100 N/mm (assumed) for the regional-isolation arithmetic — the single most
  important unmeasured input.
- 5 min map re-plan interval; shared-lift stroke 0.55 s; 0.4 mm nozzle / PLA.

## What remains uncertain / most informative next test

The cheapest discriminator for S1, S2 **and** S4 is the **Q5 regional-isolation rig**: two adjacent
true-pitch tiles, one loaded, the neighbor cleared/changed/settled, measuring neighbor peak motion,
residual height error, insertion force, seam step and misreads. Build that before any 10×10 tile.
The coupon's own top gate is **printed pawl release-force sd ≤ 9% of mean** across 10 copies.

## Coupon gates (must be run physically to close)

| Gate | Threshold | If failed |
|---|---|---|
| Missed / double steps over 100 cycles | 0 errors | S1 broadcast decode unreliable |
| Loaded neighbor release (1 N) | < 0.2 mm motion | Regional isolation claim dies |
| Pawl release force spread, 10 copies | sd ≤ 9% of mean | 6,400-part board cannot be trusted |
| Idle holding under 1 N | no creep > 0.2 mm/1 h | Passive load path dies |

## Manifold caveat (honest)

STLs are unions of axis-aligned boxes; where same-part boxes touch face-to-face the mesh is not
strictly edge-manifold (`trimesh.is_watertight` is `False` for `frame`, `pawl`, `assembly`).
Expected for a box union without CSG and handled correctly by slicers; `coupon_checks.py` asserts
slicer-relevant properties, not strict manifoldness.

Co-Authored-By: Paperclip <noreply@paperclip.ing>
