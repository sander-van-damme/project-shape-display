---
status: complete
builds-on: [E-006, A-004, DES-003]
---

# E-007: Architecture Comparison - Regional Isolation vs. Segmented Load Paths

## Objective
Compare the elastic disturbance mitigation potential of the segmented `A-004` architecture against the monolithic `DES-003` baseline.

## Disturbance-transfer model comparison

The `DES-003` baseline has disturbance that scales with the perimeter of the updated region. In `E-006`, a 20x20 update with an assumed 5% coupling fraction requires 124.26 N/mm support stiffness to stay within the proposed 0.10 mm neighbour-motion gate. This is a sensitivity calculation, not a measured property.

| Metric | `DES-003` baseline | `A-004` segmented candidate |
|---|---|---|
| Load path | Continuous through the assembly | Segmented by tile-level couplers |
| Disturbance scaling | Proportional to `4 × (side − 1)` boundary cells in the sensitivity model | Potentially proportional to active couplers at a tile boundary |
| Effective coupling | Unknown; elastic transfer remains unresolved | Unknown; coupler isolation is only an inference |
| Required stiffness | 26.16 / 58.86 / 124.26 N/mm for 5% coupling at 5x5 / 10x10 / 20x20 | Cannot be calculated without a coupler transfer function |

**Inference:** segmentation could prevent the baseline perimeter scaling, but no evidence here establishes that a conceptual coupler actually does so.

## Cost and complexity comparison

| Metric | `DES-003` | `A-004` |
|---|---:|---:|
| Working purchased-cost estimate | ~$210 | ~$192–$384 for 64 couplers |
| Primary complexity | Gantry coordination and optical readback | Coupler isolation, shaft torsion/backlash, and per-cell selection |
| Main unresolved failure modes | Reader classification, registration, wear, loaded-neighbour disturbance | Jam propagation, coupler wear, torsion/backlash, and tile assembly yield |

The cost figures are sourced-class sketches inherited from the candidate documents, not purchase quotes. Printed parts are excluded.

## Gates and disposition

* `DES-003` regional isolation for updates larger than 10x10: **FAIL / unresolved**, pending stiffness and coupling evidence.
* `A-004` regional isolation: **POTENTIAL PASS only**, pending a coupler coupon.
* Cost, refresh speed, reliability, and manufacturability of `A-004`: **unresolved**; segmentation is not a free improvement.

The bounded analytical comparison is complete. It does not promote `A-004` or qualify `DES-003` for regional updates. The cheapest decisive follow-up is a two-tile coupler isolation coupon: apply the 3.27 N service-load case to one tile, measure untouched-neighbour vertical/lateral motion and residual error, and compare effective coupling against direct contact. A 10x reduction is the pre-registered gate for justifying the added coupler complexity. Physical stiffness and coupling remain unmeasured.

Evidence class: calculated sensitivity model, sourced-class cost sketch, and inference from proposed load-path topology. No physical validation, FEA, or print-ready claim.
