+++
id = "M-014"
type = "mechanism"
name = "Reprogrammable planar aperture layer"
status = "hypothesis"
domains = ["D-001", "D-005", "D-009"]
functions = ["state-retention", "selection", "height-encoding"]
related_principles = ["P-004", "P-006"]
related_architectures = ["A-003"]
related_backlog = ["R15", "R17"]
related_tests = []
evidence = ["hypothesis"]
last_reviewed = "2026-09-27"
+++

# Reprogrammable planar aperture layer

## Core principle
Reusable shutters, tabs, sliding strips, rotating apertures or compliant features
replace destructive punched holes in a planar memory layer.

## What it solves well
Retains parallel planar readout while allowing repeated programming.

## What it does not solve
If every aperture needs its own bought actuator, the architecture recreates the
original 6400-channel problem.

## Cheapest discriminating experiment
One 5×5 reusable aperture plane, written through shared hardware, with adversarial
patterns and cycle testing.
