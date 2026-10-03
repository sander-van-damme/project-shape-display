# E‑010: Analytical Regional Coupling Bound

## Goal
Estimate a conservative screening displacement and maximum allowable coupling
fraction for 5×5, 10×10, and 20×20 regional updates. This is an analytical
sensitivity bound, not a geometry-resolved FEA result.

## Assumptions
- Candidate stiffness (`k`) in *N/mm*: **10, 32.7, 50** (**inferred
  sensitivity values**, not measured or actually derived by the present CAD)
- Coupling fractions considered: **1 %, 5 %, 10 %**
- Base total force for 5×5 is 1000 N (**unresolved/inferred sensitivity input**;
  it is not established by the DES-003 CAD). Force scales with area:
  `F = 1000 × (size/5)^2`.
- Peak displacement `δ = (coupling × F) / k`.
- Target maximum displacement: **0.01 mm**.

## Geometry and boundary audit

The only geometry reference is the DES-003 5×5 Coupon-B SCAD fixture
(`scad/a1_coupon_b_5x5.scad`), a 40 mm square at 5.08 mm pitch. The 10×10
and 20×20 cases are represented only by the area-scaling factor; they are not
meshed or geometry-resolved here. Support compliance, actuator trajectory,
contact/clearance, material properties, and worst boundary orientation are
omitted from this screening model and remain **unresolved**. Consequently,
the stiffness and force inputs must not be described as CAD-derived results.

## Results

| Size | k (N/mm) | Coupling | δ (mm) |
|------|----------|----------|--------|
| 5    | 10  | 1 % | 1.0000 |
| 5    | 10  | 5 % | 5.0000 |
| 5    | 10  |10 % |10.0000 |
| 5    | 32.7| 1 % | 0.3058 |
| 5    | 32.7| 5 % | 1.5291 |
| 5    | 32.7|10 % | 3.0581 |
| 5    | 50  | 1 % | 0.2000 |
| 5    | 50  | 5 % | 1.0000 |
| 5    | 50  |10 % | 2.0000 |
|10    | 10  | 1 % | 4.0000 |
|10    | 10  | 5 % |20.0000 |
|10    | 10  |10 % |40.0000 |
|10    |32.7 | 1 % |1.2232 |
|10    |32.7 | 5 % |6.1162 |
|10    |32.7 |10 % |12.2324 |
|10    |50   | 1 % |0.8000 |
|10    |50   | 5 % |4.0000 |
|10    |50   |10 % |8.0000 |
|20    |10   | 1 % |16.0000 |
|20    |10   | 5 % |80.0000 |
|20    |10   |10 % |160.0000|
|20    |32.7 | 1 % |4.8930 |
|20    |32.7 | 5 % |24.4648 |
|20    |32.7 |10 % |48.9297 |
|20    |50   | 1 % |3.2000 |
|20    |50   | 5 % |16.0000 |
|20    |50   |10 % |32.0000 |

## Maximum Coupling to Keep δ < 0.01 mm
| Size | k (N/mm) | max coupling |
|------|----------|---------------|
|5     |10  |0.0100 % |
|5     |32.7|0.0327 % |
|5     |50  |0.0500 % |
|10    |10  |0.0025 % |
|10    |32.7|0.0082 % |
|10    |50  |0.0125 % |
|20    |10  |0.0006 % |
|20    |32.7|0.0020 % |
|20    |50  |0.0031 % |

## Summary and disposition
- The calculation contradicts the earlier claim that 5×5 at 1% coupling is
  viable: at 32.7 N/mm it predicts **0.3058 mm**, and at 50 N/mm it predicts
  **0.2000 mm**, both above the 0.01 mm target.
- The exact bounds are **0.0327%** (32.7 N/mm) and **0.0500%** (50 N/mm) for
  5×5, not 1%. For 10×10 and 20×20 the allowable fractions are lower by 4×
  and 16× respectively.
- Therefore this screening bound does **not qualify DES-003**. It is an
  adverse calculated sensitivity result, while the force, support compliance,
  material properties, actuator trajectory, contact/clearance, and worst
  boundary orientation remain unresolved. No physical validation is claimed.

## Next Steps
- Freeze and run the E-009 Coupon-B sequence, or replace this screening bound
  with a geometry/material/support-resolved FEA model before making a regional
  qualification claim.
