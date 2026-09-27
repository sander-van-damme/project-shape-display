+++
id = "M-003"
type = "mechanism"
name = "Bistable mechanical latch"
status = "hypothesis"
domains = ["D-005", "D-008"]
functions = ["state-retention", "load-support", "selection"]
related_principles = ["P-002"]
related_architectures = ["A-002", "A-006"]
related_backlog = ["R03"]
related_tests = []
evidence = ["hypothesis"]
last_reviewed = "2026-09-27"
+++

# Bistable mechanical latch

## Core principle
A mechanism has two stable states and changes only after crossing a mechanical
threshold.

## What it solves well
Passive state retention and potentially passive load support.

## What it does not solve
Addressing and programming energy remain external.

## Key risks
Toggle-force variation, creep, accidental release and manufacturing consistency
at 5.08 mm pitch.

## Cheapest discriminating experiment
Single-cell and 3×3 coupons measuring toggle force, holding load, repeatability
and cycle wear.
