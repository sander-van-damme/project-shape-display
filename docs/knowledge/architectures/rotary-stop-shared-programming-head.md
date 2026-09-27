+++
id = "A-001"
type = "architecture"
name = "Rotary-stop array with shared programming head"
status = "conditional"
mechanisms = ["M-012", "M-001"]
principles = ["P-002", "P-007", "P-008", "P-009"]
related_backlog = []
related_tests = ["test08_architecture_search", "test09_test08_validation"]
evidence = ["hypothesis"]
last_reviewed = "2026-09-27"
+++

# Rotary-stop array with shared programming head

## System concept
Each cell stores one of several heights in a rotary stepped stop. A common platen
provides long-stroke lift while a wide programming head writes rotor angles.

## Evidence and history
Test08 produced a conditional 26.25 s schedule. Test09 reproduced timing but found
unresolved detent, coupling, structure and sourcing gates.

## Decision state
Useful reference architecture; not product-qualified.
