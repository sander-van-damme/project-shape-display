---
status: complete
---
Hypothesis: Reducing shared-register writer channels alone can meet a $250 cost target.
Method: Fixed purchased base plus motor/channel costs; timing-constrained topology sweep using the historical shared-register model. Delivered estimate = purchased ×1.16.
Result: Fixed base $218.70 purchased, $253.69 delivered before writer channels. Historical cheapest timing-preserving configuration: $345.90 delivered (≈$298.19 purchased), 29.987 s modelled update.
Conclusion: Channel reduction alone failed the $250 target within this model. The fixed base proves a $250 delivered floor failure; it does not alone prove a $250 purchased failure. Reopen on a sourced base reduction or an architecture change.
Risk: Prices and component allowances are historical estimates. Timing margin is only 0.013 s; physical tolerances, retry and load are unverified. Search is restricted to modelled topologies, not a universal impossibility proof.
Evidence class: Calculation over historical BOM estimates and assumed timing; no quotation or physical test.
