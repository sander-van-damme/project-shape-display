+++
id = "A-003"
type = "architecture"
name = "Planar mechanical memory with independently updateable tiles"
status = "hypothesis"
mechanisms = ["M-013", "M-014", "M-011"]
principles = ["P-003", "P-004", "P-006", "P-008", "P-009"]
related_backlog = ["R14", "R15", "R17"]
related_tests = []
evidence = ["hypothesis"]
last_reviewed = "2026-09-27"
+++

# Planar mechanical memory with independently updateable tiles

## System concept
Partition the board into local tiles. Each tile contains planar height memory and
can be cleared/reprogrammed without resetting neighboring terrain.

## Functional decomposition
- selection: module/tile selector;
- power: shared module lift;
- memory: perforated or reprogrammable planar layers;
- load support: first-stop plate or local hard support;
- regional update: independent tile operation.

## Main unknowns
Tile size, seams, sheet registration, local lift coupling, insertion force and a
writer that does not recreate thousands of bought channels.

## Cheapest falsification path
Two adjacent 5×5 tiles; modify one while measuring motion of the loaded untouched
tile.
