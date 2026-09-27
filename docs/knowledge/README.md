# Mechanical knowledge base

This directory is the project's **conceptual engineering memory**. Tests remain
important, but they are the evidence layer rather than the primary storage model.

```text
discipline
  -> mechanism
  -> transferable principle
  -> architecture hypothesis
  -> critical uncertainty
  -> test / calculation / CAD / physical experiment
  -> evidence
  -> knowledge-base update
```

## Knowledge levels

- **Disciplines (`D-xxx`)** — fields with analogous engineering problems.
- **Mechanisms (`M-xxx`)** — concrete mechanisms such as latches, ratchets,
  selectors, clutches and patterned plates.
- **Principles (`P-xxx`)** — transferable ideas such as shared power with local
  selection or passive state retention.
- **Architectures (`A-xxx`)** — project-specific combinations of mechanisms and
  principles.

The [research backlog](../research-backlog.md) tracks unresolved project
hypotheses. It should link here rather than becoming a duplicate encyclopedia.

## Dynamic catalog

There is deliberately **no hand-maintained catalog file**.

```bash
python scripts/knowledge_catalog.py
python scripts/knowledge_catalog.py --format markdown
python scripts/knowledge_catalog.py --type mechanism
python scripts/knowledge_catalog.py --format json --write results/knowledge-catalog.json
```

The script scans the current repository tree and reads TOML frontmatter from
knowledge cards. Non-card support files are reported too unless
`--cards-only` is used.

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

A mechanism can be established elsewhere while its transfer to this shape display
remains only a hypothesis.

## Rules for AI-assisted research

1. Preserve source facts versus project extrapolation.
2. Record what a mechanism **does not solve**.
3. Prefer stable cards over one-off brainstorm documents.
4. Link architectures to the mechanisms and principles they combine.
5. Treat historical tests as evidence, not blanket rejection of a family.
6. Feed durable test conclusions back into the relevant card.
7. Prefer falsifiable unknowns over vague "promising" language.
8. Keep the design target in view: ~5.08 mm pitch, ~6400 cells, >=40 mm travel,
   <30 s full-map update, regional updates, low bought-part cost and reliable
   tabletop load support.

Metadata uses TOML frontmatter delimited by `+++`, readable with Python 3.11
`tomllib` without another dependency.
