---
status: candidate
builds-on: [M-003, M-004, DES-003]
---

Encoding: three passive binary latch bits per visible cell, read as the five-code Gray sequence `000, 001, 011, 010, 110` for 0/10/20/30/40 mm. The two unused codes are invalid and must be rejected by the reader; arbitrary transitions may change up to two bits.

Operating principle: a travelling writer addresses the three bit lanes and a fixed-height reader verifies all three bits after writing. Each latch is load-bearing only through a hard stop; state retention is passive. A cell is accepted only when its three-bit code is valid and equals the requested level. Retry can rewrite a failed bit or the whole cell.

Strengths: uses DES-003's mature binary latch/readback pattern; Gray adjacency limits the number of contacts that must move for neighbouring levels; a single stuck bit is observable as either a wrong valid code or an invalid code.

Failure modes and unknowns: three latch contacts per cell triple wear, force opportunities and printed alignment burden; two-bit changes during a large jump can transiently form a different valid height; a reader channel or common gantry fault can correlate errors. The cost and timing advantage disappears if all three bits cannot be written/read in parallel.

Analytical screen: serial bit passes require approximately 3 × DES-003's 5.864 s write and 3 × 5.864 s verify passes, before retry, exceeding 30 s. Parallel channels retain the timing but add two writer contacts and two reader channels per head. Using the current BOM allowances, the rough purchased delta is 8×2×($6+$12) = $288, taking the $181 DES-003 sketch to about $469 before delivery uplift; this is a calculation, not a quote.

Cheapest falsification: print one 5.08 mm-pitch 5-cell strip with three bit latches and a three-prong writer/read target. Measure whether all valid codes can be read under loaded neighbours and whether the two unused codes are reliably rejected. Reject if any bit needs serial timing or if the code cannot be classified with a generous threshold margin.

Evidence: encoding and cost/timing screen are calculations/inferences from DES-003's BOM and timing model; no physical validation.
