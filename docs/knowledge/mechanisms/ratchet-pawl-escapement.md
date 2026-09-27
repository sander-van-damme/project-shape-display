+++
id = "M-004"
type = "mechanism"
name = "Ratchet / pawl / escapement height memory"
status = "hypothesis"
domains = ["D-002"]
functions = ["state-retention", "indexing", "load-support"]
related_principles = ["P-002", "P-007"]
related_architectures = ["A-002"]
related_backlog = ["R04"]
related_tests = []
evidence = ["hypothesis"]
last_reviewed = "2026-09-27"
+++

# Ratchet / pawl / escapement height memory

## Core principle
An indexed member moves incrementally while a pawl prevents reverse motion until
release.

## What it solves well
Discrete position memory, indexing and load support.

## What it does not solve
Selective addressing and fast scalable reset remain separate problems.

## Cheapest discriminating experiment
One cell followed by a 1×5 shared-drive row; measure missed/double steps, holding
force, release force and wear.
