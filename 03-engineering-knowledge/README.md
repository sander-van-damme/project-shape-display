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
3. Prefer stable stage sections over one-off brainstorm documents.
4. Keep architecture sections explicitly connected to the mechanisms and principles they combine.
5. Treat historical tests as evidence, not blanket rejection of a family.
6. Feed durable test conclusions back into the relevant knowledge section.
7. Prefer falsifiable unknowns over vague "promising" language.
8. Keep the design target in view: ~5.08 mm pitch, ~6400 cells, >=40 mm travel, <30 s full-map update, regional updates, low bought-part cost and reliable tabletop load support.

The [research backlog](../05-research-questions/) tracks unresolved project hypotheses. Experiments live in [`06-experiments/`](../06-experiments/) and consolidated evidence in [`07-evidence-and-decisions/`](../07-evidence-and-decisions/).

## Mechanism × function matrix

Legend: ✓ primary, ◐ partial/supporting, — not provided.

| Mechanism | Selection | Power | State memory | Load support | Indexing | Regional-friendly |
|---|---:|---:|---:|---:|---:|---:|
| M-001 travelling head | ✓ | ✓ | — | — | ◐ | ✓ |
| M-002 Jacquard selector | ✓ | — | ◐ | — | ◐ | ◐ |
| M-003 bistable latch | ◐ | — | ✓ | ✓ | — | ✓ |
| M-004 ratchet/pawl | — | ◐ | ✓ | ✓ | ✓ | ◐ |
| M-005 compliant snap-through | ◐ | — | ✓ | ◐ | — | ✓ |
| M-006 Geneva indexer | — | ◐ | — | — | ✓ | ◐ |
| M-007 coded drum/pinwheel | ◐ | — | ✓ | — | ✓ | ◐ |
| M-008 shared shaft/clutch | ✓ | ✓ | — | — | — | ✓ |
| M-009 cable/tendon bus | ◐ | ✓ | — | — | — | ✓ |
| M-010 resonant selector | ✓ | — | — | — | ◐ | ✓ |
| M-011 sliding matrix | ✓ | — | — | — | ◐ | ✓ |
| M-012 rotary stepped stop | — | — | ✓ | ✓ | ✓ | ◐ |
| M-013 perforated height plate | — | — | ✓ | ✓ | — | ✓ when tiled |
| M-014 reprogrammable aperture | ✓ | — | ✓ | ◐ | — | ✓ |
| M-015 shared pressure source | — | ✓ | — | — | — | ◐ |

## Source map

## Repository source collections

- [Test08 source ledger](../06-experiments/test08_architecture_search/)
- [Test08 architecture comparison](../06-experiments/test08_architecture_search/)
- [Cross-disciplinary mechanical research](../05-research-questions/)
- [Externalized-memory research direction](../05-research-questions/)
- [Fabrication context](../02-design-criteria/)
- [Miniature dimensions](../02-design-criteria/)

## Named research leads already recorded

- Timothy E. Amish et al. (2025), *Electrostatic Clutches Enable High-Force
  Mechanical Multiplexing: Demonstrating Single-Motor Full-Actuation of a 4-DoF
  Hand*, arXiv:2501.08469.
- 2026 work on 3D-printed serial snap-through architectures referenced in the
  research backlog.
- Historical mechanism literature on Jacquard/dobby selection, Geneva motion,
  pinwheel calculators, coded drums and mechanical indexing.

## Research hygiene

Future sources should distinguish primary/technical source, secondary discovery
source, source fact, project extrapolation, and access date where pricing/specs
are time-sensitive.
