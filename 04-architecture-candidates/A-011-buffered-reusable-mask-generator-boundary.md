---
status: superseded
builds-on: [Q-010, P-009, DES-003, DES-004, E-017]
---
# A-011: reusable parallel mask-generator reference

Architecture hypothesis: four binary threshold planes plus a bottom stop encode five heights. A parallel writer changes the planes during one addressed engagement; positive registration, clamp/transport, exact state verification, bounded retry and replaceable media complete the product boundary. E-018 defines a carrier/interface and protocol; it does not implement the rewritable aperture mechanism.

Historical timing: `6400/(8×71)=11.27 s` writing, plus 0.05 processing +1.50 registration +5.864 verification +0.50 settling +1.00 retry gives 20.18 s. Four sequential plane passes at the same eight-head rate give about 45.07 s writing and 53.98 s total. All are assumed/calculated schedules, not measured performance. Local 5×5 predictions are 0.72/1.72 s depending on transport. Verification duration and hardware parallelism must be justified by an actual implementation.

E-044 retains historical cost scenarios and their incomplete scaling/compatibility assumptions; E-046 retains reader/actuator limits. E-048 leaves loaded-neighbour isolation unresolved. Registration, real simultaneous state changes, force, readback, wear and correlation remain unqualified.

Under ADR-009 this is a comparison reference, not the selected leader or a required embodiment. Its reusable-state/shared-energy/verification principles may seed new architectures. Do not continue another coupon or sourcing loop without a concrete new mechanism and decision-relevant computational comparison. Four planes, eight heads and the inherited pitch-level writer interface are this hypothesis's assumptions, not universal constraints on invention.
