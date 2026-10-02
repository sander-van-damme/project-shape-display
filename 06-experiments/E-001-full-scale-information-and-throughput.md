---
status: complete
---
Hypothesis: Sharing actuators can make an 80×80, five-state field affordable and fast.
Method: Count independent states, completed transactions and purchased selectors; 6,400 cells, full update strictly below 30 s.
Result: Information floor = 6,400 × log2(5) ≈ 14,860 bits. Three-bit coding uses 19,200 bits. A serial writer needs >213.3 completed cells/s before reset, travel, settling or retry. Four unary thresholds require 25,600 passive decisions. Even $0.50 purchased selection per cell costs $3,200.
Conclusion: Share purchased selection or place it in a reusable programmer. Parallelism is necessary unless complete serial transactions are demonstrably fast enough.
Evidence class: Calculation. No demonstrated mechanism rate. Information capacity does not establish an attainable physical programming rate.
