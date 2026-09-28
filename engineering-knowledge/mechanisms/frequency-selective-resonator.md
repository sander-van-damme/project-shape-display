+++
id = "M-010"
type = "mechanism"
name = "Frequency-selective mechanical resonator"
status = "exploratory"
domains = ["D-006"]
functions = ["selection", "addressing"]
related_principles = ["P-001"]
related_architectures = []
related_backlog = ["R11"]
related_tests = []
evidence = ["hypothesis"]
last_reviewed = "2026-09-27"
+++

# Frequency-selective mechanical resonator

## Core principle
Elements with intentionally different resonances receive a common oscillatory
input while only the tuned class crosses a trigger threshold.

## What it solves well
Potential broadcast addressing with little spatial routing.

## What it does not solve
It supplies only a selection event; long-stroke motion and stable load support
must come from elsewhere.

## Key risks
Tolerance drift, modal coupling, load sensitivity and settling time.

## Cheapest discriminating experiment
5–10 printed resonators with separated targets, tested before and after added
load and print-to-print variation.
