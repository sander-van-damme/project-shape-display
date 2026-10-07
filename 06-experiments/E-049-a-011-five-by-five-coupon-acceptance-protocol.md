---
status: complete
builds-on: [ADR-006, ADR-009, Q-010, E-018, E-044, E-046, E-048]
---

# E-049: A-011 coupon acceptance extensions

Retained protocol assumptions, not a frozen fabrication release or physical result. E-018 is canonical for interface geometry, map allocation and schema; its undefined rewritable medium, event-coverage gaps and incomplete residual validation prevent executing this as a complete mechanism test. ADR-009 ends automatic coupon preparation. The original packet is archived in commit `7c52d3a`.

## Distinct proposed acceptance lessons

- Record channel-specific breakaway, engagement and return forces. Historical proposed margins were 2× breakaway and 1.25× return requirement; these are unvalidated engineering choices, not component capabilities.
- Log simultaneous current/voltage, pulse/return time and temperatures. The proposed 20% supply/driver margin and 20 °C rise ceiling need comparison with actual ratings and duty cycle before reuse.
- Deliberately block an aperture, mis-seat/swap a plane and corrupt an unchanged cell at preflight and midpoint. Exact-state comparison must reject each; a confidence score cannot override a wrong state.
- Treat replacing a failed plane as a new sample, preserving the stopped run. Inspect force/retry/wear trends under a rule specified before observing results; do not discard early failures or adjust alignment to obtain a pass.
- Preserve instrument/calibration IDs, raw signals, complete per-plane residual coverage, load vectors, fixture datums, as-built geometry and uncertainty. A synthetic schema check does not validate these measurements.

The inherited 0.85 reader threshold is uncalibrated. The 1,000-cycle/100-reseat plan is a proposed allocation, not reliability evidence. E-048 establishes that E-018's 0.20 mm neighbour gate does not close the historical 0.10 mm peak/residual screen, and neither is an approved product limit. Five centres at 5.08 mm pitch span **20.32 mm**; 25.40 mm is the five-cell footprint, not the centre-to-centre span.

Before reuse, define and computationally screen an actual state-changing mechanism through all required states and transitions, repair event/residual coverage, and propagate manufacturing and reader uncertainty. A physical proposal must identify a decision-changing parameter or qualification claim and justify its article and sample sizes. No procurement or fabrication follows from this retained protocol.
