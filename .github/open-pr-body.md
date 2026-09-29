# DND-117: restructure repo to `08-integrated-designs/` (retire `09-`/`10-`)

## What changed

The numbered root flow now **terminates at 08**. `08-integrated-designs/` is the single
container for complete machine architectures, and the old per-design top-level stages are retired.
This is an **information-architecture migration** ([DND-116](/DND/issues/DND-116) parent); no
engineering conclusion changed.

## Engineering question addressed

How should the repository represent alternative machine architectures so that a new architecture
does **not** create a new numbered engineering stage (`09-`, `10-`, `11-`, …)? Stage 08 must hold
multiple integrated designs with distinct statuses, while incomplete exploration stays in the
candidate/experiment stages.

## Moves (git-aware, history preserved)

| Old | New |
|---|---|
| `08-current-design/` | `08-integrated-designs/s5r-shared-drive-register/` |
| `10-reliability-mask/` | `08-integrated-designs/a1-reliability-first/` |
| `09-low-cost-variant/s6lc/` | `08-integrated-designs/s6lc-low-cost/` |
| `09-low-cost-variant/*` (S5-R-trim negative result, divergent machines, primitives, sourcing, reliability primitives/machines) | `06-experiments/test14_low_cost_program/` (exploratory provenance — **not** a promoted integrated design) |

`09-low-cost-variant/README.md` and `divergent/README.md` link to the selected S6-LC and to
`07-evidence-and-decisions`; the divergent A1/A2/A3 and the DND-106/DND-107 machines remain
**architecture candidates / experiments**, not stage-08 designs.

## New documentation

- **`08-integrated-designs/README.md`** — stage entry point: what qualifies for stage 08 (integrated
  machine architecture, **not** physical validation); multiple designs may coexist; status table read
  from the repo; where new exploratory designs belong; and the explicit rule that future alternative
  designs must **not** create new numbered root stages. Status vocabulary: CANDIDATE, PROMOTED,
  SUPERSEDED, REJECTED, MEASUREMENT-GATED, ARCHIVED.
- **`CONTRIBUTING.md`** — durable repository contribution rule: *new machine architectures do not
  receive new numbered root directories*.
- Per-design status/relocation notes in each design README.
- Root `README.md`, `01-project-description`, `04-architecture-candidates`, `06-experiments`,
  `07-evidence-and-decisions` updated so the flow ends `07 -> 08 integrated designs`.

## Status assigned (read from the repository, not guessed)

| Design | Primary idea | Status | Evidence class |
|---|---|---|---|
| S5-R | shared-drive programmable rotary register | **PROMOTED** (historical single-winner; slicer-ready package of record) | CAD + CALCULATION; measurement-only residue |
| S6-LC | low-cost broadcast / mask-gate | **MEASUREMENT-GATED** (mission gates pass; per-cell reliability G8 unresolved) | CAD + CALCULATION |
| A1 | binary-latch + shared writer/reader | **CANDIDATE** (selected reliability-first candidate) | CAD + CALCULATION |

## Path fixes (no script left broken)

- Depth-sensitive repo-root derivations updated for the +1-level moves: S5-R fabrication tools
  (`FAB.parents[1] -> parents[2]`), A1 `reliability_mask(.checks)`, `test12/register_checks.py`.
- `06-experiments/test14_low_cost_program`: `s5r_ultra(.checks)`, divergent tooling/analysis,
  `s6lc/analysis/render_s6lc_images.py` sys.path.
- `07-evidence-and-decisions/falsifier_dnd74_checks.py` and `falsifier_dnd91_checks.py` re-pointed
  to `08-integrated-designs/s6lc-low-cost/`.
- `.github/workflows/ci.yml`, `.github/open-pr-body.md`, `tools/validate/validate_geometry.py`,
  `tools/validate/readme_s5r_coherence.py` updated.

## Historical truth preserved

ADR-002 (`convergence-decision-2026-09-b.md`) keeps its original wording ("promoted to
`08-current-design/`") with a **relocation note**; the 07 README carries one consolidated relocation
note for pre-DND-117 records. Links are repointed; wording is not rewritten.

## Verification (commands + results)

Evidence class: **CAD + CALCULATION** over sourced listings. No print/measurement
([DND-27](/DND/issues/DND-27)).

- `08-integrated-designs/s5r-shared-drive-register/fabrication/tools/fab_package_checks.py` → **GATE PASS (C1–C8)**
- `tools/validate/readme_s5r_coherence.py` → **GATE PASS (R1–R6)**
- `tools/validate/validate_geometry.py --no-render` → **HARNESS OK**
- `render_images.py --check` → PASS (45 images); `render_machine.py --check` → PASS (8 images);
  `gen_manifests.py` reproduces (14 parts, 25,661 pieces)
- `a1-reliability-first/analysis/reliability_mask_checks.py` → **64/64**; `a1_writer_rate.py` → OK
- `07-evidence-and-decisions/falsifier_dnd112_checks.py --gate` → **CLEAN**; `falsifier_dnd114_checks.py --gate` → **CLEAN**
- `s6lc-low-cost/analysis/s6lc_checks.py` → **48/48**; `s6lc_bom_reratify_checks.py` → **68/68**
- `test14_low_cost_program/s5r_ultra_checks.py` → **19/19**; divergent/primitives/reliability gates → PASS
- `07/falsifier_dnd74_checks.py` → 31/31; `falsifier_dnd91_checks.py` → 37/37; `falsifier_dnd104_checks.py` → 26/26
- 06 `test08`–`test13` and test12 `s5r_*`/`falsifier` checks → PASS
- **All markdown relative links resolve (0 broken).**
- Re-grep: no `*.py`/`*.sh`/`*.yml`/`*.scad` operationally references `08-current-design`,
  `09-low-cost-variant` or `10-reliability-mask`; remaining occurrences are historical
  comments/docstrings and intentional relocation notes.

## Assumptions

- The chosen semantic names (`s5r-shared-drive-register`, `s6lc-low-cost`, `a1-reliability-first`)
  match the content's own architectural identities.
- The low-cost program's negative results / divergence / primitives are experimental provenance, so
  they belong in `06-experiments/` rather than stage 08.

## Remaining uncertainty / next

- S6-LC keeps an unresolved per-cell reliability gate (measurement-only under DND-27); A1's
  promotion remains a proposal for the next convergence gate. Neither is affected by this migration.
- Most informative next test: none specific to this migration; the restructure is verified.
