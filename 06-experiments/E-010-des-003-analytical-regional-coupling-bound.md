# E‑010: Analytical Regional Coupling Bound

## Goal
Estimate peak displacement and maximum allowable coupling fraction for 5×5, 10×10, 20×20 regional updates using CAD‑derived stiffness values.

## Assumptions
- Stiffness (`k`) in *N/mm* derived from CAD: **10, 32.7, 50**
- Coupling fractions considered: **1 %, 5 %, 10 %**
- Base total force for 5×5 is 1000 N. Force scales with area: `F = 1000 × (size/5)^2`.
- Peak displacement `δ = (coupling × F) / k`.
- Target maximum displacement: **0.01 mm**.

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
|5     |10  |0.01 % |
|5     |32.7|0.03 % |
|5     |50  |0.05 % |
|10    |10  |0.00 % |
|10    |32.7|0.01 % |
|10    |50  |0.01 % |
|20    |10  |0.00 % |
|20    |32.7|0.00 % |
|20    |50  |0.00 % |

## Summary
- For **5×5** updates, 1 % coupling exceeds the 0.01 mm displacement limit with the softest stiffness (10 N/mm). The softest usable stiffness at 1 % coupling is **32.7 N/mm**.
- Larger updates (10×10, 20×20) amplify displacements by area. Even with a 1 % coupling, the required stiffness to stay below 0.01 mm is effectively infinite – i.e., we cannot satisfy the limit with any realistic stiffness for those sizes.
- The analysis suggests restricting coupling to well below 1 % for larger regional updates or adopting much stiffer materials.

## Next Steps
- Verify the CAD‐derived stiffness values with a quick FEM test.
- Explore alternative manufacturing methods to increase stiffness without significant cost.
- Consider limiting regional updates to 5×5 or smaller when operating under the 0.01 mm displacement budget.
