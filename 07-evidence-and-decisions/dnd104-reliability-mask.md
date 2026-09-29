# DND-104 — Reliability-first low-cost shape display + automatic mask system

- **Issue:** [DND-104](/DND/issues/DND-104) (CTO). Parent [DND-102](/DND/issues/DND-102).
- **Criteria of record:** [`02-design-criteria/README.md`](../02-design-criteria/README.md)
  (strengthened by [DND-103](/DND/issues/DND-103), PR #83).
- **Deliverable:** new candidate architecture `A1 binary-latch + shared
  writer/reader` under [`10-reliability-mask/`](../10-reliability-mask/README.md).
- **Evidence class:** **CALCULATION** over sourced FDM limits + sourced actuator
  ratings, plus **CAD** (real OpenSCAD + trimesh mesh validation). **No print, no
  purchase, no measurement** ([DND-27](/DND/issues/DND-27)). No board contact
  ([DND-32](/DND/issues/DND-32)).
- **Does not touch** `08-current-design/` (S5-R provenance) or
  `09-low-cost-variant/` (S6-LC). A1 is a new, separate candidate root.
- **Reproduce:** `python 10-reliability-mask/analysis/reliability_mask.py`
  (`convergence` arg for the decision view), `..._checks.py` (35/35),
  `render_a1_cad.py`, `make_table.py`.

## 1. The problem this program addresses

DND-103 made **reliability a first-class gate** and posed the decisive question:
**"What has to work correctly 6,400 times?"** Both prior machines answer "6,400":

| Machine | Repeated elements that must be perfect | Feedback |
|---|---:|---|
| S5-R | 6,400 passive pawl+rotor cells | none |
| S6-LC | 6,400 passive pawl+pocket cells | none (G8 explicitly unresolved) |

At a plausible 0.01 % per-cell defect rate, `P(map correct) = (1−q)^6400 = 52.7 %`.
A missed latch is **silent** — the operator cannot see or correct it. S6-LC's own
adversarial audit ([DND-91](/DND/issues/DND-91), A6) found exactly this and left
it open. This is the structural weakness the program must remove.

## 2. Divergence (≥6 materially different architectures, before selection)

The DND-104 brief required comparison of at least: S6-LC-style threshold masks;
automatically punched film/sheet; continuous punched tape; reusable mechanical
comb masks; automatically rewritten printed combs; and ≥1 novel alternative. The
screen defines **seven** and prints every field for each
([`reliability_mask.py`](../10-reliability-mask/analysis/reliability_mask.py),
table in [`architecture_table.md`](../10-reliability-mask/analysis/architecture_table.md)):

| # | Architecture | Family | Bought actuators | Silent elements | Full map | Parts |
|---|---|---|---:|---:|---:|---:|
| **A1** | binary-latch + shared writer/reader | external shared writer/verifier | 4 | **0** | 24.15 s | $181 |
| A2 | global broadcast binary interlock | broadcast lock-and-lift | 2 | 6,400 | 11.05 s | $224 |
| A3 | punched-film mask | physical bit-image film | 2 | 6,400 | 33.55 s | $187 |
| A4 | rewritable printed comb | reusable comb | 2 | 6,400 | 17.55 s | $171 |
| A5 | banked binary ratchet + coarse readback | threshold ratchet (S6-LC evolved) | 4 | 6,392 | 17.05 s | $213 |
| A6 | embossed-tape mask | relief tape | 2 | 6,400 | 29.55 s | $179 |
| A7 | shared-camshaft bank | rotating camshaft | 1 | 6,400 | 13.05 s | $158 |

Every record includes the ten-job allocation, mask-generation method, reset
method, timing decomposition, BOM sketch, printability class, correlated vs
single-cell failure modes, prototype coupon and a **decisive falsifier**.

## 3. Reliability gate result

The gate scores the **silent-error set** `N_s` — repeated mechanisms whose single
failure yields a wrong cell the machine cannot notice — plus readback and a cheap
coupon. A1 is the **only** architecture with `N_s = 0`, because a shared reader
pass verifies every cell and failed toggles are re-driven (bounded retry). A1 is
also the only architecture with **zero precision contacts per cell and zero
compliant printed parts deciding correctness**: its state is bounded by two
printed hard stops and held in compression (the DND-103 "preferred" list).

The reliability gate also exposed a second product failure across **all**
global-lift architectures: a miniature sitting on the moving common platen
(DND-91 A7). A1 works region-by-region and is the only architecture that passes
the tabletop-load gate without a larger lift axis.

## 4. Decision

**Selected: A1 binary-latch + shared writer/reader** — the only all-gate-feasible
machine (reliability, tabletop load, <30 s, <$250 purchased parts).

| Machine | Bought actuators | Silent cells | Full map | Parts | Delivered | Reliability gate |
|---|---:|---:|---:|---:|---:|---|
| S5-R (`08-`) | 42 | 6,400 | 24.615 s | $348.79 | $404.60 | fails |
| S6-LC (`09-`) | 3 | 6,400 | 11.96 s | $226.77 | $263.05 | unresolved (G8 measurement-only) |
| **A1 (`10-`, new)** | **4** | **0** | **24.15 s** | **$181.00** | **$209.96** | **passes** |

A1 is **proposed for promotion** as the reliability-first low-cost candidate,
**conditional on** prototype A/B bounding the writer/reader rate (~1 ms/cell) and
the latch toggle. This is an **explicit proposal**, not a silent replacement — S5-R
and S6-LC are unchanged (per DND-104 §5).

## 5. Honest timing

A1 has **no physical mask**, so there is no hidden preparation: sustained
arbitrary-map cycle time **equals** the visible transition time (24.15 s worst
case). Stages: digital 0.05 / mask generation 0.00 / transport 2.0 / reset 3.0 /
write 8.8 / settle 1.5 / verify 8.8. The write and verify terms are **computed**
from the head count and rate, not asserted.

## 6. Residual uncertainty (measurement-only under DND-27)

- Writer/reader rate (1 ms/cell) and single-cell read resolution — assumption-class;
  **prototype B is the kill test**.
- Gantry XY registration over 406 mm (belt stretch, thermal) — unmeasured.
- Hinge wear across 6,400 pivots — measurement-only.
- As-printed hard-stop dimensions and toggle snap-force spread — measurement-only.
- Column top land dimensions — CAD-provisional until a calibration coupon exists.

A1 is **not** claimed print-ready or physically validated. It is a definition whose
every mission gate passes on the DND-27 evidence classes and whose reliability
structure converts 6,400 silent failures into a monitored, recoverable, local
failure.

## 7. Failed ideas recorded

- **A2 global broadcast binary interlock** — attractive actuator count (2) and
  speed (11.05 s) but 6,400 silent elements and a precision per-level interlock
  plate; fails the reliability gate and the tabletop-load gate.
- **A3 punched film / A6 embossed tape** — consumables that must register to
  <0.1 mm and can tear/creep; 6,400 silent elements. A3 also fails <30 s.
- **A4 rewritable comb** — no consumable, but the comb writer is itself a repeated
  precision mechanism and a stuck slat silently corrupts an 80-cell band.
- **A5 S6-LC-evolved** — best of the rest (score 6.4) but bank-only readback leaves
  6,392 silent elements; readback granularity, not its presence, is the gate.
- **A7 shared camshaft** — fewest actuators (1) but a printed 80-lobe camshaft to
  ≤0.1 mm angular repeatability is unproven and leaves 6,400 silent elements.
