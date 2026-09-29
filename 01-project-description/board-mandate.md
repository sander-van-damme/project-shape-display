<!-- © 2024 Sander Van Damme - All Rights Reserved. -->

# Standing Board mandate — Shape Display laboratory

> Provenance: faithful copy of the Board mandate delivered via
> [SHA-6](/SHA/issues/SHA-6), sourced from the standing mandate in
> [SHA-5](/SHA/issues/SHA-5#document-board-mandate).
> Stored 2026-09-29 by the CEO as the authoritative operational reference.
> The copy below is verbatim from the issue brief; operational notes live
> outside this quoted block.

---
# Board mandate: launch and continuously improve the Shape Display organization

The organization is now ready to begin substantive work.

Your task is to establish the strategic mandate below and hand operational execution to the CEO.

The CEO is the only agent authorized to hire additional agents. Do not hire the operational team yourself. Instead, instruct the CEO to design the organizational structure, create the required agents, assign responsibilities, and continuously reorganize or replace roles when that improves results.

The existing repository is the source of truth for the current project state, requirements, prior research, experiments, designs, and engineering knowledge:

`/home/odroid/project-shape-display`

Repository:

`git@github.com:sander-van-damme/project-shape-display.git`

Preserve existing work and build on it. Existing designs are starting points, not commitments.

# Mission

The organization's mission is to design the best practical Shape Display for tabletop Dungeons & Dragons terrain.

The system should physically reproduce terrain or map geometry through a shape-changing surface while satisfying the requirements documented in the repository.

The organization should relentlessly search for better ways to achieve this.

There is no assumption that the current design is the final design.

Existing mechanisms may be improved, combined, simplified, or abandoned entirely when evidence supports a better approach.

# Primary optimization objective

Optimize simultaneously for:

1. **Minimum total cost**
2. **Maximum practical quality**

Neither objective should be treated in isolation.

The goal is not merely to build the cheapest possible system, nor the most sophisticated system regardless of cost.

The goal is to find architectures that deliver the greatest useful performance, reliability, durability, manufacturability, and feature coverage for the lowest realistic total cost.

# Cost

Drive total system cost as low as reasonably possible.

Count all meaningful physical costs, including:

* purchased components;
* actuators;
* motors;
* electronics;
* sensors;
* bearings, fasteners, springs, magnets, cables, and other external hardware;
* fabrication materials;
* 3D printing material and printing burden;
* the number and complexity of manufactured parts;
* assembly effort where it materially affects practicality.

Prefer eliminating components over merely finding cheaper versions of them.

Whenever possible, replace large numbers of expensive active components with inexpensive passive geometry, shared actuation, clever mechanics, printed structures, or other lower-cost approaches.

3D-printed material is not free and must be treated as part of the cost.

A design with fewer purchased components but excessive printed volume, print time, difficult supports, high failure rates, or many complicated parts is not automatically cheaper.

Evaluate the complete physical system.

# Quality

Maximize practical engineering quality.

Important quality dimensions include:

## Reliability

The display should work consistently.

Mechanisms should tolerate repeated activation without frequent jams, missed states, synchronization problems, drift, or manual correction.

Prefer architectures that fail predictably and can recover gracefully.

## Durability

The mechanism should survive repeated real-world use.

Avoid designs that depend on fragile features, excessive friction, rapid wear, marginal tolerances, or components likely to degrade quickly.

## Manufacturability

The system should be easy and reliable to manufacture, especially with common 3D-printing processes.

Prefer:

* fewer unique parts;
* fewer total parts;
* simple geometries;
* reasonable tolerances;
* minimal support material;
* easy print orientation;
* low risk of failed prints;
* straightforward assembly;
* designs that tolerate normal printer variation.

Avoid unnecessary mechanical complexity.

## Performance

The Shape Display must respond quickly enough to be practical during tabletop play.

Optimize the time required to construct or modify terrain.

Support efficient local updates so that changing a small region does not unnecessarily require rebuilding the entire surface.

Seek architectures that allow fast, selective, and scalable state changes.

## Requirement coverage

Maximize fulfillment of the requirements documented in the repository.

Do not optimize one attractive metric while ignoring important system requirements.

When requirements conflict, quantify the tradeoff and search for architectures that reduce or eliminate the conflict.

## Compactness

Keep the system reasonably compact in operation and storage.

Avoid architectures whose supporting machinery becomes disproportionately large relative to the useful display area.

Consider the complete system volume, not only the visible surface.

## Maintainability

Prefer mechanisms that can be understood, serviced, repaired, and iterated without replacing the entire system.

Modularity is useful where it improves reliability or serviceability, but should not be added when it increases complexity or cost without meaningful benefit.

# Continuous improvement mandate

This is not a project that ends when the first acceptable design is found.

The organization has a standing mandate to continuously ask:

* Can this be made cheaper?
* Can components be eliminated?
* Can the same function be achieved with simpler geometry?
* Can one actuator replace many?
* Can a passive mechanism replace an active mechanism?
* Can reliability be improved?
* Can wear be reduced?
* Can it be printed more easily?
* Can assembly be simplified?
* Can activation become faster?
* Can local updates become more efficient?
* Can the mechanism become more compact?
* Can more requirements be satisfied simultaneously?
* Is there an entirely different architecture that makes the current design obsolete?

An apparently successful design should become a baseline for further improvement, not a reason to stop searching.

There is no protected architecture.

Any design may be challenged.

# Evidence-driven engineering

Do not select concepts primarily because they sound elegant.

Require evidence.

Use the cheapest useful method to reduce uncertainty:

* analytical reasoning;
* calculations;
* CAD;
* simple simulations;
* tolerance analysis;
* mechanism sketches;
* small printed tests;
* isolated mechanism prototypes;
* durability tests;
* repeated-cycle tests;
* cost estimates;
* timing measurements;
* comparative experiments.

Prefer small experiments that answer one important uncertainty quickly.

Record failures as engineering knowledge rather than hiding or repeatedly rediscovering them.

A failed mechanism can be valuable if it establishes why an approach does not work and under what conditions.

# Organizational strategy

The CEO should design the organization around the work rather than around a fixed org chart.

The CEO may hire specialized agents when there is a real capability or capacity need.

Useful areas may include, where justified:

* mechanical architecture;
* mechanism exploration;
* cost reduction;
* reliability engineering;
* additive manufacturing and printability;
* actuation systems;
* electronics;
* simulation;
* CAD and parametric design;
* prototyping and experimental design;
* requirement analysis;
* competitive or prior-art research;
* integration and system architecture;
* independent design review.

These are examples, not mandatory departments.

The CEO should choose the structure that best advances the mission.

Parallel independent exploration is encouraged when the design space is uncertain.

It can be valuable to have different agents pursue genuinely different mechanisms rather than prematurely converging on one architecture.

At the same time, avoid creating agents whose responsibilities substantially overlap without a reason.

The CEO should periodically reconsider whether the current organizational structure is still useful.

# Agent runtime

New operational agents should use the established free-model OpenCode runtime unless there is a specific approved reason to do otherwise.

Default configuration:

Adapter:
`opencode_local`

Command:
Leave empty

Primary model:
`relay/auto`

Working directory:
`/home/odroid/project-shape-display`

Environment:
`OPENCODE_ALLOW_ALL_MODELS=true`

The failover wrapper must be used rather than raw `opencode`.

Do not switch to paid models merely for convenience.

All newly hired agents must have:

`canCreateAgents=false`

Only the CEO may hire agents.

# Repository autonomy

The CEO and operational agents are authorized to work directly in the repository.

They may:

* research;
* create and modify files;
* reorganize engineering knowledge;
* create branches;
* commit;
* open pull requests;
* review pull requests;
* merge pull requests;
* replace obsolete designs;
* add experiments and test results;
* revise project documentation.

Normal repository work does not require Board approval.

The repository should become the durable engineering memory of the organization.

Important conclusions, experiments, rejected mechanisms, measurements, design rationale, and current best-known designs should be recorded there so future agents can build on previous work.

# Avoid premature convergence

Do not assume that incremental improvement of the current mechanism is necessarily the best route.

Maintain two complementary modes of work:

**Exploitation:** improve the strongest currently known architecture.

**Exploration:** continue investigating fundamentally different mechanisms that could produce a major improvement.

The balance may change over time, but exploration should never disappear entirely while major cost, reliability, speed, or manufacturability improvements remain plausible.

# Design evaluation

Compare serious candidate architectures against explicit engineering criteria.

At minimum consider:

* estimated total cost;
* purchased component count;
* printed material and complexity;
* number of unique parts;
* assembly complexity;
* reliability;
* durability;
* expected wear;
* actuation speed;
* local update capability;
* full-display update capability;
* energy requirements where relevant;
* compactness;
* manufacturability;
* repairability;
* scalability;
* requirement coverage;
* major unresolved risks.

Avoid false precision. Use ranges or confidence levels when exact numbers are not yet known.

A promising concept with an unresolved critical failure mode is not yet a superior design.

# Long-term operating principle

The organization should behave like a permanent engineering laboratory rather than a one-shot design project.

Each generation should produce:

1. a better physical design or a clearer understanding of the design space;
2. evidence about what works and what does not;
3. reusable engineering knowledge;
4. new questions worth investigating.

When a design reaches a strong level of maturity, continue looking for step-change improvements while preserving the mature design as a reliable baseline.

Never destroy a proven baseline merely because a new concept looks promising.

Validate replacements before displacing established work.

# Immediate action

Deliver this mandate to the CEO and instruct the CEO to begin.

The CEO should:

1. inspect the repository and understand the current project state;
2. understand the existing requirements, prior designs, experiments, and engineering knowledge;
3. identify the most important current uncertainties and bottlenecks;
4. design an initial organizational structure around those needs;
5. hire the agents required to start useful parallel work;
6. assign concrete tasks with clear objectives and evidence requirements;
7. begin both improvement of the strongest existing architecture and exploration of alternative architectures;
8. maintain durable engineering knowledge in the repository;
9. continuously create follow-up work from useful results rather than treating the first successful design as completion.

Do not require the CEO to return to the Board for ordinary decisions.

The Board should intervene only for matters that genuinely fall under the established Board escalation rules.

Once this mandate has been handed to the CEO and operational work has begun, return to the normal Board Delegate role.
