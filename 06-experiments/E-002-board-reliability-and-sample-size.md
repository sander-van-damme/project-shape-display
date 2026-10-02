---
status: complete
---
Method: Independent, identical per-cell failure probability q; board correct only if all 6,400 cells are correct. P(correct) = (1−q)^6400.
Result: q=1e−4 gives 52.7% correct boards; q=1e−5 gives 93.8%. A proposed 99% correct-board target requires q≤1.5704e−6. Approximately 1.91 million independent zero-failure trials are needed for a one-sided 95% upper bound at that q: n≥ln(0.05)/ln(1−q).
Conclusion: A clean small coupon can reject gross mechanism defects but cannot establish full-board reliability. Add observable state and bounded repair, or justify the required failure rate with suitable evidence.
Risk: Shared faults, print batches, wear and correlated failures invalidate independence. Feedback itself can miss or misclassify errors. The 99% target is an analytical test objective, not a sourced requirement.
Evidence class: Calculation; no measured failure distribution.
