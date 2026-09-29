<!-- © 2024 Sander Van Damme - All Rights Reserved. -->

# CEO launch assessment — 2026-09-29 ([SHA-6](/SHA/issues/SHA-6))

## Repository state (as found)

- Requirements are mature and well-documented in [`02-design-criteria/`](../02-design-criteria/README.md):
  ~400×400 mm active area, ~5.08 mm pitch (~6,400 columns), ≥40 mm travel,
  full-map change strictly <30 s, regional updates without full-board reset,
  purchased-component bands (<$200 ideal / $200–$400 acceptable / $400–$500 last
  resort / >$500 unacceptable), X1C + PLA fabrication baseline, modularity for
  the 256 mm build volume.
- Permanent program policy **no physical print tests** (DND-27): all evidence is
  CAD / CALCULATION / SIMULATION over sourced listings and stated assumptions.
- Three integrated designs coexist in [`08-integrated-designs/`](../08-integrated-designs/README.md):
  - **S5-R** (`s5r-shared-drive-register/`) — PROMOTED historical single-winner,
    slicer-ready build package of record.
  - **S6-LC** (`s6lc-low-cost/`) — MEASUREMENT-GATED; mission gates pass but
    per-cell reliability gate G8 is unresolved (and unresolvable by print under
    DND-27, carried as explicit residual).
  - **A1** (`a1-reliability-first/`) — CANDIDATE reliability-first machine;
    read/verify axis CAD-validated, writer rate bounded; only architecture with
    a structurally zero silent-error set (shared reader verifies every cell).
- Rich candidate space (S1–S5 + 30 screened topologies in
  [`04-architecture-candidates/`](../04-architecture-candidates/)) and an
  ordered falsification backlog (Q1–Q8, R01–R17) in
  [`05-research-questions/`](../05-research-questions/README.md).
- Standing mandate stored at
  [`01-project-description/board-mandate.md`](../01-project-description/board-mandate.md).

## Initial priorities

1. **Exploitation — harden A1 toward promotion.** A1 is the strongest
   reliability-first candidate. Next evidence: close the promotion gate
   (full-system timing/cost/scalability/reliability analysis + explicit
   residual risks + promotion decision record), adversarial-audit the
   binary-latch write path the way the shutter path was audited (A13/A14
   precedent), and quantify the reader/re-drive time inside the <30 s budget.
2. **Exploration — attack A1's cost and find step-changes.** A1's gantry +
   reader is mechanically heavier than S6-LC's broadcast approach. Pursue at
   least one fundamentally different low-purchased-cost architecture family
   (shared-register / banked-broadcast descendants of S3/S4, or a new family)
   with explicit kill criteria, without touching the S5-R baseline.
3. **Protect baselines.** S5-R remains the build package of record. No agent
   removes or overwrites a PROMOTED package; replacements are validated first
   and recorded in `07-evidence-and-decisions/`.

## Initial organization (CEO hires, 2026-09-29)

- **A1 Reliability Architect** (exploitation) — owns A1 promotion path.
- **Mechanism Explorer** (exploration) — owns alternative-architecture search
  with falsification-first evidence discipline.

Both use the free-model OpenCode failover runtime, `canCreateAgents=false`,
and hiring authority stays exclusively with the CEO.

## Open uncertainties (for the team first)

- A1 full-map timing decomposition with reader verify + retry inside <30 s.
- A1 purchased BOM placement in the cost bands at full 80×80 scale.
- Whether any broadcast/shared-register family can beat A1 on cost without
  reintroducing silent per-cell failure modes.
- Numeric regional-update disturbance limit (Q5 protocol proposal: 0.10 mm
  peak neighbour motion) — still a proposal, not a sourced requirement.
