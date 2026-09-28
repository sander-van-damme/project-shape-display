+++
id = "A-002"
type = "architecture"
name = "Global lift with passive bistable cell memory"
status = "hypothesis"
mechanisms = ["M-002", "M-003", "M-005"]
principles = ["P-001", "P-002", "P-008"]
related_backlog = ["R02", "R03", "R05"]
related_tests = []
evidence = ["hypothesis"]
last_reviewed = "2026-09-27"
+++

# Global lift with passive bistable cell memory

## System concept
A global lift supplies most vertical energy. Local selectors toggle passive cell
latches at one or more height planes.

## Main unknowns
Reliable tiny latches, selector density, reset strategy and correlated failure at
6400 cells.

## Cheapest falsification path
3×3 full-pitch latch array plus shared selector motion and measured cycle/load
tests.
