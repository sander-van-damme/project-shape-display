# 03 — Engineering knowledge

This stage is the project's **conceptual engineering memory**. It contains reusable knowledge that can support multiple Shape Display architectures.

The knowledge layer is split into three ordered sub-stages:

- [`03.1-engineering-disciplines/`](../03.1-engineering-disciplines/) — fields with analogous engineering problems.
- [`03.2-engineering-mechanisms/`](../03.2-engineering-mechanisms/) — concrete mechanisms such as latches, ratchets, selectors, clutches and patterned plates.
- [`03.3-engineering-principles/`](../03.3-engineering-principles/) — transferable ideas such as shared power with local selection or passive state retention.

Project-specific combinations of this knowledge belong one step later in [`04-architecture-candidates/`](../04-architecture-candidates/).

```text
discipline
  -> mechanism
  -> transferable principle
  -> architecture hypothesis
  -> critical uncertainty
  -> experiment / calculation / CAD / physical test
  -> evidence
  -> knowledge-base update
```

## Dynamic catalog

There is deliberately no hand-maintained catalog file.

```bash
python 90-tools/knowledge_catalog.py
python 90-tools/knowledge_catalog.py --format markdown
python 90-tools/knowledge_catalog.py --type mechanism
python 90-tools/knowledge_catalog.py --format json --write results/knowledge-catalog.json
```

The catalog scans the three engineering-knowledge stages plus architecture candidates and reads TOML frontmatter from knowledge cards.

## Evidence vocabulary

| Label | Meaning |
|---|---|
| `sourced` | External technical source / established mechanism description |
| `calculated` | Explicit engineering calculation |
| `simulated` | Analytical/event/physics simulation |
| `cad_checked` | Geometry/interference checked in CAD/CSG |
| `printed` | Physical part fabricated |
| `measured` | Physical measurement recorded |
| `lifetime_tested` | Repeated-cycle / durability evidence |
| `rejected` | Specific hypothesis falsified against stated gates |
| `hypothesis` | Plausible but not yet established for this project |

A mechanism can be established elsewhere while its transfer to this Shape Display remains only a hypothesis.

## Rules for AI-assisted research

1. Preserve source facts versus project extrapolation.
2. Record what a mechanism **does not solve**.
3. Prefer stable cards over one-off brainstorm documents.
4. Link architectures to the mechanisms and principles they combine.
5. Treat historical tests as evidence, not blanket rejection of a family.
6. Feed durable test conclusions back into the relevant card.
7. Prefer falsifiable unknowns over vague "promising" language.
8. Keep the design target in view: ~5.08 mm pitch, ~6400 cells, >=40 mm travel, <30 s full-map update, regional updates, low bought-part cost and reliable tabletop load support.

The [research backlog](../05-research-questions/research-backlog.md) tracks unresolved project hypotheses. Experiments live in [`06-experiments/`](../06-experiments/) and consolidated evidence in [`07-evidence-and-decisions/`](../07-evidence-and-decisions/).
