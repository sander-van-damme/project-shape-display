+++
id = "M-005"
type = "mechanism"
name = "Compliant snap-through multistable cell"
status = "hypothesis"
domains = ["D-005", "D-008"]
functions = ["state-retention", "selection"]
related_principles = ["P-002"]
related_architectures = ["A-002"]
related_backlog = ["R05"]
related_tests = []
evidence = ["hypothesis"]
last_reviewed = "2026-09-27"
+++

# Compliant snap-through multistable cell

## Core principle
Elastic geometry snaps between stable configurations without conventional
bearings or assembled springs.

## What it solves well
Potentially eliminates purchased cell-level memory parts.

## What it does not solve
Shared addressing and long-stroke energy delivery remain external.

## Key risks
PLA creep/fatigue, temperature, print variation and snap-force spread.

## Cheapest discriminating experiment
A replicated parameter sweep measuring snap force, stable displacement, creep and
cycle life.
