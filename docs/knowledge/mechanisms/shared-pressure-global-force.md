+++
id = "M-015"
type = "mechanism"
name = "Shared pressure / global force source"
status = "conditional"
domains = ["D-007"]
functions = ["power-delivery"]
related_principles = ["P-001", "P-008"]
related_architectures = []
related_backlog = ["R06"]
related_tests = ["test00_pneumatic_multiplexer"]
evidence = ["hypothesis"]
last_reviewed = "2026-09-27"
+++

# Shared pressure / global force source

## Core principle
One or a few global pressure chambers or membranes provide bulk force while local
mechanical selectors determine which elements respond.

## What it solves well
Potentially distributes force with very few bought actuators.

## What it does not solve
Selection and state retention remain separate.

## Project warning
Conventional per-cell pneumatic valves/plumbing are poor fits because of leakage,
sealing and component count. Keep only architectures that avoid those scaling
modes.
