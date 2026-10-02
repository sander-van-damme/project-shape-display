---
status: active
builds-on: [DES-003, E-002, E-005]
---
Decision: Use the reliability-first shared writer/reader architecture as the analytical baseline. Retain its integrated source; gate a full-machine build on mechanism and sensing evidence.
Basis: Modelled update fits <30 s with eight heads. Historical purchased BOM estimate is $181. Per-cell readback and retry address the silent-error problem structurally.
Consequence: First establish latch force, read discrimination, repeatable registration, hinge life and loaded regional independence. Historical coupon limits: mean snap force ≤7.14 N; no snap >10 N; optical on/off ratio ≥2. These are proposed acceptance thresholds, not measurements.
Residual risk: Readback is not proof of zero silent errors. Sensor faults, calibration drift, mechanical jams and exhausted retries remain possible. Historical cost excludes printed material and assembly. No source here physically qualifies the machine.
