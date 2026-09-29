# 08 — Integrated designs

Stage 08 is the **single container for complete machine architectures**. The numbered root
directories (`01`–`08`) describe the **engineering lifecycle**; stage 08 may hold **multiple**
integrated designs that coexist, each with its own status. Adding a design here does **not**
delete or overwrite previous designs.

This replaced the earlier single-winner stage `08-current-design/` and the top-level
`09-low-cost-variant/` / `10-reliability-mask/` stages, retired by
[DND-117](/DND/issues/DND-117) (parent [DND-116](/DND/issues/DND-116)).

## What qualifies for stage 08

An **integrated design** is an architecture developed far enough to be described and evaluated as
a whole machine — not a bare idea and not a physically validated product. Promotion requires at
minimum: a coherent full-system mechanism; interaction with all important product requirements;
timing, cost, scalability and reliability analysis; explicit unresolved risks; enough
CAD/calculation evidence to evaluate the architecture; and an evidence/decision record explaining
why it is treated as an integrated candidate.

**`integrated-designs` does NOT imply physical validation or final-product readiness.** Under the
program's permanent no-print policy ([DND-27](/DND/issues/DND-27)) no physical measurement evidence
exists; every design here is CAD / CALCULATION / SIMULATION over sourced listings and stated
assumptions.

## Index

Status and evidence class are read from the repository, not guessed. Vocabulary:
`CANDIDATE`, `PROMOTED`, `SUPERSEDED`, `REJECTED`, `MEASUREMENT-GATED`, `ARCHIVED`.

| Design | Directory | Primary idea | Status | Evidence class |
|---|---|---|---|---|
| S5-R | [`s5r-shared-drive-register/`](s5r-shared-drive-register/README.md) | shared-drive programmable rotary register: 2 bank motors + 40 writer solenoids write a 4-row-deep passive rotor bank; hard-stop height memory | **PROMOTED** (historical single-winner; remains the slicer-ready build package of record) | CAD + CALCULATION over sourced listings; measurement-only residue |
| S6-LC | [`s6lc-low-cost/`](s6lc-low-cost/README.md) | low-cost broadcast / mask-gate machine: off-line punched-card per-bank mask selects cells; one lead-screw stepper; passive printed pawls hold height | **MEASUREMENT-GATED** (mission gates pass; per-cell reliability `G8` unresolved) | CAD + CALCULATION over sourced FDM/actuator data |
| A1 | [`a1-reliability-first/`](a1-reliability-first/README.md) | binary-latch + shared writer/reader: 2-axis gantry writes a per-cell over-centre latch, a reader verifies and re-drives (zero silent-error cells) | **PROMOTED (architecture) / MEASUREMENT-GATED (build)** — gated promotion per the SHA-7 GATE decision ([decision](../07-evidence-and-decisions/sha7-a1-promotion-decision.md)); full-machine build waits on coupon A (single cell: toggle force + read contrast) | CAD + CALCULATION over sourced component classes; R5 retired, R6 half-retired ([SHA-9](../07-evidence-and-decisions/sha9-a1-gate-residuals-regional.md)) |

Notes on the statuses:

- **S5-R** was promoted as the single buildable winner under the old `08-current-design/` stage and
  is preserved here as historically `PROMOTED`. It is the package of record (complete printable
  S5-R part set + manifests + coherence gates).
- **S6-LC** is mission-gate-passing but carries an **unresolved per-cell reliability gate**; its
  status is `MEASUREMENT-GATED` (measurement being unavailable under DND-27, the gate is carried as
  an explicit residual).
- **A1** is the **gated-promoted reliability-first architecture**: the
  architecture itself is **PROMOTED** per the SHA-7 GATE decision (timing
  19.63 s sustained, BOM $181 IDEAL, write-path audit 22/22 CLEAN), while
  the **build is MEASUREMENT-GATED on coupon A** (single cell at true
  pitch: toggle force + read contrast), which DND-27 forbids settling
  analytically. R1–R4 stay open as measurement-only; R5 is retired as an
  8-head-minimum design rule and R6 is half-retired (geometry analytic,
  elastic open as coupon B) per the
  [SHA-9 note](../07-evidence-and-decisions/sha9-a1-gate-residuals-regional.md).
  It is the only architecture in the reliability-first program with a
  structurally zero silent-error set (shared reader verifies every cell).
- The six other screened reliability-first architectures (A2–A7) are **architecture-candidates /
  experiment screen material**, not promoted integrated designs; they are preserved in the A1
  package's screen table and the low-cost program experiments.

## Where new work belongs

```
engineering knowledge
      ↓
04-architecture-candidates   ← new mechanism/system concepts (many may accumulate)
      ↓
05-research-questions
      ↓
06-experiments               ← calculations, simulations, CAD, screens, falsification
      ↓
07-evidence-and-decisions    ← durable conclusions, comparisons, ADRs, promote/reject
      ↓
08-integrated-designs/<semantic-name>/   ← only mature complete machines
```

- Most exploration should remain in `04-architecture-candidates/` and `06-experiments/`; stage 08
  must not be flooded with raw concepts.
- Supporting provenance for a design may either live alongside the design (when tightly coupled) or
  be placed in the appropriate earlier stage. Do not duplicate files to make the tree look clean.

## Rule for future agents

> **New machine architectures do not receive new numbered root directories.**
>
> Never create `09-new-design/`, `10-next-design/`, `11-even-newer-design/`, or any other new
> numbered root stage for an alternative architecture. New ideas begin in the research / candidate /
> experiment stages; a mature machine-level design belongs under
> `08-integrated-designs/<semantic-design-name>/`. The root numbers represent the engineering
> lifecycle, not architecture version numbers.

Historical note: the prior layout had `08-current-design/` (S5-R), `09-low-cost-variant/` (S6-LC
and its low-cost program) and `10-reliability-mask/` (the reliability-first program). The
sibling-turned-stage pattern is exactly what this stage prevents. See
[DND-117](/DND/issues/DND-117) and [DND-116](/DND/issues/DND-116).
