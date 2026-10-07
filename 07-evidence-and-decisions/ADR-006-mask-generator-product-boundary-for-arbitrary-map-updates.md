---
status: proposed
builds-on: [Q-010, E-017, A-011, ADR-005]
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

The purchased boundary starts from the $370 DES-003 shared-machine baseline,
then requires a real BOM for reusable media, clamp/fiducials, four writer
channels, verification, and service stock. No cost pass or supplier claim is
made; omitting these terms would repeat the product-boundary error this ADR
resolves.

## Rejected classes

Prepared masks and cassette inventories cannot represent an unanticipated
map without a generator. A serial consumable writer fails the 30 s bound and
adds recurring media, waste, feed, registration, and verification faults.
Buffered masks reduce expected wait only for known future maps; they do not
change worst-case arbitrary-map generation or eliminate inventory cost.

## Consequence and next owner/action

Do not expand detailed CAD or procurement until a coupon owner demonstrates
parallel write yield, reseat registration, reader discrimination, media wear,
and loaded-neighbour isolation. The next action is the 5 x 5 four-plane
coupon specified in E-017; the architecture/coupon owner should report
measurements separately from this analytical acceptance. Until then A-011 is
conditional and DES-003/DES-004 remain the display baselines.

## Rollback and verification

Rollback is deleting/reverting ADR-006, A-011, E-017 and the Q-010 update;
DES-002 through DES-005 and ADR-005 are unchanged. Reproduce the arithmetic
with `./repo check` and inspect E-017; no physical-performance claim follows.
