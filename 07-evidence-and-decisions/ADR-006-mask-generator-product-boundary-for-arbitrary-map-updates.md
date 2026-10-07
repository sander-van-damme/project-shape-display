---
status: active
builds-on: [Q-010, E-017, A-011, ADR-005, E-044]
---
# ADR-006: complete arbitrary-map product accounting

Decision: include all machinery and time needed to produce an unanticipated map. Count programming, selection/memory, transport or registration, load actuation, sensing, recovery and service media. Buffering can reduce visible wait but cannot hide sustained generation time or purchased hardware.

The former preference for a reusable four-plane writer is superseded by ADR-009. A-011 is one comparison hypothesis; four planes, a travelling writer and a 5×5 coupon are not mandatory product features. Other mechanisms may satisfy the same complete boundary.

Basis: E-017 shows why prepared media, cassette inventory and buffering alone are incomplete answers to arbitrary-map generation. The examined serial writer misses the timing target under its assumed rates; this is a bounded rejection, not a universal rejection of serial or different addressing topologies. A-011's 20.18 s prediction depends on simultaneous plane writing and inherited verification/actuation rates. E-044 and E-046 preserve incomplete cost/compatibility evidence, not a procurement pass.

Consequence: compare new complete architectures computationally, propagate manufacturing and model uncertainty, and preserve regional isolation and exact fault handling. Stop automatic coupon/RFQ handoffs for the old boundary. A new candidate must define its actual state-changing mechanism before fixture detail can count as implementation evidence.

Residual risk: complete accounting does not prove manufacturability, sensing, durability or physical performance. The selected implementation will require appropriate physical qualification after computational screening and targeted calibration.
