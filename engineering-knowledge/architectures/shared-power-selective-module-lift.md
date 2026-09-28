+++
id = "A-006"
type = "architecture"
name = "Shared power with selective module lift"
status = "hypothesis"
mechanisms = ["M-008", "M-011", "M-003"]
principles = ["P-001", "P-003", "P-006", "P-008"]
related_backlog = ["R09", "R12", "R17"]
related_tests = []
evidence = ["hypothesis"]
last_reviewed = "2026-09-27"
+++

# Shared power with selective module lift

## System concept
One or a few power sources feed a module-level mechanical bus. A clutch or matrix
selector couples only requested tiles to the lift. An "all modules" mode can
support fast full-board reset.

## Why it may fit
The selector problem is reduced from ~6400 cells to tens of modules while local
reveals remain possible.

## Cheapest falsification path
Two-module lift with one shared actuator and selective coupling; one module stays
loaded and stationary while the other cycles.
