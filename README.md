<!-- © 2024 Sander Van Damme - All Rights Reserved. -->

# D&D battle-map shape display

This repository develops a tabletop shape display for physical Dungeons & Dragons battle maps: a dense grid of square or rectangular columns that can form terrain, walls, platforms, stairs, pits and other relief while remaining usable with miniatures.

## Engineering flow

The numbered root directories are intentionally ordered. Read them as the project argument from problem definition to current design:

1. [`01-project-description/`](01-project-description/) — what is being built and why.
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
8. [`08-current-design/`](08-current-design/) — the current integrated design state, including an explicit statement when no architecture is yet qualified.


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
  -> current design
  -> new questions / updated knowledge
```

Experiments are evidence, not the primary place to store durable engineering knowledge. Conclusions that survive testing should be fed back into the relevant mechanism, principle or architecture section.

## Useful entry points

- [Design criteria](02-design-criteria/README.md)
- [Engineering knowledge model](03-engineering-knowledge/README.md)
- [Architecture candidates](04-architecture-candidates/)
- [Research questions](05-research-questions/)
- [Experiment guide](06-experiments/README.md)
- [Evidence and decisions](07-evidence-and-decisions/)
- [Current design state](08-current-design/)

## Copyright

© 2024-2026 Sander Van Damme - All Rights Reserved.
