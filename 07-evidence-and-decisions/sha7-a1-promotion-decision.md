<!-- © 2024 Sander Van Damme - All Rights Reserved. -->

# SHA-7 A1 promotion decision — GATE (promote architecture, gate build on coupon A)

> **Evidence class: CALCULATION + CAD only** (DND-27). This note promotes no
> hardware and validates nothing physically. S5-R and S6-LC are untouched.

## Verdict: GATE

A1 meets every paper gate for promotion — timing, cost, reliability structure,
write-path audit — with the margins recorded in
[`sha7-a1-promotion-timing-cost.md`](sha7-a1-promotion-timing-cost.md). The
remaining blockers are **measurement-only questions DND-27 forbids settling
analytically**, so the promotion is conditional: A1 is the reliability-first
candidate of record, and a full-machine build waits on **coupon A**
(single cell at true pitch: toggle force + read contrast).

## Why not REJECT

- Sustained full-map cycle **19.63 s < 30 s** with verify + bounded retry
  (10.4 s margin; stress corners also clear).
- Purchased BOM **$181 IDEAL**, hostile reprice still IDEAL, enforceable
  per-unit ceiling stated and asserted.
- Write-path audit **CLEAN 22/22**; the only architecture with a structurally
  zero silent-error set and per-cell readback + bounded retry.
- Pre-registered DND-108 audit stays CLEAN (11/11); DND-112/114/115 gates green.

## Why not unconditional PROMOTE

Explicit residual-risk list (each with its kill line):

| # | Residual | Class | Kill line |
|---|---|---|---|
| R1 | As-printed latch **snap force** (3.0 N nominal assumed) | assumption → coupon | coupon A kills if measured snap mean > **7.14 N** |
| R2 | Hinge **wear** across 6,400 pivots | measurement-only | coupon B (5×5 cycling) kills on stall/fracture |
| R3 | Gantry **registration** over 406 mm (thermal, belt stretch) | measurement-only | coupon C kills on > half-pitch drift |
| R4 | Flap **reflectance** (ρ ≈ 0.05) + aperture constants | assumption | coupon A kills if on/off < **2×** |
| R5 | 4-head boundary (30.0 s) — head count is load-bearing | calc | build adopts **8 heads minimum** |
| R6 | Regional disturbance 0.00 mm is modelled, Q5 0.10 mm still a proposal | calc | coupon B measures neighbour motion |

## Next action

CEO: accept GATE (or redirect); the buildable next step is coupon A as defined
in the A1 prototype ladder — a physical handoff, not agent-reachable under
DND-27. No further analysis can retire R1–R4.
