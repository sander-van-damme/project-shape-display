---
status: active
builds-on: [A-001, A-002, P-009]
---

What complete physical mask generator fits purchased cost and sustained arbitrary-map timing?

Answer (analytical, not physically validated): the minimum complete boundary
is a reusable rewritable tile/cartridge with parallel four-plane writing,
positive fiducial registration, local clamp or controlled transport,
per-cell readback, bounded retry, and serviceable replacement media. A
prepared mask, serial writer, cassette inventory, or buffered queue alone is
not an arbitrary-map generator because it either represents only a finite
prior map set or omits the on-demand write path.

Using the current 80 x 80 reference field and DES-003's conservative 71
cells/s/head with eight head positions, the parallel write term is 11.27 s.
Explicit processing, registration, verification, settling and retry terms
give a 20.18 s full-field analytical bound and 0.72 s for a locally clamped
5 x 5 update (1.72 s if full transport is required). A serial four-plane
writer is 360.6 s before overhead. These are calculations/CAD-derived
assumptions, not hardware performance.

The complete purchased-component cost is not yet closed: start from the
$370 DES-003 shared-machine baseline and add actual costs for reusable media,
clamp/fiducials, four writer channels, verification, and service stock.
Prepared-mask, cassette-only, and buffer-only cost claims are rejected as
incomplete; serial consumables are rejected for the 30 s mode. See E-017 and
ADR-006 for the full accounting and falsification coupon.

Compare reusable, consumable, cassette and buffered media. Count writer channels, consumables, transport, registration, verification, faults and unexpected regional map latency. Do not treat a prepared mask or a serial writer as free outside machinery.
