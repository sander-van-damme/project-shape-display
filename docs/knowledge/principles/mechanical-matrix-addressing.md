+++
id = "P-003"
type = "principle"
name = "Mechanical matrix addressing"
status = "active"
related_mechanisms = ["M-002", "M-011"]
related_architectures = ["A-003", "A-006"]
last_reviewed = "2026-09-27"
+++

# Mechanical matrix addressing

## Statement
Use row/column or other coincidence selection so a small number of control
members can address many intersections.

## Scaling consequence
An 80×80 grid suggests O(160) addressing members rather than O(6400), but only if
the intersections remain simple and arbitrary-pattern programming is fast enough.
