---
status: proposed
builds-on: [Q-010, E-017, A-011, ADR-005, E-022]
---

# ADR-006: minimum complete mask-generator boundary

## Decision

Close Q-010's product-boundary uncertainty analytically: retain only a
reusable rewritable mask medium with parallel four-plane writing, positive
registration, transport or local clamping, per-cell verification, bounded
retry, and serviceable replacement media as a complete arbitrary-map
architecture. Keep prepared-mask, consumable-serial, cassette-only, and
buffer-only approaches as noncompetitive modes/accessories, not substitutes.

## Basis

The current conservative rate anchor gives 11.27 s to write 6,400 cells with
eight parallel head positions at 71 cells/s/head. Adding explicit map,
registration, verification, settling, and retry terms gives a 20.18 s
analytical full-field bound. A serial writer needs at least 90.1 s for one
state code and 360.6 s for four binary planes. The surviving regional bound
is 0.72 s for a locally clamped 5 x 5 tile, or 1.72 s if full transport is
needed. These values are calculations, not hardware validation.

The purchased boundary starts from the separate $370 DES-003 shared-machine
baseline, then requires a BOM for reusable media, clamp/fiducials, four
writer channels, verification, and service stock. E-022 bounds the complete
boundary at $486.29–$872.29 when inherited reader heads pass compatibility,
or $505.59–$921.59 when the explicit QRE1113/ADC/carrier fallback is needed.
The fallback reader stack is an alternative, not an addition to the reuse
case. These are allowances and catalogue observations, not supplier quotes;
the $370 baseline is not itself the complete-boundary cost.

The remaining cost risks are medium/media life, clamp and fiducial fit,
actuator force/stroke/life, reader compatibility and carrier if needed,
harness interface, and cleaning/service stock. No cost pass, procurement
commitment, or hardware validation follows from this analytical screen.

## Rejected classes

Prepared masks and cassette inventories cannot represent an unanticipated
map without a generator. A serial consumable writer fails the 30 s bound and
adds recurring media, waste, feed, registration, and verification faults.
Buffered masks reduce expected wait only for known future maps; they do not
change worst-case arbitrary-map generation or eliminate inventory cost.

## Consequence and next owner/action

Do not expand detailed CAD or procurement until the coupon owner measures
parallel write yield, reseat registration, reader discrimination, media wear,
and loaded-neighbour isolation. First run the E-022 falsification screen:
request a drawing-level quote for five cut/debur media planes, one
clamp/fiducial set, and four writer actuators, and measure the eight DES-003
reader heads against the E-018 coupon optical stack. Include material,
thickness, aperture process, force/stroke, life, tolerances, MOQ, lead time,
packaging, freight, and delivered price. Report physical measurements
separately from this analytical acceptance. Until then A-011 is conditional
and DES-003/DES-004 remain the display baselines.

## Rollback and verification

Rollback is deleting/reverting ADR-006, A-011, E-017 and the Q-010 update;
DES-002 through DES-005 and ADR-005 remain historical comparison records.
Reproduce the arithmetic with `./repo check` and inspect E-017/E-022; no
physical-performance claim follows.
