+++
id = "M-012"
type = "mechanism"
name = "Rotary stepped stop / cam memory"
status = "conditional"
domains = ["D-002", "D-007"]
functions = ["state-retention", "load-support", "height-encoding"]
related_principles = ["P-002", "P-007", "P-008"]
related_architectures = ["A-001"]
related_backlog = []
related_tests = ["test08_architecture_search", "test09_test08_validation"]
evidence = ["hypothesis"]
last_reviewed = "2026-09-27"
+++

# Rotary stepped stop / cam memory

## Core principle
A small rotor presents one of several discrete support heights to a follower.

## What it solves well
Compact passive multi-level memory and hard load support.

## Project evidence
Test08 found five levels geometrically plausible and a conditional 26.25 s
full-map schedule with an 80-channel programming head. Test09 reproduced timing
but exposed unresolved detent, coupling, sourcing and structural gates.

## What it does not solve
The rotor still needs fast reliable programming and return motion.

## Decision state
Worth mechanism-level study, but not product-qualified.
