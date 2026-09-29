# DND-103: reliability-first design-criteria audit (buildability + repeated-mechanism gate)

Closes [DND-103](/DND/issues/DND-103). Parent program: [DND-102](/DND/issues/DND-102).

## What changed

Doc-only update to `02-design-criteria/README.md` (no code, geometry, BOM or CAD touched):

- **Surface pitch does not constrain the internal mechanism** — the 5.08 mm figure is a *visible
  surface resolution* requirement, **not** a per-cell mechanism-size budget. Internal selection /
  memory / locking / programming machinery may live under several cells, beside the display, at
  bank/module level, in a moving external mechanism, in a replaceable mask, in a tape/card/film, or
  in a separate mask-generation subsystem.
- **Repeated-mechanism reliability criteria** — explicit *strongly discouraged* list (one-extrusion-line
  moving features; tiny printed springs whose exact force decides correctness; sub-mm precision
  interactions repeated thousands of times; friction-sensitive retention where a hard stop is possible;
  6,400-cell tight tolerances; silent unrecoverable single-cell failures) and *preferred* list (large
  positive engagement; hard stops; compression-loaded structures; generous clearances; replaceable
  modules; accessible wear parts; individually testable repeated parts; redundancy / recovery).
- **Per-architecture reliability audit (required)** — repeated moving parts, precision contacts/cell,
  compliant printed elements, wear interfaces, tolerance-sensitive interactions, correlated vs
  single-cell failure modes, serviceability. Gate question: *what has to work correctly 6,400 times?*
- **Provisional design rule** for minimum repeatable feature size — no invented precision around
  printer tolerances (7 µm lidar ≠ part tolerance; X1C publishes no universal part tolerance).
- **Mask subsystem + honest timing** — mask generator is inside the product boundary; timing must be
  decomposed (digital / mask-gen / transport / reset / lift / settle / verify) and both
  *visible-transition* and *sustained cycle* times reported.
- **Prototype ladder requirement** — Prototype A single cell → B 5×5 array → C one bank → D multiple
  banks → full machine.
- **Reliability + prototype testability added as gates** in the concept-comparison list (items 10–11).
- **Regional-update trade-off** — regional updates may be satisfied at bank/segment/mask-strip level
  where simpler; the trade-off must be quantified and surfaced.

## Purpose

Removes the failure mode where surface pitch silently becomes an internal mechanism budget, and makes
reliability/buildability a first-class gate. Unblocks the [DND-104](/DND/issues/DND-104) reliability-first
architecture program for convergence/selection.

## Evidence discipline

Documentation/engineering-policy change only. No print, no purchase, no measurement (DND-27). No
sourced-fact, calculation, CAD or measured claims are introduced beyond the already-sourced X1C /
miniature references.

## Verification

- Doc-only diff; no executable checks affected.
- `engineering-checks` CI suite runs green on the push event for this branch.
