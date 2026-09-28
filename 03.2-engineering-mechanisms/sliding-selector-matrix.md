+++
id = "M-011"
type = "mechanism"
name = "Sliding selector plate / matrix"
status = "hypothesis"
domains = ["D-001", "D-009"]
functions = ["selection", "addressing"]
related_principles = ["P-003"]
related_architectures = ["A-003", "A-006"]
related_backlog = ["R12"]
related_tests = []
evidence = ["hypothesis"]
last_reviewed = "2026-09-27"
+++

# Sliding selector plate / matrix

## Core principle
Thin sliding bars or plates create temporary mechanical paths or constraints.
Orthogonal row/column motion can form coincidence selection.

## What it solves well
Many intersections can be addressed from a small number of edge actuators.

## What it does not solve
State retention and power delivery are separate.

## Key risks
Accumulated friction, plate deflection, combinatorial transactions and clearance.

## Cheapest discriminating experiment
A 5×5 orthogonal selector matrix plus common lift, including checkerboard and
single-cell patterns.
