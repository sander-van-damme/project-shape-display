+++
id = "M-008"
type = "mechanism"
name = "Shared shaft with selectable clutches"
status = "hypothesis"
domains = ["D-006"]
functions = ["power-delivery", "selection"]
related_principles = ["P-001", "P-008"]
related_architectures = ["A-006"]
related_backlog = ["R09"]
related_tests = []
evidence = ["hypothesis"]
last_reviewed = "2026-09-27"
+++

# Shared shaft with selectable clutches

## Core principle
A common power bus is selectively coupled to outputs through clutches.

## What it solves well
Reduces motor count and can power several outputs simultaneously.

## What it does not solve
The clutch/selector itself must be cheap and dense enough not to recreate the
cost problem.

## Cheapest discriminating experiment
One motor and four independently selected loaded outputs; measure engagement,
slip, torque and wear.
