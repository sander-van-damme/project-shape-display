---
status: rejected
builds-on: [DES-004, M-013, M-014, P-006, P-008]
---
# A-010: retired translating aperture-gate implementation

The proposal replaced per-cell rotary axles with a five-position planar slider, a separately supported follower/stop and shared writer/readback. Removing axle hardware could reduce purchased cost, but a complete five-height support mechanism was never established.

E-034 rejects the original five-state claim; E-039 rejects the bounded repair. A 3.00 mm aperture translated through 3.20 mm needs at least 6.20 mm longitudinal envelope, exceeding the frozen 4.90 mm pocket. The actual CAD also has an oversized slider, only the S2 aperture and no stop-plate-to-frame connector. Scalar clearance checks passed despite these defects. Evidence is calculation/CAD inspection, with no physical measurements.

Retired under ADR-009. Keep the failure and source for comparison; stop incremental repairs and coupon handoffs within this interface. A materially redefined mechanism may reopen the principle only after modeling every height, transition, actual guide envelope and continuous load path, then comparing complete-machine cost/time and manufacturing uncertainty against other families. Planar mechanisms as a class are not rejected.
