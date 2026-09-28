+++
id = "P-008"
type = "principle"
name = "Functional separation"
status = "active"
related_mechanisms = ["M-008", "M-009", "M-012", "M-015"]
related_architectures = ["A-001", "A-006"]
last_reviewed = "2026-09-27"
+++

# Functional separation

## Statement
Do not require one component to simultaneously select, move, remember and support
a cell.

Separate power delivery, addressing, state memory, load support, reset and
verification. This is a central synthesis lesson from Test08 and the broader
research.
