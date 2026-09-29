# DND-104: reliability-first low-cost shape display + automatic mask system

Closes [DND-104](/DND/issues/DND-104). Parent [DND-102](/DND/issues/DND-102).
Children folded into this PR: [DND-107](/DND/issues/DND-107) (InventorBeta
divergent machines), [DND-109](/DND/issues/DND-109) (CostManufacturing cost +
printability envelope). [DND-106](/DND/issues/DND-106) (InventorAlpha primitives)
and [DND-108](/DND/issues/DND-108) (Falsifier pre-registered criteria) land on
their own branches/PRs.

## What changed

A **new candidate architecture root `10-reliability-mask/`** plus supporting
divergence and envelope material. `08-current-design/` (S5-R provenance) and the
existing `09-low-cost-variant/` machine definitions are **untouched**.

- `10-reliability-mask/README.md` — the selected machine definition: mechanism,
  reliability audit, honest timing, BOM, prototype ladder, decisive falsifier.
- `10-reliability-mask/analysis/reliability_mask.py` — divergence screen of
  **seven** materially different architectures, the DND-103 reliability gate,
  timing decomposition, BOM, and the convergence/selection record.
- `10-reliability-mask/analysis/reliability_mask_checks.py` — **38/38** pinned
  regression checks (wired into CI).
- `10-reliability-mask/analysis/architecture_table.md` — the full per-architecture
  comparison table (mechanism, actuators, repeated-cell complexity, mask method,
  reset method, timing, BOM, printability, reliability risks, prototype path,
  decisive falsifier).
- `10-reliability-mask/scad/a1_binary_latch_cell.scad` + `cad/stl/*` +
  `cad/render_record.json` — **real OpenSCAD** unit cell, mesh-validated
  watertight.
- `10-reliability-mask/bom_a1.csv` — purchased BOM.
- `09-low-cost-variant/divergent/reliability_machines_beta.*` — InventorBeta
  DND-107: three additional complete machines (B1 screw/nut memory, B2 pressure
  blanket, B3 rotary drum mask) with their own 28 checks + CAD.
- `09-low-cost-variant/reliability_sourcing/cost_envelope_dnd104.*` —
  CostManufacturing DND-109: sourced-class cost + FDM-printability envelope.
- `09-low-cost-variant/divergent/reliability_primitives_alpha.*` — InventorAlpha
  DND-106: reliability-first **cell/selection/reset primitives** (R1 toggle-rocker
  row-shared state, R2 double-acting wedge-gate cell, R3 mechanical read-rod
  readback, R4 shared return bar **rejected**), full reliability-audit schema +
  ten functional jobs, with 30 checks and a true-pitch CAD cell.
- `07-evidence-and-decisions/dnd104-reliability-mask.md` — the decision record;
  evidence matrix updated.
- `.github/workflows/ci.yml` — DND-104 checks + a `dnd104-cad-render` job.

## Engineering question

Which machine actually answers DND-103's gate — **"what has to work correctly
6,400 times?"** — and can it still meet ~400×400 mm / 5.08 mm / 6,400 cells /
≥40 mm travel / <30 s / <$250 purchased?

## Evidence produced

- **Divergence of seven architectures** (A1–A7), then selection: nothing pre-picked.
- **Reliability gate result.** A1 (`binary-latch + shared writer/reader`) is the
  **only** architecture with a **structurally zero silent-error set** and the only
  one passing the tabletop-load gate (DND-91 A7). Every other architecture has
  ≈6,400 silent elements. On the program model `(1−q)^6400`, at q=1e-4 that is
  100 % vs 52.7 % map correctness.
- **Selection:** A1 — two-state columns held by an over-centre latch between two
  printed hard stops (zero compliant parts deciding correctness, zero precision
  contacts/cell), a shared 2-axis gantry that writes only changed cells then
  **reads every cell back** so a failed toggle is detected and re-driven.
  **$181.00 parts / $209.96 delivered**, **24.15 s** worst case *including*
  verification, **4 bought actuators**, no per-cell/no per-row bought actuator.
- **Honest timing:** no physical mask ⇒ sustained cycle time **equals** visible
  transition time. Write and verify terms are **computed** from head count × rate.
- **CAD:** binary-latch unit cell rendered with real OpenSCAD, watertight, bed-fitting.
- **Full comparison table** with a decisive falsifier recorded per architecture.
- **DND-106 primitives (InventorAlpha):** three materially different
  reliability-first primitives, each answering the full reliability-audit schema:
  R1 cuts the "must work 6,400 times" count to **80 row-rocker decisions** (80×
  looser q, 80-cell detectable blast radius); R2 makes reset a **platen-driven
  positive hard stop**, removing DND-91's A8 gravity-drop failure class; R3 adds
  **80 mechanical read points** (2 bought sensors, $4) turning a correlated error
  into a detectable/recoverable one. R4 (shared return bar: 3,904 N summed, one
  jam stalls all) is recorded **REJECTED**. 30/30 checks; the machine clears the
  <30 s visible gate at **11.80 s**; analytic printability: all walls PASS, only
  the intentional compliant R3 sensing finger is RISK.

## Assumptions

- Writer/reader rate 1 ms/cell at 8 parallel heads (assumption-class; **prototype
  B is the kill test**).
- Gantry XY registration over 406 mm, hinge wear, and as-printed hard-stop
  dimensions are unmeasured.
- Sourced-class point-in-time prices (2026-09); no quotation obtained.

## What passed / failed

- **Passed:** 38/38 DND-104 checks; 28/28 InventorBeta checks; CostManufacturing
  envelope gate; 30/30 DND-106 InventorAlpha primitive checks (+ analytic CAD);
  all pre-existing S5-R/S6-LC/falsifier gates (no regressions).
- **Failed / rejected (recorded, not hidden):** A2 global interlock, A3 punched
  film, A4 rewritable comb, A6 embossed tape (6,400 silent elements; A3 also
  >30 s); A5 (bank-only readback, 6,392 silent); A7 (camshaft repeatability +
  6,400 silent). InventorBeta's B1 shared driveshaft FAILS as drawn (timing- and
  torque-feasible sets disjoint).

## What remains uncertain

- The 1 ms/cell writer/reader rate and single-cell read resolution — the whole A1
  reliability advantage rests on prototype B.
- Gantry registration, hinge wear, printed hard-stop dimensions (measurement-only
  under [DND-27](/DND/issues/DND-27)).

## Most informative next test

**Prototype A** (one cell: latch toggle + reader distinguish) then **Prototype B**
(5×5 array: writer/reader scan + a deliberately stuck cell caught by retry) — the
cheapest tests that bound the A1 falsifier.

## Governance / evidence discipline

CALCULATION over sourced FDM limits + sourced actuator ratings, plus CAD. **No
print, no purchase, no measurement** ([DND-27](/DND/issues/DND-27)). No
`08-current-design/` change. No board contact ([DND-32](/DND/issues/DND-32)).
