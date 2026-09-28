+++
id = "M-006"
type = "mechanism"
name = "Geneva / intermittent-motion indexer"
status = "hypothesis"
domains = ["D-002", "D-003"]
functions = ["indexing", "sequencing"]
related_principles = ["P-007"]
related_architectures = []
related_backlog = ["R07"]
related_tests = []
evidence = ["hypothesis"]
last_reviewed = "2026-09-27"
+++

# Geneva / intermittent-motion indexer

## Core principle
Input motion is converted into discrete indexed steps with dwell periods.

## What it solves well
Deterministic sequencing and geometric indexing.

## What it does not solve
Used one event per cell it remains too serial; it needs a group-level role.

## Cheapest discriminating experiment
A shared indexer driving 5–20 selector states at realistic speed and load.
