<!-- © 2024 Sander Van Damme - All Rights Reserved. -->

# Contributing to the shape-display repository

## Repository layout is the engineering lifecycle

The numbered root directories (`01`–`08`) describe the **engineering process**, not design
versions. Read them in order:

```
01-project-description
02-design-criteria
03-engineering-knowledge  (+ 03.1 disciplines, 03.2 mechanisms, 03.3 principles)
04-architecture-candidates
05-research-questions
06-experiments
07-evidence-and-decisions
08-integrated-designs
```

## Rule: new machine architectures do not get new numbered root directories

> Do **not** create `09-new-design/`, `10-next-design/`, `11-even-newer-design/`, or any other new
> numbered root stage for an alternative machine architecture.

Where new work goes instead:

- **New ideas / mechanism / system concepts** → [`04-architecture-candidates/`](04-architecture-candidates/).
- **Evidence-generating work** (calculations, simulations, CAD, screens, falsification) →
  [`06-experiments/`](06-experiments/).
- **Durable conclusions, comparisons, ADRs, promote/reject decisions** →
  [`07-evidence-and-decisions/`](07-evidence-and-decisions/).
- **A mature complete machine** → [`08-integrated-designs/`](08-integrated-designs/README.md)
  under a **meaning-bearing** name (never `design-1/`, `design-2/`, or a number).

Stage 08 may hold **multiple** integrated designs that coexist, each with its own status
(`CANDIDATE`, `PROMOTED`, `SUPERSEDED`, `REJECTED`, `MEASUREMENT-GATED`, `ARCHIVED`). Adding a
design does not delete or overwrite previous designs. Promotion into stage 08 requires a coherent
full-system mechanism, all important product requirements addressed, timing/cost/scalability/
reliability analysis, explicit unresolved risks, enough CAD/calculation evidence to evaluate the
architecture, and an evidence/decision record. Stage 08 must not be flooded with raw exploration.

## Evidence discipline

Clearly distinguish **sourced fact**, **assumption**, **calculation**, **simulation**, **CAD**, and
**printed/measured evidence**. Never present analytical work as physical validation.

## Program policy: no physical print tests

Per [DND-27](/DND/issues/DND-27), the program performs **no physical print tests** and no physical
measurement. Retire risks with sourced process limits, analytic calculations, tolerance/interference
stack-ups, kinematic/force analysis, and CAD/mesh validation, and state the residual uncertainty
explicitly.

## Git workflow

- Work on clearly named feature branches from the latest `main`; do not push directly to `main`.
- Open a PR per coherent engineering result, with checks/evidence recorded in the PR body.
- Use the SSH remote (`git@github.com:sander-van-damme/project-shape-display.git`); never commit
  or embed credentials.
