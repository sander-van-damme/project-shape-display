# J — fresh final-package review

15 October 2026. Independent release review of the DES-008 recommendation,
construction and timing claims, owner handoffs, delivered meshes and portable
source archive. This review does not replace the separate adversarial CAD
checks and does not claim physical validation. Integration and portable-source verification are recorded below.

## Disposition

The recommendation is supportable as a **negative full-machine engineering
result with one useful small physical handoff**. Do not present it as a
qualified affordable, manufacturable or playable Shape Display. The package
states this directly, preserves failed alternatives, separates conditional
scene timing from stress and preparation times, and does not promote owner
short-thread observations into whole-array evidence.

The P1 rack article is appropriately narrower than the resident architecture.
Its operator observes support and retires dogs individually; it cannot
validate automatic simultaneous release on a common A frame. The delivered
instructions state that distinction and deliberately challenge mixed free
and dragged outputs. The memory article is correctly DEFERRED because its continuous
channels and short flags do not validate the resident paired discrete-pocket
writer. Preserving its verified files does not create a print obligation.

The original resident guide fails a reproduced admitted-play counterexample.
The separately named longer-bearing/shallower-tooth variant removes the tested
planar failures, but does not establish a general spatial tolerance proof.
Its entire nominal 0.10-mm unload margin can be consumed by vertical guide
play. Both that unresolved support transfer and the bank junction collision
must remain visible in the final recommendation. Neither is repaired by a
favorable ideal timing calculation.

## Independent artifact checks

The reviewer used an independent scratch audit for mesh/hash/link checks, separate from the authors’ validation scripts. The released plate manifests and canonical checkers retain the reproducible artifact evidence.

- All 17 local Markdown links in the two owner handoff directories resolve.
- Rack CAD source SHA-256:
  `0d75dbccb58f0134b698a23b19b4550c2cabab21a4e8aa852bce8a03ef6c3964`.
- Actual owner rack STL SHA-256:
  `0f2eac6dba80a600c243c5a252ebc9b59dc3d51421ab48e2ca614628d8dd4039`.
  It has **46 closed watertight bodies**, bounds
  **180.675 × 181.621 × 38 mm**, and approximately **39,445.90 mm³** volume.
  The final plate manifest matches the actual file and CAD. Its individual
  part quantities sum to 46. Small binary mesh coordinate rounding explains
  the negligible difference from the pre-export summed volume.
- All four rack result files name that same final CAD hash. They record
  **240 operation, 648 mixed-drag/retirement, 2,048 guide-play and 686
  assembly-path cases**, with no reported collisions. I checked consistency
  of these stored results; I did not repeat E's entire CAD campaign.
- Rack PDF source footer matches the released source. Its dimensions,
  76-mm stack, ten screw/nut joints, positive forced-descent requirement and
  individual retirement instruction agree with the handoff prose.
- Memory CAD source SHA-256:
  `c6bd26a5f29215c4c34e9e8b53471034562b58a0cf65c35863cc9377d86f89fd`.
- Actual deferred memory STL SHA-256:
  `6133ccb35fbcabd58ed9f2a67a199b3b2bcb4e4e079715c2d0c1bcee42bb0221`.
  It has **19 closed watertight bodies**, bounds **82.6 × 99.6 × 16.6 mm**.
  Both PDF and prose identify revision 3 and withdraw the general tolerance
  guarantee. Their numerical planar screen is explicitly restricted.

A closed mesh, source match and consistent drawing are release checks, not
proof of print stability, elastic return, manual assembly success, loading,
neighbor isolation or wear. No physical pass follows from this review.

## Portable reproduction

I generated and extracted a source ZIP into a separate directory, then ran
its calculation scripts from that extracted tree. No parent checkout source
was needed by the extracted calculation paths.

- `run_timing.py` reproduced the canonical timing JSON byte-for-byte:
  SHA-256 `f630338b13f4c860aad0b9c4c4a644521947d895683a3eb2adeef4c3a44b9216`.
- `check_revised_system.py` reproduced the full canonical revised-system JSON
  exactly, including source paths/hashes and corrected category ledgers.
- Independent timing and bounds scripts, cost and bank-drive scripts all ran
  successfully with the bundled historical dependency set.

The historical timing JSON is explicitly a baseline. Current recommendations
use the corrected 0.4-mm take-up and post-ground 0.7-mm seat/0.3-mm centering
sequence for both signs, while acknowledging physical rate and tolerance
limits. Retaining both result sets is honest only with their current labels.

## Release wording findings

Two minor consistency findings were sent to the lead during integration:

1. The verification introduction called both articles architecture-changing,
   despite the correct decision that P2 no longer qualifies the selected
   writer. Describe the two artifacts according to their current priorities.
2. The construction principle section describes continuous code channels,
   while the integrated writer requires paired discrete pockets. Label the
   continuous-channel paragraph as the earlier principle article and point
   explicitly to the integrated distinction. Local reproduction commands in
   resident documents should state their working directory, unlike the
   repository-root commands in verification.

These are reconciliation requests, not reasons to reopen discarded CAD.
The dispositions follow below.

The lead corrected both wording findings. The resident reproduction paragraphs
now use repository-root command paths, consistent with the verification page. The independent integration final review also
explicitly limits its 3,390-check upward seating interpolation to the sampled
free-seating path. This closes a source-scope concern without silently
promoting that replay into a sticky-contact dynamics proof.

Only the rack handoff is currently READY/P1. The memory and DES-007 owner
articles are DEFERRED, consistent with the current recommendations.

## Integrated-source archive check

After resident integration was copied, I built a second portable archive and
verified all **123 then-included manifest file hashes** against the ZIP bytes.
The original and separately named variant sources match their reviewed frozen
hashes. From the extracted tree, both `check_resident_counterexample.py` and
`check_resident_escape.py` ran successfully and reproduced their canonical
JSON records exactly: 0.1013509041 mm³ own-rack and 14.68805388 mm³ bank
counterexamples, and the bounded variant's 1,954 candidates / 1,924 admitted
planar poses with zero reported tested collisions. Empty Boolean intersections
produced ordinary trimesh center-of-mass warnings in the counterexample run;
they did not change its numeric result.

A final canonical Markdown sweep found three incorrectly relative links in
`review/manufacturing-screen.md`: its bank-drive and two analysis references
needed a parent-directory prefix after the document was relocated. This was
corrected before release. No new mechanism or artifact blocker emerged.
