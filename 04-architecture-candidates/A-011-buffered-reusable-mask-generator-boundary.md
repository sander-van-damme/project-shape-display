---
status: candidate
builds-on: [Q-010, P-009, DES-003, DES-004, A-010, E-017]
---

# A-011: reusable parallel mask-generator boundary

The minimum complete arbitrary-map mask generator is a reusable, rewritable
tile or cartridge with a parallel four-plane writer, positive fiducial/datum
registration, local clamp or controlled transport, per-cell verification,
bounded retry, and replaceable service media. A library of prepared masks,
disposable sheets, cassettes, or a queue of buffered masks may be useful
accessories, but none is a complete arbitrary-map generator by itself.

Operating principle: encode each five-level cell in four binary aperture
planes, write all planes during one addressed engagement, clamp the tile to
hard datums, read every changed state, and hold or quarantine the tile if
verification fails. A-010's planar cartridge is one possible mechanical
implementation; this architecture deliberately does not select its slider
geometry.

Analytical screen: at the existing conservative 71 cells/s/head and eight
head positions, full-field parallel write is 11.27 s. Adding 0.05 s map
processing, 1.50 s transport/register, 5.864 s full-field verification,
0.50 s settling, and 1.00 s retry allowance gives 20.18 s. A 5 x 5 local
update is 0.72 s with local clamp, or 1.72 s if it pays the full transport
allowance. These are inherited calculations and assumptions, not measured
performance.

Strengths: arbitrary maps remain on-demand; no per-update sheet waste; local
updates avoid global reset; readback exposes silent wrong cells; reusable
tiles permit service and inventory control.

Failure modes: serialised plane writes miss the 30 s bound; fiducial error
causes map skew; a partially seated tile can pass a naive reader; media wear
or debris blocks apertures; one dead channel creates correlated wrong states;
clamp motion disturbs loaded terrain; repeated retries can exceed the bound.

Cheapest falsification: a final-pitch 5 x 5 four-plane coupon with two
fiducials, one writer per plane, fixed reader, loaded neighbours, and 1,000
adversarial write/verify cycles. Reject if any plane needs serial recovery,
registration margin is lost after reseat, verification cannot distinguish a
blocked aperture, or an adjacent loaded cell moves beyond the project
regional-isolation criterion.

Evidence boundary: analytical/CAD-derived only; no physical validation,
supplier commitment, or production-readiness claim.

## Current disposition

**HOLD for integration.** E-043 independently retains A-011 as the leading
arbitrary-map boundary candidate, while E-040/E-022/E-023 leave sourcing,
reader/actuator compatibility, and physical acceptance unresolved. The next
gate is the controlled E-018 coupon package: parallel four-plane engagement,
reseat registration, exact readback with blocked/wrong-plane rejection,
actuator/reader compatibility, and loaded-neighbour isolation. Until it
passes, do not procure or integrate A-011; DES-003/DES-004 remain the current
display baselines. A critical failure rejects A-011 for the 30 s mode.
