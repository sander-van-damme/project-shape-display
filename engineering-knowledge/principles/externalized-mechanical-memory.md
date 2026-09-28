+++
id = "P-004"
type = "principle"
name = "Externalized mechanical memory"
status = "active"
related_mechanisms = ["M-013", "M-014"]
related_architectures = ["A-003", "A-004"]
last_reviewed = "2026-09-27"
+++

# Externalized mechanical memory

## Statement
Store terrain state in replaceable or rewriteable mechanical media rather than
inside the load-bearing cell.

## Why it matters
The display can read many states in parallel while a separate writer handles
programming.

## Caveat
Writer throughput and regional-update behavior become product constraints.
