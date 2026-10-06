---
status: candidate
builds-on: [DES-003, A-005, M-012]
---

Decision: select a five-stop rotary support rotor as the smallest bounded successor to DES-003. Each 5.08 mm visible column is carried by one printed rotor/follower pair with hard stops at 0/10/20/30/40 mm. A frame-fixed vane or coded face presents the selected state to the travelling reader at constant standoff. The rotor is detented/passively retained; the writer turns only changed rotors and the reader verifies every addressed cell, with bounded retry.

## Candidate comparison

| Gate | Rotary five-stop rotor (selected) | Three-bit Gray latch (A-009) |
|---|---|---|
| Encoding | One direct 5-state mechanical code; no invalid visible states | `000,001,011,010,110`; two invalid codes and 3 bits/cell |
| Write/read | Travelling indexed writer; fixed-height coded vane reader; full-field verification and retry | Travelling three-prong writer and 3-channel reader, or 3 serial passes |
| Failure observability | Wrong stop/read code is detected; jam is retryable if the rotor can move | Wrong/invalid bit code is detectable; correlated channel faults remain |
| Regional update | Change only target rotors; no global reset; verify target region or full field | Same in principle, but more contacts can disturb neighbours |
| Purchased delta | No new bought actuator is identified, but the DES-004 BOM is not reconciled; $0 delta is unresolved until shafts/axles, reader/writer interfaces and service spares are priced. Existing 8 actuator/reader positions are retained; printed rotor replaces printed latch geometry | Parallel implementation roughly +$288 allowance, about $469 total; serial implementation fails timing |
| Print/manufacture | One larger rotating part/cam per cell; generous hard stops, but detent friction and shaft clearance are critical | Three repeated latch interfaces/cell; more alignment, contact wear and duplicate read channels |
| Update-time scaling | Changed-cell write plus verification; regional time is O(changed cells) with fixed gantry overhead | O(changed cells) if parallel, approximately 3× passes if serial |

## Decisive analytical bound

The current DES-003 calculation gives 5.08 ms traverse time per pitch at 1,000 mm/s. Bound the rotary writer at four worst-case detent increments × 2.0 ms/increment = 8.0 ms actuation, plus 1.0 ms settling. The write pass is therefore `6400/8 × (8+1) ms + 1.0 s ramp = 8.2 s`. Retain DES-003's calculated 5.864 s full-field verification, 3.0 s reset/transport allowance, 0.05 s map processing, 1.5 s settling and 1.3472 s expected retry budget at 1% miss. Total = `8.2 + 5.864 + 3.0 + 0.05 + 1.5 + 1.3472 = 19.9612 s`, leaving 10.0388 s analytical margin. This remains below 30 s, but the 2 ms/increment and rotor-return assumptions are unresolved assumptions, not measurements.

A sensitivity bound is more useful than the nominal point: with 4 ms/increment, write becomes `6400/8 × (16+1) ms + 1 s = 14.6 s`, total `26.3612 s`; with 5 ms/increment, total is `29.5612 s`; the bound crosses 30 s at about 5.14 ms per detent increment. Regional updates retain the DES-003 structural property because no full-board lift/reset is required; exact local time is unqualified until rotor torque and return behaviour are measured.

## Reliability and fabrication screen

Strengths are one state-bearing element per cell, passive load retention, direct five-level encoding, per-cell readback/retry, and no purchased component multiplied by 6,400. Main risks are detent creep/wear, rotor shaft friction under miniature load, cross-cell coupling during writer engagement, and whether a coded vane remains optically separable at a fixed reader standoff. Printability is plausible but not qualified: the actual process needs clearance and cycle-life coupons.

Cheapest credible falsification: a final-pitch 5×5 loaded rotor/readback coupon with a frame-fixed reader target and proposed writer prong. Use 10,000 balanced transitions across all directed stops while applying the 3.27 N design service load; record missed stops, return force, read-code margin, neighbour displacement, and before/after clearances. This is a smoke/falsification gate, not life qualification: 1,000 transitions are too weak for the project map-yield target, and even 10,000 transitions cannot establish it. Before that test, CAD clearance and the timing/cost bounds above are the cheapest checks.

Disposition: bounded successor remains conditionally viable, but no detailed production CAD is justified until the independent timing, readback, load/isolation, fit, and BOM gates are closed. Do not claim hardware performance or merge to main. Evidence is analytical/CAD-derived/inferred from DES-003; no physical validation.
