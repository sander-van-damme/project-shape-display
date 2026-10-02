---
status: complete
builds-on: [DES-003]
---
Method: Historical reliability-first timing model with eight writer heads, 1.0 m/s traverse, snap-trigger writing, full readback, 1% assumed miss rate and bounded retries.
Result: 19.6252 s sustained full-board prediction. Four heads predict 31.3532 s and fail the <30 s target. Eight heads at 5% assumed misses predict 25.0140 s. Slow 0.5 m/s traverse with pessimistic actuation predicts 29.0252 s. Addressed local predictions: one cell 0.3124 s; 10×10 cells 0.4730 s; 20×20 cells 0.9922 s.
Conclusion: Retain eight heads as the model baseline. Confirm complete loaded write/read/retry cycles and gantry reversal overhead before treating timing as demonstrated.
Risk: Snap force, speed, settle time, optical classification and retry convergence are unmeasured. A modelled zero rigid-body neighbour displacement does not bound elastic disturbance. The 0.10 mm disturbance limit remains a proposed test threshold.
Evidence class: Calculation over CAD geometry, actuator limits and assumptions; no physical timing measurement.
