<!-- © 2024 Sander Van Damme - All Rights Reserved. -->

# D&D battle-map shape display

This repository develops a tabletop shape display for physical Dungeons & Dragons battle maps: a dense grid of square or rectangular columns that can form terrain, walls, platforms, stairs, pits and other relief while remaining usable with miniatures.

## Engineering flow

The numbered root directories are intentionally ordered. Read them as the project argument from problem definition to integrated designs:

1. [`01-project-description/`](01-project-description/) — what is being built and why, including the [standing Board mandate](01-project-description/board-mandate.md).
2. [`02-design-criteria/`](02-design-criteria/) — requirements, scale, fabrication context and success criteria.
3. Engineering knowledge used to construct solutions:
   - [`03-engineering-knowledge/`](03-engineering-knowledge/) — knowledge model, sources and cross-cutting synthesis.
   - [`03.1-engineering-disciplines/`](03.1-engineering-disciplines/) — analogous engineering fields.
   - [`03.2-engineering-mechanisms/`](03.2-engineering-mechanisms/) — concrete reusable mechanisms.
   - [`03.3-engineering-principles/`](03.3-engineering-principles/) — transferable design principles.
4. [`04-architecture-candidates/`](04-architecture-candidates/) — Shape Display-specific combinations of mechanisms and principles.
5. [`05-research-questions/`](05-research-questions/) — unresolved hypotheses, investigations and research directions.
6. [`06-experiments/`](06-experiments/) — calculations, simulations, CAD, prototypes and physical tests that generate evidence.
7. [`07-evidence-and-decisions/`](07-evidence-and-decisions/) — consolidated evidence, architecture investigations and durable decisions.
8. [`08-integrated-designs/`](08-integrated-designs/README.md) — the **single stage for complete machine architectures**. Stage 08 may hold **multiple** integrated-design packages, each with its own status (see the [stage index](08-integrated-designs/README.md)); a design becoming integrated does **not** delete or overwrite previous integrated designs.

The numbered flow **terminates at 08**. A new machine architecture does **not** receive a new
numbered root directory — see [New designs do not get new numbered stages](#new-designs-do-not-get-new-numbered-stages) below.


## Core target

The detailed requirements live in [`02-design-criteria/README.md`](02-design-criteria/README.md). The current target includes approximately 400 × 400 mm active area, about 5.08 mm or finer pitch, roughly 6,200–6,400 cells at full scale, at least 40 mm provisional vertical travel, regional updates, a playable full-map change in under 30 seconds, and tight purchased-component cost limits.

## How knowledge should move

```text
project description
  -> design criteria
  -> disciplines
  -> mechanisms
  -> principles
  -> architecture candidates
  -> research questions
  -> experiments
  -> evidence and decisions
  -> integrated designs (08, may hold several)
  -> new questions / updated knowledge
```

Experiments are evidence, not the primary place to store durable engineering knowledge. Conclusions that survive testing should be fed back into the relevant mechanism, principle or architecture section.

## New designs do not get new numbered stages

The root numbers describe the **engineering lifecycle**, not architecture versions. Do not
create `09-*`, `10-*`, `11-*`, … for a new machine.

- A new **idea / mechanism / system concept** belongs in [`04-architecture-candidates/`](04-architecture-candidates/).
- Evidence-generating work (calculations, simulations, CAD, screens, falsification tests)
  belongs in [`06-experiments/`](06-experiments/).
- Durable conclusions, comparisons and selection/rejection decisions belong in
  [`07-evidence-and-decisions/`](07-evidence-and-decisions/).
- Only an architecture that has matured into a **complete machine** is placed under
  [`08-integrated-designs/<semantic-design-name>/`](08-integrated-designs/README.md).
  Use meaning-bearing names, never `design-1/`, `design-2/`, or a new number.

Promotion into stage 08 requires at minimum a coherent full-system mechanism, interaction with
all important product requirements, timing/cost/scalability/reliability analysis, explicit
unresolved risks, enough CAD/calculation evidence to evaluate the architecture, and an
evidence/decision record explaining the promotion. Stage 08 must not be flooded with raw
exploration.

## Agent autonomy and repository operations

This repository is an autonomous engineering workspace. Paperclip agents are trusted to manage
ordinary repository work without waiting for board approval or rejection.

- Agents may create, modify, move, or delete repository files; create branches and commits; open,
  update, review, close, and **merge pull requests themselves**.
- **No board approval is required for merges, ordinary refactors, experiments, design decisions, or
  promotion of an architecture when the documented engineering evidence supports it.**
- Branches, PRs, reviews, and checks are useful for traceability and engineering quality; they are
  **not permission gates**.
- Do not block ongoing work waiting for a board response. Escalation is reserved for genuinely
  exceptional actions outside normal project iteration (for example, destroying/replacing the
  repository as a whole).
- Never commit credentials, tokens, private keys, or other secrets.

## Useful entry points

- [Design criteria](02-design-criteria/README.md)
- [Engineering knowledge model](03-engineering-knowledge/README.md)
- [Architecture candidates](04-architecture-candidates/)
- [Research questions](05-research-questions/)
- [Experiment guide](06-experiments/README.md)
- [Evidence and decisions](07-evidence-and-decisions/)
- [Integrated designs (stage 08)](08-integrated-designs/README.md)

## Copyright

© 2024-2026 Sander Van Damme - All Rights Reserved.
