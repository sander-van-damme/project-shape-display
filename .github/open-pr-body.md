# DND-103: reliability-first design criteria (buildability + repeated-mechanism gate)

Closes [DND-103](/DND/issues/DND-103). Addresses section 1 of [DND-102](/DND/issues/DND-102).

## What changed

`02-design-criteria/README.md` — adds the reliability-first design-criteria revision. No existing
mission requirement is weakened; the new content is additive and gates.

- **Surface pitch does not constrain the internal mechanism.** 5.08 mm is *visible surface
  resolution*, not a per-cell mechanism-size budget. Selection / memory / locking / programming
  machinery may live under several cells, beside the display, at row/bank/module level, in a moving
  external mechanism, a replaceable mask, a tape/card/film, or a separate mask-generation subsystem.
  Program principle: *thousands of simple things + a few sophisticated shared mechanisms.*
- **Repeated-mechanism reliability criteria** (new section): strongly-discouraged list
  (single-extrusion-line moving features, exact-force tiny printed springs, sub-mm precision
  interactions repeated thousands of times, friction-sensitive retention where a hard stop works,
  tight tolerances across all 6,400 cells, silent microscopic failures with no recovery), preferred
  list (large positive engagement, hard stops, compression-loaded structures, generous clearances,
  print-variation tolerance, replaceable modules, accessible wear parts, individually testable
  repeated parts, architecture-level redundancy/error recovery), the gate question **"what has to
  work correctly 6,400 times?"**, and a required per-architecture reliability audit (repeated moving
  parts, precision contacts/cell, compliant printed elements, wear interfaces, tolerance-sensitive
  interactions, correlated vs single-cell failure modes, serviceability).
- **Reliability and prototype-testability are now first-class gates** (comparison axes 10 and 11),
  not tie-breakers.
- **Provisional design rule** for minimum repeatable feature size — conservatively labelled
  provisional until an actual X1C + PLA calibration coupon confirms it; no false precision from the
  7 µm lidar sensor spec.
- **Mask subsystem is part of the machine** — inside the product boundary for design, cost, timing
  and test; mask-generation time is inside the map-change budget unless double buffering is
  explicitly designed and the UX explained.
- **Honest timing decomposition** — digital processing / physical mask generation / mask
  transport-indexing / display reset / broadcast lift / settling-locking / verification, reporting
  **visible-transition time** and **sustained arbitrary-map cycle time** separately.
- **Prototype ladder requirement** — A single cell → B small full-pitch array → C one bank/module →
  D multiple banks → full machine; a mechanism that cannot be meaningfully tested in a small cheap
  coupon is scored down.
- **Regional-update product trade-off note** — a full-board reset for every small reveal is a
  product-level weakness.

## Engineering question

Can the design criteria force future architectures to optimize for real-world buildability and
repeated-mechanism reliability rather than merely CAD/geometric fit and spreadsheet cost? The
central decision: **the dense visible surface may stay at 5.08 mm pitch, but the precision machinery
controlling it should be as large, shared, sparse, external, or modular as possible.**

## Evidence class

PRODUCT DECISION / DOCUMENTATION only. No CAD, print, purchase or measurement. No mission
requirement is relaxed; the new criteria add gates.

## Passed / failed / uncertain

- **Passed:** all DND-103 required edits present and explicit; existing mission requirements
  (~400×400 mm, 5.08 mm pitch, ~6,400 cells, ≥40 mm travel, <30 s full-map, <$500 purchased,
  regional updates, prototype ladder) unchanged.
- **Uncertain:** the numerical minimum repeatable feature size remains a *provisional* rule pending
  an X1C + PLA calibration coupon — honestly labelled as such.
