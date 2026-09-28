+++
id = "A-004"
type = "architecture"
name = "Double-buffered mechanical map cartridges"
status = "conditional"
mechanisms = ["M-013"]
principles = ["P-004", "P-005"]
related_backlog = ["R16"]
related_tests = []
evidence = ["hypothesis"]
last_reviewed = "2026-09-27"
+++

# Double-buffered mechanical map cartridges

## System concept
One cartridge drives visible terrain while another is programmed off-line, then
the media are swapped during a short visible transition.

## Strength
Can hide mechanical write time behind gameplay.

## Weakness
A single full-board cartridge conflicts with unexpected local reveals. The idea is
stronger when applied at tile level and combined with A-003.

## Decision state
Keep as a buffering principle, not the preferred monolithic architecture.
