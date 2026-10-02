---
status: candidate
builds-on: [M-008, M-004, P-006]
---

A common shaft/belt/rail supplies motion to tiles with local passive memory. One tile-level coupler enables regional reset/replay; all couplers enable full-map operation.

Risks: expensive couplers, hidden per-cell selector complexity, shaft torsion/backlash and jam propagation. A 64-tile design has only $3–6/coupler before consuming $192–384 of bought budget; these are screening allowances, not sourced prices.

Test: two 2×4 tiles on one bus; load one while cycling the other, then both. Measure torque, phase error, isolation, fault propagation and complete coupler cost.
