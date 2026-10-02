---
status: proposed
builds-on: [ADR-002]
---
Decision: Keep global reset only as an unimplemented cost-reduction hypothesis. Do not adopt it as a replacement for isolated regional updates.
Basis: Historical arithmetic deletes carriage hardware for a $37.59 reduction: $189.18 purchased and $219.45 with 1.16 uplift; predicted mechanism cycle 4.9 s and lift torque margin 1.29. Source/BOM/CAD were not updated to implement the proposal.
Consequence: Any reconsideration must establish reset load path, platen stiffness, mask preparation cost and behaviour of untouched loaded terrain. A fast reset-and-rewrite still disturbs unrelated terrain.
Residual risk: Added global load, synchronisation and silent failures are unvalidated. No demonstrated regional isolation; the cost and cycle estimates do not resolve that requirement.
