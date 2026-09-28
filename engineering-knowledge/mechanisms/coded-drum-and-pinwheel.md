+++
id = "M-007"
type = "mechanism"
name = "Coded drum / pinwheel mechanical decoder"
status = "hypothesis"
domains = ["D-003", "D-004"]
functions = ["decoding", "sequencing", "memory"]
related_principles = ["P-007"]
related_architectures = []
related_backlog = ["R08", "R13"]
related_tests = []
evidence = ["hypothesis"]
last_reviewed = "2026-09-27"
+++

# Coded drum / pinwheel mechanical decoder

## Core principle
Rotating notches, pins or selectively active teeth mechanically encode or decode
state and sequence.

## What it solves well
Compact program representation and repeated sequencing.

## What it does not solve
Historic implementations are often read-only or slow to rewrite.

## Cheapest discriminating experiment
A small drum encoding selectable step counts and five dummy outputs; compare
code-setting overhead with direct programming.
