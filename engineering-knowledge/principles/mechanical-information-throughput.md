+++
id = "P-009"
type = "principle"
name = "Mechanical information throughput"
status = "active"
related_mechanisms = ["M-001", "M-002", "M-007", "M-011"]
related_architectures = ["A-003", "A-005"]
last_reviewed = "2026-09-27"
+++

# Mechanical information throughput

## Statement
Evaluate how many independent cell states or state bits an architecture writes per
mechanical engagement and per second, not just actuator speed.

A five-level 6400-cell map contains at least about
`6400 × log2(5) ≈ 14,860 bits`, implying roughly 495 state bits/s over 30 s before
reset, motion, verification and recovery overhead.

This is a screening metric, not a complete machine model.
